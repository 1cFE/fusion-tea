# Model Enhancement Specification: Coffee Maker Pattern Fixes

**Type**: Model Enhancement
**Modeling Scope**: Enhance Existing
**Epic:** Cost Modeling Patterns De-Risking (P0)
**Status:** Draft
**Owner:** Reid Westwood
**Created:** 2026-01-12
**Last Updated:** 2026-01-12

## Overview

Fix the coffee maker demo model to use validated SysML v2 patterns for cost rollup with multiplicity. The current implementation uses hardcoded placeholder values that defeat the purpose of automatic cost aggregation.

## Current State

### Existing Models

- **File**: `models/tests/coffee_maker/library.sysml`
  - Relevant elements: `'Brewing System'` part def (lines 382-440)
  - Current capabilities: Declares `part heater : 'Heating Element' [2]` but uses placeholder attributes
  - **Issue**: Lines 411-414 declare `heater_total_cost`, `heater_total_material`, etc. as manual placeholders

- **File**: `models/tests/coffee_maker/design.sysml`
  - Relevant elements: `coffee_maker` instantiation (lines 12-56)
  - Current capabilities: Binds placeholder values
  - **Issue**: Lines 33-36 hardcode `26.25`, `15.0`, `9.0`, `2.25` - values that will drift

### Known Issues

1. **Missing Import**: No `import NumericalFunctions::sum` - the function exists but wasn't imported
2. **Hardcoded Values**: `heater_total_cost = 26.25` defeats automatic rollup
3. **Shadowing Warnings**: Re-declaring parts like `part heater : 'Heating Element' [2]` in usages causes warnings
4. **Fixed Multiplicity**: `[2]` is hardcoded in definition, not parameterized

### Root Cause

Prior research incorrectly concluded `sum()` doesn't exist. See: `modeling_pm/research/20260112-055807_multiplicity-cost-rollup-gap.md` and `modeling_pm/research/20260112-061548_sysmlv2-discovery-reflection.md`

## Modeling Requirements

### MR-001: Import NumericalFunctions::sum

- **Type**: Functional
- **Description**: The model SHALL import `NumericalFunctions::sum` in `library.sysml`
- **Priority**: Must Have
- **Rationale**: Required for automatic cost aggregation over multiplicities
- **Validation**: Import statement exists at top of file

### MR-002: Remove Placeholder Attributes

- **Type**: Functional
- **Description**: The model SHALL remove `heater_total_cost`, `heater_total_material`, `heater_total_fab`, `heater_total_install` placeholder attributes from `'Brewing System'`
- **Priority**: Must Have
- **Rationale**: These were workarounds for missing `sum()` import
- **Validation**: Attributes no longer exist in part def

### MR-003: Use sum() for Multiplicity Aggregation

- **Type**: Functional
- **Description**: The `'Brewing System'` part def SHALL use `sum(heater.capital_cost)` for cost aggregation
- **Priority**: Must Have
- **Rationale**: Enables automatic rollup regardless of multiplicity count
- **Validation**: `:>> capital_cost = sum(heater.capital_cost) + pump.capital_cost + ...`

### MR-004: Parameterized Multiplicity

- **Type**: Functional
- **Description**: Part multiplicities SHALL be parameterizable via attributes where appropriate
- **Priority**: Should Have
- **Rationale**: Allows design files to set counts without modifying definitions
- **Validation**: `'Brewing System'` has `attribute heater_count` with `part heater[heater_count]`

### MR-005: Dot Notation for Attribute Binding

- **Type**: Functional
- **Description**: Design usages SHALL use dot notation (`:>> heater.power_rating = 1000.0`) instead of re-declaring parts
- **Priority**: Must Have
- **Rationale**: Avoids shadowing warnings, cleaner syntax
- **Validation**: No `part heater : 'Heating Element'` re-declarations in design.sysml

### MR-006: Explicit Redefines When Needed

- **Type**: Functional
- **Description**: When parts need additional features in usages, the model SHALL use `part redefines heater { ... }`
- **Priority**: Should Have
- **Rationale**: Explicit intent, no shadowing warnings
- **Validation**: Any nested part specializations use `redefines` keyword

### MR-007: Remove Hardcoded Values from Design

- **Type**: Functional
- **Description**: The design file SHALL NOT contain manually calculated aggregate values
- **Priority**: Must Have
- **Rationale**: Values should flow automatically from component calculations
- **Validation**: No literal values like `26.25` for aggregate costs in design.sysml

### MR-008: No Shadowing Warnings

- **Type**: Quality
- **Description**: `syside check` SHALL produce no warnings about member name shadowing
- **Priority**: Must Have
- **Rationale**: Warnings indicate semantic ambiguity
- **Validation**: `syside check models/tests/coffee_maker/*.sysml` produces only parse success or acceptable warnings

### MR-009: Update Documentation

- **Type**: Traceability
- **Description**: Doc comments SHALL reference the corrected pattern research
- **Priority**: Should Have
- **Rationale**: Maintain traceability to discovery
- **Validation**: Doc comments reference `20260112-055807_multiplicity-cost-rollup-gap.md`

### MR-010: Validate Recursive Rollup

- **Type**: Functional
- **Description**: Multi-level aggregation SHALL work (e.g., `sum(brewing.capital_cost)` where brewing uses `sum(heater.capital_cost)`)
- **Priority**: Must Have
- **Rationale**: Fusion plant will have 4+ hierarchy levels
- **Validation**: `'Coffee Maker'` correctly aggregates from `'Brewing System'` which aggregates from `'Heating Element'`

## Scope Boundaries

### In Scope

- `models/tests/coffee_maker/library.sysml` - Add import, remove placeholders, use sum()
- `models/tests/coffee_maker/design.sysml` - Use dot notation, remove hardcoded values
- `modeling_pm/backlog/epic-cost-patterns-derisking.md` - Add validated pattern notes
- `modeling_pm/MODELING_GUIDE.md` - Add NumericalFunctions import requirement

### Out of Scope

- Other test models in `models/tests/`
- sysml-codegen modifications
- Creating new components

## Success Criteria

### Functional Success

- [ ] `sum(heater.capital_cost)` correctly aggregates heater costs
- [ ] Multiplicity can be changed in design without modifying library
- [ ] Cost values flow automatically (no manual calculation)

### Quality Success

- [ ] Parse validation: `syside check` passes with exit code 0
- [ ] Warning-free: No shadowing warnings
- [ ] Documentation updated with corrected pattern

### Validation Success

- [ ] Changing `heater.material_mass` in design automatically updates `brewing.capital_cost`
- [ ] Pattern works for 3-level hierarchy (Coffee Maker → Brewing System → Heating Element)

## Assumptions & Risks

### Assumptions

- **A-001**: `NumericalFunctions::sum` works correctly for cost aggregation
  - Confidence: High (validated in `models/tests/multiplicity_cost_rollup_validated.sysml`)
  - Impact if Wrong: Would need alternative aggregation approach

- **A-002**: Parameterized multiplicity (`[heater_count]`) evaluates correctly
  - Confidence: High (validated in `models/tests/pattern_d_multiplicity_test.sysml`)
  - Impact if Wrong: Would use fixed multiplicity with sum()

### Risks

- **R-001**: sum() works for parsing but not for sysml-codegen extraction
  - Likelihood: Low
  - Impact: Medium
  - Mitigation: Pattern is standard SysML v2; codegen can be updated if needed

## Traceability

### Source Requirements

- Research: `modeling_pm/research/20260112-055807_multiplicity-cost-rollup-gap.md` - Discovered `sum()` works
- Research: `modeling_pm/research/20260112-061548_sysmlv2-discovery-reflection.md` - Process lessons
- Standard Library: `syside/sysml.library/Kernel Libraries/Kernel Function Library/NumericalFunctions.kerml`

### Downstream Impacts

- Epic: Updates `modeling_pm/backlog/epic-cost-patterns-derisking.md` with validated pattern
- Guide: Updates `modeling_pm/MODELING_GUIDE.md` with required imports
- Phase 4: Unblocks cost calculation implementation with correct patterns

## Validated Patterns (from testing today)

### Pattern B: Dot Notation (Recommended for simple binding)

```sysml
part brewing_system : 'Brewing System' {
    :>> heater.power_rating = 1000.0;
    :>> heater.material_mass = 0.15;
}
```

### Pattern C: Explicit Redefines (When adding features)

```sysml
part brewing_system : 'Brewing System' {
    part redefines heater {
        :>> power_rating = 1000.0;
        :>> material_mass = 0.15;
    }
}
```

### Multiplicity Aggregation

```sysml
private import NumericalFunctions::sum;

part def 'Brewing System' {
    part heater : 'Heating Element' [2];
    :>> capital_cost = sum(heater.capital_cost) + pump.capital_cost;
}
```

### Parameterized Multiplicity

```sysml
part def 'Brewing System' {
    attribute heater_count : Integer default := 2;
    part heater : 'Heating Element' [heater_count];
}
```

## Test Files Created During Discovery

| File | Purpose | Status |
|------|---------|--------|
| `models/tests/multiplicity_sum_test.sysml` | Initial sum() test (no import) | ❌ Failed |
| `models/tests/multiplicity_sum_import_test.sysml` | sum() with import | ✅ Passed |
| `models/tests/multiplicity_alternatives_test.sysml` | Alternative patterns | ✅ Passed |
| `models/tests/multiplicity_cost_rollup_validated.sysml` | Complete pattern | ✅ Passed |
| `models/tests/redefinition_patterns_test.sysml` | Dot notation vs redefines | ✅ Passed |
| `models/tests/pattern_b_detailed_test.sysml` | Dot notation detail | ✅ Passed |
| `models/tests/pattern_c_detailed_test.sysml` | Redefines detail | ✅ Passed |
| `models/tests/pattern_d_multiplicity_test.sysml` | Parameterized multiplicity | ✅ Passed |

## Acceptance Criteria Checklist

- [ ] All MR-XXX requirements implemented
- [ ] Functional success criteria met
- [ ] Quality success criteria met (no shadowing warnings)
- [ ] Validation success criteria met (automatic rollup works)
- [ ] Epic updated with validated patterns
- [ ] MODELING_GUIDE updated with required imports
- [ ] Documentation complete

## Related Artifacts

**Research**: `modeling_pm/research/20260112-055807_multiplicity-cost-rollup-gap.md`
**Research**: `modeling_pm/research/20260112-061548_sysmlv2-discovery-reflection.md`
**Epic**: `modeling_pm/backlog/epic-cost-patterns-derisking.md`
**Existing Spec**: `modeling_pm/active/cost-patterns-demo/spec.md`

---
**Next Steps**: After approval → Implement changes to library.sysml and design.sysml
