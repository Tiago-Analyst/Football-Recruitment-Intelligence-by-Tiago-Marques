"""Reusable table rendering."""
from __future__ import annotations

import pandas as pd
import streamlit as st


def data_table(frame: pd.DataFrame, height: int = 420) -> None:
    """Render a full-width sortable dataframe without its index."""
    st.dataframe(frame, use_container_width=True, hide_index=True, height=height)

