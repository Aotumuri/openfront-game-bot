import discord
from discord import app_commands

from shared.session import get_session
from player.service import build_player_payload


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
