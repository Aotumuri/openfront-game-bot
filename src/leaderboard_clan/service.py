from typing import Any, Dict, Optional

from leaderboard_clan.api import fetch_clan_leaderboard


async def fetch_clan_leaderboard_payload(
    session: Any,
) -> tuple[Optional[Dict[str, Any]], Optional[str]]:
    try:
        data = await fetch_clan_leaderboard(session)
    except RuntimeError as exc:
        return None, str(exc)
    if not data:
        return None, "Leaderboard not available."
    return data, None
