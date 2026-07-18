"""Player profile timeline helpers."""
from __future__ import annotations

import pandas as pd


def chronological_timeline(*frames: pd.DataFrame) -> pd.DataFrame:
    """Combine profile events with a stable chronological sort."""
    non_empty = [frame for frame in frames if not frame.empty]
    if not non_empty:
        return pd.DataFrame(columns=["date", "event_type", "description"])
    return pd.concat(non_empty, ignore_index=True).sort_values("date", kind="stable")
