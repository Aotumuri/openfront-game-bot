from typing import Any, Dict, List

import discord

from player.stats import get_public_wins_losses
from shared.time import format_iso


def build_recent_games(games: List[Dict[str, Any]], limit: int = 5) -> str:
    if not games:
        return "N/A"
    lines = []
    for index, game in enumerate(games[:limit], start=1):
        start = format_iso(game.get("start", ""))
        mode = game.get("mode", "N/A")
        game_type = game.get("type", "N/A")
        game_map = game.get("map", "N/A")
        difficulty = game.get("difficulty", "N/A")
        game_id = game.get("gameId", "N/A")
        lines.append(
            f"{index}. {start} | {mode} | {game_type} | {game_map} | {difficulty} | {game_id}"
        )
    return "\n".join(lines)


def sum_public_results(stats: Dict[str, Any], mode: str) -> str:
    wins, losses = get_public_wins_losses(stats, mode)
    if not wins and not losses:
        return "N/A"
    total = wins + losses
    win_rate = (wins / total * 100) if total else 0.0
    return f"{wins}W / {losses}L ({win_rate:.1f}%)"


def build_player_embed(
    data: Dict[str, Any], player_id: str, score: float
) -> discord.Embed:
    games = data.get("games", [])
    created_at = data.get("createdAt", "")
    stats = data.get("stats", {})
    public_ffa = sum_public_results(stats, "Free For All")
    public_team = sum_public_results(stats, "Team")

    embed = discord.Embed(
        title="OpenFront Player Summary",
        color=0x1F8B4C,
    )
    embed.add_field(name="Player ID", value=player_id, inline=False)
    embed.add_field(name="Created", value=format_iso(created_at), inline=False)
    embed.add_field(name="Score", value=f"{score:.2f}", inline=True)
    embed.add_field(name="Public FFA", value=public_ffa, inline=True)
    embed.add_field(name="Public Team", value=public_team, inline=True)
    embed.add_field(name="Recent Games", value=build_recent_games(games), inline=False)
    embed.set_thumbnail(url="attachment://rank.png")
    embed.set_footer(text="Use the buttons below to view game details.")
    return embed
