import asyncio
import os
from typing import Any, Dict, Optional

import aiohttp


def get_api_url() -> str:
    url = os.getenv("OPENFRONT_CLAN_API_URL")
    if not url:
        raise RuntimeError("OPENFRONT_CLAN_API_URL is not set")
    return url


def get_leaderboard_url() -> str:
    url = os.getenv("OPENFRONT_CLAN_LEADERBOARD_API_URL")
    if not url:
        raise RuntimeError("OPENFRONT_CLAN_LEADERBOARD_API_URL is not set")
    return url


def build_clan_url(base_url: str, clan_name: str) -> str:
    if "{clan_name}" not in base_url:
        raise RuntimeError("OPENFRONT_CLAN_API_URL must include {clan_name}")
    return base_url.format(clan_name=clan_name)


async def fetch_clan(
    session: aiohttp.ClientSession, clan_name: str
) -> Optional[Dict[str, Any]]:
    url = build_clan_url(get_api_url(), clan_name)
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


async def fetch_clan_leaderboard(
    session: aiohttp.ClientSession,
) -> Optional[Dict[str, Any]]:
    try:
        async with session.get(get_leaderboard_url()) as response:
            if response.status != 200:
                return None
            payload = await response.json(content_type=None)
    except (aiohttp.ClientError, asyncio.TimeoutError, ValueError):
        return None

    if not isinstance(payload, dict):
        return None
    return payload
