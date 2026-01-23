# Model Enhancement Specification: Cost Patterns Demo (Coffee Maker)

**Type**: Model Enhancement
**Modeling Scope**: New Models (test/validation models)
**Epic:** Cost Modeling Patterns De-Risking (P0, blocking Phase 4)
**Status:** Draft
**Owner:** Reid Westwood
**Created:** 2026-01-12
**Last Updated:** 2026-01-12

## Overview

Create a "coffee maker" demo model using Pattern A (nested cost models) to validate that the SysML v2 cost modeling patterns compile, are AST-traversable, and support the required output format before investing in sysml-codegen tooling upgrades.

## Current State

### Existing Models

None - creating new models. The `models/tests/` directory is empty.

### Known Issues

- Cost modeling pattern has been researched but not validated in practice
- sysml-codegen tooling gap is theoretical - need to prove SysML patterns work first
- No existing test cases for nested cost model pattern with multiplicity or allocation costs

## Modeling Requirements

### MR-001: Costed Component Interface

- **Type**: Functional
- **Description**: The model SHALL define an abstract `'Costed Component'` part def in `models/tests/coffee_maker/library.sysml`
- **Priority**: Must Have
- **Rationale**: Establishes the standard cost interface per research findings
- **Validation**: Part def exists with `capital_cost`, `raw_material_cost`, `fabrication_cost`, `installation_cost` attributes

### MR-002: Leaf Cost Calc Definitions

- **Type**: Functional
- **Description**: The model SHALL define 7 leaf cost calc defs in `models/tests/coffee_maker/library.sysml`
- **Priority**: Must Have
- **Rationale**: Each leaf part type needs its own cost calculation
- **Validation**: Calc defs exist: `HeatingElementCostCalc`, `WaterPumpCostCalc`, `BrewChamberCostCalc`, `WaterReservoirCostCalc`, `CarafeCostCalc`, `OuterShellCostCalc`, `ControlPanelCostCalc`

### MR-003: Allocation Cost Calc Definition

- **Type**: Functional
- **Description**: The model SHALL define 1 allocation cost calc def (`AllocationCostCalc`) for assembly-level minor items
- **Priority**: Must Have
- **Rationale**: Tests Rule R3 (allocation costs for fasteners, seals, etc.)
- **Validation**: Calc def exists with outputs for `fastener_cost`, `seal_cost`, `total_allocation`

### MR-004: Embedded Cost Model Pattern

- **Type**: Functional
- **Description**: Each leaf part def SHALL contain an embedded calc usage named `cost_model`
- **Priority**: Must Have
- **Rationale**: Validates Pattern A (nested cost models) and standard naming convention
- **Validation**: 7 leaf part defs each contain `calc cost_model : {PartType}CostCalc`

### MR-005: Assembly Cost Aggregation

- **Type**: Functional
- **Description**: Each assembly part def SHALL aggregate child `capital_cost` values plus allocation/overhead
- **Priority**: Must Have
- **Rationale**: Validates recursive rollup pattern (Rule R2)
- **Validation**: `'Brewing System'`, `'Housing'`, `'Coffee Maker'` part defs sum child costs

### MR-006: Design Instance

- **Type**: Functional
- **Description**: The model SHALL instantiate `coffee_maker` in `models/tests/coffee_maker/design.sysml` with all nested parts
- **Priority**: Must Have
- **Rationale**: Validates that design files are clean (just parameter bindings)
- **Validation**: Design file contains `part coffee_maker : 'Coffee Maker'` with full hierarchy

### MR-007: Multiplicity Test

- **Type**: Functional
- **Description**: The model SHALL include `heater [2]` multiplicity in the brewing system
- **Priority**: Must Have
- **Rationale**: Tests per-unit vs total cost rollup with arrayed parts
- **Validation**: `part heater : 'Heating Element' [2]` exists in brewing_system

### MR-008: AST Calc Usage Discovery

- **Type**: Functional
- **Description**: The AST validation script SHALL find all 7 leaf `cost_model` calc usages with owning part paths
- **Priority**: Must Have
- **Rationale**: Proves the pattern is traversable by tooling
- **Validation**: Script outputs all 7 calc usages with correct qualified paths

### MR-009: AST Binding Resolution

- **Type**: Functional
- **Description**: The AST validation script SHALL trace bindings through redefinition chains
- **Priority**: Must Have
- **Rationale**: Validates that sysml-codegen can resolve `:>> attribute = value` bindings
- **Validation**: Script identifies literal bindings from design parameter redefinitions

### MR-010: AST Allocation Detection

- **Type**: Functional
- **Description**: The AST validation script SHALL identify allocation costs at assembly level
- **Priority**: Must Have
- **Rationale**: Validates Rule R3 pattern is detectable
- **Validation**: Script finds `allocation_model` in `'Brewing System'`

### MR-011: Syntax Validation

- **Type**: Quality
- **Description**: All `.sysml` files SHALL parse without syntax errors
- **Priority**: Must Have
- **Rationale**: Basic syntax validation is prerequisite for all other validation
- **Validation**: `syside check models/tests/coffee_maker/*.sysml` returns exit code 0

### MR-012: Documentation Standards

- **Type**: Quality / Traceability
- **Description**: All part definitions and calc definitions SHALL have doc comments
- **Priority**: Should Have
- **Rationale**: Maintain documentation standards per MODELING_GUIDE
- **Validation**: Every `part def` and `calc def` has `doc /* ... */` block

### MR-013: Multi-Category Cost Outputs

- **Type**: Quality
- **Description**: All calc defs SHALL expose multi-category outputs (`raw_material_cost`, `fabrication_cost`, `installation_cost`, `total_cost`)
- **Priority**: Must Have
- **Rationale**: Enables BOM-like output with cost breakdown visibility
- **Validation**: Each leaf calc def has 4 output attributes

### MR-014: Assembly Calc Constraint

- **Type**: Constraint
- **Description**: Assembly part defs SHALL NOT have direct `cost_model` calc usages (only allocation calcs allowed)
- **Priority**: Must Have
- **Rationale**: Enforces Rule R2 - assemblies aggregate, leaves calculate
- **Validation**: `'Brewing System'`, `'Housing'`, `'Coffee Maker'` have no `cost_model`, only optional `allocation_model`

### MR-015: Idiot Index Formula

- **Type**: Constraint
- **Description**: The `idiot_index` attribute SHALL be computed as `capital_cost / raw_material_cost`
- **Priority**: Should Have
- **Rationale**: Standard efficiency metric per research
- **Validation**: Derived attribute formula matches specification

### MR-016: Expected Output CSV

- **Type**: Traceability
- **Description**: The expected output CSV SHALL document the target cost breakdown format
- **Priority**: Must Have
- **Rationale**: Defines Stage 2 deliverable for stakeholder approval
- **Validation**: CSV file exists with columns: `path`, `quantity`, `unit_cost`, `raw_material_cost`, `fabrication_cost`, `installation_cost`, `total_cost`, `idiot_index`, `cost_type`

### MR-017: Research Traceability

- **Type**: Traceability
- **Description**: Model patterns SHALL trace to research documents
- **Priority**: Should Have
- **Rationale**: Maintain traceability to architecture decisions
- **Validation**: Doc comments reference `20260107-final-cost-architecture.md` and `20260110-strategic-cost-patterns.md`

## Scope Boundaries

### In Scope

- `models/tests/coffee_maker/library.sysml` - Abstract interface, 8 calc defs, 10 part defs
- `models/tests/coffee_maker/design.sysml` - `coffee_maker` instance with full hierarchy
- `models/tests/coffee_maker/validate_ast.py` - AST traversal script using SysIDE Python API
- `models/tests/coffee_maker/expected_output.csv` - Hand-crafted target output format

### Out of Scope

- sysml-codegen modifications (deferred to Stage 4 of epic)
- teax-simkit execution (out of scope for this epic)
- Full fusion plant models (future work)
- AACE metadata, confidence bands (deferred to v2 per epic)
- Uncertainty analysis / Monte Carlo (future)
- Real material costs or physics (pattern validation only)

## Success Criteria

### Functional Success

- [ ] All MR-001 through MR-010 implemented
- [ ] Model elements defined in correct locations (`library.sysml` vs `design.sysml`)
- [ ] AST script produces expected output

### Quality Success

- [ ] Parse validation: `syside check` passes (exit code 0)
- [ ] Documentation: All defs have doc comments

### Validation Success

- [ ] AST script finds all 7 leaf `cost_model` calc usages
- [ ] AST script traces bindings through multiplicity (`heater [2]`)
- [ ] AST script identifies allocation costs at assembly level
- [ ] Rollup math is manually verifiable (sum of children + allocation = parent)

## Assumptions & Risks

### Assumptions

- **A-001**: SysIDE Python API can traverse calc usages inside part definitions
  - Confidence: High
  - Impact if Wrong: Would need alternative AST traversal approach

- **A-002**: Redefinition semantics (`:>>`) propagate through nested part hierarchies
  - Confidence: High (validated in prior research)
  - Impact if Wrong: Pattern A would be invalidated

- **A-003**: Multiplicity (`[2]`) is accessible via AST for cost rollup
  - Confidence: Medium
  - Impact if Wrong: Would need workaround for arrayed parts

### Risks

- **R-001**: Pattern doesn't compile with `syside check`
  - Likelihood: Low
  - Impact: High
  - Mitigation: Similar patterns tested in prior research; iterate on syntax if needed

- **R-002**: AST traversal more complex than expected
  - Likelihood: Medium
  - Impact: Medium
  - Mitigation: Start simple, reference existing sysml-codegen extraction code

- **R-003**: Multiplicity handling requires special logic
  - Likelihood: Medium
  - Impact: Low
  - Mitigation: Can simplify to single instances if blocking; document limitation

## Traceability

### Source Requirements

- Research: `modeling_pm/research/20260107-final-cost-architecture.md` - Pattern A architecture
- Research: `modeling_pm/research/20260110-strategic-cost-patterns.md` - Standardization decisions, output schema
- Epic: `modeling_pm/backlog/epic-cost-patterns-derisking.md` - Stage 1 requirements

### Downstream Impacts

- This validates patterns before Phase 4 (Cost Calculations) implementation
- AST script findings will inform sysml-codegen upgrade specification (Stage 4)
- Expected output format will be used for full fusion model cost reporting

## Target Hierarchy

```
CoffeeMaker (assembly)
├── BrewingSystem (assembly + allocation costs)
│   ├── HeatingElement [2] (leaf, arrayed)  ← tests multiplicity
│   ├── WaterPump (leaf)
│   └── BrewChamber (leaf)
│   └── [allocation: fasteners, seals, wiring harness]
├── WaterReservoir (leaf)
├── Carafe (leaf)
└── Housing (assembly)
    ├── OuterShell (leaf)
    └── ControlPanel (leaf)
```

## Acceptance Criteria Checklist

- [ ] All MR-XXX requirements implemented
- [ ] Functional success criteria met
- [ ] Quality success criteria met (`syside check` passes)
- [ ] Validation success criteria met (AST script finds all calcs, traces bindings)
- [ ] No regressions in existing models (N/A - no existing models)
- [ ] Documentation complete (doc comments in models)
- [ ] Epic Stage 1 exit criteria met

## Related Artifacts

**Research**: `modeling_pm/research/20260107-final-cost-architecture.md`
**Research**: `modeling_pm/research/20260110-strategic-cost-patterns.md`
**Epic**: `modeling_pm/backlog/epic-cost-patterns-derisking.md`
**Design**: `modeling_pm/active/cost-patterns-demo/design.md` (to be created)
**Plan**: `modeling_pm/active/cost-patterns-demo/plan.md` (to be created)

---
**Next Steps**: After approval → `/design-model`
