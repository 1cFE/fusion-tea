#!/usr/bin/env python3
"""Tests for InvokeResult and JSON event stream parsing in lib/claude.py."""

import json
import subprocess
from pathlib import Path
from unittest.mock import patch, MagicMock

import pytest

from lib.claude import (
    InvokeResult, invoke_claude, _parse_json_events, _extract_result_meta,
    _check_interface,
)


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


class TestExtractResultMeta:
    """Best-effort run accounting parsed off the result event (diagnostic)."""

    def test_extracts_cost_usage_turns(self):
        events = [
            {"type": "system", "session_id": "s"},
            {"type": "result", "result": "ok", "total_cost_usd": 12.34,
             "usage": {"input_tokens": 100, "output_tokens": 50}, "num_turns": 7},
        ]
        meta = _extract_result_meta(json.dumps(events))
        assert meta["cost_usd"] == 12.34
        assert meta["usage"] == {"input_tokens": 100, "output_tokens": 50}
        assert meta["num_turns"] == 7

    def test_absent_fields_are_none(self):
        events = [{"type": "result", "result": "ok"}]
        meta = _extract_result_meta(json.dumps(events))
        assert meta["cost_usd"] is None and meta["num_turns"] is None

    def test_malformed_stream_returns_empty_never_raises(self):
        assert _extract_result_meta("not json") == {}
        assert _extract_result_meta("[]") == {}


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


# ---------------------------------------------------------------------------
# _decide_retry_mode + invoke_claude_validated timeout-retry path.
#
# Concepts 14 and 15 of the 13-24 regen batch hit iter-1 ERROR because the
# claude subprocess timed out at 900s during cold-start analyze. The original
# retry path required a non-None session_id to send `--resume <sid>` — but
# TimeoutExpired in invoke_claude returns rc=-1 with session_id=None, so the
# retry was structurally unreachable. _decide_retry_mode now picks "fresh"
# (re-send the original prompt as a brand-new invocation) when the prior
# attempt was a timeout, recovering from the same failure mode.
# ---------------------------------------------------------------------------


_OK_JSON = '[{"type":"system","session_id":"sid-fresh"},{"type":"result","result":"ok"}]'
_OK_JSON_2 = '[{"type":"system","session_id":"sid-fresh-2"},{"type":"result","result":"ok2"}]'


def _timeout_call():
    """Mock for subprocess.run that raises TimeoutExpired (claude.py:130)."""
    return subprocess.TimeoutExpired(cmd="claude", timeout=900)


def _ok_call(json_payload: str = _OK_JSON) -> MagicMock:
    return MagicMock(returncode=0, stdout=json_payload, stderr="")


class TestDecideRetryMode:
    """Unit tests for the retry-mode decision helper."""

    def _result(self, rc: int) -> InvokeResult:
        return InvokeResult(stdout="", stderr="", returncode=rc, session_id=None)

    def test_resume_when_session_id_present(self):
        from lib.claude import _decide_retry_mode
        r = InvokeResult(stdout="", stderr="", returncode=0, session_id="sid")
        # Resume path: budget remaining, session_id present, fix message ready.
        assert _decide_retry_mode(1, 3, "sid", r) == "resume"

    def test_fresh_when_timeout_and_no_session_id(self):
        from lib.claude import _decide_retry_mode
        # The concept-14/15 case: TimeoutExpired sets rc=-1, session_id=None.
        # We must be able to retry with the original prompt as a fresh call.
        assert _decide_retry_mode(1, 3, None, self._result(-1)) == "fresh"

    def test_none_when_budget_exhausted(self):
        from lib.claude import _decide_retry_mode
        r = InvokeResult(stdout="", stderr="", returncode=0, session_id="sid")
        # attempt == total_attempts: no retries left.
        assert _decide_retry_mode(3, 3, "sid", r) is None

    def test_none_when_no_session_and_not_timeout(self):
        from lib.claude import _decide_retry_mode
        # JSON parse failure: session_id=None but rc=0. Don't retry — the
        # next attempt would just churn the same malformed stdout.
        assert _decide_retry_mode(1, 3, None, self._result(0)) is None

    def test_none_when_resume_but_no_fix_message(self):
        from lib.claude import _decide_retry_mode
        r = InvokeResult(stdout="", stderr="", returncode=0, session_id="sid")
        # session_id present but the validator couldn't articulate a fix —
        # resume-with-empty-fix would be wasteful. Don't retry.
        assert (
            _decide_retry_mode(1, 3, "sid", r, have_fix_message=False) is None
        )

    def test_fresh_even_when_resume_possible_but_no_fix(self):
        from lib.claude import _decide_retry_mode
        # If the prior attempt timed out and there's no fix message,
        # fresh is still appropriate (re-send original prompt).
        assert (
            _decide_retry_mode(
                1, 3, None, self._result(-1), have_fix_message=False
            )
            == "fresh"
        )

    def test_none_when_rc_minus_two(self):
        from lib.claude import _decide_retry_mode
        # rc=-2 is FileNotFoundError (claude CLI missing). Retrying won't
        # help; the binary isn't on PATH. Only rc=-1 (timeout) is retryable.
        assert _decide_retry_mode(1, 3, None, self._result(-2)) is None


class TestInvokeClaudeValidatedTimeoutRetry:
    """End-to-end test of the validated-invoker timeout-retry path.

    The pre-fix behavior: one TimeoutExpired and the orchestrator gave up
    (single validation_log entry, ``warn: ... no session_id — cannot
    retry``). The post-fix behavior: timeout → fresh re-invocation → if the
    fresh call writes the output file, validation passes.
    """

    def test_timeout_then_success_writes_file_on_retry(self, tmp_path, capsys):
        """The cold-start-analyze recovery path. Attempt 1 times out (no
        file). Attempt 2 is a fresh invocation that writes the file. The
        validator passes on attempt 2 and the validated result reports
        ``validation_passed=True`` with ``attempts=2``."""
        from lib.claude import invoke_claude_validated
        from lib.validators import validate_non_empty

        out_path = tmp_path / "body.md"

        # subprocess.run sequence: TimeoutExpired, then OK.
        # The OK call must also write the output file (the production
        # behavior is that the LLM writes via tool calls, but in the test
        # we simulate that side-effect on the second subprocess.run).
        call_count = {"n": 0}

        def fake_run(*args, **kwargs):
            call_count["n"] += 1
            if call_count["n"] == 1:
                raise _timeout_call()
            # Second invocation: simulate the LLM writing the body file.
            out_path.write_text("# analysis body\n\ncontent here", encoding="utf-8")
            return _ok_call(_OK_JSON_2)

        with patch("lib.claude.subprocess.run", side_effect=fake_run):
            log_file = tmp_path / "validation_log.json"
            result = invoke_claude_validated(
                "the original prompt",
                cwd=tmp_path,
                timeout=900,
                validator=validate_non_empty,
                output_path=out_path,
                step_label="cold-start",
                log_path=log_file,
            )

        assert result.validation_passed
        assert result.attempts == 2
        # The fresh retry adopted the second invocation's session_id.
        assert result.invoke.session_id == "sid-fresh-2"

        # Validation log records: (1) timeout, (2) success — and the timeout
        # entry carries the new ``retry_reason`` marker so operators can
        # grep the regen logs for this recovery path.
        log = json.loads(log_file.read_text(encoding="utf-8"))
        assert len(log) == 2
        assert log[0]["passed"] is False
        assert log[0]["details"].startswith("Output file not found")
        assert "retry_reason" in log[0]
        assert "timeout" in log[0]["retry_reason"]
        assert "fresh invocation" in log[0]["retry_reason"]
        assert log[1]["passed"] is True

    def test_three_timeouts_exhausts_budget(self, tmp_path, capsys):
        """Three timeouts in a row exhaust the default retry budget
        (max_retries=2 → 3 total attempts). The result reports
        ``validation_passed=False`` and the log captures all three
        attempts, each tagged with ``retry_reason: timeout``."""
        from lib.claude import invoke_claude_validated
        from lib.validators import validate_non_empty

        out_path = tmp_path / "body.md"
        log_file = tmp_path / "validation_log.json"

        with patch(
            "lib.claude.subprocess.run",
            side_effect=[_timeout_call(), _timeout_call(), _timeout_call()],
        ) as run_mock:
            result = invoke_claude_validated(
                "the original prompt",
                cwd=tmp_path,
                timeout=900,
                validator=validate_non_empty,
                output_path=out_path,
                step_label="cold-start",
                log_path=log_file,
            )

        assert not result.validation_passed
        # Three subprocess.run calls — one initial + two fresh retries.
        assert run_mock.call_count == 3
        log = json.loads(log_file.read_text(encoding="utf-8"))
        assert len(log) == 3
        # First two entries should announce a fresh retry (budget remaining);
        # the final entry should not (terminal).
        assert "retry_reason" in log[0]
        assert "retry_reason" in log[1]
        assert "retry_reason" not in log[2]

    def test_pre_fix_failure_mode_now_recovers(self, tmp_path):
        """Regression test pinned to the concept-14/15 failure mode.

        Pre-fix: a single TimeoutExpired in attempt 1 left
        ``validation_log.json`` with one entry, ``warn: ... no session_id —
        cannot retry`` on stderr, and ``validation_passed=False``. Post-fix:
        the same first-attempt timeout triggers a fresh retry that succeeds,
        and the recovery is auditable in the log."""
        from lib.claude import invoke_claude_validated
        from lib.validators import validate_non_empty

        out_path = tmp_path / "analysis_body.md"
        log_file = tmp_path / "validation_log.json"
        sequence = [_timeout_call(), _ok_call()]

        def fake_run(*args, **kwargs):
            event = sequence.pop(0)
            if isinstance(event, BaseException):
                raise event
            # Simulate the LLM's tool-write on the successful retry.
            out_path.write_text(
                "# Design Point\nrecovered after timeout", encoding="utf-8",
            )
            return event

        with patch("lib.claude.subprocess.run", side_effect=fake_run):
            r = invoke_claude_validated(
                "cold-start prompt",
                cwd=tmp_path,
                timeout=900,
                validator=validate_non_empty,
                output_path=out_path,
                step_label="cold-start",
                log_path=log_file,
            )

        assert r.validation_passed
        # Output file is what the validator read; round-trip confirms it.
        assert "recovered after timeout" in out_path.read_text(encoding="utf-8")
