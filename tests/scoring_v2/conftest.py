"""Shared fixtures for scoring_v2 tests.

Test isolation: every test that touches features/ or scores/ runs against an
isolated copy under tmp_path, never the live directory.
"""
from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
SCORING_V2 = REPO_ROOT / "exploration" / "scoring_v2"


@pytest.fixture
def repo_root() -> Path:
    return REPO_ROOT


@pytest.fixture
def live_features_dir() -> Path:
    return SCORING_V2 / "features"


@pytest.fixture
def tmp_features_dir(tmp_path: Path, live_features_dir: Path) -> Path:
    """A tmp copy of the live features/ directory."""
    dest = tmp_path / "features"
    if live_features_dir.exists():
        shutil.copytree(live_features_dir, dest)
    else:
        dest.mkdir()
    return dest


@pytest.fixture
def tmp_scores_dir(tmp_path: Path) -> Path:
    d = tmp_path / "scores"
    d.mkdir()
    return d


@pytest.fixture
def tmp_weights_file(tmp_path: Path) -> Path:
    """A tmp copy of the live default weights file."""
    src = SCORING_V2 / "weights" / "default.yaml"
    dest = tmp_path / "default.yaml"
    if src.exists():
        shutil.copy(src, dest)
    return dest


@pytest.fixture
def run_cli(tmp_features_dir: Path, tmp_scores_dir: Path, tmp_weights_file: Path):
    """Run extract.py or score.py against the tmp dirs."""
    def _run(script: str, *args: str, check: bool = True, weights: Path | None = None) -> subprocess.CompletedProcess:
        cmd = [
            sys.executable,
            str(SCORING_V2 / script),
            *args,
            "--features-dir", str(tmp_features_dir),
        ]
        if script == "score.py":
            cmd += ["--scores-dir", str(tmp_scores_dir),
                    "--weights", str(weights or tmp_weights_file)]
        result = subprocess.run(cmd, capture_output=True, text=True, cwd=REPO_ROOT)
        if check and result.returncode != 0:
            raise AssertionError(
                f"{script} failed (rc={result.returncode})\n"
                f"stdout:\n{result.stdout}\n"
                f"stderr:\n{result.stderr}"
            )
        return result
    return _run
