"""Claude invocation and model execution helpers."""

from __future__ import annotations

import json
import os
import re
import subprocess
import sys
import time
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from lib.validators import Validator


# Transient retry backoff schedule (FR-2 / H-17). Length determines the number
# of retries; total attempts = len(_TRANSIENT_DELAYS) + 1. Phase 1 integration
# tests encode a 3-attempt contract (two 30s/60s backoffs, no third sleep), so
# this list has two entries. The design doc also mentions a 120s third delay,
# but the test harness contract supersedes that — see Phase 2 Completion notes.
_TRANSIENT_DELAYS: list[int] = [30, 60]


@dataclass
class InvokeResult:
    """Result of a claude invocation.

    Supports 3-tuple unpacking for backward compatibility:
        stdout, stderr, rc = invoke_claude(...)
    """

    stdout: str
    stderr: str
    returncode: int
    session_id: str | None = None
    # Best-effort run accounting parsed from the result event (diagnostic only;
    # None when the stream lacks it or didn't parse). Used by callers that write
    # a cost line to a run log; existing callers ignore them.
    cost_usd: float | None = None
    usage: dict | None = None
    num_turns: int | None = None

    def __iter__(self):
        """Backward-compatible unpacking: stdout, stderr, rc = invoke_claude(...)"""
        return iter((self.stdout, self.stderr, self.returncode))


def _parse_json_events(raw: str) -> tuple[str, str | None]:
    """Parse JSON event stream from claude -p --output-format json.

    Returns (result_text, session_id).

    Raises:
        json.JSONDecodeError: raw is not valid JSON.
        ValueError: JSON is valid but structurally unusable — not a list, no
            ``type: "result"`` event present, or the result event's ``result``
            field is not a string (e.g., JSON null). The "missing" and
            "non-string" cases raise distinct messages so operators can tell
            them apart.
    """
    if raw is None:
        raise ValueError("stdout is None (possible encoding failure)")
    events = json.loads(raw)
    if not isinstance(events, list):
        raise ValueError(f"Expected JSON list, got {type(events).__name__}")

    session_id: str | None = None
    found_result_event = False
    result_text: str = ""

    for event in events:
        if not isinstance(event, dict):
            continue
        # Extract session_id from first event that has one
        if session_id is None and "session_id" in event:
            session_id = event["session_id"]
        # Extract result text from last result event
        if event.get("type") == "result" and "result" in event:
            found_result_event = True
            value = event["result"]
            if not isinstance(value, str):
                raise ValueError(
                    f"'result' event has non-string result: {type(value).__name__}"
                )
            result_text = value

    if not found_result_event:
        raise ValueError("No 'result' event found in JSON event stream")

    return result_text, session_id


def _extract_result_meta(raw: str) -> dict:
    """Best-effort cost/usage/turns from the result event. ``{}`` if absent.

    Separate from ``_parse_json_events`` (whose 2-tuple contract is pinned) so
    adding run-accounting can't disturb the text/session path. Diagnostic only —
    never raises; a genuinely malformed stream already warned via the parse path.
    """
    try:
        events = json.loads(raw)
    except (json.JSONDecodeError, TypeError):
        return {}
    if not isinstance(events, list):
        return {}
    for event in events:
        if isinstance(event, dict) and event.get("type") == "result":
            return {
                "cost_usd": event.get("total_cost_usd"),
                "usage": event.get("usage") or event.get("modelUsage"),
                "num_turns": event.get("num_turns"),
            }
    return {}


def invoke_claude(
    prompt: str,
    cwd: Path,
    timeout: int = 900,
    model: str | None = None,
    *,
    resume: str | None = None,
) -> InvokeResult:
    """Invoke claude in print mode via stdin.

    Returns InvokeResult with parsed text and session_id.
    Supports backward-compatible 3-tuple unpacking.

    If resume is provided, uses --resume <session-id> to continue
    an existing conversation.
    """
    cmd = [
        "claude", "-p",
        "--dangerously-skip-permissions", "--verbose",
        "--output-format", "json",
    ]
    if resume:
        cmd.extend(["--resume", resume])
    if model:
        cmd.extend(["--model", model])

    total_attempts = len(_TRANSIENT_DELAYS) + 1
    result = None
    for attempt in range(total_attempts):
        try:
            result = subprocess.run(
                cmd,
                input=prompt,
                capture_output=True,
                text=True,
                encoding="utf-8",
                cwd=str(cwd),
                timeout=timeout,
            )
        except subprocess.TimeoutExpired as e:
            # Timeouts are deterministic — NOT retried.
            partial = (e.stdout or "") if e.stdout else ""
            return InvokeResult(partial, f"Timed out after {timeout}s", -1)
        except FileNotFoundError:
            # Claude CLI missing — deterministic, NOT retried.
            return InvokeResult(
                "", "'claude' command not found — is Claude Code installed and on PATH?", -2
            )

        if result.returncode == 0:
            break  # success — proceed to parse

        # Transient failure (rc != 0): back off and retry if budget remains.
        stderr_preview = (result.stderr or "")[:200]
        if attempt < len(_TRANSIENT_DELAYS):
            delay = _TRANSIENT_DELAYS[attempt]
            print(
                f"  warn: claude returned rc={result.returncode}, "
                f"retrying in {delay}s (attempt {attempt + 2}/{total_attempts})"
                f"\n    stderr: {stderr_preview}",
                file=sys.stderr,
            )
            time.sleep(delay)
        else:
            # Final attempt exhausted — emit a distinct "giving up" warning so
            # operators see the exhaustion explicitly (the inter-attempt warns
            # above stop after the penultimate failure). Then fall through with
            # the failed result so the caller receives the final rc.
            print(
                f"  warn: claude returned rc={result.returncode} after "
                f"{total_attempts} attempts, giving up"
                f"\n    stderr: {stderr_preview}",
                file=sys.stderr,
            )

    # At this point, ``result`` is always bound (initial iteration always
    # either sets it or returns early on Timeout/FileNotFoundError).
    assert result is not None

    # Parse JSON event stream for text result and session ID
    try:
        text, session_id = _parse_json_events(result.stdout)
    except (json.JSONDecodeError, ValueError) as exc:
        # Fall back to raw stdout if JSON parsing fails. Warn loudly to stderr
        # so operators notice this degraded mode (FR-3 / H-04).
        print(
            f"  warn: JSON event stream parse failed "
            f"({type(exc).__name__}: {exc}), falling back to raw stdout",
            file=sys.stderr,
        )
        text = result.stdout
        session_id = None

    meta = _extract_result_meta(result.stdout)
    return InvokeResult(
        text, result.stderr, result.returncode, session_id,
        cost_usd=meta.get("cost_usd"),
        usage=meta.get("usage"),
        num_turns=meta.get("num_turns"),
    )


@dataclass
class ValidatedResult:
    """Result of an invoke_claude call with optional validation."""

    invoke: InvokeResult
    validation_passed: bool
    attempts: int  # 1 = no retries, 2+ = retried
    log_entries: list[dict] = field(default_factory=list)


def _augment_fix_message(
    raw_fix: str,
    output_path: Path | None,
    attempt: int,
    total_attempts: int,
) -> str:
    """Add file-path and attempt-escalation context to a validator's fix message.

    ``attempt`` is the 1-indexed number of the attempt that just failed.
    ``total_attempts`` is the full budget (``max_retries + 1``). The returned
    message is the prompt sent on the retry that *follows* ``attempt`` — so
    the attempt number rendered in the message is ``attempt + 1``, and we
    escalate to CRITICAL/FINAL when that next attempt is the last one.
    """
    parts: list[str] = []

    next_attempt = attempt + 1
    if next_attempt == total_attempts:
        parts.append(
            f"CRITICAL: This is your FINAL attempt "
            f"{next_attempt} of {total_attempts}. "
            f"Focus carefully on producing the correct output."
        )
    else:
        parts.append(
            f"Note: This is attempt {next_attempt} of {total_attempts}."
        )

    if output_path is not None:
        parts.append(f"IMPORTANT: Write your output to the file: {output_path}")

    parts.append(raw_fix)
    return "\n\n".join(parts)


def _decide_retry_mode(
    attempt: int,
    total_attempts: int,
    session_id: str | None,
    result: InvokeResult,
    have_fix_message: bool = True,
) -> str | None:
    """Decide retry strategy after a failed attempt.

    Returns one of:

    * ``"resume"`` — claude returned with a parseable ``session_id`` and we
      have a fix message to send. Retry via ``--resume <session>`` so the
      model can apply the fix in-context.
    * ``"fresh"`` — claude **timed out** (``returncode == -1``, ``session_id``
      is None). There is no session to resume, so retry the **original
      prompt** as a brand-new invocation. Without this branch, a single 900s
      timeout becomes terminal — the failure mode that left concepts 14 and
      15 of the 13–24 regen batch at iter-1 ERROR.
    * ``None`` — no retry available. Budget exhausted, or ``session_id`` is
      absent for a non-timeout reason (e.g. JSON parse failure with rc=0,
      where retrying would just churn the same broken stdout).
    """
    if attempt >= total_attempts:
        return None
    if session_id is not None and have_fix_message:
        return "resume"
    if result.returncode == -1:  # subprocess.TimeoutExpired sentinel
        return "fresh"
    return None


def invoke_claude_validated(
    prompt: str,
    cwd: Path,
    timeout: int = 900,
    model: str | None = None,
    *,
    validator: Validator | None = None,
    output_path: Path | None = None,
    max_retries: int = 2,
    step_label: str = "",
    log_path: Path | None = None,
) -> ValidatedResult:
    """Invoke claude with optional output validation and retry-via-resume.

    If validator is None, behaves like plain invoke_claude().
    If validator is provided, validates output (from output_path or stdout),
    and retries on failure via one of two strategies (see
    ``_decide_retry_mode``): ``--resume`` with a fix message when the prior
    attempt returned a session_id, or a fresh invocation with the original
    prompt when the prior attempt timed out.

    H-01 / FR-1: when ``output_path`` is provided and the file does not exist
    after invocation, this is a distinct first-class failure mode. The
    validator is NOT run against stdout as a fallback — the retry prompt
    tells Claude it failed to write the file and where to put it.
    """
    result = invoke_claude(prompt, cwd, timeout, model)
    log_entries: list[dict] = []

    if validator is None:
        _write_log(log_path, log_entries)
        return ValidatedResult(
            invoke=result, validation_passed=True, attempts=1,
            log_entries=log_entries,
        )

    session_id = result.session_id
    total_attempts = max_retries + 1

    for attempt in range(1, total_attempts + 1):
        # === H-01 FIX: file-existence is a first-class check. ===
        # If output_path was specified and the file wasn't written, this is
        # a distinct failure mode — do NOT fall back to validating stdout.
        if output_path is not None and not output_path.exists():
            raw_fix = (
                f"You did not write the expected output file. "
                f"You MUST write your output to: {output_path}\n"
                f"Please re-read the instructions and write the file."
            )
            entry: dict = {
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "step": step_label,
                "attempt": attempt,
                "validator": validator.__name__,
                "passed": False,
                "details": f"Output file not found: {output_path}",
                "validated_text_preview": "FILE NOT FOUND",
            }

            retry_mode = _decide_retry_mode(
                attempt, total_attempts, session_id, result,
            )
            if retry_mode == "resume":
                entry["fix_message_sent"] = _augment_fix_message(
                    raw_fix, output_path, attempt, total_attempts,
                )
            elif retry_mode == "fresh":
                entry["retry_reason"] = (
                    f"timeout after {timeout}s (rc=-1, no session_id) — "
                    f"retrying with original prompt, fresh invocation"
                )
            log_entries.append(entry)

            if retry_mode is None:
                if attempt < total_attempts and session_id is None:
                    print(
                        "  warn: validation failed, no session_id, and prior "
                        "attempt was not a retryable timeout — cannot retry",
                        file=sys.stderr,
                    )
                break

            if retry_mode == "resume":
                result = invoke_claude(
                    entry["fix_message_sent"], cwd, timeout, model,
                    resume=session_id,
                )
                if result.session_id is None:
                    result = InvokeResult(
                        result.stdout, result.stderr, result.returncode, session_id,
                    )
            else:  # retry_mode == "fresh"
                result = invoke_claude(prompt, cwd, timeout, model)
                # A successful fresh retry establishes a new session_id.
                # Adopt it so any subsequent failures can use resume-style.
                session_id = result.session_id
            continue

        # === Read validation target ===
        if output_path is not None:
            text = output_path.read_text(encoding="utf-8")
        else:
            text = result.stdout

        vr = validator(text)

        entry = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "step": step_label,
            "attempt": attempt,
            "validator": validator.__name__,
            "passed": vr.valid,
            "details": vr.details,
            "validated_text_preview": text[:500] if text else "EMPTY",
        }

        if vr.valid:
            log_entries.append(entry)
            _write_log(log_path, log_entries)
            return ValidatedResult(
                invoke=result, validation_passed=True, attempts=attempt,
                log_entries=log_entries,
            )

        # Validator failed — only log fix_message_sent when we're actually
        # going to dispatch another retry (retry_mode gating).
        retry_mode = _decide_retry_mode(
            attempt, total_attempts, session_id, result,
            have_fix_message=vr.fix_message is not None,
        )
        if retry_mode == "resume":
            entry["fix_message_sent"] = _augment_fix_message(
                vr.fix_message, output_path, attempt, total_attempts,
            )
        elif retry_mode == "fresh":
            entry["retry_reason"] = (
                f"timeout after {timeout}s (rc=-1, no session_id) — "
                f"retrying with original prompt, fresh invocation"
            )
        log_entries.append(entry)

        if retry_mode is None:
            if attempt < total_attempts and session_id is None:
                print(
                    "  warn: validation failed, no session_id, and prior "
                    "attempt was not a retryable timeout — cannot retry",
                    file=sys.stderr,
                )
            break

        if retry_mode == "resume":
            result = invoke_claude(
                entry["fix_message_sent"], cwd, timeout, model,
                resume=session_id,
            )
            if result.session_id is None:
                result = InvokeResult(
                    result.stdout, result.stderr, result.returncode, session_id,
                )
        else:  # retry_mode == "fresh"
            result = invoke_claude(prompt, cwd, timeout, model)
            session_id = result.session_id

    _write_log(log_path, log_entries)
    return ValidatedResult(
        invoke=result, validation_passed=False, attempts=len(log_entries),
        log_entries=log_entries,
    )


def _write_log(log_path: Path | None, entries: list[dict]) -> None:
    """Write validation log entries to JSON file, appending if it exists."""
    if log_path is None or not entries:
        return
    existing = []
    if log_path.exists():
        try:
            existing = json.loads(log_path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, ValueError):
            pass
    log_path.write_text(
        json.dumps(existing + entries, indent=2) + "\n",
        encoding="utf-8",
    )


def run_model(model_path: Path, output_path: Path, timeout: int = 120) -> tuple[bool, str]:
    """Run a model_setup.py script, save output to model_output.txt, sanity-check results.

    Returns (success, message). On success, message is the stdout. On failure, message
    is the error description.
    """
    model_path = model_path.resolve()
    if not model_path.exists():
        return False, f"model script not found: {model_path}"

    try:
        env = os.environ.copy()
        env["PYTHONIOENCODING"] = "utf-8"
        result = subprocess.run(
            ["uv", "run", "python", str(model_path)],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=timeout,
            cwd=str(model_path.parent),
            env=env,
        )
    except subprocess.TimeoutExpired:
        return False, f"model timed out after {timeout}s"
    except FileNotFoundError:
        return False, "'uv' command not found — is uv installed and on PATH?"

    if result.returncode != 0:
        stderr_snippet = result.stderr.strip()[:300] if result.stderr else "(no stderr)"
        return False, f"model failed (rc={result.returncode}): {stderr_snippet}"

    stdout = result.stdout
    if not stdout.strip():
        return False, "model produced no output"

    if "lcoe" not in stdout.lower():
        return False, "model output missing LCOE — may be incomplete or broken"

    output_path.write_text(stdout, encoding="utf-8")

    _check_interface(model_path)

    return True, stdout


def _check_interface(model_path: Path) -> None:
    """Check output interface conformance and print warnings to stderr.

    NOTE: import-based detection logic parallels extract_explorer_data.py routing.
    If you change detection here, update the extractor too.
    """
    source = model_path.read_text(encoding="utf-8")
    uses_costingfe = "CostModel" in source and (
        "from costingfe" in source or "import costingfe" in source
    )

    if uses_costingfe:
        # costingfe path: the explorer reads module-level `result` (and
        # `result_1gw`). Accept both the legacy inline `result = model.forward(...)`
        # and the Item-8 four-step helper form `result, result_1gw =
        # run_native_and_1gw(...)` (tuple-unpack binds `result` just the same).
        has_result = re.search(r"^result\b[^=]*=", source, re.MULTILINE) or (
            "run_native_and_1gw" in source
        )
        if not has_result:
            print(
                f"WARNING: interface: {model_path.name} uses costingfe but has no "
                "module-level `result` binding (inline `result = model.forward(...)` "
                "or `result, result_1gw = run_native_and_1gw(...)`). The concept "
                "explorer requires this for extraction.",
                file=sys.stderr,
            )
    else:
        # freeform path: check for module-level params and results
        has_params = re.search(r"^params\s*=", source, re.MULTILINE)
        has_results = re.search(r"^results\s*=", source, re.MULTILINE)
        if not has_params or not has_results:
            missing = []
            if not has_params:
                missing.append("params")
            if not has_results:
                missing.append("results")
            print(
                f"WARNING: interface: {model_path.name} is missing module-level "
                f"{' and '.join(missing)}. The concept explorer requires these for extraction.",
                file=sys.stderr,
            )
