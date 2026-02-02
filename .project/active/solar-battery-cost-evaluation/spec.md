# Spec: Solar+Battery Cost Evaluation & Entry Point Generation

**Status:** Complete
**Owner:** Reid Westwood
**Created:** 2026-02-01 23:56 UTC
**Complexity:** MEDIUM
**Branch:** visualization
**Epic:** End-to-End Pipeline De-Risking (Item 3)

---

## Business Goals

### Why This Matters

This is the bridge between the completed SysML model (Item 1) and the downstream codegen/TEAx pipeline (Items 4-5). Without cost evaluation and JSON entry points, the pipeline has no data to consume. The solar+battery model has been validated structurally (AST traversal, `syside check`), but its cost calculations have never been **evaluated** — we need to prove the numbers come out right before wiring them into TEAx.

### Success Criteria

- [ ] Component costs evaluated from SysML model match hand-calculated expected values
- [ ] JSON entry points generated in TEAx-compatible format for downstream consumption
- [ ] LCOE can be independently verified from the component cost outputs

### Priority

P0 — blocks Items 4 (Codegen Pipeline Run) and 5 (TEAx End-to-End Execution).

---

## Problem Statement

### Current State

- The solar+battery SysML model exists and compiles (`models/tests/solar_battery/`)
- `expected_output.csv` and `expected_system_outputs.csv` contain hand-calculated target values
- The coffee maker's `generate_costs.py` (1631 lines) proves the evaluation pattern works
- No evaluation script exists for the solar+battery model
- No JSON entry point files exist for TEAx consumption

### Desired Outcome

A `generate_costs.py` script that evaluates all component costs from the solar+battery SysML model, produces a validated CSV, and generates two JSON entry point files (`component_costs.json` and `design_params.json`) ready for TEAx pipeline consumption in Items 4-5.

---

## Scope

### In Scope

1. **`generate_costs.py`** — Adapted from coffee maker pattern
2. **`component_costs.json`** — CAPEX breakdown as TEAx entry point
3. **`design_params.json`** — System-level parameters as TEAx entry point
4. **`test_generate_costs.py`** — Validation tests
5. **`actual_output.csv`** — Generated output for comparison

### Out of Scope

- Shared library extraction from coffee maker's generate_costs.py (deferred)
- Pydantic schema class definitions for TEAx (Item 4 — codegen generates these)
- Pipeline YAML creation (Item 4)
- Changes to agentic-mbse
- Changes to the SysML model (Item 1 is complete)
- TEAx execution (Item 5)

### Edge Cases & Considerations

- **Permitting soft cost**: `PermittingCostCalc` outputs `material_cost = 0.0` and `idiot_index = 0.0` — the evaluator MUST NOT divide by zero or require positive material cost for this leaf
- **Assembly idiot_index with zero-material children**: Site Infrastructure includes Permitting (zero material), so `raw_material_cost` for the assembly is only from Racking + Electrical Panel. The idiot_index ($3995.50 / $1426.00 = 2.80) will be higher than typical — this is correct behavior
- **Allocation cost**: Only Solar Array has an `allocation_model`; Battery System and Site Infrastructure do not
- **Multiplicity via parameterized attributes**: Solar Array uses `module_count` (Integer, default 20) and `inverter_count` (Integer, default 4); Battery System uses `pack_count` (Integer, default 8). The evaluator must handle `cached_lower_bound` fallback for parameterized multiplicities (same pattern as coffee maker)

---

## Requirements

### Functional Requirements

> Requirements below are from the epic's Item 3 specification and user request unless marked [INFERRED] or [FROM INVESTIGATION].

**FR-1: Cost Evaluation Script**

The `generate_costs.py` script MUST:
- Load the solar+battery SysML model via `SysideAdapter.load_model()`
- Extract all 15 calc definitions (9 component + 1 allocation + 5 system-level)
- Map 9 leaf part definitions to their `cost_model` calc usages
- Extract the design hierarchy rooted at `solar_battery_plant`
- Resolve parameter bindings through `:>>` redefinition chains from `design.sysml`
- Evaluate all 9 component cost calcs with correct input parameters
- Handle multiplicity: PV Module[20], String Inverter[4], Battery Pack[8]
- Aggregate assembly costs (Solar Array, Battery System, Site Infrastructure, top-level)
- Evaluate Solar Array's `allocation_model` (AllocationCostCalc with child_count=25, total_child_mass=50)
- Output `actual_output.csv` in the 14-column schema

**FR-2: CSV Output Format**

The `actual_output.csv` MUST use the same 14-column schema as the coffee maker:
```
path, part_def, quantity, unit_material_cost, unit_fab_cost, unit_install_cost, unit_total_cost,
total_material_cost, total_fab_cost, total_install_cost, total_cost, idiot_index, cost_type, calc_def
```

Row order MUST be pre-order traversal: assembly, then children, then allocation.

**FR-3: CSV Validation**

The script MUST compare `actual_output.csv` against `expected_output.csv` within tolerance (0.011 for rounding). Expected row count: 15 (1 top-level + 3 assemblies + 9 leaves + 1 allocation + 1 Site Infra allocation... actually: 1 top + 3 assemblies + 9 leaves + 1 allocation = 14 rows). Per the expected CSV: 15 rows (header + 14 data rows including 1 allocation for Solar Array only).

**FR-4: Component Costs JSON**

`component_costs.json` MUST contain:
- `total_capex`: Total plant capital cost ($41,205.00)
- Subsystem-level breakdown with `total_cost`, `material_cost`, `fab_cost`, `install_cost` for each of: `solar_array`, `battery_system`, `site_infra`
- [INFERRED] Format SHOULD be a flat or shallow dict structure compatible with Pydantic `BaseModel` instantiation (no nested objects deeper than one level)

**FR-5: Design Parameters JSON**

`design_params.json` MUST contain all system-level parameters from `design.sysml`:

| Parameter | Value | Source |
|-----------|-------|--------|
| `p_net_mw` | 0.008 | design.sysml line 53 |
| `n_mod` | 1.0 | design.sysml line 54 |
| `plant_availability` | 0.159 | design.sysml line 55 |
| `plant_lifetime` | 25.0 | design.sysml line 56 |
| `yearly_inflation` | 0.0245 | design.sysml line 57 |
| `discount_rate` | 0.05 | design.sysml line 58 |
| `om_rate_per_kw_year` | 20.0 | design.sysml line 59 |
| `p_net_kw` | 8.0 | Derived: p_net_mw * 1000 |
| `fuel_unit_cost` | 0.0 | design.sysml line 61 |
| `fuel_consumption` | 0.0 | design.sysml line 62 |
| `total_capex` | 41205.00 | From component cost rollup |

[INFERRED] The JSON SHOULD use simple field names (not fully-qualified SysML names) since the exact codegen naming will be determined in Item 4. Item 4 can remap if needed.

**FR-6: Public API**

`compute_costs()` MUST return a dict mapping qualified paths to cost attribute dicts, following the same interface as the coffee maker:
```python
{
    "solar_battery_plant": {
        "capital_cost": 41205.00,
        "raw_material_cost": 22716.00,
        "fabrication_cost": 10179.00,
        "installation_cost": 6786.00,
        "idiot_index": 1.81
    },
    "solar_battery_plant.solar_array": { ... },
    ...
}
```

**FR-7: Test Suite**

`test_generate_costs.py` MUST include tests for:
1. `compute_costs()` returns a dict
2. All expected paths present (12 parts: 1 root + 3 assemblies + 8 leaves... actually 1 root + 3 assemblies + 9 leaves = 13 paths, excluding allocation entries per coffee maker pattern)
3. All cost attributes present on each path
4. All values are numeric
5. Root CAPEX matches $41,205.00 (within tolerance)
6. Individual leaf costs match expected (at least one spot-check, e.g., PV Module)
7. `component_costs.json` is generated and contains `total_capex`
8. `design_params.json` is generated and contains all required parameters
9. Invalid model path raises `ValueError`

---

## Acceptance Criteria

### Core Functionality

- [ ] `uv run python models/tests/solar_battery/generate_costs.py` exits 0
- [ ] `actual_output.csv` matches `expected_output.csv` (15 data rows, all numeric fields within 0.011 tolerance)
- [ ] `component_costs.json` exists with `total_capex = 41205.00`
- [ ] `design_params.json` exists with all 11 parameters from FR-5
- [ ] CAPEX total is $41,205.00 (within sanity range $35k-$45k)

### Quality & Integration

- [ ] All tests pass: `uv run python -m pytest models/tests/solar_battery/test_generate_costs.py -v`
- [ ] Existing coffee maker tests still pass (no regressions)
- [ ] JSON files are valid JSON (parseable by `json.load()`)
- [ ] LCOE can be independently computed from JSON outputs: verify $288.68/MWh from `expected_system_outputs.csv` using `total_capex` + design params

### Verification Values (from expected_output.csv)

| Part | total_cost | Qty | Notes |
|------|-----------|-----|-------|
| Solar Battery Plant | $41,205.00 | 1 | Top-level rollup |
| Solar Array | $21,204.00 | 1 | Including $120 allocation |
| PV Module | $14,980.00 | 20 | $749.00 each |
| String Inverter | $4,004.00 | 4 | $1,001.00 each |
| Array BOS | $2,100.00 | 1 | |
| Solar Array Allocation | $120.00 | 1 | AllocationCostCalc |
| Battery System | $16,005.50 | 1 | No allocation |
| Battery Pack | $12,005.00 | 8 | $1,500.625 each |
| Hybrid Inverter | $2,999.50 | 1 | |
| Battery BOS | $1,001.00 | 1 | |
| Site Infrastructure | $3,995.50 | 1 | No allocation |
| Racking & Mounting | $1,995.00 | 1 | |
| Electrical Panel | $500.50 | 1 | |
| Permitting & Interconnect | $1,500.00 | 1 | Soft cost (material=0) |

### System-Level Verification (from expected_system_outputs.csv)

| Calc | Output | Expected Value |
|------|--------|---------------|
| EnergyProductionCalc | annual_energy_mwh | 11.14272 |
| AnnualizedOMCalc | annual_om_cost | $160.00 |
| AnnualizedFuelCalc | annual_fuel_cost | $0.00 |
| AnnualizedFinancialCalc | capital_recovery_factor | 0.070952 |
| AnnualizedFinancialCalc | annualized_capital_cost | $2,923.60 |
| LCOECalc | lcoe_per_mwh | $288.68 |

---

## Implementation Notes

### Adaptation from Coffee Maker

The coffee maker's `generate_costs.py` is ~1631 lines and handles the same structural patterns. Key changes needed:

1. `ROOT_PART_NAME`: `"coffee_maker"` -> `"solar_battery_plant"`
2. Hierarchy is deeper (3 levels vs 2) but uses the same traversal
3. More leaf types (9 vs 5) but all follow the same cost_model pattern
4. Multiplicity values differ but extraction logic is identical
5. Only Solar Array has allocation (vs both assemblies in coffee maker... actually coffee maker has allocation on both Brewing System and Housing — need to verify)
6. **New**: JSON generation functions added to `main()` and as utility functions

### JSON Format Decisions

**`component_costs.json`** (proposed structure):
```json
{
    "total_capex": 41205.00,
    "solar_array": {
        "total_cost": 21204.00,
        "material_cost": 12144.00,
        "fab_cost": 5421.60,
        "install_cost": 3614.40
    },
    "battery_system": {
        "total_cost": 16005.50,
        "material_cost": 9146.00,
        "fab_cost": 4115.70,
        "install_cost": 2743.80
    },
    "site_infra": {
        "total_cost": 3995.50,
        "material_cost": 1426.00,
        "fab_cost": 641.70,
        "install_cost": 427.80
    }
}
```

**`design_params.json`** (proposed structure):
```json
{
    "p_net_mw": 0.008,
    "n_mod": 1.0,
    "plant_availability": 0.159,
    "plant_lifetime": 25.0,
    "yearly_inflation": 0.0245,
    "discount_rate": 0.05,
    "om_rate_per_kw_year": 20.0,
    "p_net_kw": 8.0,
    "fuel_unit_cost": 0.0,
    "fuel_consumption": 0.0,
    "total_capex": 41205.00
}
```

### TEAx Compatibility

These JSON files will be consumed as `EntryPoint` artifacts in Item 5. Item 4 (codegen) will generate Pydantic schema classes and pipeline YAML that reference these files. The exact field naming may be adjusted in Item 4 if codegen uses fully-qualified names — but the values must remain identical.

---

## Related Artifacts

- **Epic:** `.project/backlog/epic-end-to-end-pipeline-derisking.md` (Item 3)
- **SysML Model:** `models/tests/solar_battery/library.sysml`, `design.sysml`
- **Expected Values:** `models/tests/solar_battery/expected_output.csv`, `expected_system_outputs.csv`
- **Reference Implementation:** `models/tests/coffee_maker/generate_costs.py`
- **Foundation:** `models/library/foundation/costing.sysml` ('Costed Component' interface)
- **Design:** `.project/active/solar-battery-cost-evaluation/design.md` (to be created)

---

**Next Steps:** After approval, proceed to `/_my_design`
