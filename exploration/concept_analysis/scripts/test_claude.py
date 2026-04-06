#!/usr/bin/env python3
"""Tests for InvokeResult and JSON event stream parsing in lib/claude.py."""

import json
from unittest.mock import patch, MagicMock

from lib.claude import InvokeResult, invoke_claude, _parse_json_events


# ---------------------------------------------------------------------------
# InvokeResult backward compatibility
# ---------------------------------------------------------------------------


class TestInvokeResult:
    def test_unpacking_three_tuple(self):
        """Existing callers use: stdout, stderr, rc = invoke_claude(...)"""
        r = InvokeResult(stdout="hello", stderr="", returncode=0, session_id="abc")
        stdout, stderr, rc = r
        assert stdout == "hello"
        assert stderr == ""
        assert rc == 0

    def test_session_id_accessible(self):
        r = InvokeResult(stdout="hello", stderr="", returncode=0, session_id="abc-123")
        assert r.session_id == "abc-123"

    def test_session_id_default_none(self):
        r = InvokeResult(stdout="hello", stderr="", returncode=0)
        assert r.session_id is None

    def test_unpacking_ignores_session_id(self):
        """3-tuple unpacking should not include session_id."""
        r = InvokeResult(stdout="a", stderr="b", returncode=1, session_id="sid")
        parts = list(r)
        assert len(parts) == 3
        assert parts == ["a", "b", 1]


# ---------------------------------------------------------------------------
# JSON event stream parsing
# ---------------------------------------------------------------------------


class TestParseJsonEvents:
    def test_normal_events(self):
        events = [
            {"type": "system", "session_id": "uuid-here"},
            {"type": "assistant", "message": {"content": [{"text": "thinking"}]}},
            {"type": "result", "result": "Hello world", "session_id": "uuid-here"},
        ]
        text, session_id = _parse_json_events(json.dumps(events))
        assert text == "Hello world"
        assert session_id == "uuid-here"

    def test_minimal_events(self):
        events = [
            {"type": "result", "result": "Just the result", "session_id": "s1"},
        ]
        text, session_id = _parse_json_events(json.dumps(events))
        assert text == "Just the result"
        assert session_id == "s1"

    def test_session_id_from_system_event(self):
        events = [
            {"type": "system", "session_id": "from-system"},
            {"type": "result", "result": "text"},
        ]
        text, session_id = _parse_json_events(json.dumps(events))
        assert session_id == "from-system"

    def test_no_result_event(self):
        """If no result event, returns empty text."""
        events = [
            {"type": "system", "session_id": "sid"},
        ]
        text, session_id = _parse_json_events(json.dumps(events))
        assert text == ""
        assert session_id == "sid"

    def test_invalid_json_raises(self):
        """Invalid JSON should raise ValueError."""
        try:
            _parse_json_events("not json at all")
            assert False, "Should have raised"
        except (json.JSONDecodeError, ValueError):
            pass

    def test_empty_list(self):
        text, session_id = _parse_json_events("[]")
        assert text == ""
        assert session_id is None


# ---------------------------------------------------------------------------
# invoke_claude integration (mocked subprocess)
# ---------------------------------------------------------------------------


class TestInvokeClaude:
    def _make_json_output(self, result_text="response", session_id="test-sid"):
        events = [
            {"type": "system", "session_id": session_id},
            {"type": "result", "result": result_text, "session_id": session_id},
        ]
        return json.dumps(events)

    @patch("lib.claude.subprocess.run")
    def test_returns_invoke_result(self, mock_run):
        mock_run.return_value = MagicMock(
            stdout=self._make_json_output("hello", "sid-1"),
            stderr="verbose output",
            returncode=0,
        )
        result = invoke_claude("prompt", cwd="/tmp")
        assert isinstance(result, InvokeResult)
        assert result.stdout == "hello"
        assert result.session_id == "sid-1"
        assert result.returncode == 0

    @patch("lib.claude.subprocess.run")
    def test_backward_compat_unpacking(self, mock_run):
        mock_run.return_value = MagicMock(
            stdout=self._make_json_output("text", "sid"),
            stderr="err",
            returncode=0,
        )
        stdout, stderr, rc = invoke_claude("prompt", cwd="/tmp")
        assert stdout == "text"
        assert stderr == "err"
        assert rc == 0

    @patch("lib.claude.subprocess.run")
    def test_json_parse_failure_fallback(self, mock_run):
        """If stdout isn't valid JSON, fall back to raw stdout."""
        mock_run.return_value = MagicMock(
            stdout="plain text response",
            stderr="",
            returncode=0,
        )
        result = invoke_claude("prompt", cwd="/tmp")
        assert result.stdout == "plain text response"
        assert result.session_id is None
        assert result.returncode == 0

    @patch("lib.claude.subprocess.run")
    def test_output_format_json_in_command(self, mock_run):
        mock_run.return_value = MagicMock(
            stdout=self._make_json_output(),
            stderr="",
            returncode=0,
        )
        invoke_claude("prompt", cwd="/tmp")
        cmd = mock_run.call_args[0][0]
        assert "--output-format" in cmd
        assert "json" in cmd

    @patch("lib.claude.subprocess.run")
    def test_timeout_returns_invoke_result(self, mock_run):
        import subprocess
        mock_run.side_effect = subprocess.TimeoutExpired(cmd="claude", timeout=900)
        result = invoke_claude("prompt", cwd="/tmp", timeout=900)
        assert result.returncode == -1
        assert result.session_id is None
        assert "Timed out" in result.stderr

    @patch("lib.claude.subprocess.run")
    def test_not_found_returns_invoke_result(self, mock_run):
        mock_run.side_effect = FileNotFoundError()
        result = invoke_claude("prompt", cwd="/tmp")
        assert result.returncode == -2
        assert result.session_id is None

    @patch("lib.claude.subprocess.run")
    def test_nonzero_rc_still_parses_json(self, mock_run):
        """Even on rc != 0, parse JSON if available for session_id."""
        mock_run.return_value = MagicMock(
            stdout=self._make_json_output("error output", "err-sid"),
            stderr="something went wrong",
            returncode=1,
        )
        result = invoke_claude("prompt", cwd="/tmp")
        assert result.returncode == 1
        assert result.session_id == "err-sid"
        assert result.stdout == "error output"
