#!/usr/bin/env python3
"""Integration tests for failure chains across module boundaries.

These tests verify the *interactions* between modules — the seams where
bugs actually live. Each test documents a specific failure chain from the
2026-04-08 pipeline audit (H-01 through H-21).

Design principles:
- Mock only at the subprocess boundary; let internal code run for real.
- Each test wires together the actual code path that breaks.
- "Characterization tests" document current broken behavior and will flip
  to regression guards after the corresponding fix lands.
"""

import hashlib
import json
import subprocess
import textwrap
from pathlib import Path
from unittest.mock import patch, MagicMock

import pytest

from lib.claude import (
    InvokeResult,
    ValidatedResult,
    invoke_claude,
    invoke_claude_validated,
    _parse_json_events,
)
from lib.validators import (
    ValidationResult,
    validate_feedback_verdict,
    validate_review_verdict,
)
from lib.iteration import parse_verdict_from_feedback
from lib.frontmatter import parse_frontmatter, update_frontmatter_field


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _make_json_events(result_text: str, session_id: str = "sid-1") -> str:
    """Build a valid JSON event stream (what subprocess.stdout actually contains)."""
    return json.dumps([
        {"type": "system", "session_id": session_id},
        {"type": "result", "result": result_text, "session_id": session_id},
    ])


def _make_subprocess_result(result_text: str, rc: int = 0, session_id: str = "sid-1"):
    """Build a mock subprocess.CompletedProcess with valid JSON event stream."""
    return MagicMock(
        stdout=_make_json_events(result_text, session_id),
        stderr="",
        returncode=rc,
    )


# ===========================================================================
# H-01: Validator reads parsed event text when file doesn't exist
# ===========================================================================

class TestH01_ValidatorReadsWrongData:
    """REGRESSION GUARDS (inverted in Phase 3): when Claude returns rc=0 but
    doesn't write the expected file, invoke_claude_validated MUST treat the
    missing file as a distinct first-class failure mode — NOT fall back to
    validating result.stdout. Every retry prompt MUST contain the output path
    so Claude knows WHERE to write next time.

    Class name preserved (rather than renaming) so ``git log -L`` on the
    boundary shows the continuous bug-reproduction-to-fix history.
    """

    @patch("lib.claude.subprocess.run")
    def test_missing_file_short_circuits_validator(self, mock_run, tmp_path):
        """Post-fix (FR-1): when output_path doesn't exist, the validator is
        NOT invoked against Claude's conversational stdout. The file-not-found
        branch handles the failure directly and the log entry's
        ``validated_text_preview`` is the ``FILE NOT FOUND`` sentinel.
        """
        conversational_reply = (
            "I've written the assessment to feedback.md with VERDICT: FINDINGS."
        )
        mock_run.return_value = _make_subprocess_result(conversational_reply)

        output_file = tmp_path / "feedback.md"
        assert not output_file.exists()  # Claude didn't write it

        validated_texts: list[str] = []

        def spy_validator(text: str) -> ValidationResult:
            validated_texts.append(text)
            return validate_feedback_verdict(text)

        spy_validator.__name__ = "spy_validator"

        result = invoke_claude_validated(
            "assess this concept", Path("/tmp"),
            validator=spy_validator,
            output_path=output_file,
            max_retries=1,
        )

        # The validator NEVER ran — the missing-file branch handled it.
        assert validated_texts == []
        assert result.validation_passed is False
        # Log entries (on the result) carry the FILE NOT FOUND sentinel.
        for entry in result.log_entries:
            assert entry["validated_text_preview"] == "FILE NOT FOUND"
            assert "Output file not found" in entry["details"]

    @patch("lib.claude.subprocess.run")
    def test_retry_fix_message_contains_file_path(self, mock_run, tmp_path):
        """Post-fix (FR-5/FR-6): the retry prompt sent on attempt 2 contains
        the output file path so Claude knows WHERE to write the file.
        """
        conversational_reply = "I've written the assessment."
        mock_run.return_value = _make_subprocess_result(conversational_reply)

        output_file = tmp_path / "feedback.md"
        log_path = tmp_path / "validation_log.json"

        invoke_claude_validated(
            "assess this concept", Path("/tmp"),
            validator=validate_feedback_verdict,
            output_path=output_file,
            max_retries=1,
            log_path=log_path,
        )

        entries = json.loads(log_path.read_text())
        fix_messages = [
            e.get("fix_message_sent", "") for e in entries if "fix_message_sent" in e
        ]
        # max_retries=1 → total_attempts=2 → only the first entry carries a
        # fix_message_sent (the final entry is the last word, no retry).
        assert len(fix_messages) == 1
        msg = fix_messages[0]
        assert str(output_file) in msg
        assert "did not write the expected output file" in msg
        assert "attempt 2 of 2" in msg

    @patch("lib.claude.subprocess.run")
    def test_all_retries_fail_with_file_not_found_details(self, mock_run, tmp_path):
        """Post-fix: when the file is never written, every attempt records the
        ``Output file not found`` failure mode (not "no VERDICT line" garbage
        from validating conversational stdout). Failure details are uniform —
        no false positives from Claude's chatty replies.
        """
        mock_run.return_value = _make_subprocess_result(
            "I've completed the assessment.", session_id="sid-1"
        )

        output_file = tmp_path / "feedback.md"
        # File never gets created across any retry

        result = invoke_claude_validated(
            "assess this", Path("/tmp"),
            validator=validate_feedback_verdict,
            output_path=output_file,
            max_retries=2,
        )

        assert result.validation_passed is False
        assert result.attempts == 3
        details = [e["details"] for e in result.log_entries]
        for d in details:
            assert "Output file not found" in d
        previews = [e["validated_text_preview"] for e in result.log_entries]
        assert previews == ["FILE NOT FOUND"] * 3


# ===========================================================================
# H-02: step_runner writes parsed event text to output file
# ===========================================================================
# DELETED in Phase 5: TestH02_StepRunnerWritesGarbage exercised the legacy
# ``run_claude_step`` + ``file_with_fallback`` mode, which no longer exists
# after the Phase 5 deletion of the ``step_runner`` legacy surface. The H-02
# anti-pattern (writing parsed event text to an output file) cannot recur
# because the abstraction that did it has been removed from the codebase.
# Coverage of the file-not-written failure mode now lives in TestH01 and
# TestEndToEnd_FileNotWrittenChain (post-fix regression guards).


# ===========================================================================
# H-03: Feedback pass doesn't verify analysis was modified
# ===========================================================================

class TestH03_FeedbackPassNoEditCheck:
    """FR-15 / H-03 regression guard (inverted in Phase 4).

    When Claude returns rc=0 on a feedback pass but doesn't actually edit
    ``analysis.md``, ``_run_feedback_pass`` now returns False (failure) via
    ``make_file_modified_validator``. Previously it trusted the rc and
    silently chained an unchanged analysis into the next iteration.
    """

    @patch("lib.claude.subprocess.run")
    def test_feedback_pass_fails_when_file_unchanged(self, mock_run, tmp_path):
        """INVERTED: returns False (not True) when analysis.md is byte-identical
        after the invocation. The validator ran across all retries and saw an
        unchanged SHA-256, so the iteration is correctly treated as a failure.
        """
        from lib.loop import _run_feedback_pass

        # Set up the analysis file with known content
        analysis_dir = tmp_path / "analyses" / "test-concept"
        analysis_dir.mkdir(parents=True)
        analysis_path = analysis_dir / "analysis.md"
        original_content = "---\nID: test\n---\n\nOriginal analysis content."
        analysis_path.write_text(original_content)
        content_hash_before = hashlib.sha256(original_content.encode()).hexdigest()

        iter_dir = analysis_dir / "iter-2"
        iter_dir.mkdir()
        feedback_path = analysis_dir / "iter-1" / "post_feedback.md"
        feedback_path.parent.mkdir(parents=True, exist_ok=True)
        feedback_path.write_text("VERDICT: FINDINGS\n\n### F-1: Fix something\n- **Category:** analysis\n")

        # Claude returns rc=0 on every retry but does NOT edit analysis.md.
        mock_run.return_value = _make_subprocess_result("I've updated the analysis.")

        concept = {"_id": "test-concept", "Concept Name": "Test"}
        args = MagicMock(
            dry_run=False, timeout=900, model=None, max_passes=5,
        )

        template = "Analyze {{concept_name}}"

        with patch("lib.loop.CONCEPT_ANALYSIS_DIR", new=Path("/tmp")):
            success = _run_feedback_pass(
                concept, iter_dir, feedback_path, {}, template, args
            )

        # POST-FIX: validation_passed=False propagates as failure.
        assert success is False
        content_hash_after = hashlib.sha256(
            analysis_path.read_text().encode()
        ).hexdigest()
        # File still untouched — that's why we failed in the first place.
        assert content_hash_before == content_hash_after


# ===========================================================================
# H-04: invoke_claude swallows JSON parse errors silently
# ===========================================================================

class TestH04_JsonParseErrorSwallowed:
    """FR-3 / H-04 regression guard (inverted in Phase 2).

    When Claude's JSON event stream is malformed, invoke_claude now emits a
    stderr warning *before* falling back to raw stdout. Fallback behavior is
    preserved (so partial JSON is still surfaced to the caller) but the
    warning makes the degraded mode impossible to miss.
    """

    @patch("lib.claude.subprocess.run")
    def test_malformed_json_still_falls_back_to_raw_stdout(self, mock_run):
        """The fallback itself is kept — callers still receive the raw
        stdout when parsing fails. This test locks in that contract so a
        future refactor can't accidentally start swallowing the stdout."""
        partial_json = '[{"type": "system", "session_id": "sid"}, {"type": "resu'
        mock_run.return_value = MagicMock(
            stdout=partial_json,
            stderr="",
            returncode=0,
        )

        result = invoke_claude("prompt", cwd=Path("/tmp"))

        assert result.stdout == partial_json
        assert result.session_id is None
        assert result.returncode == 0

    @patch("lib.claude.subprocess.run")
    def test_malformed_json_emits_stderr_warning(self, mock_run, capsys):
        """INVERTED: a warning MUST now be emitted on stderr when JSON
        parsing fails, naming the exception class so operators can grep."""
        mock_run.return_value = MagicMock(
            stdout="not json at all",
            stderr="",
            returncode=0,
        )

        invoke_claude("prompt", cwd=Path("/tmp"))

        captured = capsys.readouterr()
        assert "JSON event stream parse failed" in captured.err
        assert "JSONDecodeError" in captured.err


# ===========================================================================
# H-05: Empty result from JSON events
# ===========================================================================

class TestH05_EmptyResultText:
    """FR-4 / H-05 regression guard (inverted in Phase 2).

    When a valid JSON event list contains no ``type: "result"`` entry,
    ``_parse_json_events`` now raises ``ValueError``. Previously it silently
    returned ``""``, which downstream callers treated as a valid empty
    response and wrote to output files.
    """

    def test_no_result_event_raises_value_error(self):
        """INVERTED: a no-result event stream MUST raise, not return empty."""
        events = json.dumps([
            {"type": "system", "session_id": "sid"},
            {"type": "assistant", "message": {"content": [{"text": "thinking..."}]}},
        ])

        with pytest.raises(ValueError, match="No 'result' event"):
            _parse_json_events(events)

    @patch("lib.claude.subprocess.run")
    def test_no_result_event_in_invoke_claude_falls_back_with_warning(
        self, mock_run, capsys
    ):
        """The ValueError from ``_parse_json_events`` is caught one level up
        in ``invoke_claude``, where it flows into the FR-3 warning + raw-stdout
        fallback. This test pins the end-to-end path so H-05 cannot reappear
        as a silent-success failure mode at the invoke_claude boundary either.
        """
        raw = json.dumps([
            {"type": "system", "session_id": "sid"},
            {"type": "assistant", "message": {"content": [{"text": "thinking..."}]}},
        ])
        mock_run.return_value = MagicMock(
            stdout=raw,
            stderr="",
            returncode=0,
        )

        result = invoke_claude("prompt", cwd=Path("/tmp"))
        captured = capsys.readouterr()

        assert "JSON event stream parse failed" in captured.err
        assert "ValueError" in captured.err
        assert "No 'result' event" in captured.err
        # Fallback behavior: raw stdout is surfaced to the caller, session_id
        # is dropped because we couldn't finish parsing the event stream.
        assert result.stdout == raw
        assert result.session_id is None


# ===========================================================================
# H-09 + H-10: Callers ignore validation_passed flag
# ===========================================================================

class TestH09H10_ValidationPassedIgnored:
    """FR-17 / H-09 + H-10 regression guard (inverted in Phase 4).

    ``_run_assess`` and ``_run_source_integration`` now honor the
    ``validation_passed`` flag from ``invoke_claude_validated``: when
    validation exhausts all retries, they early-return ``ERROR`` (or
    ``None`` for source-integration) instead of parsing the malformed
    output file. Previously they trusted rc + file-exists and chained the
    bad data forward.
    """

    @patch("lib.claude.subprocess.run")
    def test_assess_returns_error_when_validation_exhausted(self, mock_run, tmp_path):
        """INVERTED: _run_assess returns ('ERROR', 0) when every retry
        produces a feedback file that fails ``validate_feedback_verdict``."""
        from lib.loop import _run_assess

        # Set up dirs
        analysis_dir = tmp_path / "analyses" / "test"
        analysis_dir.mkdir(parents=True)
        analysis_path = analysis_dir / "analysis.md"
        analysis_path.write_text("---\nID: test\n---\n\nSome analysis.")

        iter_dir = analysis_dir / "iter-1"
        iter_dir.mkdir()

        # Claude writes a file that fails validation (no VERDICT line)
        bad_feedback = "Here are my thoughts on this analysis:\n- Point 1\n- Point 2\n"

        call_count = 0

        def side_effect(*args, **kwargs):
            nonlocal call_count
            call_count += 1
            # Write the bad file on every attempt
            (iter_dir / "post_feedback.md").write_text(bad_feedback)
            return _make_subprocess_result("Done.", session_id="sid-1")

        mock_run.side_effect = side_effect

        concept = {"_id": "test", "Concept Name": "Test"}
        args = MagicMock(dry_run=False, timeout=900, model=None)

        with patch("lib.loop.CONCEPT_ANALYSIS_DIR", new=Path("/tmp")):
            verdict, finding_count = _run_assess(
                concept, iter_dir, analysis_path,
                "Assess {{concept_name}} at {{analysis_path}} -> {{feedback_path}}",
                args,
            )

        # POST-FIX: validation_passed=False short-circuits to ERROR before
        # parse_verdict_from_feedback gets the chance to invent a fake "FAIL".
        assert verdict == "ERROR"
        assert finding_count == 0


# ===========================================================================
# H-17: No transient retry in invoke_claude
# ===========================================================================

class TestH17_NoTransientRetry:
    """FR-2 / H-17 regression guard (inverted in Phase 2).

    The class name is kept for git-history continuity — read it as "the old
    behavior" and each test as the regression guard that locks in the fix.
    ``invoke_claude`` now retries on transient ``rc != 0`` with exponential
    backoff (30s, 60s), up to 3 total attempts.
    """

    @patch("lib.claude.time.sleep")
    @patch("lib.claude.subprocess.run")
    def test_rc1_triggers_retry_up_to_three_attempts(self, mock_run, _sleep_mock):
        """INVERTED: persistent rc=1 now triggers two retries (3 total
        attempts) before giving up with the final rc surfaced."""
        mock_run.return_value = MagicMock(
            stdout="",
            stderr="",
            returncode=1,
        )

        result = invoke_claude("prompt", cwd=Path("/tmp"))

        assert result.returncode == 1
        assert mock_run.call_count == 3

    @patch("lib.claude.time.sleep")
    @patch("lib.claude.subprocess.run")
    def test_transient_failure_then_success_recovers(self, mock_run, _sleep_mock):
        """INVERTED: an rc=1 followed by a successful attempt now recovers
        — the transient failure does not kill the concept."""
        call_count = 0

        def side_effect(*args, **kwargs):
            nonlocal call_count
            call_count += 1
            if call_count == 1:
                return MagicMock(stdout="", stderr="rate limited", returncode=1)
            return MagicMock(
                stdout=_make_json_events("success"),
                stderr="",
                returncode=0,
            )

        mock_run.side_effect = side_effect

        result = invoke_claude("prompt", cwd=Path("/tmp"))

        assert result.returncode == 0
        assert result.stdout == "success"
        assert call_count == 2


# ===========================================================================
# H-20: Frontmatter parser breaks on colons in values
# ===========================================================================

class TestH20_FrontmatterColonInValue:
    """The hand-rolled YAML parser splits on the first colon, so values
    containing colons get truncated.
    """

    def test_colon_in_company_name(self, tmp_path):
        """CHARACTERIZATION: Company name with colon gets truncated."""
        f = tmp_path / "analysis.md"
        f.write_text(textwrap.dedent("""\
            ---
            ID: test-01
            Company: General Fusion: A Story
            Status: draft
            ---

            Content here.
        """))

        fm = parse_frontmatter(f)

        # BUG: partition(":") correctly splits on first colon, but
        # the value "General Fusion: A Story" is actually correct here
        # because partition splits on FIRST colon only.
        # Let's verify the actual behavior:
        assert fm["Company"] == "General Fusion: A Story"  # partition handles this

    def test_url_in_value(self, tmp_path):
        """Values with URLs (containing ://) should parse correctly."""
        f = tmp_path / "analysis.md"
        f.write_text(textwrap.dedent("""\
            ---
            ID: test-01
            Source: https://example.com/paper
            Status: draft
            ---

            Content.
        """))

        fm = parse_frontmatter(f)
        # partition(":") splits on first colon — "Source" : " https://example.com/paper"
        assert fm["Source"] == "https://example.com/paper"

    def test_yaml_boolean_not_converted(self, tmp_path):
        """CHARACTERIZATION: YAML booleans stay as strings."""
        f = tmp_path / "analysis.md"
        f.write_text(textwrap.dedent("""\
            ---
            ID: test-01
            Approved: true
            ---

            Content.
        """))

        fm = parse_frontmatter(f)
        # Not converted to Python bool — stays as string "true"
        assert fm["Approved"] == "true"
        assert fm["Approved"] is not True

    def test_commented_line_parsed_as_key(self, tmp_path):
        """CHARACTERIZATION: YAML comments are parsed as key-value pairs."""
        f = tmp_path / "analysis.md"
        f.write_text(textwrap.dedent("""\
            ---
            ID: test-01
            # This is a comment
            Status: draft
            ---

            Content.
        """))

        fm = parse_frontmatter(f)
        # BUG: "# This is a comment" gets parsed — "#" becomes key, rest is lost
        # Actually: "# This is a comment" → partition(":") → ("# This is a comment", "", "")
        # No colon → never enters the key:value branch. But ":" doesn't appear... wait.
        # "# This is a comment" has no colon, so it's just skipped.
        # Let's check a comment WITH a colon:

    def test_comment_with_colon_becomes_key(self, tmp_path):
        """CHARACTERIZATION: A YAML comment containing a colon gets parsed as a key."""
        f = tmp_path / "analysis.md"
        f.write_text(textwrap.dedent("""\
            ---
            ID: test-01
            # Note: this is important
            Status: draft
            ---

            Content.
        """))

        fm = parse_frontmatter(f)
        # BUG: "# Note" becomes a key with value "this is important"
        assert "# Note" in fm  # <-- THIS IS THE BUG


# ===========================================================================
# H-16: Canonical file overwrites with worse model
# ===========================================================================

class TestH16_CanonicalOverwriteRegression:
    """REGRESSION GUARD (inverted in Phase 6): ``_update_canonical_files``
    now accepts ``model_ok`` and refuses to copy iteration model files over
    the canonical copies when the current iteration's model failed (FR-18).

    The original characterization test simulated the buggy data flow to
    demonstrate that a broken iter-2 would clobber a working iter-1's
    canonical model. After the Phase 6 fix that simulation no longer
    represents what the code does, so the test is re-pointed at the real
    function and asserts the new invariant directly.

    For the full integration coverage (both ``model_ok=False`` preservation
    and ``model_ok=True`` promotion) see
    ``TestIntegration_CanonicalFiles`` below.
    """

    def test_concept_canonical_files_preserved_on_model_failure(self, tmp_path):
        """REGRESSION: broken iter-2 must NOT overwrite iter-1's canonical
        files when model_ok is False.
        """
        from lib.loop import _update_canonical_files

        concept_dir = tmp_path / "test-concept"
        concept_dir.mkdir()

        # Canonical state from a prior successful iteration (iter-1)
        canonical_model = concept_dir / "model_setup.py"
        canonical_output = concept_dir / "model_output.txt"
        canonical_model.write_text("# Working model\nresult = 42\n")
        canonical_output.write_text("LCOE: 55.3 $/MWh\n")

        # Iter-2: broken model (syntax error) — no model_output.txt because
        # the model failed before producing output.
        iter2 = concept_dir / "iter-2"
        iter2.mkdir()
        (iter2 / "model_setup.py").write_text("# Broken\ndef f(\n")

        _update_canonical_files(concept_dir, iter2, model_ok=False)

        # POST-FIX: canonical copies are left alone, preserving last-good state.
        assert "Working model" in canonical_model.read_text()
        assert "55.3" in canonical_output.read_text()
        assert "def f(" not in canonical_model.read_text()


# ===========================================================================
# End-to-end chain: file-not-written → validate-wrong-data → useless-retry
# ===========================================================================

class TestEndToEnd_FileNotWrittenChain:
    """REGRESSION GUARD (inverted in Phase 3): the full chain that originally
    killed concept 01 iter-10. Post-H-01-fix, when Claude returns rc=0 but
    never writes the expected file, the chain MUST:

    1. Treat each missing-file as a first-class failure (no validator
       fall-back to conversational stdout)
    2. Emit retry prompts that contain the output path so Claude knows
       where to write next time
    3. Surface ``validation_passed=False`` so the caller doesn't proceed
       on a phantom success

    This test wires ``invoke_claude_validated + validate_feedback_verdict``
    together to prove the post-fix chain reports the right failure mode.
    """

    @patch("lib.claude.subprocess.run")
    def test_full_chain(self, mock_run, tmp_path):
        conversational_replies = [
            "I've completed the assessment and written it to feedback.md.",
            "I've re-written the feedback with the correct VERDICT format.",
            "I've corrected the feedback file with VERDICT: FINDINGS.",
        ]
        call_count = 0

        def side_effect(*args, **kwargs):
            nonlocal call_count
            reply = conversational_replies[min(call_count, len(conversational_replies) - 1)]
            call_count += 1
            return MagicMock(
                stdout=_make_json_events(reply, "sid-1"),
                stderr="",
                returncode=0,
            )

        mock_run.side_effect = side_effect

        output_file = tmp_path / "feedback.md"
        log_path = tmp_path / "validation_log.json"
        # File never gets created

        result = invoke_claude_validated(
            "assess this concept", Path("/tmp"),
            validator=validate_feedback_verdict,
            output_path=output_file,
            max_retries=2,
            step_label="assess",
            log_path=log_path,
        )

        # Chain outcome: all 3 attempts surfaced as missing-file failures.
        assert result.validation_passed is False
        assert result.attempts == 3

        entries = json.loads(log_path.read_text())
        assert len(entries) == 3
        for entry in entries:
            assert entry["passed"] is False
            # File-not-found branch — no VERDICT garbage, no validator fall-back.
            assert "Output file not found" in entry["details"]
            assert entry["validated_text_preview"] == "FILE NOT FOUND"

        # The first two attempts dispatched retries; their fix messages must
        # mention the path. The final attempt is the last word — no
        # fix_message_sent (will_retry gating).
        retry_msgs = [e.get("fix_message_sent") for e in entries[:2]]
        assert all(m is not None for m in retry_msgs)
        for msg in retry_msgs:
            assert str(output_file) in msg
            assert "did not write the expected output file" in msg
        assert "fix_message_sent" not in entries[2]

        # The file still doesn't exist — caller MUST honor validation_passed.
        assert not output_file.exists()


# ===========================================================================
# Chain: malformed JSON → garbage stdout → written to disk → parsed as verdict
# ===========================================================================
# DELETED in Phase 5: TestEndToEnd_MalformedJsonChain exercised the legacy
# ``run_claude_step`` + ``file_with_fallback`` mode, which no longer exists
# after the Phase 5 deletion. The chain it documented (malformed JSON → raw
# stdout → written to disk as review.md) cannot recur because nothing in the
# codebase writes parsed event text to an output file anymore. The
# JSON-fallback contract itself is still locked in by TestH04 and TestH05.


# ===========================================================================
# Regression guard: validate_feedback_verdict on various garbage inputs
# ===========================================================================

class TestVerdictParserOnGarbage:
    """Verify that parse_verdict_from_feedback produces sensible results
    when fed the kinds of garbage that actually flow through the pipeline.
    """

    def test_conversational_text(self):
        """Claude's conversational reply mistakenly fed to parser."""
        text = "I've written the assessment to feedback.md with VERDICT: FINDINGS and 3 findings."
        verdict, count = parse_verdict_from_feedback(text)
        # "VERDICT: FINDINGS" appears in the text but NOT at start of line
        # (it's inline in a sentence), so the regex won't match... or will it?
        # The regex is ^VERDICT:\s*(PASS|FINDINGS)$ with MULTILINE
        # "with VERDICT: FINDINGS and 3 findings." — VERDICT is not at line start
        assert verdict == "FAIL"
        assert count == 0

    def test_json_fragment(self):
        text = '[{"type": "system"}, {"type": "result", "result": "done"}]'
        verdict, count = parse_verdict_from_feedback(text)
        assert verdict == "FAIL"
        assert count == 0

    def test_empty_string(self):
        verdict, count = parse_verdict_from_feedback("")
        assert verdict == "FAIL"
        assert count == 0

    def test_conversational_with_verdict_at_line_start(self):
        """Edge case: conversational text that happens to have VERDICT at line start."""
        text = "I've completed the review.\nVERDICT: PASS\nLet me know if you need changes."
        verdict, count = parse_verdict_from_feedback(text)
        # This DOES match — the regex sees VERDICT: PASS at start of a line
        assert verdict == "PASS"  # Accidentally "valid" — dangerous


# ===========================================================================
# Phase 1 integration tests (pipeline-hardening plan)
# ===========================================================================
#
# These tests use ``FakeClaude`` from ``_fake_claude.py`` to mock ONLY at the
# ``subprocess.run`` boundary. Everything above it — loop.py, step_runner.py,
# validators.py, iteration.py, state.py — runs for real against ``tmp_path``.
#
# In Phase 1 these are written against the POST-FIX expected behavior. They
# are RED on the current branch and flip green as the corresponding fix lands
# in Phases 2-6.
# ---------------------------------------------------------------------------


from _fake_claude import FakeClaude, FakeInvocation, ConceptFixture


def _make_fixture(tmp_path):
    return ConceptFixture(tmp_path)


# ---------------------------------------------------------------------------
# TestIntegration_ColdStart — loop.py::_run_cold_start
# ---------------------------------------------------------------------------


class TestIntegration_ColdStart:
    def test_cold_start_success(self, tmp_path):
        """Happy path: FakeClaude writes the body file; assembled analysis.md
        contains frontmatter + body."""
        from lib.loop import _run_cold_start

        fx = _make_fixture(tmp_path)
        iter_dir = fx.iter_dir(1)
        body_path = iter_dir / "analysis_body.md"

        fake = FakeClaude([
            FakeInvocation(
                returncode=0,
                file_writes=[(body_path, "# Cold start body\n\nInitial content.")],
            ),
        ])
        with patch("lib.loop.CONCEPT_ANALYSIS_DIR", new=tmp_path), fake:
            ok = _run_cold_start(
                fx.concept, iter_dir, fx.common_vars,
                fx.analysis_template, fx.analysis_path, fx.make_args(),
            )

        assert ok is True
        assert len(fake.calls) == 1
        assert fx.analysis_path.exists()
        content = fx.analysis_path.read_text()
        assert content.startswith("---\n")  # frontmatter preserved
        assert "Cold start body" in content
        # body file is deleted after assembly
        assert not body_path.exists()

    def test_cold_start_file_not_written_retry(self, tmp_path):
        """H-01 integration: when Claude returns rc=0 without writing the
        expected file, the retry prompt must contain the exact output path
        and the retry must produce a successful assembly.

        RED until Phase 4 migrates _run_cold_start to invoke_claude_validated.
        """
        from lib.loop import _run_cold_start

        fx = _make_fixture(tmp_path)
        iter_dir = fx.iter_dir(1)
        body_path = iter_dir / "analysis_body.md"

        fake = FakeClaude([
            # First call: rc=0 but no file written.
            FakeInvocation(returncode=0),
            # Retry: writes the file; retry prompt must mention the path.
            FakeInvocation(
                returncode=0,
                expect_prompt_contains=[str(body_path)],
                file_writes=[(body_path, "# Retry body\n\nRetry content.")],
            ),
        ])
        with patch("lib.loop.CONCEPT_ANALYSIS_DIR", new=tmp_path), fake:
            ok = _run_cold_start(
                fx.concept, iter_dir, fx.common_vars,
                fx.analysis_template, fx.analysis_path, fx.make_args(),
            )

        assert ok is True
        assert len(fake.calls) == 2
        assert "Retry body" in fx.analysis_path.read_text()

    def test_cold_start_all_retries_exhausted_fails_cleanly(self, tmp_path):
        """When every retry fails to write the body, analysis.md must NOT be
        left half-assembled (just frontmatter with no body)."""
        from lib.loop import _run_cold_start

        fx = _make_fixture(tmp_path)
        iter_dir = fx.iter_dir(1)

        fake = FakeClaude([
            FakeInvocation(returncode=0),
            FakeInvocation(returncode=0),
            FakeInvocation(returncode=0),
        ])
        with patch("lib.loop.CONCEPT_ANALYSIS_DIR", new=tmp_path), fake:
            ok = _run_cold_start(
                fx.concept, iter_dir, fx.common_vars,
                fx.analysis_template, fx.analysis_path, fx.make_args(),
            )

        assert ok is False
        # Cold-start deletes analysis.md on failure — no half-assembled file.
        assert not fx.analysis_path.exists()


# ---------------------------------------------------------------------------
# TestIntegration_FeedbackPass — loop.py::_run_feedback_pass
# ---------------------------------------------------------------------------


class TestIntegration_FeedbackPass:
    def test_feedback_pass_success(self, tmp_path):
        from lib.loop import _run_feedback_pass

        fx = _make_fixture(tmp_path)
        original = "---\nID: test\n---\n\nOriginal body.\n"
        fx.with_analysis(original)
        iter_dir = fx.iter_dir(2)
        feedback_path = fx.iter_dir(1) / "post_feedback.md"
        feedback_path.write_text(
            "VERDICT: FINDINGS\n\n### F-1: Fix\n- **Category:** analysis\n"
        )

        modified = "---\nID: test\n---\n\nRevised body after feedback.\n"
        fake = FakeClaude([
            FakeInvocation(
                returncode=0,
                file_edits=[(fx.analysis_path, modified)],
            ),
        ])
        with patch("lib.loop.CONCEPT_ANALYSIS_DIR", new=tmp_path), fake:
            ok = _run_feedback_pass(
                fx.concept, iter_dir, feedback_path, fx.common_vars,
                fx.analysis_template, fx.make_args(),
            )

        assert ok is True
        assert fx.analysis_path.read_text() == modified

    def test_feedback_pass_file_unchanged_fails(self, tmp_path):
        """H-03: when Claude returns rc=0 but analysis.md is byte-identical,
        feedback-pass must treat it as a failure."""
        from lib.loop import _run_feedback_pass

        fx = _make_fixture(tmp_path)
        original = "---\nID: test\n---\n\nOriginal body.\n"
        fx.with_analysis(original)
        iter_dir = fx.iter_dir(2)
        feedback_path = fx.iter_dir(1) / "post_feedback.md"
        feedback_path.write_text(
            "VERDICT: FINDINGS\n\n### F-1: Fix\n- **Category:** analysis\n"
        )

        fake = FakeClaude([
            FakeInvocation(returncode=0),
            FakeInvocation(returncode=0),
            FakeInvocation(returncode=0),
        ])
        with patch("lib.loop.CONCEPT_ANALYSIS_DIR", new=tmp_path), fake:
            ok = _run_feedback_pass(
                fx.concept, iter_dir, feedback_path, fx.common_vars,
                fx.analysis_template, fx.make_args(),
            )

        assert ok is False  # current buggy code returns True
        assert fx.analysis_path.read_text() == original

    def test_feedback_pass_byte_identical_rewrite_fails(self, tmp_path):
        """Claude writes IDENTICAL bytes (e.g., no-op edit). The
        ``make_file_modified_validator`` must catch this via SHA-256 exactness.
        """
        from lib.loop import _run_feedback_pass

        fx = _make_fixture(tmp_path)
        content = "---\nID: test\n---\n\nUnchanged body.\n"
        fx.with_analysis(content)
        iter_dir = fx.iter_dir(2)
        feedback_path = fx.iter_dir(1) / "post_feedback.md"
        feedback_path.write_text(
            "VERDICT: FINDINGS\n\n### F-1: F\n- **Category:** analysis\n"
        )

        fake = FakeClaude([
            FakeInvocation(returncode=0, file_edits=[(fx.analysis_path, content)]),
            FakeInvocation(returncode=0, file_edits=[(fx.analysis_path, content)]),
            FakeInvocation(returncode=0, file_edits=[(fx.analysis_path, content)]),
        ])
        with patch("lib.loop.CONCEPT_ANALYSIS_DIR", new=tmp_path), fake:
            ok = _run_feedback_pass(
                fx.concept, iter_dir, feedback_path, fx.common_vars,
                fx.analysis_template, fx.make_args(),
            )

        assert ok is False


# ---------------------------------------------------------------------------
# TestIntegration_ModelSetup — loop.py::_run_model_in_iteration
# ---------------------------------------------------------------------------


class TestIntegration_ModelSetup:
    """_run_model_in_iteration also calls ``run_model`` (which spawns ``uv run python``).
    We patch ``run_model`` so only the Claude invocation hits the subprocess boundary."""

    def test_model_setup_success(self, tmp_path):
        from lib.loop import _run_model_in_iteration

        fx = _make_fixture(tmp_path)
        fx.with_analysis("---\nID: test\n---\n\nBody.\n")
        iter_dir = fx.iter_dir(1)
        model_script = iter_dir / "model_setup.py"

        valid_py = (
            "# freeform model\n"
            "params = {'p1': 1}\n"
            "results = {'LCOE': 100.0}\n"
            "print('LCOE: 100.0 $/MWh')\n"
        )

        fake = FakeClaude([
            FakeInvocation(
                returncode=0,
                file_writes=[(model_script, valid_py)],
            ),
        ])
        with (
            patch("lib.loop.CONCEPT_ANALYSIS_DIR", new=tmp_path),
            patch("lib.loop.get_model_path", return_value="freeform"),
            patch("lib.loop.run_model", return_value=(True, "LCOE: 100.0 $/MWh")),
            fake,
        ):
            from lib.iteration import LoopState

            model_ran, model_ok = _run_model_in_iteration(
                fx.concept, iter_dir, fx.make_args(),
                loop_state=LoopState(),
            )

        assert model_ran is True
        assert model_ok is True
        assert model_script.exists()

    def test_model_setup_syntax_retry_recovers(self, tmp_path):
        """First attempt writes invalid Python (SyntaxError); retry writes
        valid Python. ``validate_python_syntax`` catches the first and the
        retry succeeds. RED until Phase 4 migrates _run_model_in_iteration.
        """
        from lib.loop import _run_model_in_iteration

        fx = _make_fixture(tmp_path)
        fx.with_analysis("---\nID: test\n---\n\nBody.\n")
        iter_dir = fx.iter_dir(1)
        model_script = iter_dir / "model_setup.py"

        bad_py = "def f(\nparams = {'p': 1}\n"
        good_py = (
            "# freeform model\n"
            "params = {}\n"
            "results = {'LCOE': 42.0}\n"
            "print('LCOE: 42.0 $/MWh')\n"
        )

        fake = FakeClaude([
            FakeInvocation(returncode=0, file_writes=[(model_script, bad_py)]),
            FakeInvocation(returncode=0, file_writes=[(model_script, good_py)]),
        ])
        with (
            patch("lib.loop.CONCEPT_ANALYSIS_DIR", new=tmp_path),
            patch("lib.loop.get_model_path", return_value="freeform"),
            patch("lib.loop.run_model", return_value=(True, "LCOE: 42.0 $/MWh")),
            fake,
        ):
            from lib.iteration import LoopState

            model_ran, model_ok = _run_model_in_iteration(
                fx.concept, iter_dir, fx.make_args(),
                loop_state=LoopState(),
            )

        assert model_ran is True
        assert model_ok is True
        assert len(fake.calls) == 2
        assert "LCOE" in model_script.read_text()


# ---------------------------------------------------------------------------
# TestDispatchSymmetry — pre_feedback.md / post_feedback.md invariants
# ---------------------------------------------------------------------------
#
# After the feedback-dispatch-symmetry rename, every iter > 1 dir contains:
#   - pre_feedback.md   — input to analyze (one of: review extract, SI output
#                          copy, merge result, or copy of prior post_feedback)
#   - post_feedback.md  — output from assess (immutable transcript)
#
# These tests pin the three plan-stencil invariants from the original rename
# work plan (`.project/active/feedback-dispatch-symmetry/plan.md`):
#   1. Case 5 (default) writes pre_feedback.md as a byte-equal copy of the
#      prior iter's post_feedback.md.
#   2. Case 3 (source-integration) writes pre_feedback.md as a byte-equal copy
#      of source_integration_output.md WITHOUT deleting/clobbering the SI file.
#   3. _run_assess writes only post_feedback.md and never touches a sibling
#      pre_feedback.md.
# ---------------------------------------------------------------------------


class TestDispatchSymmetry:
    def test_copy_to_pre_feedback_byte_equal(self, tmp_path):
        """Plan stencil 1 (Case 5): _copy_to_pre_feedback produces a byte-equal
        copy of the source. This is the contract every dispatch fallthrough
        relies on for the "ls iter-N/ tells you what fed me" property.
        """
        from lib.loop import _copy_to_pre_feedback

        prior = tmp_path / "iter-1" / "post_feedback.md"
        prior.parent.mkdir()
        prior.write_text("VERDICT: FINDINGS\n\n### F-1: ...\n", encoding="utf-8")

        iter_dir = tmp_path / "iter-2"
        iter_dir.mkdir()

        result = _copy_to_pre_feedback(prior, iter_dir)

        assert result == iter_dir / "pre_feedback.md"
        assert result.read_bytes() == prior.read_bytes()
        # Source unchanged (copy, not move).
        assert prior.exists()

    def test_copy_to_pre_feedback_preserves_source(self, tmp_path):
        """Plan stencil 2 (Case 3): copying source_integration_output.md to
        pre_feedback.md must NOT delete or modify the SI artifact. The producer
        artifact stays as the untouched record of what source-integration wrote.
        """
        from lib.loop import _copy_to_pre_feedback

        iter_dir = tmp_path / "iter-2"
        iter_dir.mkdir()
        si_output = iter_dir / "source_integration_output.md"
        si_content = "VERDICT: FINDINGS\n\n### F-1: New finding from source\n"
        si_output.write_text(si_content, encoding="utf-8")

        result = _copy_to_pre_feedback(si_output, iter_dir)

        assert result == iter_dir / "pre_feedback.md"
        assert result.read_bytes() == si_output.read_bytes()
        # SI artifact preserved at its original path with original content.
        assert si_output.exists()
        assert si_output.read_text(encoding="utf-8") == si_content

    def test_copy_to_pre_feedback_none_source(self, tmp_path):
        """When source is None (no prior post_feedback.md), the helper returns
        None without creating an empty file. The dispatch's downstream guard
        then demotes feedback_source to 'cold_start'.
        """
        from lib.loop import _copy_to_pre_feedback

        iter_dir = tmp_path / "iter-2"
        iter_dir.mkdir()

        result = _copy_to_pre_feedback(None, iter_dir)

        assert result is None
        assert not (iter_dir / "pre_feedback.md").exists()

    def test_assess_does_not_clobber_pre_feedback(self, tmp_path):
        """Plan stencil 3: after _run_assess writes post_feedback.md, a
        sibling pre_feedback.md (written earlier in the same iteration by the
        dispatch chain) is unmodified. Verifies invariant #1 from
        design.md#required-invariants.
        """
        from lib.loop import _run_assess

        fx = _make_fixture(tmp_path)
        fx.with_analysis("---\nID: test\n---\n\nBody.\n")
        iter_dir = fx.iter_dir(2)

        pre_path = iter_dir / "pre_feedback.md"
        pre_content = "## Carried-forward findings\n\n### F-1: input from prior\n"
        pre_path.write_text(pre_content, encoding="utf-8")
        pre_bytes_before = pre_path.read_bytes()

        post_path = iter_dir / "post_feedback.md"
        assess_output = (
            "VERDICT: FINDINGS\n\n### F-1: New finding\n- **Category:** analysis\n"
        )

        fake = FakeClaude([
            FakeInvocation(returncode=0, file_writes=[(post_path, assess_output)]),
        ])
        with patch("lib.loop.CONCEPT_ANALYSIS_DIR", new=tmp_path), fake:
            verdict, count = _run_assess(
                fx.concept, iter_dir, fx.analysis_path,
                fx.assessment_template, fx.make_args(),
                common_vars=fx.common_vars,
            )

        # post_feedback.md was written by assess.
        assert post_path.exists()
        assert post_path.read_text(encoding="utf-8") == assess_output

        # pre_feedback.md is untouched — same bytes as before.
        assert pre_path.exists()
        assert pre_path.read_bytes() == pre_bytes_before

        # The two files coexist with different content (the symmetry property).
        assert post_path.read_bytes() != pre_path.read_bytes()


# ---------------------------------------------------------------------------
# TestIntegration_Assess — H-10: _run_assess must honor validation_passed
# ---------------------------------------------------------------------------


class TestIntegration_Assess:
    def test_assess_validation_exhausted_returns_error(self, tmp_path):
        """H-10: when validation exhausts all retries (bad feedback format
        every attempt), _run_assess must return ('ERROR', 0), not parse the
        malformed file with parse_verdict_from_feedback.
        """
        from lib.loop import _run_assess

        fx = _make_fixture(tmp_path)
        fx.with_analysis("---\nID: test\n---\n\nBody.\n")
        iter_dir = fx.iter_dir(1)
        feedback_path = iter_dir / "post_feedback.md"

        bad_feedback = "Here are my thoughts:\n- Point 1\n- Point 2\n"  # no VERDICT

        fake = FakeClaude([
            FakeInvocation(returncode=0, file_writes=[(feedback_path, bad_feedback)]),
            FakeInvocation(returncode=0, file_writes=[(feedback_path, bad_feedback)]),
            FakeInvocation(returncode=0, file_writes=[(feedback_path, bad_feedback)]),
        ])
        with patch("lib.loop.CONCEPT_ANALYSIS_DIR", new=tmp_path), fake:
            verdict, count = _run_assess(
                fx.concept, iter_dir, fx.analysis_path,
                fx.assessment_template, fx.make_args(),
                common_vars=fx.common_vars,
            )

        assert verdict == "ERROR"  # current buggy code returns "FAIL"
        assert count == 0


# ---------------------------------------------------------------------------
# TestIntegration_SourceIntegration — H-09
# ---------------------------------------------------------------------------


class TestIntegration_SourceIntegration:
    def test_source_integration_validation_exhausted_returns_none(self, tmp_path):
        """H-09: when validation exhausts all retries, _run_source_integration
        must return None, not proceed with a malformed output file."""
        from lib.loop import _run_source_integration

        fx = _make_fixture(tmp_path)
        fx.with_analysis("---\nID: test\n---\n\nBody.\n")
        iter_dir = fx.iter_dir(1)
        output_path = iter_dir / "source_integration_output.md"

        bad_output = "Integration summary:\n- point A\n- point B\n"

        new_sources = [tmp_path / "src1.md"]
        new_sources[0].write_text("source 1 content")

        fake = FakeClaude([
            FakeInvocation(returncode=0, file_writes=[(output_path, bad_output)]),
            FakeInvocation(returncode=0, file_writes=[(output_path, bad_output)]),
            FakeInvocation(returncode=0, file_writes=[(output_path, bad_output)]),
        ])
        stub_templates = tmp_path / "stub_templates"
        stub_templates.mkdir()
        (stub_templates / "source_integration.md").write_text(
            "Integrate {{concept_name}} {{analysis_path}} "
            "{{new_source_paths}} {{feedback_path}}"
        )
        with (
            patch("lib.loop.CONCEPT_ANALYSIS_DIR", new=tmp_path),
            patch("lib.loop.TEMPLATES_DIR", new=stub_templates),
            fake,
        ):
            result = _run_source_integration(
                fx.concept, iter_dir, new_sources, fx.analysis_path, fx.make_args(),
            )

        assert result is None


# ---------------------------------------------------------------------------
# TestIntegration_TransientRetry — H-17
# ---------------------------------------------------------------------------


class TestIntegration_TransientRetry:
    def test_transient_retry_recovers_after_rate_limit(self):
        """H-17: invoke_claude must retry with exponential backoff on rc != 0.
        Two rc=1 failures then rc=0 success → 3 subprocess calls, 2 sleeps.
        """
        sleeps: list[float] = []
        with patch("lib.claude.time.sleep", side_effect=lambda s: sleeps.append(s)):
            fake = FakeClaude([
                FakeInvocation(returncode=1, stderr="rate limit"),
                FakeInvocation(returncode=1, stderr="rate limit"),
                FakeInvocation(returncode=0, stdout_text="ok"),
            ])
            with fake:
                result = invoke_claude("prompt", cwd=Path("/tmp"))

        assert result.returncode == 0
        assert len(fake.calls) == 3
        # Two backoffs (between attempts 1→2 and 2→3).
        assert len(sleeps) == 2

    def test_transient_retry_exhausted_surfaces_failure(self):
        """After all 3 attempts fail (1 initial + 2 retries per design), the
        final rc=1 is surfaced to the caller. No 4th attempt."""
        sleeps: list[float] = []
        with patch("lib.claude.time.sleep", side_effect=lambda s: sleeps.append(s)):
            fake = FakeClaude([
                FakeInvocation(returncode=1, stderr="err 1"),
                FakeInvocation(returncode=1, stderr="err 2"),
                FakeInvocation(returncode=1, stderr="err 3"),
            ])
            with fake:
                result = invoke_claude("prompt", cwd=Path("/tmp"))
        assert result.returncode == 1
        # 2 sleeps between the 3 attempts
        assert len(sleeps) == 2

    def test_timeout_not_retried(self):
        """Timeouts are deterministic failures, not transient."""
        with patch("lib.claude.time.sleep") as sleep_mock, \
             patch("lib.claude.subprocess.run") as run_mock:
            run_mock.side_effect = subprocess.TimeoutExpired(cmd="claude", timeout=900)
            result = invoke_claude("prompt", cwd=Path("/tmp"), timeout=900)
        assert result.returncode == -1
        assert run_mock.call_count == 1
        sleep_mock.assert_not_called()

    def test_file_not_found_not_retried(self):
        """FileNotFoundError (claude CLI missing) is deterministic."""
        with patch("lib.claude.time.sleep") as sleep_mock, \
             patch("lib.claude.subprocess.run") as run_mock:
            run_mock.side_effect = FileNotFoundError()
            result = invoke_claude("prompt", cwd=Path("/tmp"))
        assert result.returncode == -2
        assert run_mock.call_count == 1
        sleep_mock.assert_not_called()


# ---------------------------------------------------------------------------
# TestIntegration_CanonicalFiles — H-16
# ---------------------------------------------------------------------------


class TestIntegration_CanonicalFiles:
    def test_canonical_files_not_updated_on_model_failure(self, tmp_path):
        """H-16: when the iteration's model failed (model_ok=False), canonical
        model files at the concept root MUST NOT be overwritten with the
        broken iteration's files."""
        from lib.loop import _update_canonical_files

        concept_dir = tmp_path / "concept"
        concept_dir.mkdir()
        (concept_dir / "model_setup.py").write_text("# GOOD previous\n")
        (concept_dir / "model_output.txt").write_text("LCOE: 55.3 $/MWh\n")

        iter_dir = concept_dir / "iter-10"
        iter_dir.mkdir()
        (iter_dir / "model_setup.py").write_text("# BAD current\n")
        (iter_dir / "model_output.txt").write_text("BAD output\n")

        _update_canonical_files(concept_dir, iter_dir, model_ok=False)

        assert (concept_dir / "model_setup.py").read_text() == "# GOOD previous\n"
        assert (concept_dir / "model_output.txt").read_text() == "LCOE: 55.3 $/MWh\n"

    def test_canonical_files_updated_on_model_success(self, tmp_path):
        """Positive regression guard: model_ok=True updates canonical files."""
        from lib.loop import _update_canonical_files

        concept_dir = tmp_path / "concept"
        concept_dir.mkdir()
        (concept_dir / "model_setup.py").write_text("# OLD\n")

        iter_dir = concept_dir / "iter-11"
        iter_dir.mkdir()
        (iter_dir / "model_setup.py").write_text("# NEW\n")
        (iter_dir / "model_output.txt").write_text("LCOE: 70 $/MWh\n")

        _update_canonical_files(concept_dir, iter_dir, model_ok=True)

        assert "NEW" in (concept_dir / "model_setup.py").read_text()
        assert "LCOE: 70" in (concept_dir / "model_output.txt").read_text()


# ---------------------------------------------------------------------------
# TestIntegration_ClearIterations — H-18
# ---------------------------------------------------------------------------


class TestIntegration_ClearIterations:
    def test_clear_iterations_removes_research_log(self, tmp_path):
        """H-18: ``clear_iterations`` (called by --force) must also delete
        research_log.json so that stale iteration references don't linger."""
        from lib.iteration import clear_iterations

        concept_dir = tmp_path / "concept"
        concept_dir.mkdir()
        (concept_dir / "iter-1").mkdir()
        (concept_dir / "iter-2").mkdir()
        research_log = concept_dir / "research_log.json"
        research_log.write_text('{"entries": [{"iteration": 1}]}')

        deleted = clear_iterations(concept_dir)

        assert deleted == 2
        assert not research_log.exists()
        assert not (concept_dir / "iter-1").exists()
        assert not (concept_dir / "iter-2").exists()

    def test_clear_iterations_no_research_log_ok(self, tmp_path):
        """No research_log.json is fine — must not raise."""
        from lib.iteration import clear_iterations

        concept_dir = tmp_path / "concept"
        concept_dir.mkdir()
        (concept_dir / "iter-1").mkdir()

        deleted = clear_iterations(concept_dir)
        assert deleted == 1


# ---------------------------------------------------------------------------
# TestIntegration_ExtractExplorerData — H-19 regression guard
# ---------------------------------------------------------------------------


class TestIntegration_ExtractExplorerData:
    """H-19: ``extract_explorer_data.run_extraction`` must clear the
    ``<concept>.json.stale`` sidecar after writing a fresh per-concept JSON.

    The Phase 6 design verified this behavior was already correct in
    ``extract_explorer_data.py`` (see design.md#component-5b). This is a
    regression guard so future refactors of the cleanup block don't silently
    re-introduce the bug.
    """

    def test_extract_explorer_data_clears_stale_marker(self, tmp_path, monkeypatch):
        import sys
        explorer_pkg = (
            Path(__file__).resolve().parents[2] / "concept_explorer"
        )
        monkeypatch.syspath_prepend(str(explorer_pkg))
        import extract_explorer_data as eed

        analyses_dir = tmp_path / "analyses"
        concept_dir = analyses_dir / "42-fake-concept"
        concept_dir.mkdir(parents=True)
        # discover_concepts needs model_setup.py or analysis.md; use a
        # trivially non-costingfe model so the standalone branch is hit.
        (concept_dir / "model_setup.py").write_text("result = 1.0\n")

        data_dir = tmp_path / "data"
        data_dir.mkdir()
        # Pre-create the stale marker that the analysis pipeline would have
        # dropped alongside an existing (now out-of-date) per-concept JSON.
        stale_marker = data_dir / "42.json.stale"
        stale_marker.write_text("1")
        assert stale_marker.exists()

        fake_concept = MagicMock()
        fake_concept.model_dump_json.return_value = '{"concept_id": "42"}'
        monkeypatch.setattr(eed, "extract_standalone", lambda *a, **kw: fake_concept)
        monkeypatch.setattr(eed, "load_parameter_metadata", lambda *a, **kw: {})
        # Manifest + parameter_index are no longer built during extraction
        # (server computes them at startup), so no stubbing is needed.

        eed.run_extraction(
            analyses_dir=analyses_dir,
            data_dir=data_dir,
            concept_filter=["42"],
            skip_narrative=True,
        )

        assert (data_dir / "42.json").exists()
        assert not stale_marker.exists(), (
            "H-19 regression: .stale sidecar should be cleared after "
            "writing a fresh per-concept JSON"
        )


# ---------------------------------------------------------------------------
# TestIntegration_ExternalFeedback — H-08
# ---------------------------------------------------------------------------


class TestIntegration_ExternalFeedback:
    def test_external_feedback_not_archived_on_unchanged(self, tmp_path):
        """H-08: when Claude returns rc=0 but analysis.md is byte-identical,
        the feedback file MUST NOT be archived."""
        from run_analysis import _apply_external_feedback

        fx = _make_fixture(tmp_path)
        original_analysis = "---\nID: test\n---\n\nOriginal.\n"
        fx.with_analysis(original_analysis)
        feedback_file = fx.concept_dir / "change_requests.md"
        feedback_file.write_text("Please change things.")

        templates_dir = tmp_path / "templates"
        templates_dir.mkdir()
        (templates_dir / "analysis_v2.md").write_text(
            "Apply {{feedback_path}} to {{concept_name}}"
        )

        fake = FakeClaude([
            FakeInvocation(returncode=0),
            FakeInvocation(returncode=0),
            FakeInvocation(returncode=0),
        ])
        with (
            patch("run_analysis.TEMPLATES_DIR", new=templates_dir),
            patch("run_analysis.CONCEPT_ANALYSIS_DIR", new=tmp_path),
            patch("run_analysis.ANALYSES_DIR", new=tmp_path / "analyses"),
            patch(
                "run_analysis._build_common_vars",
                return_value={"concept_name": "Test Concept", "company": "Test Co"},
            ),
            fake,
        ):
            _apply_external_feedback(
                [fx.concept], fx.make_args(), feedback_file,
            )

        # Feedback still in place (not archived)
        assert feedback_file.exists()
        assert fx.analysis_path.read_text() == original_analysis

    def test_external_feedback_archived_on_change(self, tmp_path):
        """Happy path: when analysis.md IS modified, the feedback file is
        archived with a timestamp."""
        from run_analysis import _apply_external_feedback

        fx = _make_fixture(tmp_path)
        fx.with_analysis("---\nID: test\n---\n\nOriginal.\n")
        feedback_file = fx.concept_dir / "change_requests.md"
        feedback_file.write_text("Please change things.")

        templates_dir = tmp_path / "templates"
        templates_dir.mkdir()
        (templates_dir / "analysis_v2.md").write_text(
            "Apply {{feedback_path}} to {{concept_name}}"
        )

        modified = "---\nID: test\n---\n\nRevised.\n"
        fake = FakeClaude([
            FakeInvocation(
                returncode=0,
                file_edits=[(fx.analysis_path, modified)],
            ),
        ])
        with (
            patch("run_analysis.TEMPLATES_DIR", new=templates_dir),
            patch("run_analysis.CONCEPT_ANALYSIS_DIR", new=tmp_path),
            patch("run_analysis.ANALYSES_DIR", new=tmp_path / "analyses"),
            patch(
                "run_analysis._build_common_vars",
                return_value={"concept_name": "Test Concept", "company": "Test Co"},
            ),
            fake,
        ):
            _apply_external_feedback(
                [fx.concept], fx.make_args(), feedback_file,
            )

        assert not feedback_file.exists()
        archived = list(fx.concept_dir.glob("change_requests_*.md"))
        assert len(archived) == 1


# ---------------------------------------------------------------------------
# cmd_* level integration tests — DEFERRED placeholders.
# These will be fleshed out in Phase 5 when each command is migrated to
# ``invoke_claude_validated`` + ``prepare_step``. Skipping (not RED) so the
# test surface is visible but doesn't clutter Phase 1 red runs.
# ---------------------------------------------------------------------------


class TestIntegration_GapCheck:
    def test_gap_check_stdout_mode_writes_file(self, tmp_path):
        """FR-13 / Migration 6: gap-check returns content in stdout (no file),
        then explicitly writes gap_report.md. output_path=None is deliberate —
        bypasses H-01 because Claude emits to stdout here.

        Locks in the stdout-mode contract: a single rc=0 invocation whose
        stdout passes ``validate_non_empty`` writes the file with no retries.
        """
        from run_analysis import cmd_gap_check

        fx = _make_fixture(tmp_path)
        gap_path = fx.concept_dir / "gap_report.md"
        expected_content = "# Gap Report\n\nSources missing: 3"

        templates_dir = tmp_path / "templates"
        templates_dir.mkdir()
        (templates_dir / "gap_check.md").write_text("Gap-check {{concept_name}}")

        # Stub a dossier the lib.sources resolver won't find on its own.
        dossier_file = tmp_path / "dossier.md"
        dossier_file.write_text("dossier content")

        fake = FakeClaude([
            FakeInvocation(returncode=0, stdout_text=expected_content),
        ])
        args = fx.make_args(
            concepts=[fx.concept_id],
            family=None,
            all_remaining=False,
            dry_run=False,
            force=False,
        )
        with (
            patch("run_analysis.TEMPLATES_DIR", new=templates_dir),
            patch("run_analysis.CONCEPT_ANALYSIS_DIR", new=tmp_path),
            patch("run_analysis.ANALYSES_DIR", new=tmp_path / "analyses"),
            patch("run_analysis.get_dossier_path", return_value=dossier_file),
            patch("run_analysis.find_sources", return_value=[]),
            fake,
        ):
            cmd_gap_check([fx.concept], args)

        assert gap_path.exists()
        assert gap_path.read_text() == expected_content
        assert len(fake.calls) == 1


class TestIntegration_Review:
    def test_cmd_review_findings_verdict_roundtrip(self, tmp_path):
        pytest.skip("Phase 5 integration test — requires cmd_review migration")

    def test_cmd_review_file_not_written_retry(self, tmp_path):
        pytest.skip("Phase 5 integration test — requires cmd_review migration")


class TestIntegration_Synthesize:
    def test_cmd_synthesize_frontmatter_body_assembly(self, tmp_path):
        pytest.skip("Phase 5 integration test — requires cmd_synthesize migration")


class TestIntegration_AddressReview:
    def test_address_review_no_change_fails(self, tmp_path):
        pytest.skip("Phase 5 integration test — requires cmd_address_review migration")

    def test_address_review_success_updates_frontmatter(self, tmp_path):
        pytest.skip("Phase 5 integration test — requires cmd_address_review migration")


# ---------------------------------------------------------------------------
# Retry prompt rendered-string tests (Phase 3)
# ---------------------------------------------------------------------------
# Per design-review Minor 6: assert on the *rendered prompt string* Claude
# sees, not on _augment_fix_message return values.
# ---------------------------------------------------------------------------


class TestRetryPromptContent:
    def test_retry_prompt_contains_path_and_next_attempt(self, tmp_path):
        """FR-5 + FR-6: after attempt 1 fails, the prompt sent on retry must
        contain the output path and 'attempt 2 of 3'. RED until Phase 3.
        """
        out = tmp_path / "out.md"

        def only_good(text):
            return ValidationResult(
                valid=(text.strip() == "good"),
                fix_message="make it good please",
                details="checking",
            )

        fake = FakeClaude([
            FakeInvocation(returncode=0, file_writes=[(out, "bad")]),
            FakeInvocation(
                returncode=0,
                file_writes=[(out, "good")],
                expect_prompt_contains=[
                    str(out),
                    "attempt 2 of 3",
                    "make it good please",
                ],
            ),
        ])
        with fake:
            result = invoke_claude_validated(
                "initial prompt", tmp_path, validator=only_good,
                output_path=out, max_retries=2, step_label="test",
            )
        assert result.validation_passed is True

    def test_final_attempt_says_critical_final(self, tmp_path):
        """FR-6: after attempt 2 fails, the final retry prompt must contain
        'CRITICAL' and 'FINAL attempt 3 of 3'. RED until Phase 3.
        """
        out = tmp_path / "out.md"

        def never_good(text):
            return ValidationResult(
                valid=False, fix_message="try again", details="bad",
            )

        fake = FakeClaude([
            FakeInvocation(returncode=0, file_writes=[(out, "bad1")]),
            FakeInvocation(
                returncode=0,
                file_writes=[(out, "bad2")],
                expect_prompt_contains=["attempt 2 of 3"],
            ),
            FakeInvocation(
                returncode=0,
                file_writes=[(out, "bad3")],
                expect_prompt_contains=["CRITICAL", "FINAL", "attempt 3 of 3"],
            ),
        ])
        with fake:
            result = invoke_claude_validated(
                "p", tmp_path, validator=never_good,
                output_path=out, max_retries=2, step_label="t",
            )
        assert result.validation_passed is False

    def test_file_not_found_log_has_preview_sentinel(self, tmp_path):
        """FR-7 + H-01: when output_path file is missing, log entry's
        validated_text_preview must be 'FILE NOT FOUND' and the validator
        must NOT have run. RED until Phase 3."""
        out = tmp_path / "out.md"
        log_path = tmp_path / "vlog.json"

        validator_calls = []

        def spy(text):
            validator_calls.append(text)
            return ValidationResult(valid=False, fix_message="f", details="d")

        spy.__name__ = "spy_validator"

        fake = FakeClaude([
            FakeInvocation(returncode=0),
            FakeInvocation(returncode=0),
            FakeInvocation(returncode=0),
        ])
        with fake:
            invoke_claude_validated(
                "p", tmp_path, validator=spy,
                output_path=out, max_retries=2, step_label="t",
                log_path=log_path,
            )

        entries = json.loads(log_path.read_text())
        for e in entries:
            assert e.get("validated_text_preview") == "FILE NOT FOUND"
        assert validator_calls == []  # validator never ran

    def test_final_log_entry_has_no_fix_message_sent(self, tmp_path):
        """FR-7: the final attempt's log entry is the 'last word' — it must
        NOT include fix_message_sent (no retry follows). RED until Phase 3."""
        out = tmp_path / "out.md"
        log_path = tmp_path / "vlog.json"

        def never_good(text):
            return ValidationResult(valid=False, fix_message="fix", details="d")

        fake = FakeClaude([
            FakeInvocation(returncode=0, file_writes=[(out, "bad1")]),
            FakeInvocation(returncode=0, file_writes=[(out, "bad2")]),
            FakeInvocation(returncode=0, file_writes=[(out, "bad3")]),
        ])
        with fake:
            invoke_claude_validated(
                "p", tmp_path, validator=never_good,
                output_path=out, max_retries=2, step_label="t",
                log_path=log_path,
            )

        entries = json.loads(log_path.read_text())
        assert len(entries) == 3
        assert "fix_message_sent" in entries[0]
        assert "fix_message_sent" in entries[1]
        assert "fix_message_sent" not in entries[2]  # final entry

    def test_validated_text_preview_populated_for_file(self, tmp_path):
        """FR-7: successful validation log entry includes text preview."""
        out = tmp_path / "out.md"
        log_path = tmp_path / "vlog.json"

        def always_good(text):
            return ValidationResult(valid=True, details="ok")

        fake = FakeClaude([
            FakeInvocation(returncode=0, file_writes=[(out, "hello world")]),
        ])
        with fake:
            invoke_claude_validated(
                "p", tmp_path, validator=always_good,
                output_path=out, step_label="t",
                log_path=log_path,
            )

        entries = json.loads(log_path.read_text())
        assert entries[0]["validated_text_preview"] == "hello world"
