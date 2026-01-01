import asyncio
from typing import Optional, Tuple

import aiohttp
import discord

from game.service import build_game_payload
from game.message_parser import extract_game_ids, should_ignore_message


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

    async def build_game_message(
        self, game_id: str
    ) -> Optional[Tuple[discord.Embed, discord.ui.View, Optional[discord.File]]]:
        if not self.http_session:
            await self.setup()
        if not self.http_session:
            return None

        return await build_game_payload(self.http_session, game_id)

    async def handle_message(self, message: discord.Message) -> None:
        if should_ignore_message(message):
            return

        game_ids = extract_game_ids(message.content)
        if not game_ids:
            return

        sent_any = False
        for game_id in game_ids:
            payload = await self.build_game_message(game_id)
            if not payload:
                continue
            embed, view, thumbnail_file = payload
            if thumbnail_file:
                await message.channel.send(embed=embed, view=view, file=thumbnail_file)
            else:
                await message.channel.send(embed=embed, view=view)
            sent_any = True

        if sent_any:
            return
