"""Claude invocation and model execution helpers."""

from __future__ import annotations

import json
import re
import subprocess
import sys
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from lib.validators import Validator


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

    def __iter__(self):
        """Backward-compatible unpacking: stdout, stderr, rc = invoke_claude(...)"""
        return iter((self.stdout, self.stderr, self.returncode))


def _parse_json_events(raw: str) -> tuple[str, str | None]:
    """Parse JSON event stream from claude -p --output-format json.

    Returns (result_text, session_id). Raises on invalid JSON.
    """
    events = json.loads(raw)
    if not isinstance(events, list):
        raise ValueError(f"Expected JSON list, got {type(events).__name__}")

    session_id = None
    result_text = ""

    for event in events:
        if not isinstance(event, dict):
            continue
        # Extract session_id from first event that has one
        if session_id is None and "session_id" in event:
            session_id = event["session_id"]
        # Extract result text from last result event
        if event.get("type") == "result" and "result" in event:
            result_text = event["result"]

    return result_text, session_id


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

    try:
        result = subprocess.run(
            cmd,
            input=prompt,
            capture_output=True,
            text=True,
            cwd=str(cwd),
            timeout=timeout,
        )
    except subprocess.TimeoutExpired as e:
        partial = (e.stdout or "") if e.stdout else ""
        return InvokeResult(partial, f"Timed out after {timeout}s", -1)
    except FileNotFoundError:
        return InvokeResult(
            "", "'claude' command not found — is Claude Code installed and on PATH?", -2
        )

    # Parse JSON event stream for text result and session ID
    try:
        text, session_id = _parse_json_events(result.stdout)
    except (json.JSONDecodeError, ValueError):
        # Fall back to raw stdout if JSON parsing fails
        text = result.stdout
        session_id = None

    return InvokeResult(text, result.stderr, result.returncode, session_id)


@dataclass
class ValidatedResult:
    """Result of an invoke_claude call with optional validation."""

    invoke: InvokeResult
    validation_passed: bool
    attempts: int  # 1 = no retries, 2+ = retried
    log_entries: list[dict] = field(default_factory=list)


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
    and retries via --resume on failure.
    """
    result = invoke_claude(prompt, cwd, timeout, model)
    log_entries: list[dict] = []

    if validator is None:
        _write_log(log_path, log_entries)
        return ValidatedResult(
            invoke=result, validation_passed=True, attempts=1,
            log_entries=log_entries,
        )

    # Validate loop: initial attempt + up to max_retries
    session_id = result.session_id
    for attempt in range(1, max_retries + 2):  # 1-indexed, includes initial
        # Read validation target
        if output_path is not None and output_path.exists():
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
        }
        if not vr.valid and vr.fix_message:
            entry["fix_message_sent"] = vr.fix_message
        log_entries.append(entry)

        if vr.valid:
            _write_log(log_path, log_entries)
            return ValidatedResult(
                invoke=result, validation_passed=True, attempts=attempt,
                log_entries=log_entries,
            )

        # Can we retry?
        if attempt > max_retries:
            break

        if session_id is None:
            print(
                f"  warn: validation failed but no session_id — cannot retry",
                file=sys.stderr,
            )
            break

        # Retry via --resume
        result = invoke_claude(
            vr.fix_message, cwd, timeout, model, resume=session_id,
        )
        # Preserve session_id if resume didn't return one
        if result.session_id is None:
            result = InvokeResult(
                result.stdout, result.stderr, result.returncode, session_id,
            )

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
        result = subprocess.run(
            ["uv", "run", "python", str(model_path)],
            capture_output=True,
            text=True,
            timeout=timeout,
            cwd=str(model_path.parent),
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
        # costingfe path: check for module-level 'result = ...'
        if not re.search(r"^result\s*=", source, re.MULTILINE):
            print(
                f"WARNING: interface: {model_path.name} uses costingfe but has no "
                "module-level 'result = model.forward(...)'. The concept explorer "
                "requires this for extraction.",
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
