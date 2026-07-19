import json
import shutil
from pathlib import Path

import duckdb
import pytest

from app import warehouse


def create_test_warehouse(path: Path) -> None:
    with duckdb.connect(str(path)) as connection:
        for table in sorted(warehouse.REQUIRED_TABLES):
            connection.execute(f"CREATE TABLE {table} (id INTEGER)")


def test_local_database_is_preferred(runtime_path):
    database = runtime_path / "local.duckdb"
    create_test_warehouse(database)

    resolved = warehouse.resolve_database(
        local_database=database,
        manifest_path=runtime_path / "missing.json",
    )

    assert resolved == database


def test_published_database_is_downloaded_and_verified(runtime_path, monkeypatch):
    source = runtime_path / "source.duckdb"
    create_test_warehouse(source)
    digest = warehouse.sha256_file(source)
    manifest = runtime_path / "latest.json"
    manifest.write_text(
        json.dumps(
            {
                "version": "123",
                "sha256": digest,
                "download_url": "https://example.test/warehouse.duckdb",
            }
        ),
        encoding="utf-8",
    )

    def fake_download(_url, destination):
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, destination)
        return destination

    monkeypatch.setattr(warehouse, "download_file", fake_download)
    resolved = warehouse.resolve_database(
        local_database=runtime_path / "missing.duckdb",
        manifest_path=manifest,
        cache_directory=runtime_path / "cache",
    )

    assert resolved.exists()
    assert warehouse.sha256_file(resolved) == digest


def test_checksum_mismatch_removes_download(runtime_path, monkeypatch):
    source = runtime_path / "source.duckdb"
    create_test_warehouse(source)
    manifest = runtime_path / "latest.json"
    manifest.write_text(
        json.dumps(
            {
                "version": "123",
                "sha256": "0" * 64,
                "download_url": "https://example.test/warehouse.duckdb",
            }
        ),
        encoding="utf-8",
    )

    def fake_download(_url, destination):
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, destination)
        return destination

    monkeypatch.setattr(warehouse, "download_file", fake_download)
    with pytest.raises(warehouse.WarehouseUnavailable, match="checksum mismatch"):
        warehouse.resolve_database(
            local_database=runtime_path / "missing.duckdb",
            manifest_path=manifest,
            cache_directory=runtime_path / "cache",
        )


def test_manifest_rejects_missing_fields(runtime_path):
    manifest = runtime_path / "latest.json"
    manifest.write_text("{}", encoding="utf-8")

    with pytest.raises(warehouse.WarehouseUnavailable, match="missing"):
        warehouse.load_manifest(manifest)
