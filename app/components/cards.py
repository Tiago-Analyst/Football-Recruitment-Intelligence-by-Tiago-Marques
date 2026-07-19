"""KPI card helpers."""
from __future__ import annotations

import math
from datetime import timezone

import streamlit as st

from app.i18n import tr


def format_refresh_time(value: object) -> str:
    """Format a warehouse timestamp consistently in UTC without microseconds."""
    timestamp = value.to_pydatetime() if hasattr(value, "to_pydatetime") else value
    if hasattr(timestamp, "astimezone"):
        timestamp = timestamp.astimezone(timezone.utc)
    return timestamp.strftime("%Y-%m-%d %H:%M UTC")


def compact_number(value: float | int | None, currency: bool = False) -> str:
    """Format counts and euros compactly."""
    if value is None or (isinstance(value, float) and math.isnan(value)):
        return tr("Unavailable", "Indisponível")
    prefix = "€" if currency else ""
    value = float(value)
    if abs(value) >= 1_000_000_000:
        return f"{prefix}{value / 1_000_000_000:.1f}bn"
    if abs(value) >= 1_000_000:
        return f"{prefix}{value / 1_000_000:.1f}m"
    if abs(value) >= 1_000:
        return f"{prefix}{value / 1_000:.1f}k"
    return f"{prefix}{value:,.0f}"


def metric_row(items: list[tuple[str, str, str | None]]) -> None:
    """Render a responsive row of metrics."""
    columns = st.columns(len(items))
    for column, (label, value, help_text) in zip(columns, items, strict=True):
        column.metric(label, value, help=help_text)
