"""Cross-platform project paths."""
from __future__ import annotations

from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]


def project_path(*parts: str) -> Path:
    """Return a path rooted at the repository, creating no files."""
    return PROJECT_ROOT.joinpath(*parts)


def ensure_directories() -> None:
    """Create runtime directories idempotently."""
    for path in (
        project_path("data", "raw"),
        project_path("data", "staging"),
        project_path("data", "processed"),
        project_path("data", "review"),
        project_path("database"),
        project_path("output", "powerbi"),
        project_path("output", "reports"),
        project_path("output", "logs"),
    ):
        path.mkdir(parents=True, exist_ok=True)

