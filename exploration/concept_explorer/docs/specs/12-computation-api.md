# Computation API and Slider Controls

## Purpose
Allow users to adjust parameter values on a concept profile page and see updated LCOE and CAS breakdown in real time via server-side model recomputation.

## Requirements
- `POST /api/compute` accepts `{ concept_id, overrides: dict[str, float] }` and returns `CostModelData`
- Recomputes using `model.forward()` with the overridden parameters applied
- Sensitivity data in the response uses pre-computed baseline elasticities (NOT recomputed on each slider change)
- Only costingfe-backed concepts support computation; standalone concepts return HTTP 422
- In-memory LRU cache keyed on `(concept_id, frozenset(overrides.items()))` — same params → same result
- Frontend slider controls appear only for costingfe-backed concepts with sensitivity data
- Sliders are bounded by `ParameterMetadata.range` for each parameter
- Slider changes are debounced (200ms) before calling `POST /api/compute`
- On slider change, updated `slider_overrides` are reported via `POST /api/state`
- After computation, only headline economics and CAS breakdown are updated; tornado chart bars remain at baseline

## Acceptance Criteria
- Given a costingfe concept with `availability` overridden to 0.80 (vs. baseline 0.70), when `POST /api/compute` is called, then the returned `headline.lcoe_per_mwh` differs from the baseline value
- Given a standalone concept, when `POST /api/compute` is called, then HTTP 422 is returned with `{"detail": "Slider computation only available for costingfe-backed concepts"}`
- Given `POST /api/compute` is called twice with identical `concept_id` and `overrides`, when the second call is made, then the result is served from cache (no second call to `model.forward()`)
- Given a user drags a slider, when fewer than 200ms have elapsed since the last drag event, then no API call is made
- Given a user drags a slider, when 200ms have elapsed since the last drag event, then `POST /api/compute` is called once
- Given a valid computation response, when the frontend receives it, then the headline card and CAS breakdown update; the tornado chart bars do NOT change
- Given a parameter with `range: [0.50, 0.85]`, when the slider renders, then its minimum is 0.50 and maximum is 0.85
- Given `POST /api/compute` fails (HTTP 500), then an error state is shown near the affected components and the last valid values remain displayed

## Interfaces
```
POST /api/compute  body: ComputeRequest → CostModelData
  ComputeRequest: { concept_id: str, overrides: dict[str, float] }
```
- **Slider UI**: rendered by `concept_page.js` only when `model_type === "costingfe"` and `sensitivities` is non-null
- **Per-slider bounds**: from `ParameterMetadata.range` in `concept.parameter_metadata`
- **Updates**: `renderCASBreakdown()` and headline card; does NOT call `renderTornado()`
- **State reporting**: calls `POST /api/state` with updated `slider_overrides` after computation
- **Depends on**: `specs/03-server.md` (FastAPI app), `specs/01-data-models.md` (ComputeRequest, CostModelData), `specs/11-explorer-state.md` (state reporting), 1costingfe `model.forward()`

## Constraints
- NEVER recompute sensitivity (elasticities) on slider change — serves baseline sensitivities only
- NEVER show slider controls for standalone concepts
- NEVER block the UI during computation — show a loading indicator while the request is in-flight
- Cache must not be invalidated between requests (computation is deterministic)
- Sliders must not allow values outside `ParameterMetadata.range`; clamp if necessary

## Out of Scope
- Recomputing sensitivity elasticities on slider change (deferred pending profiling)
- Saving "what-if" scenarios
- Batch computation across multiple parameter combinations
- Slider controls in the comparison view
