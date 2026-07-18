"""Run warehouse data-quality rules."""
from __future__ import annotations

import sys
from pathlib import Path

import duckdb

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.data.validation import assert_no_critical_failures, quality_results  # noqa: E402


def main() -> None:
    with duckdb.connect(str(ROOT / "database" / "football_recruitment.duckdb"), read_only=True) as connection:
        results = quality_results(connection)
    print(results.to_string(index=False))
    assert_no_critical_failures(results)


if __name__ == "__main__":
    main()

