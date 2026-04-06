# Implementation Plan: Iterative Analysis Loop

**Status:** Complete
**Created:** 2026-03-28
**Last Updated:** 2026-03-28

## Source Documents
- **Spec:** `.project/active/iterative-analysis-loop/spec.md`
- **Design:** `.project/active/iterative-analysis-loop/design.md` ← See here for component details, config file contents, prompt structures, function signatures

## Implementation Strategy

**Phasing Rationale:**
Config extraction + template loading first because everything else depends on `{{@...}}` working. Prompts second because they're pure content once the loading mechanism is proven. Loop orchestration third because it wires the prompts into the pipeline — needs both configs and prompts to exist. Integration testing last because it validates the whole system end-to-end on real data.

**Overall Validation Approach:**
- Each phase has a dry-run or script-level verification
- Phase 4 is the real convergence test on live concepts
- Backward compatibility checked via `--max-passes 1` throughout

---

## Phase 1: Config Extraction + `fill_template` Extension

### Goal
Create the 5 config files and extend `fill_template()` to support `{{@path}}` file inclusion. This is first because every prompt template in Phase 2 depends on config loading working correctly.

### Test Stencil (Write This First)
```python
# Test stencil — run as inline validation after implementing fill_template changes
# No formal test file exists for run_analysis.py; validate via dry-run + manual check

# 1. Verify config files exist and are non-empty
for f in ["analysis_goals.md", "assessment_checklist.md", "quality_standards.md",
          "review_checklist.md", "feedback_format.md"]:
    path = TEMPLATES_DIR / "config" / f
    assert path.exists(), f"Missing config: {f}"
    assert len(path.read_text()) > 100, f"Config too short: {f}"

# 2. Verify {{@...}} expansion
template = "Before\n{{@config/analysis_goals.md}}\nAfter"
result = fill_template(template, {})
assert "Analysis Goals" in result, "Config inclusion failed"
assert "{{@" not in result, "Unexpanded inclusion marker"

# 3. Verify existing {{variable}} and {{#if}} still work
template = "{{name}} {{#if flag}}yes{{/if}}"
result = fill_template(template, {"name": "test", "flag": "true"})
assert result == "test yes"
```

### Changes Required

**See `design.md#component-1` for:** Full config file contents (analysis_goals.md, assessment_checklist.md, quality_standards.md, review_checklist.md, feedback_format.md)
**See `design.md#component-2` for:** `fill_template()` updated signature and implementation

**Specific file changes:**

#### 1. Config Directory and Files
**Directory:** `exploration/concept_analysis/prompt_templates/config/` (NEW)
- [x] Create `config/` directory
- [x] Create `analysis_goals.md` — 5 shape-focused goals (FR-1, content in `design.md#analysis_goals.md`)
- [x] Create `assessment_checklist.md` — concrete checkable criteria (FR-2, content in `design.md#assessment_checklist.md`)
- [x] Create `quality_standards.md` — citation, anti-hallucination, depth (FR-3, content in `design.md#quality_standards.md`)
- [x] Create `review_checklist.md` — numerical accuracy checks (FR-4, content in `design.md#review_checklist.md`)
- [x] Create `feedback_format.md` — structured feedback spec with VERDICT/F-N format (FR-21, content in `design.md#feedback_format.md`)

#### 2. `fill_template()` Extension
**File:** `exploration/concept_analysis/scripts/run_analysis.py:441-461`
- [x] Add `templates_dir` parameter (default `TEMPLATES_DIR`)
- [x] Add `{{@path}}` regex pass before conditionals (see `design.md#component-2` for exact code)
- [x] Import `re` is already present — no new imports needed

### Validation (How to Verify This Phase)

**Automated:**
- [x] Run the test stencil above as a quick script or in Python REPL
- [x] Verify `fill_template("{{@config/analysis_goals.md}}", {})` expands correctly
- [x] Verify `fill_template("{{@config/nonexistent.md}}", {})` produces `[CONFIG FILE NOT FOUND: ...]`
- [x] Verify existing templates still render: `fill_template("{{name}}", {"name": "test"})` → `"test"`

**Manual:**
- [x] `ls prompt_templates/config/` shows 5 .md files
- [x] Each config file is readable standalone (makes sense without the prompt context)
- [x] Spot-check: analysis_goals.md contains all 5 goals from FR-1

**What We Know Works After This Phase:**
Config files exist and `fill_template()` can load them via `{{@...}}`. The foundation for all prompt templates is ready.

---

## Phase 2: Prompt Templates

### Goal
Create `analysis_v2.md` (modal), `assessment.md`, and `agents/source_reader.md`. Rename old `analysis.md` → `analysis.md.old`. This is now safe because Phase 1 proved config loading works.

### Test Stencil (Write This First)
```python
# Validate prompt templates render correctly in each mode

analysis_template = (TEMPLATES_DIR / "analysis_v2.md").read_text()

# Cold-start mode
result = fill_template(analysis_template, {
    "concept_name": "Test Concept", "concept_id": "99-test",
    "cold_start": "true", "feedback_pass": "", "self_advance": "",
    "dossier_path": "/fake/dossier.md", "source_paths": "- src1.md",
    "output_path": "/fake/body.md", "analysis_path": "/fake/analysis.md",
    # ... other vars
})
assert "Cold Start" in result
assert "Feedback Pass" not in result
assert "Self-Advance" not in result
assert "Analysis Goals" in result  # config was expanded

# Feedback-pass mode
result = fill_template(analysis_template, {
    "cold_start": "", "feedback_pass": "true", "self_advance": "",
    "feedback_path": "/fake/feedback.md",
    # ... other vars
})
assert "Feedback Pass" in result
assert "Cold Start" not in result

# Assessment template
assess_template = (TEMPLATES_DIR / "assessment.md").read_text()
result = fill_template(assess_template, {
    "concept_name": "Test", "analysis_path": "/fake/a.md",
    "feedback_path": "/fake/f.md",
})
assert "Assessment Checklist" in result  # config expanded
assert "feedback_format" not in result or "VERDICT" in result  # format expanded
```

### Changes Required

**See `design.md#component-3` for:** Modal analysis prompt structure, mode flags, template constraint (no nested `{{#if}}`)
**See `design.md#component-4` for:** Source reader subagent prompt
**See `design.md#component-5` for:** Assessment prompt structure

**Specific file changes:**

#### 1. Source Reader Subagent
**Directory:** `exploration/concept_analysis/prompt_templates/agents/` (NEW)
**File:** `prompt_templates/agents/source_reader.md` (NEW)
- [x] Create `agents/` directory
- [x] Create `source_reader.md` per `design.md#component-4`

#### 2. Modal Analysis Prompt
**File:** `prompt_templates/analysis_v2.md` (NEW)
- [x] Create modal prompt with 3 flat `{{#if}}` blocks (cold_start, feedback_pass, self_advance)
- [x] Include `{{@config/analysis_goals.md}}` and `{{@config/quality_standards.md}}`
- [x] Include `{{@agents/source_reader.md}}` in the per-source reading section
- [x] Verify NO nested `{{#if}}` blocks (the regex-based fill_template breaks on nesting)
- [x] Cold-start section: output to `{{output_path}}` (analysis_body.md)
- [x] Feedback-pass section: Edit tool on `{{analysis_path}}`
- [x] Self-advance section: included but not wired in orchestrator yet (for future epic Items 3, 5)

#### 3. Assessment Prompt
**File:** `prompt_templates/assessment.md` (NEW)
- [x] Create assessment prompt per `design.md#component-5`
- [x] Include `{{@config/analysis_goals.md}}`, `{{@config/assessment_checklist.md}}`, `{{@config/feedback_format.md}}`
- [x] Output to `{{feedback_path}}`
- [x] Explicit "What You Are NOT Checking" section (numerical accuracy, citations)

#### 4. Rename Old Prompt
**File:** `prompt_templates/analysis.md` → `prompt_templates/analysis.md.old`
- [x] Rename old analysis prompt (preserve for reference until v2 is proven)

### Validation (How to Verify This Phase)

**Automated:**
- [x] Run the test stencil above
- [x] Grep `analysis_v2.md` for nested `{{#if}}` — must find none
- [x] Verify all `{{@...}}` references resolve to existing config files

**Manual:**
- [x] Read rendered cold-start prompt — goals and quality standards expanded inline
- [x] Read rendered feedback-pass prompt — feedback_path variable present, no cold-start content
- [x] Read rendered assessment prompt — checklist and feedback format expanded inline
- [x] Verify source_reader.md is self-contained and makes sense as a subagent prompt

**What We Know Works After This Phase:**
All prompt templates exist, render correctly in each mode, and properly include config content. The old prompt is preserved as `.old` for rollback if needed.

---

## Phase 3: Loop Orchestration + Staleness + CLI

### Goal
Replace `cmd_analyze()` with the iterative loop, add staleness propagation, update state detection and status display, and add `--max-passes` CLI argument. This is the core pipeline change.

### Test Stencil (Write This First)
```python
# Validate loop orchestration via --dry-run (no Claude calls)

# 1. Single-pass dry-run: only analysis_prompt_iter_1.md generated
# uv run python scripts/run_analysis.py analyze 11 --max-passes 1 --dry-run
# Expected: analysis_prompt_iter_1.md exists, no assessment_prompt files

# 2. Multi-pass dry-run: analysis + assessment prompts for iter 1 generated
# (dry-run can only generate cold-start prompt; assessment depends on analysis.md existing)
# uv run python scripts/run_analysis.py analyze 11 --max-passes 3 --dry-run
# Expected: analysis_prompt_iter_1.md exists

# 3. Staleness propagation unit test
from pathlib import Path
import tempfile
with tempfile.TemporaryDirectory() as tmp:
    out = Path(tmp) / "test-concept"
    out.mkdir()
    # Create fake downstream artifacts
    (out / "review.md").write_text("---\nStatus: clean\n---\nContent")
    (out / "model_setup.py").write_text("# model code")

    stale = propagate_staleness("test-concept", "test-reason", analyses_dir=Path(tmp))
    assert "review.md" in stale
    assert "model_setup.py" in stale

    # Verify markers
    review_text = (out / "review.md").read_text()
    assert "Stale: true" in review_text
    model_text = (out / "model_setup.py").read_text()
    assert "# STALE: test-reason" in model_text
```

### Changes Required

**See `design.md#component-6` for:** Full loop logic, CLI arguments, loop flow diagram
**See `design.md#component-7` for:** `propagate_staleness()`, updated `get_concept_state()`, updated `cmd_status()`
**See `design.md#component-8` for:** Backward compatibility details

**Specific file changes:**

#### 1. New Function: `propagate_staleness()`
**File:** `run_analysis.py` (NEW function, add near `get_concept_state` around line 413)
- [x] Add `propagate_staleness(concept_id, reason, analyses_dir)` per `design.md#component-7`
- [x] Handle .py files (comment marker) and .md files (frontmatter fields)
- [x] Return list of stale file names

#### 2. New Function: `_has_downstream_artifacts()`
**File:** `run_analysis.py` (NEW function, add near `propagate_staleness`)
- [x] Add helper that checks for model_setup.py, review.md, synthesis.md existence

#### 3. Replace `cmd_analyze()`
**File:** `run_analysis.py:820-921`
- [x] Replace current single-pass `cmd_analyze` with iterative loop per `design.md#component-6`
- [x] Load `analysis_v2.md` instead of `analysis.md` (line 832)
- [x] Load `assessment.md` template
- [x] Add `common_vars` dict for shared template variables
- [x] Cold-start pass with `analysis_prompt_iter_1.md` naming
- [x] Assessment loop with `feedback_iter_N.md` and `assessment_prompt_iter_N.md`
- [x] Feedback-pass analyze with `analysis_prompt_iter_N.md`
- [x] Convergence check: `^VERDICT:\s*PASS` regex
- [x] Staleness propagation after `--force` cold start and after feedback passes
- [x] `--max-passes 1` skips assessment loop entirely
- [x] Per-pass status output (pass number, duration, result)

#### 4. Update `get_concept_state()`
**File:** `run_analysis.py:379-412`
- [x] Add stale detection: check downstream .md frontmatter for `Stale: true`
- [x] Check model_setup.py first line for `# STALE:`
- [x] Append `*` suffix to state string when stale artifacts found

#### 5. Update `cmd_status()`
**File:** `run_analysis.py:703-740`
- [x] Handle `*` suffix in state: `sym = state_symbols.get(state.rstrip("*"), "  ?")`
- [x] Replace trailing space with `*` when stale: `sym = sym[:-1] + "*"`
- [x] Update legend to include stale indicator explanation
- [x] Update counts dict to handle `*` suffix states

#### 6. CLI: Add `--max-passes`
**File:** `run_analysis.py:1489-1497` (analyze parser) and `run_analysis.py:1543-1554` (stage1-all parser)
- [x] Add `--max-passes` argument to `p_analyze` (default 3)
- [x] Add `--max-passes` argument to `p_s1` (default 3)

### Validation (How to Verify This Phase)

**Automated:**
- [x] `uv run python scripts/run_analysis.py analyze 11 --max-passes 1 --dry-run` → generates `analysis_prompt_iter_1.md` only
- [x] `uv run python scripts/run_analysis.py analyze 11 --max-passes 3 --dry-run` → generates `analysis_prompt_iter_1.md`
- [x] Verify `--max-passes` appears in `--help` for both `analyze` and `stage1-all`
- [x] Run staleness unit test from stencil above

**Manual:**
- [x] Read generated `analysis_prompt_iter_1.md` — verify cold-start mode content, goals expanded, quality standards expanded
- [x] Verify `analysis.md.old` is not referenced anywhere in the new code
- [x] `uv run python scripts/run_analysis.py status` still works (no crash on concepts without stale artifacts)

**What We Know Works After This Phase:**
The full loop orchestration is wired, CLI accepts `--max-passes`, staleness propagation marks downstream artifacts, and `status` shows stale indicators. Ready for live testing.

---

## Phase 4: Integration Testing

### Goal
Run the iterative loop on real concepts to validate convergence, quality, and backward compatibility. No code changes — this phase is pure validation.

### Test Plan

#### 4a: Backward Compatibility
- [x] `uv run python scripts/run_analysis.py analyze 11 --max-passes 1 --force` → produces analysis.md with same structure as before
- [x] Verify frontmatter, 8 sections, citations all present
- [x] `uv run python scripts/run_analysis.py status` → shows correct state, no crashes

#### 4b: Iterative Loop (3 concepts)
Tested on 09 (MFE QI Stellarator), 22 (IFE Projectile ICF), 14 (MIF MTF Pneumatic):
- [x] `uv run python scripts/run_analysis.py analyze 09 22 14 --max-passes 3`
- [x] Check `feedback_iter_1.md` — does it contain real, specific findings?
- [x] Check if pass 2 fixes the issues raised in pass 1
- [x] Does the loop converge (VERDICT: PASS) within 3 passes?
- [x] Repeat for 2 more concepts
- [x] **Success criterion**: Assessment finds real issues on pass 1 that pass 2 fixes for ≥3 concepts — **MET**; loop converges within 3 passes for ≥2 of 3 — **PARTIAL (1 of 3)**

#### 4c: Staleness Verification
- [x] Run `analyze --force` on a concept that has review.md and model_setup.py
- [x] Verify `review.md` gets `Stale: true` frontmatter — **N/A** (review.md lacks frontmatter, correctly skipped)
- [x] Verify `model_setup.py` gets `# STALE:` comment
- [x] Verify `status` shows `*` indicator for that concept

#### 4d: Pipeline Integration
- [x] `uv run python scripts/run_analysis.py stage1-all 15 --max-passes 1 --dry-run` → verified argument wiring, correct prompt naming
- [x] All downstream stages skip correctly when analysis.md not yet created

#### 4e: Audit Trail
- [x] Check concept output dir for: `analysis_prompt_iter_1.md`, `assessment_prompt_iter_1.md`, `feedback_iter_1.md`, etc.
- [x] Verify prompt files contain the fully-rendered prompt (config expanded, mode selected)

**What We Know Works After This Phase:**
The full iterative analysis loop works end-to-end on real concepts. Assessment quality is validated. Backward compatibility confirmed. Staleness propagation works. Pipeline integration intact.

---

## Environment Setup

**See CLAUDE.md for full environment rules**

- Always use `uv run python ...` for script execution
- Pipeline script: `exploration/concept_analysis/scripts/run_analysis.py`
- Templates: `exploration/concept_analysis/prompt_templates/`
- Analyses output: `exploration/concept_analysis/analyses/`

---

## Risk Management

**See `design.md#potential-risks` for detailed risk analysis**

**Phase-Specific Mitigations:**
- **Phase 1**: `{{@...}}` regex collision risk → test with existing templates to confirm no false matches
- **Phase 2**: Nested `{{#if}}` risk → grep-verify no nesting exists in the final template
- **Phase 3**: `cmd_analyze` replacement is the highest-risk change → validate with `--dry-run` before any live calls; keep `analysis.md.old` for rollback
- **Phase 4**: Assessment quality (too soft/harsh) → start with one concept, review findings manually before scaling to batch

## Implementation Notes

### Phase 1 Completion
**Completed:** 2026-03-28
**Actual Changes:**
- Created `prompt_templates/config/` directory with 5 config files:
  - `analysis_goals.md` (1053 chars) — 5 shape-focused goals
  - `assessment_checklist.md` (1430 chars) — concrete checkable criteria
  - `quality_standards.md` (1226 chars) — citation, anti-hallucination, depth
  - `review_checklist.md` (862 chars) — numerical accuracy checks
  - `feedback_format.md` (1917 chars) — structured feedback spec with VERDICT/F-N format
- Extended `fill_template()` in `run_analysis.py:441` with:
  - Added `templates_dir` parameter (default `TEMPLATES_DIR`)
  - Added `{{@path}}` regex pass before conditionals for config file inclusion
- Verified: config inclusion works, missing config produces error marker, existing {{variable}} and {{#if}} still work, no collision with existing templates
**Issues:** None
**Deviations:** None

### Phase 2 Completion
**Completed:** 2026-03-28
**Actual Changes:**
- Created `prompt_templates/agents/` directory
- Created `agents/source_reader.md` — subagent prompt template for per-source reading
- Created `analysis_v2.md` — modal analysis prompt with 3 flat `{{#if}}` blocks (cold_start, feedback_pass, self_advance). Carries forward all essential content from old prompt (reading order, citation format, output instructions, reuse). Adds: goals/quality config inclusion, per-source subagent pattern, feedback-pass Edit instructions, self-advance mode.
- Created `assessment.md` — assessment prompt with goals, checklist, and feedback format config inclusions. Explicit "What You Are NOT Checking" section.
- Renamed `analysis.md` → `analysis.md.old`
- Verified: all 3 modes render correctly (correct content included, other modes stripped), no nested `{{#if}}`, all `{{@...}}` resolve, assessment renders with expanded configs
**Issues:** None
**Deviations:**
- `source_reader.md` simplified vs design: removed `{{source_path}}`/`{{questions}}` template vars that would collide with fill_template. Instead uses plain instructions that the analysis agent adapts per source. The source_reader is a reference pattern, not a fill_template template.

### Phase 3 Completion
**Completed:** 2026-03-28
**Actual Changes:**
- Added `propagate_staleness(concept_id, reason, analyses_dir)` after `get_concept_state()` — marks downstream .py (comment marker) and .md (frontmatter fields) as stale
- Added `_has_downstream_artifacts(out_dir)` helper
- Updated `get_concept_state()` to detect staleness: checks .md frontmatter for `Stale: true` and .py first line for `# STALE:`, appends `*` suffix
- Updated `cmd_status()` to handle `*` suffix: strips for symbol lookup, replaces trailing space with `*`, added stale count and legend entry
- Replaced `cmd_analyze()` with iterative loop: loads `analysis_v2.md` + `assessment.md`, cold-start pass 1, assessment loop with convergence check (`^VERDICT:\s*PASS`), feedback-pass analyze, staleness propagation on `--force` and after feedback passes
- Added `--max-passes` CLI arg (default 3) to both `analyze` and `stage1-all` parsers
- All validation checks pass: dry-run generates correct prompts, cold-start mode only (no feedback/self-advance content), status works across all 38 concepts, staleness unit test passes, `--max-passes` in help
**Issues:** None
**Deviations:** None — implementation matches design exactly

### Phase 4 Completion
**Completed:** 2026-03-28
**Actual Changes:** No code changes (pure validation). One bug fix during 4a: `sym[:-1] + "*"` was eating the state letter (e.g., `"  S"[:-1]` = `"  "`), changed to `sym + "*"`.
**Results:**
- 4a: Backward compat confirmed — concept 11 single-pass produces 8-section analysis with 31 citations, correct frontmatter
- 4b: Iterative loop tested on 3 concepts (09 MFE, 22 IFE, 14 MIF):
  - All 3: assessment found real, substantive issues on pass 1 that pass 2 addressed
  - 1 of 3 converged (concept 14 PASS on iter 3); 2 of 3 did not converge in 3 passes
  - Non-convergent findings are genuinely useful (progressively deeper issues each pass)
  - Convergence criterion (≥2 of 3) partially met — suggests `--max-passes 4-5` or lighter assessment prompt for full convergence
- 4c: Staleness verified on concept 11 — model_setup.py got `# STALE:`, synthesis.md got `Stale: true`, status shows `S*`. review.md correctly skipped (no frontmatter).
- 4d: stage1-all dry-run confirms `--max-passes` wiring, correct prompt naming
- 4e: Full audit trail present — iteration-numbered prompt and feedback files with expanded configs
**Issues:**
- review.md lacks YAML frontmatter (starts with `# Review:`) — staleness code correctly skips it but this means review.md cannot be marked stale via frontmatter. Low impact: review is downstream of analysis and will be re-run anyway.
- Assessment agent may be too demanding for 3-pass convergence — finding deeper issues each pass rather than converging. Consider `--max-passes 4-5` default or lighter assessment criteria.
**Deviations:** None in code. Testing used concepts 09/22/14 instead of 11/22/31 from plan (concept 11 was used for 4a backward compat instead).

---

**Status**: Draft → In Progress → Complete
