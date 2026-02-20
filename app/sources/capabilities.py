from __future__ import annotations

import os
from typing import Any


SOURCE_CAPABILITIES: dict[str, dict[str, Any]] = {
    "telegram": {
        "supports_discovery_api": False,
        "requires_location": False,
        "supports_rating_filter": False,
        "supports_verified_filter": False,
        "supports_has_website_filter": False,
        "supports_has_phone_filter": False,
        "credential_required": False,
        "credential_param": None,
        "credential_env": None,
        "credential_label": None,
    },
    "google_maps": {
        "supports_discovery_api": True,
        "requires_location": False,
        "supports_rating_filter": True,
        "supports_verified_filter": True,
        "supports_has_website_filter": True,
        "supports_has_phone_filter": True,
        "credential_required": True,
        "credential_param": "api_key",
        "credential_env": "GOOGLE_MAPS_API_KEY",
        "credential_label": "Google Maps API Key",
    },
    "reddit": {
        "supports_discovery_api": True,
        "requires_location": False,
        "supports_rating_filter": False,
        "supports_verified_filter": True,
        "supports_has_website_filter": True,
        "supports_has_phone_filter": True,
        "credential_required": False,
        "credential_param": "user_agent",
        "credential_env": "REDDIT_USER_AGENT",
        "credential_label": "Reddit User-Agent",
        "oauth_envs": ["REDDIT_CLIENT_ID", "REDDIT_CLIENT_SECRET"],
    },
}


def get_source_capabilities(source: str) -> dict[str, Any]:
    if source not in SOURCE_CAPABILITIES:
        raise ValueError(f"Unsupported source: {source}")
    return dict(SOURCE_CAPABILITIES[source])


def get_platform_capabilities() -> dict[str, dict[str, Any]]:
    return {key: dict(value) for key, value in SOURCE_CAPABILITIES.items()}


def get_platform_capabilities_with_runtime() -> dict[str, dict[str, Any]]:
    runtime_caps = get_platform_capabilities()
    for source, values in runtime_caps.items():
        env_name = values.get("credential_env")
        if not env_name:
            values["configured"] = True
        else:
            values["configured"] = bool((os.getenv(env_name) or "").strip())

        oauth_envs = values.get("oauth_envs") or []
        values["oauth_configured"] = bool(
            oauth_envs
            and all(bool((os.getenv(name) or "").strip()) for name in oauth_envs)
        )
    return runtime_caps
