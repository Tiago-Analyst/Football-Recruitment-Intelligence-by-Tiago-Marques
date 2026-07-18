"""Transparent youth development indicators."""
from __future__ import annotations

import pandas as pd


def youth_minutes_share(minutes: pd.Series, ages: pd.Series, max_age: int) -> float:
    """Return the share of minutes played by players at or below max_age."""
    valid = minutes.fillna(0).clip(lower=0)
    total = float(valid.sum())
    return float(valid[ages <= max_age].sum() / total) if total else 0.0


def development_index(
    u21_share: float,
    u23_share: float,
    young_players_used: int,
    weights: dict[str, float] | None = None,
) -> float:
    """Calculate a bounded configurable directional index (0-100)."""
    weights = weights or {
        "u21_minutes_share": 0.45,
        "u23_minutes_share": 0.30,
        "young_players_used": 0.25,
    }
    player_component = min(max(young_players_used, 0) / 10, 1)
    raw = (
        weights["u21_minutes_share"] * min(max(u21_share, 0), 1)
        + weights["u23_minutes_share"] * min(max(u23_share, 0), 1)
        + weights["young_players_used"] * player_component
    )
    return round(raw * 100, 2)

