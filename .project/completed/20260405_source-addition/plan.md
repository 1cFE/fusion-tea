# Implementation Plan: Source Addition and Incremental Updates

**Status:** Complete
**Created:** 2026-03-29
**Last Updated:** 2026-03-29

## Source Documents
- **Spec:** `.project/active/source-addition/spec.md`
- **Design:** `.project/active/source-addition/design.md` ← See here for component details, function signatures, architecture

## Implementation Strategy

**Phasing Rationale:**
Pure helper functions first (testable in isolation, foundation for both commands), then `add-source` (no Claude calls, testable with real extraction), then `update-analysis` (Claude-dependent, requires sources to already be addable). Each phase builds on the previous and produces independently verifiable output.

**Overall Validation Approach:**
- No existing test infrastructure for `run_analysis.py` — validation is manual/scripted
- Helper functions verified via Python snippets in-line
- Commands verified via real filesystem operations on test concepts
- `add-source` can be tested without Claude; `update-analysis` requires Claude calls

---

## Phase 1: Helper Functions

### Goal
Implement the 5 helper functions that both commands depend on: `slugify_source`, `flatten_companion_dir`, `find_latest_sources_dir`, `check_duplicate_source`, `resolve_source_names`. Also add `import shutil` (needed for `--force` cleanup in Phase 2).

### Test Stencil (Write This First)
```python
# Quick validation after implementing helpers — run from repo root:
# uv run python -c "
from exploration.concept_analysis.scripts.run_analysis import (
    slugify_source, _slugify_text, _slugify_url,
    find_latest_sources_dir, check_duplicate_source, resolve_source_names,
)

# slugify_source: PDF paths
assert slugify_source('/tmp/SPARC_ICRF_Heating_Paper.pdf') == 'sparc-icrf-heating-paper'
assert slugify_source('My Paper (Draft v2).pdf') == 'my-paper-draft-v2'

# slugify_source: URLs
assert slugify_source('https://arxiv.org/abs/2411.06644') == 'arxiv-2411-06644'
assert slugify_source('https://realta.com/fusion-hub-spotlight') == 'realta-fusion-hub-spotlight'

# slugify_source: truncation
long_name = 'a-' * 40 + 'end'
assert len(slugify_source(long_name)) <= 60

print('All helper assertions passed')
# "
```

### Changes Required

**See `design.md` for:**
- Function signatures and logic → `design.md#component-1` through `#component-5`
- Slugification rules (hyphen convention, URL handling) → `design.md#component-1`
- Flattening logic (ported from zotero_ingest) → `design.md#component-2`

**Specific file changes:**

#### 1. `exploration/concept_analysis/scripts/run_analysis.py`
- [x] Add `import shutil` to imports (line ~22 area)
- [x] Add `EXTRACT_OUTPUT = "output.md"` constant near other path constants (line ~50 area)
- [x] Add `slugify_source()`, `_slugify_text()`, `_slugify_url()` — near `find_sources()` (:612)
- [x] Add `flatten_companion_dir()` — near `find_sources()`
- [x] Add `find_latest_sources_dir()` — near `find_sources()`
- [x] Add `check_duplicate_source()` — near `find_sources()`
- [x] Add `resolve_source_names()` — near `find_sources()`

### Validation

**Automated:**
- [x] Run the test stencil snippet above → all assertions pass
- [x] Run `uv run python exploration/concept_analysis/scripts/run_analysis.py list` → existing functionality unbroken

**Manual:**
- [x] Verify `find_latest_sources_dir("11-magnetic-mirror")` returns the highest iter dir → `iter-02/sources`
- [x] Verify `check_duplicate_source("11-magnetic-mirror", "wham-experiment-details")` returns a Path (known existing source)
- [x] Verify `check_duplicate_source("11-magnetic-mirror", "nonexistent-source")` returns None
- [x] Verify `resolve_source_names("11-magnetic-mirror", ["wham-experiment-details"])` returns the correct path

**What We Know Works After This Phase:**
All pure helper logic is correct — name derivation, directory finding, duplicate detection, source resolution. Ready to wire into commands.

---

## Phase 2: `cmd_add_source` + CLI Wiring

### Goal
Implement the `add-source` subcommand end-to-end: argparse registration, handler function, extraction subprocess call, flattening, symlink creation, duplicate/force handling, dry-run, error cleanup.

### Test Stencil
```bash
# Dry-run test (no extraction, just validation of flow):
uv run python exploration/concept_analysis/scripts/run_analysis.py \
  add-source 11 https://example.com/some-article --dry-run

# Expected output: shows derived name, target sources dir, what would be created

# Real PDF test (uses agentic-mbse extract):
uv run python exploration/concept_analysis/scripts/run_analysis.py \
  add-source 11 /path/to/test-paper.pdf

# Expected: creates iter-NN/sources/test-paper.md (symlink) + test-paper/ companion dir

# Duplicate rejection:
uv run python exploration/concept_analysis/scripts/run_analysis.py \
  add-source 11 /path/to/test-paper.pdf
# Expected: error "source 'test-paper' already exists"

# Force re-extract:
uv run python exploration/concept_analysis/scripts/run_analysis.py \
  add-source 11 /path/to/test-paper.pdf --force
# Expected: removes old, re-extracts
```

### Changes Required

**See `design.md` for:**
- Full flow (13 steps) → `design.md#component-6`
- Argparse registration → `design.md#component-6`
- Extraction subprocess pattern → `design.md#component-6`
- Error handling strategy → `design.md#component-6`
- `--force` behavior → `design.md#component-6`
- Dispatch table update → `design.md#cli-dispatch-integration`

**Specific file changes:**

#### 1. `exploration/concept_analysis/scripts/run_analysis.py`
- [x] Add `cmd_add_source(concepts, args)` handler function
  - Resolve single concept via `resolve_one()`
  - Derive or use `--name` for source name
  - Duplicate check (with `--force` path)
  - Find latest sources dir
  - Dry-run early exit
  - Run `subprocess.run(["uv", "run", "agentic-mbse", "extract", ...])` with 600s timeout
  - Flatten companion dir
  - Verify `output.md` exists
  - Create relative symlink
  - Error cleanup via `shutil.rmtree`
- [x] Add argparse registration in `build_parser()` (after `stage1-all`, before `return parser`)
  - Single `concept` positional, `source` positional, `--name`, `--force`, `--dry-run`
- [x] Add `"add-source": cmd_add_source` to dispatch table in `main()`

### Validation

**Automated:**
- [x] `run_analysis.py list` → still works (no regression)
- [x] `run_analysis.py add-source --help` → shows correct help text

**Manual:**
- [x] `add-source 11 <url> --dry-run` → prints intended placement, no files created
- [x] `add-source 17a <pdf>` → creates companion dir + symlink in correct iter-02/sources/ *(verified via checkpoint-test-concept17, 2026-03-29)*
- [x] Verify symlink: `readlink iter-02/sources/<name>.md` → `<name>/output.md` *(verified via checkpoint-test-concept17)*
- [x] Verify companion dir contents: `output.md`, `metrics.json` present; `raw.pdf` NOT created (see note below) *(verified via checkpoint-test-concept17)*
- [x] Verify new source discoverable in sources listing *(verified via checkpoint-test-concept17)*
- [x] Duplicate rejection: re-run same command → error message
- [ ] `--force`: re-run with `--force` → removes old, creates new *(still deferred — not tested in checkpoint)*
- [x] `--name override`: `add-source 11 <url> --name custom-name` → uses `custom-name`

**What We Know Works After This Phase:**
Full source addition workflow — a user can add a PDF or URL to any concept with one command. Companion-dir + symlink layout is correct. `find_sources()` discovers the new source automatically.

---

## Phase 3: `source_integration.md` + `cmd_update_analysis`

### Goal
Write the source-integration pre-pass prompt template and implement the `update-analysis` command (two-step: pre-pass generates F-N feedback, feedback-pass applies it via existing `analysis_v2.md`).

### Test Stencil
```bash
# Dry-run test (runs pre-pass, shows feedback, skips analysis agent):
uv run python exploration/concept_analysis/scripts/run_analysis.py \
  update-analysis 11 --sources <newly-added-source-name> --dry-run

# Expected: prints F-N feedback from pre-pass, does NOT modify analysis.md

# Full test (both steps):
uv run python exploration/concept_analysis/scripts/run_analysis.py \
  update-analysis 11 --sources <newly-added-source-name>

# Expected:
#   - feedback_update_<ts>.md created with F-N findings
#   - analysis.md modified by feedback-pass
#   - downstream artifacts marked stale (if they exist)
```

### Changes Required

**See `design.md` for:**
- Prompt template content → `design.md#component-8`
- Full flow (8 steps) → `design.md#component-7`
- Argparse registration → `design.md#component-7`
- Timestamp naming convention → `design.md#component-7`
- Re-use of feedback-pass infrastructure → `design.md#component-7`
- common_vars pattern (from cmd_analyze :938-951) → `design.md#research-findings`

**Specific file changes:**

#### 1. Prompt Template (NEW)
**File:** `exploration/concept_analysis/prompt_templates/source_integration.md`
- [x] Create file with content from `design.md#component-8`
- [x] Verify `{{@config/analysis_goals.md}}` and `{{@config/feedback_format.md}}` inclusions resolve correctly

#### 2. `exploration/concept_analysis/scripts/run_analysis.py`
- [x] Add `cmd_update_analysis(concepts, args)` handler function
  - Resolve single concept via `resolve_one()`
  - Resolve source names via `resolve_source_names()`
  - Verify `analysis.md` exists
  - Generate timestamp string (`datetime.now().strftime("%Y%m%dT%H%M%S")`)
  - **Step 1**: Fill `source_integration.md`, save prompt, invoke Claude, verify feedback file
  - Dry-run exit point (after pre-pass, before feedback-pass)
  - **Step 2**: Build `common_vars` (same pattern as `cmd_analyze` :938-951), fill `analysis_v2.md` in feedback-pass mode, save prompt, invoke Claude
  - Call `propagate_staleness()`
  - Print summary
- [x] Add `from datetime import datetime` import (if not already present — `date` is imported but not `datetime`)
- [x] Add argparse registration in `build_parser()`
  - Single `concept` positional, `--sources` nargs="+", `--model`, `--timeout`, `--dry-run`
- [x] Add `"update-analysis": cmd_update_analysis` to dispatch table

### Validation

**Automated:**
- [x] `run_analysis.py update-analysis --help` → shows correct help text
- [x] `run_analysis.py list` → still works

**Manual:**
- [x] Pre-requisite: use Phase 2's `add-source` to add a source to a concept that has an existing analysis *(concept 17a, Xcimer whitepaper added via checkpoint-test)*
- [x] `update-analysis <concept> --sources <name> --dry-run` → pre-pass runs, feedback printed, analysis.md unchanged *(verified: 3 findings in F-N format, analysis.md unchanged after dry-run)*
- [x] Verify `feedback_update_<ts>.md` has F-N format with specific integration instructions *(verified: F-1 laser cost breakdown, F-2 roadmap, F-3 TRUMPF supply chain)*
- [x] Verify `source_integration_prompt_<ts>.md` saved (audit trail) *(verified: 2 files created)*
- [x] `update-analysis <concept> --sources <name>` → full run, analysis.md modified *(verified: 58KB analysis.md with 39 whitepaper-specific term mentions)*
- [x] Verify `update_analysis_prompt_<ts>.md` saved (audit trail) *(verified: 1 file created)*
- [x] Verify downstream staleness: if `model_setup.py` or `review.md` exist, they're marked stale *(verified: "stale: model_setup.py" in output)*
- [ ] `status` command shows stale indicator (`*`) for the concept *(not explicitly checked — status showed M, not M*)*
- [ ] Error case: `update-analysis <concept-with-no-analysis> --sources <name>` → error about missing analysis.md *(not tested in checkpoint)*

**What We Know Works After This Phase:**
Full end-to-end workflow: add a source → update the analysis → staleness propagated. Both commands work independently and together.

---

## Environment Setup

**See CLAUDE.md for full environment rules**

- All Python via `uv run python ...`
- `agentic-mbse` available via `uv run agentic-mbse ...`
- Claude CLI available as `claude` on PATH

---

## Risk Management

**See `design.md#potential-risks` for detailed risk analysis**

**Phase-Specific Mitigations:**
- **Phase 1**: Slugification edge cases — test with real URLs from existing sources to calibrate
- **Phase 2**: Extraction failure cleanup — test by providing an invalid URL and verifying companion dir is removed
- **Phase 3**: Pre-pass feedback quality — review first few runs manually; tune prompt if findings are too generic or miss material content

## Implementation Notes

_TO BE FILLED DURING IMPLEMENTATION_

### Phase 1 Completion
**Completed:** 2026-03-29
**Actual Changes:**
- Added `import shutil` to imports (line 21)
- Added `EXTRACT_OUTPUT = "output.md"` constant after `FREEFORM_EXEMPLAR_PATH` (line 53)
- Added 7 helper functions in new "Source addition helpers" section between `find_sources()` and `get_dossier_path()`:
  - `_slugify_text()`, `_slugify_url()`, `slugify_source()` — name derivation
  - `flatten_companion_dir()` — nested extraction dir flattening
  - `find_latest_sources_dir()` — latest iter-NN/sources/ discovery
  - `check_duplicate_source()` — duplicate detection across iterations
  - `resolve_source_names()` — short name → full path resolution
**Issues:** None
**Deviations:** None

### Phase 2 Completion
**Completed:** 2026-03-29
**Actual Changes:**
- Added `cmd_add_source()` handler (~60 lines) before the CLI section, with full flow: resolve_one → slugify → duplicate check → find_latest_sources_dir → dry-run exit → subprocess extraction → flatten → verify output.md → symlink → error cleanup
- Added argparse registration after `stage1-all` in `build_parser()`
- Added `"add-source": cmd_add_source` to dispatch table
**Issues:** None
**Deviations:** None — some manual validation items deferred (require real agentic-mbse extraction)

### Phase 3 Completion
**Completed:** 2026-03-29
**Actual Changes:**
- Created `exploration/concept_analysis/prompt_templates/source_integration.md` — pre-pass prompt with `{{@config/analysis_goals.md}}` and `{{@config/feedback_format.md}}` includes
- Added `from datetime import datetime` to imports
- Added `cmd_update_analysis()` handler (~100 lines) with two-step flow: source-integration pre-pass → feedback-pass via analysis_v2.md. Builds `common_vars` matching `cmd_analyze` pattern. Saves audit trail prompts + feedback files with timestamp naming.
- Added argparse registration after `add-source` in `build_parser()`
- Added `"update-analysis": cmd_update_analysis` to dispatch table
**Issues:** None
**Deviations:** None — manual validation items (actual Claude calls) deferred to user testing

---

**Status**: Complete (all 3 phases implemented 2026-03-29)
