import random

import discord


def is_chocolate_reaction(reaction: discord.Reaction) -> bool:
    emoji = reaction.emoji
    if isinstance(emoji, str):
        return emoji == "🍫"
    return getattr(emoji, "name", "") == "chocolate_bar"


async def handle_chocolate_reaction(
    reaction: discord.Reaction, user: discord.User | discord.Member
) -> None:
    responses = [
        "Thanks for the chocolate! 🍫",
        "Sweet! You're awesome. 🍫",
        "Chocolate received. Powering up! 🍫",
        "You're the best! 🍫",
        "OpenChocolate! 🍫",
        "Choco-front engaged! 🍫",
    ]
    await reaction.message.channel.send(f"{user.mention} {random.choice(responses)}")
