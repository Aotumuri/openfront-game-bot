from typing import Iterable, List, Optional

import discord

from player.cmd import build_player_payload
from shared.session import get_session


class LeaderboardPlayerButton(discord.ui.Button):
    def __init__(self, index: int, player_id: str) -> None:
        super().__init__(
            label=f"Player {index}",
            style=discord.ButtonStyle.secondary,
            custom_id=f"leaderboard_player_{index}",
        )
        self.player_id = player_id

    async def callback(self, interaction: discord.Interaction) -> None:
        session = await get_session(interaction)
        if not session:
            if interaction.response.is_done():
                await interaction.followup.send("Bot not ready.", ephemeral=True)
            else:
                await interaction.response.send_message(
                    "Bot not ready.", ephemeral=True
                )
            return

        await interaction.response.defer(ephemeral=True)

        embed, view, rank_file, error = await build_player_payload(
            session, self.player_id
        )
        if error:
            await interaction.followup.send(error, ephemeral=True)
            return

        await interaction.followup.send(
            embed=embed,
            view=view,
            file=rank_file,
            ephemeral=True,
            allowed_mentions=discord.AllowedMentions.none(),
        )


class LeaderboardPlayersView(discord.ui.View):
    def __init__(self, player_ids: Iterable[str]) -> None:
        super().__init__(timeout=300)
        self.message: Optional[discord.Message] = None
        ids: List[str] = [player_id for player_id in player_ids if player_id]
        for index, player_id in enumerate(ids, start=1):
            self.add_item(LeaderboardPlayerButton(index, player_id))

    async def on_timeout(self) -> None:
        for item in self.children:
            if isinstance(item, discord.ui.Button):
                item.disabled = True
        if self.message:
            await self.message.edit(view=self)
