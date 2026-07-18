"""Ingestion metadata and schema-change detection."""
from __future__ import annotations

import json
from pathlib import Path

import duckdb


def schema_signature(database: Path, tables: list[str]) -> dict[str, list[tuple[str, str]]]:
    """Return deterministic table/column signatures for change monitoring."""
    with duckdb.connect(str(database), read_only=True) as connection:
        return {
            table: [
                (row[0], row[1])
                for row in connection.execute(f'DESCRIBE "{table}"').fetchall()
            ]
            for table in tables
        }


def signature_json(signature: dict[str, list[tuple[str, str]]]) -> str:
    """Serialise a schema signature stably."""
    return json.dumps(signature, sort_keys=True)

