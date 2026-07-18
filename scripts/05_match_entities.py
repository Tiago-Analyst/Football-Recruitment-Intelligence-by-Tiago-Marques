"""Report pending cross-source entity matches (none in the single-source MVP)."""
from __future__ import annotations

from pathlib import Path

import duckdb

ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    with duckdb.connect(str(ROOT / "database" / "football_recruitment.duckdb"), read_only=True) as connection:
        print(connection.execute("SELECT * FROM entity_matching_review").fetchdf().to_string(index=False))


if __name__ == "__main__":
    main()

