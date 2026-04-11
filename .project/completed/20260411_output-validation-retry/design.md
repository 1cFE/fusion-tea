# Design: Output Validation & Retry for Headless Claude Pipeline

**Status:** Complete
**Owner:** Reid W
**Created:** 2026-04-06
**Complexity:** MEDIUM
**Branch:** design-space-explore

## Overview

Add a validate-then-retry layer to `invoke_claude()` that captures session
IDs, runs caller-supplied validators on LLM output, and resumes the
conversation to request fixes when validation fails.

## Related Artifacts

- **Spec:** `.project/active/output-validation-retry/spec.md`
- **Research:** `.project/research/20260406-concept-analysis-fragile-control-flow.md`
- **Current code:** `exploration/concept_analysis/scripts/lib/claude.py` (73 lines)
- **Call sites:** `lib/loop.py`, `lib/step_runner.py`, `run_analysis.py`

## Research Findings

### Current `invoke_claude()` anatomy (`lib/claude.py:7-35`)

```python
def invoke_claude(prompt, cwd, timeout=900, model=None) -> tuple[str, str, int]:
    cmd = ["claude", "-p", "--dangerously-skip-permissions", "--verbose"]
    result = subprocess.run(cmd, input=prompt, capture_output=True, text=True, ...)
    return result.stdout, result.stderr, result.returncode
```

Returns `(stdout, stderr, rc)`. No session ID, no JSON parsing.

### Session ID availability (verified empirically)

`claude -p --output-format json --verbose` produces clean JSON on stdout
(verbose goes to stderr). The JSON is a list of event objects:
- First event: `{"type": "system", "session_id": "uuid", ...}`
- Last event: `{"type": "result", "result": "text response", "session_id": "uuid"}`

`claude -p --resume <session-id> --output-format json` preserves full
conversation context and returns the same JSON structure.

### Call site patterns — two tiers

**Tier A: Direct callers in `loop.py`** (5 functions, all follow same pattern):

| Function | Lines | Parses output? | Validator candidate? |
|----------|-------|----------------|---------------------|
| `_run_cold_start` | 353 | File existence only | No |
| `_run_feedback_pass` | 416 | rc only | No |
| `_run_model_in_iteration` | 487 | File existence + LCOE cosmetic | No |
| `_run_assess` | 604 | **`parse_verdict_from_feedback()`** | **Yes** |
| `_run_source_integration` | 662 | **`parse_verdict_from_feedback()`** | **Yes** |

Pattern: `_stdout, stderr, rc = invoke_claude(prompt, cwd, timeout, model)` →
check rc → check file exists → read file → parse.

**Tier B: `step_runner.py:run_claude_step()`** (wraps `invoke_claude`):
- Used by `cmd_review`, `cmd_gap_check`, `cmd_synthesize`, etc.
- `invoke_claude` call at line 97-99
- Post-hook callback receives `StepResult` with `output_text`
- `cmd_review`'s post-hook does verdict regex parsing → **validator candidate**

**Tier C: `research.py:run_research_step()`** (line 86):
- Parses JSON from agent output file, but filesystem diff is source of truth
- Agent JSON is audit-only, not control flow → **not a validator candidate**

### File-based output dominance

All validator-candidate steps write output to files (Claude uses Write/Edit
tools). The validator reads file contents, not stdout. On retry, Claude
re-writes the file.

### `--verbose` + `--output-format json` compatibility (verified)

`--verbose` output goes to stderr. `--output-format json` controls stdout.
No interference. `subprocess.run(capture_output=True)` separates them.

## Proposed Design

### Component 1: Extended `invoke_claude()` — `lib/claude.py`

Replace the current return type with a result dataclass. Keep the function
name and existing 3-tuple unpacking working via `__iter__`.

```python
@dataclass
class InvokeResult:
    stdout: str
    stderr: str
    returncode: int
    session_id: str | None = None

    def __iter__(self):
        """Backward-compatible unpacking: stdout, stderr, rc = invoke_claude(...)"""
        return iter((self.stdout, self.stderr, self.returncode))
```

Changes to `invoke_claude()`:
1. Add `--output-format json` to the command
2. Parse stdout as JSON event list
3. Extract `session_id` from first event, `result` text from last event
4. Return `InvokeResult` with text result as `stdout` (backward compat)
5. On JSON parse failure (shouldn't happen, but defensive): fall back to
   raw stdout, `session_id=None`

The `__iter__` method means every existing call site that does
`stdout, stderr, rc = invoke_claude(...)` or `_stdout, stderr, rc = ...`
continues to work unchanged. Callers that need session ID access it via
`result = invoke_claude(...); result.session_id`.

### Component 2: Shared format constants and validation protocol — `lib/validators.py` (new file)

**Shared regex constants** — used by both validators and the existing
parsers (`parse_verdict_from_feedback`, `_extract_model_findings`,
`_get_review_feedback`, etc.) to eliminate drift between validation and
consumption:

```python
import re

# Feedback format (assessment, source-integration)
FEEDBACK_VERDICT_RE = re.compile(r"^VERDICT:\s*(PASS|FINDINGS)\s*$", re.MULTILINE)
FINDING_HEADER_RE = re.compile(r"^### F-\d+:", re.MULTILINE)
FINDING_CATEGORY_RE = re.compile(
    r"^\-\s+\**Category\**:?\s*(analysis|model)", re.MULTILINE
)

# Review format
REVIEW_VERDICT_RE = re.compile(r"^VERDICT:\s*(PROCEED|REVISE)\s*$", re.MULTILINE)
CORRECTIVE_ACTIONS_RE = re.compile(r"^## Corrective Actions", re.MULTILINE)
PROPOSED_ACTION_RE = re.compile(r"^### (PA-\d+):\s*(.+)$", re.MULTILINE)
```

These constants replace the inline regex literals in:
- `iteration.py:parse_verdict_from_feedback()` → uses `FEEDBACK_VERDICT_RE`,
  `FINDING_HEADER_RE`
- `loop.py:_extract_model_findings()` → uses `FINDING_HEADER_RE`,
  `FINDING_CATEGORY_RE`
- `loop.py:_get_review_feedback()` → uses `REVIEW_VERDICT_RE` (adapted:
  currently matches just `REVISE`, replace with `REVIEW_VERDICT_RE` and
  check group), `CORRECTIVE_ACTIONS_RE`, `FINDING_HEADER_RE`
- `run_analysis.py:cmd_review._post()` → uses `REVIEW_VERDICT_RE`
- `sources.py:parse_proposed_actions()` → uses `PROPOSED_ACTION_RE`

**Note on anchoring**: The validator regexes use `\s*$` end-anchors
(e.g., `^VERDICT:\s*(PASS|FINDINGS)\s*$`). This is intentionally stricter
than the existing `parse_verdict_from_feedback()` which has no end-anchor.
The stricter pattern catches lines like `VERDICT: PASS — all goals met`
that would match the old regex but indicate the LLM is adding freeform
text on the verdict line. The existing parsers will be updated to use
the same anchored constants — this is a tightening, not a loosening,
and is safe because the prompt contract already specifies the verdict
must be on its own line.

**Validation protocol:**

```python
@dataclass
class ValidationResult:
    valid: bool
    fix_message: str | None = None
    details: str = ""  # human-readable explanation for logging

Validator = Callable[[str], ValidationResult]
```

The validator receives the output text (file contents) and returns whether
it's valid. If invalid, `fix_message` is the prompt sent to Claude on retry.
`details` goes to the validation log.

### Component 3: Validated invocation — `lib/claude.py`

```python
@dataclass
class ValidatedResult:
    """Result of an invoke_claude call with optional validation."""
    invoke: InvokeResult          # final invocation result
    validation_passed: bool       # True if valid (or no validator)
    attempts: int                 # 1 = no retries, 2+ = retried
    log_entries: list[dict]       # validation log entries

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
```

Flow:
1. Call `invoke_claude(prompt, cwd, timeout, model)` — get `InvokeResult`
2. If no validator → return immediately (backward compat path)
3. Read validation target: `output_path.read_text()` if provided, else
   `result.stdout`
4. Run `validator(text)` → `ValidationResult`
5. Log attempt (pass or fail)
6. If valid → return
7. If invalid and retries remain:
   a. Build resume command: `["claude", "-p", "--resume", session_id,
      "--dangerously-skip-permissions", "--verbose", "--output-format", "json"]`
   b. Call with `fix_message` as stdin
   c. Parse result, re-read output file, re-validate
   d. Loop until valid or max retries exceeded
8. Return `ValidatedResult` with final state

**Session ID absence handling**: If `session_id` is None (JSON parse failed
on initial call), skip retry — cannot resume without a session. Log a
warning. Return with `validation_passed=False`.

**Dry-run handling**: `invoke_claude_validated()` does not need its own
`--dry-run` check. All callers gate on `args.dry_run` *before* calling
`invoke_claude()` / `invoke_claude_validated()`, returning early with
`StepResult(status="dry_run")` or a boolean. The validated wrapper is
never reached in dry-run mode.

### Component 4: Concrete validators — `lib/validators.py`

#### `validate_feedback_verdict(text: str) -> ValidationResult`

For Fragilities 1 + 4 (assessment and source-integration output).

```python
def validate_feedback_verdict(text: str) -> ValidationResult:
    # 1. Check verdict line exists (uses shared FEEDBACK_VERDICT_RE)
    verdict_match = FEEDBACK_VERDICT_RE.search(text)
    if not verdict_match:
        return ValidationResult(
            valid=False,
            fix_message=(
                "Your feedback file is missing the required verdict line. "
                "The file MUST contain exactly one line reading either "
                "`VERDICT: PASS` or `VERDICT: FINDINGS` (on its own line, "
                "at the start of the line, with no extra text). "
                "Please re-write the feedback file with the correct format."
            ),
            details="No VERDICT line found matching ^VERDICT:\\s*(PASS|FINDINGS)$",
        )

    # 2. If FINDINGS, check for F-N blocks (uses shared FINDING_HEADER_RE)
    if verdict_match.group(1) == "FINDINGS":
        findings = FINDING_HEADER_RE.findall(text)
        if not findings:
            return ValidationResult(
                valid=False,
                fix_message=(
                    "Your feedback has `VERDICT: FINDINGS` but no finding blocks. "
                    "Each finding MUST use a `### F-N:` header (e.g., `### F-1: Title`). "
                    "Please re-write the feedback file with properly formatted findings."
                ),
                details="VERDICT: FINDINGS but no ### F-N: blocks found",
            )

        # 3. Check Category field on each finding (uses shared constants)
        finding_blocks = re.split(r"(?=^### F-\d+:)", text, flags=re.MULTILINE)
        finding_blocks = [b for b in finding_blocks if FINDING_HEADER_RE.match(b)]
        missing_cat = []
        for block in finding_blocks:
            cat = FINDING_CATEGORY_RE.search(block)
            if not cat:
                header = block.split("\n", 1)[0].strip()
                missing_cat.append(header)

        if missing_cat:
            headers = "; ".join(missing_cat)
            return ValidationResult(
                valid=False,
                fix_message=(
                    f"The following findings are missing a valid Category field: {headers}. "
                    "Each finding MUST include `- **Category:** analysis` or "
                    "`- **Category:** model` on its own line. "
                    "Please re-write the feedback file with Category fields on all findings."
                ),
                details=f"Missing Category on: {headers}",
            )

    return ValidationResult(valid=True, details="Feedback format valid")
```

#### `validate_review_verdict(text: str) -> ValidationResult`

For Fragilities 2 + 3 + 5 (review output).

```python
def validate_review_verdict(text: str) -> ValidationResult:
    # 1. Check verdict line (uses shared REVIEW_VERDICT_RE)
    verdict_match = REVIEW_VERDICT_RE.search(text)
    if not verdict_match:
        return ValidationResult(
            valid=False,
            fix_message=(
                "Your review is missing the required verdict line. "
                "The review MUST contain exactly one line reading either "
                "`VERDICT: PROCEED` or `VERDICT: REVISE` (on its own line). "
                "Please re-write the review file with the correct verdict."
            ),
            details="No VERDICT line matching ^VERDICT:\\s*(PROCEED|REVISE)$",
        )

    # 2. If REVISE, check Corrective Actions section with F-N blocks
    if verdict_match.group(1) == "REVISE":
        ca_match = CORRECTIVE_ACTIONS_RE.search(text)
        if not ca_match:
            return ValidationResult(
                valid=False,
                fix_message=(
                    "Your review has `VERDICT: REVISE` but is missing the "
                    "`## Corrective Actions` section. When the verdict is REVISE, "
                    "you MUST include a `## Corrective Actions` section containing "
                    "`### F-N:` findings that describe what needs to change. "
                    "Please re-write the review file with corrective actions."
                ),
                details="VERDICT: REVISE but no ## Corrective Actions section",
            )

        # Check for F-N blocks after Corrective Actions (uses shared FINDING_HEADER_RE)
        ca_text = text[ca_match.start():]
        findings = FINDING_HEADER_RE.findall(ca_text)
        if not findings:
            return ValidationResult(
                valid=False,
                fix_message=(
                    "Your `## Corrective Actions` section has no findings. "
                    "It MUST contain at least one `### F-N:` finding block. "
                    "Please re-write the review with corrective action findings."
                ),
                details="## Corrective Actions exists but contains no ### F-N: blocks",
            )

    return ValidationResult(valid=True, details="Review format valid")
```

### Component 5: Validation log — written by `invoke_claude_validated()`

Each validation attempt produces a log entry:

```json
{
  "timestamp": "2026-04-06T15:30:00+00:00",
  "step": "assess",
  "attempt": 1,
  "validator": "validate_feedback_verdict",
  "passed": false,
  "details": "No VERDICT line found",
  "fix_message_sent": "Your feedback file is missing..."
}
```

Written as a JSON array to `validation_log.json`. The caller passes `log_path`
to `invoke_claude_validated()`; if omitted, no log is written.

```python
def invoke_claude_validated(
    ...
    log_path: Path | None = None,
    ...
) -> ValidatedResult:
```

The function accumulates `log_entries: list[dict]` internally and writes
them to `log_path` at the end (both success and failure cases). If the file
already exists (multiple validated calls in one iteration), it appends to
the existing array.

### Component 6: Integration into call sites

#### `_run_assess()` — `loop.py:~604`

Current:
```python
_stdout, stderr, rc = invoke_claude(assess_prompt, cwd=..., timeout=..., model=...)
# ... check rc, check file exists ...
feedback_text = feedback_path.read_text(encoding="utf-8")
verdict, finding_count = parse_verdict_from_feedback(feedback_text)
```

Proposed:
```python
result = invoke_claude_validated(
    assess_prompt, cwd=CONCEPT_ANALYSIS_DIR,
    timeout=args.timeout, model=args.model,
    validator=validate_feedback_verdict,
    output_path=feedback_path,
    step_label="assess",
    log_path=iter_dir / "validation_log.json",
)
if result.invoke.returncode != 0:
    # ... existing failure handling ...
if not feedback_path.exists():
    # ... existing failure handling ...
feedback_text = feedback_path.read_text(encoding="utf-8")
verdict, finding_count = parse_verdict_from_feedback(feedback_text)
# validation_passed is informational — parse_verdict_from_feedback still
# does the actual control flow, but now it gets well-formed input
```

The validator doesn't replace `parse_verdict_from_feedback()` — it ensures
the input to that function is well-formed. If max retries are exhausted,
the existing regex parsing runs on whatever Claude last produced (graceful
degradation to current behavior).

#### `_run_source_integration()` — `loop.py:~662`

Same pattern as `_run_assess`. Replace `invoke_claude` with
`invoke_claude_validated`, same validator, same output path.

#### `cmd_review()` — `run_analysis.py:~495` (P0 warning only, no retry)

This goes through `step_runner.py:run_claude_step()`, which doesn't expose
session IDs. Full retry integration requires threading validation through
step_runner (Phase 2). For Phase 1, add the P0 warning from the fragility
audit — this is a standalone `stderr` print, not part of the validation
infrastructure, but it addresses the highest-severity silent failure
(Fragility 2: `has-actions` fallthrough).

```python
# In cmd_review's _post hook, after the existing regex cascade:
if review_status == "has-actions":
    print(f"\n  WARNING: could not detect PROCEED/REVISE verdict in review output."
          f"\n  Defaulting to 'has-actions'. Check review.md manually.", file=sys.stderr)
```

Phase 2 will add `validator` and `max_retries` parameters to
`run_claude_step()` for full retry support on review and other
step_runner-based commands.

## Potential Risks

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| `--output-format json` changes stdout shape for all callers | Certain | High if not handled | `InvokeResult.__iter__` returns text, not JSON — backward compat by construction |
| Claude rewrites *entire* file on retry instead of fixing format | Medium | Low — file is still valid, just regenerated | Acceptable; the fix-up prompt can say "fix the format" not "rewrite everything" |
| Retry succeeds but Claude changes substantive content alongside format fix | Low | Medium — subtle content drift | Fix-up messages explicitly say "re-emit with correct format" not "redo the analysis" |
| Session persistence disabled or session expires | Very low | Retry silently fails | Check `session_id is not None` before attempting retry; log warning |
| JSON parse failure on `--output-format json` stdout | Very low | Falls back to raw stdout | Defensive try/except in `invoke_claude` |

## Integration Strategy

**Phase 1** (this work item):
- Create `lib/validators.py` with shared regex constants, `ValidationResult`,
  and concrete validators
- Migrate existing parsers (`parse_verdict_from_feedback`, `_extract_model_findings`,
  `_get_review_feedback`, `cmd_review._post`, `parse_proposed_actions`) to use
  shared constants from `validators.py` — eliminates regex duplication
- Modify `invoke_claude()` to use `--output-format json` and return `InvokeResult`
- Add `invoke_claude_validated()` wrapper
- Integrate into `_run_assess()` and `_run_source_integration()`
- Add P0 WARNING in `cmd_review`'s `_post` hook for `has-actions` fallthrough

**Phase 2** (future):
- Add `validator` parameter to `run_claude_step()` for full step_runner integration
- Integrate review validator into `cmd_review` with retry capability
- Consider validators for PA-N block format (Fragility 5)

## Validation Approach

### Automated
- Unit tests for `validate_feedback_verdict` and `validate_review_verdict`
  with known-good and known-bad inputs
- Unit test for `InvokeResult.__iter__` backward compatibility
- Unit test for JSON event stream parsing (mock subprocess output)

### Manual
- Run `stage1-all` on a concept with `--max-passes 2` and verify
  `validation_log.json` appears in `iter-N/`
- Intentionally malform a feedback.md (remove VERDICT line) and verify
  retry fires (can test by adding a pre-validation hook that corrupts
  output, or by using `--dry-run` to inspect prompts)
- Run parallel concepts and verify session IDs are distinct

### Regression
- All existing callers of `invoke_claude()` that use 3-tuple unpacking
  must continue working without changes
- `--dry-run` mode must be unaffected (no validation runs on dry-run)

---

**Next Step:** After approval → `/_my_plan` or `/_my_implement`
