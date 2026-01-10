from typing import Iterable

import discord


def build_info_embed(
    bot_name: str,
    author: str,
    git_url: str,
    contributors: Iterable[str],
    is_dev: bool = False,
) -> discord.Embed:
    embed = discord.Embed(
        title="OpenFront Bot Info",
        color=0x1F8B4C,
    )
    embed.add_field(name="Bot Name", value=bot_name, inline=False)
    embed.add_field(name="Author", value=author, inline=False)
    if contributors:
        embed.add_field(name="Contributors", value="\n".join(contributors), inline=False)
    if is_dev:
        embed.add_field(
            name="Mode",
            value="This is the development build.",
            inline=False,
        )
    embed.add_field(name="Git", value=git_url, inline=False)
    embed.set_footer(text="Please give me chocolate!")
    return embed
