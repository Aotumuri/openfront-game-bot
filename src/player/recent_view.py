from typing import Iterable, List, Optional

import discord


class RecentGameButton(discord.ui.Button):
    def __init__(self, index: int, game_id: str) -> None:
        super().__init__(
            label=f"Game {index}",
            style=discord.ButtonStyle.secondary,
            custom_id=f"recent_game_{index}",
        )
        self.game_id = game_id

    async def callback(self, interaction: discord.Interaction) -> None:
        client = interaction.client
        controller = getattr(client, "controller", None)
        if not controller:
            await interaction.response.send_message(
                "Bot not ready.", ephemeral=True
            )
            return

        payload = await controller.build_game_message(self.game_id)
        if not payload:
            await interaction.response.send_message(
                "Game not found.", ephemeral=True
            )
            return

        embed, view, thumbnail_file = payload
        if thumbnail_file:
            await interaction.response.send_message(
                embed=embed, view=view, file=thumbnail_file, ephemeral=True
            )
        else:
            await interaction.response.send_message(
                embed=embed, view=view, ephemeral=True
            )


class RecentGamesView(discord.ui.View):
    def __init__(self, game_ids: Iterable[str]) -> None:
        super().__init__(timeout=300)
        ids: List[str] = [game_id for game_id in game_ids if game_id]
        for index, game_id in enumerate(ids, start=1):
            self.add_item(RecentGameButton(index, game_id))

    async def on_timeout(self) -> None:
        for item in self.children:
            if isinstance(item, discord.ui.Button):
                item.disabled = True
