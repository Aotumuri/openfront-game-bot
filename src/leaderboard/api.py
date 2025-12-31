import asyncio
import os
from typing import Any, Dict, List, Optional

import aiohttp

def get_leaderboard_url() -> str:
    url = os.getenv("OPENFRONT_LEADERBOARD_API_URL")
    if not url:
        raise RuntimeError("OPENFRONT_LEADERBOARD_API_URL is not set")
    return url


async def fetch_leaderboard(
    session: aiohttp.ClientSession,
) -> Optional[List[Dict[str, Any]]]:
    try:
        async with session.get(get_leaderboard_url()) as response:
            if response.status != 200:
                return None
            payload = await response.json(content_type=None)
    except (aiohttp.ClientError, asyncio.TimeoutError, ValueError):
        return None

    if not isinstance(payload, list):
        return None
    return payload
