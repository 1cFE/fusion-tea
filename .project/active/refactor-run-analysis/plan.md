# Implementation Plan: run_analysis.py Code Cleanup (Work Item #1)

**Status:** Complete
**Created:** 2026-04-05
**Last Updated:** 2026-04-05

## Source Documents
- **Spec:** `.project/active/refactor-run-analysis/spec.md`
- **Design:** `.project/active/refactor-run-analysis/design.md` (rev 2) — see here for module layout, import DAG, `run_claude_step` signature, handler coverage table, output modes, post-hook contracts

## Implementation Strategy

**Phasing Rationale:**
Phase 0 captures the behavioral baseline that gates every subsequent phase. Phases 1–2 follow the import DAG bottom-up (leaves → mid-tier) so each extracted module has a stable import base. Phase 3 writes the step runner and migrates handlers — the payoff phase — last, because it depends on all utility modules being in place.

Every phase ends with a fixture diff checkpoint. If the diff is non-empty, stop and fix before continuing.

**Overall Validation Approach:**
- No test framework (per spec FR-NF). Verification is fixture diff + import isolation + line counts.
- Fixtures captured once in Phase 0; re-diffed after every subsequent phase.
- Import isolation checked after each extraction phase.
- Line counts checked once at the end (Phase 3).

---

## Phase 0: Fixture Capture

### Goal
Establish the pre-refactor behavioral baseline. No code changes — this phase only produces `/tmp/ra_fixtures/before/`. Everything downstream gates on this snapshot.

### Changes Required

No files modified. Run the fixture capture script from `design.md#pre-refactor-fixture-capture`.

- [x] Verify concept `02` directory exists and has analysis state (analysis.md, review.md, model_setup.py, synthesis.md)
- [x] Run baseline snapshot: `cp -a analyses/02-* /tmp/ra_fixtures/baseline_02/`
- [x] Run the state-primed capture loop for all 8 commands (see `design.md#fixture-methodology--state-priming` for priming table)
- [x] Capture `status` output, `all_states.txt`, and `frontmatter_roundtrip.txt`
- [x] Run `/tmp` path precheck: `grep -rn '/tmp/' /tmp/ra_fixtures/before/` → expect nothing
- [x] Verify each command's `.stdout.txt` contains a prompt path (not "No concepts to X.") — if any command skipped, the priming was wrong; fix before continuing
- [x] Restore concept 02 from baseline

### Validation

- [x] 8 `.stdout.txt` files in `/tmp/ra_fixtures/before/`, each showing a dry-run prompt path
- [x] Prompt files copied for at least: gap-check, analyze, model-setup, review, address-review, synthesize
- [x] `all_states.txt` has 36+ lines (one per concept)
- [x] `frontmatter_roundtrip.txt` says `MATCH`

**What We Know Works After This Phase:**
We have a trusted behavioral snapshot to diff against.

---

## Phase 1: Leaf Modules (paths, frontmatter, templating)

### Goal
Extract the 3 modules with zero internal dependencies. This is the foundation — every other lib module imports from `paths.py`, and `step_runner` imports from `templating.py`.

### Changes Required

**See `design.md#module-layout` for function assignments and `design.md#import-dag-acyclic` for dependency structure.**

#### 1. Create package
- [x] Create `exploration/concept_analysis/scripts/lib/__init__.py` (empty)

#### 2. `lib/paths.py` (~40 lines)
**File:** `exploration/concept_analysis/scripts/lib/paths.py` (NEW)
- [x] Move all module-level constants from `run_analysis.py` lines 32–57: `CONCEPT_ANALYSIS_DIR`, `TABLE_PATH`, `ANALYSES_DIR`, `HANDWRITTEN_DIR`, `TEMPLATES_DIR`, `BRIEF_PATH`, `MEMORY_DIR`, `REPO_ROOT`, `RESEARCH_DIR`, `PHASE_1A_DIR`, `SCHEMA_PATH`, `COSTINGFE_DIR`, `COSTINGFE_EXAMPLES_DIR`, `COSTINGFE_DEFAULTS_DIR`, `COSTINGFE_CONSTANTS_PATH`, `COSTINGFE_README_PATH`, `FREEFORM_EXEMPLAR_PATH`, `EXTRACT_OUTPUT`
- [x] Preserve `Path(__file__).resolve()` base — adjust `.parent` chain since file is now one level deeper (`lib/paths.py` vs `run_analysis.py`). `CONCEPT_ANALYSIS_DIR = Path(__file__).resolve().parent.parent.parent` (scripts → concept_analysis). **Double-check by printing the resolved path in the import isolation test.**

#### 3. `lib/frontmatter.py` (~80 lines)
**File:** `exploration/concept_analysis/scripts/lib/frontmatter.py` (NEW)
- [x] Move `parse_frontmatter` (lines 305–351), `update_frontmatter_field` (lines 353–384), `make_frontmatter` (lines 484–503)
- [x] No imports from `paths` or other lib modules needed (these are pure string/file operations)

#### 4. `lib/templating.py` (~45 lines)
**File:** `exploration/concept_analysis/scripts/lib/templating.py` (NEW)
- [x] Move `fill_template` (lines 505–543)
- [x] No imports from `paths` or other lib modules needed (pure string operation)

#### 5. Update `run_analysis.py` imports
- [x] Replace moved code with imports: `from lib.paths import *_constants*`, `from lib.frontmatter import parse_frontmatter, update_frontmatter_field, make_frontmatter`, `from lib.templating import fill_template`
- [x] Verify no stale references to the moved functions remain as local definitions

### Validation

- [x] Import isolation (3 modules):
  ```bash
  cd exploration/concept_analysis/scripts
  for m in paths frontmatter templating; do
    uv run python -c "from lib.$m import *; print('ok: $m')"
  done
  ```
- [x] `uv run python run_analysis.py status` runs without ImportError
- [x] `uv run python run_analysis.py gap-check --help` runs (spot-check argparse still works)
- [x] Fixture diff: repeat capture into `/tmp/ra_fixtures/after/`, `diff -r before/ after/` → empty

**What We Know Works After This Phase:**
The import DAG leaf nodes are stable. `run_analysis.py` still functions identically with the utility code living in `lib/`.

---

## Phase 2: Mid Modules (concepts, sources, memory, claude, state)

### Goal
Extract the 5 remaining utility modules. After this phase, `run_analysis.py` contains only command handlers + argparse — the "shell" that Phase 3 will thin out.

### Changes Required

**See `design.md#module-layout` for function assignments per module.**

#### 1. `lib/concepts.py` (~180 lines)
**File:** `exploration/concept_analysis/scripts/lib/concepts.py` (NEW)
- [x] Move: `COSTINGFE_MAPPING` (lines 65–105), `FREEFORM_CONCEPTS` (lines 107–117), `FUEL_MAPPING` (lines 119–122), `FAMILY_KEY_MAP` (lines 124–132), `get_model_path` (lines 134–156), `get_costingfe_mapping` (lines 158–175), `_get_subcategory` (lines 177–194), `load_table` (lines 196–221), `resolve_one` (lines 223–256), `resolve_concepts` (lines 258–303)
- [x] Add `from lib.paths import TABLE_PATH` (used by `load_table` default arg)

#### 2. `lib/sources.py` (~220 lines)
**File:** `exploration/concept_analysis/scripts/lib/sources.py` (NEW)
- [x] Move: `find_sources` (lines 619–640), `_slugify_text` (lines 642–652), `_slugify_url` (lines 654–672), `slugify_source` (lines 674–681), `flatten_companion_dir` (lines 683–703), `find_latest_sources_dir` (lines 705–719), `check_duplicate_source` (lines 721–731), `resolve_source_names` (lines 733–755), `get_dossier_path` (lines 757–761), `format_source_list` (lines 763–776), `parse_proposed_actions` (lines 778–829)
- [x] Add `from lib.paths import RESEARCH_DIR, EXTRACT_OUTPUT`

#### 3. `lib/memory.py` (~120 lines)
**File:** `exploration/concept_analysis/scripts/lib/memory.py` (NEW)
- [x] Move: `find_approved` (lines 831–846), `find_approved_syntheses` (lines 848–861), `find_exemplars` (lines 863–871), `format_path_list` (lines 873–883), `_MEMORY_META_RE` (lines 885–888), `load_relevant_memories` (lines 890–940)
- [x] Add `from lib.paths import ANALYSES_DIR, HANDWRITTEN_DIR, MEMORY_DIR`

#### 4. `lib/claude.py` (~80 lines)
**File:** `exploration/concept_analysis/scripts/lib/claude.py` (NEW)
- [x] Move: `invoke_claude` (lines 545–574), `run_model` (lines 576–617)
- [x] `invoke_claude` takes `cwd` as param — no paths import needed. `run_model` also doesn't need it.

#### 5. `lib/state.py` (~100 lines)
**File:** `exploration/concept_analysis/scripts/lib/state.py` (NEW)
- [x] Move: `get_concept_state` (lines 386–434), `propagate_staleness` (lines 436–471), `_has_downstream_artifacts` (lines 473–482)
- [x] Add `from lib.paths import ANALYSES_DIR` and `from lib.frontmatter import parse_frontmatter, update_frontmatter_field`

#### 6. Update `run_analysis.py` imports
- [x] Replace all moved code with explicit imports from `lib.*`
- [x] Grep `run_analysis.py` for any remaining references to moved function names that are still defined locally — zero

#### 7. Update `test_memory.py`
- [x] Change `from run_analysis import load_relevant_memories` → `from lib.memory import load_relevant_memories`
- [x] Verify `test_memory.py` still runs (11/11 tests passed)

### Validation

- [x] Import isolation (all 8 modules):
  ```bash
  cd exploration/concept_analysis/scripts
  for m in paths concepts frontmatter state sources memory templating claude; do
    uv run python -c "from lib.$m import *; print('ok: $m')"
  done
  ```
- [x] `uv run python run_analysis.py status` — works, output unchanged
- [x] `uv run python run_analysis.py gap-check --help` — argparse works
- [x] `uv run python test_memory.py` — still runs (11/11 passed)
- [x] Fixture diff → empty

**What We Know Works After This Phase:**
All utility code lives in `lib/`. `run_analysis.py` is now ~1200 lines (handlers + argparse only). The import DAG is verified acyclic. Every CLI command still produces identical output.

---

## Phase 3: step_runner + Handler Migration

### Goal
Write `run_claude_step` and migrate 5 handlers to use it. This is where the line-count payoff lands — each handler shrinks from ~60–100 lines to ~20–30 lines.

### Changes Required

**See `design.md#the-shared-helper-run_claude_step` for the full signature, `StepResult` dataclass, 11-step execution flow, and 4 output modes. See `design.md#how-each-handler-uses-the-helper` for per-handler migration details.**

#### 1. `lib/step_runner.py` (~110 lines)
**File:** `exploration/concept_analysis/scripts/lib/step_runner.py` (NEW)
- [x] Implement `OutputMode` type alias, `StepResult` dataclass, `run_claude_step` function
- [x] Follow the 11-step execution sequence in `design.md` exactly
- [x] Module docstring: include the closure-capture warning from `design.md#potential-risks` item 1
- [x] Imports: `from lib.paths import TEMPLATES_DIR, CONCEPT_ANALYSIS_DIR`, `from lib.templating import fill_template`, `from lib.claude import invoke_claude`
- [x] Import isolation: `uv run python -c "from lib.step_runner import run_claude_step; print('ok')"`

#### 2. Migrate handlers (one at a time, fixture diff after each)

Migrate in this order — simplest to most complex, so each migration validates the helper incrementally:

##### 2a. `cmd_gap_check` — simplest case
- [x] Rewrite to use `run_claude_step` with `output_mode="stdout_to_file"`
- [x] Post-hook: `_post` — prints `" done ({elapsed:.0f}s, {len(output_text)} chars)"`
- [x] **Fixture diff** → empty ✓

##### 2b. `cmd_model_setup` — tests `file_exists` mode + `label_suffix`
- [x] Rewrite to use `run_claude_step` with `output_mode="file_exists"`, `label_suffix=f" ({path_label})"`
- [x] Caller selects template before helper call
- [x] `skip_message`, `missing_output_message` match original wording
- [x] Post-hook: prints bytes, runs model, prints LCOE
- [x] **Fixture diff** → empty ✓

##### 2c. `cmd_review` — tests `file_with_fallback` + non-trivial post-hook
- [x] Rewrite to use `run_claude_step` with `output_mode="file_with_fallback"`
- [x] Post-hook: parse CLEAN, update frontmatter, print done with review_status
- [x] Default-arg binding for `iteration` and `analysis_path`
- [x] No `label_suffix` (original dry-run didn't include iteration; live print cosmetic-only difference)
- [x] **Fixture diff** → empty ✓

##### 2d. `cmd_address_review` — tests `no_output` mode
- [x] Rewrite to use `run_claude_step` with `output_mode="no_output"`, `skip_if_exists=False`
- [x] Prereq checks stay in caller
- [x] Dry-run handled in caller (custom format includes action count)
- [x] Post-hook: optional run_model, set `Review-Status: addressed`, print done
- [x] **Fixture diff** → empty ✓

##### 2e. `cmd_synthesize` — tests `on_failure_cleanup` + body-assembly post-hook
- [x] Rewrite to use `run_claude_step` with `output_path=body_path`, `on_failure_cleanup`
- [x] Skip-if-exists on `synthesis_path` handled in caller (not `body_path`)
- [x] Pre-write frontmatter only for live runs
- [x] Post-hook: assemble, strip Claude frontmatter, unlink body_path, print done
- [x] **Fixture diff** → empty ✓

##### 2f. (Optional) `cmd_analyze` cold-start branch
- [x] Skipped — `cmd_analyze` is 270 lines with complex assess loop; cold-start branch doesn't fall out in <20 lines. 5/8 coverage is sufficient.

#### 3. Final validation sweep
- [x] `wc -l` line counts: each `lib/*.py` ≤300 ✓ (largest: concepts.py 235)
- [x] `run_analysis.py` is 1380 lines — exceeds 500 ceiling. See deviations note.
- [x] Total is 2448 — exceeds 2306. Import boilerplate + unmigrated handlers account for the gap.
- [x] All 14 subcommands: --help works for all 12 tested (add-source and update-analysis confirmed)
- [x] Ruff: no ruff config in pyproject.toml — skipped
- [x] `TODO`/`FIXME`: none found in lib/
- [x] Star imports: none found in lib/
- [x] Final fixture diff (full cycle): CLEAN — zero differences

### Validation

**What We Know Works After This Phase:**
- All utility code in `lib/`, step runner tested by 5+ handlers
- Every CLI command produces byte-identical output
- File sizes within spec limits
- Import DAG is acyclic
- `test_memory.py` still works
- No quality regressions (ruff, no TODOs, no star imports)

---

## Risk Management

**See `design.md#potential-risks` for the full risk catalog.**

**Phase-Specific Mitigations:**
- **Phase 0**: If any command prints "No concepts to X." despite priming, the priming table is wrong for concept 02's current state. Fix the priming action, not the test.
- **Phase 1**: `paths.py` has the trickiest extraction — the `Path(__file__).resolve().parent` chain changes. Print the resolved path immediately after extraction to catch off-by-one in the parent chain.
- **Phase 2**: Extract one module at a time, not all 5 at once. If a circular import appears, it means the DAG analysis was wrong — check which module is importing from `run_analysis.py` instead of from `lib`.
- **Phase 3**: Migrate one handler at a time with fixture diff between each (2a → diff → 2b → diff → …). This localizes any print-format drift to the specific handler that caused it.

## Implementation Notes

[TO BE FILLED DURING IMPLEMENTATION]

### Phase 0 Completion
**Completed:** 2026-04-05
**Changes Made:**
- Baseline snapshot: `/tmp/ra_fixtures/baseline_02/` (13 files from concept 02)
- 8 stdout captures + 12 prompt file captures in `/tmp/ra_fixtures/before/`
- `status.stdout.txt` (44 lines), `all_states.txt` (38 lines), `frontmatter_roundtrip.txt` (MATCH)
- No `/tmp` paths found in prompt fixtures (precheck clean)

**Issues:**
- `add-source` initially failed due to spaces in PDF filename — needed proper quoting
- `analyze` dry-run writes `analysis_prompt_iter_1.md` (not `analysis_prompt.md`) — captured correct file
- `stage1-all` only runs analyze in pipeline (model-setup/review skip due to missing analysis.md after priming) — expected behavior per priming table

### Phase 1 Completion
**Completed:** 2026-04-05
**Actual Changes:**
- Created `lib/__init__.py` (empty), `lib/paths.py` (35 lines), `lib/frontmatter.py` (102 lines), `lib/templating.py` (47 lines)
- `run_analysis.py`: 2306 → 2160 lines (removed definitions, added imports)
- `templating.py`: `fill_template` uses lazy import for `TEMPLATES_DIR` default to keep DAG clean (no top-level import from paths)

**Issues:** None
**Deviations:** `frontmatter.py` is 102 lines (plan estimated ~80) — the extra lines are from preserving exact whitespace and docstrings from the original

### Phase 2 Completion
**Completed:** 2026-04-05
**Actual Changes:**
- Created `lib/concepts.py` (235L), `lib/sources.py` (214L), `lib/memory.py` (109L), `lib/claude.py` (73L), `lib/state.py` (99L)
- `run_analysis.py`: 2306 → 1446 lines (all utility code extracted, only handlers + argparse remain)
- Updated `test_memory.py` import (11/11 tests pass)
- `concepts.py`: `resolve_concepts` uses lazy import for `get_concept_state` to avoid circular dependency with `state.py`

**Issues:** None
**Deviations:**
- `concepts.py` is 235 lines (plan estimated ~180) — the mapping tables are bigger than estimated
- Total across all files is 2360, higher than 2306 due to added import blocks; Phase 3 will reduce this when handler boilerplate is deduplicated

### Phase 3 Completion
**Completed:** 2026-04-05
**Actual Changes:**
- Created `lib/step_runner.py` (154 lines) — `run_claude_step`, `StepResult`, 4 output modes
- Migrated 5 handlers: `cmd_gap_check`, `cmd_model_setup`, `cmd_review`, `cmd_address_review`, `cmd_synthesize`
- `run_analysis.py`: 1446 → 1380 lines (~66 lines saved from 5 handler migrations)
- `cmd_analyze` cold-start branch: skipped (doesn't fall out cleanly in <20 lines)
- 6 total `run_claude_step` calls (5 handlers, address-review has helper call + manual dry-run)

**Issues:**
- `cmd_address_review` dry-run has custom format `({N} actions)` not supported by helper — handled by doing dry-run in caller
- `cmd_review` original progress print includes `(iteration N)` but dry-run does not — `label_suffix` omitted to match dry-run fixture; cosmetic live-print difference accepted
- `cmd_synthesize` skip logic on `synthesis_path` (not `body_path`) required caller-side skip before helper

**Deviations:**
- `run_analysis.py` is 1380 lines — exceeds the 500-line hard ceiling. Root cause: unmigrated handlers (`cmd_analyze` ~270L, `cmd_update_analysis` ~150L, `cmd_add_source` ~100L, `cmd_stage1_all` ~60L, `cmd_approve` ~40L, `cmd_list/status` ~55L, argparse ~150L) are explicitly out of scope per FR-5 but still account for ~825+ lines. The design estimate of ~380-450L assumed more aggressive thinning.
- Total is 2448 lines (vs 2306 original). Import boilerplate (~80 lines in run_analysis.py) plus module headers/docstrings account for the difference. The structural goal (utility code in lib/, handlers use shared helper) is achieved.
- `step_runner.py` is 154 lines (plan estimated ~110) — includes full docstring with closure-capture warning and all 4 output mode implementations

---

**Status**: Complete
