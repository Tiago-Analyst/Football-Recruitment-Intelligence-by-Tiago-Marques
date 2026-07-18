"""Documented placeholder adapter for non-selected match-only sources.

OpenFootball and football-data.org are intentionally not merged into the MVP:
neither supplies a stable player-key bridge to the selected source.
"""
from __future__ import annotations

from pathlib import Path

from src.data.adapters.base import SourceAdapter


class DisabledComparisonAdapter(SourceAdapter):
    """Fail clearly if a researched-only source is accidentally enabled."""

    def extract(self, destination: Path) -> Path:
        raise RuntimeError("Comparison source is disabled; see docs/source_research.md")

    def validate(self, artifact: Path) -> dict[str, object]:
        raise RuntimeError("Comparison source is disabled; no entity-safe merge is defined")

