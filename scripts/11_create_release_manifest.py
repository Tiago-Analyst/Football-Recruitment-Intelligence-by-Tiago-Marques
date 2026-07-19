"""Create the version manifest consumed by the deployed Streamlit app."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.services.publication import create_manifest  # noqa: E402


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--database", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--repository", required=True)
    parser.add_argument("--version", required=True)
    parser.add_argument("--tag", default="data-latest")
    args = parser.parse_args()
    manifest = create_manifest(
        args.database,
        args.output,
        args.repository,
        args.version,
        args.tag,
    )
    print(json.dumps(manifest, indent=2))


if __name__ == "__main__":
    main()
