"""Publication metadata for the deployable analytics warehouse."""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

from src.utils.hashing import sha256_file


def create_manifest(
    database: Path,
    output: Path,
    repository: str,
    version: str,
    tag: str = "data-latest",
) -> dict[str, object]:
    """Write an auditable manifest for a GitHub Release warehouse asset."""
    if not database.exists() or database.stat().st_size == 0:
        raise FileNotFoundError(f"Warehouse does not exist or is empty: {database}")
    filename = database.name
    manifest: dict[str, object] = {
        "schema_version": 1,
        "version": version,
        "published_at": datetime.now(timezone.utc).isoformat(),
        "filename": filename,
        "size_bytes": database.stat().st_size,
        "sha256": sha256_file(database),
        "download_url": f"https://github.com/{repository}/releases/download/{tag}/{filename}",
    }
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    return manifest
