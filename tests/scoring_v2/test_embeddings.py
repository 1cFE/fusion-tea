"""Phase 3 acceptance tests: plant_level_modularity ordering + iteration affordances."""
from __future__ import annotations

import csv
from pathlib import Path

import yaml


def _read_csv(p: Path) -> list[dict[str, str]]:
    with open(p) as f:
        return list(csv.DictReader(f))


def _mso_by_id(scores_dir: Path) -> dict[str, float]:
    rows = _read_csv(scores_dir / "table.csv")
    return {r["concept_id"]: float(r["manufacturability_scale_out"]) for r in rows}


def test_plant_level_modularity_ordering(run_cli, tmp_scores_dir: Path):
    run_cli("score.py")
    mso = _mso_by_id(tmp_scores_dir)
    helion = mso["08-frc-w-direct-conversion"]
    cfs = mso["01-hts-compact-tokamak"]
    stell = mso["10-large-scale-stellarator"]
    assert helion > cfs > stell, f"order broken: helion={helion} cfs={cfs} stell={stell}"
    assert abs(helion - 4.80) < 0.05
    assert abs(cfs - 2.90) < 0.05
    assert abs(stell - 1.50) < 0.05


def test_weight_edit_propagates_without_extraction(
    run_cli, tmp_scores_dir: Path, tmp_weights_file: Path
):
    run_cli("score.py")
    before = _mso_by_id(tmp_scores_dir)["08-frc-w-direct-conversion"]
    # Double unit_multiplicity weight; Helion's multiplicity score is 4, so MSO should
    # gain 0.20 * 4 = 0.80 (and a smaller bump from inherent renormalization, since we're
    # just adding weight, not renormalizing).
    weights = yaml.safe_load(tmp_weights_file.read_text())
    weights["manufacturability_scale_out"]["unit_multiplicity"] = 0.40
    tmp_weights_file.write_text(yaml.safe_dump(weights, sort_keys=False))
    run_cli("score.py")
    after = _mso_by_id(tmp_scores_dir)["08-frc-w-direct-conversion"]
    # Helion multiplicity=4, weight +0.20 → +0.80.
    assert abs((after - before) - 0.80) < 1e-6


def test_feature_edit_changes_score_deterministically(
    run_cli, tmp_features_dir: Path, tmp_scores_dir: Path
):
    run_cli("score.py")
    cfs_before = _mso_by_id(tmp_scores_dir)["01-hts-compact-tokamak"]

    target = tmp_features_dir / "01-hts-compact-tokamak.yaml"
    doc = yaml.safe_load(target.read_text())
    # HTS (wound) → Resistive flips hardware_topology_complexity out of the HTS-compact branch.
    doc["magnet_type"]["value"] = "Resistive"
    target.write_text(yaml.safe_dump(doc, sort_keys=False))
    run_cli("score.py")
    cfs_after = _mso_by_id(tmp_scores_dir)["01-hts-compact-tokamak"]
    assert cfs_after < cfs_before
