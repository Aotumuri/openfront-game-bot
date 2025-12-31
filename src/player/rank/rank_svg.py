import os
from typing import Dict, Tuple

RANK_ORDER = ("E", "D", "C", "B", "A", "S")


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


def build_rank_svg(rank: str, progress: float) -> str:
    progress = max(0.0, min(1.0, progress))
    circumference = 2 * 3.141592653589793 * 80
    dash = circumference * progress
    gap = circumference - dash

    colors = {
        "E": "#9aa0a6",
        "D": "#1f8b4c",
        "C": "#2a6fdb",
        "B": "#7a3eb1",
        "A": "#d4a017",
        "S": "#d12f2f",
    }
    stroke = colors.get(rank, "#1f8b4c")
    text_fill = stroke
    
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 200" width="200" height="200">
  <g fill="none" stroke-linecap="round">
    <circle cx="100" cy="100" r="80" stroke="#d0d7de" stroke-width="12" />
    <circle cx="100" cy="100" r="80" stroke="{stroke}" stroke-width="12"
            stroke-dasharray="{dash} {gap}" transform="rotate(-90 100 100)" />
  </g>
  <text x="100" y="112" font-family="Arial, sans-serif" font-size="56"
        font-weight="700" text-anchor="middle" fill="{text_fill}">{rank}</text>
</svg>
"""

