"""Transfer classifications and aggregations."""
from __future__ import annotations

import pandas as pd


def fee_status(fee: float | None) -> str:
    """Classify fee availability without claiming zero means free or loan."""
    if fee is None or pd.isna(fee) or float(fee) <= 0:
        return "unknown_or_zero"
    return "reported_positive"


def transfer_window(month: int) -> str:
    """Map a calendar month to a transparent broad transfer window."""
    if month in (6, 7, 8, 9):
        return "Summer"
    if month in (1, 2):
        return "Winter"
    return "Outside main windows"


def aggregate_pathways(frame: pd.DataFrame) -> pd.DataFrame:
    """Aggregate source-to-destination country/competition pathways."""
    if frame.empty:
        return pd.DataFrame(
            columns=["source_country", "destination_country", "transfer_count", "average_fee_eur"]
        )
    return (
        frame.groupby(["source_country", "destination_country"], dropna=False)
        .agg(transfer_count=("player_key", "size"), average_fee_eur=("transfer_fee_eur", "mean"))
        .reset_index()
    )

