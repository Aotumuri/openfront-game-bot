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
- `/leaderboard` shows the public player leaderboard.
- `/leaderboard_clan` shows the public clan leaderboard. Supports `weighted_wlr`, `wins`, or `games`.
- `/info` shows bot info (name, author, git link).
- `/clan` fetches a clan summary.

Rank images require `rsvg-convert` on your PATH.
Install on macOS: `brew install librsvg`

Create a `.env` file with the required token and API URLs:

```sh
DISCORD_TOKEN=your-token-here
OPENFRONT_GAME_API_URL=https://api.openfront.io/game/{game_id}
OPENFRONT_PLAYER_API_URL=https://api.openfront.io/player/{player_id}
OPENFRONT_LEADERBOARD_API_URL=https://api.openfront.io/leaderboard/public/ffa
OPENFRONT_CLAN_LEADERBOARD_API_URL=https://api.openfront.io/public/clans/leaderboard
OPENFRONT_CLAN_API_URL=https://api.openfront.io/public/clan/{clan_name}
OPENFRONT_RANK_THRESHOLDS=E:0,D:100,C:200,B:400,A:700,S:1000
OPENFRONT_SCORE_WIN_WEIGHT=10.0
OPENFRONT_SCORE_LOSS_WEIGHT=1.0
OPENFRONT_SCORE_SINGLE_SCALE=0.4
OPENFRONT_SCORE_TEAM_SCALE=0.1
OPENFRONT_SCORE_SINGLE_GAME_BONUS=0.6
OPENFRONT_SCORE_TEAM_GAME_BONUS=0.2
OPENFRONT_BOT_NAME=OpenFrontStatus
OPENFRONT_BOT_AUTHOR=your-name-here
OPENFRONT_BOT_GIT_URL=https://github.com/your/repo
```

The bot listens for links like `https://openfront.io/#join=1xkMyV4S` and queries
`OPENFRONT_GAME_API_URL` must include `{game_id}` (full endpoint template).
If the API returns `{"error":"Not found"}`, it does nothing.

## resource/map License

resource/map is used under OpenFront's CC BY-SA 4.0 license.

## Source Code (src) - MIT License

Source code in the `src/` directory is licensed under the MIT License.
