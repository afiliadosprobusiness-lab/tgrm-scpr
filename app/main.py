from __future__ import annotations

import argparse
import asyncio
import os
from pathlib import Path

from .config import load_app_config, load_telegram_settings
from .exporters import export_messages
from .storage import Storage
from .utils import setup_logging


def _default_path(env_name: str, fallback: str) -> str:
    env_value = os.getenv(env_name)
    if env_value:
        return env_value
    if os.getenv("VERCEL") and fallback.startswith("data/"):
        return "/tmp/telegram_scraper.db"
    return fallback


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="python -m app",
        description="Telegram Group/Channel Scraper (Telethon + SQLite).",
    )
    parser.add_argument(
        "--config",
        default=_default_path("SCRAPER_CONFIG_PATH", "config.json"),
        help="Path to scraper config JSON file (default: config.json).",
    )
    parser.add_argument(
        "--db",
        default=_default_path("SCRAPER_DB_PATH", "data/telegram_scraper.db"),
        help="Path to SQLite DB (default: data/telegram_scraper.db).",
    )
    parser.add_argument(
        "--env-file",
        default=_default_path("SCRAPER_ENV_FILE", ".env"),
        help="Path to .env file (default: .env).",
    )
    parser.add_argument(
        "--log-file",
        default=_default_path("SCRAPER_LOG_FILE", "logs/app.log"),
        help="Path to app log file (default: logs/app.log).",
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("init-db", help="Initialize SQLite schema.")

    scrape_parser = subparsers.add_parser("scrape", help="Scrape configured targets.")
    scrape_parser.add_argument("--target", help="Scrape only one target (e.g. @channel).")
    scrape_parser.add_argument(
        "--backfill",
        action="store_true",
        help="Backfill historical messages up to limit_per_target.",
    )
    scrape_parser.add_argument(
        "--dry-run",
        action="store_true",
        help="List targets and last_message_id without scraping messages.",
    )

    export_parser = subparsers.add_parser("export", help="Export stored messages.")
    export_parser.add_argument("--format", required=True, choices=["csv", "json"])
    export_parser.add_argument("--out", required=True, help="Output file path.")

    subparsers.add_parser("stats", help="Show per-target stats and recent scrape runs.")

    web_parser = subparsers.add_parser("web", help="Run web dashboard.")
    web_parser.add_argument("--host", default="127.0.0.1", help="Bind host (default: 127.0.0.1).")
    web_parser.add_argument("--port", default=8000, type=int, help="Bind port (default: 8000).")
    web_parser.add_argument(
        "--debug",
        action="store_true",
        help="Enable Flask debug mode for local development.",
    )
    return parser


def main() -> int:
    parser = _build_parser()
    args = parser.parse_args()

    logger = setup_logging(Path(args.log_file))

    if args.command == "web":
        from .web import create_app

        app = create_app(
            config_path=Path(args.config),
            db_path=Path(args.db),
            env_path=Path(args.env_file),
            log_path=Path(args.log_file),
        )
        app.run(host=args.host, port=args.port, debug=bool(args.debug))
        return 0

    storage = Storage(Path(args.db))

    try:
        storage.init_db()

        if args.command == "init-db":
            print(f"DB initialized at: {Path(args.db).resolve()}")
            return 0

        if args.command == "export":
            count = export_messages(storage, args.format, Path(args.out))
            print(f"Exported {count} messages to: {Path(args.out).resolve()}")
            return 0

        if args.command == "stats":
            _print_stats(storage)
            return 0

        if args.command == "scrape":
            return asyncio.run(
                _run_scrape(
                    config_path=Path(args.config),
                    env_path=Path(args.env_file),
                    storage=storage,
                    logger=logger,
                    target=args.target,
                    backfill=bool(args.backfill),
                    dry_run=bool(args.dry_run),
                )
            )

        parser.print_help()
        return 1
    finally:
        storage.close()


def _print_stats(storage: Storage) -> None:
    target_rows = storage.get_target_stats()
    recent_runs = storage.get_recent_runs(limit=10)

    print("Targets:")
    if not target_rows:
        print("- No targets in DB yet.")
    else:
        for row in target_rows:
            print(
                "- "
                f"target_id={row['target_id']} "
                f"target={row.get('target_username') or row.get('title') or row.get('target_input')} "
                f"messages={row['total_messages']} "
                f"last_message_id={row.get('last_message_id') or 0} "
                f"last_scraped_at={row.get('last_scraped_at') or 'never'}"
            )

    print("\nRecent scrape runs:")
    if not recent_runs:
        print("- No scrape runs recorded.")
    else:
        for run in recent_runs:
            print(
                "- "
                f"id={run['id']} mode={run['mode']} "
                f"targets_ok={run['targets_ok']}/{run['targets_total']} "
                f"messages_new={run['messages_new']} flood_waits={run['flood_waits']} "
                f"finished_at={run['finished_at']}"
            )


async def _run_scrape(
    *,
    config_path: Path,
    env_path: Path,
    storage: Storage,
    logger,
    target: str | None,
    backfill: bool,
    dry_run: bool,
) -> int:
    from .scraper import TelegramScraper
    from .telegram_client import TelegramClientManager

    app_config = load_app_config(config_path)
    telegram_settings = load_telegram_settings(env_path if env_path.exists() else None)

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

        print("\nScrape summary:")
        print(f"- mode: {summary.mode}")
        print(f"- targets ok: {summary.targets_ok}/{summary.targets_total}")
        print(f"- targets failed: {summary.targets_failed}")
        print(f"- new messages: {summary.messages_new}")
        print(f"- flood waits: {summary.flood_waits}")
        print(f"- started_at: {summary.started_at}")
        print(f"- finished_at: {summary.finished_at}")

        if dry_run:
            print("\nDry run target state:")
            for item in summary.dry_run_items:
                name = item.resolved_username or item.resolved_title or item.input_target
                print(
                    "- "
                    f"target={item.input_target} "
                    f"resolved={name} "
                    f"target_id={item.resolved_target_id} "
                    f"last_message_id={item.last_message_id}"
                )

        return 0 if summary.targets_failed == 0 else 2
    finally:
        await client_manager.disconnect()
