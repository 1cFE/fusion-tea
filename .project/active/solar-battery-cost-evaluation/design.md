# Design: Solar+Battery Cost Evaluation & Entry Point Generation

**Status:** Draft
**Owner:** Reid Westwood
**Created:** 2026-02-01 23:58 UTC
**Updated:** 2026-02-02 00:05 UTC
**Branch:** visualization
**Commit:** 6bf245d

## Overview

Adapt the coffee maker's `generate_costs.py` for the solar+battery model, changing only the root part name and path strings, then add two JSON generation functions for TEAx entry points and an automated LCOE sanity check. The existing evaluation engine (extract -> resolve -> evaluate -> aggregate) handles the solar battery model without structural changes.

## Related Artifacts

- **Spec:** `.project/active/solar-battery-cost-evaluation/spec.md`
- **Epic:** `.project/backlog/epic-end-to-end-pipeline-derisking.md` (Item 3)
- **Reference:** `models/tests/coffee_maker/generate_costs.py` (1631 lines)
- **Reference tests:** `models/tests/coffee_maker/test_generate_costs.py` (113 lines)
- **SysML model:** `models/tests/solar_battery/library.sysml`, `design.sysml`
- **Expected values:** `models/tests/solar_battery/expected_output.csv`, `expected_system_outputs.csv`

## Research Findings

### Coffee Maker Pattern Analysis

The coffee maker `generate_costs.py` has these sections (all reusable as-is):

| Section | Lines | Purpose | Solar Battery Changes |
|---------|-------|---------|----------------------|
| Data structures | 33-100 | `InputParam`, `OutputFormula`, `CalcDefInfo`, `AllocationInfo`, `PartInstance`, `CostResult` | None |
| Calc def extractor | 107-241 | `extract_calc_defs()`, literal/ref extraction | None |
| Part def mapper | 248-304 | `map_part_defs_to_calcs()` | None |
| Design extractor | 312-505 | `extract_design_hierarchy()`, binding resolution | `ROOT_PART_NAME` constant |
| Formula evaluator | 909-1058 | `evaluate_calc()`, expression AST evaluation | None |
| Cost aggregator | 1066-1299 | Leaf, assembly, allocation cost computation | None |
| Public API | 1306-1379 | `compute_costs()` | `ROOT_PART_NAME` constant |
| Output generator | 1387-1511 | `write_csv()`, `compare_outputs()` | None |
| Main | 1519-1631 | CLI entry point | Add JSON output + LCOE check |

### Structural Compatibility Verification

The solar battery model uses identical SysML patterns to the coffee maker:

| Pattern | Coffee Maker | Solar Battery | Compatible? |
|---------|-------------|---------------|-------------|
| Nested `cost_model` CalcUsage in PartDef | 5 leaves | 9 leaves | Yes |
| `:>>` bindings in `part redefines` blocks | 2 contexts (brewing, housing) | 3 contexts (solar_array, battery_system, site_infra) | Yes |
| Parameterized multiplicity | heater[2] | pv_module[20], inverter[4], battery_pack[8] | Yes |
| `allocation_model` on assembly | Brewing System only | Solar Array only | Yes |
| Assembly aggregation | 2 assemblies + root | 3 assemblies + root | Yes |
| `idiot_index = total_cost / material_cost` | All leaves have material > 0 | Permitting has material = 0, but calc outputs `idiot_index = 0.0` directly | Yes (see below) |

### Edge Case: Permitting Soft Cost

`PermittingCostCalc` (library.sysml:210-229) outputs `material_cost = 0.0` and `idiot_index = 0.0` as literal values. The evaluator reads these from the calc output — it does NOT compute `idiot_index` itself for leaves. No division by zero occurs.

For Site Infrastructure assembly: `raw_material_cost = 1140 + 286 + 0 = 1426 > 0`, so the assembly-level `idiot_index = 3995.50 / 1426.00 = 2.80` is safe.

### Design Parameters Extraction

The design.sysml attributes (`p_net_mw`, `n_mod`, etc.) are `AttributeUsage` elements owned by the `solar_battery_plant` part usage. These are NOT extracted by the existing binding resolution code (which only handles `:>>` redefinitions on child parts). New extraction logic is needed to read these top-level attributes.

The `p_net_kw` attribute is a derived expression (`p_net_mw * 1000.0`). Rather than evaluating this expression through the AST, the JSON generator should compute it from the extracted `p_net_mw` value — simpler and the same result.

### System-Level Calcs: Scope Clarification

The 5 system-level CalcDefs (EnergyProductionCalc, AnnualizedOMCalc, AnnualizedFuelCalc, AnnualizedFinancialCalc, LCOECalc) are **extracted** by `extract_calc_defs()` (they exist in the model) but are **not evaluated through the SysML AST** by this script. Evaluating them through the codegen -> TEAx path is the purpose of Items 4-5.

However, since `design_params.json` contains all inputs needed to compute LCOE independently, this script SHOULD include an automated LCOE sanity check that:
1. Computes LCOE from the design params using the PyFECONS formula in Python
2. Compares against `expected_system_outputs.csv`
3. Validates that the entry point data is correct _before_ Items 4-5 consume it

This catches errors in parameter extraction without duplicating the codegen pipeline.

## Design Decisions

**DD-1: System-level calcs evaluated in Python, not through SysML AST.**

The 5 system-level calcs are not evaluated via the SysML expression evaluator. Instead, a pure-Python `verify_system_outputs()` function computes LCOE from the extracted design params and total CAPEX, then compares against `expected_system_outputs.csv`. This validates the entry point data is correct without duplicating Item 4-5's codegen path.

## Proposed Design

### Architecture

```
generate_costs.py (adapted copy)
├── [UNCHANGED] Data structures (dataclasses)
├── [UNCHANGED] Calc def extractor
├── [UNCHANGED] Part def mapper
├── [CHANGED]   Design extractor (uses ROOT_PART_NAME module constant)
├── [UNCHANGED] Formula evaluator
├── [UNCHANGED] Cost aggregator
├── [UNCHANGED] Public API: compute_costs()
├── [UNCHANGED] Output generator (write_csv, compare_outputs)
├── [NEW]       JSON generators: write_component_costs_json(), write_design_params_json()
├── [NEW]       Design param extractor: extract_design_params()
├── [NEW]       System-level verifier: verify_system_outputs()
└── [CHANGED]   Main (adds JSON output + system verification steps)
```

### File 1: `models/tests/solar_battery/generate_costs.py`

**Approach:** Full copy of `models/tests/coffee_maker/generate_costs.py` with targeted edits.

#### Change 1: Module-level ROOT_PART_NAME constant

Define once near the top of the file (~line 30):

```python
ROOT_PART_NAME = "solar_battery_plant"
```

Referenced by `extract_design_hierarchy()`, `compute_costs()`, and `main()`. Eliminates the hardcoded string in multiple locations.

#### Change 2: New function `extract_design_params()`

```python
def extract_design_params(
    root_usage: Any,
    total_capex: float,
) -> dict[str, float]:
    """Extract system-level parameters from the design's root part usage.

    Reads AttributeUsage elements with literal values from the root part.
    Returns flat dict suitable for design_params.json.
    """
```

**Logic:**
1. Iterate `root_usage.owned_members` looking for `AttributeUsage` elements
2. For each, extract name and `feature_value_expression` literal value via `_extract_literal_from_expr()`
3. Filter to the known parameter names: `p_net_mw`, `n_mod`, `plant_availability`, `plant_lifetime`, `yearly_inflation`, `discount_rate`, `om_rate_per_kw_year`, `fuel_unit_cost`, `fuel_consumption`
4. Compute derived: `p_net_kw = p_net_mw * 1000.0`
5. Add `total_capex` from the cost rollup result
6. Validate all 11 expected keys are present; raise `ValueError` if any are missing
7. Skip `p_net_kw` from AST extraction (it's an `OperatorExpression`, not a `LiteralRational` — `_extract_literal_from_expr()` returns `None`)

#### Change 3: New function `write_component_costs_json()`

```python
def write_component_costs_json(
    results: list[CostResult],
    output_path: Path,
) -> None:
    """Write component costs as JSON entry point for TEAx.

    Values come from assembly-level CostResult rows (the aggregated totals),
    not re-summed from children.
    """
```

**Logic:**
1. Find the root assembly `CostResult` (where `path == ROOT_PART_NAME`)
2. Find subsystem assembly `CostResult` rows by exact path match:
   - `ROOT_PART_NAME + ".solar_array"`
   - `ROOT_PART_NAME + ".battery_system"`
   - `ROOT_PART_NAME + ".site_infra"`
3. Build dict using each `CostResult`'s `total_cost`, `total_material_cost`, `total_fab_cost`, `total_install_cost` fields:
   ```python
   {
       "total_capex": root_result.total_cost,
       "solar_array": {
           "total_cost": sa_result.total_cost,
           "material_cost": sa_result.total_material_cost,
           "fab_cost": sa_result.total_fab_cost,
           "install_cost": sa_result.total_install_cost,
       },
       "battery_system": { ... },
       "site_infra": { ... },
   }
   ```
4. Write with `json.dump(data, f, indent=2)`

#### Change 4: New function `write_design_params_json()`

```python
def write_design_params_json(
    params: dict[str, float],
    output_path: Path,
) -> None:
    """Write design parameters as JSON entry point for TEAx."""
```

Simple: `json.dump(params, f, indent=2)`

#### Change 5: New function `verify_system_outputs()`

```python
def verify_system_outputs(
    params: dict[str, float],
    expected_path: Path,
    tolerance: float = 0.01,
) -> tuple[bool, list[str]]:
    """Compute system-level outputs from design params and verify against expected.

    Evaluates the 5 PyFECONS-aligned calculations in pure Python (not through
    the SysML AST) to validate that entry point data produces correct LCOE.
    """
```

**Logic:**
1. Compute each system-level output from `params`:
   - `annual_energy_mwh = 8760 * p_net_mw * n_mod * plant_availability`
   - `annual_om_cost = om_rate_per_kw_year * p_net_kw`
   - `annual_fuel_cost = fuel_unit_cost * fuel_consumption`
   - `crf = r * (1+r)^n / ((1+r)^n - 1)` where `r = discount_rate`, `n = plant_lifetime`
   - `annualized_capital_cost = crf * total_capex`
   - `lcoe_per_mwh = (annualized_capital_cost + (annual_om_cost + annual_fuel_cost) * (1 + yearly_inflation)^plant_lifetime) / annual_energy_mwh`
2. Read `expected_system_outputs.csv`
3. Compare each output against expected value within tolerance (1% relative)
4. Return `(passed, diffs)` tuple matching `compare_outputs()` pattern

#### Change 6: Updated `main()`

After Phase 5 (write CSV), add:

```
Phase 6: Extract design params from root part usage
Phase 7: Write component_costs.json
Phase 8: Write design_params.json
Phase 9: Verify system-level outputs against expected_system_outputs.csv
Phase 10: Compare CSV with expected (existing, renumbered)
```

The root part usage (`root_usage`) needs to be accessible for `extract_design_params()`. Find it in `main()` by scanning for `ROOT_PART_NAME` in PartUsages (~3 lines). This is the same lookup `extract_design_hierarchy()` does internally but avoids changing that function's return type, keeping `compute_costs()` API unchanged.

### File 2: `models/tests/solar_battery/test_generate_costs.py`

**Approach:** Adapt from `models/tests/coffee_maker/test_generate_costs.py` (113 lines).

Tests:

| # | Test | Adapted From | Notes |
|---|------|-------------|-------|
| 1 | `test_compute_costs_returns_dict` | Coffee maker test 1 | |
| 2 | `test_compute_costs_has_all_expected_paths` | Coffee maker test 2 | 13 paths |
| 3 | `test_compute_costs_has_all_cost_attributes` | Coffee maker test 3 | |
| 4 | `test_compute_costs_values_are_numeric` | Coffee maker test 4 | |
| 5 | `test_compute_costs_root_values_match_expected` | Coffee maker test 5 | $41,205.00 |
| 6 | `test_compute_costs_pv_module_values_match_expected` | Coffee maker test 6 | PV Module[20] = $14,980.00 |
| 7 | `test_compute_costs_invalid_path_raises` | Coffee maker test 7 | |
| 8 | `test_write_component_costs_json` | **New** | Call `write_component_costs_json()` with `tmp_path`, verify structure and values |
| 9 | `test_write_design_params_json` | **New** | Call `extract_design_params()` + `write_design_params_json()` with `tmp_path`, verify 11 keys and values |
| 10 | `test_verify_system_outputs_passes` | **New** | Call `verify_system_outputs()`, assert passes — validates LCOE = $288.68/MWh |

**Test 8 and 9 details:** These tests call the JSON writer functions directly with pytest's `tmp_path` fixture, avoiding file side effects in the model directory. They load the model once (via `compute_costs()` for test 8, via `SysideAdapter` for test 9), generate JSON to `tmp_path`, and verify contents.

**Test 10 detail:** Calls `verify_system_outputs()` with extracted params and the `expected_system_outputs.csv` path. Asserts the function returns `(True, [])`. This provides automated validation of all 6 system-level outputs.

**Expected paths** (13 total, excluding allocation per coffee maker pattern):
```python
{
    "solar_battery_plant",
    "solar_battery_plant.solar_array",
    "solar_battery_plant.solar_array.pv_module",
    "solar_battery_plant.solar_array.inverter",
    "solar_battery_plant.solar_array.array_bos",
    "solar_battery_plant.battery_system",
    "solar_battery_plant.battery_system.battery_pack",
    "solar_battery_plant.battery_system.hybrid_inverter",
    "solar_battery_plant.battery_system.battery_bos",
    "solar_battery_plant.site_infra",
    "solar_battery_plant.site_infra.racking",
    "solar_battery_plant.site_infra.electrical_panel",
    "solar_battery_plant.site_infra.permitting",
}
```

### Generated Output Files

These files are written to `models/tests/solar_battery/` alongside the script:

| File | Generated By | Contents |
|------|-------------|----------|
| `actual_output.csv` | `write_csv()` | 14-column CSV, 14 data rows |
| `component_costs.json` | `write_component_costs_json()` | Total CAPEX + 3 subsystem breakdowns |
| `design_params.json` | `write_design_params_json()` | 11 system-level parameters |

## Potential Risks

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Solar battery SysML model has AST differences from coffee maker | Low | Medium | `validate_ast.py` already confirms the model is traversable with the same patterns |
| `extract_design_params()` misses an attribute due to AST structure | Low | Low | Validate all 11 expected keys are present; raise `ValueError` if any missing |
| JSON format doesn't match what Item 4 codegen expects | Medium | Low | JSON uses simple field names; Item 4 can remap. Values are the contract, not names. |
| `verify_system_outputs()` formula drift from SysML model | Low | Medium | Formula is copied from library.sysml CalcDefs with comments citing source lines |

## Integration Strategy

- This item produces **data files** consumed by Items 4-5
- `compute_costs()` API matches the coffee maker's — same interface for the visualization pipeline
- JSON files are standalone artifacts; no runtime dependency on this script by TEAx
- Coffee maker tests remain untouched (no shared code modified)
- `verify_system_outputs()` serves as a bridge validation: proves the entry point data can produce correct LCOE before Items 4-5 wire it through codegen/TEAx

## Validation Approach

### Automated

1. `uv run python models/tests/solar_battery/generate_costs.py` — CSV match + system output verification
2. `uv run python -m pytest models/tests/solar_battery/test_generate_costs.py -v` — 10 tests
3. `uv run python -m pytest models/tests/coffee_maker/test_generate_costs.py -v` — regression check

### Automated System-Level Verification (via `verify_system_outputs()`)

| Calc | Output | Expected | Formula |
|------|--------|----------|---------|
| EnergyProductionCalc | annual_energy_mwh | 11.14272 | 8760 * 0.008 * 1.0 * 0.159 |
| AnnualizedOMCalc | annual_om_cost | 160.00 | 20.0 * 8.0 |
| AnnualizedFuelCalc | annual_fuel_cost | 0.00 | 0.0 * 0.0 |
| AnnualizedFinancialCalc | capital_recovery_factor | 0.070952 | r*(1+r)^n / ((1+r)^n - 1) |
| AnnualizedFinancialCalc | annualized_capital_cost | 2923.60 | 0.070952 * 41205.00 |
| LCOECalc | lcoe_per_mwh | 288.68 | (2923.60 + (160+0) * 1.0245^25) / 11.14272 |

---

**Next Step:** After approval -> `/_my_implement`
