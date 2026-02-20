from __future__ import annotations

import json
import os
from typing import Any

from .filter_utils import clean, location_text, passes_presence_filter, safe_float
from .http_utils import http_get_json
from .models import DiscoveryFilters, SourceRecord


FOURSQUARE_SEARCH_URL = "https://api.foursquare.com/v3/places/search"


class FoursquareSource:
    def __init__(self, api_key: str | None = None):
        self.api_key = api_key or os.getenv("FOURSQUARE_API_KEY")
        if not self.api_key:
            raise ValueError("Missing FOURSQUARE_API_KEY in environment.")

    def search(self, filters: DiscoveryFilters) -> list[SourceRecord]:
        query = filters.merged_query() or "business"
        params: dict[str, Any] = {
            "query": query,
            "limit": min(filters.limit, 50),
        }
        if filters.location:
            params["near"] = filters.location

        payload = http_get_json(
            url=FOURSQUARE_SEARCH_URL,
            params=params,
            headers={
                "Authorization": self.api_key,
                "Accept": "application/json",
            },
            retries=4,
        )
        results = payload.get("results") or []

        records: list[SourceRecord] = []
        for item in results:
            record = self._to_record(item=item, filters=filters)
            if record is None:
                continue
            records.append(record)
            if len(records) >= filters.limit:
                break
        return records

    def _to_record(self, *, item: dict[str, Any], filters: DiscoveryFilters) -> SourceRecord | None:
        fsq_id = clean(item.get("fsq_id"))
        name = clean(item.get("name"))
        if not fsq_id or not name:
            return None

        website = clean(item.get("website"))
        phone = clean(item.get("tel"))
        if not passes_presence_filter(filters.has_website, website):
            return None
        if not passes_presence_filter(filters.has_phone, phone):
            return None

        rating = safe_float(item.get("rating"))
        if rating is not None and rating < filters.min_rating:
            return None

        is_verified = bool(item.get("verified"))
        if filters.only_verified and not is_verified:
            return None

        categories = item.get("categories") or []
        category_names = [clean(category.get("name")) for category in categories if isinstance(category, dict)]
        description = ", ".join(value for value in category_names if value)

        return SourceRecord(
            source="foursquare",
            external_id=fsq_id,
            name=name,
            url=clean(item.get("link")) or f"https://foursquare.com/v/{fsq_id}",
            description=description or None,
            website=website,
            phone=phone,
            rating=rating,
            review_count=None,
            location=location_text(item.get("location")) or filters.location or None,
            niche=filters.niche,
            is_verified=is_verified,
            raw_json=json.dumps(item, ensure_ascii=False),
        )
