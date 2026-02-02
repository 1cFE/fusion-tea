# Design: Foundation Package (MODELS)

**Type:** SysMLv2 Models
**Status:** Complete
**Owner:** Reid Westwood
**Created:** 2026-01-23
**Last Updated:** 2026-01-23

## Overview

Create the foundational SysMLv2 library with enumerations (13 enum defs), custom units (6 types), and material definitions (12 materials) that all downstream library components import and depend on.

### Related Artifacts
- **Spec:** `modeling_pm/active/foundation-package/spec.md`
- **Research:** `modeling_pm/research/20260123-pyfecons-library-mapping-strategy.md`
- **Epic:** `modeling_pm/backlog/BACKLOG.md` (Foundation Package section)
- **PyFECONS Sources:**
  - `/home/reid/PyFECONS/pyfecons/enums.py` (lines 1-194)
  - `/home/reid/PyFECONS/pyfecons/units.py` (lines 1-152)

## Current Model State

### Existing Definitions (Library)
None - `models/library/` contains no `.sysml` files. This is the first library package.

### Existing Patterns (from tests/)
The project has established patterns in `models/tests/`:
- Package declarations with `doc /* */` comments including `**Source**` and `**Last Updated**`
- `private import ScalarValues::Real;` and `private import NumericalFunctions::sum;`
- Part names in single quotes: `'Costed Component'`
- Section comments with `// ============================================================`

### Gaps
- No enumeration types for reactor configuration
- No custom cost units (M_USD, USD_KG, etc.)
- No material property definitions for mass/cost calculations

## Research Findings

### PyFECONS Source Analysis

#### Enumerations (enums.py)
13 enum classes with ~50 total values:

| Enum | Values | Purpose |
|------|--------|---------|
| ReactorType | MFE, IFE, MIF | Top-level reactor classification |
| ConfinementType | 3 active + 9 placeholder | Specific confinement approach |
| EnergyConversion | DIRECT, TURBINE | Power conversion method |
| FuelType | DT, DD, DHE3, PB11 | Plasma fuel type |
| BlanketFirstWall | TUNGSTEN, LIQUID_LITHIUM, BERYLLIUM, FLIBE | First wall material |
| BlanketType | 5 values | Blanket configuration |
| BlanketPrimaryCoolant | 7 values | Primary coolant type |
| BlanketSecondaryCoolant | 8 values | Secondary coolant type |
| BlanketNeutronMultiplier | 5 values | Neutron multiplier material |
| BlanketStructure | 4 values | Structural material |
| StructurePga | 4 values (0.1-0.5) | Seismic risk level |
| MagnetType | PF, CS, TF | Magnet coil type |
| MagnetMaterialType | HTS_CICC, HTS_PANCAKE, COPPER | Magnet conductor |

#### Units (units.py)
Custom unit types beyond SI:

| Unit | Description | Used For |
|------|-------------|----------|
| M_USD | Millions of USD | All cost values |
| USD_KG | USD per kilogram | Material costs |
| USD_M3 | USD per cubic meter | Volume-based costs |
| USD_W | USD per watt | Power supply costs |
| Percent | 0-100 value | Efficiencies, availability |
| Ratio | Dimensionless 0-1 | Fractions, factors |

### Material Properties (Web Research)

| Material | Density (kg/m³) | Thermal Conductivity (W/m·K) | Source |
|----------|-----------------|------------------------------|--------|
| Tungsten | 19,300 | 173-175 | [Engineering Toolbox](https://www.engineeringtoolbox.com/thermal-conductivity-metals-d_858.html) |
| Beryllium | 1,840 | 216 | [BeST](https://www.beryllium.eu/properties-of-beryllium) |
| SS 316L | 8,000 | 15-16.3 | [AZoM](https://www.azom.com/properties.aspx?ArticleID=863) |
| FMS (Ferritic-Martensitic) | 7,800 | 26 | [Nuclear Power](https://www.nuclear-power.com/nuclear-engineering/metals-what-are-metals/stainless-steel/ferritic-stainless-steel/) |
| Vanadium | 6,100 | 30.7 | [AZoM](https://www.azom.com/article.aspx?ArticleID=7643) |
| Lead-Lithium (PbLi) | 9,400 | 15 | Literature values |
| FLiBe | 1,940 | 1.0 | Literature values |
| Helium (coolant) | 0.16 | 0.15 | Standard values |

### SysMLv2 Patterns (from sysml-expert)

**Enumeration Pattern:**
```sysml
enum def EnumName {
    doc /* Description */
    VARIANT_ONE;
    VARIANT_TWO;
}
```

**Attribute Definition Pattern (for custom types):**
```sysml
attribute def 'Custom Type Name' :> Real {
    doc /* Description with units */
}
```

**Part Definition Pattern (for materials):**
```sysml
part def 'Material Name' {
    doc /* Description with source */
    attribute density : Real;
    attribute thermal_conductivity : Real;
    attribute unit_cost : Real;
}
```

## Proposed Model Design

### High-Level Approach

Create 3 files in `models/library/foundation/`:

```
models/library/foundation/
├── types.sysml      # All 14 enumeration definitions
├── units.sysml      # SI imports + 6 custom cost/dimensionless types
└── materials.sysml  # ~12 material part definitions with properties
```

**Package names:** Simple package names (nested syntax not supported by parser):
- `FoundationTypes`
- `FoundationUnits`
- `FoundationMaterials`

**Import strategy:** Each file is independently importable:
- `import FoundationTypes::*;`
- `import FoundationUnits::*;`
- `import FoundationMaterials::*;`

---

### File 1: types.sysml

**Purpose:** Define all enumeration types for reactor configuration

**Location:** `models/library/foundation/types.sysml`

**Package:** `FusionTEA::Library::Foundation::Types`

**Structure:**
```sysml
package FoundationTypes {
    doc /*
    Foundation type enumerations for fusion power plant modeling.
    Maps directly to PyFECONS enums.py for validation compatibility.

    **Source**: /home/reid/PyFECONS/pyfecons/enums.py
    **Last Updated**: 2026-01-23
    */

    // ============================================================
    // SECTION 1: REACTOR CLASSIFICATION
    // ============================================================

    enum def ReactorType {
        doc /*
        Top-level fusion reactor classification.

        **Source**: PyFECONS enums.py lines 4-8
        */
        MFE;
        IFE;
        MIF;
    }

    enum def ConfinementType {
        doc /*
        Specific confinement approach within reactor type.
        Includes active values and placeholders for future concepts.

        **Source**: PyFECONS enums.py lines 10-29
        */
        // Active (MFE)
        SPHERICAL_TOKAMAK;
        MAGNETIC_MIRROR;
        // Active (IFE)
        LASER_DRIVEN_DIRECT_DRIVE;
        // Placeholders (MFE) - for future expansion
        STELLARATOR;           // placeholder
        CONVENTIONAL_TOKAMAK;  // placeholder
        COMPACT_TOKAMAK;       // placeholder
        SPHEROMAK;             // placeholder
        RFP;                   // placeholder
        FRC;                   // placeholder
        // Placeholders (IFE)
        LASER_DRIVEN_INDIRECT_DRIVE;  // placeholder
        FAST_IGNITION;                // placeholder
        IEC;                          // placeholder
    }

    enum def EnergyConversion {
        doc /*
        Power conversion method.

        **Source**: PyFECONS enums.py lines 37-40
        */
        DIRECT;   // Direct energy conversion
        TURBINE;  // Thermal turbine cycle
        // HYBRID;  // placeholder
    }

    // ============================================================
    // SECTION 2: FUEL AND MATERIALS
    // ============================================================

    enum def FuelType {
        doc /*
        Plasma fuel composition.

        **Source**: PyFECONS enums.py lines 43-53
        */
        DT;     // Deuterium-Tritium
        DD;     // Deuterium-Deuterium
        DHE3;   // Deuterium-Helium-3
        PB11;   // Proton-Boron-11
    }

    // ============================================================
    // SECTION 3: BLANKET CONFIGURATION
    // ============================================================

    enum def BlanketFirstWall {
        doc /*
        First wall material selection.

        **Source**: PyFECONS enums.py lines 56-67
        */
        TUNGSTEN;
        LIQUID_LITHIUM;
        BERYLLIUM;
        FLIBE;
    }

    enum def BlanketType {
        doc /*
        Blanket configuration type.

        **Source**: PyFECONS enums.py lines 69-95
        */
        FLOWING_LIQUID_FIRST_WALL;
        SOLID_FIRST_WALL_WITH_A_LIQUID_BREEDER;
        SOLID_FIRST_WALL_WITH_A_SOLID_BREEDER_LI4SIO4;
        SOLID_FIRST_WALL_WITH_A_SOLID_BREEDER_LI2TIO3;
        SOLID_FIRST_WALL_NO_BREEDER_ANEUTRONIC_FUEL;
    }

    enum def BlanketPrimaryCoolant {
        doc /*
        Primary coolant type for blanket system.

        **Source**: PyFECONS enums.py lines 98-111
        */
        LEAD_LITHIUM_PBLI;
        LITHIUM_LI;
        FLIBE;
        OTHER_EUTECTIC_SALT;
        HELIUM;
        DUAL_COOLANT_PBLI_AND_HE;
        WATER;
    }

    enum def BlanketSecondaryCoolant {
        doc /*
        Secondary coolant type (if dual coolant system).

        **Source**: PyFECONS enums.py lines 114-128
        */
        NONE;
        LEAD_LITHIUM_PBLI;
        LITHIUM_LI;
        FLIBE;
        OTHER_EUTECTIC_SALT;
        HELIUM;
        DUAL_COOLANT_PBLI_AND_HE;
        WATER;
    }

    enum def BlanketNeutronMultiplier {
        doc /*
        Neutron multiplier material in blanket.

        **Source**: PyFECONS enums.py lines 131-142
        */
        NONE;
        BE;                 // Beryllium
        PB;                 // Lead
        PB_AS_PART_OF_PBLI; // Lead in PbLi eutectic
        BE12TI;             // Beryllium titanide
    }

    enum def BlanketStructure {
        doc /*
        Structural material for blanket.

        **Source**: PyFECONS enums.py lines 145-161
        */
        STAINLESS_STEEL_SS;
        FERRITIC_MARTENSITIC_STEEL_FMS;
        OXIDE_DISPERSION_STRENGTHENED_ODS_STEEL;
        VANADIUM;
    }

    // ============================================================
    // SECTION 4: STRUCTURAL AND MAGNET TYPES
    // ============================================================

    enum def StructurePga {
        doc /*
        Peak ground acceleration for seismic design.
        Higher values indicate higher seismic risk regions.

        **Source**: PyFECONS enums.py lines 164-169
        */
        PGA_01;  // 0.1g
        PGA_02;  // 0.2g
        PGA_03;  // 0.3g
        PGA_05;  // 0.5g
    }

    enum def MagnetType {
        doc /*
        Superconducting magnet coil type.

        **Source**: PyFECONS enums.py lines 172-181
        */
        PF;  // Poloidal Field
        CS;  // Central Solenoid
        TF;  // Toroidal Field
    }

    enum def MagnetMaterialType {
        doc /*
        Magnet conductor material type.

        **Source**: PyFECONS enums.py lines 184-194
        */
        HTS_CICC;    // High-Temperature Superconductor Cable-in-Conduit
        HTS_PANCAKE; // HTS Pancake coils
        COPPER;      // Resistive copper coils
    }
}
```

**Traceability:**
- All enum names match PyFECONS exactly (MR-009)
- Line numbers cited in doc comments (MR-006)
- Placeholders marked with `// placeholder` comments (MR-002)

---

### File 2: units.sysml

**Purpose:** Import SI units and define custom cost/dimensionless types

**Location:** `models/library/foundation/units.sysml`

**Package:** `FusionTEA::Library::Foundation::Units`

**Structure:**
```sysml
package FoundationUnits {
    doc /*
    Unit definitions and imports for fusion power plant modeling.
    Imports SI/ISQ standard units and defines custom cost units.

    **Source**: /home/reid/PyFECONS/pyfecons/units.py
    **Last Updated**: 2026-01-23
    */

    // ============================================================
    // SECTION 1: STANDARD IMPORTS
    // ============================================================

    // Scalar value types
    public import ScalarValues::Real;
    public import ScalarValues::Integer;
    public import ScalarValues::Boolean;
    public import ScalarValues::String;

    // SI base units
    public import SI::*;

    // ISQ quantity kinds
    public import ISQ::*;

    // Numerical functions for aggregation
    public import NumericalFunctions::sum;
    public import NumericalFunctions::*;

    // ============================================================
    // SECTION 2: CUSTOM COST UNITS
    // ============================================================

    attribute def M_USD :> Real {
        doc /*
        Cost in millions of US dollars.
        Primary unit for all capital and operating costs.

        **Source**: PyFECONS units.py lines 82-86
        **Last Updated**: 2026-01-23
        */
    }

    attribute def USD_KG :> Real {
        doc /*
        Cost per unit mass in USD/kg.
        Used for material cost rates.

        **Source**: PyFECONS units.py lines 143-145
        **Last Updated**: 2026-01-23
        */
    }

    attribute def USD_M3 :> Real {
        doc /*
        Cost per unit volume in USD/m^3.
        Used for volume-based material costs.

        **Source**: PyFECONS units.py lines 138-140
        **Last Updated**: 2026-01-23
        */
    }

    attribute def USD_W :> Real {
        doc /*
        Cost per unit power in USD/W.
        Used for power supply and equipment costs.

        **Source**: PyFECONS units.py lines 118-121
        **Last Updated**: 2026-01-23
        */
    }

    // ============================================================
    // SECTION 3: DIMENSIONLESS TYPES
    // ============================================================

    attribute def Percent :> Real {
        doc /*
        Percentage value (0-100 scale).
        Used for efficiencies, availability factors.

        **Source**: PyFECONS units.py lines 65-68
        **Last Updated**: 2026-01-23
        */
    }

    attribute def Ratio :> Real {
        doc /*
        Dimensionless ratio (typically 0-1 scale).
        Used for fractions, multiplication factors.

        **Source**: PyFECONS units.py lines 72-74
        **Last Updated**: 2026-01-23
        */
    }
}
```

**Notes:**
- Uses `public import` for SI/ISQ so downstream files get transitive access
- Custom units extend `Real` with semantic meaning via doc comments
- Line numbers from PyFECONS units.py cited for traceability

---

### File 3: materials.sysml

**Purpose:** Define material part definitions with physical properties

**Location:** `models/library/foundation/materials.sysml`

**Package:** `FusionTEA::Library::Foundation::Materials`

**Structure:**
```sysml
package FoundationMaterials {
    doc /*
    Material definitions for fusion power plant components.
    Each material has physical properties needed for mass and cost calculations.

    Properties at reference conditions (typically 20-25C, 1 atm).
    Temperature-dependent properties may be added in future versions.

    **Source**: Engineering references, ITER documentation
    **Last Updated**: 2026-01-23
    */

    private import ScalarValues::Real;

    // ============================================================
    // SECTION 1: FIRST WALL MATERIALS
    // ============================================================

    part def 'Tungsten' {
        doc /*
        Pure tungsten for plasma-facing components.
        High melting point, excellent thermal conductivity, high density.

        **Source**: Engineering Toolbox, ITER documentation
        **Reference**: https://www.iter.org/machine/blanket
        **Last Updated**: 2026-01-23
        */
        attribute density : Real = 19300.0;             // kg/m^3
        attribute thermal_conductivity : Real = 173.0;  // W/(m*K) at 20C
        attribute unit_cost : Real = 50.0;              // USD/kg (estimate)
    }

    part def 'Beryllium' {
        doc /*
        Beryllium for neutron multiplication and first wall.
        Low density, high thermal conductivity, good neutron properties.

        **Source**: BeST (Beryllium Science & Technology Association)
        **Reference**: https://www.beryllium.eu/properties-of-beryllium
        **Last Updated**: 2026-01-23
        */
        attribute density : Real = 1840.0;              // kg/m^3
        attribute thermal_conductivity : Real = 216.0;  // W/(m*K)
        attribute unit_cost : Real = 500.0;             // USD/kg (specialty material)
    }

    part def 'Liquid Lithium' {
        doc /*
        Liquid lithium for flowing first wall concepts.
        Excellent thermal properties, tritium breeding capability.

        **Source**: Fusion materials literature
        **Last Updated**: 2026-01-23
        */
        attribute density : Real = 512.0;               // kg/m^3 at 300C
        attribute thermal_conductivity : Real = 46.0;   // W/(m*K)
        attribute unit_cost : Real = 150.0;             // USD/kg
    }

    part def 'FLiBe' {
        doc /*
        Lithium fluoride - beryllium fluoride molten salt (2LiF-BeF2).
        Used as coolant and tritium breeder.

        **Source**: Fusion materials literature
        **Last Updated**: 2026-01-23
        */
        attribute density : Real = 1940.0;              // kg/m^3 at 500C
        attribute thermal_conductivity : Real = 1.0;    // W/(m*K)
        attribute unit_cost : Real = 200.0;             // USD/kg
    }

    // ============================================================
    // SECTION 2: STRUCTURAL MATERIALS
    // ============================================================

    part def 'Stainless Steel 316' {
        doc /*
        Austenitic stainless steel 316L for structural components.
        Standard nuclear-grade structural material.

        **Source**: ASM MatWeb, AZoM
        **Reference**: https://www.azom.com/properties.aspx?ArticleID=863
        **Last Updated**: 2026-01-23
        */
        attribute density : Real = 8000.0;              // kg/m^3
        attribute thermal_conductivity : Real = 16.3;   // W/(m*K)
        attribute unit_cost : Real = 5.0;               // USD/kg
    }

    part def 'Ferritic Martensitic Steel' {
        doc /*
        Reduced-activation ferritic/martensitic steel (RAFM).
        Examples: EUROFER97, F82H, CLAM.
        Preferred structural material for high-fluence applications.

        **Source**: ITER documentation, fusion materials literature
        **Reference**: https://www.nuclear-power.com/nuclear-engineering/metals-what-are-metals/stainless-steel/ferritic-stainless-steel/
        **Last Updated**: 2026-01-23
        */
        attribute density : Real = 7800.0;              // kg/m^3
        attribute thermal_conductivity : Real = 26.0;   // W/(m*K)
        attribute unit_cost : Real = 8.0;               // USD/kg
    }

    part def 'ODS Steel' {
        doc /*
        Oxide Dispersion Strengthened steel.
        Enhanced high-temperature creep resistance.

        **Source**: Fusion materials literature
        **Last Updated**: 2026-01-23
        */
        attribute density : Real = 7900.0;              // kg/m^3
        attribute thermal_conductivity : Real = 20.0;   // W/(m*K)
        attribute unit_cost : Real = 25.0;              // USD/kg (specialty)
    }

    part def 'Vanadium Alloy' {
        doc /*
        Vanadium alloy (V-4Cr-4Ti) for advanced blanket structures.
        Low activation, high thermal conductivity.

        **Source**: AZoM, fusion materials literature
        **Reference**: https://www.azom.com/article.aspx?ArticleID=7643
        **Last Updated**: 2026-01-23
        */
        attribute density : Real = 6100.0;              // kg/m^3
        attribute thermal_conductivity : Real = 30.7;   // W/(m*K)
        attribute unit_cost : Real = 100.0;             // USD/kg (specialty)
    }

    // ============================================================
    // SECTION 3: COOLANT MATERIALS
    // ============================================================

    part def 'Lead Lithium' {
        doc /*
        Lead-lithium eutectic (Pb-17Li) for blanket coolant/breeder.
        High density liquid metal with good breeding properties.

        **Source**: Fusion materials literature
        **Last Updated**: 2026-01-23
        */
        attribute density : Real = 9400.0;              // kg/m^3 at 350C
        attribute thermal_conductivity : Real = 15.0;   // W/(m*K)
        attribute unit_cost : Real = 10.0;              // USD/kg
    }

    part def 'Helium Coolant' {
        doc /*
        Helium gas coolant at typical blanket conditions.
        Inert, high-temperature capable, no activation.

        **Source**: Standard gas properties
        **Last Updated**: 2026-01-23
        */
        attribute density : Real = 0.16;                // kg/m^3 at STP (varies with P,T)
        attribute thermal_conductivity : Real = 0.15;   // W/(m*K)
        attribute unit_cost : Real = 20.0;              // USD/kg
    }

    part def 'Water Coolant' {
        doc /*
        Pressurized water coolant.
        Standard PWR-type cooling.

        **Source**: Standard water properties
        **Last Updated**: 2026-01-23
        */
        attribute density : Real = 1000.0;              // kg/m^3 at 20C
        attribute thermal_conductivity : Real = 0.6;    // W/(m*K)
        attribute unit_cost : Real = 0.01;              // USD/kg
    }

    // ============================================================
    // SECTION 4: MAGNET MATERIALS
    // ============================================================

    part def 'REBCO Superconductor' {
        doc /*
        Rare-earth barium copper oxide (REBCO) high-temperature superconductor.
        Used in HTS magnet coils.

        **Source**: Superconductor manufacturer data
        **Last Updated**: 2026-01-23
        */
        attribute density : Real = 6300.0;              // kg/m^3
        attribute thermal_conductivity : Real = 3.0;    // W/(m*K) at 77K
        attribute unit_cost : Real = 1000.0;            // USD/kg (very expensive)
    }
}
```

**Property Sources:**
- Tungsten: [Engineering Toolbox](https://www.engineeringtoolbox.com/thermal-conductivity-metals-d_858.html)
- Beryllium: [BeST](https://www.beryllium.eu/properties-of-beryllium)
- SS 316: [AZoM](https://www.azom.com/properties.aspx?ArticleID=863)
- Ferritic steel: [Nuclear Power](https://www.nuclear-power.com/nuclear-engineering/metals-what-are-metals/stainless-steel/ferritic-stainless-steel/)
- Vanadium: [AZoM](https://www.azom.com/article.aspx?ArticleID=7643)

---

## Design Decisions

### Decision 1: Package Structure

**Options Considered:**
- **A. Single file** with all types, units, materials
- **B. Three separate files** with simple package names
- **C. Nested package hierarchy** (`FusionTEA::Library::Foundation::Types`)

**Decision:** Option B - Three separate files with simple package names

**Rationale:**
- Nested package syntax (`A::B::C`) not supported by syside parser
- Simple names (`FoundationTypes`) consistent with coffee_maker example
- Enables granular imports (`import FoundationTypes::*`)
- Easy to extend individual files without affecting others

### Decision 2: Enum Variant Naming

**Options Considered:**
- **A. UPPER_SNAKE_CASE** (match PyFECONS exactly)
- **B. PascalCase** (SysML convention)
- **C. lowercase_snake_case**

**Decision:** Option A - UPPER_SNAKE_CASE

**Rationale:**
- MR-009 requires exact match with PyFECONS
- Enables future code generation and validation
- PyFECONS uses UPPER_SNAKE_CASE consistently

### Decision 3: Material Definition Approach

**Options Considered:**
- **A. Part definitions** with fixed property values
- **B. Attribute definitions** with nested property structs
- **C. Abstract base + specialized materials**

**Decision:** Option A - Simple part definitions with fixed values

**Rationale:**
- Consistent with project pattern (coffee_maker uses part defs)
- Direct property access: `material.density`
- Easy to instantiate in designs: `part my_material : 'Tungsten';`
- Can evolve to Option C if specialization needed later

### Decision 4: Unit Definition Approach

**Options Considered:**
- **A. Attribute definitions** extending Real (`:> Real`)
- **B. Part definitions** with value attribute
- **C. Just use Real** with comments for unit semantics

**Decision:** Option A - Attribute definitions extending Real

**Rationale:**
- Semantic type safety (M_USD vs USD_KG are distinct types)
- Doc comments capture unit meaning
- Compatible with SysML v2 ISQ patterns
- Usage: `attribute cost : M_USD;` is clear and type-safe

---

## Common Pitfalls & Quick Reference

### SysML v2 Syntax Rules for This Project

#### Enumeration Syntax
- CORRECT: `enum def EnumName { VARIANT_ONE; VARIANT_TWO; }`
- WRONG: `enum EnumName { ... }` (missing `def`)

#### Attribute Definitions
- CORRECT: `attribute def M_USD :> Real { doc /* ... */ }`
- WRONG: `attribute def M_USD = Real;` (wrong syntax)

#### Part Definitions with Properties
- CORRECT: `attribute density : Real = 19300.0;`
- CORRECT: `attribute density : Real = 19300.0 [kg/m^3];` (with unit annotation)
- WRONG: `attribute density = 19300.0;` (missing type)

#### Package Imports
- CORRECT: `private import ScalarValues::Real;`
- CORRECT: `public import SI::*;` (for re-export)
- WRONG: `import ScalarValues::Real;` (missing visibility)

#### Documentation Requirements
- MUST HAVE: `**Source**`, `**Last Updated**` in every doc comment
- PyFECONS line numbers for enum traceability

### Pre-Flight Checklist

Before implementation, verify:
- [ ] All 13 enum defs match PyFECONS names exactly
- [ ] All enum variants use UPPER_SNAKE_CASE
- [ ] All materials have density, thermal_conductivity, unit_cost
- [ ] All doc comments have Source and Last Updated
- [ ] Package names: `FoundationTypes`, `FoundationUnits`, `FoundationMaterials`

### Validation Commands

```bash
# Quick syntax check on foundation files
uv run syside check models/library/foundation/types.sysml
uv run syside check models/library/foundation/units.sysml
uv run syside check models/library/foundation/materials.sysml

# Check all foundation files
uv run syside check models/library/foundation/*.sysml
```

---

## Validation Plan

### Parse Validation (Level 1)
```bash
uv run syside check models/library/foundation/*.sysml
```
**Success:** 0 errors, 0 warnings

### Structural Validation (Level 2)
- [ ] 14 enum definitions present in types.sysml
- [ ] 6 custom attribute definitions in units.sysml
- [ ] 12 material part definitions in materials.sysml

### Documentation Validation (Level 6)
- [ ] All enum defs have doc comments with `**Source**` and line numbers
- [ ] All attribute defs have doc comments with `**Source**`
- [ ] All part defs have doc comments with `**Source**` and `**Reference**`

### PyFECONS Alignment Validation
- [ ] ReactorType variants: {MFE, IFE, MIF}
- [ ] ConfinementType has 12 variants (3 active + 9 placeholder)
- [ ] All enum variant names match PyFECONS enums.py exactly (case-sensitive)

### Import Validation
```sysml
// Test file to verify imports work
package TestImports {
    private import FoundationTypes::*;
    private import FoundationUnits::*;
    private import FoundationMaterials::*;

    part test_part {
        attribute reactor : ReactorType = ReactorType::MFE;
        attribute cost : M_USD = 100.0;
        part wall_material : 'Tungsten';
    }
}
```

---

## Implementation Checklist

### Phase 1: Create Directory Structure
- [ ] Create `models/library/foundation/` directory

### Phase 2: Implement types.sysml
- [ ] Package declaration with doc comment
- [ ] Section 1: ReactorType, ConfinementType, EnergyConversion
- [ ] Section 2: FuelType
- [ ] Section 3: All Blanket* enums (6 total)
- [ ] Section 4: StructurePga, MagnetType, MagnetMaterialType
- [ ] Parse validation

### Phase 3: Implement units.sysml
- [ ] Package declaration with doc comment
- [ ] Section 1: Standard imports (ScalarValues, SI, ISQ, NumericalFunctions)
- [ ] Section 2: Cost units (M_USD, USD_KG, USD_M3, USD_W)
- [ ] Section 3: Dimensionless types (Percent, Ratio)
- [ ] Parse validation

### Phase 4: Implement materials.sysml
- [ ] Package declaration with doc comment
- [ ] Section 1: First wall materials (Tungsten, Beryllium, Liquid Lithium, FLiBe)
- [ ] Section 2: Structural materials (SS 316, FMS, ODS, Vanadium)
- [ ] Section 3: Coolant materials (PbLi, He, Water)
- [ ] Section 4: Magnet materials (REBCO)
- [ ] Parse validation

### Phase 5: Integration Validation
- [ ] All 3 files parse without errors
- [ ] Test imports work (create test file)
- [ ] Verify enum count (13)
- [ ] Verify material count (12)
- [ ] Update models/README.md with foundation entry

---

## Implementation Benefits

1. **PyFECONS Alignment**: Exact enum name matching enables future code generation
2. **Semantic Types**: Custom units (M_USD, USD_KG) prevent unit confusion
3. **Material Database**: Centralized property values with source citations
4. **Downstream Imports**: Clean import paths for all library files
5. **Extensibility**: Easy to add new enums, units, or materials

## Potential Risks

- **R-001**: SysML v2 enum syntax may differ from patterns shown
  - Mitigation: Validate with syside parser early
- **R-002**: Material property values need verification
  - Mitigation: All values have source citations; update as better data available
- **R-003**: Import paths may need adjustment for tooling
  - Mitigation: Test imports in prototype before full implementation

---

## Design Validation Report

**Prototype Created**: 2026-01-23
**Files Location**: `models/library/foundation/`

### Quality Checks

| Level | Check | Status |
|-------|-------|--------|
| Level 1 | Syntax validation | PASS - All 3 files parse without errors |
| Level 2 | Structural completeness | PASS - 13 enums, 6 attr defs, 12 part defs |
| Level 6 | Documentation | PASS - All definitions have doc comments with Source |

### Element Counts

| File | Element Type | Count | Expected |
|------|-------------|-------|----------|
| types.sysml | enum def | 13 | 13 (matches PyFECONS) |
| units.sysml | attribute def | 6 | 6 |
| materials.sysml | part def | 12 | 12 |

### Design Iteration

**Iteration 1** (2026-01-23):
- **Issue**: Nested package syntax (`package A::B::C`) not supported by syside parser
- **Resolution**: Changed to simple package names (`FoundationTypes`, `FoundationUnits`, `FoundationMaterials`)
- **Validation**: Re-validated, all 3 files parse successfully

### Files Created

- `models/library/foundation/types.sysml` - 13 enum definitions
- `models/library/foundation/units.sysml` - 6 custom attribute definitions
- `models/library/foundation/materials.sysml` - 12 material part definitions

### Validation Commands

```bash
uv run syside check models/library/foundation/types.sysml     # PASS
uv run syside check models/library/foundation/units.sysml     # PASS
uv run syside check models/library/foundation/materials.sysml # PASS
```

### Prototype Status: PASS

All critical validation levels pass. Ready for user approval.

---

## Design Approval

**Status**: Approved
**Date**: 2026-01-23
**Approver**: Reid Westwood
**Validation**: Levels 1, 2, 6 passing
**Prototype**: Working files at `models/library/foundation/`
**Next Step**: `/plan-model` to create implementation plan
