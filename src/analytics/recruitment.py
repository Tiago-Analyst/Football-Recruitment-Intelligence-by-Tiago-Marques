"""Club recruitment metrics and documented profiles."""
from __future__ import annotations

import pandas as pd


def recruitment_profile(row: pd.Series) -> str:
    """Apply evidence-based recruitment labels; thresholds are explicit."""
    labels: list[str] = []
    if row.get("average_recruitment_age", 99) < 23:
        labels.append("Young talent recruiter")
    if row.get("domestic_share", 0) >= 0.60:
        labels.append("Domestic-market recruiter")
    if row.get("international_share", 0) >= 0.60:
        labels.append("International-market recruiter")
    if row.get("u23_share", 0) >= 0.50:
        labels.append("Development-focused recruiter")
    return ", ".join(labels) if labels else "Balanced recruiter"

