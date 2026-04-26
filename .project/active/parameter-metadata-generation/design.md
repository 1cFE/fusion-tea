# Design: Parameter Metadata Generation

**Status:** Draft
**Owner:** Reid W
**Created:** 2026-04-26
**Updated:** 2026-04-26
**Branch:** pipeline-cleanup
**Commit:** 150d572

## Overview

Generate `ParameterMetadata` entries from data already available at extraction time — sensitivity baselines and parameter categories — so the existing slider UI lights up without any manual authoring.

## Related Artifacts

- **Spec:** `.project/active/parameter-metadata-generation/spec.md`
- **Research:** `.project/research/20260426-134728_sensitivity-analysis-state.md`
- **Research:** `.project/research/20260413-parameter-metadata-pipeline-trace.md`
- **Spec 12:** `exploration/concept_explorer/docs/specs/12-computation-api.md`
- **Model:** `exploration/concept_explorer/models.py:306-317` — `ParameterMetadata`
- **Extractor:** `exploration/concept_explorer/extract_explorer_data.py:132-153` — `build_sensitivity_analysis()`
- **Costingfe validation:** `1costingfe/src/costingfe/validation.py:45-119` — `CostingInput`

## Research Findings

### What the frontend actually needs

The slider renderer (`concept_page.js:234-305`) accesses exactly five fields:

- `range` — slider min/max (required, no fallback)
- `baseline` — initial slider position (required)
- `display_name` — label text (required)
- `display_multiplier` — raw→display conversion (defaults to `1.0`)
- `display_unit` — unit suffix (defaults to `""`)

The server compute path (`server.py:534-582`) does not touch metadata at all. It takes raw `{param_name: float}` overrides and calls `model.forward()`.

### What data exists at extraction time

When `build_sensitivity_analysis()` runs (`extract_explorer_data.py:205`), we have:

- **`SensitivityAnalysis`** — every param name, its elasticity, its baseline value, and whether it's engineering or financial. This is everything the function just computed.
- **`result.params`** — the full 168-parameter dict from `model.forward()`. Superset of sensitivity params.

That's all three required fields: the name is the dict key, the baseline is `SensitivityEntry.baseline`, and the range is derivable from the baseline.

### Physical bounds from costingfe

`CostingInput` (`validation.py:45-119`) has Pydantic `Field` constraints on a handful of "customer" parameters:

| Parameter | Constraint |
|-----------|-----------|
| `availability` | `gt=0, le=1` |
| `lifetime_yr` | `gt=0` |
| `construction_time_yr` | `gt=0` |
| `interest_rate` | `gt=0` |
| `net_electric_mw` | `gt=0` |

Engineering parameters (`eta_th`, `mn`, `p_cryo`, etc.) have no `Field` constraints — they default to `None` and are filled from YAML templates. Their physical bounds aren't encoded in costingfe's validation layer.

### What the Pydantic model requires

`ParameterMetadata` (`models.py:306-317`) has five required fields with no defaults:

- `display_name: str`
- `category: ParameterCategory`
- `confidence: Confidence`
- `baseline: float`
- `range: tuple[float, float]`

## Core Concept

This is a **derivation function**, not a data registry. At extraction time, `build_sensitivity_analysis()` already iterates every parameter and knows its name, baseline, category (engineering vs financial), and elasticity. A single function takes that `SensitivityAnalysis` and produces a `dict[str, ParameterMetadata]` — one entry per sensitivity parameter.

The key insight: every field the slider needs is either already present in the sensitivity data (baseline, category) or trivially derivable from it (display name from the key, range from the baseline). There is no missing data source. The "adapter" between cost model and UI should have been built the same day the sensitivity computation was built — it's the same information, shaped differently.

The only design question worth answering is range derivation: given a baseline, what are physically reasonable slider bounds? The answer is `baseline ± 30%` with two clamps: a floor at zero (no negative physical quantities) and a ceiling at 1.0 for parameters that are fractions (efficiencies, availability). That covers 100% of the parameter space without a registry.

## Key Bets & Decisions

### Bet 1: No static registry

A mapping of 249 parameter names to display metadata is not worth building or maintaining. The extraction pipeline already knows everything it needs. A registry adds a synchronization problem (new params in costingfe require registry updates) for zero functional benefit.

**What we give up:** Some display names will be mediocre (`eta_th` → "Eta Th" instead of "Thermal Efficiency"). This is acceptable because (a) the sliders work regardless, (b) `model_metadata.yaml` exists as the override path for any param that deserves a curated name, and (c) the tornado chart already shows raw param names today with no complaints.

### Bet 2: Range derivation from baseline, not from costingfe introspection

We could try to introspect costingfe's `CostingInput` Field constraints to extract `gt`, `le`, etc. But only 5 of ~47 sensitivity parameters have Field constraints. The rest have `None` defaults with no bounds. Introspecting the validation layer would add a costingfe coupling for marginal gain on 5 params.

Instead: `baseline ± 30%`, clamp `[max(0, lo), hi]`, and additionally clamp to `[0, 1]` for known-fractional params. Simple, complete, no external dependency.

### Bet 3: Generate for sensitivity params only, not all 168 result.params

Sliders only make sense for parameters that have sensitivity data (the tornado chart shows their impact). Generating metadata for the other ~121 params in `result.params` would produce sliders for parameters with unknown LCOE impact. The frontend gates on `sensitivities ∩ parameter_metadata` — only params in both dicts get sliders.

## Architecture

### Data Flow

```
build_sensitivity_analysis(model, result)
    → SensitivityAnalysis                     # already exists

generate_parameter_metadata(sensitivities)
    → dict[str, ParameterMetadata]            # NEW — the one new function

load_parameter_metadata(concept_dir)
    → dict[str, ParameterMetadata]            # already exists (yaml overrides)

merge: {**generated, **yaml_overrides}
    → dict[str, ParameterMetadata]            # yaml wins on key collision

ConceptData(..., parameter_metadata=merged)
    → JSON → frontend → sliders render
```

The new function slots between the existing sensitivity computation and the existing yaml-override loader. No new files, no new abstractions, no new data sources.

### Integration Point

In `extract_costingfe()` (`extract_explorer_data.py:183-250`), between line 205 (sensitivity built) and line 239 (ConceptData constructed):

```python
sensitivities = build_sensitivity_analysis(model, effective_result)
generated_meta = generate_parameter_metadata(sensitivities)
merged_meta = {**generated_meta, **param_metadata}  # yaml overrides win
# ... later ...
concept = ConceptData(..., parameter_metadata=merged_meta, ...)
```

Three lines of glue. The function itself is the only new code.

## Required Invariants

1. **yaml overrides always win** — if `model_metadata.yaml` defines an entry for `eta_th`, it replaces the generated one entirely. The merge is a simple dict spread, not a field-level merge.
2. **Every sensitivity param gets metadata** — no param in `SensitivityAnalysis.engineering` or `.financial` should be absent from `parameter_metadata` after generation.
3. **Ranges never produce degenerate sliders** — `lo < hi` always. If baseline is 0 (edge case: should be impossible since `_build_lcoe_fn` filters `params[k] != 0`), produce a fallback range like `[0, 1]` rather than `[0, 0]`.
4. **No costingfe import in the extractor** — the function takes a `SensitivityAnalysis`, not a costingfe model. It works for standalone concepts too (if they ever get sensitivity data with baselines).

## Component Overview

### `generate_parameter_metadata(sensitivities: SensitivityAnalysis) -> dict[str, ParameterMetadata]`

Single new function in `extract_explorer_data.py`. Takes the sensitivity analysis that was just computed. Iterates engineering and financial entries. For each `(name, SensitivityEntry)` pair, produces a `ParameterMetadata` with:

- **`display_name`**: titlecase the snake_case key (`eta_th` → `"Eta Th"`, `thermal_efficiency` → `"Thermal Efficiency"`)
- **`baseline`**: from `SensitivityEntry.baseline`
- **`category`**: `ParameterCategory.UNCLASSIFIED` (engineering vs financial is known, but the `ParameterCategory` enum encodes a richer taxonomy — shared-baseline, key-innovation, etc. — that requires analyst judgment. Default to unclassified.)
- **`confidence`**: `Confidence.UNKNOWN`
- **`range`**: `(baseline * 0.7, baseline * 1.3)`, clamped to `[0, ∞)`, and additionally clamped to `[0, 1]` for params identified as fractional

### Fractional parameter identification

A parameter is treated as fractional (0-1 bounded) if its baseline is in `(0, 1]` AND its name matches known patterns: contains `eta`, `efficiency`, `availability`, `fraction`, `f_` prefix, or equals specific names like `burn_fraction`, `fuel_recovery`. This is a heuristic, not a registry — it errs on the side of not clamping (a non-fractional param with baseline 0.5 just gets `[0.35, 0.65]`, which is fine).

## Non-Goals

- **Curated display names**: The auto-generated names are functional. Polishing `eta_th` → "Thermal Efficiency" is a `model_metadata.yaml` concern, not an extraction concern.
- **Display multiplier/unit**: Showing "0.33" instead of "33%" is a UX refinement. The slider works without it. `model_metadata.yaml` can add these per-param.
- **Standalone concept sliders**: Standalone concepts can't recompute (no `model.forward()`). Generating metadata for them would populate tornado display names but not enable sliders. Out of scope.
- **Synonym normalization**: `availability` vs `plant_availability` are different params in different models. Each gets its own metadata. No normalization.
- **Comparison-view sliders**: Deferred per spec 12.

## Implementation Notes

- The function lives in `extract_explorer_data.py` alongside `build_sensitivity_analysis`. No new files.
- The fractional-detection heuristic should be a simple set/predicate, not a class or configuration object.
- The merge point is in `extract_costingfe()` — the standalone extraction path (`extract_standalone()`) does not call this function (standalone concepts don't support recompute).
- After implementing, re-extract all concepts (`uv run python exploration/concept_explorer/extract_explorer_data.py`) and verify sliders appear in the browser.

## Potential Risks

**Risk: Some baselines are 0.** Costingfe's `_build_lcoe_fn` filters `params[k] != 0`, so zero-baseline params shouldn't appear in sensitivities. But if they do, `0 * 0.7 = 0` and `0 * 1.3 = 0` gives a degenerate range. Mitigation: detect and use a fallback range `(0, 1)`.

**Risk: Fractional heuristic miscategorizes a param.** A non-fractional param with baseline 0.8 might get clamped to `[0, 1]` instead of `[0.56, 1.04]`. The practical impact is a slightly narrower slider range. Low severity.

**Risk: ParameterMetadata Pydantic validation rejects a generated entry.** Unlikely since we control all field values, but worth having a try/except with a warning (same pattern as `load_parameter_metadata`).

## Integration Strategy

This is a pure addition to the extraction pipeline. No frontend, backend, CSS, or test changes. The existing slider rendering code, compute endpoint, and test suite remain untouched.

After extraction, the data JSON files gain populated `parameter_metadata` dicts. The frontend picks them up on next page load. The slider section un-hides itself.

## Validation Approach

1. **Unit test**: `generate_parameter_metadata()` given a known `SensitivityAnalysis` → verify output has correct display names, ranges within expected bounds, all keys present
2. **Integration test**: Extract one costingfe concept → verify `parameter_metadata` is non-empty in the output JSON
3. **Manual verification**: Load concept explorer, navigate to a costingfe concept profile page, confirm sliders render and `POST /api/compute` returns updated values on drag
4. **Existing tests**: `pytest exploration/concept_explorer/tests/` must still pass (no regressions)

## Next-Stage Handoff

**Fixed (do not revisit in plan):**
- One new function, `generate_parameter_metadata()`, in `extract_explorer_data.py`
- Merge with yaml overrides via dict spread in `extract_costingfe()`
- Range strategy: `baseline ± 30%`, clamp to `[0, ∞)`, fractional params clamp to `[0, 1]`
- Default category: `unclassified`. Default confidence: `unknown`.

**Open (plan should decide):**
- Exact list of names/patterns for the fractional-param heuristic
- Whether to also wire into `extract_standalone()` for tornado display-name enrichment (not for sliders — standalone can't recompute)

**De-risk first:**
- Verify that re-extraction actually works end-to-end (costingfe import, model.forward(), sensitivity, metadata generation, JSON write, frontend render) before writing tests

---

Next Step: After approval → `/_my_plan` or `/_my_implement`
