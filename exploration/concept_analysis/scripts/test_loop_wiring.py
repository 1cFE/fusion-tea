#!/usr/bin/env python3
"""Tests for Item 8 Phase 3 — loop wiring, common-vars, shared constant.

Covers:
- the model-setup output gate chaining the contract + override-registry gates
  onto all three branches (costingfe), and staying syntax-only for freeform;
- the assess surface's net-new coherence-flag feed;
- the four new common-vars / model-vars substitution keys;
- the single-source fit-grade override-count band.
"""

import tempfile
from pathlib import Path

import pytest

from lib.canonical_accounts import FIT_GRADE_OVERRIDE_BAND
from lib.loop import (
    _count_enabled_overrides,
    build_coherence_flags,
    select_model_setup_validator,
)
from lib.prompt_blocks import (
    canonical_accounts_block,
    comparables_block,
    design_point_block,
    fit_grade_band_line,
)

# A conformant three-forward helper-form model_setup.py (Item 7 contract +
# six-field registry).
HELPER_FORM = '''\
from lib.model_setup_helpers import generic_reference, run_native_and_1gw
from costingfe import ConfinementConcept, CostModel, Fuel

spec = dict(R0=3.3, plasma_t=1.13, elon=1.84)
P_native = 233.0
model = CostModel(concept=ConfinementConcept.TOKAMAK, fuel=Fuel.DT)

generic = generic_reference(model, spec, P_native)

overrides = [
    {"account": "C220103", "value": 6901.0, "enabled": True,
     "provenance": "derived", "source": "Sorbom 2015", "rationale": "magnet"},
    {"account": "CAS27", "value": 146.0, "enabled": False,
     "provenance": "derived", "source": "Araiinejad 2025", "rationale": "FLiBe"},
]

native, result_1gw = run_native_and_1gw(model, spec, overrides, P_native)
'''

# A three-forward inline form (`native`/`result_1gw` hand-rolled) — rejected by
# strict_helper_only=True. `generic` is still via generic_reference (mandatory).
INLINE_FORM = '''\
from lib.model_setup_helpers import generic_reference
from costingfe import ConfinementConcept, CostModel, Fuel

spec = dict(R0=3.3)
P_native = 233.0
model = CostModel(concept=ConfinementConcept.TOKAMAK, fuel=Fuel.DT)

generic = generic_reference(model, spec, P_native)
native = model.forward(net_electric_mw=233.0, n_mod=1, cost_overrides={}, override_reference_mw=233.0)
result_1gw = model.forward(net_electric_mw=1000, n_mod=4.3, cost_overrides={}, override_reference_mw=233.0)
overrides = []
'''


def _script(tmp: Path, text: str = "overrides = []\n") -> Path:
    p = tmp / "model_setup.py"
    p.write_text(text, encoding="utf-8")
    return p


# ---------------------------------------------------------------------------
# Validator selection — contract + registry on all three costingfe branches
# ---------------------------------------------------------------------------

BRANCHES = [
    ("cold_start", "", ""),
    ("edit_pass_analysis", "/prior.py", "### F-1: x\n- **Category:** analysis\n"),
    ("edit_pass_model", "/prior.py", "### F-1: x\n- **Category:** model\n"),
]


@pytest.mark.parametrize("label,prior,feedback", BRANCHES)
def test_contract_and_registry_chained_in_all_three_costingfe_branches(
    label, prior, feedback, tmp_path
):
    chain = select_model_setup_validator(
        prior_model_path=prior,
        model_feedback=feedback,
        model_script=_script(tmp_path),
        is_costingfe=True,
    )
    assert "validate_model_setup_contract_strict" in chain.__name__
    assert "validate_override_registry" in chain.__name__


@pytest.mark.parametrize("label,prior,feedback", BRANCHES)
def test_freeform_branches_stay_syntax_only(label, prior, feedback, tmp_path):
    chain = select_model_setup_validator(
        prior_model_path=prior,
        model_feedback=feedback,
        model_script=_script(tmp_path),
        is_costingfe=False,
    )
    assert "validate_model_setup_contract_strict" not in chain.__name__
    assert "validate_override_registry" not in chain.__name__


def test_costingfe_gate_accepts_helper_form(tmp_path):
    chain = select_model_setup_validator(
        prior_model_path="", model_feedback="",
        model_script=_script(tmp_path), is_costingfe=True,
    )
    assert chain(HELPER_FORM).valid


def test_costingfe_gate_rejects_inline_two_knob(tmp_path):
    chain = select_model_setup_validator(
        prior_model_path="", model_feedback="",
        model_script=_script(tmp_path), is_costingfe=True,
    )
    assert not chain(INLINE_FORM).valid


# ---------------------------------------------------------------------------
# Enabled-override counting (feeds the fit-grade check)
# ---------------------------------------------------------------------------


def test_count_enabled_overrides_counts_only_enabled():
    # HELPER_FORM has one enabled (C220103) and one disabled (CAS27).
    assert _count_enabled_overrides(HELPER_FORM) == 1


def test_count_enabled_overrides_handles_syntax_error():
    assert _count_enabled_overrides("def f(\n") == 0


def test_count_enabled_overrides_empty_list():
    assert _count_enabled_overrides("overrides = []\n") == 0


# ---------------------------------------------------------------------------
# Assess coherence-flag feed (net-new, FR-27)
# ---------------------------------------------------------------------------

DP_ROW = {
    "concept_id": "01-hts-compact-tokamak",
    "design_name": "ARC 2015 Conservative Pilot",
    "maturity_tier": "paper-concept",
    "p_native_mwe": "233",
    "grounding_confidence": "high",
    "primary_sources": "arc-reactor-specifications.md",
}


def _concept(**over) -> dict:
    base = {
        "_id": "01-hts-compact-tokamak",
        "Concept Name": "ARC",
        "archetype_enum": "TOKAMAK",
        "fit_grade": "High",
        "comparables": ["21-spherical-tokamak-hts"],
        "design_point": DP_ROW,
    }
    base.update(over)
    return base


def test_build_coherence_flags_empty_without_model_setup(tmp_path):
    # No model_setup.py in the iter dir → nothing to check yet.
    flags = build_coherence_flags(_concept(), tmp_path, tmp_path / "analysis.md")
    assert flags == ""


def test_build_coherence_flags_empty_without_design_point(tmp_path):
    _script(tmp_path, HELPER_FORM)
    flags = build_coherence_flags(
        _concept(design_point=None), tmp_path, tmp_path / "analysis.md"
    )
    assert flags == ""


def test_build_coherence_flags_flags_pnative_drift(tmp_path):
    # model_setup P_native = 400 but design-point row says 233 → coherence FLAG.
    drifted = HELPER_FORM.replace("P_native = 233.0", "P_native = 400.0")
    _script(tmp_path, drifted)
    flags = build_coherence_flags(_concept(), tmp_path, tmp_path / "analysis.md")
    assert "FLAG" in flags
    assert "P_native" in flags


def test_build_coherence_flags_clean_trio_no_flag(tmp_path):
    _script(tmp_path, HELPER_FORM)
    flags = build_coherence_flags(_concept(), tmp_path, tmp_path / "analysis.md")
    # P_native coherent (233 == 233); the line is rendered without a FLAG prefix.
    assert "coherent" in flags.lower()
    assert "P_native" not in flags.split("\n")[0] or "FLAG" not in flags.split("\n")[0]


# ---------------------------------------------------------------------------
# Common-vars / model-vars new keys + prompt blocks
# ---------------------------------------------------------------------------


def test_design_point_block_renders_selection_fields():
    block = design_point_block(_concept())
    assert "## Design Point" in block
    assert "ARC 2015 Conservative Pilot" in block
    assert "233 MWe" in block
    assert "forbidden to edit" in block


def test_design_point_block_honest_when_pending():
    block = design_point_block(_concept(design_point=None))
    assert "upstream-pending" in block


def test_canonical_accounts_block_archetype_filtered():
    block = canonical_accounts_block(_concept())
    assert "C220103" in block  # tokamak has confinement magnets
    # An archetype with no mapping renders an honest note, not a fabricated list.
    note = canonical_accounts_block(_concept(archetype_enum=""))
    assert "does not apply" in note


def test_comparables_block_renders_list():
    assert "21-spherical-tokamak-hts" in comparables_block(_concept())
    assert "No comparable" in comparables_block(_concept(comparables=[]))


def test_fit_grade_band_line_single_source():
    line = fit_grade_band_line(_concept())
    assert "0–4" in line  # High band from FIT_GRADE_OVERRIDE_BAND


def test_fit_grade_band_constant_single_source():
    assert FIT_GRADE_OVERRIDE_BAND["High"] == (0, 4)
    assert FIT_GRADE_OVERRIDE_BAND["Med"] == (3, 8)
    assert FIT_GRADE_OVERRIDE_BAND["Low"] == (6, 12)


def test_build_common_vars_includes_four_new_keys():
    # Exercise the real _build_common_vars against a concept with a dossier.
    import sys
    sys.path.insert(0, "exploration/concept_analysis/scripts")
    from lib.concepts import load_concepts
    from run_analysis import _build_common_vars

    arc = next(c for c in load_concepts() if c["_id"].startswith("01-"))
    cv = _build_common_vars(arc)
    if cv is None:
        pytest.skip("ARC dossier not present in this checkout")
    for key in ("design_point_block", "canonical_accounts", "comparables_block", "fit_grade_band"):
        assert key in cv and cv[key]
