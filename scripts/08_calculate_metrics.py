"""Display current analytical output counts."""
from __future__ import annotations

from pathlib import Path

import duckdb

ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    relations = ["fact_club_recruitment", "fact_player_development", "fact_club_sales"]
    with duckdb.connect(str(ROOT / "database" / "football_recruitment.duckdb"), read_only=True) as connection:
        for relation in relations:
            print(relation, connection.execute(f'SELECT COUNT(*) FROM "{relation}"').fetchone()[0])


if __name__ == "__main__":
    main()
