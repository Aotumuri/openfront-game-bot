from typing import Any, Dict

import discord
from discord import app_commands

from player.api import fetch_player
from player.embeds import build_player_embed
from player.rank.file import build_rank_file
from player.rank.rank_svg import parse_rank_thresholds
from player.score import calculate_score
from player.session import get_session
from player.views import build_recent_games_view


@app_commands.command(
    name="player", description="Fetch an OpenFront player summary by ID."
)
@app_commands.describe(player_id="Player ID")
async def player_command(interaction: discord.Interaction, player_id: str) -> None:
    session = await get_session(interaction)
    if not session:
        await interaction.response.send_message("Bot not ready.", ephemeral=True)
        return

    try:
        data = await fetch_player(session, player_id)
    except RuntimeError:
        await interaction.response.send_message(
            "OPENFRONT_PLAYER_API_URL is not set.", ephemeral=True
        )
        return
    if not data:
        await interaction.response.send_message("Player not found.", ephemeral=True)
        return

    stats = data.get("stats", {})
    try:
        score = calculate_score(stats)
        thresholds = parse_rank_thresholds()
    except (KeyError, RuntimeError) as exc:
        await interaction.response.send_message(str(exc), ephemeral=True)
        return
    except ValueError:
        await interaction.response.send_message(
            "Env vars must be valid numbers.", ephemeral=True
        )
        return

    embed = build_player_embed(data, player_id, score)
    view = build_recent_games_view(data)
    rank_file = build_rank_file(score, thresholds)
    await interaction.response.send_message(embed=embed, view=view, file=rank_file)
