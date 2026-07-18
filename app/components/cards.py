"""KPI card helpers."""
from __future__ import annotations

import math

import streamlit as st

from app.i18n import tr


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
