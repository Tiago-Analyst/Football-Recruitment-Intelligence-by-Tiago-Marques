"""Interface implemented by reproducible data-source adapters."""
from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path


class SourceAdapter(ABC):
    """Minimal contract for external source adapters."""

    @abstractmethod
    def extract(self, destination: Path) -> Path:
        """Retrieve an immutable raw artifact."""

    @abstractmethod
    def validate(self, artifact: Path) -> dict[str, object]:
        """Validate structure and return source metadata."""

