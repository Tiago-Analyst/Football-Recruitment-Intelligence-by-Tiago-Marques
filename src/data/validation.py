"""Source and warehouse data-quality checks."""
from __future__ import annotations

from datetime import date
from pathlib import Path

import duckdb
import pandas as pd


class CriticalDataQualityError(RuntimeError):
    """Raised when any critical quality rule fails."""


def inspect_source_database(path: Path, expected_tables: list[str]) -> dict[str, object]:
    """Open a source read-only, verify tables, and return measured metadata."""
    if not path.exists() or path.stat().st_size == 0:
        raise CriticalDataQualityError("Source artifact is missing or empty")
    try:
        with duckdb.connect(str(path), read_only=True) as connection:
            tables = {row[0] for row in connection.execute("SHOW TABLES").fetchall()}
            missing = sorted(set(expected_tables) - tables)
            if missing:
                raise CriticalDataQualityError(f"Missing source tables: {missing}")
            counts = {
                table: connection.execute(f'SELECT COUNT(*) FROM "{table}"').fetchone()[0]
                for table in expected_tables
            }
            empty = [table for table, count in counts.items() if count == 0]
            if empty:
                raise CriticalDataQualityError(f"Empty source tables: {empty}")
            return {
                "tables": sorted(tables),
                "record_counts": counts,
                "latest_game_date": connection.execute("SELECT MAX(date) FROM games").fetchone()[0],
                "latest_valuation_date": connection.execute(
                    "SELECT MAX(date) FROM player_valuations"
                ).fetchone()[0],
                "source_commit": connection.execute("SELECT commit_hash FROM version").fetchone()[0],
            }
    except duckdb.Error as exc:
        raise CriticalDataQualityError(f"Invalid DuckDB source: {exc}") from exc


def quality_results(connection: duckdb.DuckDBPyConnection) -> pd.DataFrame:
    """Execute deterministic warehouse checks and return all findings."""
    rules = [
        ("missing_player_id", "critical", "SELECT COUNT(*) FROM dim_players WHERE source_player_id IS NULL"),
        ("duplicate_player_id", "critical", "SELECT COUNT(*)-COUNT(DISTINCT source_player_id) FROM dim_players"),
        ("missing_club_id", "critical", "SELECT COUNT(*) FROM dim_clubs WHERE source_club_id IS NULL"),
        ("duplicate_club_id", "critical", "SELECT COUNT(*)-COUNT(DISTINCT source_club_id) FROM dim_clubs"),
        ("negative_transfer_fee", "critical", "SELECT COUNT(*) FROM fact_transfers WHERE transfer_fee_eur < 0"),
        ("transfer_before_birth", "critical", "SELECT COUNT(*) FROM fact_transfers WHERE age_at_transfer < 0"),
        ("negative_minutes", "critical", "SELECT COUNT(*) FROM fact_player_appearances WHERE minutes_played < 0"),
        ("duplicate_appearance", "critical", "SELECT COUNT(*)-COUNT(DISTINCT appearance_id) FROM fact_player_appearances"),
        ("negative_market_value", "critical", "SELECT COUNT(*) FROM fact_player_valuations WHERE market_value_eur < 0"),
        (
            "stale_player_in_squad_snapshot",
            "critical",
            "SELECT COUNT(*) FROM fact_squad_snapshots s JOIN dim_players p USING(player_key) WHERE p.last_season <> (SELECT MAX(last_season) FROM dim_players)",
        ),
        (
            "stale_club_in_squad_snapshot",
            "critical",
            "SELECT COUNT(*) FROM fact_squad_snapshots s JOIN dim_clubs c USING(club_key) WHERE c.last_season <> (SELECT MAX(last_season) FROM dim_clubs)",
        ),
        (
            "stale_portuguese_player_abroad",
            "critical",
            "SELECT COUNT(*) FROM portuguese_players_abroad a JOIN dim_players p USING(player_key) WHERE p.last_season <> (SELECT MAX(last_season) FROM dim_players)",
        ),
        ("future_transfer", "warning", "SELECT COUNT(*) FROM fact_transfers WHERE transfer_date > CURRENT_DATE"),
        ("unknown_transfer_fee", "warning", "SELECT COUNT(*) FROM fact_transfers WHERE transfer_fee_eur IS NULL"),
        ("unavailable_loan_type", "warning", "SELECT COUNT(*) FROM fact_transfers WHERE transfer_type_key = 1"),
    ]
    rows: list[dict[str, object]] = []
    checked_at = pd.Timestamp.now(tz="UTC")
    for rule_name, severity, sql in rules:
        count = int(connection.execute(sql).fetchone()[0] or 0)
        rows.append(
            {
                "rule_name": rule_name,
                "severity": severity,
                "status": "FAIL" if count else "PASS",
                "issue_count": count,
                "checked_at": checked_at,
            }
        )
    return pd.DataFrame(rows)


def assert_no_critical_failures(results: pd.DataFrame) -> None:
    """Stop the pipeline when one or more critical rules fail."""
    failed = results[(results["severity"] == "critical") & (results["status"] == "FAIL")]
    if not failed.empty:
        names = ", ".join(failed["rule_name"].tolist())
        raise CriticalDataQualityError(f"Critical data-quality failures: {names}")


def is_stale(latest_date: date, reference_date: date, threshold_days: int) -> bool:
    """Return whether the last observed date exceeds the configured threshold."""
    return (reference_date - latest_date).days > threshold_days
