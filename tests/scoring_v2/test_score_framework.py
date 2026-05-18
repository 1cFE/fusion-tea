"""Phase 2 framework tests: determinism, schema-fail-loud, no-LLM, FR-7/FR-8 shape."""
from __future__ import annotations

import csv
import shutil
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parents[2]
SCORING_V2 = REPO_ROOT / "exploration" / "scoring_v2"


def _read_csv(p: Path) -> list[dict[str, str]]:
    with open(p) as f:
        return list(csv.DictReader(f))


def test_score_runs_against_all_38(run_cli, tmp_scores_dir: Path):
    run_cli("score.py")
    rows = _read_csv(tmp_scores_dir / "table.csv")
    assert len(rows) == 38
    expected_cols = {
        "concept_id", "name",
        "economic_potential", "technical_feasibility", "manufacturability_scale_out",
        "ep_evidence", "tf_evidence", "mso_evidence",
    }
    assert expected_cols.issubset(set(rows[0].keys()))
    # Economic potential + technical feasibility are unwired (empty dims) → zero everywhere.
    for r in rows:
        assert float(r["economic_potential"]) == 0.0
        assert float(r["technical_feasibility"]) == 0.0


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


def test_evidence_columns_discriminate_under_default_weights(run_cli, tmp_scores_dir: Path):
    # Slice 2 introduces non-`high` confidence into M&SO:
    #   - concepts with a cost model contribute cm_aggregate at confidence=medium
    #   - concepts without a cost model leave w_* absent → cm_aggregate confidence=low
    # Either way, mso_evidence must no longer be uniformly "high" — this is the
    # mixed-confidence-aggregation discrimination the slice was meant to surface.
    run_cli("score.py")
    rows = _read_csv(tmp_scores_dir / "table.csv")
    mso_evidence_values = {r["mso_evidence"] for r in rows}
    assert mso_evidence_values != {"high"}, (
        f"mso_evidence is uniformly high — mixed-confidence aggregation not "
        f"discriminating. Saw: {mso_evidence_values}"
    )
