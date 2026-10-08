"""Current raw modularity arithmetic, active lookup coverage and diagnostics.

Seven component-level anchors exercise the production formula. The MIF cases
use independent source CAS amounts and the approved two-slot driver/chamber ratings.
"""

from __future__ import annotations

from pathlib import Path

import pytest
import yaml

from exploration.scoring_v2 import score
from exploration.scoring_v2.lib import schema as schema_mod

REPO_ROOT = Path(__file__).resolve().parents[2]
WEIGHTS_DEFAULT = REPO_ROOT / "exploration" / "scoring_v2" / "weights" / "default.yaml"

# Per-concept tolerance for v5 calibration. 0.20 absorbs the residual drift
# between idealized capex shares assumed by the v5 narrative and what the
# cost_model extractor produces from model_output.txt.
PER_CONCEPT_TOLERANCE = 0.20


def _run_score(
    run_cli, tmp_scores_dir: Path, tmp_features_dir: Path | None = None
) -> dict[str, float | None]:
    """Return per-concept *raw* modularity scores (pre-normalization).

    The v5 calibration tests check the raw weighted-formula output, not the
    corpus-normalized output that score.py writes to table.csv. Evaluate the
    current feature inputs through production embeddings; persisted diagnostics
    alone would not detect a formula regression.
    """
    if tmp_features_dir is None:
        # Live features directory — fallback when fixture wasn't passed.
        tmp_features_dir = REPO_ROOT / "exploration" / "scoring_v2" / "features"
    rows: dict[str, float | None] = {}
    weights = yaml.safe_load(WEIGHTS_DEFAULT.read_text())
    schema = schema_mod.load_schema()
    for f in sorted(Path(tmp_features_dir).glob("*.yaml")):
        doc = yaml.safe_load(f.read_text())
        cid = doc["_meta"]["concept_id"]
        embeddings, confidence = score._evaluate_concept(doc, weights, schema)
        rows[cid], _ = score._score_axis(weights["modularity"], embeddings, confidence)
    return rows


# June 17 two-slot inputs from weights/default.yaml and the source CAS rows.
# MagLIF: energy delivery = 1.2 + 364.5; containment = 102.8 + 6.4 + 14.9 + 134.9 + 8.3.
# NearStar: its narrative M$ subaccount lines are unparsed; only CAS27 supplies containment.
_CURRENT_MIF_ANCHORS = {
    "07-maglif": (5, 5, 4.5, 3 - 0.5, 1.2 + 364.5, 102.8 + 6.4 + 14.9 + 134.9 + 8.3),
    "37-magnetized-target-inertial-fusion-mtif": (5, 5, 2, 4, 0, 4.1),
}


# ─── Top-level shape ─────────────────────────────────────────────────────


def test_modularity_score_in_band_for_all_concepts(run_cli, tmp_scores_dir: Path):
    """Every concept's modularity score is in [1.0, 5.0] (or None for
    null-handled axes — but modularity is fully wired so none should be
    null on this PR)."""
    scores = _run_score(run_cli, tmp_scores_dir)
    assert len(scores) == 40
    for cid, s in scores.items():
        assert s is not None, f"{cid}: modularity is null"
        assert 1.0 <= s <= 5.0, f"{cid}: modularity={s} out of band"


def test_modularity_distribution_non_degenerate(run_cli, tmp_scores_dir: Path):
    """At least 5 distinct values across 40 concepts (R8 cross-axis sanity)."""
    scores = _run_score(run_cli, tmp_scores_dir)
    rounded = {round(s, 1) for s in scores.values() if s is not None}
    assert len(rounded) >= 5, (
        f"modularity distribution too narrow: {len(rounded)} distinct values ({sorted(rounded)})"
    )


# ─── V5 calibration anchors ──────────────────────────────────────────────
# Spec-explicit anchors from modularity_implementation_spec.md "Predicted scores".


_ANCHORS = [
    # (concept_id, expected, rationale)
    ("01-hts-compact-tokamak", 3.71, "CFS ARC worked example"),
    ("08-frc-w-direct-conversion", 5.00, "Helion worked example"),
    ("33-state-backed-tokamak-best", 1.91, "BEST worked example (LTS-override floor)"),
    ("07-maglif", 4.93, "Pacific MagLIF"),
    ("37-magnetized-target-inertial-fusion-mtif", 5.00, "NearStar MTIF"),
    ("14-magnetized-target-fusion-pneumatic-compression", 4.88, "General Fusion"),
    ("36-helical-coil-stellarator", 2.03, "Helical Fusion continuous winding"),
]


@pytest.mark.parametrize("cid,expected,reason", _ANCHORS)
def test_v5_anchor(run_cli, tmp_scores_dir: Path, cid: str, expected: float, reason: str):
    """Current raw formula anchors reproduce within PER_CONCEPT_TOLERANCE."""
    if cid in _CURRENT_MIF_ANCHORS:
        mvs, units, driver, chamber, energy, containment = _CURRENT_MIF_ANCHORS[cid]
        weights = yaml.safe_load(WEIGHTS_DEFAULT.read_text())["modularity"]
        if cid == "07-maglif":
            accounts = {
                "C220104": 1.2,
                "C220107": 364.5,
                "C220101": 102.8,
                "C220105": 6.4,
                "C220106": 14.9,
                "C220108": 134.9,
                "CAS27": 8.3,
            }
            source = REPO_ROOT / f"exploration/concept_analysis/analyses/{cid}/model_output.txt"
            observed = {
                parts[0]: float(parts[3])
                for line in source.read_text().splitlines()
                if (parts := line.split()) and parts[0] in accounts
            }
            assert observed == accounts
            assert weights["driver_modularity_lookup"]["MIF|LTD pulsed power"] == driver
            assert weights["chamber_blanket_lookup"]["chamber_base"]["MIF|large"] == 3
            assert weights["chamber_blanket_lookup"]["blanket_penalty"]["TBD"] == -0.5
        else:
            source = REPO_ROOT / f"exploration/concept_analysis/analyses/{cid}/model_output.txt"
            special = next(
                line.split()[-1]
                for line in source.read_text().splitlines()
                if line.startswith("CAS27 ")
            )
            assert float(special) == containment
            assert weights["driver_modularity_lookup"]["MIF|Railgun"] == driver
            assert weights["chamber_blanket_lookup"]["chamber_base"]["MIF|medium"] == chamber
            assert weights["chamber_blanket_lookup"]["blanket_penalty"]["None"] == 0
            doc = yaml.safe_load(
                (REPO_ROOT / f"exploration/scoring_v2/features/{cid}.yaml").read_text()
            )
            assert doc["fuel"]["value"] == "D-D"
            assert doc["w_energy_delivery"]["value"] == energy
        expected = (
            0.5 * mvs
            + 0.25 * ((driver * energy + chamber * containment) / (energy + containment))
            + 0.25 * units
        )
    scores = _run_score(run_cli, tmp_scores_dir)
    actual = scores[cid]
    assert actual is not None, f"{cid}: score is null ({reason})"
    diff = abs(actual - expected)
    assert diff <= PER_CONCEPT_TOLERANCE, (
        f"{cid}: actual={actual:.3f} vs expected={expected:.2f} "
        f"(|diff|={diff:.3f} > {PER_CONCEPT_TOLERANCE}) — {reason}"
    )


# ─── Embedding-level traceability ────────────────────────────────────────


def test_modularity_diagnostics_block_present():
    """Every feature file has a modularity_diagnostics block populated by
    populate_modularity_diagnostics.py."""
    feature_files = sorted((REPO_ROOT / "exploration" / "scoring_v2" / "features").glob("*.yaml"))
    for f in feature_files:
        doc = yaml.safe_load(f.read_text())
        block = doc.get("modularity_diagnostics")
        assert isinstance(block, dict), f"{f.name}: modularity_diagnostics missing"
        for required_key in (
            "min_viable_device_scale",
            "percent_mod",
            "unit_multiplicity",
            "modularity_score",
            "mvs_lookup_key",
            "vessel_lookup_key",
            "magnet_driver_lookup_key",
            "blanket_lookup_key",
            "vessel_modularity_rating",
            "magnet_driver_modularity_rating",
            "blanket_modularity_rating",
            "capex_shares_used",
            "unit_count_estimate",
            "v5_calibration_target",
        ):
            assert required_key in block, f"{f.name}: modularity_diagnostics.{required_key} missing"


def test_all_lookup_keys_resolve_for_all_concepts():
    """Every concept's diagnostic block lookup keys exist in default.yaml's
    sub-tables. Catches new concepts that need lookup-table additions."""
    weights = yaml.safe_load(WEIGHTS_DEFAULT.read_text())
    modularity = weights.get("modularity") or {}
    mvs = modularity.get("mvs_lookup") or {}
    vessel = modularity.get("vessel_lookup") or {}
    magnet = modularity.get("magnet_driver_lookup") or {}
    blanket = modularity.get("blanket_lookup") or {}
    feature_files = sorted((REPO_ROOT / "exploration" / "scoring_v2" / "features").glob("*.yaml"))
    missing = []
    for f in feature_files:
        doc = yaml.safe_load(f.read_text())
        d = doc.get("modularity_diagnostics") or {}
        family = doc["confinement_family"]["value"]
        active = [("mvs_lookup", mvs, "mvs_lookup_key")]
        if family in ("IFE", "MIF"):
            assert d["percent_mod_path"] == "two_slot", f.stem
            active.extend(
                [
                    (
                        "driver_modularity_lookup",
                        modularity["driver_modularity_lookup"],
                        "driver_lookup_key",
                    ),
                    (
                        "chamber_blanket_lookup.chamber_base",
                        modularity["chamber_blanket_lookup"]["chamber_base"],
                        "chamber_blanket_lookup_key",
                    ),
                ]
            )
            penalty = (
                "None"
                if doc["fuel"]["value"] in ("p-B11", "D-He3", "D-D")
                else doc["blanket_config"]["value"]
            )
            if penalty in ("N/A", "N/A (no tritium)", "N/A (non-power)"):
                penalty = "None"
            assert penalty in modularity["chamber_blanket_lookup"]["blanket_penalty"], f.stem
        else:
            assert d["percent_mod_path"] == "three_slot", f.stem
            active.extend(
                [
                    ("vessel_lookup", vessel, "vessel_lookup_key"),
                    ("magnet_driver_lookup", magnet, "magnet_driver_lookup_key"),
                    ("blanket_lookup", blanket, "blanket_lookup_key"),
                ]
            )
        for tbl_name, table, key_field in active:
            key = d.get(key_field)
            if key not in table:
                missing.append(f"{f.stem}.{key_field}={key!r} not in {tbl_name}")
    assert not missing, "Lookup-table coverage gaps:\n  " + "\n  ".join(missing)


def test_bracket_schedule_matches_v5_calibration():
    """The unit_count brackets in default.yaml match the v5 spec table."""
    weights = yaml.safe_load(WEIGHTS_DEFAULT.read_text())
    brackets = weights.get("modularity", {}).get("unit_count_brackets")
    assert brackets, "unit_count_brackets missing from weights"
    schedule = {b["max_count"]: b["score"] for b in brackets}
    # Spec Change A: 1→1, 4→2, 10→3, 30→4, floor 5
    assert schedule == {1: 1, 4: 2, 10: 3, 30: 4}, f"unit_count brackets drift: {schedule}"
    floor = weights["modularity"].get("unit_count_floor_score")
    assert floor == 5
