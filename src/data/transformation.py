"""Build the analytical warehouse from the validated source artifact."""
from __future__ import annotations

import logging
from pathlib import Path

import duckdb

from src.utils.paths import project_path

LOGGER = logging.getLogger(__name__)


def build_warehouse(source_path: Path, database_path: Path) -> None:
    """Execute ordered, idempotent SQL against a fresh DuckDB warehouse."""
    database_path.parent.mkdir(parents=True, exist_ok=True)
    database_path.unlink(missing_ok=True)
    connection = duckdb.connect(str(database_path))
    escaped_source = str(source_path.resolve()).replace("'", "''")
    connection.execute(f"ATTACH '{escaped_source}' AS source (READ_ONLY)")
    try:
        for sql_path in sorted(project_path("sql").glob("*.sql")):
            LOGGER.info("Executing %s", sql_path.name)
            connection.execute(sql_path.read_text(encoding="utf-8"))
        connection.execute("DETACH source")
    finally:
        connection.close()

