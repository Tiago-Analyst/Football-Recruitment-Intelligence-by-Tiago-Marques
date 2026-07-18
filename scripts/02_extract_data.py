"""Download the latest immutable primary-source artifact."""
from __future__ import annotations

import sys
from datetime import datetime, timezone
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.data.adapters.source_a import TransfermarktDatasetsAdapter  # noqa: E402


def main() -> None:
    source = yaml.safe_load((ROOT / "config" / "sources.yaml").read_text(encoding="utf-8"))["sources"]["transfermarkt_datasets"]
    output = ROOT / "data" / "raw" / datetime.now(timezone.utc).strftime("%Y%m%d") / "transfermarkt-datasets.duckdb"
    adapter = TransfermarktDatasetsAdapter(source["url"], source["expected_tables"])
    print(adapter.extract(output))


if __name__ == "__main__":
    main()

