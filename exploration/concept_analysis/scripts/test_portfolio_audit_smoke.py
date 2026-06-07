#!/usr/bin/env python3
"""End-to-end smoke test for the portfolio-audit runner with a canned lead.

`invoke_claude` is replaced by a stub that simulates what a real lead does — it
writes `report.md`, a per-concept doc under `concepts/`, and a `findings.jsonl`
line, then returns an InvokeResult carrying cost/usage. This codifies the
runner's contract (design "Integration smoke test"): given a lead that produces
the expected artifacts, the run folder ends up with manifest.json,
cohort_digest.json, prompts/lead_prompt.md, report.md, concepts/<id>.md, and a
run.log with cost — and nothing outside the run folder is touched.

It does NOT exercise the real lead (that's the manual, token-spending de-risk
run). It tests the plumbing around the lead, which is valid regardless of how the
real lead behaves.
"""

from __future__ import annotations

import json
import types
from pathlib import Path

import pytest

from lib.concepts import load_concepts
from lib.paths import ANALYSES_DIR
from lib.portfolio_audit import runner

COHORT = ["01-hts-compact-tokamak", "07-maglif", "21-spherical-tokamak-hts"]


@pytest.fixture
def records():
    by_id = {r["concept_id"]: r for r in load_concepts()}
    return [by_id[c] for c in COHORT]


def _canned_lead(run_dir: Path):
    """A stub invoke_claude that simulates the lead's filesystem side effects."""

    def fake_invoke(prompt, *, cwd, timeout, model):
        # The lead writes its report and one confirmed finding's doc + jsonl line.
        (run_dir / "report.md").write_text(
            "# Portfolio audit report\n\nThe MFE tokamaks cluster sensibly.\n"
            "Flagged: [01](concepts/01-hts-compact-tokamak.md).\n",
            encoding="utf-8",
        )
        (run_dir / "concepts" / "01-hts-compact-tokamak.md").write_text(
            "# 01 — CAS22 looks high\n\n## The issue\n...\n",
            encoding="utf-8",
        )
        (run_dir / "findings.jsonl").write_text(
            json.dumps({
                "concept_id": "01-hts-compact-tokamak",
                "severity": "medium",
                "summary": "CAS22 sits above its tokamak neighbors",
                "evidence_pointers": ["model_output.txt", "analysis.md §5b"],
            }) + "\n",
            encoding="utf-8",
        )
        return types.SimpleNamespace(
            returncode=0, stderr="", cost_usd=18.42,
            usage={"input_tokens": 50000, "output_tokens": 12000}, num_turns=24,
        )

    return fake_invoke


def test_smoke_canned_lead_transcript(tmp_path, monkeypatch, records):
    run_dir = tmp_path / "run"
    monkeypatch.setattr(runner, "invoke_claude", _canned_lead(run_dir))

    # Snapshot the cohort's concept dirs to prove the run mutates none of them.
    def snapshot():
        snap = {}
        for cid in COHORT:
            for p in (ANALYSES_DIR / cid).rglob("*"):
                if p.is_file():
                    snap[str(p)] = p.stat().st_mtime
        return snap

    before = snapshot()
    runner.run(records, run_dir=run_dir, model="opus", cli="portfolio-audit 01 07 21")
    after = snapshot()

    # All expected artifacts present.
    assert (run_dir / "manifest.json").exists()
    assert (run_dir / "cohort_digest.json").exists()
    assert (run_dir / "prompts" / "lead_prompt.md").exists()
    assert (run_dir / "report.md").exists()
    assert (run_dir / "findings.jsonl").exists()
    concept_docs = list((run_dir / "concepts").glob("*.md"))
    assert len(concept_docs) >= 1

    # Manifest + digest cover all three concepts.
    manifest = json.loads((run_dir / "manifest.json").read_text())
    digest = json.loads((run_dir / "cohort_digest.json").read_text())
    assert set(manifest["concepts"]) == set(COHORT)
    assert set(digest["concepts"]) == set(COHORT)

    # run.log captured the lead cost from the result event.
    run_log = (run_dir / "run.log").read_text()
    assert "$18.42" in run_log
    assert "turns: 24" in run_log

    # Invariant 1 / 10: nothing outside the run folder was touched.
    assert before == after


def test_smoke_run_log_notes_missing_cost(tmp_path, monkeypatch, records):
    """When the lead result carries no cost, run.log says so plainly."""
    run_dir = tmp_path / "run"

    def fake_invoke(prompt, *, cwd, timeout, model):
        (run_dir / "report.md").write_text("# Report\n", encoding="utf-8")
        return types.SimpleNamespace(returncode=0, stderr="")  # no cost fields

    monkeypatch.setattr(runner, "invoke_claude", fake_invoke)
    runner.run(records, run_dir=run_dir, model="opus", cli="x")
    assert "cost: unavailable" in (run_dir / "run.log").read_text()
