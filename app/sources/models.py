from __future__ import annotations

from dataclasses import dataclass
from typing import Any


ALLOWED_BOOL_FILTERS = {"any", "yes", "no"}


@dataclass(frozen=True)
class DiscoveryFilters:
    query: str
    niche: str
    has_website: str
    has_phone: str
    location: str
    min_rating: float
    only_verified: bool
    limit: int

    @classmethod
    def from_payload(cls, payload: dict[str, Any]) -> "DiscoveryFilters":
        query = str(payload.get("query", "")).strip()
        niche = str(payload.get("niche", "all")).strip() or "all"
        has_website = str(payload.get("has_website", "any")).strip().lower() or "any"
        has_phone = str(payload.get("has_phone", "any")).strip().lower() or "any"
        location = str(payload.get("location", "")).strip()
        only_verified = bool(payload.get("only_verified", False))

        min_rating_raw = payload.get("min_rating", 0)
        try:
            min_rating = float(min_rating_raw)
        except (TypeError, ValueError) as exc:
            raise ValueError("min_rating must be a valid number.") from exc
        if min_rating < 0 or min_rating > 5:
            raise ValueError("min_rating must be between 0 and 5.")

        limit_raw = payload.get("limit", 20)
        try:
            limit = int(limit_raw)
        except (TypeError, ValueError) as exc:
            raise ValueError("limit must be a valid integer.") from exc
        if limit <= 0:
            raise ValueError("limit must be greater than 0.")
        limit = min(limit, 100)

        if has_website not in ALLOWED_BOOL_FILTERS:
            raise ValueError("has_website must be one of: any, yes, no.")
        if has_phone not in ALLOWED_BOOL_FILTERS:
            raise ValueError("has_phone must be one of: any, yes, no.")

        return cls(
            query=query,
            niche=niche,
            has_website=has_website,
            has_phone=has_phone,
            location=location,
            min_rating=min_rating,
            only_verified=only_verified,
            limit=limit,
        )

    def merged_query(self) -> str:
        parts = [self.query]
        if self.niche and self.niche != "all":
            parts.append(self.niche.replace("_", " "))
        if self.location:
            parts.append(self.location)
        merged = " ".join(item.strip() for item in parts if item and item.strip())
        return merged.strip()

    def to_api_dict(self) -> dict[str, Any]:
        return {
            "query": self.query,
            "niche": self.niche,
            "has_website": self.has_website,
            "has_phone": self.has_phone,
            "location": self.location,
            "min_rating": self.min_rating,
            "only_verified": self.only_verified,
            "limit": self.limit,
        }


@dataclass(frozen=True)
class SourceRecord:
    source: str
    external_id: str
    name: str
    url: str | None
    description: str | None
    website: str | None
    phone: str | None
    rating: float | None
    review_count: int | None
    location: str | None
    niche: str | None
    is_verified: bool
    raw_json: str

    def to_storage_row(self) -> dict[str, Any]:
        return {
            "source": self.source,
            "external_id": self.external_id,
            "name": self.name,
            "url": self.url,
            "description": self.description,
            "website": self.website,
            "phone": self.phone,
            "rating": self.rating,
            "review_count": self.review_count,
            "location": self.location,
            "niche": self.niche,
            "is_verified": 1 if self.is_verified else 0,
            "raw_json": self.raw_json,
        }

    def to_api_dict(self) -> dict[str, Any]:
        return {
            "source": self.source,
            "external_id": self.external_id,
            "name": self.name,
            "url": self.url,
            "description": self.description,
            "website": self.website,
            "phone": self.phone,
            "rating": self.rating,
            "review_count": self.review_count,
            "location": self.location,
            "niche": self.niche,
            "is_verified": self.is_verified,
        }
