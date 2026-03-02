# Spec: 'Costed Component' Interface

**Status:** Draft
**Owner:** Reid Westwood
**Created:** 2026-01-26 16:56 UTC
**Complexity:** LOW
**Branch:** visualization

---

## Business Goals

### Why This Matters

All P1 work items (Power Core Definitions, Magnet System, Geometry Calculations, First CATF MFE Design) require a consistent cost modeling interface. Without this foundation, each component would define cost attributes ad-hoc, leading to:
- Inconsistent attribute names across components
- No automatic cost rollup capability
- Inability to generate CAS-compatible cost reports
- Validation failures against PyFECONS outputs

This interface is the **single source of truth** for how costs are modeled in the fusion library.

### Success Criteria

- [ ] All costed fusion parts can specialize `'Costed Component'`
- [ ] Costs can be aggregated automatically via `sum()` over multiplicities
- [ ] CAS category is type-safe (enum prevents typos)
- [ ] Cost reports can be extracted grouped by CAS category
- [ ] Pattern matches validated Coffee Maker demo model

### Priority

**P0.5** - Blocking all P1 epics. Must be completed before Power Core Definitions, Magnet System, or any other costed component work.

---

## Problem Statement

### Current State

The cost modeling pattern has been validated in the Coffee Maker demo model (`models/tests/coffee_maker/`), but the `'Costed Component'` interface is **not yet in the fusion library**. The Coffee Maker version:
- Uses `String` for cost categories (not CAS-aware)
- Is in a test package, not the main library
- Lacks the `cas_category` attribute added in the 2026-01-26 strategy update

### Desired Outcome

A production-ready `'Costed Component'` interface in `library/foundation/costing.sysml` that:
- Includes the `CASCategory` enum with all PyFECONS categories
- Provides type-safe CAS assignment
- Is importable by all fusion component definitions
- Follows the validated nested cost model pattern

---

## Scope

### In Scope

1. **`CASCategory` enum definition** - All ~37 CAS codes from PyFECONS
2. **`'Costed Component'` abstract part def** - The interface with 6 attributes
3. **Required imports** - `NumericalFunctions::sum`, `ScalarValues::Real`
4. **Documentation** - Doc comments with Source citations
5. **Validation test** - Simple test file that imports and specializes the interface

### Out of Scope

- Calc definitions (those go in `library/calculations/costing/`)
- Concrete fusion component definitions (P1 work)
- Cost evaluation scripts (separate tooling)
- LCOE calculation (P2 work)

### Edge Cases & Considerations

1. **Reactor-type-specific CAS codes**: CAS220103 means "Coils" for MFE but "Lasers" for IFE. The enum value is the same; the interpretation depends on reactor type.
2. **Hierarchy not captured**: CAS220103 is "under" CAS22, but the enum is flat. Rollup hierarchy is captured via part structure, not the enum.
3. **Future CAS codes**: If PyFECONS adds new categories, the enum must be updated. This is acceptable since PyFECONS changes are rare.

---

## Requirements

### Functional Requirements

> All requirements below are from the backlog task, strategy document, and COST_MODELING.md.

1. **FR-1**: The file MUST be located at `models/library/foundation/costing.sysml`
2. **FR-2**: The file MUST define `enum def CASCategory` with all PyFECONS CAS codes
3. **FR-3**: The file MUST define `abstract part def 'Costed Component'` with:
   - `cas_category : CASCategory` (enum type, not String)
   - `capital_cost : Real`
   - `raw_material_cost : Real`
   - `fabrication_cost : Real`
   - `installation_cost : Real`
   - `idiot_index : Real`
4. **FR-4**: The file MUST import `NumericalFunctions::sum` for use by specializing parts
5. **FR-5**: The file MUST include doc comments with Source citations per MODELING_GUIDE.md
6. **FR-6**: [INFERRED] The enum SHOULD include descriptive comments for each CAS code

### CAS Category Enum Values

Based on PyFECONS `costing/categories/`:

| Level | Code | Description |
|-------|------|-------------|
| 1 | CAS10 | Pre-Construction Costs |
| 1 | CAS20 | Direct Costs (total) |
| 2 | CAS21 | Buildings and Structures |
| 2 | CAS22 | Reactor Plant Equipment (total) |
| 3 | CAS220101 | Reactor Equipment |
| 3 | CAS220102 | Radiation Shield |
| 3 | CAS220103 | Magnets/Coils (MFE) or Lasers (IFE) |
| 3 | CAS220104 | Supplementary Heating (MFE) or Ignition (IFE) |
| 3 | CAS220105 | Primary Structure |
| 3 | CAS220106 | Vacuum System |
| 3 | CAS220107 | Power Supplies |
| 3 | CAS220108 | Divertor (MFE) or Target Factory (IFE) |
| 3 | CAS220109 | Direct Energy Converter |
| 3 | CAS220111 | Installation |
| 3 | CAS220119 | Scheduled Replacement |
| 3 | CAS2202 | Main/Secondary Coolant |
| 3 | CAS2203 | Auxiliary Cooling |
| 3 | CAS2204 | Radioactive Waste Treatment |
| 3 | CAS2205 | Fuel Handling |
| 3 | CAS2206 | Other Reactor Equipment |
| 3 | CAS2207 | Instrumentation & Control |
| 2 | CAS23 | Turbine Plant Equipment |
| 2 | CAS24 | Electric Plant Equipment |
| 2 | CAS25 | Miscellaneous Plant Equipment |
| 2 | CAS26 | Heat Rejection System |
| 2 | CAS27 | Special Materials |
| 2 | CAS28 | Digital Twin |
| 2 | CAS29 | Contingency (Direct) |
| 1 | CAS30 | Capitalized Indirect Service Costs |
| 1 | CAS40 | Capitalized Owner Costs |
| 1 | CAS50 | Capitalized Supplementary Costs |
| 1 | CAS60 | Capitalized Financial Costs |
| 1 | CAS70 | Annualized O&M Costs |
| 1 | CAS80 | Annualized Fuel Costs |
| 1 | CAS90 | Annualized Financial Costs |

### Non-Functional Requirements

- **NFR-1**: File MUST parse without errors via `uv run syside check`
- **NFR-2**: File SHOULD parse without warnings (shadowing warnings acceptable in test files only)

---

## Acceptance Criteria

### Core Functionality

- [ ] `costing.sysml` exists at `models/library/foundation/costing.sysml`
- [ ] `CASCategory` enum contains all 37 CAS codes from PyFECONS
- [ ] `'Costed Component'` abstract part def has all 6 required attributes
- [ ] `cas_category` attribute uses `CASCategory` enum type (not String)
- [ ] File includes `private import NumericalFunctions::sum`
- [ ] Doc comments include Source citations

### Validation

- [ ] `uv run syside check models/library/foundation/costing.sysml` passes (exit 0)
- [ ] Test file can import and specialize `'Costed Component'`
- [ ] Test file can assign `cas_category` using enum value

### Documentation

- [ ] COST_MODELING.md updated to show enum usage (not String)
- [ ] Strategy document Section 9.1 updated to show enum usage

---

## Risks & Mitigations

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Enum values don't match PyFECONS exactly | Low | Medium | Cross-reference against PyFECONS `costing/categories/` files |
| SysML enum syntax issues | Low | Low | Validated in types.sysml already; same pattern |
| Future PyFECONS CAS additions | Low | Low | Enum can be extended; PyFECONS rarely changes |
| Import conflicts with types.sysml | Low | Low | Use explicit package paths if needed |

---

## Validation Plan

### Level 1: Parse Validation
```bash
uv run syside check models/library/foundation/costing.sysml
```
Expected: Exit code 0, no errors

### Level 2: Import Validation
Create `models/tests/costing_import_test.sysml`:
```sysml
package CostingImportTest {
    import FusionTEA::Library::Foundation::Costing::*;

    part def 'Test Costed Part' :> 'Costed Component' {
        :>> cas_category = CASCategory::CAS220103;
        :>> capital_cost = 100.0;
        :>> raw_material_cost = 50.0;
        :>> fabrication_cost = 30.0;
        :>> installation_cost = 20.0;
        :>> idiot_index = 2.0;
    }
}
```
Expected: Parses without errors

### Level 3: Integration Validation
- Verify foundation package exports include costing
- Verify no naming conflicts with existing types.sysml enums

---

## Related Artifacts

- **Validated Pattern**: `models/tests/coffee_maker/library.sysml`
- **Cost Modeling Guide**: `modeling_pm/docs/COST_MODELING.md`
- **Strategy Document**: `modeling_pm/research/20260123-pyfecons-library-mapping-strategy.md`
- **Backlog Task**: `modeling_pm/backlog/BACKLOG.md` (P0.5 section)
- **PyFECONS Reference**: `/home/reid/PyFECONS/pyfecons/costing/categories/`

---

## Design Decisions Captured

| Decision | Choice | Rationale |
|----------|--------|-----------|
| CAS type | Enum (not String) | Type safety, IDE completion, prevents typos |
| Enum location | `costing.sysml` (co-located) | Single file for all costing infrastructure |
| Enum naming | `CASCategory` | Matches PyFECONS naming convention |
| Attribute type for cas_category | `CASCategory` | Direct enum reference, not String |

---

**Next Steps:** After approval, proceed to `/_my_design`
