---
date: 2026-02-10T01:30:00-06:00
researcher: Claude
topic: "Attribute Expression E2E Validation Plan — Gap Analysis and Test Strategy"
tags: [research, attr-expr, codegen, validation, e2e, teax, formula, computed-attributes]
status: complete
last_updated: 2026-02-10
---

# Research: Attribute Expression E2E Validation Plan

**Date**: 2026-02-10T01:30:00-06:00
**Researcher**: Claude
**Research Type**: Integration / Gap Analysis / Validation Planning

## Research Question

After completing major changes to sysml-codegen (ATTR-EXPR Phase 2: in-line attribute expression compilation) and agentic-mbse (FORMULA validation exemption):

1. What gaps remain for effectively using these features in fusion-tea?
2. What new models should exercise all the new patterns?
3. What does a thorough e2e codegen + TEAx execution validation plan look like?

## Summary

- **Five blocking gaps remain** for full CostedComponent cost pipeline generation, all in Phase 3 (not yet started): CalcUsage-in-PartDef template instantiation, `:>>` redefinition chain resolution, `sum()` function calls, multiplicity `[count]`, and assembly cost aggregation expressions.
- **Three capabilities are NEW and ready for validation**: FORMULA computed attributes (synthetic modules), CalcDef auto-implementation (Phase 1, 15/15 solar_battery), and FORMULA→CalcUsage wiring.
- **The existing solar_battery pipeline is a hybrid** — a hand-crafted `ComponentCostEvaluator` wraps `generate_costs.py` for the 9 leaf-part cost calculations because codegen can't yet handle CalcUsage-in-PartDef. Only the 5 system-level CalcUsages are codegen-generated.
- **A new flat test model** can exercise all new patterns without triggering the Phase 3 gaps. This is the recommended validation target.
- **E2E validation should run in 4 phases**: codegen regeneration on solar_battery, new flat model codegen, TEAx pipeline execution, and numerical verification.

---

## Detailed Findings

### 1. What Changed (Three Codebases)

#### sysml-codegen — ATTR-EXPR Phase 2 (Complete)

| Change | Impact | Ref |
|--------|--------|-----|
| `ComputedAttributeData` extraction + 5-way classification | FORMULA attributes on PartDef/PartUsage detected and classified | `extraction/computed_attribute_extractor.py` |
| Step 4.5 in `build_pipeline_context()` | FORMULA attributes removed from design_attributes before ParameterGroupDeriver; prevents false entry points | `generation/initialization.py:140-196` |
| Backtracker computed attribute awareness | CalcUsage bindings to FORMULA attributes resolve as MODULE_OUTPUT from synthetic module | `analysis/dependency_backtracker.py:395-413` |
| Graph builder FORMULA module generation | Synthetic `PipelineModule` created for each FORMULA attr, with auto-implemented code | `resolution/graph_builder.py:623-740` |
| Unified topological sort (Kahn's algorithm) | CalcUsage + computed attr modules sorted together for correct execution order | `resolution/graph_builder.py:743-813` |
| E2E test suite: 285 tests, 0 failures | Covers attr_expr_probe (9 FORMULA patterns), solar_battery (p_net_kw), chain_spike, CATF MFE | `tests/integration/test_computed_attributes_e2e.py` |

#### sysml-codegen — Phase 1 EXPR-CODEGEN (Complete, Prerequisite)

| Change | Impact | Ref |
|--------|--------|-----|
| Expression compiler: `build_expression_ast()` + `compile_expression()` | CalcDef outputs with formulas auto-compile to Python | `extraction/expression_compiler.py` |
| Auto-implementation template | Generated `_impl.py` files with `AUTO_IMPLEMENTED = True` | `auto_implementation.py.jinja2` |
| CalcDef compilability classification | 15/15 solar_battery, 19/21 CATF CalcDefs auto-implemented | Step 6.5 in pipeline |

#### agentic-mbse — EPIC-COMPATTR-001 (Complete)

| Change | Impact | Ref |
|--------|--------|-----|
| `_is_formula_pattern()` in V2 validation | FORMULA expressions (`attribute area = length * width`) no longer flagged as V2 violations | `validation/adr002.py:393-459` |
| L8 codegen readiness exemption | FORMULA and EXPOSE patterns exempt from extractability check | `validation/level8_codegen.py:377-405` |
| Pattern docs updated | `adr002-calculations.md` includes FORMULA row, decision flow, amendment; `expose-pattern.md` distinguishes FORMULA from EXPOSE | `docs/patterns/` |
| Agent commands updated | `/implement-model` and `/design-model` include FORMULA guidance | `claude/commands/` |
| 7 new FORMULA tests, 886 total, 0 regressions | Simple FORMULA, chain, literal+FORMULA, EXPOSE_COMPUTED still fails | `tests/test_sysml/test_adr002.py:514-561` |

---

### 2. Gap Analysis: What's NOT Yet Supported

#### Gap A: CalcUsage-in-PartDef Template Instantiation (BLOCKING — Phase 3)

**Pattern**: The "nested cost model" pattern used by ALL 9 leaf parts in solar_battery:

```sysml
part def 'PV Module' :> 'Costed Component' {
    attribute wattage : Real;
    calc cost_model : PVModuleCostCalc {
        in wattage = wattage;      // Binds to parent's attribute
    }
    :>> capital_cost = cost_model.total_cost;  // EXPOSE_PURE
}

// In design.sysml:
part solar_battery_plant : 'Solar Battery Plant' {
    part redefines solar_array {
        :>> pv_module.wattage = 400.0;  // Redefinition chain
    }
}
```

**Why it doesn't work**: `cost_model` is a CalcUsage owned by PartDefinition `'PV Module'`, not by a PartUsage. The extractor finds it but generates only one template module — it does NOT instantiate per-PartUsage (e.g., creating `solar_array__pv_module__cost_model` with wattage=400.0 resolved through the redefinition chain).

**Research doc**: `sysml-codegen/.project/research/20260109-205122_cost-modeling-codegen-changes.md` describes this gap in detail with a ~740-line implementation plan.

**Status**: Explicitly deferred to Phase 3 in the ATTR-EXPR epic. No implementation started.

#### Gap B: `:>>` Redefinition Chain Resolution (BLOCKING — Phase 3)

**Pattern**: Design file binds values through nested part redefinitions:

```sysml
:>> pv_module.wattage = 400.0;       // Sets leaf part parameter
:>> inverter.power_rating = 2000.0;   // Through assembly→leaf chain
```

**Why it doesn't work**: The backtracker and extraction phases don't resolve binding values through `:>>` redefinition chains on PartUsages that instantiate PartDefinitions. When `cost_model` in `'PV Module'` binds `in wattage = wattage`, and the design sets `:>> pv_module.wattage = 400.0`, codegen cannot trace `wattage` → 400.0.

**Dependency**: Required by Gap A (template instantiation needs resolved bindings).

#### Gap C: `sum()` / NumericalFunctions (NOT COMPILABLE)

**Pattern**: Assembly cost rollup uses `sum()` for arrayed parts:

```sysml
:>> capital_cost = sum(pv_module.capital_cost) + inverter.capital_cost;
```

**Why it doesn't work**: The expression compiler only handles arithmetic operators (`+`, `-`, `*`, `/`, `**`). `InvocationExpression` (function calls like `sum()`) returns an UNSUPPORTED node. This would classify as UNRESOLVABLE.

**Frequency**: Used in 3 of 4 assembly-level parts (Solar Array, Battery System, Site Infrastructure doesn't use it for singletons, but 'Solar Battery Plant' top-level does).

#### Gap D: Multiplicity `[count]` (NOT HANDLED)

**Pattern**: Parameterized arrays of parts:

```sysml
attribute module_count : Integer default := 20;
part pv_module : 'PV Module' [module_count];
```

**Why it doesn't work**: The codegen pipeline treats parts as singletons. Generating per-instance modules for arrayed parts with parameterized count requires runtime array expansion, not static compilation.

**Dependency**: Required by Gap C (`sum()` iterates over arrayed part instances).

#### Gap E: Assembly Cost Aggregation Expressions (MIXED PATTERNS)

**Pattern**: Assembly redefinitions combine cross-part references, function calls, and arithmetic:

```sysml
:>> capital_cost =
    sum(pv_module.capital_cost) +
    sum(inverter.capital_cost) +
    array_bos.capital_cost +
    misc_hardware_cost;
```

**Why it doesn't work**: This expression contains:
- `sum()` function calls (Gap C)
- Cross-part references (`pv_module.capital_cost` — FeatureChainExpression through child parts)
- Sibling references (`misc_hardware_cost`)
- Mix of all three → would be classified UNRESOLVABLE

**Resolution**: This requires all of Gaps A-D to be resolved first.

### 3. What DOES Work — Currently Validatable Patterns

| Pattern | Example | Pipeline Treatment | Tested? |
|---------|---------|-------------------|---------|
| **FORMULA** (sibling arithmetic) | `p_net_kw = p_net_mw * 1000.0` | Synthetic module + auto-impl | Yes (sysml-codegen E2E) |
| **FORMULA chain** | `cost = area * rate` (area is computed) | Synthetic module, topo-sorted after dependency | Yes (attr_expr_probe) |
| **FORMULA fan-in** | `cost_density = cost / volume` | Module with 2 upstream module inputs | Yes (attr_expr_probe) |
| **CalcDef auto-impl** | `out total_cost = material_cost + fab_cost + install_cost` | Auto-implemented `_impl.py` | Yes (Phase 1, 15/15 solar_battery) |
| **CalcDef multi-output** | AnnualizedFinancialCalc (CRF + annualized_capital_cost) | Multi-output module | Yes (solar_battery) |
| **CalcDef `**` exponent** | `(1.0 + discount_rate) ** plant_lifetime` | Compiles to Python `**` | Yes (AnnualizedFinancialCalc) |
| **FORMULA → CalcUsage wiring** | `annualized_om { in p_net_kw = p_net_kw }` where p_net_kw is FORMULA | Binding resolves as MODULE_OUTPUT | Yes (solar_battery p_net_kw) |
| **EXPOSE_PURE** (alias) | `scale_result = scale_calc.result` | Channel alias, no module | Yes (attr_expr_probe) |
| **V2 validation exemption** | `attribute area = length * width` passes agentic-mbse validate | No V2 violation | Yes (7 agentic-mbse tests) |
| **L8 codegen exemption** | FORMULA/EXPOSE skip extractability check | No false L8 warnings | Yes (agentic-mbse tests) |

### 4. Current Pipeline State — The Hybrid Workaround

The existing `generated/solar_battery/` uses a **hybrid pipeline** (`pipelines/pipeline.yaml`):

```
[Entry Point] → [ComponentCostEvaluator] → [5 system-level modules] → [Exit Point]
       ↓                    ↓                         ↓
  pipeline_config    Wraps generate_costs.py     Codegen-generated
                     Handles ALL 9 leaf-part     (energy_production,
                     cost calcs + rollups        annualized_om/fuel/financial,
                     Returns total_capex + params lcoe)
```

**Why hybrid**: The 9 leaf-part CalcUsages are inside PartDefinitions (Gap A), and the assembly rollup uses `sum()` (Gap C) and cross-part references (Gap E). The `ComponentCostEvaluator` manually evaluates the SysML model to compute these costs, then passes results to the codegen-generated system-level modules.

**What changes with ATTR-EXPR**: When codegen regenerates:
1. `p_net_kw` FORMULA attribute will generate a new synthetic module
2. `annualized_om`'s binding to `p_net_kw` will resolve as MODULE_OUTPUT (not from ComponentCostEvaluator)
3. All 15 CalcDef `_impl.py` files will have `AUTO_IMPLEMENTED = True` (Phase 1)
4. But the hybrid structure remains necessary for component-level costs

---

### 5. Existing Solar Battery Codegen — What We Already Have

The `generated/solar_battery/` was generated from a prior codegen run (2026-02-02). Contents:

| Artifact | Contents | Status |
|----------|----------|--------|
| `modules/solarbatterylibrary/` | 5 system-level CalcUsage module wrappers | Generated, not auto-impl'd |
| `modules/component_cost_evaluator.py` | Hand-crafted wrapper for generate_costs.py | Manual |
| `handwritten/solarbatterylibrary/` | 15 `_impl.py` stubs (all `raise NotImplementedError`) | Need Phase 1 auto-impl |
| `schemas/` | Pydantic parameter schemas | Generated |
| `pipelines/pipeline.yaml` | Hybrid pipeline YAML | Hand-crafted |
| `IMPLEMENTATION_BACKLOG.md` | 15 functions to implement (all `[ ]`) | Pre-Phase 1 |
| `run_pipeline.py` | TEAx execution entry point | Working |
| `verify_pipeline.py` | Output verification script | Working |
| `outputs/` | Prior execution results | Exists |

**Key observation**: This was generated BEFORE Phase 1 (auto-impl) and Phase 2 (FORMULA). A regeneration will:
- Auto-implement all 15 CalcDef `_impl.py` files
- Add `solar_battery_plant__p_net_kw` synthetic module
- Update pipeline YAML with computed attribute module
- Update IMPLEMENTATION_BACKLOG.md to show 0 functions to implement

---

## Validation Plan

### Phase A: Regenerate Solar Battery with Latest Codegen

**Goal**: Verify that the existing solar_battery model produces correct, improved output with Phase 1 + Phase 2 features.

**Steps**:

1. **Run codegen** with `--smart-regen --preserve-handwritten`:
   ```bash
   cd ~/1cfe/fusion-tea
   uv run sysml-codegen generate \
     --models models/tests/solar_battery/ \
     --output generated/solar_battery \
     --package-name solar_battery \
     --smart-regen --preserve-handwritten --verbose
   ```

2. **Verify auto-implementation** (Phase 1):
   - All 15 CalcDef `_impl.py` files should have `AUTO_IMPLEMENTED = True`
   - Check for correct Python expressions in each
   - Verify `IMPLEMENTATION_BACKLOG.md` shows "0 functions to implement"

3. **Verify FORMULA module** (Phase 2):
   - `solar_battery_plant__p_net_kw` synthetic module appears in pipeline YAML
   - Module marked with `# source: computed_attribute`
   - Auto-implemented with `(inputs.p_net_mw * 1000.0)`

4. **Verify wiring** (Phase 2):
   - `annualized_om.p_net_kw` input wired to `solar_battery_plant__p_net_kw` module output
   - NOT wired to ComponentCostEvaluator output or entry point

5. **Expected results**: Pipeline YAML should have 6 modules (5 system-level + 1 FORMULA synthetic) plus ComponentCostEvaluator for the component costs. All 15+1 = 16 impl files auto-implemented.

**Risk**: The hybrid `pipeline.yaml` was hand-crafted. Smart-regen may or may not update it. We may need to update it manually to wire the new synthetic module.

---

### Phase B: New Test Model — Flat CostedComponent Exercise

**Goal**: Create a new model that exercises ALL new patterns without triggering Phase 3 gaps. This validates FORMULA + CalcDef auto-impl + wiring in a clean environment.

**Model Design**: A flat design (no nesting, no PartDef CalcUsages) with:
- Multiple FORMULA computed attributes (simple, chain, fan-in)
- Multiple CalcUsage bindings to FORMULA attributes
- Multi-output CalcDefs
- `**` exponentiation
- EXPOSE_PURE patterns
- A simplified "costed component" calculation

**File: `models/tests/e2e_attr_expr/library.sysml`**

```sysml
package E2EAttrExprLibrary {
    private import ScalarValues::Real;

    // Simple cost calculation (2 inputs, 5 outputs)
    calc def ComponentCostCalc {
        in attribute quantity : Real;
        in attribute unit_cost : Real;
        in attribute fab_factor : Real default := 0.45;
        in attribute install_factor : Real default := 0.30;

        out attribute material_cost : Real = quantity * unit_cost;
        out attribute fab_cost : Real = material_cost * fab_factor;
        out attribute install_cost : Real = material_cost * install_factor;
        out attribute total_cost : Real = material_cost + fab_cost + install_cost;
        out attribute idiot_index : Real = total_cost / material_cost;
    }

    // Financial calculation with exponentiation
    calc def AnnualizedCostCalc {
        in attribute total_capex : Real;
        in attribute discount_rate : Real;
        in attribute lifetime : Real;

        out attribute crf : Real =
            discount_rate * (1.0 + discount_rate) ** lifetime
            / ((1.0 + discount_rate) ** lifetime - 1.0);
        out attribute annualized_cost : Real = crf * total_capex;
    }

    // Energy calculation (simple)
    calc def EnergyCalc {
        in attribute power_mw : Real;
        in attribute availability : Real;

        out attribute annual_energy_mwh : Real = 8760.0 * power_mw * availability;
    }

    // LCOE (consumes upstream outputs)
    calc def SimpleLCOECalc {
        in attribute annualized_capital : Real;
        in attribute annual_om : Real;
        in attribute annual_energy : Real;

        out attribute lcoe : Real = (annualized_capital + annual_om) / annual_energy;
    }
}
```

**File: `models/tests/e2e_attr_expr/design.sysml`**

```sysml
package E2EAttrExprDesign {
    private import ScalarValues::Real;
    private import E2EAttrExprLibrary::*;

    part e2e_plant {
        // Literal parameters (entry points)
        attribute quantity : Real = 100.0;
        attribute unit_cost : Real = 50.0;
        attribute discount_rate : Real = 0.05;
        attribute lifetime : Real = 25.0;
        attribute availability : Real = 0.90;
        attribute om_rate : Real = 20.0;

        // FORMULA: unit conversion (simple)
        attribute power_mw : Real = quantity * unit_cost / 1000000.0;

        // FORMULA: chain (depends on power_mw FORMULA)
        attribute power_kw : Real = power_mw * 1000.0;

        // FORMULA: O&M cost from FORMULA chain
        attribute annual_om : Real = om_rate * power_kw;

        // FORMULA: area (for fan-in testing)
        attribute length : Real = 10.0;
        attribute width : Real = 5.0;
        attribute height : Real = 3.0;
        attribute area : Real = length * width;
        attribute volume : Real = length * width * height;
        attribute cost_per_sqm : Real = 12.0;

        // FORMULA: fan-in (depends on area FORMULA + literal)
        attribute surface_cost : Real = area * cost_per_sqm;

        // CalcUsage: binds to literal params
        calc component_cost : ComponentCostCalc {
            in quantity = quantity;
            in unit_cost = unit_cost;
        }

        // EXPOSE_PURE: surface calc output
        attribute total_capex : Real = component_cost.total_cost;

        // CalcUsage: financial calc with exponentiation
        calc financial : AnnualizedCostCalc {
            in total_capex = total_capex;
            in discount_rate = discount_rate;
            in lifetime = lifetime;
        }

        // CalcUsage: energy calc, binds to FORMULA computed attr
        calc energy : EnergyCalc {
            in power_mw = power_mw;         // Binds to FORMULA!
            in availability = availability;
        }

        // CalcUsage: LCOE, binds to mix of upstream outputs + FORMULA
        calc lcoe : SimpleLCOECalc {
            in annualized_capital = financial.annualized_cost;
            in annual_om = annual_om;         // Binds to FORMULA!
            in annual_energy = energy.annual_energy_mwh;
        }
    }
}
```

**Ground Truth Values** (hand-calculated):

| Attribute/Output | Formula | Value |
|-----------------|---------|-------|
| `power_mw` | 100.0 * 50.0 / 1000000.0 | 0.005 |
| `power_kw` | 0.005 * 1000.0 | 5.0 |
| `annual_om` | 20.0 * 5.0 | 100.0 |
| `area` | 10.0 * 5.0 | 50.0 |
| `volume` | 10.0 * 5.0 * 3.0 | 150.0 |
| `surface_cost` | 50.0 * 12.0 | 600.0 |
| `component_cost.material_cost` | 100.0 * 50.0 | 5000.0 |
| `component_cost.fab_cost` | 5000.0 * 0.45 | 2250.0 |
| `component_cost.install_cost` | 5000.0 * 0.30 | 1500.0 |
| `component_cost.total_cost` | 5000 + 2250 + 1500 | 8750.0 |
| `component_cost.idiot_index` | 8750.0 / 5000.0 | 1.75 |
| `total_capex` (EXPOSE) | = component_cost.total_cost | 8750.0 |
| `financial.crf` | 0.05*(1.05^25)/((1.05^25)-1) | ~0.07095 |
| `financial.annualized_cost` | ~0.07095 * 8750.0 | ~620.84 |
| `energy.annual_energy_mwh` | 8760.0 * 0.005 * 0.90 | 39.42 |
| `lcoe.lcoe` | (~620.84 + 100.0) / 39.42 | ~18.27 |

**Patterns Exercised**:

| # | Pattern | SysML | Expected Treatment |
|---|---------|-------|--------------------|
| 1 | Simple FORMULA | `power_mw = quantity * unit_cost / 1000000.0` | Synthetic module, auto-impl |
| 2 | Chain FORMULA | `power_kw = power_mw * 1000.0` | Synthetic module, topo-sorted after #1 |
| 3 | 2-hop chain FORMULA | `annual_om = om_rate * power_kw` | Synthetic module, topo-sorted after #2 |
| 4 | Simple FORMULA (binary) | `area = length * width` | Synthetic module |
| 5 | 3-term FORMULA | `volume = length * width * height` | Synthetic module |
| 6 | Fan-in FORMULA | `surface_cost = area * cost_per_sqm` | Inputs from FORMULA #4 + literal |
| 7 | CalcDef auto-impl (5 outputs) | ComponentCostCalc | 5 output expressions auto-compiled |
| 8 | CalcDef with `**` | AnnualizedCostCalc CRF formula | Exponentiation compiled to Python `**` |
| 9 | EXPOSE_PURE | `total_capex = component_cost.total_cost` | Channel alias, no module |
| 10 | FORMULA → CalcUsage wiring | `energy { in power_mw = power_mw }` | Binding resolves as MODULE_OUTPUT |
| 11 | FORMULA → CalcUsage (2-hop) | `lcoe { in annual_om = annual_om }` | MODULE_OUTPUT from 3-hop chain |
| 12 | CalcUsage → CalcUsage (via EXPOSE) | `financial { in total_capex = total_capex }` | Transitive resolution through EXPOSE alias |

**Validation Steps**:

1. **Parse** model with syside:
   ```bash
   uv run syside check models/tests/e2e_attr_expr/
   ```

2. **Validate** with agentic-mbse (L1-L8):
   ```bash
   uv run agentic-mbse validate models/tests/e2e_attr_expr/ --complete
   ```
   Expected: No V2 violations on FORMULA attributes, L8 passes.

3. **Generate** code:
   ```bash
   uv run sysml-codegen generate \
     --models models/tests/e2e_attr_expr/ \
     --output generated/e2e_attr_expr \
     --package-name e2e_attr_expr \
     --overwrite --verbose
   ```

4. **Inspect** generated output:
   - Count total modules: expect 4 CalcUsage + ~6 FORMULA synthetic + entry/exit = ~12
   - Verify all `_impl.py` have `AUTO_IMPLEMENTED = True`
   - Verify FORMULA modules in pipeline YAML with `# source: computed_attribute`
   - Verify `annualized_om` is NOT FORMULA (it's just a FORMULA attribute) — wait, actually `annual_om` IS a FORMULA attribute. The CalcUsage `lcoe { in annual_om = annual_om }` should wire from the synthetic module.
   - Verify IMPLEMENTATION_BACKLOG.md shows 0 functions to implement

5. **Execute** via TEAx:
   ```bash
   uv run python generated/e2e_attr_expr/run_pipeline.py
   ```

6. **Verify** numerical outputs against ground truth table.

---

### Phase C: Regression — Existing Tests

**Goal**: Confirm no regressions across all three codebases.

1. **sysml-codegen tests** (285 tests):
   ```bash
   cd ~/1cfe/sysml-codegen && uv run pytest tests/ -v
   ```

2. **agentic-mbse tests** (886 tests):
   ```bash
   cd ~/1cfe/agentic-mbse && uv run pytest tests/ -v
   ```

3. **fusion-tea model tests** (39+ tests):
   ```bash
   cd ~/1cfe/fusion-tea && uv run pytest tests/ -v
   ```

4. **fusion-tea agentic-mbse validate**:
   ```bash
   cd ~/1cfe/fusion-tea && uv run agentic-mbse validate models/ --complete
   ```

---

### Phase D: E2E Pipeline Execution — Solar Battery via TEAx

**Goal**: Run the full solar_battery hybrid pipeline with regenerated codegen and verify LCOE output.

**Steps**:

1. **Regenerate** (Phase A output)
2. **Update hybrid pipeline.yaml** to include `solar_battery_plant__p_net_kw` synthetic module (replace ComponentCostEvaluator's p_net_kw output with the synthetic module's output)
3. **Execute**:
   ```bash
   uv run python generated/solar_battery/run_pipeline.py
   ```
4. **Verify** against existing output values in `generated/solar_battery/outputs/`
5. **Compare** LCOE value: should be identical to prior hybrid pipeline run

---

## Architecture Insights

### The Three-Phase Expression Feature Roadmap

```
Phase 1: EXPR-CODEGEN (Complete)
  ├── CalcDef output expression auto-compilation
  ├── 15/15 solar_battery CalcDefs auto-implemented
  ├── 19/21 CATF CalcDefs auto-implemented
  └── Eliminated _impl.py bottleneck for CalcDefs

Phase 2: ATTR-EXPR (Complete)
  ├── FORMULA computed attributes → synthetic modules
  ├── 5-way classification (FORMULA, EXPOSE_PURE, EXPOSE_COMPUTED, LITERAL, UNRESOLVABLE)
  ├── Backtracker FORMULA→MODULE_OUTPUT resolution
  ├── Graph builder unified topological sort
  ├── agentic-mbse V2 + L8 FORMULA exemption
  └── Eliminated CalcDef ceremony for simple formulas

Phase 3: Nested Hierarchies (NOT STARTED)
  ├── CalcUsage-in-PartDef template instantiation (Gap A)
  ├── :>> redefinition chain resolution (Gap B)
  ├── sum() / NumericalFunctions compilation (Gap C)
  ├── Multiplicity [count] handling (Gap D)
  ├── Assembly cost aggregation expressions (Gap E)
  └── Eliminates hybrid pipeline → full codegen for CostedComponent
```

### What Phase 3 Unlocks

When Phase 3 is complete, the entire solar_battery pipeline becomes purely codegen-generated:
- 9 leaf-part cost_model CalcUsages instantiated per-PartUsage
- Assembly cost rollup via sum() and cross-part refs compiled
- No more ComponentCostEvaluator wrapper
- Full LCOE pipeline from SysML → Python → TEAx without manual code

### The FORMULA-CalcUsage Interaction is the Key Innovation

The most valuable new pattern is FORMULA → CalcUsage wiring:

```sysml
attribute p_net_kw = p_net_mw * 1000.0;  // FORMULA → synthetic module
calc annualized_om : AnnualizedOMCalc {
    in p_net_kw = p_net_kw;  // Binds to FORMULA output, not entry point
}
```

This eliminates the need for:
1. A CalcDef for unit conversion (`UnitConversionCalc`)
2. A CalcUsage wiring the conversion to downstream calc
3. A `_impl.py` for the conversion calc

**Impact**: Every simple derived attribute that feeds a downstream calculation can now be a FORMULA instead of a CalcDef. This reduces modeling overhead by ~100 lines per formula.

---

## Feasibility Assessment

### What's Immediately Testable

| Test | Feasibility | Effort | Blocking? |
|------|-------------|--------|-----------|
| Phase A: Regenerate solar_battery | **High** — just run codegen | 1-2 hours | No |
| Phase B: New e2e_attr_expr model | **High** — flat model, no Phase 3 gaps | 2-4 hours | No |
| Phase C: Regression tests | **High** — existing suites | 30 min | No |
| Phase D: TEAx execution | **Medium** — may need pipeline.yaml update | 2-4 hours | No |

### What Requires Phase 3

| Capability | Effort | Blocking For |
|-----------|--------|-------------|
| CalcUsage-in-PartDef template instantiation | ~3-5 days | Full CostedComponent pipeline |
| `:>>` redefinition chain resolution | ~2-3 days | Template instantiation bindings |
| `sum()` compilation | ~1-2 days | Assembly cost rollup |
| Multiplicity handling | ~2-3 days | Arrayed part expansion |
| Assembly aggregation | ~1-2 days | Full cost pipeline |
| **Total Phase 3** | **~10-15 days** | **Replacing hybrid pipeline entirely** |

---

## Recommendations

### 1. Execute Phases A-D Immediately

All four validation phases are feasible now with existing tooling. They exercise all Phase 1 + Phase 2 features without triggering Phase 3 gaps. This provides confidence that the features work correctly before pursuing Phase 3.

### 2. Create the e2e_attr_expr Test Model

The model design in Phase B exercises 12 distinct patterns. It should become a permanent regression test in fusion-tea, alongside the existing solar_battery and coffee_maker models.

### 3. Write fusion-tea Integration Tests

Add pytest tests that:
- Run codegen on e2e_attr_expr model
- Assert correct module count and types
- Assert auto-implementation for all functions
- Execute TEAx pipeline
- Assert numerical outputs against ground truth

### 4. Phase 3 Planning as Separate Epic

The Phase 3 gaps are substantial (~10-15 days) and should be a separate epic in sysml-codegen. The priority is:
1. Template instantiation + redefinition resolution (must be together)
2. `sum()` compilation + multiplicity handling (must be together)
3. Assembly aggregation expressions (depends on 1+2)

### 5. Update fusion-tea Backlog

- Update WI-006 status to Complete (CostedComponent interface exists)
- Add new WI for Phase 3 dependency tracking
- Note that WI-007 through WI-010 are blocked on Phase 3 for full codegen, but can proceed with the hybrid pattern

---

## Open Questions

1. **Should the e2e_attr_expr model live in `models/tests/` or as a sysml-codegen test fixture?** Recommendation: Both. Create in fusion-tea for end-to-end TEAx validation, and a simplified version in sysml-codegen for unit/integration tests.

2. **Should we update the hybrid pipeline.yaml for solar_battery?** The current pipeline routes p_net_kw through ComponentCostEvaluator. After regeneration, the codegen-generated pipeline will have a synthetic module for p_net_kw. The hybrid pipeline needs manual updating to use the synthetic module instead.

3. **Is there value in running Phase 1 auto-impl on the hybrid pipeline?** Yes — the 15 CalcDef `_impl.py` stubs would be auto-implemented, eliminating the "15 functions to implement" backlog. Even if the hybrid pipeline structure stays, the implementations would be auto-generated.

4. **Should the `generated/` and `generated2/` directories be cleaned up?** `generated2/` has only `__pycache__` remnants and no source files. It should be removed. `generated/solar_battery/` should be regenerated with latest codegen.

---

## Code References

### sysml-codegen (Phase 2 implementation)

- `src/sysml_codegen/extraction/computed_attribute_extractor.py` — FORMULA extraction + classification
- `src/sysml_codegen/extraction/data_models.py` — ComputedAttributeData, ComputedAttributeClassification
- `src/sysml_codegen/extraction/expression_compiler.py` — Expression AST → Python compilation
- `src/sysml_codegen/generation/initialization.py:140-196` — Step 4.5 integration
- `src/sysml_codegen/analysis/dependency_backtracker.py:395-413` — FORMULA MODULE_OUTPUT resolution
- `src/sysml_codegen/resolution/graph_builder.py:623-740` — FORMULA module generation
- `tests/integration/test_computed_attributes_e2e.py` — 21 E2E tests

### agentic-mbse (FORMULA validation)

- `src/agentic_mbse/validation/adr002.py:393-459` — `_is_formula_pattern()`
- `src/agentic_mbse/validation/level8_codegen.py:377-405` — `_is_codegen_handled_pattern()`
- `tests/test_sysml/test_adr002.py:514-561` — 7 FORMULA tests
- `docs/patterns/adr002-calculations.md:261-305` — FORMULA section

### fusion-tea (models and infrastructure)

- `models/library/foundation/costing.sysml` — 'Costed Component' interface
- `models/tests/solar_battery/library.sysml` — 14 CalcDefs + 13 PartDefs
- `models/tests/solar_battery/design.sysml` — Design instance with p_net_kw FORMULA
- `generated/solar_battery/pipelines/pipeline.yaml` — Hybrid pipeline
- `generated/solar_battery/run_pipeline.py` — TEAx execution entry point

### ADRs

- `sysml-codegen/docs/architecture/ADR-004-computed-attribute-pipeline-integration.md` — Option C, Step 4.5, naming
- `sysml-codegen/docs/architecture/ADR-005-computed-attribute-classification.md` — 5-way classification

---

**Last Updated**: 2026-02-10
