"""Resolve a validated local or published DuckDB warehouse for the app."""
from __future__ import annotations

import json
import os
import tempfile
from pathlib import Path

import duckdb

from src.data.extraction import download_file
from src.utils.hashing import sha256_file

ROOT = Path(__file__).resolve().parents[1]
LOCAL_DATABASE = ROOT / "database" / "football_recruitment.duckdb"
DEFAULT_MANIFEST = ROOT / "database" / "latest.json"
REQUIRED_TABLES = {"dim_clubs", "fact_transfers", "powerbi_last_refresh"}


class WarehouseUnavailable(RuntimeError):
    """Raised when no trustworthy warehouse can be made available."""


def load_manifest(path: Path = DEFAULT_MANIFEST) -> dict[str, object]:
    """Load and validate the public warehouse manifest."""
    if not path.exists():
        raise WarehouseUnavailable(f"Warehouse manifest not found: {path}")
    try:
        manifest = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise WarehouseUnavailable(f"Warehouse manifest is invalid: {exc}") from exc

    required = {"download_url", "sha256", "version"}
    missing = required.difference(manifest)
    if missing:
        raise WarehouseUnavailable(
            "Warehouse manifest is missing: " + ", ".join(sorted(missing))
        )
    digest = str(manifest["sha256"]).lower()
    if len(digest) != 64 or any(character not in "0123456789abcdef" for character in digest):
        raise WarehouseUnavailable("Warehouse manifest contains an invalid SHA-256 digest")
    return manifest


def validate_warehouse(path: Path) -> None:
    """Reject corrupt downloads and warehouses without the app's core tables."""
    try:
        with duckdb.connect(str(path), read_only=True) as connection:
            tables = {row[0] for row in connection.execute("SHOW TABLES").fetchall()}
    except (duckdb.Error, OSError) as exc:
        raise WarehouseUnavailable(f"Published warehouse cannot be opened: {exc}") from exc
    missing = REQUIRED_TABLES.difference(tables)
    if missing:
        raise WarehouseUnavailable(
            "Published warehouse is missing required tables: " + ", ".join(sorted(missing))
        )


def resolve_database(
    local_database: Path = LOCAL_DATABASE,
    manifest_path: Path = DEFAULT_MANIFEST,
    cache_directory: Path | None = None,
) -> Path:
    """Prefer a local warehouse, otherwise download the published validated version."""
    if local_database.exists():
        validate_warehouse(local_database)
        return local_database

    manifest = load_manifest(manifest_path)
    expected_digest = str(manifest["sha256"]).lower()
    cache_root = cache_directory or Path(
        os.getenv(
            "FRI_WAREHOUSE_CACHE",
            str(Path(tempfile.gettempdir()) / "football-recruitment-intelligence"),
        )
    )
    destination = cache_root / f"football_recruitment_{expected_digest[:12]}.duckdb"

    if destination.exists() and sha256_file(destination) == expected_digest:
        validate_warehouse(destination)
        return destination

    destination.unlink(missing_ok=True)
    try:
        download_file(str(manifest["download_url"]), destination)
    except Exception as exc:
        raise WarehouseUnavailable(f"Published warehouse download failed: {exc}") from exc

    actual_digest = sha256_file(destination)
    if actual_digest != expected_digest:
        destination.unlink(missing_ok=True)
        raise WarehouseUnavailable(
            f"Published warehouse checksum mismatch: expected {expected_digest}, got {actual_digest}"
        )
    try:
        validate_warehouse(destination)
    except WarehouseUnavailable:
        destination.unlink(missing_ok=True)
        raise
    return destination
