---
Status: completed
Scale: standard
Epic: Foundation Package
Owner: Reid Westwood
Created: 2026-01-23
Updated: 2026-01-23
---

# Model Enhancement Specification: Foundation Package

**Type**: Model Enhancement
**Modeling Scope**: New Models
**Epic:** Foundation Package (P0)
**Status:** Complete
**Owner:** Reid Westwood
**Created:** 2026-01-23
**Last Updated:** 2026-01-23

## Overview

Create the foundational library infrastructure with enumerations, unit definitions, and material properties that all downstream library components and design usages depend on. This is the first library package and blocks all other epics.

## Current State

### Existing Models
None - creating new models. The `models/library/` directory exists but contains no `.sysml` files.

### Known Issues
- No foundation layer exists for the FusionTEA library
- Cannot begin Power Balance, Power Core, or any other epic without types and units
- No material property definitions for mass/cost calculations

## Modeling Requirements

### MR-001: Types File with Enumerations
- **Type**: Functional
- **Description**: The model SHALL define a `types.sysml` file in `models/library/foundation/` containing all 14 enumeration definitions from PyFECONS
- **Priority**: Must Have
- **Rationale**: Enums are referenced by all downstream components for reactor type branching and configuration
- **Validation**: Parse check passes; enum count matches PyFECONS `enums.py` (14 enum defs)

### MR-002: Placeholder Enum Variants
- **Type**: Functional
- **Description**: The model SHALL include placeholder enum variants (commented in PyFECONS) with doc comments indicating "placeholder" status
- **Priority**: Should Have
- **Rationale**: Enables future expansion to stellarators, FRCs, and other concepts without library restructuring
- **Validation**: All 12 ConfinementType values present (3 active + 9 placeholder)

### MR-003: Units File with SI Imports and Custom Units
- **Type**: Functional
- **Description**: The model SHALL define a `units.sysml` file importing SI/ISQ standard libraries and defining custom cost units (`M_USD`, `USD_KG`, `USD_M3`, `USD_W`) and dimensionless types (`Ratio`, `Percent`)
- **Priority**: Must Have
- **Rationale**: Cost units not in SI standard; needed for all costing calculations throughout the library
- **Validation**: Parse check passes; custom units usable in downstream calc defs

### MR-004: Materials File with Part Definitions
- **Type**: Functional
- **Description**: The model SHALL define a `materials.sysml` file with part definitions for ~12 materials used in blanket, shield, and structure systems
- **Priority**: Must Have
- **Rationale**: Material properties (density, cost) drive mass and cost calculations in CAS22 costing
- **Validation**: Material defs present for all BlanketFirstWall and BlanketStructure enum values

### MR-005: Material Property Attributes
- **Type**: Functional
- **Description**: Each material part def SHALL include attributes for `density` (kg/m³), `thermal_conductivity` (W/m·K), and `unit_cost` (USD/kg or USD/m³)
- **Priority**: Must Have
- **Rationale**: These properties are used in PyFECONS volume→mass→cost calculation chain
- **Validation**: All material defs have these three attributes with appropriate units

### MR-006: Documentation with Source Citations
- **Type**: Quality / Traceability
- **Description**: All enum definitions SHALL have doc comments citing PyFECONS `enums.py` with line numbers
- **Priority**: Must Have
- **Rationale**: Maintain traceability per MODELING_GUIDE standards
- **Validation**: Level 6 documentation check - all defs have `**Source**` citation

### MR-007: Parse Validation
- **Type**: Quality
- **Description**: All files SHALL parse without errors using `syside check`
- **Priority**: Must Have
- **Rationale**: Foundation must be syntactically correct for all downstream imports
- **Validation**: `uv run syside check models/library/foundation/*.sysml` returns 0 errors

### MR-008: Package Naming Convention
- **Type**: Quality
- **Description**: Package naming SHALL follow `FusionTEA::Library::Foundation` convention
- **Priority**: Must Have
- **Rationale**: Consistent with MODELING_GUIDE package structure for import resolution
- **Validation**: Package declarations match `FusionTEA::Library::Foundation::{types|units|materials}`

### MR-009: Enum Name Matching
- **Type**: Constraint
- **Description**: Enum variant names SHALL match PyFECONS enum value strings exactly (e.g., `SPHERICAL_TOKAMAK`, not `SphericalTokamak`)
- **Priority**: Must Have
- **Rationale**: Enables future code generation and validation against PyFECONS outputs
- **Validation**: String comparison of enum variant names vs PyFECONS enums.py values

### MR-010: Material Property Sources
- **Type**: Constraint / Traceability
- **Description**: Material property values SHALL be sourced from engineering references with citations in doc comments
- **Priority**: Should Have
- **Rationale**: Material data must be defensible for LCOE analysis credibility
- **Validation**: Each material has source citation for property values

## Scope Boundaries

### In Scope
- `models/library/foundation/types.sysml` - 14 enum defs from PyFECONS enums.py:
  - ReactorType, ConfinementType, EnergyConversion, FuelType
  - BlanketFirstWall, BlanketType, BlanketPrimaryCoolant, BlanketSecondaryCoolant
  - BlanketNeutronMultiplier, BlanketStructure, StructurePga
  - MagnetType, MagnetMaterialType
- `models/library/foundation/units.sysml` - SI/ISQ imports + custom units:
  - Cost units: M_USD, USD_KG, USD_M3, USD_W
  - Dimensionless: Ratio, Percent
- `models/library/foundation/materials.sysml` - ~12 material part defs:
  - First wall: Tungsten, Beryllium, Liquid Lithium, FLiBe
  - Structure: Stainless Steel, Ferritic-Martensitic Steel, ODS Steel, Vanadium
  - Coolants: Lead-Lithium (PbLi), Helium, Water
  - Properties: density, thermal_conductivity, unit_cost
- Package structure: `FusionTEA::Library::Foundation`
- Doc comments with PyFECONS source citations

### Out of Scope
- Calculation definitions (Power Balance epic)
- Part definitions for reactor components (Power Core epic)
- Design usages and parameter values (CATF MFE Design epic)
- Full material property databases beyond core properties
- Derived unit types beyond the 6 custom units listed

## Success Criteria

### Functional Success
- [ ] All 3 files created in `models/library/foundation/`
- [ ] 14 enumeration definitions present in types.sysml
- [ ] 6 custom unit/type definitions in units.sysml (M_USD, USD_KG, USD_M3, USD_W, Ratio, Percent)
- [ ] ~12 material part definitions in materials.sysml
- [ ] All materials have density, thermal_conductivity, unit_cost attributes

### Quality Success
- [ ] Parse validation (Level 1): All .sysml files parse without syntax errors
- [ ] Structural validation (Level 2): No unused definitions, complete interfaces
- [ ] Documentation validation (Level 6): All definitions have doc comments with sources

### Validation Success
- [ ] Enum variant names match PyFECONS enums.py exactly (case-sensitive string match)
- [ ] Custom units importable and usable in test calc def
- [ ] Materials importable by downstream Power Core definitions
- [ ] `uv run syside check models/library/foundation/*.sysml` returns 0 errors

### Regression Test Assertions
Test file: `tests/models/test_foundation.py`

| Requirement | Test Assertion |
|-------------|----------------|
| Enums exist | `len([e for e in model.elements(EnumerationDefinition)]) >= 14` |
| ReactorType values | `{"MFE", "IFE", "MIF"} <= {v.name for v in reactor_type.variants}` |
| ConfinementType count | `len(confinement_type.variants) >= 12` |
| Materials exist | `len([p for p in model.elements(PartDefinition) if "Material" in p.name or material_names]) >= 10` |
| No parse errors | `len([d for d in diagnostics if d.severity == Error]) == 0` |
| Custom units defined | `{"M_USD", "USD_KG", "USD_M3"} <= {a.name for a in model.elements(AttributeDefinition)}` |

## Assumptions & Risks

### Assumptions
- **A-001**: SysML v2 enum def syntax supports all PyFECONS enum patterns
  - Confidence: High
  - Impact if Wrong: May need workaround for complex enums (e.g., ConfinementType with reactor_type association)

- **A-002**: ISQ/SI standard libraries provide all base physical units needed
  - Confidence: High
  - Impact if Wrong: Define additional base units in units.sysml

- **A-003**: Material property values can be sourced from public engineering references
  - Confidence: Medium
  - Impact if Wrong: Use placeholder values with TODO comments

### Risks
- **R-001**: SysML enum syntax may not support PyFECONS enum patterns (e.g., enum with associated data)
  - Likelihood: Low
  - Impact: Medium
  - Mitigation: Use doc comments to capture associated data; consider attribute defs if needed

- **R-002**: Material property values vary by grade/temperature; single values may be insufficient
  - Likelihood: Medium
  - Impact: Low (for initial LCOE estimates)
  - Mitigation: Document reference conditions; extend with temperature-dependent properties later

## Traceability

### Source Requirements
- PyFECONS enums: `/home/reid/PyFECONS/pyfecons/enums.py` (lines 1-194)
- PyFECONS units: `/home/reid/PyFECONS/pyfecons/units.py` (lines 1-152)
- Research: `modeling_pm/research/20260123-pyfecons-library-mapping-strategy.md` (Section 7.2)

### Downstream Impacts
- **Power Balance Calculations**: Will import types.sysml for ReactorType branching
- **Power Core Definitions**: Will import materials.sysml for blanket/shield material selection
- **All Costing Calculations**: Will import units.sysml for M_USD and cost-per-unit types
- **All Design Usages**: Will import types.sysml for configuration enums

## Acceptance Criteria Checklist

- [ ] All MR-001 through MR-010 requirements implemented
- [ ] Functional success criteria met (3 files, 14 enums, 12 materials, 6 units)
- [ ] Quality success criteria met (Levels 1, 2, 6 pass)
- [ ] Validation success criteria met (name matching, parse clean, imports work)
- [ ] No regressions - N/A (first library package)
- [ ] Regression tests added (`tests/models/test_foundation.py`)
- [ ] Documentation complete (doc comments in all definitions)
- [ ] Epic progress updated in BACKLOG.md

## Related Artifacts
- **Research**: `modeling_pm/research/20260123-pyfecons-library-mapping-strategy.md`
- **Epic**: `modeling_pm/backlog/BACKLOG.md` (Foundation Package section)
- **PyFECONS Sources**:
  - `/home/reid/PyFECONS/pyfecons/enums.py`
  - `/home/reid/PyFECONS/pyfecons/units.py`
- **Design**: `modeling_pm/active/foundation-package/design.md` (to be created)
- **Plan**: `modeling_pm/active/foundation-package/plan.md` (to be created)

---
**Next Steps**: After approval → `/design-model`
