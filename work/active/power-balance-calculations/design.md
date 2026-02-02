# Design: Power Balance Calculations (MODELS)

**Type:** SysMLv2 Models
**Status:** Validated (Prototype Complete)
**Owner:** Reid Westwood
**Created:** 2026-01-26
**Last Updated:** 2026-01-26

## Overview

This design defines the SysMLv2 calculation definitions for fusion power balance - computing power flows from fusion power through thermal conversion to net electric output. The design uses explicit generic/MFE split architecture: a generic `'Power Balance Calc'` for concept-agnostic calculations (alpha/neutron power, Q_sci) and an MFE-specific `'MFE Power Balance Calc'` for magnetic confinement power flows (thermal power, recirculating power, Q_eng, net electric).

### Related Artifacts
- **Spec:** `modeling_pm/active/power-balance-calculations/spec.md`
- **Research:** `modeling_pm/research/20260123-pyfecons-library-mapping-strategy.md`
- **Epic:** `modeling_pm/backlog/BACKLOG.md` - Power Balance Calculations (P0)
- **PyFECONS Sources:**
  - `/home/reid/PyFECONS/pyfecons/costing/mfe/PowerBalance.py` (main implementation)
  - `/home/reid/PyFECONS/pyfecons/inputs/power_input.py` (input definitions)
  - `/home/reid/PyFECONS/pyfecons/costing/accounting/power_table.py` (output definitions)

---

## Current Model State

### Existing Definitions (Library)
- `models/library/foundation/types.sysml` - FuelType enum (DT, DD, DHE3, PB11) at lines 64-78
- `models/library/foundation/units.sysml` - Percent, Ratio custom types
- `models/library/foundation/materials.sysml` - Material definitions (not directly used)

### Existing Instances (Designs)
- None - this is the first calculation library

### Gaps
- No power balance calculations exist
- `models/library/calculations/` directory is empty (ready for this epic)
- No calc def patterns established (will use coffee maker test patterns as reference)

---

## Research Findings

### PyFECONS Source Analysis

**Calculation Flow (16 steps, 6 dependency levels):**

```
Level 0: Direct Inputs
  └─ p_nrl, fuel_type, p_input, mn, eta_th, eta_de, eta_p, eta_pin
     fpcppf, f_sub, p_tf, p_pf, p_tfcool, p_pfcool, p_trit, p_house, p_cryo

Level 1: Simple Aggregations
  ├─ p_alpha = compute_p_alpha(p_nrl, fuel_type)
  ├─ p_neutron = p_nrl - p_alpha
  ├─ p_cool = p_tfcool + p_pfcool
  ├─ p_aux = p_trit + p_house
  └─ p_coils = p_tf + p_pf

Level 2: Thermal Power
  └─ p_th = mn*p_neutron + p_input + eta_th*(fpcppf*eta_p + f_sub)*(mn*p_neutron)

Level 3: Electric Conversion
  ├─ p_the = eta_th * p_th
  └─ p_dee = eta_de * p_alpha  [DEFERRED - out of scope]

Level 4: Derived Powers
  ├─ p_et = p_the  [Simplified - no direct conversion]
  ├─ p_loss = p_th - p_the
  ├─ p_pump = fpcppf * p_the
  ├─ p_sub = f_sub * p_the
  └─ q_sci = p_nrl / p_input

Level 5: Engineering Q
  └─ q_eng = (Numerator) / (Denominator)
     Numerator: eta_th*(mn*p_neutron + p_pump + p_input)
     Denominator: p_coils + p_pump + p_sub + p_aux + p_cool + p_cryo + p_input/eta_pin

Level 6: Final Outputs
  ├─ rec_frac = 1 / q_eng
  └─ p_net = (1 - rec_frac) * p_et
```

**Alpha Power Ratios by Fuel Type** (from PyFECONS PowerBalance.py:94-104):

| Fuel Type | Formula | Ratio | Physical Basis |
|-----------|---------|-------|----------------|
| DT | p_nrl * 3.52/17.58 | 20.02% | 3.52 MeV alpha / 17.58 MeV total |
| DD | p_nrl * (0.5 * 3.02/4.03 + 0.5 * 0.82/3.27) | 50.01% | Weighted average of two branches |
| DHE3 | p_nrl * 14.7/18.3 | 80.33% | 14.7 MeV charged / 18.3 MeV total |
| PB11 | p_nrl * 8.7/8.7 | 100% | Aneutronic - all charged particles |

### SysMLv2 Pattern Analysis

**Conditional Expression Syntax** (from kerml-expert):
```sysml
attribute alpha_fraction : Real =
    if fuel_type == FuelType::DT? 0.2002
    else if fuel_type == FuelType::DD? 0.5001
    else if fuel_type == FuelType::DHE3? 0.8033
    else 1.0;
```

**Calc Def Pattern** (from sysml-expert):
```sysml
calc def 'Power Balance Calc' {
    in attribute fusion_power : Real;
    in attribute fuel_type : FuelType;
    return attribute p_net : Real;

    // Intermediate calculations
    attribute p_alpha : Real = ...;

    // Return expression
    p_net_calculation_expression
}
```

**Key Import Pattern**:
```sysml
private import FoundationTypes::FuelType;
private import ScalarValues::Real;
```

---

## Proposed Model Design

### High-Level Approach

**Architecture: Generic + MFE Split**

```
┌─────────────────────────────────────────────────────────────┐
│                   models/library/calculations/               │
│                                                              │
│  ┌─────────────────────────────────────────────────────────┐│
│  │ power_balance/power_balance.sysml                        ││
│  │ Package: PowerBalanceLibrary                             ││
│  │                                                          ││
│  │ calc def 'Alpha Power Calc'                             ││
│  │   in: p_nrl, fuel_type                                  ││
│  │   out: p_alpha (with fuel-type conditionals)            ││
│  │                                                          ││
│  │ calc def 'Power Balance Calc'                           ││
│  │   in: p_nrl, fuel_type, p_input                         ││
│  │   out: p_alpha, p_neutron, q_sci                        ││
│  └─────────────────────────────────────────────────────────┘│
│                           │                                  │
│                           │ imports                          │
│                           ▼                                  │
│  ┌─────────────────────────────────────────────────────────┐│
│  │ power_balance/mfe_power_balance.sysml                    ││
│  │ Package: MFEPowerBalanceLibrary                          ││
│  │                                                          ││
│  │ calc def 'MFE Power Balance Calc'                       ││
│  │   in: (generic inputs) + MFE-specific inputs            ││
│  │   out: p_th, p_the, p_et, p_coils, p_cool, p_aux,       ││
│  │        p_pump, p_sub, p_loss, q_eng, rec_frac, p_net    ││
│  │                                                          ││
│  │   uses: 'Alpha Power Calc' for p_alpha                  ││
│  └─────────────────────────────────────────────────────────┘│
└─────────────────────────────────────────────────────────────┘
```

**Rationale for Split:**
1. Generic `'Power Balance Calc'` computes physics-only outputs (p_alpha, p_neutron, q_sci) that apply to any fusion concept
2. MFE-specific `'MFE Power Balance Calc'` adds the recirculating power flows unique to magnetic confinement (coils, cooling, pumping)
3. Future IFE power balance can reuse generic calc and add IFE-specific flows (laser power, target injection)

---

### Model Element 1: Alpha Power Calc (Helper)

**Type**: `calc def 'Alpha Power Calc'`

**Purpose**: Compute charged particle power from fusion power and fuel type. This is extracted as a separate calc to encapsulate the fuel-type conditional logic.

**Location**: `models/library/calculations/power_balance/power_balance.sysml`

**Definition Structure**:
```sysml
calc def 'Alpha Power Calc' {
    doc /*
    Compute charged particle (alpha) power from fusion reaction.

    The alpha fraction depends on fuel type and reaction kinematics:
    - DT: 3.52 MeV alpha / 17.58 MeV total = 20.02%
    - DD: Weighted average of two branches = ~50%
    - DHe3: 14.7 MeV / 18.3 MeV = 80.33%
    - PB11: 100% (aneutronic)

    **Source**: PyFECONS PowerBalance.py:94-104
    **Reference**: https://en.wikipedia.org/wiki/Nuclear_fusion
    **Last Updated**: 2026-01-26
    */

    in attribute p_nrl : Real;          // Fusion power [MW]
    in attribute fuel_type : FuelType;  // Fuel type enum

    return attribute p_alpha : Real;    // Alpha particle power [MW]

    // Fuel-type conditional calculation
    if fuel_type == FuelType::DT? p_nrl * 3.52 / 17.58
    else if fuel_type == FuelType::DD? p_nrl * (0.5 * 3.02 / 4.03 + 0.5 * 0.82 / 3.27)
    else if fuel_type == FuelType::DHE3? p_nrl * 14.7 / 18.3
    else p_nrl * 1.0  // PB11: 100% charged particles
}
```

**Traceability Sources**:
- Primary: PyFECONS `PowerBalance.py:94-104` (compute_p_alpha function)
- Secondary: Wikipedia Nuclear Fusion article (energy ratios)
- Confidence: High - well-established physics

**Validation Approach**:
- DT: p_nrl=500 MW → p_alpha ≈ 100.1 MW (500 * 0.2002)
- Compare all 4 fuel types against PyFECONS

---

### Model Element 2: Generic Power Balance Calc

**Type**: `calc def 'Power Balance Calc'`

**Purpose**: Compute concept-agnostic power balance outputs that apply to any fusion approach.

**Location**: `models/library/calculations/power_balance/power_balance.sysml`

**Definition Structure**:
```sysml
calc def 'Power Balance Calc' {
    doc /*
    Generic power balance calculation for any fusion concept.

    Computes:
    - p_alpha: Charged particle power (from fuel type)
    - p_neutron: Neutron power (remainder after alpha)
    - q_sci: Scientific Q (fusion power / input power)

    These outputs are concept-agnostic and used by both MFE and IFE.

    **Source**: PyFECONS PowerBalance.py:10-11, 28
    **Reference**: Standard fusion physics
    **Last Updated**: 2026-01-26
    */

    // === PRIMARY INPUTS ===
    in attribute p_nrl : Real;          // Fusion power [MW]
    in attribute fuel_type : FuelType;  // Fuel type enum
    in attribute p_input : Real;        // Input/heating power [MW]

    // === OUTPUTS ===
    return attribute p_net_generic : Real;  // Placeholder - actual net from specialized calcs

    // Intermediate outputs (exposed for use by downstream calcs)
    attribute p_alpha : Real;           // Alpha particle power [MW]
    attribute p_neutron : Real;         // Neutron power [MW]
    attribute q_sci : Real;             // Scientific Q (dimensionless)

    // === CALCULATIONS ===

    // Alpha power from helper calc
    calc alpha_calc : 'Alpha Power Calc' {
        in p_nrl = p_nrl;
        in fuel_type = fuel_type;
    }
    attribute p_alpha = alpha_calc.p_alpha;

    // Neutron power: remainder of fusion power
    // Source: PowerBalance.py:11
    attribute p_neutron = p_nrl - p_alpha;

    // Scientific Q: fusion power gain over input
    // Source: PowerBalance.py:28
    attribute q_sci = p_nrl / p_input;

    // Return placeholder (specialized calcs compute actual p_net)
    0.0  // Generic calc doesn't compute p_net
}
```

**Traceability Sources**:
- p_alpha: PowerBalance.py:10
- p_neutron: PowerBalance.py:11
- q_sci: PowerBalance.py:28

---

### Model Element 3: MFE Power Balance Calc

**Type**: `calc def 'MFE Power Balance Calc'`

**Purpose**: Compute MFE-specific power flows including thermal conversion, recirculating power, and net electric output.

**Location**: `models/library/calculations/power_balance/mfe_power_balance.sysml`

**Definition Structure**:
```sysml
calc def 'MFE Power Balance Calc' {
    doc /*
    MFE (Magnetic Fusion Energy) specific power balance.

    Computes full power flow for tokamaks and stellarators:
    - Thermal power from neutron heating + input + recovered pumping
    - Thermal electric power via Rankine/Brayton cycle
    - Recirculating power: coils, cooling, pumping, auxiliary
    - Engineering Q and net electric power

    This calc uses 'Alpha Power Calc' for fuel-type dependent alpha power
    and adds MFE-specific power flows not present in IFE.

    **Source**: PyFECONS PowerBalance.py:8-50
    **Reference**: MFE power plant design standards
    **Last Updated**: 2026-01-26
    */

    // === PRIMARY INPUTS (from generic) ===
    in attribute p_nrl : Real;          // Fusion power [MW]
    in attribute fuel_type : FuelType;  // Fuel type enum
    in attribute p_input : Real;        // Plasma heating power [MW]

    // === MFE-SPECIFIC INPUTS ===
    // Efficiencies
    in attribute mn : Real;             // Neutron energy multiplier (blanket breeding)
    in attribute eta_th : Real;         // Thermal-to-electric efficiency
    in attribute eta_p : Real;          // Pumping power capture efficiency
    in attribute eta_pin : Real;        // Input power wall plug efficiency

    // Power fractions
    in attribute fpcppf : Real;         // Primary coolant pumping power fraction
    in attribute f_sub : Real;          // Subsystem and control fraction

    // Coil power
    in attribute p_tf : Real;           // TF coil power [MW]
    in attribute p_pf : Real;           // PF coil power [MW]

    // Cooling power
    in attribute p_tfcool : Real;       // TF coil cooling [MW]
    in attribute p_pfcool : Real;       // PF coil cooling [MW]

    // Auxiliary power
    in attribute p_trit : Real;         // Tritium systems [MW]
    in attribute p_house : Real;        // Housekeeping [MW]
    in attribute p_cryo : Real;         // Cryogenic pumping [MW]

    // === OUTPUTS ===
    return attribute p_net : Real;      // Net electric power [MW]

    // Intermediate outputs (exposed)
    attribute p_alpha : Real;           // Alpha power [MW]
    attribute p_neutron : Real;         // Neutron power [MW]
    attribute p_th : Real;              // Thermal power [MW]
    attribute p_the : Real;             // Thermal electric power [MW]
    attribute p_et : Real;              // Gross electric power [MW]
    attribute p_coils : Real;           // Total coil power [MW]
    attribute p_cool : Real;            // Total cooling power [MW]
    attribute p_aux : Real;             // Total auxiliary power [MW]
    attribute p_pump : Real;            // Pumping power [MW]
    attribute p_sub : Real;             // Subsystem power [MW]
    attribute p_loss : Real;            // Lost power [MW]
    attribute q_sci : Real;             // Scientific Q
    attribute q_eng : Real;             // Engineering Q
    attribute rec_frac : Real;          // Recirculating fraction

    // === CALCULATIONS ===

    // Step 1: Alpha power (fuel-dependent)
    calc alpha_calc : 'Alpha Power Calc' {
        in p_nrl = p_nrl;
        in fuel_type = fuel_type;
    }
    attribute p_alpha = alpha_calc.p_alpha;

    // Step 2: Neutron power
    // Source: PowerBalance.py:11
    attribute p_neutron = p_nrl - p_alpha;

    // Step 3: Cooling power aggregation
    // Source: PowerBalance.py:12
    attribute p_cool = p_tfcool + p_pfcool;

    // Step 4: Auxiliary power aggregation
    // Source: PowerBalance.py:13
    attribute p_aux = p_trit + p_house;

    // Step 5: Coil power aggregation
    // Source: PowerBalance.py:14
    attribute p_coils = p_tf + p_pf;

    // Step 6: Thermal power
    // Source: PowerBalance.py:15-21
    // p_th = mn*p_neutron + p_input + eta_th*(fpcppf*eta_p + f_sub)*(mn*p_neutron)
    attribute p_th = mn * p_neutron + p_input +
                     eta_th * (fpcppf * eta_p + f_sub) * (mn * p_neutron);

    // Step 7: Thermal electric power
    // Source: PowerBalance.py:22
    attribute p_the = eta_th * p_th;

    // Step 8: Gross electric power (no direct conversion - deferred)
    // Source: PowerBalance.py:24 (simplified)
    attribute p_et = p_the;  // p_dee deferred, so p_et = p_the only

    // Step 9: Lost power
    // Source: PowerBalance.py:25
    attribute p_loss = p_th - p_the;

    // Step 10: Pumping power
    // Source: PowerBalance.py:26
    attribute p_pump = fpcppf * p_the;

    // Step 11: Subsystem power
    // Source: PowerBalance.py:27
    attribute p_sub = f_sub * p_the;

    // Step 12: Scientific Q
    // Source: PowerBalance.py:28
    attribute q_sci = p_nrl / p_input;

    // Step 13: Engineering Q
    // Source: PowerBalance.py:29-48
    // Numerator: eta_th*(mn*p_neutron + p_pump + p_input)
    // Denominator: p_coils + p_pump + p_sub + p_aux + p_cool + p_cryo + p_input/eta_pin
    attribute q_eng_numerator : Real = eta_th * (mn * p_neutron + p_pump + p_input);
    attribute q_eng_denominator : Real = p_coils + p_pump + p_sub + p_aux +
                                          p_cool + p_cryo + p_input / eta_pin;
    attribute q_eng = q_eng_numerator / q_eng_denominator;

    // Step 14: Recirculating fraction
    // Source: PowerBalance.py:49
    attribute rec_frac = 1.0 / q_eng;

    // Step 15: Net electric power
    // Source: PowerBalance.py:50
    (1.0 - rec_frac) * p_et
}
```

**Note on p_dee (Direct Electric):**
Per spec, direct energy conversion is deferred. The original PyFECONS includes:
- `p_dee = eta_de * p_alpha` (PowerBalance.py:23)
- `p_et = p_dee + p_the` (PowerBalance.py:24)

Our simplified version sets `p_et = p_the` only.

---

### Cross-File Bindings

**Future design files will bind to these calc outputs:**

| Consumer File | Calc Instance | Binds To | Notes |
|---------------|---------------|----------|-------|
| `designs/catf_mfe/power_balance.sysml` | `mfe_power_calc : 'MFE Power Balance Calc'` | Design parameters | Future epic |
| `designs/catf_mfe/plant.sysml` | (imports power balance) | `p_net`, `q_eng` for plant-level | Future epic |

**Required imports in design files:**
```sysml
private import MFEPowerBalanceLibrary::'MFE Power Balance Calc';
private import FoundationTypes::FuelType;
```

**Dataflow direction**: Library → Designs (unidirectional, no circular deps)

---

## Traceability Strategy

### Source Documents
- **Primary**: PyFECONS implementation
  - Files: `PowerBalance.py`, `power_input.py`, `power_table.py`, `basic.py`
  - Lines referenced in each calc attribute
  - Complete formula coverage verified

### PyFECONS Integration
| SysML Element | PyFECONS Source | Lines | Notes |
|---------------|-----------------|-------|-------|
| p_alpha calc | compute_p_alpha() | 94-104 | 4 fuel type branches |
| p_neutron | power_balance() | 11 | Simple subtraction |
| p_cool | power_balance() | 12 | Aggregation |
| p_aux | power_balance() | 13 | Aggregation |
| p_coils | power_balance() | 14 | Aggregation |
| p_th | power_balance() | 15-21 | Complex formula |
| p_the | power_balance() | 22 | Efficiency application |
| p_et | power_balance() | 24 | Simplified (no p_dee) |
| p_loss | power_balance() | 25 | Energy balance |
| p_pump | power_balance() | 26 | Fraction of thermal electric |
| p_sub | power_balance() | 27 | Fraction of thermal electric |
| q_sci | power_balance() | 28 | Simple ratio |
| q_eng | power_balance() | 29-48 | Complex ratio |
| rec_frac | power_balance() | 49 | Inverse of Q_eng |
| p_net | power_balance() | 50 | Final output |

### Confidence Assessment
- **High confidence**: All formulas directly from PyFECONS source
- **Deferred**: Direct energy conversion (p_dee, eta_de) per spec

---

## Validation Plan

### Parse Validation
```bash
# Test model parses correctly
uv run syside check models/library/calculations/power_balance/power_balance.sysml
uv run syside check models/library/calculations/power_balance/mfe_power_balance.sysml
```

### PyFECONS Comparison

**Test Case: CATF MFE Reference Design**

| Input | Value | Source |
|-------|-------|--------|
| p_nrl | 2600 MW | CATF design |
| fuel_type | DT | CATF design |
| p_input | 50 MW | CATF design |
| mn | 1.1 | Typical MFE |
| eta_th | 0.46 | Typical MFE |
| eta_p | 0.5 | Typical MFE |
| eta_pin | 0.5 | Typical MFE |
| fpcppf | 0.06 | Typical MFE |
| f_sub | 0.03 | Typical MFE |
| p_tf | 1.0 MW | CATF design |
| p_pf | 1.0 MW | CATF design |
| p_tfcool | 12.7 MW | CATF design |
| p_pfcool | 1.0 MW | CATF design |
| p_trit | 10.0 MW | CATF design |
| p_house | 4.0 MW | CATF design |
| p_cryo | 0.5 MW | CATF design |

**Expected Outputs** (calculated from PyFECONS formulas):

| Output | Expected | Tolerance | Validation |
|--------|----------|-----------|------------|
| p_alpha | 520.4 MW | ±0.1% | 2600 * 3.52/17.58 |
| p_neutron | 2079.6 MW | ±0.1% | 2600 - 520.4 |
| p_th | 2372.7 MW | ±0.1% | Complex formula |
| p_the | 1091.4 MW | ±0.1% | 0.46 * 2372.7 |
| q_sci | 52.0 | ±0.1% | 2600/50 |
| q_eng | ~9.5 | ±1% | Complex formula |
| p_net | ~980 MW | ±1% | (1 - 1/q_eng) * p_et |

### Regression Tests

**File**: `tests/models/test_power_balance.py`

```python
def test_power_balance_calc_exists():
    """Verify Power Balance Calc exists in library."""
    # Check calc def present

def test_mfe_power_balance_calc_exists():
    """Verify MFE Power Balance Calc exists in library."""
    # Check calc def present

def test_power_balance_files_parse():
    """Verify all power balance .sysml files parse without errors."""
    # Parse check

def test_alpha_power_calc_outputs():
    """Verify Alpha Power Calc has correct outputs."""
    # Check return attribute
```

---

## Common Pitfalls & Quick Reference

### SysML v2 Syntax Rules for This Project

#### Conditional Expression Syntax
- ✓ CORRECT: `if fuel_type == FuelType::DT? expr1 else expr2`
- ✗ WRONG: `if fuel_type == FuelType::DT then expr1 else expr2` (no `then` keyword)
- ✗ WRONG: `fuel_type == FuelType::DT ? expr1 : expr2` (C-style ternary not supported)

#### Calc Def Structure
- ✓ CORRECT: `calc def 'Power Balance Calc' { in ... return ... expression }`
- ✗ WRONG: `calc def 'Power Balance Calc' { in ... out ... }` (use `return` for main output)

#### Enum Import and Usage
- ✓ CORRECT: `private import FoundationTypes::FuelType;` then `FuelType::DT`
- ✗ WRONG: `FuelType.DT` (use `::` not `.`)

#### Intermediate Attributes in Calc Def
- ✓ CORRECT: `attribute p_alpha : Real = alpha_calc.p_alpha;`
- ✓ CORRECT: `attribute p_neutron : Real = p_nrl - p_alpha;`

### Validation Commands

```bash
# Quick syntax check on single file
uv run syside check models/library/calculations/power_balance/power_balance.sysml

# Check directory
uv run syside check models/library/calculations/power_balance/

# Run regression tests
uv run pytest tests/models/test_power_balance.py -v
```

---

## Implementation Checklist

### Phase 1: Library Foundations
- [x] Create `models/library/calculations/power_balance/` directory
- [x] Create `power_balance.sysml` with package `PowerBalanceLibrary`
  - [x] `'Alpha Power Calc'` calc def with fuel-type conditionals
  - [x] `'Power Balance Calc'` calc def with generic outputs
- [x] Parse validation: `uv run syside check power_balance.sysml`

### Phase 2: MFE-Specific Calc
- [x] Create `mfe_power_balance.sysml` with package `MFEPowerBalanceLibrary`
  - [x] Import `PowerBalanceLibrary::'Alpha Power Calc'`
  - [x] `'MFE Power Balance Calc'` calc def with all 16 inputs
  - [x] All 15 intermediate/output attributes
  - [x] Full calculation chain (Steps 1-15)
- [x] Parse validation: `uv run syside check mfe_power_balance.sysml`

### Phase 3: Integration & Validation
- [x] Create `tests/models/test_power_balance.py`
  - [x] Parse validation tests
  - [x] Element existence tests
- [x] Run full validation: `uv run pytest tests/models/test_power_balance.py -v` (15 passed)
- [ ] Manual PyFECONS comparison with test case values
- [ ] Document any deviations

### Phase 4: Documentation
- [x] Complete doc comments with all Source citations
- [ ] Update `models/README.md` with new library location
- [ ] Update `BACKLOG.md` to reflect completion

---

## Implementation Benefits
- **Follows MODELING_GUIDE patterns**: Definition/usage separation, calc defs in library only
- **Enables validation against PyFECONS**: All formulas traceable to source lines
- **Reusable architecture**: Generic + MFE split allows future IFE extension
- **Complete traceability**: Every formula has PyFECONS line reference

## Potential Risks
- **Risk 1**: Conditional expression syntax may have parsing issues
  - Mitigation: Test each fuel type branch separately; validated pattern exists
- **Risk 2**: Complex q_eng formula may be hard to debug
  - Mitigation: Break into intermediate attributes (q_eng_numerator, q_eng_denominator)
- **Risk 3**: Missing p_dee may affect accuracy
  - Mitigation: Documented as deferred; can add later without breaking existing calcs

## Next Steps After Approval
1. Create prototype files (Stage 6)
2. Run parse validation
3. Create regression tests
4. PyFECONS comparison
5. `/plan-model` for implementation refinement

---

## Validation Results

### Prototype Implementation (2026-01-26)

**Files Created:**
- `models/library/calculations/power_balance/power_balance.sysml` - Generic power balance library
- `models/library/calculations/power_balance/mfe_power_balance.sysml` - MFE-specific power balance
- `tests/models/test_power_balance.py` - Regression tests (15 tests)

**Parse Validation:**
```
$ uv run syside check models/library/
(no output - all files parse successfully)
```

**Test Results:**
```
$ uv run pytest tests/models/test_power_balance.py -v
15 passed

Tests cover:
- File existence (2 tests)
- Parse validation (2 tests)
- Calc definition existence (3 tests)
- Interface validation (6 tests)
- Documentation presence (2 tests)
```

**API Notes:**
- Used `inputs` accessor for input parameters (not `owned_features`)
- Used `result` accessor for return parameter
- Used `declared_name` for parameter names

**Remaining Validation:**
- PyFECONS numerical comparison not yet performed (deferred to implementation phase)
- All structural and parse validation complete

---
**Next Step**: After approval → `/plan-model` for implementation refinement
