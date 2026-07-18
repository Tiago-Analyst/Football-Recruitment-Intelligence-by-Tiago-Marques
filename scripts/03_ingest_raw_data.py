"""Validate the latest local source artifact before transformation."""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.data.validation import inspect_source_database  # noqa: E402


def main() -> None:
    sources = sorted((ROOT / "data" / "raw").glob("*/transfermarkt-datasets.duckdb"))
    if not sources:
        raise FileNotFoundError("Run scripts/02_extract_data.py first")
    expected = [
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
    print(json.dumps(inspect_source_database(sources[-1], expected), default=str, indent=2))


if __name__ == "__main__":
    main()
