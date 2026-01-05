# Work Backlog

Prioritized list of work epics for the CATF MFE model implementation.

---

## Recently Completed

<!-- Move completed items here with dates -->

---

## Priority 0: READY

### Epic: Phase 1 - Foundation Library
**Status**: READY
**Priority**: P0
**Source**: [CATF MFE Architecture Research](../research/20260105-103000_catf-mfe-architecture.md)

**Goal**: Establish the foundational library infrastructure for FusionTEA models, enabling all downstream calculations and definitions.

**Scope**:
- Create `library/foundation.sysml` with FusionTEA package structure
- Define unit imports (SI, ISQ)
- Create enums: ReactorType, FuelType, ConfinementType, MagnetType
- Define base attribute definitions
- Create `library/calculations/power_balance.sysml` with PowerBalanceCalc
- Include core power flows (p_alpha, p_neutron, p_th, p_net) and Q-value calculations

**Dependencies**: None

---

## Priority 1: After P0 Complete

### Epic: Phase 2 - Geometry & Structure
**Status**: PENDING
**Priority**: P1
**Source**: [CATF MFE Architecture Research](../research/20260105-103000_catf-mfe-architecture.md)

**Goal**: Add geometry calculations and magnet definitions to support radial build and coil modeling.

**Scope**:
- Create `library/calculations/geometry.sysml` with radial build calculations
- Implement volume/area computations (ToroidalVolumeCalc, etc.)
- Create `library/definitions/magnets.sysml` with TF, CS, PF coil part definitions
- Define magnet attributes (dimensions, material, current density)

**Dependencies**: Phase 1 - Foundation Library

---

### Epic: Phase 3 - First CATF Design
**Status**: PENDING
**Priority**: P1
**Source**: [CATF MFE Architecture Research](../research/20260105-103000_catf-mfe-architecture.md)

**Goal**: Create the first concrete CATF design using library definitions and validate against PyFECONS.

**Scope**:
- Create `designs/catf/parameters.sysml` with all CATF input values
- Create `designs/catf/plant.sysml` with top-level integration
- Wire power balance and geometry calculations
- Validate power balance outputs against PyFECONS
- Validate geometry calculations against PyFECONS

**Dependencies**: Phase 2 - Geometry & Structure

---

## Priority 2: Medium Term

### Epic: Phase 4 - Cost Calculations
**Status**: BACKLOG
**Priority**: P2
**Source**: [CATF MFE Architecture Research](../research/20260105-103000_catf-mfe-architecture.md)

**Goal**: Add costing calculation definitions to enable LCOE estimation.

**Scope**:
- Add CAS22 subsystem costing calc defs (magnets, blanket, vessel)
- Implement cost rollup to CAS20
- Create LCOE calculation (LCOECalc)
- Create `library/calculations/costing.sysml`
- Create `library/calculations/lcoe.sysml`

**Dependencies**: Phase 3 - First CATF Design (validated)

---

## Priority 3: Deferred

### Epic: Phase 5 - Complete Model
**Status**: BACKLOG
**Priority**: P3
**Source**: [CATF MFE Architecture Research](../research/20260105-103000_catf-mfe-architecture.md)

**Goal**: Achieve full PyFECONS parity with comprehensive cost account coverage.

**Scope**:
- Full subsystem coverage (all CAS categories)
- All cost accounts (CAS10-CAS90)
- Comprehensive validation against PyFECONS outputs
- Additional definitions: blanket.sysml, vacuum_system.sysml, power_systems.sysml, balance_of_plant.sysml
- Materials library: fusion_materials.sysml

**Dependencies**: Phase 4 - Cost Calculations

---

## Documentation References

- **Project Overview**: `project/OVERVIEW.md`
- **Modeling Guide**: `project/MODELING_GUIDE.md`
- **Workflow**: `project/MODELING_PROCESS.md`
- **Source Index**: `SOURCE_INDEX.md`
- **Architecture Research**: `project/research/20260105-103000_catf-mfe-architecture.md`

---

**Last Updated**: 2026-01-05
**Next Review**: After Phase 1 completion
