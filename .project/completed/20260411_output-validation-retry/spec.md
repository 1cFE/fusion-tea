# Spec: Output Validation & Retry for Headless Claude Pipeline

**Status:** Complete
**Owner:** Reid W
**Created:** 2026-04-06
**Complexity:** MEDIUM
**Branch:** design-space-explore

---

## Business Goals

### Why This Matters

The concept analysis pipeline makes control flow decisions by regex-parsing
free-text LLM output (verdicts, finding categories, review sections). When
Claude's formatting deviates from the expected patterns, the pipeline silently
degrades: extra iterations, stuck concepts, or discarded review feedback. The
fragility audit (`.project/research/20260406-concept-analysis-fragile-control-flow.md`)
identified 5 Tier-1 fragilities where the producer is an LLM and there is
currently zero validation between "Claude wrote something" and "we parsed it
for control flow."

This feature adds a validate-then-retry layer: after each Claude invocation,
run a caller-supplied validator on the output. If validation fails, continue
the *same* conversation (via `claude -p --resume <session-id>`) with a
targeted fix-up prompt explaining what was wrong. This preserves the full
context window — Claude can see what it wrote and fix just the formatting
issue — and avoids the cost of a full re-run.

### Success Criteria

- [ ] Pipeline steps that parse LLM output for control flow can opt into
      validation with a callback
- [ ] Validation failures produce a retry via conversation continuation
      (not a fresh invocation)
- [ ] Session IDs are explicitly tracked (no reliance on "most recent"
      which breaks under parallel runs)
- [ ] Retries are capped to prevent infinite loops
- [ ] All validation attempts and outcomes are logged to a per-invocation
      log file for debugging
- [ ] Existing behavior is unchanged for callers that don't opt in

### Priority

P1. The fragility audit's P0 items (add warnings) are trivial and can ship
independently. This spec addresses the P1/P2 structural fix.

---

## Problem Statement

### Current State

`invoke_claude()` returns `(stdout, stderr, returncode)`. Callers check
`rc != 0` and whether an output file exists, then immediately parse the
output with regex for control flow. There is no validation step and no
mechanism to ask Claude to fix a malformed output.

Session IDs are not captured — `invoke_claude()` discards them because it
reads stdout as plain text (`claude -p` without `--output-format`).

### Desired Outcome

A reusable validation-retry wrapper around `invoke_claude()` that:
1. Captures the session ID from the initial invocation
2. Runs a caller-supplied validator on the output
3. On failure, resumes the conversation with a fix-up message
4. Returns the final output (plus metadata about retries) to the caller

---

## Scope

### In Scope

- New `invoke_claude_validated()` function in `lib/claude.py` (or new module)
- Session ID capture via `--output-format json` parsing
- Validator callback protocol (signature, return type, fix-up message)
- Retry loop with configurable max attempts
- Per-invocation validation log
- Concrete validators for Fragilities 1, 2, 3, 4, 5 (see Applicability
  section)
- Integration into call sites that currently do post-hoc regex parsing

### Out of Scope

- Changing prompt templates to produce structured JSON (that's a separate,
  complementary effort)
- Tier-2 fragilities (6, 7) — these parse pipeline-written data, not LLM
  output; retry doesn't apply
- Retry on `rc != 0` (that's an invocation failure, not an output format
  issue)
- Changes to `step_runner.py` integration (see Edge Cases)

---

## Edge Cases & Considerations

- **`step_runner.py` vs direct callers**: The pipeline has two invocation
  patterns. `step_runner.py:run_claude_step()` wraps `invoke_claude()` for
  commands like `review`, `gap-check`, `synthesize`. The loop functions
  (`loop.py`) call `invoke_claude()` directly for `analyze`, `assess`,
  `model-setup`, and `source-integration`. The validation infrastructure
  MUST work with both patterns; however, integration with `step_runner` is
  deferred — initial validators target the direct-call sites in `loop.py`
  where the control-flow parsing happens.

- **`--output-format json` changes stdout shape**: Currently `invoke_claude()`
  returns raw stdout (Claude's text response). With `--output-format json`,
  stdout is a JSON event stream. The function MUST parse the JSON to extract
  the text result *and* the session ID, and return the text result in the
  same position so callers are not broken.

- **File-based output**: Most pipeline steps have Claude write to a file
  (via the Write/Edit tools), not stdout. The validator receives the
  *file contents* (which the caller already reads post-invocation), not
  stdout. The retry prompt tells Claude to re-emit/fix the file.

- **Parallel runs**: Multiple concepts run concurrently. Each invocation
  gets its own session ID. The infrastructure MUST NOT use `--continue`
  (which resumes "most recent in cwd"). It MUST use
  `--resume <session-id>`.

- **Cost of retries**: Each retry is a conversation continuation, not a
  new invocation. Context is already loaded, so the marginal cost is low
  (just the fix-up prompt + response). But retries still cost money — the
  max-retries cap prevents runaway spend.

- **Existing `--verbose` flag**: We currently pass `--verbose` to
  `claude -p`. MUST verify this is compatible with `--output-format json`.

---

## Requirements

### Functional Requirements

> Requirements below are from user's request unless marked [INFERRED].

#### FR-1: Session ID tracking

`invoke_claude()` (or a new wrapper) MUST capture the session ID from each
invocation. It MUST use `--output-format json` to parse the session ID from
the event stream, and MUST extract the text result from the `type: "result"`
event. The session ID MUST be returned to the caller (as part of an extended
return type or result object).

#### FR-2: Validator callback protocol

The validation function MUST follow a common signature:

```python
def validator(output_text: str) -> ValidationResult
```

Where `ValidationResult` is a dataclass/namedtuple containing:
- `valid: bool` — whether the output passes validation
- `fix_message: str | None` — if invalid, the message to send as the
  retry prompt. The validator is responsible for composing a clear,
  specific fix-up message that tells Claude exactly what format is
  expected and what was wrong.

The validator receives the output text (file contents or stdout, depending
on the step). It does NOT receive the raw JSON event stream.

#### FR-3: Retry via conversation continuation

When validation fails, the infrastructure MUST resume the conversation
using `--resume <session-id>` with the validator's `fix_message` as the
prompt. The retry invocation MUST use the same `--output-format json` to
capture the new session ID (in case further retries are needed, though
the session ID should remain stable across resumes).

After retry, the infrastructure MUST re-read the output (file or stdout)
and re-run the validator. If the output file was the validation target,
Claude is expected to re-write it in the retry.

#### FR-4: Max retry cap

The infrastructure MUST accept a `max_retries` parameter (default: 2).
After `max_retries` failed validation attempts, it MUST stop retrying and
return the last output with a validation-failure indication. The caller
decides whether to treat this as a hard failure or proceed with degraded
parsing (current behavior).

#### FR-5: Validation log

Each invocation that uses validation MUST produce a log entry containing:
- Timestamp
- Step name / context identifier
- Attempt number (1 = initial, 2+ = retries)
- Validator name or description
- Pass/fail
- If failed: the fix-up message sent
- If passed after retry: which attempt succeeded

The log SHOULD be written to the iteration directory (e.g.,
`iter-N/validation_log.json`) as an append-friendly JSON-lines or
JSON-array file. For steps outside the iteration loop (e.g., review),
the log SHOULD go to the concept's `prompts/` directory.

#### FR-6: Backward compatibility

Callers that do not supply a validator MUST get identical behavior to
today. The validation infrastructure MUST be opt-in. The return type
change (adding session ID and validation metadata) MUST NOT break
existing callers — either through a new function name, an extended
return type with backward-compatible unpacking, or a result object
that the caller can ignore.

#### FR-7: [INFERRED] Validator implementations for Tier-1 fragilities

Concrete validators MUST be provided for each applicable fragility.
See the Applicability Matrix below for which fragilities are covered
and the validation logic for each.

---

## Applicability Matrix

Which fragilities from the audit can use validate-and-retry, and what
does each validator check?

### Fragility 1: Assessment/Source-Integration Verdict — APPLICABLE

**Call site**: `loop.py:_run_assess()` (line ~604), `loop.py:_run_source_integration()` (line ~662)
**Output**: `iter-N/feedback.md` (file written by Claude)
**Current parsing**: `parse_verdict_from_feedback()` — regex for `^VERDICT:\s*PASS` and `^### F-\d+:`

**Validator logic**:
1. Check that output contains a line matching `^VERDICT:\s*(PASS|FINDINGS)\s*$`
2. If VERDICT is FINDINGS, check that at least one `^### F-\d+:` block exists
3. If VERDICT is FINDINGS, check each finding has a `Category` field matching `analysis|model`

**Fix-up message template**:
> Your feedback output is missing the required format. The file MUST begin
> with a verdict line: exactly `VERDICT: PASS` or `VERDICT: FINDINGS` on
> its own line. Each finding MUST use `### F-N:` headers and include a
> `- **Category:** analysis | model` field. Please re-write the feedback
> file with the correct format.

**Impact**: Eliminates false-FAIL from missing/malformed verdict. Also
addresses Fragility 4 (category routing) by validating Category fields
in the same pass.

### Fragility 2: Review Verdict — APPLICABLE

**Call site**: `run_analysis.py:cmd_review()` (via `step_runner`, line ~495)
**Output**: `review.md` (file written by Claude)
**Current parsing**: regex cascade for PROCEED/REVISE/legacy

**Validator logic**:
1. Check that output contains a line matching `^VERDICT:\s*(PROCEED|REVISE)\s*$`
2. If REVISE, check that a `## Corrective Actions` section exists
3. If REVISE, check that at least one `### F-\d+:` block exists under Corrective Actions
4. If PROCEED, optionally check for `### PA-\d+:` blocks (non-blocking — PAs are optional)

**Fix-up message template**:
> Your review output is missing the required verdict format. The review
> MUST contain exactly one verdict line: `VERDICT: PROCEED` or
> `VERDICT: REVISE` on its own line. If REVISE, there MUST be a
> `## Corrective Actions` section containing `### F-N:` findings.
> If PROCEED, any proposed actions MUST use `### PA-N:` headers.
> Please re-write the review file with the correct format.

**Impact**: Eliminates the `has-actions` fallthrough (Fragility 2) and
the silent discard of corrective actions (Fragility 3) in one validator.

### Fragility 3: Review Feedback Extraction — COVERED BY FRAGILITY 2

The Fragility 2 validator already ensures `## Corrective Actions` + `### F-N:`
blocks exist when REVISE is the verdict. No separate validator needed.

### Fragility 4: Finding Category Routing — COVERED BY FRAGILITY 1

The Fragility 1 validator already checks that each finding has a valid
`Category` field. No separate validator needed.

### Fragility 5: Proposed Actions Parsing — APPLICABLE (low priority)

**Call site**: `run_analysis.py:cmd_review()` (same as Fragility 2)
**Output**: `review.md`
**Current parsing**: `parse_proposed_actions()` — regex for `### PA-N:` and field patterns

**Validator logic** (extend the Fragility 2 validator):
1. If PROCEED and `### PA-\d+:` blocks exist, check each has the required
   fields: Category, Severity, Location, Finding, Proposed Fix, Decision
2. Check that field values use `- **Key:** Value` format

**Impact**: Prevents address-review from receiving unparseable PA-N blocks.
Low priority because PA-N parsing failures are recoverable (human re-runs
review).

### Fragility 6: Frontmatter String Conventions — NOT APPLICABLE

Producer is the pipeline itself, not an LLM. Fix with string constants,
not retry.

### Fragility 7: Model Output Validation — NOT APPLICABLE

Producer is an LLM-generated Python script, not a Claude conversation.
The script runs via `uv run python`, not `claude -p`. No session to resume.

---

## Acceptance Criteria

### Core Functionality
- [ ] `invoke_claude()` (or wrapper) captures session ID via `--output-format json`
- [ ] Session ID is returned to caller without breaking existing call sites
- [ ] Validator callback receives output text, returns `(valid, fix_message)`
- [ ] Failed validation triggers `--resume <session-id>` with fix message
- [ ] Retries capped at configurable max (default 2)
- [ ] Validation log written per-invocation with attempt details

### Validators
- [ ] Assessment verdict validator catches missing/malformed `VERDICT:` line
- [ ] Assessment verdict validator catches missing `Category` field on findings
- [ ] Review verdict validator catches missing PROCEED/REVISE verdict
- [ ] Review verdict validator catches missing `## Corrective Actions` on REVISE

### Integration
- [ ] `_run_assess()` in `loop.py` uses assessment verdict validator
- [ ] `_run_source_integration()` in `loop.py` uses assessment verdict validator
- [ ] `cmd_review()` in `run_analysis.py` uses review verdict validator
- [ ] All other callers of `invoke_claude()` continue to work unchanged
- [ ] `--dry-run` mode is unaffected

### Quality & Edge Cases
- [ ] Parallel runs: each invocation tracks its own session ID
- [ ] `--verbose` and `--output-format json` work together without conflict
- [ ] Retry with `--resume` preserves conversation context (verified manually)
- [ ] Max retries exceeded: caller receives output + failure indication, can
      fall back to current regex behavior
- [ ] Validation log is valid JSON and includes all required fields

---

## Related Artifacts

- **Research:** `.project/research/20260406-concept-analysis-fragile-control-flow.md`
- **Design:** `.project/active/output-validation-retry/design.md` (to be created)
- **Pipeline README:** `exploration/concept_analysis/README.md`
- **Current invocation code:** `exploration/concept_analysis/scripts/lib/claude.py`
- **Current step runner:** `exploration/concept_analysis/scripts/lib/step_runner.py`

---

**Next Steps:** After approval, proceed to `/_my_design`
