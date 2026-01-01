from typing import Any, Dict

import discord

from shared.parsing import parse_int


def build_clan_embed(
    data: Dict[str, Any],
    clan_name: str,
    wlr_rank: int | None,
    wins_rank: int | None,
    games_rank: int | None,
) -> discord.Embed:
    clan = data.get("clan", {})
    tag = clan.get("clanTag") or clan_name
    games = parse_int(clan.get("games"))
    sessions = parse_int(clan.get("playerSessions"))
    wins = parse_int(clan.get("wins"))
    losses = parse_int(clan.get("losses"))
    ratio_value = wins / losses if losses else float(wins) if wins else 0.0
    ratio_text = f"{ratio_value:.2f}"
    wlr_label = f"Rank {wlr_rank}" if wlr_rank else "Unranked"
    ratio_text = f"{ratio_text} ({wlr_label})"

    embed = discord.Embed(
        title="OpenFront Clan Summary",
        color=0x1F8B4C,
    )
    embed.add_field(name="Clan", value=tag, inline=True)
    games_label = f"Rank {games_rank}" if games_rank else "Unranked"
    wins_label = f"Rank {wins_rank}" if wins_rank else "Unranked"
    games_text = f"{games} ({games_label})"
    wins_text = f"{wins} ({wins_label})"

    embed.add_field(name="Games", value=games_text, inline=True)
    embed.add_field(name="Wins", value=wins_text, inline=True)
    embed.add_field(name="Losses", value=str(losses), inline=True)
    embed.add_field(name="Player Sessions", value=str(sessions), inline=True)
    embed.add_field(name="WLR", value=ratio_text, inline=True)
    return embed
