# Design: Phase 1 - Foundation Library (MODELS)

**Type:** SysMLv2 Models
**Status:** Draft
**Owner:** Reid Westwood
**Created:** 2026-01-05
**Last Updated:** 2026-01-05

## Overview

Create the foundational SysML v2 library infrastructure for FusionTEA: package structure, standard imports, enumerations (FuelType, ReactorType, ConfinementType, MagnetType), and the core PowerBalanceCalc definition with full fidelity to PyFECONS (17 inputs, 16 outputs, fuel-type-dependent alpha power).

### Related Artifacts
- **Spec:** `project/active/phase1-foundation/spec.md`
- **Research:** `project/research/20260105-103000_catf-mfe-architecture.md`
- **Epic:** `project/backlog/BACKLOG.md` (Phase 1 - Foundation Library)
- **PyFECONS Sources:**
  - `/home/reid/PyFECONS/pyfecons/costing/mfe/PowerBalance.py`
  - `/home/reid/PyFECONS/pyfecons/enums.py`

## Current Model State

### Existing Definitions (Library)
- **None** - `models/library/` is empty, no `.sysml` files exist

### Existing Instances (Designs)
- **None** - `models/designs/` is empty

### Gaps
- No package structure defined
- No standard imports configured
- No enumerations available for fuel types, reactor types, etc.
- No power balance calculation definition
- Cannot begin any design work without this foundation

## Research Findings

### PyFECONS Codebase Analysis

**Source**: `/home/reid/PyFECONS` (from SOURCE_INDEX.md)

#### Enumerations Extracted (`pyfecons/enums.py`)

| Enum | Values | Lines | Notes |
|------|--------|-------|-------|
| **FuelType** | DT, DD, DHE3, PB11 | 43-53 | Each has (value, display_name) tuple |
| **ReactorType** | IFE, MFE, MIF | 4-7 | Inertial, Magnetic, Magnetized Inertial |
| **ConfinementType** | SPHERICAL_TOKAMAK, MAGNETIC_MIRROR, LASER_DRIVEN_DIRECT_DRIVE | 10-34 | Many commented out for future expansion |
| **MagnetType** | PF, CS, TF | 172-181 | Poloidal, Central Solenoid, Toroidal Field |
| **MagnetMaterialType** | HTS_CICC, HTS_PANCAKE, COPPER | 184-193 | For future use |

#### PowerBalance.py Analysis (lines 8-105)

**Function signature** (line 8):
```python
def power_balance(basic: Basic, power_input: PowerInput) -> PowerTable
```

**17 Input Parameters** (from `Basic` and `PowerInput` classes):

| Parameter | Type | Source Class | Description |
|-----------|------|--------------|-------------|
| `p_nrl` | MW | Basic | Fusion power |
| `fuel_type` | FuelType | Basic | Fusion fuel type |
| `mn` | Ratio | PowerInput | Neutron energy multiplier |
| `eta_th` | Percent | PowerInput | Thermal conversion efficiency |
| `eta_de` | Percent | PowerInput | Direct energy conversion efficiency |
| `eta_p` | Percent | PowerInput | Pumping power capture efficiency |
| `eta_pin` | Percent | PowerInput | Input power wall plug efficiency |
| `p_input` | MW | PowerInput | Input power (heating) |
| `p_tf` | MW | PowerInput | Power into TF coils |
| `p_pf` | MW | PowerInput | Power into PF coils |
| `p_tfcool` | MW | PowerInput | TF coil cooling power |
| `p_pfcool` | MW | PowerInput | PF coil cooling power |
| `p_trit` | MW | PowerInput | Tritium systems power |
| `p_house` | MW | PowerInput | Housekeeping power |
| `p_cryo` | MW | PowerInput | Cryogenic vacuum pumping |
| `fpcppf` | Percent | PowerInput | Primary coolant pumping power fraction |
| `f_sub` | Percent | PowerInput | Subsystem and control fraction |

**16 Output Parameters** (lines 10-50):

| Output | Formula | Line |
|--------|---------|------|
| `p_alpha` | `compute_p_alpha(p_nrl, fuel_type)` | 10 |
| `p_neutron` | `p_nrl - p_alpha` | 11 |
| `p_cool` | `p_tfcool + p_pfcool` | 12 |
| `p_aux` | `p_trit + p_house` | 13 |
| `p_coils` | `p_tf + p_pf` | 14 |
| `p_th` | `mn * p_neutron + p_input + eta_th * (fpcppf * eta_p + f_sub) * (mn * p_neutron)` | 15-21 |
| `p_the` | `eta_th * p_th` | 22 |
| `p_dee` | `eta_de * p_alpha` | 23 |
| `p_et` | `p_dee + p_the` | 24 |
| `p_loss` | `p_th - p_the - p_dee` | 25 |
| `p_pump` | `fpcppf * p_the` | 26 |
| `p_sub` | `f_sub * p_the` | 27 |
| `q_sci` | `p_nrl / p_input` | 28 |
| `q_eng` | (complex formula, lines 29-48) | 29-48 |
| `rec_frac` | `1 / q_eng` | 49 |
| `p_net` | `(1 - 1/q_eng) * p_et` | 50 |

**Alpha Power Calculation** (`compute_p_alpha`, lines 94-105):

| Fuel Type | Formula | Charged Fraction |
|-----------|---------|------------------|
| DT | `p_nrl * 3.52 / 17.58` | 20.0% |
| DD | `p_nrl * (0.5 * 3.02 / 4.03 + 0.5 * 0.82 / 3.27)` | ~24.4% |
| DHE3 | `p_nrl * 14.7 / 18.3` | 80.3% |
| PB11 | `p_nrl * 8.7 / 8.7` | 100% (aneutronic) |

### SysMLv2 Patterns Guidance

**Source**: sysmlv2-doc-analyzer agent

**Enumeration Syntax**:
```sysml
enum def FuelType {
    enum DT;
    enum DD;
    enum DHE3;
    enum PB11;
}
```

**Conditional Logic in Calc Defs** (if-then-else-endif):
```sysml
out alphaPowerFraction : Real =
    if fuelType == FuelType::DT then 0.20
    else if fuelType == FuelType::DD then 0.244
    else if fuelType == FuelType::DHE3 then 0.803
    else if fuelType == FuelType::PB11 then 1.0
    else 0.0
    endif endif endif endif;
```

**Package Structure Pattern**:
```sysml
package FusionTEA {
    public import ScalarValues::*;
    public import ISQ::*;
    public import SI::*;

    package Library { /* definitions */ }
    package Designs { /* usages */ }
}
```

### Existing Model Analysis

- **No existing models** - Library is empty
- **Patterns from MODELING_GUIDE.md**:
  - Definitions in `library/` with Title Case names
  - Usages in `designs/` with snake_case names
  - ADR-002: All calc defs in library only
  - EXPOSE pattern for cross-file access

## Proposed Model Design

### High-Level Approach

Create two files following the library-first pattern:

1. **`models/library/foundation.sysml`** - Package structure, imports, enumerations
2. **`models/library/calculations/power_balance.sysml`** - PowerBalanceCalc calc def

### Dataflow Architecture

```
Layer 1: Foundation (enums, imports)
    ↓
Layer 2: PowerBalanceCalc (physics calculations)
    ↓
[Future] Layer 3: Geometry, Subsystems
    ↓
[Future] Layer 4: LCOE
```

**Key principle**: Definitions only, no usages until Phase 3 (CATF Design).

---

## Model Element 1: Foundation Package

**Type**: `package FusionTEA`

**Purpose**: Establish project-wide namespace with standard imports and enumerations

**Location**: `models/library/foundation.sysml`

### Package Structure

```sysml
package FusionTEA {
    doc /*
    FusionTEA - Fusion Techno-Economic Analysis Models

    Root package providing project namespace, standard imports,
    and enumeration definitions for fusion power plant modeling.

    **Source**: Project architecture research
    **Reference**: project/research/20260105-103000_catf-mfe-architecture.md
    **Last Updated**: 2026-01-05
    */

    // Standard library imports
    public import ScalarValues::*;
    public import ISQ::*;
    public import SI::*;

    // Nested package for reusable definitions
    package Library {
        doc /* Reusable definitions (calc defs, part defs, enums) */
    }

    // Nested package for specific design instances
    package Designs {
        doc /* Design-specific usages (CATF, Stellarator, etc.) */
    }
}
```

### Enumeration: FuelType

```sysml
enum def FuelType {
    doc /*
    Fusion fuel type enumeration

    Determines alpha power fraction and neutron energy for power balance.

    **Source**: PyFECONS
    **File**: pyfecons/enums.py
    **Lines**: 43-53
    **Reference**: https://en.wikipedia.org/wiki/Nuclear_fusion
    **Last Updated**: 2026-01-05
    */

    enum DT;    // Deuterium-Tritium (20% charged particles)
    enum DD;    // Deuterium-Deuterium (~24% charged particles)
    enum DHE3;  // Deuterium-Helium-3 (80% charged particles)
    enum PB11;  // Proton-Boron-11 (100% charged, aneutronic)
}
```

### Enumeration: ReactorType

```sysml
enum def ReactorType {
    doc /*
    Reactor type classification

    **Source**: PyFECONS
    **File**: pyfecons/enums.py
    **Lines**: 4-7
    **Last Updated**: 2026-01-05
    */

    enum IFE;   // Inertial Fusion Energy
    enum MFE;   // Magnetic Fusion Energy
    enum MIF;   // Magnetized Inertial Fusion
}
```

### Enumeration: ConfinementType

```sysml
enum def ConfinementType {
    doc /*
    Confinement approach classification

    Currently enabled types; many future options commented in PyFECONS.

    **Source**: PyFECONS
    **File**: pyfecons/enums.py
    **Lines**: 10-34
    **Last Updated**: 2026-01-05
    */

    enum SPHERICAL_TOKAMAK;
    enum MAGNETIC_MIRROR;
    enum LASER_DRIVEN_DIRECT_DRIVE;
    // Future: STELLARATOR, CONVENTIONAL_TOKAMAK, etc.
}
```

### Enumeration: MagnetType

```sysml
enum def MagnetType {
    doc /*
    Magnet system type classification

    **Source**: PyFECONS
    **File**: pyfecons/enums.py
    **Lines**: 172-181
    **Last Updated**: 2026-01-05
    */

    enum TF;    // Toroidal Field
    enum CS;    // Central Solenoid
    enum PF;    // Poloidal Field
}
```

### Enumeration: MagnetMaterialType

```sysml
enum def MagnetMaterialType {
    doc /*
    Magnet conductor material type classification

    Used for magnet cost calculations in Phase 2.

    **Source**: PyFECONS
    **File**: pyfecons/enums.py
    **Lines**: 184-193
    **Last Updated**: 2026-01-05
    */

    enum HTS_CICC;    // High Temperature Superconductor Cable-In-Conduit-Conductor
    enum HTS_PANCAKE; // High Temperature Superconductor Pancake
    enum COPPER;      // Copper (resistive)
}
```

### Traceability Sources
- **Primary**: PyFECONS `pyfecons/enums.py` lines 4-193
- **Secondary**: Architecture research document
- **Confidence**: High - direct enum extraction

### Validation Approach
- Parse validation: `syside check models/library/foundation.sysml`
- All four enums defined with correct values
- Package hierarchy resolves correctly

---

## Model Element 2: PowerBalanceCalc

**Type**: `calc def PowerBalanceCalc`

**Purpose**: Core power balance calculation for MFE fusion reactors with fuel-type-dependent alpha power

**Location**: `models/library/calculations/power_balance.sysml`

### Calculation Structure

```sysml
package FusionTEA::Library::Calculations {
    doc /*
    Physics calculation definitions for fusion power plants
    */

    private import FusionTEA::*;
    private import FusionTEA::Library::FuelType;

    calc def PowerBalanceCalc {
        doc /*
        Power balance calculation for MFE fusion reactors

        Calculates power flows from fusion power through thermal conversion,
        direct energy conversion, and recirculating power to net electric output.

        **Source**: PyFECONS
        **File**: pyfecons/costing/mfe/PowerBalance.py
        **Lines**: 8-105
        **Original Reference**: Cited Wikipedia for alpha fractions
        **Assumptions**:
        - Steady-state operation
        - No transient effects
        - Energy multiplier mn accounts for blanket neutron multiplication
        **Validation**: Compare outputs to PyFECONS power_table for CATF case
        **Last Updated**: 2026-01-05
        */

        // === INPUTS (17 parameters) ===

        // Primary fusion parameters
        in attribute p_nrl : Real;      // Fusion power [MW]
        in attribute fuel_type : FuelType;

        // Efficiency parameters
        in attribute mn : Real;         // Neutron energy multiplier (blanket)
        in attribute eta_th : Real;     // Thermal conversion efficiency
        in attribute eta_de : Real;     // Direct energy conversion efficiency
        in attribute eta_p : Real;      // Pumping power capture efficiency
        in attribute eta_pin : Real;    // Input power wall plug efficiency

        // Power inputs
        in attribute p_input : Real;    // Heating/input power [MW]
        in attribute p_tf : Real;       // Power into TF coils [MW]
        in attribute p_pf : Real;       // Power into PF coils [MW]

        // Cooling power
        in attribute p_tfcool : Real;   // TF coil cooling power [MW]
        in attribute p_pfcool : Real;   // PF coil cooling power [MW]

        // Auxiliary systems
        in attribute p_trit : Real;     // Tritium systems power [MW]
        in attribute p_house : Real;    // Housekeeping power [MW]
        in attribute p_cryo : Real;     // Cryogenic vacuum pumping [MW]

        // Fraction parameters
        in attribute fpcppf : Real;     // Primary coolant pumping power fraction
        in attribute f_sub : Real;      // Subsystem and control fraction

        // === INTERMEDIATE CALCULATIONS ===

        // Alpha power fraction based on fuel type
        attribute alpha_fraction : Real =
            if fuel_type == FuelType::DT then 3.52 / 17.58
            else if fuel_type == FuelType::DD then 0.5 * 3.02 / 4.03 + 0.5 * 0.82 / 3.27
            else if fuel_type == FuelType::DHE3 then 14.7 / 18.3
            else if fuel_type == FuelType::PB11 then 1.0
            else 0.0
            endif endif endif endif;

        // === OUTPUTS (16 parameters) ===

        // Primary power split
        out attribute p_alpha : Real = p_nrl * alpha_fraction;
        out attribute p_neutron : Real = p_nrl - p_alpha;

        // Aggregated powers
        out attribute p_cool : Real = p_tfcool + p_pfcool;
        out attribute p_aux : Real = p_trit + p_house;
        out attribute p_coils : Real = p_tf + p_pf;

        // Thermal power chain
        out attribute p_th : Real = mn * p_neutron + p_input +
            eta_th * (fpcppf * eta_p + f_sub) * (mn * p_neutron);
        out attribute p_the : Real = eta_th * p_th;

        // Direct conversion
        out attribute p_dee : Real = eta_de * p_alpha;

        // Total and net electric
        out attribute p_et : Real = p_dee + p_the;
        out attribute p_loss : Real = p_th - p_the - p_dee;

        // Recirculating power components
        out attribute p_pump : Real = fpcppf * p_the;
        out attribute p_sub : Real = f_sub * p_the;

        // Q values
        out attribute q_sci : Real = p_nrl / p_input;

        // Engineering Q (complex formula)
        out attribute q_eng : Real =
            (eta_th * (mn * p_neutron + p_pump + p_input) + eta_de * p_alpha) /
            (p_coils + p_pump + p_sub + p_aux + p_cool + p_cryo + p_input / eta_pin);

        // Final outputs
        out attribute rec_frac : Real = 1.0 / q_eng;
        out attribute p_net : Real = (1.0 - 1.0 / q_eng) * p_et;

        // === CONSTRAINTS ===

        assert constraint PositiveFusionPower {
            doc /* Fusion power must be positive */
            p_nrl > 0
        }

        assert constraint PositiveNetPower {
            doc /* Net electric power must be positive for viable plant */
            p_net > 0
        }

        assert constraint ReasonableQ {
            doc /* Engineering Q must be > 1 for net power production */
            q_eng > 1.0
        }
    }
}
```

### Parameter Sources (Traceability)

| Parameter | PyFECONS Source | Line |
|-----------|-----------------|------|
| p_alpha calculation | `compute_p_alpha()` | 94-105 |
| p_neutron | `power_table.p_neutron` | 11 |
| p_cool | `power_table.p_cool` | 12 |
| p_aux | `power_table.p_aux` | 13 |
| p_coils | `power_table.p_coils` | 14 |
| p_th | `power_table.p_th` | 15-21 |
| p_the | `power_table.p_the` | 22 |
| p_dee | `power_table.p_dee` | 23 |
| p_et | `power_table.p_et` | 24 |
| p_loss | `power_table.p_loss` | 25 |
| p_pump | `power_table.p_pump` | 26 |
| p_sub | `power_table.p_sub` | 27 |
| q_sci | `power_table.q_sci` | 28 |
| q_eng | `power_table.q_eng` | 29-48 |
| rec_frac | `power_table.rec_frac` | 49 |
| p_net | `power_table.p_net` | 50 |

### Validation Approach

**Expected values from PyFECONS CATF case**:

| Metric | Expected Range | Source |
|--------|----------------|--------|
| p_alpha / p_nrl (DT) | 0.200 (20.0%) | PowerBalance.py:97-98 |
| p_alpha / p_nrl (DD) | 0.244 (24.4%) | PowerBalance.py:99-100 |
| p_alpha / p_nrl (DHE3) | 0.803 (80.3%) | PowerBalance.py:101-102 |
| p_alpha / p_nrl (PB11) | 1.000 (100%) | PowerBalance.py:103-104 |
| q_eng | > 1.0 | Physics requirement |
| p_net | > 0 | Viable plant |

**Validation commands**:
```bash
syside check models/library/calculations/power_balance.sysml
```

---

## Design Alternatives

### Decision Point 1: Conditional Logic Syntax

**Context**: SysMLv2 supports if-then-else-endif for conditional expressions. Need to verify this works in calc def attributes.

**Option A: Nested if-then-else (Shown Above)**
- Syntax: `if ... then ... else if ... endif endif`
- Pros: Standard SysMLv2 syntax, directly translates logic
- Cons: Verbose with multiple nesting, each `if` needs matching `endif`
- Recommendation: **Use this** - matches spec documentation

**Option B: Separate Calc Defs per Fuel Type**
- Syntax: `calc def AlphaPowerDT`, `calc def AlphaPowerDD`, etc.
- Pros: Simpler individual calc defs, no conditional logic
- Cons: More files, requires dispatch logic in design, harder to maintain
- Not recommended for Phase 1

**Decision**: Use Option A (nested if-then-else). Will validate during prototyping.

### Decision Point 2: Package Organization

**Context**: How to organize foundation vs calculations packages

**Option A: Single Foundation File (Shown Above)**
- `foundation.sysml` contains FusionTEA package with enums
- `calculations/power_balance.sysml` contains calc def
- Pros: Clear separation, matches spec requirements
- Cons: Two files to manage

**Option B: All in One File**
- Single `foundation.sysml` with everything
- Pros: Simpler for Phase 1
- Cons: Won't scale, mixes concerns

**Decision**: Use Option A. Two files provides proper separation for future growth.

### Decision Point 3: Alpha Fraction Calculation

**Context**: How to implement fuel-type-dependent alpha power

**Option A: Inline Conditional in Calc Def (Shown Above)**
- Alpha fraction computed inside PowerBalanceCalc
- Pros: Self-contained, clear traceability
- Cons: Large calc def

**Option B: Separate AlphaFractionCalc**
- `calc def AlphaFractionCalc` in separate file
- PowerBalanceCalc imports and uses it
- Pros: More modular, reusable
- Cons: More complexity for Phase 1, cross-file dependencies

**Decision**: Use Option A for Phase 1. Can refactor to Option B if needed later.

---

## Cross-File Bindings

**For Phase 1, there are minimal cross-file bindings:**

| Target | Source File | Source Element | Notes |
|--------|-------------|----------------|-------|
| FuelType | foundation.sysml | FusionTEA::Library::FuelType | Used by PowerBalanceCalc |

**Required imports in power_balance.sysml**:
```sysml
private import FusionTEA::*;
private import FusionTEA::Library::FuelType;
```

**Dataflow direction**:
```
foundation.sysml (enums)
    ↓ (imports)
calculations/power_balance.sysml (calc def)
    ↓ (future imports)
designs/catf/*.sysml (usages)
```

---

## Common Pitfalls & Quick Reference

### SysML v2 Syntax Rules for This Project

#### Enumeration Definitions
- CORRECT: `enum def FuelType { enum DT; enum DD; }`
- WRONG: `enum FuelType { DT, DD }` (not SysMLv2 syntax)

#### Conditional Expressions
- CORRECT: `if x == Enum::Value then a else b endif`
- WRONG: `x == Enum::Value ? a : b` (ternary not supported)
- TIP: Each `if` needs matching `endif`; nested requires multiple `endif`

#### Enum Comparisons
- CORRECT: `fuel_type == FuelType::DT`
- WRONG: `fuel_type == "DT"` (string comparison)

#### Package Imports
- CORRECT: `private import FusionTEA::Library::FuelType;`
- WRONG: `import FuelType;` (unqualified)

#### Attribute with Units
- CORRECT: `attribute power : Real = 2600.0;` (units in comment)
- NOTE: ISQ units like `[MW]` may require specific setup

#### Documentation Requirements
- MUST HAVE: `doc /* ... */` on every calc def, enum def
- MUST HAVE: Source, File, Lines citations
- MUST HAVE: Last Updated date

### Pre-Flight Checklist

Before implementation, verify:
- [ ] Enum syntax tested with validation script
- [ ] Conditional expressions validated
- [ ] Package import paths correct
- [ ] All 17 inputs documented
- [ ] All 16 outputs match PyFECONS formulas

### Validation Commands

```bash
# Quick syntax check on single file
syside check models/library/foundation.sysml
syside check models/library/calculations/power_balance.sysml

# Check entire library
syside check models/library/
```

---

## Validation Plan

### Parsing Validation
```bash
# All files must parse without errors
syside check models/library/foundation.sysml
syside check models/library/calculations/power_balance.sysml
```

### Documentation Validation
- [ ] FusionTEA package has doc comment
- [ ] All four enums have doc comments with PyFECONS citations
- [ ] PowerBalanceCalc has comprehensive doc comment
- [ ] All 17 inputs documented
- [ ] All 16 outputs documented with formulas

### Traceability Validation
- [ ] FuelType enum values match PyFECONS enums.py:43-53
- [ ] ReactorType values match enums.py:4-7
- [ ] PowerBalanceCalc formulas match PowerBalance.py:8-50
- [ ] Alpha fraction formulas match PowerBalance.py:94-105

### Constraint Validation
- [ ] PositiveFusionPower constraint defined
- [ ] PositiveNetPower constraint defined
- [ ] ReasonableQ constraint defined

---

## Implementation Checklist

### Phase 1a: Foundation (foundation.sysml)
- [ ] Create `models/library/foundation.sysml`
  - [ ] FusionTEA package with doc comment
  - [ ] Standard imports (ScalarValues, ISQ, SI)
  - [ ] Library nested package
  - [ ] Designs nested package
  - [ ] FuelType enum with doc comment
  - [ ] ReactorType enum with doc comment
  - [ ] ConfinementType enum with doc comment
  - [ ] MagnetType enum with doc comment
  - [ ] MagnetMaterialType enum with doc comment
- [ ] Parse validation: `syside check models/library/foundation.sysml`

### Phase 1b: PowerBalanceCalc (calculations/power_balance.sysml)
- [ ] Create `models/library/calculations/` directory
- [ ] Create `models/library/calculations/power_balance.sysml`
  - [ ] Package declaration with imports
  - [ ] PowerBalanceCalc calc def
  - [ ] All 17 input parameters with doc comments
  - [ ] Alpha fraction calculation with fuel-type conditional
  - [ ] All 16 output parameters with formulas
  - [ ] Three constraints (PositiveFusionPower, PositiveNetPower, ReasonableQ)
  - [ ] Full doc comment with PyFECONS traceability
- [ ] Parse validation: `syside check models/library/calculations/power_balance.sysml`

### Phase 1c: Integration Validation
- [ ] Run full library validation
- [ ] Verify imports resolve correctly
- [ ] Document any syntax issues or workarounds
- [ ] Update spec checklist with results

---

## Implementation Benefits

1. **Follows MODELING_GUIDE patterns**: Definitions in library, proper naming conventions
2. **Enables downstream work**: All Phase 2+ features can import foundation
3. **Full PyFECONS traceability**: Every parameter and formula cited with line numbers
4. **Reusable calc def**: PowerBalanceCalc works for any MFE reactor design
5. **ADR-002 compliant**: All calc defs in library, no calculations in designs

## Potential Risks

### R-001: Conditional Expression Syntax
- **Risk**: SysIDE may not support nested if-then-else as documented
- **Likelihood**: Low (spec shows support)
- **Impact**: Medium (would require workaround)
- **Mitigation**: Test conditional syntax early in prototyping; fallback to separate calc defs per fuel type

### R-002: Enum Comparison Syntax
- **Risk**: Enum value comparison `fuel_type == FuelType::DT` may have parsing issues
- **Likelihood**: Low
- **Impact**: Low
- **Mitigation**: Test enum comparison early; use alternative comparison patterns if needed

### R-003: Import Resolution
- **Risk**: Cross-file imports may not resolve as expected
- **Likelihood**: Medium
- **Impact**: Medium
- **Mitigation**: Follow tested patterns from MODELING_GUIDE; adjust package structure if needed

---

## Next Steps After Implementation

1. **Parse validation**: `syside check models/library/` to ensure all files parse
2. **Documentation review**: Verify all doc comments complete and accurate
3. **Update epic status**: Mark Phase 1 deliverables complete in BACKLOG.md
4. **Proceed to Phase 2**: Geometry calculations, magnet definitions

---

## Design Decisions (User Approved)

**Date**: 2026-01-05

1. **ConfinementType Enum Scope**: **Minimal (Option A)**
   - Only include 3 currently enabled values
   - Note: Project is focused on CATF implementation
   - Rationale: Keep Phase 1 minimal and focused

2. **Unit Handling**: **Comments Only (Option A)**
   - Keep units in doc comments (`// Fusion power [MW]`)
   - Defer ISQ integration to future phase
   - Rationale: Simplifies Phase 1, avoids library setup complexity

3. **Additional Enums**: **Add MagnetMaterialType (Option B)**
   - Include: FuelType, ReactorType, ConfinementType, MagnetType, MagnetMaterialType
   - MagnetMaterialType needed for Phase 2 magnet cost calculations
   - Defer blanket enums to later phases

---

## Design Validation Report

**Date**: 2026-01-05

### Prototype Files Created

| File | Location | Status |
|------|----------|--------|
| foundation.sysml | `models/library/foundation.sysml` | PASS |
| power_balance.sysml | `models/library/calculations/power_balance.sysml` | PASS |

### Quality Checks

| Level | Check | Status | Notes |
|-------|-------|--------|-------|
| Level 1 | Syntax validation | PASS | `syside check models/library/` exits 0 |
| Level 2 | Structural completeness | PASS | 5 enums, 1 calc def with 18 in / 16 out |
| Level 3 | Dataflow integrity | PASS | Unidirectional: foundation → power_balance |

### Validation Results

**foundation.sysml**: PASS
- Package declaration with doc comment
- Standard imports (ScalarValues, ISQ, SI)
- 5 enum definitions (FuelType, ReactorType, ConfinementType, MagnetType, MagnetMaterialType)
- Nested Library and Designs packages
- All enums have doc comments with PyFECONS citations

**power_balance.sysml**: PASS
- Package declaration with imports
- PowerBalanceCalc calc def with comprehensive doc comment
- 18 input parameters (17 original + alpha_fraction with default)
- 16 output parameters with formulas matching PyFECONS
- 3 assert constraints (PositiveFusionPower, PositiveNetPower, ReasonableQ)

### Design Iteration: Conditional Expression Limitation

**Issue Discovered**: SysMLv2 does NOT support conditional expressions (`if-then-else-endif` or `?:` ternary) in calc def attribute value assignments.

**Original Design** (failed validation):
```sysml
attribute alpha_fraction : Real =
    if fuel_type == FuelType::DT then 0.20
    else if fuel_type == FuelType::DD then 0.24
    ...
    endif endif;
```

**Revised Design** (passes validation):
```sysml
// Alpha fraction as input parameter with DT default
in attribute alpha_fraction : Real default := 0.2002275313;
```

**Impact**:
- PowerBalanceCalc now has 18 inputs (added alpha_fraction)
- Fuel-type flexibility achieved by overriding alpha_fraction at usage time
- DT fuel (used by CATF) is the default - no change needed for CATF design
- Other fuel types: override alpha_fraction with appropriate value (DD: 0.2499, DHE3: 0.8033, PB11: 1.0)

**Tradeoff**: Less automatic fuel-type handling, but more flexible and explicit parameter binding.

### Prototype Status: PASS

---

**Next Step**: User approval to proceed to `/plan-model`

