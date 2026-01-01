from typing import Any, Dict, List, Optional

import discord

from shared.parsing import parse_float, parse_int
from shared.time import format_iso


def _sort_key(entry: Dict[str, Any], metric: str) -> float:
    if metric == "weightedWLRatio":
        value = parse_float(entry.get("weightedWLRatio"))
    elif metric == "wins":
        value = parse_int(entry.get("wins"))
    elif metric == "games":
        value = parse_int(entry.get("games"))
    else:
        value = parse_int(entry.get("wins"))
    return float(value) if value is not None else 0.0


def sort_clans(data: Dict[str, Any], metric: str) -> List[Dict[str, Any]]:
    clans = data.get("clans")
    if not isinstance(clans, list):
        return []
    return sorted(clans, key=lambda entry: _sort_key(entry, metric), reverse=True)


def build_clan_leaderboard_embed(
    data: Dict[str, Any],
    limit: int = 10,
    metric: str = "weightedWLRatio",
    entries: Optional[List[Dict[str, Any]]] = None,
    start_rank: int = 1,
    highlight_tag: Optional[str] = None,
) -> discord.Embed:
    embed = discord.Embed(
        title="OpenFront Clan Leaderboard",
        color=0x1F8B4C,
    )
    clans = entries if entries is not None else sort_clans(data, metric)
    if not clans:
        embed.description = "No clan leaderboard data available."
        return embed

    lines: List[str] = []
    for index, entry in enumerate(clans[:limit], start=start_rank):
        tag = entry.get("clanTag") or "Unknown"
        display_tag = tag
        highlight = False
        if highlight_tag and str(tag).upper() == highlight_tag.upper():
            highlight = True
        wins = parse_int(entry.get("wins"))
        losses = parse_int(entry.get("losses"))
        games = parse_int(entry.get("games"))
        ratio = parse_float(entry.get("weightedWLRatio"))
        ratio_text = f"{ratio:.2f}" if ratio is not None else "N/A"
        line = (
            f"{index}) [{display_tag}] - WLR {ratio_text} | {wins}W/{losses}L ({games})"
        )
        if highlight:
            line = f"**{line}**"
        lines.append(line)

    embed.description = "\n".join(lines)
    start = format_iso(data.get("start"))
    end = format_iso(data.get("end"))
    label_map = {
        "weightedWLRatio": "WLR",
        "wins": "Wins",
        "games": "Games",
    }
    label = label_map.get(metric, "Wins")
    embed.set_footer(text=f"Ranked by {label} | Period: {start} - {end}")
    return embed


def build_clan_leaderboard_embed_for_tag(
    data: Dict[str, Any],
    metric: str,
    clan_tag: str,
) -> tuple[Optional[discord.Embed], Optional[str]]:
    tag = clan_tag.upper()
    sorted_clans = sort_clans(data, metric)
    match_index = next(
        (
            index
            for index, entry in enumerate(sorted_clans)
            if str(entry.get("clanTag", "")).upper() == tag
        ),
        None,
    )
    if match_index is None:
        return None, f"Clan {tag} not found."

    start = max(match_index - 4, 0)
    end = min(match_index + 5, len(sorted_clans))
    window = sorted_clans[start:end]
    return (
        build_clan_leaderboard_embed(
            data,
            metric=metric,
            entries=window,
            start_rank=start + 1,
            highlight_tag=tag,
        ),
        None,
    )
