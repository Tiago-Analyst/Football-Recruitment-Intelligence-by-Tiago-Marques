"""Reusable analytical filters."""
from __future__ import annotations

import streamlit as st

from app.i18n import tr


def season_filter(seasons: list[str], key: str = "season") -> list[str]:
    """Render a multi-season filter defaulting to the three latest."""
    ordered = sorted([str(value) for value in seasons], reverse=True)
    return st.multiselect(tr("Season", "Época"), ordered, default=ordered[:3], key=key)


def club_filter(clubs: list[str], key: str = "club") -> str:
    """Render a single club selector."""
    return st.selectbox(tr("Club", "Clube"), sorted(clubs), key=key)
