from typing import Any, Optional

import discord


async def get_session(interaction: discord.Interaction) -> Optional[Any]:
    client = interaction.client
    controller = getattr(client, "controller", None)
    session = getattr(controller, "http_session", None)

    if controller and not session:
        await controller.setup()
        session = getattr(controller, "http_session", None)

    return session
