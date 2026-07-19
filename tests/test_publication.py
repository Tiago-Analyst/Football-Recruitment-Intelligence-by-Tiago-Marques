import json

import pytest

from src.services.publication import create_manifest
from src.utils.hashing import sha256_file


def test_release_manifest_contains_verified_asset_metadata(runtime_path):
    database = runtime_path / "football_recruitment.duckdb"
    database.write_bytes(b"validated-warehouse")
    output = runtime_path / "latest.json"

    manifest = create_manifest(
        database,
        output,
        "Tiago-Analyst/example",
        "run-123",
    )
    persisted = json.loads(output.read_text(encoding="utf-8"))

    assert persisted == manifest
    assert manifest["sha256"] == sha256_file(database)
    assert manifest["size_bytes"] == database.stat().st_size
    assert manifest["download_url"].endswith(
        "/data-latest/football_recruitment.duckdb"
    )


def test_release_manifest_rejects_empty_database(runtime_path):
    database = runtime_path / "empty.duckdb"
    database.touch()

    with pytest.raises(FileNotFoundError, match="empty"):
        create_manifest(database, runtime_path / "latest.json", "owner/repo", "run-123")
