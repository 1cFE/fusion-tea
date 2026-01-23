# Implementation Plan: Phase 1 - Foundation Library (MODELS)

**Type:** SysMLv2 Models
**Status:** Draft
**Owner:** Reid Westwood
**Created:** 2026-01-05

## Source Documents
- **Design:** `modeling_pm/active/phase1-foundation/design.md` - **PRIMARY REFERENCE**
- **Spec:** `modeling_pm/active/phase1-foundation/spec.md` - For acceptance criteria
- **Epic:** `modeling_pm/backlog/BACKLOG.md` (Phase 1 - Foundation Library)

## Implementation Strategy

### Design Summary

Create foundational SysML v2 library infrastructure for FusionTEA: package structure, standard imports, enumerations (FuelType, ReactorType, ConfinementType, MagnetType, MagnetMaterialType), and the core PowerBalanceCalc definition with full fidelity to PyFECONS (18 inputs including alpha_fraction default, 16 outputs).

See design document for:
- Engineering rationale and component descriptions
- Traceability sources and PyFECONS codebase references
- Alpha fraction calculation limitation and workaround (conditional expressions not supported)
- Design decisions (minimal enums, comments-only units, DT default alpha fraction)
- Prototype files created and validation report

**This plan focuses on refinement**: organizing improvements to the validated prototype into phases with validation checkpoints.

### Prototype Baseline

**From design validation (Stage 6)**:
- Prototype files:
  - `models/library/foundation.sysml` - Package structure, 5 enums
  - `models/library/calculations/power_balance.sysml` - PowerBalanceCalc calc def
- Validation status: Levels 1-3 passing (`syside check models/library/` exits 0)
- Known refinement needs (from design document):
  - Level 4: All 3 assert constraints present
  - Level 5: Naming conventions followed
  - Level 6: Documentation present but could add traceability matrix entries
  - Level 7: Package structure aligned with MODELING_GUIDE

**Current prototype state:**
- `foundation.sysml`: 137 lines, 5 complete enum definitions, package structure in place
- `power_balance.sysml`: 216 lines, PowerBalanceCalc with 18 inputs, 16 outputs, 3 constraints

**This plan refines the prototype to achieve production quality and complete all spec acceptance criteria.**

### Phasing Approach

The prototype is already validated and complete for core functionality. Refinement is organized into 3 phases:

1. **Phase 1: Traceability & Documentation** - Complete traceability matrix entries, verify all source citations
2. **Phase 2: Integration Verification** - Verify imports resolve correctly, test cross-file binding patterns
3. **Phase 3: Final Validation & Sign-Off** - Comprehensive validation, acceptance criteria checklist

### Validation Strategy
- **After each phase**: Run `syside check` on modified files to catch errors early
- **After Phase 2**: Optional user review of import patterns
- **Final validation**: Comprehensive 8-level quality checks, traceability verification

---

## Phase 1: Traceability & Documentation

### Overview

Complete traceability matrix entries for all model elements and verify all source citations are accurate. The prototype has doc comments but traceability matrix hasn't been created.

### Prototype Baseline
**Existing files from design phase:**
- `models/library/foundation.sysml` - Complete, 5 enums with doc comments
- `models/library/calculations/power_balance.sysml` - Complete, PowerBalanceCalc with doc comment

### Design Reference
**See design document sections:**
- Model Element 1: Foundation Package (lines 182-335)
- Model Element 2: PowerBalanceCalc (lines 338-515)
- Parameter Sources (Traceability) table (lines 477-496)

**Key design decisions from design doc:**
- All enums cite PyFECONS enums.py with specific line numbers
- PowerBalanceCalc cites PowerBalance.py lines 8-105

### Files to Create/Refine

#### File: `data/traceability_matrix.csv` (NEW)

**Checklist:**
- [ ] Create `data/` directory if it doesn't exist
- [ ] Create CSV file with headers: element_name, element_type, source_type, source_name, file_path, section_line, coverage, confidence, last_updated
- [ ] Add row for `FuelType` enum
  - source_name: PyFECONS
  - file_path: pyfecons/enums.py
  - section_line: 43-53
  - confidence: High
- [ ] Add row for `ReactorType` enum
  - source_name: PyFECONS
  - file_path: pyfecons/enums.py
  - section_line: 4-7
  - confidence: High
- [ ] Add row for `ConfinementType` enum
  - source_name: PyFECONS
  - file_path: pyfecons/enums.py
  - section_line: 10-34
  - confidence: High
- [ ] Add row for `MagnetType` enum
  - source_name: PyFECONS
  - file_path: pyfecons/enums.py
  - section_line: 172-181
  - confidence: High
- [ ] Add row for `MagnetMaterialType` enum
  - source_name: PyFECONS
  - file_path: pyfecons/enums.py
  - section_line: 184-193
  - confidence: High
- [ ] Add row for `PowerBalanceCalc` calc def
  - source_name: PyFECONS
  - file_path: pyfecons/costing/mfe/PowerBalance.py
  - section_line: 8-105
  - confidence: High

#### File: `models/library/foundation.sysml` (VERIFY)

**Checklist:**
- [ ] Verify FusionTEA package doc comment includes all required fields
  - [ ] Source, Reference, Last Updated present
- [ ] Verify all 5 enum def doc comments include:
  - [ ] Source: PyFECONS
  - [ ] File: path
  - [ ] Lines: specific line numbers
  - [ ] Last Updated: date
- [ ] Verify enum values match PyFECONS enums.py exactly:
  - [ ] FuelType: DT, DD, DHE3, PB11 (lines 43-53)
  - [ ] ReactorType: IFE, MFE, MIF (lines 4-7)
  - [ ] ConfinementType: SPHERICAL_TOKAMAK, MAGNETIC_MIRROR, LASER_DRIVEN_DIRECT_DRIVE (lines 10-34)
  - [ ] MagnetType: TF, CS, PF (lines 172-181)
  - [ ] MagnetMaterialType: HTS_CICC, HTS_PANCAKE, COPPER (lines 184-193)

#### File: `models/library/calculations/power_balance.sysml` (VERIFY)

**Checklist:**
- [ ] Verify PowerBalanceCalc doc comment includes all required fields:
  - [ ] Source: PyFECONS
  - [ ] File: pyfecons/costing/mfe/PowerBalance.py
  - [ ] Lines: 8-105
  - [ ] Assumptions listed
  - [ ] Validation approach stated
  - [ ] Last Updated: date
- [ ] Verify all 18 input parameters documented with purpose comments
- [ ] Verify all 16 output parameters documented with:
  - [ ] Line reference to PyFECONS source
  - [ ] Units in comment (MW for power, dimensionless for fractions/Q values)
- [ ] Verify formulas match PyFECONS PowerBalance.py:
  - [ ] p_alpha = p_nrl * alpha_fraction (line 10)
  - [ ] p_neutron = p_nrl - p_alpha (line 11)
  - [ ] p_cool = p_tfcool + p_pfcool (line 12)
  - [ ] p_aux = p_trit + p_house (line 13)
  - [ ] p_coils = p_tf + p_pf (line 14)
  - [ ] p_th formula (lines 15-21)
  - [ ] p_the = eta_th * p_th (line 22)
  - [ ] p_dee = eta_de * p_alpha (line 23)
  - [ ] p_et = p_dee + p_the (line 24)
  - [ ] p_loss = p_th - p_the - p_dee (line 25)
  - [ ] p_pump = fpcppf * p_the (line 26)
  - [ ] p_sub = f_sub * p_the (line 27)
  - [ ] q_sci = p_nrl / p_input (line 28)
  - [ ] q_eng formula (lines 29-48)
  - [ ] rec_frac = 1.0 / q_eng (line 49)
  - [ ] p_net = (1.0 - 1.0 / q_eng) * p_et (line 50)

### Validation Checkpoint

**Documentation validation:**
- [ ] All model elements have doc comments
- [ ] All doc comments cite sources with file paths and line numbers
- [ ] Traceability matrix CSV created with all 7 entries

**Parsing validation:**
```bash
# Verify no syntax changes broke parsing
syside check models/library/foundation.sysml
syside check models/library/calculations/power_balance.sysml
```
- [ ] Both commands exit with status 0

### Phase Completion Gate
**Ready to proceed to Phase 2 when:**
- All verification checklists completed
- Traceability matrix created
- syside check passes on all files

---

## Phase 2: Integration Verification

### Overview

Verify that cross-file imports work correctly and test the import pattern from power_balance.sysml to foundation.sysml. Prepare for future design file integration.

### Prototype Baseline
**Current import in power_balance.sysml:**
```sysml
private import FusionTEA::FuelType;
```

### Design Reference
**See design document sections:**
- Cross-File Bindings (lines 574-595)
- Common Pitfalls: Package Imports (lines 616-618)

**Key design decisions from design doc:**
- Dataflow direction: foundation.sysml → power_balance.sysml → (future) designs/

### Files to Verify

#### File: `models/library/calculations/power_balance.sysml` (VERIFY IMPORTS)

**Checklist:**
- [ ] Verify import statement syntax:
  - [ ] `private import FusionTEA::FuelType;` is present
  - [ ] Import uses qualified name from foundation.sysml
- [ ] Verify FuelType reference works:
  - [ ] `in attribute fuel_type : FuelType;` resolves correctly
- [ ] Verify ScalarValues import:
  - [ ] `private import ScalarValues::*;` is present
  - [ ] `Real` type resolves correctly

#### File: `models/library/foundation.sysml` (VERIFY EXPORTS)

**Checklist:**
- [ ] Verify FuelType is accessible:
  - [ ] No `private` modifier on FuelType enum def
  - [ ] Qualified name would be `FusionTEA::FuelType`
- [ ] Verify all enums are publicly accessible (no private modifiers)

### Integration Test

**Create temporary test file to verify import resolution:**

```bash
# Create minimal test file
cat > /tmp/test_import.sysml << 'EOF'
package TestImport {
    private import FusionTEA::FuelType;
    private import FusionTEA_Calculations::PowerBalanceCalc;

    part test_system {
        // Test that we can reference both packages
        attribute test_fuel : FuelType;
    }
}
EOF

# Test parsing (should resolve imports)
syside check /tmp/test_import.sysml models/library/

# Clean up
rm /tmp/test_import.sysml
```

**Checklist:**
- [ ] Create temporary test file
- [ ] Run syside check with both library files
- [ ] Verify import resolution succeeds
- [ ] Clean up temporary file

### Validation Checkpoint

**Import validation:**
```bash
# Check all library files together
syside check models/library/
```
- [ ] Command exits with status 0
- [ ] No import resolution warnings

**Cross-file access:**
- [ ] FuelType accessible from power_balance.sysml
- [ ] No circular dependencies (dataflow is unidirectional)

### Phase Completion Gate
**Ready to proceed to Phase 3 when:**
- Import verification complete
- Integration test passes
- syside check passes on entire library

---

## Phase 3: Final Validation & Sign-Off

### Overview

Comprehensive validation against all spec requirements, acceptance criteria checklist completion, and final documentation updates.

### Prototype Baseline
**Files from earlier phases:**
- `models/library/foundation.sysml` - Verified and documented
- `models/library/calculations/power_balance.sysml` - Verified and documented
- `data/traceability_matrix.csv` - Created with 7 entries

### Design Reference
**See design document sections:**
- Validation Plan (lines 651-677)
- Implementation Checklist (lines 680-711)

### Comprehensive Validation

#### Parsing Validation

```bash
# Check all library files
syside check models/library/**/*.sysml
```
- [ ] All files parse without errors

#### Documentation Validation

- [ ] FusionTEA package has doc comment
- [ ] All 5 enums have doc comments with PyFECONS citations
- [ ] PowerBalanceCalc has comprehensive doc comment
- [ ] All 18 inputs documented
- [ ] All 16 outputs documented with formulas and line references

#### Traceability Validation

- [ ] FuelType enum values match PyFECONS enums.py:43-53
- [ ] ReactorType values match enums.py:4-7
- [ ] ConfinementType values match enums.py:10-34
- [ ] MagnetType values match enums.py:172-181
- [ ] MagnetMaterialType values match enums.py:184-193
- [ ] PowerBalanceCalc formulas match PowerBalance.py:8-50
- [ ] Alpha fraction default (0.2002275313) matches DT calculation from PowerBalance.py:94-105

#### Constraint Validation

- [ ] PositiveFusionPower constraint defined: `p_nrl > 0`
- [ ] PositiveNetPower constraint defined: `p_net > 0`
- [ ] ReasonableQ constraint defined: `q_eng > 1.0`

#### Naming Convention Validation

- [ ] Definitions use Title Case or quoted names (`part def 'Name'`, `enum def EnumName`)
- [ ] Attributes use snake_case (`attribute p_nrl`, `attribute fuel_type`)
- [ ] Package names use correct casing (`FusionTEA`, `FusionTEA_Calculations`)

### Acceptance Criteria Checklist

**From spec document (modeling_pm/active/phase1-foundation/spec.md):**

- [ ] MR-001: Package `FusionTEA` with nested `Library` and `Designs` packages defined
- [ ] MR-002: Standard imports (ScalarValues, ISQ, SI) present in foundation
- [ ] MR-003: `FuelType` enum with values DT, DD, DHE3, PB11 defined
- [ ] MR-004: Supporting enums (`ReactorType`, `ConfinementType`, `MagnetType`) defined
- [ ] MR-005: `PowerBalanceCalc` calc def in `models/library/calculations/power_balance.sysml`
- [ ] MR-006: All 17+ input parameters implemented (18 including alpha_fraction)
- [ ] MR-007: All 16 output parameters implemented with formulas
- [ ] MR-008: Fuel-dependent alpha power via input parameter with DT default
- [ ] MR-009: All definitions have doc comments with source citations
- [ ] MR-010: All files parse without syntax errors (`syside check` exits 0)
- [ ] MR-011: PowerBalanceCalc cites PyFECONS file and line numbers

### Deliverables Checklist

**From spec acceptance criteria:**
- [ ] `models/library/foundation.sysml` complete with 5 enums
- [ ] `models/library/calculations/power_balance.sysml` complete with PowerBalanceCalc
- [ ] Parse validation passes on all library files
- [ ] Documentation complete (doc comments in all definitions)
- [ ] Traceability documented (source citations, traceability matrix)

### Epic Status Update

**File: `modeling_pm/backlog/BACKLOG.md`**
- [ ] Update Phase 1 - Foundation Library status to "Complete"
- [ ] Note completion date

### Final Sign-Off

**Feature complete when:**
- All validation checks pass
- All MR-001 through MR-011 requirements met
- All deliverables present
- User reviews and approves final models

---

## Appendix: Quick Reference

### Validation Commands
```bash
# Parse check single file
syside check <file>

# Parse check directory (recursive)
syside check models/library/**/*.sysml

# Parse check entire library
syside check models/library/
```

### File Organization
```
models/
├── library/                  # Reusable definitions
│   ├── foundation.sysml      # Package structure, enums (137 lines)
│   └── calculations/
│       └── power_balance.sysml  # PowerBalanceCalc (216 lines)
└── designs/                  # (Future) Design instances
    └── catf/                 # (Future) CATF MFE design

data/
└── traceability_matrix.csv   # Source traceability (7 entries)
```

### Naming Conventions
- Definitions: `enum def FuelType`, `calc def PowerBalanceCalc`
- Usages: `part snake_case_name : 'Definition Name'`
- Attributes: `attribute snake_case_name : Type`
- Packages: `FusionTEA`, `FusionTEA_Calculations`

### Required Imports
```sysmlv2
// In foundation.sysml
public import ScalarValues::*;
public import ISQ::*;
public import SI::*;

// In power_balance.sysml
private import ScalarValues::*;
private import FusionTEA::FuelType;
```

### PyFECONS Source References
- Enums: `/home/reid/PyFECONS/pyfecons/enums.py`
  - FuelType: lines 43-53
  - ReactorType: lines 4-7
  - ConfinementType: lines 10-34
  - MagnetType: lines 172-181
  - MagnetMaterialType: lines 184-193
- PowerBalance: `/home/reid/PyFECONS/pyfecons/costing/mfe/PowerBalance.py`
  - power_balance function: lines 8-50
  - compute_p_alpha function: lines 94-105

---

## Implementation Notes

[To be filled during implementation]

### Phase 1 Notes
**Started:** [Timestamp]
**Completed:** [Timestamp]
**Changes made:** [Summary]
**Issues encountered:** [Problems and solutions]
**Deviations:** [Any changes from plan and why]

### Phase 2 Notes
**Started:** [Timestamp]
**Completed:** [Timestamp]
**Changes made:** [Summary]
**Issues encountered:** [Problems and solutions]
**Deviations:** [Any changes from plan and why]

### Phase 3 Notes
**Started:** [Timestamp]
**Completed:** [Timestamp]
**Changes made:** [Summary]
**Issues encountered:** [Problems and solutions]
**Deviations:** [Any changes from plan and why]

---

**Status Tracking:**
- [ ] Phase 1: Traceability & Documentation
- [ ] Phase 2: Integration Verification
- [ ] Phase 3: Final Validation & Sign-Off
- [ ] Final sign-off

**Overall Status**: Draft → In Progress → Complete
