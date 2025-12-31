import asyncio
import os
from typing import Any, Dict, Optional

import aiohttp


def get_api_url() -> str:
    url = os.getenv("OPENFRONT_PLAYER_API_URL")
    if not url:
        raise RuntimeError("OPENFRONT_PLAYER_API_URL is not set")
    return url


def build_player_url(base_url: str, player_id: str) -> str:
    if "{player_id}" not in base_url:
        raise RuntimeError("OPENFRONT_PLAYER_API_URL must include {player_id}")
    return base_url.format(player_id=player_id)


async def fetch_player(
    session: aiohttp.ClientSession, player_id: str
) -> Optional[Dict[str, Any]]:
    url = build_player_url(get_api_url(), player_id)
    try:
        async with session.get(url) as response:
            if response.status != 200:
                return None
            payload = await response.json(content_type=None)
    except (aiohttp.ClientError, asyncio.TimeoutError, ValueError):
        return None

    if not isinstance(payload, dict):
        return None
    return payload
