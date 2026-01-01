import os
from typing import Any, Dict

from player.stats import get_public_wins_losses


def _get_score_weights() -> tuple[float, float, float, float, float, float]:
    win_weight = float(os.environ["OPENFRONT_SCORE_WIN_WEIGHT"])
    loss_weight = float(os.environ["OPENFRONT_SCORE_LOSS_WEIGHT"])
    single_scale = float(os.environ["OPENFRONT_SCORE_SINGLE_SCALE"])
    team_scale = float(os.environ["OPENFRONT_SCORE_TEAM_SCALE"])
    single_game_bonus = float(os.environ["OPENFRONT_SCORE_SINGLE_GAME_BONUS"])
    team_game_bonus = float(os.environ["OPENFRONT_SCORE_TEAM_GAME_BONUS"])
    return (
        win_weight,
        loss_weight,
        single_scale,
        team_scale,
        single_game_bonus,
        team_game_bonus,
    )


def calculate_score(stats: Dict[str, Any]) -> float:
    """
    Score formula:
      (single_wins * WIN - single_losses * LOSS * (1 - single_win_rate)) * SINGLE_SCALE
    + (team_wins * WIN - team_losses * LOSS * (1 - team_win_rate)) * TEAM_SCALE
    + sqrt(single_total) * SINGLE_GAME_BONUS
    + sqrt(team_total) * TEAM_GAME_BONUS
    """
    (
        win_weight,
        loss_weight,
        single_scale,
        team_scale,
        single_game_bonus,
        team_game_bonus,
    ) = _get_score_weights()

    single_wins, single_losses = get_public_wins_losses(stats, "Free For All")
    team_wins, team_losses = get_public_wins_losses(stats, "Team")
    single_total = single_wins + single_losses
    team_total = team_wins + team_losses
    single_win_rate = single_wins / single_total if single_total else 0.0
    team_win_rate = team_wins / team_total if team_total else 0.0
    single_loss_weight = loss_weight * (1 - single_win_rate)
    team_loss_weight = loss_weight * (1 - team_win_rate)

    score = (single_wins * win_weight - single_losses * single_loss_weight) * single_scale
    score += (team_wins * win_weight - team_losses * team_loss_weight) * team_scale
    score += (single_total**0.5) * single_game_bonus
    score += (team_total**0.5) * team_game_bonus
    return score
