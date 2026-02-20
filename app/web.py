from __future__ import annotations

import asyncio
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from flask import Flask, Response, jsonify, render_template, request, send_file

from .config import load_app_config, load_dotenv, load_telegram_settings
from .discovery import (
    DiscoveryService,
    SUPPORTED_DISCOVERY_SOURCES,
    get_ui_capabilities_with_runtime,
)
from .exporters import export_messages
from .sources.capabilities import get_source_capabilities
from .sources.models import DiscoveryFilters
from .scraper import ScrapeSummary, TelegramScraper
from .storage import Storage
from .telegram_client import TelegramClientManager
from .utils import setup_logging, utc_now_iso

DISABLED_DISCOVERY_SOURCES = {"instagram", "linkedin"}


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
    load_dotenv(paths["env_path"] if paths["env_path"].exists() else None, override=False)

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
            discovery_runs = storage.get_recent_discovery_runs(limit=10)
        return jsonify({"targets": target_rows, "runs": runs, "discovery_runs": discovery_runs})

    @app.get("/api/capabilities")
    def api_capabilities():
        return jsonify({"platforms": get_ui_capabilities_with_runtime()})

    @app.post("/api/discover")
    def api_discover():
        payload = request.get_json(silent=True) or {}
        source = str(payload.get("platform", "")).strip().lower()

        if source == "telegram":
            return (
                jsonify(
                    {
                        "status": "error",
                        "source": source,
                        "message": "Telegram discovery is not exposed in /api/discover. Use /scrape workflow.",
                    }
                ),
                400,
            )
        if source in DISABLED_DISCOVERY_SOURCES:
            return (
                jsonify(
                    {
                        "status": "error",
                        "source": source,
                        "message": (
                            f"{source.capitalize()} connector is disabled due platform restrictions on automated "
                            "data collection without explicit authorization."
                        ),
                    }
                ),
                400,
            )
        if source not in SUPPORTED_DISCOVERY_SOURCES:
            return jsonify({"status": "error", "message": f"Unsupported source: {source}"}), 400

        try:
            filters = DiscoveryFilters.from_payload(payload)
        except ValueError as exc:
            return jsonify({"status": "error", "source": source, "message": str(exc)}), 400

        credentials = _extract_credentials(payload)

        service = DiscoveryService(logger=app.config["logger"])
        records, summary, warnings, effective_filters = service.run(
            source=source,
            filters=filters,
            credentials=credentials,
        )

        with _open_storage(app) as storage:
            storage.upsert_source_records([item.to_storage_row() for item in records], utc_now_iso())
            storage.insert_discovery_run(summary.to_storage_row(effective_filters))
            latest = storage.get_source_records(source=source, limit=20)
            recent_runs = storage.get_recent_discovery_runs(source=source, limit=6)

        if summary.status != "ok":
            status_code = 400 if _is_client_error(summary.error_message or "") else 502
            return (
                jsonify(
                    {
                        "status": summary.status,
                        "source": source,
                        "count": 0,
                        "items": [],
                        "recent_runs": recent_runs,
                        "warnings": warnings,
                        "applied_filters": effective_filters.to_api_dict(),
                        "capabilities": get_source_capabilities(source),
                        "message": summary.error_message or "Discovery failed.",
                    }
                ),
                status_code,
            )

        return jsonify(
            {
                "status": summary.status,
                "source": source,
                "count": len(records),
                "items": [item.to_api_dict() for item in records],
                "stored_items": latest,
                "recent_runs": recent_runs,
                "warnings": warnings,
                "applied_filters": effective_filters.to_api_dict(),
                "capabilities": get_source_capabilities(source),
                "message": "Discovery completed.",
            }
        )

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


def _is_client_error(message: str) -> bool:
    normalized = message.strip().lower()
    if not normalized:
        return False
    prefixes = ("missing ", "unsupported source", "invalid ")
    if normalized.startswith(prefixes):
        return True
    fragments = (
        "requires a location",
        "must be",
        "one of:",
        "request_denied",
        "invalid key",
        "invalid_request",
        "unauthorized",
    )
    return any(fragment in normalized for fragment in fragments)


def _extract_credentials(payload: dict[str, Any]) -> dict[str, str]:
    raw = payload.get("credentials")
    if not isinstance(raw, dict):
        return {}
    clean_map: dict[str, str] = {}
    for key, value in raw.items():
        if value is None:
            continue
        text = str(value).strip()
        if not text:
            continue
        clean_map[str(key)] = text
    return clean_map
