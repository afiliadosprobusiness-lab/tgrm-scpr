from __future__ import annotations

from dataclasses import dataclass, replace
from typing import Any

from .sources.capabilities import (
    get_platform_capabilities,
    get_platform_capabilities_with_runtime,
    get_source_capabilities,
)
from .sources.google_maps_source import GoogleMapsSource
from .sources.models import DiscoveryFilters, SourceRecord
from .sources.reddit_source import RedditSource
from .utils import utc_now_iso


SUPPORTED_DISCOVERY_SOURCES = {
    "google_maps",
    "reddit",
}


@dataclass(frozen=True)
class DiscoverySummary:
    source: str
    started_at: str
    finished_at: str
    result_count: int
    status: str
    error_message: str | None

    def to_storage_row(self, filters: DiscoveryFilters) -> dict[str, Any]:
        return {
            "source": self.source,
            "started_at": self.started_at,
            "finished_at": self.finished_at,
            "query": filters.query,
            "niche": filters.niche,
            "has_website": filters.has_website,
            "has_phone": filters.has_phone,
            "location": filters.location,
            "min_rating": filters.min_rating,
            "only_verified": 1 if filters.only_verified else 0,
            "limit_value": filters.limit,
            "result_count": self.result_count,
            "status": self.status,
            "error_message": self.error_message,
        }


class DiscoveryService:
    def __init__(self, logger):
        self.logger = logger

    def run(
        self, *, source: str, filters: DiscoveryFilters, credentials: dict[str, str] | None = None
    ) -> tuple[list[SourceRecord], DiscoverySummary, list[str], DiscoveryFilters]:
        started_at = utc_now_iso()
        records: list[SourceRecord] = []
        status = "ok"
        error_message = None
        warnings: list[str] = []
        effective_filters = filters

        try:
            effective_filters, warnings = _normalize_filters(source=source, filters=filters)
            records = _resolve_source_client(source, credentials=credentials).search(effective_filters)
        except Exception as exc:
            status = "error"
            error_message = str(exc)
            normalized_error = error_message.strip().lower()
            expected_error_fragments = (
                "missing ",
                "requires a location",
                "request_denied",
                "invalid key",
                "invalid_request",
                "unauthorized",
                "blocked in this runtime",
                "oauth authentication failed",
            )
            if normalized_error.startswith("missing ") or any(
                fragment in normalized_error for fragment in expected_error_fragments
            ):
                self.logger.error(
                    "Discovery validation/configuration error",
                    extra={"event": "discovery.validation_error", "source": source, "config_error": error_message},
                )
            else:
                self.logger.exception(
                    "Discovery execution failed",
                    extra={"event": "discovery.error", "source": source},
                )

        summary = DiscoverySummary(
            source=source,
            started_at=started_at,
            finished_at=utc_now_iso(),
            result_count=len(records),
            status=status,
            error_message=error_message,
        )
        return records, summary, warnings, effective_filters


def get_ui_capabilities() -> dict[str, dict[str, Any]]:
    return get_platform_capabilities()


def get_ui_capabilities_with_runtime() -> dict[str, dict[str, Any]]:
    return get_platform_capabilities_with_runtime()


def _resolve_source_client(source: str, credentials: dict[str, str] | None = None):
    credential_data = credentials or {}

    if source == "google_maps":
        return GoogleMapsSource(api_key=_get_credential(credential_data, "api_key"))
    if source == "reddit":
        return RedditSource(
            user_agent=_get_credential(credential_data, "user_agent"),
            client_id=_get_credential(credential_data, "client_id"),
            client_secret=_get_credential(credential_data, "client_secret"),
        )
    raise ValueError(f"Unsupported source: {source}")


def _normalize_filters(source: str, filters: DiscoveryFilters) -> tuple[DiscoveryFilters, list[str]]:
    capabilities = get_source_capabilities(source)
    warnings: list[str] = []
    normalized = filters

    if capabilities.get("requires_location") and not filters.location:
        raise ValueError(f"{source} discovery requires a location.")

    if not capabilities.get("supports_rating_filter") and filters.min_rating > 0:
        normalized = replace(normalized, min_rating=0.0)
        warnings.append("min_rating ignored by this source and reset to 0.")

    if not capabilities.get("supports_verified_filter") and filters.only_verified:
        normalized = replace(normalized, only_verified=False)
        warnings.append("only_verified ignored by this source and reset to false.")

    if not capabilities.get("supports_has_website_filter") and filters.has_website != "any":
        normalized = replace(normalized, has_website="any")
        warnings.append("has_website filter ignored by this source and reset to any.")

    if not capabilities.get("supports_has_phone_filter") and filters.has_phone != "any":
        normalized = replace(normalized, has_phone="any")
        warnings.append("has_phone filter ignored by this source and reset to any.")

    return normalized, warnings


def _get_credential(credentials: dict[str, str], key: str) -> str | None:
    raw = credentials.get(key)
    if raw is None:
        return None
    value = str(raw).strip()
    return value or None
