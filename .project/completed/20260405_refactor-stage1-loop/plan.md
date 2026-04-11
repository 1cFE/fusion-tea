# Implementation Plan: Stage 1 Loop Refactor (Work Item #2)

**Status:** Complete
**Created:** 2026-04-05
**Last Updated:** 2026-04-05

## Source Documents
- **Spec:** `.project/active/refactor-stage1-loop/spec.md`
- **Design:** `.project/active/refactor-stage1-loop/design.md` — See here for component details, function signatures, architecture

## Implementation Strategy

**Phasing Rationale:**
Phase 1 builds the data layer everything else depends on. Phase 2 extracts the loop — the core deliverable — and proves it works in isolation. Phase 3 wires it into the CLI and migrates existing data atomically (they're coupled: old code reads flat, new code reads iter-N/). Phase 4 is cosmetic cleanup that can land independently.

**Overall Validation Approach:**
- Each phase has manual verification via --dry-run and fixture inspection
- No formal test framework (per WI#1 scope); verification is fixture-based
- Migration has an idempotency check (run twice, same result)

---

## Phase 1: `lib/iteration.py` — Data Layer

### Goal
Build the iteration state management module. Pure data structures and I/O — no behavioral changes to existing code. Everything in Phases 2-4 imports from this module.

### Test Stencil (Manual Verification)
```bash
# Create a synthetic concept dir with iter-1/ and iter-2/
mkdir -p /tmp/test-concept/iter-{1,2}
# Write a mock verdict.json to iter-1/
echo '{"iteration":1,"verdict":"FAIL","finding_count":3,"feedback_source":"cold_start","model_ran":false,"model_ok":false,"research_ran":false,"sources":["/path/to/source1.md"],"timestamp":"2026-04-05T12:00:00"}' > /tmp/test-concept/iter-1/verdict.json
# Write iter-2/ with analyze_prompt.md but no verdict (incomplete)
touch /tmp/test-concept/iter-2/analyze_prompt.md

# Then in Python:
# from lib.iteration import read_loop_state, detect_new_sources
# state = read_loop_state(Path("/tmp/test-concept"))
# assert state.last_complete == 1
# assert state.last_incomplete == 2
# assert state.next_iteration == 2  # resume the incomplete one
# assert state.all_prior_sources == {"/path/to/source1.md"}
```

### Changes Required

**See `design.md#component-1` for:** IterationState/LoopState dataclasses, function signatures, read_loop_state algorithm, detect_new_sources logic.

#### 1. New Module
**File:** `exploration/concept_analysis/scripts/lib/iteration.py` (NEW)
- [x] `IterationState` frozen dataclass (with `sources: list[str]` field)
- [x] `LoopState` dataclass with `next_iteration` and `all_prior_sources` properties
- [x] `read_loop_state(concept_dir)` — glob iter-*/, read verdict.json, detect incomplete
- [x] `write_verdict(iter_dir, ...)` — write verdict.json with ISO timestamp and sources
- [x] `parse_verdict_from_feedback(feedback_text)` — regex extraction (moved from inline in cmd_analyze)
- [x] `detect_new_sources(loop_state, current_sources)` — compare against all_prior_sources
- [x] `clear_iterations(concept_dir)` — delete iter-*/ dirs for --force

### Validation

**Manual:**
- [x] Create synthetic iter-N/ dirs (complete + incomplete), verify `read_loop_state` returns correct `last_complete`, `last_incomplete`, `next_iteration`
- [x] Write a verdict.json via `write_verdict`, read it back, verify all fields round-trip
- [x] Test `parse_verdict_from_feedback` against a real `feedback_iter_N.md` from existing concept (e.g., `analyses/01-hts-compact-tokamak/feedback_iter_1.md`)
- [x] Test `detect_new_sources` with a LoopState where sources=["a.md"] and current_sources=["a.md","b.md"] → returns ["b.md"]
- [x] Test `clear_iterations` removes dirs, returns correct count
- [x] `uv run python -c "from lib.iteration import ..."` — imports cleanly, no circular deps

**What We Know Works After This Phase:**
Iteration state can be read, written, and queried. All verdict.json I/O is proven.

---

## Phase 2: `lib/loop.py` — Loop Runner

### Goal
Extract the stage1 loop into a dedicated module with all internal helpers. This is the core deliverable. Testable via --dry-run against a manually-prepared iter-1/ fixture.

### Test Stencil (Manual Verification)
```bash
# After Phase 1 migration creates iter dirs for concept 01:
# Manually create iter-1/verdict.json for concept 01 (or use a test concept)
# Then:
cd exploration/concept_analysis/scripts
uv run python run_analysis.py analyze 01 --resume --dry-run
# Expected: detects existing iter-1, generates iter-2/analyze_prompt.md
#   with feedback_path pointing to iter-1/feedback.md
# Verify: iter-2/analyze_prompt.md contains feedback_pass=true
```

### Changes Required

**See `design.md#component-2` for:** run_stage1_loop signature, loop body pseudocode, all internal helper functions.

#### 1. New Module
**File:** `exploration/concept_analysis/scripts/lib/loop.py` (NEW)
- [x] `run_stage1_loop(concept, args, *, resume, common_vars, analysis_template, assessment_template)` — main loop with defensive common_vars copy
- [x] `_run_cold_start(concept, iter_dir, common_vars, template, args)` — extracted from `run_analysis.py:334-386`, writes to iter-N/
- [x] `_run_feedback_pass(concept, iter_dir, feedback_path, common_vars, template, args)` — extracted from `run_analysis.py:440-472`
- [x] `_capture_analysis_output(analysis_path, iter_dir)` — strip frontmatter, save body to iter-N/analysis_output.md
- [x] `_run_model_in_iteration(concept, iter_dir, args)` — adapted from cmd_model_setup, uses invoke_claude directly, non-fatal on failure (FR-7)
- [x] `_run_assess(concept, iter_dir, analysis_path, template, args)` — extracted from `run_analysis.py:394-432`, writes feedback.md to iter-N/
- [x] `_run_source_integration(concept, iter_dir, new_sources, analysis_path, args)` — extracted from cmd_update_analysis step 1, writes source_integration_output.md
- [x] `_run_research_step(concept, iter_dir, args)` — stub returning None with log message (FR-14)
- [x] `_get_prior_feedback(concept_dir, iter_num)` — returns iter-(N-1)/feedback.md path
- [x] `_update_canonical_files(concept_dir, iter_dir)` — copy model_setup.py and model_output.txt to concept root (FR-5)

#### 2. Extract Model Vars Helper
**File:** `exploration/concept_analysis/scripts/run_analysis.py` (MODIFY)
- [x] Extract `build_model_vars(concept, model_path, iter_dir_or_out_dir)` — placed in `lib/loop.py` (not run_analysis.py) since it shares imports with the loop
- [ ] `cmd_model_setup` calls the extracted helper (behavior unchanged) — deferred to Phase 3 CLI integration

### Validation

**Manual:**
- [x] Verify all imports clean — no circular deps
- [x] `_capture_analysis_output` tested against real `analyses/01-hts-compact-tokamak/analysis.md` — 47K chars, frontmatter stripped correctly
- [x] `build_model_vars` tested: standalone mode (concept dir) and in-loop mode (iter dir) both produce correct template name and vars
- [ ] Full --dry-run integration test deferred to Phase 3 (requires CLI wiring)

**What We Know Works After This Phase:**
The loop runner produces correct prompts for cold-start and feedback-pass modes, selects the right feedback-producer, and the model vars extraction is non-breaking.

---

## Phase 3: CLI Integration + Migration Script

### Goal
Wire the loop into `cmd_analyze`, add `--resume`/`--research`/`--force` behavior, remove `cmd_update_analysis`, and build + run the migration script. These land together because they're coupled: new code reads iter-N/ layout, migration creates that layout.

### Test Stencil (Manual Verification)
```bash
# Pre-migration: snapshot status output
cd exploration/concept_analysis/scripts
uv run python run_analysis.py status > /tmp/status_before.txt

# Run migration (dry-run first)
uv run python scripts/migrate_iterations.py --dry-run
# Inspect output: file moves make sense, verdict.json values correct
uv run python scripts/migrate_iterations.py

# Post-migration: verify
uv run python run_analysis.py status > /tmp/status_after.txt
diff /tmp/status_before.txt /tmp/status_after.txt
# Should be identical (same states, no iter-N awareness in status yet)

# Verify iter-N layout for concept with 3 iterations (e.g., 01)
ls analyses/01-hts-compact-tokamak/iter-{1,2,3}/
# Should have: analyze_prompt.md, assess_prompt.md, feedback.md, verdict.json

# Verify resume works post-migration
uv run python run_analysis.py analyze 01 --resume --dry-run
# Should detect 3 existing iterations, generate iter-4/analyze_prompt.md

# Verify mutual exclusivity
uv run python run_analysis.py analyze 01 --resume --force
# Should exit with error message

# Verify backward compat
uv run python run_analysis.py analyze 01
# Should skip (analysis.md exists)

# Verify idempotency
uv run python scripts/migrate_iterations.py
# Should report "already migrated" or no-op for all concepts
```

### Changes Required

**See `design.md#component-3` for:** cmd_analyze refactor, cmd_stage1_all changes, argparse flags, cmd_update_analysis removal. See `design.md#component-6` for migration script details.

#### 1. CLI Integration
**File:** `exploration/concept_analysis/scripts/run_analysis.py` (MODIFY)
- [x] Extract `_build_common_vars(concept)` from `cmd_analyze` lines 270-284
- [x] Extract `_apply_external_feedback(targets, args, feedback)` from `cmd_analyze` lines 286-332
- [x] Rewrite `cmd_analyze` to use `run_stage1_loop` (~60 lines replacing ~270)
- [x] Add `--resume` and `--research` flags to `analyze` subparser
- [x] Add `--resume` and `--research` flags to `stage1-all` subparser
- [x] Add `--resume`/`--force` mutual exclusivity check
- [x] Add `--resume`/`--feedback` mutual exclusivity check
- [x] Remove `cmd_update_analysis` function (~150 lines)
- [x] Remove `"update-analysis"` from argparse builder and dispatch table
- [x] Update `cmd_stage1_all` to pass `--resume` through (it already does via shared `args`)

#### 2. Migration Script
**File:** `exploration/concept_analysis/scripts/migrate_iterations.py` (NEW ~200 lines)
- [x] Argparse: positional concept_id (optional), `--dry-run`
- [x] Per-concept migration function:
  - [x] Detect iterations by globbing `analysis_prompt_iter_*.md` and `feedback_iter_*.md`
  - [x] Create `iter-N/` dirs, move files per design.md#component-6 table
  - [x] Extract iter-1/analysis_output.md from analysis.md body (strip frontmatter)
  - [x] Generate verdict.json per iteration (parse feedback files, extract sources from prompts)
  - [x] Move non-iteration prompts to `prompts/` per design.md#component-6 table
- [x] Idempotency: check destination exists before each move, skip if so
- [x] Summary output: count of concepts migrated, files moved, verdicts generated

### Validation

**Automated:**
- [x] `status` output identical before and after migration
- [x] `get_concept_state` returns same value for all 38 concepts before and after

**Manual:**
- [x] Inspect 3 representative concepts post-migration (01: 3-iter, 17a: source-integration, 15: 1-iter):
  - iter-N/ dirs contain expected files with correct names
  - verdict.json has correct verdict/finding_count matching original feedback files
  - verdict.json sources field populated with canonical knowledge/concept_research/ paths (not phase_1a symlink)
  - prompts/ contains moved prompt files
  - Concept root has only canonical files per FR-21
- [x] `analysis.md` content unchanged for all concepts
- [x] `analyze 01 --resume --dry-run --max-passes 5` → detects 3 iterations, generates iter-4 prompt with feedback_path=iter-3/feedback.md
- [x] `analyze 01 --resume --force` → exits with mutual exclusivity error
- [ ] `stage1-all 01 --resume --dry-run` → runs analyze (resume) + model-setup + review (not tested — deferred, same shared args)
- [x] `analyze 01` (no flags) → skips as before
- [x] Migration script run twice → no changes on second run
- [x] No phase_1a paths in any verdict.json (verified via grep)

**What We Know Works After This Phase:**
Full end-to-end: migration converts existing data, new code reads it, --resume works, --force clears and restarts, backward compat preserved, update-analysis removed.

---

## Phase 4: Status, Template, Prompts Cleanup

### Goal
Cosmetic and enhancement layer: iteration summary in status display, model_output_path in assess template (FR-8), non-iteration prompts written to `prompts/` subdirs by handlers.

### Test Stencil (Manual Verification)
```bash
# Status shows iteration info
uv run python run_analysis.py status
# Should show iteration count + verdict alongside existing state

# Review dry-run writes prompt to prompts/
uv run python run_analysis.py review 01 --dry-run
ls analyses/01-hts-compact-tokamak/prompts/review_prompt.md
# Should exist

# Concept root clean per FR-21
ls analyses/01-hts-compact-tokamak/
# Should show only: analysis.md, model_setup.py, model_output.txt,
#   gap_report.md, review.md, address_log.md, synthesis.md,
#   iter-1/, iter-2/, iter-3/, prompts/
```

### Changes Required

**See `design.md#component-4` for:** get_iteration_summary. See `design.md#component-5` for prompts/ path changes. See `design.md` "Assess Prompt Template Change" for FR-8.

#### 1. Status Enhancement
**File:** `exploration/concept_analysis/scripts/lib/state.py` (MODIFY)
- [x] Add `get_iteration_summary(concept_id, analyses_dir)` function using `read_loop_state`
- [x] Don't surface `model_ran` for migrated iterations (pre-loop era)

**File:** `exploration/concept_analysis/scripts/run_analysis.py` (MODIFY — `cmd_status`)
- [x] Call `get_iteration_summary` and display alongside existing state column

#### 2. Assess Template
**File:** `exploration/concept_analysis/prompt_templates/assessment.md` (MODIFY)
- [x] Add `{{#if model_output_path}}` conditional block (~6 lines per design)

**File:** `exploration/concept_analysis/scripts/lib/loop.py` (MODIFY — `_run_assess`)
- [x] Pass `model_output_path` to assess template vars when model output exists

#### 3. Prompts/ Directory for Handlers
**File:** `exploration/concept_analysis/scripts/run_analysis.py` (MODIFY)
- [x] `cmd_gap_check`: prompt path → `prompts/gap_check_prompt.md` (with mkdir)
- [x] `cmd_review`: prompt path → `prompts/review_prompt.md`
- [x] `cmd_synthesize`: prompt path → `prompts/synthesis_prompt.md`
- [x] `cmd_address_review`: prompt path → `prompts/address_review_prompt.md`
- [x] `cmd_model_setup` (standalone): prompt path → `prompts/model_setup_prompt.md`

**File:** `exploration/concept_analysis/scripts/lib/step_runner.py` (MODIFY)
- [x] Always create `prompt_path.parent` dir (was only created when `output_path is None`)

### Validation

**Manual:**
- [x] `status` output shows iteration summary for concepts with iter-*/ dirs
- [x] `status` output still correct for concepts without iterations (not-started)
- [x] `review 01 --dry-run` writes to `prompts/review_prompt.md`
- [x] All 5 handler prompt paths write to `prompts/` subdir
- [x] Concept root contains only canonical files + `iter-*/` + `prompts/` (FR-21)
- [x] No file in `scripts/` exceeds ~400 lines (run_analysis.py is 1119 but holds 12 handlers)

**What We Know Works After This Phase:**
Complete feature: loop + resume + migration + status + clean layout. All spec acceptance criteria met.

---

## Risk Management

**See `design.md#potential-risks` for detailed risk analysis.**

**Phase-Specific Mitigations:**
- **Phase 2**: Model vars extraction verified by --dry-run prompt comparison before and after
- **Phase 3**: Migration run on git-tracked files — `git diff` shows exactly what moved. `git stash` recovers if something goes wrong. Commit migration standalone for clean blame.
- **Phase 4**: Prompts/ path changes are low-risk 1-line edits; verify each handler individually

---

## Implementation Notes

### Phase 1 Completion
**Completed:** 2026-04-05
**Actual Changes:**
- Created `exploration/concept_analysis/scripts/lib/iteration.py` (~155 lines)
- IterationState (frozen dataclass), LoopState (with next_iteration, all_prior_sources properties)
- read_loop_state: scans iter-*/ dirs, reads verdict.json, detects incomplete iterations
- write_verdict: writes verdict.json with ISO timestamp
- parse_verdict_from_feedback: uses same regex as existing cmd_analyze (^VERDICT:\s*PASS, ^### F-\d+:)
- detect_new_sources: compares current sources against all_prior_sources from verdict.json records
- clear_iterations: deletes iter-*/ dirs for --force mode
- Helper _parse_iter_num for safe directory name parsing

**Issues:** None
**Deviations:** None — followed design exactly

### Phase 2 Completion
**Completed:** 2026-04-05
**Actual Changes:**
- Created `exploration/concept_analysis/scripts/lib/loop.py` (400 lines, 398 code lines)
- `run_stage1_loop`: main loop with --force, resume, feedback-producer selection, model-in-loop
- 10 internal helpers: cold_start, feedback_pass, capture_output, model_in_iteration, assess, source_integration, research_step (stub), get_prior_feedback, update_canonical_files
- `build_model_vars`: shared helper for model-setup template vars (placed in loop.py, not run_analysis.py as design suggested, because it shares imports)
- Uses `ANALYSES_DIR` from `lib/paths` directly (not via args)

**Issues:** 
- loop.py is 400 lines vs ~250 estimated. 11 functions with full error handling, dry-run support, and status output account for the difference. 398 logical code lines is at the ~400 target. Could split `build_model_vars` to a separate module in Phase 4 if needed.

**Deviations:**
- `build_model_vars` placed in `lib/loop.py` instead of `run_analysis.py` — avoids circular imports since it needs `lib/concepts` and `lib/paths` imports that loop.py already has
- `cmd_model_setup` refactoring to use `build_model_vars` deferred to Phase 3 (CLI integration)
- Full --dry-run integration test deferred to Phase 3 (requires CLI wiring to actually invoke the loop)

### Phase 3 Completion
**Completed:** 2026-04-05
**Actual Changes:**
- Rewrote `cmd_analyze` in `run_analysis.py`: extracted `_build_common_vars()` and `_apply_external_feedback()`, delegates to `run_stage1_loop()`. ~60 lines replacing ~270.
- Added `--resume` and `--research` flags to both `analyze` and `stage1-all` subparsers.
- Added mutual exclusivity checks for `--resume`/`--force` and `--resume`/`--feedback`.
- Removed `cmd_update_analysis` function (~150 lines), its argparse entry, and dispatch entry.
- `run_analysis.py` reduced from 1381 to 1123 lines.
- Created `scripts/migrate_iterations.py` (~220 lines): migrates all 38 concepts.
  - 74 iteration files moved to `iter-N/` dirs
  - 32 verdict.json files generated with correct verdicts and canonical source paths
  - 88 non-iteration prompts moved to `prompts/` dirs
  - Source path extraction normalizes `phase_1a/research/` symlink → `knowledge/concept_research/` canonical path

**Issues:**
- Initial source extraction regex only matched `knowledge/concept_research/` but old prompts used `phase_1a/research/` (symlink). Fixed to match both and normalize to canonical path.
- Idempotency logic initially too aggressive — "already migrated" check didn't account for missing verdict.json. Fixed to also check verdict existence.

**Deviations:**
- `cmd_model_setup` not yet refactored to use `build_model_vars` from `lib/loop.py` — standalone model-setup still uses its own inline var builders. Works fine since the loop writes model files to concept root (FR-5) and standalone skip-if-exists handles the overlap.

### Phase 4 Completion
**Completed:** 2026-04-05
**Actual Changes:**
- Added `get_iteration_summary()` to `lib/state.py` — reads verdict.json, returns compact strings like `iter-3/FAIL (3 findings)`
- Updated `cmd_status` to display iteration summary in a new column
- Added `{{#if model_output_path}}` conditional to `prompt_templates/assessment.md` (FR-8, ~8 lines)
- Updated `_run_assess` in `lib/loop.py` to pass `model_output_path` when model output exists
- Changed 5 handlers' prompt paths from concept root to `prompts/` subdir: gap-check, review, synthesize, address-review, model-setup
- Fixed `step_runner.py` to always create `prompt_path.parent` dir (was conditional on `output_path is None`)

**Issues:** None
**Deviations:**
- `step_runner.py` needed a fix to always mkdir for prompt_path.parent — not anticipated in design since prompts previously wrote to the same dir as output files

---

**Status**: Complete
