---
epics:
  - name: "Cost Modeling Patterns De-Risking"
    priority: P0
    status: active
    file: backlog/epic-cost-patterns-derisking.md
    items:
      - id: WI-001
        name: "Coffee Maker Pattern Fixes"
        scale: standard
        status: active
      - id: WI-002
        name: "Cost Patterns Demo"
        scale: standard
        status: active

  - name: "sysml-codegen Upgrade"
    priority: P1
    status: draft
    file: backlog/epic-sysml-codegen-upgrade.md
    items: []

standalone:
  - id: WI-003
    name: "Explicit Types Redefines"
    scale: standard
    priority: P1
    status: failed
  - id: WI-004
    name: "Foundation Package"
    scale: standard
    priority: P0
    status: completed
    completed: 2026-01-26
  - id: WI-005
    name: "Power Balance Calculations"
    scale: standard
    priority: P0
    status: completed
    completed: 2026-01-26
  - id: WI-006
    name: "Create 'Costed Component' Interface"
    scale: standard
    priority: P0
    status: backlog
  - id: WI-007
    name: "Power Core Definitions"
    scale: standard
    priority: P1
    status: backlog
  - id: WI-008
    name: "Geometry Calculations"
    scale: standard
    priority: P1
    status: backlog
  - id: WI-009
    name: "Magnet System (MFE)"
    scale: standard
    priority: P1
    status: backlog
  - id: WI-010
    name: "First CATF MFE Design"
    scale: standard
    priority: P1
    status: backlog
  - id: WI-011
    name: "CAS22 Subsystem Costing"
    scale: standard
    priority: P2
    status: backlog
  - id: WI-012
    name: "Heating System Definitions"
    scale: standard
    priority: P2
    status: backlog
  - id: WI-013
    name: "Balance of Plant"
    scale: standard
    priority: P2
    status: backlog
  - id: WI-014
    name: "Cost Rollup and LCOE"
    scale: standard
    priority: P2
    status: backlog
  - id: WI-015
    name: "IFE Variant Support"
    scale: standard
    priority: P2
    status: backlog
  - id: WI-016
    name: "Full CAS Coverage"
    scale: standard
    priority: P3
    status: backlog
  - id: WI-017
    name: "Additional Fusion Concepts"
    scale: standard
    priority: P3
    status: backlog
  - id: WI-018
    name: "Model p_dee and eta_de Power Paths"
    scale: standard
    priority: P3
    status: backlog
---

# Work Backlog

Prioritized list of work items for FusionTEA SysML v2 modeling, based on PyFECONS library mapping strategy.

---

## Epics

### Cost Modeling Patterns De-Risking (P0, active)

**File**: `backlog/epic-cost-patterns-derisking.md`

| ID | Name | Scale | Status |
|----|------|-------|--------|
| WI-001 | Coffee Maker Pattern Fixes | standard | active |
| WI-002 | Cost Patterns Demo | standard | active |

**Key validated patterns**: `NumericalFunctions::sum` for multiplicity aggregation, dot notation for attribute binding, `redefines` for adding features, parameterized multiplicity.

### sysml-codegen Upgrade (P1, draft)

**File**: `backlog/epic-sysml-codegen-upgrade.md`

No sub-items decomposed yet. Spec at `backlog/epic-sysml-codegen-upgrade.md` defines the sysml-codegen changes needed to process Pattern A (nested cost models).

---

## Standalone Items

### Completed

| ID | Name | Priority | Completed |
|----|------|----------|-----------|
| WI-004 | Foundation Package | P0 | 2026-01-26 |
| WI-005 | Power Balance Calculations | P0 | 2026-01-26 |

**Foundation Package** deliverables: 13 enum defs (types.sysml), 6 custom units (units.sysml), 12 material part defs (materials.sysml), 14 regression tests.

**Power Balance Calculations** deliverables: Generic `'Power Balance Calc'` + `'MFE Power Balance Calc'` (16 inputs, 15 outputs), 25 regression tests. Formulas verified against PyFECONS PowerBalance.py. Direct energy conversion (p_dee, eta_de) deferred — see WI-018.

### Failed

| ID | Name | Priority | Status |
|----|------|----------|--------|
| WI-003 | Explicit Types Redefines | P1 | failed |

Hypothesis that explicit types on `redefines` would fix Tom Sawyer visualization was incorrect. Tool limitation, not syntax issue.

### Backlog — P0

| ID | Name | Priority | Notes |
|----|------|----------|-------|
| WI-006 | Create 'Costed Component' Interface | P0 | Blocks all P1 part definitions. See `knowledge/sources/COST_MODELING.md` for pattern. |

### Backlog — P1

| ID | Name | Priority | Dependencies |
|----|------|----------|--------------|
| WI-007 | Power Core Definitions | P1 | WI-004, WI-006 |
| WI-008 | Geometry Calculations | P1 | WI-004 |
| WI-009 | Magnet System (MFE) | P1 | WI-004, WI-006, WI-007 |
| WI-010 | First CATF MFE Design | P1 | WI-005, WI-007, WI-008, WI-009 |

### Backlog — P2

| ID | Name | Priority | Dependencies |
|----|------|----------|--------------|
| WI-011 | CAS22 Subsystem Costing | P2 | WI-010 |
| WI-012 | Heating System Definitions | P2 | WI-007 |
| WI-013 | Balance of Plant | P2 | WI-007 |
| WI-014 | Cost Rollup and LCOE | P2 | WI-011, WI-013 |
| WI-015 | IFE Variant Support | P2 | WI-004, WI-014 |

### Backlog — P3

| ID | Name | Priority | Dependencies |
|----|------|----------|--------------|
| WI-016 | Full CAS Coverage | P3 | WI-014 |
| WI-017 | Additional Fusion Concepts | P3 | WI-016, WI-015 |
| WI-018 | Model p_dee and eta_de Power Paths | P3 | WI-005, PyFECONS upstream |

---

## Documentation References

- **Project Overview**: `modeling_project/OVERVIEW.md`
- **Modeling Guide**: `modeling_project/MODELING_GUIDE.md`
- **Cost Modeling Guide**: `knowledge/sources/COST_MODELING.md`
- **Workflow**: `modeling_project/MODELING_PROCESS.md`
- **Source Index**: `knowledge/SOURCE_INDEX.md`
- **Architecture Research**: `knowledge/research/approved/20260105-103000_catf-mfe-architecture.md`
- **Library Mapping Strategy**: `knowledge/research/approved/20260123-pyfecons-library-mapping-strategy.md`
- **Cost Pattern Validation**: `models/tests/coffee_maker/` (reference implementation)

---

**Last Updated**: 2026-02-02
**Next Review**: After WI-006 ('Costed Component' Interface) completion
