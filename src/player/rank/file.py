import io
from typing import Dict

import discord

from player.rank.convert_png import build_rank_png
from player.rank.rank_svg import get_rank_progress


def build_rank_file(score: float, thresholds: Dict[str, float]) -> discord.File:
    rank, progress = get_rank_progress(score, thresholds)
    png_bytes = build_rank_png(rank, progress)
    buffer = io.BytesIO(png_bytes)
    return discord.File(buffer, filename="rank.png")
