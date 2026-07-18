"""Cached warehouse access for Streamlit."""
from __future__ import annotations

from pathlib import Path

import duckdb
import pandas as pd
import streamlit as st

from app.i18n import tr

ROOT = Path(__file__).resolve().parents[1]
DATABASE = ROOT / "database" / "football_recruitment.duckdb"


@st.cache_data(ttl=600)
def query(sql: str, parameters: tuple[object, ...] = ()) -> pd.DataFrame:
    """Run a cached parameterised read-only query."""
    if not DATABASE.exists():
        return pd.DataFrame()
    with duckdb.connect(str(DATABASE), read_only=True) as connection:
        return connection.execute(sql, list(parameters)).fetchdf()


def require_database() -> None:
    """Stop a page with a useful setup instruction when no warehouse exists."""
    if not DATABASE.exists():
        st.error(
            tr(
                "Warehouse not found. Run `python scripts/10_run_full_pipeline.py` first.",
                "Base de dados não encontrada. Execute primeiro `python scripts/10_run_full_pipeline.py`.",
            )
        )
        st.stop()
