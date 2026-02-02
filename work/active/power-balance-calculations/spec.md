---
Status: completed
Scale: standard
Epic: Power Balance Calculations
Owner: Reid Westwood
Created: 2026-01-26
Updated: 2026-01-26
---

# Model Enhancement Specification: Power Balance Calculations

**Type**: Model Enhancement
**Modeling Scope**: New Models
**Epic:** Power Balance Calculations (P0)
**Status:** Complete
**Owner:** Reid Westwood
**Created:** 2026-01-26
**Last Updated:** 2026-01-26

## Overview

Implement power balance calculations that compute fusion power flow from input parameters to key outputs (p_alpha, p_neutron, p_th, p_net, q_eng). These calculations drive most downstream cost and sizing calculations. The implementation uses explicit generic/MFE split architecture for future extensibility to IFE.

## Current State

### Existing Models
- **File**: `models/library/foundation/types.sysml`
  - `FuelType` enum (DT, DD, DHE3, PB11) - lines 64-78
  - `ReactorType` enum (MFE, IFE, MIF) - lines 14-23
  - `EnergyConversion` enum (DIRECT, TURBINE) - lines 50-58
- **File**: `models/library/foundation/units.sysml`
  - SI unit imports and custom unit definitions
- **File**: `models/library/foundation/materials.sysml`
  - Material part definitions (not directly relevant but available)

### Known Issues
- No power balance calculations exist yet
- No calculation definition infrastructure in `library/calculations/`
- Downstream epics (Power Core, Geometry, CATF Design) depend on power balance outputs

## Modeling Requirements

### MR-001: Generic Power Balance Calc Definition
- **Type**: Functional
- **Description**: The model SHALL define a generic `'Power Balance Calc'` calc def in `models/library/calculations/power_balance/power_balance.sysml` with concept-agnostic inputs and outputs
- **Priority**: Must Have
- **Rationale**: Generic calc enables reuse across MFE, IFE, and future reactor concepts
- **Validation**: File parses without errors; calc def has required inputs/outputs
- **Test Assertion**: `"Power Balance Calc" in [c.name for c in model.elements(CalcDefinition)]`

### MR-002: Alpha Power Calculation
- **Type**: Functional
- **Description**: The model SHALL compute `p_alpha` (charged particle power) from fusion power and fuel type for all 4 fuel types (DT, DD, DHE3, PB11) using conditional expressions
- **Priority**: Must Have
- **Rationale**: Alpha power fraction determines energy partition and varies by fuel type
- **Validation**: PyFECONS comparison - `compute_p_alpha()` at PowerBalance.py:94-104
- **Test Assertion**: For DT fuel with p_nrl=500 MW, p_alpha ≈ 100.1 MW (500 * 3.52/17.58)

### MR-003: Neutron Power Calculation
- **Type**: Functional
- **Description**: The model SHALL compute `p_neutron` as `p_nrl - p_alpha`
- **Priority**: Must Have
- **Rationale**: Neutron power drives blanket heating and tritium breeding
- **Validation**: PyFECONS comparison - PowerBalance.py:11
- **Test Assertion**: `p_neutron = p_nrl - p_alpha`

### MR-004: MFE Power Balance Calc Definition
- **Type**: Functional
- **Description**: The model SHALL define `'MFE Power Balance Calc'` calc def in `models/library/calculations/power_balance/mfe_power_balance.sysml` that specializes generic power balance with MFE-specific power flows
- **Priority**: Must Have
- **Rationale**: MFE has specific recirculating power paths (coils, cooling, pumping) not present in IFE
- **Validation**: File parses without errors; calc def specializes generic
- **Test Assertion**: `"MFE Power Balance Calc" in [c.name for c in model.elements(CalcDefinition)]`

### MR-005: MFE Thermal Power Calculation
- **Type**: Functional
- **Description**: The model SHALL compute `p_th` (thermal power) using the MFE formula: `p_th = mn * p_neutron + p_input + eta_th * (fpcppf * eta_p + f_sub) * (mn * p_neutron)`
- **Priority**: Must Have
- **Rationale**: Thermal power determines turbine sizing and heat rejection requirements
- **Validation**: PyFECONS comparison - PowerBalance.py:15-21
- **Test Assertion**: Calculation matches PyFECONS within 0.1%

### MR-006: MFE Engineering Q Calculation
- **Type**: Functional
- **Description**: The model SHALL compute `q_eng` (engineering Q) as the ratio of gross electric output to total recirculating power input
- **Priority**: Must Have
- **Rationale**: Engineering Q is the key figure of merit for power plant viability
- **Validation**: PyFECONS comparison - PowerBalance.py:29-48
- **Test Assertion**: Calculation matches PyFECONS within 0.1%

### MR-007: MFE Net Electric Power Calculation
- **Type**: Functional
- **Description**: The model SHALL compute `p_net` as `(1 - 1/q_eng) * p_et` where `p_et` is gross electric power
- **Priority**: Must Have
- **Rationale**: Net electric power is the saleable output that drives LCOE
- **Validation**: PyFECONS comparison - PowerBalance.py:50
- **Test Assertion**: Calculation matches PyFECONS within 0.1%

### MR-008: MFE Recirculating Power Components
- **Type**: Functional
- **Description**: The model SHALL compute intermediate recirculating power values: `p_coils`, `p_cool`, `p_aux`, `p_pump`, `p_sub`
- **Priority**: Must Have
- **Rationale**: Component-level power breakdown enables subsystem sizing and costing
- **Validation**: PyFECONS comparison - PowerBalance.py:12-27
- **Test Assertion**: Each component matches PyFECONS within 0.1%

### MR-009: Scientific Q Calculation
- **Type**: Functional
- **Description**: The model SHALL compute `q_sci` (scientific Q) as `p_nrl / p_input`
- **Priority**: Should Have
- **Rationale**: Scientific Q is a standard physics metric for fusion performance
- **Validation**: PyFECONS comparison - PowerBalance.py:28
- **Test Assertion**: `q_sci = p_nrl / p_input`

### MR-010: Documentation with Source Citations
- **Type**: Quality / Traceability
- **Description**: All calc defs SHALL have doc comments citing PyFECONS source file and line numbers
- **Priority**: Must Have
- **Rationale**: Maintain traceability per project standards (MODELING_GUIDE.md)
- **Validation**: Level 6 documentation check - all calc defs have doc blocks with **Source** tags
- **Test Assertion**: All CalcDefinition elements have non-empty documentation

### MR-011: Unit Consistency
- **Type**: Quality
- **Description**: All power attributes SHALL use ISQ::PowerValue with SI units (MW implied)
- **Priority**: Must Have
- **Rationale**: Unit consistency prevents calculation errors and enables constraint checking
- **Validation**: Manual review of attribute types
- **Test Assertion**: Power attributes typed as `ISQ::PowerValue` or `Real` with documented unit

### MR-012: Regression Test Coverage
- **Type**: Quality
- **Description**: The model SHALL have pytest regression tests in `tests/models/test_power_balance.py` verifying parse success and element existence
- **Priority**: Must Have
- **Rationale**: Regression tests protect against library breakage per MODELING_GUIDE
- **Validation**: `pytest tests/models/test_power_balance.py` passes
- **Test Assertion**: Test file exists and all tests pass

## Scope Boundaries

### In Scope
- `models/library/calculations/power_balance/power_balance.sysml` - Generic PowerBalanceCalc with:
  - Inputs: p_nrl (fusion power), fuel_type, p_input (heating power)
  - Outputs: p_alpha, p_neutron, q_sci
  - Alpha power calculation with all 4 fuel type conditionals
- `models/library/calculations/power_balance/mfe_power_balance.sysml` - MfePowerBalanceCalc with:
  - Additional inputs: mn, eta_th, eta_p, fpcppf, f_sub, p_tf, p_pf, p_tfcool, p_pfcool, p_trit, p_house, p_cryo, eta_pin
  - Additional outputs: p_th, p_the, p_et, p_coils, p_cool, p_aux, p_pump, p_sub, p_loss, q_eng, rec_frac, p_net
- `tests/models/test_power_balance.py` - Regression tests

### Out of Scope
- Direct energy conversion (`p_dee`, `eta_de`) - deferred per user request
- IFE power balance (`ife_power_balance.sysml`) - separate epic
- Design usages (will be in `designs/catf_mfe/`) - separate epic
- Thermal electric power breakdown by source - simplified to single p_the

## Success Criteria

### Functional Success
- [x] MR-001: Generic PowerBalanceCalc defined with inputs/outputs
- [x] MR-002: Alpha power calculation works for all 4 fuel types
- [x] MR-003: Neutron power calculation implemented
- [x] MR-004: MfePowerBalanceCalc defined with MFE-specific flows
- [x] MR-005: Thermal power calculation implemented
- [x] MR-006: Engineering Q calculation implemented
- [x] MR-007: Net electric power calculation implemented
- [x] MR-008: Recirculating power components calculated
- [x] MR-009: Scientific Q calculation implemented

### Quality Success
- [x] Parse validation (Level 1): All .sysml files parse without syntax errors
- [x] Structural validation (Level 2): No unused definitions, complete interfaces
- [x] Documentation validation (Level 6): All calc defs have doc comments with Source citations
- [x] MR-010: Documentation complete with PyFECONS references
- [x] MR-011: Unit consistency verified
- [x] MR-012: Regression tests pass (25 tests)

### Validation Success
- [x] PyFECONS comparison: p_alpha matches `compute_p_alpha()` for all fuel types
- [x] PyFECONS comparison: p_th, q_eng, p_net formulas match (simplified - no p_dee)
- [x] Integration: Calc defs can be imported by future design files

## Assumptions & Risks

### Assumptions
- **A-001**: SysML conditional expressions support the branching needed for fuel type selection
  - Confidence: High (verified in SysML v2 spec)
  - Impact if Wrong: Would need separate calc defs per fuel type

- **A-002**: Foundation package FuelType enum is complete and correct
  - Confidence: High (verified against PyFECONS enums.py)
  - Impact if Wrong: Minor - add missing enum values

- **A-003**: ISQ power units are compatible with PyFECONS MW type
  - Confidence: High (both use SI base units)
  - Impact if Wrong: Add unit conversion layer

### Risks
- **R-001**: Complex q_eng formula may be difficult to express in single SysML expression
  - Likelihood: Medium
  - Impact: Medium
  - Mitigation: Break into intermediate calculations; use EXPOSE pattern for readability

- **R-002**: Conditional expression syntax for fuel type may have parsing issues
  - Likelihood: Low
  - Impact: Medium
  - Mitigation: Test each fuel type branch separately; have fallback to DT-only

## Traceability

### Source Requirements
- PyFECONS: `/home/reid/PyFECONS/pyfecons/costing/mfe/PowerBalance.py` (lines 1-105)
- PyFECONS: `/home/reid/PyFECONS/pyfecons/inputs/power_input.py` (lines 1-28)
- PyFECONS: `/home/reid/PyFECONS/pyfecons/costing/accounting/power_table.py` (lines 1-25)
- Research: `modeling_pm/research/20260123-pyfecons-library-mapping-strategy.md`

### Downstream Impacts
- **Designs affected**: Future `designs/catf_mfe/power_balance.sysml` will instantiate these calc defs
- **Epics affected**:
  - Power Core Definitions (P1) - will use p_th for thermal sizing
  - Geometry Calculations (P1) - independent but may need power values
  - First CATF MFE Design (P1) - will bind to power balance outputs
  - CAS22 Subsystem Costing (P2) - uses p_net for plant sizing

## Acceptance Criteria Checklist

- [x] All MR-XXX requirements implemented (MR-001 through MR-012)
- [x] Functional success criteria met (all calculations working)
- [x] Quality success criteria met (Levels 1, 2, 6 pass)
- [x] Validation success criteria met (PyFECONS comparison within tolerance)
- [x] No regressions in existing models (foundation package unchanged)
- [x] Regression tests added (`tests/models/test_power_balance.py` - 25 tests)
- [x] Documentation complete (doc comments in models with Source citations)
- [x] BACKLOG.md updated to reflect completion

## Related Artifacts
**Research**: `modeling_pm/research/20260123-pyfecons-library-mapping-strategy.md`
**Epic**: `modeling_pm/backlog/BACKLOG.md` - Power Balance Calculations (P0) - **COMPLETE**
**PyFECONS Sources**:
- `/home/reid/PyFECONS/pyfecons/costing/mfe/PowerBalance.py`
- `/home/reid/PyFECONS/pyfecons/inputs/power_input.py`
- `/home/reid/PyFECONS/pyfecons/costing/accounting/power_table.py`
**Design**: `modeling_pm/active/power-balance-calculations/design.md`
**Plan**: `modeling_pm/active/power-balance-calculations/plan.md`

---
**Status**: COMPLETE (2026-01-26)
