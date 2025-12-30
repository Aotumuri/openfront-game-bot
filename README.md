# openfront-game-bot

Discord bot that detects OpenFront join links and posts a game summary embed.

## Usage

```sh
uv sync
uv run python src/bot.py
```

Create a `.env` file with your bot token and API URL:

```sh
DISCORD_TOKEN=your-token-here
OPENFRONT_GAME_API_URL=https://api.openfront.io/game/{game_id}
```

The bot listens for links like `https://openfront.io/#join=1xkMyV4S` and queries
`OPENFRONT_GAME_API_URL` must include `{game_id}` (full endpoint template).
If the API returns `{"error":"Not found"}`, it does nothing.

## resource/map License

resource/map is used under OpenFront's CC BY-SA 4.0 license.

## Source Code (src) - MIT License

Source code in the `src/` directory is licensed under the MIT License.
