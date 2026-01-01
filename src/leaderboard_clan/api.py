import asyncio
import os
from typing import Any, Dict, Optional

import aiohttp


def get_clan_leaderboard_url() -> str:
    url = os.getenv("OPENFRONT_CLAN_LEADERBOARD_API_URL")
    if not url:
        raise RuntimeError("OPENFRONT_CLAN_LEADERBOARD_API_URL is not set")
    return url


async def fetch_clan_leaderboard(
    session: aiohttp.ClientSession,
) -> Optional[Dict[str, Any]]:
    try:
        async with session.get(get_clan_leaderboard_url()) as response:
            if response.status != 200:
                return None
            payload = await response.json(content_type=None)
    except (aiohttp.ClientError, asyncio.TimeoutError, ValueError):
        return None

    if not isinstance(payload, dict):
        return None
    return payload


async def fetch_clan_leaderboard_payload(
    session: aiohttp.ClientSession,
) -> tuple[Optional[Dict[str, Any]], Optional[str]]:
    try:
        data = await fetch_clan_leaderboard(session)
    except RuntimeError as exc:
        return None, str(exc)
    if not data:
        return None, "Leaderboard not available."
    return data, None
