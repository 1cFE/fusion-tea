---
date: 2026-01-05T10:30:00-08:00
researcher: Claude
topic: "CATF MFE Model Architecture"
tags: [research, models, domain, architecture]
status: complete
last_updated: 2026-01-05
---

# Research: CATF MFE Model Architecture

**Date**: 2026-01-05 10:30 PST
**Researcher**: Claude
**Research Type**: Integration (Codebase + Models + Domain)

## Research Question

How should a CATF MFE (Compact Advanced Tokamak Fusion - Magnetic Fusion Energy) model be structured in SysMLv2 to enable LCOE estimation, following project conventions and aligning with PyFECONS?

## Summary

- **PyFECONS uses CAS (Cost Account Structure)** with ~40 cost categories organized hierarchically (CAS10-CAS90, LCOE)
- **Calculation flow is acyclic**: PowerBalance → Geometry → Subsystem Costs → Totals → LCOE
- **Project has established patterns**: Definitions in `library/`, usages in `designs/`, EXPOSE pattern for cross-file bindings
- **Recommended architecture**: 6-layer structure mirroring PyFECONS with library calc defs and design instantiation
- **Key challenge**: Mapping ~1400 lines of Python calculations to reusable SysML calc defs

## Detailed Findings

### PyFECONS Architecture

**Cost Account Hierarchy (ARPA-E Standard)**:

```
CAS10 - Pre-Construction Costs
  └── C110000-C190000 (Management, Licensing, R&D, etc.)

CAS21 - Buildings & Infrastructure
  └── C210100-C211900 (Reactor building, Turbine, Control, etc.)

CAS22 - REACTOR PLANT EQUIPMENT (Major Focus)
  ├── CAS220101 - Reactor Equipment (Vessel, blanket, radial build)
  ├── CAS220102 - Shield
  ├── CAS220103 - Coils/Magnets (TF, CS, PF)
  ├── CAS220104 - Supplementary Heating
  ├── CAS220105 - Primary Structure
  ├── CAS220106 - Vacuum System
  ├── CAS220107 - Power Supplies
  ├── CAS220108 - Divertor
  ├── CAS220109 - Direct Energy Converter
  ├── CAS220111 - Installation
  ├── CAS220119 - Scheduled Replacement
  ├── CAS2202-2207 - Supporting systems
  └── Total → CAS22

CAS23-29 - Other Plant Systems
CAS20 - Total Direct Capital Cost
CAS30-60 - Indirect, Owner's, Financial Costs
CAS70 - Annualized O&M
CAS80 - Annualized Fuel (Tritium)
CAS90 - Annualized Financial Charges
LCOE - Final Output ($/MWh)
```

**Key Input Parameters** (from PyFECONS inputs/):

| Category | Parameter | CATF Value | Unit |
|----------|-----------|------------|------|
| Basic | p_nrl (fusion power) | 2600 | MW |
| Basic | plant_lifetime | 30 | years |
| Basic | plant_availability | 0.85 | fraction |
| Power | eta_th (thermal efficiency) | 0.46 | fraction |
| Power | eta_de (direct conversion) | 0.85 | fraction |
| Power | p_input (heating) | 50 | MW |
| Geometry | axis_t (major radius) | 3.0 | m |
| Geometry | elon (elongation) | 3.0 | ratio |
| Coils | TF coils | 12 | count |
| Coils | Coil material | HTS CICC | type |

**Calculation Flow**:

```
1. PowerBalance
   Inputs: basic, power_input
   Outputs: power_table (p_alpha, p_neutron, p_th, p_the, q_eng, p_net)
   ↓
2. Geometry (CAS220101)
   Inputs: radial_build, blanket
   Outputs: radii, volumes, surface areas
   ↓
3. Subsystem Costs (CAS220102-CAS2207)
   Each depends on: power_table, geometry, component-specific inputs
   ↓
4. Plant Systems (CAS23-28)
   Depends on: power_table, component costs
   ↓
5. Totals (CAS20, CAS30-60)
   Depends on: all direct costs
   ↓
6. Annualized (CAS70-90)
   Depends on: totals, power_table
   ↓
7. LCOE
   Formula: [C90 + (C70+C80)*(1+inflation)^lifetime] / [8760*p_net*availability]
```

### Project Modeling Conventions

**From MODELING_GUIDE.md**:

1. **Definitions vs Usages**: Definitions (library) use Title Case with quotes; Usages (designs) use snake_case
2. **ADR-002**: All `calc def` in `library/` only; designs contain values and wiring
3. **EXPOSE Pattern**: `attribute exposed_value = my_calc.output;` for cross-file access
4. **Package Uniqueness**: Each file has unique package name (no merging)
5. **Documentation**: All elements require source citations

**Key Constraint from ADR-002**:
```
Design attributes can ONLY contain:
- Literal values: = 3.0 [m]
- Static expressions: = 3.14159 * 2.0
- EXPOSE pattern: = my_calc.output

NOT allowed:
- = radius * 2.0 (references design attribute)
- = calc.power * 0.95 (computation on calc output)
```

### SysMLv2 Patterns for Fusion

**Physical Flows**:
```sysml
port def ThermalPort {
    attribute temperature : ISQ::ThermodynamicTemperatureValue;
    attribute pressure : ISQ::PressureValue;
    out item thermalPower : ThermalPower;
}
```

**Calculation Chains**:
```sysml
calc def PowerBalance {
    in p_nrl : Real;
    in fuel_type : FuelType;
    out p_alpha : Real = p_nrl * 0.2;  // Simplified
    out p_neutron : Real = p_nrl - p_alpha;
}
```

**Cost Rollup**:
```sysml
part plant {
    attribute totalCost : Real = subsystem1.cost + subsystem2.cost;
    part subsystem1 { attribute cost : Real; }
    part subsystem2 { attribute cost : Real; }
}
```

**Constraints**:
```sysml
assert constraint TempLimit {
    doc /* Operating temperature must not exceed limit */
    temperature < max_temperature
}
```

## Suggested Architecture

### Library Structure (`models/library/`)

```
library/
├── foundation.sysml           # Base types, units, enums
├── calculations/
│   ├── power_balance.sysml    # Power balance calc defs
│   ├── geometry.sysml         # Volume/area calc defs
│   ├── costing.sysml          # Cost calculation patterns
│   └── lcoe.sysml             # LCOE calculation
├── definitions/
│   ├── plasma.sysml           # Plasma part defs
│   ├── magnets.sysml          # Magnet part defs (TF, CS, PF)
│   ├── blanket.sysml          # Blanket/first-wall part defs
│   ├── vacuum_system.sysml    # Vacuum vessel, divertor
│   ├── power_systems.sysml    # Power conversion, supplies
│   └── balance_of_plant.sysml # Turbine, electrical, misc
├── materials/
│   └── fusion_materials.sysml # Material properties (HTS, structural)
└── interfaces/
    └── thermal_ports.sysml    # Port definitions for flows
```

### Design Structure (`models/designs/catf/`)

```
catf/
├── parameters.sysml       # All input parameter values
├── geometry.sysml         # Radial build, dimensions
├── reactor_core.sysml     # Plasma, blanket, shield, magnets
├── power_systems.sysml    # Power conversion, cooling
├── plant.sysml            # Top-level integration
└── cost_analysis.sysml    # Cost calc usages, LCOE
```

### Package Hierarchy

```sysml
package FusionTEA {
    package Library {
        package Foundation { /* types, units */ }
        package Calculations { /* calc defs */ }
        package Definitions { /* part defs */ }
        package Materials { /* material properties */ }
    }
    package Designs {
        package CATF { /* CATF MFE design usages */ }
    }
}
```

### Layer Architecture

```
Layer 6: LCOE (Final Output)
    ↑ depends on
Layer 5: Financial (CAS30-60, CAS90)
    ↑ depends on
Layer 4: Totals (CAS20, CAS70-80)
    ↑ depends on
Layer 3: Subsystems (CAS21-29)
    ↑ depends on
Layer 2: Physics (Power Balance, Geometry)
    ↑ depends on
Layer 1: Parameters (Inputs, Materials)
```

### Key Calc Defs Required

**Power Balance** (`library/calculations/power_balance.sysml`):
```sysml
calc def PowerBalanceCalc {
    doc /*
    Power balance for MFE tokamak

    **Source**: PyFECONS
    **File**: pyfecons/costing/mfe/PowerBalance.py
    */

    in p_nrl : Real;           // Fusion power [MW]
    in fuel_type : FuelType;
    in eta_th : Real;          // Thermal efficiency
    in eta_de : Real;          // Direct conversion efficiency
    in p_input : Real;         // Heating power [MW]
    in mn : Real;              // Neutron multiplier

    // Outputs
    out p_alpha : Real;        // Alpha power
    out p_neutron : Real;      // Neutron power
    out p_th : Real;           // Total thermal power
    out p_the : Real;          // Thermal electric power
    out p_et : Real;           // Gross electric power
    out p_net : Real;          // Net electric power
    out q_eng : Real;          // Engineering Q
}
```

**Geometry** (`library/calculations/geometry.sysml`):
```sysml
calc def ToroidalVolumeCalc {
    in major_radius : Real;    // Axis to center
    in minor_radius_outer : Real;
    in minor_radius_inner : Real;

    out volume : Real = 2.0 * 3.14159 * 3.14159 * major_radius *
                        (minor_radius_outer * minor_radius_outer -
                         minor_radius_inner * minor_radius_inner);
}
```

**Costing** (`library/calculations/costing.sysml`):
```sysml
calc def MagnetCostCalc {
    in material_mass : Real;   // kg
    in material_cost_per_kg : Real;
    in structural_factor : Real;
    in cooling_cost : Real;

    out material_cost : Real = material_mass * material_cost_per_kg;
    out structural_cost : Real = material_cost * structural_factor;
    out total_cost : Real = material_cost + structural_cost + cooling_cost;
}
```

**LCOE** (`library/calculations/lcoe.sysml`):
```sysml
calc def LCOECalc {
    in capital_cost : Real;    // Total CAS10-60 [$M]
    in annual_om : Real;       // CAS70 [$M/yr]
    in annual_fuel : Real;     // CAS80 [$M/yr]
    in annual_financial : Real;// CAS90 [$M/yr]
    in p_net : Real;           // Net power [MW]
    in availability : Real;    // Capacity factor
    in lifetime : Real;        // Years
    in inflation : Real;       // Annual rate

    out lcoe : Real;           // $/MWh
    // Formula: [C90 + (C70+C80)*(1+inflation)^lifetime] / [8760*p_net*availability]
}
```

### Example Design Usage

**`designs/catf/plant.sysml`**:
```sysml
package FusionTEA::Designs::CATF {
    private import FusionTEA::Library::Calculations::*;
    private import FusionTEA::Library::Definitions::*;

    part catf_plant : 'Fusion Power Plant' {
        // Input parameters
        attribute p_nrl : Real = 2600.0 [MW];
        attribute eta_th : Real = 0.46;
        attribute plant_availability : Real = 0.85;

        // Power balance calculation
        calc power_balance : PowerBalanceCalc {
            in p_nrl = catf_plant::p_nrl;
            in eta_th = catf_plant::eta_th;
            // ... other inputs
        }

        // EXPOSE pattern for downstream access
        attribute p_net : Real = power_balance.p_net;
        attribute q_eng : Real = power_balance.q_eng;

        // Subsystems with costs
        part tokamak : 'Tokamak System' {
            part magnets : 'Magnet System' {
                attribute cost : Real;  // Calculated via MagnetCostCalc
            }
            part blanket : 'Blanket System' {
                attribute cost : Real;
            }
        }

        // Cost rollup
        attribute total_capital : Real = /* sum of subsystem costs */;

        // LCOE calculation
        calc lcoe_calc : LCOECalc {
            in capital_cost = catf_plant::total_capital;
            in p_net = catf_plant::p_net;
            in availability = catf_plant::plant_availability;
            // ...
        }

        attribute lcoe : Real = lcoe_calc.lcoe;  // EXPOSE
    }
}
```

## Feasibility Assessment

**Can be implemented**: Yes, with phased approach

**Challenges**:
1. **Volume of calculations**: PyFECONS has ~40 cost calculation modules; need to prioritize core ones
2. **Data extraction**: Some PyFECONS uses lookup tables/empirical correlations that need translation
3. **Unit handling**: SysML ISQ units need careful mapping to PyFECONS conventions

**Prerequisites**:
1. Foundation library with units and enums
2. Power balance calc def (drives most downstream calculations)
3. Geometry calculations (radial build)
4. Material properties database

**Risks**:
- Calculation fidelity: SysML expressions are simpler than Python; may need external tool integration
- Validation: Need systematic comparison with PyFECONS outputs

## Recommendations

### Phase 1: Foundation (Start Here)
1. Create `library/foundation.sysml` with:
   - FusionTEA package structure
   - Unit imports (SI, ISQ)
   - Enums: ReactorType, FuelType, ConfinementType, MagnetType
   - Base attribute definitions

2. Create `library/calculations/power_balance.sysml`:
   - PowerBalanceCalc with core power flows
   - Q-value calculations

### Phase 2: Geometry & Structure
3. Create `library/calculations/geometry.sysml`:
   - Radial build calculations
   - Volume/area computations

4. Create `library/definitions/magnets.sysml`:
   - TF, CS, PF coil part definitions
   - Magnet attributes (dimensions, material, current density)

### Phase 3: First Design
5. Create `designs/catf/`:
   - `parameters.sysml` - All CATF input values
   - `plant.sysml` - Top-level integration
   - Wire power balance and geometry calcs

6. Validate against PyFECONS:
   - Power balance outputs
   - Geometry calculations

### Phase 4: Cost Calculations
7. Add costing calc defs progressively:
   - CAS22 subsystems (magnets, blanket, vessel)
   - Rollup to CAS20
   - LCOE calculation

### Phase 5: Complete Model
8. Full subsystem coverage
9. All cost accounts
10. Comprehensive validation

## Design Decisions

1. **Cost category scope**: Focus on major cost drivers
   - Priority: CAS22 (reactor equipment ~60% of cost)
   - Then: Power balance, LCOE calculation
   - Defer: Minor cost categories until core model validated

2. **Lookup tables/material costs**: Embed in materials library
   - Material properties as attribute definitions
   - Cost factors embedded in calc defs or material part defs
   - Keeps model self-contained and traceable

3. **Physics fidelity**: Match PyFECONS level
   - Simplified scaling laws (not full physics simulation)
   - Enables direct validation against PyFECONS outputs
   - Sufficient for techno-economic analysis

4. **Integration approach**: sysml-codegen pipeline
   - Will generate Python from SysML for simulation
   - Enables systematic comparison with PyFECONS
   - Supports design space exploration

---

## Model/Code References

**PyFECONS Structure**:
- Main entry: `/home/reid/PyFECONS/pyfecons/pyfecons.py` - RunCosting, CreateReportContent
- MFE calculations: `/home/reid/PyFECONS/pyfecons/costing/mfe/`
- Power balance: `/home/reid/PyFECONS/pyfecons/costing/mfe/PowerBalance.py`
- Cost categories: `/home/reid/PyFECONS/pyfecons/costing/categories/`
- CATF example: `/home/reid/PyFECONS/customers/CATF/mfe/DefineInputs.py`

**Project Conventions**:
- Modeling guide: `/home/reid/1cfe/fusion-tea/project/MODELING_GUIDE.md`
- Overview: `/home/reid/1cfe/fusion-tea/project/OVERVIEW.md`

**SysMLv2 Patterns**:
- Reference: `/home/reid/1cfe/agentic-mbse/docs/sysmlv2/Cheatsheet/sysml_textual_notation_cheatsheet.md`
- Intro guide: `/home/reid/1cfe/agentic-mbse/docs/sysmlv2/SysML_IntroGuide_v2/full_document.md`

---

**Last Updated**: 2026-01-05
