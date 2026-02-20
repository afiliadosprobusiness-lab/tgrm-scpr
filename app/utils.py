from __future__ import annotations

import asyncio
import json
import logging
import random
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any


RESERVED_LOG_RECORD_FIELDS = {
    "name",
    "msg",
    "args",
    "levelname",
    "levelno",
    "pathname",
    "filename",
    "module",
    "exc_info",
    "exc_text",
    "stack_info",
    "lineno",
    "funcName",
    "created",
    "msecs",
    "relativeCreated",
    "thread",
    "threadName",
    "processName",
    "process",
    "message",
    "asctime",
}


class JsonLogFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        payload: dict[str, Any] = {
            "ts_utc": datetime.now(timezone.utc).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
        }
        for key, value in record.__dict__.items():
            if key not in RESERVED_LOG_RECORD_FIELDS and not key.startswith("_"):
                payload[key] = value
        if record.exc_info:
            payload["exception"] = self.formatException(record.exc_info)
        return json.dumps(payload, ensure_ascii=True)


def setup_logging(log_file: Path, level: int = logging.INFO) -> logging.Logger:
    log_file.parent.mkdir(parents=True, exist_ok=True)

    root_logger = logging.getLogger()
    root_logger.handlers.clear()
    root_logger.setLevel(level)

    formatter = JsonLogFormatter()

    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(level)
    stream_handler.setFormatter(formatter)

    file_handler = logging.FileHandler(log_file, encoding="utf-8")
    file_handler.setLevel(level)
    file_handler.setFormatter(formatter)

    root_logger.addHandler(stream_handler)
    root_logger.addHandler(file_handler)
    return logging.getLogger("app")


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def utc_datetime_from_days_ago(days: int | None) -> datetime | None:
    if days is None:
        return None
    return datetime.now(timezone.utc) - timedelta(days=days)


def calculate_backoff_seconds(
    attempt: int, base_seconds: float = 1.0, cap_seconds: float = 60.0
) -> float:
    exp = min(cap_seconds, base_seconds * (2 ** max(0, attempt - 1)))
    jitter = random.uniform(0.0, exp * 0.25)
    return exp + jitter


async def async_random_sleep(min_ms: int, max_ms: int) -> None:
    if max_ms <= 0:
        return
    value_ms = min_ms if min_ms == max_ms else random.randint(min_ms, max_ms)
    await asyncio.sleep(max(0, value_ms) / 1000.0)


def random_jitter_seconds(min_seconds: float = 0.5, max_seconds: float = 2.0) -> float:
    return random.uniform(min_seconds, max_seconds)


def serialize_entities(message: Any) -> str:
    entities = []
    content = getattr(message, "message", "") or ""
    for entity in getattr(message, "entities", []) or []:
        item: dict[str, Any] = {"type": entity.__class__.__name__}

        offset = getattr(entity, "offset", None)
        length = getattr(entity, "length", None)
        if offset is not None:
            item["offset"] = offset
        if length is not None:
            item["length"] = length
        if offset is not None and length is not None:
            item["text"] = content[offset : offset + length]

        for attr in ("url", "user_id", "language"):
            value = getattr(entity, attr, None)
            if value is not None:
                item[attr] = value

        entities.append(item)

    return json.dumps(entities, ensure_ascii=False)


def extract_media_payload(message: Any, include_metadata: bool) -> tuple[str | None, str | None]:
    media = getattr(message, "media", None)
    if media is None:
        return None, None

    media_type = media.__class__.__name__
    if not include_metadata:
        return media_type, None

    metadata: dict[str, Any] = {}
    file_obj = getattr(message, "file", None)
    if file_obj is not None:
        for attr in ("size", "mime_type", "name", "ext", "duration", "width", "height"):
            value = getattr(file_obj, attr, None)
            if value is not None:
                metadata[attr] = value

    if not metadata:
        metadata["hint"] = "No direct file metadata available."

    return media_type, json.dumps(metadata, ensure_ascii=False)


def ensure_timezone_aware(dt: datetime | None) -> datetime | None:
    if dt is None:
        return None
    if dt.tzinfo is None:
        return dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc)
