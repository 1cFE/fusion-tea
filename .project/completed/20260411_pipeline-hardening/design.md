# Design: Pipeline Hardening

**Status:** Implemented (all components landed across Phases 2–6; see `plan.md` for phase-by-phase completion notes)
**Owner:** Reid W
**Created:** 2026-04-08 22:09 PDT
**Updated:** 2026-04-11 (implementation complete; audit passed clean)
**Branch:** design-space-explore

## Overview

Harden the concept analysis pipeline by fixing `invoke_claude_validated`'s foundation, adding transient retry, replacing `run_claude_step` entirely, and migrating all Claude call sites to validated invocation. 22 issues addressed, 3 deferred.

## Related Artifacts

- **Spec:** `.project/active/pipeline-hardening/spec.md`
- **Research:** `.project/research/20260408-pipeline-holes-comprehensive-audit.md`
- **Prior research:** `.project/research/20260408-validation-retry-failure-analysis.md`

## Research Findings

### File Map

All code lives under `exploration/concept_analysis/scripts/lib/` (the audit omits the `lib/` segment in file references):

| File | Lines | Role |
|------|-------|------|
| `lib/claude.py` | 303 | `invoke_claude`, `invoke_claude_validated`, `run_model`, `_check_interface` |
| `lib/validators.py` | 164 | `ValidationResult`, `Validator` type, `validate_feedback_verdict`, `validate_review_verdict` |
| `lib/step_runner.py` | 156 | `run_claude_step` — the framework being replaced |
| `lib/loop.py` | 775 | Stage 1 loop: cold-start, feedback-pass, model-setup, assess, source-integration |
| `lib/research.py` | 225 | Autonomous source acquisition via `invoke_claude` |
| `lib/iteration.py` | 170 | Iteration state, verdicts, `clear_iterations` |
| `lib/state.py` | 163 | Concept state, staleness, extraction state |
| `lib/sources.py` | 215 | Source discovery, `resolve_source_names` (has `sys.exit`) |
| `lib/concepts.py` | 236 | Concept table, `resolve_concepts` (has `sys.exit`) |
| `lib/landscape.py` | ~120 | Concept landscape, has canonical `_extract_iter_count` |
| `run_analysis.py` | ~1050 | CLI commands: gap-check, analyze, model-setup, review, synthesize, etc. |

### Existing Patterns

- **`InvokeResult`** (claude.py:19-33): Dataclass with backward-compatible 3-tuple unpacking. All callers use `_stdout, stderr, rc = invoke_claude(...)`. This unpacking pattern must survive.
- **`ValidatedResult`** (claude.py:115-122): Has `invoke`, `validation_passed`, `attempts`, `log_entries`.
- **`Validator`** type (validators.py:45): `Callable[[str], ValidationResult]` — takes text, returns valid/invalid with fix_message.
- **Template filling**: `fill_template(template_text, vars_dict)` used everywhere for prompt construction.
- **Test patterns**: `test_claude.py` (255 lines), `test_validated.py` (285 lines), `test_validators.py` (319 lines). All use `unittest.mock.patch` on `lib.claude.subprocess.run` or `lib.claude.invoke_claude`. Tests run via `uv run python -m pytest` from `scripts/`.

### Call Site Inventory (Complete)

Every production Claude invocation:

| # | Call site | File:Line | Current method | Output mode | Post-processing |
|---|-----------|-----------|---------------|-------------|-----------------|
| 1 | `_run_cold_start` | loop.py:355 | `invoke_claude` | Writes `analysis_body.md` (new file) | Assembles frontmatter + body into `analysis.md`, deletes body |
| 2 | `_run_feedback_pass` | loop.py:418 | `invoke_claude` | Edits `analysis.md` in-place (Edit tool) | rc check only |
| 3 | `_run_model_in_iteration` | loop.py:489 | `invoke_claude` | Writes `model_setup.py` (new file) | Checks exists, runs model |
| 4 | `_run_assess` | loop.py:612 | `invoke_claude_validated` | Writes `feedback.md` (new file) | **Already migrated** — parses verdict |
| 5 | `_run_source_integration` | loop.py:679 | `invoke_claude_validated` | Writes `source_integration_output.md` | **Already migrated** — parses verdict |
| 6 | `cmd_gap_check` | run_analysis.py:223 | `run_claude_step` | `stdout_to_file` → `gap_report.md` | Prints done |
| 7 | `cmd_model_setup` | run_analysis.py:465 | `run_claude_step` | `file_exists` → `model_setup.py` | Runs model |
| 8 | `cmd_review` | run_analysis.py:562 | `run_claude_step` | `file_with_fallback` → `review.md` | Detects verdict, updates frontmatter |
| 9 | `cmd_synthesize` | run_analysis.py:809 | `run_claude_step` | `file_with_fallback` → `synthesis_body.md` | Assembles frontmatter + body |
| 10 | `cmd_address_review` | run_analysis.py:678 | `run_claude_step` | `no_output` (Edit tool) | Re-runs model, updates frontmatter |
| 11 | `_apply_external_feedback` | run_analysis.py:402 | `invoke_claude` | Edits `analysis.md` in-place | Propagates staleness, archives feedback |
| 12 | `run_research_step` | research.py:86 | `invoke_claude` | No expected file (filesystem diff) | Detects new sources, updates log |

### `run_claude_step` Feature Audit

What `run_claude_step` does, and where each feature goes after replacement:

| Feature | Lines | Replacement |
|---------|-------|-------------|
| Ensure output/prompt dirs exist | 70-72 | Inline at each caller (1 line) |
| Skip-if-exists | 75-77 | Inline at each caller (2 lines), or keep existing caller-level skip logic |
| Build vars + fill template | 80-83 | Inline — callers already have `build_vars` functions |
| Write prompt to disk | 85 | Inline (1 line) |
| Dry-run bail | 88-90 | Inline (2 lines) |
| Progress print | 93 | Inline (1 line) |
| `invoke_claude()` call | 97-99 | Replaced by `invoke_claude_validated()` |
| Elapsed timing | 102 | Inline (2 lines) |
| Failure check (rc != 0) | 104-112 | Handled by `invoke_claude_validated` + transient retry |
| Output mode resolution | 114-144 | **Eliminated** — validator + H-01 fix replaces this entirely |
| Post-hook | 152-153 | Inline per-caller logic (already unique per site) |

Each caller needs ~15-20 lines of boilerplate (dirs, skip, template, dry-run, print, timing). The unique logic (validators, post-processing) is what matters and is already per-caller.

---

## Design Callout: Validator Signature

The spec (FR-6) says "The Validator type MUST accept attempt context." The audit proposes extending the `Callable` signature. After studying the code, I recommend a different approach that achieves the same goal with less churn:

**Keep `Validator = Callable[[str], ValidationResult]` unchanged.** Instead, have the retry loop in `invoke_claude_validated` augment the fix_message with attempt context and file path before sending it to Claude.

**Why this is better:**
- The validator's job is **format checking** — "does this text match the expected format?" That doesn't depend on which attempt we're on.
- The retry loop's job is **constructing the retry message** — it knows the attempt number, output path, and escalation strategy.
- Changing the `Validator` signature breaks both existing validators (`validate_feedback_verdict`, `validate_review_verdict`) and all tests. For zero benefit — the validator would just ignore the attempt number in its format-checking logic and only use it to vary the fix_message, which the retry loop can do itself.
- The file path (FR-5, FR-12a) is also a retry-loop concern, not a validator concern. The validator checks text content; it doesn't know where the text came from.

**Concrete mechanism:** See `_augment_fix_message` in Component 2b below — a single helper owned by the retry loop that prepends file-path and attempt-escalation context to the validator's raw fix message.

The loop is 1-indexed (`for attempt in range(1, max_retries + 2)`) and `total = max_retries + 1`. The helper displays `{attempt}` directly (not `attempt + 1`) and guards the FINAL-attempt escalation with `attempt == total`, so for `max_retries=2` the messages read "attempt 2 of 3" and "attempt 3 of 3 (FINAL)" — not the off-by-one values the audit's original sketch produced.

This satisfies FR-5 (path in fix messages), FR-6 (escalating attempts), and FR-12a (path included) without changing the `Validator` type.

---

## Proposed Design

### Architecture

Three layers, modified bottom-up:

```
┌──────────────────────────────────────────────┐
│  Call Sites (loop.py, run_analysis.py,        │
│  research.py)                                 │
│  - Each calls invoke_claude_validated directly │
│  - Each provides a validator                  │
│  - Per-caller pre/post logic inline           │
├──────────────────────────────────────────────┤
│  invoke_claude_validated (claude.py)           │
│  - File-existence first-class check (H-01)    │
│  - Fix message augmentation (path, attempt)   │
│  - Validation log with text preview (H-14)    │
├──────────────────────────────────────────────┤
│  invoke_claude (claude.py)                     │
│  - Transient retry with backoff (H-17)        │
│  - JSON parse warning (H-04)                  │
│  - _parse_json_events raises on no result     │
└──────────────────────────────────────────────┘
```

`step_runner.py` is **repurposed**, not deleted: `run_claude_step`, `StepResult`, and `OutputMode` are removed; the file becomes the home for `prepare_step` + `StepContext` (the pipeline-orchestration helper described in Component 6). The remaining unique per-caller logic (validators, post-processing) lives at the call sites. Co-locating `prepare_step` in `step_runner.py` keeps `claude.py` focused on the subprocess/client boundary and preserves the natural home for "prepare a step" code.

### Component 1: `invoke_claude` Hardening

**File:** `lib/claude.py:61-112`

#### 1a. Transient retry (FR-2)

Add exponential backoff retry around the `subprocess.run()` call for transient failures.

```python
import time

_TRANSIENT_DELAYS = [30, 60, 120]  # seconds between retries

def invoke_claude(
    prompt: str,
    cwd: Path,
    timeout: int = 900,
    model: str | None = None,
    *,
    resume: str | None = None,
) -> InvokeResult:
    cmd = [...]  # unchanged

    for attempt in range(len(_TRANSIENT_DELAYS) + 1):
        try:
            result = subprocess.run(cmd, input=prompt, ...)
        except subprocess.TimeoutExpired as e:
            # Timeouts are NOT retried — they're deterministic
            return InvokeResult(...)
        except FileNotFoundError:
            # Not installed — NOT retried
            return InvokeResult(...)

        if result.returncode == 0:
            break  # success — proceed to parse

        # Transient failure: rc != 0
        if attempt < len(_TRANSIENT_DELAYS):
            delay = _TRANSIENT_DELAYS[attempt]
            stderr_preview = (result.stderr or "")[:200]
            print(
                f"  warn: claude returned rc={result.returncode}, "
                f"retrying in {delay}s (attempt {attempt + 2}/{len(_TRANSIENT_DELAYS) + 1})"
                f"\n    stderr: {stderr_preview}",
                file=sys.stderr,
            )
            time.sleep(delay)
        # else: last attempt, fall through

    # Parse JSON event stream (same as current code)
    ...
```

**Key decisions:**
- Timeout (`-1`) and FileNotFoundError (`-2`) are NOT retried — they're deterministic failures.
- Only `result.returncode != 0` from subprocess triggers retry.
- Delays are configurable via module constant, not parameter (keeps call sites clean).
- Each retry re-runs the SAME command (not `--resume`) — this is transient retry, not content retry.

#### 1b. JSON parse warning (FR-3)

```python
try:
    text, session_id = _parse_json_events(result.stdout)
except (json.JSONDecodeError, ValueError) as exc:
    print(
        f"  warn: JSON event stream parse failed ({type(exc).__name__}: {exc}), "
        f"falling back to raw stdout",
        file=sys.stderr,
    )
    text = result.stdout
    session_id = None
```

#### 1c. `_parse_json_events` raises on no result (FR-4)

```python
def _parse_json_events(raw: str) -> tuple[str, str | None]:
    events = json.loads(raw)
    if not isinstance(events, list):
        raise ValueError(f"Expected JSON list, got {type(events).__name__}")

    session_id = None
    result_text = None  # Changed from "" to None as sentinel

    for event in events:
        if not isinstance(event, dict):
            continue
        if session_id is None and "session_id" in event:
            session_id = event["session_id"]
        if event.get("type") == "result" and "result" in event:
            result_text = event["result"]

    if result_text is None:
        raise ValueError("No 'result' event found in JSON event stream")

    return result_text, session_id
```

**Tests to update:** `test_no_result_event` and `test_empty_list` in `test_claude.py` must change from expecting `""` to expecting `ValueError`.

### Component 2: `invoke_claude_validated` Fix + Enrichment

**File:** `lib/claude.py:125-208`

#### 2a. File-existence first-class check (FR-1)

The critical H-01 fix. When `output_path` is provided but the file doesn't exist after invocation, this is a **distinct failure mode** — NOT a fallback to stdout validation.

```python
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
    result = invoke_claude(prompt, cwd, timeout, model)
    log_entries: list[dict] = []

    if validator is None:
        _write_log(log_path, log_entries)
        return ValidatedResult(invoke=result, validation_passed=True,
                               attempts=1, log_entries=log_entries)

    session_id = result.session_id
    total_attempts = max_retries + 1
    for attempt in range(1, total_attempts + 1):
        # === H-01 FIX: file-existence is a first-class check ===
        if output_path is not None and not output_path.exists():
            # File not written — distinct failure mode
            raw_fix = (
                f"You did not write the expected output file. "
                f"You MUST write your output to: {output_path}\n"
                f"Please re-read the instructions and write the file."
            )
            entry = {
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "step": step_label,
                "attempt": attempt,
                "validator": validator.__name__,
                "passed": False,
                "details": f"Output file not found: {output_path}",
                "validated_text_preview": "FILE NOT FOUND",
            }

            # Only log fix_message_sent when we're actually going to retry.
            will_retry = attempt < total_attempts and session_id is not None
            if will_retry:
                entry["fix_message_sent"] = _augment_fix_message(
                    raw_fix, output_path, attempt, total_attempts)
            log_entries.append(entry)

            if not will_retry:
                break
            result = invoke_claude(
                entry["fix_message_sent"], cwd, timeout, model,
                resume=session_id,
            )
            if result.session_id is None:
                result = InvokeResult(
                    result.stdout, result.stderr, result.returncode, session_id)
            continue

        # === Read validation target ===
        if output_path is not None:
            text = output_path.read_text(encoding="utf-8")
        else:
            text = result.stdout

        # === Run validator ===
        vr = validator(text)

        # === Build log entry (FR-7: includes text preview) ===
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
            return ValidatedResult(invoke=result, validation_passed=True,
                                   attempts=attempt, log_entries=log_entries)

        # Failed — only log fix_message_sent if we're actually going to retry.
        will_retry = (
            attempt < total_attempts
            and vr.fix_message is not None
            and session_id is not None
        )
        if will_retry:
            entry["fix_message_sent"] = _augment_fix_message(
                vr.fix_message, output_path, attempt, total_attempts)
        log_entries.append(entry)

        if not will_retry:
            if attempt < total_attempts and session_id is None:
                print("  warn: validation failed but no session_id — cannot retry",
                      file=sys.stderr)
            break

        result = invoke_claude(
            entry["fix_message_sent"], cwd, timeout, model,
            resume=session_id,
        )
        if result.session_id is None:
            result = InvokeResult(
                result.stdout, result.stderr, result.returncode, session_id)

    _write_log(log_path, log_entries)
    return ValidatedResult(invoke=result, validation_passed=False,
                           attempts=len(log_entries), log_entries=log_entries)
```

**Key invariants:**
- `attempt` is 1-indexed; `total_attempts = max_retries + 1` (initial + retries).
- `fix_message_sent` is only recorded in the log entry for attempts that actually send a retry prompt. The final attempt's entry contains no `fix_message_sent` — it's the last word.
- The file-not-found branch and the validator-failed branch use the same `will_retry` discipline, so log semantics are uniform.

#### 2b. Fix message augmentation (FR-5, FR-6, FR-12a)

New helper function in `claude.py`:

```python
def _augment_fix_message(
    raw_fix: str,
    output_path: Path | None,
    attempt: int,
    total_attempts: int,
) -> str:
    """Add file-path and attempt-escalation context to a validator's fix message.

    ``attempt`` is 1-indexed. ``total_attempts`` is the full budget
    (max_retries + 1). The returned message is the prompt sent on the retry
    that *follows* ``attempt``.
    """
    parts = []

    # Attempt escalation. The retry this message launches will be
    # ``attempt + 1`` of ``total_attempts``, so escalate to CRITICAL when
    # the next attempt is the last one.
    next_attempt = attempt + 1
    if next_attempt == total_attempts:
        parts.append(
            f"CRITICAL: This is your FINAL attempt "
            f"({next_attempt} of {total_attempts}). "
            f"Focus carefully on producing the correct output."
        )
    else:
        parts.append(
            f"Note: This is attempt {next_attempt} of {total_attempts}."
        )

    # File path context
    if output_path is not None:
        parts.append(f"IMPORTANT: Write your output to the file: {output_path}")

    parts.append(raw_fix)
    return "\n\n".join(parts)
```

**Note on semantics:** The helper is called *before* a retry is dispatched, so the attempt-number it names is the *next* one. With `total_attempts=3`:
- After attempt 1 fails → retry prompt reads "attempt 2 of 3"
- After attempt 2 fails → retry prompt reads "CRITICAL: FINAL attempt 3 of 3"
- After attempt 3 fails → no retry, no message

This matches the user-facing expectation that "FINAL" refers to the attempt Claude is about to perform, not the one that just failed.

### Component 3: New Validators

**File:** `lib/validators.py` (append to existing file)

```python
import hashlib

def validate_non_empty(text: str) -> ValidationResult:
    """Minimum viable validator — output must be non-empty."""
    if not text.strip():
        return ValidationResult(
            valid=False,
            fix_message=(
                "Your output was empty. Please re-read the instructions "
                "and produce the requested output."
            ),
            details="Output is empty or whitespace-only",
        )
    return ValidationResult(valid=True, details=f"Non-empty ({len(text)} chars)")


def validate_python_syntax(text: str) -> ValidationResult:
    """Check that output is parseable Python."""
    try:
        compile(text, "<model_setup>", "exec")
    except SyntaxError as e:
        return ValidationResult(
            valid=False,
            fix_message=(
                f"The Python file has a syntax error on line {e.lineno}: {e.msg}. "
                f"Please fix the syntax error and re-write the file."
            ),
            details=f"SyntaxError line {e.lineno}: {e.msg}",
        )
    return ValidationResult(valid=True, details="Valid Python syntax")


def make_file_modified_validator(path: Path) -> Validator:
    """Factory: returns a validator that checks file bytes actually changed.

    The factory snapshots the file's SHA-256 *at construction time*, then on
    each call re-reads the file's raw bytes and compares. The ``text`` argument
    passed by ``invoke_claude_validated`` is ignored — we deliberately read
    bytes directly to avoid any UTF-8 / line-ending / BOM normalization
    round-trip that would make an unchanged file hash differently from its
    snapshot.

    Usage:
        validator = make_file_modified_validator(analysis_path)
        result = invoke_claude_validated(
            ..., validator=validator, output_path=analysis_path)
    """
    original_hash = hashlib.sha256(path.read_bytes()).hexdigest()

    def _check(_text: str) -> ValidationResult:
        # Re-read bytes directly — NOT text.encode("utf-8"). The caller's
        # ``text`` has been through ``read_text(encoding="utf-8")`` which
        # normalizes line endings and may strip BOMs. Hashing the encoded
        # string can therefore disagree with ``read_bytes()`` even when the
        # file on disk is byte-identical to the snapshot.
        if not path.exists():
            # Should be unreachable — invoke_claude_validated's H-01 branch
            # handles file-missing before calling the validator — but keep
            # the check for defense in depth.
            return ValidationResult(
                valid=False,
                fix_message=f"File missing at {path}",
                details="File missing during file-modified check",
            )
        current = hashlib.sha256(path.read_bytes()).hexdigest()
        if current == original_hash:
            return ValidationResult(
                valid=False,
                fix_message=(
                    "The file was not modified. You MUST apply the requested "
                    "changes using the Edit tool. Read the file, identify what "
                    "needs to change, and use Edit to make the changes."
                ),
                details="File content unchanged (SHA-256 match)",
            )
        return ValidationResult(valid=True, details="File content changed")

    _check.__name__ = "validate_file_modified"  # for log entries
    return _check
```

**Note on naming and signature:** The audit calls it `validate_file_modified` (noun), but it's a factory that returns a validator. Naming it `make_*` makes the factory pattern explicit. The factory takes the `Path` directly (not a pre-computed hash) for two reasons:

1. **Hashing must be byte-exact.** An earlier sketch let the caller compute `sha256(path.read_bytes())` and passed only the hash into the factory, expecting the validator to hash `text.encode("utf-8")` inside. That round-trip is unsafe: `read_text` normalizes line endings to `\n` and (in some configurations) strips a BOM, so an unchanged file can hash differently from its snapshot, giving a **false pass**. Owning both hash operations inside the closure guarantees they use the same input.
2. **Fewer surprises for callers.** Callers no longer need to remember the exact hash invocation — the factory name tells them it will snapshot the file.

The `text` argument is deliberately unused (`_text`) — the validator signature is preserved so the `Validator` type and retry loop don't change, but the actual check reads disk bytes. This is a small ergonomic compromise (we re-read the file once) in exchange for correctness.

#### FR-8: Verdict type in details

Patch `validate_feedback_verdict` (validators.py:110):
```python
# Current:
return ValidationResult(valid=True, details="Feedback format valid")

# Changed:
verdict_type = verdict_match.group(1)  # "PASS" or "FINDINGS"
return ValidationResult(valid=True, details=f"Feedback format valid (verdict: {verdict_type})")
```

Same pattern for `validate_review_verdict` (validators.py:163).

### Component 4: Call Site Migrations

Each migration follows the same pattern:
1. Replace `invoke_claude`/`run_claude_step` with `invoke_claude_validated`
2. Add appropriate validator
3. Handle `ValidatedResult` (check `validation_passed`)
4. Keep per-caller pre/post logic

#### Migration 1: `_run_cold_start` (loop.py:319-378)

**Current:** `invoke_claude` + manual `body_path.exists()` check.
**New:** `invoke_claude_validated` with `validate_non_empty`, `output_path=body_path`.

```python
def _run_cold_start(concept, iter_dir, common_vars, template, analysis_path, args):
    cid = concept["_id"]
    body_path = iter_dir / "analysis_body.md"

    ctx = prepare_step(
        step_label="analyze (cold start)",
        concept_id=cid,
        prompt_text=fill_template(template, {**common_vars, ...}),
        prompt_path=iter_dir / "analyze_prompt.md",
        out_dir=iter_dir,
        dry_run=args.dry_run,
    )
    if not ctx.proceed:
        return True

    analysis_path.write_text(make_frontmatter(concept), encoding="utf-8")

    from lib.validators import validate_non_empty
    result = invoke_claude_validated(
        ctx.prompt_text, cwd=CONCEPT_ANALYSIS_DIR,
        timeout=args.timeout, model=args.model,
        validator=validate_non_empty,
        output_path=body_path,
        step_label="cold-start",
        log_path=iter_dir / "validation_log.json",
    )
    elapsed = time.time() - ctx.start_time

    if result.invoke.returncode != 0 or not result.validation_passed:
        print(f" FAILED ({elapsed:.0f}s)")
        analysis_path.unlink(missing_ok=True)
        return False

    # Assemble: frontmatter + body (unchanged)
    fm_raw = analysis_path.read_text(encoding="utf-8").rstrip("\n") + "\n"
    body = body_path.read_text(encoding="utf-8")
    analysis_path.write_text(fm_raw + "\n" + body, encoding="utf-8")
    body_path.unlink()
    print(f" done ({elapsed:.0f}s, {len(body)} chars)")
    return True
```

#### Migration 2: `_run_feedback_pass` (loop.py:381-430)

**Current:** `invoke_claude` + rc check only.
**New:** `invoke_claude_validated` with `make_file_modified_validator`, `output_path=analysis_path`.

```python
def _run_feedback_pass(concept, iter_dir, feedback_path, common_vars, template, args):
    cid = concept["_id"]
    analysis_path = iter_dir.parent / "analysis.md"
    iter_num = int(iter_dir.name.split("-")[1])

    ctx = prepare_step(
        step_label=f"analyze iter {iter_num}/{args.max_passes} (feedback pass)",
        concept_id=cid,
        prompt_text=fill_template(template, {**common_vars, ...}),
        prompt_path=iter_dir / "analyze_prompt.md",
        out_dir=iter_dir,
        dry_run=args.dry_run,
    )
    if not ctx.proceed:
        return True

    # Factory MUST be constructed after prepare_step but before invocation,
    # so it snapshots the file bytes immediately before Claude touches it.
    from lib.validators import make_file_modified_validator
    file_modified = make_file_modified_validator(analysis_path)

    result = invoke_claude_validated(
        ctx.prompt_text, cwd=CONCEPT_ANALYSIS_DIR,
        timeout=args.timeout, model=args.model,
        validator=file_modified,
        output_path=analysis_path,
        step_label="feedback-pass",
        log_path=iter_dir / "validation_log.json",
    )
    elapsed = time.time() - ctx.start_time

    if result.invoke.returncode != 0:
        print(f" FAILED ({elapsed:.0f}s, rc={result.invoke.returncode})")
        return False

    if not result.validation_passed:
        print(f" WARN ({elapsed:.0f}s) — analysis.md not modified")
        return False  # Treat as failure — no point continuing with unchanged analysis

    print(f" done ({elapsed:.0f}s)")
    return True
```

#### Migration 3: `_run_model_in_iteration` (loop.py:453-515)

**Current:** `invoke_claude` + manual `model_script.exists()` check.
**New:** `invoke_claude_validated` with `validate_python_syntax`, `output_path=model_script`.

Same pattern as cold-start. On validation failure (syntax error), `model_ok=False` (model failures are non-fatal per FR-7).

#### Migration 4: `_run_assess` (loop.py:575-641) — Already migrated

Uses `invoke_claude_validated` with `validate_feedback_verdict`.

**Changes needed:** Add `validation_passed` check (FR-17/H-10):
```python
# After the existing rc and exists checks, ADD:
if not result.validation_passed:
    print(f" FAILED ({elapsed:.0f}s) — validation exhausted")
    return "ERROR", 0
```

#### Migration 5: `_run_source_integration` (loop.py:644-705) — Already migrated

Same `validation_passed` check needed (FR-17/H-09).

#### Migration 6: `cmd_gap_check` (run_analysis.py:184-234)

**Current:** `run_claude_step` with `stdout_to_file`.
**New:** `invoke_claude_validated` with `validate_non_empty`, `output_path=None` (stdout mode), then explicit file write.

```python
for c in targets:
    cid = c["_id"]
    rid = c["_research_id"]
    out_dir = ANALYSES_DIR / cid
    gap_path = out_dir / "gap_report.md"

    # Eligibility checks that prepare_step does not own (dossier, sources).
    dossier_path = get_dossier_path(rid)
    if not dossier_path:
        print(f"  skip {cid} (no Phase 1a dossier found)")
        continue
    sources = find_sources(rid)
    template_text = (TEMPLATES_DIR / "gap_check.md").read_text(encoding="utf-8")

    ctx = prepare_step(
        step_label="gap-check",
        concept_id=cid,
        prompt_text=fill_template(template_text, {
            "concept_id": cid, "concept_name": c["Concept Name"], ...
        }),
        prompt_path=out_dir / "prompts" / "gap_check_prompt.md",
        out_dir=out_dir,
        skip_if_exists=gap_path,
        dry_run=args.dry_run,
        force=args.force,
    )
    if not ctx.proceed:
        continue

    from lib.validators import validate_non_empty
    result = invoke_claude_validated(
        ctx.prompt_text, cwd=CONCEPT_ANALYSIS_DIR,
        timeout=args.timeout, model=args.model,
        validator=validate_non_empty,
        step_label="gap-check",
    )
    elapsed = time.time() - ctx.start_time

    if result.invoke.returncode != 0 or not result.validation_passed:
        print(f" FAILED ({elapsed:.0f}s)")
        continue

    # Explicit write (no more stdout_to_file magic)
    gap_path.write_text(result.invoke.stdout, encoding="utf-8")
    print(f" done ({elapsed:.0f}s, {len(result.invoke.stdout)} chars)")
```

**Note:** Gap-check is a stdout-mode call (Claude produces the gap report in its response, not as a file). We validate the stdout text and then explicitly write it. This replaces the `stdout_to_file` output mode.

**IMPORTANT — do not "fix" this to use `output_path`.** Passing `output_path=None` here is deliberate: it routes `invoke_claude_validated` into the stdout-validation branch and bypasses the H-01 file-existence check, because for gap-check there is no file for Claude to write. A future maintainer looking at this site and comparing it to the other migrations will notice the inconsistency — that is by design. The inline comment at the call site should explicitly call this out so the explanation lives with the code, not just in this design doc.

#### Migration 7: `cmd_model_setup` (run_analysis.py:425-478)

**Current:** `run_claude_step` with `file_exists`.
**New:** `invoke_claude_validated` with `validate_python_syntax`, `output_path=model_path`.

Post-hook (running the model) becomes inline after the validated result check.

#### Migration 8: `cmd_review` (run_analysis.py:481-574)

**Current:** `run_claude_step` with `file_with_fallback`, post-hook does verdict detection.
**New:** `invoke_claude_validated` with `validate_review_verdict`, `output_path=review_path`.

The `_post` hook logic (frontmatter update) becomes inline. The verdict detection moves from regex-on-output-text to reading from the validated review file. The `file_with_fallback` mode is eliminated — if the file doesn't exist, the H-01 fix catches it.

#### Migration 9: `cmd_synthesize` (run_analysis.py:692-823)

**Current:** `run_claude_step` with `file_with_fallback`, pre-write frontmatter, post-hook assembles.
**New:** `invoke_claude_validated` with `validate_non_empty`, `output_path=body_path`.

Pre-write frontmatter and post-assembly logic become inline (already unique to this caller).

#### Migration 10: `cmd_address_review` (run_analysis.py:577-689)

**Current:** `run_claude_step` with `no_output` (Claude uses Edit tool).
**New:** `invoke_claude_validated` with `make_file_modified_validator(analysis_path)`, `output_path=analysis_path`.

Claude edits `analysis.md` (and potentially `model_setup.py`) in-place. We validate that `analysis.md` changed. As with the other in-place sites, the factory call must happen *before* the invocation so it can snapshot the original bytes.

**Validator scope decision (review follow-up):** `cmd_address_review` may result in Claude modifying `analysis.md`, `model_setup.py`, both, or neither. We validate **only `analysis.md`** for three reasons:
1. The primary deliverable of "address review" is an updated analysis. A review response that only tweaks `model_setup.py` without touching the narrative has not actually addressed the review.
2. A narrative-only update (analysis.md changes, model unchanged) IS a valid outcome — many reviews request wording, scope, or framing changes that don't affect the cost model.
3. Adding a second `make_file_modified_validator(model_setup_path)` would require either an AND (too strict — rejects valid narrative-only updates) or an OR (too loose — accepts model-only updates that skip the narrative).

If review experience shows this is wrong (e.g., Claude gaming the check by whitespace-editing `analysis.md`), revisit with a content-level validator. Not in scope for this design.

#### Migration 11: `_apply_external_feedback` (run_analysis.py:363-423)

**Current:** `invoke_claude` + rc check, archives feedback unconditionally.
**New:** `invoke_claude_validated` with `make_file_modified_validator`, `output_path=analysis_path`.

**FR-16:** Only archive the feedback file if validation passed (analysis.md actually changed).

```python
from lib.validators import make_file_modified_validator
# Factory snapshots analysis_path bytes *before* the invocation.
file_modified = make_file_modified_validator(analysis_path)

result = invoke_claude_validated(
    prompt, cwd=CONCEPT_ANALYSIS_DIR,
    timeout=args.timeout, model=args.model,
    validator=file_modified,
    output_path=analysis_path,
    step_label="external-feedback",
)

if result.invoke.returncode != 0 or not result.validation_passed:
    print(f" FAILED ({elapsed:.0f}s)")
    if not result.validation_passed:
        print(f"    analysis.md was not modified — feedback file preserved")
    continue  # Do NOT archive feedback

# Only archive after confirmed modification
print(f" done ({elapsed:.0f}s)")
feedback.rename(archived)
```

#### Migration 12: `run_research_step` (research.py:86)

**Current:** `invoke_claude` + filesystem diff.
**New:** `invoke_claude_validated` with `validate_non_empty`, `output_path=None`.

Low-priority migration. The filesystem diff is the real success check (did new sources appear?). The validator just ensures Claude produced some output. The `research_output.json` is parsed separately after the call.

### Component 5: Standalone Fixes

#### 5a. Canonical file guard (FR-18, H-16)

**File:** `lib/loop.py:762-774`

`_update_canonical_files` currently copies unconditionally. Add `model_ok` parameter:

```python
def _update_canonical_files(concept_dir: Path, iter_dir: Path, *, model_ok: bool = True) -> None:
    iter_model = iter_dir / "model_setup.py"
    if iter_model.exists() and model_ok:  # Only copy if model succeeded
        shutil.copy2(iter_model, concept_dir / "model_setup.py")

    iter_output = iter_dir / "model_output.txt"
    if iter_output.exists() and model_ok:
        shutil.copy2(iter_output, concept_dir / "model_output.txt")
```

Update caller at loop.py:197:
```python
_update_canonical_files(concept_dir, iter_dir, model_ok=model_ok)
```

#### 5b. Stale marker cleanup (FR-19, H-19) — already satisfied

**Finding:** H-19 is already fixed in the current codebase. `extract_explorer_data.py:797-801` already deletes the `.stale` sidecar after writing a fresh per-concept JSON:

```python
# exploration/concept_explorer/extract_explorer_data.py
out_path = data_dir / f"{concept_id}.json"
out_path.write_text(concept_data.model_dump_json(indent=2), encoding="utf-8")
print(f"  wrote {out_path}")

# Clear staleness sidecar if present (analysis pipeline creates these)
stale_marker = out_path.with_suffix(".json.stale")
if stale_marker.exists():
    stale_marker.unlink()
    print(f"  cleared stale marker: {stale_marker.name}")
```

`extract_explorer_data.py:793` is the only write site for per-concept explorer JSON. Manifest and `parameter_index.json` are aggregates and do not carry `.stale` sidecars.

**Conclusion:** No code change is required for FR-19. The audit flagged H-19 before verifying the current state of `extract_explorer_data.py`. The design does not introduce a `clear_stale_marker` helper — inlining the three-line cleanup at its one call site is simpler than a one-call-site helper.

**Verification step for implementation:** Before closing FR-19, reproduce the flow end-to-end: run `propagate_staleness` on a concept with existing explorer data → confirm `.stale` is created → run `extract_explorer_data.py` for that concept → confirm `.stale` is removed. If the flow works, mark FR-19 complete with a note in the implementation log.

#### 5c. Clear research_log on --force (FR-20, H-18)

**File:** `lib/iteration.py:157-164`

```python
def clear_iterations(concept_dir: Path) -> int:
    """Delete all iter-*/ directories. Used by --force. Returns count deleted."""
    count = 0
    for d in concept_dir.glob("iter-*/"):
        if _parse_iter_num(d.name) is not None:
            shutil.rmtree(d)
            count += 1
    # Clear research log (H-18) — references iteration numbers that no longer exist
    research_log = concept_dir / "research_log.json"
    if research_log.exists():
        research_log.unlink()
    return count
```

#### 5d. Code smell fixes

**S-01:** Delete unused import in `run_analysis.py:55`:
```python
# Remove: from lib.state import ..., _has_downstream_artifacts
```

**S-02:** See Component 5e below — rather than importing a private symbol, rename `_extract_iter_count` → `extract_iter_count` in `lib/landscape.py` and import the public name from `run_analysis.py`.

**S-06/S-07:** Change `sys.exit(1)` to `raise ValueError` in `resolve_source_names` (sources.py:131,138) and `resolve_concepts` (concepts.py:224,228). Update callers in `run_analysis.py` to catch `ValueError`:

In `resolve_concepts` (concepts.py:220-231):
```python
# Replace sys.exit(1) with:
raise ValueError(f"No concept matching '{q}'")
# and:
raise ValueError(
    f"Ambiguous query '{q}' matched {len(matches)} concepts: "
    + ", ".join(m['_id'] for m in matches)
)
```

In `resolve_source_names` (sources.py:130-138):
```python
# Replace sys.exit(1) with:
raise ValueError(f"Source '{name}' not found under {concept_dir}/iter-*/sources/")
# and:
raise ValueError(f"Source '{name}' found in multiple iterations: {matches}")
```

Callers in `run_analysis.py` that use `resolve_concepts` need wrapping. Since `resolve_concepts` is called at the top of every `cmd_*` function, the simplest fix is to catch `ValueError` in the CLI `main()` dispatcher:

```python
def main():
    ...
    try:
        handler(concepts, args)
    except ValueError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)
```

#### 5e. Rename `_extract_iter_count` → `extract_iter_count`

FR-22 (S-02) says deduplicate the helper. Rather than importing the private `_extract_iter_count` from `lib/landscape.py` into `run_analysis.py`, rename it:

- Rename `_extract_iter_count` → `extract_iter_count` in `lib/landscape.py`.
- Update the one existing in-file caller in `landscape.py`.
- Delete the duplicate in `run_analysis.py:94-99`.
- Add `from lib.landscape import extract_iter_count` at the top of `run_analysis.py`.

The leading-underscore on the original is a vestige of when it had a single in-module caller. Once a second module uses it, it is public-by-use, so make it public-by-name.

### Component 6: Shared step helper (`prepare_step`)

**File:** `lib/step_runner.py` (repurposed — old `run_claude_step`/`StepResult`/`OutputMode` deleted, file becomes the home for `prepare_step` + `StepContext`)

**Design-review decision (2026-04-10):** `prepare_step` does filesystem I/O, prompt-path management, skip-if-exists bookkeeping, and progress printing — none of which are Claude-client concerns. Placing it in `lib/claude.py` would mix pipeline-orchestration responsibilities with the subprocess boundary and grow `claude.py` past ~380 lines. Instead, we repurpose `step_runner.py`: delete the legacy surface (`run_claude_step`, `StepResult`, `OutputMode`, `_MISSING`) and replace it with `prepare_step` + `StepContext`. The file's existing imports (`fill_template`, `CONCEPT_ANALYSIS_DIR`, `TEMPLATES_DIR`) are the right neighborhood for the new helper. `claude.py` stays focused on `invoke_claude` / `invoke_claude_validated` / `run_model`.

Inlining the `run_claude_step` boilerplate at every call site would duplicate ~90 lines of near-identical dir-ensure / prompt-write / dry-run / print / timing code across 5+ sites. FR-12 explicitly permits "a minimal helper for shared concerns like template-filling and dry-run". The helper replaces `run_claude_step` but carries **zero** output-mode logic — it handles only the pre-invocation boilerplate, then hands off to the caller to invoke `invoke_claude_validated` with the validator it knows about.

```python
@dataclass
class StepContext:
    """Return value of prepare_step: pre-invocation artifacts and state.

    NOTE: ``proceed=False`` intentionally collapses two distinct reasons
    (skip-if-exists and dry-run) into one signal — no current call site
    branches on the difference, and both mean "don't invoke Claude now".
    If a future caller needs to distinguish them, add an explicit
    ``reason`` field rather than inferring from other state.
    """
    proceed: bool          # False → caller should continue/skip (dry-run or already-done)
    prompt_text: str       # fully-filled prompt (written to prompt_path only on proceed)
    start_time: float      # for elapsed-time reporting (0.0 when proceed is False)


def prepare_step(
    *,
    step_label: str,
    concept_id: str,
    prompt_text: str,
    prompt_path: Path,
    out_dir: Path,
    skip_if_exists: Path | None = None,
    dry_run: bool = False,
    force: bool = False,
) -> StepContext:
    """Handle the pre-invocation boilerplate shared by every Claude call site.

    - Ensures ``out_dir`` and ``prompt_path.parent`` exist.
    - If ``skip_if_exists`` is set, points to an existing file, and ``force``
      is False: prints a skip message and returns ``proceed=False`` **without
      writing the prompt file** (avoids churning the prompt on skipped runs).
    - If ``dry_run`` is True: writes the prompt (so the operator can inspect
      it), prints a dry-run message, returns ``proceed=False``.
    - Otherwise: writes the prompt, prints the progress header
      ("  {label} {cid} ..."), records ``time.time()`` as ``start_time``,
      and returns ``proceed=True``.

    The helper deliberately does NOT call ``invoke_claude_validated`` — each
    site constructs its own validator and handles its own post-processing,
    which is the part that actually differs between sites.
    """
    out_dir.mkdir(parents=True, exist_ok=True)
    prompt_path.parent.mkdir(parents=True, exist_ok=True)

    # Skip-check BEFORE writing the prompt file — no reason to churn the
    # on-disk prompt when we're about to bail.
    if skip_if_exists is not None and skip_if_exists.exists() and not force:
        print(f"  skip {concept_id} ({skip_if_exists.name} exists, use --force to re-run)")
        return StepContext(proceed=False, prompt_text=prompt_text, start_time=0.0)

    # Dry-run DOES write the prompt so the operator can inspect what would
    # have been sent. This matches `run_claude_step`'s observable behavior.
    prompt_path.write_text(prompt_text, encoding="utf-8")

    if dry_run:
        print(f"  dry-run {concept_id}: {step_label} prompt saved to {prompt_path}")
        return StepContext(proceed=False, prompt_text=prompt_text, start_time=0.0)

    print(f"  {step_label} {concept_id} ...", end="", flush=True)
    return StepContext(proceed=True, prompt_text=prompt_text, start_time=time.time())
```

**Behavioral note vs. `run_claude_step`:** The legacy helper wrote the prompt *before* the skip check (step_runner.py:72-77), so skipped sites still got a fresh prompt file on disk. This rewrite deliberately reorders: **skip → (write → dry-run-bail or proceed)**. The dry-run path still writes the prompt so operators can inspect it, but the skip path no longer touches the file. If any tooling was relying on "prompt file is always refreshed even on skip" (none found), it would need to be re-plumbed — mark this during implementation review.

Typical call site after adoption:

```python
ctx = prepare_step(
    step_label="gap-check",
    concept_id=cid,
    prompt_text=fill_template(template_text, vars_dict),
    prompt_path=out_dir / "prompts" / "gap_check_prompt.md",
    out_dir=out_dir,
    skip_if_exists=gap_path,
    dry_run=args.dry_run,
    force=args.force,
)
if not ctx.proceed:
    continue

result = invoke_claude_validated(
    ctx.prompt_text, cwd=CONCEPT_ANALYSIS_DIR,
    timeout=args.timeout, model=args.model,
    validator=validate_non_empty,
    step_label="gap-check",
)
elapsed = time.time() - ctx.start_time
```

**What the helper does NOT do:**
- No post-hook machinery. `run_claude_step`'s `post_hook` was used by one site (`cmd_review`) and the logic is unique — inline it there.
- No template-filling. Callers already have per-site `build_vars` functions; `fill_template(template_text, vars_dict)` is one line at the caller.
- No output-mode enum. That abstraction is what we're deleting.
- No validator choice. That is exactly what the caller should decide.
- No return-code / validation-passed handling. That belongs to the invocation call.

**Why this passes the "does this earn its existence" test:** The helper is a pure composition of the six operations every call site does identically (mkdir, mkdir, write_text, skip-check, dry-run-bail, print+timing). It adds zero new concepts — no new enums, no new state machines, no new framework. Removing it would mean repeating those six operations at every call site; keeping it means each call site is just the caller's unique logic plus a helper call. The line savings are real (~15 lines/site × 5-7 sites ≈ 75-105 lines), and there is nothing here that risks drifting from the `run_claude_step` anti-pattern because the helper is strictly smaller than `run_claude_step` and does not cross the invocation boundary.

### Component 7: Repurpose `step_runner.py`

After all call sites are migrated to `prepare_step` + `invoke_claude_validated`, the legacy surface of `step_runner.py` is dead code. The file is **repurposed, not deleted** (see Component 6 rationale): its contents are replaced with `prepare_step` + `StepContext`, the obsolete symbols are removed, and the import in `run_analysis.py:77` is updated.

**Removed:** `run_claude_step`, `StepResult`, `OutputMode`, `_MISSING` sentinel, and the associated docstring warning about closure capture in post-hooks (post-hooks no longer exist).

**Retained/added:** `prepare_step`, `StepContext`, along with the existing imports that are still useful for the new helper (`fill_template`, `CONCEPT_ANALYSIS_DIR`, `TEMPLATES_DIR`).

**Import change in `run_analysis.py:77`:**
```python
# Before:
from lib.step_runner import run_claude_step, StepResult
# After:
from lib.step_runner import prepare_step, StepContext
```

`StepResult` is not used by any call site after migration. Each call site works with `ValidatedResult` directly.

#### Test audit: `test_failure_chains.py`

Design-review follow-up. The file contains 9 characterization test classes, one per bug being fixed. Every test asserts that the *current buggy behavior* exists — when the fix lands, these tests will fail unless inverted. They must be updated as part of implementation, not ignored.

**References to `run_claude_step`** (all in characterization tests for bugs this design fixes):

| Line | Test class | Bug under test | Disposition after fix |
|------|------------|---------------|-----------------------|
| 182, 202 | `TestH02_StepRunnerWritesGarbage` | H-02 (file_with_fallback writes conversational text) | **Delete** — the pattern is eliminated by removing `run_claude_step`, so the bug cannot recur. |
| 716, 733 | `TestEndToEnd_MalformedJsonChain` | H-02 chained with H-04 (malformed JSON becomes review.md) | **Delete** — same reason. After the fix, `invoke_claude_validated` never writes parsed event text; the chain cannot form. |

Both test classes are pure "here's how today's code misbehaves" characterization. There is no legitimate behavior we need to preserve — the abstraction they exercise is being removed.

**Other test classes in the same file that must be inverted** (not referenced in the review but part of the same implementation scope):

| Test class | Bug | Action after fix |
|------------|-----|------------------|
| `TestH01_ValidatorReadsWrongData` (3 tests) | H-01 validator falls back to stdout | Invert to assert: file-not-found produces a distinct log entry with `validated_text_preview == "FILE NOT FOUND"` and a fix message containing the path. |
| `TestH03_FeedbackPassNoEditCheck` | H-03 feedback pass doesn't verify modification | Invert: `_run_feedback_pass` returns `False` when `analysis.md` is byte-identical. |
| `TestH04_JsonParseErrorSwallowed` | H-04 silent JSON parse failure | Invert: assert warning is emitted to stderr. |
| `TestH05_EmptyResultText` | H-05 empty result returns empty string | Invert: assert `ValueError` propagates through to the `except` block and the warning fires. |
| `TestH09H10_ValidationPassedIgnored` | H-09/H-10 source-integration and assess don't check `validation_passed` | Invert: assert both early-return `"ERROR"` when validation fails. |
| `TestH17_NoTransientRetry` | H-17 no retry on transient failures | Invert: assert 3 subprocess invocations and backoff sleep. |
| `TestH16_CanonicalOverwriteRegression` | H-16 canonical files overwritten on failed model | Invert: assert canonical files untouched when `model_ok=False`. |
| `TestEndToEnd_FileNotWrittenChain` | H-01 end-to-end | Either delete (covered by unit tests) or invert to assert the H-01 fix catches it cleanly. |
| `TestH20_FrontmatterColonInValue` | H-20 (YAML parser) — **deferred** | Leave as-is; documented as known bug. |
| `TestVerdictParserOnGarbage` | Regression guard on `parse_verdict_from_feedback` | Leave as-is; still useful. |

The characterization-test-inversion work is part of FR-13 / FR-17's "existing tests continue to pass" acceptance criterion. Plan to handle it in the same PR as the corresponding fix, not as a separate test sweep — otherwise the test suite sits red between fix and test update.

**No hidden behavioral coverage.** A second pass through `test_failure_chains.py` confirms: `run_claude_step` is only exercised to prove the H-02 bug. No test uses `run_claude_step` to assert a non-buggy behavior that we need to preserve. Deleting it is safe from a coverage standpoint.

---

## Potential Risks

1. **Retry delays in batch mode**: Worst-case wall-clock cost per concept is larger than it first appears because transient retry (in `invoke_claude`) nests *inside* validation retry (in `invoke_claude_validated`):
   - Transient delays alone: `sum(_TRANSIENT_DELAYS) = 30 + 60 + 120 = 210s ≈ 3.5 min` per `invoke_claude` call.
   - A validated step runs `invoke_claude` once per validation attempt: initial + `max_retries=2` = 3 times.
   - Worst case (every transient retry used, every validation retry used): `3 × 210s = 630s ≈ 10.5 min` of *delays only*, on top of up to `3 × 900s = 45 min` of subprocess timeouts if every call also hangs.
   - Realistic case (one rate-limit burst, first validation attempt recovers after one 30s backoff): ~30s per affected concept.

   For a 20-concept batch where 10 hit rate limits in the realistic case, that is ~5 min of delay total. The worst case is alarming on paper but requires every attempt to fail transiently, which is rare. The alternative (losing concepts and re-running manually) is still worse. Operators running long batches should be aware that transient storms can multiply. If this becomes a problem we can cap total retry time per concept in a follow-up — out of scope for this design.

2. **`validate_file_modified` false negatives**: If Claude re-writes a file identically (same content), the validator rejects it. This is correct behavior — an identical re-write means no progress was made. But it could be confusing if Claude makes a no-op edit (e.g., fixes whitespace that doesn't change the hash). SHA-256 is exact, not semantic. Acceptable tradeoff.

3. **`_parse_json_events` raising ValueError**: Changing from empty string to ValueError changes the contract. Callers that expect empty string will now get an exception. The only caller is `invoke_claude`, which already catches `ValueError` in the `except` block. Safe. **Verification step during implementation:** grep for `_parse_json_events` across `exploration/` and `scripts/` before the change lands, to confirm no downstream code calls it directly. The leading underscore suggests internal-only, but confirm.

4. **Test churn**: Existing tests for `invoke_claude_validated` assume the current behavior (stdout fallback on missing file). These must be updated. About 3-4 tests need changes.

5. **`run_claude_step` removal churn**: 5 call sites need ~20 lines of inlined boilerplate each. Manageable, and the explicit code is more debuggable than the output-mode enum abstraction.

---

## Integration Strategy

### Ordering

Changes are safe to implement bottom-up:

1. **Foundation** (can be done in parallel):
   - `_parse_json_events` raise on no result (H-05)
   - JSON parse warning (H-04)
   - Transient retry in `invoke_claude` (H-17)
   - New validators in `validators.py` (FR-9, FR-10, FR-11)

2. **`invoke_claude_validated` rewrite** (depends on 1):
   - File-existence first-class check (H-01)
   - Fix message augmentation via `_augment_fix_message` (FR-5, FR-6)
   - Validation log text preview (FR-7)
   - Gated `fix_message_sent` logging (only on attempts that actually retry)

3. **Shared helper** (depends on 2):
   - Add `prepare_step` + `StepContext` in `lib/claude.py`

4. **Call site migrations** (depends on 3, can be done per-site):
   - Migrate loop.py sites first (cold-start, feedback-pass, model-setup)
   - Then run_analysis.py sites (gap-check, model-setup, review, synthesize, address-review, external-feedback)
   - Then research.py
   - Delete `step_runner.py` last

5. **Standalone fixes** (independent of 1-4):
   - H-16: canonical file guard
   - H-18: research_log cleanup
   - H-19: verify existing cleanup in `extract_explorer_data.py:797-801` still runs (no code change)
   - S-01, S-02 (rename), S-06/S-07

### Test Strategy

- **Update existing tests**: `test_claude.py` (2 tests for H-05), `test_validated.py` (update file-existence behavior, update attempt-counter fixtures to match 1-indexed loop with `total_attempts = max_retries + 1`)
- **New tests in `test_validated.py`**:
  - File-not-found produces distinct error with path in fix message
  - Attempt escalation displays correct numbers. **Assert on the rendered message string, not just the helper's arguments** — given `max_retries=2` (total=3), after attempt 1 fails the next retry prompt sent to Claude must contain `"attempt 2 of 3"`, after attempt 2 fails it must contain both `"CRITICAL"` and `"FINAL attempt 3 of 3"`, and after attempt 3 fails no retry is sent. The "attempt number displayed is the NEXT attempt, not the one that just failed" semantics is subtle enough that the test should be phrased in terms of "what Claude sees in the prompt string", not "what `_augment_fix_message` returns for inputs X/Y".
  - Final attempt's log entry does NOT contain `fix_message_sent` (confirms the `will_retry` gating).
  - `validated_text_preview` populated for file, stdout, empty, and FILE NOT FOUND cases
- **New tests in `test_validators.py`**:
  - `validate_non_empty` rejects `""`, `"  \n"`, accepts `"x"`
  - `validate_python_syntax` rejects `"def f("`, accepts `"def f(): pass"`, surfaces `lineno` / `msg` in fix message
  - `make_file_modified_validator` — critically, test that a no-op UTF-8 round-trip is **not** falsely reported as modified. Concrete fixture: write a file with `\r\n` line endings, snapshot the factory, re-write identical bytes, verify validator reports unchanged. Also test the BOM case.
- **New test for `prepare_step`**: dry-run returns `proceed=False`, skip-if-exists respects `force`, progress message is printed on real runs, `start_time` is monotonic.
- **Integration test**: Run pipeline on one concept end-to-end after all changes

---

## Validation Approach

1. **Unit tests pass**: `uv run python -m pytest exploration/concept_analysis/scripts/ -v`
2. **Dry-run smoke test**: `uv run python run_analysis.py stage1-all 01 --dry-run` succeeds
3. **Single concept live run**: `uv run python run_analysis.py analyze 01 --max-passes 2` completes with validation logs written
4. **Inspect validation logs**: Check that `validation_log.json` entries include `validated_text_preview` and `fix_message_sent` fields

---

## Review Follow-up Log

### 2026-04-10 — Design review revisions

Addressed in this revision of the design:

**Major 1 — `prepare_step` relocation.** Moved `prepare_step` + `StepContext` from `lib/claude.py` to a repurposed `lib/step_runner.py`. The legacy `run_claude_step`/`StepResult`/`OutputMode` surface is deleted but the file is kept. `claude.py` stays focused on the Claude subprocess boundary. Updated: Architecture diagram (design.md §Architecture), Component 6 header + added design-review decision paragraph, Component 7 retitled from "Delete" → "Repurpose", import change at `run_analysis.py:77` documented.

**Major 2 — `test_failure_chains.py` audit.** All `run_claude_step` references (lines 182, 202, 716, 733) are in pure characterization tests for H-02 and the malformed-JSON chain — both fixed by this design. A full table of the file's 11 test classes and their post-fix disposition (delete vs. invert vs. leave) is now in Component 7. Inversion of characterization tests is planned for the same PR as the corresponding fix to avoid a red test suite between fix and test update. No hidden behavioral coverage found.

Addressed inline as notes rather than structural changes:

- **Minor 3 — `cmd_address_review` validator scope:** Explicit scope decision added to Migration 10 (validate only `analysis.md`, not `model_setup.py`; rationale and revisit condition documented).
- **Minor 4 — `prepare_step` skip before write:** Reordered: skip-check happens before prompt file write. Dry-run still writes so operators can inspect. Behavioral-change note vs. `run_claude_step` added.
- **Minor 5 — `StepContext.proceed` ambiguity:** Dataclass docstring now notes that skip and dry-run intentionally collapse into one signal, and what to do if a future caller needs to distinguish them.
- **Minor 6 — `_augment_fix_message` semantics test:** Test plan now requires asserting on the *rendered prompt string* Claude sees ("attempt 2 of 3", "CRITICAL ... FINAL attempt 3 of 3"), not just the helper's return value.
- **Minor 7 — `cmd_gap_check` stdout-mode documentation:** Added "do not 'fix' this" paragraph calling out that `output_path=None` is deliberate and bypasses H-01 because gap-check is stdout-mode.
- **Minor 8 — `_parse_json_events` grep check:** Added verification step to Potential Risks #3 — grep for direct callers before shipping the ValueError-raising change.

---

**Next Step:** After approval → `/_my_plan`
