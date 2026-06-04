#!/usr/bin/env python3
"""Tests for Item 11 Phase 3 — status stats (P_native, native LCOE, 1 GWe LCOE).

Covers the module-load LCOE source (`lib.model_stats`):
- a real three-forward concept dir resolves all three stats from its
  `model_setup.py` (`native`/`result_1gw`) and `analysis.md` frontmatter
  (`P-Native`);
- graceful degradation to blanks (None) when `model_setup.py` is absent or
  un-loadable, with `P_native` still read from frontmatter when present.
"""

import math
from pathlib import Path

from lib.model_stats import load_concept_stats
import run_analysis as ra

CONCEPT01 = ra.ANALYSES_DIR / "01-hts-compact-tokamak"


def test_real_three_forward_concept_resolves_all_stats():
    """Concept 01 (regenerated, three-forward) yields P_native + both LCOEs."""
    stats = load_concept_stats(CONCEPT01)
    assert stats.p_native == 233.0  # frontmatter "P-Native: 233"
    assert stats.native_lcoe is not None and math.isfinite(stats.native_lcoe)
    assert stats.native_lcoe > 0
    assert stats.result_1gw_lcoe is not None and math.isfinite(stats.result_1gw_lcoe)
    assert stats.result_1gw_lcoe > 0


def test_blank_when_no_model_setup(tmp_path: Path):
    """Empty dir → all stats blank (None); no exception."""
    stats = load_concept_stats(tmp_path)
    assert stats.p_native is None
    assert stats.native_lcoe is None
    assert stats.result_1gw_lcoe is None


def test_p_native_read_without_model_setup(tmp_path: Path):
    """P_native comes from frontmatter even when model_setup.py is absent."""
    (tmp_path / "analysis.md").write_text(
        "---\nID: x\nP-Native: 412\n---\nbody\n", encoding="utf-8")
    stats = load_concept_stats(tmp_path)
    assert stats.p_native == 412.0
    assert stats.native_lcoe is None  # no model_setup.py
    assert stats.result_1gw_lcoe is None


def test_unloadable_model_setup_degrades_to_blank(tmp_path: Path):
    """A model_setup.py that raises on import → LCOEs blank, no crash."""
    (tmp_path / "analysis.md").write_text(
        "---\nP-Native: 100\n---\n", encoding="utf-8")
    (tmp_path / "model_setup.py").write_text(
        "raise RuntimeError('boom')\n", encoding="utf-8")
    stats = load_concept_stats(tmp_path)
    assert stats.p_native == 100.0
    assert stats.native_lcoe is None
    assert stats.result_1gw_lcoe is None
