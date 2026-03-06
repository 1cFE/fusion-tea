---
Status: completed
Scale: standard
Epic: IFE Cost Modeling
Owner: reid
Created: 2026-03-02
Updated: '2026-03-02'
---

# WI-007: Generic IFE Concept Model

## Overview

Build a driver-agnostic IFE power plant model that uses the library definitions from WI-006 (IFE Cost Structure Library). The model defines the assembly structure, abstraction boundaries, and cost rollup pathway for any IFE plant — serving as the template that driver-specific instantiations (WI-008 HIF, future laser/pulser concepts) will specialize.

## Goals & Context

**Goals served**:
- RQ-1: IFE cost drivers — the assembly structure shows where money goes in an IFE plant
- RQ-2: Credible LCOE ranges — LCOE computation using library's DCF formula with default parameters
- RQ-3: Shared vs. divergent structure — the model concretely separates shared subsystems (BOP, turbine) from IFE-divergent ones (driver, target factory, chamber)

**Domain insights applied**:
- DI-001: Fusion cycle gain viability threshold → MR-WI007-6 (power balance integration)
- DI-002: CAS22 is the IFE-MFE divergence point → MR-WI007-5 (CAS22 level 3 disaggregation)
- DI-003: Target cost as unique IFE operating cost → MR-WI007-3 (target factory subsystem)
- DI-004: Driver cost reference points by driver type → MR-WI007-2 (abstract driver with parameterized cost)
- DI-005: Hawker's 14-parameter model → MR-WI007-7, MR-WI007-8 (cost rollup and parameter binding)

**Epic context**: Second item in a strictly sequential chain (WI-006 → **WI-007** → WI-008). Depends on WI-006's library definitions. Establishes the plant-level assembly pattern that WI-008 specializes.

## Current State

**Library exists** (WI-006 output — 6 files in `models/library/`):
- `foundation/economic_parameter.sysml` — `Economic Parameter` attribute def (value, min, max, sensitivity)
- `foundation/costed_component.sysml` — abstract `Costed Component` part def (capital_cost, cas_code)
- `cost_structure/cas_hierarchy.sysml` — CAS level 2 account defs (CAS20–27, CAS90) with scope classification
- `cost_structure/ife_cost_parameters.sysml` — `IFE Cost Parameters` part def with all 14 Hawker parameters
- `analyses/fusion_cycle.sysml` — `Recirculating Power Fraction` calc def, `Viability Threshold` constraint def
- `analyses/ife_lcoe.sysml` — `IFE LCOE` calc def (14 inputs → LCOE in $/MWh)

**No designs exist** — `models/designs/` is empty. This is the first design model in the project.

## Modeling Requirements

### Functional

#### MR-WI007-1: IFE Power Plant Assembly

The model SHALL define an IFE power plant top-level part that composes all major subsystems (driver, target factory, reaction chamber, balance of plant, indirect costs) and maps each subsystem to its CAS account.

- **Type**: Functional
- **Priority**: Must
- **Derives from**: RQ-1, MR-1
- **Validation**: Model inspection — all subsystems present with CAS mapping (SV-006)

#### MR-WI007-2: Abstract Driver Interface

The model SHALL define an abstract driver part def with the four driver-specific Hawker parameters — efficiency (eta), cost per joule (gamma), energy (E_d), and lifetime in shots (N_d) — as required attributes, suitable for specialization by HIF, laser, and pulser instantiations.

- **Type**: Functional
- **Priority**: Must
- **Derives from**: Epic Item 2, DI-004
- **Validation**: Driver is abstract; 4 parameters present as typed attributes (SV-009)

#### MR-WI007-3: Target Factory as Operating Cost

The model SHALL model the target factory (CAS22.1.8) as a subsystem with per-target manufacturing cost (delta) as its primary cost parameter, treated as an operating cost separate from driver capital cost.

- **Type**: Functional
- **Priority**: Must
- **Derives from**: DI-003, Epic Item 2
- **Validation**: Target factory present with per-target cost attribute; cost flows to annual operating cost, not capital cost

#### MR-WI007-4: Abstract Reaction Chamber

The model SHALL define a reaction chamber with an abstract wall type classification (dry-wall, wetted-wall, liquid-wall) and blanket energy multiple parameter.

- **Type**: Functional
- **Priority**: Must
- **Derives from**: Epic Item 2, EIF-1992 chamber concepts
- **Validation**: Chamber has wall type enum and blanket energy multiple attribute

The three wall types reflect fundamentally different chamber engineering:
- **Dry-wall**: SiC or carbon composite first wall, limited by surface damage (laser IFE typical)
- **Wetted-wall**: Thin liquid film on structural wall, moderate protection
- **Liquid-wall**: Thick liquid curtain (FLiBe, Li), maximum protection, eliminates solid first wall (HIF typical)

> Source: `knowledge/sources/energy_from_inertial_fusion/output.md`
> Ref: Chamber concepts section
> Basis: EIF-1992 classification of IFE chamber approaches

#### MR-WI007-5: CAS22 Level 3 Sub-Account Disaggregation

The model SHALL disaggregate CAS22 (Power Core) into IFE-relevant level 3 sub-accounts, each specializing the library's `CAS Account`:

| Sub-Account | Name | Scope | Notes |
|-------------|------|-------|-------|
| CAS22.1.1 | First Wall / Blanket | shared | Energy capture, tritium breeding |
| CAS22.1.2 | Shield | shared | Neutron shielding |
| CAS22.1.3 | Driver | ife_divergent | Abstract — specialized per driver type |
| CAS22.1.5 | Primary Structure | shared | Vacuum vessel, support |
| CAS22.1.8 | Target Factory | ife_divergent | Per-shot consumable manufacturing |

- **Type**: Functional
- **Priority**: Must
- **Derives from**: DI-002, MR-1, ARIES Cost Account Doc
- **Validation**: Sub-accounts present with correct scope classification (SV-007)

CAS22.1.4 (Supplementary Heating / Ignition), 22.1.6 (Vacuum System), 22.1.7 (Power Supplies), 22.1.9 (Direct Energy Conversion), and 22.1.11 (Assembly/Installation) are deferred — they can be added when specific concepts need them.

> Source: `knowledge/sources/aries_cost_account_documentation/output.md`
> Ref: CAS22 sub-account definitions
> Basis: ARIES CAS framework with IFE-specific account mapping per DI-002

#### MR-WI007-6: Power Balance Integration

The model SHALL use the library's `Recirculating Power Fraction` calc and `Viability Threshold` constraint to compute net electric power and validate the eta*G viability condition.

- **Type**: Functional
- **Priority**: Must
- **Derives from**: DI-001, Epic Item 2
- **Validation**: Recirculating power fraction and viability constraint are bound to plant parameters

The power balance connects physics to economics:
- Gross thermal power = fusion energy per shot × blanket multiple × frequency
- Gross electric power = gross thermal × thermal efficiency
- Net electric power = gross electric − recirculating power (dominated by driver)
- Recirculating power fraction = 1 / (eta × G × M × epsilon_th)

#### MR-WI007-7: Cost Rollup to LCOE

The model SHALL connect subsystem costs through the CAS hierarchy to produce an LCOE value using the library's `IFE LCOE` calculation, with the 14 Hawker parameters bound to their physical subsystem sources.

- **Type**: Functional
- **Priority**: Must
- **Derives from**: RQ-2, Epic Item 2
- **Validation**: LCOE with default parameters within Hawker's $25–120/MWh range (SV-008)

Hawker's five cost categories map to CAS as follows:

| Hawker Category | Parameters | CAS Mapping |
|----------------|------------|-------------|
| Plant cost (C_p = alpha × P_e) | alpha | CAS20 + CAS21 + CAS23–26 |
| Yield cost (C_Y = beta × E_f) | beta | CAS22.1.1 (chamber/blanket) |
| Driver cost (C_d = gamma × E_d) | gamma, E_d, N_d | CAS22.1.3 (driver) |
| Target cost (delta per shot) | delta | CAS22.1.8 (target factory) |
| O&M cost (epsilon × P_e/yr) | epsilon | Operations (not CAS capital) |

> Source: `knowledge/sources/a_simplified_economic_model_for_inertial_fusion/output.md`
> Ref: Equations 1–6 (cost decomposition)
> Basis: Hawker 2020 cost category → CAS mapping

#### MR-WI007-8: Hawker Parameter Binding

The model SHALL bind each of the 14 Hawker parameters to the subsystem that physically governs it:

| Parameter | Symbol | Bound To |
|-----------|--------|----------|
| Availability | mu_a | Plant operations |
| Blanket energy multiple | E_b | Reaction chamber |
| Discount rate | d | Plant financial |
| Driver cost constant | gamma | Driver |
| Driver efficiency | eta / mu_d | Driver |
| Driver energy | E_d | Driver |
| Driver lifetime | N_d | Driver |
| Frequency | f | Plant operations |
| Gain | G | Target / physics |
| O&M cost constant | epsilon | Plant operations |
| Plant cost constant | alpha | Balance of plant |
| Target cost constant | delta | Target factory |
| Thermal efficiency | mu_th | Power conversion (CAS23) |
| Yield cost constant | beta | Reaction chamber |

- **Type**: Functional
- **Priority**: Should
- **Derives from**: DI-005, Hawker 2020
- **Validation**: Each parameter traces to a specific subsystem or plant-level context

### Quality

#### MR-WI007-9: Traceable Citations

All quantitative values SHALL carry structured citations per MR-4 (Source/Ref/Basis in doc comments). Structural decisions (e.g., which CAS sub-accounts apply, chamber wall types) SHALL cite their source.

- **Type**: Quality
- **Priority**: Must
- **Derives from**: MR-4, PR-5
- **Validation**: Every numeric literal and structural choice has a citation; no unattributed values

#### MR-WI007-10: Driver-Agnostic Abstraction

The model SHALL NOT contain driver-type-specific parameter values (no HIF, laser, or pulser specifics). All driver specialization is deferred to WI-008 and future items.

- **Type**: Quality
- **Priority**: Must
- **Derives from**: Epic Item 2 ("driver-agnostic IFE plant model")
- **Validation**: Review — no references to specific driver types in parameter values or defaults

### Constraint

#### MR-WI007-11: Design Location

All files SHALL reside in `models/designs/generic_ife/`.

- **Type**: Constraint
- **Derives from**: MR-3, project structure

#### MR-WI007-12: Library Import Without Modification

The model SHALL import from `models/library/` without modifying any library files.

- **Type**: Constraint
- **Derives from**: MR-3

#### MR-WI007-13: Parse Validation

All model files SHALL pass syside validation (Level 1 — zero parse errors).

- **Type**: Constraint
- **Priority**: Must
- **Derives from**: Epic success criteria
- **Validation**: `uv run syside check models/designs/generic_ife/*.sysml` — zero errors (SV-010)

## Scope Boundaries

### In Scope

- `models/designs/generic_ife/` — all model files for the generic IFE concept
- Top-level IFE power plant assembly with composed subsystems
- Abstract driver interface (4 parameters, no driver-specific values)
- Target factory as operating cost subsystem
- Reaction chamber with wall type classification
- CAS22 level 3 sub-accounts (22.1.1, 22.1.2, 22.1.3, 22.1.5, 22.1.8)
- Power balance integration with library's fusion cycle calcs
- Cost rollup through CAS to LCOE using library's calc
- SV-006 through SV-010 entries in VALIDATION_MATRIX.md

### Out of Scope

- Driver-specific parameter values or cost formulas (WI-008)
- HIF, laser, or pulser instantiations (WI-008 and future)
- CAS22 sub-accounts not needed for the generic model (22.1.4, 22.1.6, 22.1.7, 22.1.9, 22.1.11)
- Monte Carlo simulation or parametric sweeps (analysis phase)
- Modifications to library files (WI-006 output is consumed, not changed)
- Shared CAS element detail (CAS23 turbine internals, CAS24 electrical detail)
- MFE-specific structures

## Success Criteria

### Functional

- IFE power plant assembly exists with all required subsystems composed and CAS-mapped
- Driver interface is abstract with eta, gamma, E_d, N_d as typed attributes
- Target factory models per-shot operating cost separate from capital
- Chamber has wall type enum (dry/wetted/liquid) and blanket energy multiple
- CAS22 disaggregated to level 3 with shared/divergent classification
- Power balance uses library's recirculating power fraction and viability constraint
- LCOE calc produces output via library's `IFE LCOE` with all 14 parameters bound

### Quality

- Every quantitative value and structural decision carries Source/Ref/Basis citation
- No driver-type-specific values anywhere in the model
- All files parse cleanly with `uv run syside check`

### Verification

- SV-006 through SV-010 registered in VALIDATION_MATRIX.md
- SV-008 (LCOE reasonableness): default parameters produce $25–120/MWh

## Assumptions & Risks

| # | Assumption/Risk | Type | Confidence/Likelihood | Impact | Mitigation |
|---|----------------|------|----------------------|--------|------------|
| A1 | WI-006 library definitions are stable and sufficient for the design layer | Assumption | High — WI-006 is in implementation | Low if wrong — library can be extended | |
| A2 | Hawker's 5 cost categories map cleanly to CAS sub-accounts | Assumption | Medium — Hawker's model is aggregate, CAS is granular | Medium — mapping may be approximate | Document mapping rationale; refine in WI-008 if needed |
| A3 | Five CAS22 sub-accounts (22.1.1, .2, .3, .5, .8) are sufficient for the generic model | Assumption | High — covers the primary IFE-divergent structure | Low — additional sub-accounts can be added per-concept | |
| R1 | SysML abstract part defs may not express the driver interface cleanly for downstream specialization | Risk | Medium | Medium — may need workaround patterns | Prototype driver → HIF specialization pattern during design |
| R2 | Parameter binding (14 params → subsystems → LCOE calc) may be complex to express in SysML | Risk | Medium | Medium — could require intermediate binding elements | Design phase should prototype the binding pattern |
| R3 | LCOE validation against $25–120/MWh depends on default parameters being consistent | Risk | Low | Low — defaults come from Hawker | Use Hawker's exact defaults from WI-006 |

## Traceability

### Source Requirements

| Source | What it provides | Requirements served |
|--------|-----------------|-------------------|
| `knowledge/sources/energy_from_inertial_fusion/output.md` | IFE process chain, chamber concepts (dry/wet/liquid), subsystem identification | MR-WI007-1, MR-WI007-4 |
| `knowledge/sources/aries_cost_account_documentation/output.md` | CAS22 sub-account definitions, shared/divergent classification | MR-WI007-5 |
| `knowledge/sources/a_simplified_economic_model_for_inertial_fusion/output.md` | Hawker's cost categories, parameter-to-subsystem mapping, LCOE formula | MR-WI007-7, MR-WI007-8 |
| `/home/reid/PyFECONS` | IFE module structure — driver/chamber/target factory as Union types in CAS22 | MR-WI007-1, MR-WI007-5 |

### Downstream Impacts

- WI-008 (HIF Concept Instantiation) specializes the abstract driver with HIF-specific parameters
- Future laser/pulser concept items specialize the same driver interface
- Cross-concept comparison (OVERVIEW.md comparison axes) consumes LCOE and CAS cost outputs

### Applicable Project Requirements

- MR-1: CAS hierarchy as primary cost decomposition
- MR-2: Standard costed component interface (inherited via library)
- MR-3: Library concept-agnostic, designs concept-specific
- MR-4: Traceable citations on all quantitative values
- MR-5: Standard output schema for cross-concept comparison (LCOE output)
- MR-6: Modeling patterns — this item validates the library patterns established in WI-006

## Related Artifacts

- **Epic**: `work/backlog/epic-ife-cost-modeling.md`
- **Predecessor**: `work/active/WI-006_ife-cost-structure-library/` (library definitions consumed)
- **Research**: `knowledge/research/approved/20260302-165055_ife-system-modeling-first-pass.md`
- **Design**: `work/active/WI-007_generic-ife-concept-model/design.md` (to be created)
- **Plan**: `work/active/WI-007_generic-ife-concept-model/plan.md` (to be created)
