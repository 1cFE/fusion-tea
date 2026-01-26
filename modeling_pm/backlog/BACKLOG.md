# Work Backlog

Prioritized list of work items for FusionTEA SysML v2 modeling, based on PyFECONS library mapping strategy.

---

## Recently Completed

### Epic: Foundation Package - COMPLETE (2026-01-26)
**Priority**: P0

**Deliverables**:
- `models/library/foundation/types.sysml` - 13 enum definitions
- `models/library/foundation/units.sysml` - 6 custom attribute definitions
- `models/library/foundation/materials.sysml` - 12 material part definitions
- `tests/models/test_foundation.py` - 14 regression tests
- `models/tests/foundation_import_test.sysml` - Import validation

**Validation**: All tests pass, all files parse, documentation complete with Source citations

---

### Epic: Power Balance Calculations - COMPLETE (2026-01-26)
**Priority**: P0
**Source**: [PyFECONS Library Mapping Strategy](../research/20260123-pyfecons-library-mapping-strategy.md)

**Goal**: Implement power balance calculations that drive most downstream calculations.

**Deliverables**:
- `models/library/calculations/power_balance/power_balance.sysml` - Generic PowerBalanceLibrary
  - `'Alpha Power Calc'` - Fuel-type dependent alpha power (DT, DD, DHE3, PB11)
  - `'Power Balance Calc'` - Generic p_alpha, p_neutron, q_sci
- `models/library/calculations/power_balance/mfe_power_balance.sysml` - MFEPowerBalanceLibrary
  - `'MFE Power Balance Calc'` - Full MFE power flow (16 inputs, 15 outputs)
- `tests/models/test_power_balance.py` - 25 regression tests (structure + numerical validation)

**Validation**:
- All 25 tests pass
- All files parse without errors
- Formulas verified against PyFECONS PowerBalance.py:8-50, 94-104
- Documentation complete with Source citations

**Note**: Direct energy conversion (p_dee, eta_de) deferred per spec - see P3 task "Model p_dee and eta_de Power Paths"

**Dependencies**: Foundation Package (COMPLETE)

---

## Priority 1: After P0 Complete

### Epic: Power Core Definitions
**Status**: PENDING
**Priority**: P1
**Source**: [PyFECONS Library Mapping Strategy](../research/20260123-pyfecons-library-mapping-strategy.md)

**Goal**: Define core reactor components shared across fusion concepts.

**Scope**:
- `library/definitions/plant.sysml` - Top-level 'Fusion Power Plant' part def
- `library/definitions/power_core/plasma.sysml` - 'Plasma' part def with confinement parameters
- `library/definitions/power_core/blanket.sysml` - 'Blanket System' with material variants
- `library/definitions/power_core/shield.sysml` - 'Radiation Shield' part def
- `library/definitions/power_core/vacuum_vessel.sysml` - 'Vacuum Vessel' part def

**Validation**: Attributes map to PyFECONS `inputs/blanket.py`, `inputs/shield.py`

**Dependencies**: Foundation Package (COMPLETE)

---

### Epic: Geometry Calculations
**Status**: PENDING
**Priority**: P1
**Source**: [PyFECONS Library Mapping Strategy](../research/20260123-pyfecons-library-mapping-strategy.md)

**Goal**: Implement radial build and volume calculations for toroidal geometry.

**Scope**:
- `library/calculations/geometry/radial_build.sysml` - Layer thickness calculations (14 layers per PyFECONS)
- `library/calculations/geometry/toroidal_volume.sysml` - Volume and surface area calcs

**Validation**: Compare geometry outputs against PyFECONS CAS220101 calculations

**Dependencies**: Foundation Package (COMPLETE)

---

### Epic: Magnet System (MFE)
**Status**: PENDING
**Priority**: P1
**Source**: [PyFECONS Library Mapping Strategy](../research/20260123-pyfecons-library-mapping-strategy.md)

**Goal**: Define magnet coil components and cost calculations for MFE reactors.

**Scope**:
- `library/definitions/magnets/coil.sysml` - Base 'Magnet Coil' part def
- `library/definitions/magnets/tf_coil.sysml` - 'TF Coil' specialization
- `library/definitions/magnets/pf_coil.sysml` - 'PF Coil' specialization
- `library/definitions/magnets/cs_coil.sysml` - 'Central Solenoid' specialization
- `library/calculations/costing/magnet_cost.sysml` - Magnet costing calc (CAS220103)

**Validation**: Coil attributes map to PyFECONS `inputs/coils.py`; cost calc validates against `costing/mfe/cas22/cas220103_coils.py`

**Dependencies**: Foundation Package, Power Core Definitions

---

### Epic: First CATF MFE Design
**Status**: PENDING
**Priority**: P1
**Source**: [PyFECONS Library Mapping Strategy](../research/20260123-pyfecons-library-mapping-strategy.md)

**Goal**: Create first concrete CATF design instance using library definitions.

**Scope**:
- `designs/catf_mfe/parameters.sysml` - All CATF input values from PyFECONS DefineInputs.py
- `designs/catf_mfe/radial_build.sysml` - Geometry instance with layer values
- `designs/catf_mfe/reactor_core.sysml` - Core assembly (magnets, blanket, shield, vessel)
- `designs/catf_mfe/plant.sysml` - Top-level plant integration

**Validation Checkpoint**:
- Power balance: p_net, q_eng match PyFECONS
- Geometry: volumes, surface areas match PyFECONS
- Initial cost estimates for major components

**Dependencies**: Power Balance Calculations, Power Core Definitions, Geometry Calculations, Magnet System

---

## Priority 2: Medium Term

### Epic: CAS22 Subsystem Costing
**Status**: BACKLOG
**Priority**: P2
**Source**: [PyFECONS Library Mapping Strategy](../research/20260123-pyfecons-library-mapping-strategy.md)

**Goal**: Implement cost calculations for all CAS22 reactor equipment categories.

**Scope**:
- `library/calculations/costing/cas220101_reactor_equipment.sysml` - Geometry-driven costs
- `library/calculations/costing/cas220102_shield.sysml` - Shield costing
- `library/calculations/costing/cas220104_heating.sysml` - Supplementary heating (NBI, ICRF)
- `library/calculations/costing/cas220105_structure.sysml` - Primary structure
- `library/calculations/costing/cas220106_vacuum.sysml` - Vacuum system
- `library/calculations/costing/cas220107_power_supplies.sysml` - Power supply costing
- `library/calculations/costing/cas220108_divertor.sysml` - Divertor costing (MFE)

**Validation**: Each calc validates against corresponding PyFECONS `costing/mfe/cas22/` module

**Dependencies**: First CATF MFE Design (validated)

---

### Epic: Heating System Definitions
**Status**: BACKLOG
**Priority**: P2
**Source**: [PyFECONS Library Mapping Strategy](../research/20260123-pyfecons-library-mapping-strategy.md)

**Goal**: Define heating system components for MFE reactors.

**Scope**:
- `library/definitions/heating/heating_system.sysml` - Base 'Primary Heating System' part def
- `library/definitions/heating/nbi.sysml` - 'Neutral Beam Injection' specialization
- `library/definitions/heating/icrf.sysml` - 'Ion Cyclotron RF' specialization
- `library/definitions/exhaust/divertor.sysml` - 'Divertor' part def

**Validation**: Attributes map to PyFECONS `inputs/supplementary_heating.py`

**Dependencies**: Power Core Definitions

---

### Epic: Balance of Plant
**Status**: BACKLOG
**Priority**: P2
**Source**: [PyFECONS Library Mapping Strategy](../research/20260123-pyfecons-library-mapping-strategy.md)

**Goal**: Define shared balance-of-plant components and cost calculations.

**Scope**:
- `library/definitions/bop/buildings.sysml` - Building part defs (CAS21)
- `library/definitions/bop/electrical.sysml` - 'Electrical Plant' (CAS24)
- `library/definitions/bop/cooling.sysml` - 'Heat Rejection System' (CAS26)
- `library/definitions/power_conversion/turbine.sysml` - 'Turbine Plant' (CAS23)
- `library/definitions/power_conversion/power_supplies.sysml` - 'Power Supply System'

**Validation**: Shared calculations match PyFECONS `costing/calculations/`

**Dependencies**: Power Core Definitions

---

### Epic: Cost Rollup and LCOE
**Status**: BACKLOG
**Priority**: P2
**Source**: [PyFECONS Library Mapping Strategy](../research/20260123-pyfecons-library-mapping-strategy.md)

**Goal**: Implement cost aggregation and final LCOE calculation.

**Scope**:
- `library/calculations/costing/cas_rollup.sysml` - Cost aggregation patterns
- `library/calculations/costing/component_cost.sysml` - Unit cost calculations
- `library/calculations/costing/learning_curve.sysml` - Nth-of-a-kind reduction
- `library/calculations/lcoe/lcoe.sysml` - Final LCOE calculation

**Validation**: LCOE output matches PyFECONS for CATF design

**Dependencies**: CAS22 Subsystem Costing, Balance of Plant

---

### Epic: IFE Variant Support
**Status**: BACKLOG
**Priority**: P2
**Source**: [PyFECONS Library Mapping Strategy](../research/20260123-pyfecons-library-mapping-strategy.md)

**Goal**: Add IFE-specific components to enable laser fusion designs.

**Scope**:
- `library/definitions/lasers/laser_system.sysml` - 'Laser System' base def
- `library/definitions/lasers/target_factory.sysml` - 'Target Factory' part def
- `library/calculations/power_balance/ife_power_balance.sysml` - IFE power flow
- `library/calculations/costing/cas220103_lasers.sysml` - Laser system costing
- `library/calculations/costing/cas220108_target.sysml` - Target factory costing

**Validation**: IFE calculations match PyFECONS `costing/ife/` modules

**Dependencies**: Foundation Package (COMPLETE), Cost Rollup and LCOE

---

## Priority 3: Deferred

### Epic: Full CAS Coverage
**Status**: BACKLOG
**Priority**: P3
**Source**: [PyFECONS Library Mapping Strategy](../research/20260123-pyfecons-library-mapping-strategy.md)

**Goal**: Achieve full PyFECONS parity with all cost account categories.

**Scope**:
- CAS10 - Pre-Construction Costs (land, permits, licensing)
- CAS21 - All 19 building categories
- CAS27 - Special Materials
- CAS28 - Digital Twin
- CAS30-60 - Capitalized indirect, owner, supplementary, financial costs
- CAS70-90 - Annualized O&M, fuel, financial costs

**Validation**: Full cost breakdown matches PyFECONS output reports

**Dependencies**: Cost Rollup and LCOE

---

### Epic: Additional Fusion Concepts
**Status**: BACKLOG
**Priority**: P3
**Source**: [PyFECONS Library Mapping Strategy](../research/20260123-pyfecons-library-mapping-strategy.md)

**Goal**: Extend library to support stellarator, mirror, and other MFE concepts.

**Scope**:
- Stellarator-specific geometry calculations
- Mirror machine definitions
- Concept-specific specializations as needed
- Refine library for maximum reuse

**Dependencies**: Full CAS Coverage, IFE Variant Support

---

### Task: Model p_dee and eta_de Power Paths
**Status**: BACKLOG
**Priority**: P3
**Source**: PyFECONS PowerBalance.py (paths marked TODO in source)

**Goal**: Model the direct energy extraction (DEE) power paths when PyFECONS implements them.

**Context**: During Power Balance Calculations work, found that `p_dee` (direct energy extraction power) and `eta_de` (direct energy conversion efficiency) paths exist in PyFECONS but are marked as TODO / not yet implemented.

**Scope**:
- Monitor PyFECONS for implementation of these paths
- Add `p_dee` attribute to power balance calculations
- Add `eta_de` efficiency parameter to library
- Update MFE power balance to include DEE path in recirculating power

**Validation**: Match PyFECONS implementation when available

**Dependencies**: Power Balance Calculations (COMPLETE), PyFECONS upstream implementation

---

## Documentation References

- **Project Overview**: `modeling_pm/OVERVIEW.md`
- **Modeling Guide**: `modeling_pm/MODELING_GUIDE.md`
- **Workflow**: `modeling_pm/MODELING_PROCESS.md`
- **Source Index**: `SOURCE_INDEX.md`
- **Architecture Research**: `modeling_pm/research/20260105-103000_catf-mfe-architecture.md`
- **Library Mapping Strategy**: `modeling_pm/research/20260123-pyfecons-library-mapping-strategy.md`

---

**Last Updated**: 2026-01-26
**Next Review**: After Power Core Definitions or Geometry Calculations completion
