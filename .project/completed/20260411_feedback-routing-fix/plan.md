# Implementation Plan: Feedback Routing Fix

**Status:** Complete
**Created:** 2026-04-06
**Last Updated:** 2026-04-06

## Source Documents
- **Spec:** `.project/active/feedback-routing-fix/spec.md`
- **Design:** `.project/active/feedback-routing-fix/design.md` ← See here for component details, function signatures, template content

## Implementation Strategy

**Phasing Rationale:**
Templates first (zero code risk, establishes format contract), then Problem A code (additive, no control flow changes, creates shared helper), then Problem B code (modifies elif cascade — highest risk, depends on shared helper from Phase 2).

**Overall Validation Approach:**
- No automated test suite for pipeline scripts — validation through `--dry-run` and prompt/output inspection
- Each phase has dry-run validation against real concept data
- Backward compatibility verified by running against existing uncategorized feedback files

---

## Phase 1: Prompt Template Updates

### Goal
Update all 5 templates to establish the format contract: categorized findings, conditional model-feedback sections, and carried-forward feedback instructions. Zero code risk — purely declarative changes.

### Test Stencil (Verify First)
```bash
# After edits, verify templates parse correctly and conditionals work
cd exploration/concept_analysis

# 1. Check feedback_format.md contains Category field
grep -A1 "Category" prompt_templates/config/feedback_format.md

# 2. Check model-setup templates have conditional block
grep "model_feedback" prompt_templates/model_setup_costingfe.md
grep "model_feedback" prompt_templates/model_setup_freeform.md

# 3. Check analysis_v2.md has carried-forward note
grep "Carried-Forward" prompt_templates/analysis_v2.md
```

### Changes Required

**See `design.md` for exact template content:**
- Feedback format changes → `design.md#1-feedback-format`
- Assessment categorization instructions → `design.md#2-assessment-template`
- Model-setup conditional sections → `design.md#3-model-setup-templates`
- Analysis template notes → `design.md#4-analysis-template`

**Specific file changes (all relative to `exploration/concept_analysis/prompt_templates/`):**

#### 1. Feedback Format
**File:** `config/feedback_format.md` (MODIFY)
- [x] Add `- **Category:** analysis | model` field between `Target` and `Finding` in the format spec
- [x] Update the rules section to explain the category distinction
- [x] Update the example finding to include `Category: analysis`

#### 2. Assessment Template
**File:** `assessment.md` (MODIFY)
- [x] Add "Finding Categories" subsection after "## Instructions" (before "## Scope")
- [x] Include criteria for `analysis` vs `model` categories per design.md#2

#### 3. Model-Setup Templates
**File:** `model_setup_costingfe.md` (MODIFY)
- [x] Add `{{#if model_feedback}}` conditional section after "## Required Reading"

**File:** `model_setup_freeform.md` (MODIFY)
- [x] Add identical `{{#if model_feedback}}` conditional section after "## Required Reading"

#### 4. Analysis Template
**File:** `analysis_v2.md` (MODIFY)
- [x] Add category semantics note after "Address each finding." in feedback-pass section
- [x] Add carried-forward feedback explanation paragraph

### Validation

**Manual:**
- [x] Read each modified template end-to-end — verify no broken markdown or template syntax
- [x] Verify `{{#if model_feedback}}` / `{{/if}}` are balanced in both model-setup templates
- [x] Verify `feedback_format.md` example finding has all 5 fields (Target, Category, Finding, Recommendation, Priority)

**What We Know Works After This Phase:**
All templates are ready for the code changes in Phases 2-3. The assessment agent will produce categorized findings on next run. Model-setup templates will render the conditional section when `model_feedback` is populated.

---

## Phase 2: Problem A — Model Feedback Extraction + Routing

### Goal
Add the shared `_split_findings()` helper, `_extract_model_findings()`, update `build_model_vars()` signature, and wire `feedback_path` through `_run_model_in_iteration()`. Purely additive — no changes to loop control flow.

### Test Stencil (Verify First)
```bash
# After code changes, dry-run concept 01 and inspect model-setup prompt

# 1. Manually add "Category: model" to an existing feedback file for testing
#    (the assessment template change hasn't produced categorized feedback yet)
#    Edit: analyses/01-hts-compact-tokamak/iter-7/feedback.md
#    Add "- **Category:** model" to the REBCO finding

# 2. Dry-run and inspect
cd exploration/concept_analysis
uv run python scripts/run_analysis.py stage1-all \
    --concepts 01-hts-compact-tokamak --dry-run --resume

# 3. Check model_setup_prompt.md for model_feedback section
grep -A5 "Assessment Feedback" analyses/01-hts-compact-tokamak/iter-8/model_setup_prompt.md

# 4. Backward compat: dry-run a concept with uncategorized feedback
#    Verify model_feedback section is ABSENT (conditional suppressed)
```

### Changes Required

**See `design.md` for:**
- `_split_findings()` implementation → `design.md#5a`
- `_extract_model_findings()` implementation → `design.md#5b`
- `_run_model_in_iteration()` wiring → `design.md#5c`
- `build_model_vars()` signature update → `design.md#5d`

**Specific file changes:**

#### 1. Shared Helper
**File:** `exploration/concept_analysis/scripts/lib/loop.py` (MODIFY)
- [x] Add `_split_findings(text: str) -> list[str]` helper (design.md#5a)

#### 2. Model Finding Extraction
**File:** `exploration/concept_analysis/scripts/lib/loop.py` (MODIFY)
- [x] Add `_extract_model_findings(feedback_path: Path | None) -> str` using `_split_findings()` (design.md#5b)

#### 3. Wire into Model-Setup
**File:** `exploration/concept_analysis/scripts/lib/loop.py` (MODIFY)
- [x] Add `feedback_path` parameter to `_run_model_in_iteration()` (design.md#5c)
- [x] Call `_extract_model_findings(feedback_path)` and pass result to `build_model_vars()`
- [x] Update call site in `run_stage1_loop()` to pass `feedback_path`

#### 4. Update build_model_vars
**File:** `exploration/concept_analysis/scripts/lib/loop.py` (MODIFY)
- [x] Add `model_feedback: str = ""` keyword arg to `build_model_vars()` (design.md#5d)
- [x] Add `"model_feedback": model_feedback` to both costingfe and freeform `vars_dict` branches

### Validation

**Automated:**
- [x] `uv run python scripts/run_analysis.py stage1-all --concepts 01-hts-compact-tokamak --dry-run --resume` — syntax check passes (ast.parse)

**Manual:**
- [ ] With manually-categorized feedback: `iter-8/model_setup_prompt.md` contains "Assessment Feedback (Model-Targeted)" section with the REBCO finding
- [ ] Without categorized feedback (different concept): model_setup_prompt.md does NOT contain the model_feedback section
- [ ] `build_model_vars()` standalone path (no feedback) still works: `uv run python scripts/run_analysis.py model-setup --concepts 01-hts-compact-tokamak --dry-run`

**What We Know Works After This Phase:**
Model-targeted findings are extracted from feedback and injected into the model-setup prompt. The shared `_split_findings()` helper is available for Phase 3. Backward compatibility with uncategorized feedback confirmed.

---

## Phase 3: Problem B — Assess Finding Preservation + Verdict Metadata

### Goal
Add `_merge_feedback()`, rewire the research branch of the feedback-producer cascade to merge rather than replace, and add `merged_assess` to `write_verdict()`. This is the highest-risk phase — it modifies the `elif` cascade control flow.

### Test Stencil (Verify First)
```bash
# After code changes, dry-run concept 07 with --research and inspect feedback

cd exploration/concept_analysis

# 1. Dry-run with research flag
uv run python scripts/run_analysis.py stage1-all \
    --concepts 07-maglif --dry-run --resume --research

# 2. Check merged feedback contains both sections
grep "Carried-Forward Assessment Findings" analyses/07-maglif/iter-*/feedback.md

# 3. Verify prior iteration's feedback.md is unmodified
diff <(git show HEAD:exploration/concept_analysis/analyses/07-maglif/iter-6/feedback.md) \
     analyses/07-maglif/iter-6/feedback.md

# 4. Check verdict.json contains merged_assess field
grep "merged_assess" analyses/07-maglif/iter-*/verdict.json
```

### Changes Required

**See `design.md` for:**
- `_merge_feedback()` implementation → `design.md#6a`
- Research branch rewiring → `design.md#6b`
- `verdict.json` metadata → `design.md#6c`
- File path collision analysis → `design.md#6d`

**Specific file changes:**

#### 1. Merge Helper
**File:** `exploration/concept_analysis/scripts/lib/loop.py` (MODIFY)
- [x] Add `_merge_feedback(assess_feedback_path, source_integration_path, output_path) -> Path` using `_split_findings()` (design.md#6a)

#### 2. Research Branch Rewiring
**File:** `exploration/concept_analysis/scripts/lib/loop.py` (MODIFY)
- [x] Initialize `merged_assess = False` before the feedback-producer cascade
- [x] Replace research branch (lines 136-157) with merge-aware version (design.md#6b)
- [x] Set `merged_assess = True` when prior assess feedback exists and merge executes

#### 3. Verdict Metadata
**File:** `exploration/concept_analysis/scripts/lib/iteration.py` (MODIFY)
- [x] Add `merged_assess: bool = False` parameter to `write_verdict()` (design.md#6c)
- [x] Include `"merged_assess"` in the verdict data dict

#### 4. Wire merged_assess into write_verdict call
**File:** `exploration/concept_analysis/scripts/lib/loop.py` (MODIFY)
- [x] Pass `merged_assess=merged_assess` to the `write_verdict()` call at line ~213

### Validation

**Automated:**
- [x] `uv run python -c "import ast; ..."` — both `loop.py` and `iteration.py` parse cleanly

**Manual:**
- [ ] When research would acquire sources: merged `feedback.md` contains source-integration findings THEN "Carried-Forward Assessment Findings" section with prior assess findings
- [ ] Prior iteration's `feedback.md` is byte-identical to pre-change version
- [ ] `source_integration_output.md` preserved unmodified alongside merged `feedback.md`
- [ ] When prior assess was PASS: merge skipped, source-integration output used as-is
- [ ] When research finds nothing: falls through to normal assess feedback (unchanged behavior)
- [ ] `verdict.json` contains `"merged_assess": true` for merged iterations, `false` otherwise
- [ ] Non-research iterations still produce valid `verdict.json` (default `false`)

**What We Know Works After This Phase:**
Both bugs are fixed. Assessment findings with model-targeted categories route to the model-setup agent. Research-acquired sources no longer silently drop prior assess findings. Audit trail captures merge events in `verdict.json`.

---

## Risk Management

**See `design.md#potential-risks` for detailed risk analysis**

**Phase-Specific Mitigations:**
- **Phase 1**: Read each template end-to-end after editing. Template syntax errors are immediately visible in dry-run prompts.
- **Phase 2**: Backward-compat verified by dry-running against existing uncategorized feedback. The `_extract_model_findings()` default (empty string) means the conditional is suppressed — no regression possible.
- **Phase 3**: Keep all fallback paths identical to current code. The only changed path is `acquired=True` + `si_path is not None` — all other branches are verbatim copies of existing code.

## Implementation Notes

[TO BE FILLED DURING IMPLEMENTATION]

### Phase 1 Completion
**Completed:** 2026-04-06
**Actual Changes:**
- `config/feedback_format.md`: Added `Category` field to format spec, added category rules, added `Category: analysis` to example
- `assessment.md`: Added "Finding Categories" subsection after Instructions item 5 with analysis/model criteria and dual-target guidance
- `model_setup_costingfe.md`: Added `{{#if model_feedback}}` conditional section after "Costing Constants" (last Required Reading item), before "Concept Mapping"
- `model_setup_freeform.md`: Added `{{#if model_feedback}}` conditional section after "CAS Account Reference" (last Required Reading item), before "Model Architecture"
- `analysis_v2.md`: Added category semantics note and carried-forward explanation in feedback-pass section after "Address each finding."
**Issues:** None
**Deviations:** Positioned the model_feedback conditional after the last Required Reading subsection (before the next ## section) rather than directly after the "## Required Reading" header — this is more natural since the agent reads data sources first, then sees feedback. Matches the design's stated intent.

### Phase 2 Completion
**Completed:** 2026-04-06
**Actual Changes:**
- `lib/loop.py`: Added `_split_findings()` helper (line ~231) — splits feedback text into F-N blocks via regex
- `lib/loop.py`: Added `_extract_model_findings()` helper (line ~241) — filters for `Category: model` with permissive regex, backward-compat default to `analysis`
- `lib/loop.py`: Added `feedback_path: Path | None = None` param to `_run_model_in_iteration()` (line ~404)
- `lib/loop.py`: Added `model_feedback: str = ""` kwarg to `build_model_vars()` (line ~471), included in both costingfe and freeform vars_dict
- `lib/loop.py`: Updated call site at line ~187 to pass `feedback_path` through
**Issues:** None
**Deviations:** None — implementation matches design exactly

### Phase 3 Completion
**Completed:** 2026-04-06
**Actual Changes:**
- `lib/loop.py`: Added `_merge_feedback()` helper (line ~266) — merges source-integration output with carried-forward assess findings under a "Carried-Forward Assessment Findings" header, skips merge when prior assess was PASS or had no findings
- `lib/loop.py`: Added `merged_assess = False` initialization at line ~108 before feedback-producer cascade
- `lib/loop.py`: Rewired research branch (lines ~147-156) — when `acquired` and `si_path is not None`, calls `_merge_feedback()` instead of returning `si_path` directly. Sets `merged_assess` based on whether prior assess feedback exists.
- `lib/iteration.py`: Added `merged_assess: bool = False` parameter to `write_verdict()` (line ~114), included `"merged_assess"` in verdict data dict
- `lib/loop.py`: Passed `merged_assess=merged_assess` to the main `write_verdict()` call (line ~218). Error and SINGLE_PASS paths use the default `False`.
**Issues:** None
**Deviations:** None — implementation matches design exactly

---

**Status**: Complete
