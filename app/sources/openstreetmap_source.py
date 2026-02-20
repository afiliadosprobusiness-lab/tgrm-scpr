from __future__ import annotations

import json
import os
import re
import time
import urllib.error
import urllib.parse
import urllib.request
from typing import Any

from ..utils import calculate_backoff_seconds
from .filter_utils import clean, passes_presence_filter
from .http_utils import http_get_json
from .models import DiscoveryFilters, SourceRecord


NOMINATIM_URL = "https://nominatim.openstreetmap.org/search"
OVERPASS_URL = "https://overpass-api.de/api/interpreter"


class OpenStreetMapSource:
    def __init__(self, user_agent: str | None = None):
        self.user_agent = user_agent or os.getenv(
            "OSM_USER_AGENT", "proyectos-sass-scraper/1.0 (contact: local-admin)"
        )

    def search(self, filters: DiscoveryFilters) -> list[SourceRecord]:
        if not filters.location:
            raise ValueError("OpenStreetMap discovery requires a location.")

        lat, lon = self._resolve_location(filters.location)
        query = self._build_overpass_query(filters=filters, lat=lat, lon=lon)
        try:
            payload = self._run_overpass_query(query=query)
        except urllib.error.HTTPError as exc:
            if exc.code != 400:
                raise
            return self._search_with_nominatim(filters)

        results: list[SourceRecord] = []
        for element in payload.get("elements", []):
            record = self._to_record(element=element, filters=filters)
            if record is None:
                continue
            results.append(record)
            if len(results) >= filters.limit:
                break
        if not results:
            return self._search_with_nominatim(filters)
        return results

    def _resolve_location(self, location: str) -> tuple[float, float]:
        payload = http_get_json(
            url=NOMINATIM_URL,
            params={"q": location, "format": "jsonv2", "limit": 1},
            headers={"User-Agent": self.user_agent},
            retries=4,
        )
        if not isinstance(payload, list) or not payload:
            raise ValueError(f"Could not resolve location in OpenStreetMap: {location}")

        first = payload[0]
        lat = float(first.get("lat"))
        lon = float(first.get("lon"))
        return lat, lon

    def _run_overpass_query(self, *, query: str) -> dict[str, Any]:
        data = urllib.parse.urlencode({"data": query}).encode("utf-8")
        headers = {
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "User-Agent": self.user_agent,
            "Accept": "application/json",
        }

        for attempt in range(1, 4):
            try:
                request = urllib.request.Request(OVERPASS_URL, data=data, headers=headers, method="POST")
                with urllib.request.urlopen(request, timeout=40) as response:
                    payload = response.read().decode("utf-8")
                    return json.loads(payload)
            except urllib.error.HTTPError as exc:
                if attempt >= 3:
                    raise
                if exc.code not in {429, 500, 502, 503, 504}:
                    raise
                time.sleep(calculate_backoff_seconds(attempt=attempt))
            except (urllib.error.URLError, TimeoutError):
                if attempt >= 3:
                    raise
                time.sleep(calculate_backoff_seconds(attempt=attempt))
        return {}

    def _search_with_nominatim(self, filters: DiscoveryFilters) -> list[SourceRecord]:
        payload = http_get_json(
            url=NOMINATIM_URL,
            params={
                "q": filters.merged_query() or filters.location or "business",
                "format": "jsonv2",
                "limit": min(filters.limit, 50),
                "addressdetails": 1,
                "extratags": 1,
            },
            headers={"User-Agent": self.user_agent},
            retries=4,
        )
        if not isinstance(payload, list):
            return []

        results: list[SourceRecord] = []
        for item in payload:
            record = self._to_nominatim_record(item=item, filters=filters)
            if record is None:
                continue
            results.append(record)
            if len(results) >= filters.limit:
                break
        return results

    def _build_overpass_query(self, *, filters: DiscoveryFilters, lat: float, lon: float) -> str:
        radius = 6000
        keywords = []
        if filters.query:
            keywords.append(filters.query)
        if filters.niche and filters.niche != "all":
            keywords.append(filters.niche.replace("_", " "))
        regex = "|".join(re.escape(item) for item in keywords if item.strip())

        name_filter = f'["name"~"(?i){regex}"]' if regex else ""
        return (
            '[out:json][timeout:25];'
            "("
            f'node(around:{radius},{lat},{lon})["name"]{name_filter}["shop"];'
            f'way(around:{radius},{lat},{lon})["name"]{name_filter}["shop"];'
            f'node(around:{radius},{lat},{lon})["name"]{name_filter}["amenity"];'
            f'way(around:{radius},{lat},{lon})["name"]{name_filter}["amenity"];'
            f'node(around:{radius},{lat},{lon})["name"]{name_filter}["office"];'
            f'way(around:{radius},{lat},{lon})["name"]{name_filter}["office"];'
            ");"
            "out tags center 200;"
        )

    def _to_record(self, *, element: dict[str, Any], filters: DiscoveryFilters) -> SourceRecord | None:
        tags = element.get("tags") or {}
        name = str(tags.get("name") or "").strip()
        if not name:
            return None

        website = clean(tags.get("website") or tags.get("contact:website"))
        phone = clean(tags.get("phone") or tags.get("contact:phone"))

        if not passes_presence_filter(filters.has_website, website):
            return None
        if not passes_presence_filter(filters.has_phone, phone):
            return None

        is_verified = bool(tags.get("wikidata") or tags.get("brand:wikidata"))
        if filters.only_verified and not is_verified:
            return None

        element_type = str(element.get("type") or "node")
        element_id = str(element.get("id") or "")
        if not element_id:
            return None

        center = element.get("center") or {}
        lat = element.get("lat") or center.get("lat")
        lon = element.get("lon") or center.get("lon")
        location = filters.location
        if lat is not None and lon is not None:
            location = f"{filters.location} ({lat}, {lon})"

        description = tags.get("shop") or tags.get("amenity") or tags.get("office")
        return SourceRecord(
            source="openstreetmap",
            external_id=f"{element_type}_{element_id}",
            name=name,
            url=f"https://www.openstreetmap.org/{element_type}/{element_id}",
            description=str(description or ""),
            website=website,
            phone=phone,
            rating=None,
            review_count=None,
            location=location,
            niche=filters.niche,
            is_verified=is_verified,
            raw_json=json.dumps(element, ensure_ascii=False),
        )

    def _to_nominatim_record(self, *, item: dict[str, Any], filters: DiscoveryFilters) -> SourceRecord | None:
        place_id = clean(item.get("place_id"))
        display_name = clean(item.get("display_name"))
        if not place_id or not display_name:
            return None

        extratags = item.get("extratags") or {}
        website = clean(extratags.get("website") or extratags.get("contact:website"))
        phone = clean(extratags.get("phone") or extratags.get("contact:phone"))
        if not passes_presence_filter(filters.has_website, website):
            return None
        if not passes_presence_filter(filters.has_phone, phone):
            return None

        is_verified = bool(extratags.get("wikidata") or extratags.get("brand:wikidata"))
        if filters.only_verified and not is_verified:
            return None

        lat = clean(item.get("lat"))
        lon = clean(item.get("lon"))
        location = display_name
        if lat and lon:
            location = f"{display_name} ({lat}, {lon})"

        osm_type = clean(item.get("osm_type")) or "node"
        osm_id = clean(item.get("osm_id")) or place_id
        return SourceRecord(
            source="openstreetmap",
            external_id=f"{osm_type}_{osm_id}",
            name=display_name.split(",")[0].strip() or display_name,
            url=f"https://www.openstreetmap.org/{osm_type}/{osm_id}",
            description=clean(item.get("type")) or clean(item.get("class")) or "",
            website=website,
            phone=phone,
            rating=None,
            review_count=None,
            location=location,
            niche=filters.niche,
            is_verified=is_verified,
            raw_json=json.dumps(item, ensure_ascii=False),
        )
