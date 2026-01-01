import discord
from discord import app_commands

from clan.service import build_clan_payload
from shared.session import get_session


@app_commands.command(name="clan", description="Fetch an OpenFront clan summary.")
@app_commands.describe(clan_name="Clan name or tag")
async def clan_command(interaction: discord.Interaction, clan_name: str) -> None:
    session = await get_session(interaction)
    if not session:
        await interaction.response.send_message("Bot not ready.", ephemeral=True)
        return

    await interaction.response.defer()
    embed, error = await build_clan_payload(session, clan_name)
    if error:
        await interaction.followup.send(error, ephemeral=True)
        return

    await interaction.followup.send(embed=embed)
