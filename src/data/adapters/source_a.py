"""Adapter for the selected CC0 transfermarkt-datasets DuckDB artifact."""
from __future__ import annotations

from pathlib import Path

from src.data.adapters.base import SourceAdapter
from src.data.extraction import download_file
from src.data.validation import inspect_source_database


class TransfermarktDatasetsAdapter(SourceAdapter):
    """Download and validate the documented public DuckDB release."""

    def __init__(self, url: str, expected_tables: list[str]) -> None:
        self.url = url
        self.expected_tables = expected_tables

    def extract(self, destination: Path) -> Path:
        return download_file(self.url, destination)

    def validate(self, artifact: Path) -> dict[str, object]:
        return inspect_source_database(artifact, self.expected_tables)

