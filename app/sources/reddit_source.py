from __future__ import annotations

import base64
import json
import os
import re
import time
import urllib.error
import urllib.parse
import urllib.request
from typing import Any

from ..utils import calculate_backoff_seconds
from .filter_utils import passes_presence_filter, safe_int
from .http_utils import http_get_json
from .models import DiscoveryFilters, SourceRecord


REDDIT_SEARCH_URL = "https://www.reddit.com/search.json"
REDDIT_OAUTH_SEARCH_URL = "https://oauth.reddit.com/search"
REDDIT_OAUTH_TOKEN_URL = "https://www.reddit.com/api/v1/access_token"
PHONE_REGEX = re.compile(r"(\+?\d[\d\-\s().]{7,}\d)")
URL_REGEX = re.compile(r"(https?://[^\s]+)")


class RedditSource:
    def __init__(
        self,
        user_agent: str | None = None,
        client_id: str | None = None,
        client_secret: str | None = None,
    ):
        self.user_agent = user_agent or os.getenv(
            "REDDIT_USER_AGENT", "proyectos-sass-scraper/1.0 (by u/local_operator)"
        )
        self.client_id = client_id or os.getenv("REDDIT_CLIENT_ID")
        self.client_secret = client_secret or os.getenv("REDDIT_CLIENT_SECRET")

    def search(self, filters: DiscoveryFilters) -> list[SourceRecord]:
        query = filters.merged_query() or filters.query or "business"
        payload = self._fetch_payload(query=query, limit=min(filters.limit, 100))
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

    def _fetch_payload(self, *, query: str, limit: int) -> dict[str, Any]:
        base_params = {
            "q": query,
            "limit": limit,
            "sort": "relevance",
            "t": "month",
            "raw_json": 1,
            "type": "link",
        }
        if self._has_oauth_credentials():
            oauth_token = self._fetch_oauth_token()
            return http_get_json(
                url=REDDIT_OAUTH_SEARCH_URL,
                params=base_params,
                headers={
                    "User-Agent": self.user_agent,
                    "Authorization": f"bearer {oauth_token}",
                },
                retries=4,
            )

        try:
            return http_get_json(
                url=REDDIT_SEARCH_URL,
                params=base_params,
                headers={"User-Agent": self.user_agent},
                retries=4,
            )
        except urllib.error.HTTPError as exc:
            if getattr(exc, "code", 0) == 403:
                raise ValueError(
                    "Reddit public endpoint is blocked in this runtime. Configure REDDIT_CLIENT_ID and "
                    "REDDIT_CLIENT_SECRET for OAuth access."
                ) from exc
            raise

    def _has_oauth_credentials(self) -> bool:
        return bool((self.client_id or "").strip() and (self.client_secret or "").strip())

    def _fetch_oauth_token(self) -> str:
        if not self._has_oauth_credentials():
            raise ValueError("Missing Reddit OAuth credentials.")

        auth_value = f"{self.client_id}:{self.client_secret}".encode("utf-8")
        basic_token = base64.b64encode(auth_value).decode("ascii")
        encoded_body = urllib.parse.urlencode({"grant_type": "client_credentials"}).encode("utf-8")
        request = urllib.request.Request(
            REDDIT_OAUTH_TOKEN_URL,
            data=encoded_body,
            method="POST",
            headers={
                "Accept": "application/json",
                "Authorization": f"Basic {basic_token}",
                "Content-Type": "application/x-www-form-urlencoded",
                "User-Agent": self.user_agent,
            },
        )

        for attempt in range(1, 5):
            try:
                with urllib.request.urlopen(request, timeout=20) as response:
                    payload = json.loads(response.read().decode("utf-8"))
                access_token = str(payload.get("access_token") or "").strip()
                if not access_token:
                    raise ValueError("Reddit OAuth token response missing access_token.")
                return access_token
            except urllib.error.HTTPError as exc:
                status = getattr(exc, "code", 0)
                if status in {401, 403}:
                    raise ValueError(
                        "Reddit OAuth authentication failed. Verify REDDIT_CLIENT_ID/REDDIT_CLIENT_SECRET."
                    ) from exc
                retryable = status in {408, 429, 500, 502, 503, 504}
                if attempt >= 4 or not retryable:
                    raise ValueError(f"Reddit OAuth token request failed with status {status}.") from exc
                time.sleep(calculate_backoff_seconds(attempt=attempt))
            except (urllib.error.URLError, TimeoutError) as exc:
                if attempt >= 4:
                    raise ValueError("Reddit OAuth token request failed due network error.") from exc
                time.sleep(calculate_backoff_seconds(attempt=attempt))

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
