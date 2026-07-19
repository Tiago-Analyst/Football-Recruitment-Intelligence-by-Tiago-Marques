"""End-to-end orchestration for local and scheduled refreshes."""
from __future__ import annotations

import json
import logging
import shutil
import time
import uuid
from datetime import datetime, timezone
from pathlib import Path

import duckdb
import yaml

from src.data.adapters.source_a import TransfermarktDatasetsAdapter
from src.data.export import export_powerbi
from src.data.transformation import build_warehouse
from src.data.validation import assert_no_critical_failures, quality_results
from src.utils.hashing import sha256_file
from src.utils.paths import ensure_directories, project_path

LOGGER = logging.getLogger(__name__)


def _config() -> tuple[dict, dict]:
    settings = yaml.safe_load(project_path("config", "settings.yaml").read_text(encoding="utf-8"))
    sources = yaml.safe_load(project_path("config", "sources.yaml").read_text(encoding="utf-8"))
    return settings, sources["sources"]["transfermarkt_datasets"]


def run_pipeline(source_file: Path | None = None, download: bool = True) -> dict[str, object]:
    """Refresh source, warehouse, checks and exports; return auditable metadata."""
    ensure_directories()
    settings, source = _config()
    run_id = str(uuid.uuid4())
    started = datetime.now(timezone.utc)
    started_clock = time.perf_counter()
    raw_dir = project_path("data", "raw", started.strftime("%Y%m%d"))
    raw_path = raw_dir / "transfermarkt-datasets.duckdb"
    adapter = TransfermarktDatasetsAdapter(source["url"], source["expected_tables"])

    if source_file:
        source_file = source_file.resolve()
        raw_dir.mkdir(parents=True, exist_ok=True)
        if raw_path.resolve() != source_file:
            shutil.copy2(source_file, raw_path)
    elif download:
        adapter.extract(raw_path)
    elif not raw_path.exists():
        raise FileNotFoundError("Offline mode requested but no dated raw artifact exists")

    source_metadata = adapter.validate(raw_path)
    digest = sha256_file(raw_path)
    database_path = project_path(*settings["database_path"].split("/"))
    build_warehouse(raw_path, database_path)

    with duckdb.connect(str(database_path)) as connection:
        connection.execute(
            "INSERT INTO pipeline_run_log VALUES (?, ?, NULL, 'running', NULL, NULL)",
            [run_id, started],
        )
        total_records = sum(source_metadata["record_counts"].values())
        connection.execute(
            "INSERT INTO source_ingestion_log VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            [
                run_id,
                "transfermarkt-datasets",
                source["url"],
                datetime.now(timezone.utc),
                source_metadata["latest_game_date"],
                raw_path.name,
                digest,
                "2012-2025",
                "PO1",
                total_records,
                "full",
                "success",
                time.perf_counter() - started_clock,
                None,
            ],
        )
        results = quality_results(connection)
        results.insert(0, "pipeline_run_id", run_id)
        connection.register("quality_frame", results)
        connection.execute("INSERT INTO data_quality_results SELECT * FROM quality_frame")
        connection.unregister("quality_frame")
        assert_no_critical_failures(results)
        completed = datetime.now(timezone.utc)
        duration = time.perf_counter() - started_clock
        connection.execute(
            "UPDATE pipeline_run_log SET completed_at=?, status='success', duration_seconds=? "
            "WHERE pipeline_run_id=?",
            [completed, duration, run_id],
        )
        results.to_csv(
            project_path("output", "reports", "data_quality_report.csv"),
            index=False,
            encoding="utf-8",
        )

    written = export_powerbi(database_path, project_path("output", "powerbi"))
    metadata = {
        "pipeline_run_id": run_id,
        "status": "success",
        "source_file": raw_path.relative_to(project_path()).as_posix(),
        "source_hash": digest,
        "source_metadata": source_metadata,
        "database": database_path.relative_to(project_path()).as_posix(),
        "exports": len(written),
        "duration_seconds": round(time.perf_counter() - started_clock, 2),
    }
    snapshot = project_path("output", "snapshots", "last_refresh.json")
    snapshot.parent.mkdir(parents=True, exist_ok=True)
    snapshot.write_text(json.dumps(metadata, default=str, indent=2), encoding="utf-8")
    LOGGER.info("Pipeline %s completed in %.2fs", run_id, metadata["duration_seconds"])
    return metadata
