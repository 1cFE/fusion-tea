"""Upper Capacity Factor axis acceptance tests."""
from __future__ import annotations

import csv
from pathlib import Path

import pytest
import yaml

from exploration.scoring_v2.embeddings.rulebook import (
    _compute_triggered_cf_penalties,
    _load_upper_cf_weights,
)

REPO_ROOT = Path(__file__).resolve().parents[2]
SCORING_V2 = REPO_ROOT / "exploration" / "scoring_v2"
PREDICTED = REPO_ROOT / "tests" / "scoring_v2" / "predicted_scores.yaml"
WEIGHTS = yaml.safe_load((SCORING_V2 / "weights" / "default.yaml").read_text())
SEV = _load_upper_cf_weights(WEIGHTS)

PER_CONCEPT_TOLERANCE = 0.55

# Concepts whose feature data drifts from the spec's predicted-scores
# expectation. The Upper CF rules + features produce different scores
# than the spec narrative table; reconciliation is P7 calibration work.
KNOWN_DRIFTS = {
    "27-polywell":                  "EMC2 D-T + TBD; spec implies 3.0, rules give 4.0",
    "33-state-backed-tokamak-best": "BEST D-T + TBD; spec implies 3.0, rules give 4.0",
}


# ─── Weights surface ─────────────────────────────────────────────────────


class TestWeightsExposedInDefaultYaml:
    def test_axis_exists(self):
        assert "upper_cf" in WEIGHTS

    def test_axis_weight_is_one(self):
        assert WEIGHTS["upper_cf"]["axis_weight"] == 1.0

    def test_severity_weights(self):
        assert SEV["pulsed_operation"] == 0.5
        assert SEV["neutronic_fuel"] == 1.0
        assert SEV["non_renewable_blanket"] == 0.5

    def test_missing_weight_raises(self):
        partial = {"upper_cf": {"operational_penalty_weights": {"pulsed_operation": 0.5}}}
        with pytest.raises(ValueError, match="missing required keys"):
            _load_upper_cf_weights(partial)


# ─── Trigger rules ───────────────────────────────────────────────────────


def _triggered(fuel, blanket, op):
    return _compute_triggered_cf_penalties(fuel, blanket, op, SEV)


class TestTriggerRules:
    def test_pulsed_only(self):
        assert "pulsed_operation" in _triggered("p-B11", "N/A (no tritium)", "Pulsed")
        for op in ("Steady-state", "Quasi-steady"):
            assert "pulsed_operation" not in _triggered("p-B11", "N/A (no tritium)", op)

    def test_neutronic_fuel(self):
        assert "neutronic_fuel" in _triggered("D-T", "Liquid metal", "Steady-state")
        assert "neutronic_fuel" in _triggered("D-D", "N/A (no tritium)", "Pulsed")
        for fuel in ("p-B11", "D-He3"):
            assert "neutronic_fuel" not in _triggered(fuel, "N/A (no tritium)", "Pulsed")

    def test_non_renewable_blanket_requires_neutronic(self):
        # Liquid metal renewable → no penalty
        assert "non_renewable_blanket" not in _triggered("D-T", "Liquid metal", "Steady-state")
        # Static blankets + neutronic → penalty
        for blk in ("Solid breeder", "Molten salt", "Other/hybrid"):
            assert "non_renewable_blanket" in _triggered("D-T", blk, "Steady-state")
        # Aneutronic fuel → no penalty regardless of blanket
        assert "non_renewable_blanket" not in _triggered("p-B11", "Solid breeder", "Steady-state")
        # TBD blanket → Liquid metal → renewable → no penalty
        assert "non_renewable_blanket" not in _triggered("D-T", "TBD", "Steady-state")


# ─── Score ladder ────────────────────────────────────────────────────────


def _score(fuel, blanket, op):
    weight = sum(_triggered(fuel, blanket, op).values())
    return max(1.0, 5.0 - weight)


class TestScoreLadder:
    def test_aneutronic_steady_state_top(self):
        assert _score("p-B11", "N/A (no tritium)", "Steady-state") == 5.0

    def test_aneutronic_pulsed(self):
        assert _score("p-B11", "N/A (no tritium)", "Pulsed") == 4.5

    def test_dt_liquid_metal_steady(self):
        # neutronic only (Liquid metal renewable): -1.0 → 4.0
        assert _score("D-T", "Liquid metal", "Steady-state") == 4.0

    def test_dt_solid_breeder_steady(self):
        # neutronic + non_renewable: -1.5 → 3.5
        assert _score("D-T", "Solid breeder", "Steady-state") == 3.5

    def test_dt_solid_breeder_pulsed(self):
        # all three penalties: -2.0 → 3.0
        assert _score("D-T", "Solid breeder", "Pulsed") == 3.0


# ─── Whole-corpus ────────────────────────────────────────────────────────


def _read_actual(run_cli, tmp_scores_dir: Path) -> dict[str, float | None]:
    run_cli("score.py")
    out = {}
    with open(tmp_scores_dir / "table.csv") as f:
        for r in csv.DictReader(f):
            v = r["upper_cf"]
            out[r["concept_id"]] = float(v) if v else None
    return out


class TestScoreInvariants:
    def test_all_in_band(self, run_cli, tmp_scores_dir: Path):
        scores = _read_actual(run_cli, tmp_scores_dir)
        for cid, v in scores.items():
            assert v is not None and 1.0 <= v <= 5.0, f"{cid}: {v}"

    def test_distribution_non_degenerate(self, run_cli, tmp_scores_dir: Path):
        scores = _read_actual(run_cli, tmp_scores_dir)
        unique = {round(v, 2) for v in scores.values() if v is not None}
        assert len(unique) >= 3, f"degenerate: {sorted(unique)}"


def test_corpus_drift_under_threshold(run_cli, tmp_scores_dir: Path):
    predicted = yaml.safe_load(PREDICTED.read_text()).get("upper_cf", {})
    actual = _read_actual(run_cli, tmp_scores_dir)
    diffs = []
    for cid, exp in predicted.items():
        v = actual.get(cid)
        if v is None:
            continue
        diffs.append(abs(v - float(exp)))
    mean = sum(diffs) / len(diffs)
    assert mean < 0.4, f"upper_cf mean |diff| = {mean:.3f}"
