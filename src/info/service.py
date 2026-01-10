import os
from typing import Optional, Tuple

import discord

from info.constants import (
    BOT_AUTHOR,
    BOT_CONTRIBUTORS_RAW,
    BOT_GIT_URL,
    BOT_NAME,
)
from info.embeds import build_info_embed


def build_info_payload() -> Tuple[Optional[discord.Embed], Optional[str]]:
    contributors = [
        item.strip()
        for item in BOT_CONTRIBUTORS_RAW.split(",")
        if item.strip()
    ]
    is_dev = os.getenv("OPENFRONT_BOT_MODE") == "dev"
    embed = build_info_embed(BOT_NAME, BOT_AUTHOR, BOT_GIT_URL, contributors, is_dev)
    return embed, None
