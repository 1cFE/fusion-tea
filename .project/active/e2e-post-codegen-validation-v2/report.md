# Validation Report: E2E Post-Codegen Validation V4 (COST-PATTERN Epic)

**Date:** 2026-02-20
**Branch (sysml-codegen):** cost-pattern-refactor
**Branch (fusion-tea):** e2e-attr-expr
**Validator:** Claude (automated)
**V2 Report:** `.project/active/e2e-attr-expr-validation-v2/report.md`

---

## Executive Summary

V4 validation confirms that **all 7 original codegen bugs are fully fixed** (including Bug 2 EXPOSE→CalcUsage, which was PARTIAL in V2). The COST-PATTERN hierarchy features (template instantiation, `:>>` resolution, multiplicity handling, aggregation modules, topological ordering) all generate correctly and produce numerically accurate results.

The **ComponentCostEvaluator hybrid merge is no longer needed** — native codegen produces 36 pipeline modules (vs 16 in V2) that replace it entirely. One new bug was discovered (Bug 12: pipeline.yaml output mismatch for CalcDefs with defaulted outputs).

**Workaround count: V1 = 7 bugs / ~15 edits → V2 = 1 workaround + 2 __init__.py → V4 = 1 new workaround (Bug 12, 2 edits) → V5 = 0 workarounds**

**UPDATE (2026-02-20):** V5 clean regeneration confirms Bug 11/12 are fixed in the codegen. Both `solar_battery_v5` and `e2e_attr_expr_v5` run from clean codegen output with zero manual edits. All ground truth values pass. See V5 section at end of report.

| Phase | Status | Summary |
|-------|--------|---------|
| 1 (Regression Baseline) | SKIPPED | sysml-codegen mid-refactor (30 uncommitted files), user confirmed safe |
| 2 (E2E Attr Expr Codegen) | **PASS** | All structural bug checks pass, including Bug 2 FULLY FIXED |
| 3 (E2E Attr Expr Pipeline) | **PASS** | 16/16 values, 0 workarounds |
| 4 (Solar Battery Codegen) | **PASS** | All hierarchy features generate correctly |
| 5 (Solar Battery Pipeline) | **PASS** | 7/7 values, 1 workaround (Bug 12), no ComponentCostEvaluator |
| 6 (Report) | This document |

---

## Phase 2-3: E2E Attr Expr Results

### Codegen Output (V4)
- 10 modules generated (4 CalcDef + 6 FORMULA)
- 10/10 _impl files AUTO_IMPLEMENTED
- 0 functions to implement
- **0 workarounds needed** (V2 required 1 workaround + 2 __init__.py)

### Structural Bug Verification
- Bug 1 (FORMULA entry points): PASS — all 7 FORMULA input params in design_params.py
- Bug 2 (EXPOSE→CalcUsage): **PASS — FULLY FIXED** (was PARTIAL in V2). `total_capex` wired to `component_cost__total_cost` MODULE_OUTPUT. No orphaned entry point.
- Bug 3 (Float/float): PASS — all input fields use lowercase `float`
- Bug 7 (__init__.py): **PASS — FULLY FIXED** (was PARTIAL in V2). No missing __init__.py anywhere.

### Numerical Results (16/16 PASS)

| Value | Expected | Actual | Tolerance | Status |
|-------|----------|--------|-----------|--------|
| power_mw | 0.005 | 0.005 | exact | PASS |
| power_kw | 5.0 | 5.0 | exact | PASS |
| annual_om | 100.0 | 100.0 | exact | PASS |
| area | 50.0 | 50.0 | exact | PASS |
| volume | 150.0 | 150.0 | exact | PASS |
| surface_cost | 600.0 | 600.0 | exact | PASS |
| material_cost | 5000.0 | 5000.0 | exact | PASS |
| fab_cost | 2250.0 | 2250.0 | exact | PASS |
| install_cost | 1500.0 | 1500.0 | exact | PASS |
| total_cost | 8750.0 | 8750.0 | exact | PASS |
| idiot_index | 1.75 | 1.75 | exact | PASS |
| crf | 0.07095 | 0.07095246 | 1e-4 | PASS |
| annualized_cost | 620.84 | 620.834 | 1e-4 | PASS |
| annual_energy_mwh | 39.42 | 39.42 | exact | PASS |
| lcoe | 18.27 | 18.286 | 1e-3 | PASS |
| total_capex (transitive) | 8750.0 | 8750.0 | transitive | PASS |

---

## Phase 4-5: Solar Battery Results

### Codegen Output (V4)
- 36 modules generated (15 CalcDef + 20 aggregation + 1 FORMULA)
- 36/36 _impl files AUTO_IMPLEMENTED
- 0 functions to implement
- 3 parameter group schemas: design_params, library_params, system_design
- **ComponentCostEvaluator NOT needed** — native aggregation replaces it

### Hierarchy Feature Verification

| Feature | Expected | Actual | Status |
|---------|----------|--------|--------|
| 9 leaf-part cost modules | Generated with hierarchy names | All 9 generated: pv_module, inverter, array_bos, battery_pack, hybrid_inverter, battery_bos, racking, electrical_panel, permitting | **PASS** |
| Allocation model | Generated | solar_array__allocation_model generated (AllocationCostCalcModule) | **PASS** |
| 4 aggregation assemblies | Generated with `# source: aggregation` | 20 aggregation modules generated (capital, raw_material, fabrication, installation, idiot_index at 4 levels) | **PASS** (exceeds expected) |
| `:>>` literal resolution | 13 design params resolved | All 13 in system_design.py with correct default values | **PASS** |
| Multiplicity entry points | 3 counts (20, 4, 8) | module_count=20.0, inverter_count=4.0, pack_count=8.0 in system_design.py | **PASS** (float type, see Bug 10) |
| Topological ordering | leaf → aggregation → system | leaf → sub-assembly aggregation → plant aggregation → system calcs → lcoe | **PASS** |
| System CalcUsage wiring | total_capex → aggregation output | `total_capex: float ...capital_cost__capital_cost.root` (MODULE_OUTPUT) | **PASS** |
| ComponentCostEvaluator merge | Not needed | Confirmed: native pipeline runs without it | **PASS** |
| LCOE numerical correctness | 7/7 values pass | All 7 pass (see table below) | **PASS** |

### Numerical Results (7/7 PASS)

| Metric | Expected | Actual | Tolerance | Status |
|--------|----------|--------|-----------|--------|
| total_capex | 41205.0 | 41205.0 | exact | PASS |
| annual_energy_mwh | 11.14272 | 11.14272 | 1% | PASS |
| annual_om_cost | 160.0 | 160.0 | 1% | PASS |
| annual_fuel_cost | 0.0 | 0.0 | exact | PASS |
| capital_recovery_factor | 0.07095246 | 0.07095246 | 1% | PASS |
| annualized_capital_cost | 2923.60 | 2923.596 | 1% | PASS |
| lcoe_per_mwh | 288.68 | 288.676 | 1% | PASS |

### Smart-Regen Test (Bug 5)
- 34 preserved (signature unchanged), 2 regenerated, 0 new
- 36/36 AUTO_IMPLEMENTED after smart-regen
- 0 NotImplementedError
- **PASS**: No stub downgrading

---

## Per-Bug Fix Verification Matrix

| Bug | Description | V1 | V2 | V4 | Evidence |
|-----|-------------|----|----|-----|----------|
| 1 | FORMULA entry point omission | FAIL (7 manual params) | PASS | **PASS** | Phase 2: all 7 FORMULA params in design_params.py |
| 2 | Backtracker wiring (EXPOSE→CalcUsage) | FAIL (3 manual rewires) | PARTIAL | **PASS** | Phase 2: total_capex wired to MODULE_OUTPUT, no orphaned entry point |
| 3 | FORMULA Float/float types | FAIL (6 manual edits) | PASS | **PASS** | Phase 2: all input fields use `float` |
| 4 | ExitPoint float handler | FAIL (manual writes) | PASS | **PASS** | Phase 3: all float channels serialize to JSON via ExitPoint |
| 5 | Smart-regen stub upgrade | Documented | N/A | **PASS** | Phase 5.7: 36/36 preserved AUTO_IMPLEMENTED after smart-regen |
| 6 | `&` in Python identifiers | FAIL (manual renames) | PASS | **PASS** | Phase 4: `&` only in comments, not identifiers |
| 7 | Missing `__init__.py` | FAIL (2 manual) | PARTIAL | **PASS** | Phase 2+4: no missing __init__.py in any directory |
| 8 | `__init__.py` wrong import paths + name collisions | N/A | N/A | **PASS** | Phase 4: aliased imports handle 5 collision groups correctly |
| 9 | Missing `system_design.` prefix on entry point channels | N/A | N/A | **PASS** | Phase 4: 3 param groups with correct prefixes (design_params, library_params, system_design) |
| 10 | `int` type for multiplicity counts | N/A | N/A | **NOTED** | Phase 4: multiplicity counts are `float` (20.0, 4.0, 8.0). Functionally correct but semantically imprecise. |
| 11 | `default=0.0` on MultiOutput fields | N/A | N/A | **~~NEW BUG 12~~ FIXED V5** | Phase 5: PermittingCostCalc defaults cause registry/pipeline mismatch. **V5 UPDATE:** Schema now uses `Field(description=...)` without defaults. TEAx registers all 5 outputs. |
| 12 | Pipeline.yaml declares unregistered outputs | N/A | N/A | **~~WORKAROUND~~ FIXED V5** | Phase 5: PermittingCostCalcOutput fields with `default=0.0` not registered by TEAx. **V5 UPDATE:** Root cause fixed — pipeline.yaml now declares all 5 outputs and they all register correctly. 0 edits needed. |

**Summary:** 9 PASS, 1 NOTED (Bug 10 — cosmetic), ~~1 NEW with workaround (Bug 12)~~ **V5: 11 PASS, 1 NOTED (Bug 10). All bugs fully resolved.**

---

## V1 vs V2 vs V4 Comparison

### Workaround Count

| Metric | V1 | V2 | V4 | V5 (Delta) |
|--------|----|----|-----|------------|
| Bugs requiring workarounds | 7 | 1 (Bug 2) | 1 (Bug 12 new) | **0** |
| Files manually modified post-codegen | ~15 edits | 4 edits (2 Bug 2 + 2 __init__.py) | 2 edits (Bug 12 pipeline.yaml) | **0 edits** |
| ComponentCostEvaluator hybrid merge | Yes (8 files) | Yes (8 files) | **NO** | **NO** |
| Total manual intervention | ~23 edits + hybrid merge | 4 edits + hybrid merge | 2 edits, no hybrid | **0 edits, 0 workarounds** |

**V5 UPDATE:** The V4→V5 column reflects clean regeneration after Bug 11/12 fix in sysml-codegen. Zero manual intervention required.

### Module Generation

| Metric | V1 | V2 | V4 |
|--------|----|----|-----|
| e2e_attr_expr modules | 10 | 10 | 10 |
| solar_battery modules | 16 | 16 | **36** (+20 aggregation/hierarchy) |
| solar_battery _impl files | 16 | 16 | **36** |
| Parameter group schemas | 1 | 1 | **3** (design, library, system_design) |
| JSON input templates | 1 | 1 | **3** |

### Test Results

| Codebase | V1 | V2 | V4 |
|----------|----|----|-----|
| sysml-codegen | 285 passed | 313 passed | N/A (skipped Phase 1) |
| agentic-mbse | 886 passed | 886 passed | N/A (skipped Phase 1) |
| fusion-tea core | 42 passed | 48 passed | 48 passed, 1 skipped |
| e2e_attr_expr generated | 4 passed | 4 passed | 4 passed |
| solar_battery generated | N/A | 15 passed | 15 passed |

---

## New Issues Discovered

### Bug 12: Pipeline.yaml declares unregistered outputs for CalcDefs with defaulted MultiOutput fields

**Description:** When a CalcDef's output schema has fields with `default=0.0` (e.g., PermittingCostCalc's `material_cost`, `fab_cost`, `install_cost`, `idiot_index`), TEAx's `create_registry()` excludes these fields from the module's output metadata. However, the codegen's pipeline.yaml generator declares all schema fields as outputs. This mismatch causes `PipelineValidationError: Output bindings do not match registry metadata`.

**Root Cause:** The codegen pipeline generator uses the SysML CalcDef attribute count to determine output declarations, rather than checking what `create_registry()` will actually register.

**Workaround:** Edit pipeline.yaml to only declare `total_cost` as the output for PermittingCostCalc. 2 edits (module outputs + exit_point). Smart-regen overwrites this workaround.

**Impact:** Affects any CalcDef where some output attributes have `default :=` values in the SysML model. PermittingCostCalc is the only affected CalcDef in the solar_battery model.

**Recommended Fix:** In sysml-codegen, the pipeline output declaration should match what TEAx will register — either (a) don't generate `default=` on output schema fields, or (b) only declare outputs that lack defaults.

### Bug 10 (cosmetic): Multiplicity counts use float type

**Description:** `module_count`, `inverter_count`, `pack_count` are generated as `float` (20.0, 4.0, 8.0) rather than `int`. This is functionally correct (TEAx treats all numerics as float in pipeline channels) but semantically imprecise.

---

## Gate Decision

### PASS — COST-PATTERN epic hierarchy features validated end-to-end

**Justification:**

1. **All original bugs fully fixed:** 9/9 testable bugs PASS (including Bug 2 which was PARTIAL in V2 and Bug 7 which was PARTIAL in V2).
2. **Hierarchy features generate correctly:** 9 leaf-part modules, 20 aggregation modules, 13 `:>>` resolutions, 3 multiplicity entry points, correct topological ordering — all native from codegen.
3. **ComponentCostEvaluator eliminated:** The external hybrid merge pattern is no longer needed. Native codegen produces a complete pipeline.
4. **Numerical accuracy confirmed:** All 23 ground truth values pass (16 e2e_attr_expr + 7 solar_battery).
5. **Smart-regen safe:** No stub downgrading on re-runs.
6. **Minimal workarounds:** Only Bug 12 (2 edits) — a new issue in the pipeline output declaration, not a regression.

**Conditions:**

- File Bug 12 (pipeline.yaml output mismatch for defaulted MultiOutput fields) against sysml-codegen — non-blocking, 2-edit workaround
- Bug 10 (float multiplicity counts) is cosmetic — file for future cleanup
- Smart-regen overwrites Bug 12 workaround — document in project notes

---

---

## **UPDATE: V5 Clean Regeneration (2026-02-20)**

### Purpose
Regenerated both packages from scratch as `_v5` to confirm Bug 11/12 fixes are in the codegen itself — no manual workarounds needed.

### Codegen Results

| Package | Modules | CalcDefs Compiled | Manual Impls | Workarounds |
|---------|---------|-------------------|--------------|-------------|
| e2e_attr_expr_v5 | 10 | 4/4 fully_compilable | 0 | 0 |
| solar_battery_v5 | 36 | 15/15 fully_compilable | 0 | 0 |

### Bug 11/12 Fix Verification

**Bug 11 (default=0.0 on MultiOutput fields):**
- V4: `PermittingCostCalcOutput` had `material_cost: float = Field(default=0.0, ...)` — TEAx excluded defaulted fields from registry
- V5: `PermittingCostCalcOutput` has `material_cost: float = Field(description="...")` — no defaults, all 5 fields registered

**Bug 12 (pipeline.yaml declares unregistered outputs):**
- V4: pipeline.yaml trimmed to only `total_cost` for PermittingCostCalc (manual workaround, 2 edits)
- V5: pipeline.yaml declares all 5 outputs (`material_cost`, `fab_cost`, `install_cost`, `total_cost`, `idiot_index`) — matches registry, no edits needed

### Pipeline Execution Results

**solar_battery_v5: ALL 7 VALUES PASS**

| Metric | Expected | Actual | Status |
|--------|----------|--------|--------|
| total_capex | 41205.0 | 41205.0 | PASS |
| annual_energy_mwh | 11.14272 | 11.14272 | PASS |
| annual_om_cost | 160.0 | 160.0 | PASS |
| annual_fuel_cost | 0.0 | 0.0 | PASS |
| capital_recovery_factor | 0.07095246 | 0.07095246 | PASS |
| annualized_capital_cost | 2923.60 | 2923.596 | PASS |
| lcoe_per_mwh | 288.68 | 288.676 | PASS |

**e2e_attr_expr_v5: ALL 16 VALUES PASS**
- All 15 ExitPoint values pass + EXPOSE_PURE (total_capex) verified transitively
- Patterns 1-12 all confirmed

### Revised Workaround Progression

```
V1:  ~23 edits + ComponentCostEvaluator hybrid merge
V2:  4 edits + ComponentCostEvaluator hybrid merge
V4:  2 edits (Bug 12), no hybrid merge
V5:  0 edits, 0 workarounds, no hybrid merge   <<<--- CLEAN
```

### Remaining Informational Warnings (not bugs)
- 10 "Registry unresolved" warnings for binding-traced params — resolve via JSON entry points (working as designed)
- 3 unresolved aggregation inputs for `permitting.{raw_material_cost, fabrication_cost, installation_cost}` — fall back to `system_design` JSON defaulting to 0.0 (correct for soft-cost-only component)
- Bug 10 (float multiplicity counts) remains cosmetic

### Revised Gate Decision

### PASS — All bugs fully resolved, zero workarounds

The V5 clean regeneration confirms the codegen fix for Bug 11/12 is complete. The full pipeline from SysML models to verified LCOE output now runs with **zero manual intervention**. COST-PATTERN Item 5 (E2E Validation & Documentation) is fully validated.

---

**Report complete.** COST-PATTERN Item 5 (E2E Validation & Documentation) can proceed to closure.
