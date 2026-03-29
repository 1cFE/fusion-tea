
## Purpose
Serve live cost model recomputation with parameter overrides, enabling interactive slider what-if exploration.

## Requirements
- `POST /api/compute` accepts `ComputeRequest(concept_id, overrides: dict[str, float])` and returns `CostModelData`
- Only costingfe-backed concepts support computation; standalone concepts return HTTP 422 with `{"detail": "Concept does not support live computation"}`
- The computation calls `model.forward(overrides)` on the appropriate costingfe model instance then `CostModelData.from_forward_result()`
- Results are cached with LRU keyed on `(concept_id, frozenset(overrides.items()))` — cache size ~100 entries
- Sensitivity is recomputed on each call (not cached separately from the forward result) unless profiling shows it is prohibitively slow
- The baseline result for each costingfe concept is pre-warmed into the cache at server startup

## Acceptance Criteria
- `POST /api/compute` with `{"concept_id": "01-hts-compact-tokamak", "overrides": {"availability": 0.8}}` returns `CostModelData` with updated `headline.lcoe_per_mwh`
- The same request sent twice produces identical responses (cache hit on second call)
- `POST /api/compute` for a standalone concept returns HTTP 422
- `POST /api/compute` for a nonexistent `concept_id` returns HTTP 404
- The cache warms for all costingfe concepts at startup without raising errors

## Interfaces
- **File**: `exploration/concept_explorer/server.py`
- **Request model**: `ComputeRequest` (see `01-data-models.md`)
- **Response model**: `CostModelData` (see `01-data-models.md`)
- **Depends on**: `02-costingfe-adapter.md` (`from_forward_result()`), 1costingfe `CostModel`
- **Called by**: `17-concept-profile-page.md` (slider debounce handler)

## Constraints
- NEVER run `model.forward()` synchronously on the hot path without profiling — if >200ms, move to a background thread and return 202 Accepted
- NEVER return a cached result for a different override set (cache key must include all override values)
- HTTP 422 MUST be returned for standalone concepts, not 404

## Out of Scope
- Sensitivity-only recomputation without a full forward pass
- Persistent computation history
- Multi-concept batch computation

