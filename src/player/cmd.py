import discord
from discord import app_commands

from player.api import fetch_player
from player.embeds import build_player_embed
from player.score import calculate_score
from player.recent_view import RecentGamesView


@app_commands.command(
    name="player", description="Fetch an OpenFront player summary by ID."
)
@app_commands.describe(player_id="Player ID")
async def player_command(interaction: discord.Interaction, player_id: str) -> None:
    client = interaction.client
    controller = getattr(client, "controller", None)
    session = getattr(controller, "http_session", None)

    if controller and not session:
        await controller.setup()
        session = getattr(controller, "http_session", None)

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
    except KeyError as exc:
        await interaction.response.send_message(
            f"Missing env var: {exc.args[0]}", ephemeral=True
        )
        return
    except ValueError:
        await interaction.response.send_message(
            "Score env vars must be numbers.", ephemeral=True
        )
        return

    embed = build_player_embed(data, player_id, score)
    games = data.get("games", [])
    game_ids = [game.get("gameId") for game in games[:5]]
    view = RecentGamesView(game_ids) if game_ids else None
    await interaction.response.send_message(embed=embed, view=view)
