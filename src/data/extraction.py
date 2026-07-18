"""Reliable, immutable HTTP extraction."""
from __future__ import annotations

import logging
import os
import time
from pathlib import Path

import requests

LOGGER = logging.getLogger(__name__)


class ExtractionError(RuntimeError):
    """Raised when a source artifact cannot be retrieved safely."""


def download_file(
    url: str,
    destination: Path,
    timeout: int = 600,
    retries: int = 3,
    session: requests.Session | None = None,
) -> Path:
    """Stream a URL to an atomic temporary file and reject empty responses."""
    destination.parent.mkdir(parents=True, exist_ok=True)
    client = session or requests.Session()
    temporary = destination.with_suffix(destination.suffix + ".part")
    last_error: Exception | None = None
    for attempt in range(1, retries + 1):
        try:
            with client.get(url, stream=True, timeout=timeout) as response:
                response.raise_for_status()
                with temporary.open("wb") as output:
                    for chunk in response.iter_content(chunk_size=1024 * 1024):
                        if chunk:
                            output.write(chunk)
            if not temporary.exists() or temporary.stat().st_size == 0:
                raise ExtractionError(f"Empty response from {url}")
            os.replace(temporary, destination)
            LOGGER.info("Downloaded %s (%s bytes)", destination, destination.stat().st_size)
            return destination
        except (requests.RequestException, OSError, ExtractionError) as exc:
            last_error = exc
            temporary.unlink(missing_ok=True)
            if attempt < retries:
                time.sleep(min(2**attempt, 10))
    raise ExtractionError(f"Failed to download {url}: {last_error}")

