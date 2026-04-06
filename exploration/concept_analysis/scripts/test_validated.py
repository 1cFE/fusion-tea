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

        # Second call should use --resume
        second_call_args = mock_invoke.call_args_list[1]
        assert second_call_args[0][0] == "Add VERDICT: PASS"  # fix_message as prompt


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
