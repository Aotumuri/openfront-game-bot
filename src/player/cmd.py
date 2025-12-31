from typing import Any, Dict, Optional, Tuple

import discord
from discord import app_commands

from player.api import fetch_player
from player.embeds import build_player_embed
from player.rank.file import build_rank_file
from player.rank.rank_svg import parse_rank_thresholds
from player.score import calculate_score
from shared.session import get_session
from player.views import build_recent_games_view


async def build_player_payload(
    session: Any, player_id: str
) -> Tuple[
    Optional[discord.Embed],
    Optional[discord.ui.View],
    Optional[discord.File],
    Optional[str],
]:
    try:
        data = await fetch_player(session, player_id)
    except RuntimeError:
        return None, None, None, "OPENFRONT_PLAYER_API_URL is not set."
    if not data:
        return None, None, None, "Player not found."

    stats = data.get("stats", {})
    try:
        score = calculate_score(stats)
        thresholds = parse_rank_thresholds()
    except (KeyError, RuntimeError) as exc:
        return None, None, None, str(exc)
    except ValueError:
        return None, None, None, "Env vars must be valid numbers."

    embed = build_player_embed(data, player_id, score)
    view = build_recent_games_view(data)
    rank_file = build_rank_file(score, thresholds)
    return embed, view, rank_file, None


@app_commands.command(
    name="player", description="Fetch an OpenFront player summary by ID."
)
@app_commands.describe(player_id="Player ID")
async def player_command(interaction: discord.Interaction, player_id: str) -> None:
    session = await get_session(interaction)
    if not session:
        await interaction.response.send_message("Bot not ready.", ephemeral=True)
        return

    embed, view, rank_file, error = await build_player_payload(session, player_id)
    if error:
        await interaction.response.send_message(error, ephemeral=True)
        return

    await interaction.response.send_message(embed=embed, view=view, file=rank_file)
