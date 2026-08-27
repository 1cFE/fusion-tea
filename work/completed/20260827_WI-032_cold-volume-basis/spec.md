---
Status: completed
Scale: standard
Epic: MFE Cost Modeling — Tokamak & Stellarator
Owner: reid
Created: 2026-08-26
Updated: '2026-08-27'
---

# WI-032: Cold-Volume Basis — `vol_cold_cryo` Computed or Held

**⛔ This item stops at spec. Its load-bearing requirement needs an owner ruling first.** MR-WI032-1 retires `vol_cold_cryo` as a settable input. That value is an entry point of the sealed package (`exploration/stellarator_e2e/generated/contracts/model_contract.json:1832`) and an arm-definition key of a committed study (`exploration/stellarator_e2e/studies/20260823-magnet-technology-ab/study.py:44-47`), so retiring it changes what that study's arms mean. It is reserved gate 2 of goal `cryo-volume-basis` (`work/orchestration/goals/cryo-volume-basis/goal.md` § Reserved gates). No design, no plan, and no edit under `models/` until the owner rules. § Open decisions for the owner states what the ruling is between.

**Required reading: `knowledge/holdout/aries-cs/PROTOCOL.md`.** This is a stellarator-demo model-development item and the ARIES-CS hold-out is sealed. Admissible sources are the Stellaris sources under `knowledge/concept_research/09-qi-stellarator-hts/iter-01..03/sources/**` minus the barred entries (`knowledge/SOURCE_INDEX.md:179-189`), the ingested EU-DEMO conductor source (`knowledge/sources/eu_demo_rw_tf_coil_conductor_dematte_bruzzone/output.md`, `SOURCE_INDEX.md:206-216`), and 1costingFE at its pin.

## Why this item exists

Study `20260823-magnet-technology-ab` sighted it (record `@e204aee7` § 15, finding `#2`): "The model already computes the coil ampere-turns (Ampère's law in the magnet-cost calc), and DI-010 gives the engineering current density per conductor; volume should follow from the two." The row was routed here on 2026-08-26 (`exploration/stellarator_e2e/studies/DISCOVERY_LOG.md@4464c354`, id `20260823-magnet-technology-ab#2`).

The precedent is WI-030 (`work/completed/20260822_WI-030_computed-beta-peak-field/`), which retired a typed-in beta into a computed one with a stated tolerance against the source's printed value. This item is the same move on a different quantity, and it is argued against that shape.

**The reason the item is not a wiring job.** The identity the finding proposes does not hold as stated. § Current state shows the arithmetic. The finding is right that something is wrong with a held cold volume; it is wrong that the two quantities already in hand multiply out to it.

## Current state

### The three quantities, and what each actually is

- **The carried ampere-turns.** `models/library/analyses/mfe_magnet_cost.sysml@8f3b510c:44` — `total_kAm = G * B * R0 * r_coil / (mu0 * 1000.0)`, sourced to 1costingFE `cas22.py:427`. At the Stellaris design point (`G = 78.95683520871486`, `B = 9.0` T, `R0 = 12.7` m, `r_coil = 3.0` m, `mu0 = 1.25663706212e-6`) this is **2.1545e7 kA·m**.
- **The held volume.** `models/designs/stellarator_09/stellarator_plant.sysml@ba5c9945:570` — `vol_cold_cryo = 136.56` m³, built geometrically: six unique square winding-pack cross-sections (Table 8 image, sides 360/360/340/340/320/300 mm) × 8 occurrences × 25 m typical circumference. Σside² = 0.6828 m²; × 8 × 25 = 136.56 m³. Its doc names its own weak link — per-coil circumferences are not printed, so the 25 m is "typical but approximate."
- **The current density.** `knowledge/KNOWLEDGE.md@ffa5c54c` DI-010 — Stellaris REBCO winding-pack `J_eng` **112–124 A/mm²** at 20 K, against Nb₃Sn 14.6–28 A/mm² at 12 T class.

### What `G` is, and where the gap comes from

`G = 78.95683520871486` is `8π²` exactly. Substituting, the calc factorises into a current and a length:

```
total_kAm × 1000  =  I_link × L_proxy
I_link  = 2π R0 B / mu0 = 5.715e8 A·turns     (Ampère's law, the current linking the magnetic axis)
L_proxy = 4π r_coil     = 37.699 m            (the 1costingFE cost-proxy length, from the coil-bore radius)
```

`r_coil` is the **coil-bore** radius and falls out of the radial build (`stellarator_plant.sysml@ba5c9945:138-139`: `magnet.r_coil = rb.r_coil`, the vessel outer radius, 3.00 m). It is not a winding length and was never meant to be one. So `total_kAm` is a cost proxy — ampere-turn-metres against a stand-in length — and dividing it by `J_eng` divides the wrong length.

That is the whole of the 27–41 % gap recorded in the goal's grounding evidence, and it splits into two independent pieces:

| Piece | Size | What it is |
|---|---|---|
| Length form factor | `L_proxy / 25 m = 1.508` | The proxy length is 51 % longer than Stellaris's actual mean coil circumference. Dominant. |
| Residual current | 1.07 – 1.19 | Even at the true circumference, DI-010's band does not reproduce the anchor. Physical, see below. |

**With the actual winding geometry substituted** — 48 coils (sec. 2.9: 4 periods × (6 independent + 6 mirrored)) × 25 m — the total ampere-turn-metres are `I_link × 25 = 1.4287e10 A·m`, and:

| `J_eng` (A/mm²) | Volume (m³) | vs held 136.56 |
|---|---|---|
| 112 | 127.57 | −6.6 % |
| 118 | 121.08 | −11.3 % |
| 124 | 115.22 | −15.6 % |

Reproducing 136.56 m³ exactly would need `J_eng = 104.6 A/mm²`, **below** DI-010's sourced 112–124 band.

### Why the residual is physics, not error

Read the residual the other way. If the winding packs really are 136.56 m³ at 112–124 A/mm², they carry 1.53e10–1.69e10 A·m — **7 % to 18 % more ampere-turn-metres than Ampère's law on the magnetic axis accounts for**. That is expected for a modular quasi-isodynamic stellarator: the coils produce the helical shaping field as well as the toroidal field, and the shaping currents largely do not link the axis. Ampère's law on axis is therefore a **lower bound** on modular-coil current, not an estimate of it.

This matters for the decision, because it says the ampere-turn route is not merely uncalibrated — it is systematically the wrong quantity for this coil topology, by a margin the size of the effect being modelled.

### What the package does *not* carry

Neither the coil count nor the coil circumference exists anywhere in the models (grep over `models/`: `r_coil` is the only coil-geometry name, and it is the bore). Nor does `J_eng`. So computing the volume needs **at least one new bound input beyond the two the finding names**. Both the 48 and the 25 m are sourced and citable (Table 8 image, raw.pdf sec. 2.9) — the gap is that they are in a doc comment, not in the model.

### Downstream, and why the tolerance matters

`vol_cold_cryo` reaches the verdicts through one channel: → cryoplant heat load → cryoplant electrical → power balance → `rec_frac` and `p_net` (`mfe_plant.sysml@ba5c9945:265-280`, `mfe_cryo_plant.sysml@8f3b510c`). The committed study's certification addendum (record `@e204aee7`, 2026-08-23) quantified the sensitivity: swinging arm B's cold volume across its full sourced range 285–390 m³ moves `rec_frac` by 0.005, and the headline held in every case. A ±16 % tolerance on arm A is inside that order.

The second-order effect is larger than the first. Arm B's 390 m³ is itself derived *from* the held anchor — `136.56 × (118/21.5) × (4.69/9.0)` (`study.py:38-42`). If arm A's volume becomes computed, arm B's stops being a hand ratio off a held number and becomes the same formula at Nb₃Sn's `J_eng` and ceiling field. **That, not arm A's accuracy, is the real prize.**

## The three routes, assessed

**R1 — compute from winding length (recommended if the gate opens).** `vol_cold_cryo = I_link × n_coils × c_coil / J_eng`, with `n_coils`, `c_coil`, and `J_eng` bound in `designs/` (MR-3) and the Ampère's-law current taken from the same expression the magnet calc already uses. Reproduces the anchor to −6.6 %/−15.6 %; the shortfall is disclosed as the modular-coil current the axis-linking law does not see. Gains: arm B derives instead of being a hand ratio; the volume responds to `B` as physics says it should.

**R2 — calibrated form factor. Rejected.** Bind `f = L_total / (4π r_coil)` fitted at the design point so the formula returns 136.56 m³. It reproduces the anchor by construction, adds no physics, and hides the modular-coil discrepancy inside a fudge factor. Out of scope: a fitted form factor is not required, because a value calibrated to the point it is validated against cannot be validated.

**R3 — keep it held, reasoned.** The geometric build-up is the better basis for arm A on its own terms: it is cross-checked twice (each side² equals turns × (20 mm)² exactly against the Table 8 turns row; the no-casing masses 128.7 t × 8 imply ~7540 kg/m³, consistent with the Table 7 material mix), where the ampere-turn route is a provable lower bound. Under R3 this item closes as a `BOUNDED_NEGATIVE` with that reasoning as the product, and arm B's derivation stays a disclosed hand ratio.

## Modeling requirements — proposed, gated

These are written so the owner can rule on them. **None is authorized until the gate in the banner is resolved.**

#### MR-WI032-1: The cold volume is computed from winding ampere-turn-metres
**Type:** Functional | **Priority:** P0 | **Source:** discovery row `20260823-magnet-technology-ab#2`; DI-010 model implication | **Gated:** reserved gate 2
The model SHALL compute `vol_cold_cryo = (2π R0 B / μ0) × n_coils × c_coil / J_eng`, and `vol_cold_cryo` SHALL no longer be an entry point. The printed 136.56 m³ remains in the instance doc as the cross-check, exactly as WI-030 demoted `beta = 0.0276`.
**Rationale:** the only way the field lever reaches the cryogenic load, and the only way arm B's volume stops being a hand ratio anchored on arm A.
**Validation:** the computed volume at the Stellaris design point falls within the tolerance of MR-WI032-2; `vol_cold_cryo` absent from `contracts/model_contract.json` parameters; a `cold_volume_calc__vol_cold` output channel present.

#### MR-WI032-2: The tolerance is stated, and it is wide
**Type:** Quality | **Priority:** P0 | **Source:** WI-030 precedent (a stated tolerance against a printed value)
The item SHALL state its tolerance against the 136.56 m³ anchor as **−16 % / +0 %**, and SHALL record in the binding doc that the shortfall is the modular-coil shaping current that Ampère's law on the magnetic axis does not account for — not a data error and not a fitting residual.
**Rationale:** a tolerance tight enough to look respectable could only be met by calibrating, which is R2. The honest band is the one the sourced `J_eng` range produces.
**Validation:** the computed value lands in [114.7, 136.56] m³ at the design point; the doc states the physical reason for the offset.

#### MR-WI032-3: Library stays concept-agnostic; values live in the instance
**Type:** Constraint | **Priority:** P0 | **Source:** MR-3, restated in `work/backlog/epic-mfe-cost-modeling.md@f22bd288`
The calc def SHALL carry no concept values. `n_coils = 48`, `c_coil = 25.0`, and `J_eng` SHALL be bound in `stellarator_plant.sysml`; `μ0` is a defaulted constant declared last. `generic_mfe/mfe_plant.sysml` SHALL wire the calc from `magnet.B` and the plant's `R0` so a second MFE instance binds values only.
**Validation:** grep — no numeric literal other than the defaulted constant in the new library def; `mfe_plant.sysml` carries no Stellaris value.

#### MR-WI032-4: Every new value sourced (no fallbacks)
**Type:** Traceability | **Priority:** P0 | **Source:** MR-4
Every new bound value SHALL carry `Source / Ref / Basis`: `n_coils = 48` and `c_coil = 25.0` (raw.pdf sec. 2.9, the same reference the held value's own doc already cites); `J_eng` from DI-010's Stellaris band with the chosen point stated and the band recorded as the tolerance basis. Nothing bound from a typical-literature value.
**Validation:** citation-by-citation read at audit; every Ref resolves to an image or a pinned upstream line.

#### MR-WI032-5: The committed study's arms are restated, not silently broken
**Type:** Constraint | **Priority:** P0 | **Source:** `modeling_project/STUDY_POLICY.md@ad2fb4ea` § 2 rule 1 and rule 3 | **Gated:** reserved gate 2
`vol_cold_cryo` retires as a sweep/arm key. The item SHALL record the replacement arm definition — arm B defined by `J_eng` at Nb₃Sn's band and `magnet__B_max = 13.0` rather than by a derived 390 m³ — and SHALL state that study `20260823-magnet-technology-ab` is not reproducible as written against the new package.
**Rationale:** policy § 2 rule 3 is explicit that internalizing a lever retires the axis. What it does not do is authorize breaking a committed study's reproducibility silently.
**Validation:** the replacement arm definition is written down before any regeneration; the study record's non-reproducibility is disclosed in this item's record.

## Scope boundaries

**In scope (post-gate):** a new `calc def` in `models/library/analyses/` and its wiring in `models/designs/generic_mfe/mfe_plant.sysml`; bindings in `models/designs/stellarator_09/stellarator_plant.sysml`; the byte-identical `exploration/stellarator_e2e/models/` twin.

**Out of scope:**
- Coil thickness, radial build, and the field loop (discovery row `#3`, policy § 4 R1) — a different goal.
- Re-basing `f_carnot_cryo` from 0.20 (DI-009 says it applies to all arms at once).
- Minting a DI or amending DI-010.
- Regeneration, verification, and re-pinning of the package. The `integrate` seam has no native tracked procedure and no documented hand pattern (`work/orchestration/GOAL_RUNBOOK.md` § The native seams); it is handed to the operator, not improvised here.
- Re-running study `20260823-magnet-technology-ab`.

## Open decisions for the owner

**Ruled 2026-08-27 `[OWNER]`: R3 — keep it held.** The knob stays a settable design parameter (the product sets parameters and observes attributes); measured sensitivity across the full sourced volume range turns no verdict; the held value is the better number at the anchor. Decisions 2 and 3 fall with it: gate 2 is not opened, and the `J_eng` point value is moot. **Reversal condition:** reopen through a new work item if a future study's verdicts turn on cryoplant load — this spec's derivation stands ready. The item closes as the `BOUNDED_NEGATIVE` § The three routes' R3 branch describes.


1. **R1 or R3** — compute at a −16 % tolerance, or keep it held with the reasoning as the answer. § The three routes is the argument; the recommendation is R1, and the reason is arm B, not arm A.
2. **Reserved gate 2** — retiring `vol_cold_cryo` as a settable input, which follows automatically from R1 and is what makes the committed study non-reproducible as written (MR-WI032-5).
3. **The `J_eng` point value** inside DI-010's 112–124 band, if R1. The choice sets where in the −6.6 %/−15.6 % band the design point lands.

## Related artifacts

- Goal: `work/orchestration/goals/cryo-volume-basis/` (question, invariants, reserved gates, close rule)
- Precedent: `work/completed/20260822_WI-030_computed-beta-peak-field/spec.md`
- Finding: `exploration/stellarator_e2e/studies/20260823-magnet-technology-ab/record.md@e204aee7` § 15 `#2`, § 2, certification addendum
- Epic: `work/backlog/epic-mfe-cost-modeling.md@f22bd288`
- Design and plan: not created — the item is gated at spec.
