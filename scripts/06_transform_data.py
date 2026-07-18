"""Build the warehouse from the most recent local raw artifact."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.data.transformation import build_warehouse  # noqa: E402


def main() -> None:
    sources = sorted((ROOT / "data" / "raw").glob("*/transfermarkt-datasets.duckdb"))
    if not sources:
        raise FileNotFoundError("No dated source artifact found")
    build_warehouse(sources[-1], ROOT / "database" / "football_recruitment.duckdb")


if __name__ == "__main__":
    main()

