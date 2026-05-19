"""Slice-2 acceptance tests for the component_modularity embedding group.

Covers FR-5 (xlsx-collapse within ±0.4), FR-6 (slice-1 preservation when the
component aggregate is zeroed), and band correctness for the seven rating
embeddings.
"""
from __future__ import annotations

import csv
from pathlib import Path

import pytest
import yaml

from exploration.scoring_v2 import score
from exploration.scoring_v2.embeddings import rulebook
from exploration.scoring_v2.lib import schema as schema_mod
from exploration.scoring_v2.lib.extractors import taxonomy

REPO_ROOT = Path(__file__).resolve().parents[2]
FEATURES_DIR = REPO_ROOT / "exploration" / "scoring_v2" / "features"
SLICE1_WEIGHTS = REPO_ROOT / "exploration" / "scoring_v2" / "weights" / "slice1.yaml"

# xlsx "Worked Examples" final modularity scores (Concept Multipliers tab).
# These are the calibration targets for the xlsx-collapse hypothesis (FR-5).
XLSX_FINAL = {
    "01-hts-compact-tokamak":      5.00,
    "08-frc-w-direct-conversion":  4.65,
    "10-large-scale-stellarator":  2.18,
    "00a-iter":                    1.40,
    "00b-nif":                     1.83,
    "00c-inertia-life":            4.15,
}

# Concepts where the xlsx-collapse hypothesis is known to fail with documented
# diagnosis (see .project/active/scoring-v2-component-modularity-slice/
# implementation_notes.md). Per FR-5, a documented negative result is acceptable
# evidence; keep these on the radar via xfail rather than silencing them.
XLSX_KNOWN_GAPS = {
    "01-hts-compact-tokamak": (
        "CFS ARC under-rates by ~1.0. Coils dominate (78% capex share) and "
        "coils_rating tops out at 4 for HTS+compact tokamak. xlsx implicitly "
        "treats this configuration as the modularity ideal (rating 5). Fix: "
        "tighten coils_rating to distinguish 'HTS+compact+small modules' from "
        "'HTS+compact'. Deferred to slice 3."
    ),
    "08-frc-w-direct-conversion": (
        "v3-data deviation: Mallory's ontology v3 (main PR #16) reclassified Helion's "
        "Magnet Type from 'Pulsed EM' to 'Resistive', which lowers the coils_rating "
        "and the xlsx-collapse aggregate (3.98 vs xlsx-baseline 4.65, delta -0.67). "
        "The pre-v3 xlsx baseline was authored against the older taxonomy. "
        "Re-baselining vs v3 data is a slice-3 task (see concept-downselect-merge "
        "implementation_notes Phase 3)."
    ),
}

RATING_EMBEDDINGS = (
    "vessel_rating", "coils_rating", "blanket_rating", "bop_rating",
    "fuel_cycle_rating", "aux_rating", "civil_rating",
)


def _load_doc(cid: str) -> dict | None:
    p = FEATURES_DIR / f"{cid}.yaml"
    if not p.exists():
        return None
    return yaml.safe_load(p.read_text())


def _aggregate_for(cid: str) -> float | None:
    doc = _load_doc(cid)
    if doc is None:
        return None
    values, _conf = score._evaluate_concept(doc)
    return values.get("component_modularity_aggregate")


def test_every_rating_is_int_in_band_for_all_concepts():
    """FR-1: each rating returns an integer 1..5 for every concept on disk."""
    for cid in taxonomy.all_concept_ids():
        doc = _load_doc(cid)
        if doc is None:
            continue
        values, _ = score._evaluate_concept(doc)
        for name in RATING_EMBEDDINGS:
            v = values[name]
            assert isinstance(v, int), f"{cid}.{name}: not int ({type(v).__name__})"
            assert 1 <= v <= 5, f"{cid}.{name}: {v} out of 1..5 band"


def test_aggregate_returns_none_when_weights_absent():
    """Concepts without a cost model leave w_* absent → aggregate is None."""
    # 02-acoustic-icf-sonofusion is one such concept (no model_output.txt).
    val = _aggregate_for("02-acoustic-icf-sonofusion")
    assert val is None


def test_aggregate_is_in_band_when_weights_present():
    """When the seven w_* are present, the weighted sum is in 1..5."""
    val = _aggregate_for("01-hts-compact-tokamak")
    assert val is not None
    assert 1.0 <= val <= 5.0


@pytest.mark.parametrize("cid,xlsx_final", sorted(XLSX_FINAL.items()))
def test_xlsx_collapse_within_tolerance(cid: str, xlsx_final: float, request):
    """FR-5: aggregate matches xlsx final score within ±0.4 (no family multiplier).

    Reference concepts (00a/00b/00c) are user-added; skip until they exist.
    Known-gap concepts (XLSX_KNOWN_GAPS) are marked xfail with diagnosis —
    per FR-5, a documented negative result is acceptable evidence.
    """
    val = _aggregate_for(cid)
    if val is None:
        pytest.skip(f"{cid}: not in features/ yet (reference concept pending)")
    if cid in XLSX_KNOWN_GAPS:
        request.applymarker(pytest.mark.xfail(
            reason=XLSX_KNOWN_GAPS[cid], strict=True,
        ))
    delta = val - xlsx_final
    assert abs(delta) <= 0.4, (
        f"{cid}: aggregate={val:.3f} vs xlsx={xlsx_final:.3f} (delta={delta:+.3f}) "
        f"— xlsx-collapse hypothesis under-discriminates. See implementation_notes."
    )


@pytest.mark.xfail(
    reason=(
        "v3-data deviation: ontology v3 taxonomy edits invalidate slice-1 baselines "
        "(Helion Magnet Type changed Pulsed EM -> Resistive). Re-baseline in slice 3. "
        "See concept-downselect-merge implementation_notes Phase 3."
    ),
    strict=True,
)
def test_slice1_preservation_under_slice1_weights(tmp_path):
    """FR-6: with component_modularity zeroed, slice-1 numbers reproduce exactly."""
    scores_dir = tmp_path / "scores"
    out = score.run(FEATURES_DIR, scores_dir, SLICE1_WEIGHTS)
    rows = list(csv.DictReader(out.open()))
    mso = {r["concept_id"]: float(r["manufacturability_scale_out"]) for r in rows}
    assert abs(mso["08-frc-w-direct-conversion"] - 4.80) < 0.01
    assert abs(mso["01-hts-compact-tokamak"] - 2.90) < 0.01
    assert abs(mso["10-large-scale-stellarator"] - 1.50) < 0.01


def test_score_deterministic_byte_identical_under_default_weights(tmp_path):
    """FR-8: two runs over unchanged inputs produce byte-identical output."""
    sd1 = tmp_path / "s1"
    sd2 = tmp_path / "s2"
    weights = REPO_ROOT / "exploration" / "scoring_v2" / "weights" / "default.yaml"
    out1 = score.run(FEATURES_DIR, sd1, weights)
    out2 = score.run(FEATURES_DIR, sd2, weights)
    assert out1.read_bytes() == out2.read_bytes()
