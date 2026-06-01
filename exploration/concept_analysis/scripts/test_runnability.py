#!/usr/bin/env python3
"""Tests for lib.concepts.Runnability + runnability() — the shared four-state
classifier that ``cmd_regenerate_concept`` and ``cmd_model_critic`` dispatch on.

Pins all four enum values, the wrapping of ``costingfe`` +
``costingfe-asterisked`` into ``RUNNABLE``, and the regen refusal copy
preservation (Phase 1 of the model_critic plan).
"""

import subprocess
import sys
from pathlib import Path

from lib.concepts import Runnability, runnability

_UNSET = object()
_RUN_ANALYSIS = Path(__file__).resolve().parent / "run_analysis.py"


def make_record(fit_grade="High", design_point=_UNSET, dp_grounding=None,
                in_freeform_routes=False, **extra):
    """Minimal record dict matching the shape ``runnability`` consumes."""
    if dp_grounding is not None:
        dp = {"grounding_confidence": dp_grounding}
    elif design_point is not _UNSET:
        dp = design_point
    else:
        dp = None
    rec = {
        "fit_grade": fit_grade,
        "design_point": dp,
        "in_freeform_routes": in_freeform_routes,
    }
    rec.update(extra)
    return rec


# ---------------------------------------------------------------------------
# Four enum values
# ---------------------------------------------------------------------------


def test_runnability_costingfe_runnable():
    rec = make_record(fit_grade="High", design_point={"p_native_mwe": 233,
                                                      "grounding_confidence": "high"})
    assert runnability(rec) is Runnability.RUNNABLE


def test_runnability_costingfe_asterisked_is_runnable():
    rec = make_record(fit_grade="Low", dp_grounding="low")
    assert runnability(rec) is Runnability.RUNNABLE


def test_runnability_freeform_deferred_by_fit_grade():
    rec = make_record(fit_grade="None")
    assert runnability(rec) is Runnability.FREEFORM_DEFERRED


def test_runnability_freeform_deferred_by_routes():
    rec = make_record(fit_grade="High", in_freeform_routes=True, design_point=None)
    assert runnability(rec) is Runnability.FREEFORM_DEFERRED


def test_runnability_pending_design_point():
    rec = make_record(fit_grade="High", in_freeform_routes=False, design_point=None)
    assert runnability(rec) is Runnability.PENDING_DESIGN_POINT


# ---------------------------------------------------------------------------
# Regen-refusal copy preservation — Phase 1's regression net
# ---------------------------------------------------------------------------


def test_regen_refusal_copy_freeform_by_fit_grade():
    """fit_grade=None freeform retains its Item-11-tagged phrasing verbatim."""
    from run_analysis import _regen_refusal_reason

    rec = make_record(fit_grade="None")
    assert _regen_refusal_reason(rec) == (
        "fit_grade=None — freeform, out of scope to model (Item 11)"
    )


def test_regen_refusal_copy_freeform_by_routes():
    from run_analysis import _regen_refusal_reason

    rec = make_record(fit_grade="High", in_freeform_routes=True, design_point=None)
    assert _regen_refusal_reason(rec) == (
        "freeform by judgment (listed in design_point_freeform_routes.md) — "
        "out of scope to model (Item 11)"
    )


def test_regen_refusal_copy_pending_design_point():
    from run_analysis import _regen_refusal_reason

    rec = make_record(fit_grade="High", design_point=None, in_freeform_routes=False)
    assert _regen_refusal_reason(rec) == (
        "pending-design-point — design-point row missing in Item 5's batch; "
        "populate design_point.csv first"
    )


def test_regen_refusal_none_for_runnable():
    from run_analysis import _regen_refusal_reason

    rec = make_record(fit_grade="High", dp_grounding="high")
    assert _regen_refusal_reason(rec) is None
