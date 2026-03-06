---
Status: completed
Scale: standard
Epic: IFE Cost Modeling
Owner: reid
Created: 2026-03-02
Updated: '2026-03-02'
---

# WI-006: IFE Cost Structure Library

## Overview

Define the reusable, driver-agnostic library definitions for IFE economic modeling. This is the foundation layer for the IFE Cost Modeling epic — all downstream work items (WI-007 Generic IFE Concept Model, WI-008 HIF Concept Instantiation) import from these definitions.

## Goals & Context

**Goals served**:
- RQ-1: Cost drivers across confinement approaches — this item defines the parameter structure that captures IFE cost drivers
- RQ-2: Credible LCOE ranges — the LCOE calculation framework enables range exploration
- RQ-3: Shared vs. divergent cost structure — CAS mapping with shared/divergent classification directly answers this
- RQ-5: High-sensitivity, high-uncertainty parameters — sensitivity rankings on all 14 parameters enable identification

**Domain insights applied**:
- DI-001: Fusion cycle gain viability threshold (eta*G > 10) → MR-WI006-4
- DI-002: CAS22 is the IFE-MFE divergence point → MR-WI006-2
- DI-003: Target cost as unique IFE operating cost → informs parameter definition
- DI-004: Driver cost reference points spanning 3 orders of magnitude → informs range metadata
- DI-005: Hawker's 14-parameter model with sensitivity rankings → MR-WI006-1, MR-WI006-3

**Epic context**: First item in a strictly sequential chain (WI-006 → WI-007 → WI-008). No dependencies; establishes patterns for the entire epic.

**Pattern-defining nature**: This is the first SysML work in the project. Since no modeling patterns exist yet (MR-6, PR-3), the conventions established here — how attributes carry ranges, how CAS accounts nest, how citations attach to values — become the implicit template for all subsequent modeling work.

## Current State

No SysML models exist. The `models/library/` and `models/designs/` directories are empty. No architectural decisions (AD-XXX) have been registered.

The research basis is complete:
- 7 IFE sources ingested and registered in SOURCE_INDEX.md
- 5 domain insights captured (DI-001 through DI-005)
- Approved research: `knowledge/research/approved/20260302-165055_ife-system-modeling-first-pass.md`
- Modeling target selection: `modeling_project/intent/IFE Modeling Target Selection.md`

## Modeling Requirements

### Functional

#### MR-WI006-1: Hawker's 14 Parameters as Typed Attributes

The library SHALL define all 14 Hawker parameters as typed attributes with units, value ranges (min/max), default values, and Pearson sensitivity rankings.

- **Type**: Functional
- **Priority**: Must
- **Derives from**: DI-005, RQ-5
- **Validation**: Inspect model — 14 attributes present, each with unit, range, default, and sensitivity metadata (SV-001)

The 14 parameters are:

| # | Parameter | Symbol | Units | Range | Default | Pearson r |
|---|-----------|--------|-------|-------|---------|-----------|
| 1 | Availability | mu_a | fraction | 0.50–1.00 | 0.70 | -0.127 |
| 2 | Blanket energy multiple | E_b | dimensionless | 0.6–1.4 | 1.2 | -0.038 |
| 3 | Discount rate | d | fraction | 0.02–0.12 | 0.08 | +0.247 |
| 4 | Driver cost constant | gamma | $/J | 2–10 | 5 | +0.075 |
| 5 | Driver efficiency | mu_d | fraction | 0.05–0.30 | 0.10 | -0.063 |
| 6 | Driver energy (to target) | E_d | MJ | 0.5–50 | 10 | +0.011 |
| 7 | Driver lifetime | N_d | shots | 1e6–1e9 | 5e7 | -0.134 |
| 8 | Frequency | f | Hz | 0.01–10 | 0.2 | +0.035 |
| 9 | Gain | G | dimensionless | 10–1000 | 500 | -0.164 |
| 10 | O&M cost constant | epsilon | $/kWe-yr | 10–100 | 30 | +0.050 |
| 11 | Plant cost constant | alpha | $/kWe | 1000–6000 | 3000 | +0.210 |
| 12 | Target cost constant | delta | $/target | 1–100 | 10 | +0.186 |
| 13 | Thermal efficiency | mu_th | fraction | 0.30–0.60 | 0.40 | -0.033 |
| 14 | Yield cost constant | beta | $/GJ | 5e5–5e7 | 5e6 | +0.026 |

> Source: `knowledge/sources/a_simplified_economic_model_for_inertial_fusion/output.md`
> Ref: Table 1 (parameter definitions), Figure 3 (sensitivity rankings)
> Basis: Complete parameter set from Hawker 2020 Monte Carlo analysis

#### MR-WI006-2: CAS Account Hierarchy with IFE Classification

The library SHALL define a CAS account hierarchy at level 2 (CAS20–27, 91–99) with each account classified as shared (MFE+IFE), IFE-specific, or IFE-divergent.

- **Type**: Functional
- **Priority**: Must
- **Derives from**: DI-002, MR-1, RQ-3
- **Validation**: Inspect model — CAS accounts present with classification metadata (SV-002)

Level 3 disaggregation (CAS22.1.x sub-accounts) is deferred to WI-007 where the generic IFE model needs driver-specific structure.

Account classification per DI-002 and ARIES Cost Account Doc:

| Account | Name | Classification |
|---------|------|----------------|
| CAS20 | Land and Land Rights | shared |
| CAS21 | Structures and Site Facilities | shared (volumes differ) |
| CAS22 | Power Core Equipment | IFE-divergent |
| CAS23 | Turbine Plant Equipment | shared |
| CAS24 | Electric Plant Equipment | shared |
| CAS25 | Heat Rejection Equipment | shared |
| CAS26 | Miscellaneous Plant Equipment | shared |
| CAS27 | Special Materials | shared (coolant-dependent) |
| CAS91–99 | Indirect Costs | shared (percentages vary) |

> Source: `knowledge/sources/aries_cost_account_documentation/output.md`
> Ref: L185-186 (universality), L1005-1008 (CAS22 divergence)
> Basis: CAS framework from Schulte et al. 1978, used across all MFE and IFE design studies

#### MR-WI006-3: LCOE Calculation Framework

The library SHALL implement an LCOE calculation using Hawker's discounted cash flow formula, taking the 14 parameters as inputs and producing LCOE in $/MWh.

- **Type**: Functional
- **Priority**: Must
- **Derives from**: DI-005, RQ-2
- **Validation**: Formula structure matches Hawker equations; dimensional analysis produces $/MWh (SV-003)

Hawker's LCOE formula decomposes total cost into five categories:
1. Plant cost: C_p = alpha * P_e
2. Yield cost: C_Y = beta * E_f / Y_c (reaction vessel proportional to fusion energy per shot)
3. Driver cost: C_d = gamma * E_d (construction and periodic replacement over lifetime N_d)
4. Target cost: per-shot operating cost = delta per target
5. O&M cost: epsilon * P_e per year

LCOE is the annualized sum of capital (discounted), replacement (driver lifetime), operating (target + O&M), divided by annual energy production (P_e * mu_a * 8760).

> Source: `knowledge/sources/a_simplified_economic_model_for_inertial_fusion/output.md`
> Ref: Equations 1–6 (cost decomposition), Section 3 (DCF methodology)
> Basis: Hawker 2020 DCF LCOE model

#### MR-WI006-4: Fusion Cycle Gain Constraint

The library SHALL define the fusion cycle gain relationship (eta * G * M * epsilon) and a viability constraint requiring eta*G > 10.

- **Type**: Functional
- **Priority**: Must
- **Derives from**: DI-001, RQ-1
- **Validation**: Constraint expression present and evaluable (SV-004)

The recirculating power fraction f = 1 / (eta * G * M * epsilon). The product eta*G must exceed ~10 for economically viable IFE. This creates fundamentally different gain requirements by driver type, but the constraint itself is driver-agnostic.

> Source: `knowledge/sources/energy_from_inertial_fusion/output.md`, `knowledge/sources/accelerators_for_inertial_fusion_energy_production/output.md`
> Ref: EIF-1992 "Components" section; Accel-2013 Section 3
> Basis: Physics-derived minimum for economic viability across all IFE driver types

#### MR-WI006-5: Costed Component Interface

The library SHALL define a costed component interface with at minimum a `capital_cost` attribute, suitable for specialization by downstream concept models.

- **Type**: Functional
- **Priority**: Must
- **Derives from**: MR-2
- **Validation**: Interface definition exists; downstream usability verified during WI-007

### Quality

#### MR-WI006-6: Traceable Citations on All Quantitative Values

All quantitative values (ranges, defaults, sensitivity coefficients) SHALL carry structured citations per MR-4 format (Source/Ref/Basis in doc comments).

- **Type**: Quality
- **Priority**: Must
- **Derives from**: MR-4, PR-5
- **Validation**: Every numeric literal has a citation; no unattributed values

#### MR-WI006-7: Concept-Agnostic Definitions

All definitions SHALL be concept-agnostic — no driver-type-specific or reactor-specific parameter values.

- **Type**: Quality
- **Priority**: Must
- **Derives from**: MR-3
- **Validation**: Review — no references to specific driver types (HIF, laser, pulser) in parameter defaults

### Constraint

#### MR-WI006-8: Library Location

All files SHALL reside in `models/library/`.

- **Derives from**: MR-3, project structure

#### MR-WI006-9: Parse Validation

All model files SHALL pass syside validation (Level 1 — parse without errors).

- **Priority**: Must
- **Derives from**: Epic success criteria
- **Validation**: `uv run syside check models/library/*.sysml` — zero errors (SV-005)

## Scope Boundaries

### In Scope

- `models/library/ife_cost_parameters.sysml` — Hawker's 14 parameters as typed attributes with metadata
- `models/library/cas_hierarchy.sysml` — CAS level 2 account definitions with IFE classification
- `models/library/lcoe_calculation.sysml` — LCOE calculation framework
- `models/library/costed_component.sysml` — costed component interface definition
- SV-001 through SV-005 entries in VALIDATION_MATRIX.md

### Out of Scope

- Driver-specific parameter values or cost formulas (WI-007, WI-008)
- CAS22 level 3 sub-account disaggregation (WI-007)
- Formal written modeling pattern document — patterns are implicit in the SysML files
- Shared CAS elements that are also MFE-relevant (e.g., CAS23 turbine plant detail) — defer to MFE modeling
- Monte Carlo simulation or parametric sweeps (analysis phase)
- Generic IFE concept model assembly (WI-007)

## Success Criteria

### Functional

- All 14 Hawker parameters exist as typed attributes with units, ranges, defaults, and sensitivity rankings
- CAS level 2 hierarchy covers accounts 20–27 and 91–99 with shared/divergent classification
- LCOE calculation definition takes the 14 parameters and produces $/MWh output
- Fusion cycle gain constraint (eta*G > 10) is defined and evaluable
- Costed component interface exists with `capital_cost` attribute

### Quality

- Every quantitative value carries a Source/Ref/Basis citation in doc comments
- No driver-specific values anywhere in library definitions
- All files parse cleanly with `uv run syside check`

### Verification

- SV-001 through SV-005 registered in VALIDATION_MATRIX.md
- All SV entries achievable via model inspection after implementation

## Assumptions & Risks

| # | Assumption/Risk | Type | Confidence/Likelihood | Impact | Mitigation |
|---|----------------|------|----------------------|--------|------------|
| A1 | Hawker's 14 parameters are sufficient to characterize IFE LCOE at the library level | Assumption | High — validated by Monte Carlo in paper | Low if wrong — can add parameters later | |
| A2 | SysML v2 can represent parameter ranges and sensitivity metadata in attribute definitions | Assumption | Medium — depends on syside support for annotations/doc comments | Medium — may need workaround patterns | Prototype during design phase |
| R1 | CAS level 2 may be too coarse for meaningful cost comparison | Risk | Medium | Low — level 3 added in WI-007 | Epic acknowledges: "disaggregate incrementally" |
| R2 | syside parser limitations may constrain how calculation definitions are expressed | Risk | Medium | Medium — may limit LCOE formula expressiveness | Test calc def syntax during design |
| R3 | First SysML files establish patterns without explicit pattern review | Risk | Medium | Medium — rework if patterns don't scale | Treat as pattern-defining; review conventions before WI-007 |

## Traceability

### Source Requirements

| Source | What it provides | Requirements served |
|--------|-----------------|-------------------|
| `knowledge/sources/a_simplified_economic_model_for_inertial_fusion/output.md` | 14 parameters, LCOE formula, sensitivity rankings | MR-WI006-1, MR-WI006-3 |
| `knowledge/sources/aries_cost_account_documentation/output.md` | CAS hierarchy, IFE/MFE account mapping | MR-WI006-2 |
| `knowledge/sources/energy_from_inertial_fusion/output.md` | Fusion cycle gain, IFE process chain | MR-WI006-4 |
| `knowledge/sources/accelerators_for_inertial_fusion_energy_production/output.md` | Driver efficiency ranges, eta*G threshold | MR-WI006-4 |
| `/home/reid/PyFECONS` | CAS22 implementation, costed component patterns | MR-WI006-2, MR-WI006-5 |

### Downstream Impacts

- WI-007 (Generic IFE Concept Model) imports all library definitions from this item
- WI-008 (HIF Concept Instantiation) specializes the costed component interface
- Future MFE modeling may reuse CAS hierarchy and LCOE calculation (shared accounts)

### Applicable Project Requirements

- MR-1: CAS hierarchy as primary cost decomposition
- MR-2: Standard costed component interface
- MR-3: Library concept-agnostic, designs concept-specific
- MR-4: Traceable citations on all quantitative values
- MR-6: Modeling patterns defined before production models (this item is pattern-defining)
- PR-3: Documented patterns before production models (implicit in SysML files)
- PR-5: Committed artifacts at every phase

## Related Artifacts

- **Epic**: `work/backlog/epic-ife-cost-modeling.md`
- **Research**: `knowledge/research/approved/20260302-165055_ife-system-modeling-first-pass.md`
- **Target selection**: `modeling_project/intent/IFE Modeling Target Selection.md`
- **Design**: `work/active/WI-006_ife-cost-structure-library/design.md` (to be created)
- **Plan**: `work/active/WI-006_ife-cost-structure-library/plan.md` (to be created)
