#!/usr/bin/env python3
"""Tests for ``prepare_step`` + ``StepContext`` in lib/step_runner.py.

These tests cover the pre-invocation boilerplate helper that replaces
``run_claude_step``. ``prepare_step`` is introduced in Phase 4 of the
pipeline-hardening plan; until then these tests are RED with ImportError.
"""

from __future__ import annotations

import time

import pytest


class TestPrepareStepRealRun:
    def test_real_run_returns_proceed_and_writes_prompt(self, tmp_path):
        from lib.step_runner import prepare_step, StepContext

        prompt_path = tmp_path / "prompts" / "p.md"
        out_dir = tmp_path / "out"
        ctx = prepare_step(
            step_label="test",
            concept_id="01",
            prompt_text="PROMPT BODY",
            prompt_path=prompt_path,
            out_dir=out_dir,
            dry_run=False,
            force=False,
        )
        assert isinstance(ctx, StepContext)
        assert ctx.proceed is True
        assert ctx.prompt_text == "PROMPT BODY"
        assert prompt_path.exists()
        assert prompt_path.read_text() == "PROMPT BODY"
        assert out_dir.exists()
        assert ctx.start_time > 0.0

    def test_start_time_is_monotonic_on_proceed(self, tmp_path):
        from lib.step_runner import prepare_step

        t_before = time.time()
        ctx = prepare_step(
            step_label="test",
            concept_id="01",
            prompt_text="x",
            prompt_path=tmp_path / "p.md",
            out_dir=tmp_path,
            dry_run=False,
        )
        t_after = time.time()
        assert t_before <= ctx.start_time <= t_after


class TestPrepareStepDryRun:
    def test_dry_run_writes_prompt_but_returns_no_proceed(self, tmp_path, capsys):
        """Dry-run writes the prompt so operators can inspect it, but does
        not set ``proceed=True`` (caller should skip the Claude invocation).
        """
        from lib.step_runner import prepare_step

        prompt_path = tmp_path / "prompts" / "p.md"
        ctx = prepare_step(
            step_label="gap-check",
            concept_id="01",
            prompt_text="PROMPT",
            prompt_path=prompt_path,
            out_dir=tmp_path / "out",
            dry_run=True,
        )
        assert ctx.proceed is False
        assert prompt_path.exists(), "dry-run must still write the prompt for inspection"
        assert prompt_path.read_text() == "PROMPT"
        assert ctx.start_time == 0.0

        captured = capsys.readouterr()
        assert "dry-run" in captured.out.lower()


class TestPrepareStepSkipIfExists:
    def test_skip_if_exists_does_not_touch_prompt_file(self, tmp_path, capsys):
        """Behavioral change vs. run_claude_step: skip-if-exists must NOT
        write the prompt file (which the legacy helper did, churning prompts
        on skipped runs). See design §component-6 behavioral-note.
        """
        from lib.step_runner import prepare_step

        prompt_path = tmp_path / "prompts" / "p.md"
        existing_output = tmp_path / "already_exists.md"
        existing_output.write_text("done")

        ctx = prepare_step(
            step_label="test",
            concept_id="01",
            prompt_text="PROMPT",
            prompt_path=prompt_path,
            out_dir=tmp_path / "out",
            skip_if_exists=existing_output,
            dry_run=False,
            force=False,
        )
        assert ctx.proceed is False
        assert not prompt_path.exists()  # ← behavioral change
        captured = capsys.readouterr()
        assert "skip" in captured.out.lower()

    def test_skip_if_exists_bypassed_by_force(self, tmp_path):
        from lib.step_runner import prepare_step

        prompt_path = tmp_path / "prompts" / "p.md"
        existing_output = tmp_path / "already.md"
        existing_output.write_text("done")

        ctx = prepare_step(
            step_label="test",
            concept_id="01",
            prompt_text="PROMPT",
            prompt_path=prompt_path,
            out_dir=tmp_path / "out",
            skip_if_exists=existing_output,
            dry_run=False,
            force=True,
        )
        assert ctx.proceed is True
        assert prompt_path.exists()

    def test_skip_if_exists_none_does_not_skip(self, tmp_path):
        from lib.step_runner import prepare_step

        ctx = prepare_step(
            step_label="test",
            concept_id="01",
            prompt_text="PROMPT",
            prompt_path=tmp_path / "p.md",
            out_dir=tmp_path,
            skip_if_exists=None,
        )
        assert ctx.proceed is True


class TestPrepareStepDirectoryCreation:
    def test_mkdirs_out_dir_and_prompt_parent(self, tmp_path):
        from lib.step_runner import prepare_step

        deep_out = tmp_path / "a" / "b" / "c"
        deep_prompt = tmp_path / "x" / "y" / "z" / "p.md"

        ctx = prepare_step(
            step_label="test",
            concept_id="01",
            prompt_text="PROMPT",
            prompt_path=deep_prompt,
            out_dir=deep_out,
        )
        assert ctx.proceed is True
        assert deep_out.exists() and deep_out.is_dir()
        assert deep_prompt.parent.exists() and deep_prompt.parent.is_dir()


class TestStepContext:
    def test_proceed_false_has_zero_start_time(self, tmp_path):
        """Documented invariant in the design: when proceed=False, start_time
        is 0.0 (not None, not time.time())."""
        from lib.step_runner import prepare_step

        existing = tmp_path / "done.md"
        existing.write_text("x")
        ctx = prepare_step(
            step_label="test",
            concept_id="01",
            prompt_text="x",
            prompt_path=tmp_path / "p.md",
            out_dir=tmp_path,
            skip_if_exists=existing,
        )
        assert ctx.proceed is False
        assert ctx.start_time == 0.0
