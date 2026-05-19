"""Phase 3 acceptance tests: plant_level_modularity ordering + iteration affordances.

Slice 2 introduced the component_modularity group, so the slice-1 acceptance
numbers only land under the slice-1 reference weights (weights/slice1.yaml,
which zeroes the component aggregate). These tests pin them under that config.
"""
from __future__ import annotations

import csv
from pathlib import Path

import pytest
import yaml

# v3-data deviation: see implementation_notes.md for concept-downselect-merge,
# Phase 3. Ontology v3 (main PR #16) changed taxonomy values for several
# concepts (notably Helion 08 Magnet Type Pulsed EM -> Resistive), so the
# slice-1 acceptance numbers (Helion 4.80, CFS 2.90, Stellarator 1.50) no
# longer reproduce under the new data. Re-baselining is a slice-3 task.
V3_DATA_DEVIATION = (
    "v3-data deviation: ontology v3 taxonomy edits invalidate slice-1 baselines "
    "(Helion Magnet Type changed Pulsed EM -> Resistive). Re-baseline in slice 3."
)

REPO_ROOT = Path(__file__).resolve().parents[2]
SLICE1_WEIGHTS = REPO_ROOT / "exploration" / "scoring_v2" / "weights" / "slice1.yaml"


def _read_csv(p: Path) -> list[dict[str, str]]:
    with open(p) as f:
        return list(csv.DictReader(f))


def _mso_by_id(scores_dir: Path) -> dict[str, float]:
    rows = _read_csv(scores_dir / "table.csv")
    return {r["concept_id"]: float(r["manufacturability_scale_out"]) for r in rows}


@pytest.mark.xfail(reason=V3_DATA_DEVIATION, strict=True)
def test_plant_level_modularity_ordering(run_cli, tmp_scores_dir: Path):
    run_cli("score.py", weights=SLICE1_WEIGHTS)
    mso = _mso_by_id(tmp_scores_dir)
    helion = mso["08-frc-w-direct-conversion"]
    cfs = mso["01-hts-compact-tokamak"]
    stell = mso["10-large-scale-stellarator"]
    assert helion > cfs > stell, f"order broken: helion={helion} cfs={cfs} stell={stell}"
    assert abs(helion - 4.80) < 0.05
    assert abs(cfs - 2.90) < 0.05
    assert abs(stell - 1.50) < 0.05


def test_weight_edit_propagates_without_extraction(
    run_cli, tmp_scores_dir: Path, tmp_path: Path
):
    # Run under slice-1 weights to make the per-embedding contribution
    # arithmetic exact (no cm_aggregate noise).
    import shutil
    weights_path = tmp_path / "slice1.yaml"
    shutil.copy(SLICE1_WEIGHTS, weights_path)
    run_cli("score.py", weights=weights_path)
    before = _mso_by_id(tmp_scores_dir)["08-frc-w-direct-conversion"]
    # Double unit_multiplicity weight; Helion's multiplicity score is 4, so MSO should
    # gain 0.20 * 4 = 0.80.
    weights = yaml.safe_load(weights_path.read_text())
    weights["manufacturability_scale_out"]["unit_multiplicity"] = 0.40
    weights_path.write_text(yaml.safe_dump(weights, sort_keys=False))
    run_cli("score.py", weights=weights_path)
    after = _mso_by_id(tmp_scores_dir)["08-frc-w-direct-conversion"]
    assert abs((after - before) - 0.80) < 1e-6


def test_feature_edit_changes_score_deterministically(
    run_cli, tmp_features_dir: Path, tmp_scores_dir: Path
):
    run_cli("score.py", weights=SLICE1_WEIGHTS)
    cfs_before = _mso_by_id(tmp_scores_dir)["01-hts-compact-tokamak"]

    target = tmp_features_dir / "01-hts-compact-tokamak.yaml"
    doc = yaml.safe_load(target.read_text())
    # HTS (wound) → Resistive flips hardware_topology_complexity out of the HTS-compact branch.
    doc["magnet_type"]["value"] = "Resistive"
    target.write_text(yaml.safe_dump(doc, sort_keys=False))
    run_cli("score.py", weights=SLICE1_WEIGHTS)
    cfs_after = _mso_by_id(tmp_scores_dir)["01-hts-compact-tokamak"]
    assert cfs_after < cfs_before
