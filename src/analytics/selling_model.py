"""Selling model calculations."""
from __future__ import annotations

import pandas as pd


def selling_profile(row: pd.Series) -> str:
    """Assign documented labels from sale volume, age and destination mix."""
    labels: list[str] = []
    if row.get("sales_count", 0) >= 10:
        labels.append("High-volume seller")
    if row.get("average_sale_age", 99) < 24:
        labels.append("Young-player seller")
    if row.get("international_share", 0) >= 0.60:
        labels.append("International exporter")
    if row.get("known_sales_eur", 0) >= 50_000_000:
        labels.append("Elite-talent seller")
    return ", ".join(labels) if labels else "Balanced seller"

