from __future__ import annotations

import json
import os
import random
import time
from typing import Any

from .filter_utils import passes_presence_filter, safe_int
from .http_utils import http_get_json
from .models import DiscoveryFilters, SourceRecord


TEXT_SEARCH_URL = "https://maps.googleapis.com/maps/api/place/textsearch/json"
DETAILS_URL = "https://maps.googleapis.com/maps/api/place/details/json"


class GoogleMapsSource:
    def __init__(self, api_key: str | None = None):
        self.api_key = api_key or os.getenv("GOOGLE_MAPS_API_KEY")
        if not self.api_key:
            raise ValueError("Missing GOOGLE_MAPS_API_KEY in environment.")

    def search(self, filters: DiscoveryFilters) -> list[SourceRecord]:
        query = filters.merged_query() or "business"
        results: list[SourceRecord] = []
        page_token: str | None = None

        while len(results) < filters.limit:
            params: dict[str, Any] = {
                "key": self.api_key,
                "query": query,
                "language": "en",
            }
            if page_token:
                # Google requires a short wait before next_page_token becomes valid.
                time.sleep(2)
                params["pagetoken"] = page_token

            payload = http_get_json(url=TEXT_SEARCH_URL, params=params, retries=4)
            status = str(payload.get("status", "UNKNOWN"))
            if status not in {"OK", "ZERO_RESULTS"}:
                if status == "INVALID_REQUEST" and page_token:
                    time.sleep(2)
                    continue
                raise ValueError(f"Google Maps API error: {status}")

            for item in payload.get("results", []):
                record = self._to_record(item=item, filters=filters)
                if record is None:
                    continue
                results.append(record)
                if len(results) >= filters.limit:
                    break

            page_token = payload.get("next_page_token")
            if not page_token:
                break

        return results[: filters.limit]

    def _to_record(self, *, item: dict[str, Any], filters: DiscoveryFilters) -> SourceRecord | None:
        place_id = str(item.get("place_id") or "")
        if not place_id:
            return None

        details = self._fetch_details(place_id)
        website = details.get("website")
        phone = details.get("formatted_phone_number")

        rating_raw = item.get("rating")
        rating = float(rating_raw) if rating_raw is not None else None
        if rating is not None and rating < filters.min_rating:
            return None

        if not passes_presence_filter(filters.has_website, website):
            return None
        if not passes_presence_filter(filters.has_phone, phone):
            return None

        is_verified = str(item.get("business_status", "")).upper() == "OPERATIONAL"
        if filters.only_verified and not is_verified:
            return None

        raw = {"text_search": item, "details": details}
        return SourceRecord(
            source="google_maps",
            external_id=place_id,
            name=str(item.get("name") or "unknown"),
            url=details.get("url"),
            description=str(item.get("types") or ""),
            website=website,
            phone=phone,
            rating=rating,
            review_count=safe_int(item.get("user_ratings_total")),
            location=str(item.get("formatted_address") or ""),
            niche=filters.niche,
            is_verified=is_verified,
            raw_json=json.dumps(raw, ensure_ascii=False),
        )

    def _fetch_details(self, place_id: str) -> dict[str, Any]:
        time.sleep(random.uniform(0.1, 0.35))
        payload = http_get_json(
            url=DETAILS_URL,
            params={
                "key": self.api_key,
                "place_id": place_id,
                "fields": "url,website,formatted_phone_number,name",
            },
            retries=4,
        )
        status = str(payload.get("status", "UNKNOWN"))
        if status not in {"OK", "ZERO_RESULTS"}:
            return {}
        return payload.get("result", {}) or {}
