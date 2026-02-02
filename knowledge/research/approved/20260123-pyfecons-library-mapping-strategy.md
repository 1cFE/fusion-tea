---
date: 2026-01-23T10:30:00-08:00
researcher: Claude
topic: "PyFECONS to SysMLv2 Library Mapping Strategy"
tags: [research, integration, architecture, pyfecons, library-design]
status: complete
last_updated: 2026-01-26
---

# Research: PyFECONS to SysMLv2 Library Mapping Strategy

**Date**: 2026-01-23 10:30 PST
**Researcher**: Claude
**Research Type**: Integration (Codebase + Models + Architecture)

## Research Question

How should we map PyFECONS structure into our SysMLv2 modeling library to enable:
1. Multi-concept fusion plant modeling (MFE, IFE, MIF)
2. Component reuse between designs
3. LCOE estimation with traceable cost breakdowns
4. Validation against PyFECONS calculations

## Summary

- **PyFECONS has 3 reactor types** (MFE, IFE, MIF) with ~60% shared code and ~40% design-specific modules
- **Cost Account Structure (CAS)** provides hierarchical taxonomy with 37 categories from CAS10-LCOE
- **Key branching points**: CAS220103 (coils vs lasers), CAS220104 (heating vs ignition), CAS220108 (divertor vs target factory)
- **Input structure**: 25 input categories with ~200-300 parameters per design
- **Recommended SysML architecture**: Definition/Usage split with shared library and design-specific specializations

---

## Detailed Findings

### 1. PyFECONS Architecture Overview

#### 1.1 Supported Reactor Types

| Type | Status | Confinement Types |
|------|--------|-------------------|
| **MFE** | Fully implemented | Spherical Tokamak, Magnetic Mirror |
| **IFE** | Fully implemented | Laser-Driven Direct Drive |
| **MIF** | Placeholder only | Not yet implemented |

Additional confinement types are defined but commented out:
- MFE: Stellarator, conventional tokamak, compact tokamak, spheromak, RFP, FRC
- IFE: Indirect drive, fast ignition, IEC, projectile
- MIF: Z-pinch, plasma jet, theta pinch

#### 1.2 Code Organization

```
pyfecons/
├── inputs/              # 25 input parameter modules
│   ├── all_inputs.py    # Master container (AllInputs)
│   ├── basic.py         # Reactor type, power, fuel
│   ├── radial_build.py  # 14 geometric layers
│   ├── coils.py         # Magnet specifications
│   ├── blanket.py       # Breeding blanket config
│   └── ... (20 more)
├── costing/
│   ├── calculations/    # SHARED cost calculations (70%)
│   ├── categories/      # 37 CAS data classes
│   ├── accounting/      # NPV, power tables
│   ├── mfe/             # MFE-specific (30%)
│   │   ├── cas22/       # MFE reactor equipment
│   │   └── PowerBalance.py
│   └── ife/             # IFE-specific (30%)
│       ├── cas22/       # IFE reactor equipment
│       └── PowerBalance.py
├── data.py              # Output container (Data class)
└── enums.py             # Type enumerations
```

**Code Reuse Statistics**:
- ~70 shared files (calculations, categories, accounting, models)
- ~48 design-specific files (MFE + IFE implementations)
- Approximately 60% code sharing between designs

### 2. Cost Account Structure (CAS) Hierarchy

The CAS provides a complete cost taxonomy:

```
CAS10 - Pre-Construction Costs
├── C110000 - Land and Land Rights
├── C120000 - Site Permits
├── C130000 - Plant Licensing
├── C140000 - Plant Permits
├── C150000 - Plant Studies
├── C160000 - Plant Reports
├── C170000 - Other Pre-Construction
└── C190000 - Contingency

CAS20 - Direct Costs (aggregates CAS21-29)

CAS21 - Buildings and Structures
├── C210100-C211900 (19 building categories)
└── C210000 - Total

CAS22 - Reactor Plant Equipment [MAJOR COMPLEXITY]
├── CAS220101 - Reactor Equipment (geometry, volumes)
├── CAS220102 - Radiation Shield
├── CAS220103 - Coils (MFE) / Lasers (IFE)        ★ BRANCH POINT
├── CAS220104 - Heating (MFE) / Ignition (IFE)    ★ BRANCH POINT
├── CAS220105 - Primary Structure
├── CAS220106 - Vacuum System
├── CAS220107 - Power Supplies
├── CAS220108 - Divertor (MFE) / Target (IFE)     ★ BRANCH POINT
├── CAS220109 - Direct Energy Converter
├── CAS220111 - Installation
├── CAS220119 - Scheduled Replacement
├── CAS220200 - Main/Secondary Coolant
├── CAS220300 - Auxiliary Cooling
├── CAS220400 - Radioactive Waste
├── CAS220500 - Fuel Handling
├── CAS220600 - Other Equipment
└── CAS220700 - Instrumentation & Control

CAS23 - Turbine Plant Equipment (shared)
CAS24 - Electric Plant Equipment (shared)
CAS25 - Miscellaneous Plant Equipment (shared)
CAS26 - Heat Rejection System (shared)
CAS27 - Special Materials (shared)
CAS28 - Digital Twin (shared)
CAS29 - Contingency (shared)

CAS30 - Capitalized Indirect Service Costs
CAS40 - Capitalized Owner Costs
CAS50 - Capitalized Supplementary Costs
CAS60 - Capitalized Financial Costs
CAS70 - Annualized O&M
CAS80 - Annualized Fuel (MFE vs IFE versions)
CAS90 - Annualized Financial Costs

LCOE - Levelized Cost of Electricity (final output)
```

### 3. Component Reuse Patterns in PyFECONS

#### 3.1 Shared Components (Used by All Reactor Types)

| Component | Files | Description |
|-----------|-------|-------------|
| Buildings | `cas21_buildings.py` | Standard facility structures |
| Turbine Plant | `cas23_turbine_plant_equipment.py` | Thermal conversion |
| Electrical | `cas24_electric_plant_equipment.py` | Grid connection |
| Heat Rejection | `cas26_heat_rejection.py` | Cooling towers |
| Financials | `cas30-60, cas90` | Cost accounting |
| LCOE Calc | `lcoe.py` | Final rollup |
| Geometry | `volume.py`, `thermal.py` | Physics utilities |

#### 3.2 Design-Specific Components

**MFE-Specific** (`pyfecons/costing/mfe/`):
- `cas220103_coils.py` - Complex magnet costing (~600 lines)
- `cas220104_supplementary_heating.py` - NBI/ICRF systems
- `cas220106_vacuum_system.py` - Tokamak vacuum
- `cas220107_power_supplies.py` - Magnet power
- `cas220108_divertor.py` - Plasma exhaust
- `PowerBalance.py` - MFE power flow

**IFE-Specific** (`pyfecons/costing/ife/`):
- `cas220103_lasers.py` - Laser system costing
- `cas220104_ignition_lasers.py` - Ignition laser
- `cas220106_vacuum_systems.py` - Chamber vacuum
- `cas220107_power_supplies.py` - Capacitor power
- `cas220108_target_factory.py` - Fuel capsules
- `PowerBalance.py` - IFE power flow

#### 3.3 Reuse Mechanisms

1. **Dataclass Inheritance**: All CAS categories inherit from `TemplateProvider`
2. **Function Composition**: No deep class hierarchies; reuse via parameters
3. **Enum-Based Branching**: `ReactorType` determines calculation path
4. **Union Types**: `Data` class uses `Union[CAS220103Coils, CAS220103Lasers]`
5. **Factory Pattern**: Conditional initialization in `Data.__post_init__()`

### 4. Input Data Model

#### 4.1 Input Categories (25 modules)

| Category | Key Parameters | Shared/Specific |
|----------|----------------|-----------------|
| `Basic` | reactor_type, power, fuel, lifetime | Shared |
| `RadialBuild` | 14 layer thicknesses | Shared |
| `Coils` | magnet specs (list of Magnet) | MFE |
| `Lasers` | beamlet curves, NIF reference | IFE |
| `Blanket` | first_wall, coolant, breeder | Shared |
| `Shield` | material fractions | Shared |
| `PowerInput` | efficiencies, powers | Shared |
| `VacuumSystem` | pump specs, temperatures | Shared |
| `PowerSupplies` | cost_per_watt, capacitor specs | Shared |
| `SupplementaryHeating` | NBI/ICRF power | MFE |
| `TargetFactory` | learning curve | IFE |
| `Financial` | discount rates, inflation | Shared |
| `LsaLevels` | maturity cost factors | Shared |

#### 4.2 Type System

**Physical Units**: `Meters`, `MW`, `K`, `Amperes`, `Megapascal`
**Cost Units**: `M_USD`, `USD_KG`, `USD_M3`
**Dimensionless**: `Ratio`, `Percent`, `Count`

#### 4.3 Enumeration Categories

```python
ReactorType: MFE, IFE, MIF
ConfinementType: SPHERICAL_TOKAMAK, MAGNETIC_MIRROR, LASER_DRIVEN_DIRECT_DRIVE
FuelType: DT, DD, DHE3, PB11
EnergyConversion: DIRECT, TURBINE
MagnetType: TF, CS, PF
MagnetMaterialType: HTS_CICC, HTS_PANCAKE, COPPER
BlanketFirstWall: TUNGSTEN, LIQUID_LITHIUM, BERYLLIUM, FLIBE
BlanketType: 5 options (flowing/solid variants)
BlanketPrimaryCoolant: 7 options
```

### 5. Calculation Flow

```
Inputs (AllInputs)
    │
    ├─► PowerBalance (reactor-specific)
    │   └─► PowerTable (p_alpha, p_neutron, p_th, p_net, q_eng)
    │
    ├─► Geometry (CAS220101)
    │   └─► Radii, volumes, surface areas
    │
    ├─► Subsystem Costs (CAS220102-220700)
    │   ├─► Shared: shield, structure, vacuum, cooling
    │   └─► Specific: coils/lasers, heating/ignition, divertor/target
    │
    ├─► Plant Systems (CAS23-29)
    │   └─► Turbine, electrical, misc, heat rejection
    │
    ├─► Totals (CAS20, CAS30-60)
    │   └─► Direct cost, indirect costs, financials
    │
    ├─► Annualized (CAS70-90)
    │   └─► O&M, fuel, financial charges
    │
    └─► LCOE
        └─► $/MWh final output
```

---

## Recommended SysML Library Architecture

### 6. Library Structure Proposal

Based on PyFECONS patterns, our modeling conventions (MODELING_GUIDE.md), and the **validated cost modeling patterns** (COST_MODELING.md):

```
models/
├── library/
│   ├── foundation/
│   │   ├── types.sysml              # Enums: ReactorType, FuelType, etc.
│   │   ├── units.sysml              # SI imports, custom units
│   │   ├── materials.sysml          # Material part defs with properties
│   │   └── costing.sysml            # 'Costed Component' abstract interface ✓
│   │
│   ├── definitions/
│   │   ├── plant.sysml              # 'Fusion Power Plant' top-level
│   │   ├── power_core/
│   │   │   ├── plasma.sysml         # 'Plasma' part def
│   │   │   ├── blanket.sysml        # 'Blanket System' variants
│   │   │   ├── shield.sysml         # 'Radiation Shield'
│   │   │   └── vacuum_vessel.sysml  # 'Vacuum Vessel'
│   │   ├── magnets/                 # MFE-specific
│   │   │   ├── coil.sysml           # 'Magnet Coil' base def
│   │   │   ├── tf_coil.sysml        # 'TF Coil' specialization
│   │   │   ├── pf_coil.sysml        # 'PF Coil' specialization
│   │   │   └── cs_coil.sysml        # 'Central Solenoid'
│   │   ├── lasers/                  # IFE-specific
│   │   │   ├── laser_system.sysml   # 'Laser System' base
│   │   │   └── target_factory.sysml # 'Target Factory'
│   │   ├── heating/
│   │   │   ├── heating_system.sysml # 'Heating System' base
│   │   │   ├── nbi.sysml            # 'Neutral Beam Injection'
│   │   │   └── icrf.sysml           # 'Ion Cyclotron RF'
│   │   ├── exhaust/
│   │   │   └── divertor.sysml       # 'Divertor' (MFE)
│   │   ├── power_conversion/
│   │   │   ├── power_supplies.sysml # 'Power Supply System'
│   │   │   ├── turbine.sysml        # 'Turbine Plant'
│   │   │   └── direct_converter.sysml # 'Direct Energy Converter'
│   │   └── bop/                     # Balance of Plant
│   │       ├── buildings.sysml      # 'Building' definitions
│   │       ├── electrical.sysml     # 'Electrical Plant'
│   │       └── cooling.sysml        # 'Heat Rejection System'
│   │
│   └── calculations/
│       ├── power_balance/
│       │   ├── power_balance.sysml  # Generic 'PowerBalanceCalc'
│       │   ├── mfe_power_balance.sysml  # MFE-specific
│       │   └── ife_power_balance.sysml  # IFE-specific
│       ├── geometry/
│       │   ├── toroidal_volume.sysml    # Volume calculations
│       │   └── radial_build.sysml       # Layer geometry
│       ├── costing/
│       │   ├── cas_rollup.sysml     # Cost aggregation patterns
│       │   ├── component_cost.sysml # Unit cost calculations
│       │   └── learning_curve.sysml # Nth-of-a-kind reduction
│       └── lcoe/
│           └── lcoe.sysml           # LCOE calculation
│
├── designs/
│   ├── catf_mfe/                    # CATF Tokamak
│   │   ├── parameters.sysml         # Input values
│   │   ├── radial_build.sysml       # Geometry instance
│   │   ├── reactor_core.sysml       # Core assembly
│   │   ├── magnets.sysml            # Coil instances
│   │   ├── power_systems.sysml      # Conversion systems
│   │   ├── plant.sysml              # Top-level integration
│   │   └── cost_analysis.sysml      # Cost calculations
│   │
│   ├── catf_ife/                    # CATF Laser Fusion
│   │   ├── parameters.sysml
│   │   ├── ... (similar structure)
│   │   └── laser_system.sysml       # IFE-specific
│   │
│   └── stellarator/                 # Future design
│       └── ... (when ready)
│
└── tests/
    ├── power_balance_test.sysml
    ├── geometry_test.sysml
    └── cost_rollup_test.sysml
```

### 7. Definition Mapping: PyFECONS → SysML

#### 7.1 Input Classes → Part Definitions

| PyFECONS Input | SysML Part Definition | Location |
|----------------|----------------------|----------|
| `Basic` | `'Fusion Power Plant'` attributes | `library/definitions/plant.sysml` |
| `RadialBuild` | `'Radial Build'` | `library/definitions/power_core/radial_build.sysml` |
| `Coils` | `'Magnet System'` containing `'Magnet Coil'` | `library/definitions/magnets/` |
| `Magnet` | `'Magnet Coil'`, `'TF Coil'`, etc. | `library/definitions/magnets/` |
| `Blanket` | `'Blanket System'` | `library/definitions/power_core/blanket.sysml` |
| `Shield` | `'Radiation Shield'` | `library/definitions/power_core/shield.sysml` |
| `VacuumSystem` | `'Vacuum Vessel'` | `library/definitions/power_core/vacuum_vessel.sysml` |
| `PowerInput` | Part of `'Fusion Power Plant'` | Various |
| `SupplementaryHeating` | `'Heating System'`, `'NBI'`, `'ICRF'` | `library/definitions/heating/` |
| `Lasers` | `'Laser System'` | `library/definitions/lasers/` |
| `TargetFactory` | `'Target Factory'` | `library/definitions/lasers/` |
| `Financial` | Analysis parameters | `library/calculations/lcoe/` |

#### 7.2 Enums → SysML Enumerations

```sysml
// library/foundation/types.sysml
package FusionTEA::Library::Foundation {
    enum def ReactorType {
        MFE;    // Magnetic Fusion Energy
        IFE;    // Inertial Fusion Energy
        MIF;    // Magneto-Inertial Fusion
    }

    enum def FuelType {
        DT;     // Deuterium-Tritium
        DD;     // Deuterium-Deuterium
        DHE3;   // Deuterium-Helium-3
        PB11;   // Proton-Boron-11
    }

    enum def MagnetType {
        TF;     // Toroidal Field
        CS;     // Central Solenoid
        PF;     // Poloidal Field
    }

    // ... additional enums
}
```

#### 7.3 CAS Categories → Calc Definitions

| CAS Category | SysML Calc Definition | Notes |
|--------------|----------------------|-------|
| Power Balance | `calc def 'Power Balance Calc'` | Reactor-specific specializations |
| CAS220101 | `calc def 'Reactor Equipment Cost Calc'` | Geometry → volumes → costs |
| CAS220103 (coils) | `calc def 'Magnet System Cost Calc'` | MFE only |
| CAS220103 (lasers) | `calc def 'Laser System Cost Calc'` | IFE only |
| CAS21 | `calc def 'Building Cost Calc'` | Shared |
| CAS22 Total | `calc def 'Reactor Equipment Total Calc'` | Aggregates sub-costs |
| CAS20 | `calc def 'Direct Cost Calc'` | Sum of CAS21-29 |
| LCOE | `calc def 'LCOE Calc'` | Final output |

### 8. Component Reuse Strategy

#### 8.1 Shared Definitions (Library)

Define **concept-agnostic** components usable by any reactor type. **All costed components must specialize `'Costed Component'`** to enable automatic cost rollup:

```sysml
// REQUIRED: Import NumericalFunctions for cost aggregation
private import NumericalFunctions::sum;

// Shared: Any reactor has power conversion
part def 'Power Conversion System' :> 'Costed Component' {
    attribute thermal_efficiency : Real;
    attribute gross_electric_power : ISQ::PowerValue;
    attribute net_electric_power : ISQ::PowerValue;

    // Embedded cost model (leaf pattern)
    calc cost_model : PowerConversionCostCalc {
        in efficiency = thermal_efficiency;
        in power = gross_electric_power;
    }

    :>> capital_cost = cost_model.total_cost;
    :>> raw_material_cost = cost_model.material_cost;
    :>> fabrication_cost = cost_model.fab_cost;
    :>> installation_cost = cost_model.install_cost;
    :>> idiot_index = cost_model.idiot_index;
}

// Shared: Any reactor needs cooling
part def 'Heat Rejection System' :> 'Costed Component' {
    attribute heat_load : ISQ::PowerValue;
    attribute cooling_capacity : ISQ::PowerValue;

    calc cost_model : HeatRejectionCostCalc { /* ... */ }
    // Cost attribute bindings follow same pattern
}
```

**Reference**: See `modeling_pm/docs/COST_MODELING.md` for the complete validated pattern.

#### 8.2 Specialization for Reactor Types

Use SysML specialization for reactor-specific components:

```sysml
// Base definition (shared)
part def 'Primary Heating System' {
    attribute input_power : ISQ::PowerValue;
    attribute heating_efficiency : Real;
}

// MFE specialization
part def 'Neutral Beam Injection' :> 'Primary Heating System' {
    attribute beam_energy : ISQ::EnergyValue;
    attribute number_of_beamlines : Integer;
}

// MFE specialization
part def 'Ion Cyclotron RF' :> 'Primary Heating System' {
    attribute frequency : ISQ::FrequencyValue;
    attribute antenna_count : Integer;
}

// IFE "heating" equivalent
part def 'Laser Driver' :> 'Primary Heating System' {
    attribute laser_energy : ISQ::EnergyValue;
    attribute pulse_frequency : ISQ::FrequencyValue;
}
```

#### 8.3 Design Assembly Patterns

Designs compose library definitions:

```sysml
// designs/catf_mfe/reactor_core.sysml
package FusionTEA::Designs::CATF_MFE {
    import FusionTEA::Library::Definitions::*;

    part catf_reactor : 'Tokamak Reactor' {
        // MFE-specific components
        part magnet_system : 'Magnet System' {
            part tf_coils[12] : 'TF Coil' { ... }
            part cs_coil : 'Central Solenoid' { ... }
            part pf_coils[6] : 'PF Coil' { ... }
        }
        part heating : 'Neutral Beam Injection' { ... }
        part divertor : 'Divertor' { ... }

        // Shared components
        part blanket : 'Blanket System' { ... }
        part shield : 'Radiation Shield' { ... }
        part vessel : 'Vacuum Vessel' { ... }
    }
}
```

### 9. Mapping to CAS Cost Structure

**IMPORTANT**: This section describes the **validated cost modeling pattern** from the Coffee Maker de-risking effort. All fusion components must follow this pattern to enable automatic cost rollup and multi-category visibility.

**Reference**: `modeling_pm/docs/COST_MODELING.md` is the authoritative guide.

#### 9.1 The 'Costed Component' Interface

Every cost-bearing component must specialize the abstract `'Costed Component'` interface:

**Implementation**: See `models/library/foundation/costing.sysml` for production definition.

```sysml
// library/foundation/costing.sysml
private import Costing::*;  // Provides CASCategory enum and 'Costed Component'

abstract part def 'Costed Component' {
    doc /*
    Abstract interface for all cost-bearing components.
    Every costed part must specialize this and provide values for cost attributes.

    **Source**: Validated by Coffee Maker demo model
    **Reference**: modeling_pm/docs/COST_MODELING.md
    */

    // CAS category for cost reporting (type-safe enum)
    attribute cas_category : CASCategory;   // Maps to PyFECONS CAS hierarchy

    // Required cost attributes (aligned to CAS multi-category breakdown)
    attribute capital_cost : Real;          // Total cost for LCOE calculation
    attribute raw_material_cost : Real;     // Material portion for cost driver analysis
    attribute fabrication_cost : Real;      // Manufacturing labor/overhead
    attribute installation_cost : Real;     // On-site assembly and integration

    // Derived efficiency metric (SpaceX "idiot index")
    attribute idiot_index : Real;           // capital_cost / raw_material_cost
}
```

> **Note**: The `CASCategory` enum is defined in `costing.sysml` with all 35 PyFECONS CAS codes.

#### 9.2 Leaf Part Pattern (Direct Calculation)

Leaf parts compute their own cost via an embedded `cost_model` calc usage:

```sysml
part def 'Magnet Coil' :> 'Costed Component' {
    // CAS category - inherited by specializations (TF, PF, CS all roll up to CAS220103)
    :>> cas_category = CASCategory::CAS220103;

    // Physical attributes
    attribute radius : ISQ::LengthValue;
    attribute mass : ISQ::MassValue;
    attribute material_type : MagnetMaterialType;

    // Embedded cost model - computes cost from physical parameters
    calc cost_model : MagnetCoilCostCalc {
        in coil_mass = mass;
        in mat_type = material_type;
        // Cost factors have defaults in calc def
    }

    // Expose cost outputs via redefinition binding
    :>> capital_cost = cost_model.total_cost;
    :>> raw_material_cost = cost_model.material_cost;
    :>> fabrication_cost = cost_model.fab_cost;
    :>> installation_cost = cost_model.install_cost;
    :>> idiot_index = cost_model.idiot_index;
}
```

#### 9.3 Assembly Part Pattern (Aggregation)

Assembly parts aggregate costs from their children using `sum()`:

```sysml
private import NumericalFunctions::sum;  // REQUIRED IMPORT

part def 'Magnet System' :> 'Costed Component' {
    // CAS category for this assembly (same as children for CAS220103)
    :>> cas_category = CASCategory::CAS220103;

    // Child parts (with multiplicity)
    part tf_coils : 'TF Coil' [12];
    part pf_coils : 'PF Coil' [6];
    part cs_coil : 'Central Solenoid';

    // AUTOMATIC aggregation using sum()
    :>> capital_cost =
        sum(tf_coils.capital_cost) +
        sum(pf_coils.capital_cost) +
        cs_coil.capital_cost;

    :>> raw_material_cost =
        sum(tf_coils.raw_material_cost) +
        sum(pf_coils.raw_material_cost) +
        cs_coil.raw_material_cost;

    :>> fabrication_cost =
        sum(tf_coils.fabrication_cost) +
        sum(pf_coils.fabrication_cost) +
        cs_coil.fabrication_cost;

    :>> installation_cost =
        sum(tf_coils.installation_cost) +
        sum(pf_coils.installation_cost) +
        cs_coil.installation_cost;

    :>> idiot_index = capital_cost / raw_material_cost;
}
```

#### 9.4 Allocation Costs (Assembly-Level Minor Items)

For items not worth modeling as separate parts (<5% of assembly cost):

```sysml
calc def AllocationCostCalc {
    in attribute child_count : Real;
    in attribute total_child_mass : Real;

    in attribute fastener_cost_per_child : Real default := 0.50;
    in attribute seal_cost_per_child : Real default := 0.30;
    in attribute wiring_cost_per_kg : Real default := 2.0;

    out attribute total_allocation : Real =
        child_count * fastener_cost_per_child +
        child_count * seal_cost_per_child +
        total_child_mass * wiring_cost_per_kg;

    out attribute material_portion : Real = total_allocation * 0.8;
}

part def 'Reactor Core Assembly' :> 'Costed Component' {
    part blanket : 'Blanket System';
    part shield : 'Radiation Shield';

    // Allocation for minor items
    calc allocation_model : AllocationCostCalc {
        in child_count = 2.0;
        in total_child_mass = 1000.0;  // kg
    }

    :>> capital_cost =
        blanket.capital_cost +
        shield.capital_cost +
        allocation_model.total_allocation;

    :>> raw_material_cost =
        blanket.raw_material_cost +
        shield.raw_material_cost +
        allocation_model.material_portion;
    // ... other aggregations
}
```

#### 9.5 Cost Attribute Pattern (DEPRECATED)

~~Every costed component has a cost attribute:~~

**NOTE**: The inline cost attribute pattern below is **deprecated**. Use the `'Costed Component'` interface pattern above instead, which provides:
- Consistent multi-category breakdown
- Automatic cost rollup via `sum()`
- Idiot index tracking for manufacturing efficiency
- Clean separation of physical attributes from cost attributes

#### 9.6 Cost Rollup Hierarchy (CAS Mapping)

The `'Costed Component'` pattern enables automatic rollup through the CAS hierarchy:

```
Plant Total Cost (CAS Total)          ← 'Fusion Power Plant'.capital_cost
├── Pre-Construction (CAS10)
├── Direct Costs (CAS20)
│   ├── Buildings (CAS21)             ← sum(building.capital_cost)
│   ├── Reactor Equipment (CAS22)
│   │   ├── CAS220101                 ← 'Reactor Core'.capital_cost
│   │   ├── CAS220102                 ← 'Radiation Shield'.capital_cost
│   │   ├── CAS220103                 ← 'Magnet System'.capital_cost (sum of coils)
│   │   ├── CAS220104                 ← 'Heating System'.capital_cost
│   │   └── ... (other CAS22 items)
│   ├── Turbine (CAS23)               ← 'Turbine Plant'.capital_cost
│   └── ... (CAS24-29)
├── Indirect (CAS30-60)
└── Annualized (CAS70-90)
```

Each CAS line item corresponds to a `capital_cost` attribute from a `'Costed Component'` part.

### 10. Implementation Roadmap

#### Phase 1: Foundation (Week 1) ✓ COMPLETE
1. **Create foundation package** (`library/foundation/`)
   - `types.sysml` - All enumerations (ReactorType, FuelType, etc.) ✓
   - `units.sysml` - SI imports, custom unit aliases ✓
   - `materials.sysml` - Material definitions with properties ✓
   - **`costing.sysml` - `'Costed Component'` abstract interface with `CASCategory` enum** ✓ (see Section 9.1)

2. **Create power balance** (`library/calculations/power_balance/`)
   - Generic `'Power Balance Calc'` with inputs/outputs ✓
   - Validate against PyFECONS PowerBalance.py ✓

**NOTE on costing.sysml**: This file defines the `'Costed Component'` interface that all cost-bearing parts must specialize. See `modeling_pm/docs/COST_MODELING.md` for the validated pattern.

#### Phase 2: Core Components (Week 2-3)
3. **Radial build and geometry** (`library/definitions/power_core/`)
   - `'Radial Build'` with layer thicknesses
   - Volume and area calculations

4. **Magnet system** (MFE) (`library/definitions/magnets/`)
   - `'Magnet Coil' :> 'Costed Component'` base definition with embedded cost_model
   - TF, CS, PF specializations (inherit cost pattern)
   - `'Magnet System' :> 'Costed Component'` assembly with sum() aggregation

5. **Blanket and shield** (`library/definitions/power_core/`)
   - `'Blanket System' :> 'Costed Component'` with material options
   - `'Radiation Shield' :> 'Costed Component'`

**IMPORTANT**: All part definitions in Phase 2 must:
- Specialize `'Costed Component'`
- Include embedded `cost_model` calc usage (leaf parts) OR `sum()` aggregation (assemblies)
- Bind all five cost attributes (`:>>` redefinition pattern)

#### Phase 3: First Design (Week 4)
6. **CATF MFE design** (`designs/catf_mfe/`)
   - Wire all parameters from PyFECONS `DefineInputs.py`
   - Instantiate components
   - Run power balance calculation

7. **Validation checkpoint**
   - Compare SysML outputs with PyFECONS for:
     - Power balance (p_net, q_eng)
     - Volumes and geometry
     - Initial cost estimates

#### Phase 4: Cost Calculations (Week 5-6)
8. **CAS22 subsystems**
   - Add cost calc defs for each CAS220xxx category
   - Wire costs to components

9. **Cost rollup**
   - CAS21-29 aggregation
   - CAS20 total direct cost

10. **LCOE calculation**
    - Financial parameters
    - Final LCOE output

#### Phase 5: Multi-Concept (Week 7+)
11. **IFE variant** (`designs/catf_ife/`)
    - Laser system definitions
    - Target factory
    - IFE power balance

12. **Shared vs specific analysis**
    - Refine library based on lessons learned
    - Optimize for maximum reuse

---

## Feasibility Assessment

### Can Be Implemented: YES

**Strengths**:
- PyFECONS provides clear component taxonomy (CAS structure)
- Input dataclasses map naturally to SysML part definitions
- Calculation functions map to SysML calc definitions
- Existing reuse patterns (shared vs specific) translate well

**Challenges**:
1. **Complexity of magnet costing**: ~600 lines in PyFECONS; need multiple calc defs
2. **Lookup tables**: Material costs, PGA costs need embedded data
3. **Learning curves**: Nth-of-a-kind economics need calc support
4. **Physics fidelity**: SysML expressions are simpler than Python

**Mitigations**:
- Start with simplified calculations, add complexity progressively
- Embed material data in `materials.sysml`
- Use EXPOSE pattern consistently for calc outputs
- Validate incrementally against PyFECONS

---

## Recommendations

### Immediate Next Steps

1. **Create foundation package first** - types, units, materials
2. **Start with power balance** - it drives most downstream calculations
3. **Build CATF MFE incrementally** - add components as library definitions mature
4. **Validate early and often** - compare outputs at each stage

### Architecture Decisions

1. **Strict Definition/Usage separation** per MODELING_GUIDE
2. **One CAS category = one calc def** for traceability
3. **EXPOSE pattern everywhere** for cross-file binding
4. **Shared components in library root**, reactor-specific in subdirectories
5. **Design files contain only values and wiring** (ADR-002)

### Key Files to Create First

| Priority | File | Content |
|----------|------|---------|
| 1 | `library/foundation/types.sysml` | All enumerations |
| 2 | `library/foundation/units.sysml` | Unit imports |
| 3 | `library/foundation/materials.sysml` | Material properties |
| **4** | **`library/foundation/costing.sysml`** | **`'Costed Component'` interface** |
| 5 | `library/calculations/power_balance/power_balance.sysml` | Power flow calc |
| 6 | `library/definitions/plant.sysml` | Top-level plant definition |
| 7 | `designs/catf_mfe/parameters.sysml` | Input parameter values |

---

## Code/Model References

### PyFECONS Key Files
- `/home/reid/PyFECONS/pyfecons/inputs/all_inputs.py` - Input container
- `/home/reid/PyFECONS/pyfecons/data.py` - Output container with CAS fields
- `/home/reid/PyFECONS/pyfecons/enums.py` - Type enumerations
- `/home/reid/PyFECONS/pyfecons/costing/mfe/mfe.py` - MFE orchestrator
- `/home/reid/PyFECONS/pyfecons/costing/mfe/PowerBalance.py` - MFE power balance
- `/home/reid/PyFECONS/pyfecons/costing/calculations/` - Shared calculations
- `/home/reid/PyFECONS/customers/CATF/mfe/DefineInputs.py` - CATF example

### Project References
- `/home/reid/1cfe/fusion-tea/modeling_pm/MODELING_GUIDE.md` - SysML conventions
- **`/home/reid/1cfe/fusion-tea/modeling_pm/docs/COST_MODELING.md`** - **Validated cost modeling patterns (REQUIRED READING)**
- `/home/reid/1cfe/fusion-tea/modeling_pm/backlog/epic-cost-patterns-derisking.md` - Cost pattern de-risking epic (completed)
- `/home/reid/1cfe/fusion-tea/models/tests/coffee_maker/` - Validated cost pattern demo model
- `/home/reid/1cfe/fusion-tea/modeling_pm/research/20260105-103000_catf-mfe-architecture.md` - Prior research

---

## Open Questions

1. **MIF support timeline**: Should we design library to support MIF from the start, or defer?
2. **Calculation fidelity**: Which PyFECONS calculations need full fidelity vs. simplified versions?
3. **Learning curves**: How to model Nth-of-a-kind cost reduction in SysML?
4. ~~**Code generation**: Will we use sysml-codegen for validation against PyFECONS?~~ **ANSWERED**: Custom evaluation scripts (e.g., `generate_costs.py`) handle cost evaluation; sysml-codegen handles structural extraction.

---

## Revision History

| Date | Changes |
|------|---------|
| 2026-01-23 | Initial strategy document |
| 2026-01-26 | **Integrated validated 'Costed Component' pattern** from Coffee Maker de-risking. Updated Sections 6, 8, 9, 10. Added references to COST_MODELING.md. |

---

**Last Updated**: 2026-01-26
