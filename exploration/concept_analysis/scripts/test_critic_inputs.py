#!/usr/bin/env python3
"""Tests for lib/critic_inputs.py — the pure model_critic input loader.

The plan stencil names ``01-arc-tokamak`` as the real-data fixture; the actual
concept ID is ``01-hts-compact-tokamak`` (the ARC reference is a draft typo in
the spec/plan/design — flagged in plan Implementation Notes).
"""

from __future__ import annotations

import shutil
import sys
import textwrap
import types
from pathlib import Path

import pytest

from lib.critic_inputs import (
    DRIFT_THRESHOLD,
    CriticInputs,
    _detect_drift,
    _parse_static_lcoe,
    collect,
    format_check_block,
)
from lib.concepts import load_concepts
from lib.validators import ValidationResult


REAL_CID = "01-hts-compact-tokamak"


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture
def record_real():
    """The real, on-disk record for the reference concept."""
    by_id = {r["concept_id"]: r for r in load_concepts()}
    return by_id[REAL_CID]


def _fake_sanity(_cid):
    """Stand-in sanity_check returning a quiet, valid dict."""
    return {
        "concept_id": _cid,
        "comparables": [],
        "accounts": [
            {"account": "CAS21", "value": 1.0, "comparable_median": 1.0,
             "ratio": 1.0, "flag": "in_range", "comparable_values": {}},
        ],
    }


def _seed_concept_dir(dst: Path, src: Path) -> None:
    """Copy analysis.md / model_setup.py / model_output.txt from src into dst."""
    dst.mkdir(parents=True, exist_ok=True)
    for name in ("analysis.md", "model_setup.py", "model_output.txt"):
        s = src / name
        if s.exists():
            shutil.copy2(s, dst / name)


@pytest.fixture
def tmp_concept_dir(tmp_path, monkeypatch, record_real):
    """A writable concept dir under tmp; ANALYSES_DIR repointed at its parent."""
    fake_analyses = tmp_path / "analyses"
    fake_analyses.mkdir()
    cdir = fake_analyses / REAL_CID
    real_src = Path(__file__).resolve().parent.parent / "analyses" / REAL_CID
    _seed_concept_dir(cdir, real_src)
    monkeypatch.setattr("lib.critic_inputs.ANALYSES_DIR", fake_analyses)
    return cdir


# ---------------------------------------------------------------------------
# collect() — happy path against the real reference concept
# ---------------------------------------------------------------------------


def test_collect_happy_path(record_real):
    inputs = collect(record_real, sanity_check=_fake_sanity)
    assert isinstance(inputs, CriticInputs)
    assert inputs.concept_id == REAL_CID
    assert inputs.analysis_md  # non-empty
    assert inputs.model_setup_py  # non-empty
    assert inputs.model_output_txt  # non-empty
    assert inputs.import_status == "imported OK"
    assert inputs.live_result_1gw is not None
    assert isinstance(inputs.enabled_count, int) and inputs.enabled_count >= 0
    assert inputs.dpc.valid is True  # 3-leg coherence should hold for the reference
    assert inputs.drift_flag is None  # live vs static should agree at parity


# ---------------------------------------------------------------------------
# collect() — broken model_setup.py falls back gracefully
# ---------------------------------------------------------------------------


def test_collect_broken_model_setup_falls_back(record_real, tmp_concept_dir):
    """Replace the seed model_setup.py with one that has a SyntaxError."""
    (tmp_concept_dir / "model_setup.py").write_text(
        "def broken(:\n  pass\n", encoding="utf-8",
    )
    inputs = collect(record_real, sanity_check=_fake_sanity)
    assert "SyntaxError" in inputs.import_status or "import failed" in inputs.import_status
    assert inputs.live_result_1gw is None
    assert inputs.enabled_count is None
    # contract validator catches the syntax error leg
    assert inputs.contract.valid is False
    # count_smell synthesizes a failure result when enabled_count is unavailable
    assert inputs.count_smell.valid is False
    # No drift flag possible without live LCOE
    assert inputs.drift_flag is None


# ---------------------------------------------------------------------------
# collect() — drift flag fires when live LCOE diverges from static
# ---------------------------------------------------------------------------


def test_collect_drift_flag_fires_above_threshold(record_real, tmp_concept_dir, monkeypatch):
    """Stub live import to return a result_1gw whose costs.lcoe is far from static."""
    static_lcoe = _parse_static_lcoe((tmp_concept_dir / "model_output.txt").read_text())
    assert static_lcoe is not None
    drifted = static_lcoe * 1.10  # 10% off, well above 2% threshold

    fake_costs = types.SimpleNamespace(lcoe=drifted)
    fake_r1gw = types.SimpleNamespace(costs=fake_costs)
    fake_module = types.SimpleNamespace(result_1gw=fake_r1gw, overrides=[])

    monkeypatch.setattr(
        "lib.critic_inputs._try_import",
        lambda _path: (fake_module, "imported OK"),
    )

    inputs = collect(record_real, sanity_check=_fake_sanity)
    assert inputs.drift_flag is not None
    assert "drift" in inputs.drift_flag.lower()


def test_detect_drift_unit():
    assert _detect_drift(100.0, 100.0) is None
    assert _detect_drift(100.0, 101.5) is None  # 1.5% — under 2% threshold
    assert _detect_drift(110.0, 100.0) is not None
    assert _detect_drift(None, 100.0) is None
    assert _detect_drift(100.0, None) is None
    assert _detect_drift(100.0, 0.0) is None
    # DRIFT_THRESHOLD is the boundary — exactly threshold should NOT flag
    assert _detect_drift(102.0, 100.0) is None  # exactly 2%
    assert _detect_drift(102.5, 100.0) is not None  # >2%


# ---------------------------------------------------------------------------
# format_check_block() — uniform shape across ValidationResult and dict
# ---------------------------------------------------------------------------


def test_format_check_block_uniform_shape_validation_result_ok():
    vr = ValidationResult(valid=True, details="all good (one leg)")
    block = format_check_block("dpc", vr)
    assert block.startswith("### dpc")
    assert "status: ok" in block
    assert "summary: all good (one leg)" in block
    assert "detail: all good (one leg)" in block


def test_format_check_block_validation_result_flagged():
    vr = ValidationResult(valid=True, details="FLAG: High fit with 7 overrides (expected 0–4)")
    block = format_check_block("count_smell", vr)
    assert "status: flagged" in block
    assert "FLAG:" in block


def test_format_check_block_validation_result_error():
    vr = ValidationResult(valid=False, fix_message="syntax error on line 3", details="SyntaxError")
    block = format_check_block("contract", vr)
    assert "status: error" in block
    assert "syntax error on line 3" in block


def test_format_check_block_sanity_dict_with_error():
    sanity = {"concept_id": REAL_CID, "error": "no model_setup.py or it failed to import"}
    block = format_check_block("sanity", sanity)
    assert block.startswith("### sanity")
    assert "status: error" in block
    assert "no model_setup.py" in block


def test_format_check_block_sanity_dict_with_outliers():
    sanity = {
        "concept_id": REAL_CID,
        "comparables": ["x"],
        "accounts": [
            {"account": "CAS21", "value": 100.0, "comparable_median": 10.0,
             "ratio": 10.0, "flag": "outlier_high", "comparable_values": {"x": 10.0}},
            {"account": "CAS22", "value": 1.0, "comparable_median": 1.0,
             "ratio": 1.0, "flag": "in_range", "comparable_values": {"x": 1.0}},
        ],
    }
    block = format_check_block("sanity", sanity)
    assert "status: flagged" in block
    assert "CAS21" in block
    assert "ratio=10.00" in block


def test_format_check_block_rejects_unknown_type():
    with pytest.raises(TypeError):
        format_check_block("bogus", "not a result")


# ---------------------------------------------------------------------------
# _parse_static_lcoe() unit
# ---------------------------------------------------------------------------


def test_parse_static_lcoe_first_line_format():
    text = "LCOE: 539.0 $/MWh   (1 GWe NOAK projection)\nOther stuff\n"
    assert _parse_static_lcoe(text) == 539.0


def test_parse_static_lcoe_missing_returns_none():
    assert _parse_static_lcoe("no headline here\n") is None
