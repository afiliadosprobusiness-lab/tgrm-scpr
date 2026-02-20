from __future__ import annotations

import asyncio
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from flask import Flask, Response, jsonify, render_template, request, send_file

from .config import load_app_config, load_telegram_settings
from .exporters import export_messages
from .scraper import ScrapeSummary, TelegramScraper
from .storage import Storage
from .telegram_client import TelegramClientManager
from .utils import setup_logging


def _build_paths(
    config_path: Path | None,
    db_path: Path | None,
    env_path: Path | None,
    log_path: Path | None,
) -> dict[str, Path]:
    project_root = Path(__file__).resolve().parent.parent

    def normalize_path(raw_path: str | Path) -> Path:
        value = Path(raw_path)
        if value.is_absolute():
            return value
        return (project_root / value).resolve()

    is_vercel = bool(os.getenv("VERCEL"))
    vercel_default_db = Path("/tmp/telegram_scraper.db") if is_vercel else Path("data/telegram_scraper.db")
    vercel_default_log = Path("/tmp/app.log") if is_vercel else Path("logs/app.log")
    vercel_default_exports = Path("/tmp/exports") if is_vercel else Path("exports")
    return {
        "config_path": normalize_path(os.getenv("SCRAPER_CONFIG_PATH", str(config_path or "config.json"))),
        "db_path": normalize_path(os.getenv("SCRAPER_DB_PATH", str(db_path or vercel_default_db))),
        "env_path": normalize_path(os.getenv("SCRAPER_ENV_FILE", str(env_path or ".env"))),
        "log_path": normalize_path(os.getenv("SCRAPER_LOG_FILE", str(log_path or vercel_default_log))),
        "exports_dir": normalize_path(os.getenv("SCRAPER_EXPORTS_PATH", str(vercel_default_exports))),
        "manual_path": normalize_path(os.getenv("SCRAPER_MANUAL_PATH", "docs/MANUAL.md")),
    }


def create_app(
    *,
    config_path: Path | None = None,
    db_path: Path | None = None,
    env_path: Path | None = None,
    log_path: Path | None = None,
) -> Flask:
    app = Flask(__name__, template_folder="templates", static_folder="static")
    paths = _build_paths(config_path=config_path, db_path=db_path, env_path=env_path, log_path=log_path)
    app.config.update(paths)
    app.secret_key = os.getenv("FLASK_SECRET_KEY", "change-this-secret-key")

    logger = setup_logging(paths["log_path"])
    app.config["logger"] = logger

    @app.get("/")
    def dashboard():
        return render_template("dashboard.html", **_build_dashboard_view(app))

    @app.post("/scrape")
    def run_scrape():
        target = (request.form.get("target") or "").strip() or None
        backfill = bool(request.form.get("backfill"))
        dry_run = bool(request.form.get("dry_run"))

        try:
            summary = asyncio.run(
                _execute_scrape(
                    app=app,
                    target=target,
                    backfill=backfill,
                    dry_run=dry_run,
                )
            )
            return render_template(
                "dashboard.html",
                **_build_dashboard_view(app),
                scrape_summary=summary,
                scrape_error=None,
            )
        except Exception as exc:
            return render_template(
                "dashboard.html",
                **_build_dashboard_view(app),
                scrape_summary=None,
                scrape_error=str(exc),
            )

    @app.post("/export")
    def run_export():
        output_format = (request.form.get("format") or "csv").strip().lower()
        if output_format not in {"csv", "json"}:
            output_format = "csv"

        timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
        output_path = app.config["exports_dir"] / f"messages_{timestamp}.{output_format}"
        output_path.parent.mkdir(parents=True, exist_ok=True)

        with _open_storage(app) as storage:
            count = export_messages(storage, output_format, output_path)

        logger.info(
            "Web export complete",
            extra={
                "event": "web.export.complete",
                "format": output_format,
                "rows": count,
                "path": str(output_path),
            },
        )
        return send_file(output_path, as_attachment=True, download_name=output_path.name)

    @app.get("/health")
    def health():
        return jsonify({"status": "ok"})

    @app.get("/manual")
    def manual():
        manual_path: Path = app.config["manual_path"]
        if manual_path.exists():
            return send_file(manual_path, mimetype="text/markdown; charset=utf-8")
        return Response("Manual not found.", status=404)

    @app.get("/favicon.ico")
    def favicon():
        return Response(status=204)

    @app.get("/api/stats")
    def api_stats():
        with _open_storage(app) as storage:
            target_rows = storage.get_target_stats()
            runs = storage.get_recent_runs(limit=10)
        return jsonify({"targets": target_rows, "runs": runs})

    return app


def _build_dashboard_view(app: Flask) -> dict[str, Any]:
    config_error = None
    target_config: list[str] = []
    try:
        app_config = load_app_config(app.config["config_path"])
        target_config = app_config.targets
    except Exception as exc:
        config_error = str(exc)

    with _open_storage(app) as storage:
        target_rows = storage.get_target_stats()
        runs = storage.get_recent_runs(limit=8)

    total_messages = sum(int(item.get("total_messages") or 0) for item in target_rows)
    return {
        "db_path": str(app.config["db_path"]),
        "config_path": str(app.config["config_path"]),
        "env_path": str(app.config["env_path"]),
        "config_targets": target_config,
        "config_error": config_error,
        "target_rows": target_rows,
        "recent_runs": runs,
        "total_targets": len(target_rows),
        "total_messages": total_messages,
        "scrape_summary": None,
        "scrape_error": None,
    }


def _open_storage(app: Flask) -> Storage:
    storage = Storage(app.config["db_path"])
    storage.init_db()
    return storage


async def _execute_scrape(
    *,
    app: Flask,
    target: str | None,
    backfill: bool,
    dry_run: bool,
) -> ScrapeSummary:
    config_path: Path = app.config["config_path"]
    env_path: Path = app.config["env_path"]
    logger = app.config["logger"]

    app_config = load_app_config(config_path)
    telegram_settings = load_telegram_settings(env_path if env_path.exists() else None)

    storage = _open_storage(app)
    client_manager = TelegramClientManager(telegram_settings)
    try:
        await client_manager.connect()
        scraper = TelegramScraper(
            client_manager=client_manager,
            storage=storage,
            app_config=app_config,
            logger=logger,
        )
        summary = await scraper.run(target_filter=target, backfill=backfill, dry_run=dry_run)
        storage.insert_scrape_run(summary.to_record())
        return summary
    finally:
        await client_manager.disconnect()
        storage.close()
