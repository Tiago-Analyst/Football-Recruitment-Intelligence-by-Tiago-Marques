"""Power BI-ready CSV and Parquet exports."""
from __future__ import annotations

import logging
from pathlib import Path

import duckdb
import pandas as pd
import yaml

from src.utils.paths import project_path

LOGGER = logging.getLogger(__name__)

EXPORTS = {
    "dim_players": "dim_players",
    "dim_clubs": "dim_clubs",
    "dim_competitions": "dim_competitions",
    "dim_countries": "dim_countries",
    "dim_seasons": "dim_seasons",
    "fact_transfers": "fact_transfers",
    "fact_player_appearances": "fact_player_appearances",
    "fact_player_statistics": "fact_player_season_statistics",
    "fact_player_valuations": "fact_player_valuations",
    "fact_game_events": "fact_game_events",
    "fact_loans": "fact_loans",
    "fact_club_recruitment": "fact_club_recruitment",
    "fact_player_development": "fact_player_development",
    "fact_club_sales": "fact_club_sales",
    "fact_squad_snapshots": "fact_squad_snapshots",
    "transfer_pathways": "transfer_pathways",
    "club_profiles": "club_profiles",
    "squad_alerts": "squad_alerts",
}


def export_powerbi(database_path: Path, output_dir: Path) -> list[Path]:
    """Export stable UTF-8 CSVs and Parquet copies from the warehouse."""
    output_dir.mkdir(parents=True, exist_ok=True)
    written: list[Path] = []
    with duckdb.connect(str(database_path), read_only=True) as connection:
        for output_name, relation in EXPORTS.items():
            frame = connection.execute(f'SELECT * FROM "{relation}"').fetchdf()
            csv_path = output_dir / f"{output_name}.csv"
            parquet_path = output_dir / f"{output_name}.parquet"
            frame.to_csv(csv_path, index=False, encoding="utf-8")
            frame.to_parquet(parquet_path, index=False)
            written.extend((csv_path, parquet_path))
        quality = connection.execute(
            "SELECT severity, status, COUNT(*) AS rule_count, SUM(issue_count) AS issue_count "
            "FROM data_quality_results GROUP BY severity, status"
        ).fetchdf()
        quality_path = output_dir / "data_quality_summary.csv"
        quality.to_csv(quality_path, index=False, encoding="utf-8")
        written.append(quality_path)
        refresh = connection.execute("SELECT * FROM powerbi_last_refresh").fetchdf()
        refresh_path = output_dir / "last_refresh.csv"
        refresh.to_csv(refresh_path, index=False, encoding="utf-8")
        written.append(refresh_path)

    metrics_config = yaml.safe_load(
        project_path("config", "metric_definitions.yaml").read_text(encoding="utf-8")
    )["metrics"]
    metrics = pd.DataFrame(
        [{"metric_name": key, **value} for key, value in metrics_config.items()]
    )
    metrics_path = output_dir / "metric_definitions.csv"
    metrics.to_csv(metrics_path, index=False, encoding="utf-8")
    written.append(metrics_path)
    LOGGER.info("Created %s Power BI files", len(written))
    return written
