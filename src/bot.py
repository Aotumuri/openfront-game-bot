import os
from typing import Any

import discord
from discord import app_commands
from dotenv import load_dotenv

from easteregg.chocolate import handle_chocolate_reaction, is_chocolate_reaction
from clan.cmd import clan_command
from game.cmd import game_command
from info.cmd import info_command
from leaderboard.cmd import leaderboard_command
from leaderboard_clan.cmd import leaderboard_clan_command
from player.cmd import player_command
from game.controller import GameController


class OpenFrontBot(discord.Client):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.controller = GameController()
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self) -> None:
        await self.controller.setup()
        self.tree.add_command(game_command)
        self.tree.add_command(leaderboard_clan_command)
        self.tree.add_command(player_command)
        self.tree.add_command(leaderboard_command)
        self.tree.add_command(info_command)
        self.tree.add_command(clan_command)
        await self.tree.sync()

    async def close(self) -> None:
        await self.controller.close()
        await super().close()

    async def on_message(self, message: discord.Message) -> None:
        await self.controller.handle_message(message)

    async def on_reaction_add(
        self, reaction: discord.Reaction, user: discord.User | discord.Member
    ) -> None:
        if user.bot:
            return
        if not self.user or reaction.message.author.id != self.user.id:
            return

        if not is_chocolate_reaction(reaction):
            return

        await handle_chocolate_reaction(reaction, user)


def main() -> None:
    load_dotenv()
    token = os.getenv("DISCORD_TOKEN")
    if not token:
        raise RuntimeError("DISCORD_TOKEN is not set")

    intents = discord.Intents.default()
    intents.message_content = True
    client = OpenFrontBot(intents=intents)
    client.run(token)


if __name__ == "__main__":
    main()
