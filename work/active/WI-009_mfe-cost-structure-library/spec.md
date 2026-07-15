---
Status: active
Scale: standard
Epic: MFE Cost Modeling — Tokamak & Stellarator
Owner: reid
Created: 2026-07-03
Updated: 2026-07-13
---

# WI-009: MFE Cost Structure Library

## Overview

Define the reusable, concept-agnostic library primitives for magnetic-fusion (MFE) economic modeling: a magnet/coil system as a costed component, the MFE-divergent CAS22 sub-account types, a plasma scaling calc that derives fusion power from physical machine parameters, the MFE power balance calc, magnet cost scaling, and MFE viability constraints. This is the foundation layer for the MFE epic — WI-010 (Generic MFE Plant Model) and WI-011 (Tokamak & Stellarator Instantiations) import from these definitions, and WI-012 runs `sysml-codegen` over them.

## Goals & Context

**Research questions served**:
- RQ-1: Dominant cost drivers by approach — the magnet system is the MFE analogue of the IFE driver; this item defines it as the dominant CAS22 component.
- RQ-2: Credible LCOE ranges — the power balance and cost primitives feed the LCOE calc reused from the IFE library.
- RQ-3: Shared vs. divergent structure — the MFE CAS22 sub-accounts + `mfe_divergent` scope directly encode where MFE diverges from IFE (DI-002).

**Domain insights applied**:
- DI-002: CAS22 is the IFE-MFE divergence point (22.1.3 magnets, 22.1.4 heating/current-drive, 22.1.8 divertor) → MR-WI009-4, MR-WI009-6.

**Epic context**: First item in a strictly sequential chain (WI-009 → WI-010 → WI-011 → WI-012). Reuses the IFE library (`costed_component`, `cas_hierarchy` CAS20–90, `economic_parameter`, `ife_lcoe`) unchanged except for one additive enum member. Pattern-defining for all MFE work (MR-6): the conventions for magnet costing, physical parameterization, and MFE viability established here become the template for WI-010/011.

**Two scoping decisions locked with the user (2026-07-03)**:
1. The magnet system definition and MFE CAS22 sub-account *types* live in the **library** (this item), per MR-3's explicit "a magnet system definition works for any MFE concept" example — not in the design layer where IFE placed its subsystem types. This is a deliberate, more MR-3-consistent choice than the IFE precedent; register as an AD during implementation.
2. Fusion **power is a derived output**, not a free input. The library derives it from physical machine parameters (major radius R, field B, plasma performance), so a downstream sweep over physical parameters (R, B, plasma gain, availability) propagates through to net electric power and LCOE. This is what makes WI-012's viability sweep physical rather than a sweep of abstract cost knobs.

## Current State

The IFE library exists and is reused as-is:
- `models/library/foundation/costed_component.sysml` — `'Costed Component'` (capital_cost, cas_code).
- `models/library/foundation/economic_parameter.sysml` — `'Economic Parameter'`, `'CAS Scope'` enum (currently two members: `shared`, `ife_divergent`).
- `models/library/cost_structure/cas_hierarchy.sysml` — `'CAS Account'` + CAS20–27, CAS90. `'CAS22 Power Core'` already documents the MFE side of the 22.1.x divergence.
- `models/library/analyses/ife_lcoe.sysml` — `'IFE LCOE'` closed-form DCF calc (most parameters technology-agnostic; reused for MFE LCOE).

No MFE definitions exist in the active tree. The archived MFE power balance is a strong revival base:
- `archive/models/library/calculations/power_balance/mfe_power_balance.sysml` — `'MFE Power Balance Calc'`, 16 inputs, computes thermal/recirculating/net-electric power, engineering Q (`q_eng`), and recirculating fraction (`rec_frac`). Ported from PyFECONS `PowerBalance.py`. Takes fusion power (`p_nrl`) and heating power (`p_input`) as inputs; depends on archived `'Alpha Power Calc'` and `FuelType`.

## Modeling Requirements

### Functional

#### MR-WI009-1: MFE Power Balance Calc

The library SHALL provide an MFE power balance calc that takes fusion power, plasma heating power, and the coil/cooling/auxiliary/efficiency parameters, and produces net electric power, engineering Q, and recirculating power fraction.

- **Type**: Functional
- **Priority**: Must
- **Derives from**: RQ-1, RQ-2; revives `archive/.../mfe_power_balance.sysml`
- **Validation**: Calc produces net electric power, `q_eng`, and `rec_frac` for a reference MFE design point in a physically sensible range (SV-016)

Revive and adapt `'MFE Power Balance Calc'`. The archived `'Alpha Power Calc'`/`FuelType` dependency is replaced by an inlined D-T alpha fraction (α ≈ 1/5 of fusion power to alphas, 4/5 to neutrons) — a documented simplification, resolved in design.

> Source: `/home/reid/PyFECONS/pyfecons/costing/mfe/PowerBalance.py`
> Ref: PowerBalance.py:8-50
> Basis: MFE power flow (thermal, recirculating, net electric, engineering Q) for tokamaks and stellarators

#### MR-WI009-2: Plasma Scaling — Fusion Power from Physical Parameters

The library SHALL provide a plasma scaling calc that derives fusion power from physical machine parameters, at minimum major radius R and magnetic field B, so that fusion power is a computed output rather than a free input.

- **Type**: Functional
- **Priority**: Must
- **Derives from**: RQ-1; user decision 2 (physical parameterization)
- **Validation**: Fusion power increases with B and with R in the physically expected direction (SV-017)

The scaling relation and its source are pinned in design (candidate: fusion power ∝ (βB²)²·volume with volume ∝ R³, from an ARIES/systems-code scaling). The requirement here is the capability: R and B drive fusion power. Combined with plasma gain (Q = fusion/heating power) and availability, this exposes the four intended WI-012 sweep axes so they propagate to net electric power and LCOE.

> Source: `knowledge/sources/tea_dt_mfe_cost_analysis/output.md`, `/home/reid/PyFECONS`
> Ref: [to pin in design — MFE fusion power scaling]
> Basis: MFE-generic engineering scaling of fusion power with size and field

#### MR-WI009-3: Magnet Cost Scaling

The library SHALL provide a magnet cost scaling calc that derives magnet/coil capital cost from coil geometry and field, concept-agnostic across MFE approaches.

- **Type**: Functional
- **Priority**: Must
- **Derives from**: RQ-1 (magnet is the dominant MFE cost driver)
- **Validation**: Magnet cost increases with R and B in the expected direction (SV-018)

> Source: `/home/reid/PyFECONS` (CAS220103 magnet costing), `knowledge/sources/tea_dt_mfe_cost_analysis/output.md`
> Ref: [to pin in design]
> Basis: Superconducting magnet cost scaling with conductor/stored-energy, applicable to any MFE coil set

#### MR-WI009-4: Magnet System Costed Component + MFE CAS22 Sub-Account Types

The library SHALL define the MFE-divergent CAS22 sub-account types — `'CAS22.1.3 Magnet System'`, `'CAS22.1.4 Heating and Current Drive'`, `'CAS22.1.8 Divertor'` — each specializing `'CAS22 Power Core'` with `scope = mfe_divergent`, and a concept-agnostic `'Magnet System'` costed component specializing `'CAS22.1.3 Magnet System'`.

- **Type**: Functional
- **Priority**: Must
- **Derives from**: DI-002, MR-1, MR-2, MR-3
- **Validation**: Specialization chain resolves (`'Magnet System'` → CAS22.1.3 → CAS22 Power Core → CAS Account → Costed Component) (SV-022)

The `'Magnet System'` carries `capital_cost` (from MR-WI009-3) and is parameterized, not fixed — no tokamak- or stellarator-specific values (those are set in WI-011).

> Source: `knowledge/sources/aries_cost_account_documentation/output.md`
> Ref: L1005-1008 (CAS22 divergence)
> Basis: DI-002 — MFE CAS22 sub-accounts mirror the IFE ones by function

#### MR-WI009-5: MFE Viability Constraints

The library SHALL define MFE viability constraint(s) as `constraint def`(s): at minimum, net electric power > 0 (equivalently engineering Q > 1), and a recirculating-power-fraction bound as an adjustable, documented economic threshold.

- **Type**: Functional
- **Priority**: Must
- **Derives from**: RQ-1; mirrors the IFE `'Viability Threshold'` pattern (`fusion_cycle.sysml`)
- **Validation**: Constraint expressions present and evaluable; net-electric-positive check evaluates true/false correctly (SV-019)

Net-electric > 0 is a hard physics constraint (unambiguous). The tighter economic recirc knee needs a source basis (ARIES/PyFECONS), pinned in design; it is a parameterized threshold, not a magic number.

> Source: `/home/reid/PyFECONS`, `knowledge/sources/aries_cost_account_documentation/output.md`
> Ref: [economic recirc threshold — pin in design]
> Basis: Net electric > 0 is physics-hard; economic threshold is a documented, adjustable parameter

#### MR-WI009-6: CAS Scope Extension

The library SHALL extend the `'CAS Scope'` enum with an `mfe_divergent` member, additively, leaving existing IFE models unaffected.

- **Type**: Functional
- **Priority**: Must
- **Derives from**: DI-002
- **Validation**: `'CAS Scope'` has three members; IFE models still parse (SV-020)

### Quality

#### MR-WI009-7: Traceable Citations

All quantitative values (scaling coefficients, cost constants, thresholds) SHALL carry structured Source/Ref/Basis citations per MR-4.

- **Type**: Quality
- **Priority**: Must
- **Derives from**: MR-4, PR-5
- **Validation**: No unattributed numeric literals

#### MR-WI009-8: Concept-Agnostic Definitions

All definitions SHALL be concept-agnostic — no tokamak- or stellarator-specific values, geometries, or costs. Only parameterization and scaling forms belong here; concept values are set in WI-011.

- **Type**: Quality
- **Priority**: Must
- **Derives from**: MR-3
- **Validation**: Review — no concept-specific literals (no ARC/CFS/Type One numbers) in library files

#### MR-WI009-9: IFE Reuse Preserved

The change to `'CAS Scope'` and the shared CAS accounts SHALL NOT alter behavior of the existing IFE models; the shared CAS20–90 accounts and `'IFE LCOE'` calc are reused, not re-authored.

- **Type**: Quality
- **Priority**: Must
- **Derives from**: MR-3, epic reuse goal
- **Validation**: IFE library + design files parse cleanly after the enum change (SV-020)

### Constraint

#### MR-WI009-10: Library Location

All new files SHALL reside in `models/library/` under the existing subdirectory scheme (`cost_structure/`, `analyses/`) per AD-004.

- **Derives from**: MR-3, AD-004

#### MR-WI009-11: Parse Validation

All model files SHALL pass syside validation (Level 1 — parse without errors).

- **Priority**: Must
- **Derives from**: epic success criteria
- **Validation**: `uv run syside check models/library/**/*.sysml` — zero errors (SV-021)

#### MR-WI009-12: Codegen-Compatible Constructs

Calc and constraint defs SHALL stay within the SysML construct set that `sysml-codegen` supports (as exercised by the IFE calc defs and the codegen demos), so WI-012 can generate Python from them without model rework.

- **Type**: Constraint
- **Priority**: Should
- **Derives from**: WI-012 dependency; MR-6
- **Validation**: Constructs match those already proven codegen-friendly; any gap is recorded as a `sysml-codegen` finding, not worked around in the model
- **Flag for promotion**: Candidate PR-XXX — "MFE/library calc defs must remain codegen-compatible" — if it holds up through WI-012.

## Scope Boundaries

### In Scope

- `models/library/foundation/economic_parameter.sysml` — add `mfe_divergent` to `'CAS Scope'` (edit)
- `models/library/cost_structure/` — MFE CAS22 sub-account types + `'Magnet System'` costed component (new file, e.g. `mfe_power_core.sysml`)
- `models/library/analyses/mfe_power_balance.sysml` — revived MFE power balance calc
- `models/library/analyses/mfe_plasma_scaling.sysml` — fusion power from R, B, plasma params
- `models/library/analyses/mfe_magnet_cost.sysml` — magnet cost scaling
- `models/library/analyses/mfe_viability.sysml` — MFE viability constraint(s)
- SV-016 through SV-022 in VALIDATION_MATRIX.md
- One AD registering the "magnet system in library" decision

Exact file grouping is a design choice (some of the analyses files may merge); the requirement is the definitions, not the file count.

### Out of Scope

- The generic MFE plant assembly that composes these and binds the calcs (WI-010)
- Tokamak/stellarator-specific parameter values, coil topologies, current-drive presence (WI-011)
- Running `sysml-codegen` and the viability sweep harness (WI-012)
- Direct energy conversion in the power balance (deferred, as in the archived calc)
- Modifying the IFE LCOE calc or shared CAS accounts beyond the additive enum member
- A formal written pattern document — patterns are implicit in the SysML, as with WI-006

## Success Criteria

### Functional

- MFE power balance calc produces net electric power, engineering Q, and recirculating fraction
- Fusion power is derived from R and B (a computed output, not a free input)
- Magnet cost is derived from coil geometry and field
- MFE CAS22 sub-account types and `'Magnet System'` exist with the correct specialization chain and `mfe_divergent` scope
- MFE viability constraint(s) present and evaluable
- `'CAS Scope'` has an `mfe_divergent` member

### Quality

- Every quantitative value carries a Source/Ref/Basis citation
- No concept-specific values anywhere in library definitions
- IFE library and design files parse cleanly after the enum change
- All new files parse cleanly with `uv run syside check`

### Verification

- SV-016 through SV-022 registered in VALIDATION_MATRIX.md (status `pending` until implementation)

## Assumptions & Risks

| # | Assumption/Risk | Type | Confidence/Likelihood | Impact | Mitigation |
|---|----------------|------|----------------------|--------|------------|
| A1 | A defensible MFE-generic fusion-power scaling (R, B → P_fus) exists in PyFECONS/ARIES at the fidelity a TEA needs | Assumption | Medium | Medium — sweep axes depend on it | Pin the relation + source in design; keep it simple and cited |
| A2 | The archived power balance revives cleanly once `'Alpha Power Calc'`/`FuelType` are inlined | Assumption | High | Low | Inline D-T alpha fraction; validate against a reference design point |
| R1 | WI-009 is on the larger side (physics scaling + power balance + magnet cost + structure) | Risk | Medium | Low | If design shows it's too big, split the physics scaling into its own item |
| R2 | `sysml-codegen` may not support a construct used in the physics/cost calcs | Risk | Medium | Medium | MR-WI009-12: stay within proven constructs; treat gaps as codegen-repo findings (surfaces in WI-012, not here) |
| R3 | The economic recirc-power viability threshold lacks a single authoritative value | Risk | Medium | Low | Net-electric>0 is unambiguous; make the economic threshold a documented, adjustable parameter |

## Traceability

### Source Requirements

| Source | What it provides | Requirements served |
|--------|-----------------|-------------------|
| `/home/reid/PyFECONS` | MFE power balance, magnet costing (CAS220103), engineering Q | MR-WI009-1, MR-WI009-3, MR-WI009-5 |
| `knowledge/sources/tea_dt_mfe_cost_analysis/output.md` | MFE cost breakdowns, magnet cost scaling, fusion power scaling | MR-WI009-2, MR-WI009-3 |
| `knowledge/sources/aries_cost_account_documentation/output.md` | CAS structure, CAS22 divergence, scope classification | MR-WI009-4, MR-WI009-5, MR-WI009-6 |

### Downstream Impacts

- WI-010 (Generic MFE Plant Model) composes the magnet system, CAS22 sub-accounts, and binds the power balance / scaling / LCOE calcs
- WI-011 (Tokamak & Stellarator Instantiations) sets concept-specific values on these parameterized types
- WI-012 (Codegen + Viability Sweep) runs `sysml-codegen` over these calcs/constraints and sweeps R, B, plasma gain, availability

### Applicable Project Requirements

- MR-1 (CAS as primary decomposition), MR-2 (costed component interface), MR-3 (library concept-agnostic), MR-4 (traceable citations), MR-6 (patterns before production models)
- AD-001 (plain Real), AD-004 (library subdirectories), AD-005 (CAS as typed part defs), AD-006 (parameters separate from calculation)
- PR-5 (committed artifacts at every phase)

## Related Artifacts

- **Epic**: `work/backlog/epic-mfe-cost-modeling.md`
- **Revival base**: `archive/models/library/calculations/power_balance/mfe_power_balance.sysml`
- **IFE precedent**: `work/completed/20260302_WI-006_ife-cost-structure-library/spec.md`
- **Design**: `work/active/WI-009_mfe-cost-structure-library/design.md` (to be created)
- **Plan**: `work/active/WI-009_mfe-cost-structure-library/plan.md` (to be created)
