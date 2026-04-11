#!/usr/bin/env python3
"""Tests for invoke_claude_validated() wrapper in lib/claude.py."""

import json
from pathlib import Path
from unittest.mock import patch, MagicMock, call

from lib.claude import (
    InvokeResult,
    ValidatedResult,
    invoke_claude_validated,
)
from lib.validators import ValidationResult


def _make_invoke_result(stdout="response", session_id="test-sid", rc=0):
    return InvokeResult(stdout=stdout, stderr="", returncode=rc, session_id=session_id)


# ---------------------------------------------------------------------------
# ValidatedResult basics
# ---------------------------------------------------------------------------


class TestValidatedResult:
    def test_fields(self):
        r = ValidatedResult(
            invoke=_make_invoke_result(),
            validation_passed=True,
            attempts=1,
            log_entries=[],
        )
        assert r.validation_passed is True
        assert r.attempts == 1


# ---------------------------------------------------------------------------
# invoke_claude_validated
# ---------------------------------------------------------------------------


class TestValidatedNoValidator:
    @patch("lib.claude.invoke_claude")
    def test_no_validator_passthrough(self, mock_invoke):
        mock_invoke.return_value = _make_invoke_result("output", "sid")
        result = invoke_claude_validated("prompt", Path("/tmp"))
        assert result.validation_passed is True
        assert result.attempts == 1
        assert result.invoke.stdout == "output"
        mock_invoke.assert_called_once()


class TestValidatedPassesFirstTry:
    @patch("lib.claude.invoke_claude")
    def test_passes_first_try(self, mock_invoke, tmp_path):
        mock_invoke.return_value = _make_invoke_result(session_id="sid")
        output_file = tmp_path / "feedback.md"
        output_file.write_text("VERDICT: PASS\n")

        def validator(text):
            return ValidationResult(valid=True, details="ok")

        result = invoke_claude_validated(
            "prompt", Path("/tmp"),
            validator=validator, output_path=output_file,
        )
        assert result.validation_passed is True
        assert result.attempts == 1
        mock_invoke.assert_called_once()


class TestValidatedRetryOnFailure:
    @patch("lib.claude.invoke_claude")
    def test_retries_on_failure(self, mock_invoke, tmp_path):
        output_file = tmp_path / "feedback.md"

        # Track call count to change file contents on retry
        call_count = 0

        def side_effect(*args, **kwargs):
            nonlocal call_count
            call_count += 1
            if call_count == 1:
                # First call: write bad file
                output_file.write_text("No verdict here")
                return _make_invoke_result(session_id="sid-1")
            else:
                # Retry: write good file
                output_file.write_text("VERDICT: PASS\n")
                return _make_invoke_result(session_id="sid-1")

        mock_invoke.side_effect = side_effect

        def validator(text):
            if "VERDICT: PASS" in text:
                return ValidationResult(valid=True, details="ok")
            return ValidationResult(
                valid=False,
                fix_message="Add VERDICT: PASS",
                details="missing verdict",
            )

        result = invoke_claude_validated(
            "prompt", Path("/tmp"),
            validator=validator, output_path=output_file,
        )
        assert result.validation_passed is True
        assert result.attempts == 2
        assert mock_invoke.call_count == 2

        # Second call should use --resume; the fix message is now augmented
        # with attempt-escalation context and the output path (FR-5/FR-6).
        second_call_args = mock_invoke.call_args_list[1]
        retry_prompt = second_call_args[0][0]
        assert "Add VERDICT: PASS" in retry_prompt
        assert "attempt 2 of 3" in retry_prompt
        assert str(output_file) in retry_prompt


class TestValidatedMaxRetriesExceeded:
    @patch("lib.claude.invoke_claude")
    def test_max_retries_exceeded(self, mock_invoke, tmp_path):
        output_file = tmp_path / "feedback.md"
        output_file.write_text("bad output")

        mock_invoke.return_value = _make_invoke_result(session_id="sid")

        def validator(text):
            return ValidationResult(
                valid=False,
                fix_message="Fix it",
                details="still bad",
            )

        result = invoke_claude_validated(
            "prompt", Path("/tmp"),
            validator=validator, output_path=output_file,
            max_retries=2,
        )
        assert result.validation_passed is False
        assert result.attempts == 3  # 1 initial + 2 retries
        assert mock_invoke.call_count == 3


class TestValidatedNoSessionId:
    @patch("lib.claude.invoke_claude")
    def test_no_session_id_skips_retry(self, mock_invoke, tmp_path):
        output_file = tmp_path / "feedback.md"
        output_file.write_text("bad output")

        # No session_id — can't resume
        mock_invoke.return_value = _make_invoke_result(session_id=None)

        def validator(text):
            return ValidationResult(valid=False, fix_message="Fix", details="bad")

        result = invoke_claude_validated(
            "prompt", Path("/tmp"),
            validator=validator, output_path=output_file,
        )
        assert result.validation_passed is False
        assert result.attempts == 1
        mock_invoke.assert_called_once()


class TestValidatedStdoutFallback:
    @patch("lib.claude.invoke_claude")
    def test_validates_stdout_when_no_output_path(self, mock_invoke):
        mock_invoke.return_value = _make_invoke_result(stdout="VERDICT: PASS\n", session_id="sid")

        def validator(text):
            if "VERDICT: PASS" in text:
                return ValidationResult(valid=True, details="ok")
            return ValidationResult(valid=False, fix_message="Fix", details="bad")

        result = invoke_claude_validated(
            "prompt", Path("/tmp"),
            validator=validator,
        )
        assert result.validation_passed is True
        assert result.attempts == 1


class TestValidationLog:
    @patch("lib.claude.invoke_claude")
    def test_log_written(self, mock_invoke, tmp_path):
        output_file = tmp_path / "feedback.md"
        output_file.write_text("VERDICT: PASS\n")
        log_path = tmp_path / "validation_log.json"

        mock_invoke.return_value = _make_invoke_result(session_id="sid")

        def validator(text):
            return ValidationResult(valid=True, details="format ok")

        invoke_claude_validated(
            "prompt", Path("/tmp"),
            validator=validator, output_path=output_file,
            step_label="assess", log_path=log_path,
        )

        assert log_path.exists()
        entries = json.loads(log_path.read_text())
        assert len(entries) == 1
        assert entries[0]["step"] == "assess"
        assert entries[0]["passed"] is True
        assert "timestamp" in entries[0]
        assert entries[0]["attempt"] == 1

    @patch("lib.claude.invoke_claude")
    def test_log_appends(self, mock_invoke, tmp_path):
        """Log appends to existing file."""
        log_path = tmp_path / "validation_log.json"
        log_path.write_text(json.dumps([{"existing": True}]))

        output_file = tmp_path / "feedback.md"
        output_file.write_text("VERDICT: PASS\n")
        mock_invoke.return_value = _make_invoke_result(session_id="sid")

        def validator(text):
            return ValidationResult(valid=True, details="ok")

        invoke_claude_validated(
            "prompt", Path("/tmp"),
            validator=validator, output_path=output_file,
            log_path=log_path,
        )

        entries = json.loads(log_path.read_text())
        assert len(entries) == 2
        assert entries[0]["existing"] is True
        assert entries[1]["passed"] is True

    @patch("lib.claude.invoke_claude")
    def test_log_records_failure_and_retry(self, mock_invoke, tmp_path):
        output_file = tmp_path / "feedback.md"
        log_path = tmp_path / "validation_log.json"

        call_count = 0

        def side_effect(*args, **kwargs):
            nonlocal call_count
            call_count += 1
            if call_count == 1:
                output_file.write_text("bad")
                return _make_invoke_result(session_id="sid")
            else:
                output_file.write_text("VERDICT: PASS\n")
                return _make_invoke_result(session_id="sid")

        mock_invoke.side_effect = side_effect

        def validator(text):
            if "VERDICT: PASS" in text:
                return ValidationResult(valid=True, details="ok")
            return ValidationResult(valid=False, fix_message="Fix it", details="missing verdict")

        invoke_claude_validated(
            "prompt", Path("/tmp"),
            validator=validator, output_path=output_file,
            step_label="assess", log_path=log_path,
        )

        entries = json.loads(log_path.read_text())
        assert len(entries) == 2
        assert entries[0]["passed"] is False
        assert entries[0]["attempt"] == 1
        assert "fix_message_sent" in entries[0]
        assert entries[1]["passed"] is True
        assert entries[1]["attempt"] == 2

    @patch("lib.claude.invoke_claude")
    def test_no_log_when_no_path(self, mock_invoke, tmp_path):
        """No log_path means no file written."""
        output_file = tmp_path / "feedback.md"
        output_file.write_text("VERDICT: PASS\n")
        mock_invoke.return_value = _make_invoke_result(session_id="sid")

        def validator(text):
            return ValidationResult(valid=True, details="ok")

        invoke_claude_validated(
            "prompt", Path("/tmp"),
            validator=validator, output_path=output_file,
        )

        # No validation_log.json should exist
        assert not (tmp_path / "validation_log.json").exists()


# ---------------------------------------------------------------------------
# Phase 3: file-not-found first-class branch + augmented retry prompts (H-01)
# ---------------------------------------------------------------------------


class TestValidatedFileNotFound:
    """H-01 / FR-1: when output_path is provided and the file does not exist
    after invocation, treat it as a distinct failure mode. Do NOT fall back
    to validating stdout — and tell Claude on retry where to write the file.
    """

    @patch("lib.claude.invoke_claude")
    def test_file_missing_does_not_run_validator(self, mock_invoke, tmp_path):
        """The validator must NOT see Claude's conversational text — the
        missing-file branch short-circuits before any validator call."""
        output_file = tmp_path / "feedback.md"
        log_path = tmp_path / "vlog.json"

        validator_calls: list[str] = []

        def spy(text: str) -> ValidationResult:
            validator_calls.append(text)
            return ValidationResult(valid=False, fix_message="x", details="d")

        spy.__name__ = "spy_validator"

        # All 3 attempts return success rc with no file write.
        mock_invoke.return_value = _make_invoke_result(
            stdout="I wrote the file.", session_id="sid",
        )

        result = invoke_claude_validated(
            "prompt", Path("/tmp"),
            validator=spy, output_path=output_file,
            max_retries=2, step_label="t", log_path=log_path,
        )

        assert result.validation_passed is False
        assert validator_calls == []  # validator never ran
        entries = json.loads(log_path.read_text())
        assert len(entries) == 3
        for e in entries:
            assert e["validated_text_preview"] == "FILE NOT FOUND"
            assert "Output file not found" in e["details"]

    @patch("lib.claude.invoke_claude")
    def test_file_missing_retry_prompt_contains_path(self, mock_invoke, tmp_path):
        """The retry prompt sent on attempt 2 must contain the output path
        and 'attempt 2 of 3'."""
        output_file = tmp_path / "feedback.md"

        # Both calls return success rc but no file write; capture the second
        # call's prompt and assert path + attempt label appear.
        mock_invoke.return_value = _make_invoke_result(
            stdout="I wrote it.", session_id="sid",
        )

        invoke_claude_validated(
            "prompt", Path("/tmp"),
            validator=lambda t: ValidationResult(valid=False, fix_message="f", details="d"),
            output_path=output_file,
            max_retries=2,
        )

        retry_prompt = mock_invoke.call_args_list[1][0][0]
        assert str(output_file) in retry_prompt
        assert "attempt 2 of 3" in retry_prompt
        assert "did not write the expected output file" in retry_prompt


class TestAugmentedRetryPrompt:
    @patch("lib.claude.invoke_claude")
    def test_augmented_retry_prompt_contains_path_and_next_attempt(
        self, mock_invoke, tmp_path,
    ):
        """FR-5 + FR-6: when validation fails on attempt 1 of 3, the retry
        prompt sent on attempt 2 must contain the path and 'attempt 2 of 3'.
        """
        output_file = tmp_path / "out.md"
        call_count = 0

        def side_effect(*args, **kwargs):
            nonlocal call_count
            call_count += 1
            if call_count == 1:
                output_file.write_text("bad")
            else:
                output_file.write_text("good")
            return _make_invoke_result(session_id="sid")

        mock_invoke.side_effect = side_effect

        def only_good(text: str) -> ValidationResult:
            return ValidationResult(
                valid=(text == "good"),
                fix_message="make it good",
                details="checking",
            )

        result = invoke_claude_validated(
            "initial prompt", Path("/tmp"),
            validator=only_good, output_path=output_file,
            max_retries=2, step_label="test",
        )

        assert result.validation_passed is True
        retry_prompt = mock_invoke.call_args_list[1][0][0]
        assert str(output_file) in retry_prompt
        assert "attempt 2 of 3" in retry_prompt
        assert "make it good" in retry_prompt
        # Not the FINAL escalation yet
        assert "CRITICAL" not in retry_prompt

    @patch("lib.claude.invoke_claude")
    def test_augmented_retry_final_attempt_says_critical_final(
        self, mock_invoke, tmp_path,
    ):
        """FR-6: after attempt 2 fails, the next retry prompt (the one
        launching attempt 3 of 3) must contain 'CRITICAL' and 'FINAL attempt
        3 of 3'.
        """
        output_file = tmp_path / "out.md"

        def side_effect(*args, **kwargs):
            output_file.write_text("still bad")
            return _make_invoke_result(session_id="sid")

        mock_invoke.side_effect = side_effect

        result = invoke_claude_validated(
            "p", Path("/tmp"),
            validator=lambda t: ValidationResult(
                valid=False, fix_message="try harder", details="d",
            ),
            output_path=output_file, max_retries=2, step_label="t",
        )

        assert result.validation_passed is False
        assert mock_invoke.call_count == 3
        final_retry_prompt = mock_invoke.call_args_list[2][0][0]
        assert "CRITICAL" in final_retry_prompt
        assert "FINAL" in final_retry_prompt
        assert "attempt 3 of 3" in final_retry_prompt
        assert "try harder" in final_retry_prompt


class TestValidatedTextPreview:
    """FR-7: every log entry includes validated_text_preview."""

    @patch("lib.claude.invoke_claude")
    def test_preview_populated_for_file(self, mock_invoke, tmp_path):
        output_file = tmp_path / "out.md"
        output_file.write_text("hello world")
        log_path = tmp_path / "vlog.json"
        mock_invoke.return_value = _make_invoke_result(session_id="sid")

        invoke_claude_validated(
            "p", Path("/tmp"),
            validator=lambda t: ValidationResult(valid=True, details="ok"),
            output_path=output_file, log_path=log_path,
        )

        entries = json.loads(log_path.read_text())
        assert entries[0]["validated_text_preview"] == "hello world"

    @patch("lib.claude.invoke_claude")
    def test_preview_empty_when_text_empty(self, mock_invoke, tmp_path):
        """Empty stdout (no output_path) records preview as 'EMPTY'."""
        log_path = tmp_path / "vlog.json"
        mock_invoke.return_value = _make_invoke_result(stdout="", session_id="sid")

        invoke_claude_validated(
            "p", Path("/tmp"),
            validator=lambda t: ValidationResult(valid=True, details="ok"),
            log_path=log_path,
        )

        entries = json.loads(log_path.read_text())
        assert entries[0]["validated_text_preview"] == "EMPTY"

    @patch("lib.claude.invoke_claude")
    def test_preview_file_not_found_sentinel(self, mock_invoke, tmp_path):
        """Missing file uses 'FILE NOT FOUND' sentinel; validator never ran."""
        output_file = tmp_path / "missing.md"
        log_path = tmp_path / "vlog.json"
        mock_invoke.return_value = _make_invoke_result(session_id="sid")

        invoke_claude_validated(
            "p", Path("/tmp"),
            validator=lambda t: ValidationResult(
                valid=False, fix_message="f", details="d",
            ),
            output_path=output_file, max_retries=0, log_path=log_path,
        )

        entries = json.loads(log_path.read_text())
        assert entries[0]["validated_text_preview"] == "FILE NOT FOUND"


class TestFinalAttemptHasNoFixMessage:
    """FR-7 will_retry gating: the final attempt's log entry is the last
    word — no retry follows, so no fix_message_sent should be recorded."""

    @patch("lib.claude.invoke_claude")
    def test_final_attempt_log_entry_has_no_fix_message_sent(
        self, mock_invoke, tmp_path,
    ):
        output_file = tmp_path / "out.md"
        log_path = tmp_path / "vlog.json"

        def side_effect(*args, **kwargs):
            output_file.write_text("never good")
            return _make_invoke_result(session_id="sid")

        mock_invoke.side_effect = side_effect

        invoke_claude_validated(
            "p", Path("/tmp"),
            validator=lambda t: ValidationResult(
                valid=False, fix_message="fix", details="d",
            ),
            output_path=output_file, max_retries=2,
            log_path=log_path,
        )

        entries = json.loads(log_path.read_text())
        assert len(entries) == 3
        assert "fix_message_sent" in entries[0]
        assert "fix_message_sent" in entries[1]
        assert "fix_message_sent" not in entries[2]
