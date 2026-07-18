"""Inspect saved source-validation samples and print measured evidence."""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.data.validation import inspect_source_database  # noqa: E402

EXPECTED = [
    "appearances",
    "clubs",
    "competitions",
    "countries",
    "games",
    "game_events",
    "player_valuations",
    "players",
    "transfers",
]


def main() -> None:
    sample = ROOT / "data" / "raw" / "source_validation" / "transfermarkt-datasets.duckdb"
    print(json.dumps(inspect_source_database(sample, EXPECTED), default=str, indent=2))
    football_data = json.loads(
        (ROOT / "data" / "raw" / "source_validation" / "football-data_competitions.json").read_text(encoding="utf-8")
    )
    portugal = [c for c in football_data["competitions"] if c["area"]["name"] == "Portugal"]
    print(json.dumps({"football_data_portugal_competitions": portugal}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
