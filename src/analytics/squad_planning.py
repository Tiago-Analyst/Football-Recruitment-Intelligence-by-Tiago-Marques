"""Squad composition and alert rules."""
from __future__ import annotations

import pandas as pd


def position_depth_alerts(frame: pd.DataFrame, meaningful_minutes: int = 450) -> pd.DataFrame:
    """Flag positions with only one meaningful contributor."""
    active = frame[frame["minutes"] >= meaningful_minutes]
    depth = active.groupby(["club", "position"]).size().rename("meaningful_players").reset_index()
    depth["alert"] = depth["meaningful_players"].map(
        lambda count: "Limited position depth" if count <= 1 else ""
    )
    return depth[depth["alert"] != ""]


def minute_concentration(minutes: pd.Series, top_n: int = 5) -> float:
    """Return the share of minutes held by the top N players."""
    values = minutes.fillna(0).clip(lower=0)
    return float(values.nlargest(top_n).sum() / values.sum()) if values.sum() else 0.0

