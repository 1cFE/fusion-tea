---
Status: complete
Created: 2026-03-02
Updated: '2026-03-02'
Related Artifacts:
  Spec: ./spec.md
  Design: ./design.md
---

# WI-006: IFE Cost Structure Library — Implementation Plan

## Source Documents

- **Design**: `./design.md` — primary. Architecture, element catalog, validation report.
- **Spec**: `./spec.md` — acceptance criteria, SV-XXX verification entries.
- **Epic**: `work/backlog/epic-ife-cost-modeling.md`

## Design Summary

6 SysML v2 files across `models/library/{foundation,cost_structure,analyses}/` providing: `attribute def 'Economic Parameter'`, `enum def 'CAS Scope'`, `abstract part def 'Costed Component'`, 9 CAS level 2 part defs, 14 Hawker parameters as `'IFE Cost Parameters'`, `calc def 'IFE LCOE'` (closed-form DCF), `calc def 'Recirculating Power Fraction'`, and `constraint def 'Viability Threshold'`. See design doc for rationale, source analysis, and design decisions DD-1 through DD-6.

## Prototype Baseline

All 6 prototype files exist and pass syside Levels 1-3. No Level 4-6 issues were identified during prototyping.

| File | Status | Refinement Needed |
|------|--------|-------------------|
| `foundation/economic_parameter.sysml` | PASS L1-3 | Audit doc comments for completeness |
| `foundation/costed_component.sysml` | PASS L1-3 | Audit doc comments for completeness |
| `cost_structure/cas_hierarchy.sysml` | PASS L1-3 | Audit doc comments; verify all 9 CAS accounts have Source/Ref/Basis |
| `cost_structure/ife_cost_parameters.sysml` | PASS L1-3 | Audit all 14 parameter doc comments for MR-4 compliance |
| `analyses/ife_lcoe.sysml` | PASS L1-3 | Audit intermediate citations; verify formula comments |
| `analyses/fusion_cycle.sysml` | PASS L1-3 | Audit doc comments for completeness |

## Phasing Approach

Two phases. The prototype is already functional — refinement is documentation completeness, project integration, and formal verification. Phase 1 handles the model files; Phase 2 handles project-level artifacts and SV verification.

## Validation Strategy

- **Per-phase**: `uv run python -m syside check` on all modified files (Levels 1-3)
- **Final**: All 6 files together, SV-001 through SV-005 verified, spec acceptance criteria checked

---

## Phase 1: Documentation Audit & Refinement

### Overview

Audit all 6 prototype files for MR-4 citation completeness and MR-WI006-7 concept-agnosticism. Fix any gaps. This phase refines existing files — no new files created.

### Design Reference

See design doc sections:
- "Per-Element Design" — for each element's intended structure and citations
- "DD-1: Plain Real for all values" — units documented in doc comments, not types
- "DD-6: Separate parameter definitions from LCOE calculation" — parameter metadata lives in `ife_cost_parameters.sysml`, calc is pure math

### Files to Modify

All files are REFINE (no new files):

- `models/library/foundation/economic_parameter.sysml` — REFINE
- `models/library/foundation/costed_component.sysml` — REFINE
- `models/library/cost_structure/cas_hierarchy.sysml` — REFINE
- `models/library/cost_structure/ife_cost_parameters.sysml` — REFINE
- `models/library/analyses/ife_lcoe.sysml` — REFINE
- `models/library/analyses/fusion_cycle.sysml` — REFINE

### Checklist

#### MR-4 Citation Audit

- [x] `economic_parameter.sysml`: Verify `'Economic Parameter'` doc comment has Source/Ref/Basis — FIXED: Source changed from abstract to file path, added Ref and Basis
- [x] `economic_parameter.sysml`: Verify `'CAS Scope'` doc comment cites ARIES Cost Account Doc — FIXED: added Basis line
- [x] `costed_component.sysml`: Verify `'Costed Component'` doc comment references MR-2 — FIXED: Source changed to file path, added proper Ref/Basis
- [x] `cas_hierarchy.sysml`: Verify `'CAS Account'` base doc comment cites ARIES doc with line numbers — OK, already compliant
- [x] `cas_hierarchy.sysml`: Verify each of 9 level 2 accounts (`'CAS20 Land'` through `'CAS90 Indirect Costs'`) has Source/Ref/Basis — FIXED: added Basis lines to all 9
- [x] `ife_cost_parameters.sysml`: Verify top-level `'IFE Cost Parameters'` doc comment cites Hawker Table 1 — OK, already compliant
- [x] `ife_cost_parameters.sysml`: Verify each of 14 parameter attributes has doc comment with units, source, and Hawker Table 1 reference — OK, all 14 have units + source + Hawker ref
- [x] `ife_lcoe.sysml`: Verify `'IFE LCOE'` doc comment cites Hawker Eqs 2.1-2.16 — OK, already compliant
- [x] `ife_lcoe.sysml`: Verify intermediate attributes have inline comments explaining derivation — OK, all intermediates have equation refs
- [x] `ife_lcoe.sysml`: Verify the recirculating power factor of 2 is cited (Hawker approximation) — OK, doc comment lines 21-22
- [x] `ife_lcoe.sysml`: Verify `31557600.0` constant has comment (seconds per Julian year) — FIXED: added inline comment
- [x] `fusion_cycle.sysml`: Verify `'Recirculating Power Fraction'` cites EIF-1992 and Accel-2013 — OK, already compliant
- [x] `fusion_cycle.sysml`: Verify `'Viability Threshold'` cites DI-001 and threshold source — OK, already compliant

#### MR-WI006-7 Concept-Agnosticism Check

- [x] `ife_cost_parameters.sysml`: No driver-specific values in defaults (all 14 defaults are Hawker's technology-agnostic MC center values) — VERIFIED
- [x] `cas_hierarchy.sysml`: No concept-specific cost values — VERIFIED
- [x] `ife_lcoe.sysml`: No hardcoded concept-specific constants — VERIFIED (factor of 2 is Hawker's general approximation)
- [x] `fusion_cycle.sysml`: Threshold is parameterized (not hardcoded to a specific driver type) — VERIFIED (in attribute with default 10.0)

#### Naming Consistency Check

- [x] All definitions use `'Title Case'` with quotes — VERIFIED
- [x] All attributes use `snake_case` — VERIFIED
- [x] All packages use `lowercase_underscores` — VERIFIED
- [x] All imports use `private import` (not bare `import`) — VERIFIED

### Validation Checkpoint

```bash
uv run python -m syside check models/library/foundation/economic_parameter.sysml \
    models/library/foundation/costed_component.sysml \
    models/library/cost_structure/cas_hierarchy.sysml \
    models/library/cost_structure/ife_cost_parameters.sysml \
    models/library/analyses/ife_lcoe.sysml \
    models/library/analyses/fusion_cycle.sysml
```

- [x] All 6 files pass syside check (no regressions from edits) — PASSED

### Phase Completion Gate

- All MR-4 citation audit items checked
- All MR-WI006-7 concept-agnosticism items checked
- All naming items checked
- syside check passes

---

## Phase 2: Project Integration & Verification

### Overview

Update project-level artifacts: register architectural decisions from design DD-1 through DD-6, update `models/README.md` with the library catalog, verify SV-001 through SV-005, and update their statuses in VALIDATION_MATRIX.md. Close the work item.

### Design Reference

See design doc sections:
- "Design Decisions" — DD-1 through DD-6, to be registered as AD-XXX
- "Element Catalog" — table of all elements for README
- "Validation Report" — prototype status to carry forward

### Files to Modify

- `models/README.md` — REFINE (add library catalog)
- `modeling_project/ARCHITECTURE.md` — REFINE (register AD-XXX decisions)
- `modeling_project/VALIDATION_MATRIX.md` — REFINE (update SV statuses)

### Checklist

#### models/README.md Update

- [x] Add library catalog section listing all 6 files with:
  - File path
  - Package name
  - Key elements defined
  - Purpose (1 sentence)
- [x] Organize by subdirectory (foundation, cost_structure, analyses)

#### Architectural Decisions

Register design decisions as AD-XXX in `modeling_project/ARCHITECTURE.md`:

- [x] AD-001: Plain `Real` for all values (DD-1) — registered
- [x] AD-002: `attribute def` bundles parameter metadata (DD-2) — registered
- [x] AD-003: Closed-form DCF for LCOE (DD-3) — registered
- [x] AD-004: Library subdirectory organization (DD-4) — registered
- [x] AD-005: CAS hierarchy as typed part def specializations (DD-5) — registered
- [x] AD-006: Parameters separate from calculation (DD-6) — registered

#### SV-XXX Verification

Verify each SV entry against the implemented prototype:

- [x] **SV-001**: 14 attributes counted, each typed `'Economic Parameter'` with value/min_value/max_value/sensitivity — PASSING
- [x] **SV-002**: 9 CAS part defs (CAS20-27, CAS90), each with scope classification — PASSING
- [x] **SV-003**: `return lcoe : Real`, dimensional chain traced via doc comments to $/MWh — PASSING
- [x] **SV-004**: `eta * gain >= threshold` constraint expression present — PASSING
- [x] **SV-005**: All 6 files pass `uv run python -m syside check` with 0 errors — PASSING
- [x] Update all 5 SV entries in `modeling_project/VALIDATION_MATRIX.md` from `pending` to `passing`

#### Spec Acceptance Criteria Verification

Cross-check against spec.md Success Criteria:

- [x] Functional: All 14 Hawker parameters exist as typed attributes with units, ranges, defaults, and sensitivity rankings
- [x] Functional: CAS level 2 hierarchy covers accounts 20-27 and 91-99 with shared/divergent classification
- [x] Functional: LCOE calculation definition takes the 14 parameters and produces $/MWh output
- [x] Functional: Fusion cycle gain constraint (eta*G > 10) is defined and evaluable
- [x] Functional: Costed component interface exists with `capital_cost` attribute
- [x] Quality: Every quantitative value carries a Source/Ref/Basis citation in doc comments
- [x] Quality: No driver-specific values anywhere in library definitions
- [x] Quality: All files parse cleanly with `uv run syside check`

### Validation Checkpoint

```bash
# Final full validation
uv run python -m syside check models/library/foundation/economic_parameter.sysml \
    models/library/foundation/costed_component.sysml \
    models/library/cost_structure/cas_hierarchy.sysml \
    models/library/cost_structure/ife_cost_parameters.sysml \
    models/library/analyses/ife_lcoe.sysml \
    models/library/analyses/fusion_cycle.sysml
```

- [x] All 6 files pass syside check

### Phase Completion Gate

- [x] README.md updated with library catalog
- [x] All 6 AD-XXX decisions registered in ARCHITECTURE.md
- [x] All 5 SV-XXX entries verified and updated to `passing`
- [x] All 8 spec acceptance criteria verified
- [x] Final syside check passes

---

## Post-Implementation

After Phase 2 completion:
- [x] Update WI-006 status to `completed` via `uv run agentic-mbse pm close-item WI-006` — DONE, archived to work/completed/
- [x] Verify WI-007 is unblocked in backlog — WI-006 was WI-007's only blocker

## Feasibility Concerns

| Concern | Likelihood | Mitigation |
|---------|-----------|------------|
| Doc comment edits introduce parse errors | Low | syside check after every edit batch |
| AD-XXX registration format unclear (no existing entries) | Medium | Follow ARCHITECTURE.md's "AD-XXX" convention header; create first entries as the pattern |
| SV-001 count may not match if parameter names changed | Very Low | Cross-reference against Hawker Table 1 in spec |

---

**Estimated effort**: Small — 2 phases of refinement on validated prototypes. No new SysML definitions to create.
