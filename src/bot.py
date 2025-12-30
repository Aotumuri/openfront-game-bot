import os
from typing import Any

import discord
from dotenv import load_dotenv

from game.controller import GameController


class OpenFrontBot(discord.Client):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.controller = GameController()

    async def setup_hook(self) -> None:
        await self.controller.setup()

    async def close(self) -> None:
        await self.controller.close()
        await super().close()

    async def on_message(self, message: discord.Message) -> None:
        await self.controller.handle_message(message)


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
