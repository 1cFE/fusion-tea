# Implementation Plan: Analysis Loop Symmetry & Cleanup

**Status:** Draft
**Created:** 2026-04-13
**Last Updated:** 2026-04-13

## Source Documents
- **Spec:** `.project/active/model-feedback-starvation/spec.md`
- **Design:** `.project/active/model-feedback-starvation/design.md` ← See here for component details, function signatures, architecture

## Implementation Strategy

**Phasing Rationale:**
Phase 1 builds the validator foundation (testable in isolation). Phase 2 is an independent deletion. Phase 3 wires the validators into the loop orchestration. Phase 4 adds the template conditionals that Phase 3's variables drive. This order means each phase's inputs are already validated before it runs.

**Overall Validation Approach:**
- Phase 1 & 2 are fully automated (unit tests + grep)
- Phase 3 & 4 use dry-run prompts as integration tests
- Existing test suite must pass after every phase

---

## Phase 1: Validator Additions (test-first)

### Goal
Add `_split_finding_blocks`, `chain_validators`, and `has_model_category_findings` to `validators.py`. Refactor `validate_feedback_verdict` to use the shared helper. This phase has zero callers — pure library additions.

### Test Stencil (Write This First)
```python
# In test_validators.py

class TestChainValidators:
    def test_both_pass(self):
        # Two passing validators → valid
    def test_first_fails(self):
        # First fails → returns first failure, second never called
    def test_second_fails(self):
        # First passes, second fails → returns second failure
    def test_name_concatenation(self):
        # __name__ is "a+b"

class TestHasModelCategoryFindings:
    def test_empty_string(self):
        # "" → False
    def test_no_findings(self):
        # Text without F-N blocks → False
    def test_analysis_only(self):
        # All Category: analysis → False
    def test_model_finding(self):
        # Category: model → True
    def test_missing_category(self):
        # No Category field → True (conservative)
    def test_mixed_categories(self):
        # One analysis + one model → True
```

### Changes Required

**See `design.md#c-model-continuity--chain_validators-and-_has_model_category_findings-fr-c5-fr-c6` for function signatures and logic.**

#### 1. Test File
**File:** `exploration/concept_analysis/scripts/test_validators.py`
- [x] Add `chain_validators` and `has_model_category_findings` to imports
- [x] Add `TestChainValidators` class (4 tests)
- [x] Add `TestHasModelCategoryFindings` class (6 tests)

#### 2. Implementation
**File:** `exploration/concept_analysis/scripts/lib/validators.py`
- [x] Add `_split_finding_blocks()` helper after `FINDING_CATEGORY_RE` (~line 26)
- [x] Refactor `validate_feedback_verdict` lines 90-91 to use `_split_finding_blocks()`
- [x] Add `chain_validators()` after `make_file_modified_validator` (~line 275)
- [x] Add `has_model_category_findings()` after `chain_validators`

### Validation

**Automated:**
- [x] `cd exploration/concept_analysis/scripts && uv run python -m pytest test_validators.py -v` → all 68 pass (10 new + 58 existing)
- [x] `uv run python -m pytest test_validators.py::TestValidateFeedbackVerdict -v` → existing tests still pass after refactor

**What We Know Works After This Phase:**
- `chain_validators` correctly short-circuits and concatenates names
- `has_model_category_findings` correctly scans F-N blocks for category tags
- `validate_feedback_verdict` unchanged behavior (refactor only)

---

## Phase 2: Remove `stage1-all`

### Goal
Delete the `stage1-all` command — function, parser, dispatch entry, docstring references. Independent of all other phases.

### Test Stencil
No new tests. Verification via grep.

### Changes Required

**See `design.md#a-remove-stage1-all-fr-a1-fr-a2` for the four deletion targets.**

**File:** `exploration/concept_analysis/scripts/run_analysis.py`
- [x] Delete `cmd_stage1_all()` function (~lines 994-1036)
- [x] Delete `stage1-all` parser block (~lines 1245-1272)
- [x] Delete `"stage1-all": cmd_stage1_all` dispatch entry (~line 1299)
- [x] Update script docstring — remove `stage1-all` from usage examples, add chaining guidance

### Validation

**Automated:**
- [x] `grep -r "stage1.all\|cmd_stage1_all" exploration/concept_analysis/scripts/` → no matches
- [x] `uv run python -m pytest exploration/concept_analysis/scripts/ -v` → 205 passed, 5 skipped

**What We Know Works After This Phase:**
- `stage1-all` is fully excised. No dangling references.

---

## Phase 3: Model Continuity in `loop.py`

### Goal
Wire prior-model lookup, copy, tiered validator selection, and updated template variables into the iteration loop. This is the core orchestration change.

### Test Stencil
No new unit tests for this phase — the logic depends on filesystem state (iter dirs, verdict.json) and `invoke_claude_validated` which is tested via integration tests. Validation is via dry-run inspection.

### Changes Required

**See `design.md` sections:**
- `#c-model-continuity--find_best_prior_model-fr-c1-fr-c2` — new helper
- `#c-model-continuity--_run_model_in_iteration-changes-fr-c1-fr-c3-fr-c5-fr-c7` — orchestration
- `#c-model-continuity--build_model_vars-changes-fr-c3` — template variables
- `#c-model-continuity--validation-failure-handling-fr-c5` — failure message

**File:** `exploration/concept_analysis/scripts/lib/loop.py`
- [x] Update `from lib.validators import` block (line 44) — add `chain_validators`, `has_model_category_findings`
- [x] Add `_find_best_prior_model()` helper near `_run_model_in_iteration` (~line 474)
- [x] Update `_run_model_in_iteration` signature: add `*, loop_state: LoopState`
- [x] Add `iter_num = int(iter_dir.name.split("-")[1])` derivation inside function
- [x] Add prior-model copy logic (before `prepare_step`)
- [x] Replace `validator=validate_python_syntax` with tiered validator selection
- [x] Update failure message (line 537) to use `validator.__name__`
- [x] Update `build_model_vars` signature: add `prior_model_path: str = ""`
- [x] Add `prior_model_path`, `cold_start`, `feedback_pass` to both vars_dict blocks
- [x] Update `build_model_vars` call-site in `_run_model_in_iteration` to pass `prior_model_path`
- [x] Update call-site at line 201: add `loop_state=loop_state`

### Validation

**Automated:**
- [x] `uv run python -m pytest exploration/concept_analysis/scripts/ -v` → 205 passed, 5 skipped
- [ ] `uv run python exploration/concept_analysis/scripts/run_analysis.py analyze 13 --dry-run --resume` → no errors, prompt file written

**Manual:**
- [ ] Inspect `iter-N/model_setup_prompt.md` for a concept at iter-2+: should contain "Read the existing model" (once templates are updated in Phase 4, for now verify the variable substitution slots are present)
- [ ] Inspect iter-1 prompt: should contain cold-start instructions (current behavior)

**What We Know Works After This Phase:**
- `_find_best_prior_model` walks loop_state correctly
- Prior model is copied into iter dir before invocation
- Tiered validator selection based on finding categories
- `build_model_vars` emits correct template variables for both modes
- Standalone `cmd_model_setup` unchanged (default `prior_model_path=""`)

---

## Phase 4: Template Conditional Blocks

### Goal
Add `{{#if feedback_pass}}`/`{{#if cold_start}}` mode switch to both model-setup templates. Existing template body becomes the cold-start block. New feedback-pass block added above it.

### Test Stencil
No unit tests — validated via dry-run prompt inspection.

### Changes Required

**See `design.md#c-model-continuity--template-changes-fr-c4` for the conditional pattern.**

**File:** `exploration/concept_analysis/prompt_templates/model_setup_costingfe.md`
- [x] Wrap existing body (lines 1-113) inside `{{#if cold_start}}...{{/if}}`
- [x] Move existing `{{#if model_feedback}}` block inside `{{#if cold_start}}`
- [x] Add `{{#if feedback_pass}}...{{/if}}` block above with edit-mode instructions and nested `{{#if model_feedback}}`

**File:** `exploration/concept_analysis/prompt_templates/model_setup_freeform.md`
- [x] Wrap existing body (lines 1-163) inside `{{#if cold_start}}...{{/if}}`
- [x] Move existing `{{#if model_feedback}}` block inside `{{#if cold_start}}`
- [x] Add `{{#if feedback_pass}}...{{/if}}` block above with edit-mode instructions and nested `{{#if model_feedback}}`

### Validation

**Automated:**
- [ ] `uv run python exploration/concept_analysis/scripts/run_analysis.py analyze 13 --dry-run --resume` → prompt contains "Read the existing model" for iter-2+
- [ ] `uv run python exploration/concept_analysis/scripts/run_analysis.py analyze 13 --dry-run --force` → prompt contains "Write a self-contained Python script" (cold start)

**Manual:**
- [ ] Verify iter-1 prompt has full cold-start instructions (CAS mapping, power standardization, etc.)
- [ ] Verify iter-2+ prompt has edit-mode instructions with prior model path
- [ ] Verify `{{#if model_feedback}}` renders correctly in both modes when findings exist

**What We Know Works After This Phase:**
- Templates render correct instructions for both modes
- Nested conditionals (`model_feedback` inside `feedback_pass`/`cold_start`) work
- Cold-start instructions are byte-identical to prior behavior

---

## Phase 5: Verify FR-B (feedback starvation fix)

### Goal
Verify the already-implemented feedback starvation fix is intact. No code changes.

- [x] `extract_findings()` at loop.py:265-277 returns all findings (no category filter) — splits on `### F-N:` and joins all blocks
- [x] Model-setup templates have `{{#if model_feedback}}` with framing note in both feedback_pass and cold_start modes
- [x] Assessment template (line 52) treats Category as informational metadata: "does not gate visibility"

---

## Environment Setup

**See CLAUDE.md for full environment rules**

- All Python via `uv run python ...`
- Tests: `cd exploration/concept_analysis/scripts && uv run python -m pytest`

---

## Risk Management

**See `design.md#potential-risks` for detailed risk analysis.**

**Phase-Specific Mitigations:**
- **Phase 1**: Refactoring `validate_feedback_verdict` — existing tests catch regressions
- **Phase 3**: SHA-256 timing — mirror analysis pattern exactly (copy before prepare_step, validator after)
- **Phase 4**: Nested `{{#if}}` — template engine uses DOTALL + non-greedy matching via `(.*?)`, so inner `{{/if}}` closes inner block correctly. Verify via dry-run.

## Implementation Notes

_To be filled during implementation._

### Phase 1 Completion
**Completed:** 2026-04-13
**Actual Changes:**
- Added `_split_finding_blocks()` helper to `validators.py` (after regex constants, line ~28)
- Refactored `validate_feedback_verdict` to use `_split_finding_blocks()` (replaced inline split)
- Added `chain_validators()` after `make_file_modified_validator` (end of file)
- Added `has_model_category_findings()` after `chain_validators` (end of file)
- Added `TestChainValidators` (4 tests) and `TestHasModelCategoryFindings` (6 tests) to `test_validators.py`
- Updated imports in `test_validators.py` to include `chain_validators`, `has_model_category_findings`
**Issues:** None
**Deviations:** None

### Phase 2 Completion
**Completed:** 2026-04-13
**Actual Changes:**
- Deleted `cmd_stage1_all()` function and its section comment (~lines 989-1036)
- Deleted `stage1-all` parser block (~lines 1245-1272)
- Deleted `"stage1-all": cmd_stage1_all` dispatch entry
- Updated docstring usage example: `stage1-all 01 02 03` → `analyze 01 02 03 && review 01 02 03`
- Updated `cmd_address_review` skip message: `stage1-all --resume` → `analyze --resume`
**Issues:** None
**Deviations:** Also fixed a `stage1-all` reference in the address-review skip message (line 686)

### Phase 3 Completion
**Completed:** 2026-04-13
**Actual Changes:**
- Added `LoopState` to `from lib.iteration import` block
- Added `chain_validators`, `has_model_category_findings` to `from lib.validators import` block
- Added `_find_best_prior_model()` helper (~line 478)
- Updated `_run_model_in_iteration` signature with `*, loop_state: LoopState`
- Added prior-model copy logic (iter_num derivation, `_find_best_prior_model` call, `shutil.copy2`)
- Added tiered validator selection (model findings → chain, analysis-only → syntax, cold start → syntax)
- Updated failure message to use `validator.__name__`
- Updated `build_model_vars` signature with `prior_model_path: str = ""`
- Added `prior_model_path`, `cold_start`, `feedback_pass` to both costingfe and freeform vars_dict
- Updated call-site in `run_stage1_loop` to pass `loop_state=loop_state`
- Fixed 2 existing tests in `test_failure_chains.py` to pass `loop_state=LoopState()` (cold start)
**Issues:** None
**Deviations:** Had to fix 2 existing tests that directly call `_run_model_in_iteration` — passed empty `LoopState()` since they test iter-1 (cold start)

### Phase 4 Completion
**Completed:** 2026-04-13
**Actual Changes:**
- Rewrote `model_setup_costingfe.md` with `{{#if feedback_pass}}` / `{{#if cold_start}}` conditional blocks
- Rewrote `model_setup_freeform.md` with same conditional structure
- Feedback-pass blocks: edit-mode instructions, prior model path, nested `{{#if model_feedback}}` with category guidance
- Cold-start blocks: identical to prior template content (full instructions preserved)
- Verified both templates render correctly: feedback_pass shows edit instructions only, cold_start shows write instructions only
- Cleaned up dry-run artifacts (iter-6 through iter-10)
**Issues:** None
**Deviations:** None — nested conditionals work correctly with the non-greedy DOTALL regex engine

---

**Status**: Complete
