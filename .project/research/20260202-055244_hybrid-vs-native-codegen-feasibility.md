---
date: 2026-02-02T05:52:44Z
researcher: Claude
topic: "Hybrid pipeline (generate_costs.py wrapper) vs native codegen enhancement for nested CalcUsages"
tags: [research, codegen, pipeline, feasibility]
status: complete
last_updated: 2026-02-02
---

# Research: Hybrid Pipeline vs Native Codegen Enhancement

**Date**: 2026-02-02 05:52 UTC
**Researcher**: Claude
**Research Type**: Architecture / Feasibility

## Research Question

Is it easier to (A) wrap `generate_costs.py` as a TEAx module in a two-step codegen process, or (B) enhance sysml-codegen to discover nested CalcUsages natively? What's the honest effort comparison?

## Summary

- **Path A (hybrid wrapper) is significantly easier**: ~150-200 lines of new code, uses proven logic, LOW risk
- **Path B (native codegen) is substantially harder than it looks**: the "discovery" part is small, but per-PartUsage instantiation, `:>>` binding resolution, multiplicity, assembly aggregation, and allocation models are each non-trivial problems. Estimated 500-800 lines across 4-5 files in sysml-codegen, MEDIUM-HIGH risk.
- **Path A proves the pipeline end-to-end**, giving Path B a working reference to test against
- **Recommendation**: Do Path A first, then Path B incrementally

## Detailed Findings

### Path A: Wrap generate_costs.py as a TEAx Module

#### What it involves

1. **Create a TEAx ModuleBase wrapper** around `compute_costs()`:
   - Input: model path (or design parameters)
   - Output: `total_capex` + cost breakdown as Pydantic model
   - The wrapper calls `compute_costs()` internally
   - ~50-100 lines

2. **Create Pydantic schemas** for input/output types:
   - Input schema: model path or pre-resolved design params
   - Output schema: `ComponentCostOutput` with total_capex and per-subsystem breakdown
   - ~30 lines

3. **Wire into pipeline YAML**:
   - Cost evaluator module runs first (or as entry point data provider)
   - System-level modules (from codegen) consume its `total_capex` output
   - ~20 lines of YAML

4. **Register module** and execute pipeline:
   - Add to registry alongside codegen-generated modules
   - ~10 lines

#### TEAx integration surface (from research)

- EntryPoints are **static JSON only** — cannot run Python (`pipeline_schema.py:222-230`)
- Modules can run **arbitrary Python** via `ModuleBase.run()` — this is the integration point
- `compute_costs()` returns `dict[str, dict[str, float]]` — wraps cleanly in `RootModel[dict]`
- Battery-tea-demo shows the exact pattern: `CostCalculatorModule` does computation in `run()`
- Chain spike shows codegen output pattern: generated module calls `handwritten/*_impl.py`

#### Effort estimate

| Work Item | Lines | Risk |
|-----------|-------|------|
| ModuleBase wrapper | ~80 | LOW — straightforward pattern from battery-tea-demo |
| Pydantic schemas | ~30 | LOW — simple data models |
| Pipeline YAML wiring | ~20 | LOW — follows existing patterns |
| Registry + execution script | ~30 | LOW — proven in chain spike |
| Integration test | ~50 | LOW — compare against known-good values |
| **Total** | **~210** | **LOW** |

#### What it proves

- `generate_costs.py` output flows correctly through TEAx as a module
- Codegen-generated system-level modules consume computed costs correctly
- Full pipeline: SysML → (generate_costs.py + codegen) → TEAx → LCOE
- The hybrid approach actually works as an integrated pipeline

#### What it doesn't prove

- That codegen can handle nested CalcUsages natively
- That the workaround scales beyond solar+battery (each new model needs its own generate_costs.py)

---

### Path B: Enhance sysml-codegen Natively

#### The discovery problem (SMALL)

`usage_extractor.py:155` uses `SysideAdapter.elements_of_type(model, "CalculationUsage")` for a flat search. The `_get_parent_part_path()` function (line 407-421) only looks for `PartUsage` parents, not `PartDefinition`.

Whether syside's `model.elements(CalculationUsage)` actually returns CalcUsages nested inside PartDefinitions is **empirically unknown**. If it does, the discovery fix is ~1 line. If it doesn't, explicit PartDef traversal is needed (~20-30 lines).

**This is the easy part.**

#### The hard parts (LARGE)

**Problem 1: Per-PartUsage Instantiation**

There is ONE `cost_model` CalcUsage inside the `'PV Module'` PartDefinition. But there are multiple PartUsages of `'PV Module'` across the design (e.g., `solar_array.pv_module[20]`). Codegen currently creates one `CalcUsageData` per CalcUsage element. For nested calcs, it needs to create one per PartUsage that references the containing PartDef, with different bindings for each.

This requires:
- Walking the PartUsage hierarchy (the design tree)
- For each PartUsage, checking if its PartDef contains CalcUsages
- Creating synthetic `CalcUsageData` with unique qualified names (`solar_array__pv_module__cost_model`)
- This logic does not exist in codegen today

**Estimated**: ~100-150 lines in `usage_extractor.py`, new function

**Problem 2: Binding Resolution Through `:>>`**

Current `dependency_backtracker.py` resolves bindings between CalcUsages and design attributes. It does NOT handle the `:>>` chain:

```
design.sysml:  :>> pv_module.wattage = 400.0
                    ↓
library.sysml: attribute wattage : Real     (in 'PV Module' PartDef)
                    ↓
library.sysml: calc cost_model : PVModuleCostCalc {
                   in wattage = wattage      (calc input binds to part attribute)
               }
```

This is a 3-hop chain: design `:>>` → part attribute → calc input. Nothing in `dependency_backtracker.py` handles this. The binding types (`BindingType.CHAIN`, `REFERENCE`, `LITERAL`) don't include "parent part attribute resolved via design redefinition."

`generate_costs.py` handles this with a 3-priority resolution system (`_resolve_bindings`, lines 739-808): design bindings > usage bindings > calc def defaults. This logic (~70 lines) would need to be replicated in `dependency_backtracker.py`.

**Estimated**: ~100-150 lines in `dependency_backtracker.py`, new resolution pathway

**Problem 3: Multiplicity**

`pv_module[20]` means 20 instances, each with the same unit cost. The generated TEAx module needs to multiply unit costs by quantity. Codegen currently has no concept of multiplicity — it generates one module per CalcUsage, period.

Options:
- Generate a multiplicity-aware module that outputs `total_cost = unit_cost * quantity`
- Generate a wrapper module that does the multiplication
- Handle in pipeline YAML somehow

**Estimated**: ~50-80 lines across module generation templates

**Problem 4: Assembly Aggregation**

Assembly PartDefs (Solar Array, Battery System, Site Infrastructure) compute costs as `sum(child.capital_cost) + ...`. These are SysML expressions, not CalcUsages. Codegen generates modules from CalcUsages — there's no mechanism to generate a "rollup" module from a SysML `sum()` expression on part attributes.

Options:
- Generate explicit rollup modules from assembly PartDef cost expressions
- Generate a generic aggregation module
- Leave aggregation to pipeline YAML wiring

**Estimated**: ~100-150 lines, possibly new generation pathway

**Problem 5: Allocation Models**

3 assembly PartDefs have optional `allocation_model` CalcUsages with hardcoded literal bindings. These are simpler than component costs (no design `:>>` chain), but they need to be discovered, instantiated, and their outputs wired into the assembly rollup.

**Estimated**: ~50 lines, handled as part of Problem 1 if generalized

#### Files to change

| File | Changes | Estimated Lines |
|------|---------|----------------|
| `extraction/usage_extractor.py` | Discovery + per-PartUsage instantiation | +150-200 |
| `analysis/dependency_backtracker.py` | `:>>` binding resolution | +100-150 |
| `generation/modules.py` or templates | Multiplicity-aware module generation | +50-80 |
| `resolution/graph_builder.py` | Assembly rollup nodes | +50-100 |
| `generation/pipeline.py` | Rollup module wiring in YAML | +30-50 |
| Tests | New fixtures + test cases | +100-150 |
| **Total** | | **+500-730** |

#### Risk assessment

| Risk | Likelihood | Impact |
|------|-----------|--------|
| syside doesn't return nested CalcUsages at all | MEDIUM | HIGH — need explicit traversal |
| Per-PartUsage instantiation creates duplicate qualified names | MEDIUM | MEDIUM — naming scheme design |
| `:>>` resolution has edge cases not in solar model | HIGH | MEDIUM — fragile to new patterns |
| Assembly rollup breaks existing pipeline generation | MEDIUM | HIGH — regression risk |
| Multiplicity handling interacts badly with existing module generation | LOW | MEDIUM |

**Overall risk: MEDIUM-HIGH**

---

### Comparison

| Dimension | Path A (Hybrid Wrapper) | Path B (Native Codegen) |
|-----------|------------------------|------------------------|
| New code | ~210 lines | ~500-730 lines |
| Files changed | 3-4 new files (this repo) | 5-6 files (sysml-codegen repo) |
| Uses proven code | YES (compute_costs()) | NO (all new logic) |
| Risk | LOW | MEDIUM-HIGH |
| Proves E2E pipeline | YES | YES |
| Eliminates workaround | NO | YES |
| Scales to new models | NO (needs per-model generate_costs.py) | YES |
| Testable incrementally | YES (known-good reference) | HARDER (no reference until Path A exists) |
| Unblocks fusion modeling | YES (with workaround) | YES (natively) |

---

## Architecture Insights

### generate_costs.py is more generic than it looks

Analysis shows ~67% of generate_costs.py (1,260 LOC) is generic:
- Expression evaluator, topological sort, binding resolution, cost aggregation
- Model-specific: just `ROOT_PART_NAME` and subsystem names
- Coffee maker and solar battery share identical core logic
- Could be extracted into a reusable `cost_evaluation_engine` library

This means Path A's "each model needs its own generate_costs.py" is overstated. A generic library with model-specific configuration (~20 lines) is viable.

### TEAx modules can wrap anything

TEAx `ModuleBase.run()` executes arbitrary Python. The pattern from battery-tea-demo and chain spike is clear:
- Module wraps computation logic
- Input/output types are Pydantic models
- Registry handles discovery
- Pipeline YAML handles wiring

### The real problem in codegen is not discovery

The codegen agent's analysis suggests a 1-line fix. That's only the discovery part. The actual hard problems are:
1. Per-PartUsage instantiation (one CalcUsage per PartDef → many instances)
2. 3-hop binding resolution (design `:>>` → part attr → calc input)
3. Multiplicity (quantity multiplication)
4. Assembly aggregation (sum of children)
5. Allocation models

These are 5 distinct problems, each requiring new logic that doesn't exist in codegen today. `generate_costs.py` solves all 5 in its ~1,260 LOC generic core.

---

## Recommendations

### Recommended path: A then B

1. **Do Path A** (Item 5, revised): Create a TEAx module wrapping `compute_costs()`, wire into pipeline with codegen-generated system-level modules, verify LCOE end-to-end. This proves the pipeline works and creates a testable reference.

2. **Then do Path B** (Item 6): Enhance codegen incrementally, testing each change against Path A's known-good output. Tackle in order:
   - Discovery + per-PartUsage instantiation
   - Binding resolution
   - Multiplicity
   - Assembly aggregation
   - Allocation models

3. **Consider extracting generic cost evaluation library** from generate_costs.py as an intermediate step. This makes Path A scale to new models without per-model scripts.

### Why not skip Path A?

Path B has no working reference to test against. If codegen produces wrong LCOE, you won't know if it's discovery, binding resolution, multiplicity, aggregation, or pipeline wiring. Path A gives you the correct answer to test against at each step.

### Retire Item 4?

Yes. Item 4 (run codegen on solar+battery, fill in 5 handwritten implementations) is still useful but can be folded into revised Item 5. The codegen run is a prerequisite for the pipeline, not a standalone deliverable.

## Open Questions

1. **Does `model.elements(CalculationUsage)` return CalcUsages inside PartDefinitions?** — 5-minute empirical test would answer this and inform Path B scope
2. **Should generate_costs.py be extracted into a library before wrapping?** — Depends on whether fusion models will also use this pattern short-term
3. **How does the cost evaluator module get the SysML model path at runtime?** — Could be entry point parameter, environment variable, or pipeline configuration

## Code References

- `generate_costs.py` public API: `compute_costs()` at solar_battery/generate_costs.py:1308-1381
- TEAx ModuleBase: `/home/reid/1cfe/teax/packages/teax-simkit/simkit/core/base.py`
- TEAx pipeline executor: `simkit/core/pipeline_executor.py:270-310` (entry point loading)
- Codegen usage extraction: `sysml-codegen/src/sysml_codegen/extraction/usage_extractor.py:133-168`
- Codegen binding resolution: `sysml-codegen/src/sysml_codegen/analysis/dependency_backtracker.py:626-703`
- Parent path extraction (the "1-line fix"): `usage_extractor.py:407-421`
- Battery-tea-demo module pattern: `battery-tea-demo/battery_tea/modules/cost_calc/module.py`
- Chain spike generated module: `generated/codegen_chain_spike/modules/chainspikelibrary/costcalc.py`
