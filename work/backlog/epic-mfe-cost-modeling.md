---
Status: draft
Priority: P0
Created: 2026-07-03
Updated: 2026-07-03
---

# Epic: MFE Cost Modeling — Tokamak & Stellarator

## Executive Summary

Build the magnetic-fusion (MFE) half of the cross-concept comparison as a self-contained SysML vertical slice, and use it to prove three capabilities end-to-end on a single model: the **costed-component pattern**, the **full codegen process** (SysML → executable Python), and a **constraint-based viability sweep** over the input space.

The slice mirrors the completed IFE Cost Modeling epic (WI-006/007/008): a concept-agnostic library, a generic plant model, concrete instantiations, and — new to this epic — a codegen-and-sweep item that closes a loop the project has never closed before. Today `sysml-codegen` has only ever run on demo models, and no fusion `.sysml` has been turned into executable code. This epic takes the tokamak/stellarator models the whole way through.

The tokamak/stellarator pair is deliberate. They share nearly every subsystem — blanket, balance-of-plant, thermal conversion, buildings, indirect costs — and diverge in essentially one place: the magnet/coil system and current drive. That contrast is the cleanest possible demonstration of MR-3 reuse (library concept-agnostic, designs concept-specific) and of the CAS22 divergence identified in DI-002.

**Critical success factor**: A tokamak and a stellarator model that (a) reuse the shared IFE library CAS accounts and LCOE calc unchanged, (b) differ only in their magnet/current-drive subsystems, and (c) flow through `sysml-codegen` into a Python `forward()` plus constraint predicates that a standalone sweep harness uses to map the viable region of the input space.

---

## Context

**What exists.** The IFE epic established the full modeling idiom and a reusable spine:
- `'Costed Component'` interface (`models/library/foundation/costed_component.sysml`) — MR-2.
- CAS hierarchy as typed part defs (`models/library/cost_structure/cas_hierarchy.sysml`), AD-005 — with a `'CAS Scope'` enum (`shared` / `ife_divergent`) that was designed from the start to receive an MFE branch.
- A closed-form DCF LCOE calc (`models/library/analyses/ife_lcoe.sysml`), AD-003 — most of its 14 parameters are technology-agnostic and reusable for MFE.
- The viability-constraint pattern (`models/library/analyses/fusion_cycle.sysml`) — a `constraint def` asserted by the plant. This is the seed for MFE viability.

**What this epic adds.** The MFE-specific structure: the magnet/coil system as the dominant CAS22 cost driver, the MFE-divergent CAS22 sub-accounts, an MFE power-balance calc, MFE viability constraints, and the two instantiations — then the codegen and sweep.

**Load-bearing domain insight.** DI-002: the CAS framework (20–99) is universal across fusion approaches. MFE and IFE share CAS20–21, 23–27, and 91–99. All divergence concentrates in CAS22 sub-accounts — 22.1.3 (magnets ↔ driver), 22.1.4 (heating/current-drive ↔ ignition), 22.1.8 (divertor ↔ target factory). This tells us exactly which library elements are reused and which are new.

**Research questions served.** RQ-1 (MFE cost drivers — the magnet system), RQ-2 (credible MFE LCOE range and its assumptions), RQ-3 (shared vs. divergent structure — this epic *is* the MFE side that makes cross-concept comparison real).

**Architectural constraints (must respect).** AD-001 (plain `Real`, units in doc comments), AD-002 (`'Economic Parameter'` attribute def for parameter metadata), AD-003 (closed-form DCF), AD-004 (library subdirectory organization: `foundation/`, `cost_structure/`, `analyses/`), AD-005 (CAS accounts as typed part def specializations of `'Costed Component'`), AD-006 (parameters separate from calculation).

---

## Authority Source Dependencies

| Source | Use For | Items | Status |
|--------|---------|-------|--------|
| ARIES Cost Account Documentation | CAS hierarchy, MFE direct/indirect accounts, escalation/contingency conventions | 1, 3 | Ingested |
| TEA D-T MFE Cost Analysis | MFE CAS cost breakdowns, LCOE calculation approach, plant economics | 1, 3 | Ingested |
| PyFECONS | MFE power-balance model, CAS22 magnet costing, engineering Q | 1, 3 | Available (external codebase) |
| Helios stellarator design | Stellarator plant architecture (steady-state, thick shield, sector maintenance); reference for stellarator subsystem assumptions | 3 (stellarator) | Ingested |
| Concept 01 research dossier (HTS compact tokamak) | Tokamak instantiation parameters — HTS TF coils, high field, compact geometry | 3 (tokamak) | Available (concept_research) |
| `sysml-codegen` | SysML → Python code generation | 4 | Available (external codebase, editable dep) |

**Source gap to resolve in Item 3 spec**: the user's target stellarator is the modular-HTS-coil type (Type One). The ingested stellarator source (Helios) is a *planar-coil* design — a valid stellarator power-plant reference, but not the same coil topology. Item 3's spec must confirm whether Type-One-specific coil and cost numbers are available in the concept dossier, or whether Helios stands in as the stellarator architecture reference with a documented basis. Do not invent stellarator coil costs — surface the gap.

---

## Success Criteria

- [ ] Magnet/coil system modeled as a `'Costed Component'`, reading as the dominant CAS22 cost driver (RQ-1)
- [ ] MFE-divergent CAS22 sub-accounts (magnets 22.1.3, heating/current-drive 22.1.4, divertor 22.1.8) specialize the shared CAS accounts; CAS20–21, 23–27, 90 reused unchanged from the IFE library (MR-3 reuse demonstrated, not re-authored)
- [ ] MFE power-balance calc produces net electric power and engineering Q
- [ ] Viability expressed as SysML `constraint def`s (at minimum: net electric power > 0; recirculating-power fraction bounded)
- [ ] Tokamak and stellarator instantiations differ **only** in the magnet/current-drive subsystems; every other subsystem is inherited
- [ ] LCOE output within a credible MFE range cross-checked against ARIES / TEA-D-T-MFE
- [ ] `sysml-codegen` produces a Python `forward()` plus evaluable constraint predicates from the MFE models
- [ ] A self-contained sweep harness varies R, B, plasma gain, and availability and partitions the input grid into constraint-satisfying (viable) vs. constraint-violating (non-viable) regions, with the feasible boundary visualized
- [ ] Every quantitative value carries an MR-4 `Source / Ref / Basis` citation
- [ ] Models pass validation Levels 1–3

---

## Items

### Item 1: MFE Cost Structure Library

**Scale**: standard
**Dependencies**: None (reuses the existing IFE library; does not modify it beyond an additive enum member)

**Scope**: The concept-agnostic MFE building blocks. Magnet/coil system costed-component types, the MFE-divergent CAS22 sub-account specializations (per DI-002), an MFE power-balance calc def (revive and adapt the archived PyFECONS-derived `mfe_power_balance.sysml`), and the MFE viability constraint(s). Extend `'CAS Scope'` with an `mfe_divergent` member — an additive change that leaves existing IFE models untouched. Everything here stays confinement-agnostic (MR-3): no tokamak-vs-stellarator specifics.

**Key requirements**:
- [ ] Magnet/coil system as `'Costed Component'` with cost attributes sufficient for CAS22 rollup
- [ ] CAS22 MFE sub-accounts (22.1.3 magnets, 22.1.4 heating/current-drive, 22.1.8 divertor) specializing the shared CAS22 account
- [ ] MFE power-balance calc def: gross/net electric, recirculating power, engineering Q (adapted from PyFECONS)
- [ ] Viability `constraint def`(s): net electric > 0, recirculating-power fraction bound
- [ ] `'CAS Scope'` extended with `mfe_divergent`; IFE models unaffected

**Deliverables**: `models/library/cost_structure/` (MFE CAS sub-accounts, magnet system types), `models/library/analyses/mfe_power_balance.sysml`, `models/library/analyses/mfe_viability.sysml`

---

### Item 2: Generic MFE Plant Model

**Scale**: standard
**Dependencies**: Item 1

**Scope**: A confinement-agnostic MFE plant that composes the subsystems and wires the calculations — the direct analogue of `ife_plant.sysml`. Composes an abstract magnet/coil system, heating/current-drive, first-wall/blanket, divertor, vacuum, and the shared balance-of-plant. Binds the MFE power balance and the (largely reused) LCOE calc, and asserts the viability constraints. The magnet/coil system is an **abstract** interface here; the tokamak and stellarator specialize it in Item 3.

**Key requirements**:
- [ ] Composes MFE subsystems with abstract magnet/coil and current-drive interfaces
- [ ] Reuses shared CAS20–21, 23–27, 90 accounts and the LCOE calc from the IFE library
- [ ] Binds MFE power balance; exposes net electric power and LCOE as derived attributes
- [ ] Asserts the Item 1 viability constraints
- [ ] LCOE within a credible MFE range for default parameters

**Deliverables**: `models/designs/generic_mfe/` — subsystem definitions and the plant assembly

---

### Item 3: Tokamak & Stellarator Instantiations

**Scale**: standard
**Dependencies**: Item 2

**Scope**: Two concrete leaf designs that specialize the generic MFE plant, kept in one item **because their contrast is the deliverable**. The tokamak (HTS compact, concept 01) uses HTS toroidal-field coils, external current drive, and high field. The stellarator (modular HTS, Type One) uses 3-D modular coils and no current drive (steady-state by design). Everything outside the magnet/current-drive subsystems is inherited from Item 2 unchanged — the diff between the two designs should be almost entirely the coil system. Validate each LCOE against ARIES / TEA-D-T-MFE, and the stellarator subsystem assumptions against Helios.

**Key requirements**:
- [ ] Tokamak: HTS TF coil system + external current-drive subsystem, high-field compact parameters from the concept 01 dossier
- [ ] Stellarator: modular-HTS coil system, current-drive subsystem removed/zeroed, steady-state operation
- [ ] The only structural divergence between the two is the magnet/current-drive subsystems (MR-3 demonstration)
- [ ] Each concept's LCOE cross-checked against an MFE reference; sources cited per MR-4
- [ ] Stellarator coil/cost basis documented (see the Item 3 source gap above)

**Deliverables**: `models/designs/hts_tokamak/`, `models/designs/hts_stellarator/`, and a short validation note comparing each LCOE to its reference

---

### Item 4: Codegen + Viability Sweep

**Scale**: standard
**Dependencies**: Items 1–3 (the models must exist)

**Scope**: The end-to-end demonstration. Run `sysml-codegen` over the MFE library and designs to emit a Python `forward()` and evaluable constraint predicates. Then build a **self-contained** sweep harness (no 1costingfe): grid over R, B, plasma gain, and availability; evaluate each grid point through the generated `forward()` and the emitted constraints; classify each point as viable (violates no constraint) or non-viable; visualize the feasible region and the viability knee. This is the item most likely to hit unknowns — see Risks.

**Key requirements**:
- [ ] `sysml-codegen` runs over the MFE models and emits Python (`forward()` + constraint predicates)
- [ ] Sweep harness varies R, B, plasma gain, availability across a grid
- [ ] Each grid point classified viable/non-viable by whether it violates any emitted constraint
- [ ] Feasible region and knee visualized; output committed
- [ ] Harness is standalone — no dependency on 1costingfe or the hosted concept_explorer

**Deliverables**: `generated/mfe/` (codegen output), a sweep script + viability visualization committed under `exploration/` or `data/`

---

## Sequencing

```
Item 1: MFE Cost Structure Library (reuses IFE library)
  └─> Item 2: Generic MFE Plant Model
       └─> Item 3: Tokamak & Stellarator Instantiations
            └─> Item 4: Codegen + Viability Sweep
```

Strictly sequential — each item builds on the previous. The critical path is all four. Items 1–3 follow the proven IFE pattern and carry low execution risk; Item 4 is where the novel, higher-risk work concentrates.

---

## Risks

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| `sysml-codegen` doesn't support every construct used in the MFE models (Item 4) | Medium | Medium | Keep MFE calc/constraint defs within the construct set already proven codegen-friendly by the IFE calc defs and the `solar_battery` / chain-spike demos. Where a construct is unsupported, that's a finding to feed back to the `sysml-codegen` repo, not a workaround in the model. |
| Type One (modular-HTS) stellarator cost/coil data is thin in the corpus; Helios is planar-coil | Medium | Medium | Resolve in the Item 3 spec: confirm concept-dossier coverage or document Helios as the stellarator architecture reference with an explicit basis. Do not invent coil costs. |
| MFE economic viability threshold (what makes a design non-viable) needs a defensible definition | Low | Medium | Anchor on net-electric > 0 and the recirculating-power knee, cited to PyFECONS/ARIES; keep the threshold a documented, adjustable parameter, not a magic number. |
| Extending `'CAS Scope'` touches the shared library and could disturb IFE models | Low | Low | Additive enum member only; IFE models don't reference `mfe_divergent`. Re-run IFE validation after the change. |

---

## Deferred Decisions (revisit)

- **Material shape factor on conformal subsystem volumes** — deferred by owner ruling 2026-07-17 (WI-021 checkpoint). WI-021 forward-computes the CAS22 material volumes (blanket/shield/structure/vessel), first-wall area, and coil-bore radius as **pure torus shells with no shape factor**, matching 1costingFE (Option 1). The alternative (Option 2) would apply a stellarator shaping factor to these engineered annuli — a blanket/shield conforming to a shaped plasma encloses less than a full torus shell, which would reduce the volume-scaled costs. Deferred because it deviates from the admissible engineering source (1costingFE, which uses torus shells) and needs a defensible per-layer factor the current sources do not provide. Revisit if a sourced conformal-volume basis becomes available or the hold-out comparison motivates it. Scope if picked up: re-baselines the four CAS22 volume-scaled costs and LCOE, parallel to WI-020's plasma-volume re-baseline.

---

**Last Updated**: 2026-07-17
**Next Action**: `/spec-model` on Item 1 (MFE Cost Structure Library)
