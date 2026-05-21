"""Plant Complexity axis acceptance tests."""
from __future__ import annotations

import csv
from pathlib import Path

import pytest
import yaml

from exploration.scoring_v2.embeddings.rulebook import (
    _compute_triggered_pc_subsystems,
    _load_pc_weights,
)

REPO_ROOT = Path(__file__).resolve().parents[2]
SCORING_V2 = REPO_ROOT / "exploration" / "scoring_v2"
PREDICTED = REPO_ROOT / "tests" / "scoring_v2" / "predicted_scores.yaml"
WEIGHTS = yaml.safe_load((SCORING_V2 / "weights" / "default.yaml").read_text())
SEV = _load_pc_weights(WEIGHTS)

PER_CONCEPT_TOLERANCE = 0.55

KNOWN_DRIFTS = {
    "06-magnetic-mirror": "Pale Blue D-T mirror; spec table 3.5 vs rules 4.5",
    "07-maglif":          "Pacific MagLIF MIF; spec table 2.0 vs rules 1.0",
    "17a-laser-icf-hybrid-drive": "Xcimer Hybrid KrF; spec table 1.0 vs rules 2.5",
}


def _read_actual(run_cli, tmp_scores_dir: Path) -> dict[str, float | None]:
    run_cli("score.py")
    out = {}
    with open(tmp_scores_dir / "table.csv") as f:
        for r in csv.DictReader(f):
            v = r["plant_complexity"]
            out[r["concept_id"]] = float(v) if v else None
    return out


def _triggered(features: dict) -> dict[str, float]:
    return _compute_triggered_pc_subsystems(
        features.get("fuel", ""),
        features.get("confinement_family", ""),
        features.get("confinement_concept", ""),
        features.get("ife_driver", ""),
        features.get("mif_method", ""),
        features.get("magnet_type", ""),
        features.get("blanket_config", ""),
        features.get("energy_capture", ""),
        features.get("primary_heating", ""),
        features.get("operation_mode", ""),
        features.get("repetition_rate", ""),
        SEV,
    )


# ─── Weights surface ─────────────────────────────────────────────────────


class TestWeightsSurface:
    def test_all_14_weights_present(self):
        for sub in ("tritium_plant", "remote_maintenance", "hybrid_energy",
                    "cryoplant_lts", "cryoplant_hts",
                    "target_factory_high", "target_factory_low",
                    "pulsed_power_thermal", "high_power_aux", "rf_aux",
                    "disruption_mitigation", "current_drive",
                    "liquid_metal_handling", "levitation_stabilization"):
            assert sub in SEV

    def test_critical_tier(self):
        assert SEV["target_factory_high"] == 2.0

    def test_severe_tiers(self):
        for s in ("tritium_plant", "remote_maintenance", "cryoplant_lts",
                  "high_power_aux", "disruption_mitigation", "pulsed_power_thermal"):
            assert SEV[s] == 1.0

    def test_moderate_tiers(self):
        for m in ("cryoplant_hts", "rf_aux", "hybrid_energy",
                  "target_factory_low", "liquid_metal_handling",
                  "current_drive", "levitation_stabilization"):
            assert SEV[m] == 0.5


# ─── Trigger rules ───────────────────────────────────────────────────────


class TestTriggerRules:
    def test_tritium_plant_fires_for_dt(self):
        t = _triggered({"fuel": "D-T", "blanket_config": "Liquid metal",
                         "confinement_family": "MFE", "mfe_topology": "Tokamak"})
        assert "tritium_plant" in t

    def test_tritium_plant_skipped_for_shine(self):
        t = _triggered({"fuel": "D-T", "blanket_config": "N/A (non-power)",
                         "confinement_family": "Non-Standard"})
        assert "tritium_plant" not in t

    def test_remote_maintenance_for_neutronic(self):
        for fuel in ("D-T", "D-D"):
            t = _triggered({"fuel": fuel, "blanket_config": "N/A (no tritium)"})
            assert "remote_maintenance" in t
        for fuel in ("p-B11", "D-He3"):
            t = _triggered({"fuel": fuel, "blanket_config": "N/A (no tritium)"})
            assert "remote_maintenance" not in t

    def test_target_factory_high(self):
        t = _triggered({
            "fuel": "D-T", "confinement_family": "IFE",
            "ife_driver": "Laser", "repetition_rate": "~10 Hz",
        })
        assert "target_factory_high" in t

    def test_target_factory_acoustic_excluded(self):
        # Acoustic implosion (Sonofusion) doesn't use manufactured targets
        t = _triggered({
            "fuel": "D-D", "confinement_family": "IFE",
            "ife_driver": "Acoustic", "repetition_rate": "kHz",
        })
        assert "target_factory_high" not in t
        assert "target_factory_low" not in t

    def test_disruption_mitigation_tokamaks(self):
        for cc in ("Compact tokamak", "Spherical tokamak", "Tokamak",
                   "Negative triangularity tokamak", "Z-pinch (sheared-flow)"):
            t = _triggered({"fuel": "D-T", "confinement_family": "MFE",
                             "confinement_concept": cc})
            assert "disruption_mitigation" in t

    def test_current_drive_steady_tokamak(self):
        t = _triggered({"fuel": "D-T", "confinement_family": "MFE",
                         "confinement_concept": "Compact tokamak",
                         "operation_mode": "Quasi-steady"})
        assert "current_drive" in t

    def test_levitation_for_dipole(self):
        t = _triggered({"fuel": "D-T", "confinement_family": "MFE",
                         "confinement_concept": "Levitated dipole"})
        assert "levitation_stabilization" in t


# ─── Whole-corpus invariants ──────────────────────────────────────────────


class TestScoreInvariants:
    def test_all_in_band(self, run_cli, tmp_scores_dir: Path):
        scores = _read_actual(run_cli, tmp_scores_dir)
        for cid, v in scores.items():
            assert v is not None and 1.0 <= v <= 5.0

    def test_distribution_non_degenerate(self, run_cli, tmp_scores_dir: Path):
        scores = _read_actual(run_cli, tmp_scores_dir)
        unique = {round(v, 1) for v in scores.values() if v is not None}
        assert len(unique) >= 4


def test_corpus_drift_under_threshold(run_cli, tmp_scores_dir: Path):
    predicted = yaml.safe_load(PREDICTED.read_text()).get("plant_complexity", {})
    actual = _read_actual(run_cli, tmp_scores_dir)
    diffs = []
    for cid, exp in predicted.items():
        if exp is None:
            continue
        v = actual.get(cid)
        if v is None:
            continue
        diffs.append(abs(v - float(exp)))
    if diffs:
        mean = sum(diffs) / len(diffs)
        assert mean < 0.5, f"plant_complexity mean |diff| = {mean:.3f}"
