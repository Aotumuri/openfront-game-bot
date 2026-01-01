from typing import Optional, Tuple

import discord

from info.api import get_bot_author, get_bot_name, get_git_url
from info.embeds import build_info_embed


def build_info_payload() -> Tuple[Optional[discord.Embed], Optional[str]]:
    try:
        bot_name = get_bot_name()
        author = get_bot_author()
        git_url = get_git_url()
    except RuntimeError as exc:
        return None, str(exc)

    embed = build_info_embed(bot_name, author, git_url)
    return embed, None
