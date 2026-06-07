#!/usr/bin/env python3
"""Tests for the --inherit-from all-or-nothing resume (runner).

Inheritance is strict (design Invariant 9): the new cohort must be byte-identical
to the prior run — same concepts, same artifact SHAs, same staleness — or the run
aborts naming what changed. On an exact match the prior report / per-concept docs
/ findings are copied forward and the lead prompt gets the recovery preamble.

All runs here use dry_run=True so no lead is invoked (invoke_claude is stubbed to
raise, proving it is never called on these paths).
"""

from __future__ import annotations

import json

import pytest

from lib.concepts import load_concepts
from lib.portfolio_audit import runner

REAL_CID = "01-hts-compact-tokamak"


@pytest.fixture
def record_real():
    by_id = {r["concept_id"]: r for r in load_concepts()}
    return by_id[REAL_CID]


@pytest.fixture(autouse=True)
def _never_call_lead(monkeypatch):
    # Every resume path is exercised with dry_run=True; the lead must not run.
    monkeypatch.setattr(runner, "invoke_claude", lambda *a, **k: 1 / 0)


def _seed_prior_run(tmp_path, record_real):
    """A prior run folder with forensics + simulated lead output."""
    prior = tmp_path / "prior"
    runner.run([record_real], run_dir=prior, model="opus", cli="x", dry_run=True)
    (prior / "report.md").write_text("# prior report\nwork so far\n", encoding="utf-8")
    (prior / "concepts" / f"{REAL_CID}.md").write_text("# prior doc\n", encoding="utf-8")
    (prior / "findings.jsonl").write_text(
        json.dumps({"concept_id": REAL_CID, "severity": "low"}) + "\n", encoding="utf-8"
    )
    return prior


# ---------------------------------------------------------------------------
# diff_manifests — the resume gate, unit-level
# ---------------------------------------------------------------------------


def test_diff_manifests_identical_is_empty():
    base = {"concepts": {"a": {"sha256": {"x": "1"}, "model_stale": False}}}
    assert runner.diff_manifests(base, base) == []


def test_diff_manifests_detects_sha_cohort_and_staleness():
    base = {"concepts": {"a": {"sha256": {"x": "1"}, "model_stale": False}}}

    sha_changed = {"concepts": {"a": {"sha256": {"x": "2"}, "model_stale": False}}}
    assert any("SHAs changed" in r for r in runner.diff_manifests(sha_changed, base))

    added = {"concepts": {
        "a": {"sha256": {"x": "1"}, "model_stale": False},
        "b": {"sha256": {}, "model_stale": False},
    }}
    assert any(r.startswith("b:") for r in runner.diff_manifests(added, base))

    removed = {"concepts": {}}
    assert any(r.startswith("a:") for r in runner.diff_manifests(removed, base))

    stale_changed = {"concepts": {"a": {"sha256": {"x": "1"}, "model_stale": True}}}
    assert any("model_stale" in r for r in runner.diff_manifests(stale_changed, base))


# ---------------------------------------------------------------------------
# Exact match → copy forward + recovery preamble
# ---------------------------------------------------------------------------


def test_inherit_exact_match_copies_forward(tmp_path, record_real):
    prior = _seed_prior_run(tmp_path, record_real)
    new = tmp_path / "new"
    runner.run(
        [record_real], run_dir=new, model="opus", cli="x",
        dry_run=True, inherit_from=prior,
    )
    assert (new / "report.md").read_text() == (prior / "report.md").read_text()
    assert (new / "findings.jsonl").exists()
    assert (new / "concepts" / f"{REAL_CID}.md").exists()
    assert "Recovery:" in (new / "prompts" / "lead_prompt.md").read_text()


def test_no_recovery_preamble_without_inherit(tmp_path, record_real):
    new = tmp_path / "new"
    runner.run([record_real], run_dir=new, model="opus", cli="x", dry_run=True)
    assert "Recovery:" not in (new / "prompts" / "lead_prompt.md").read_text()


# ---------------------------------------------------------------------------
# Any difference → abort naming the changed concept
# ---------------------------------------------------------------------------


def test_inherit_any_diff_errors_out(tmp_path, record_real, capsys):
    prior = _seed_prior_run(tmp_path, record_real)
    # Mutate the prior manifest so an artifact SHA no longer matches.
    manifest = json.loads((prior / "manifest.json").read_text())
    manifest["concepts"][REAL_CID]["sha256"]["analysis_md"] = "DIFFERENT"
    (prior / "manifest.json").write_text(json.dumps(manifest), encoding="utf-8")

    new = tmp_path / "new"
    with pytest.raises(SystemExit):
        runner.run(
            [record_real], run_dir=new, model="opus", cli="x",
            dry_run=True, inherit_from=prior,
        )
    err = capsys.readouterr().err
    assert REAL_CID in err  # names the concept that changed


def test_inherit_missing_prior_manifest_errors(tmp_path, record_real):
    new = tmp_path / "new"
    with pytest.raises(SystemExit):
        runner.run(
            [record_real], run_dir=new, model="opus", cli="x",
            dry_run=True, inherit_from=tmp_path / "does-not-exist",
        )
