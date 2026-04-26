# Spec: Parameter Metadata Generation

**Status:** Draft
**Owner:** Reid W
**Created:** 2026-04-26 14:34 PDT
**Complexity:** MEDIUM
**Branch:** pipeline-cleanup

---

## Work Item Summary

The concept explorer has a fully built slider/recompute system that lets users adjust parameters and see updated LCOE and CAS breakdown in real time. The entire pipeline works — backend endpoint, frontend rendering, CSS, tests — but **sliders never appear** because the data that drives them doesn't exist.

## Why This Matters Now

A significant feature is completely invisible. Users land on a concept profile page and see a static tornado chart and CAS breakdown, with no way to explore "what if availability were higher?" or "what if interest rate dropped?" — even though every line of code to support that interaction is already shipped.

## Key Bets / Constraints

- **Bet:** All the data needed to generate parameter metadata already exists at extraction time — baselines, sensitivity keys, parameter types. No new data sources are required.
- **Constraint:** The existing `model_metadata.yaml` override path MUST be preserved — if someone hand-authors metadata for a concept, it should win over auto-generated values.
- **Non-goal:** This work item does not change the frontend, backend, or compute endpoint. Those are done.

---

## Business Goals

### Why This Matters

The slider system was built as part of the concept explorer (spec 12, "Computation API and Slider Controls"). It works end-to-end when given proper data. But sliders depend on `ParameterMetadata` entries — specifically, each parameter needs a `display_name`, `range`, `baseline`, and other fields. These were designed to come from hand-authored `model_metadata.yaml` files, one per concept. The extraction spec (spec 02) explicitly put "authoring `model_metadata.yaml`" as out of scope. Nobody ever authored them. Zero files exist across all 36 concepts.

The result: `load_parameter_metadata()` returns `{}` for every concept. The frontend's `renderSliders()` sees no parameters with `range` and skips rendering entirely. The "Parameter What-If" section stays `display: none`.

### Success Criteria

- [ ] Sliders appear on concept profile pages for concepts that support live recompute
- [ ] Dragging a slider calls `POST /api/compute` and updates headline economics + CAS breakdown
- [ ] Parameter display names are human-readable (not raw Python variable names like `eta_th`)
- [ ] Slider ranges are physically reasonable (no efficiency > 100%, no negative power)

### Priority

P1 — unblocks a fully-built, fully-tested feature.

---

## Problem Statement

### Current State

- 36 concepts have sensitivity data (`has_sensitivities: true`)
- 19 concepts have `model_setup` paths (costingfe-backed, support live recompute)
- `parameter_metadata` is `{}` for every single concept
- `renderSliders()` requires at least one parameter with a `range` field to show anything
- Zero `model_metadata.yaml` files exist anywhere in the repo
- The concept profile page shows Economics, Sensitivity Analysis (tornado), and CAS Cost Breakdown — but no slider controls

### Desired Outcome

Concept profile pages for costingfe-backed concepts show slider controls. Users can adjust parameters and see the economics update. The data pipeline generates the metadata that the existing frontend/backend already consume.

---

## Scope

### In Scope

- Generating `ParameterMetadata` entries during extraction so that `parameter_metadata` is populated in concept data JSON files
- Covering the parameter names that appear in sensitivity analysis (249 unique across all concepts: 78 shared, 171 concept-unique)
- Re-extracting concepts to populate the metadata

### Out of Scope

- Frontend changes (already built — `concept_page.js:234-510`)
- Backend changes (already built — `server.py:534-582`)
- CSS changes (already built — `explorer.css:906-945`)
- Slider controls on the comparison page (deferred per spec 12)
- Saving what-if scenarios (deferred per spec 12)
- Recomputing sensitivity elasticities on slider change (deferred per spec 12)

---

## Requirement Selection Notes

There is one real requirement here: the extraction pipeline must produce `ParameterMetadata` entries that satisfy the frontend's existing rendering conditions. Everything else — how to generate display names, how to derive ranges, how to handle unknown parameters — is design territory.

---

## Requirements

### Functional Requirements

1. **FR-1**: After extraction, costingfe-backed concepts MUST have non-empty `parameter_metadata` with entries for parameters that appear in their sensitivity analysis.
2. **FR-2**: Each generated `ParameterMetadata` entry MUST include `display_name`, `baseline`, `range`, `category`, and `confidence` — these are required fields on the Pydantic model.
3. **FR-3**: If a `model_metadata.yaml` file exists for a concept, its entries MUST override the auto-generated entries for the same parameter names.
4. **FR-4**: Generated slider ranges SHOULD be physically reasonable — no values that violate known constraints (e.g., efficiencies > 1.0, negative quantities).

---

## Acceptance Criteria

### Core Functionality
- [ ] At least one costingfe-backed concept shows slider controls on its profile page after re-extraction
- [ ] Dragging a slider triggers `POST /api/compute` and the headline card updates with new values
- [ ] All 19 costingfe-backed concepts have non-empty `parameter_metadata` in their data JSON
- [ ] No extraction errors or Pydantic validation failures from auto-generated metadata

### Quality & Integration
- [ ] Existing tests continue to pass (`pytest exploration/concept_explorer/tests/`)
- [ ] `model_metadata.yaml` override path still works (if a YAML file is created, its entries take precedence)
- [ ] Tornado chart and CAS breakdown continue to render correctly (no regressions)

---

## Next-Stage Handoff

**Settled in this spec:**
- The problem is purely data generation — no frontend/backend/CSS changes needed
- The fix lives in the extraction pipeline (`extract_explorer_data.py`)
- `model_metadata.yaml` remains the override mechanism

**Design must figure out:**
- How to generate human-readable display names for 249 parameter names (static registry? heuristic? hybrid?)
- How to derive physically reasonable slider ranges from baselines
- How to assign `category` and `confidence` values
- Whether to generate metadata for freeform/standalone concepts (sliders won't work for them, but display names would enrich tornado charts)
- Where the registry/mapping data lives (inline in extractor? separate file?)

**Watch-outs for design:**
- 78 shared params appear across multiple concepts; 171 are concept-unique. A purely static registry won't cover everything without a fallback strategy.
- Some parameters have the same semantic meaning but different names across concepts (e.g., `construction_time_yr` vs `construction_time_years`, `availability` vs `plant_availability`). The design should decide whether to normalize these.
- The `costingfe-scaled-overrides` work item (`.project/active/costingfe-scaled-overrides/`) is in progress and also touches the extractor. Coordinate.

---

## Related Artifacts

- **Research:** `.project/research/20260413-parameter-metadata-pipeline-trace.md`
- **Research:** `.project/research/20260426-134728_sensitivity-analysis-state.md`
- **Spec 12:** `exploration/concept_explorer/docs/specs/12-computation-api.md`
- **Spec 02:** `exploration/concept_explorer/docs/specs/02-data-extraction.md`
- **Active (related):** `.project/active/costingfe-scaled-overrides/`

---

**Next Steps:** After approval, proceed to `/_my_design`
