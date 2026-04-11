#!/usr/bin/env python3
"""Tests for InvokeResult and JSON event stream parsing in lib/claude.py."""

import json
import subprocess
from pathlib import Path
from unittest.mock import patch, MagicMock

import pytest

from lib.claude import InvokeResult, invoke_claude, _parse_json_events, _check_interface


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

    def test_no_result_event_raises(self):
        """FR-4 / H-05: events without a ``type: "result"`` entry must raise
        ValueError instead of returning an empty string (which downstream
        callers would silently write to an output file)."""
        events = [
            {"type": "system", "session_id": "sid"},
        ]
        with pytest.raises(ValueError, match="No 'result' event"):
            _parse_json_events(json.dumps(events))

    def test_invalid_json_raises(self):
        """Invalid JSON should raise ValueError."""
        try:
            _parse_json_events("not json at all")
            assert False, "Should have raised"
        except (json.JSONDecodeError, ValueError):
            pass

    def test_empty_list_raises(self):
        """FR-4 / H-05: an empty event list is structurally unusable — it has
        no result event — so it must raise ValueError, not return ``""``."""
        with pytest.raises(ValueError, match="No 'result' event"):
            _parse_json_events("[]")

    def test_result_event_with_null_raises(self):
        """A ``result`` event whose ``result`` field is JSON null is malformed,
        not missing. The error message MUST distinguish this from the "no
        result event" case so operators can tell them apart — otherwise a
        null-result bug masquerades as a protocol error."""
        events = [
            {"type": "system", "session_id": "sid"},
            {"type": "result", "result": None, "session_id": "sid"},
        ]
        with pytest.raises(ValueError, match="non-string result: NoneType"):
            _parse_json_events(json.dumps(events))

    def test_result_event_with_non_string_raises(self):
        """Same protection, but for a result that's a dict/int/etc."""
        events = [{"type": "result", "result": {"nested": "thing"}}]
        with pytest.raises(ValueError, match="non-string result: dict"):
            _parse_json_events(json.dumps(events))


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
        """Even on rc != 0, parse JSON if available for session_id.

        NOTE: The transient-retry loop exhausts all attempts when every call
        returns rc != 0, so to exercise the "parse JSON on rc=1" code path we
        need to also patch ``lib.claude.time.sleep`` to avoid real backoff.
        """
        mock_run.return_value = MagicMock(
            stdout=self._make_json_output("error output", "err-sid"),
            stderr="something went wrong",
            returncode=1,
        )
        with patch("lib.claude.time.sleep"):
            result = invoke_claude("prompt", cwd="/tmp")
        assert result.returncode == 1
        assert result.session_id == "err-sid"
        assert result.stdout == "error output"


# ---------------------------------------------------------------------------
# Transient retry (FR-2 / H-17)
# ---------------------------------------------------------------------------


class TestInvokeClaudeTransientRetry:
    """Exercise the transient-rc retry loop in isolation (unit-level).

    The integration flavor of these tests lives in
    ``test_failure_chains.py::TestIntegration_TransientRetry``. These unit
    tests pin the exact subprocess and sleep interactions so regressions in
    the delay schedule or retry conditions are obvious.
    """

    _OK_JSON = '[{"type":"system","session_id":"s"},{"type":"result","result":"ok"}]'

    def _fail(self, stderr="rate limit") -> MagicMock:
        return MagicMock(returncode=1, stdout="", stderr=stderr)

    def _ok(self) -> MagicMock:
        return MagicMock(returncode=0, stdout=self._OK_JSON, stderr="")

    def test_retries_on_transient_rc(self):
        """Two rc=1 failures followed by rc=0 success: 3 calls, 2 sleeps."""
        sleeps: list[float] = []
        calls = [self._fail(), self._fail(), self._ok()]
        with patch("lib.claude.time.sleep", side_effect=lambda s: sleeps.append(s)), \
             patch("lib.claude.subprocess.run", side_effect=calls) as run_mock:
            result = invoke_claude("prompt", cwd=Path("/tmp"))
        assert result.returncode == 0
        assert run_mock.call_count == 3
        assert sleeps == [30, 60]

    def test_exhausts_retries_and_returns_last_rc(self):
        """If all attempts fail, the final rc=1 is surfaced. No 4th call."""
        sleeps: list[float] = []
        calls = [
            self._fail("err 1"),
            self._fail("err 2"),
            self._fail("err 3"),
        ]
        with patch("lib.claude.time.sleep", side_effect=lambda s: sleeps.append(s)), \
             patch("lib.claude.subprocess.run", side_effect=calls) as run_mock:
            result = invoke_claude("prompt", cwd=Path("/tmp"))
        assert result.returncode == 1
        assert run_mock.call_count == 3
        assert sleeps == [30, 60]

    def test_does_not_retry_on_timeout(self):
        """Timeouts are deterministic — exactly one call, no sleeps."""
        with patch("lib.claude.time.sleep") as sleep_mock, \
             patch("lib.claude.subprocess.run") as run_mock:
            run_mock.side_effect = subprocess.TimeoutExpired(cmd="claude", timeout=900)
            result = invoke_claude("prompt", cwd=Path("/tmp"), timeout=900)
        assert result.returncode == -1
        assert run_mock.call_count == 1
        sleep_mock.assert_not_called()

    def test_does_not_retry_on_file_not_found(self):
        """FileNotFoundError is deterministic — exactly one call, no sleeps."""
        with patch("lib.claude.time.sleep") as sleep_mock, \
             patch("lib.claude.subprocess.run") as run_mock:
            run_mock.side_effect = FileNotFoundError()
            result = invoke_claude("prompt", cwd=Path("/tmp"))
        assert result.returncode == -2
        assert run_mock.call_count == 1
        sleep_mock.assert_not_called()

    def test_retry_warning_emitted_to_stderr(self, capsys):
        """Operator visibility: each retry emits a warn line naming the rc
        and the next delay."""
        calls = [self._fail("throttled"), self._ok()]
        with patch("lib.claude.time.sleep"), \
             patch("lib.claude.subprocess.run", side_effect=calls):
            invoke_claude("prompt", cwd=Path("/tmp"))
        captured = capsys.readouterr()
        assert "claude returned rc=1" in captured.err
        assert "retrying in 30s" in captured.err
        assert "attempt 2/3" in captured.err
        assert "throttled" in captured.err

    def test_exhaustion_warning_emitted_to_stderr(self, capsys):
        """When all attempts fail, the final failure must emit a distinct
        ``giving up`` warn line naming the attempt count, so operators see
        the exhaustion explicitly instead of having to infer it from the
        absence of a further ``retrying in`` message."""
        calls = [self._fail("err 1"), self._fail("err 2"), self._fail("err 3")]
        with patch("lib.claude.time.sleep"), \
             patch("lib.claude.subprocess.run", side_effect=calls):
            invoke_claude("prompt", cwd=Path("/tmp"))
        captured = capsys.readouterr()
        assert "giving up" in captured.err
        assert "after 3 attempts" in captured.err
        # Final stderr preview must also be attached to the giving-up line.
        assert "err 3" in captured.err


# ---------------------------------------------------------------------------
# JSON parse warning (FR-3 / H-04)
# ---------------------------------------------------------------------------


class TestJsonParseWarning:
    def test_json_parse_warning_emitted_to_stderr(self, capsys):
        """Invalid JSON stdout must trigger a warn line to stderr before
        falling back to raw stdout, so silent garbage-in/garbage-out is
        impossible to miss."""
        with patch("lib.claude.subprocess.run") as mock_run:
            mock_run.return_value = MagicMock(
                returncode=0, stdout="not valid json at all", stderr="",
            )
            result = invoke_claude("prompt", cwd=Path("/tmp"))
        captured = capsys.readouterr()
        assert "JSON event stream parse failed" in captured.err
        assert "JSONDecodeError" in captured.err
        # Fallback still succeeds with the raw stdout as the text.
        assert result.stdout == "not valid json at all"
        assert result.session_id is None

    def test_no_result_event_warning_emitted_to_stderr(self, capsys):
        """A well-formed JSON event list with no ``result`` entry must also
        surface a warning — that's the FR-4 ValueError flowing into FR-3."""
        events = [{"type": "system", "session_id": "sid"}]
        with patch("lib.claude.subprocess.run") as mock_run:
            mock_run.return_value = MagicMock(
                returncode=0, stdout=json.dumps(events), stderr="",
            )
            result = invoke_claude("prompt", cwd=Path("/tmp"))
        captured = capsys.readouterr()
        assert "JSON event stream parse failed" in captured.err
        assert "ValueError" in captured.err
        assert "No 'result' event" in captured.err
        assert result.stdout == json.dumps(events)


# ---------------------------------------------------------------------------
# Interface validation (_check_interface)
# ---------------------------------------------------------------------------


class TestCheckInterface:
    def test_conforming_costingfe_no_warnings(self, tmp_path, capsys):
        """costingfe script with 'result = ...' at module level → no warnings."""
        script = tmp_path / "model_setup.py"
        script.write_text(
            "from costingfe.model import CostModel\n"
            "model = CostModel()\n"
            "result = model.forward()\n"
        )
        _check_interface(script)
        captured = capsys.readouterr()
        assert "WARNING" not in captured.err

    def test_missing_result_warns(self, tmp_path, capsys):
        """costingfe script without module-level 'result =' → warning."""
        script = tmp_path / "model_setup.py"
        script.write_text(
            "from costingfe.model import CostModel\n"
            "model = CostModel()\n"
            "output = model.forward()\n"  # wrong name
        )
        _check_interface(script)
        captured = capsys.readouterr()
        assert "result" in captured.err.lower()

    def test_freeform_missing_results_warns(self, tmp_path, capsys):
        """Freeform script without module-level results → warning."""
        script = tmp_path / "model_setup.py"
        script.write_text(
            "# freeform script\n"
            "params = MyParams()\n"
            # no module-level results
        )
        _check_interface(script)
        captured = capsys.readouterr()
        assert "results" in captured.err

    def test_freeform_with_params_and_results_no_warnings(self, tmp_path, capsys):
        """Freeform script with module-level params and results → no warnings."""
        script = tmp_path / "model_setup.py"
        script.write_text(
            "# freeform script\n"
            "params = MyParams()\n"
            "results = params.compute()\n"
        )
        _check_interface(script)
        captured = capsys.readouterr()
        assert "WARNING" not in captured.err

    def test_indented_result_not_counted(self, tmp_path, capsys):
        """'result = ...' inside a function (indented) should still warn."""
        script = tmp_path / "model_setup.py"
        script.write_text(
            "from costingfe.model import CostModel\n"
            "model = CostModel()\n"
            "def run():\n"
            "    result = model.forward()\n"  # indented — not module-level
        )
        _check_interface(script)
        captured = capsys.readouterr()
        assert "result" in captured.err.lower()
