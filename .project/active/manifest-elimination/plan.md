# Implementation Plan: Eliminate Static Manifest and Parameter Index

**Status:** Draft
**Created:** 2026-04-26
**Last Updated:** 2026-04-26

## Source Documents
- **Spec:** `spec.md`
- **Design:** `design.md` — see here for component details, test impact survey, migration hazards

## Implementation Strategy

**Phasing Rationale:** Pure refactor first (move functions), then behavior change (wire server), then test cleanup. Each phase is independently verifiable.

**Critical Path:** Move builders → wire server → fix fixtures

**First Proof Point:** Phase 1 — all existing tests pass after relocating builder functions. Proves they have no hidden coupling to extraction internals.

---

## Phase 1: Move builders to models.py

### Goal
Relocate `build_manifest()` and `build_parameter_index()` from `extract_explorer_data.py` to `models.py`. Update all imports. Zero behavior change.

### Assumption Under Test
The builder functions are pure — no hidden dependencies on extraction-module state or imports.

### Test Stencil (Write This First)
No new tests. Existing `TestBuildManifest` and `TestBuildParameterIndex` in `test_extraction.py:670-720` are the proof — they must pass after the import path changes.

### Changes Required

#### 1. `exploration/concept_explorer/models.py`
- [x] Add `build_manifest()` function (cut from `extract_explorer_data.py:649-684`)
- [x] Add `build_parameter_index()` function (cut from `extract_explorer_data.py:687-726`)
- [x] Add necessary imports (`datetime`, `UTC`, `Confidence`, `ParameterCategory` — verify which are already present)

#### 2. `exploration/concept_explorer/extract_explorer_data.py`
- [x] Replace `build_manifest` / `build_parameter_index` definitions with imports from `models`
- [x] Verify extraction still calls them at lines 824-832 (don't remove yet — Phase 2)

#### 3. `exploration/concept_explorer/tests/test_extraction.py:670-720`
- [x] Update imports: `from ...models import build_manifest, build_parameter_index`

### Validation
- [x] `uv run python -m pytest exploration/concept_explorer/tests/test_extraction.py -x` — all pass (44 tests)
- [x] `uv run python -m pytest exploration/concept_explorer/tests/ -x` — full test suite, no regressions (153 tests; playwright-dependent test_*_manual.py files skipped — pre-existing fixture issue unrelated to this change)
- [ ] Run extraction on one concept to verify it still writes manifest: `uv run python exploration/concept_explorer/extract_explorer_data.py --concept 19 --skip-narrative` (deferred — about to remove this write in Phase 2)

**What We Know Works After This Phase:** Builder functions are cleanly importable from `models.py`. All existing behavior preserved.

---

## Phase 2: Wire server startup + strip extraction writes

### Goal
`_load_data()` computes manifest and parameter index from loaded concepts. `run_extraction()` stops writing those files.

### Assumption Under Test
Server-computed manifest is identical in shape to the previously file-based one.

### Test Stencil (Write This First)
```python
# AC-1: bare data dir startup
def test_load_data_without_manifest_files(tmp_path):
    """Server starts with only per-concept JSONs — no manifest.json needed."""
    data_dir = tmp_path / "data"
    data_dir.mkdir()
    # Write one minimal ConceptData JSON
    (data_dir / "01.json").write_text(minimal_concept_json("01"))
    
    concepts, manifest, param_index = _load_data(data_dir)
    assert len(manifest.concepts) == 1
    assert manifest.concepts[0].concept_id == "01"
```

### Changes Required

#### 1. `exploration/concept_explorer/server.py` — `_load_data()`
- [x] Remove manifest_path existence check and file read (lines 212-217, 241)
- [x] Remove index_path existence check and file read (lines 219-224, 242)
- [x] Add `from .models import build_manifest, build_parameter_index`
- [x] After loading concepts dict, call `build_manifest(list(concepts.values()))` and `build_parameter_index(list(concepts.values()))`
- [x] Keep `manifest.json` and `parameter_index.json` in `_NON_CONCEPT_FILES` (see `design.md#2` — stale file hazard)
- [x] Add comment on `generated_at` noting it now records server start time, not extraction time

#### 2. `exploration/concept_explorer/extract_explorer_data.py` — `run_extraction()`
- [x] Remove lines 824-832 (manifest + parameter_index generation and file writes)
- [x] Remove the import of `build_manifest` / `build_parameter_index` (no longer called here)

#### 3. New test: `tests/test_server.py` — AC-1 regression
- [x] Add `test_load_data_without_manifest_files` per stencil above
- [x] Added bonus `test_load_data_ignores_stale_manifest_files` to cover the stale-files-on-disk migration hazard from design.md#2

### Validation
- [x] `uv run python -m pytest exploration/concept_explorer/tests/test_server.py -x` — passes for new AC-1 tests; pre-existing tests fail due to fixture mismatch (expected; fixed in Phase 3)
- [ ] Start server manually with current `data/` dir (has stale manifest.json on disk) — verify it starts and `/api/manifest` returns all concepts (deferred — covered by `test_load_data_ignores_stale_manifest_files` unit test)
- [ ] Delete `data/manifest.json` and `data/parameter_index.json`, restart server — verify it still starts (deferred — covered by `test_load_data_without_manifest_files` unit test)

**What We Know Works After This Phase:** Server computes manifest at startup. Extraction is per-concept only. Stale files on disk don't crash anything.

---

## Phase 3: Fix test fixtures + regression tests

### Goal
Align all test fixtures with the new reality (no manifest files). Add AC-4 regression test. Clean up monkeypatches.

### Assumption Under Test
All tests exercise real behavior, not stale fixture patterns.

### Test Stencil (Write This First)
```python
# AC-4: filtered extraction doesn't hide concepts
def test_filtered_extraction_preserves_other_concepts(tmp_path):
    """Running --concept 01 must not affect visibility of other concepts."""
    data_dir = tmp_path / "data"
    data_dir.mkdir()
    # Pre-populate with 01.json through 05.json
    for i in range(1, 6):
        (data_dir / f"{i:02d}.json").write_text(minimal_concept_json(f"{i:02d}"))
    
    # Re-extract only concept 01 (overwrites 01.json)
    run_extraction(analyses_dir, data_dir, concept_filter=["01"])
    
    # Server should see all 5
    concepts, manifest, _ = _load_data(data_dir)
    assert len(manifest.concepts) == 5
```

### Changes Required

#### 1. `tests/test_server.py`
- [x] Remove `_minimal_manifest()` helper (line 53)
- [x] Remove manifest.json + parameter_index.json writes from fixtures
- [x] Ensure fixtures write per-concept JSONs (they already do)

#### 2. `tests/test_taxonomy_server.py:108-110`
- [x] Remove manifest.json + parameter_index.json writes from fixtures

#### 3. `tests/test_state_and_compute.py:191-196`
- [x] Remove manifest.json + parameter_index.json writes from `costingfe_base_dir` fixture

#### 4. `tests/test_extraction.py:856-858`
- [x] Rework filtered extraction test: assert only `01.json` was written, not manifest contents

#### 5. `concept_analysis/scripts/test_failure_chains.py:1431-1438`
- [x] Remove `build_manifest` / `build_parameter_index` monkeypatches
- [x] Verify H-19 stale-marker test still exercises stale-marker creation/cleanup

#### 6. New test: AC-4 regression
- [x] Add `test_filtered_extraction_preserves_other_concepts` per stencil above

### Validation
- [x] `uv run python -m pytest exploration/concept_explorer/tests/ -x` — all pass (209 passed, 5 skipped; manual playwright suites pre-skipped)
- [x] `uv run python -m pytest exploration/concept_analysis/ -x` — failure chains test passes (53 passed, 5 skipped)
- [x] Verify no test imports `build_manifest` from `extract_explorer_data` — confirmed via grep

**What We Know Works After This Phase:** Full test suite green. Both regression tests (AC-1, AC-4) cover the motivating bug.

---

## Phase 4: Documentation

### Goal
Update docs that reference manifest.json / parameter_index.json as extraction outputs.

### Changes Required
- [x] `exploration/concept_explorer/README.md` (lines 39, 42, 61-62, 293-294, 310)
- [x] `exploration/concept_explorer/docs/DESIGN.md` (lines 47-48, 691) — file is at this path, not `docs/DESIGN.md` as the plan said
- [x] Note: these are now computed at server startup, not generated by extraction

### Validation
- [x] Read updated docs for accuracy

---

## Risk Management

See `design.md#risk` for full analysis.

**Phase-Specific:**
- **Phase 1**: Near-zero risk — pure move, tests prove it.
- **Phase 2**: Stale files on disk — mitigated by keeping names in `_NON_CONCEPT_FILES`.
- **Phase 3**: Missed fixture — design review caught 4 test files. Grep for `manifest.json` across test files before declaring done.

## Implementation Notes

### Phase 1 Completion
**Completed:** 2026-04-26
**Actual Changes:**
- `models.py`: added `from datetime import UTC, datetime`; appended `build_manifest()` and `build_parameter_index()` after `ComputeRequest` (with section header comment).
- `extract_explorer_data.py`: removed `build_manifest`/`build_parameter_index` definitions and the section comment header; trimmed model imports (dropped now-unneeded `ConceptManifest`, `ConceptManifestEntry`, `Confidence`, `ParameterCategory`, `ParameterConceptEntry`, `ParameterIndex`, `ParameterIndexEntry`); added `build_manifest`/`build_parameter_index` to the model import list; removed unused `from datetime import UTC, datetime` import.
- `tests/test_extraction.py`: moved `build_manifest`/`build_parameter_index` from extract_explorer_data import block into models import block.
**Issues:** None.
**Deviations:** Minor — also pruned newly-unused model imports from `extract_explorer_data.py` rather than leaving them dangling.

### Phase 2 Completion
**Completed:** 2026-04-26
**Actual Changes:**
- `server.py`: imported `build_manifest`/`build_parameter_index` from `.models`; rewrote `_load_data()` to drop manifest_path/index_path existence checks and file reads, glob per-concept JSONs first, then call the builders against `list(concepts.values())`; expanded the docstring to call out the in-memory computation and the stale-file rationale; left `_NON_CONCEPT_FILES` set unchanged.
- `extract_explorer_data.py`: deleted the post-loop `build_manifest`/`build_parameter_index` invocations and `manifest.json`/`parameter_index.json` writes; removed the `build_manifest`/`build_parameter_index` model imports (now unused).
- `tests/test_server.py`: imported `_load_data`; added `test_load_data_without_manifest_files` (AC-1) and a sibling `test_load_data_ignores_stale_manifest_files` covering design.md#2; rewrote `test_startup_fails_when_data_dir_empty` to drop its manifest.json/parameter_index.json fixture writes (the `RuntimeError` it asserts now fires before any read of those files anyway).
**Issues:** None.
**Deviations:**
- Added a second AC-1 test (`test_load_data_ignores_stale_manifest_files`) to lock down the stale-file hazard explicitly. Plan only listed one test; this is additive.
- Trimmed the now-pointless manifest/parameter_index writes inside `test_startup_fails_when_data_dir_empty` instead of waiting for Phase 3 — it sat alongside the AC-1 tests and would have been confusing to leave as-is.

### Phase 3 Completion
**Completed:** 2026-04-26
**Actual Changes:**
- `tests/test_server.py`: dropped `_minimal_manifest`/`_minimal_parameter_index` helpers; added `_concept_with_sensitivities` so the fixture concept produces an "availability" entry in the server-computed parameter index; trimmed model imports; rewrote `base_dir` to write only per-concept JSON; refreshed the comment in `test_parameter_index_validates_as_parameter_index`.
- `tests/test_taxonomy_server.py`: dropped `_minimal_manifest`/`_minimal_parameter_index` helpers; trimmed model imports; rewrote `base_dir` fixture to skip manifest/parameter_index writes (taxonomy seed copies still happen).
- `tests/test_state_and_compute.py`: trimmed model imports; removed `_manifest_entry` helper; rewrote `costingfe_base_dir` to drop the manifest.json and parameter_index.json writes.
- `tests/test_extraction.py`: rewrote `TestConceptFilter::test_filters_to_single_concept` to assert manifest.json/parameter_index.json are NOT written (post-refactor extraction is per-concept only); appended new AC-4 regression test `test_filtered_extraction_preserves_other_concepts` that pre-populates 01–05.json, runs `--concept 01` extraction, then calls `_load_data` and asserts all five remain visible.
- `concept_analysis/scripts/test_failure_chains.py`: removed the two `build_manifest`/`build_parameter_index` monkeypatches in the H-19 stale-marker test (no longer needed — extraction never touches them).
**Issues:** None.
**Deviations:**
- Cleaned up stale `_manifest_entry` helper / unused imports in `tests/test_state_and_compute.py` rather than leave them dangling. Plan only said "remove writes" — pruning the now-orphaned support code keeps the file coherent.

### Phase 4 Completion
**Completed:** 2026-04-26
**Actual Changes:**
- `exploration/concept_explorer/README.md`: redrew the Stage 2 ASCII diagram so it shows only `{id}.json` as extraction output; rewrote the Stage 2 narrative to call out that `ConceptManifest` and `ParameterIndex` are computed at server startup, not by extraction; updated the "Output Generation" section's enumeration; rewrote step 1 of "Startup Lifecycle" to describe in-memory computation and the stale-file handling.
- `exploration/concept_explorer/docs/DESIGN.md`: removed `manifest.json` and `parameter_index.json` lines from the directory tree; rewrote the extraction "Key steps" comment block to drop the manifest/index build steps and add a NOTE pointing at `_load_data` and the `models.py` builder functions.
**Issues:** Plan listed `docs/DESIGN.md`, but the file is actually at `exploration/concept_explorer/docs/DESIGN.md`. Top-level `docs/` has no DESIGN.md. Updated the right file.
**Deviations:**
- Did not touch the historical planning artifacts (`exploration/concept_explorer/docs/IMPLEMENTATION_PLAN_v1.md`, `specs/03-server.md`, `DESIGN_REVIEW.md`) — those are dated design records that describe the original intent at the time of writing and aren't in the plan's scope.
