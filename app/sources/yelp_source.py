from __future__ import annotations

import json
import os
from typing import Any

from .filter_utils import clean, passes_presence_filter, safe_float, safe_int
from .http_utils import http_get_json
from .models import DiscoveryFilters, SourceRecord


YELP_SEARCH_URL = "https://api.yelp.com/v3/businesses/search"


class YelpSource:
    def __init__(self, api_key: str | None = None):
        self.api_key = api_key or os.getenv("YELP_API_KEY")
        if not self.api_key:
            raise ValueError("Missing YELP_API_KEY in environment.")

    def search(self, filters: DiscoveryFilters) -> list[SourceRecord]:
        if not filters.location:
            raise ValueError("Yelp discovery requires a location.")

        query = filters.query or (filters.niche.replace("_", " ") if filters.niche != "all" else "business")
        payload = http_get_json(
            url=YELP_SEARCH_URL,
            params={
                "term": query,
                "location": filters.location,
                "limit": min(filters.limit, 50),
                "sort_by": "best_match",
            },
            headers={"Authorization": f"Bearer {self.api_key}"},
            retries=4,
        )
        results = payload.get("businesses") or []

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
        external_id = clean(item.get("id"))
        name = clean(item.get("name"))
        if not external_id or not name:
            return None

        website = clean(item.get("url"))
        phone = clean(item.get("display_phone")) or clean(item.get("phone"))
        if not passes_presence_filter(filters.has_website, website):
            return None
        if not passes_presence_filter(filters.has_phone, phone):
            return None

        rating = safe_float(item.get("rating"))
        if rating is not None and rating < filters.min_rating:
            return None

        is_closed = bool(item.get("is_closed"))
        is_verified = not is_closed
        if filters.only_verified and not is_verified:
            return None

        categories = item.get("categories") or []
        category_names = [clean(category.get("title")) for category in categories if isinstance(category, dict)]
        description = ", ".join(value for value in category_names if value)

        location_items = (item.get("location") or {}).get("display_address") or []
        location_text = ", ".join(clean(value) or "" for value in location_items).strip(", ")
        location = location_text or filters.location or None

        return SourceRecord(
            source="yelp",
            external_id=external_id,
            name=name,
            url=website,
            description=description or None,
            website=website,
            phone=phone,
            rating=rating,
            review_count=safe_int(item.get("review_count")),
            location=location,
            niche=filters.niche,
            is_verified=is_verified,
            raw_json=json.dumps(item, ensure_ascii=False),
        )
