from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from telethon import TelegramClient
from telethon.sessions import StringSession

from .config import TelegramSettings, normalize_target


@dataclass
class ResolvedTarget:
    target_input: str
    target_id: int
    target_username: str | None
    title: str | None
    entity: Any


class TelegramClientManager:
    def __init__(self, settings: TelegramSettings):
        self.settings = settings
        session = (
            StringSession(settings.string_session)
            if settings.string_session
            else settings.session_name
        )
        self.client = TelegramClient(
            session,
            settings.api_id,
            settings.api_hash,
        )

    async def connect(self, allow_interactive: bool = True) -> None:
        if allow_interactive:
            await self.client.start()
            return

        await self.client.connect()
        is_authorized = await self.client.is_user_authorized()
        if is_authorized:
            return

        raise RuntimeError(
            "Telegram session is not authorized for web scraping. Configure TELEGRAM_STRING_SESSION "
            "or authorize the session locally first using CLI."
        )

    async def disconnect(self) -> None:
        await self.client.disconnect()

    async def resolve_target(self, raw_target: str) -> ResolvedTarget:
        normalized = normalize_target(raw_target)
        entity = await self.client.get_entity(normalized)

        target_id = int(getattr(entity, "id"))
        target_username = getattr(entity, "username", None)
        title = getattr(entity, "title", None) or target_username

        return ResolvedTarget(
            target_input=normalized,
            target_id=target_id,
            target_username=target_username,
            title=title,
            entity=entity,
        )
