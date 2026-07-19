"""Cached warehouse access for Streamlit."""
from __future__ import annotations

from pathlib import Path

import duckdb
import pandas as pd
import streamlit as st

from app.i18n import tr
from app.warehouse import WarehouseUnavailable, resolve_database


@st.cache_resource(ttl=3600, show_spinner=False)
def database_path() -> Path:
    """Return the local development DB or a verified published warehouse."""
    return resolve_database()


@st.cache_data(ttl=600)
def query(sql: str, parameters: tuple[object, ...] = ()) -> pd.DataFrame:
    """Run a cached parameterised read-only query."""
    try:
        warehouse = database_path()
    except WarehouseUnavailable:
        return pd.DataFrame()
    with duckdb.connect(str(warehouse), read_only=True) as connection:
        return connection.execute(sql, list(parameters)).fetchdf()


def require_database() -> None:
    """Stop a page with a useful local or deployment setup error."""
    try:
        database_path()
    except WarehouseUnavailable as exc:
        st.error(
            tr(
                "The analytics warehouse is temporarily unavailable. Check the latest data refresh or run `python scripts/10_run_full_pipeline.py` locally.",
                "A base analítica está temporariamente indisponível. Verifique a atualização de dados mais recente ou execute localmente `python scripts/10_run_full_pipeline.py`.",
            )
        )
        st.caption(str(exc))
        st.stop()
