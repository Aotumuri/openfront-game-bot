import discord
from discord import app_commands

from info.service import build_info_payload


@app_commands.command(name="info", description="Show bot info.")
async def info_command(interaction: discord.Interaction) -> None:
    embed, error = build_info_payload()
    if error:
        await interaction.response.send_message(error, ephemeral=True)
        return

    await interaction.response.send_message(
        embed=embed,
        ephemeral=True,
        allowed_mentions=discord.AllowedMentions.none(),
    )
