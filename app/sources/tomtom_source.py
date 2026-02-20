from __future__ import annotations

import json
import os
import urllib.parse
from typing import Any

from .filter_utils import clean, passes_presence_filter
from .http_utils import http_get_json
from .models import DiscoveryFilters, SourceRecord


TOMTOM_SEARCH_URL = "https://api.tomtom.com/search/2/search/{query}.json"


class TomTomSource:
    def __init__(self, api_key: str | None = None):
        self.api_key = api_key or os.getenv("TOMTOM_API_KEY")
        if not self.api_key:
            raise ValueError("Missing TOMTOM_API_KEY in environment.")

    def search(self, filters: DiscoveryFilters) -> list[SourceRecord]:
        query = filters.merged_query() or "business"
        encoded_query = urllib.parse.quote(query, safe="")
        url = TOMTOM_SEARCH_URL.format(query=encoded_query)
        payload = http_get_json(
            url=url,
            params={
                "key": self.api_key,
                "limit": min(filters.limit, 100),
                "idxSet": "POI",
                "typeahead": "false",
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
        poi = item.get("poi") or {}
        external_id = clean(item.get("id"))
        name = clean(poi.get("name"))
        if not external_id or not name:
            return None

        website = clean(poi.get("url"))
        phone = clean(poi.get("phone"))
        if not passes_presence_filter(filters.has_website, website):
            return None
        if not passes_presence_filter(filters.has_phone, phone):
            return None

        is_verified = bool(poi.get("brands"))
        if filters.only_verified and not is_verified:
            return None

        position = item.get("position") or {}
        lat = position.get("lat")
        lon = position.get("lon")
        source_link = None
        if lat is not None and lon is not None:
            source_link = f"https://www.tomtom.com/maps/?center={lat},{lon}&zoom=15"

        location_payload = item.get("address") or {}
        location = clean(location_payload.get("freeformAddress")) or filters.location or None

        categories = poi.get("categories") or []
        description = ", ".join(clean(category) or "" for category in categories).strip(", ")

        return SourceRecord(
            source="tomtom",
            external_id=external_id,
            name=name,
            url=source_link,
            description=description or None,
            website=website,
            phone=phone,
            rating=None,
            review_count=None,
            location=location,
            niche=filters.niche,
            is_verified=is_verified,
            raw_json=json.dumps(item, ensure_ascii=False),
        )
