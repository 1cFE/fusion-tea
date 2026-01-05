# Model Enhancement Specification: Phase 1 - Foundation Library

**Type**: Model Enhancement
**Modeling Scope**: New Models
**Epic:** Phase 1 - Foundation Library
**Status:** Draft
**Owner:** Reid Westwood
**Created:** 2026-01-05
**Last Updated:** 2026-01-05

## Overview

Create the foundational SysML v2 library infrastructure for FusionTEA, including package structure, standard imports, enumerations, and the core PowerBalanceCalc definition. This enables all downstream CATF modeling work.

## Current State

### Existing Models
None - creating new models. The `models/` directory contains no `.sysml` files.

### Known Issues
- No model infrastructure exists
- Cannot begin any design work without foundation
- No reusable calculation definitions available

## Modeling Requirements

### MR-001: FusionTEA Package Structure
- **Type**: Functional
- **Description**: The model SHALL define package `FusionTEA` with nested `Library` and `Designs` packages in `models/library/foundation.sysml`
- **Priority**: Must Have
- **Rationale**: Establishes project-wide namespace per architecture research
- **Validation**: Package structure parseable, imports resolve

### MR-002: Standard Library Imports
- **Type**: Functional
- **Description**: The model SHALL import standard libraries (ScalarValues, ISQ, SI) in foundation
- **Priority**: Must Have
- **Rationale**: Required for unit-aware attributes per MODELING_GUIDE
- **Validation**: Imports resolve without errors

### MR-003: FuelType Enumeration
- **Type**: Functional
- **Description**: The model SHALL define enum `FuelType` with values DT, DD, DHE3, PB11
- **Priority**: Must Have
- **Rationale**: Fuel type determines alpha power fraction (PyFECONS `PowerBalance.py:94-105`)
- **Validation**: Enum parseable, all four values defined

### MR-004: Supporting Enumerations
- **Type**: Functional
- **Description**: The model SHALL define enums `ReactorType`, `ConfinementType`, `MagnetType`
- **Priority**: Must Have
- **Rationale**: Required for future design parameterization
- **Validation**: Enums parseable

### MR-005: PowerBalanceCalc Definition
- **Type**: Functional
- **Description**: The model SHALL define `PowerBalanceCalc` calc def in `models/library/calculations/power_balance.sysml`
- **Priority**: Must Have
- **Rationale**: Core calculation driving all downstream analyses
- **Validation**: Calc def parseable with all inputs/outputs

### MR-006: PowerBalanceCalc Inputs
- **Type**: Functional
- **Description**: The model SHALL implement all PowerBalanceCalc inputs matching PyFECONS parameters: p_nrl, fuel_type, mn, eta_th, eta_de, eta_p, eta_pin, p_input, p_tf, p_pf, p_tfcool, p_pfcool, p_trit, p_house, p_cryo, fpcppf, f_sub
- **Priority**: Must Have
- **Rationale**: Full fidelity to PyFECONS `PowerBalance.py:8-50`
- **Validation**: All 17 input parameters defined

### MR-007: PowerBalanceCalc Outputs
- **Type**: Functional
- **Description**: The model SHALL implement all PowerBalanceCalc outputs: p_alpha, p_neutron, p_th, p_the, p_dee, p_et, p_loss, p_pump, p_sub, p_cool, p_coils, p_aux, p_net, q_sci, q_eng, rec_frac
- **Priority**: Must Have
- **Rationale**: Complete power table for downstream calculations
- **Validation**: All 16 output parameters defined with formulas

### MR-008: Fuel-Dependent Alpha Power
- **Type**: Functional
- **Description**: The model SHALL implement fuel-type-dependent alpha power calculation
- **Priority**: Must Have
- **Rationale**: Different fusion reactions have different charged particle fractions (PyFECONS `PowerBalance.py:94-105`)
- **Validation**: Conditional logic for DT, DD, DHE3, PB11

### MR-009: Documentation Standards
- **Type**: Quality / Traceability
- **Description**: All definitions SHALL have doc comments with source citations
- **Priority**: Must Have
- **Rationale**: Maintain traceability per MODELING_GUIDE documentation standards
- **Validation**: Every `calc def`, `enum def`, package has doc comment

### MR-010: Parse Validation
- **Type**: Quality
- **Description**: All files SHALL parse without syntax errors using SysIDE
- **Priority**: Must Have
- **Rationale**: Basic correctness gate
- **Validation**: `syside check` exits with code 0

### MR-011: Source Traceability
- **Type**: Traceability
- **Description**: PowerBalanceCalc SHALL cite PyFECONS source file and line numbers
- **Priority**: Must Have
- **Rationale**: Enable verification against reference implementation
- **Validation**: Doc comment includes `**File**: pyfecons/costing/mfe/PowerBalance.py` and line references

## Scope Boundaries

### In Scope
- `models/library/foundation.sysml` - Package structure, imports, enums
- `models/library/calculations/power_balance.sysml` - PowerBalanceCalc calc def
- Full fidelity to PyFECONS power balance (17 inputs, 16 outputs)
- All four fuel types (DT, DD, DHE3, PB11)

### Out of Scope
- Design usages in `models/designs/` (Phase 3)
- Geometry calculations (Phase 2)
- Magnet part definitions (Phase 2)
- Cost calculations (Phase 4)
- Materials library (Phase 5)
- Automated PyFECONS comparison testing

## Success Criteria

### Functional Success
- [ ] All MR-001 through MR-008 implemented
- [ ] Package structure defined with correct hierarchy
- [ ] All enumerations defined (FuelType, ReactorType, ConfinementType, MagnetType)
- [ ] PowerBalanceCalc has all 17 inputs and 16 outputs
- [ ] Alpha power calculation handles all four fuel types

### Quality Success
- [ ] Parse validation: All `.sysml` files parse without errors (`syside check` exits 0)
- [ ] Documentation: All definitions have doc comments
- [ ] Naming conventions followed (Title Case for defs, snake_case for attributes)

### Traceability Success
- [ ] PyFECONS source citations present in doc comments
- [ ] File paths and line numbers referenced for key calculations

## Assumptions & Risks

### Assumptions
- **A-001**: SysIDE parser supports all required SysML v2 syntax (enums, calc defs, conditionals)
  - Confidence: High
  - Impact if Wrong: May need syntax workarounds

- **A-002**: Conditional expressions (ternary) work in calc def output formulas for fuel-type logic
  - Confidence: Medium
  - Impact if Wrong: May need separate calc defs per fuel type

### Risks
- **R-001**: SysML v2 expression limitations may prevent direct translation of PyFECONS formulas
  - Likelihood: Low
  - Impact: Medium
  - Mitigation: Simplify expressions, use intermediate attributes if needed

- **R-002**: Enum syntax may differ from expected
  - Likelihood: Low
  - Impact: Low
  - Mitigation: Check SysIDE documentation, test incrementally

## Traceability

### Source Requirements
- PyFECONS: `/home/reid/PyFECONS/pyfecons/costing/mfe/PowerBalance.py` (lines 1-105)
- PyFECONS: `/home/reid/PyFECONS/pyfecons/enums.py` (FuelType enum)
- Architecture: `project/research/20260105-103000_catf-mfe-architecture.md`

### Downstream Impacts
- Phase 2 (Geometry): Will import foundation.sysml
- Phase 3 (CATF Design): Will instantiate PowerBalanceCalc
- All future library additions: Will use FusionTEA package namespace

## Acceptance Criteria Checklist

- [ ] All MR-001 through MR-011 requirements implemented
- [ ] Functional success criteria met
- [ ] Quality success criteria met (parse passes, docs complete)
- [ ] Traceability success criteria met (source citations)
- [ ] No regressions in existing models (N/A - first models)
- [ ] Documentation complete (doc comments in models)
- [ ] Epic progress updated in BACKLOG.md

## Related Artifacts
**Research**: `project/research/20260105-103000_catf-mfe-architecture.md`
**Epic**: `project/backlog/BACKLOG.md` (Phase 1 - Foundation Library)
**PyFECONS Sources**:
- `/home/reid/PyFECONS/pyfecons/costing/mfe/PowerBalance.py`
- `/home/reid/PyFECONS/pyfecons/enums.py`
**Design**: `project/active/phase1-foundation/design.md` (to be created)
**Plan**: `project/active/phase1-foundation/plan.md` (to be created)

---
**Next Steps**: After approval → `/design-model`
