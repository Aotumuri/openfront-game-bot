import discord
from discord import app_commands

from leaderboard.api import fetch_leaderboard
from leaderboard.embeds import build_leaderboard_embed
from leaderboard.view import LeaderboardPlayersView
from shared.session import get_session


@app_commands.command(
    name="leaderboard", description="Show the OpenFront player leaderboard."
)
async def leaderboard_command(
    interaction: discord.Interaction,
) -> None:
    session = await get_session(interaction)
    if not session:
        await interaction.response.send_message("Bot not ready.", ephemeral=True)
        return

    try:
        data = await fetch_leaderboard(session)
    except RuntimeError as exc:
        await interaction.response.send_message(str(exc), ephemeral=True)
        return
    if not data:
        await interaction.response.send_message(
            "Leaderboard not available.", ephemeral=True
        )
        return

    embed = build_leaderboard_embed(data)
    player_ids = [entry.get("public_id") for entry in data[:10]]
    view = LeaderboardPlayersView(player_ids)
    await interaction.response.send_message(
        embed=embed,
        view=view,
        allowed_mentions=discord.AllowedMentions.none(),
    )
    view.message = await interaction.original_response()
