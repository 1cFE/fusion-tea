"""Acceptance tests for the corpus-wide axis normalization step
(`score.py:_normalize_axes`).

Axes that declare a `normalization:` block in weights/default.yaml are
post-processed so their corpus mean and variance match the declared
targets within `tolerance`. Currently applied to `modularity` and
`upper_cf` to even their contribution to the composite alongside the
other 5 axes (SC, PC, Cust, TF, DA).
"""

from __future__ import annotations

import csv
import statistics
from pathlib import Path

import pytest
import yaml

REPO_ROOT = Path(__file__).resolve().parents[2]
SCORING_V2 = REPO_ROOT / "exploration" / "scoring_v2"
WEIGHTS = yaml.safe_load((SCORING_V2 / "weights" / "default.yaml").read_text())

NORMALIZED_AXES = [
    axis
    for axis in (
        "modularity",
        "supply_chain",
        "plant_complexity",
        "customization",
        "upper_cf",
        "technical_feasibility",
        "data_availability",
    )
    if (WEIGHTS.get(axis) or {}).get("normalization")
]


@pytest.fixture
def scored_table(run_cli, tmp_scores_dir):
    run_cli("score.py")
    return tmp_scores_dir / "table.csv"


def _read_axis(axis: str, table: Path) -> list[float]:
    with table.open() as f:
        return [float(r[axis]) for r in csv.DictReader(f) if r.get(axis)]


def test_normalized_axes_declared():
    """The normalization framework is currently applied to modularity and
    upper_cf — guards against accidental removal of the normalization block."""
    assert "modularity" in NORMALIZED_AXES
    assert "upper_cf" in NORMALIZED_AXES


def test_normalized_axis_means_within_tolerance(scored_table):
    for axis in NORMALIZED_AXES:
        block = WEIGHTS[axis]["normalization"]
        target = float(block["target_mean"])
        tol = float(block.get("tolerance", 0.1))
        vals = _read_axis(axis, scored_table)
        m = statistics.mean(vals)
        assert abs(m - target) <= tol, (
            f"{axis} normalized mean {m:.3f} outside ±{tol} of target {target}"
        )


def test_normalized_axis_variances_within_tolerance(scored_table):
    for axis in NORMALIZED_AXES:
        block = WEIGHTS[axis]["normalization"]
        target = float(block["target_variance"])
        tol = float(block.get("tolerance", 0.1))
        vals = _read_axis(axis, scored_table)
        v = statistics.variance(vals)
        assert abs(v - target) <= tol, (
            f"{axis} normalized variance {v:.3f} outside ±{tol} of target {target}"
        )


def test_normalized_axes_stay_in_score_range(scored_table):
    """Floor at 1.0 is preserved; no axis goes negative or above 5.0."""
    for axis in NORMALIZED_AXES:
        vals = _read_axis(axis, scored_table)
        assert min(vals) >= 1.0 - 1e-6, f"{axis} below 1.0 floor"
        assert max(vals) <= 5.0 + 1e-6, f"{axis} above 5.0 ceiling"


def test_normalization_preserves_per_concept_ordering_within_tier(
    run_cli, tmp_features_dir, tmp_scores_dir
):
    """Concepts with identical raw scores stay identical after normalization
    (the transform is monotone)."""
    from exploration.scoring_v2 import score
    from exploration.scoring_v2.lib import schema

    run_cli("score.py")
    with (tmp_scores_dir / "table.csv").open() as stream:
        normalized_rows = {row["concept_id"]: row for row in csv.DictReader(stream)}
    # Diagnostic blocks and published explorer JSON are retained snapshots.
    # Evaluate raw values from the same inputs as this fresh scoring execution.
    raw_rows = {}
    for path in sorted(tmp_features_dir.glob("*.yaml")):
        doc = yaml.safe_load(path.read_text())
        values, confidence = score._evaluate_concept(doc, WEIGHTS, schema.load_schema())
        raw_rows[doc["_meta"]["concept_id"]] = {
            axis: score._score_axis(WEIGHTS[axis], values, confidence)[0]
            for axis in NORMALIZED_AXES
        }
    assert len(raw_rows) == 40
    assert set(normalized_rows) == set(raw_rows)
    for axis in NORMALIZED_AXES:
        groups: dict[float, list[float]] = {}
        for cid, raw_values in raw_rows.items():
            raw = raw_values[axis]
            normalized = normalized_rows[cid][axis]
            if raw is None:
                assert normalized == ""
                continue
            groups.setdefault(raw, []).append(float(normalized))
        assert any(len(values) > 1 for values in groups.values())
        for raw, normalized_list in groups.items():
            assert len(set(normalized_list)) == 1, (
                f"{axis} raw={raw} produced different normalized values: {normalized_list}"
            )
        ordered = [values[0] for _, values in sorted(groups.items())]
        assert ordered == sorted(ordered), f"{axis}: normalization reversed raw order"
