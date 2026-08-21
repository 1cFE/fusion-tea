---
Status: completed
Scale: standard
Epic: MFE Cost Modeling — Tokamak & Stellarator
Owner: reid
Created: 2026-07-17
Updated: '2026-07-17'
---

# WI-020: Stellarator-Correct Plasma Geometry

**Required Reading: `knowledge/holdout/aries-cs/PROTOCOL.md`** — this is a stellarator-demo model-development item. The ARIES-CS hold-out is sealed; the §3 barred paths must not be read, cited, or opened. Admissible sources for this item: the Stellaris design sources under `knowledge/concept_research/09-qi-stellarator-hts/iter-01..03/sources/**` (minus the barred entries) for physics/geometry, and 1costingFE (pinned `0254385`) for engineering formulas.

## Overview

Give the plasma-volume calc a stellarator-correct value. Today `'Plasma Geometry'` uses the elongated-torus formula `V = 2π²Ra²κ`, which yields 564 m³ at the Stellaris bindings (R=12.7, a=1.5, κ=1.0). The Stellaris source tabulates a plasma volume of **448 m³** — the QI stellarator plasma is a shaped (bean-cross-section, twisted) column, not a smooth elongated torus, and the torus formula over-predicts its volume by ~26%. This item adds a multiplicative shape/packing factor so the modeled volume matches the source, and re-solves the effective D-T reactivity so the 2700 MW design fusion power is preserved. Item 4 of the demo-deepening plan (order 3→4→1→2; item 3 / WI-019 is done). It precedes items 1 and 2 because volume drives fusion power (item 2) and, later, material volumes (item 1).

## Goals & Context

**Research questions served**:
- RQ-2 (credible LCOE range): plasma volume sets fusion power, the head of the whole power→cost→LCOE spine. A 26% volume error is a physics-fidelity defect at the top of that chain even when (as here) we hold the design power fixed.
- RQ-3 (shared vs. divergent structure): the tokamak/stellarator split is *exactly* where geometry diverges. A stellarator that reuses the tokamak torus volume erases the divergence this epic exists to make real. The shape factor is the concept-divergent geometry knob (default 1.0 = torus for tokamaks; <1 for a shaped stellarator).

**Demo context**: The Stage-3 backlog (`.project/CURRENT_WORK.md`) lists "torus-volume 564 vs Stellaris 448" as a standing fidelity gap carried since Stage 2. The `stellarator_plant.sysml` instance already flags it in a MAPPING/CROSS-CHECK NOTE (lines 250-255) — but that note's diagnosis is wrong (see Current State), which is itself a reason to close this now.

**Epic context**: Edits the WI-009 library file `models/library/analyses/mfe_plasma_scaling.sysml` (`'Plasma Geometry'` calc). Consumed by WI-010 (`models/designs/generic_mfe/mfe_plant.sysml`, `geom` calc block) and the WI-018 concept-09 instance (`models/designs/stellarator_09/stellarator_plant.sysml`).

**Relevant prior insight**: WI-019 established (handoff Key Discovery) that `sigma_v` was back-solved to hit p_fus = 2700 MW at V = 564. Any change to V must decide what happens to that back-solve — see the central decision below.

## Current State

`models/library/analyses/mfe_plasma_scaling.sysml:27-28` computes

```
V = 2.0 * pi**2 * R * a**2 * kappa
```

At the Stellaris instance bindings (R=12.7, a=1.5, κ=1.0) this is **564.05 m³**. The Stellaris source (`knowledge/concept_research/09-qi-stellarator-hts/iter-01/sources/stellaris-design-details.md`) tabulates the plasma volume in **Table 2, line 230: 448 m³**.

**V's only consumer is fusion power.** `mfe_plant.sysml:120` binds `in V = geom.V` into the `'DT Fusion Power'` calc, and `p_fus` is linear in V. No other model element reads V. (Subsystem/material volumes — blanket, shield, structure, vessel — are separate injected constants; that is item 1, radial build.) So a change to V propagates to exactly one place: p_fus.

**The instance's existing cross-check note is arithmetically wrong.** `stellarator_plant.sysml:252-254` claims the 448-vs-564 gap is "the R/a rounding difference in the source tables… consistent with R=12.0, a=1.38 rather than R=12.7, a=1.5." That is false: the torus formula at R=12.0, a=1.5, κ=1.0 gives **533 m³**, not 448; and at a=1.38 it gives 451 m³ only by shrinking the minor radius below the source's own stated 1.5 m. No (R, a) pair from the source reproduces 448 via the torus formula. The real cause is geometric shaping, not rounding. This note is replaced by this item (see MR-WI020-4).

## Source Conflict — surfaced, not silently resolved

The admissible Stellaris source is internally inconsistent about the plasma's size. Three figures, three values:

| Where | Major radius R | Plasma volume V |
|---|---|---|
| Table 2 "Key parameters" (lines 227, 230) | **12 m** | **448 m³** |
| Prose §2.1 (line 251) | ~12.7 m | — |
| Fig. 2 size-comparison text (line 253) | — | **425 m³** |

The model currently uses R = 12.7 (from the prose, line 251), and that 12.7 is threaded through other bindings (magnet `R0 = 12.7`, coil geometry). The two tabulated volumes (448, 425) differ by ~5%. This conflict is real in the source and cannot be resolved by us; it is a decision for the owner checkpoint (Decision B below). Per the capture-fidelity surfacing rule, dependent conclusions (the exact shape-factor value) are parked on that decision.

The physical decomposition, for the owner's judgment:
- The torus formula at the source's **own** self-consistent Table-2 geometry (R=12, a=1.5, κ=1.0) gives 533 m³. Source volume 448 → genuine QI shaping factor ≈ **0.84** (a 16% reduction — the real physical effect).
- The model keeps R=12.7 (prose + rest-of-model consistency). Torus at R=12.7 gives 564 m³. Hitting 448 from there needs factor ≈ **0.794**, which bundles the 0.84 physical shaping with the source's own R=12-vs-12.7 table inconsistency.

## Central Decisions — OWNER RULING (2026-07-17)

Both decisions were surfaced at the owner checkpoint. The owner ruled:

**Decision A — DO NOT re-solve sigma_v. Make the model accurate; explore inputs at codegen.** (Owner, 2026-07-17: *"don't re-solve. Just make sure the model is accurate. We can test various inputs at the codegen phase."*)
- `sigma_v` stays at its current value (5.985e-23 m³/s) — a genuine point on the Bosch-Hale curve (T_eff ≈ 7.9 keV), no longer justified as a back-solve to a target power.
- V is corrected to 448 (Decision B1). Fusion power is then a **computed output**, not a pinned anchor: p_fus = 2700 × (448/564.05) ≈ **2144 MW** at the current sigma_v.
- **This re-baselines the headline.** p_fus drops ~20% → power balance, every power-scaled cost account, net electric, and LCOE all recompute (implement produces the exact numbers via the oracle/pipeline). Direction: net electric falls back toward the pre-WI-019 range (~580–600 MW; WI-019's power-balance gain and this volume correction partly offset); LCOE rises correspondingly; wall load drops to ~2.1 MW/m² (more margin); all viability constraints still pass.
- The 2144-vs-2700 gap is the honest 0D-model limitation (real n, T profiles are peaked, concentrating fusion in the hot core). It is left **visible**, not papered over, and is the target of item 2 (predictive confinement). The owner will probe input sensitivity (sigma_v / effective temperature) at the codegen execution phase; implement SHALL report a small sigma_v sensitivity to support that.
- *Rejected alternative (the spec's original recommendation): re-solve sigma_v ≈ 7.535e-23 to hold p_fus = 2700. Rejected by the owner as a fudge — a back-solve tunes an input to a predetermined output, the opposite of "accurate." Recorded per the correction rule; not to be reintroduced.*

**Decision B — which volume figure, and how to set the factor. OWNER: B1 (agreed).** Three admissible options were offered:

| Option | Keeps | Shape factor | Modeled V | Note |
|---|---|---|---|---|
| **B1 (recommended)** | R=12.7 (prose + model), a=1.5, κ=1.0 | f_shape = 448/564.05 = **0.7943** | 448 m³ | Hits the Table-2 headline volume; factor is an empirical packing factor bundling QI shaping + the source's R inconsistency, documented honestly as such. Smallest blast radius: only the geometry calc + one instance binding change; magnet R0 etc. stay 12.7. |
| B2 | R=12.7, target Fig-2 volume | f_shape = 425/564.05 = 0.7535 | 425 m³ | Uses the size-comparison aside (425) instead of the parameter table (448). |
| B3 | change R to 12.0, a=1.5, κ=1.0 | f_shape = 448/533 = 0.840 | 448 m³ | Most internally consistent with Table 2 (R, a, V all one table); f_shape is then pure physical shaping. But changes R=12.7→12.0, touching the magnet R0 binding and the geometry cross-checks, and contradicts the prose's 12.7. Larger blast radius. |

*Owner ruled B1.* The item's whole purpose is to make the model reproduce the source's tabulated plasma volume; 448 is the headline parameter-table value (425 is an approximate size-comparison aside), and B1 hits it with the least disturbance to the rest of the model. The factor is documented as empirical (packing factor reconciling the model's R=12.7/a=1.5/κ=1.0 to the tabulated 448 m³), not dressed up as pure physics.

## Modeling Requirements

### Functional

#### MR-WI020-1: Shape/packing factor on plasma volume

The `'Plasma Geometry'` calc SHALL apply a multiplicative shape factor `f_shape` to the elongated-torus volume: `V = 2π²Ra²κ · f_shape`, keeping V forward-computable from R/a/κ (so the geometry→fusion-power chain and SV-017 monotonicity survive). `f_shape` SHALL be a defaulted input with **default 1.0** (a pure elongated torus — tokamaks and the 1costingFE torus geometry unchanged).

- **Type**: Functional
- **Priority**: Must
- **Derives from**: RQ-3 (concept-divergent geometry); handoff item 4
- **Validation**: SV-027; L1 parse

> Source: `knowledge/concept_research/09-qi-stellarator-hts/iter-01/sources/stellaris-design-details.md`
> Ref: Table 2 line 230 (plasma volume = 448 m³); §2.1 line 251 (near-circular average cross-section, R ≈ 12.7 m)
> Basis: QI stellarator plasma is a shaped column; elongated-torus formula over-predicts its volume

#### MR-WI020-2: Stellaris instance binds the shape factor to the source volume

The concept-09 instance SHALL bind `f_shape` to the value that reproduces the Stellaris tabulated plasma volume at the instance's R/a/κ, per the owner's Decision B (recommended B1: `f_shape = 0.7943`, targeting Table-2 V = 448 m³ at R=12.7, a=1.5, κ=1.0). The binding SHALL carry an MR-4 citation to the Stellaris source volume and state, in its doc comment, that the factor is an empirical packing factor reconciling the model's geometry inputs to the tabulated volume (not a first-principles shaping computation).

- **Type**: Functional
- **Priority**: Must
- **Derives from**: MR-WI020-1; Decision B
- **Validation**: SV-027

> Source: `knowledge/concept_research/09-qi-stellarator-hts/iter-01/sources/stellaris-design-details.md`
> Ref: Table 2 line 230 (V = 448 m³)
> Basis: shape factor = tabulated V / elongated-torus V at the Stellaris bindings

#### MR-WI020-3: sigma_v unchanged; fusion power becomes a computed output; doc made honest

Per the owner's Decision A, the concept-09 instance SHALL leave `sigma_v` at its current value (5.985e-23 m³/s) — **no re-solve**. Fusion power is then a computed model output (≈ 2144 MW at the corrected volume), not a pinned anchor. The `sigma_v` doc comment SHALL be rewritten to remove the back-solve justification (it currently claims the value "reproduces the Stellaris 2700 MW design fusion power … under … the geometry volume (564 m³)") and instead state plainly: sigma_v is a 0D-effective D-T reactivity at T_eff ≈ 7.9 keV (a real point on the Bosch-Hale curve); at the corrected volume 448 m³ with the volume-averaged density it yields ≈ 2144 MW, below the Stellaris 2700 MW design point; the gap is the 0D single-temperature limitation (real n, T profiles are peaked) and is the target of item 2 (predictive confinement), not closed here.

- **Type**: Functional / traceability correction
- **Priority**: Must
- **Derives from**: Decision A (owner ruling); capture-fidelity correction rule (delete the now-false back-solve claim, don't annotate around it)
- **Validation**: SV-027 (p_fus is the computed value, bit-exact vs oracle); doc-comment inspection at review

> Source: `/home/reid/1cfe/1costingfe/src/costingfe/layers/reactivity.py`
> Ref: reactivity.py:54-70 (sigv_dt Bosch-Hale D-T, the curve the 5.985e-23 / 7.9 keV point lies on); stellaris-design-details.md Table 5 line 742 (P_fus = 2700 MW design point, now shown as unmet by the 0D model)
> Basis: sigma_v is an unchanged 0D-effective reactivity; fusion power is computed, and the design-point gap is left visible

#### MR-WI020-4: Replace the wrong cross-check note

The instance's MAPPING/CROSS-CHECK NOTE (`stellarator_plant.sysml:250-255`) SHALL be rewritten. It currently attributes the 448-vs-564 gap to "R/a rounding" — arithmetically false (torus at R=12, a=1.5 = 533, not 448). The replacement SHALL state the correct cause (QI shaping represented by `f_shape`), record the source's internal V/R inconsistency (448 vs 425; R 12 vs 12.7) as a documented decision per Decision B, and note that `f_shape` bundles shaping with that inconsistency under B1.

- **Type**: Traceability / correction
- **Priority**: Must
- **Derives from**: capture-fidelity correction + surfacing rules
- **Validation**: doc-comment inspection at review

### Constraint

#### MR-WI020-5: Codegen envelope

The change SHALL stay in the proven codegen envelope: `f_shape` a flat `Real` input with a literal default, the volume expression a single added multiply (`... * f_shape`). No conditionals, no transcendentals, no nested calc invocations.

- **Type**: Constraint
- **Priority**: Must
- **Derives from**: epic risk 1; `exploration/stellarator_e2e/CODEGEN_FINDINGS.md`
- **Validation**: snapshot → V11-bridge codegen succeeds; SV-027 runs through the generated pipeline

#### MR-WI020-6: Downstream consumers updated coherently; handshake stays closed

The change SHALL be propagated to every consumer in the same change: the generic plant `geom` calc block (`mfe_plant.sysml:104-108` — add the `f_shape` attribute + `in f_shape = f_shape` binding, defaulting or bound so the tokamak/torus path is unchanged), the codegen-adapted staged copies under `exploration/stellarator_e2e/models/`, the regenerated pipeline, the pure-Python oracle (`verify_stellaris.py` — add `f_shape` to `IN`, update `sigma_v`, apply the factor in `compute()`), and the runner headline check (`run_stellaris.py:230` — change the V assertion from 564 to 448). The **Anchor A handshake SHALL remain closed with no numeric change**: `handshake_1costingfe.py` injects 1costingFE's own torus geometry and solves sigma_v against the torus, so with `f_shape` defaulting to 1.0 (or explicitly injected as 1.0) the generated model reproduces 1cfe's point exactly as before — SV-025 and SV-026 must still pass unchanged.

- **Type**: Constraint
- **Priority**: Must
- **Derives from**: MR-WI020-1 (default 1.0 guarantees handshake closure); the canonical-vs-staged split
- **Validation**: L1–L6 on canonical models; SV-025/026 re-run unchanged; `run_stellaris.py` oracle agreement

### Traceability

#### MR-WI020-7: Citations, clean-room

Every changed formula and value SHALL carry an MR-4 `Source / Ref / Basis` citation resolving to an admissible Stellaris source (geometry/physics) or to 1costingFE at `0254385` (engineering). No ARIES-CS-informed source may be cited or read (PROTOCOL.md §3). Geometry is physics — deviating here from the 1costingFE torus formula is consistent with the demo's sourcing rule (admissible source = the Stellaris paper), and MR-WI020-4's note SHALL say so explicitly.

- **Type**: Traceability
- **Priority**: Must
- **Derives from**: MR-4; PROTOCOL.md §3
- **Validation**: citation inspection at review

## Scope Boundaries

**In scope**
- `models/library/analyses/mfe_plasma_scaling.sysml` — add `f_shape` to `'Plasma Geometry'` (MR-WI020-1).
- `models/designs/generic_mfe/mfe_plant.sysml` — thread `f_shape` through the `geom` calc block (MR-WI020-6).
- `models/designs/stellarator_09/stellarator_plant.sysml` — bind `f_shape` and re-solve `sigma_v`; rewrite the cross-check note (MR-WI020-2/3/4).
- `exploration/stellarator_e2e/` — staged copies, regenerated pipeline, oracle (`verify_stellaris.py`) and runner (`run_stellaris.py`) updates, handshake re-run (must be unchanged).
- `modeling_project/VALIDATION_MATRIX.md` — SV-027 (created by this spec, status pending).

**Out of scope**
- First-wall area (`wall_area = 802.201`) and all subsystem/material volumes (blanket, shield, structure, vessel) — those are 1costingFE torus-geometry injected constants; the radial build is item 1. Item 4 is the plasma volume only. (The instance's `wall_area` doc note references "the same build that yields plasma_vol = 564"; it will be lightly clarified to say 564 is 1cfe's internal torus volume while the SysML plasma volume is now 448 — no value change.)
- Predictive confinement / profile-integrated reactivity — item 2. sigma_v stays an unchanged 0D-effective input here; the design-point gap it now exposes is item 2's target.
- Recomputing the STALE-BASIS pass-throughs (`buildings_capital`, `preconstruction_capital`, `annual_om`) at the new p_net — those stay documented pass-throughs (WI-019 open item 1); their STALE-BASIS annotations SHALL be updated to cite the new p_net, but recomputation remains the Stage-3 account-scope item.

## Success Criteria

1. **SV-027 (corrected volume + honest computed power)**: the generated model produces `geom.V = 448 m³` (Decision B1) at the Stellaris instance, and `p_fus` is the value that volume computes at the unchanged sigma_v (≈ 2144 MW — a computed output, not pinned), bit-exact through the codegen pipeline via `run_stellaris.py` against the updated oracle.
2. **SV-025 and SV-026 still pass, numerically unchanged** — the Anchor A handshake is untouched because `f_shape` defaults to 1.0 on 1cfe's torus point (the handshake never uses the Stellaris shape factor).
3. Validation Levels 1–6 pass on the canonical models (compare counts to the WI-019 baseline: L1 = 0, L2 = 3 pre-existing IFE, L6 = 105 pre-existing); the IFE anchor regression (SV-023) still passes; `run_stellaris.py` remains bit-exact against the updated oracle; all three viability constraints (beta, wall load, TBR) still pass at the re-baselined power.
4. The re-baselined Stellaris headline (V = 448 m³; new p_fus ≈ 2144 MW and the recomputed p_th / p_net / LCOE / total capital / account shares) is recorded in the work item and `.project/CURRENT_WORK.md`, with the volume-vs-torus gap noted as closed and the 2144-vs-2700 design-point gap noted as the visible 0D limitation handed to item 2.
5. **Input sensitivity reported**: implement records how p_fus and LCOE respond to sigma_v (a small sweep around 5.985e-23), supporting the owner's "test various inputs at the codegen phase" direction.

## Assumptions & Risks

1. **This re-baselines the headline (not a no-op)** (likelihood: certain under Decision A, impact: expected/accepted): p_fus drops ~20% and every power-scaled account and LCOE recompute. This is the owner's chosen accurate outcome. Implement produces the exact numbers; the design and close SHALL state them plainly so the change is auditable against WI-019's headline.
2. **Viability constraints hold at lower power** (likelihood: high, impact: high if wrong): lower p_fus lowers wall load (more margin) and lowers net electric and q_eng. Net electric must stay positive and q_eng > 1 for the viability asserts to pass. Estimated p_net ≈ 580–600 MW, q_eng ≈ 3 — passing. Implement SHALL confirm; if net electric approached zero the item would surface it, but the estimate is comfortably clear.
3. **f_shape default 1.0 preserves the handshake** (likelihood: certain, impact: high if wrong): if the factor's default were anything but 1.0, the Anchor A sigma_v injection would break. MR-WI020-1 fixes the default; MR-WI020-6 optionally injects 1.0 explicitly in the handshake as belt-and-suspenders.
4. **SV-017 monotonicity preserved** (likelihood: certain): V stays linear in R (f_shape is a constant multiplier), so d(p_fus)/dR > 0 still holds; no SV-017 regression.
5. **Empirical factor honesty** (impact: low): under B1, f_shape bundles physical shaping with the source's R inconsistency. MR-WI020-2/4 require this be stated plainly in the doc comments so a later reader is not misled into treating 0.7943 as a first-principles shaping coefficient.
6. **STALE-BASIS pass-throughs drift further** (likelihood: certain, impact: low): the new p_net moves `buildings_capital` / `preconstruction_capital` / `annual_om` further from their derivation basis. Kept honest via updated annotations (out of scope to recompute — Stage-3 account item); surfaced again at close.

## Traceability

**Sources**
- `knowledge/concept_research/09-qi-stellarator-hts/iter-01/sources/stellaris-design-details.md`: Table 2 line 230 (V = 448 m³), line 227 (R = 12), line 251 (prose R ≈ 12.7 m; near-circular avg cross-section), line 253 (Fig. 2: V = 425 m³), Table 5 line 742 (P_fus = 2700 MW).
- `/home/reid/1cfe/1costingfe` @ `0254385`: `src/costingfe/layers/tokamak.py:172-174` (torus volume formula, the tokamak/torus basis for f_shape = 1.0); `src/costingfe/layers/reactivity.py:54-70` (sigv_dt, the sigma_v curve).

**Downstream impacts**: WI-010 generic plant `geom` block, WI-018 instance (`f_shape`, `sigma_v`, cross-check note), staged e2e models/pipeline/oracle/runner, handshake (verified unchanged), VALIDATION_MATRIX SV-027, Stellaris headline (V line only) in `.project/CURRENT_WORK.md`.

**Applicable project rules**: MR-4 (citations), MR-3 (library stays concept-agnostic — `f_shape` is a generic input defaulting to 1.0; the stellarator value binds in the instance), PROTOCOL.md §3 (clean-room), capture-fidelity surfacing (source conflict raised, not resolved silently) and correction (the wrong cross-check note is deleted/amended, not annotated around).

## Related Artifacts

- Epic: `work/backlog/epic-mfe-cost-modeling.md`
- Handoff (item 4): `/tmp/handoff-20260717-114235.md`
- Prior item (WI-019, template): `work/completed/20260714_WI-019_faithful-mfe-power-balance/`
- Handshake: `exploration/stellarator_e2e/HANDSHAKE_REPORT.md`
- Design: `work/active/WI-020_stellarator-correct-geometry/design.md` (to be created after owner checkpoint)
- Plan: `work/active/WI-020_stellarator-correct-geometry/plan.md` (to be created)
