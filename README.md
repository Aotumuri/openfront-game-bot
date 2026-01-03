# openfront-game-bot

Discord bot that detects OpenFront join links and posts a game summary embed.

## Setup

Install `uv` (Python package manager). Details: https://github.com/astral-sh/uv

Requires Python 3.11+ (managed by `uv`).

```sh
# macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

Then install dependencies:

```sh
uv sync
```

Create a `.env` file based on `.env.example`:

## Usage

```sh
uv run python src/bot.py
```

Slash commands:
- `/game` fetches a game summary.
- `/player` fetches a player summary.
- `/leaderboard` shows the public player leaderboard.
- `/leaderboard_clan` shows the public clan leaderboard. Supports `weighted_wlr`, `wins`, or `games`.
- `/info` shows bot info (name, author, git link).
- `/clan` fetches a clan summary.

Rank images are rendered via `Pillow`.

The bot listens for links like `https://openfront.io/#join=1xkMyV4S` and queries
`OPENFRONT_GAME_API_URL` must include `{game_id}` (full endpoint template).
If the API returns `{"error":"Not found"}`, it does nothing.

## resource/map License

resource/map is used under OpenFront's CC BY-SA 4.0 license.

## Source Code (src) - MIT License

Source code in the `src/` directory is licensed under the MIT License.
