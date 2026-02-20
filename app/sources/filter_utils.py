from __future__ import annotations

from typing import Any


def clean(value: Any) -> str | None:
    if value is None:
        return None
    text = str(value).strip()
    return text or None


def passes_presence_filter(mode: str, value: str | None) -> bool:
    has_value = bool((value or "").strip())
    if mode == "yes":
        return has_value
    if mode == "no":
        return not has_value
    return True


def safe_int(value: Any) -> int | None:
    try:
        if value is None:
            return None
        return int(value)
    except (TypeError, ValueError):
        return None


def safe_float(value: Any) -> float | None:
    try:
        if value is None:
            return None
        return float(value)
    except (TypeError, ValueError):
        return None


def location_text(address_payload: Any) -> str | None:
    if isinstance(address_payload, str):
        return clean(address_payload)
    if not isinstance(address_payload, dict):
        return None

    candidates = [
        address_payload.get("formatted_address"),
        address_payload.get("freeformAddress"),
    ]
    for key in ("address_line1", "address_line2", "locality", "region", "postcode", "country"):
        value = clean(address_payload.get(key))
        if value:
            candidates.append(value)

    compact = ", ".join(value for value in (clean(item) for item in candidates) if value)
    return compact or None
