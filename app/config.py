from __future__ import annotations

import json
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

try:
    from dotenv import load_dotenv as _load_dotenv
except ImportError:
    _load_dotenv = None


@dataclass(frozen=True)
class TelegramSettings:
    api_id: int
    api_hash: str
    session_name: str
    string_session: str | None


@dataclass(frozen=True)
class ScrapeSettings:
    limit_per_target: int
    since_days: int | None
    sleep_min_ms: int
    sleep_max_ms: int
    include_media_metadata: bool
    batch_size: int
    max_retries: int


@dataclass(frozen=True)
class AppConfig:
    targets: list[str]
    scrape: ScrapeSettings
    source_path: Path


def _fallback_load_dotenv(env_path: Path | None, override: bool) -> None:
    candidates = [env_path] if env_path else [Path(".env")]
    for candidate in candidates:
        if candidate is None or not candidate.exists():
            continue

        for line in candidate.read_text(encoding="utf-8").splitlines():
            stripped = line.strip()
            if not stripped or stripped.startswith("#") or "=" not in stripped:
                continue
            key, value = stripped.split("=", 1)
            key = key.strip()
            value = value.strip().strip('"').strip("'")
            if not key:
                continue
            if key in os.environ and not override:
                continue
            os.environ[key] = value


def load_dotenv(env_path: Path | None = None, override: bool = False) -> None:
    if _load_dotenv is not None:
        if env_path is None:
            _load_dotenv(override=override)
        else:
            _load_dotenv(dotenv_path=env_path, override=override)
        return
    _fallback_load_dotenv(env_path, override=override)


def _as_int(value: Any, field_name: str) -> int:
    try:
        return int(value)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"Invalid integer for '{field_name}': {value!r}") from exc


def normalize_target(raw_target: str) -> str:
    target = (raw_target or "").strip()
    if not target:
        raise ValueError("Target cannot be empty.")

    if target.startswith(("http://", "https://")):
        parsed = urlparse(target)
        host = (parsed.netloc or "").lower()
        if host not in {"t.me", "telegram.me", "www.t.me", "www.telegram.me"}:
            raise ValueError(f"Unsupported target host: {host}")

        path_parts = [part for part in parsed.path.split("/") if part]
        if not path_parts:
            raise ValueError(f"Invalid Telegram target URL: {target}")

        first = path_parts[0]
        if first in {"joinchat"} or first.startswith("+"):
            raise ValueError(
                "Private invite links are not supported. Use public targets or targets "
                "where your account already has legitimate access."
            )

        if first == "s" and len(path_parts) >= 2:
            first = path_parts[1]

        return f"@{first.lstrip('@')}"

    if target.startswith("t.me/") or target.startswith("telegram.me/"):
        return normalize_target(f"https://{target}")

    if target.startswith("https://t.me/+") or target.startswith("t.me/+"):
        raise ValueError(
            "Private invite links are not supported. Use public targets or accessible chats."
        )

    if target.startswith("@"):
        username = target[1:]
        if not username:
            raise ValueError(f"Invalid target: {raw_target!r}")
        return f"@{username}"

    if "/" in target:
        raise ValueError(f"Invalid target format: {raw_target!r}")

    return f"@{target}"


def load_telegram_settings(env_path: Path | None = None) -> TelegramSettings:
    load_dotenv(env_path=env_path, override=False)

    api_id_raw = os.getenv("TELEGRAM_API_ID")
    api_hash = os.getenv("TELEGRAM_API_HASH")
    default_session = "/tmp/telegram_user_session" if os.getenv("VERCEL") else "telegram_user_session"
    session_name = os.getenv("TELEGRAM_SESSION_NAME", default_session)
    string_session = (os.getenv("TELEGRAM_STRING_SESSION") or "").strip() or None

    if not api_id_raw:
        raise ValueError("Missing TELEGRAM_API_ID in environment.")
    if not api_hash:
        raise ValueError("Missing TELEGRAM_API_HASH in environment.")

    api_id = _as_int(api_id_raw, "TELEGRAM_API_ID")
    if api_id <= 0:
        raise ValueError("TELEGRAM_API_ID must be greater than 0.")

    return TelegramSettings(
        api_id=api_id,
        api_hash=api_hash,
        session_name=session_name,
        string_session=string_session,
    )


def load_app_config(config_path: Path) -> AppConfig:
    if not config_path.exists():
        raise FileNotFoundError(f"Config file not found: {config_path}")

    raw = json.loads(config_path.read_text(encoding="utf-8"))
    targets_raw = raw.get("targets", [])
    if not isinstance(targets_raw, list):
        raise ValueError("'targets' must be a list.")

    seen: set[str] = set()
    targets: list[str] = []
    for raw_target in targets_raw:
        normalized = normalize_target(str(raw_target))
        if normalized not in seen:
            seen.add(normalized)
            targets.append(normalized)

    if not targets:
        raise ValueError("Config must include at least one target in 'targets'.")

    scrape_raw = raw.get("scrape", {})
    if not isinstance(scrape_raw, dict):
        raise ValueError("'scrape' must be an object.")

    limit_per_target = _as_int(scrape_raw.get("limit_per_target", 2000), "limit_per_target")
    sleep_min_ms = _as_int(scrape_raw.get("sleep_min_ms", 600), "sleep_min_ms")
    sleep_max_ms = _as_int(scrape_raw.get("sleep_max_ms", 1400), "sleep_max_ms")
    batch_size = _as_int(scrape_raw.get("batch_size", 200), "batch_size")
    max_retries = _as_int(scrape_raw.get("max_retries", 3), "max_retries")

    since_days_raw = scrape_raw.get("since_days")
    since_days = _as_int(since_days_raw, "since_days") if since_days_raw is not None else None

    include_media_metadata = bool(scrape_raw.get("include_media_metadata", False))

    if limit_per_target <= 0:
        raise ValueError("limit_per_target must be greater than 0.")
    if sleep_min_ms < 0 or sleep_max_ms < 0:
        raise ValueError("sleep_min_ms and sleep_max_ms must be >= 0.")
    if sleep_min_ms > sleep_max_ms:
        raise ValueError("sleep_min_ms cannot be greater than sleep_max_ms.")
    if since_days is not None and since_days <= 0:
        raise ValueError("since_days must be greater than 0 when provided.")
    if batch_size <= 0:
        raise ValueError("batch_size must be greater than 0.")
    if max_retries <= 0:
        raise ValueError("max_retries must be greater than 0.")

    scrape = ScrapeSettings(
        limit_per_target=limit_per_target,
        since_days=since_days,
        sleep_min_ms=sleep_min_ms,
        sleep_max_ms=sleep_max_ms,
        include_media_metadata=include_media_metadata,
        batch_size=batch_size,
        max_retries=max_retries,
    )
    return AppConfig(targets=targets, scrape=scrape, source_path=config_path)
