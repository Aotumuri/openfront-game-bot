from typing import Optional, Tuple

import aiohttp
import discord

from game.api import fetch_game
from game.embeds import build_embed
from game.replay_view import build_view
from shared.maps import get_thumbnail_file


async def build_game_payload(
    session: aiohttp.ClientSession, game_id: str
) -> Optional[Tuple[discord.Embed, discord.ui.View, Optional[discord.File]]]:
    data = await fetch_game(session, game_id)
    if not data:
        return None

    map_name = data.get("info", {}).get("config", {}).get("gameMap", "")
    thumbnail_file = get_thumbnail_file(map_name)
    thumbnail_name = thumbnail_file.filename if thumbnail_file else None
    embed = build_embed(data, game_id, thumbnail_name)
    view = build_view(game_id)
    return embed, view, thumbnail_file
