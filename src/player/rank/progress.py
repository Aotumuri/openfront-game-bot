import os
from typing import Dict, Tuple

from player.rank.constants import RANK_ORDER


def parse_rank_thresholds() -> Dict[str, float]:
    raw = os.environ.get("OPENFRONT_RANK_THRESHOLDS")
    if not raw:
        raise RuntimeError("OPENFRONT_RANK_THRESHOLDS is not set")

    thresholds: Dict[str, float] = {}
    pairs = [item.strip() for item in raw.split(",") if item.strip()]
    for pair in pairs:
        if ":" not in pair:
            raise ValueError("OPENFRONT_RANK_THRESHOLDS must be Rank:Score pairs")
        rank, value = [part.strip() for part in pair.split(":", 1)]
        if rank not in RANK_ORDER:
            raise ValueError(f"Unknown rank in OPENFRONT_RANK_THRESHOLDS: {rank}")
        thresholds[rank] = float(value)

    missing = [rank for rank in RANK_ORDER if rank not in thresholds]
    if missing:
        raise ValueError(
            "OPENFRONT_RANK_THRESHOLDS is missing: " + ", ".join(missing)
        )
    return thresholds


def get_rank_progress(score: float, thresholds: Dict[str, float]) -> Tuple[str, float]:
    current_rank = "E"
    for rank in RANK_ORDER:
        if score >= thresholds[rank]:
            current_rank = rank
        else:
            break

    if current_rank == "S":
        return current_rank, 1.0

    current_index = RANK_ORDER.index(current_rank)
    next_rank = RANK_ORDER[current_index + 1]
    current_threshold = thresholds[current_rank]
    next_threshold = thresholds[next_rank]
    if next_threshold <= current_threshold:
        return current_rank, 0.0

    progress = (score - current_threshold) / (next_threshold - current_threshold)
    progress = max(0.0, min(1.0, progress))
    return current_rank, progress
