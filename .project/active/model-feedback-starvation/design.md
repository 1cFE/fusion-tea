# Design: Analysis Loop Symmetry & Cleanup

**Status:** Draft
**Owner:** Reid W
**Created:** 2026-04-13
**Updated:** 2026-04-13
**Branch:** main
**Commit:** fd0fc2a

---

## Overview

Add model continuity (edit-not-rewrite) to the analysis loop and remove the `stage1-all` footgun. The model agent will receive its prior iteration's `model_setup.py` and be instructed to edit it rather than rewrite from scratch — mirroring how the analysis agent already works.

## Related Artifacts

- **Spec:** `.project/active/model-feedback-starvation/spec.md`
- **Research:** `.project/research/20260413-run-analysis-analyze-stage1all-audit.md`
- **Code:** `exploration/concept_analysis/scripts/run_analysis.py`
- **Code:** `exploration/concept_analysis/scripts/lib/loop.py`
- **Code:** `exploration/concept_analysis/scripts/lib/validators.py`
- **Code:** `exploration/concept_analysis/scripts/lib/iteration.py`
- **Templates:** `exploration/concept_analysis/prompt_templates/model_setup_costingfe.md`
- **Templates:** `exploration/concept_analysis/prompt_templates/model_setup_freeform.md`

---

## Research Findings

### Current model-setup flow (`loop.py:475-552`)

`_run_model_in_iteration()` writes to `iter_dir / "model_setup.py"` — a fresh path every iteration. `build_model_vars()` (loop.py:555-609) constructs template variables with `model_feedback` but no reference to any prior model. The validator is always `validate_python_syntax` (loop.py:519).

### Analysis feedback-pass pattern (the model to mirror)

`_run_feedback_pass()` (loop.py:389-452) demonstrates the edit-not-rewrite pattern:
1. Analysis file already exists at `concept_dir / "analysis.md"` (canonical copy)
2. Template uses `{{#if feedback_pass}}` conditional to switch instructions
3. Validator: `make_file_modified_validator(analysis_path)` constructed AFTER `prepare_step` but BEFORE invocation (loop.py:430), so SHA-256 snapshot is taken immediately before Claude touches the file
4. Claude is instructed to use Edit tool on the existing file

### Validator system (`validators.py`)

- `ValidationResult`: dataclass with `valid: bool`, `fix_message: str | None`, `details: str`
- `Validator = Callable[[str], ValidationResult]` (type alias at line 47)
- `make_file_modified_validator(path)`: factory that snapshots SHA-256, returns closure comparing on each call. Sets `__name__ = "validate_file_modified"` for log readability
- `validate_python_syntax(text)`: uses `compile(text, ..., 'exec')`
- No existing chain/composite validator pattern

### `FINDING_CATEGORY_RE` (`validators.py:24-26`)

```python
FINDING_CATEGORY_RE = re.compile(
    r"^\-\s+\**Category:?\**:?\s*(analysis|model)", re.MULTILINE
)
```

Used in `validate_feedback_verdict` (line 94) to extract category from each F-N block. Can be reused to scan model feedback text for `model` category findings.

### Iteration state (`iteration.py:57-100`)

`read_loop_state()` returns a `LoopState` with `iterations: list[IterationState]`. Each `IterationState` has `model_ok: bool` read from `verdict.json`. The main loop already calls `read_loop_state()` at loop.py:85 — accessible for prior-model lookup.

### Canonical file promotion (`loop.py:809-829`)

`_update_canonical_files()` copies `iter_dir/model_setup.py` → `concept_dir/model_setup.py` when `model_ok=True`. This means `concept_dir/model_setup.py` always holds the last known-good model — a natural fallback.

### `stage1-all` (`run_analysis.py:994-1036`)

Assembles `[cmd_gap_check?, cmd_analyze, cmd_model_setup, cmd_review]` and runs sequentially. Registered at parser line ~1245, dispatch table line ~1299. Docstring at file top references it in usage examples.

### Template conditional pattern (`analysis_v2.md`)

Uses mutually exclusive `{{#if cold_start}}` / `{{#if feedback_pass}}` / `{{#if self_advance}}` blocks. Model-setup templates currently only have `{{#if model_feedback}}` for optional feedback. Will add `{{#if prior_model_path}}` for the edit-vs-write mode switch.

---

## Proposed Design

### A. Remove `stage1-all` (FR-A1, FR-A2)

**Files changed:** `run_analysis.py`

1. **Delete `cmd_stage1_all()`** (~lines 994-1036)
2. **Delete parser block** for `stage1-all` (~lines 1245-1272)
3. **Delete dispatch entry** `"stage1-all": cmd_stage1_all` (~line 1299)
4. **Update script docstring** — remove `stage1-all` from usage examples. Replace with explicit chaining guidance: `analyze 01 && review 01`

No other files reference `cmd_stage1_all` or `stage1-all` (verified via grep).

### B. Verify feedback starvation fix (FR-B1-B4)

Already implemented. Implementation agent verifies:
- `extract_findings()` at loop.py:259-271 returns all findings (no category filter)
- Model-setup templates have `{{#if model_feedback}}` block with framing note
- Assessment template (`assessment.md`) treats Category as informational

No code changes needed.

### C. Model continuity — `chain_validators()` and `_has_model_category_findings()` (FR-C5, FR-C6)

**File:** `validators.py`

Add a `chain_validators()` combinator that runs validators in sequence, short-circuiting on first failure:

```python
def chain_validators(*validators: Validator) -> Validator:
    """Run validators in order; return first failure or final success."""
    def _chain(text: str) -> ValidationResult:
        for v in validators:
            result = v(text)
            if not result.valid:
                return result
        return ValidationResult(valid=True, details="All validators passed")
    _chain.__name__ = "+".join(v.__name__ for v in validators)
    return _chain
```

Location: after `make_file_modified_validator()` (~line 275), since it composes the same validator types.

Add a shared helper for splitting feedback text into F-N blocks (used by both `validate_feedback_verdict` and the new `has_model_category_findings`):

```python
def _split_finding_blocks(text: str) -> list[str]:
    """Split feedback text into individual F-N finding blocks."""
    blocks = re.split(r"(?=^### F-\d+:)", text, flags=re.MULTILINE)
    return [b for b in blocks if FINDING_HEADER_RE.match(b)]
```

Refactor `validate_feedback_verdict` (line 90-91) to use `_split_finding_blocks()` instead of inline splitting.

Add `has_model_category_findings()` — the category-scanning helper, placed in `validators.py` alongside the regex constants and similar block-splitting logic it uses:

```python
def has_model_category_findings(feedback_text: str) -> bool:
    """Check if any findings in the feedback are tagged Category: model.

    Returns True if at least one model finding exists, or if any finding
    lacks a Category field (conservative: assume model-targeted).
    """
    if not feedback_text:
        return False

    finding_blocks = _split_finding_blocks(feedback_text)
    if not finding_blocks:
        return False

    for block in finding_blocks:
        cat_match = FINDING_CATEGORY_RE.search(block)
        if cat_match is None:
            return True  # Missing category → conservative, treat as model
        if cat_match.group(1) == "model":
            return True

    return False
```

Note: public function (no underscore prefix) — it's called from `loop.py` and should be part of the validators module's API.

### C. Model continuity — `find_best_prior_model()` (FR-C1, FR-C2)

**File:** `loop.py`

New helper function near `_run_model_in_iteration()`:

```python
def _find_best_prior_model(
    concept_dir: Path,
    current_iter: int,
    loop_state: LoopState,
) -> Path | None:
    """Find the best prior model_setup.py for edit-based continuity.

    Selection order:
    1. Most recent iter < current_iter with model_ok=True → that iter's model_setup.py
    2. concept_dir / "model_setup.py" (canonical copy from _update_canonical_files)
    3. None (cold start)
    """
    # Walk backward through completed iterations
    for it in reversed(loop_state.iterations):
        if it.iteration >= current_iter:
            continue
        if it.model_ok:
            candidate = concept_dir / f"iter-{it.iteration}" / "model_setup.py"
            if candidate.exists():
                return candidate

    # Fallback: canonical copy at concept root
    canonical = concept_dir / "model_setup.py"
    if canonical.exists():
        return canonical

    return None
```

**Why walk `loop_state.iterations` instead of scanning disk?** The `LoopState` is already constructed at loop.py:85 and contains parsed `model_ok` from each `verdict.json`. No duplicate I/O.

### C. Model continuity — `_run_model_in_iteration()` changes (FR-C1, FR-C3, FR-C5, FR-C7)

**File:** `loop.py`, function at line 475

**Signature change:** Add `loop_state` as a required keyword argument:

```python
def _run_model_in_iteration(
    concept: dict,
    iter_dir: Path,
    args: argparse.Namespace,
    feedback_path: Path | None = None,
    *,
    loop_state: LoopState,
) -> tuple[bool, bool]:
```

`iter_num` is NOT a parameter — derived from `iter_dir.name` per existing convention (matching `_run_assess` at line 625):

```python
iter_num = int(iter_dir.name.split("-")[1])
```

**New import** — add `has_model_category_findings` and `chain_validators` to the existing `from lib.validators import` block (line 44):

```python
from lib.validators import (
    chain_validators,
    has_model_category_findings,
    make_file_modified_validator,
    validate_feedback_verdict,
    validate_non_empty,
    validate_python_syntax,
)
```

**New logic before `invoke_claude_validated`** (after line 504, before `prepare_step`):

```python
# --- Prior model continuity (FR-C1) ---
iter_num = int(iter_dir.name.split("-")[1])
prior_model_src = None
prior_model_path = ""
if iter_num > 1:
    prior_model_src = _find_best_prior_model(
        iter_dir.parent, iter_num, loop_state
    )
if prior_model_src is not None:
    # Copy into current iter dir so Claude can Edit it in place
    shutil.copy2(prior_model_src, model_script)
    prior_model_path = str(model_script)
```

**Validator selection** (replacing the current `validate_python_syntax` at line 519):

```python
# --- Validator selection (FR-C5, FR-C6) ---
if prior_model_path:
    # Feedback pass: tiered validation based on finding categories
    if has_model_category_findings(model_feedback):
        file_modified = make_file_modified_validator(model_script)
        validator = chain_validators(file_modified, validate_python_syntax)
    else:
        # All findings are analysis-only — model MAY change but isn't required to
        validator = validate_python_syntax
else:
    # Cold start: syntax only
    validator = validate_python_syntax
```

Note: `has_model_category_findings` is imported from `validators.py` (see Section C above). No local helper needed in `loop.py`.

**Call-site update** (loop.py:201):

```python
# Current:
model_ran, model_ok = _run_model_in_iteration(concept, iter_dir, args, feedback_path)

# Updated:
model_ran, model_ok = _run_model_in_iteration(
    concept, iter_dir, args, feedback_path,
    loop_state=loop_state,
)
```

`loop_state` is already in scope at the call site (loop.py:85).

### C. Model continuity — `build_model_vars()` changes (FR-C3)

**File:** `loop.py`, function at line 555

**Signature change:** Add `prior_model_path` parameter:

```python
def build_model_vars(
    concept: dict,
    model_path: Path,
    iter_dir_or_out_dir: Path,
    *,
    standalone: bool = False,
    model_feedback: str = "",
    prior_model_path: str = "",
) -> tuple[str, dict] | None:
```

**Add to both vars_dict blocks** (costingfe at line 597, freeform at line 607):

```python
"prior_model_path": prior_model_path,
"cold_start": "true" if not prior_model_path else "",
"feedback_pass": "true" if prior_model_path else "",
```

Three template variables support the mode switch:
- `prior_model_path` — the path string (for use in instructions)
- `cold_start` — truthy when no prior model exists
- `feedback_pass` — truthy when editing a prior model

These use the same names as the analysis template (`cold_start`, `feedback_pass`) — the templates are separate files with separate vars dicts, so there is no collision. Matching names preserve symmetry: a reader looking at either template sees the same conditional structure.

**Call-site update** in `_run_model_in_iteration()` (loop.py:497):

```python
model_vars = build_model_vars(concept, model_script, iter_dir,
                              model_feedback=model_feedback,
                              prior_model_path=prior_model_path)
```

The standalone `cmd_model_setup()` is intentionally NOT changed — it always writes from scratch (see spec: Out of Scope). Its default `prior_model_path=""` produces `cold_start="true"`, preserving current behavior.

### C. Model continuity — Template changes (FR-C4)

**Files:** `model_setup_costingfe.md`, `model_setup_freeform.md`

Add a conditional mode switch using `{{#if prior_model_path}}` / `{{else}}` blocks. The existing `{{#if model_feedback}}` block is nested inside the feedback-pass section.

**Pattern for both templates** — uses mutually exclusive `{{#if feedback_pass}}` / `{{#if cold_start}}` blocks (same variable names as `analysis_v2.md`, since the template engine doesn't support `{{else}}`):

```markdown
{{#if feedback_pass}}
## Mode: Feedback Pass (Edit Existing Model)

An existing model from a prior iteration has been copied to `{{output_path}}`.

**Your task**: Read the existing model at `{{prior_model_path}}` and apply targeted edits based on the assessment findings below. Use the Edit tool to make changes — do NOT rewrite the file from scratch.

**Rules**:
- Preserve ALL existing sweeps, scenarios, parameters, and sensitivity analyses unless a finding specifically says to change them
- Maintain the existing code structure and organization
- Add new content incrementally — do not restructure working code
- Every change must be traceable to a specific finding or a direct consequence of one

{{#if model_feedback}}
## Assessment Findings

The following findings were raised by the assessor. Focus on findings tagged `Category: model`. Findings tagged `Category: analysis` are informational — they describe prose changes the analysis agent is handling. You may still adjust model parameters if an analysis finding implies the model's assumptions are wrong.

{{model_feedback}}
{{/if}}
{{/if}}

{{#if cold_start}}
## Mode: Cold Start (Write New Model)

[... existing template body — "Write a self-contained Python script" instructions unchanged ...]

{{#if model_feedback}}
## Assessment Feedback

{{model_feedback}}
{{/if}}
{{/if}}
```

The exact integration point differs per template:
- **costingfe**: The existing template body (CostingFE-specific instructions, mapping notes, example paths) goes inside the `{{#if model_cold_start}}` block. The `{{#if model_feedback_pass}}` block is added above it.
- **freeform**: Same pattern. The 5-layer architecture instructions go inside the `{{#if model_cold_start}}` block.

Both templates retain their full cold-start instructions unchanged — the conditional just gates which instruction set Claude sees. The `{{#if model_feedback}}` block appears in BOTH modes (cold start can have feedback from source-integration or review kick-back).

### C. Model continuity — Validation failure handling (FR-C5)

The existing non-fatal failure path (loop.py:530-538) remains unchanged. When `result.validation_passed` is `False`:

- **file-modified failure** (feedback pass with model findings): Claude didn't change the file. Printed as "WARN — model_setup.py not modified". `model_ok=False`, canonical files not promoted. The prior good model is preserved.
- **python-syntax failure**: Same as today. `model_ok=False`.
- **chain failure**: The chain validator's `__name__` (`"validate_file_modified+validate_python_syntax"`) appears in `validation_log.json`, making it clear which validator failed.

The WARN message at loop.py:537 currently says "syntax validation exhausted". This should be made generic since the validator may now be a chain:

```python
# Current (line 537):
print(f" FAILED ({elapsed:.0f}s) — syntax validation exhausted")

# Updated:
validator_name = getattr(validator, "__name__", "validation")
print(f" FAILED ({elapsed:.0f}s) — {validator_name} exhausted")
```

---

## Potential Risks

1. **Template variable mutual exclusivity**: `cold_start` and `feedback_pass` are set as mutually exclusive strings in `build_model_vars()`. If a caller passes `prior_model_path` incorrectly (non-empty but pointing to a nonexistent file), the template renders in feedback-pass mode but Claude can't find the model. Mitigation: `_run_model_in_iteration()` only sets `prior_model_path` after `shutil.copy2` succeeds, so the file always exists when the variable is set.

2. **SHA-256 snapshot timing**: `make_file_modified_validator(model_script)` must be called AFTER `shutil.copy2()` puts the prior model in place, but BEFORE `invoke_claude_validated`. The proposed code ordering handles this — copy happens before `prepare_step`, validator constructed after `prepare_step` (mirroring the analysis pattern at loop.py:427-430).

3. **Edge case: prior model has import errors but valid syntax**: `validate_python_syntax` only checks `compile()`, not imports. This is existing behavior and acceptable — `run_model()` catches runtime errors separately, and `model_ok` is already set based on that.

4. **`cmd_model_setup` standalone unchanged**: Intentional. It writes from scratch with no prior model context. Its `build_model_vars()` call passes default `prior_model_path=""`, so templates render in cold-start mode.

---

## Integration Strategy

- **`stage1-all` removal** is independent. Can be done first as a clean, risk-free deletion.
- **Model continuity** integrates at three points:
  - `_run_model_in_iteration()` — the main orchestration change
  - `build_model_vars()` — adds one template variable
  - Templates — conditional blocks, no existing behavior changed
- **Validator chain and `has_model_category_findings`** are additive — new functions in validators.py, used only by the new code path. `_split_finding_blocks` is a refactor of existing inline code.
- **`loop_state` threading**: Already in scope at the call site (loop.py:85). Single required keyword argument — no plumbing needed.

---

## Validation Approach

### Automated verification

1. **Template rendering**: After template changes, run `analyze --dry-run` on a concept at iter-2+ to verify the prompt contains "Read the existing model" (feedback pass) vs "Write a self-contained Python script" (cold start). Compare iter-1 (cold start) vs iter-2+ (feedback pass).

2. **Validator chain**: Add unit test in `test_validators.py` for `chain_validators()`:
   - Both pass → valid
   - First fails → returns first failure
   - Second fails → returns second failure
   - `__name__` is formatted correctly

3. **`has_model_category_findings()`** (in `test_validators.py`): Unit test with:
   - Empty string → False
   - Findings with only `Category: analysis` → False
   - Findings with `Category: model` → True
   - Finding missing Category field → True (conservative)
   - Mixed categories → True

### Manual verification

1. Run a concept that's at iter-2+ with `--resume` and verify:
   - Prior `model_setup.py` is copied into `iter-N/` before Claude runs
   - Model-setup prompt contains edit-mode instructions
   - Claude uses Edit tool on the model (visible in validation log)
2. Run a concept at iter-1 (cold start) and verify unchanged behavior
3. Verify `stage1-all` produces "unknown command" error

---

Next Step: After approval → `/_my_plan` or `/_my_implement`
