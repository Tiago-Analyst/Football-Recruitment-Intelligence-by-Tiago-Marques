"""Read-only query access used by Streamlit and services."""
from __future__ import annotations

from pathlib import Path

import duckdb
import pandas as pd


class AnalyticsRepository:
    """Short-lived read-only DuckDB repository."""

    def __init__(self, database_path: Path) -> None:
        self.database_path = database_path

    def query(self, sql: str, parameters: list[object] | None = None) -> pd.DataFrame:
        """Execute a parameterised read query."""
        with duckdb.connect(str(self.database_path), read_only=True) as connection:
            return connection.execute(sql, parameters or []).fetchdf()

    def table_exists(self, name: str) -> bool:
        """Check table/view existence without raising on a new install."""
        if not self.database_path.exists():
            return False
        with duckdb.connect(str(self.database_path), read_only=True) as connection:
            return bool(
                connection.execute(
                    "SELECT COUNT(*) FROM information_schema.tables WHERE table_name = ?", [name]
                ).fetchone()[0]
            )

