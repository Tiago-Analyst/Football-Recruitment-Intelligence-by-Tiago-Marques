"""Workspace-local test paths for Windows environments with restricted temp ACLs."""
from __future__ import annotations

import re
import shutil
from pathlib import Path

import pytest


@pytest.fixture
def runtime_path(request):
    """Provide a test-isolated path without pytest's chmod-based tmp_path logic."""
    root = Path(__file__).parent / ".runtime"
    name = re.sub(r"[^a-zA-Z0-9_-]", "_", request.node.name)
    path = root / name
    if path.exists():
        shutil.rmtree(path)
    path.mkdir(parents=True)
    yield path
    shutil.rmtree(path, ignore_errors=True)

