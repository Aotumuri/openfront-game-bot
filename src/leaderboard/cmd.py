import discord
from discord import app_commands

from leaderboard.service import build_leaderboard_payload
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

    embed, view, error = await build_leaderboard_payload(session)
    if error:
        await interaction.response.send_message(error, ephemeral=True)
        return
    if not embed or not view:
        await interaction.response.send_message(
            "Leaderboard not available.", ephemeral=True
        )
        return
    await interaction.response.send_message(
        embed=embed,
        view=view,
        allowed_mentions=discord.AllowedMentions.none(),
    )
    view.message = await interaction.original_response()
