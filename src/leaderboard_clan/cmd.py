from typing import Optional

import discord
from discord import app_commands
from leaderboard_clan.api import fetch_clan_leaderboard_payload
from leaderboard_clan.embeds import (
    build_clan_leaderboard_embed,
    build_clan_leaderboard_embed_for_tag,
)
from shared.session import get_session


@app_commands.command(
    name="leaderboard_clan", description="Show the OpenFront clan leaderboard."
)
@app_commands.describe(
    clan_metric="ranking metric for clans",
    clan_tag="show this clan and 4 above/below",
)
@app_commands.choices(
    clan_metric=[
        app_commands.Choice(name="weighted_wlr", value="weightedWLRatio"),
        app_commands.Choice(name="wins", value="wins"),
        app_commands.Choice(name="games", value="games"),
    ]
)
async def leaderboard_clan_command(
    interaction: discord.Interaction,
    clan_metric: app_commands.Choice[str] | None = None,
    clan_tag: str | None = None,
) -> None:
    session = await get_session(interaction)
    if not session:
        await interaction.response.send_message("Bot not ready.", ephemeral=True)
        return

    data, error = await fetch_clan_leaderboard_payload(session)
    if error:
        await interaction.response.send_message(error, ephemeral=True)
        return

    metric = _resolve_metric(clan_metric)
    embed, error = _build_embed(data, metric, clan_tag)
    if error:
        await interaction.response.send_message(error, ephemeral=True)
        return

    await interaction.response.send_message(
        embed=embed, allowed_mentions=discord.AllowedMentions.none()
    )


def _resolve_metric(clan_metric: app_commands.Choice[str] | None) -> str:
    return clan_metric.value if clan_metric else "weightedWLRatio"


def _build_embed(
    data: dict,
    metric: str,
    clan_tag: str | None,
) -> tuple[Optional[discord.Embed], Optional[str]]:
    if not clan_tag:
        return build_clan_leaderboard_embed(data, metric=metric), None

    return build_clan_leaderboard_embed_for_tag(data, metric, clan_tag)
