from __future__ import annotations

import json
import os
from typing import Any

from .filter_utils import clean, passes_presence_filter
from .http_utils import http_get_json
from .models import DiscoveryFilters, SourceRecord


OPENCORPORATES_SEARCH_URL = "https://api.opencorporates.com/v0.4/companies/search"
ACTIVE_STATES = {"active", "registered", "incorporated", "normal"}


class OpenCorporatesSource:
    def __init__(self, api_token: str | None = None):
        self.api_token = api_token or os.getenv("OPENCORPORATES_API_TOKEN")
        if not self.api_token:
            raise ValueError("Missing OPENCORPORATES_API_TOKEN in environment.")

    def search(self, filters: DiscoveryFilters) -> list[SourceRecord]:
        query = filters.merged_query() or "company"
        params: dict[str, Any] = {
            "q": query,
            "per_page": min(filters.limit, 100),
            "order": "score",
        }
        params["api_token"] = self.api_token

        payload = http_get_json(url=OPENCORPORATES_SEARCH_URL, params=params, retries=4)
        result_items = ((payload.get("results") or {}).get("companies")) or []

        records: list[SourceRecord] = []
        for item in result_items:
            company = (item or {}).get("company") or {}
            record = self._to_record(company=company, filters=filters)
            if record is None:
                continue
            records.append(record)
            if len(records) >= filters.limit:
                break
        return records

    def _to_record(self, *, company: dict[str, Any], filters: DiscoveryFilters) -> SourceRecord | None:
        jurisdiction_code = clean(company.get("jurisdiction_code")) or "unknown"
        company_number = clean(company.get("company_number")) or clean(company.get("native_company_number"))
        name = clean(company.get("name"))
        if not company_number or not name:
            return None

        external_id = f"{jurisdiction_code}/{company_number}"
        website = clean(company.get("registry_url")) or clean(company.get("homepage_url"))
        phone = clean(company.get("telephone_number"))

        if not passes_presence_filter(filters.has_website, website):
            return None
        if not passes_presence_filter(filters.has_phone, phone):
            return None

        status_text = (clean(company.get("current_status")) or "").lower()
        inactive = bool(company.get("inactive"))
        is_verified = (not inactive) and (
            not status_text or any(keyword in status_text for keyword in ACTIVE_STATES)
        )
        if filters.only_verified and not is_verified:
            return None

        description = clean(company.get("company_type"))
        if not description:
            description = clean(company.get("industry_codes"))

        return SourceRecord(
            source="opencorporates",
            external_id=external_id,
            name=name,
            url=clean(company.get("opencorporates_url")) or website,
            description=description,
            website=website,
            phone=phone,
            rating=None,
            review_count=None,
            location=clean(company.get("registered_address_in_full")) or filters.location or None,
            niche=filters.niche,
            is_verified=is_verified,
            raw_json=json.dumps(company, ensure_ascii=False),
        )
