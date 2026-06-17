"""Technical Feasibility axis acceptance tests."""
from __future__ import annotations

import csv
from pathlib import Path

import pytest
import yaml

from exploration.scoring_v2.embeddings.rulebook import (
    _load_tf_tables,
    _tf_score_from_log_gap,
    _TF_FLOOR_SCORE,
)

REPO_ROOT = Path(__file__).resolve().parents[2]
SCORING_V2 = REPO_ROOT / "exploration" / "scoring_v2"
PREDICTED = REPO_ROOT / "tests" / "scoring_v2" / "predicted_scores.yaml"
WEIGHTS = yaml.safe_load((SCORING_V2 / "weights" / "default.yaml").read_text())
REQUIRED, ACHIEVED = _load_tf_tables(WEIGHTS)

PER_CONCEPT_TOLERANCE = 0.55

KNOWN_DRIFTS = {
    # ENN p-B11 spherical tokamak: the achieved triple product credits the
    # confinement family with its (fuel-blind) D-T-equivalent demo, while
    # required_triple_product[p-B11][MFE] is the alpha-channeled Ochs 2022
    # target. Rules land at 2.0; the TF spec floored all p-B11 at 1.0.
    "39-spherical-tokamak-cs-free-p-b11": "ENN p-B11 spherical; spec floor 1.0 vs rules 2.0",
}


def _read_actual(run_cli, tmp_scores_dir: Path) -> dict[str, float | None]:
    run_cli("score.py")
    out = {}
    with open(tmp_scores_dir / "table.csv") as f:
        for r in csv.DictReader(f):
            v = r["technical_feasibility"]
            out[r["concept_id"]] = float(v) if v else None
    return out


# ─── Weights surface ─────────────────────────────────────────────────────


class TestWeightsSurface:
    def test_required_table_complete(self):
        for fuel in ("D-T", "D-D", "D-He3", "p-B11", "Unknown"):
            assert fuel in REQUIRED

    def test_required_d_t_at_3e21(self):
        # Scalar fuels normalize to a {'*': value} dict.
        assert REQUIRED["D-T"] == {"*": 3.0e21}

    def test_required_p_b11_family_keyed(self):
        # p-B11 carries an un-channeled '*' default plus a steady-state
        # magnetic override (alpha channeling realistic). See Ochs 2022.
        assert REQUIRED["p-B11"]["*"] == 1.4e25
        assert REQUIRED["p-B11"]["MFE"] == 5.0e24

    def test_achieved_has_major_families(self):
        for key in ("MFE|Compact tokamak", "MFE|Stellarator",
                    "IFE|Laser ICF (indirect drive)",
                    "MIF|FRC compression (MIF)", "MIF|MagLIF"):
            assert key in ACHIEVED, f"missing achieved entry: {key}"

    def test_no_data_families_omitted(self):
        # NOTE: "IFE|Laser ICF (liquid jet)" used to live here but as of
        # 2026-06-17 it shares the laser ICF family-best achieved value (5.0e21)
        # and is clamped to score 1.0 via a -4.00 laser_approach_modifier
        # instead. See test_laser_icf_single_family_value below.
        for key in ("IFE|Acoustic ICF (sonofusion)",
                    "Non-Standard|Polywell",
                    "Non-Standard|Electrostatic hybrid",
                    "Non-Standard|Beam-target fusion",
                    "Non-Standard|Muon-catalyzed fusion"):
            assert key not in ACHIEVED


# ─── Family-best consistency ─────────────────────────────────────────────
#
# Every confinement family must expose exactly one distinct non-null achieved
# triple product across all sub-architectural variants. Sub-architectural risk
# differences (e.g., direct drive vs indirect drive vs fast ignition) are
# expressed through the laser_approach_modifier table, not by varying the
# "achieved" input per concept.
#
# Regression guard against the 2026-06-17 issue, where the IFE|Laser ICF
# family had five distinct achieved values (5e21, 5e21, 1e20, 1e18, 1e21)
# split by laser approach. That split moved load-bearing methodology decisions
# from the rule layer into the data layer, defeating the framework's claim
# of rule-based scoring. The MFE families never had this problem; this test
# enforces the same discipline for IFE Laser ICF and any future families.


class TestFamilyBestConsistency:
    """Each confinement family exposes one achieved value across all variants."""

    # Map every achieved-table key prefix to the canonical family it belongs to.
    # Lookup keys are "Family|Concept", where Concept may carry a sub-architectural
    # parenthetical (e.g. "Laser ICF (direct drive)"). We collapse on the
    # pre-parenthetical concept root so all variants of one family compare.
    @staticmethod
    def _family_root(key: str) -> str:
        family, concept = key.split("|", 1) if "|" in key else (key, "")
        # Strip any "(...)" parenthetical suffix from the concept name so that
        # "Laser ICF (direct drive)" and "Laser ICF (fast ignition)" collapse to
        # the same "Laser ICF" root.
        idx = concept.find(" (")
        if idx != -1:
            concept = concept[:idx]
        return f"{family}|{concept}"

    def test_each_family_has_one_distinct_value(self):
        grouped: dict[str, set[float]] = {}
        for key, value in ACHIEVED.items():
            root = self._family_root(key)
            grouped.setdefault(root, set()).add(float(value))

        offenders = {root: sorted(vals) for root, vals in grouped.items() if len(vals) > 1}
        assert not offenders, (
            "Each confinement family must expose exactly one achieved triple "
            "product across all sub-architectural variants. Variants split with "
            "different achieved values move load-bearing methodology decisions "
            "from the rule layer into the data layer. Sub-architectural risk "
            "belongs in laser_approach_modifier (or an equivalent modifier table "
            "for future families), not in the achieved-value lookup. Offenders:\n"
            + "\n".join(f"  {root}: {vals}" for root, vals in offenders.items())
        )

    def test_laser_icf_single_family_value(self):
        # Explicit anchor: every IFE|Laser ICF (...) entry shares the family
        # best (NIF ignition at 5.0e21). Differentiation between direct vs
        # indirect vs fast ignition vs ultrashort vs liquid jet vs hybrid drive
        # lives in laser_approach_modifier.
        laser_keys = [k for k in ACHIEVED if k.startswith("IFE|Laser ICF")]
        assert len(laser_keys) >= 5, (
            f"expected the laser ICF family to enumerate every variant for clarity; "
            f"saw only {laser_keys}"
        )
        laser_values = {float(ACHIEVED[k]) for k in laser_keys}
        assert laser_values == {5.0e21}, (
            f"all IFE|Laser ICF entries must share the family-best value "
            f"5.0e21 (NIF ignition); got {sorted(laser_values)}"
        )

    def test_laser_approach_modifier_covers_every_lookup_key(self):
        # Every laser-ICF variant present in the achieved table must have a
        # corresponding modifier entry so the rule's lookup never silently
        # defaults to 0.0 for a known architecture. The modifier table is
        # where architectural-risk differentiation lives now, so an unmapped
        # variant would inherit indirect-drive's "no penalty" score.
        modifiers = WEIGHTS["technical_feasibility"]["laser_approach_modifier"]
        # The achieved table uses "Laser ICF (direct drive)" style suffixes;
        # the modifier table uses bare "Direct drive" style keys. Map between
        # them by stripping the "Laser ICF (" prefix and trailing ")".
        for key in [k for k in ACHIEVED if k.startswith("IFE|Laser ICF")]:
            suffix = key.split("(", 1)[1].rstrip(")")
            # Modifier keys are title-cased ("Direct drive", "Indirect drive").
            normalized = suffix[:1].upper() + suffix[1:]
            assert normalized in modifiers, (
                f"laser approach {normalized!r} missing from laser_approach_modifier; "
                f"a known variant in the achieved table would default to 0.0"
            )


# ─── Bucket schedule ─────────────────────────────────────────────────────


class TestBucketSchedule:
    def test_at_target_score_5(self):
        # log_gap = 0 → score 5
        assert _tf_score_from_log_gap(0.0) == 5.0

    def test_within_10x_score_4(self):
        assert _tf_score_from_log_gap(0.5) == 4.0
        assert _tf_score_from_log_gap(1.0) == 4.0

    def test_within_1000x_score_3(self):
        assert _tf_score_from_log_gap(1.5) == 3.0
        assert _tf_score_from_log_gap(3.0) == 3.0

    def test_within_100000x_score_2(self):
        assert _tf_score_from_log_gap(4.0) == 2.0
        assert _tf_score_from_log_gap(5.0) == 2.0

    def test_floor(self):
        assert _tf_score_from_log_gap(6.0) == 1.0
        assert _tf_score_from_log_gap(10.0) == 1.0


# ─── Score invariants ────────────────────────────────────────────────────


class TestScoreInvariants:
    def test_all_in_band(self, run_cli, tmp_scores_dir: Path):
        scores = _read_actual(run_cli, tmp_scores_dir)
        for cid, v in scores.items():
            assert v is not None and 1.0 <= v <= 5.0

    def test_distribution_non_degenerate(self, run_cli, tmp_scores_dir: Path):
        scores = _read_actual(run_cli, tmp_scores_dir)
        unique = {round(v, 1) for v in scores.values() if v is not None}
        assert len(unique) >= 4


# ─── Score anchors ───────────────────────────────────────────────────────


_ANCHORS = [
    # NIF indirect drive at ignition: log10(3e21/5e21) = -0.22 → 5 + 0.0 = 5.0
    ("26-laser-icf-indirect-drive", 5.0),
    ("30-laser-icf-nif-commercialization", 5.0),
    # OMEGA direct drive: log10(3e21/5e21) = -0.22 → 5 + (-0.25) = 4.75
    ("31-laser-icf-oec-architecture", 4.75),
    ("32-laser-icf-french-national", 4.75),
    # Acoustic ICF (no data) → floor 1.0
    ("02-acoustic-icf-sonofusion", 1.0),
    # Polywell electrostatic (no data) → floor 1.0
    ("27-polywell", 1.0),
    # SHINE accelerator (no data) → floor 1.0
    ("38-particle-accelerator-driven-fusion", 1.0),
]


@pytest.mark.parametrize("cid,expected", _ANCHORS)
def test_anchor(run_cli, tmp_scores_dir: Path, cid: str, expected: float):
    scores = _read_actual(run_cli, tmp_scores_dir)
    actual = scores[cid]
    assert actual is not None
    assert abs(actual - expected) <= PER_CONCEPT_TOLERANCE, (
        f"{cid}: actual={actual} vs expected={expected}"
    )


def test_corpus_drift_under_threshold(run_cli, tmp_scores_dir: Path):
    predicted = yaml.safe_load(PREDICTED.read_text()).get("technical_feasibility", {})
    actual = _read_actual(run_cli, tmp_scores_dir)
    diffs = []
    for cid, exp in predicted.items():
        v = actual.get(cid)
        if v is None or exp is None:
            continue
        diffs.append(abs(v - float(exp)))
    mean = sum(diffs) / len(diffs)
    assert mean < 0.3, f"technical_feasibility mean |diff| = {mean:.3f}"
