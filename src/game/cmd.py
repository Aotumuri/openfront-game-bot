import discord
from discord import app_commands

from game.message_parser import extract_game_ids


@app_commands.command(name="game", description="Fetch an OpenFront game summary by ID.")
@app_commands.describe(game_id="Game ID or join URL (https://openfront.io/#join=...)")
async def game_command(interaction: discord.Interaction, game_id: str) -> None:
    extracted = extract_game_ids(game_id)
    if extracted:
        game_id = extracted[0]

    client = interaction.client
    controller = getattr(client, "controller", None)
    if not controller:
        await interaction.response.send_message("Bot not ready.", ephemeral=True)
        return

    payload = await controller.build_game_message(game_id)
    if not payload:
        await interaction.response.send_message("Game not found.", ephemeral=True)
        return

    embed, view, thumbnail_file = payload
    if thumbnail_file:
        await interaction.response.send_message(
            embed=embed, view=view, file=thumbnail_file
        )
    else:
        await interaction.response.send_message(embed=embed, view=view)
