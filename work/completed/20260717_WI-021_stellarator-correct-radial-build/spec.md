---
Status: completed
Scale: standard
Epic: MFE Cost Modeling — Tokamak & Stellarator
Owner: reid
Created: 2026-07-17
Updated: '2026-07-17'
---

# WI-021: Stellarator-Correct Radial-Build Volumes

**Required Reading: `knowledge/holdout/aries-cs/PROTOCOL.md`** — this is a stellarator-demo model-development item. The ARIES-CS hold-out is sealed; the §3 barred paths must not be read, cited, or opened. Admissible sources for this item: the Stellaris design sources under `knowledge/concept_research/09-qi-stellarator-hts/iter-01..03/sources/**` (minus the barred entries) for geometry inputs, and **1costingFE (pinned `0254385`) for the radial-build formulas** — the radial-build geometry descends from the ARIES/Starfire family, a lineage exception already scoped as admissible in PROTOCOL §3; `compute_geometry` carries no ARIES-CS-specific values.

## Overview

Replace the six injected geometry constants in the concept-09 instance with a **forward-computed radial build** in SysML. Today the subsystem/material volumes, the first-wall area, and the coil-bore radius are hand-copied constants, each cited to `costingfe.layers.geometry.compute_geometry(STELLARATOR)`. This item computes them from `R0`, `a`, elongation, and the radial-build layer thicknesses — cumulative radii → torus-shell volumes → torus surface area — so the whole geometry chain becomes traceable arithmetic instead of magic numbers. Item 1 of the demo-deepening plan (order 3→4→1→2; items 3/WI-019 and 4/WI-020 are done). It precedes item 2 (predictive confinement) because material geometry precedes the physics rework and the two are otherwise independent.

## Goals & Context

**Research questions served**:
- RQ-2 (credible LCOE range): the material volumes drive the four CAS22 volume-scaled cost accounts (blanket, shield, structure, vessel) and — through `r_coil` — the magnet cost. Making them forward-computed removes six unexplained constants from the cost spine and lets a reader see how a change in the radial build moves cost.
- RQ-3 (shared vs. divergent structure): the radial build is a concept-agnostic pattern (torus shells for MFE, sphere shells for IFE); this item builds the MFE-torus branch as a reusable library calc, keeping the concept-divergent part (thicknesses, shape) in the instance.

**Demo context**: The Stage-3 backlog lists these injected volumes as a standing fidelity gap. WI-020 explicitly deferred the first-wall area to "item 1 / radial build" (see the `wall_area` doc note, `stellarator_plant.sysml:507-517`). This item closes that deferral.

**Epic context**: Adds a radial-build calc def to the WI-009 library file (`models/library/analyses/mfe_plasma_scaling.sysml`), threads it through the generic plant (`models/designs/generic_mfe/mfe_plant.sysml`), and wires the computed outputs into the WI-018 concept-09 instance (`models/designs/stellarator_09/stellarator_plant.sysml`).

**Relevant prior insight**: WI-020's `f_shape` gotcha — a defaulted calc-def input does NOT reach the generated pipeline as its default; the snapshot bakes in the **instance** binding. Any new geometry input added here must be handled so the Anchor A handshake stays byte-identical (see MR-WI021-6).

## Current State

Six injected constants in `models/designs/stellarator_09/stellarator_plant.sysml`, each cited to `compute_geometry(STELLARATOR)` at the Stellaris radial build:

| Constant | Line | Value | Aggregation (1costingFE) |
|---|---|---|---|
| `blanket.blanket_vol` | ~145 | 1118.695 | firstwall_vol + blanket_vol + reflector_vol (`model.py:1205`) |
| `shield.shield_vol` | ~158 | 552.140 | ht_shield_vol + lt_shield_vol (`model.py:1206`) |
| `structure.structure_vol` | ~169 | 219.979 | structure_vol (`model.py:1207`) |
| `vessel.vessel_vol` | ~180 | 157.933 | vol(gap1_or, vessel_or) (`model.py:1208`) |
| `wall_area` (instance attr) | ~507 | 802.201 | `_torus_surface_area(R, vacuum_or, kappa)`; feeds `wall_load_calc` |
| `magnet.r_coil` | ~117 | 3.20 | `vessel_or` (radial-build sum); feeds magnet cost |

A seventh value depends on the first: `special_materials_capital = 26289000.0` (line ~445) is the CAS27 PbLi inventory, doc-derived as `blanket_vol × 0.50 × 9400 × 5.0 / 1e6`. It is currently a hardcoded pass-through whose doc references `blanket_vol = 1118.695`.

**How the constants flow**: the four material volumes are `:>> vol = ...` redefinitions inside the `blanket`/`shield`/`structure`/`vessel` parts; the cost calc blocks read them (`blanket_cost` binds `in blanket_vol = blanket.blanket_vol`, etc.). `r_coil` is a magnet-part attribute read by `magnet_cost`. `wall_area` is an instance attribute read by `wall_load_calc`.

**The formulas (1costingFE, admissible)** — `src/costingfe/layers/geometry.py`:
- Cumulative radii (`compute_geometry`, lines 106–118): flat sums of thicknesses from `plasma_or = plasma_t` outward through `vessel_or`, `bioshield_or`.
- `_torus_shell_volume(R, r_in, r_out, kappa)` (lines 67–73): `V = kappa · 2π²·R·(r_out² − r_in²)`.
- `_torus_surface_area(R, a, kappa)` (lines 76–81): `SA = kappa · 4π²·R·a`; `firstwall_area = _torus_surface_area(R, vacuum_or, kappa)`.
- CAS22 aggregation (`model.py:1205–1208`) as in the table above.

Verified: at the Stellaris build (R0=12.7, plasma_t=1.5, elon=1.0; blanket_t=0.80, ht_shield_t=0.20, structure_t=0.15, vessel_t=0.10 from `steady_state_stellarator.yaml:39-42`; the rest from the `RadialBuild` dataclass defaults `geometry.py:19-40`), the formulas reproduce all six constants exactly (e.g. `_torus_surface_area(12.7, 1.60, 1.0) = 802.19`; `vessel_or = 1.5+0.10+0.05+0.80+0.20+0.20+0.15+0.10+0.10 = 3.20`).

## Central Decision — OWNER RULING (2026-07-17)

Surfaced at the mandatory checkpoint; the owner ruled **Option 1** (torus shells, no material shape factor), **yes to all three scope sub-decisions**, and directed that Option 2 be recorded as a deferred item in the parent epic (done: `work/backlog/epic-mfe-cost-modeling.md`, "Deferred Decisions"). Commit cadence: proceed on top of the uncommitted WI-020 state (owner did not require committing WI-020 first). The decision as presented, for the record:

**Does a stellarator shape factor apply to the MATERIAL volumes too?**

WI-020 applied `f_shape = 0.794` to the **plasma** volume (a shaped QI plasma encloses less than its torus). The question here: do the blanket/shield/structure/vessel volumes — and the first-wall area — get a shape factor too?

- **Option 1 (RECOMMENDED): match 1costingFE — pure torus shells, NO shape factor on material volumes.** 1costingFE computes every material volume as a pure torus shell (no `f_shape`); the material layers are engineered annular structures sized by the radial build, not by the plasma's fine cross-section. **Consequence: the six values reproduce the current constants exactly. Costs and LCOE are unchanged.** Item 1 becomes a fidelity/traceability win — six magic numbers become forward-computed arithmetic — not a re-baseline. It also keeps the Anchor A handshake trivially closed (the Stellaris instance's radial-build inputs already ARE 1costingFE's, so the computed volumes equal 1cfe's).
- **Option 2: apply shaping to conformal material volumes.** Physical argument: a blanket/shield conforming to a shaped plasma encloses somewhat less than a full torus shell, so a shape factor would reduce material volumes and drop the volume-scaled costs. **This deviates from 1costingFE** (the admissible engineering source), re-baselines cost/LCOE, and needs a defensible factor per layer — which the source does not give.

**Ruling: Option 1** (torus shells, no material shape factor). Rationale: 1costingFE is the admissible engineering source for the radial build and it uses torus shells; the shaping WI-020 modeled is a plasma-physics effect, and extending it to engineered material annuli is a physical claim the admissible sources do not support. The physical argument for Option 2 is real but sourced only by intuition, so it is deferred (epic "Deferred Decisions"), not adopted.

**The requirements below are written under Option 1** (the ruling). Option 2 is recorded in the parent epic for later revisit.

### Scope sub-decisions — OWNER: yes to all three

- **(a) Include `wall_area`** via `_torus_surface_area`? **Yes** — it is the same radial build and feeds `wall_load_ok`; leaving it a constant while everything around it is computed is inconsistent.
- **(b) Include `r_coil = vessel_or`?** **Yes** — removes another magic constant and makes the magnet cost depend on the radial build.
- **(c) Rebind `special_materials_capital` to the computed `blanket_vol`?** **Yes** — keeps the CAS27 chain honest (it is literally `blanket_vol × …`). Under Option 1 the value is unchanged; the point is provenance, not a number change. (Design note: keys off the aggregate blanket_vol = firstwall+blanket+reflector = 1118.695; keep the aggregate to hold the value, absent a reason to change.)

## Modeling Requirements

### Functional

#### MR-WI021-1: Radial-build calc def in the library

`models/library/analyses/mfe_plasma_scaling.sysml` SHALL gain a concept-agnostic calc def (working name `'MFE Radial Build'`) that takes `R`, `a`, `kappa`, `pi` (defaulted input, existing pattern), and the radial-build layer thicknesses as inputs, and outputs: the four CAS22 aggregate volumes (`blanket_vol`, `shield_vol`, `structure_vol`, `vessel_vol`), the first-wall area (`wall_area`), and the coil-bore radius (`vessel_or` / `r_coil`). Internally it SHALL compute the cumulative radii as flat sums and each layer volume via the torus-shell formula `kappa · 2·pi²·R·(r_out² − r_in²)`, and the surface area via `kappa · 4·pi²·R·a_ref`, reproducing `compute_geometry`'s STEADY_STATE/torus branch and the `model.py:1205-1208` aggregation exactly.

- **Type**: Functional
- **Priority**: Must
- **Derives from**: RQ-2, RQ-3; handoff item 1
- **Validation**: SV-028; L1 parse

> Source: `/home/reid/1cfe/1costingfe/src/costingfe/layers/geometry.py`
> Ref: geometry.py:67-81 (`_torus_shell_volume`, `_torus_surface_area`), 106-118 (cumulative radii), 156-170 (per-layer volumes); model.py:1205-1208 (CAS22 aggregation)
> Basis: forward radial build = cumulative thicknesses then torus-shell volumes

#### MR-WI021-2: Torus shells, no material shape factor (Option 1)

Under the owner's Option-1 ruling, the material volumes and `wall_area` SHALL be computed as **pure torus shells with no shape factor** — matching 1costingFE. The calc's outputs at the Stellaris bindings SHALL reproduce the current injected constants (1118.695 / 552.140 / 219.979 / 157.933 / 802.201 / 3.20) to within display tolerance.

- **Type**: Functional
- **Priority**: Must
- **Derives from**: Central Decision (owner ruling); MR-4 (1costingFE is the admissible engineering source)
- **Validation**: SV-028 (computed = injected constants); handshake unchanged (MR-WI021-6)

> Source: `/home/reid/1cfe/1costingfe/src/costingfe/layers/geometry.py`
> Ref: geometry.py:140-148 (torus branch, no shape factor on material layers)
> Basis: engineered annular material structures are sized by the radial build, not the plasma cross-section

#### MR-WI021-3: Generic plant threads the radial-build calc

`models/designs/generic_mfe/mfe_plant.sysml` SHALL add a calc block instantiating `'MFE Radial Build'`, with its inputs bound to the plant's geometry attributes and its outputs available to the subsystem/cost calc blocks — following the existing `geom` / `'Plasma Geometry'` idiom (`mfe_plant.sysml:107`). The generic plant SHALL stay concept-agnostic (MR-3): thicknesses are inputs with library-generic defaults; concept-specific thicknesses bind in the instance.

- **Type**: Functional
- **Priority**: Must
- **Derives from**: MR-WI021-1; MR-3
- **Validation**: SV-028; L1–L6 on canonical models

#### MR-WI021-4: Instance wires computed outputs, replacing the six constants

`models/designs/stellarator_09/stellarator_plant.sysml` SHALL bind the radial-build thicknesses (from `steady_state_stellarator.yaml` + `RadialBuild` defaults, cited) and route the calc outputs into the consumers currently fed by constants: `blanket.blanket_vol`, `shield.shield_vol`, `structure.structure_vol`, `vessel.vessel_vol`, `wall_area`, and `magnet.r_coil`. The six injected constants SHALL be removed (or become computed redefinitions), and their doc comments updated to describe the forward computation instead of the copied value.

- **Type**: Functional
- **Priority**: Must
- **Derives from**: MR-WI021-1; handoff item 1
- **Validation**: SV-028; doc inspection at review

> Source: `/home/reid/1cfe/1costingfe/src/costingfe/data/defaults/steady_state_stellarator.yaml`
> Ref: steady_state_stellarator.yaml:39-42 (blanket/shield/structure/vessel thickness); geometry.py:19-40 (RadialBuild defaults for the remaining layers)
> Basis: Stellaris stellarator radial build

#### MR-WI021-5: Rebind `special_materials_capital` to the computed blanket volume (sub-decision c)

Pending owner confirmation of sub-decision (c), the CAS27 `special_materials_capital` SHALL be rebound to compute from the radial-build `blanket_vol` (`blanket_vol × vol_frac × density × price / 1e6`) instead of carrying a hardcoded value, keeping the CAS27 chain traceable. Under Option 1 the value is unchanged.

- **Type**: Functional / traceability
- **Priority**: Should (gated on sub-decision c)
- **Derives from**: capture-fidelity provenance; handoff item-1 scope note
- **Validation**: SV-028 (value unchanged under Option 1); doc inspection

> Source: `/home/reid/1cfe/1costingfe/src/costingfe/data/defaults/costing_constants.yaml`
> Ref: costing_constants.yaml:208 (pbli density 9400, vol_frac 0.50, price 5.0); costs.py:182-202 (cas27_special_materials)
> Basis: volume-based PbLi inventory keyed to the blanket volume

### Constraint

#### MR-WI021-6: Codegen envelope; downstream consumers coherent; handshake stays closed

The change SHALL stay in the proven codegen envelope: flat `Real` inputs with literal defaults, cumulative radii as `+` sums, layer volumes as `... * (r_out**2 - r_in**2)`, surface area as `... * a`. No conditionals, no transcendentals, no nested calc invocations beyond the existing single-level `calc x : 'Def'` idiom. The change SHALL be propagated to every consumer in the same edit: the codegen-adapted staged copies under `exploration/stellarator_e2e/models/`, the regenerated snapshot + pipeline, the pure-Python oracle (`verify_stellaris.py` — add the radial-build formulas), and the runner (`run_stellaris.py`). The **Anchor A handshake SHALL remain closed with no numeric change** (SV-025/SV-026 unchanged): under Option 1 the Stellaris instance's radial-build inputs equal 1costingFE's, so the computed volumes equal 1cfe's torus volumes. Per the WI-020 `f_shape` gotcha, the handshake's treatment of the new geometry inputs SHALL be verified explicitly (inject 1cfe's thicknesses, or confirm the instance bindings match) so SV-025/026 stay byte-identical.

- **Type**: Constraint
- **Priority**: Must
- **Derives from**: epic risk 1; `exploration/stellarator_e2e/CODEGEN_FINDINGS.md`; WI-020 handshake gotcha
- **Validation**: snapshot → V11-bridge codegen succeeds; SV-025/026 re-run unchanged; `run_stellaris.py` bit-exact vs updated oracle

### Traceability

#### MR-WI021-7: Citations, clean-room

Every added formula and bound value SHALL carry an MR-4 `Source / Ref / Basis` citation resolving to 1costingFE at `0254385` (radial-build formulas, thicknesses) or an admissible Stellaris source (R/a/kappa). No ARIES-CS-informed source may be read or cited (PROTOCOL.md §3). The radial-build geometry's ARIES/Starfire lineage is the scoped admissible exception (PROTOCOL §3); the calc-def doc SHALL note this basis explicitly.

- **Type**: Traceability
- **Priority**: Must
- **Derives from**: MR-4; PROTOCOL.md §3
- **Validation**: citation inspection at review

## Scope Boundaries

**In scope**
- `models/library/analyses/mfe_plasma_scaling.sysml` — new `'MFE Radial Build'` calc def (MR-WI021-1/2).
- `models/designs/generic_mfe/mfe_plant.sysml` — radial-build calc block, concept-agnostic (MR-WI021-3).
- `models/designs/stellarator_09/stellarator_plant.sysml` — bind thicknesses; wire six computed outputs; rebind `special_materials_capital` (MR-WI021-4/5); update the six doc comments.
- `exploration/stellarator_e2e/` — staged copies, regenerated snapshot/pipeline, oracle (`verify_stellaris.py`), runner (`run_stellaris.py`), handshake re-run (must be unchanged).
- `modeling_project/VALIDATION_MATRIX.md` — SV-028 (created by this spec, status pending).

**Out of scope**
- Plasma volume / fusion power / sigma_v — WI-020's territory, unchanged here.
- Predictive confinement — item 2.
- Any shape factor on material volumes — excluded under Option 1 (the central decision); if the owner picks Option 2 this line is struck and MR-WI021-2 changes.
- The bioshield volume and coil volume — `compute_geometry` computes a bioshield volume not used by the four CAS22 aggregates, and the coil has no torus-shell volume (magnet cost is a separate model); this item computes only what the six consumers need. If the calc emits bioshield_vol for completeness it stays unconsumed.
- Recomputing the STALE-BASIS pass-throughs (`buildings_capital`, `preconstruction_capital`, `annual_om`) — Stage-3 account item, unchanged.

## Success Criteria

1. **SV-028 (forward-computed radial build)**: the generated model produces the four CAS22 volumes, `wall_area`, and `r_coil` as forward computations from the radial-build inputs, reproducing the current injected constants (1118.695 / 552.140 / 219.979 / 157.933 / 802.201 / 3.20) under Option 1, bit-exact through the codegen pipeline via `run_stellaris.py` against the updated oracle.
2. **SV-025 and SV-026 still pass, numerically unchanged** — Anchor A handshake untouched (the Stellaris radial-build inputs equal 1costingFE's).
3. Validation Levels 1–6 pass on the canonical models (compare to the WI-020 baseline: L1 = 0, L2 = 3 pre-existing IFE, L6 = 105 pre-existing); the IFE anchor regression (SV-023) still passes; `run_stellaris.py` bit-exact against the updated oracle; all three viability constraints (beta, wall load, TBR) still pass (unchanged under Option 1).
4. The (unchanged, under Option 1) Stellaris headline is confirmed in the work item and `.project/CURRENT_WORK.md`, with the six-constants fidelity gap noted as closed. If Option 2 is chosen, the re-baselined headline is recorded instead.
5. Six injected constants removed; the geometry chain is forward-computed and traceable end to end.

## Assumptions & Risks

1. **Under Option 1 this is a no-op on the numbers** (likelihood: certain if Option 1; impact: expected): the win is fidelity/traceability, not a headline change. If the owner picks Option 2, it re-baselines cost/LCOE like WI-020 — the design and close SHALL state the numbers plainly either way.
2. **Handshake stays closed** (likelihood: high under Option 1; impact: high if wrong): the new geometry inputs must be handled per the WI-020 gotcha so SV-025/026 stay byte-identical. Implement verifies explicitly.
3. **Bigger than WI-020, same envelope** (likelihood: certain; impact: manageable): ~13 thickness inputs → ~9 shell volumes + aggregates + surface area is more surface area than WI-020's single added multiply, but all flat arithmetic. Risk is transcription error in the cumulative-radii chain — the oracle and SV-028 catch it.
4. **`special_materials_capital` aggregate vs. blanket-layer basis** (likelihood: low; impact: low): the current constant keys the PbLi inventory off the aggregate blanket_vol (firstwall+blanket+reflector); confirm at design whether that or the blanket layer alone is the intended basis. Under Option 1 the number is unchanged regardless.
5. **`wall_area` uses `vacuum_or` as the reference minor radius, not `a`** (likelihood: certain; impact: correctness): `_torus_surface_area(R, vacuum_or, kappa)` uses the first-wall standoff radius (`vacuum_or = a + vacuum_t`), not the plasma minor radius `a`. The calc SHALL pass `vacuum_or` (a computed cumulative radius), matching `geometry.py:148`. Getting this wrong would mismatch the 802.201 constant.

## Traceability

**Sources**
- `/home/reid/1cfe/1costingfe` @ `0254385`: `src/costingfe/layers/geometry.py:19-40` (RadialBuild defaults), `:67-81` (torus-shell volume + surface area), `:106-118` (cumulative radii), `:140-170` (torus branch + aggregation into the Geometry dataclass); `src/costingfe/model.py:1205-1208` (CAS22 volume aggregation); `src/costingfe/data/defaults/steady_state_stellarator.yaml:39-42` (Stellaris thicknesses); `costing_constants.yaml:208` + `costs.py:182-202` (CAS27 PbLi inventory).
- `knowledge/concept_research/09-qi-stellarator-hts/iter-01/sources/stellaris-design-details.md`: R ≈ 12.7 (line 251), a = 1.5 (line 228) — the R/a/kappa the radial build is evaluated at.

**Downstream impacts**: WI-009 library (new radial-build calc), WI-010 generic plant (radial-build block), WI-018 instance (six wired outputs + `special_materials_capital` rebind + six doc comments), staged e2e models/snapshot/pipeline/oracle/runner, handshake (verified unchanged), VALIDATION_MATRIX SV-028, Stellaris headline in `.project/CURRENT_WORK.md` (unchanged under Option 1).

**Applicable project rules**: MR-4 (citations), MR-3 (library stays concept-agnostic — the radial-build calc is generic; thicknesses bind in the instance), PROTOCOL.md §3 (clean-room; radial-build ARIES/Starfire lineage is the scoped admissible exception), capture-fidelity surfacing (the material-shape-factor decision is raised, not resolved silently) and provenance (six copied constants become forward-computed with their basis stated).

## Related Artifacts

- Epic: `work/backlog/epic-mfe-cost-modeling.md`
- Handoff (item 1): `/tmp/handoff-20260717-122307.md`
- Prior item (WI-020, closest template): `work/completed/20260717_WI-020_stellarator-correct-geometry/`
- Handshake: `exploration/stellarator_e2e/HANDSHAKE_REPORT.md`
- Design: `work/active/WI-021_stellarator-correct-radial-build/design.md` (to be created after owner checkpoint)
- Plan: `work/active/WI-021_stellarator-correct-radial-build/plan.md` (to be created)
