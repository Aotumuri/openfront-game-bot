from typing import Iterable, List, Optional

import discord

from clan.service import build_clan_payload
from shared.session import get_session


class LeaderboardClanButton(discord.ui.Button):
    def __init__(self, clan_tag: str) -> None:
        super().__init__(
            label=clan_tag,
            style=discord.ButtonStyle.secondary,
            custom_id=f"leaderboard_clan_{clan_tag}",
        )
        self.clan_tag = clan_tag

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
        embed, error = await build_clan_payload(session, self.clan_tag)
        if error:
            await interaction.followup.send(error, ephemeral=True)
            return

        await interaction.followup.send(
            embed=embed,
            ephemeral=True,
            allowed_mentions=discord.AllowedMentions.none(),
        )


class LeaderboardClansView(discord.ui.View):
    def __init__(self, clan_tags: Iterable[str]) -> None:
        super().__init__(timeout=300)
        self.message: Optional[discord.Message] = None
        tags: List[str] = [tag for tag in clan_tags if tag]
        for tag in tags:
            self.add_item(LeaderboardClanButton(tag))

    async def on_timeout(self) -> None:
        for item in self.children:
            if isinstance(item, discord.ui.Button):
                item.disabled = True
        if self.message:
            await self.message.edit(view=self)
