# Design: Solar+Battery SysML Model

**Status:** Draft
**Owner:** Reid Westwood
**Created:** 2026-01-31 23:37 UTC
**Branch:** visualization
**Spec:** `.project/active/solar-battery-sysml-model/spec.md`

## Overview

Design the SysML model structure, calc defs, part hierarchy, and validation tooling for a solar+battery plant that exercises the full LCOE pipeline using PyFECONS-aligned calculations. Follows the coffee maker's proven Pattern A (nested cost models) and extends it with system-level calcs.

## Related Artifacts

- **Spec:** `.project/active/solar-battery-sysml-model/spec.md`
- **Epic:** `.project/backlog/epic-end-to-end-pipeline-derisking.md` (Item 1)
- **Reference Pattern:** `models/tests/coffee_maker/` (library.sysml, design.sysml)
- **Foundation Package:** `models/library/foundation/costing.sysml`
- **Research:** `modeling_pm/research/20260126-lcoe-visibility-requirements-analysis.md`

---

## Research Findings

### Coffee Maker Pattern Analysis

The coffee maker model at `models/tests/coffee_maker/` establishes the proven patterns:

**library.sysml** (502 lines):
- Defines its own local `'Costed Component'` (lines 19–37) — solar model will import from foundation instead
- 7 component CalcDefs (lines 43–220), each with `in` params, `out` formulas for material/fab/install/total/idiot_index
- 7 leaf PartDefs (lines 226–378), each embedding `calc cost_model : CalcDef { in X = attr; }` with `:>>` redefinitions
- 2 assembly PartDefs + 1 top-level (lines 384–501), using `sum()` for arrayed parts and direct `+` for singletons
- 1 AllocationCostCalc (lines 195–220) used in `'Brewing System'` assembly

**design.sysml** (56 lines):
- Single root instance: `part coffee_maker : 'Coffee Maker' { ... }`
- Parameter binding via `part redefines X : Type { :>> child.param = value; }`
- No system-level CalcUsages (coffee maker has no LCOE)

**validate_ast.py** (555 lines):
- Uses `SysideAdapter.load_model()` and `elements_of_type()` to discover calc usages and part usages
- Key functions: `find_cost_models()` (line 83), `find_part_usages_with_multiplicity()` (line 217), `validate_cost_patterns()` (line 351)
- Data structures: `CostModelInfo`, `PartInfo`, `ValidationResult` (lines 28–77)
- Tests multiplicity via `_extract_multiplicity_bound()` examining `upper_bound` on MultiplicityRange

**generate_costs.py** (1630 lines):
- Pipeline: extract calc defs → map part defs → extract design hierarchy → compute costs → write CSV
- Expression evaluator (line 992–1058): supports `+`, `-`, `*`, `/` but **NOT** `**` or `^`
- This is Item 3's scope — the solar model just needs to compile and be AST-traversable

**expected_output.csv** (14-column schema):
```
path, part_def, quantity, unit_material_cost, unit_fab_cost, unit_install_cost, unit_total_cost,
total_material_cost, total_fab_cost, total_install_cost, total_cost, idiot_index, cost_type, calc_def
```
- Assemblies: unit columns empty, totals from summation
- Allocations: cost_type = "allocation"
- Leaf parts: cost_type = "leaf", calc_def = CalcDef name

### Foundation Costing Package

**`models/library/foundation/costing.sysml`** (124 lines):
- `CASCategory` enum with 30+ values (lines 21–82): CAS10–90 (Level 1), CAS21–29 (Level 2), CAS220101–220119 (Level 3), CAS2202–2207 (Level 3 auxiliary)
- `'Costed Component'` abstract part def (lines 88–123): adds `cas_category : CASCategory` beyond the coffee maker's interface, plus same 5 cost attributes
- Import pattern proven in `models/tests/costing_import_test.sysml` (line 14): `private import Costing::*;`

### Exponentiation Support in SysML v2

**Validated**: syside parses `**` and `^` operators correctly. A test file with the CRF formula `r * (1.0 + r) ** n / ((1.0 + r) ** n - 1.0)` compiles without errors. Both `**` and `^` are standard KerML operators (right-associative, highest binary precedence).

**Evaluator gap**: The coffee maker's `generate_costs.py` expression evaluator does not support `**`/`^`. This is an Item 3 concern — the solar `generate_costs.py` will need to add this operator. For Item 1, the model just needs to compile.

### PyFECONS Formula Reference

From `/home/reid/PyFECONS/pyfecons/costing/calculations/`:

| Calc | PyFECONS File | Formula |
|------|---------------|---------|
| Energy | lcoe.py:24 (denominator) | `8760 * p_net * n_mod * plant_availability` |
| O&M (C700000) | cas70_annualized_om.py:10 | `om_rate * p_net_kw` (PyFECONS uses 60 $/kW-yr hardcoded) |
| Fuel (C800000) | cas80_annualized_fuel.py:14 | `fuel_unit_cost * fuel_consumption` (complex for fusion; 0 for solar) |
| Financial (C900000) | cas90_annualized_financial.py:14 | `CRF * total_capex` where CRF = `r*(1+r)^n / ((1+r)^n - 1)` |
| LCOE (C1000000) | lcoe.py:18-25 | `(C900000 + (C700000 + C800000) * (1+infl)^lifetime) / annual_energy` |

**Note**: PyFECONS uses `capital_recovery_factor = 0.09` as a pre-computed default. The epic specifies computing CRF from `discount_rate` and `plant_lifetime` — this is more general and correct for the solar model.

---

## Design Decision: CAS Category Assignments

The foundation `'Costed Component'` requires `cas_category` on every part. The solar model is a test model, not an actual fusion plant, so the CAS mappings are approximate analogs:

| Solar Part | CAS Category | Rationale |
|------------|-------------|-----------|
| PV Module | CAS220101 | Core energy-producing component (≈ First Wall/Blanket) |
| String Inverter | CAS220107 | Power conversion (≈ Power Supplies) |
| Array BOS | CAS24 | Electrical infrastructure (≈ Electric Plant Equipment) |
| Battery Pack | CAS27 | Energy storage material (≈ Special Materials) |
| Hybrid Inverter | CAS220107 | Power conversion (≈ Power Supplies) |
| Battery BOS | CAS2207 | Control systems (≈ Instrumentation and Control) |
| Racking & Mounting | CAS220105 | Structural support (≈ Primary Structure) |
| Electrical Panel | CAS24 | Electrical infrastructure (≈ Electric Plant Equipment) |
| Permitting & Interconnect | CAS10 | Pre-construction costs |
| Solar Array (assembly) | CAS22 | Reactor Plant Equipment analog |
| Battery System (assembly) | CAS25 | Miscellaneous Plant Equipment |
| Site Infrastructure (assembly) | CAS21 | Buildings and Structures |
| Solar Battery Plant (top) | CAS20 | Direct Costs aggregate |

These mappings are for the test model only. They enable CAS-based reporting without implying the solar model is a fusion plant.

---

## Proposed Design

### File Structure

```
models/tests/solar_battery/
├── library.sysml                # CalcDefs + PartDefs (~600 lines)
├── design.sysml                 # Concrete instance + system CalcUsages (~120 lines)
├── validate_ast.py              # AST validation (~350 lines)
├── expected_output.csv          # Hand-calculated component cost verification target
└── expected_system_outputs.csv  # Hand-calculated system-level calc verification target
```

### 1. library.sysml — Package `SolarBatteryLibrary`

**Imports:**
```sysml
package SolarBatteryLibrary {
    private import ScalarValues::Real;
    private import ScalarValues::Integer;
    private import NumericalFunctions::sum;
    private import Costing::*;
    ...
}
```

Key difference from coffee maker: imports `Costing::*` instead of defining a local interface.

**Section 1: Component Cost CalcDefs (9 defs)**

Each follows the coffee maker pattern: typed inputs, formula-based outputs. All produce `material_cost`, `fab_cost`, `install_cost`, `total_cost`, `idiot_index` — except PermittingCostCalc which is a soft cost.

| CalcDef | Key Inputs | Cost Formula Approach |
|---------|-----------|----------------------|
| PVModuleCostCalc | wattage, efficiency | material = wattage * cost_per_watt; fab = material * fab_factor; install = material * install_factor |
| InverterCostCalc | power_rating | material = power_rating * cost_per_watt; fab = material * fab_factor; install = material * install_factor |
| ArrayBOSCostCalc | string_count, panel_count | material = string_count * cost_per_string + panel_count * cost_per_panel_bos; fab/install via factors |
| BatteryPackCostCalc | capacity_kwh, chemistry_factor | material = capacity_kwh * cost_per_kwh * chemistry_factor; fab/install via factors |
| HybridInverterCostCalc | power_rating | material = power_rating * cost_per_watt; fab/install via factors |
| BatteryBOSCostCalc | pack_count | material = pack_count * cost_per_pack_bos; fab/install via factors |
| RackingCostCalc | panel_count, tilt_angle | material = panel_count * cost_per_panel_rack; fab/install via factors |
| ElectricalPanelCostCalc | circuit_count | material = base_cost + circuit_count * cost_per_circuit; fab/install via factors |
| PermittingCostCalc | system_capacity_kw | total_cost = system_capacity_kw * cost_per_kw (soft cost — no material/fab/install split) |

**Design note on PermittingCostCalc**: Since this is a soft cost, `material_cost = 0`, `fab_cost = 0`, `install_cost = 0`, `total_cost = system_capacity_kw * cost_per_kw`. The `idiot_index` would be division by zero if using `total_cost / material_cost`, so set `idiot_index = 0.0` (or 1.0 as a convention). This mirrors how permitting doesn't have a physical material basis.

**Specific parameter values**: The CalcDef `default :=` values should be chosen so that when combined with the design parameter bindings (FR-12), the resulting CAPEX lands in the $35k–$45k sanity range. Approximate target breakdown:

| Subsystem | Target Range | Leaf Composition |
|-----------|-------------|------------------|
| Solar Array | $18k–$22k | 20 PV modules (~$15k) + 4 inverters (~$4k) + BOS (~$2k) |
| Battery System | $14k–$18k | 8 battery packs (~$12k) + hybrid inverter (~$3k) + BOS (~$1k) |
| Site Infrastructure | $3k–$5k | Racking (~$2k) + panel (~$0.5k) + permitting (~$1.5k) |

Working backwards from these targets with the design quantities:
- PV Module: 20 × ~$750 = $15k → material ~$428/unit at cost factors
- Battery Pack: 8 × ~$1500 = $12k → material ~$857/unit at cost factors
- (Full parameter derivation to be done during implementation when computing expected_output.csv)

**Section 2: AllocationCostCalc (1 def)**

Duplicate the coffee maker's `AllocationCostCalc` pattern into `SolarBatteryLibrary` (source: coffee maker library.sysml:195–220). This is a copy, not a shared import — the coffee maker's calc lives in `CoffeeMakerLibrary` which is a separate package with its own local `'Costed Component'`. Inputs: `child_count`, `total_child_mass`. Outputs: `fastener_cost`, `seal_cost`, `wiring_cost`, `total_allocation`, `material_portion`.

**Justification for duplication**: Extracting AllocationCostCalc into a shared library would require the coffee maker to also import from the foundation Costing package (breaking its self-contained test nature). A shared allocation library is a reasonable future refactoring but out of scope for this item.

Decision: which assembly gets the allocation model? The coffee maker gives it to `'Brewing System'` only. For solar, use it on **Solar Array** (the largest subsystem with the most physical parts — PV modules with racking, combiner boxes, conduit). The other assemblies can get allocation too if needed, but one is sufficient for the pattern demonstration.

**Section 3: System-Level CalcDefs (5 defs)**

These are NEW — the coffee maker doesn't have them. They use `**` for exponentiation.

```sysml
calc def EnergyProductionCalc {
    in attribute p_net_mw : Real;
    in attribute n_mod : Real;
    in attribute plant_availability : Real;
    out attribute annual_energy_mwh : Real = 8760.0 * p_net_mw * n_mod * plant_availability;
}

calc def AnnualizedOMCalc {
    in attribute om_rate_per_kw_year : Real;
    in attribute p_net_kw : Real;
    out attribute annual_om_cost : Real = om_rate_per_kw_year * p_net_kw;
}

calc def AnnualizedFuelCalc {
    in attribute fuel_unit_cost : Real;
    in attribute fuel_consumption : Real;
    out attribute annual_fuel_cost : Real = fuel_unit_cost * fuel_consumption;
}

calc def AnnualizedFinancialCalc {
    in attribute total_capex : Real;
    in attribute discount_rate : Real;
    in attribute plant_lifetime : Real;
    out attribute capital_recovery_factor : Real =
        discount_rate * (1.0 + discount_rate) ** plant_lifetime
        / ((1.0 + discount_rate) ** plant_lifetime - 1.0);
    out attribute annualized_capital_cost : Real = capital_recovery_factor * total_capex;
}

calc def LCOECalc {
    in attribute annualized_capital_cost : Real;
    in attribute annual_om_cost : Real;
    in attribute annual_fuel_cost : Real;
    in attribute yearly_inflation : Real;
    in attribute plant_lifetime : Real;
    in attribute annual_energy_mwh : Real;
    out attribute lcoe_per_mwh : Real =
        (annualized_capital_cost + (annual_om_cost + annual_fuel_cost)
         * (1.0 + yearly_inflation) ** plant_lifetime)
        / annual_energy_mwh;
}
```

**Key design notes:**
- `EnergyProductionCalc` outputs MWh (not MW) — matches PyFECONS denominator
- `AnnualizedOMCalc` takes `p_net_kw` (not MW) — matches the epic's specification of `om_rate_per_kw_year * p_net_kw`
- `AnnualizedFinancialCalc` computes CRF inline rather than using PyFECONS's hardcoded 0.09 — more general
- `LCOECalc` takes all 5 inputs from other calcs plus `yearly_inflation` and `plant_lifetime` — matches PyFECONS formula exactly
- All outputs in plain `Real` (not M_USD units) — the solar model uses USD throughout, not millions

**Section 4: Leaf PartDefs (9 defs)**

Each follows this pattern (mirroring coffee maker, e.g., `'Heating Element'` at library.sysml:226–252):

```sysml
part def 'PV Module' :> 'Costed Component' {
    :>> cas_category = CASCategory::CAS220101;

    // Design parameters (set by usage in design.sysml)
    attribute wattage : Real;
    attribute efficiency : Real;

    // Embedded cost model
    calc cost_model : PVModuleCostCalc {
        in wattage = wattage;
        in efficiency = efficiency;
    }

    // Expose cost outputs
    :>> capital_cost = cost_model.total_cost;
    :>> raw_material_cost = cost_model.material_cost;
    :>> fabrication_cost = cost_model.fab_cost;
    :>> installation_cost = cost_model.install_cost;
    :>> idiot_index = cost_model.idiot_index;
}
```

**PermittingCostCalc special case**: Since it has no material/fab/install split:
```sysml
part def 'Permitting & Interconnect' :> 'Costed Component' {
    :>> cas_category = CASCategory::CAS10;

    attribute system_capacity_kw : Real;

    calc cost_model : PermittingCostCalc {
        in system_capacity_kw = system_capacity_kw;
    }

    :>> capital_cost = cost_model.total_cost;
    :>> raw_material_cost = 0.0;
    :>> fabrication_cost = 0.0;
    :>> installation_cost = 0.0;
    :>> idiot_index = 0.0;  // No material basis for soft cost
}
```

**Section 5: Assembly PartDefs (3 defs + 1 top-level)**

Follow the `'Brewing System'` pattern (library.sysml:384–438):

```sysml
part def 'Solar Array' :> 'Costed Component' {
    :>> cas_category = CASCategory::CAS22;

    attribute module_count : Integer default := 20;
    attribute inverter_count : Integer default := 4;

    part pv_module : 'PV Module' [module_count];
    part inverter : 'String Inverter' [inverter_count];
    part array_bos : 'Array BOS';

    // Allocation for assembly minor items
    calc allocation_model : AllocationCostCalc {
        in child_count = 25.0;  // 20 panels + 4 inverters + 1 BOS
        in total_child_mass = 50.0;  // Approximate total mass in kg
    }

    attribute misc_hardware_cost : Real = allocation_model.total_allocation;

    :>> capital_cost =
        sum(pv_module.capital_cost) +
        sum(inverter.capital_cost) +
        array_bos.capital_cost +
        misc_hardware_cost;

    :>> raw_material_cost =
        sum(pv_module.raw_material_cost) +
        sum(inverter.raw_material_cost) +
        array_bos.raw_material_cost +
        allocation_model.material_portion;

    :>> fabrication_cost =
        sum(pv_module.fabrication_cost) +
        sum(inverter.fabrication_cost) +
        array_bos.fabrication_cost;

    :>> installation_cost =
        sum(pv_module.installation_cost) +
        sum(inverter.installation_cost) +
        array_bos.installation_cost;

    :>> idiot_index = capital_cost / raw_material_cost;
}
```

`'Battery System'` and `'Site Infrastructure'` follow the same structure. Key differences:
- `'Battery System'`: parts are battery_pack[8], hybrid_inverter, battery_bos. No allocation model (simpler assembly).
- `'Site Infrastructure'`: parts are racking, panel, permitting. No allocation model. Note: permitting has `raw_material_cost = 0`, so assembly material rollup must handle this.

`'Solar Battery Plant'` (top-level): aggregates the 3 assemblies, no allocation model, same pattern as `'Coffee Maker'` (library.sysml:460–501).

**Design note — idiot_index on Site Infrastructure**: The `idiot_index = capital_cost / raw_material_cost` formula can produce inflated values when soft costs (permitting, with `raw_material_cost = 0`) dominate. At the assembly level this isn't a division-by-zero issue — racking and electrical panel do contribute non-zero material costs — but the ratio will be higher than typical physical assemblies. This is correct behavior: a high idiot index on Site Infrastructure accurately reflects that most of its cost is labor/permitting, not materials. No special handling needed.

### 2. design.sysml — Package `SolarBatteryDesign`

**Imports:**
```sysml
package SolarBatteryDesign {
    private import SolarBatteryLibrary::*;
    ...
}
```

**Structure**: One root instance with parameter bindings, following the coffee maker design pattern (design.sysml:16–55):

```sysml
part solar_battery_plant : 'Solar Battery Plant' {

    // Solar Array subsystem
    part redefines solar_array : 'Solar Array' {
        :>> pv_module.wattage = 400.0;       // 400W panels
        :>> pv_module.efficiency = 0.21;      // 21% efficiency
        :>> inverter.power_rating = 2000.0;   // 2kW micro-inverters
        :>> array_bos.string_count = 4.0;     // 4 strings
        :>> array_bos.panel_count = 20.0;     // 20 panels
    }

    // Battery System subsystem
    part redefines battery_system : 'Battery System' {
        :>> battery_pack.capacity_kwh = 5.0;       // 5kWh per pack
        :>> battery_pack.chemistry_factor = 1.0;    // LFP baseline
        :>> hybrid_inverter.power_rating = 10000.0; // 10kW bidirectional
        :>> battery_bos.pack_count = 8.0;           // 8 packs
    }

    // Site Infrastructure subsystem
    part redefines site_infra : 'Site Infrastructure' {
        :>> racking.panel_count = 20.0;        // 20 panels
        :>> racking.tilt_angle = 30.0;         // 30° tilt
        :>> electrical_panel.circuit_count = 4.0;  // 4 circuits
        :>> permitting.system_capacity_kw = 8.0;   // 8kW system
    }

    // ================================================================
    // SYSTEM-LEVEL CALC USAGES (visible to codegen)
    // ================================================================

    // Operating parameters
    attribute p_net_mw : Real = 0.008;           // 8 kW
    attribute n_mod : Real = 1.0;
    attribute plant_availability : Real = 0.159;  // (4.5/24) × 0.85
    attribute plant_lifetime : Real = 25.0;       // years
    attribute yearly_inflation : Real = 0.0245;   // BLS long-run
    attribute discount_rate : Real = 0.05;        // 5% real
    attribute om_rate_per_kw_year : Real = 20.0;  // $/kW-yr
    attribute p_net_kw : Real = p_net_mw * 1000.0;  // Derived from p_net_mw to avoid sync errors
    attribute fuel_unit_cost : Real = 0.0;        // No fuel for solar
    attribute fuel_consumption : Real = 0.0;      // No fuel for solar

    // System-level calculations — explicit CalcUsages at top level
    calc energy_production : EnergyProductionCalc {
        in p_net_mw = p_net_mw;
        in n_mod = n_mod;
        in plant_availability = plant_availability;
    }

    calc annualized_om : AnnualizedOMCalc {
        in om_rate_per_kw_year = om_rate_per_kw_year;
        in p_net_kw = p_net_kw;
    }

    calc annualized_fuel : AnnualizedFuelCalc {
        in fuel_unit_cost = fuel_unit_cost;
        in fuel_consumption = fuel_consumption;
    }

    calc annualized_financial : AnnualizedFinancialCalc {
        in total_capex = capital_cost;  // from 'Solar Battery Plant' rollup
        in discount_rate = discount_rate;
        in plant_lifetime = plant_lifetime;
    }

    calc lcoe : LCOECalc {
        in annualized_capital_cost = annualized_financial.annualized_capital_cost;
        in annual_om_cost = annualized_om.annual_om_cost;
        in annual_fuel_cost = annualized_fuel.annual_fuel_cost;
        in yearly_inflation = yearly_inflation;
        in plant_lifetime = plant_lifetime;
        in annual_energy_mwh = energy_production.annual_energy_mwh;
    }
}
```

**Key design points:**

1. **System-level CalcUsages are at the top level** of `solar_battery_plant`, not nested in any PartDef. This makes them visible to codegen (FR-11).

2. **`annualized_financial.total_capex = capital_cost`** wires the total CAPEX from the `'Solar Battery Plant'` cost rollup into the financial calc. This is the critical link between component costs and LCOE.

3. **`lcoe` calc wires outputs from other calcs** via dot notation (e.g., `annualized_financial.annualized_capital_cost`). This creates the inter-calc dependency chain that Item 2 (codegen spike) tests.

4. **All parameters are explicit attributes** at the plant level, not hardcoded in calc usages. This makes them bindable and inspectable.

### 3. validate_ast.py

Follow the coffee maker's `validate_ast.py` structure (555 lines) with extensions for system-level calcs.

**Duplicated from coffee maker** (copy and adapt, not shared import — same rationale as AllocationCostCalc: the coffee maker is a self-contained test):
- `SysideAdapter` loading pattern
- `CostModelInfo`, `PartInfo` dataclasses (extend as needed)
- `find_cost_models()` — discover embedded `cost_model` calc usages
- `find_part_usages_with_multiplicity()` — detect arrays
- `_extract_multiplicity_bound()` — extract quantity
- `print_results()` and `result_to_dict()` output patterns

**New functionality:**

| Function | Purpose |
|----------|---------|
| `find_system_level_calcs()` | Discover the 5 system-level CalcUsages (energy, om, fuel, financial, lcoe) |
| `verify_calc_at_design_level()` | Confirm system calcs are top-level in design, not nested in PartDefs |
| `verify_inter_calc_dependencies()` | Trace LCOECalc inputs to other calc outputs (dot-notation bindings) |
| `verify_assembly_rollups()` | Check that assemblies use `sum()` expressions, not calc usages |

**Discovery strategy for system-level calcs:**

The 5 system-level calcs are `CalculationUsage` elements whose `typings` resolve to the system-level CalcDefs (`EnergyProductionCalc`, `AnnualizedOMCalc`, etc.). To distinguish them from embedded `cost_model` usages:
- Embedded cost models: owned by PartDefinition elements
- System-level calcs: owned by the root PartUsage (design instance) or the design package

The validator should check the owner chain: if the calc usage's owner is a PartUsage (the design instance), it's system-level. If owned by a PartDefinition, it's an embedded cost model.

**Validation checks (mapping to FR-13 through FR-17):**

| Check | Expected Count | What It Validates |
|-------|---------------|-------------------|
| Embedded cost_model CalcUsages | 9 leaf + 1 allocation = 10 | FR-13 |
| System-level CalcUsages at design level | 5 | FR-13, FR-15 |
| Arrayed parts with multiplicity > 1 | 3 (pv_module[20], inverter[4], battery_pack[8]) | FR-14 |
| Inter-calc dependencies on LCOECalc | 3+ input bindings referencing other calc outputs | FR-16 |
| Assembly parts with sum() rollup | 3 (Solar Array, Battery System, Site Infrastructure) | FR-17 |

### 4. expected_output.csv

**Schema**: Same 14 columns as coffee maker (FR-20).

**Row order** (pre-order traversal, matching coffee maker's `_emit_preorder` pattern):

```
1.  solar_battery_plant                          (assembly, top-level)
2.  solar_battery_plant.solar_array              (assembly)
3.  solar_battery_plant.solar_array.pv_module    (leaf, qty=20)
4.  solar_battery_plant.solar_array.inverter     (leaf, qty=4)
5.  solar_battery_plant.solar_array.array_bos    (leaf, qty=1)
6.  solar_battery_plant.solar_array.allocation   (allocation, qty=1)
7.  solar_battery_plant.battery_system           (assembly)
8.  solar_battery_plant.battery_system.battery_pack      (leaf, qty=8)
9.  solar_battery_plant.battery_system.hybrid_inverter   (leaf, qty=1)
10. solar_battery_plant.battery_system.battery_bos       (leaf, qty=1)
11. solar_battery_plant.site_infra               (assembly)
12. solar_battery_plant.site_infra.racking       (leaf, qty=1)
13. solar_battery_plant.site_infra.electrical_panel  (leaf, qty=1)
14. solar_battery_plant.site_infra.permitting    (leaf, qty=1)
```

14 rows total (1 top-level + 3 assemblies + 9 leaves + 1 allocation).

**Hand calculation approach**: During implementation, choose CalcDef default cost parameters such that:
1. Each leaf cost = material + fab + install = material × (1 + fab_factor + install_factor)
2. Assembly cost = sum of children × quantities + allocation (for Solar Array)
3. Total CAPEX = sum of assemblies → target $35k–$45k range
4. LCOE = PyFECONS formula with exact parameters → target $0.15–$0.35/kWh range

The expected_output.csv will also include system-level calc results as additional rows or a separate section. Since the coffee maker CSV only has component costs, and this model adds system-level calcs, the CSV should include:

```
15. [system] energy_production     (system-level, annual_energy_mwh)
16. [system] annualized_om         (system-level, annual_om_cost)
17. [system] annualized_fuel       (system-level, annual_fuel_cost)
18. [system] annualized_financial  (system-level, annualized_capital_cost + CRF)
19. [system] lcoe                  (system-level, lcoe_per_mwh)
```

System-level results use a **separate file** rather than extending the 14-column CSV:

**`expected_system_outputs.csv`** (new file, 6 columns):
```
calc_name,calc_def,output_name,output_value,unit,notes
energy_production,EnergyProductionCalc,annual_energy_mwh,11149.44,MWh,8760 * 0.008 * 1 * 0.159
annualized_om,AnnualizedOMCalc,annual_om_cost,160.00,USD,20 * 8
annualized_fuel,AnnualizedFuelCalc,annual_fuel_cost,0.00,USD,0 * 0 (solar)
annualized_financial,AnnualizedFinancialCalc,capital_recovery_factor,0.07095,ratio,r*(1+r)^n/((1+r)^n-1)
annualized_financial,AnnualizedFinancialCalc,annualized_capital_cost,[CRF*CAPEX],USD,CRF * total CAPEX
lcoe,LCOECalc,lcoe_per_mwh,[computed],USD/MWh,PyFECONS formula
```

**Rationale**: The 14-column component cost CSV (FR-20) and system-level outputs serve different purposes. Component costs have quantity, unit vs. total, cost categories. System-level calcs have named scalar outputs with units. Forcing them into the same schema would require empty columns and confusing semantics. Separate files also match the downstream pipeline architecture: `component_costs.json` + `design_params.json` are separate entry points in Items 3–5.

The `expected_output.csv` remains component-costs-only (14 rows, 14 columns). The `expected_system_outputs.csv` is the LCOE verification target. Both are hand-calculated.

---

## Potential Risks

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| syside doesn't evaluate `**` correctly in complex expressions | Low | High | Validated with test file; CRF formula parses. If issues arise during generate_costs.py (Item 3), can decompose into intermediate `out` attributes |
| `cas_category` assignment causes compilation issues with foundation package | Low | Low | Proven in `costing_import_test.sysml`. Pattern is established |
| `sum()` on arrayed parts with foundation `'Costed Component'` behaves differently | Low | Medium | Coffee maker proves `sum()` works on part arrays. Foundation adds `cas_category` but doesn't change aggregation behavior |
| Cost parameter values don't produce sanity-check range | Medium | Low | Adjust CalcDef defaults during expected_output.csv creation. Parameters are independently tunable |
| Permitting soft cost (material=0) causes division by zero in idiot_index | Medium | Low | Set `idiot_index = 0.0` explicitly in PartDef, bypassing the formula |
| validate_ast.py can't distinguish system-level calcs from embedded calcs | Low | Medium | Check owner chain: system calcs owned by root PartUsage, embedded calcs owned by PartDefinition |

---

## Integration Strategy

This model integrates with the existing codebase at three points:

1. **Foundation package** (`models/library/foundation/costing.sysml`): Import-only dependency. No changes needed. The solar model is a consumer of `'Costed Component'` and `CASCategory`.

2. **Coffee maker pattern** (`models/tests/coffee_maker/`): The solar model follows the same structural patterns but extends them. No changes to coffee maker needed.

3. **Downstream pipeline** (Items 2–6): The solar model's `design.sysml` is designed so that:
   - System-level CalcUsages are at the top level → visible to codegen (Item 2, 4)
   - Component costs follow Pattern A → evaluable by generate_costs.py (Item 3)
   - Inter-calc wiring (lcoe ← financial, om, fuel, energy) → testable by codegen spike (Item 2)

---

## Validation Approach

### Compilation
```bash
uv run syside check models/tests/solar_battery/
```
Must exit 0 with no errors (warnings acceptable).

### AST Validation
```bash
uv run python models/tests/solar_battery/validate_ast.py
```
Reports counts and pass/fail for each check.

### Expected Output Verification
Hand-calculate all values using exact CalcDef formulas and design parameters. Verify:
- Total CAPEX in $35k–$45k
- Annual energy in 10,000–12,000 kWh
- LCOE in $0.15–$0.35/kWh
- Each leaf cost matches formula evaluation

### Regression Check
```bash
uv run syside check models/tests/coffee_maker/
uv run python models/tests/coffee_maker/validate_ast.py
```
Coffee maker must still pass.

---

**Next Step:** After approval → `/_my_plan` to break implementation into phases, or `/_my_implement` if the scope is clear enough to proceed directly.
