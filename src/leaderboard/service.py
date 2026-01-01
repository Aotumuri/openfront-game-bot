from typing import Any, Optional, Tuple

import discord

from leaderboard.api import fetch_leaderboard
from leaderboard.embeds import build_leaderboard_embed
from leaderboard.view import LeaderboardPlayersView


async def build_leaderboard_payload(
    session: Any,
) -> Tuple[Optional[discord.Embed], Optional[discord.ui.View], Optional[str]]:
    try:
        data = await fetch_leaderboard(session)
    except RuntimeError as exc:
        return None, None, str(exc)
    if not data:
        return None, None, "Leaderboard not available."

    embed = build_leaderboard_embed(data)
    player_ids = [entry.get("public_id") for entry in data[:10]]
    view = LeaderboardPlayersView(player_ids)
    return embed, view, None
