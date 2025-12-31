from typing import Any, Dict, Optional

from player.recent_view import RecentGamesView


def build_recent_games_view(data: Dict[str, Any]) -> Optional[RecentGamesView]:
    games = data.get("games", [])
    game_ids = [game.get("gameId") for game in games[:5]]
    return RecentGamesView(game_ids) if game_ids else None
