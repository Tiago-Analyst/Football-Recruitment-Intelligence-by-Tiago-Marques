"""Generate Power BI-ready exports from the current warehouse."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.data.export import export_powerbi  # noqa: E402

if __name__ == "__main__":
    files = export_powerbi(ROOT / "database" / "football_recruitment.duckdb", ROOT / "output" / "powerbi")
    print(f"Created {len(files)} files")

