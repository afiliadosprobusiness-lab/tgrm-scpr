from __future__ import annotations

import asyncio
import logging
from dataclasses import asdict, dataclass, field
from datetime import datetime, timedelta, timezone
from typing import Any

from telethon.errors import FloodWaitError, RPCError

from .config import AppConfig, normalize_target
from .storage import Storage
from .telegram_client import TelegramClientManager, ResolvedTarget
from .utils import (
    async_random_sleep,
    calculate_backoff_seconds,
    ensure_timezone_aware,
    extract_media_payload,
    random_jitter_seconds,
    serialize_entities,
    utc_now_iso,
)


@dataclass
class DryRunItem:
    input_target: str
    resolved_target_id: int
    resolved_username: str | None
    resolved_title: str | None
    last_message_id: int


@dataclass
class ScrapeSummary:
    started_at: str
    finished_at: str | None = None
    mode: str = "incremental"
    target_filter: str | None = None
    targets_total: int = 0
    targets_ok: int = 0
    targets_failed: int = 0
    messages_new: int = 0
    flood_waits: int = 0
    error_count: int = 0
    dry_run_items: list[DryRunItem] = field(default_factory=list)

    def to_record(self) -> dict[str, Any]:
        payload = asdict(self)
        payload.pop("dry_run_items", None)
        payload["finished_at"] = self.finished_at or utc_now_iso()
        return payload


class TelegramScraper:
    def __init__(
        self,
        *,
        client_manager: TelegramClientManager,
        storage: Storage,
        app_config: AppConfig,
        logger: logging.Logger,
    ):
        self.client_manager = client_manager
        self.storage = storage
        self.app_config = app_config
        self.logger = logger

    async def run(
        self,
        *,
        target_filter: str | None = None,
        backfill: bool = False,
        dry_run: bool = False,
    ) -> ScrapeSummary:
        mode = "dry-run"
        if not dry_run:
            mode = "backfill" if backfill else "incremental"

        summary = ScrapeSummary(
            started_at=utc_now_iso(),
            mode=mode,
            target_filter=normalize_target(target_filter) if target_filter else None,
        )

        selected_targets = self._select_targets(target_filter=target_filter)
        summary.targets_total = len(selected_targets)

        for index, target in enumerate(selected_targets, start=1):
            self.logger.info(
                "Processing target",
                extra={"event": "target.start", "target": target, "index": index, "total": len(selected_targets)},
            )
            try:
                resolved = await self.client_manager.resolve_target(target)
                self.storage.upsert_target(
                    target_id=resolved.target_id,
                    target_input=resolved.target_input,
                    target_username=resolved.target_username,
                    title=resolved.title,
                    now_utc=utc_now_iso(),
                )
                last_message_id = self.storage.get_last_message_id(resolved.target_id)

                if dry_run:
                    dry_item = DryRunItem(
                        input_target=target,
                        resolved_target_id=resolved.target_id,
                        resolved_username=resolved.target_username,
                        resolved_title=resolved.title,
                        last_message_id=last_message_id,
                    )
                    summary.dry_run_items.append(dry_item)
                    summary.targets_ok += 1
                    self.logger.info(
                        "Dry run target resolved",
                        extra={
                            "event": "target.dry_run",
                            "target": target,
                            "target_id": resolved.target_id,
                            "last_message_id": last_message_id,
                        },
                    )
                else:
                    new_messages, highest_message_id, flood_waits = await self._scrape_target(
                        resolved=resolved,
                        last_message_id=last_message_id,
                        backfill=backfill,
                    )
                    summary.messages_new += new_messages
                    summary.flood_waits += flood_waits
                    summary.targets_ok += 1
                    self.storage.update_last_message_id(
                        resolved.target_id,
                        highest_message_id if highest_message_id else last_message_id,
                        utc_now_iso(),
                    )

                    self.logger.info(
                        "Target scrape complete",
                        extra={
                            "event": "target.complete",
                            "target": target,
                            "target_id": resolved.target_id,
                            "new_messages": new_messages,
                            "highest_message_id": highest_message_id,
                        },
                    )
            except Exception:
                summary.targets_failed += 1
                summary.error_count += 1
                self.logger.exception(
                    "Target processing failed",
                    extra={"event": "target.error", "target": target},
                )

            if index < len(selected_targets):
                await async_random_sleep(
                    self.app_config.scrape.sleep_min_ms,
                    self.app_config.scrape.sleep_max_ms,
                )

        summary.finished_at = utc_now_iso()
        return summary

    def _select_targets(self, target_filter: str | None) -> list[str]:
        if not target_filter:
            return list(self.app_config.targets)
        normalized = normalize_target(target_filter)
        return [normalized]

    async def _scrape_target(
        self,
        *,
        resolved: ResolvedTarget,
        last_message_id: int,
        backfill: bool,
    ) -> tuple[int, int, int]:
        scrape_settings = self.app_config.scrape
        since_cutoff = (
            datetime.now(timezone.utc) - timedelta(days=scrape_settings.since_days)
            if scrape_settings.since_days
            else None
        )

        sender_cache: dict[int, str | None] = {}
        highest_message_id = last_message_id
        new_messages = 0
        flood_waits = 0
        processed = 0

        remaining = scrape_settings.limit_per_target
        cursor_id = 0 if backfill else last_message_id
        stop_requested = False

        while remaining > 0 and not stop_requested:
            batch_limit = min(scrape_settings.batch_size, remaining)
            batch, flood_in_batch = await self._fetch_batch(
                entity=resolved.entity,
                batch_limit=batch_limit,
                backfill=backfill,
                cursor_id=cursor_id,
            )
            flood_waits += flood_in_batch

            if not batch:
                break

            for message in batch:
                message_id = int(getattr(message, "id", 0) or 0)
                if message_id <= 0:
                    continue

                if not backfill and message_id <= last_message_id:
                    continue

                message_date = ensure_timezone_aware(getattr(message, "date", None))
                if since_cutoff and message_date and message_date < since_cutoff:
                    if backfill:
                        stop_requested = True
                        break
                    continue

                sender_id = getattr(message, "sender_id", None)
                sender_username = await self._resolve_sender_username(
                    message=message,
                    sender_id=sender_id,
                    cache=sender_cache,
                )
                reply_to_msg_id = None
                reply_to = getattr(message, "reply_to", None)
                if reply_to is not None:
                    reply_to_msg_id = getattr(reply_to, "reply_to_msg_id", None)

                media_type, media_metadata_json = extract_media_payload(
                    message,
                    scrape_settings.include_media_metadata,
                )
                row = {
                    "target_id": resolved.target_id,
                    "target_username": resolved.target_username,
                    "message_id": message_id,
                    "date_utc": message_date.isoformat() if message_date else "",
                    "sender_id": sender_id,
                    "sender_username": sender_username,
                    "text": getattr(message, "message", None),
                    "entities_json": serialize_entities(message),
                    "views": getattr(message, "views", None),
                    "forwards": getattr(message, "forwards", None),
                    "reply_to_msg_id": reply_to_msg_id,
                    "media_type": media_type,
                    "media_metadata_json": media_metadata_json,
                    "scraped_at": utc_now_iso(),
                }
                inserted = self.storage.insert_message(row)
                if inserted:
                    new_messages += 1
                    if message_id > highest_message_id:
                        highest_message_id = message_id

                processed += 1

            if backfill:
                cursor_id = int(getattr(batch[-1], "id", cursor_id) or cursor_id)
            else:
                cursor_id = max(cursor_id, int(getattr(batch[-1], "id", cursor_id) or cursor_id))

            remaining -= len(batch)
            if len(batch) < batch_limit:
                break

            await async_random_sleep(scrape_settings.sleep_min_ms, scrape_settings.sleep_max_ms)

        self.logger.info(
            "Target message loop completed",
            extra={
                "event": "target.messages_done",
                "target_id": resolved.target_id,
                "processed": processed,
                "inserted": new_messages,
                "highest_message_id": highest_message_id,
            },
        )
        return new_messages, highest_message_id, flood_waits

    async def _fetch_batch(
        self,
        *,
        entity: Any,
        batch_limit: int,
        backfill: bool,
        cursor_id: int,
    ) -> tuple[list[Any], int]:
        retries = self.app_config.scrape.max_retries
        flood_waits = 0
        rpc_attempt = 0

        while True:
            try:
                if backfill:
                    batch = [
                        message
                        async for message in self.client_manager.client.iter_messages(
                            entity,
                            limit=batch_limit,
                            offset_id=cursor_id,
                            reverse=False,
                        )
                    ]
                else:
                    batch = [
                        message
                        async for message in self.client_manager.client.iter_messages(
                            entity,
                            limit=batch_limit,
                            min_id=cursor_id,
                            reverse=True,
                        )
                    ]
                return batch, flood_waits
            except FloodWaitError as exc:
                flood_waits += 1
                wait_seconds = float(getattr(exc, "seconds", 1)) + random_jitter_seconds()
                self.logger.error(
                    "FloodWait encountered. Sleeping.",
                    extra={
                        "event": "telegram.flood_wait",
                        "sleep_seconds": wait_seconds,
                        "attempt": rpc_attempt + 1,
                    },
                )
                await asyncio.sleep(wait_seconds)
            except (RPCError, OSError):
                rpc_attempt += 1
                if rpc_attempt >= retries:
                    raise
                backoff = calculate_backoff_seconds(attempt=rpc_attempt)
                self.logger.error(
                    "Telegram fetch failed. Retrying with backoff.",
                    extra={"event": "telegram.retry", "attempt": rpc_attempt, "sleep_seconds": backoff},
                )
                await asyncio.sleep(backoff)

    async def _resolve_sender_username(
        self,
        *,
        message: Any,
        sender_id: int | None,
        cache: dict[int, str | None],
    ) -> str | None:
        if sender_id is None:
            return None

        if sender_id in cache:
            return cache[sender_id]

        sender_username = None
        try:
            sender = await message.get_sender()
            sender_username = getattr(sender, "username", None) if sender else None
        except Exception:
            sender_username = None

        cache[sender_id] = sender_username
        return sender_username
