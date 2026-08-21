# Design: Eliminate Static Manifest and Parameter Index

**Status:** Draft
**Created:** 2026-04-26

---

## Approach

Move `build_manifest()` and `build_parameter_index()` from extraction-time to server-startup-time. Both functions already take `list[ConceptData]` — the server already has that list. Wire them in, delete the file I/O.

## Changes

### 1. `models.py` — relocate builder functions

Move `build_manifest()` (`extract_explorer_data.py:649`) and `build_parameter_index()` (`extract_explorer_data.py:687`) into `models.py`. They are pure functions: `list[ConceptData] → ConceptManifest` and `list[ConceptData] → ParameterIndex`. Zero extraction dependencies — they only touch Pydantic models already defined in `models.py`.

Why `models.py` and not leave them in the extraction script: the server needs to call them, and having the server import `extract_explorer_data` would pull in extraction-specific dependencies (subprocess calls, dynamic module loading, narrative prompts) that have no business in the server's import graph.

### 2. `server.py` — `_load_data()`

Currently returns `(concepts, manifest, parameter_index)` by loading three files. Change to:

- Load per-concept JSONs into `concepts: dict[str, ConceptData]` (unchanged)
- Call `build_manifest(list(concepts.values()))` to compute manifest in memory
- Call `build_parameter_index(list(concepts.values()))` to compute parameter index in memory
- **Remove**: manifest_path existence check, index_path existence check, file reads for both
- **Keep `manifest.json` and `parameter_index.json` in `_NON_CONCEPT_FILES`**. Existing deployments will still have these files on disk. If removed from the exclusion set, the concept glob picks them up and `ConceptData.model_validate_json()` crashes on non-concept JSON. Keeping them in the set is cheap and forward-safe.

`generated_at` semantics: currently records when extraction ran. Under the new design it records when the server started. Functionally equivalent for the frontend (it's used as a cache key), but the meaning shifts. Add a comment on the field noting this.

### 3. `extract_explorer_data.py` — `run_extraction()`

Remove lines 824-832 (manifest and parameter_index generation + file writes). The function becomes: discover → extract each → write per-concept JSON. Done.

Remove the now-unused imports of `build_manifest` and `build_parameter_index` (they live in `models.py` now).

### 4. Tests

**Full test impact:**

- **`tests/test_server.py`**: Fixtures (`_minimal_manifest`, line 53) write `manifest.json` and `parameter_index.json` to temp `data/` dir. Remove that setup — server builds them from per-concept JSONs the fixtures already write. Remove `_minimal_manifest` helper.

- **`tests/test_taxonomy_server.py:108-110`**: Same pattern — writes manifest.json + parameter_index.json in fixtures. Same fix: remove, let server compute.

- **`tests/test_state_and_compute.py:191-196`**: `costingfe_base_dir` fixture writes manifest.json and parameter_index.json. Same fix: remove, let server compute from per-concept JSONs.

- **`tests/test_extraction.py:670-720`**: `TestBuildManifest` and `TestBuildParameterIndex` import `build_manifest` and `build_parameter_index` from `extract_explorer_data`. After the move to `models.py`, these imports break. Update imports to `from ...models import build_manifest, build_parameter_index`. Tests themselves are still valid — they test the builder logic regardless of where it lives.

- **`concept_analysis/scripts/test_failure_chains.py:1431-1438`**: Monkeypatches `build_manifest` / `build_parameter_index` against `extract_explorer_data` in the H-19 stale-marker test. After the move, these monkeypatches become no-ops — extraction no longer calls the builders, so stubbing them does nothing. The test's intent (avoid heavy computation during stale-marker testing) is now satisfied by default. Remove the monkeypatches; verify the test still exercises stale-marker creation/cleanup.

- **`test_extraction.py:856-858`**: The `--concept 01` filter test uses `manifest.json` as evidence that filtered extraction works. With manifest generation removed, deleting the assertion would leave the test verifying nothing useful. **Rework**: assert that only `01.json` was written (and pre-existing `02.json` etc. were not overwritten). This tests what filtered extraction actually guarantees.

- **New regression test — AC-1 (bare data dir startup)**: Create only `01.json` in `data/` (no manifest.json, no parameter_index.json). Call `_load_data()`. Assert it returns successfully and the manifest contains 1 entry.

- **New regression test — AC-4 (filtered extraction doesn't hide concepts)**: Pre-populate `data/` with `01.json` through `05.json`. Run `run_extraction(concept_filter=["01"])`. Call `_load_data()`. Assert the manifest has 5 entries. This is the contract: filtered extraction does not affect which concepts the server sees.

### 5. Documentation

Update references to `manifest.json` / `parameter_index.json` as extraction outputs:

- `exploration/concept_explorer/README.md` (lines 39, 42, 61-62, 293-294, 310)
- `docs/DESIGN.md` (lines 47-48, 691)

Note that these files are now computed at server startup, not generated by extraction.

## What Doesn't Change

- `ConceptManifest`, `ConceptManifestEntry`, `ParameterIndex`, `ParameterIndexEntry` models — same shapes, same API contracts
- Frontend — hits same endpoints, gets same JSON
- Per-concept extraction pathways (costingfe / standalone) — untouched
- Narrative extraction — untouched

## Risk

Low. The manifest and parameter index are pure derivations of data the server already loads. The computation is trivial (40 iterations over in-memory objects). No behavioral change observable from the frontend.

The one migration hazard (stale files on disk crashing the glob) is handled by keeping both names in `_NON_CONCEPT_FILES`.
