# openfront-game-bot

Discord bot that detects OpenFront join links and posts a game summary embed.

## Usage

```sh
uv sync
uv run python src/bot.py
```

Slash commands:
- `/game` fetches a game summary.
- `/player` fetches a player summary.

Create a `.env` file with your bot token and API URL:

```sh
DISCORD_TOKEN=your-token-here
OPENFRONT_GAME_API_URL=https://api.openfront.io/game/{game_id}
OPENFRONT_PLAYER_API_URL=https://api.openfront.io/player/{player_id}
OPENFRONT_SCORE_WIN_WEIGHT=1.0
OPENFRONT_SCORE_LOSS_WEIGHT=1.0
OPENFRONT_SCORE_SINGLE_SCALE=1.0
OPENFRONT_SCORE_TEAM_SCALE=1.0
OPENFRONT_SCORE_SINGLE_GAME_BONUS=0.0
OPENFRONT_SCORE_TEAM_GAME_BONUS=0.0
```

The bot listens for links like `https://openfront.io/#join=1xkMyV4S` and queries
`OPENFRONT_GAME_API_URL` must include `{game_id}` (full endpoint template).
If the API returns `{"error":"Not found"}`, it does nothing.

## resource/map License

resource/map is used under OpenFront's CC BY-SA 4.0 license.

## Source Code (src) - MIT License

Source code in the `src/` directory is licensed under the MIT License.
