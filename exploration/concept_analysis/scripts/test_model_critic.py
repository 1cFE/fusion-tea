#!/usr/bin/env python3
"""Tests for agents/model_critic.py — dry-run + real-Claude paths.

Phase 3 covers dry-run rendering + refusal copy. Phase 4 covers the
real-Claude path: mocked ``invoke_claude``, atomic write, versioned filename,
re-run preservation, FR-6b end-to-end injection, missing-concept-dir hard
error. Phase 5 will add the archived-concept simulation.
"""

from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path
from unittest.mock import patch

import pytest

from agents.model_critic import run as critic_run
from lib.claude import InvokeResult
from lib.concepts import load_concepts


REAL_CID = "01-hts-compact-tokamak"
_RUN_ANALYSIS = Path(__file__).resolve().parent / "run_analysis.py"


@pytest.fixture
def record_real():
    by_id = {r["concept_id"]: r for r in load_concepts()}
    return by_id[REAL_CID]


@pytest.fixture
def record_freeform():
    by_id = {r["concept_id"]: r for r in load_concepts()}
    # 02-acoustic-icf-sonofusion is fit_grade=None freeform-deferred.
    return by_id["02-acoustic-icf-sonofusion"]


# ---------------------------------------------------------------------------
# Dry-run path — programmatic
# ---------------------------------------------------------------------------


def test_dry_run_prints_rendered_prompt_with_all_flag_blocks(capsys, record_real):
    rc = critic_run(record_real, dry_run=True)
    out = capsys.readouterr().out
    assert rc == 0
    for block in ("### dpc", "### contract", "### count_smell", "### sanity"):
        assert block in out, f"missing prompt block: {block}"
    # Design-point block contains the table's named plant + P_native as fixed input.
    assert "p_native_mwe" in out
    # FR-5a — scope boundary prose visible.
    assert "do **not** second-guess" in out.lower() or "do not second-guess" in out.lower()
    assert "source selection" in out.lower()
    # FR-5b — selection-as-fixed-input prose visible.
    assert "fixed input" in out.lower()
    # FR-6b — "reason on top of" framing.
    assert "reason on top" in out.lower() or "reason about what" in out.lower()


def test_dry_run_writes_no_critic_review_file(capsys, record_real):
    from lib.paths import ANALYSES_DIR
    concept_dir = ANALYSES_DIR / REAL_CID
    pre = {p.name for p in concept_dir.iterdir() if p.name.startswith("critic_review_")}
    critic_run(record_real, dry_run=True)
    capsys.readouterr()
    post = {p.name for p in concept_dir.iterdir() if p.name.startswith("critic_review_")}
    assert pre == post


# ---------------------------------------------------------------------------
# Refusal paths — distinct messages per Runnability state (FR-7)
# ---------------------------------------------------------------------------


def test_dry_run_refusal_freeform(capsys, record_freeform):
    rc = critic_run(record_freeform, dry_run=True)
    assert rc != 0
    err = capsys.readouterr().err
    assert "model-critic refuses" in err
    assert "architecturally freeform" in err
    # Distinct from regen's wording and from pending-design-point's wording.
    assert "design-point row not yet populated" not in err


# ---------------------------------------------------------------------------
# Phase 4 — real-Claude path with mocked invoke_claude
# ---------------------------------------------------------------------------


@pytest.fixture
def tmp_analyses(tmp_path, monkeypatch):
    """Repoint ANALYSES_DIR (in both critic_inputs and model_critic) at a
    writable tmp tree seeded with the real reference concept's artifacts."""
    fake = tmp_path / "analyses"
    cdir = fake / REAL_CID
    real_src = Path(__file__).resolve().parent.parent / "analyses" / REAL_CID
    cdir.mkdir(parents=True)
    for name in ("analysis.md", "model_setup.py", "model_output.txt"):
        s = real_src / name
        if s.exists():
            shutil.copy2(s, cdir / name)
    monkeypatch.setattr("lib.critic_inputs.ANALYSES_DIR", fake)
    monkeypatch.setattr("agents.model_critic.ANALYSES_DIR", fake)
    return cdir


def test_real_invocation_writes_versioned_file(record_real, tmp_analyses):
    with patch("agents.model_critic.invoke_claude") as m:
        m.return_value = InvokeResult("# stub review\nbody", "", 0)
        rc = critic_run(
            record_real, model="sonnet", timeout=900, dry_run=False,
            now=lambda: "20260601-120000",
        )
    assert rc == 0
    out = tmp_analyses / "critic_review_20260601-120000.md"
    assert out.exists()
    assert out.read_text() == "# stub review\nbody"


def test_claude_failure_writes_no_file(record_real, tmp_analyses):
    with patch("agents.model_critic.invoke_claude") as m:
        m.return_value = InvokeResult("", "boom", 1)
        rc = critic_run(record_real, dry_run=False, now=lambda: "20260601-120000")
    assert rc != 0
    assert not (tmp_analyses / "critic_review_20260601-120000.md").exists()


def test_claude_empty_stdout_writes_no_file(record_real, tmp_analyses):
    """rc=0 + empty stdout is still a failure — write nothing."""
    with patch("agents.model_critic.invoke_claude") as m:
        m.return_value = InvokeResult("   \n  ", "", 0)
        rc = critic_run(record_real, dry_run=False, now=lambda: "20260601-120000")
    assert rc != 0
    assert not (tmp_analyses / "critic_review_20260601-120000.md").exists()


def test_rerun_preserves_prior_reviews(record_real, tmp_analyses):
    with patch("agents.model_critic.invoke_claude") as m:
        m.return_value = InvokeResult("# review A", "", 0)
        critic_run(record_real, dry_run=False, now=lambda: "20260601-120000")
        m.return_value = InvokeResult("# review B", "", 0)
        critic_run(record_real, dry_run=False, now=lambda: "20260601-130000")
    files = sorted(p.name for p in tmp_analyses.glob("critic_review_*.md"))
    assert files == [
        "critic_review_20260601-120000.md",
        "critic_review_20260601-130000.md",
    ]
    assert (tmp_analyses / files[0]).read_text() == "# review A"
    assert (tmp_analyses / files[1]).read_text() == "# review B"


def test_deterministic_flags_reach_invoke_claude(record_real, tmp_analyses):
    """End-to-end FR-6b: the prompt passed to invoke_claude carries all 4 blocks."""
    captured = {}
    def _capture(prompt, **kw):
        captured["prompt"] = prompt
        return InvokeResult("# done", "", 0)
    with patch("agents.model_critic.invoke_claude", side_effect=_capture):
        critic_run(record_real, dry_run=False, now=lambda: "20260601-120000")
    p = captured["prompt"]
    for block in ("### dpc", "### contract", "### count_smell", "### sanity"):
        assert block in p


def test_missing_concept_dir_hard_errors(record_real, tmp_analyses):
    """Wiping the concept dir between collect() and invoke_claude → rc=2, no write."""
    # collect() reads files lazily, so we let collect() run, then nuke the dir
    # by patching ANALYSES_DIR.exists check via removing the dir post-collect.
    # Cleanest: patch invoke_claude AND remove the dir before invoke_claude is reached.
    # Simpler: remove the dir entirely, expect critic to refuse before invoking Claude.
    shutil.rmtree(tmp_analyses)
    with patch("agents.model_critic.invoke_claude") as m:
        # collect() will see missing files but produce empty strings; the
        # orchestrator's concept_dir.exists() guard then catches it.
        rc = critic_run(record_real, dry_run=False, now=lambda: "20260601-120000")
    assert rc == 2
    assert not m.called


def test_pending_refusal_distinct_from_freeform():
    """Both non-runnable refusal messages exist and differ from each other."""
    from agents.model_critic import _REFUSAL_COPY
    from lib.concepts import Runnability
    freeform = _REFUSAL_COPY[Runnability.FREEFORM_DEFERRED]
    pending = _REFUSAL_COPY[Runnability.PENDING_DESIGN_POINT]
    assert freeform != pending
    assert "freeform" in freeform.lower()
    assert "design-point row not yet populated" in pending


# ---------------------------------------------------------------------------
# CLI subparser smoke test
# ---------------------------------------------------------------------------


def test_cli_dry_run_subprocess_emits_prompt():
    """Confirm the model-critic subcommand is wired end-to-end via the CLI."""
    result = subprocess.run(
        [sys.executable, str(_RUN_ANALYSIS), "model-critic", REAL_CID, "--dry-run"],
        capture_output=True, text=True, timeout=60,
    )
    assert result.returncode == 0, f"stderr: {result.stderr}"
    assert "### dpc" in result.stdout
    assert "Critic Review" in result.stdout  # output-format block in the template


def test_cli_refusal_subprocess_exits_nonzero():
    result = subprocess.run(
        [sys.executable, str(_RUN_ANALYSIS),
         "model-critic", "02-acoustic-icf-sonofusion", "--dry-run"],
        capture_output=True, text=True, timeout=60,
    )
    assert result.returncode != 0
    assert "model-critic refuses" in result.stderr
    assert "architecturally freeform" in result.stderr
