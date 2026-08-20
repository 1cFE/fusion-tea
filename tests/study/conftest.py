"""Fixtures for the study indicator tool tests.

The committed package under ``exploration/stellarator_e2e/pkg/`` is read-only in
these tests. Anything that mutates a package goes through the ``package_copy``
factory (added in Phase 4), which copies into ``tmp_path``.
"""

import json
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
REAL_PACKAGE = REPO_ROOT / "exploration" / "stellarator_e2e" / "pkg" / "stellarator_tea"
REAL_MANIFEST = REPO_ROOT / "exploration" / "stellarator_e2e" / "studies" / "manifest.json"
SCHEMA_DIR = REPO_ROOT / "scripts" / "study" / "schemas"
DATA_DIR = Path(__file__).parent / "data"


@pytest.fixture
def repo_root() -> Path:
    return REPO_ROOT


@pytest.fixture
def real_package_path() -> Path:
    """The committed stellarator package. Read-only — never mutate in place."""
    assert REAL_PACKAGE.is_dir(), f"missing committed package at {REAL_PACKAGE}"
    return REAL_PACKAGE


@pytest.fixture
def real_manifest_path() -> Path:
    assert REAL_MANIFEST.is_file(), f"missing committed manifest at {REAL_MANIFEST}"
    return REAL_MANIFEST


@pytest.fixture
def load_schema():
    """Load one of the committed JSON Schema files by stem."""

    def _load(stem: str) -> dict:
        path = SCHEMA_DIR / f"{stem}.schema.json"
        assert path.is_file(), f"missing schema {path}"
        return json.loads(path.read_text())

    return _load


@pytest.fixture
def minimal_manifest_dict() -> dict:
    """The smallest manifest that validates — the shape, with placeholder facts."""
    return {
        "schema_version": "study-package-manifest/v1",
        "package": {"name": "some_pkg", "path": "some/where/some_pkg"},
        "fingerprints": {
            "indicator_inputs": {
                "recipe": "indicator-input-fingerprint/v1",
                "digest": "0" * 64,
                "files": ["contracts/model_contract.json", "inputs/a.json", "pipelines/p.yaml"],
            },
            "recorded_provenance": {
                "executable_fingerprint": "1" * 64,
                "semantic_fingerprint": "2" * 64,
            },
        },
        "objective_catalog": [{"name": "cost", "channel": "some_pkg__cost_calc__cost"}],
        "ties": [{"key": "some_pkg__b__x0", "rides_with": ["some_pkg__a__x"]}],
        "baseline": {
            "point": {"some_pkg__a__x": 1.0},
            "headline": {"channel": "some_pkg__cost_calc__cost", "value": 2.0},
            "verdicts": [{"source_local_identity": "ok", "expected": "satisfied"}],
        },
        "oracle": {
            "kind": "python_callable",
            "module": "some_oracle",
            "callable": "compute",
            "sys_path": "some/where",
        },
    }
