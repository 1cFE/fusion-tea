#!/usr/bin/env python3
"""Tests for Item 11 Phase 1 — parallel batch runner (analyze + model-critic).

Covers:
- ``stage_flags`` per-stage flag construction: analyze carries ``--force`` +
  ``--max-passes``, model-critic emits no ``--force`` (its argparser rejects it),
  and any other stage raises ValueError;
- the ``run_regen_batch`` CLI contract: explicit concept list required (no
  run-all default), ``--workers`` default is 3, and only ``analyze`` +
  ``model-critic`` are dispatched (stop after critic, FR-4).
"""

import pytest

from lib import parallel_stage as rsp
import run_regen_batch as rrb


# ---------------------------------------------------------------------------
# stage_flags — per-stage subprocess flags
# ---------------------------------------------------------------------------


def test_stage_flags_analyze_carries_max_passes():
    """analyze adds --max-passes N (and --force for a clean cold-start)."""
    assert rsp.stage_flags("analyze", max_passes=5) == ["--force", "--max-passes", "5"]


def test_stage_flags_model_critic_has_no_force():
    """model-critic's argparser rejects --force; flags must be empty of it."""
    flags = rsp.stage_flags("model-critic")
    assert "--force" not in flags
    assert "--max-passes" not in flags
    assert flags == []


def test_stage_flags_unsupported_stage_raises():
    """Removed scoring stages (synthesize, score, extract-scores, etc.) raise ValueError."""
    for stage in ("synthesize", "score", "extract-scores", "calibrate", "heatmap"):
        with pytest.raises(ValueError):
            rsp.stage_flags(stage)


# ---------------------------------------------------------------------------
# run_regen_batch CLI contract
# ---------------------------------------------------------------------------


def test_batch_requires_explicit_concepts():
    """No concepts → argparse error (SystemExit). No run-all default (FR-4)."""
    parser = rrb.build_parser()
    with pytest.raises(SystemExit):
        parser.parse_args([])


def test_batch_accepts_concept_list_and_defaults():
    parser = rrb.build_parser()
    args = parser.parse_args(["01-hts-compact-tokamak", "02-foo"])
    assert args.concepts == ["01-hts-compact-tokamak", "02-foo"]
    assert args.workers == 3
    assert args.max_passes == 3


def test_batch_stages_stop_after_critic():
    """Only analyze + model-critic are dispatched; no downstream stages (FR-4)."""
    assert rrb.STAGES == ["analyze", "model-critic"]
    for stage in rrb.STAGES:
        assert stage not in ("review", "address-review", "synthesize", "score",
                             "extract-scores", "calibrate", "heatmap", "approve")
