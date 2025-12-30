import datetime as dt
from typing import Any, Dict, Optional

import discord

from shared.maps import MAP_KEY_TO_DISPLAY


def format_ts(ms: Optional[int]) -> str:
    if not ms:
        return "N/A"
    timestamp = dt.datetime.fromtimestamp(ms / 1000, tz=dt.timezone.utc)
    return timestamp.strftime("%Y-%m-%d %H:%M:%S UTC")


def format_duration(seconds: Optional[int]) -> str:
    if seconds is None:
        return "N/A"
    minutes, sec = divmod(int(seconds), 60)
    hours, minutes = divmod(minutes, 60)
    if hours:
        return f"{hours}h {minutes}m {sec}s"
    if minutes:
        return f"{minutes}m {sec}s"
    return f"{sec}s"


def parse_winner(info: Dict[str, Any]) -> Optional[str]:
    winner = info.get("winner")
    if not winner:
        return None
    players = info.get("players", [])
    id_to_name = {p.get("clientID"): p.get("username") for p in players}

    if isinstance(winner, list) and len(winner) >= 2 and winner[0] == "team":
        player_ids = [str(item) for item in winner[2:]]
        names = [id_to_name.get(pid, pid) for pid in player_ids]
        return ", ".join(names) if names else "N/A"

    if isinstance(winner, list) and len(winner) >= 2 and winner[0] == "player":
        client_id = winner[1]
        return id_to_name.get(client_id, client_id)

    if isinstance(winner, list):
        return " ".join(str(item) for item in winner)

    return str(winner)


def count_active_players(players: list[Dict[str, Any]]) -> int:
    return sum("stats" in player for player in players)


def build_embed(
    data: Dict[str, Any], game_id: str, thumbnail_name: Optional[str]
) -> discord.Embed:
    info = data.get("info", {})
    config = info.get("config", {})
    players = info.get("players", [])
    winner = parse_winner(info)

    map_key = config.get("gameMap")
    map_display = MAP_KEY_TO_DISPLAY.get(map_key, map_key or "N/A")

    embed = discord.Embed(
        title="OpenFront Game Summary",
        url=f"https://openfront.io/#join={game_id}",
        color=0x1F8B4C,
    )
    if thumbnail_name:
        embed.set_thumbnail(url=f"attachment://{thumbnail_name}")
    embed.add_field(name="Game ID", value=game_id, inline=True)
    embed.add_field(name="Mode", value=config.get("gameMode", "N/A"), inline=True)
    embed.add_field(name="Map", value=map_display, inline=True)
    embed.add_field(name="Difficulty", value=config.get("difficulty", "N/A"), inline=True)
    embed.add_field(name="Start", value=format_ts(info.get("start")), inline=True)
    embed.add_field(name="End", value=format_ts(info.get("end")), inline=True)
    embed.add_field(name="Duration", value=format_duration(info.get("duration")), inline=True)
    embed.add_field(name="Winner", value=winner or "N/A", inline=True)
    embed.add_field(
        name="Players",
        value=f"{count_active_players(players)}/{config.get('maxPlayers', 'N/A')}",
        inline=True,
    )
    embed.add_field(name="Bots", value=str(config.get("bots", "N/A")), inline=True)
    embed.add_field(name="Turns", value=str(info.get("num_turns", "N/A")), inline=True)
    embed.add_field(
        name="Game Type",
        value=config.get("gameType", "N/A"),
        inline=True,
    )
    embed.set_footer(text=f"Lobby created: {format_ts(info.get('lobbyCreatedAt'))}")
    return embed
