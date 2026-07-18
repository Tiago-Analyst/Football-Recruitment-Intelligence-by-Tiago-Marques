"""Run extraction, warehouse build, validation and exports."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.services.refresh_service import run_pipeline  # noqa: E402
from src.utils.logging_config import configure_logging  # noqa: E402


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-file", type=Path, help="Use a validated local source artifact")
    parser.add_argument("--offline", action="store_true", help="Do not download a source")
    args = parser.parse_args()
    configure_logging(ROOT / "output" / "logs" / "pipeline.log")
    result = run_pipeline(source_file=args.source_file, download=not args.offline)
    print(json.dumps(result, default=str, indent=2))


if __name__ == "__main__":
    main()

