from typing import Any, Optional, Tuple

import discord

from clan.api import fetch_clan, fetch_clan_leaderboard
from clan.embeds import build_clan_embed
from shared.parsing import parse_float, parse_int


def _weighted_ratio(entry: dict) -> float:
    ratio = parse_float(entry.get("weightedWLRatio"))
    return ratio if ratio is not None else 0.0


def _find_rank(
    leaderboard: dict, clan_tag: str, key_fn
) -> int | None:
    clans = leaderboard.get("clans")
    if not isinstance(clans, list):
        return None
    sorted_clans = sorted(clans, key=key_fn, reverse=True)
    for index, entry in enumerate(sorted_clans, start=1):
        tag = str(entry.get("clanTag", "")).upper()
        if tag == clan_tag.upper():
            return index
    return None


async def build_clan_payload(
    session: Any, clan_name: str
) -> Tuple[Optional[discord.Embed], Optional[str]]:
    try:
        data = await fetch_clan(session, clan_name)
    except RuntimeError as exc:
        return None, str(exc)
    if not data or "clan" not in data:
        return None, "Clan not found."

    wlr_rank = None
    wins_rank = None
    games_rank = None
    try:
        leaderboard = await fetch_clan_leaderboard(session)
    except RuntimeError:
        leaderboard = None
    if leaderboard:
        tag = str(data.get("clan", {}).get("clanTag", "")).strip()
        if tag:
            wlr_rank = _find_rank(leaderboard, tag, _weighted_ratio)
            wins_rank = _find_rank(
                leaderboard, tag, lambda entry: parse_int(entry.get("wins"))
            )
            games_rank = _find_rank(
                leaderboard, tag, lambda entry: parse_int(entry.get("games"))
            )

    embed = build_clan_embed(
        data,
        clan_name,
        wlr_rank,
        wins_rank,
        games_rank,
    )
    return embed, None
