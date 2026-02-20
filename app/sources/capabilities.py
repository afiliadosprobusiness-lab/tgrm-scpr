from __future__ import annotations

from typing import Any


SOURCE_CAPABILITIES: dict[str, dict[str, Any]] = {
    "telegram": {
        "supports_discovery_api": False,
        "requires_location": False,
        "supports_rating_filter": False,
        "supports_verified_filter": False,
        "supports_has_website_filter": False,
        "supports_has_phone_filter": False,
    },
    "google_maps": {
        "supports_discovery_api": True,
        "requires_location": False,
        "supports_rating_filter": True,
        "supports_verified_filter": True,
        "supports_has_website_filter": True,
        "supports_has_phone_filter": True,
    },
    "openstreetmap": {
        "supports_discovery_api": True,
        "requires_location": True,
        "supports_rating_filter": False,
        "supports_verified_filter": True,
        "supports_has_website_filter": True,
        "supports_has_phone_filter": True,
    },
    "reddit": {
        "supports_discovery_api": True,
        "requires_location": False,
        "supports_rating_filter": False,
        "supports_verified_filter": True,
        "supports_has_website_filter": True,
        "supports_has_phone_filter": True,
    },
    "foursquare": {
        "supports_discovery_api": True,
        "requires_location": False,
        "supports_rating_filter": True,
        "supports_verified_filter": True,
        "supports_has_website_filter": True,
        "supports_has_phone_filter": True,
    },
    "yelp": {
        "supports_discovery_api": True,
        "requires_location": True,
        "supports_rating_filter": True,
        "supports_verified_filter": True,
        "supports_has_website_filter": True,
        "supports_has_phone_filter": True,
    },
    "tomtom": {
        "supports_discovery_api": True,
        "requires_location": False,
        "supports_rating_filter": False,
        "supports_verified_filter": True,
        "supports_has_website_filter": True,
        "supports_has_phone_filter": True,
    },
    "opencorporates": {
        "supports_discovery_api": True,
        "requires_location": False,
        "supports_rating_filter": False,
        "supports_verified_filter": True,
        "supports_has_website_filter": True,
        "supports_has_phone_filter": True,
    },
    "instagram": {
        "supports_discovery_api": False,
        "disabled_reason": "disabled_due_compliance_policy",
    },
    "linkedin": {
        "supports_discovery_api": False,
        "disabled_reason": "disabled_due_compliance_policy",
    },
}


def get_source_capabilities(source: str) -> dict[str, Any]:
    if source not in SOURCE_CAPABILITIES:
        raise ValueError(f"Unsupported source: {source}")
    return dict(SOURCE_CAPABILITIES[source])
