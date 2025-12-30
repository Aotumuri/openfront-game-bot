import discord


def build_view(game_id: str) -> discord.ui.View:
    view = discord.ui.View()
    view.add_item(
        discord.ui.Button(
            label="view replay",
            url=f"https://openfront.io/#join={game_id}",
        )
    )
    return view
