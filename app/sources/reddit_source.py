from __future__ import annotations

import json
import os
import re
from typing import Any

from .filter_utils import passes_presence_filter, safe_int
from .http_utils import http_get_json
from .models import DiscoveryFilters, SourceRecord


REDDIT_SEARCH_URL = "https://www.reddit.com/search.json"
PHONE_REGEX = re.compile(r"(\+?\d[\d\-\s().]{7,}\d)")
URL_REGEX = re.compile(r"(https?://[^\s]+)")


class RedditSource:
    def __init__(self, user_agent: str | None = None):
        self.user_agent = user_agent or os.getenv(
            "REDDIT_USER_AGENT", "proyectos-sass-scraper/1.0 (by u/local_operator)"
        )

    def search(self, filters: DiscoveryFilters) -> list[SourceRecord]:
        query = filters.merged_query() or filters.query or "business"
        payload = http_get_json(
            url=REDDIT_SEARCH_URL,
            params={
                "q": query,
                "limit": min(filters.limit, 100),
                "sort": "relevance",
                "t": "month",
                "raw_json": 1,
            },
            headers={"User-Agent": self.user_agent},
            retries=4,
        )
        children = (((payload.get("data") or {}).get("children")) or [])

        records: list[SourceRecord] = []
        for child in children:
            data = (child or {}).get("data") or {}
            record = self._to_record(data=data, filters=filters)
            if record is None:
                continue
            records.append(record)
            if len(records) >= filters.limit:
                break
        return records

    def _to_record(self, *, data: dict[str, Any], filters: DiscoveryFilters) -> SourceRecord | None:
        reddit_id = str(data.get("id") or "")
        if not reddit_id:
            return None

        title = str(data.get("title") or "")
        selftext = str(data.get("selftext") or "")
        permalink = str(data.get("permalink") or "")
        post_url = f"https://www.reddit.com{permalink}" if permalink else str(data.get("url") or "")

        content_blob = " ".join([title, selftext, str(data.get("url") or "")]).strip()
        website = _extract_website(content_blob)
        phone = _extract_phone(content_blob)

        if not passes_presence_filter(filters.has_website, website):
            return None
        if not passes_presence_filter(filters.has_phone, phone):
            return None

        is_verified = str(data.get("distinguished") or "").lower() in {"moderator", "admin"}
        if filters.only_verified and not is_verified:
            return None

        return SourceRecord(
            source="reddit",
            external_id=reddit_id,
            name=title or f"reddit_post_{reddit_id}",
            url=post_url or None,
            description=selftext[:5000] if selftext else None,
            website=website,
            phone=phone,
            rating=None,
            review_count=safe_int(data.get("num_comments")),
            location=filters.location or None,
            niche=filters.niche,
            is_verified=is_verified,
            raw_json=json.dumps(data, ensure_ascii=False),
        )


def _extract_phone(text: str) -> str | None:
    if not text:
        return None
    match = PHONE_REGEX.search(text)
    if not match:
        return None
    return match.group(1).strip()


def _extract_website(text: str) -> str | None:
    if not text:
        return None
    matches = URL_REGEX.findall(text)
    if not matches:
        return None
    # Avoid returning reddit permalink itself as business website.
    for match in matches:
        if "reddit.com" not in match:
            return match
    return None
