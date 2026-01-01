from typing import Any, Dict

from shared.parsing import parse_int


def get_public_wins_losses(stats: Dict[str, Any], mode: str) -> tuple[int, int]:
    public_stats = stats.get("Public", {})
    mode_stats = public_stats.get(mode, {})
    if not isinstance(mode_stats, dict) or not mode_stats:
        return 0, 0

    wins = 0
    losses = 0
    for difficulty in mode_stats.values():
        if not isinstance(difficulty, dict):
            continue
        wins += parse_int(difficulty.get("wins"))
        losses += parse_int(difficulty.get("losses"))
    return wins, losses
