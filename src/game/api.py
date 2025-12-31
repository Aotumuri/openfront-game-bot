import asyncio
import os
from typing import Any, Dict, Optional

import aiohttp


def get_api_url() -> str:
    url = os.getenv("OPENFRONT_GAME_API_URL")
    if not url:
        raise RuntimeError("OPENFRONT_GAME_API_URL is not set")
    return url


def build_game_url(base_url: str, game_id: str) -> str:
    if "{game_id}" not in base_url:
        raise RuntimeError("OPENFRONT_GAME_API_URL must include {game_id}")
    return base_url.format(game_id=game_id)


async def fetch_game(
    session: aiohttp.ClientSession, game_id: str
) -> Optional[Dict[str, Any]]:
    url = build_game_url(get_api_url(), game_id)
    try:
        async with session.get(url) as response:
            if response.status != 200:
                return None
            payload = await response.json(content_type=None)
    except (aiohttp.ClientError, asyncio.TimeoutError, ValueError):
        return None

    if isinstance(payload, dict) and payload.get("error") == "Not found":
        return None
    if not isinstance(payload, dict):
        return None
    return payload
