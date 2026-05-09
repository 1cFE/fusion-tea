---
date: 2026-04-26T13:47:28-05:00
researcher: Claude
topic: "Sensitivity analysis / slider recompute — state of implementation"
tags: [research, concept-explorer, sensitivity, sliders, costingfe]
status: complete
last_updated: 2026-04-26
---

# Research: Sensitivity Analysis / Slider Recompute — State of Implementation

**Date**: 2026-04-26T13:47:28-05:00
**Researcher**: Claude
**Research Type**: Codebase

## Research Question

The concept explorer was built with "sensitivity analysis" capabilities — the ability to re-run `model_setup.py` through 1costingfe when supported. What is the conceptual design, what's built, and how is it surfaced in the front end?

## Summary

- **The full slider/recompute pipeline is fully built and wired end-to-end** — backend, frontend, CSS, tests.
- Sliders appear on the **concept profile page** (single concept view) only for costingfe-backed concepts that have sensitivity data.
- The **comparison view** (`view_sensitivity.js`) shows sensitivity *charts* (tornado overlays) but has **no slider/recompute controls** — this is explicitly out of scope per spec 12.
- The system works by calling `POST /api/compute` with parameter overrides, which re-runs `model.forward()` server-side and returns updated `CostModelData`.
- If you're not seeing sliders, it's likely because the loaded concepts either (a) lack `model_setup` paths (standalone concepts), or (b) have `has_sensitivities: false` in their data JSON.

## Detailed Findings

### Conceptual Design

The sensitivity/recompute system has two distinct layers:

1. **Static sensitivity analysis** — Pre-computed elasticities (`dLCOE/dp * p/LCOE`) for each parameter. Computed once at data extraction time by calling `model.sensitivity()` (costingfe) or `compute_sensitivity()` / finite-difference (standalone). Stored in `CostModelData.sensitivities` as `SensitivityAnalysis` with `engineering` and `financial` dicts of `SensitivityEntry(elasticity, baseline)`. These power the **tornado chart**.

2. **Live recompute ("what-if" sliders)** — The user drags a slider, the frontend debounces (200ms), calls `POST /api/compute` with `{concept_id, overrides: {param: value}}`, the server re-runs `model.forward()` with the overridden parameters, and returns a fresh `CostModelData`. The **headline economics card and CAS breakdown update** in place; the **tornado chart bars do NOT change** (they always show baseline elasticities).

The key design constraint: **sensitivity elasticities are NEVER recomputed on slider change** (spec 12, line 40). This is a deliberate performance decision — `model.sensitivity()` is expensive. The tornado stays at baseline; only the headline numbers and CAS chart reflect the overridden parameters.

### Backend Implementation (fully built)

**`server.py`** — Three pieces:

1. **Module loader** (`_load_model_module`, lines 120-136): Imports a `model_setup.py` file by path, suppresses stdout, caches with `@lru_cache(maxsize=32)`. Thread-safe via `_MODULE_LOAD_LOCK`.

2. **Forward-with-overrides** (`_forward_with_overrides`, lines 139-163): Merges `base_params` with `overrides`, splits named args (`_FORWARD_NAMED`) from physics/plant kwargs, calls `model.forward()`. Named args derived by introspecting `CostModel.forward`'s signature at import time (`_derive_forward_named`, lines 75-105), with hardcoded fallback if costingfe isn't installed.

3. **Compute endpoint** (`_compute_cached` + `compute`, lines 534-582): `POST /api/compute` → validates concept exists and has `model_setup` → calls `_compute_cached(concept_id, frozenset(overrides.items()))` → returns `CostModelData`. LRU-cached (maxsize=128), keyed on `(concept_id, frozen_overrides)`. Baseline sensitivities are always injected from the stored concept data, not recomputed.

**`models.py`** — `ComputeRequest` (line 448): `{concept_id: str, overrides: dict[str, float]}`. `CostModelData.from_forward_result()` (line 186) constructs the response from `dataclasses.asdict(forward_result)`.

### Frontend Implementation (fully built)

**`concept.html.j2`** (lines 33-46): Template has the slider DOM scaffolding:
```html
<div id="sliders-section" style="display: none;">
  <h3 class="section__subheading">Parameter What-If</h3>
  <div id="sliders-container" class="sliders-container"></div>
</div>
```
Plus `headline-loading` spinner and `compute-error` elements.

**`concept_page.js`** (lines 222-510): Full slider implementation:
- `renderSliders()` (lines 234-305): Creates a range input for each parameter that has `ParameterMetadata.range`. Slider bounds come from `[lo, hi]`, step = `(hi-lo)/200`. Value label shows `val * display_multiplier` in `display_unit`. Debounces `onSliderChange` callback at 200ms.
- Init block (lines 458-510): Gates on `isCostingfe && concept.has_sensitivities && concept.cost_model?.sensitivities`. On slider change: shows loading spinner, calls `POST /api/compute`, updates headline card + CAS breakdown, reports slider state via `POST /api/state`.

**`explorer.css`** (lines 906-945): Complete slider styling — `.slider-row`, `.slider-row__label`, `.slider-row__input`, `.slider-row__value`.

### Comparison View — Sensitivity Charts Only (no sliders)

**`view_sensitivity.js`**: This is the comparison page's sensitivity view. It has two modes:
- **Integrated mode**: Grouped tornado chart showing union of top-N parameters across all selected concepts, with shared params sorted to top and a dotted divider.
- **Landscape mode**: Per-concept top-N tornado with confidence encoding (opacity + hatch for low-confidence), synced symmetric x-axis.

Neither mode has slider controls. This is explicitly **out of scope** per spec 12: "Slider controls in the comparison view" is listed under "Out of Scope".

### Data Flow — What Gates Slider Visibility

Sliders only appear when ALL of these are true:
1. `concept.sources.model_setup != null` — the concept has a `model_setup.py` path
2. `concept.has_sensitivities == true` — sensitivity data was extracted
3. `concept.cost_model.sensitivities` is non-null — actual sensitivity entries exist
4. At least one parameter in sensitivities has a matching entry in `concept.parameter_metadata` with a `.range` defined

If sliders aren't showing for a concept, check the concept's data JSON for these fields.

### Test Coverage

**`tests/test_state_and_compute.py`** — 8 tests covering:
- Standalone concept → 422
- Costingfe concept → valid `CostModelData`
- Override changes LCOE (fake module: `LCOE = 100 * 0.85 / availability`)
- Cache hit (module not reloaded)
- Different overrides cached independently
- Missing concept → 404
- State round-trip and timestamp validation

### What's Saved as "What-If" Scenarios

Per spec 12, "Saving what-if scenarios" is **out of scope**. Slider state is only persisted in the server's in-memory `ExplorerState` (via `POST /api/state`), which resets on server restart. There is no persistence layer.

## Code References

- `exploration/concept_explorer/server.py:75-163` — Module loading and forward-with-overrides
- `exploration/concept_explorer/server.py:534-582` — `_compute_cached` and `compute` endpoint
- `exploration/concept_explorer/models.py:186-298` — `CostModelData.from_forward_result()`
- `exploration/concept_explorer/models.py:448-451` — `ComputeRequest`
- `exploration/concept_explorer/static/js/concept_page.js:222-305` — `renderSliders()`
- `exploration/concept_explorer/static/js/concept_page.js:458-510` — Slider init + compute callback
- `exploration/concept_explorer/templates/concept.html.j2:33-46` — Slider DOM scaffolding
- `exploration/concept_explorer/static/css/explorer.css:906-945` — Slider CSS
- `exploration/concept_explorer/static/js/view_sensitivity.js` — Comparison view sensitivity charts (no sliders)
- `exploration/concept_explorer/docs/specs/12-computation-api.md` — Full specification
- `exploration/concept_explorer/extract_explorer_data.py:132-156` — `build_sensitivity_analysis()`
- `exploration/concept_explorer/tests/test_state_and_compute.py` — 8 compute/state tests

## Architecture Insights

The system cleanly separates:
- **Extraction time**: Sensitivity elasticities computed once, stored in JSON
- **Request time**: `model.forward()` re-invoked with overrides, but sensitivities never recomputed
- **Caching**: LRU on `(concept_id, frozen_overrides)` — deterministic, never invalidated during server lifetime

The `_derive_forward_named()` pattern (introspecting `CostModel.forward`'s signature) is a nice touch — it adapts to costingfe API changes without hardcoding. Falls back to a hardcoded set for test environments.

## Recommendations

If the question is "why aren't sliders showing?":
1. Check a concept's data JSON: does it have `sources.model_setup` set to a real path?
2. Does `has_sensitivities` == `true`?
3. Does `parameter_metadata` have entries with non-null `range`?
4. Run the server locally and check browser console for errors.

If the goal is to add sliders to the **comparison view**, that's a new feature (spec 12 explicitly deferred it). Would require deciding: do all selected concepts share sliders, or does each get its own? Do they re-render the integrated tornado, or just the headline numbers?

## Parameter Landscape (from live server data, 2026-04-26)

### Gating conditions — verified against live data

Checked all 36 concepts via `GET /api/concepts/{id}`:
- **36/36** have `has_sensitivities: true`
- **19/36** have `sources.model_setup` set (costingfe-backed, support live recompute)
- **0/36** have any entries in `parameter_metadata` — every single concept returns `{}`
- **0/36** have a `model_metadata.yaml` file on disk

Sliders require all four conditions. Condition 4 (metadata with `range`) fails universally.

### Parameter name inventory

Surveyed all 38 concept entries in the extracted data (some concepts have multiple entries):

| Metric | Count |
|--------|-------|
| Total unique parameter names across all concepts | 249 |
| Engineering parameters | 247 |
| Financial parameters | 2 (`interest_rate`, `inflation_rate`) |
| Shared (appear in >1 concept) | 78 |
| Concept-unique (appear in exactly 1 concept) | 171 |

**Shared parameters** (78): `B`, `M_blanket`, `M_ion`, `Q_sci`, `R0`, `R_w`, `T_e`, `T_edge`, `Z_eff`, `availability`, `b_max`, `blanket_energy_multiplication`, `blanket_t`, `blanket_thickness_m`, `blanket_unit_cost`, `burn_fraction`, `chamber_inner_radius_m`, `chamber_length`, `construction_time_years`, `construction_time_yr`, `core_lifetime_FPY`, `dd_f_He3`, `dd_f_T`, `deuterium_cost_per_kg`, `dhe3_dd_frac`, `dhe3_f_T`, `disruption_damage`, `disruption_downtime`, `disruption_rate_base`, `disruption_steepness`, `elon`, `eta_de`, `eta_dec`, `eta_p`, `eta_pin`, `eta_th`, `f_GW`, `f_dec`, `f_rad`, `f_rep`, `f_sub`, `fuel_recovery`, `ht_shield_t`, `inflation_rate`, `interest_rate`, `lambda_q`, `mn`, `n_e`, `om_cost_per_MW_yr`, `p_coils`, `p_cool`, `p_cryo`, `p_cryo_MW`, `p_ecrh`, `p_fus_MW`, `p_house`, `p_house_MW`, `p_input`, `p_nbi`, `p_pump`, `p_target`, `p_trit`, `p_trit_MW`, `plant_availability`, `plant_lifetime_years`, `plasma_t`, `plasma_volume`, `q95`, `q_eng`, `r_coil`, `rep_rate_Hz`, `shield_thickness_m`, `structure_t`, `structure_thickness_m`, `tau_ratio`, `thermal_efficiency`, `vessel_t`, `vessel_thickness_m`

**Notable synonyms** (same concept, different names across models):
- `availability` vs `plant_availability`
- `construction_time_yr` vs `construction_time_years`
- `eta_th` vs `thermal_efficiency`
- `plant_lifetime_years` (standalone) vs `lifetime_yr` (costingfe forward arg)

### Example: Concept 01 (HTS Compact Tokamak)

47 sensitivity parameters (45 engineering + 2 financial). Representative sample:
- `availability: 0.80` — plant capacity factor
- `eta_th: 0.33` — thermal efficiency
- `R0: 5.0` — major radius (m)
- `interest_rate: 0.07` — discount rate
- `p_cryo: 30.0` — cryogenic power (MW)
- `disruption_rate_base: 0.01` — disruptions per year

### Costingfe display metadata — none exists

Checked `/home/reid/1cfe/1costingfe/src/costingfe/model.py`. Costingfe provides:
- Parameter categorization (engineering vs financial vs costing keys)
- `sensitivity()` method returning elasticities

It does NOT provide: display names, units, multipliers, or range bounds. Parameter names in costingfe are raw Python identifiers.

## Prior Research

This problem was previously researched on 2026-04-13:
- `.project/research/20260413-parameter-metadata-pipeline-trace.md` — same diagnosis, same root cause, recommended auto-generation in the extractor

## Spec

Work item created: `.project/active/parameter-metadata-generation/spec.md`
