# Spec: Step Runner Validation & Retry Integration

**Status:** Draft
**Owner:** Reid W
**Created:** 2026-04-06
**Complexity:** LOW
**Branch:** design-space-explore

---

## Business Goals

### Why This Matters

The output-validation-retry infrastructure (`invoke_claude_validated()`) already
works for direct `invoke_claude()` callers in `loop.py`. But commands that go
through `step_runner.py:run_claude_step()` — notably `cmd_review` — can't use
it. When `cmd_review` produces a malformed verdict (no `VERDICT: PROCEED` or
`VERDICT: REVISE` line), the pipeline falls through to `has-actions` with a
stderr warning instead of retrying. This is the exact class of failure the
validation-retry infrastructure was built to fix.

This is the "Phase 2" explicitly deferred in
`.project/active/output-validation-retry/design.md` (Integration Strategy).

### Success Criteria

- [ ] `run_claude_step()` callers can opt into validation with a callback,
      same as `invoke_claude_validated()` callers
- [ ] `cmd_review` uses `validate_review_verdict` with retry-via-resume
- [ ] The P0 stderr warning in `cmd_review` becomes a last-resort fallback
      (fires only if max retries exhausted), not the primary defense
- [ ] All other `run_claude_step()` callers continue to work unchanged

### Priority

P2. The P0 warning already catches the failure visibly. This upgrades from
"warn and degrade" to "fix automatically." Not urgent but completes the
validation-retry story.

---

## Problem Statement

### Current State

`run_claude_step()` (`step_runner.py:45-153`) calls `invoke_claude()` at
line 97, unpacks `(stdout, stderr, rc)`, and builds a `StepResult`. It has
no access to session IDs and no mechanism to re-invoke Claude on validation
failure. The post-hook runs *after* the invocation is complete — it can
inspect output but can't trigger a retry.

`cmd_review`'s post-hook (`run_analysis.py:476-501`) parses the review
verdict with `REVIEW_VERDICT_RE`. If neither PROCEED nor REVISE is detected,
it falls through to `has-actions` with a warning. There is no retry.

### Desired Outcome

`run_claude_step()` accepts optional `validator`, `max_retries`, and
`log_path` parameters. When provided, it uses `invoke_claude_validated()`
instead of `invoke_claude()`, gaining session-ID-tracked retry-via-resume.
The post-hook still runs after validation succeeds (or after max retries
are exhausted), so it can inspect the final output as before.

---

## Scope

### In Scope

- Add `validator`, `max_retries`, and `log_path` parameters to
  `run_claude_step()`
- Switch internal invocation to `invoke_claude_validated()` when a
  validator is provided
- Thread session ID and validation metadata through `StepResult`
- Integrate `validate_review_verdict` into `cmd_review`
- Remove or demote the P0 warning to a post-max-retries fallback

### Out of Scope

- Adding validators to `cmd_gap_check`, `cmd_synthesize`, or other
  step_runner callers (they don't parse output for control flow)
- Changes to the validator implementations themselves
- Changes to `invoke_claude_validated()` or `invoke_claude()`

### Edge Cases & Considerations

- **`StepResult` needs session ID**: Currently `StepResult` has no
  `session_id` field. Adding it is backward-compatible (new optional field).

- **Output mode interaction**: `run_claude_step()` has 4 output modes
  (`stdout_to_file`, `file_with_fallback`, `file_exists`, `no_output`).
  Validation MUST happen *after* the output mode logic resolves the
  output text, since the validator needs the file contents, not raw
  stdout (which is now JSON events).

- **Post-hook ordering**: The post-hook MUST run after validation
  completes (pass or fail), not between initial invocation and retry.
  The post-hook receives the *final* `StepResult` with validated output.

- **Backward compatibility**: Callers that don't pass `validator` MUST
  get identical behavior. The `invoke_claude()` → 3-tuple unpacking
  path should remain the default.

---

## Requirements

### Functional Requirements

> Requirements below are from user's request unless marked [INFERRED].

#### FR-1: Optional validator parameter on `run_claude_step()`

`run_claude_step()` MUST accept a `validator: Validator | None` parameter
(default `None`). When provided, the step runner MUST use
`invoke_claude_validated()` instead of bare `invoke_claude()`.

#### FR-2: Validation uses output_path contents

The validator MUST receive the resolved output text (file contents from
`output_path`), not raw stdout. This matches how `invoke_claude_validated()`
works when given an `output_path`.

#### FR-3: Session ID in StepResult

`StepResult` MUST expose the session ID from the invocation so that
callers and post-hooks can reference it. This SHOULD be an optional
field defaulting to `None`.

#### FR-4: [INFERRED] Validation metadata in StepResult

`StepResult` SHOULD include `validation_passed: bool` and
`attempts: int` fields so post-hooks can adjust behavior based on
whether validation succeeded.

#### FR-5: cmd_review integration

`cmd_review` MUST pass `validator=validate_review_verdict` and
`log_path` pointing to the concept's `prompts/` directory. The existing
P0 warning SHOULD remain as a fallback for when max retries are
exhausted (i.e., `validation_passed is False`).

#### FR-6: Backward compatibility

Callers that do not supply a validator MUST get identical behavior to
today. No existing call site should require changes unless opting into
validation.

---

## Acceptance Criteria

### Core Functionality
- [ ] `run_claude_step()` accepts `validator`, `max_retries`, `log_path`
- [ ] When validator is provided, uses `invoke_claude_validated()` internally
- [ ] Validation runs on resolved output text (post output-mode logic)
- [ ] Post-hook receives final StepResult after all validation attempts
- [ ] `StepResult` includes `session_id`, `validation_passed`, `attempts`

### Integration
- [ ] `cmd_review` passes `validate_review_verdict` as validator
- [ ] Validation log written to concept's `prompts/validation_log.json`
- [ ] P0 warning fires only when validation_passed is False (max retries exhausted)
- [ ] All other `run_claude_step()` callers unchanged and passing

### Quality
- [ ] Existing tests pass (98/98)
- [ ] New tests for `run_claude_step()` with validator (mocked)
- [ ] Manual test: run `review` on a concept, verify `validation_log.json` created

---

## Related Artifacts

- **Prior work:** `.project/active/output-validation-retry/` (spec, design, plan — Phase 1 complete)
- **Design reference:** `.project/active/output-validation-retry/design.md` — Component 6 and Integration Strategy Phase 2
- **Step runner:** `exploration/concept_analysis/scripts/lib/step_runner.py`
- **Review command:** `exploration/concept_analysis/scripts/run_analysis.py:476-515`
- **Validators:** `exploration/concept_analysis/scripts/lib/validators.py`

---

**Next Steps:** After approval, proceed to `/_my_design`
