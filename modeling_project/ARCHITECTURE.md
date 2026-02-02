# Model Architecture

Structural decisions about how the domain is decomposed into model packages. These are the architectural choices that shape the model ecosystem — decisions that outlive any single work item and that new work must respect.

---

## Domain Decomposition

The fusion power plant is decomposed along two axes:

**Physical hierarchy**: Plant → Subsystems → Components, following the ARPA-E CAS (Cost Account Structure) hierarchy. CAS20 (Direct Costs) subdivides into reactor plant equipment (CAS22), turbine plant (CAS23), electric plant (CAS24), and miscellaneous (CAS25–29). CAS22 further subdivides into reactor-type-specific components (magnets/lasers, heating/ignition, blanket, shield, divertor/target factory).

**Concept independence**: Shared definitions live in `library/` (concept-agnostic: types, units, materials, base calc defs). Concept-specific assemblies live in `designs/` (CATF MFE, IFE variants, etc.). This separation ensures ~60% of definitions are reusable across reactor concepts.

**Subsystem boundaries**:
- **Power Core**: Everything inside the plasma-facing first wall (magnets, blanket, shield, divertor, heating). Reactor-type-specific.
- **Balance of Plant (BOP)**: Everything outside — turbine, cooling, electrical systems. Largely shared across reactor types.
- **Plant-Level**: Buildings, site work, indirect costs (CAS30–60). Shared.

---

## Package Organization

| Package | Purpose | Domain Scope | Dependencies |
|---------|---------|--------------|--------------|
| library/foundation/ | Base types (enums), units, materials | Cross-cutting | None |
| library/calculations/power_balance/ | Power flow calculations | Plasma → grid | foundation/ |
| library/calculations/ | Shared calc defs (geometry, costing) | Cross-cutting | foundation/ |
| library/definitions/ | Part definitions (plant, components) | Cross-cutting base | foundation/ |
| library/materials/ | Material property definitions | Cross-cutting | foundation/ |
| designs/catf_mfe/ | CATF compact tokamak configuration | Full MFE plant | All library packages |

---

## Key Decisions

### AD-001: Reactor Type Taxonomy
**Decision**: MFE, IFE, MIF as top-level reactor categories. Each gets a separate `designs/` subdirectory. Shared components live in `library/`; type-specific assemblies in `designs/`.
**Rationale**: Different reactor types share ~60% of components (buildings, turbine, BOP) but diverge on power core. CAS22 branch points: CAS220103 (Coils vs Lasers), CAS220104 (Heating vs Ignition), CAS220108 (Divertor vs Target Factory). (DI-010)
**Date**: 2026-01-05
**Status**: active

### AD-002: Library vs Designs Separation
**Decision**: Concept-agnostic definitions (part defs, calc defs, enums, materials) live in `library/`. Concept-specific usages (part usages with concrete parameter values) live in `designs/{concept}/`.
**Rationale**: Enables reuse across reactor concepts and clean dependency direction (designs depend on library, never reverse). Mirrors PyFECONS shared vs type-specific module split. (DI-007)
**Date**: 2026-01-05
**Status**: active

### AD-003: Cost Aggregation Follows CAS Hierarchy
**Decision**: Cost rollup mirrors the ARPA-E CAS standard. Each cost account maps to a model package or component. Aggregation uses `NumericalFunctions::sum` for parent-level rollup.
**Rationale**: Enables direct validation against PyFECONS which uses the same hierarchy. CAS provides a standardized decomposition accepted by ARPA-E and industry. (DI-001, DI-004)
**Date**: 2026-01-06
**Status**: active

### AD-004: Foundation Package Structure
**Decision**: Foundation package contains three files: `types.sysml` (13+ enums including ReactorType, ConfinementType, FuelType), `units.sysml` (economic units: M_USD, USD_KG, etc.), `materials.sysml` (10+ material definitions with density, thermal_conductivity, unit_cost).
**Rationale**: All downstream packages depend on these base definitions. Separating types/units/materials keeps each file focused and reduces merge conflicts. Enum values match PyFECONS exactly for validation. (DI-010)
**Date**: 2026-01-23
**Status**: active

### AD-005: Power Balance Calculation Architecture
**Decision**: Three-tier calc def structure: `Alpha Power Calc` (fuel-type-dependent alpha fraction), `Power Balance Calc` (abstract base with shared logic), `MFE Power Balance Calc` (MFE-specific with 16 inputs, p_net output). Calculation flow is strictly acyclic.
**Rationale**: Power balance outputs drive all downstream costs. The tiered structure allows reactor-type specialization (MFE vs IFE vs MIF) while sharing the alpha power calculation. 16 inputs match PyFECONS PowerBalance.py interface exactly. (DI-002, DI-009)
**Date**: 2026-01-26
**Status**: active
