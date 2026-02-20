from __future__ import annotations

import json
import time
import urllib.error
import urllib.parse
import urllib.request
from typing import Any

from ..utils import calculate_backoff_seconds


def http_get_json(
    *,
    url: str,
    params: dict[str, Any] | None = None,
    headers: dict[str, str] | None = None,
    timeout_seconds: int = 20,
    retries: int = 3,
) -> Any:
    encoded_url = url
    if params:
        query = urllib.parse.urlencode(params)
        separator = "&" if "?" in url else "?"
        encoded_url = f"{url}{separator}{query}"

    request_headers = {
        "Accept": "application/json",
        "User-Agent": "proyectos-sass-scraper/1.0",
    }
    if headers:
        request_headers.update(headers)

    for attempt in range(1, retries + 1):
        try:
            request = urllib.request.Request(encoded_url, headers=request_headers, method="GET")
            with urllib.request.urlopen(request, timeout=timeout_seconds) as response:
                payload = response.read().decode("utf-8")
                return json.loads(payload)
        except urllib.error.HTTPError as exc:
            status = getattr(exc, "code", 0)
            is_retryable = status in {408, 429, 500, 502, 503, 504}
            if attempt >= retries or not is_retryable:
                raise
            time.sleep(calculate_backoff_seconds(attempt=attempt))
        except (urllib.error.URLError, TimeoutError):
            if attempt >= retries:
                raise
            time.sleep(calculate_backoff_seconds(attempt=attempt))

    return {}
