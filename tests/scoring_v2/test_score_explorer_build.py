"""Smoke tests for tools/score_explorer/build.py.

The UI is tested manually (vanilla React, no test harness configured);
this only verifies the data-generation Python script produces a well-
formed JSON shape that the UI can consume.
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
BUILD_SCRIPT = REPO_ROOT / "tools" / "score_explorer" / "build.py"
DATA_DIR = REPO_ROOT / "tools" / "score_explorer" / "data"

AXES = (
    "modularity", "supply_chain", "plant_complexity", "customization",
    "upper_cf", "technical_feasibility", "data_availability",
)


def _run_build() -> None:
    """Run build.py with the live scoring_v2 data — it reads the committed
    scores/table.csv and features/, no isolation needed."""
    result = subprocess.run(
        [sys.executable, str(BUILD_SCRIPT)],
        cwd=REPO_ROOT, capture_output=True, text=True,
    )
    if result.returncode != 0:
        raise AssertionError(
            f"build.py failed (rc={result.returncode})\n"
            f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}"
        )


# The scoring framework scores 40 concepts; the UI hides
# build.EXCLUDED_FROM_UI (currently just 30-laser-icf-nif-commercialization,
# redundant with 26-laser-icf-indirect-drive — both Inertia Enterprises).
EXPECTED_UI_CONCEPTS = 40 - 1


def test_build_emits_concepts_json():
    _run_build()
    path = DATA_DIR / "concepts.json"
    assert path.exists()
    data = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(data, list)
    assert len(data) == EXPECTED_UI_CONCEPTS


def test_excluded_concept_absent_from_ui():
    """build.EXCLUDED_FROM_UI concepts must not appear in concepts.json
    even though score.py still scores them."""
    _run_build()
    data = json.loads((DATA_DIR / "concepts.json").read_text(encoding="utf-8"))
    ids = {c["concept_id"] for c in data}
    assert "30-laser-icf-nif-commercialization" not in ids


def test_concepts_have_all_required_fields():
    _run_build()
    data = json.loads((DATA_DIR / "concepts.json").read_text(encoding="utf-8"))
    for c in data:
        for required in ("concept_id", "name", "scores", "composite",
                         "composite_axes_included", "evidence",
                         "features", "diagnostics"):
            assert required in c, f"{c.get('concept_id')}: missing {required}"
        # All seven axes appear in scores (some may be null)
        for axis in AXES:
            assert axis in c["scores"], (
                f"{c['concept_id']}: scores.{axis} missing"
            )
        # composite_axes_included is a JSON list (possibly empty)
        assert isinstance(c["composite_axes_included"], list)


def test_build_emits_weights_json():
    _run_build()
    weights = json.loads((DATA_DIR / "weights.json").read_text(encoding="utf-8"))
    assert "axes" in weights and "composite" in weights
    axes_by_name = {a["name"]: a for a in weights["axes"]}
    assert set(axes_by_name) == set(AXES)
    for axis_data in weights["axes"]:
        assert "axis_weight" in axis_data
        assert "embedding_weights" in axis_data
        assert "sub_tables" in axis_data


def test_modularity_sub_tables_in_weights_json():
    """The Modularity axis's lookup tables must reach the UI via weights.json
    so the Advanced expansion can display them."""
    _run_build()
    weights = json.loads((DATA_DIR / "weights.json").read_text(encoding="utf-8"))
    mod = next(a for a in weights["axes"] if a["name"] == "modularity")
    for table in ("mvs_lookup", "vessel_lookup", "magnet_driver_lookup",
                  "blanket_lookup", "unit_count_brackets"):
        assert table in mod["sub_tables"], f"modularity.{table} missing"


def test_all_concepts_score_all_seven_axes():
    """After the gap-report-stub work every concept has a gap_report.md,
    so every UI concept carries a non-null score on all 7 axes and a
    7-axis composite."""
    _run_build()
    data = json.loads((DATA_DIR / "concepts.json").read_text(encoding="utf-8"))
    assert len(data) == EXPECTED_UI_CONCEPTS
    for c in data:
        for axis in AXES:
            assert c["scores"][axis] is not None, (
                f"{c['concept_id']}: {axis} is null"
            )
        assert set(c["composite_axes_included"]) == set(AXES), (
            f"{c['concept_id']}: composite_axes_included = "
            f"{c['composite_axes_included']}"
        )
        assert c["composite"] is not None, f"{c['concept_id']}: composite null"


def test_composite_is_mean_of_included_axes():
    """The composite in concepts.json must be the weighted mean of the
    listed axes (with axis_weight from default.yaml)."""
    _run_build()
    weights = json.loads((DATA_DIR / "weights.json").read_text(encoding="utf-8"))
    axis_weights = {a["name"]: a["axis_weight"] for a in weights["axes"]}
    data = json.loads((DATA_DIR / "concepts.json").read_text(encoding="utf-8"))
    for c in data:
        included = c["composite_axes_included"]
        if not included:
            assert c["composite"] is None
            continue
        norm = sum(axis_weights[a] for a in included)
        expected = sum(c["scores"][a] * axis_weights[a] for a in included) / norm
        assert abs(c["composite"] - expected) < 0.01, (
            f"{c['concept_id']}: composite={c['composite']} vs expected={expected:.4f}"
        )
