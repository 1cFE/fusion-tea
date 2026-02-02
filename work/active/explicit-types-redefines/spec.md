---
Status: failed
Scale: standard
Owner: Reid Westwood
Created: 2026-01-16
Updated: 2026-01-16
---

# Model Enhancement Specification: Explicit Types for Redefines Pattern

**Type**: Model Enhancement + Documentation Update
**Modeling Scope**: Enhance Existing
**Epic:** Tooling & Patterns (cross-cutting)
**Status:** Failed - Workaround Ineffective
**Owner:** Reid Westwood
**Created:** 2026-01-16
**Last Updated:** 2026-01-16

## Overview

Update the coffee_maker test models to use explicit types with `redefines` syntax to fix Tom Sawyer visualization issues. If successful, document this as the recommended pattern in MODELING_GUIDE.md.

## Current State

### Existing Models
- **File**: `models/tests/coffee_maker/design.sysml`
  - Relevant elements: Lines 20, 40, 45, 50 - bare `part redefines X` declarations
  - Current capabilities: Semantically correct, cost aggregation works
  - Issue: Tom Sawyer shows `<<part>>` instead of actual types

- **File**: `models/tests/coffee_maker/library.sysml`
  - No changes needed - defines types correctly

### Known Issues
- Tom Sawyer visualization only shows generic `<<part>>` for redefined features
- Types are derived (not explicit), requiring tools to follow redefinition chain
- This is a tool limitation documented in research

## Modeling Requirements

### MR-001: Add Explicit Type to Brewing Redefinition
- **Type**: Functional
- **Description**: The model SHALL update `part redefines brewing` to include explicit type `part redefines brewing : 'Brewing System'`
- **Priority**: Must Have
- **Rationale**: Provides type annotation for visualization tools while maintaining redefinition semantics
- **Validation**: Line 20 of design.sysml contains `: 'Brewing System'` after `redefines brewing`

### MR-002: Add Explicit Type to Reservoir Redefinition
- **Type**: Functional
- **Description**: The model SHALL update `part redefines reservoir` to include explicit type `part redefines reservoir : 'Water Reservoir'`
- **Priority**: Must Have
- **Rationale**: Consistency with MR-001
- **Validation**: Line 40 of design.sysml contains `: 'Water Reservoir'` after `redefines reservoir`

### MR-003: Add Explicit Type to Carafe Redefinition
- **Type**: Functional
- **Description**: The model SHALL update `part redefines carafe` to include explicit type `part redefines carafe : 'Carafe'`
- **Priority**: Must Have
- **Rationale**: Consistency with MR-001
- **Validation**: Line 45 of design.sysml contains `: 'Carafe'` after `redefines carafe`

### MR-004: Add Explicit Type to Housing Redefinition
- **Type**: Functional
- **Description**: The model SHALL update `part redefines housing` to include explicit type `part redefines housing : 'Housing'`
- **Priority**: Must Have
- **Rationale**: Consistency with MR-001
- **Validation**: Line 50 of design.sysml contains `: 'Housing'` after `redefines housing`

### MR-005: Model Parses Successfully
- **Type**: Quality
- **Description**: The updated model SHALL parse without syntax or semantic errors
- **Priority**: Must Have
- **Rationale**: Ensure explicit types don't break existing functionality
- **Validation**: `uv run syside check models/tests/coffee_maker/design.sysml` returns success

### MR-006: Visualization Shows Types
- **Type**: Quality / Validation
- **Description**: Tom Sawyer visualization SHALL display the explicit types for redefined parts
- **Priority**: Must Have
- **Rationale**: This is the primary goal of the enhancement
- **Validation**: Manual visual check in Syside Modeler - parts show `'Brewing System'`, `'Water Reservoir'`, etc. instead of `<<part>>`

### MR-007: Update MODELING_GUIDE.md with Explicit Types Convention
- **Type**: Traceability / Documentation
- **Description**: MODELING_GUIDE.md SHALL include guidance on using explicit types with redefines
- **Priority**: Should Have (only if MR-006 succeeds)
- **Rationale**: Establish project-wide convention for visualization compatibility
- **Validation**: MODELING_GUIDE.md contains new section on redefines pattern with explicit types

## Scope Boundaries

### In Scope
- Update `models/tests/coffee_maker/design.sysml` with explicit types on 4 redefinitions
- Verify parsing and visualization
- Update `modeling_pm/MODELING_GUIDE.md` with pattern guidance (conditional on success)

### Out of Scope
- Changes to `library.sysml` (no changes needed)
- Changes to other test models
- Changes to production models in `models/designs/` (future work if pattern validated)
- Tool configuration changes to Syside Modeler

## Success Criteria

### Functional Success
- [ ] All 4 redefinitions have explicit types (MR-001 through MR-004)
- [ ] Model elements unchanged semantically (same cost outputs)

### Quality Success
- [ ] Parse validation (Level 1): `syside check` passes (MR-005)
- [ ] No regressions in cost calculation behavior

### Validation Success
- [ ] Visualization shows actual types instead of `<<part>>` (MR-006)
- [ ] Documentation updated with convention (MR-007, conditional)

## Assumptions & Risks

### Assumptions
- **A-001**: Adding explicit types to redefinitions is syntactically valid in SysML v2
  - Confidence: High (confirmed in KerML spec research)
  - Impact if Wrong: Would need alternative approach

- **A-002**: Tom Sawyer reads explicit type annotations from redefinitions
  - Confidence: Medium (logical expectation, not tested)
  - Impact if Wrong: Need to investigate Tom Sawyer configuration or report to Sensmetry

### Risks
- **R-001**: Explicit types may not fix visualization
  - Likelihood: Low (types should be visible)
  - Impact: Medium (workaround doesn't solve problem)
  - Mitigation: If fails, report to Sensmetry as potential tool issue

- **R-002**: Pattern may have unintended semantic effects
  - Likelihood: Very Low (spec says this is equivalent)
  - Impact: Low (test model only)
  - Mitigation: Verify cost outputs unchanged before/after

## Traceability

### Source Requirements
- Research: `modeling_pm/research/20260116-170015_sysmlv2-redefines-semantics-visualization.md`
- KerML Spec: Section 7.3.4.5 (Redefinition allows combining with explicit typing)

### Downstream Impacts
- If successful: Pattern should be applied to future design files
- MODELING_GUIDE.md update affects all future modeling work

## Acceptance Criteria Checklist

- [x] MR-001 through MR-004: All redefinitions have explicit types
- [x] MR-005: Model parses successfully
- [x] MR-006: Visualization shows types (manual verification) - **FAILED** - Explicit types did NOT fix Tom Sawyer visualization
- [ ] MR-007: Documentation updated - **REVERTED** - Not adding convention since workaround doesn't work
- [x] No regressions in cost calculation outputs (model parses, semantically equivalent)
- [x] Research document referenced in implementation

## Outcome

**Result**: The hypothesis that adding explicit types to redefinitions would fix Tom Sawyer visualization was **incorrect**. The tool still shows generic `<<part>>` for redefined features regardless of whether explicit types are provided.

**Conclusion**: This is a deeper tool limitation in Tom Sawyer/Syside Modeler that cannot be worked around with syntax changes. The visualization issue appears to be in how the tool handles redefined features, not in type derivation.

**Next Steps**:
- Consider reporting to Sensmetry as a feature request/bug
- Explore alternative visualization tools (SysON, CATIA Magic) per visualization research
- Keep the explicit types in the test model (no harm, slightly more self-documenting) but don't establish as required convention

## Related Artifacts
**Research**: `modeling_pm/research/20260116-170015_sysmlv2-redefines-semantics-visualization.md`
**Visualization Research**: `modeling_pm/research/20260116-161342_sysml-v2-visualization-tools.md`
**Test Model**: `models/tests/coffee_maker/`
**Design**: Implementation is simple enough to proceed directly (no separate design needed)
**Plan**: N/A (single-file change)

---
**Next Steps**: After approval, implement changes directly (no /design-model needed - straightforward edit)
