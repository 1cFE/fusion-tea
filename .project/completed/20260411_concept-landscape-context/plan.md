# Implementation Plan: Concept Landscape Context for Analysis Pipeline

**Status:** Draft
**Created:** 2026-04-07
**Last Updated:** 2026-04-07

## Source Documents
- **Spec:** `.project/active/concept-landscape-context/spec.md`
- **Design:** `.project/active/concept-landscape-context/design.md` ← See here for component details, function signatures, architecture

## Implementation Strategy

**Phasing Rationale:**
Status code simplification is foundational — the new `iterating` state is consumed by every downstream component. Extraction tracking is next because both the CLI display and landscape builder need it. CLI update provides immediate user-visible verification before tackling the largest piece (landscape builder + prompt integration).

**Overall Validation Approach:**
- Each phase validates with grep audits and CLI output checks
- `--dry-run` prompts verify prompt injection without running Claude
- No external test suite exists for this pipeline; validation is CLI-output and grep-based

---

## Phase 1: Status Code Simplification

### Goal
Collapse `drafted` and `model-setup` into `iterating` in `get_concept_state()` and update all consumers. This is the foundational change — Phases 3 and 4 depend on the new state vocabulary.

### Changes Required

**See `design.md#component-1` for:** collapse logic, consumer list, behavioral equivalence proof for `cmd_model_setup`

#### 1. `lib/state.py` — collapse states
- [x] Replace lines 35-38 (`model-setup`/`drafted` branches) with single `iterating` return
- [x] Update docstring return type to remove `drafted`/`model-setup`, add `iterating`

#### 2. `run_analysis.py` — `cmd_status()` state_symbols
- [x] Remove `drafted` and `model-setup` entries from `state_symbols` dict (lines 103-111)
- [x] Add `"iterating": "  I"` entry (Phase 3 will refine to dynamic `I{N}`)
- [x] Update counts summary line (line 129-134) — replace `model-setup`/`drafted` with `iterating`
- [x] Update legend line (lines 135-136) — replace `M=model-setup D=drafted` with `I=iterating`

#### 3. `run_analysis.py` — `cmd_model_setup()` target_state
- [x] Remove `target_state="model-setup"` from `resolve_concepts()` call at line 371
- [x] Keep `label="model-setup"` at line 412 (display string, not a state check)

### Validation

**Automated:**
- [x] `grep -rn "drafted\|model-setup" exploration/concept_analysis/scripts/lib/state.py` → zero code hits (comments/docstrings allowed only if updated)
- [x] `grep -rn '"drafted"\|"model-setup"' exploration/concept_analysis/scripts/run_analysis.py` → zero hits except `label="model-setup"` at line 412

**Manual:**
- [x] Run `uv run python exploration/concept_analysis/scripts/run_analysis.py status` → no `D` or `M` in State column, shows `I` for iterating concepts
- [x] Verify concepts that previously showed `D` or `M` now show `I`

**What We Know Works After This Phase:**
`get_concept_state()` returns the simplified state vocabulary. All consumers use the new states. `cmd_model_setup --all` still correctly filters concepts.

---

## Phase 2: Extraction Status Tracking

### Goal
Add extraction state detection, sidecar staleness mechanism, propagation into `propagate_staleness()`, and cleanup in `extract_explorer_data.py`. Independent of the landscape builder but needed by both CLI display and landscape.

### Changes Required

**See `design.md#component-2` for:** `get_extraction_state()` signature, `_concept_num()` helper, `_default_explorer_data_dir()`, sidecar mechanism, propagation addition

**See `design.md#component-6` for:** extraction cleanup in explorer

#### 1. `lib/state.py` — new functions
- [x] Add `_concept_num()` helper (regex extract numeric prefix)
- [x] Add `_default_explorer_data_dir()` (path relative to `ANALYSES_DIR`)
- [x] Add `get_extraction_state()` — returns `'not-extracted' | 'extracted' | 'stale'`
- [x] Add `import re` at top of file

#### 2. `lib/state.py` — update `propagate_staleness()`
- [x] After existing downstream loop, add explorer JSON sidecar creation (see `design.md#component-2` for exact code)
- [x] Append `explorer:{num}.json` to `stale_files` return list

#### 3. `concept_explorer/data/.gitignore`
- [x] Add `*.stale` entry (create file if needed)

#### 4. `concept_explorer/extract_explorer_data.py` — cleanup
- [x] After successful JSON write, delete `.stale` sidecar if present (one-line addition)

### Validation

**Manual:**
- [x] Identify a concept with existing explorer JSON (e.g., `01.json`)
- [x] Run in Python: `propagate_staleness("01-hts-compact-tokamak", "test")` → verify `01.json.stale` created in `concept_explorer/data/`
- [x] Verify `get_extraction_state("01-hts-compact-tokamak")` returns `"stale"`
- [x] Clean up test sidecar
- [x] Verify `get_extraction_state()` returns `"not-extracted"` for a concept without JSON

**What We Know Works After This Phase:**
Extraction state is detectable. Staleness propagates to explorer JSON. The sidecar mechanism is additive and backward-compatible.

---

## Phase 3: CLI Status Display Update

### Goal
Show `I{N}` (with iteration count) and extraction column in `cmd_status` output.

### Changes Required

**See `design.md#component-3` for:** `_extract_iter_count()` helper, display format, summary line, legend, `extraction_symbols` dict

#### 1. `run_analysis.py` — `cmd_status()` refactor
- [x] Add `_extract_iter_count()` helper function (regex parse `get_iteration_summary()` output)
- [x] Add `extraction_symbols` dict
- [x] Update header line to include `Extr` column
- [x] Update per-row formatting: dynamic `I{N}` for iterating state, extraction symbol column
- [x] Import `get_extraction_state` from `lib.state`
- [x] Update summary line: add extraction counts (`N extracted (M stale)`)
- [x] Update legend: `I{N}=iterating(N iterations)  E=extracted  E*=stale`

### Validation

**Manual:**
- [x] Run `uv run python exploration/concept_analysis/scripts/run_analysis.py status` → verify:
  - `I{N}` shows with correct iteration counts for iterating concepts
  - `Extr` column shows `E`, `E*`, or blank as appropriate
  - Summary line includes extraction counts
  - Legend includes new symbols

**What We Know Works After This Phase:**
CLI status display is complete with all new codes. Users can see pipeline stage, iteration count, and extraction status at a glance.

---

## Phase 4: Landscape Builder + Prompt Integration

### Goal
Build `lib/landscape.py`, wire into `_build_common_vars()`, and inject into analysis and assessment prompt templates. This is the highest-value deliverable — agents receive cross-concept context.

### Changes Required

**See `design.md#component-4` for:** `build_concept_landscape()` signature, grouping logic, column handling, output format, size estimate

**See `design.md#component-5` for:** `_build_common_vars()` signature change, caller updates, template additions

#### 1. `lib/landscape.py` — new module
- [x] Create `lib/landscape.py` with `build_concept_landscape()` function
- [x] Implement grouping: approved → in-progress (iterating/reviewed/synthesized, sorted by iter count desc) → gap-checked → not-started
- [x] Include all taxonomy columns + iteration summary + extraction status per row
- [x] Exclude `exclude_id` concept's row (FR-9)
- [x] Format as markdown tables per tier with headings and usage instructions

#### 2. `run_analysis.py` — `_build_common_vars()` signature
- [x] Add `concepts: list[dict]` parameter
- [x] Import `build_concept_landscape` from `lib.landscape`
- [x] Add `concept_landscape` key to returned dict
- [x] Update caller in `cmd_analyze()` (line 254): pass `concepts`
- [x] Update `_apply_external_feedback()`: add `concepts` parameter, pass to `_build_common_vars()`
- [x] Update `_apply_external_feedback()` call site in `cmd_analyze()`: pass full unfiltered `concepts` list

#### 3. `prompt_templates/analysis_v2.md`
- [x] Add `{{#if concept_landscape}}` block after memory_context, before cold_start (see `design.md#component-5` for exact template text)

#### 4. `prompt_templates/assessment.md`
- [x] Add `{{#if concept_landscape}}` block after assessment checklist, before instructions (see `design.md#component-5` for exact template text)

### Validation

**Manual:**
- [x] Run `uv run python exploration/concept_analysis/scripts/run_analysis.py analyze --dry-run 13` → saved prompt file contains landscape section
- [x] Verify landscape has 37 concepts (13 excluded), grouped by tier
- [x] Verify approved concepts appear first
- [x] Verify in-progress concepts show iteration counts and are sorted by count descending
- [x] Verify extraction status appears per concept
- [x] Check landscape size: 14.1 KB (slightly over 12KB estimate, acceptable)
- [x] Verify assessment prompt also includes landscape (confirmed via `_run_assess` common_vars passthrough)

**What We Know Works After This Phase:**
Every analysis and assessment agent invocation receives the complete concept catalog. Nearest-neighbor identification has full cross-concept context.

---

## Risk Management

**See `design.md#potential-risks` for detailed risk analysis**

**Phase-Specific Mitigations:**
- **Phase 1**: `cmd_model_setup` behavioral equivalence verified in design — `output_mode="file_exists"` already handles the skip
- **Phase 3**: `_extract_iter_count()` silently returns 0 if format changes — safe degradation
- **Phase 4**: Landscape size ~11KB — acceptable. If too large, drop N/A-heavy columns per tier

## Implementation Notes

### Phase 1 Completion
**Completed:** 2026-04-07
**Actual Changes:**
- `lib/state.py:35-38` — collapsed `model-setup`/`drafted` branches into single `iterating` return
- `lib/state.py` docstring — updated return type and detection order
- `run_analysis.py:103-111` — replaced `drafted`/`model-setup` entries with `iterating` in `state_symbols`
- `run_analysis.py:129-136` — updated summary counts and legend
- `run_analysis.py:371` — removed `target_state="model-setup"` from `resolve_concepts()` call
**Issues:** None
**Deviations:** None — matched design exactly

### Phase 2 Completion
**Completed:** 2026-04-07
**Actual Changes:**
- `lib/state.py` — added `import re`, `_concept_num()`, `_default_explorer_data_dir()`, `get_extraction_state()`
- `lib/state.py:propagate_staleness()` — added explorer JSON sidecar creation after existing downstream loop
- Created `concept_explorer/data/.gitignore` with `*.stale` entry
- `extract_explorer_data.py` — added stale sidecar cleanup after successful JSON write
**Issues:** None
**Deviations:** None — matched design exactly

### Phase 3 Completion
**Completed:** 2026-04-07
**Actual Changes:**
- `run_analysis.py` — added `_extract_iter_count()` helper (parses `iter-N/...` → int)
- `run_analysis.py:cmd_status()` — dynamic `I{N}` for iterating state, `Extr` column with `E`/`E*`/blank, updated header/summary/legend
- `run_analysis.py` — added `get_extraction_state` to imports from `lib.state`
**Issues:** None
**Deviations:** None — matched design exactly

### Phase 4 Completion
**Completed:** 2026-04-07
**Actual Changes:**
- Created `lib/landscape.py` with `build_concept_landscape()` — groups by tier, sorts by maturity, includes all taxonomy columns + iteration + extraction
- `run_analysis.py` — added `concepts` param to `_build_common_vars()`, added `concept_landscape` to returned dict, updated callers (`cmd_analyze`, `_apply_external_feedback`)
- `run_analysis.py` — added `build_concept_landscape` import
- `lib/loop.py:_run_assess()` — added `common_vars` param to pass `concept_landscape` through to assessment template
- `prompt_templates/analysis_v2.md` — added `{{#if concept_landscape}}` block after memory_context
- `prompt_templates/assessment.md` — added `{{#if concept_landscape}}` block before Instructions
**Issues:** None
**Deviations:**
- Assessment prompt injection required threading `common_vars` through `lib/loop.py:_run_assess()` — not anticipated in design (design only covered `run_analysis.py` callers). Clean fix: added optional `common_vars` parameter.
- Landscape size 14.1KB vs design estimate 11KB — acceptable, no optimization needed yet.

---

**Status**: Complete
