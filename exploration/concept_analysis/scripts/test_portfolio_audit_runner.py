#!/usr/bin/env python3
"""Tests for lib/portfolio_audit/runner.py — forensic prep + CLI plumbing.

The runner's contract (no live lead is invoked here — invoke_claude is stubbed):
- The three forensic files (manifest, digest, rendered lead prompt) are on disk
  *before* the lead is called, so a crash mid-lead leaves a full record.
- --dry-run writes forensics and does not call the lead.
- --passed-only filters the cohort to PASS-verdict concepts.
- run folders are timestamped and collision-safe.
- the run touches nothing inside a concept's analyses dir (advisory, non-mutating).
- the rendered lead prompt has its includes + digest substituted in.
"""

from __future__ import annotations

import types
from datetime import datetime

import pytest

from lib.concepts import load_concepts
from lib.paths import ANALYSES_DIR
from lib.portfolio_audit import runner

REAL_CID = "01-hts-compact-tokamak"


@pytest.fixture
def record_real():
    by_id = {r["concept_id"]: r for r in load_concepts()}
    return by_id[REAL_CID]


def _fake_ok_result():
    return types.SimpleNamespace(returncode=0, stderr="")


# ---------------------------------------------------------------------------
# Forensics-before-lead
# ---------------------------------------------------------------------------


def test_forensics_written_before_lead(tmp_path, monkeypatch, record_real):
    # The lead call blows up; forensics must already be on disk.
    monkeypatch.setattr(runner, "invoke_claude", lambda *a, **k: 1 / 0)
    run_dir = tmp_path / "run"
    with pytest.raises(ZeroDivisionError):
        runner.run([record_real], run_dir=run_dir, model="opus", cli="portfolio-audit 01")
    assert (run_dir / "manifest.json").exists()
    assert (run_dir / "cohort_digest.json").exists()
    assert (run_dir / "prompts" / "lead_prompt.md").exists()


def test_dry_run_writes_forensics_and_skips_lead(tmp_path, monkeypatch, record_real):
    # If the lead were called, this stub would raise — dry-run must not call it.
    monkeypatch.setattr(runner, "invoke_claude", lambda *a, **k: 1 / 0)
    run_dir = tmp_path / "run"
    runner.run([record_real], run_dir=run_dir, model="opus", cli="x", dry_run=True)
    assert (run_dir / "manifest.json").exists()
    assert (run_dir / "cohort_digest.json").exists()
    assert (run_dir / "prompts" / "lead_prompt.md").exists()
    assert not (run_dir / "run.log").exists()  # lead never ran


# ---------------------------------------------------------------------------
# --passed-only cohort filter
# ---------------------------------------------------------------------------


def test_passed_only_filters_to_pass_verdicts(monkeypatch):
    verdicts = {"a": "PASS", "b": "FAIL", "c": "PASS", "d": None}
    monkeypatch.setattr(runner, "latest_verdict", lambda cid: verdicts[cid])
    records = [{"concept_id": c} for c in ("a", "b", "c", "d")]

    cohort = runner.resolve_audit_cohort(records, passed_only=True)
    assert [r["concept_id"] for r in cohort] == ["a", "c"]
    # Without the filter, everything passes through.
    assert len(runner.resolve_audit_cohort(records, passed_only=False)) == 4


def test_latest_verdict_reads_real_concept():
    # The real concept 01 has completed iterations with a verdict.
    assert runner.latest_verdict(REAL_CID) in {"PASS", "FAIL", "SINGLE_PASS", "ERROR"}


# ---------------------------------------------------------------------------
# Run-folder timestamp collision
# ---------------------------------------------------------------------------


def test_make_run_dir_collision_suffix(tmp_path, monkeypatch):
    monkeypatch.setattr(runner, "REVIEWS_DIR", tmp_path / "reviews")
    now = datetime(2026, 6, 7, 10, 52, 43)
    d1 = runner.make_run_dir(now=now)
    d2 = runner.make_run_dir(now=now)
    assert d1.name == "20260607-105243"
    assert d2.name == "20260607-105243-2"
    assert d1.is_dir() and d2.is_dir()


# ---------------------------------------------------------------------------
# Invariant 10 — the run mutates nothing in a concept's analyses dir
# ---------------------------------------------------------------------------


def test_run_does_not_touch_concept_dir(tmp_path, monkeypatch, record_real):
    monkeypatch.setattr(runner, "invoke_claude", lambda *a, **k: _fake_ok_result())
    concept_dir = ANALYSES_DIR / REAL_CID

    def snapshot():
        return {
            str(p.relative_to(concept_dir)): p.stat().st_mtime
            for p in concept_dir.rglob("*")
            if p.is_file()
        }

    before = snapshot()
    runner.run([record_real], run_dir=tmp_path / "run", model="opus", cli="x")
    after = snapshot()
    assert before == after


# ---------------------------------------------------------------------------
# Lead prompt renders: includes inlined, digest + run_dir substituted
# ---------------------------------------------------------------------------


def test_lead_prompt_renders_includes_and_digest(tmp_path, monkeypatch, record_real):
    monkeypatch.setattr(runner, "invoke_claude", lambda *a, **k: 1 / 0)
    run_dir = tmp_path / "run"
    with pytest.raises(ZeroDivisionError):
        runner.run([record_real], run_dir=run_dir, model="opus", cli="x")

    prompt = (run_dir / "prompts" / "lead_prompt.md").read_text(encoding="utf-8")
    assert "Family-internal coherence" in prompt  # criteria include resolved
    assert "Investigator subagent" in prompt  # investigator include resolved
    assert "Writer subagent" in prompt  # writer include resolved
    assert REAL_CID in prompt  # digest content embedded
    assert str(run_dir.resolve()) in prompt  # run_dir substituted
    # Every {{...}} placeholder and {{@include}} must be resolved — none left.
    assert "{{" not in prompt
