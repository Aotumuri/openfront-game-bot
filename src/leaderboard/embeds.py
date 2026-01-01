from typing import Any, Dict, List

import discord

from shared.parsing import parse_float, parse_int

def _format_leaderboard_name(entry: Dict[str, Any]) -> str:
    user = entry.get("user")
    public_id = entry.get("public_id")
    if isinstance(user, dict):
        user_id = user.get("id")
        if public_id and user_id:
            return f"ID {public_id} (<@{user_id}>)"
    if public_id:
        return f"ID {public_id}"
    return "Unknown"


def build_leaderboard_embed(
    entries: List[Dict[str, Any]], limit: int = 10
) -> discord.Embed:
    embed = discord.Embed(
        title="OpenFront FFA Leaderboard",
        color=0x1F8B4C,
    )
    if not entries:
        embed.description = "No leaderboard data available."
        return embed

    lines = []
    for index, entry in enumerate(entries[:limit], start=1):
        name = _format_leaderboard_name(entry)
        wins = parse_int(entry.get("wins"))
        losses = parse_int(entry.get("losses"))
        total = parse_int(entry.get("total"))
        if not total:
            total = wins + losses
        wlr_value = parse_float(entry.get("wlr"))
        wlr_text = f"{wlr_value:.2f}" if wlr_value is not None else "N/A"
        lines.append(
            f"{index}. {name} - WLR {wlr_text} | {wins}W/{losses}L ({total})"
        )

    embed.description = "\n".join(lines)
    embed.set_footer(text="Source: api.openfront.io")
    return embed
