# Spec: Analysis Loop Symmetry & Cleanup

**Status:** Draft
**Owner:** Reid W
**Created:** 2026-04-13
**Complexity:** MEDIUM
**Branch:** TBD

---

## Business Goals

### Why This Matters

The concept analysis pipeline has three related problems that compound to waste iterations and produce worse models:

1. **Model feedback starvation.** Assessment findings tagged `Category: analysis` never reach the model agent. Dual-target findings (needing both prose and model changes) get tagged `analysis` because the assessor picks a "primary" target. The model agent never sees them. It takes a full extra iteration for the assessor to re-raise the finding as `Category: model`. Evidence: Concept 16 iter-1 (0/3 findings reached model), Concept 17b iter-2 (availability sweep tagged `analysis` → model blind → iter-3 re-raised).

2. **Model has no continuity across iterations.** The analysis agent reads its prior `analysis.md` and makes targeted edits. The model agent writes a fresh `model_setup.py` from scratch every iteration to a new `iter-N/` path. It never sees its own prior model. If iter-2 had 5 sensitivity sweeps and iter-3 feedback says "add one more," the model agent must independently reproduce all 5 + the addition, working only from the analysis text and findings. Sweeps silently regress.

3. **`stage1-all` is a footgun.** It's a thin wrapper that calls `cmd_analyze` (which already runs model-setup in-loop), then calls standalone `cmd_model_setup` again with no feedback, then `cmd_review`. With `--force`, the standalone model-setup overwrites the loop's feedback-driven model with a dumber version. Without `--force`, it's dead code. The only value is chaining review after analyze — a one-liner.

### Success Criteria

- [ ] Model agent receives ALL assessment findings, with guidance to ignore analysis-only ones
- [ ] Model agent sees and edits its prior iteration's model, not a blank slate
- [ ] `stage1-all` command removed
- [ ] No wasted iterations due to feedback routing or model regression
- [ ] Existing pipeline behavior unchanged for cold-start (iter-1)

### Priority

High — blocking convergence for active concepts. Each wasted iteration = ~$2-5 + pipeline time.

---

## Problem Statement

### Current State

**Feedback starvation** (RESOLVED): `extract_findings()` already passes all findings (old filter removed). Assessment template updated to treat Category as informational metadata. Model-setup templates have framing notes for mixed-category findings. See Section B below — marked as completed, no implementation work remains.

**Model amnesia** (`lib/loop.py:475-552`): `_run_model_in_iteration()` writes to `iter_dir / "model_setup.py"` — a fresh path every iteration. `build_model_vars()` (loop.py:555-609) constructs template variables with `analysis_path` and `model_feedback` but no reference to any prior iteration's model script. The model-setup templates (`model_setup_costingfe.md`, `model_setup_freeform.md`) instruct Claude to "Write a self-contained Python script" — pure creation, no edit path.

**stage1-all** (`run_analysis.py:994-1036`): Calls `cmd_gap_check` (optional) → `cmd_analyze` → `cmd_model_setup` → `cmd_review` sequentially with the same `args` namespace. The standalone `cmd_model_setup` has `skip_if_exists` logic but `--force` propagates from stage1-all, bypassing the guard.

### Desired Outcome

1. Model agent receives all findings with clear guidance on which to act on.
2. Model agent reads its prior model and makes targeted edits (symmetry with analysis agent).
3. `stage1-all` removed. Users chain `analyze` + `review` explicitly.

---

## Scope

### In Scope

#### A. Remove `stage1-all`

1. Remove `cmd_stage1_all()` function from `run_analysis.py`
2. Remove `stage1-all` from CLI parser (`build_parser()`)
3. Remove `stage1-all` from dispatch table
4. Update script docstring/usage examples

#### B. Fix model feedback starvation — COMPLETED (no implementation work)

Already implemented earlier this session:
1. `extract_findings()` passes all findings (old `extract_model_findings()` filter removed)
2. Model-setup templates have framing note for mixed-category findings
3. Assessment template updated — Category is informational metadata, not a routing gate

The implementing agent should verify these are still in place but NOT re-implement them.

#### C. Add model continuity (edit-not-rewrite)

1. **`_run_model_in_iteration()`**: On iter > 1, copy the best prior `model_setup.py` into the current `iter-N/` directory BEFORE invoking Claude. "Best prior" = most recent iteration where `model_ok=True` (from verdict.json), falling back to concept-root canonical copy, falling back to nothing (cold start).
2. **`build_model_vars()`**: Add a `prior_model_path` variable pointing to the copied prior model in the current iter dir (or empty string on cold start).
3. **Model-setup templates**: Add a conditional `feedback_pass` mode (mirroring analysis_v2.md's structure):
   - **Cold start** (no prior model): Current behavior — "Write a self-contained Python script"
   - **Feedback pass** (prior model exists): "Read the existing model at `{{prior_model_path}}`. Apply the assessment findings using the Edit tool. Do NOT rewrite from scratch. Maintain all existing sweeps, scenarios, and parameters unless a finding specifically says to change them."
4. **Validation**: For feedback pass, use `make_file_modified_validator` on the copied model file (symmetry with analysis feedback-pass validation). For cold start, keep `validate_python_syntax`.
   - **Both modes**: After the primary validator, also run `validate_python_syntax` to catch syntax errors introduced by edits. The feedback-pass validator becomes a chain: file-modified AND python-syntax.

### Out of Scope

- Adding a `both` category value to findings (unnecessary — all findings visible to both agents)
- Changing the 3-finding-per-pass limit
- Re-running stalled concepts (separate operational step)
- Changes to `FINDING_CATEGORY_RE` validator (category field stays as metadata)
- Changes to the analysis agent's feedback path (already receives everything)
- Changes to verdict.json schema
- Changes to research, source-integration, or review steps
- Adding a "model review" or model-specific assessment pass
- Replacing `cmd_model_setup` standalone command — intentionally kept as a clean-regeneration tool (writes from scratch with no prior model context). Its purpose is one-off model rebuilds when the user wants a fresh start, distinct from the in-loop edit-based flow.

### Edge Cases & Considerations

1. **Cold start (iter-1)**: No prior model exists. Behavior identical to today — write from scratch, validate with `validate_python_syntax`.

2. **Prior model had syntax errors (`model_ok=False`)**: The copy logic selects the most recent `model_ok=True` iteration. If NO prior iteration had a passing model, fall back to concept-root canonical `model_setup.py`. If that also doesn't exist, cold-start behavior.

3. **All findings are `Category: analysis`**: Model-setup still runs — analysis edits may shift parameter values or framing that the model should reflect. However, the file-modified validator is relaxed: when zero findings are tagged `Category: model`, validation only checks python syntax (not file-modified). The model agent can make changes if it sees a need, but isn't penalized for a no-op. This avoids the no-win of forcing the agent to run then failing it for not changing anything.

4. **`--force` on analyze**: Clears iterations, starts from iter-1 cold start. No continuity needed — this is intentional fresh start.

5. **`--resume` after a model failure**: Prior iteration has `model_ok=False`. The copy logic walks backward to find the last `model_ok=True` iteration. If none found, cold start.

6. **Template variable empty string**: `model_feedback` is empty string on cold start (no findings). `prior_model_path` is empty string when no prior model exists. Both templates already handle empty `model_feedback` via `{{#if model_feedback}}` conditionals. Add same pattern for `prior_model_path`.

---

## Requirements

### Functional Requirements

**A. Remove stage1-all**

1. **FR-A1**: The `stage1-all` subcommand MUST be removed from the CLI parser, dispatch table, and handler function.
2. **FR-A2**: The script docstring and usage examples MUST be updated to remove `stage1-all` references.

**B. Fix model feedback starvation — COMPLETED (verify only)**

3. **FR-B1** (done): `extract_findings()` returns all findings regardless of Category tag.
4. **FR-B2** (done): Model-setup prompt templates include framing note for mixed-category findings.
5. **FR-B3** (done): Assessment template treats Category as informational metadata.
6. **FR-B4** (done): Empty-feedback path unchanged.

*Implementing agent: verify these are in place, do not re-implement.*

**C. Add model continuity**

7. **FR-C1**: On iterations > 1, `_run_model_in_iteration()` MUST copy the best available prior `model_setup.py` into the current `iter-N/` directory before invoking Claude.
8. **FR-C2**: "Best available" is defined as: most recent iteration with `model_ok=True` in `verdict.json`, falling back to concept-root `model_setup.py`, falling back to nothing (cold start).
9. **FR-C3**: `build_model_vars()` MUST include a `prior_model_path` template variable pointing to the copied file (or empty string on cold start).
10. **FR-C4**: Model-setup templates MUST support two modes via conditional blocks:
    - Cold start (`prior_model_path` empty): "Write a self-contained Python script" (current behavior)
    - Feedback pass (`prior_model_path` set): "Read the existing model. Apply findings using Edit tool. Do NOT rewrite from scratch."
11. **FR-C5**: Feedback-pass model validation MUST be tiered based on whether any findings are tagged `Category: model`:
    - **Has model findings**: Chain validator — (a) file was modified (SHA-256 changed) AND (b) valid Python syntax.
    - **No model findings** (all `Category: analysis`): Validate python syntax only. The model agent may make changes but is not required to.
12. **FR-C6**: Cold-start model validation remains `validate_python_syntax` only (current behavior).
13. **FR-C7**: Model-setup MUST always run when a prior model exists, even if all findings are `Category: analysis`. Analysis edits may shift parameter values or framing that the model should reflect. The tiered validation in FR-C5 ensures the agent isn't penalized for a no-op when no findings target the model.

### Non-Functional Requirements

- No new dependencies
- No changes to verdict.json schema or iteration directory structure (beyond adding the copied prior model file)
- Model continuity must not break `--force` semantics (force = clean slate = cold start)
- Model continuity must not break `--resume` semantics (resume picks up from last iteration)

---

## Acceptance Criteria

### A. stage1-all removal

- [ ] `run_analysis.py stage1-all` produces "unknown command" error
- [ ] No references to `stage1-all` or `cmd_stage1_all` remain in codebase
- [ ] Script docstring updated

### B. Feedback starvation fix

- [ ] All F-N findings from assessment appear in model-setup prompt (inspect prompt file for a concept with mixed-category findings)
- [ ] Model-setup prompt contains framing note about ignoring analysis-only findings
- [ ] Assessment template no longer says "assign primary target"
- [ ] Empty-feedback path (cold start) unchanged

### C. Model continuity

- [ ] Iter-2+ model-setup prompt references a prior model path in the current iter dir
- [ ] The prior model file exists in `iter-N/` before Claude invocation (copied from best prior)
- [ ] Claude is instructed to Edit (not Write) the model in feedback-pass mode
- [ ] Validation checks file-modified AND python-syntax when model-targeted findings exist
- [ ] Validation checks python-syntax only when all findings are `Category: analysis`
- [ ] Cold start (iter-1 or no prior passing model) still works as today
- [ ] When all findings are `Category: analysis`, model-setup still runs (model may need to reflect analysis changes)
- [ ] `--force` starts from cold start (no prior model copy)
- [ ] `--resume` correctly walks back to last `model_ok=True` iteration

### Regression

- [ ] Existing `--dry-run` behavior unchanged
- [ ] Existing `--feedback` (external feedback apply) unchanged
- [ ] Existing `--research` behavior unchanged
- [ ] Source-integration feedback still reaches model agent
- [ ] Review kick-back feedback still reaches model agent

---

## Related Artifacts

- **Research:** `.project/research/20260413-run-analysis-analyze-stage1all-audit.md`
- **Prior spec:** This file's prior version (model-feedback-starvation only, 2026-04-13 07:42)
- **Code:** `exploration/concept_analysis/scripts/run_analysis.py` (cmd_analyze, cmd_stage1_all, cmd_model_setup, build_parser)
- **Code:** `exploration/concept_analysis/scripts/lib/loop.py` (run_stage1_loop, _run_model_in_iteration, build_model_vars, extract_findings)
- **Code:** `exploration/concept_analysis/scripts/lib/validators.py` (make_file_modified_validator, validate_python_syntax)
- **Code:** `exploration/concept_analysis/scripts/lib/iteration.py` (read_loop_state, verdict parsing)
- **Templates:** `exploration/concept_analysis/prompt_templates/assessment.md`
- **Templates:** `exploration/concept_analysis/prompt_templates/model_setup_costingfe.md`
- **Templates:** `exploration/concept_analysis/prompt_templates/model_setup_freeform.md`

---

## Implementation Notes

### Suggested order

1. **FR-A1/A2** — Remove stage1-all (clean, independent, no risk)
2. **FR-B1-B4** — Already done. Verify only.
3. **FR-C1-C7** — Model continuity (the actual work)

### Tiered validator pattern (FR-C5)

The feedback-pass model validation is tiered based on finding categories:

- **Has `Category: model` findings**: Use `chain_validators(file_modified, validate_python_syntax)` — the model MUST make changes AND the result must parse.
- **All `Category: analysis` findings**: Use `validate_python_syntax` only — the model MAY make changes but isn't required to.

The `chain_validators()` helper runs validators in order, returns the first failure or success if all pass. This avoids modifying the `invoke_claude_validated` retry contract — it still sees one validator.

```python
def chain_validators(*validators: Validator) -> Validator:
    def _chain(text: str) -> ValidationResult:
        for v in validators:
            result = v(text)
            if not result.valid:
                return result
        return ValidationResult(valid=True, details="All validators passed")
    _chain.__name__ = "+".join(v.__name__ for v in validators)
    return _chain
```

The category check is done by scanning feedback text for `FINDING_CATEGORY_RE` matches before selecting the validator. Conservative: a missing Category field counts as `model` (triggers the strict path).

### Prior model selection (FR-C1/C2)

Walk `iter-{N-1}`, `iter-{N-2}`, ... checking `verdict.json` for `model_ok: true`. If found, copy that iteration's `model_setup.py`. If none found, check concept-root `model_setup.py`. If neither exists, cold start.

---

**Next Steps:** `/_my_design` → `/_my_plan` → `/_my_implement`
