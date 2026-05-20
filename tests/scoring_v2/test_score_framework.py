"""Framework tests for the 7-axis score driver: column shape, determinism,
schema-fail-loud, no-LLM static invariant, null-handling.
"""
from __future__ import annotations

import csv
import json
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parents[2]
SCORING_V2 = REPO_ROOT / "exploration" / "scoring_v2"

AXES = (
    "modularity",
    "supply_chain",
    "plant_complexity",
    "customization",
    "upper_cf",
    "technical_feasibility",
    "data_availability",
)
EVIDENCE_COLS = tuple(f"{a}_evidence" for a in AXES)


def _read_csv(p: Path) -> list[dict[str, str]]:
    with open(p) as f:
        return list(csv.DictReader(f))


def test_score_csv_has_axis_keyed_shape(run_cli, tmp_scores_dir: Path):
    """CSV layout: 7 axis cols + composite + 7 evidence cols + composite
    evidence + composite_axes_included."""
    run_cli("score.py")
    rows = _read_csv(tmp_scores_dir / "table.csv")
    assert len(rows) == 40
    expected_cols = {
        "concept_id", "name",
        *AXES,
        "composite",
        *EVIDENCE_COLS,
        "composite_evidence",
        "composite_axes_included",
    }
    assert set(rows[0].keys()) == expected_cols, (
        f"unexpected CSV columns; got {sorted(rows[0].keys())}"
    )


def test_old_dimension_columns_gone(run_cli, tmp_scores_dir: Path):
    """The 3 retired dimensions and their evidence cols must NOT be in
    the CSV any more."""
    run_cli("score.py")
    rows = _read_csv(tmp_scores_dir / "table.csv")
    cols = set(rows[0].keys())
    for retired in (
        "economic_potential", "technical_feasibility_old",
        "manufacturability_scale_out", "ep_evidence", "tf_evidence",
        "mso_evidence",
    ):
        # Note: "technical_feasibility" is now a v3 AXIS, not the retired
        # dimension — only the dimension-style retired ones should be gone.
        if retired == "technical_feasibility_old":
            continue
        assert retired not in cols, (
            f"retired dimension column {retired!r} still present in CSV"
        )


# P4 wires 6 of 7 axes (data_availability lands in P5).
_WIRED_AXES_NOW = {
    "modularity", "supply_chain", "customization", "upper_cf",
    "plant_complexity", "technical_feasibility",
}


def test_wired_axes_score_others_null(run_cli, tmp_scores_dir: Path):
    """Wired axes (modularity, supply_chain, customization, upper_cf) score
    a number; the remaining placeholder axes (plant_complexity,
    technical_feasibility, data_availability) score null until P4/P5."""
    run_cli("score.py")
    rows = _read_csv(tmp_scores_dir / "table.csv")
    for r in rows:
        for axis in AXES:
            if axis in _WIRED_AXES_NOW:
                assert r[axis], f"{r['concept_id']}: {axis} empty"
            else:
                assert r[axis] == "", (
                    f"{r['concept_id']}: {axis} = {r[axis]!r} (expected null)"
                )
        included = json.loads(r["composite_axes_included"])
        assert set(included) == _WIRED_AXES_NOW, (
            f"{r['concept_id']}: composite_axes_included = {included}"
        )


def test_composite_is_mean_of_wired_axes(run_cli, tmp_scores_dir: Path):
    """With four axes wired at axis_weight=1.0 each, the composite is the
    arithmetic mean of the four axis scores."""
    run_cli("score.py")
    rows = _read_csv(tmp_scores_dir / "table.csv")
    for r in rows:
        scored = [float(r[a]) for a in _WIRED_AXES_NOW]
        expected = sum(scored) / len(scored)
        actual = float(r["composite"])
        assert abs(actual - expected) < 0.01, (
            f"{r['concept_id']}: composite={actual} vs mean={expected:.4f}"
        )


def test_score_deterministic_byte_identical(run_cli, tmp_scores_dir: Path):
    run_cli("score.py")
    a = (tmp_scores_dir / "table.csv").read_bytes()
    run_cli("score.py")
    b = (tmp_scores_dir / "table.csv").read_bytes()
    assert a == b


def test_score_aborts_on_malformed_feature_file(run_cli, tmp_features_dir: Path):
    target = tmp_features_dir / "01-hts-compact-tokamak.yaml"
    doc = yaml.safe_load(target.read_text())
    doc["confinement_family"]["value"] = "Garbage"
    target.write_text(yaml.safe_dump(doc, sort_keys=False))
    result = run_cli("score.py", check=False)
    assert result.returncode != 0
    err = result.stderr + result.stdout
    assert "01-hts-compact-tokamak" in err
    assert "confinement_family" in err


def test_no_llm_imports_in_score_path():
    targets = [
        SCORING_V2 / "score.py",
        SCORING_V2 / "lib" / "schema.py",
        SCORING_V2 / "lib" / "feature_io.py",
        SCORING_V2 / "embeddings" / "rulebook.py",
    ]
    forbidden = ("anthropic", "openai", "claude_api", "claude-api")
    for path in targets:
        src = path.read_text()
        for f in forbidden:
            assert f not in src, f"{f!r} found in {path}"


def test_score_alphabetical_concept_order(run_cli, tmp_scores_dir: Path):
    run_cli("score.py")
    rows = _read_csv(tmp_scores_dir / "table.csv")
    ids = [r["concept_id"] for r in rows]
    assert ids == sorted(ids)


def test_unknown_axis_in_weights_raises(run_cli, tmp_path):
    """Adding an unknown top-level axis to weights/default.yaml must
    cause score.py to fail loud (R10 schema fail-loud)."""
    weights_src = SCORING_V2 / "weights" / "default.yaml"
    bogus = tmp_path / "default.yaml"
    doc = yaml.safe_load(weights_src.read_text())
    doc["bogus_axis"] = {"axis_weight": 1.0, "embedding_weights": {}}
    bogus.write_text(yaml.safe_dump(doc))
    result = run_cli("score.py", check=False, weights=bogus)
    assert result.returncode != 0
    err = result.stderr + result.stdout
    assert "bogus_axis" in err
