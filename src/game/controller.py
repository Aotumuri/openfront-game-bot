import asyncio
from typing import Optional

import aiohttp
import discord

from game.embeds import build_embed
from game.game_api import fetch_game
from game.message_parser import extract_game_ids, should_ignore_message
from game.replay_view import build_view
from shared.maps import get_thumbnail_file


class GameController:
    def __init__(self) -> None:
        self.http_session: Optional[aiohttp.ClientSession] = None

    async def setup(self) -> None:
        if self.http_session:
            return
        timeout = aiohttp.ClientTimeout(total=10)
        self.http_session = aiohttp.ClientSession(timeout=timeout)

    async def close(self) -> None:
        if self.http_session:
            await self.http_session.close()
            self.http_session = None

    async def handle_message(self, message: discord.Message) -> None:
        if should_ignore_message(message):
            return

        game_ids = extract_game_ids(message.content)
        if not game_ids:
            return

        if not self.http_session:
            return

        sent_any = False
        for game_id in game_ids:
            data = await fetch_game(self.http_session, game_id)
            if not data:
                continue
            map_name = data.get("info", {}).get("config", {}).get("gameMap", "")
            thumbnail_file = get_thumbnail_file(map_name)
            thumbnail_name = thumbnail_file.filename if thumbnail_file else None
            embed = build_embed(data, game_id, thumbnail_name)
            view = build_view(game_id)
            if thumbnail_file:
                await message.channel.send(embed=embed, view=view, file=thumbnail_file)
            else:
                await message.channel.send(embed=embed, view=view)
            sent_any = True

        if sent_any:
            return
