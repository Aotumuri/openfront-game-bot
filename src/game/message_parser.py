import re
from typing import List

import discord

JOIN_RE = re.compile(r"https?://openfront\.io/#join=([A-Za-z0-9]+)")


def should_ignore_message(message: discord.Message) -> bool:
    return message.author.bot


def extract_game_ids(content: str) -> List[str]:
    return [match.group(1) for match in JOIN_RE.finditer(content)]
