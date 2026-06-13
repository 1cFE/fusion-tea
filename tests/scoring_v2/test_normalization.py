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

import yaml

REPO_ROOT = Path(__file__).resolve().parents[2]
SCORING_V2 = REPO_ROOT / "exploration" / "scoring_v2"
LIVE_TABLE = SCORING_V2 / "scores" / "table.csv"
WEIGHTS = yaml.safe_load((SCORING_V2 / "weights" / "default.yaml").read_text())

NORMALIZED_AXES = [
    axis for axis in
    ("modularity", "supply_chain", "plant_complexity", "customization",
     "upper_cf", "technical_feasibility", "data_availability")
    if (WEIGHTS.get(axis) or {}).get("normalization")
]


def _read_axis(axis: str) -> list[float]:
    with open(LIVE_TABLE) as f:
        return [
            float(r[axis])
            for r in csv.DictReader(f)
            if r.get(axis)
        ]


def test_normalized_axes_declared():
    """The normalization framework is currently applied to modularity and
    upper_cf — guards against accidental removal of the normalization block."""
    assert "modularity" in NORMALIZED_AXES
    assert "upper_cf" in NORMALIZED_AXES


def test_normalized_axis_means_within_tolerance():
    for axis in NORMALIZED_AXES:
        block = WEIGHTS[axis]["normalization"]
        target = float(block["target_mean"])
        tol = float(block.get("tolerance", 0.1))
        vals = _read_axis(axis)
        m = statistics.mean(vals)
        assert abs(m - target) <= tol, (
            f"{axis} normalized mean {m:.3f} outside ±{tol} of target {target}"
        )


def test_normalized_axis_variances_within_tolerance():
    for axis in NORMALIZED_AXES:
        block = WEIGHTS[axis]["normalization"]
        target = float(block["target_variance"])
        tol = float(block.get("tolerance", 0.1))
        vals = _read_axis(axis)
        v = statistics.variance(vals)
        assert abs(v - target) <= tol, (
            f"{axis} normalized variance {v:.3f} outside ±{tol} of target {target}"
        )


def test_normalized_axes_stay_in_score_range():
    """Floor at 1.0 is preserved; no axis goes negative or above 5.0."""
    for axis in NORMALIZED_AXES:
        vals = _read_axis(axis)
        assert min(vals) >= 1.0 - 1e-6, f"{axis} below 1.0 floor"
        assert max(vals) <= 5.0 + 1e-6, f"{axis} above 5.0 ceiling"


def test_normalization_preserves_per_concept_ordering_within_tier():
    """Concepts with identical raw scores stay identical after normalization
    (the transform is monotone)."""
    import json
    concepts = json.loads(
        (REPO_ROOT / "tools" / "score_explorer" / "data" / "concepts.json").read_text()
    )
    for axis in NORMALIZED_AXES:
        # group concepts by their raw value as recorded in the diagnostic block
        diag_key = f"{axis}_diagnostics"
        raw_score_field = "modularity_score" if axis == "modularity" else "upper_cf_score"
        groups: dict[float, list[float]] = {}
        for c in concepts:
            diag = c.get("diagnostics", {}).get(diag_key) or {}
            raw = diag.get(raw_score_field)
            normalized = c["scores"].get(axis)
            if raw is None or normalized is None:
                continue
            groups.setdefault(round(float(raw), 4), []).append(float(normalized))
        for raw, normalized_list in groups.items():
            assert len(set(round(n, 4) for n in normalized_list)) == 1, (
                f"{axis} raw={raw} produced different normalized values: "
                f"{normalized_list}"
            )
