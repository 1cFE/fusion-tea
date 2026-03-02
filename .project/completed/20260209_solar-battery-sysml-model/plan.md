# Implementation Plan: Solar+Battery SysML Model

**Status:** Complete
**Created:** 2026-02-01 16:32 UTC
**Last Updated:** 2026-02-01 16:32 UTC

## Source Documents
- **Spec:** `.project/active/solar-battery-sysml-model/spec.md`
- **Design:** `.project/active/solar-battery-sysml-model/design.md` — See here for component details, CalcDef formulas, PartDef patterns, CAS mappings, CSV schemas

## Implementation Strategy

**Phasing Rationale:**
The plan builds incrementally from CalcDefs → PartDefs → design instance → expected outputs → validation script. Each phase produces a compilable artifact that can be verified independently. The two novel elements (foundation `Costing` import and `**` exponentiation) are tested in Phase 1 before any dependent work begins. Expected outputs (Phase 4) are computed after the model is final but before the validation script (Phase 5), so the script has verification targets to compare against.

**Overall Validation Approach:**
- Every SysML phase ends with `uv run syside check models/tests/solar_battery/` → exit 0
- Phase 4 produces the hand-calculated verification targets
- Phase 5 provides automated structural validation
- Coffee maker regression check runs at the end

---

## Phase 1: Foundation Import + CalcDefs + Compilation Gate

### Goal
Create `library.sysml` with package declaration, foundation import, and all 15 CalcDefs. Validates that `Costing::*` import works in a test model and that `**` exponentiation compiles in the CRF and LCOE formulas. This is the highest-risk phase — if either novel element fails, we find out before investing in PartDefs and design wiring.

### Test Stencil (Compile Check)
```bash
# Run after writing CalcDefs — this IS the test for Phase 1
uv run syside check models/tests/solar_battery/

# Expected: exit 0, no errors (warnings acceptable)
# If ** fails: decompose AnnualizedFinancialCalc and LCOECalc into
#   intermediate out attributes to avoid complex sub-expressions
```

### Changes Required

**See `design.md` for:**
- CalcDef formulas and signatures → `design.md#section-1-component-cost-calcdefs-9-defs`
- System-level CalcDef formulas → `design.md#section-3-system-level-calcdefs-5-defs`
- AllocationCostCalc duplication rationale → `design.md#section-2-allocationcostcalc-1-def`
- Package imports → `design.md#1-librarysysml--package-solarbatterylibrary`

**Specific file changes:**

#### 1. `models/tests/solar_battery/library.sysml` (NEW — partial, ~250 lines)
- [x] Create directory: `mkdir -p models/tests/solar_battery`
- [x] Create file with package declaration and imports:
  ```sysml
  package SolarBatteryLibrary {
      private import ScalarValues::Real;
      private import ScalarValues::Integer;
      private import NumericalFunctions::sum;
      private import Costing::*;
      ...
  }
  ```
- [x] Write 9 component cost CalcDefs (see design.md table for inputs/formulas):
  - PVModuleCostCalc, InverterCostCalc, ArrayBOSCostCalc
  - BatteryPackCostCalc, HybridInverterCostCalc, BatteryBOSCostCalc
  - RackingCostCalc, ElectricalPanelCostCalc, PermittingCostCalc
- [x] Write AllocationCostCalc (duplicate from coffee maker library.sysml:195–220)
- [x] Write 5 system-level CalcDefs (exact code in design.md):
  - EnergyProductionCalc, AnnualizedOMCalc, AnnualizedFuelCalc
  - AnnualizedFinancialCalc (with `**` for CRF)
  - LCOECalc (with `**` for inflation escalation)

**CalcDef default parameter guidance:**
Choose defaults so that design-bound values produce costs in the sanity range. Approximate unit cost targets (before fab/install factors):
- PV Module: ~$428 material → with 1.75x factor → ~$750 total per unit
- String Inverter: ~$571 material → with 1.75x factor → ~$1000 total
- Battery Pack: ~$857 material → with 1.75x factor → ~$1500 total
- (See design.md subsystem target table for full breakdown)

### Validation

**Automated:**
- [x] `uv run syside check models/tests/solar_battery/ --include models/library/foundation/` → exit 0

**Manual:**
- [x] Verify `**` appears in AnnualizedFinancialCalc and LCOECalc output formulas
- [x] Verify `private import Costing::*;` is present (not a local interface)
- [x] Count: 9 component + 1 allocation + 5 system = 15 CalcDefs total

**What We Know Works After This Phase:**
- Foundation `Costing` package imports into a test model without issues
- `**` exponentiation compiles in CRF and LCOE formulas
- All 15 CalcDef formulas are syntactically valid SysML v2

---

## Phase 2: PartDefs + Assembly Hierarchy

### Goal
Add all 13 PartDefs (9 leaf + 3 assembly + 1 top-level) to `library.sysml`. Each leaf specializes `'Costed Component'` from the foundation package, assigns `cas_category`, and embeds a `cost_model` CalcUsage. Assemblies use `sum()` for arrayed part rollup. This validates the full Pattern A with the production interface.

### Test Stencil (Compile Check)
```bash
# Full library must compile with CalcDefs + PartDefs
uv run syside check models/tests/solar_battery/

# Expected: exit 0
# Watch for: cas_category binding errors, sum() type issues,
#   PermittingCostCalc soft-cost pattern with raw_material_cost = 0.0
```

### Changes Required

**See `design.md` for:**
- Leaf PartDef pattern → `design.md#section-4-leaf-partdefs-9-defs`
- PermittingCostCalc special case → `design.md#permittingcostcalc-special-case`
- Assembly pattern with sum() → `design.md#section-5-assembly-partdefs-3-defs--1-top-level`
- CAS category assignments → `design.md#design-decision-cas-category-assignments`
- Site Infrastructure idiot_index note → `design.md#design-note--idiot_index-on-site-infrastructure`

**Specific file changes:**

#### 1. `models/tests/solar_battery/library.sysml` (MODIFY — add ~350 lines)
- [x] Add 9 leaf PartDefs, each following the pattern in design.md:
  - `'PV Module'` (CAS220101), `'String Inverter'` (CAS220107), `'Array BOS'` (CAS24)
  - `'Battery Pack'` (CAS27), `'Hybrid Inverter'` (CAS220107), `'Battery BOS'` (CAS2207)
  - `'Racking & Mounting'` (CAS220105), `'Electrical Panel'` (CAS24)
  - `'Permitting & Interconnect'` (CAS10) — soft cost, material/fab/install = 0
- [x] Each leaf: `:> 'Costed Component'`, `cas_category` binding, design params, embedded `cost_model`, `:>>` redefinitions
- [x] Add 3 assembly PartDefs:
  - `'Solar Array'` (CAS22) — with allocation_model, `sum()` on pv_module[] and inverter[]
  - `'Battery System'` (CAS25) — `sum()` on battery_pack[], no allocation
  - `'Site Infrastructure'` (CAS21) — singleton children only, no allocation
- [x] Add top-level `'Solar Battery Plant'` (CAS20) — aggregates 3 assemblies

### Validation

**Automated:**
- [x] `uv run syside check models/tests/solar_battery/ --include models/library/foundation/` → exit 0

**Manual:**
- [x] Count: 9 leaf + 3 assembly + 1 top-level = 13 PartDefs
- [x] Every PartDef has `:>> cas_category = CASCategory::...`
- [x] Every leaf has `calc cost_model : ...` with `:>>` redefinitions
- [x] Assemblies use `sum()` for arrayed children, `+` for singletons
- [x] Solar Array has `allocation_model : AllocationCostCalc`
- [x] Permitting has `raw_material_cost = 0.0`, `idiot_index = 0.0`

**What We Know Works After This Phase:**
- Full library compiles with foundation `'Costed Component'` + `cas_category`
- Nested cost model pattern works with production interface
- `sum()` aggregation works on arrayed parts with foundation interface
- Soft-cost pattern (Permitting) compiles without division-by-zero

---

## Phase 3: Design Instance + System-Level CalcUsages

### Goal
Create `design.sysml` with a concrete plant instance, parameter bindings for all leaf parts, multiplicity declarations, and the 5 system-level CalcUsages wired to each other via dot notation. This is the critical phase for downstream pipeline items — the inter-calc wiring is what Item 2 (codegen spike) tests.

### Test Stencil (Compile Check)
```bash
# Full model (library + design) must compile
uv run syside check models/tests/solar_battery/

# Expected: exit 0
# Watch for: inter-calc dot notation binding errors,
#   capital_cost reference from plant rollup into annualized_financial
```

### Changes Required

**See `design.md` for:**
- Full design.sysml structure → `design.md#2-designsysml--package-solarbatterydesign`
- Parameter values → `design.md` (FR-12 values in design code block)
- Inter-calc wiring key points → `design.md#key-design-points`
- p_net_kw derived from p_net_mw → `design.md` (line 391)

**Specific file changes:**

#### 1. `models/tests/solar_battery/design.sysml` (NEW — ~120 lines)
- [x] Package declaration with `private import SolarBatteryLibrary::*;`
- [x] Root instance: `part solar_battery_plant : 'Solar Battery Plant' { ... }`
- [x] Solar Array redefines with parameter bindings:
  - pv_module: wattage=400.0, efficiency=0.21
  - inverter: power_rating=2000.0
  - array_bos: string_count=4.0, panel_count=20.0
- [x] Battery System redefines with parameter bindings:
  - battery_pack: capacity_kwh=5.0, chemistry_factor=1.0
  - hybrid_inverter: power_rating=10000.0
  - battery_bos: pack_count=8.0
- [x] Site Infrastructure redefines with parameter bindings:
  - racking: panel_count=20.0, tilt_angle=30.0
  - electrical_panel: circuit_count=4.0
  - permitting: system_capacity_kw=8.0
- [x] Operating/financial parameter attributes (p_net_mw, n_mod, plant_availability, etc.)
- [x] `attribute p_net_kw : Real = p_net_mw * 1000.0;` (derived, not independent)
- [x] 5 system-level CalcUsages at top level of root instance:
  - `calc energy_production : EnergyProductionCalc { ... }`
  - `calc annualized_om : AnnualizedOMCalc { ... }`
  - `calc annualized_fuel : AnnualizedFuelCalc { ... }`
  - `calc annualized_financial : AnnualizedFinancialCalc { in total_capex = capital_cost; ... }`
  - `calc lcoe : LCOECalc { in annualized_capital_cost = annualized_financial.annualized_capital_cost; ... }`

### Validation

**Automated:**
- [x] `uv run syside check models/tests/solar_battery/ --include models/library/foundation/` → exit 0

**Manual:**
- [x] 5 system-level CalcUsages are inside `solar_battery_plant`, not inside any PartDef
- [x] `lcoe` calc inputs reference outputs of other calcs via dot notation
- [x] `annualized_financial` wires `total_capex = capital_cost` (plant rollup)
- [x] All parameter values match FR-12 (p_net_mw=0.008, discount_rate=0.05, etc.)
- [x] Multiplicity: pv_module uses `module_count` (default 20), inverter uses `inverter_count` (default 4), battery_pack uses parameterized multiplicity (default 8)

**What We Know Works After This Phase:**
- Complete SysML model compiles end-to-end
- Inter-calc dependency chain works (lcoe ← financial, om, fuel, energy)
- `capital_cost` flows from assembly rollup into system-level financial calc
- Design parameter bindings reach leaf parts through redefines
- Model is ready for downstream items (codegen, generate_costs.py)

---

## Phase 4: Hand-Calculated Expected Outputs

### Goal
Compute exact expected values for all component costs and system-level calculations using the CalcDef formulas and design parameter values from Phases 1–3. Produce both `expected_output.csv` (component costs, 14-column schema) and `expected_system_outputs.csv` (system-level calcs, 6-column schema). These are the single verification targets for all downstream pipeline items.

### Test Stencil (Sanity Check)
```python
# Quick sanity check script (run mentally or in a scratch file)
# Phase 4 is hand calculation — the "test" is range verification

# Energy production
annual_energy = 8760 * 0.008 * 1 * 0.159  # ≈ 11,149 kWh → in range [10k, 12k] ✓

# CRF
r, n = 0.05, 25
crf = r * (1+r)**n / ((1+r)**n - 1)  # ≈ 0.07095

# O&M
annual_om = 20 * 8  # = 160 USD

# LCOE (simplified check)
# lcoe = (crf * CAPEX + (160 + 0) * (1.0245)**25) / 11149
# With CAPEX ~40k: (0.07095 * 40000 + 160 * 1.838) / 11149
#                 ≈ (2838 + 294) / 11149 ≈ $0.281/kWh → in range [0.15, 0.35] ✓
```

### Changes Required

**See `design.md` for:**
- CSV schema (14 columns) → `design.md#4-expected_outputcsv`
- Row order (pre-order traversal) → `design.md#4-expected_outputcsv`
- System outputs schema (6 columns) → `design.md` (expected_system_outputs.csv section)
- Target ranges → `spec.md` FR-21

**Specific file changes:**

#### 1. `models/tests/solar_battery/expected_output.csv` (NEW)
- [x] Write CSV header (14 columns matching coffee maker schema)
- [x] Hand-calculate each leaf part's unit costs from CalcDef formulas + design params + defaults
- [x] Apply multiplicity: total_cost = unit_cost × quantity
- [x] Aggregate assembly costs: sum children totals + allocation (Solar Array only)
- [x] Aggregate top-level: sum of 3 assemblies
- [x] Write 14 rows in pre-order (top → solar_array → leaves → allocation → battery → leaves → site → leaves)
- [x] Verify: Total CAPEX (row 1 total_cost) in $35k–$45k → $41,205

#### 2. `models/tests/solar_battery/expected_system_outputs.csv` (NEW)
- [x] Write CSV header: `calc_name,calc_def,output_name,output_value,unit,notes`
- [x] Compute: annual_energy_mwh = 8760 × 0.008 × 1 × 0.159 → 11.14272 MWh
- [x] Compute: annual_om_cost = 20 × 8 → 160.00
- [x] Compute: annual_fuel_cost = 0 × 0 → 0.00
- [x] Compute: capital_recovery_factor = 0.05 × (1.05)^25 / ((1.05)^25 - 1) → 0.070952
- [x] Compute: annualized_capital_cost = CRF × 41205 → 2923.60
- [x] Compute: lcoe_per_mwh → 288.68 USD/MWh
- [x] Verify: LCOE in $0.15–$0.35/kWh range → $0.289/kWh ✓

### Validation

**Automated:**
- [x] (None — static files verified via Python sanity script)

**Manual:**
- [x] Total CAPEX in $35k–$45k → $41,205
- [x] Annual energy in 10,000–12,000 kWh → 11,143 kWh
- [x] LCOE in $0.15–$0.35/kWh → $0.289/kWh
- [x] Each leaf: total_cost = material + fab + install (verified, no rounding errors)
- [x] Each assembly: total_cost = sum of children (+ allocation for Solar Array)
- [x] Top-level: total_cost = sum of 3 assemblies → $41,205
- [x] Cross-check: expected_system_outputs annualized_capital_cost uses CAPEX from expected_output.csv → CRF × $41,205

**What We Know Works After This Phase:**
- All expected values are computed and traceable to exact formulas
- Sanity ranges are met
- LCOE verification target exists for all downstream items
- Component cost breakdown available for Item 3 (generate_costs.py) validation

---

## Phase 5: AST Validation Script

### Goal
Create `validate_ast.py` that programmatically validates the model structure against FR-13 through FR-17. Discovers cost models, system-level calcs, multiplicity, inter-calc dependencies, and assembly rollups using syside AST traversal. This provides automated verification that the model matches its design intent.

### Test Stencil (Script Self-Validates)
```python
# validate_ast.py IS the test — it exits 0 on success, non-zero on failure
# Key assertions it makes:

# FR-13: Cost model discovery
assert len(cost_models) == 10  # 9 leaf cost_model + 1 allocation_model
assert len(system_calcs) == 5  # energy, om, fuel, financial, lcoe

# FR-14: Multiplicity
arrayed = [p for p in parts if p.is_array]
assert len(arrayed) == 3  # pv_module[20], inverter[4], battery_pack[8]

# FR-15: System calcs at design level
for calc in system_calcs:
    assert calc.owner_type == "PartUsage"  # not PartDefinition

# FR-16: Inter-calc dependencies
lcoe_inputs = get_input_bindings(lcoe_calc)
assert any("annualized_financial" in b for b in lcoe_inputs)

# FR-17: Assembly rollups
for asm in assemblies:
    assert not has_cost_model(asm)  # assemblies use sum(), not calc usages
```

### Changes Required

**See `design.md` for:**
- Validation functions and discovery strategy → `design.md#3-validate_astpy`
- Owner chain strategy for distinguishing system vs embedded calcs → `design.md#discovery-strategy-for-system-level-calcs`
- Validation check table → `design.md#validation-checks-mapping-to-fr-13-through-fr-17`

**Specific file changes:**

#### 1. `models/tests/solar_battery/validate_ast.py` (NEW — ~450 lines)
- [x] Duplicate and adapt dataclasses from coffee maker validate_ast.py:28–77
  - `CostModelInfo` — reused from coffee maker
  - `SystemCalcInfo` — NEW dataclass for system-level calcs
  - `PartInfo` — reused from coffee maker
  - `ValidationResult` — extended with `system_calcs` and `assembly_checks`
- [x] Duplicate and adapt `find_cost_models()` (coffee maker:83–137):
  - Discover `cost_model` and `allocation_model` CalculationUsages
  - Filter: owned by PartDefinition = embedded cost model
- [x] Add `find_system_level_calcs()` (NEW):
  - Discover CalculationUsages whose typings match system CalcDefs
  - Filter: owned by PartUsage (root instance) = system-level
  - Expected: 5 (energy, om, fuel, financial, lcoe)
- [x] Duplicate and adapt `find_part_usages_with_multiplicity()` (coffee maker:217–280):
  - Discover PartUsages, extract multiplicity via `_extract_multiplicity_bound()`
  - Extended to handle `FeatureReferenceExpression` for parameterized multiplicity
  - Expected arrayed: pv_module[20], inverter[4], battery_pack[8]
- [x] Add inter-calc dependency verification in `validate_all()`:
  - Find LCOECalc usage's input bindings via `_extract_input_bindings()`
  - Resolve FeatureChainExpression targets via `_resolve_feature_chain_target()`
  - Check that inputs reference outputs of other system calcs
  - Expected: at least 3 cross-calc references (found 4)
- [x] Add `verify_assembly_rollups()` (NEW):
  - For each assembly PartDef, confirm no `cost_model` CalculationUsage
  - Expected: 3 assemblies pass
- [x] Implement `validate_all()` entry point:
  - Run all checks, collect results
  - Print summary with pass/fail per check
  - Exit 0 if all pass, 1 if any fail
- [x] Implement `main()` with CLI (model path argument, --json flag)

### Validation

**Automated:**
- [x] `uv run python models/tests/solar_battery/validate_ast.py` → exit 0
- [x] All 5 checks pass:
  - 10 embedded cost calc usages found (9 leaf + 1 allocation)
  - 5 system-level CalcUsages found at design level
  - 3 arrayed parts with correct multiplicities (pv_module[20], inverter[4], battery_pack[8])
  - 4 inter-calc dependencies verified on LCOECalc
  - 3 assembly parts with sum() rollup (no cost_model)

**Manual:**
- [x] `uv run python models/tests/solar_battery/validate_ast.py --json` produces parseable output
- [x] Spot-check: system calcs are correctly classified (not counted as embedded cost models)

**Regression:**
- [x] `uv run syside check models/tests/coffee_maker/` → exit 0
- [x] `uv run python models/tests/coffee_maker/validate_ast.py` → pre-existing MR-007 issue (FeatureReferenceExpression multiplicity, not a regression)

**What We Know Works After This Phase:**
- Model structure is programmatically validated against all FR-13 through FR-17
- System-level calcs are confirmed at design level (visible to codegen)
- Inter-calc dependency chain is confirmed (Item 2 can proceed)
- Coffee maker is unaffected (no regressions)
- All acceptance criteria from spec are met

---

## Environment Setup

**See CLAUDE.md for full environment rules**

Key commands:
- `uv run syside check <path>` — SysML compilation
- `uv run python <script>` — Python execution
- All Python via `uv`, never bare `python`

---

## Risk Management

**See `design.md#potential-risks` for detailed risk analysis**

**Phase-Specific Mitigations:**
- **Phase 1**: If `**` fails to compile in complex expressions, decompose CRF into intermediate `out` attributes (e.g., `out attribute compound_factor : Real = (1.0 + discount_rate) ** plant_lifetime;` then use `compound_factor` in CRF formula)
- **Phase 2**: If `cas_category` binding fails with `sum()`, verify against `costing_import_test.sysml` pattern. The two features are independent (cas_category is just an attribute assignment, sum() operates on cost attributes)
- **Phase 3**: If inter-calc dot notation fails (e.g., `annualized_financial.annualized_capital_cost`), try explicit intermediate attributes as a workaround
- **Phase 4**: If costs don't land in sanity ranges, adjust CalcDef default cost factors. This is pure parameter tuning with no structural risk

## Implementation Notes

[TO BE FILLED DURING IMPLEMENTATION]

### Phase 1 Completion
**Completed:** 2026-02-01
**Actual Changes:**
- Created `models/tests/solar_battery/` directory
- Created `models/tests/solar_battery/library.sysml` (~360 lines) with:
  - Package `SolarBatteryLibrary` with `private import Costing::*;`
  - 9 component cost CalcDefs with default parameters tuned for $35k–$45k CAPEX range
  - 1 AllocationCostCalc (duplicated from coffee maker pattern)
  - 5 system-level CalcDefs (EnergyProductionCalc, AnnualizedOMCalc, AnnualizedFuelCalc, AnnualizedFinancialCalc, LCOECalc)
  - `**` exponentiation in AnnualizedFinancialCalc (CRF) and LCOECalc (inflation escalation)
**Issues:**
- Foundation import requires `--include models/library/foundation/` flag when running syside check. The solar_battery directory doesn't self-contain the Costing package, so the compilation command is: `uv run syside check models/tests/solar_battery/ --include models/library/foundation/`
**Deviations:**
- None. All 15 CalcDefs match the design exactly.

### Phase 2 Completion
**Completed:** 2026-02-01
**Actual Changes:**
- Modified `models/tests/solar_battery/library.sysml` — added ~400 lines with:
  - 9 leaf PartDefs (PV Module, String Inverter, Array BOS, Battery Pack, Hybrid Inverter, Battery BOS, Racking & Mounting, Electrical Panel, Permitting & Interconnect)
  - 3 assembly PartDefs (Solar Array with allocation_model, Battery System, Site Infrastructure)
  - 1 top-level PartDef (Solar Battery Plant)
  - All 13 PartDefs specialize `'Costed Component'` from foundation, assign `cas_category`, and use `:>>` redefinitions
  - Solar Array uses `sum()` on pv_module[] and inverter[] arrays
  - Battery System uses `sum()` on battery_pack[] array
  - Permitting uses soft-cost pattern (material/fab/install = 0, idiot_index = 0)
**Issues:**
- None. All patterns compiled on first attempt.
**Deviations:**
- None. All 13 PartDefs match the design exactly.

### Phase 3 Completion
**Completed:** 2026-02-01
**Actual Changes:**
- Created `models/tests/solar_battery/design.sysml` (~100 lines) with:
  - Package `SolarBatteryDesign` importing `SolarBatteryLibrary::*` and `ScalarValues::Real`
  - Root instance `solar_battery_plant : 'Solar Battery Plant'`
  - Parameter bindings for all 3 subsystems via `part redefines` + `:>>`
  - 10 operating/financial attributes at plant level (p_net_mw, discount_rate, etc.)
  - `p_net_kw` derived from `p_net_mw * 1000.0`
  - 5 system-level CalcUsages with inter-calc dot-notation wiring
  - `annualized_financial.total_capex = capital_cost` linking component rollup to LCOE
**Issues:**
- `ScalarValues::Real` was not visible in design.sysml because the library's import is `private`. Added `private import ScalarValues::Real;` to the design package. This is expected — private imports don't re-export.
**Deviations:**
- Added `private import ScalarValues::Real;` to design.sysml (not in original design.md code block). Required for `Real` type on operating parameter attributes.

### Phase 4 Completion
**Completed:** 2026-02-01
**Actual Changes:**
- Created `models/tests/solar_battery/expected_output.csv` (14 rows, 14-column schema matching coffee maker)
  - 9 leaf parts with exact unit and total costs
  - 1 allocation row (Solar Array, $120)
  - 3 assembly rows with aggregated totals
  - 1 top-level row: CAPEX = $41,205
- Created `models/tests/solar_battery/expected_system_outputs.csv` (6 rows, 6-column schema)
  - Annual energy: 11.14272 MWh (11,143 kWh)
  - Annual O&M: $160, Fuel: $0
  - CRF: 0.070952, Annualized capital: $2,923.60
  - LCOE: 288.68 USD/MWh ($0.289/kWh)
- Verified all leaf costs: material + fab + install = total (no rounding errors)
- Verified all assembly rollups: children sum = assembly total
- Verified all sanity ranges: CAPEX $41k, energy 11.1k kWh, LCOE $0.289/kWh
**Issues:**
- None.
**Deviations:**
- None.

### Phase 5 Completion
**Completed:** 2026-02-01
**Actual Changes:**
- Created `models/tests/solar_battery/validate_ast.py` (~450 lines) with:
  - `CostModelInfo`, `SystemCalcInfo`, `PartInfo`, `ValidationResult` dataclasses
  - `find_cost_models()` — discovers 9 leaf + 1 allocation embedded cost models
  - `find_system_level_calcs()` — discovers 5 system-level CalcUsages at design level
  - `find_part_usages_with_multiplicity()` — detects 3 arrayed parts
  - `verify_assembly_rollups()` — confirms 3 assemblies use sum() not cost_model
  - `validate_all()` — runs all 5 FR checks, returns pass/fail
  - `main()` with CLI (model path argument, --json flag)
  - Loads both model dir and foundation dir for Costing package resolution
**Issues:**
- `_extract_multiplicity_bound()` needed extension for `FeatureReferenceExpression` (parameterized multiplicity like `[module_count]`). Resolved by following the `referent` to get the attribute's default `LiteralInteger` value.
- `_resolve_feature_chain_target()` needed `str()` conversion on `qualified_name` — syside returns a non-string Name object where Python `in` operator doesn't work directly.
- Coffee maker's `validate_ast.py` has a pre-existing MR-007 failure (same `FeatureReferenceExpression` multiplicity issue). Not a regression — the coffee maker validator was written before this pattern was understood.
**Deviations:**
- Used `SystemCalcInfo` dataclass instead of adding `is_system_level` field to `CostModelInfo` — cleaner separation of concerns.
- Script is ~450 lines (plan estimated ~350) due to additional helper functions for FeatureChainExpression resolution and FeatureReferenceExpression multiplicity handling.

---

**Status**: Draft → In Progress → Complete
