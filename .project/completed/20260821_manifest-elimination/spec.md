# Spec: Eliminate Static Manifest and Parameter Index

**Status:** Implementation Complete
**Created:** 2026-04-26
**Complexity:** Small

---

## Problem

`extract_explorer_data.py` generates three outputs: per-concept `{id}.json` files, `manifest.json`, and `parameter_index.json`. The manifest and parameter index are **rebuilt from scratch** on every extraction run, using only the concepts extracted in that run. A filtered run (`--concept 19`) overwrites the manifest with a single entry, hiding all other concepts from the UI — even though their `.json` files are intact.

The server already loads every per-concept JSON into memory at startup (`server.py:244-247`). The manifest and parameter index contain no information that isn't derivable from those loaded objects. They are redundant derived artifacts with a destructive rebuild behavior.

## Requirements

1. The server must compute the manifest and parameter index at startup from loaded per-concept JSON files — no static files required.
2. `GET /api/manifest` and `GET /api/parameter_index` must return identical response shapes (same Pydantic models, same field semantics).
3. Extraction (`extract_explorer_data.py`) must stop generating `manifest.json` and `parameter_index.json`.
4. Filtered extraction runs (`--concept 04`) must not affect which concepts appear in the UI.
5. Existing tests for `/api/manifest` and `/api/parameters` endpoints must pass with equivalent setup (test fixtures create per-concept JSONs, not manifest files).

## Out of Scope

- Changing the ConceptManifest / ParameterIndex Pydantic models themselves (they stay as the API response shape).
- Changing the per-concept JSON format or extraction pathways.
- Changing the frontend — it hits the same endpoints with the same response shape.
- Performance optimization of startup computation (40 concepts, trivially fast).

## Acceptance Criteria

- [x] Server starts successfully with only `{id}.json` files in `data/` (no manifest.json, no parameter_index.json). — covered by `test_load_data_without_manifest_files` and `test_load_data_ignores_stale_manifest_files`.
- [x] `GET /api/manifest` returns all concepts present as `.json` files in `data/`. — covered by existing `test_manifest_validates_as_concept_manifest`, now backed by computed manifest.
- [x] `GET /api/parameter_index` returns cross-concept sensitivity data for all loaded concepts. — covered by `test_parameter_index_validates_as_parameter_index` (fixture concept now has sensitivities so a real entry is computed).
- [x] Running `--concept 19` extraction followed by server start shows all 40 concepts in the grid. — covered by `test_filtered_extraction_preserves_other_concepts` (AC-4 regression).
- [x] All existing server tests pass (with fixture adjustments). — 209 tests passing in `exploration/concept_explorer/tests/` + `exploration/concept_analysis/scripts/test_failure_chains.py`.
