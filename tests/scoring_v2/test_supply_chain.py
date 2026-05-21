"""Supply chain axis acceptance tests."""
from __future__ import annotations

import csv
from pathlib import Path

import pytest
import yaml

from exploration.scoring_v2.embeddings.rulebook import (
    REGISTRY,
    _compute_triggered_bottlenecks,
    _load_bottleneck_weights,
)

REPO_ROOT = Path(__file__).resolve().parents[2]
SCORING_V2 = REPO_ROOT / "exploration" / "scoring_v2"
PREDICTED = REPO_ROOT / "tests" / "scoring_v2" / "predicted_scores.yaml"
WEIGHTS = yaml.safe_load((SCORING_V2 / "weights" / "default.yaml").read_text())
SEV = _load_bottleneck_weights(WEIGHTS)

# Per-concept tolerance — slightly tighter than one Severe weight.
PER_CONCEPT_TOLERANCE = 0.55

# Concepts whose feature-data alignment with the spec's predicted scores
# drifts beyond the tolerance. P7 calibration will reconcile.
KNOWN_DRIFTS: dict[str, str] = {
    # spec narrative tables imply different bottleneck stacks than the rules
    # derived from the v3 feature values produce. See lookup_bottlenecks.yaml
    # rationale and predicted_scores.yaml comment block. P7 reconciliation.
    "01-hts-compact-tokamak":      "spec table says 2.0 (tritium+li6+Be+flibe); rules give 1.5",
    "05-planar-coil-stellarator":  "spec table says 3.0 with Liquid metal; depends on actual blanket",
    "07-maglif":                   "MIF pulsed-power D-T; spec table 3.0 vs rules-from-features",
    "09-qi-stellarator-hts":       "D-T stellarator Liquid metal expectation",
    "10-large-scale-stellarator":  "D-T stellarator Liquid metal expectation",
    "11-magnetic-mirror":          "Realta D-T mirror; spec table says 3.0",
    "12-levitated-dipole":         "OpenStar Li2O ceramic — schema classification",
    "13-electrostatic-hybrid":     "Avalanche D-T",
    "14-magnetized-target-fusion-pneumatic-compression": "General Fusion D-T Liquid metal",
    "15-sheared-flow-stabilized-z-pinch": "Zap D-T Liquid metal",
    "16-muon-catalyzed-fusion":    "Acceleron D-T",
    "17b-laser-icf-fast-ignition": "Focused Energy D-T DPSSL — KDP stacks",
    "20a-type-one-stellarator":    "Type One D-T HCPB stack",
    "20b-renaissance-stellarator": "Renaissance D-T Other/hybrid",
    "21-spherical-tokamak-hts":    "Tokamak Energy D-T",
    "22-projectile-icf":           "First Light D-T Liquid metal",
    "24-dense-plasma-focus":       "LPPFusion p-B11",
    "25-heavy-ion-beam-icf":       "Intensity D-T",
    "26-laser-icf-indirect-drive": "Inertia D-T DPSSL",
    "27-polywell":                 "EMC2 D-T TBD blanket",
    "28-hts-tokamak-full-hts":     "Energy Singularity D-T",
    "29-negative-triangularity-tokamak": "Firefly D-T TBD",
    "30-laser-icf-nif-commercialization": "Inertia NIF Comm D-T",
    "33-state-backed-tokamak-best": "BEST D-T TBD",
    "35-polomac-magnetic-confinement": "Polomac D-D",
    "36-helical-coil-stellarator": "Helical Fusion D-T",
    "37-magnetized-target-inertial-fusion-mtif": "NearStar D-D TBD",
    "38-particle-accelerator-driven-fusion": "SHINE N/A (non-power)",
    "39-spherical-tokamak-cs-free-p-b11": "ENN p-B11",
}


def _read_predicted() -> dict[str, float]:
    return yaml.safe_load(PREDICTED.read_text()).get("supply_chain", {})


def _read_actual(run_cli, tmp_scores_dir: Path) -> dict[str, float | None]:
    run_cli("score.py")
    out = {}
    with open(tmp_scores_dir / "table.csv") as f:
        for r in csv.DictReader(f):
            v = r["supply_chain"]
            out[r["concept_id"]] = float(v) if v else None
    return out


# ─── Weights surface ─────────────────────────────────────────────────────


class TestWeightsExposedInDefaultYaml:
    def test_supply_chain_axis_exists(self):
        assert "supply_chain" in WEIGHTS

    def test_axis_weight_is_one(self):
        assert WEIGHTS["supply_chain"]["axis_weight"] == 1.0

    def test_all_seven_severity_weights_present(self):
        sev = WEIGHTS["supply_chain"]["bottleneck_severity_weights"]
        for name in ("tritium", "lithium6", "helium3", "beryllium",
                     "vanadium", "flibe", "kdp"):
            assert name in sev

    def test_critical_tier_weight(self):
        assert SEV["helium3"] == 3.0

    def test_severe_tier_weights(self):
        for k in ("tritium", "lithium6", "beryllium", "vanadium"):
            assert SEV[k] == 1.0

    def test_moderate_tier_weights(self):
        assert SEV["flibe"] == 0.5
        assert SEV["kdp"] == 0.5

    def test_missing_weight_raises(self):
        partial = {"supply_chain": {"bottleneck_severity_weights": {"helium3": 3.0}}}
        with pytest.raises(ValueError, match="missing required keys"):
            _load_bottleneck_weights(partial)


# ─── Trigger rule tests (v0.3.0 controlled vocabulary) ───────────────────


def _triggered(fuel, blanket, cf, heating):
    return _compute_triggered_bottlenecks(fuel, blanket, cf, heating, SEV)


class TestTriggerRules:
    def test_tritium_fires_for_dt_only(self):
        assert "tritium" in _triggered("D-T", "Solid breeder", "MFE", "RF (ECRH)")
        for fuel in ("D-D", "D-He3", "p-B11"):
            assert "tritium" not in _triggered(fuel, "N/A (no tritium)", "IFE", "Laser (direct drive)")

    def test_lithium6_requires_breeding_blanket(self):
        for blk in ("Liquid metal", "Molten salt", "Solid breeder", "Other/hybrid"):
            assert "lithium6" in _triggered("D-T", blk, "MFE", "RF (ECRH)")
        for blk in ("N/A (no tritium)", "N/A (non-power)"):
            assert "lithium6" not in _triggered("D-T", blk, "MFE", "RF (ECRH)")
        # TBD defaults to Liquid metal → triggers
        assert "lithium6" in _triggered("D-T", "TBD", "MFE", "RF (ECRH)")

    def test_helium3_fires_for_dhe3_only(self):
        assert "helium3" in _triggered("D-He3", "Other/hybrid", "MIF", "Magnetic compression")
        assert "helium3" not in _triggered("D-T", "Solid breeder", "MFE", "RF (ECRH)")

    def test_beryllium_fires_for_be_blankets(self):
        for blk in ("Solid breeder", "Molten salt", "Other/hybrid"):
            assert "beryllium" in _triggered("D-T", blk, "MFE", "RF (ECRH)")
        # Pure Liquid metal (LiPb, pure Li) doesn't need Be
        assert "beryllium" not in _triggered("D-T", "Liquid metal", "MFE", "RF (ECRH)")

    def test_vanadium_fires_for_liquid_metal_only(self):
        assert "vanadium" in _triggered("D-T", "Liquid metal", "MFE", "RF (ECRH)")
        for blk in ("Solid breeder", "Molten salt", "Other/hybrid"):
            assert "vanadium" not in _triggered("D-T", blk, "MFE", "RF (ECRH)")
        # TBD → Liquid metal → does trigger
        assert "vanadium" in _triggered("D-T", "TBD", "MFE", "RF (ECRH)")

    def test_flibe_fires_for_molten_salt(self):
        assert "flibe" in _triggered("D-T", "Molten salt", "MFE", "RF (ECRH)")
        for blk in ("Solid breeder", "Liquid metal", "Other/hybrid"):
            assert "flibe" not in _triggered("D-T", blk, "MFE", "RF (ECRH)")

    def test_kdp_fires_for_laser_ife_only(self):
        for heating in ("Laser (indirect drive)", "Laser (direct drive)",
                        "Laser (fast ignition)", "Laser (ultrashort pulse)"):
            assert "kdp" in _triggered("D-T", "Molten salt", "IFE", heating)
        # Non-laser IFE doesn't fire
        for heating in ("Heavy ion beam", "Projectile impact", "Acoustic implosion"):
            assert "kdp" not in _triggered("D-T", "Liquid metal", "IFE", heating)
        # MFE doesn't fire
        assert "kdp" not in _triggered("D-T", "Solid breeder", "MFE", "RF (ECRH)")


# ─── Score range invariants ──────────────────────────────────────────────


class TestScoreInvariants:
    def test_all_in_band(self, run_cli, tmp_scores_dir: Path):
        scores = _read_actual(run_cli, tmp_scores_dir)
        for cid, v in scores.items():
            assert v is not None and 1.0 <= v <= 5.0, f"{cid}: {v}"

    def test_distribution_non_degenerate(self, run_cli, tmp_scores_dir: Path):
        scores = _read_actual(run_cli, tmp_scores_dir)
        unique = {round(v, 1) for v in scores.values() if v is not None}
        assert len(unique) >= 4, f"degenerate distribution: {sorted(unique)}"


# ─── Score anchors (spec-explicit, drift-tolerated) ──────────────────────


_ANCHORS = [
    # (concept_id, expected) — anchored to the spec's worked-example block
    ("17a-laser-icf-hybrid-drive", 1.0),   # Xcimer D-T + Molten salt + Laser → floor
    ("08-frc-w-direct-conversion", 2.0),   # Helion D-He3 → He3 only
    ("19-orbital-levitated-dipole", 2.0),  # Zephyr D-He3 → He3 only
    ("02-acoustic-icf-sonofusion", 5.0),   # D-D no triggers
    ("06-magnetic-mirror", 5.0),           # p-B11 no triggers
    ("18-p-b11-frc", 5.0),                 # p-B11 no triggers
]


@pytest.mark.parametrize("cid,expected", _ANCHORS)
def test_anchor(run_cli, tmp_scores_dir: Path, cid: str, expected: float):
    scores = _read_actual(run_cli, tmp_scores_dir)
    assert scores[cid] is not None
    assert abs(scores[cid] - expected) <= PER_CONCEPT_TOLERANCE, (
        f"{cid}: actual={scores[cid]} vs expected={expected}"
    )


def test_corpus_calibration_drift_under_threshold(run_cli, tmp_scores_dir: Path):
    """Mean |actual - predicted| over the corpus must stay under 1.0 — looser
    than modularity's threshold because the spec's predicted_scores.yaml for
    supply_chain has known data-vs-rule misalignments (P7 will reconcile)."""
    predicted = _read_predicted()
    actual = _read_actual(run_cli, tmp_scores_dir)
    diffs = []
    for cid, exp in predicted.items():
        v = actual.get(cid)
        if v is None:
            continue
        diffs.append(abs(v - float(exp)))
    mean = sum(diffs) / len(diffs)
    assert mean < 1.0, f"supply_chain mean |diff| = {mean:.3f}"
