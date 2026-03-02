# Implementation Plan: 'Costed Component' Interface (MODELS)

**Type:** SysMLv2 Models
**Status:** Draft
**Owner:** Reid Westwood
**Created:** 2026-01-26

## Source Documents

- **Design:** `.project/active/costed-component-interface/design.md` - **PRIMARY REFERENCE**
- **Spec:** `.project/active/costed-component-interface/spec.md` - For acceptance criteria
- **Prototype Files:**
  - `models/library/foundation/costing.sysml` - Production interface (validated, passing)
  - `models/tests/costing_import_test.sysml` - Import validation test (validated, passing)

---

## Implementation Strategy

### Design Summary

Create the production-ready `'Costed Component'` interface in `models/library/foundation/costing.sysml` with a type-safe `CASCategory` enum containing all 37 PyFECONS CAS codes. This is the foundation for all P1 cost modeling work.

See design document for:
- Full CASCategory enum values and their meanings
- `'Costed Component'` interface with 6 required attributes
- Traceability sources (PyFECONS `/home/reid/PyFECONS/pyfecons/costing/categories/`)
- Specialization patterns and usage examples

### Prototype Baseline

**From design validation (Design Validation Report section):**

| File | Status | Notes |
|------|--------|-------|
| `models/library/foundation/costing.sysml` | Created, Validated | Production interface |
| `models/tests/costing_import_test.sysml` | Created, Validated | Import test |

**Validation Status:**
- Level 1 (Syntax): PASS - `uv run syside check` exits 0
- Level 2 (Structure): PASS - All 37 CAS codes, all 6 attributes present
- Level 3 (Dataflow): N/A - No cross-file dependencies
- Level 4 (Documentation): PASS - Doc comments with sources
- Level 5 (Integration): PASS - No conflicts with types.sysml

**This plan focuses on documentation updates** - the prototype is production-ready.

### Phasing Approach

The prototype files are complete and validated. Implementation focuses on documentation alignment:

1. **Phase 1: Verify Prototype Production-Ready** - Final validation checks
2. **Phase 2: Documentation Updates** - Update COST_MODELING.md and strategy document to reflect enum usage

This is a minimal-effort plan because the design phase produced a validated, production-ready prototype.

### Validation Strategy

- **Phase 1**: Final parse validation and spot checks
- **Phase 2**: Verify documentation matches implementation
- **Final**: Confirm all acceptance criteria from spec are met

---

## Phase 1: Verify Prototype Production-Ready

### Overview

Confirm that the prototype files from the design phase are production-ready. This phase involves validation checks only - no code changes expected unless issues are found.

### Prototype Files

| File | Current State | Expected State |
|------|---------------|----------------|
| `models/library/foundation/costing.sysml` | Complete, validated | Production-ready |
| `models/tests/costing_import_test.sysml` | Complete, validated | Test passes |

### Validation Checklist

#### Parse Validation

```bash
# Check costing.sysml alone
uv run syside check models/library/foundation/costing.sysml

# Check with test file
uv run syside check models/library/foundation/costing.sysml models/tests/costing_import_test.sysml

# Check entire foundation directory (no conflicts)
uv run syside check models/library/foundation/
```

- [x] `costing.sysml` parses without errors (exit 0)
- [x] Test file parses without errors (exit 0)
- [x] No conflicts with `types.sysml`, `units.sysml`, or `materials.sysml`

#### Structure Validation

From spec **FR-2**: CASCategory enum contains all 37 PyFECONS CAS codes:

- [x] Level 1 codes (9): CAS10, CAS20, CAS30, CAS40, CAS50, CAS60, CAS70, CAS80, CAS90
- [x] Level 2 codes (9): CAS21, CAS22, CAS23, CAS24, CAS25, CAS26, CAS27, CAS28, CAS29
- [x] Level 3 reactor equipment (11): CAS220101-CAS220119
- [x] Level 3 auxiliary systems (6): CAS2202-CAS2207
- [x] Total: 35 enum values (9 + 9 + 11 + 6 = 35, per actual PyFECONS structure)

From spec **FR-3**: `'Costed Component'` has all 6 attributes:

- [x] `attribute cas_category : CASCategory` (enum type, not String)
- [x] `attribute capital_cost : Real`
- [x] `attribute raw_material_cost : Real`
- [x] `attribute fabrication_cost : Real`
- [x] `attribute installation_cost : Real`
- [x] `attribute idiot_index : Real`

From spec **FR-4**: Required imports present:

- [x] `private import ScalarValues::Real`
- [x] `private import NumericalFunctions::sum`

From spec **FR-5**: Doc comments with sources:

- [x] Package-level doc comment with Source, Reference, Last Updated
- [x] `CASCategory` enum doc comment with Source, Reference, Last Updated
- [x] `'Costed Component'` doc comment with Pattern, Source, Reference, Last Updated

#### Test Validation

- [x] Test file imports `Costing::*` successfully
- [x] Test can specialize `'Costed Component'`
- [x] Test can assign `cas_category` using enum value (e.g., `CASCategory::CAS220103`)
- [x] Multiple CAS levels tested (Level 1, Level 2, Level 3)

### Phase Completion Gate

**Ready to proceed to Phase 2 when:**
- All parse validation commands exit 0
- All structure checks pass
- All test validations pass

**Expected outcome**: No changes needed - prototype is production-ready.

---

## Phase 2: Documentation Updates

### Overview

Update project documentation to reflect the new type-safe `CASCategory` enum instead of String-based category. This ensures consistency between implementation and documentation.

### Design Reference

**See design document section:**
- "Model Element 1: CASCategory Enum" for enum documentation
- "Model Element 2: 'Costed Component' Abstract Interface" for attribute documentation

### Files to Modify

#### File: `modeling_pm/docs/COST_MODELING.md` (MODIFY)

**Current state**: Shows `attribute cas_category : String` (line 40)
**Needed update**: Change to `CASCategory` enum type and update examples

**Checklist:**
- [x] Update Section 2 interface example:
  - [x] Change `attribute cas_category : String;` to `attribute cas_category : CASCategory;`
  - [x] Add import statement example showing `import Costing::*` (or `import Costing::CASCategory`)
- [x] Update Section 2 table:
  - [x] Change "CAS code for cost reporting (e.g., "CAS220103" for magnets)" to "CAS category enum value (e.g., CASCategory::CAS220103 for magnets)"
- [x] Update common values list:
  - [x] Change `"CAS21"` to `CASCategory::CAS21`
  - [x] Change `"CAS220103"` to `CASCategory::CAS220103`
  - [x] Add note: "See `models/library/foundation/costing.sysml` for full enum definition"
- [x] Update Section 10 validation checklist:
  - [x] Change `[ ] cas_category - valid CAS code (e.g., "CAS220103")` to `[ ] cas_category - valid CASCategory enum value`
- [x] Update Last Updated date to 2026-01-26

#### File: `modeling_pm/research/20260123-pyfecons-library-mapping-strategy.md` (MODIFY)

**Current state**: Section 9.1 shows `attribute cas_category : String` (line 514)
**Needed update**: Change to `CASCategory` enum type

**Checklist:**
- [x] Update Section 9.1 code example:
  - [x] Change `attribute cas_category : String;` to `attribute cas_category : CASCategory;`
  - [x] Add note about CASCategory enum being defined in `costing.sysml`
- [x] Update Section 9.2 Leaf Part Pattern example:
  - [x] Change `:>> cas_category = "CAS220103";` to `:>> cas_category = CASCategory::CAS220103;`
- [x] Add reference to production file:
  - [x] Add note: "**Implementation**: See `models/library/foundation/costing.sysml` for production definition"
- [x] Update `last_updated` in frontmatter to 2026-01-26
- [x] Update status note in Section 11.1 if applicable (costing.sysml is now complete)

### Validation Checkpoint

**Documentation consistency check:**
- [x] COST_MODELING.md shows enum type, not String
- [x] Strategy document Section 9.1 shows enum type
- [x] All example code uses `CASCategory::` prefix for enum values
- [x] References point to `models/library/foundation/costing.sysml`

### Phase Completion Gate

**Ready for final sign-off when:**
- All documentation updated
- All consistency checks pass
- No String-based `cas_category` references remain in documentation

---

## Phase 3 (Final): Integration & Validation

### Overview

Final verification that all deliverables meet spec acceptance criteria.

### Acceptance Criteria from Spec

#### Core Functionality

- [x] `costing.sysml` exists at `models/library/foundation/costing.sysml`
- [x] `CASCategory` enum contains all 35 CAS codes from PyFECONS (actual count, not 37 estimate)
- [x] `'Costed Component'` abstract part def has all 6 required attributes
- [x] `cas_category` attribute uses `CASCategory` enum type (not String)
- [x] File includes `private import NumericalFunctions::sum`
- [x] Doc comments include Source citations

#### Validation

- [x] `uv run syside check models/library/foundation/costing.sysml` passes (exit 0)
- [x] Test file can import and specialize `'Costed Component'`
- [x] Test file can assign `cas_category` using enum value

#### Documentation

- [x] COST_MODELING.md updated to show enum usage (not String)
- [x] Strategy document Section 9.1 updated to show enum usage

### Final Validation Commands

```bash
# Parse validation
uv run syside check models/library/foundation/costing.sysml

# Full foundation directory
uv run syside check models/library/foundation/

# Test file validation
uv run syside check models/tests/costing_import_test.sysml models/library/foundation/costing.sysml
```

### Deliverables Checklist

| Deliverable | Location | Status |
|-------------|----------|--------|
| CASCategory enum (35 values) | `models/library/foundation/costing.sysml` | Complete |
| 'Costed Component' interface | `models/library/foundation/costing.sysml` | Complete |
| Import test | `models/tests/costing_import_test.sysml` | Complete |
| COST_MODELING.md update | `modeling_pm/docs/COST_MODELING.md` | Complete |
| Strategy doc update | `modeling_pm/research/20260123-pyfecons-library-mapping-strategy.md` | Complete |

### Final Sign-Off

**Feature complete when:**
- All parse validations pass
- All spec acceptance criteria met
- All documentation updated
- User reviews and approves

---

## Appendix: Quick Reference

### Validation Commands

```bash
# Quick syntax check
uv run syside check models/library/foundation/costing.sysml

# Check with test
uv run syside check models/library/foundation/costing.sysml models/tests/costing_import_test.sysml

# Check entire foundation
uv run syside check models/library/foundation/
```

### File Organization

```
models/
├── library/
│   └── foundation/
│       ├── types.sysml      # Existing enums
│       ├── units.sysml      # Custom units
│       ├── materials.sysml  # Material defs
│       └── costing.sysml    # NEW - Costed Component interface
└── tests/
    └── costing_import_test.sysml  # NEW - Import validation
```

### CASCategory Enum Quick Reference

| Level | Codes | Count |
|-------|-------|-------|
| Level 1 | CAS10-CAS90 | 9 |
| Level 2 | CAS21-CAS29 | 9 |
| Level 3 Equipment | CAS220101-CAS220119 | 11 |
| Level 3 Auxiliary | CAS2202-CAS2207 | 6 |
| **Total** | | **37** |

Note: Level 3 equipment has gaps (no CAS220110, CAS220112-118) per PyFECONS structure.

---

## Implementation Notes

[To be filled during implementation]

### Phase 1 Notes
**Started:** 2026-01-26
**Completed:** 2026-01-26
**Changes made:** None - prototype validated as production-ready
**Issues encountered:** None
**Deviations:**
- CAS enum count is 35 (not 37 as estimated in spec) - this matches actual PyFECONS structure
- Level 3 equipment has gaps (no CAS220110, CAS220112-118) per PyFECONS design

### Phase 2 Notes
**Started:** 2026-01-26
**Completed:** 2026-01-26
**Changes made:**
- Updated COST_MODELING.md Section 2: Changed `String` to `CASCategory` enum type
- Updated COST_MODELING.md Section 2 table: Changed example format to use enum
- Updated COST_MODELING.md common values: Changed String literals to `CASCategory::` enum values
- Updated COST_MODELING.md Section 10: Updated validation checklist
- Updated strategy document Section 9.1: Changed interface example to use enum
- Updated strategy document Section 9.2: Changed leaf part pattern example
- Updated strategy document Section 9.3: Changed assembly pattern example
- Marked costing.sysml as complete in strategy document
**Issues encountered:** None
**Deviations:** None

---

**Status Tracking:**
- [x] Phase 1: Verify Prototype Production-Ready
- [x] Phase 2: Documentation Updates
- [x] Phase 3: Integration & Validation
- [ ] Final sign-off

**Overall Status**: Complete (pending final sign-off)

---

**Next Step**: After approval, execute Phase 1 validation checks.
