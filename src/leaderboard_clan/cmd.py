from typing import Optional

import discord
from discord import app_commands
from leaderboard_clan.service import fetch_clan_leaderboard_payload
from leaderboard_clan.embeds import (
    build_clan_leaderboard_embed,
    build_clan_leaderboard_embed_for_tag,
    sort_clans,
)
from leaderboard_clan.view import LeaderboardClansView
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
        app_commands.Choice(name="weightedWLRatio", value="weightedWLRatio"),
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
    embed, clans, error = _build_embed_and_clans(data, metric, clan_tag)
    if error:
        await interaction.response.send_message(error, ephemeral=True)
        return

    clan_tags = [str(entry.get("clanTag") or "").strip() for entry in clans]
    view = LeaderboardClansView(clan_tags)
    await interaction.response.send_message(
        embed=embed,
        view=view,
        allowed_mentions=discord.AllowedMentions.none(),
    )
    view.message = await interaction.original_response()


def _resolve_metric(clan_metric: app_commands.Choice[str] | None) -> str:
    return clan_metric.value if clan_metric else "weightedWLRatio"


def _build_embed_and_clans(
    data: dict,
    metric: str,
    clan_tag: str | None,
) -> tuple[Optional[discord.Embed], list[dict], Optional[str]]:
    if not clan_tag:
        clans = sort_clans(data, metric)[:10]
        return build_clan_leaderboard_embed(data, metric=metric), clans, None

    embed, error = build_clan_leaderboard_embed_for_tag(data, metric, clan_tag)
    if error or not embed:
        return None, [], error
    sorted_clans = sort_clans(data, metric)
    tag = clan_tag.upper()
    match_index = next(
        (
            index
            for index, entry in enumerate(sorted_clans)
            if str(entry.get("clanTag", "")).upper() == tag
        ),
        None,
    )
    if match_index is None:
        return embed, [], None
    start = max(match_index - 4, 0)
    end = min(match_index + 5, len(sorted_clans))
    return embed, sorted_clans[start:end], None
