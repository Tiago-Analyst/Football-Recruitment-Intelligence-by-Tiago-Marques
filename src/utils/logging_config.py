"""Consistent console and file logging."""
from __future__ import annotations

import logging
import os
from pathlib import Path


def configure_logging(log_file: Path | None = None) -> None:
    """Configure root logging once."""
    handlers: list[logging.Handler] = [logging.StreamHandler()]
    if log_file:
        log_file.parent.mkdir(parents=True, exist_ok=True)
        handlers.append(logging.FileHandler(log_file, encoding="utf-8"))
    logging.basicConfig(
        level=os.getenv("FRI_LOG_LEVEL", "INFO"),
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        handlers=handlers,
        force=True,
    )
