# Design: Cost Patterns Demo - Coffee Maker Model

**Type:** SysMLv2 Models (Test/Validation)
**Status:** Draft
**Owner:** Reid Westwood
**Created:** 2026-01-12
**Last Updated:** 2026-01-12

## Overview

Create a "coffee maker" demo model using Pattern A (nested cost models) to validate that the SysML v2 cost modeling architecture compiles, is AST-traversable, and produces the required output format. This de-risks Phase 4 (Cost Calculations) before investing in sysml-codegen tooling upgrades.

### Related Artifacts

- **Spec:** `project/active/cost-patterns-demo/spec.md`
- **Research:** `project/research/20260107-final-cost-architecture.md` - Pattern A architecture
- **Research:** `project/research/20260110-strategic-cost-patterns.md` - Standardization decisions
- **Epic:** `project/backlog/epic-cost-patterns-derisking.md`

## Current Model State

### Existing Definitions (Library)

- `models/library/` - Empty (no .sysml files exist)
- `models/tests/` - Empty (no .sysml files exist)

### Gaps

This design will create all new models from scratch:
- Abstract cost interface (`'Costed Component'`)
- Leaf cost calc defs (7 component cost calculations)
- Allocation cost calc def (assembly-level minor items)
- Part definitions with embedded cost models (10 parts)
- Design instance with full hierarchy

## Research Findings

### SysMLv2 Pattern Guidance

Based on sysmlv2-doc-analyzer research, the following patterns are validated:

**1. Calc Usage Inside Part Def (Template Pattern)**
- Calc usages owned by part definitions act as **templates**
- When a part usage instantiates the definition, the calc is implicitly instantiated
- Bindings via `in param = attribute` create binding connectors

**2. Redefinition Semantics**
- `:>>` = subsetting + redefinition (for binding inherited attributes)
- `:>> capital_cost = cost_model.total_cost` creates a binding constraint
- This is declarative (not procedural assignment) - `capital_cost` equals the calc output

**3. Multiplicity**
- `part heater : 'Heating Element' [2]` creates two distinct instances
- Each instance gets its own implicit calc usage
- Aggregation can be done via explicit expressions or deferred to tooling

**4. Abstract Part Defs**
- `abstract part def` prevents direct instantiation
- Specializations must redefine attributes (either via calcs or explicit values)
- Enforcement is via validation rules, not language syntax

### Key Pattern: Nested Cost Model

```sysml
// Library: Abstract interface
abstract part def 'Costed Component' {
    attribute capital_cost : Real;
    attribute raw_material_cost : Real;
}

// Library: Leaf component with embedded calc
part def 'Heating Element' :> 'Costed Component' {
    attribute power_rating : Real;
    attribute material_mass : Real;

    calc cost_model : HeatingElementCostCalc {
        in power = power_rating;
        in mass = material_mass;
    }

    :>> capital_cost = cost_model.total_cost;
    :>> raw_material_cost = cost_model.material_cost;
}

// Design: Clean instantiation
part coffee_maker {
    part brewing_system {
        part heater : 'Heating Element' {
            :>> power_rating = 1000.0;
            :>> material_mass = 0.15;
        }
    }
    // heater.capital_cost "just works"
}
```

---

## Detailed Design

### File Structure

```
models/tests/coffee_maker/
├── library.sysml      # All definitions (calc defs, part defs)
├── design.sysml       # coffee_maker instance with bindings
├── validate_ast.py    # AST traversal validation script
└── expected_output.csv # Target output format
```

### File 1: library.sysml

#### Package Structure

```sysml
package CoffeeMakerLibrary {
    // Standard imports
    private import ScalarValues::Real;
    private import ScalarValues::Integer;

    // === SECTION 1: ABSTRACT INTERFACE ===
    // === SECTION 2: CALC DEFINITIONS ===
    // === SECTION 3: LEAF PART DEFINITIONS ===
    // === SECTION 4: ASSEMBLY PART DEFINITIONS ===
}
```

#### Section 1: Abstract Interface - 'Costed Component'

**Purpose**: Define standard cost attributes that all costed parts must expose.

```sysml
abstract part def 'Costed Component' {
    doc /*
    Abstract interface for all cost-bearing components.
    Every costed part must specialize this and provide values for cost attributes.

    **Source**: Cost Patterns Research
    **Reference**: project/research/20260110-strategic-cost-patterns.md
    **Last Updated**: 2026-01-12
    */

    // Required cost attributes
    attribute capital_cost : Real;
    attribute raw_material_cost : Real;
    attribute fabrication_cost : Real;
    attribute installation_cost : Real;

    // Derived efficiency metric
    attribute idiot_index : Real;
}
```

#### Section 2: Calc Definitions (8 total)

**2.1 HeatingElementCostCalc**

```sysml
calc def HeatingElementCostCalc {
    doc /*
    Cost calculation for heating elements.

    Formula: Based on power rating and material mass.
    - Material: mass * material_cost_per_kg
    - Fabrication: material * fab_factor
    - Installation: material * install_factor

    **Source**: Demo model (fictional values)
    **Last Updated**: 2026-01-12
    */

    // Inputs
    in attribute power : Real;
    in attribute mass : Real;

    // Cost factors (defaults)
    in attribute material_cost_per_kg : Real default := 50.0;
    in attribute fab_factor : Real default := 0.6;
    in attribute install_factor : Real default := 0.15;

    // Outputs
    out attribute material_cost : Real = mass * material_cost_per_kg;
    out attribute fab_cost : Real = material_cost * fab_factor;
    out attribute install_cost : Real = material_cost * install_factor;
    out attribute total_cost : Real = material_cost + fab_cost + install_cost;
    out attribute idiot_index : Real = total_cost / material_cost;
}
```

**2.2 WaterPumpCostCalc**

```sysml
calc def WaterPumpCostCalc {
    doc /*
    Cost calculation for water pump.

    **Source**: Demo model (fictional values)
    **Last Updated**: 2026-01-12
    */

    in attribute flow_rate : Real;
    in attribute material_cost_per_kg : Real default := 30.0;
    in attribute pump_mass : Real default := 0.3;
    in attribute fab_factor : Real default := 0.8;
    in attribute install_factor : Real default := 0.1;

    out attribute material_cost : Real = pump_mass * material_cost_per_kg;
    out attribute fab_cost : Real = material_cost * fab_factor;
    out attribute install_cost : Real = material_cost * install_factor;
    out attribute total_cost : Real = material_cost + fab_cost + install_cost;
    out attribute idiot_index : Real = total_cost / material_cost;
}
```

**2.3 BrewChamberCostCalc**

```sysml
calc def BrewChamberCostCalc {
    doc /*
    Cost calculation for brew chamber.

    **Source**: Demo model (fictional values)
    **Last Updated**: 2026-01-12
    */

    in attribute volume : Real;
    in attribute material_cost_per_liter : Real default := 15.0;
    in attribute fab_factor : Real default := 0.5;
    in attribute install_factor : Real default := 0.1;

    out attribute material_cost : Real = volume * material_cost_per_liter;
    out attribute fab_cost : Real = material_cost * fab_factor;
    out attribute install_cost : Real = material_cost * install_factor;
    out attribute total_cost : Real = material_cost + fab_cost + install_cost;
    out attribute idiot_index : Real = total_cost / material_cost;
}
```

**2.4 WaterReservoirCostCalc**

```sysml
calc def WaterReservoirCostCalc {
    doc /*
    Cost calculation for water reservoir.

    **Source**: Demo model (fictional values)
    **Last Updated**: 2026-01-12
    */

    in attribute capacity : Real;
    in attribute material_cost_per_liter : Real default := 5.0;
    in attribute fab_factor : Real default := 0.4;
    in attribute install_factor : Real default := 0.1;

    out attribute material_cost : Real = capacity * material_cost_per_liter;
    out attribute fab_cost : Real = material_cost * fab_factor;
    out attribute install_cost : Real = material_cost * install_factor;
    out attribute total_cost : Real = material_cost + fab_cost + install_cost;
    out attribute idiot_index : Real = total_cost / material_cost;
}
```

**2.5 CarafeCostCalc**

```sysml
calc def CarafeCostCalc {
    doc /*
    Cost calculation for carafe (coffee pot).

    **Source**: Demo model (fictional values)
    **Last Updated**: 2026-01-12
    */

    in attribute capacity : Real;
    in attribute material_cost_per_liter : Real default := 8.0;
    in attribute fab_factor : Real default := 0.3;
    in attribute install_factor : Real default := 0.05;

    out attribute material_cost : Real = capacity * material_cost_per_liter;
    out attribute fab_cost : Real = material_cost * fab_factor;
    out attribute install_cost : Real = material_cost * install_factor;
    out attribute total_cost : Real = material_cost + fab_cost + install_cost;
    out attribute idiot_index : Real = total_cost / material_cost;
}
```

**2.6 OuterShellCostCalc**

```sysml
calc def OuterShellCostCalc {
    doc /*
    Cost calculation for outer shell housing.

    **Source**: Demo model (fictional values)
    **Last Updated**: 2026-01-12
    */

    in attribute surface_area : Real;
    in attribute material_cost_per_sqm : Real default := 20.0;
    in attribute fab_factor : Real default := 0.5;
    in attribute install_factor : Real default := 0.1;

    out attribute material_cost : Real = surface_area * material_cost_per_sqm;
    out attribute fab_cost : Real = material_cost * fab_factor;
    out attribute install_cost : Real = material_cost * install_factor;
    out attribute total_cost : Real = material_cost + fab_cost + install_cost;
    out attribute idiot_index : Real = total_cost / material_cost;
}
```

**2.7 ControlPanelCostCalc**

```sysml
calc def ControlPanelCostCalc {
    doc /*
    Cost calculation for control panel.

    **Source**: Demo model (fictional values)
    **Last Updated**: 2026-01-12
    */

    in attribute button_count : Real;
    in attribute base_cost : Real default := 10.0;
    in attribute cost_per_button : Real default := 2.0;
    in attribute fab_factor : Real default := 0.7;
    in attribute install_factor : Real default := 0.15;

    out attribute material_cost : Real = base_cost + button_count * cost_per_button;
    out attribute fab_cost : Real = material_cost * fab_factor;
    out attribute install_cost : Real = material_cost * install_factor;
    out attribute total_cost : Real = material_cost + fab_cost + install_cost;
    out attribute idiot_index : Real = total_cost / material_cost;
}
```

**2.8 AllocationCostCalc**

```sysml
calc def AllocationCostCalc {
    doc /*
    Bundled allocation costs for assembly-level minor items.
    Covers items not modeled as separate parts: fasteners, seals, wiring.

    **Pattern**: Rule R3 from strategic cost patterns
    **Source**: project/research/20260110-strategic-cost-patterns.md
    **Last Updated**: 2026-01-12
    */

    in attribute child_count : Real;
    in attribute total_child_mass : Real;

    // Allocation factors
    in attribute fastener_cost_per_child : Real default := 0.50;
    in attribute seal_cost_per_child : Real default := 0.30;
    in attribute wiring_cost_per_kg : Real default := 2.0;

    out attribute fastener_cost : Real = child_count * fastener_cost_per_child;
    out attribute seal_cost : Real = child_count * seal_cost_per_child;
    out attribute wiring_cost : Real = total_child_mass * wiring_cost_per_kg;
    out attribute total_allocation : Real = fastener_cost + seal_cost + wiring_cost;

    // Material portion for idiot index (80% of allocation is material)
    out attribute material_portion : Real = total_allocation * 0.8;
}
```

#### Section 3: Leaf Part Definitions (7 total)

**3.1 'Heating Element'**

```sysml
part def 'Heating Element' :> 'Costed Component' {
    doc /*
    Heating element that converts electricity to heat.
    Contains embedded cost model that computes cost from parameters.

    **Pattern**: Nested cost model (Pattern A)
    **Source**: project/research/20260107-final-cost-architecture.md
    **Last Updated**: 2026-01-12
    */

    // Design parameters (set by usage)
    attribute power_rating : Real;
    attribute material_mass : Real;

    // Embedded cost model
    calc cost_model : HeatingElementCostCalc {
        in power = power_rating;
        in mass = material_mass;
    }

    // Expose cost outputs via redefinition
    :>> capital_cost = cost_model.total_cost;
    :>> raw_material_cost = cost_model.material_cost;
    :>> fabrication_cost = cost_model.fab_cost;
    :>> installation_cost = cost_model.install_cost;
    :>> idiot_index = cost_model.idiot_index;
}
```

**3.2 'Water Pump'**

```sysml
part def 'Water Pump' :> 'Costed Component' {
    doc /*
    Pump that moves water through the brewing system.

    **Pattern**: Nested cost model (Pattern A)
    **Last Updated**: 2026-01-12
    */

    attribute flow_rate : Real;

    calc cost_model : WaterPumpCostCalc {
        in flow_rate = flow_rate;
    }

    :>> capital_cost = cost_model.total_cost;
    :>> raw_material_cost = cost_model.material_cost;
    :>> fabrication_cost = cost_model.fab_cost;
    :>> installation_cost = cost_model.install_cost;
    :>> idiot_index = cost_model.idiot_index;
}
```

**3.3 'Brew Chamber'**

```sysml
part def 'Brew Chamber' :> 'Costed Component' {
    doc /*
    Chamber that holds coffee grounds during extraction.

    **Pattern**: Nested cost model (Pattern A)
    **Last Updated**: 2026-01-12
    */

    attribute volume : Real;

    calc cost_model : BrewChamberCostCalc {
        in volume = volume;
    }

    :>> capital_cost = cost_model.total_cost;
    :>> raw_material_cost = cost_model.material_cost;
    :>> fabrication_cost = cost_model.fab_cost;
    :>> installation_cost = cost_model.install_cost;
    :>> idiot_index = cost_model.idiot_index;
}
```

**3.4 'Water Reservoir'**

```sysml
part def 'Water Reservoir' :> 'Costed Component' {
    doc /*
    Tank that stores water for brewing.

    **Pattern**: Nested cost model (Pattern A)
    **Last Updated**: 2026-01-12
    */

    attribute capacity : Real;

    calc cost_model : WaterReservoirCostCalc {
        in capacity = capacity;
    }

    :>> capital_cost = cost_model.total_cost;
    :>> raw_material_cost = cost_model.material_cost;
    :>> fabrication_cost = cost_model.fab_cost;
    :>> installation_cost = cost_model.install_cost;
    :>> idiot_index = cost_model.idiot_index;
}
```

**3.5 'Carafe'**

```sysml
part def 'Carafe' :> 'Costed Component' {
    doc /*
    Glass carafe that holds brewed coffee.

    **Pattern**: Nested cost model (Pattern A)
    **Last Updated**: 2026-01-12
    */

    attribute capacity : Real;

    calc cost_model : CarafeCostCalc {
        in capacity = capacity;
    }

    :>> capital_cost = cost_model.total_cost;
    :>> raw_material_cost = cost_model.material_cost;
    :>> fabrication_cost = cost_model.fab_cost;
    :>> installation_cost = cost_model.install_cost;
    :>> idiot_index = cost_model.idiot_index;
}
```

**3.6 'Outer Shell'**

```sysml
part def 'Outer Shell' :> 'Costed Component' {
    doc /*
    External plastic shell housing.

    **Pattern**: Nested cost model (Pattern A)
    **Last Updated**: 2026-01-12
    */

    attribute surface_area : Real;

    calc cost_model : OuterShellCostCalc {
        in surface_area = surface_area;
    }

    :>> capital_cost = cost_model.total_cost;
    :>> raw_material_cost = cost_model.material_cost;
    :>> fabrication_cost = cost_model.fab_cost;
    :>> installation_cost = cost_model.install_cost;
    :>> idiot_index = cost_model.idiot_index;
}
```

**3.7 'Control Panel'**

```sysml
part def 'Control Panel' :> 'Costed Component' {
    doc /*
    User interface panel with buttons.

    **Pattern**: Nested cost model (Pattern A)
    **Last Updated**: 2026-01-12
    */

    attribute button_count : Real;

    calc cost_model : ControlPanelCostCalc {
        in button_count = button_count;
    }

    :>> capital_cost = cost_model.total_cost;
    :>> raw_material_cost = cost_model.material_cost;
    :>> fabrication_cost = cost_model.fab_cost;
    :>> installation_cost = cost_model.install_cost;
    :>> idiot_index = cost_model.idiot_index;
}
```

#### Section 4: Assembly Part Definitions (3 total)

**4.1 'Brewing System'**

```sysml
part def 'Brewing System' :> 'Costed Component' {
    doc /*
    Sub-assembly that produces coffee.
    Contains heating elements (x2), pump, and brew chamber.
    Includes allocation costs for fasteners, seals, and wiring.

    **Pattern**: Assembly aggregation (Rule R2) + Allocation costs (Rule R3)
    **Source**: project/research/20260110-strategic-cost-patterns.md
    **Last Updated**: 2026-01-12
    */

    // Child parts
    part heater : 'Heating Element' [2];
    part pump : 'Water Pump';
    part chamber : 'Brew Chamber';

    // Allocation cost model for minor items
    calc allocation_model : AllocationCostCalc {
        in child_count = 4;  // 2 heaters + pump + chamber
        in total_child_mass = 0.8;  // Approximate total mass
    }

    // Expose allocation details
    attribute misc_hardware_cost : Real = allocation_model.total_allocation;

    // Aggregate costs from children + allocation
    // Note: For heater[2], we access individual elements or use explicit sum
    :>> capital_cost =
        heater.capital_cost + heater.capital_cost +  // 2 heaters (explicit)
        pump.capital_cost +
        chamber.capital_cost +
        misc_hardware_cost;

    :>> raw_material_cost =
        heater.raw_material_cost + heater.raw_material_cost +
        pump.raw_material_cost +
        chamber.raw_material_cost +
        allocation_model.material_portion;

    :>> fabrication_cost =
        heater.fabrication_cost + heater.fabrication_cost +
        pump.fabrication_cost +
        chamber.fabrication_cost;

    :>> installation_cost =
        heater.installation_cost + heater.installation_cost +
        pump.installation_cost +
        chamber.installation_cost;

    :>> idiot_index = capital_cost / raw_material_cost;
}
```

**4.2 'Housing'**

```sysml
part def 'Housing' :> 'Costed Component' {
    doc /*
    Enclosure sub-assembly containing shell and control panel.

    **Pattern**: Assembly aggregation (Rule R2)
    **Last Updated**: 2026-01-12
    */

    // Child parts
    part shell : 'Outer Shell';
    part panel : 'Control Panel';

    // Aggregate costs from children (no allocation for this simple assembly)
    :>> capital_cost = shell.capital_cost + panel.capital_cost;
    :>> raw_material_cost = shell.raw_material_cost + panel.raw_material_cost;
    :>> fabrication_cost = shell.fabrication_cost + panel.fabrication_cost;
    :>> installation_cost = shell.installation_cost + panel.installation_cost;
    :>> idiot_index = capital_cost / raw_material_cost;
}
```

**4.3 'Coffee Maker'**

```sysml
part def 'Coffee Maker' :> 'Costed Component' {
    doc /*
    Top-level assembly representing the complete coffee maker product.
    Aggregates all subsystems: brewing system, reservoir, carafe, housing.

    **Pattern**: Assembly aggregation (Rule R2)
    **Last Updated**: 2026-01-12
    */

    // Child sub-assemblies and parts
    part brewing : 'Brewing System';
    part reservoir : 'Water Reservoir';
    part carafe : 'Carafe';
    part housing : 'Housing';

    // Top-level aggregation
    :>> capital_cost =
        brewing.capital_cost +
        reservoir.capital_cost +
        carafe.capital_cost +
        housing.capital_cost;

    :>> raw_material_cost =
        brewing.raw_material_cost +
        reservoir.raw_material_cost +
        carafe.raw_material_cost +
        housing.raw_material_cost;

    :>> fabrication_cost =
        brewing.fabrication_cost +
        reservoir.fabrication_cost +
        carafe.fabrication_cost +
        housing.fabrication_cost;

    :>> installation_cost =
        brewing.installation_cost +
        reservoir.installation_cost +
        carafe.installation_cost +
        housing.installation_cost;

    :>> idiot_index = capital_cost / raw_material_cost;
}
```

### File 2: design.sysml

```sysml
package CoffeeMakerDesign {
    doc /*
    Concrete coffee maker design instance with all parameter values.

    **Purpose**: Validate Pattern A (nested cost models) with specific values.
    **Last Updated**: 2026-01-12
    */

    private import CoffeeMakerLibrary::*;

    // Top-level design instance
    part coffee_maker : 'Coffee Maker' {
        doc /* Standard home coffee maker design */

        part brewing : 'Brewing System' {
            // Dual heating elements (tests multiplicity)
            part heater : 'Heating Element' [2] {
                :>> power_rating = 1000.0;   // Watts
                :>> material_mass = 0.15;    // kg per element
            }

            part pump : 'Water Pump' {
                :>> flow_rate = 0.5;  // liters per minute
            }

            part chamber : 'Brew Chamber' {
                :>> volume = 0.3;  // liters
            }
        }

        part reservoir : 'Water Reservoir' {
            :>> capacity = 1.5;  // liters
        }

        part carafe : 'Carafe' {
            :>> capacity = 1.2;  // liters
        }

        part housing : 'Housing' {
            part shell : 'Outer Shell' {
                :>> surface_area = 0.15;  // square meters
            }

            part panel : 'Control Panel' {
                :>> button_count = 3.0;  // power, strength, timer
            }
        }
    }
}
```

---

## Expected Cost Rollup (Manual Calculation)

### Leaf Component Costs

| Component | Material | Fab | Install | Total | Idiot Index |
|-----------|----------|-----|---------|-------|-------------|
| Heater (x1) | 0.15 * 50 = 7.50 | 7.50 * 0.6 = 4.50 | 7.50 * 0.15 = 1.125 | 13.125 | 1.75 |
| Heater (x2) | 15.00 | 9.00 | 2.25 | 26.25 | 1.75 |
| Pump | 0.3 * 30 = 9.00 | 9.00 * 0.8 = 7.20 | 9.00 * 0.1 = 0.90 | 17.10 | 1.90 |
| Chamber | 0.3 * 15 = 4.50 | 4.50 * 0.5 = 2.25 | 4.50 * 0.1 = 0.45 | 7.20 | 1.60 |
| Reservoir | 1.5 * 5 = 7.50 | 7.50 * 0.4 = 3.00 | 7.50 * 0.1 = 0.75 | 11.25 | 1.50 |
| Carafe | 1.2 * 8 = 9.60 | 9.60 * 0.3 = 2.88 | 9.60 * 0.05 = 0.48 | 12.96 | 1.35 |
| Shell | 0.15 * 20 = 3.00 | 3.00 * 0.5 = 1.50 | 3.00 * 0.1 = 0.30 | 4.80 | 1.60 |
| Panel | 10 + 3*2 = 16.00 | 16.00 * 0.7 = 11.20 | 16.00 * 0.15 = 2.40 | 29.60 | 1.85 |

### Allocation Costs (Brewing System)

- Fasteners: 4 * 0.50 = 2.00
- Seals: 4 * 0.30 = 1.20
- Wiring: 0.8 * 2.0 = 1.60
- **Total Allocation**: 4.80
- Material Portion: 4.80 * 0.8 = 3.84

### Assembly Rollups

| Assembly | Children Total | Allocation | Total | Material | Idiot Index |
|----------|---------------|------------|-------|----------|-------------|
| Brewing System | 26.25 + 17.10 + 7.20 = 50.55 | 4.80 | 55.35 | 15 + 9 + 4.5 + 3.84 = 32.34 | 1.71 |
| Housing | 4.80 + 29.60 = 34.40 | 0 | 34.40 | 3 + 16 = 19.00 | 1.81 |
| **Coffee Maker** | 55.35 + 11.25 + 12.96 + 34.40 = **113.96** | 0 | **113.96** | 32.34 + 7.5 + 9.6 + 19 = **68.44** | **1.66** |

---

## Common Pitfalls & Quick Reference

### SysML v2 Syntax Rules for This Project

#### Attribute Declarations
- `attribute power_rating : Real = 1000.0;` (with type and default)
- `attribute power_rating : Real;` (declaration only, value in usage)

#### Redefinition in Usages
- `:>> power_rating = 1000.0;` (redefine inherited attribute)
- `:>> capital_cost = cost_model.total_cost;` (expose calc output)

#### Calc Def Inputs/Outputs
- `in attribute param : Real;` (input)
- `in attribute param : Real default := 5.0;` (input with default)
- `out attribute result : Real = formula;` (output with formula)

#### Multiplicity
- `part heater : 'Heating Element' [2]` - array of 2 elements
- Access: `heater.capital_cost` may need explicit handling in expressions

#### Documentation Requirements
- Every `part def` and `calc def` needs `doc /* ... */`
- Include **Source**, **Reference**, **Last Updated**

### Validation Commands

```bash
# Quick syntax check
syside check models/tests/coffee_maker/library.sysml
syside check models/tests/coffee_maker/design.sysml

# Check both files together
syside check models/tests/coffee_maker/
```

---

## Validation Plan

### Level 1: Parse Validation
- `syside check` must pass for all .sysml files (exit code 0)

### Level 2: AST Traversal Validation
- Python script must find all 7 leaf `cost_model` calc usages
- Script must trace bindings through redefinitions
- Script must identify allocation costs at assembly level

### Level 3: Manual Verification
- Rollup math: sum of children + allocation = parent
- Multiplicity: heater [2] cost = 2 * unit cost
- Cross-check against expected_output.csv

---

## Implementation Checklist

### Phase 1: Create Directory and Library File
- [x] Create `models/tests/coffee_maker/` directory
- [x] Create `library.sysml` with all definitions
- [x] Parse validation: `syside check library.sysml`

### Phase 2: Create Design Instance
- [x] Create `design.sysml` with coffee_maker instance
- [x] Parse validation: `syside check design.sysml`

### Phase 3: Create Validation Script
- [x] Create `validate_ast.py` for AST traversal
- [x] Verify 7 leaf cost_models found
- [x] Verify allocation model detected

### Phase 4: Create Expected Output
- [x] Create `expected_output.csv` with target format
- [x] Manual rollup verification against calculated values

---

## Phase 3: AST Validation Script Design

### Overview

Create `validate_ast.py` to traverse the SysML model AST and validate that the cost modeling patterns are correctly implemented and discoverable by tooling.

### Dependencies

The script leverages existing `agentic-mbse` infrastructure:

| Dependency | Import Path | Purpose |
|------------|-------------|---------|
| SysideAdapter | `agentic_mbse.sysml.syside_adapter` | Model loading, element iteration, type checking |
| common utilities | `agentic_mbse.validation.common` | `get_qualified_name`, `get_element_location` |
| binding extraction | `agentic_mbse.sysml.binding` | `extract_bindings` for parameter tracing |

### Script Structure

```
models/tests/coffee_maker/validate_ast.py
```

#### Main Components

**1. CostModelInfo dataclass**

Captures discovered cost_model information:

```python
@dataclass
class CostModelInfo:
    """Information about a discovered cost_model calc usage."""
    name: str                    # "cost_model"
    calc_def_name: str           # "HeatingElementCostCalc"
    owning_part_def: str         # "Heating Element"
    qualified_path: str          # "CoffeeMakerLibrary::'Heating Element'::cost_model"
    location: str                # "library.sysml:239"
    cost_type: str               # "leaf" or "allocation"
    bound_outputs: list[str]     # ["capital_cost", "raw_material_cost", ...]
```

**2. PartInfo dataclass**

Captures part usage information with multiplicity:

```python
@dataclass
class PartInfo:
    """Information about a discovered part usage."""
    name: str                    # "heater"
    part_def_name: str           # "Heating Element"
    qualified_path: str          # "CoffeeMakerDesign::coffee_maker::brewing::heater"
    location: str                # "design.sysml:17"
    multiplicity: int            # 2 (from [2])
    is_array: bool               # True
    has_cost_model: bool         # True (part def has cost_model)
```

**3. ValidationResult dataclass**

Aggregates all findings:

```python
@dataclass
class ValidationResult:
    """Complete validation result."""
    success: bool
    cost_models: list[CostModelInfo]
    part_usages: list[PartInfo]
    allocation_models: list[CostModelInfo]
    issues: list[str]

    # Computed properties
    @property
    def leaf_cost_model_count(self) -> int: ...

    @property
    def allocation_model_count(self) -> int: ...
```

### Key Functions

**4. find_cost_models(model) -> list[CostModelInfo]**

Find all `cost_model` and `allocation_model` calc usages:

```python
def find_cost_models(model) -> list[CostModelInfo]:
    """Find all cost_model calc usages inside part definitions."""
    results = []

    for calc_usage in SysideAdapter.elements_of_type(model, "CalculationUsage"):
        name = calc_usage.name
        if name not in ("cost_model", "allocation_model"):
            continue

        # Get owning part definition
        owner = calc_usage.owning_type
        if not owner:
            continue

        # Get calc definition name
        calc_def = calc_usage.calculation_definition
        calc_def_name = calc_def.name if calc_def else "<unknown>"

        # Determine cost type
        cost_type = "allocation" if name == "allocation_model" else "leaf"

        # Get bound outputs (redefinitions that reference this calc)
        bound_outputs = _find_bound_outputs(owner, name)

        results.append(CostModelInfo(
            name=name,
            calc_def_name=calc_def_name,
            owning_part_def=owner.name,
            qualified_path=get_qualified_name(calc_usage),
            location=get_element_location(calc_usage),
            cost_type=cost_type,
            bound_outputs=bound_outputs,
        ))

    return results
```

**5. find_part_usages_with_multiplicity(model) -> list[PartInfo]**

Find all part usages and extract multiplicity:

```python
def find_part_usages_with_multiplicity(model) -> list[PartInfo]:
    """Find all part usages and extract multiplicity information."""
    results = []

    for part_usage in SysideAdapter.elements_of_type(model, "PartUsage"):
        name = part_usage.name
        if not name:
            continue

        # Get multiplicity
        multiplicity = 1
        is_array = False
        mult = part_usage.multiplicity
        if mult and hasattr(mult, 'has_cached_bounds') and mult.has_cached_bounds:
            lower = mult.cached_lower_bound
            upper = mult.cached_upper_bound
            if upper is not None and upper > 1:
                multiplicity = upper
                is_array = True
            elif lower > 1:
                multiplicity = lower
                is_array = True

        # Get part definition
        part_defs = list(part_usage.part_definitions) if hasattr(part_usage, 'part_definitions') else []
        part_def_name = part_defs[0].name if part_defs else "<unknown>"

        # Check if part def has cost_model
        has_cost_model = _part_def_has_cost_model(part_defs[0]) if part_defs else False

        results.append(PartInfo(
            name=name,
            part_def_name=part_def_name,
            qualified_path=get_qualified_name(part_usage),
            location=get_element_location(part_usage),
            multiplicity=multiplicity,
            is_array=is_array,
            has_cost_model=has_cost_model,
        ))

    return results
```

**6. trace_redefinition_bindings(model) -> list[BindingInfo]**

Trace `:>>` redefinition bindings to understand cost flow:

```python
def trace_redefinition_bindings(model) -> list[dict]:
    """Trace redefinition bindings like :>> capital_cost = cost_model.total_cost"""
    bindings = []

    for part_def in SysideAdapter.elements_of_type(model, "PartDefinition"):
        # Iterate over owned features
        if not hasattr(part_def, 'owned_features'):
            continue

        for feature in part_def.owned_features:
            # Check for redefinitions
            if not hasattr(feature, 'owned_redefinitions'):
                continue

            for redef in feature.owned_redefinitions:
                redefined = redef.redefined_feature
                if not redefined:
                    continue

                # Get the value expression if present
                value_expr = None
                if hasattr(feature, 'feature_value_expression'):
                    value_expr = feature.feature_value_expression

                bindings.append({
                    'part_def': part_def.name,
                    'attribute': redefined.name,
                    'has_value': value_expr is not None,
                    'location': get_element_location(feature),
                })

    return bindings
```

**7. validate_cost_patterns(model) -> ValidationResult**

Main validation function:

```python
def validate_cost_patterns(model) -> ValidationResult:
    """Run full cost pattern validation."""
    issues = []

    # Find cost models
    cost_models = find_cost_models(model)
    leaf_models = [cm for cm in cost_models if cm.cost_type == "leaf"]
    allocation_models = [cm for cm in cost_models if cm.cost_type == "allocation"]

    # Find part usages with multiplicity
    part_usages = find_part_usages_with_multiplicity(model)

    # Validation checks
    # MR-008: Expect 7 leaf cost_models
    if len(leaf_models) != 7:
        issues.append(f"Expected 7 leaf cost_models, found {len(leaf_models)}")

    # MR-010: Expect allocation_model in Brewing System
    brewing_alloc = [am for am in allocation_models
                     if "Brewing System" in am.owning_part_def]
    if not brewing_alloc:
        issues.append("Expected allocation_model in 'Brewing System'")

    # MR-007: Expect heater[2] multiplicity
    heater_parts = [p for p in part_usages if p.name == "heater" and p.is_array]
    if not heater_parts:
        issues.append("Expected 'heater' part with multiplicity [2]")
    elif heater_parts[0].multiplicity != 2:
        issues.append(f"Expected heater multiplicity 2, got {heater_parts[0].multiplicity}")

    # MR-014: Assemblies should NOT have cost_model (only allocation_model)
    assembly_names = ["Brewing System", "Housing", "Coffee Maker"]
    for cm in leaf_models:
        if cm.owning_part_def in assembly_names:
            issues.append(f"Assembly '{cm.owning_part_def}' should not have cost_model")

    return ValidationResult(
        success=len(issues) == 0,
        cost_models=leaf_models,
        part_usages=part_usages,
        allocation_models=allocation_models,
        issues=issues,
    )
```

### Output Format

The script outputs JSON for machine parsing and human-readable summary:

```python
def print_results(result: ValidationResult) -> None:
    """Print validation results in human-readable format."""
    print(f"\n{'='*60}")
    print("Cost Patterns AST Validation")
    print("="*60)

    # Summary
    status = "PASS" if result.success else "FAIL"
    print(f"\nStatus: {status}")
    print(f"Leaf cost_models found: {result.leaf_cost_model_count}")
    print(f"Allocation models found: {result.allocation_model_count}")
    print(f"Parts with multiplicity: {sum(1 for p in result.part_usages if p.is_array)}")

    # Details
    print("\n--- Leaf Cost Models ---")
    for cm in result.cost_models:
        print(f"  {cm.owning_part_def}::{cm.name}")
        print(f"    Calc def: {cm.calc_def_name}")
        print(f"    Path: {cm.qualified_path}")
        print(f"    Location: {cm.location}")
        print(f"    Bound outputs: {', '.join(cm.bound_outputs)}")

    print("\n--- Allocation Models ---")
    for am in result.allocation_models:
        print(f"  {am.owning_part_def}::{am.name}")
        print(f"    Calc def: {am.calc_def_name}")
        print(f"    Location: {am.location}")

    print("\n--- Parts with Multiplicity ---")
    for p in result.part_usages:
        if p.is_array:
            print(f"  {p.name} [{p.multiplicity}] : {p.part_def_name}")
            print(f"    Path: {p.qualified_path}")

    # Issues
    if result.issues:
        print("\n--- Issues ---")
        for issue in result.issues:
            print(f"  - {issue}")

    print()
```

### CLI Interface

```python
def main():
    """Main entry point."""
    import argparse
    parser = argparse.ArgumentParser(description="Validate cost patterns in SysML model")
    parser.add_argument("--json", action="store_true", help="Output JSON format")
    parser.add_argument("model_path", nargs="?",
                        default="models/tests/coffee_maker",
                        help="Path to SysML model directory")
    args = parser.parse_args()

    # Load model
    model_dir = Path(args.model_path)
    files = list(model_dir.glob("*.sysml"))
    model, diagnostics = SysideAdapter.load_model(files)

    # Check for parse errors
    if diagnostics.has_errors:
        print("Model has parse errors:")
        for msg in diagnostics.messages:
            print(f"  {msg.severity}: {msg.message}")
        sys.exit(1)

    # Run validation
    result = validate_cost_patterns(model)

    # Output
    if args.json:
        print(json.dumps(asdict(result), indent=2))
    else:
        print_results(result)

    sys.exit(0 if result.success else 1)

if __name__ == "__main__":
    main()
```

### Expected Script Output

```
============================================================
Cost Patterns AST Validation
============================================================

Status: PASS
Leaf cost_models found: 7
Allocation models found: 1
Parts with multiplicity: 1

--- Leaf Cost Models ---
  Heating Element::cost_model
    Calc def: HeatingElementCostCalc
    Path: CoffeeMakerLibrary::'Heating Element'::cost_model
    Location: library.sysml:239
    Bound outputs: capital_cost, raw_material_cost, fabrication_cost, installation_cost, idiot_index
  Water Pump::cost_model
    Calc def: WaterPumpCostCalc
    Path: CoffeeMakerLibrary::'Water Pump'::cost_model
    Location: library.sysml:262
    Bound outputs: capital_cost, raw_material_cost, fabrication_cost, installation_cost, idiot_index
  ... (5 more)

--- Allocation Models ---
  Brewing System::allocation_model
    Calc def: AllocationCostCalc
    Location: library.sysml:399

--- Parts with Multiplicity ---
  heater [2] : Heating Element
    Path: CoffeeMakerDesign::coffee_maker::brewing::heater
```

### Validation Against Spec Requirements

| Requirement | Validation Check | Script Function |
|-------------|------------------|-----------------|
| MR-008 | Find all 7 leaf cost_model calc usages | `find_cost_models()` |
| MR-009 | Trace bindings through redefinition chains | `trace_redefinition_bindings()` |
| MR-010 | Identify allocation costs at assembly level | `find_cost_models()` filtering by type |
| MR-007 | Detect heater[2] multiplicity | `find_part_usages_with_multiplicity()` |
| MR-014 | Verify assemblies have no cost_model | Validation check in `validate_cost_patterns()` |

---

## Phase 4: Expected Output CSV Design

### Overview

Create `expected_output.csv` documenting the target cost breakdown format that tooling (sysml-codegen) should produce.

### File Structure

```
models/tests/coffee_maker/expected_output.csv
```

### CSV Schema

| Column | Type | Description |
|--------|------|-------------|
| `path` | string | Qualified path from root (e.g., `coffee_maker.brewing.heater`) |
| `part_def` | string | Part definition name (e.g., `Heating Element`) |
| `quantity` | integer | Number of instances (from multiplicity) |
| `unit_material_cost` | float | Material cost per unit |
| `unit_fab_cost` | float | Fabrication cost per unit |
| `unit_install_cost` | float | Installation cost per unit |
| `unit_total_cost` | float | Total cost per unit |
| `total_material_cost` | float | Material cost * quantity |
| `total_fab_cost` | float | Fabrication cost * quantity |
| `total_install_cost` | float | Installation cost * quantity |
| `total_cost` | float | Total cost * quantity |
| `idiot_index` | float | total_cost / material_cost |
| `cost_type` | string | `leaf`, `allocation`, or `assembly` |
| `calc_def` | string | Calc def name (for leaves) or empty for assemblies |

### Expected Data

Based on the manual calculations from design document:

```csv
path,part_def,quantity,unit_material_cost,unit_fab_cost,unit_install_cost,unit_total_cost,total_material_cost,total_fab_cost,total_install_cost,total_cost,idiot_index,cost_type,calc_def
coffee_maker,Coffee Maker,1,,,,,68.44,,,113.96,1.66,assembly,
coffee_maker.brewing,Brewing System,1,,,,,32.34,,,55.35,1.71,assembly,
coffee_maker.brewing.heater,Heating Element,2,7.50,4.50,1.125,13.125,15.00,9.00,2.25,26.25,1.75,leaf,HeatingElementCostCalc
coffee_maker.brewing.pump,Water Pump,1,9.00,7.20,0.90,17.10,9.00,7.20,0.90,17.10,1.90,leaf,WaterPumpCostCalc
coffee_maker.brewing.chamber,Brew Chamber,1,4.50,2.25,0.45,7.20,4.50,2.25,0.45,7.20,1.60,leaf,BrewChamberCostCalc
coffee_maker.brewing.allocation,Brewing System Allocation,1,3.84,0.00,0.00,4.80,3.84,0.00,0.00,4.80,1.25,allocation,AllocationCostCalc
coffee_maker.reservoir,Water Reservoir,1,7.50,3.00,0.75,11.25,7.50,3.00,0.75,11.25,1.50,leaf,WaterReservoirCostCalc
coffee_maker.carafe,Carafe,1,9.60,2.88,0.48,12.96,9.60,2.88,0.48,12.96,1.35,leaf,CarafeCostCalc
coffee_maker.housing,Housing,1,,,,,19.00,,,34.40,1.81,assembly,
coffee_maker.housing.shell,Outer Shell,1,3.00,1.50,0.30,4.80,3.00,1.50,0.30,4.80,1.60,leaf,OuterShellCostCalc
coffee_maker.housing.panel,Control Panel,1,16.00,11.20,2.40,29.60,16.00,11.20,2.40,29.60,1.85,leaf,ControlPanelCostCalc
```

### Calculation Verification

The CSV includes derived values that can be cross-checked:

**Leaf Component Calculations:**
- `unit_total_cost = unit_material_cost + unit_fab_cost + unit_install_cost`
- `total_cost = unit_total_cost * quantity`
- `idiot_index = total_cost / total_material_cost`

**Assembly Aggregations:**
- `total_cost = sum(child.total_cost) + allocation.total_cost`
- `total_material_cost = sum(child.total_material_cost) + allocation.material_portion`

### Verification Script

A simple Python script can verify the CSV:

```python
def verify_csv(csv_path: str) -> bool:
    """Verify CSV calculations are internally consistent."""
    import csv

    with open(csv_path) as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    issues = []

    for row in rows:
        if row['cost_type'] == 'leaf':
            # Verify unit_total = sum of components
            expected = (float(row['unit_material_cost']) +
                       float(row['unit_fab_cost']) +
                       float(row['unit_install_cost']))
            actual = float(row['unit_total_cost'])
            if abs(expected - actual) > 0.01:
                issues.append(f"{row['path']}: unit_total mismatch")

            # Verify total = unit * quantity
            expected = float(row['unit_total_cost']) * int(row['quantity'])
            actual = float(row['total_cost'])
            if abs(expected - actual) > 0.01:
                issues.append(f"{row['path']}: total_cost mismatch")

    # Verify assembly rollups
    # ... (check parent totals equal sum of children)

    return len(issues) == 0
```

### Usage Notes

1. **Empty cells for assemblies**: Assembly rows leave unit costs empty since they aggregate children
2. **Allocation row**: The allocation is a separate line item under the assembly
3. **Quantity handling**: The `quantity` column enables multiplicity-aware rollups
4. **Traceability**: The `calc_def` column enables back-tracing to source calculations

---

## Design Validation Report

**Status**: PASS
**Date**: 2026-01-12

### Quality Checks

| Level | Check | Status | Notes |
|-------|-------|--------|-------|
| 1 | Syntax (syside check) | PASS | Exit code 0 |
| 2 | Structural | PASS | All imports resolve correctly |
| 3 | Dataflow | PASS | No circular dependencies |

### Warnings (Expected)

9 warnings about "member name shadows" - these are expected behavior when redefining inherited parts to bind parameter values. The design pattern (specialization + redefinition) causes SysIDE to warn that we're shadowing inherited members, but this is the correct SysML v2 pattern for binding values in usages.

### Files Created

- `models/tests/coffee_maker/library.sysml` - 500 lines
  - 1 abstract interface (`'Costed Component'`)
  - 8 calc defs (7 component + 1 allocation)
  - 7 leaf part defs with embedded `cost_model`
  - 3 assembly part defs with cost aggregation
- `models/tests/coffee_maker/design.sysml` - 57 lines
  - 1 top-level instance (`coffee_maker`)
  - Full hierarchy with parameter bindings
  - Multiplicity test (`heater [2]`)

### Pattern Validation Summary

| Pattern | Test | Result |
|---------|------|--------|
| Nested cost model | `calc cost_model` inside `part def` | PASS - compiles |
| Redefinition binding | `:>> capital_cost = cost_model.total_cost` | PASS - compiles |
| Assembly aggregation | `capital_cost = child_a.cost + child_b.cost` | PASS - compiles |
| Multiplicity | `part heater [2]` | PASS - compiles |
| Allocation costs | `calc allocation_model` in assembly | PASS - compiles |
| Abstract interface | `abstract part def 'Costed Component'` | PASS - compiles |

### Prototype Status

**PARTIAL** - SysML files created and validated. AST script and CSV still pending.

---

## Potential Risks

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| SysIDE API changes break script | Low | Medium | Pin syside version; use adapter pattern |
| Multiplicity bounds not cached | Medium | Low | Fall back to parsing bound expressions |
| Large models slow down validation | Low | Low | Filter early by calc name pattern |
| agentic-mbse imports not available | Medium | Medium | Add to PYTHONPATH or use relative imports |

## Integration Strategy

This validation script integrates with the existing `agentic-mbse` validation infrastructure:

1. **Reuses existing utilities**: `SysideAdapter`, `get_qualified_name`, `get_element_location`
2. **Follows validation patterns**: Uses `QualityCheckResult` dataclass style
3. **Complements existing levels**: Acts as domain-specific validation (cost patterns)
4. **Can be extended**: The same approach works for fusion plant models

## Validation Approach

### Level 1: Parse Validation
- `syside check` must pass for all .sysml files (exit code 0)

### Level 2: AST Traversal Validation
- `validate_ast.py` must find all 7 leaf `cost_model` calc usages
- Script must trace bindings through redefinitions
- Script must identify allocation costs at assembly level
- Script must detect multiplicity on heater[2]

### Level 3: Manual Verification
- Rollup math: sum of children + allocation = parent
- Multiplicity: heater [2] cost = 2 * unit cost
- Cross-check against expected_output.csv

---

## Design Approval

**Status**: Complete
**Validation**: All levels passing
**Completed**: Phases 1-4

### Summary

This design implements the coffee maker demo with:

1. **Phase 1-2: SysML Models** - Complete with all definitions and design instance
2. **Phase 3: validate_ast.py** - AST validation script (implemented 2026-01-12)
3. **Phase 4: expected_output.csv** - Reference cost breakdown (implemented 2026-01-12)

---

## Implementation Notes

### Phase 3 Completion (2026-01-12)

**Created:** `models/tests/coffee_maker/validate_ast.py` (~420 lines)

**Validation Results:**
- Status: PASS
- Leaf cost_models found: 7 (all component types)
- Allocation models found: 1 (Brewing System)
- Parts with multiplicity: 2 (heater[2] in library and design)

**Implementation Details:**
- Uses `agentic-mbse` infrastructure (`SysideAdapter`, `get_qualified_name`, `get_element_location`)
- Extracts multiplicity from `upper_bound.value` directly (not `cached_upper_bound` which had incorrect semantic value)
- Supports both human-readable and JSON output modes (`--json` flag)
- Validates requirements MR-007, MR-008, MR-010, MR-014

**Key Finding:**
- syside `cached_upper_bound` returned 3 instead of 2 for `heater[2]` - likely a semantic interpretation issue
- Solution: extract directly from `mult.upper_bound.value` or `mult.bounds_expression.value`

### Phase 4 Completion (2026-01-12)

**Created:** `models/tests/coffee_maker/expected_output.csv` (12 rows including header)

**Contents:**
- 7 leaf components with unit and total costs
- 1 allocation row (Brewing System fasteners/seals/wiring)
- 3 assembly rows with aggregated totals (Brewing System, Housing, Coffee Maker)

**Calculation Verification:**
- All leaf costs match design.md manual calculations
- Assembly aggregations verified: sum of children + allocation = parent
- Multiplicity handling: heater total = 2 × unit cost

---

**Status**: Implementation complete. Ready for integration testing with sysml-codegen.
