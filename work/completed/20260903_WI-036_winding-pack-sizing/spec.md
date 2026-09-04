---
Status: completed
Scale: standard
Epic: MFE Cost Modeling — Tokamak & Stellarator
Owner: reid
Created: 2026-09-03
Updated: '2026-09-03'
---

# WI-036: Winding-Pack Sizing Chain — Current-Sized Pack, Its Cost and Cryo Consequences, and a Conductor-Strain Check

Minted from the `magnet-closure` goal's round result (sightings `20260830-stress-fence#1` "winding length held at `c_coil`" and `#2` "`wp_side` costless"). Grounded and scoped under goal `priced-levers`, round 1, task T-003. The owner reserved no gates for this goal and delegated execution decisions to the round agent `[OWNER-VERBATIM 2026-09-02: "no gates. USE YOUR BEST JUDGEMENT ALONG THE WAY!"]`; merge, push, and work-item close remain owner-held. Requirements below are outcome-level — mechanism is deferred to design.

**Required reading:** `knowledge/holdout/aries-cs/PROTOCOL.md` (clean room, §§1–3, sealed). Admissible sources for this item: the Stellaris design source at `knowledge/concept_research/09-qi-stellarator-hts/iter-01/` and `iter-02/` (excepting the three barred entries), the pinned 1costingFE (`0254385`), and the four sources registered by goal `priced-levers` T-001/T-002 in `knowledge/sources/`. The barred-by-default costing sources are not used and no exception is claimed.

## Why this item exists

Three of the model's magnet quantities are held constants that a real design would compute, and the gap is now load-bearing rather than cosmetic.

`wp_side = 0.36` reaches exactly one consumer — the stress calc (`models/library/analyses/mfe_magnet_field.sysml:81`). It buys no conductor, no cold mass, and no radial build, so widening the winding pack to relieve stress is free. `vol_cold_cryo = 136.56` is a held literal whose "(COMPUTED)" comment describes arithmetic done by hand in prose. And `c_coil = 25.0` is a printed "typical" circumference that is the sole length term in the entire magnet cost.

The consequence was measured. In `20260901-sustainment-fence`, the study swept `I_coil` from 8 to 24 MA with the pack frozen at 0.36 m, which implies a winding-pack current density rising from 119 to 154 A/mm² against a design range of 112–124 — extra current carried by no extra conductor. The 11 points that satisfy every constraint except the two field fences are the machine's only evidenced escape from the 50 MW deadlock, and the model cannot price that escape today.

## Current state

- `wp_side` → `sigma_wp` only (`mfe_magnet_field.sysml:81`, asserted by `wp_stress_ok`, `mfe_viability.sysml:124`). No other consumer anywhere in `models/`.
- `vol_cold_cryo = 136.56` held (`stellarator_plant.sysml:686`), feeding the WI-024 cryo chain (`mfe_cryo_plant.sysml:47`) which does reach cost (`mfe_account_costs.sysml:588` → `cryoplant_capital`).
- Winding-pack cost is ampere-metre proportional and cross-section blind: `kAm_wind = n_coils * I_coil * f_set * c_coil / 1000`, `cost = kAm_wind * cost_per_kAm * f_wp_fab` (`mfe_magnet_cost.sysml:98,100`).
- Magnet structure cost is held-mass proportional: `m_casing = 63000.0` (`stellarator_plant.sysml:219`).
- The radial build carries a *separate* held coil thickness `coil_t = 0.30` (`stellarator_plant.sysml:456`), cited to 1costingFE's geometry default, inconsistent with the 0.36 m winding pack and unrelated to it.
- One structural check exists (`wp_stress_ok`). No conductor check of any kind exists.

## What must be true afterward (requirements)

#### MR-WI036-1: The winding pack is sized by the current it carries
**Type:** Functional | **Priority:** P0 | **Source:** Stellaris Table 8, image-verified; goal `priced-levers` `evidence/T-001_research_return.md` § 2
The model SHALL compute winding-pack cross-section from coil current and a winding-pack current density, rather than holding the cross-section constant while current varies. The relation SHALL be the one the source's own coil set satisfies — cross-sectional area equal to coil current divided by winding-pack current density — which closes to better than 1% across all six unique Stellaris coils. Winding-pack current density SHALL be a settable design input, since it is the quantity the source itself varies across its coil set (112–124 A/mm²).
**Validation:** SV-044.

#### MR-WI036-2: A larger winding pack costs cold mass
**Type:** Functional | **Priority:** P0 | **Source:** `evidence/T-001_research_return.md` § 2; WI-024 cryo chain
The model SHALL compute total cold winding-pack volume from the sized cross-section and the winding length, and that computed volume SHALL feed the existing cryoplant chain so that a larger pack raises cryogenic load and cryoplant capital. The computation SHALL reproduce the currently held 136.56 m³ at the design point, which the source's six cross-sections and winding length do exactly.
**Validation:** SV-045.

#### MR-WI036-3: `vol_cold_cryo` remains a settable input
**Type:** Constraint | **Priority:** P0 | **Source:** `[OWNER 2026-08-27]` WI-032 R3, restated in the `priced-levers` grounding instruction
The computed volume of MR-WI036-2 SHALL be a computed *default* with the setter preserved, never a retirement of `vol_cold_cryo` as a settable entry point. This is the shape the owner drew for `p_pump` in the same instruction — the ruling bars retiring the input, not modelling the chain behind it.
**Validation:** SV-045.

#### MR-WI036-4: Winding length follows coil geometry
**Type:** Functional | **Priority:** P1 | **Source:** sighting `20260830-stress-fence#1`; WI-036 mint record, `work/orchestration/goals/magnet-closure/trail.md:418`
Winding length SHALL follow from coil geometry rather than resting solely on the printed "typical" circumference. Per the mint record, the expected outcome is one held constant traded for a smaller one — a coil-shape factor — with the trade stated rather than hidden. Where per-coil circumferences are unprinted, the residual held quantity SHALL be named and its provenance carried.
**Validation:** SV-046.

#### MR-WI036-5: The conductor gets its own check, separate from the structure's
**Type:** Functional | **Priority:** P0 | **Source:** `evidence/T-002_criterion_return.md` §§ 2, 4; `knowledge/sources/electro_mechanical_properties_of_rebco_coated_conductors/`
The model SHALL assert a conductor strain limit as a constraint distinct from `wp_stress_ok`, because every surveyed HTS fusion design — Stellaris included — performs two checks, a stress check against the structure and a strain check against the conductor, and this model performs only the first. The limit SHALL be a settable held input with a sourced default in the 0.2–0.4% band that practitioners enforce, and its operand SHALL be computed, not held. The registered measurements SHALL be carried as the basis: irreversible strain by manufacturer at 4.2 K / 19 T, with SuperOx — the tape the source specifies — the weakest of five at 0.45–0.47%, and no discernible strain effect below 0.4%.
**Validation:** SV-047.

#### MR-WI036-6: The stress allowable is not changed, and its category is stated
**Type:** Constraint | **Priority:** P0 | **Source:** `evidence/T-002_criterion_return.md` §§ 1, 5 (T-002 ruling)
`sigma_allow` SHALL remain 800 MPa in this item, in either direction. The design SHALL state in words which stress category the operand belongs to and what allowable that category carries — primary membrane 666 MPa, peak 1.0–1.333 GPa under the ITER criteria — so that a later reader can see the comparison being made rather than infer it. No feasible region may be opened by re-categorising the operand.
**Validation:** SV-047.

#### MR-WI036-7: Unmodelled conductor limits are declared, not valued
**Type:** Traceability | **Priority:** P0 | **Source:** `evidence/T-002_criterion_return.md` § 3; MR-4 no-fallbacks
The transverse limits on the conductor — delamination in through-thickness tension (measured at 3.6 MPa, two orders of magnitude below the axial limit) and transverse compression (~200 MPa on bare tape) — SHALL be recorded as a **named gap** at the model's own disclosure surface. No value SHALL be assigned to them and no proxy SHALL stand in for them. The model computes no through-thickness stress and must not imply it checks one.
**Validation:** SV-047.

#### MR-WI036-8: Library stays concept-agnostic
**Type:** Constraint | **Priority:** P0 | **Source:** MR-3
Sizing, volume, cost and constraint definitions SHALL live in `models/library/`; every Stellaris-specific value SHALL be bound on the `stellarator_09` instance.

#### MR-WI036-9: Every value is sourced, table values image-verified, no fallbacks
**Type:** Traceability | **Priority:** P0 | **Source:** MR-4; `feedback_no_fallbacks`
Every quantitative value SHALL carry `Source`/`Ref`/`Basis`. Values taken from the Stellaris tables SHALL be verified against the table **images**, not the markdown extraction — Table 8's markdown extraction is garbled and the image governs (`images/page_022_table_0.png`; goal `evidence/T-001_research_return.md` § 1). Where an input is missing, it SHALL be surfaced with options; no family average, literature default, or "reasonable" substitute is permitted.

#### MR-WI036-10: Standing rulings preserved at their real width
**Type:** Constraint | **Priority:** P0 | **Source:** goal `goal.md` § Invariants
Clean room in full; `p_pump` stays a held settable input; `vol_cold_cryo` stays settable (MR-WI036-3); SV-016 recorded against, never fitted; Anchor A closed at its pin and not re-run. `k_sigma` was back-solved at `wp_side = 0.36` (`stellarator_plant.sysml:198,203`) — the design SHALL state explicitly what it means off that anchor point, rather than let a reader assume it was independently sourced.

#### MR-WI036-11: Committed-study consequences restated before regeneration
**Type:** Traceability | **Priority:** P0 | **Source:** WI-037 MR-WI037-7 precedent; goal § Invariants
Before any package regeneration, the item SHALL record which committed studies this change makes non-replayable as written and what a replay would have to drop or re-read. Prior retirement cost ~30 fixture re-derivation sites; the design SHALL name the fixture and suite surface explicitly rather than discover it.

## Scope boundaries

**In scope:** winding-pack sizing from current and current density; computed cold volume feeding the existing cryo chain; winding length from coil geometry; a conductor strain constraint; instance rebinds in `stellarator_09`; the disclosure of unmodelled transverse limits.

**Out of scope:** changing `sigma_allow`; the conductor peak-field ceiling `B_max` and its cost consequence (that is WI-038, and it needs this item's sizing chain first); heating-system structure (WI-039); linking `wp_side` to the radial build's `coil_t` — the two inconsistent statements of coil radial extent are **recorded as a known defect for a later item**, because reconciling them moves vessel, blanket and shield volumes and would make this item's comparison unreadable.

## Success criteria

- Sizing: SV-044 — winding-pack cross-section computed from current and current density, reproducing the six printed coils to <1% (pending).
- Cold volume: SV-045 — computed volume reproduces 136.56 m³ at the design point and drives cryoplant load, with the setter preserved (pending).
- Winding length: SV-046 — length follows coil geometry with the residual held factor named (pending).
- Conductor check: SV-047 — a conductor strain constraint with a computed operand, the stress category stated, and the transverse gap declared (pending).
- Validation battery green; affected committed studies restated per MR-WI036-11.

## Assumptions & risks

1. The model's stress form σ = k_sigma·I·B_peak/wp_side remains usable as the relief channel when `wp_side` becomes computed (confidence: high — it reproduces the committed `sigma_wp` column to the printed digit at every swept current).
2. Strain compatibility between the tape stack and the pack is a usable first-order basis for the conductor operand (confidence: medium — the soldered Cu jacket offloads the stack, cooldown pre-compresses it ~−0.15%, and von Mises is not uniaxial stress; the design must state the operand's meaning honestly and may need to hold a load-sharing factor).
3. Strain limits measured at 4.2 K and 77 K bracket the 20 K operating point (confidence: medium-high — the source states irreversible strain limits are identical between those two conditions; the one paper measuring through 20 K is paywalled and recorded as a queued gap).
4. **Risk:** the conductor check may bind before the stress check at the design point, changing the baseline's verdict set. That is a finding to disclose, not a reason to loosen the limit.

## Traceability

**Upstream:** goal `work/orchestration/goals/priced-levers/` (`goal.md`, `evidence/T-001_research_return.md`, `evidence/T-002_criterion_return.md`); sightings `20260830-stress-fence#1`/`#2`; `20260901-sustainment-fence#1`.
**Downstream impacts:** `wp_stress_ok` operand; cryoplant load and capital; magnet capital; every committed study that held `wp_side` or `vol_cold_cryo`; WI-038, which needs this sizing chain before a field-ceiling lever means anything.
**Applicable project rules:** MR-3 (library concept-agnostic), MR-4 (citations), PROTOCOL §§2–3 (clean room).

## Open decisions

None outstanding at spec stage. Three calls were made by the round agent under the standing delegation and are recorded here for override: `sigma_allow` unchanged (MR-WI036-6); transverse limits declared rather than valued (MR-WI036-7); radial-build reconciliation deferred to a later item (§ Scope boundaries).

## Related artifacts

- Goal: `work/orchestration/goals/priced-levers/` — `goal.md`, `trail.md`, `evidence/`
- Registered sources: `knowledge/sources/electro_mechanical_properties_of_rebco_coated_conductors/`, `.../coil_concepts_for_demo_and_next_step_reactors_5th_iaea_demo/`, `.../conceptual_design_of_hts_magnets_for_fusion_nuclear_science/`, `.../development_and_large_volume_production_of_extremely_high/`
- Predecessor: `work/completed/20260902_WI-037_operating-point-closure/`

## Amendments

None.
