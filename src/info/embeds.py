import discord


def build_info_embed(bot_name: str, author: str, git_url: str) -> discord.Embed:
    embed = discord.Embed(
        title="OpenFront Bot Info",
        color=0x1F8B4C,
    )
    embed.add_field(name="Bot Name", value=bot_name, inline=False)
    embed.add_field(name="Author", value=author, inline=False)
    embed.add_field(name="Git", value=git_url, inline=False)
    embed.set_footer(text="Please give me chocolate!")
    return embed
