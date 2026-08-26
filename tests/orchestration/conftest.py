"""Fixtures for the goal-contract document tests.

These tests read committed documents and assert they still agree with each
other. Nothing here mutates the repository.
"""

from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]


@pytest.fixture
def repo_root() -> Path:
    return REPO_ROOT
