---
Status: completed
Scale: standard
Epic: MFE Cost Modeling — Tokamak & Stellarator
Owner: reid
Created: 2026-07-18
Updated: '2026-07-18'
---

# WI-024: Recirculating-Power Derivation Model (Coil/Cryo Parasitic Loads)

**Required Reading: `knowledge/holdout/aries-cs/PROTOCOL.md`** — this is a stellarator-demo model-development item. The ARIES-CS hold-out is sealed; the §3 barred paths must not be read, cited, or opened. Admissible sources for this item: the Stellaris sources under `knowledge/concept_research/09-qi-stellarator-hts/iter-01..03/sources/**` (minus the barred entries) for physics, and 1costingFE (`/home/reid/1cfe/1costingfe`, pinned `0254385`) for engineering and cost.

**Alignment brief: `work/orchestration/recirc-power-derivation.md`** — objective, provenance grades, owner decisions, reserved checkpoint gates. This spec executes that brief. Evidence authority record for the source landscape: `work/completed/20260718_WI-023_magnet-field-errata-B9/spec.md` §Sweep Findings.

## Overview

WI-023 rebound `p_tf = 0.0` because no admissible source prints a total coil/cryo parasitic power in MW — the Stellaris paper explicitly defers parasitic electricity ("outside the scope of this paper", conclusion, raw.pdf-confirmed). This item builds the honest replacement ([OWNER] intent, epic WI-024 entry): instead of binding a constant, model the derivation chain that produces the coil/cryo parasitic electrical power — winding-pack nuclear heating density × winding volume → heat load at 20 K → cryo-plant electrical via COP, plus the coil-conduction and other parasitic splits — with every link either sourced from admissible material, computed from sourced geometry, or an explicit owner-approved assumption parameter. Subsumes the WI-018-era Stage-3 note (cold-mass → cryo-electrical COP treatment) recorded in the p_tf doc block.

This spec's job: establish, link by link, where each number can honestly come from (the provenance table below), map the double-counting risk against the 1costingFE-sourced parasitic slots the instance already binds, and lay out the scope options. **Hard stop after this spec** ([OWNER] 2026-07-18, Align): the derivation scope, the parameter-vs-source rulings per link, and the double-counting resolution are the owner checkpoint's substance. Nothing past spec runs until scope approval.

**Baseline moved from (WI-023 executed record, `work/completed/20260718_WI-023_magnet-field-errata-B9/plan.md` Implementation Record):** V 425 m³, p_fus 2748.1 MW, p_th 3238.1 MW, gross 1078.3 MW, p_net 915.1 MW, rec_frac 0.151, q_eng 6.609, total $12.6015B, LCOE $201.46/MWh, magnet $6.3235B / 50.2%.

## Goals & Context

**Research questions served:**
- RQ-1 (dominant cost drivers): recirculating power sets the gross-to-net gap; for a 111 GJ / 48-coil HTS system the cryo plant is a standing parasitic load the model currently carries as an admitted zero.
- RQ-2 (credible LCOE range): the LCOE denominator is net electricity; a knowingly optimistic p_net (p_tf = 0) bounds LCOE from below. A derived parasitic power replaces "knowingly optimistic" with "derived, with stated assumptions".

**Owner decisions carried in (graded in the alignment brief) — do not reopen:**
- [OWNER] 2026-07-18 (WI-023 spec checkpoint, epic entry): the item IS the derivation — derive/decompose how the recirculating power values arise, instead of binding constants. Constant-binding options are dead.
- [OWNER] 2026-07-18 (WI-023): 1costingFE `p_coils = 3.0 MW` (`steady_state_stellarator.yaml:19`) rejected for binding — a generic 5.5 m-reference default, unrepresentative of a 12.7 m / 111 GJ coil set.
- [OWNER] 2026-07-18 (validation matrix): SV-016 (Q_eng ~10–40 band) stays `pending` until WI-024 lands a derived parasitic power; the band is not adjusted to fit the provisional q_eng 6.609.
- [OWNER] 2026-07-18 (WI-023 close-out): WI-024 sequences **before** the STALE-BASIS pass-through recompute, so the recompute happens at a settled p_net.
- [OWNER] standing: no-fallbacks rule — never invent or default a value for a missing input; surface honest options, owner decides.

**Epic context:** extends the WI-018 concept-09 instance and (depending on design) the MFE power-balance surroundings. The recirculating sum lives in the library calc (`models/library/analyses/mfe_power_balance.sysml:89-126`: `recirculating = p_coils + p_pump + p_sub + p_aux + p_cool + p_cryo + p_input/eta_pin`, faithful to 1costingFE `physics.py:321-324`); whether the derivation chain lands as a library calc def (concept-agnostic, MR-3) with instance parameters, or as instance-local structure, is a design decision after the checkpoint.

## Current State

- **The stopgap:** `models/designs/stellarator_09/stellarator_plant.sysml:434-454` binds `p_tf = 0.0` with the WI-023 deferral doc — cites no MW value, names the no-fallbacks rule, and points forward to this item. Staged twin mirrors it (`exploration/stellarator_e2e/models/designs/stellarator_09/stellarator_plant.sysml`, same region).
- **The 1costingFE-sourced neighbors** (same instance file): `p_tfcool = 15.0` (:455), `p_trit = 10.0` (:458), `p_house = 4.0` (:461), `p_cryo = 0.8` (:464), `p_pump = 1.0` (:428), `f_sub = 0.03` (:431) — all from `src/costingfe/data/defaults/steady_state_stellarator.yaml` (lines 20-24, 21, 17). These already carry some coil-adjacent load; see the double-counting map.
- **Oracle and runner:** `exploration/stellarator_e2e/verify_stellaris.py:66` (`p_tf=0.0`), `run_stellaris.py` headline asserts at the WI-023 values — both move at implement if the derived value is nonzero or slots are re-scoped.
- **Handshake:** `handshake_1costingfe.py` injects `pb__p_tf` (line 216, from 1costingFE `pb["p_coils"]`) and `magnet__B` (line 271) — the WI-023 safety argument covered instance rebinds only. A new calc structure could change the injection surface; safety is re-derived at design, not carried (alignment brief, premise caveats).
- **Validation matrix:** SV-016 `pending` (re-flagged at WI-023 close, waiting on this item); SV-030 `passing` (WI-023 headline). Next free SV number: SV-031 (created by this spec, below).

## Evidence — Derivation-Chain Provenance, Link by Link

All table values below were verified against page images or the published PDF (`knowledge/concept_research/09-qi-stellarator-hts/iter-02/sources/publikationen-1000179851-172386752/tmpissrtbos/raw.pdf`, Lion et al., FED 2025, registered in `knowledge/SOURCE_INDEX.md`). **Neither text extraction's table rows were trusted** — and this spec found fresh corruption in them (Errata below). Provenance grades used: **SOURCED** (printed in an admissible source, verified), **COMPUTED** (derivable from sourced geometry, arithmetic only), **ASSUMPTION-ONLY** (no admissible value exists; must be an explicit owner-approved parameter or excluded with documentation).

### Chain A — cryo-plant electrical (the core chain)

**A1. Winding-pack nuclear heating density — SOURCED.** 35.5 W/m³ mean cryogenic nuclear heating at the winding pack. Table 6 image (`iter-01/sources/stellaris-design-details/images/page_020_table_0.png`, bottom row: "Mean cryogenic nuclear heating (winding pack) [W/m³] 35.5") + §2.8 body text (PDF-confirmed); magnets at 20 K; EU DEMO ~50 W/m³ peak as the viability reference.

**A2. Winding-pack volume — COMPUTED (with one approximate-sourced input).** Not printed anywhere. But the sourced geometry supports computing it:
- Table 8 image (`.../images/page_022_table_0.png`) prints, per unique coil (6 unique; 48 coils = 6 × 8 by symmetry, §2.9 PDF-confirmed): number of turns 324/324/289/289/256/225 and **winding-pack cross-section side length [mm] 360/360/340/340/320/300** (square winding pack, §2.9: "for each coil, we select a square winding pack").
- The §2.9 unit cell (PDF: "Each turn is sized at 20 mm × 20 mm") reproduces those cross-sections **exactly**: turns × (0.02 m)² = side² for all six coils (e.g. 324 × 4 cm² = 0.1296 m² = 0.36²). Internally consistent, two independent printed witnesses.
- Coil circumference: "a typical circumference of 25 m" (§2.9, PDF-confirmed) — **printed but approximate**; per-coil circumferences are not printed. This is the weak link of the volume computation.
- Illustration (spec-stage arithmetic, not a binding): Σ(unique cross-sections) 0.6828 m² × 8 × 25 m ≈ **137 m³** total winding-pack volume.
- Independent cross-check: Table 8 "Coil mass, no casing [ton]" 24.2/25.4/21.6/21.5/19.0/17.0 → total ≈ 1030 t; implied density ≈ 7500 kg/m³, plausible for the Table 7 material mix (image `page_021_table_0.png`: tape stack 9%, copper jacket 35%, solder 12%, steel 36%, helium 8%). A mass-based volume route is also possible but needs assumed material densities (handbook values → assumption-grade), so the cross-section × circumference route is the cleaner COMPUTED candidate.

**A3. Heat load at 20 K — COMPUTED from A1 × A2 plus a SOURCED term, but an explicit lower bound.**
- Nuclear heating: 35.5 W/m³ × ~137 m³ ≈ 4.9 kW (illustration).
- Resistive-joint losses: **~7.5 kW steady-state for the entire coil set — SOURCED** (§2.9, PDF-confirmed: "10 W per joint … approximately 7.5 kW steady-state losses for the entire stellarator coil set … negligible compared to other electricity consumption and within the cooling capacity of existing cryocooler designs").
- **The paper itself declares this incomplete**: "this steady state electrical power should be smaller than the total nuclear heating of the coils, the coil cases, and the remaining 20 K cooled parts of the support structure, which will be examined in future studies" (§2.9, PDF-confirmed). Casing/cold-structure nuclear heating, current-lead heat leak, and thermal radiation/conduction loads are **not printed** — any inclusion is ASSUMPTION-ONLY (explicit uplift parameter, or excluded with the understatement documented). The printed-loads total (~12 kW) is a knowing lower bound.

**A4. 20 K cryo-plant COP (or specific power W_elec/W_cold) — ASSUMPTION-ONLY.** No admissible printed value:
- The Stellaris paper: qualitative only ("Operating at this higher temperature offers an increase in efficiency of the cryogenic plant", §2.8) — no number.
- **1costingFE (checked at this spec, pinned `0254385`): no COP/cryo-electrical code treatment exists.** Its `MagnetProperties` carries `cryo_temp_k = 20.0` for `rebco_hts` (`defaults.py:611` — admissible corroboration of the 20 K operating point) and `recirc_power_factor = 0.0` for all superconductors (`defaults.py:611-614`, used only by the copper resistive model `tokamak.py:182-186`). The cryoplant appears only as a CAS21 **building cost** driver via `coil_material` (`model.py:1229-1233`), never as a power computation. The single COP-adjacent datum in the whole codebase is a YAML comment on the **dipole** concept's default (`steady_state_dipole.yaml:52-53`: "eta_cryo ~1.25%" at 24.6 K, citing that concept's own "Reactor A Table 9") — machine-specific to a different concept, value-inadmissible under the no-fallbacks precedent (same ruling class as W7-X), shape-relevant at most.
- W7-X cryo figures (iter-02 sources): inadmissible as values ([OWNER]/[AGENT], WI-023 — 4 K NbTi experiment vs 20 K HTS plant); shape only.
- Honest parameterization options (owner picks form at checkpoint, value at checkpoint or design): (i) a direct specific-power assumption parameter (W_elec per W at 20 K); (ii) Carnot COP at 20 K (T_c/(T_amb − T_c) ≈ 0.071 — pure arithmetic, COMPUTED) × an explicit fraction-of-Carnot assumption parameter. Either way exactly one owner-approved assumption number.

**A5. Cryo-plant electrical = A3 / COP — COMPUTED once A4 is ruled.** Order-of-magnitude illustration only (not a proposal): ~12 kW printed loads × specific power ~30–70 W_e/W_cold ≈ **0.4–0.9 MW** — small against the 15.8 MW the p_tfcool + p_cryo slots currently carry, which is why the double-counting ruling, not the chain arithmetic, decides the headline movement.

### Chain B — coil conduction / electrical drive — SOURCED-as-negligible plus ASSUMPTION-ONLY remainders

- Steady-state DC drive of superconducting coils dissipates the ~7.5 kW joint losses (already counted in A3 as heat at 20 K; as an electrical-drive term it is negligible — the paper says so, PDF-confirmed). 1costingFE's own model agrees: `recirc_power_factor = 0` for superconductors.
- Current-lead resistive/thermal losses and coil power-supply standing losses: not printed in any admissible source → ASSUMPTION-ONLY or zero-with-documentation.

### Chain C — the other parasitic splits (scope option (b) only) — no admissible Stellaris values

The paper defers parasitic electricity wholesale, so p_tfcool, p_cryo, p_pump, p_trit, p_house, f_sub have **no Stellaris-printed values at all**; the only admissible material is the 1costingFE defaults the instance already binds. A "full decomposition" therefore cannot add sourced data — it can only convert 1costingFE defaults into explicit assumption parameters (or re-scope them against the Chain A derivation). This is the honest content of option (b), stated plainly for the checkpoint.

### Extraction errata found at this spec (surfaced, not silently corrected)

Both text-extraction lineages were already known to corrupt/invent table rows; this spec's verification found further concrete instances, recorded so no future session trusts them:

1. **Table 8 (iter-01 extraction ~lines 1906-1934) is corrupted nearly wholesale** vs the image (`page_022_table_0.png`): coil masses printed as 44.5–55.4 t (image: 24.2/25.4/21.6/21.5/19.0/17.0 t); cross-section side lengths as 500 mm (image: 360/360/340/340/320/300); total energy as "11250 (2.70 GJ per field period)" (image: **110.58 GJ, 2.76 GJ per coil** — consistent with Table 2's 111 GJ); contact resistance units as aΩ (image: μΩ); charging time "<300" (image: ≃600 h, 26 days); extra invented columns on several rows.
2. **§2.9 unit-cell text corrupted**: extraction says "Each turn is sized at 35 mm × 20 mm"; the PDF prints **20 mm × 20 mm** — and only the PDF value reproduces Table 8's cross-sections exactly. Any volume computation from the extraction's 35 mm would be wrong by 1.75×.
3. **Table 6 extraction rows corrupted** (TBR "1.15" vs image 1.074 — the instance already binds the image value; flux rows and units garbled: "W/kg²"). The image (`page_020_table_0.png`) is the witness, as WI-023 established.
4. Minor: extraction "current density in steel … 353 A/mm²" vs PDF "current density per turn … per copper fraction … 355 A/mm²". Also noted: Table 8 prints per-coil peak field max 24.6 T while Table 2 and §2.9 body text print 24.9 T peak — both printed in the paper, not load-bearing for this item, recorded to prevent a future "phantom" false alarm.

## Double-Counting Map — 1costingFE Slot Semantics vs a WI-024 Derivation

The instance binds six 1costingFE-sourced parasitic slots. What each covers **in 1costingFE's own semantics** (all refs at pin `0254385`), and how a WI-024 derivation interacts:

| Slot (instance binding) | 1costingFE semantics | Interaction with a derived cryo/coil chain |
|---|---|---|
| `p_tf = 0.0` (yaml `p_coils`, :19: "Coil power [MW] (complex 3D coils)"; `types.py:229`) | Electrical power to the coils. 1costingFE's own physics treats this as resistive dissipation, **zero for superconductors** (`recirc_power_factor = 0.0`, `defaults.py:611-614`; `tokamak.py:182-186`); the 3.0 MW stellarator default is a generic allowance (rejected for binding, [OWNER]) | **The empty slot WI-024 fills** under option (a) — though semantically the derived quantity (cryo-plant wall-plug) may belong in `p_cryo`'s slot instead; placement is checkpoint question Q2 |
| `p_tfcool = 15.0` (yaml `p_cool`, :20: "Cooling power [MW]"; `types.py:230`) | Undocumented composition beyond "Cooling power (MFE)". At 15 MW it is cryoplant-scale for the 5.5 m reference machine — if it already carries the coil cooling/cryo compressor electrical, coexisting with a derived cryo-electrical **double-counts the same physical load** | Replace, re-scope, or keep — checkpoint Q2. Note the derived printed-loads value (~0.4–0.9 MW) is far below 15 MW, so the ruling here dominates the headline movement, in either direction |
| `p_cryo = 0.8` (yaml :24: "Cryogenic power [MW]"; `types.py:231`) | "Cryogenic system power". Elsewhere in 1costingFE's own defaults (dipole, `steady_state_dipole.yaml:52`) `p_cryo` is precisely the cryoplant **wall-plug electrical computed from heat load × eta_cryo** — i.e. the same physical quantity Chain A derives | **Direct semantic collision** with the Chain A output — checkpoint Q2 |
| `p_pump = 1.0` (yaml :21) | Primary-coolant (blanket loop) pumping — not coil-adjacent | Coexists under option (a); touched only under option (b) |
| `p_trit = 10.0`, `p_house = 4.0` (yaml :22-23) | Tritium processing, housekeeping (`p_aux`) — not coil-adjacent | Coexists under (a); option (b) only |
| `f_sub = 0.03` (yaml :17) | Subsystem/control power fraction, `p_sub = f_sub × p_et` (`physics.py:315`) | Coexists under (a); option (b) only |
| (`p_input/eta_pin`, 50/0.5 MW) | ECRH wall-plug — sourced (Stellaris 50 MW; 1costingFE gyrotron efficiency) | Untouched either way |

## Scope Options for the Owner Checkpoint (laid out, not chosen)

**Option (a) — cryo-electrical derivation only, filling the coil-power gap.**
- Builds Chain A (+ Chain B's negligible/zero documentation): heating density × winding volume + joint losses → 20 K heat load → electrical via COP. One new assumption parameter minimum (COP), possibly two (unprinted-loads treatment).
- Touches: the p_tf slot (or p_cryo, per Q2), its doc, oracle/runner, regen, SV-031. The p_tfcool/p_cryo neighbors change **only if** the Q2 ruling re-scopes them.
- Cost: smallest honest step; the calc structure is new (design decides library vs instance placement) but the blast radius is the WI-023-mapped chain (recirc → p_net → q_eng → LCOE denominator; capital invariant).
- Limitation: leaves the 15.8 MW of 1costingFE defaults in place with whatever double-count/overlap the Q2 ruling accepts or documents.

**Option (b) — full parasitic decomposition touching the other slots.**
- Everything in (a), plus re-deriving or re-parameterizing p_tfcool, p_cryo, p_pump, p_trit, p_house, f_sub as explicit assumption parameters or derived sub-chains.
- Honest content warning (from Chain C): there is **no admissible Stellaris data** behind any of those slots — the paper defers parasitics wholesale. Option (b) mostly converts 1costingFE constants into named assumption parameters; it adds structure and owner visibility, not sourced values.
- Cost: larger edit surface (six slots + docs + oracle/runner), larger design and checkpoint burden (an assumption ruling per slot), same standing bars. Headline movement depends entirely on the per-slot rulings.

## Modeling Requirements

Written to hold under either scope option; scope-conditional parts are marked. EARS format per the requirements-tracking skill.

#### MR-WI024-1: Derived, not bound — the parasitic chain is modeled

The model SHALL compute the coil/cryo parasitic electrical power through an explicit derivation chain (heat-load links → heat load at 20 K → cryo-plant electrical via a COP treatment, plus the coil-conduction disposition), replacing the WI-023 `p_tf = 0.0` stopgap, with the chain's structure and placement (library calc def vs instance-local) decided at design under the ratified checkpoint scope.

- **Type**: Functional | **Priority**: Must | **Derives from**: [OWNER] intent (epic WI-024 entry); RQ-1/RQ-2
- **Validation**: SV-031; run_stellaris bit-exact vs oracle (rel 1e-9)

#### MR-WI024-2: Every link sourced, computed, or an explicit owner-approved assumption

Each link in the implemented chain SHALL be exactly one of: (i) an admissibly sourced value verified against page images or the raw PDF (never extracted table text), (ii) computed from sourced geometry by stated arithmetic, or (iii) an explicit assumption parameter carrying the owner's approval (checkpoint or design ruling, dated) and a doc stating that no admissible source value exists. The model SHALL contain no silent defaults and no values borrowed from inadmissible machines (W7-X, the 1costingFE dipole eta_cryo comment) — those may inform shape only.

- **Type**: Traceability / Constraint | **Priority**: Must | **Derives from**: [OWNER] standing no-fallbacks rule; MR-4; WI-022/023 extraction-errata lessons
- **Validation**: per-link citation inspection at review against this spec's provenance table

#### MR-WI024-3: The double-counting ruling is implemented and documented

The implemented binding set SHALL reflect the owner's checkpoint ruling on slot placement and overlap (which slots the derivation replaces vs coexists with), and the doc of every affected slot (`p_tf`, `p_tfcool`, `p_cryo`, and under option (b) the rest) SHALL state what that slot covers after WI-024, so no future reader re-discovers the overlap question.

- **Type**: Functional / Traceability | **Priority**: Must | **Derives from**: [AGENT] WI-023 double-counting finding (alignment brief); checkpoint Q2 ruling
- **Validation**: doc inspection at review; SV-031 records the executed slot set

#### MR-WI024-4: Standing bars hold; handshake safety re-derived at design

The change SHALL hold the inherited bars: L1 = 0 over the model set with the L2–L6 offender list exactly the 6 pre-existing (`mfe_plant.sysml:329/335/340`, `ife_plant.sysml:33/41`, `hif_plant.sysml:205` — compare the offender list, not level-summary flags), zero new; regen via the sysml-codegen snapshot + `bridge_v11_generate.py` with `preserve_handwritten=True` and the WI-022 handwritten reactivity impl surviving content-identical; `run_stellaris.py` bit-exact vs the updated oracle at rel 1e-9; IFE anchors unchanged (`run_anchors.py`: 252.30/68.69/270.12 $/MWh, Meier 4.735 c/kWh); pytest tally unchanged (2 failed + 18 errors pre-existing baseline); canonical↔staged mirroring. The Anchor A handshake (`handshake_1costingfe.py` unedited, empty `git diff` on `handshake_comparison.json`) is the target bar, **but the WI-023 safety argument does not carry**: the script injects `pb__p_tf` (line 216) and a new calc structure can change the injection surface — the design SHALL re-derive handshake safety for the ratified structure before implement, and surface any injection-surface change rather than assert safety.

- **Type**: Constraint | **Priority**: Must | **Derives from**: [INHERITED: handoff] standing bars; alignment brief premise caveat (handshake re-derivation)
- **Validation**: SV-031; SV-025/026 byte-identical (or the design-surfaced successor bar if the injection surface changes — owner sees it first); L1–L6 offender-list compare; SV-023 unchanged

#### MR-WI024-5: Citations and clean-room

Every changed value and doc SHALL carry an MR-4 `Source / Ref / Basis` citation resolving to an admissible Stellaris source image or the raw PDF, or to 1costingFE at `0254385`. No ARIES-CS-informed source may be read or cited (PROTOCOL.md §3). Assumption parameters cite the approval, not a source.

- **Type**: Traceability | **Priority**: Must | **Derives from**: MR-4; PROTOCOL.md §3
- **Validation**: citation inspection at review

#### MR-WI024-6: SV-016 is recorded against, never fitted

At close, the item SHALL record the derived q_eng against the SV-016 band (~10–40, `pending`) and flag it for the owner; the band SHALL NOT be adjusted, resolved, or reworded by this item.

- **Type**: Constraint | **Priority**: Must | **Derives from**: [OWNER] 2026-07-18 SV-016 ruling
- **Validation**: matrix inspection at close

## Scope Boundaries

**In scope (invariant under either option):**
- The derivation-chain model per the ratified scope: new calc structure (placement per design), the `p_tf`-slot resolution, per-link citations, assumption parameters as ruled.
- `models/designs/stellarator_09/stellarator_plant.sysml` + staged twin: affected bindings and docs (at minimum the p_tf block :434-454; p_tfcool/p_cryo docs per the Q2 ruling).
- Oracle (`verify_stellaris.py`) and runner (`run_stellaris.py`) re-baseline; regenerated pipeline artifacts (regen only, never hand-edited).
- `modeling_project/VALIDATION_MATRIX.md` — SV-031 (created by this spec, `pending`).
- Library power-balance calc (`mfe_power_balance.sysml`) **only if** the design ruling places the chain there; the recirculating-sum formula itself (1costingFE-faithful) is not up for change.

**In scope only under option (b):** the p_tfcool/p_cryo/p_pump/p_trit/p_house/f_sub bindings and docs as explicit assumption parameters or derived sub-chains, per the per-slot rulings.

**Out of scope:**
- The STALE-BASIS pass-through recompute (buildings/preconstruction/O&M at p_net 575.3) — sequenced after WI-024 ([OWNER]); not registered yet, register at pick-up.
- Adjusting the SV-016 band (MR-WI024-6).
- Magnet capital cost, the B binding, geometry, confinement — all settled by WI-020..023; p_tf was capital-invariant (WI-023 verified) and this item does not touch capital formulas.
- Heating wall-plug (`p_input/eta_pin`) — sourced, untouched.
- Cryoplant **capital/building** cost treatment (1costingFE CAS21 via `coil_material`) — cost side is not this item; this item is the power side.

## Success Criteria

1. **SV-031 (created `pending` by this spec):** the coil/cryo parasitic electrical power is a computed output of the derivation chain (not a bound constant), every link graded per this spec's provenance table with owner-approved assumptions explicit; executed headline (p_net, rec_frac, q_eng, LCOE) recorded at implement per the ratified scope, bit-exact vs oracle at rel 1e-9. Expected direction from printed loads only: derived cryo-electrical ~0.4–0.9 MW (COP-assumption-dependent); actual headline movement depends on the Q2 slot ruling (a re-scope of p_tfcool 15 MW moves p_net far more than the derived term itself). No target value is set — the honest output is whatever the ratified chain computes.
2. **Standing bars** (MR-WI024-4): L1–L6 offender list = the 6 pre-existing, zero new; regen with handwritten-impl survival; pipeline bit-exact rel 1e-9; IFE anchors and pytest tally unchanged.
3. **Handshake:** SV-025/026 byte-identical, under a design-stage re-derived safety argument for the new calc structure; any injection-surface change is surfaced before implement, not absorbed.
4. **Docs:** every affected slot states its post-WI-024 coverage (MR-WI024-3); no silent defaults anywhere in the chain (MR-WI024-2); q_eng recorded against SV-016 and flagged (MR-WI024-6).

## Checkpoint Rulings ([OWNER] 2026-07-18)

1. **Scope: option (a)** — cryo-electrical derivation only, filling the coil-power gap. Option (b) not selected (recorded above as the considered alternative; the other slots are untouched by this item).
2. **Slot placement, double-counting resolution, COP treatment (form and value), winding-volume route, and unprinted-loads treatment are design decisions**, delegated to `/design-model`.
3. **Handshake successor bar accepted ([OWNER] 2026-07-18, post-design):** the design-surfaced deviation (D7) — the injection surface necessarily changes when a slot becomes chain-computed — is ratified with the successor bar: `handshake_1costingfe.py` edited only within the `set_1cfe_inputs` injection map (no comparison-logic change), `git diff exploration/stellarator_e2e/handshake_comparison.json` empty after the run (SV-025/026 byte-identical). This supersedes the "handshake unedited" wording in MR-WI024-4. [OWNER-VERBATIM]: *"spec should capture the outcomes — how the model is built should be done with the expertise of SysML modeling."* On placement specifically ([OWNER], non-binding lean): *"I like the idea of looking at `p_cryo`, but this is really a modeling decision that should be resolved during design — you need to look at the implications and what has the most semantic value and will make sense moving forward."* Design resolves each with documented basis; assumption-parameter values set at design (sanctioned by this ruling), still subject to the no-fallbacks rule's honesty bar: explicit, cited as assumptions, never silent.

## Assumptions & Risks

1. **The derived value from printed loads is small (~1 MW-scale), so the honest headline movement is dominated by the Q2 slot ruling** (certain in direction, ruling-dependent in magnitude). Stated up front so the checkpoint is decided on numbers: at unchanged neighbors, p_net moves ≤ ~1 MW and LCOE ~$0.2/MWh; a p_tfcool re-scope could move p_net upward by ~15 MW.
2. **Lower-bound honesty** (certain): the printed heat loads understate the true cryo load (the paper says so). Whatever the Q5 ruling, the model documents the bound explicitly — the item's claim is "derived from what the source prints, with stated assumptions", not "the true parasitic power".
3. **Handshake injection-surface risk** (medium likelihood, contained): a new calc feeding the recirc sum may alter what `handshake_1costingfe.py` must inject. Design re-derives; any change is surfaced pre-implement (MR-WI024-4). Blast radius otherwise verified at WI-023: recirc → p_net → q_eng → LCOE denominator; capital invariant.
4. **Circumference approximation** (low impact, documented): the 25 m "typical" circumference is printed but approximate; per-coil values are not printed. The mass cross-check (implied density ~7500 kg/m³, consistent with Table 7) bounds the plausibility; the residual is documented or absorbed per Q4.
5. **codegen coverage of the new chain** (low–medium): the chain is new calc structure through regen; constructs stay within the proven set (per the epic's codegen risk posture), and the WI-022 handwritten-impl survival gotcha is a named bar. Any unsupported construct is a finding, not a workaround.
6. **q_eng will move again and may still sit below SV-016's band** (likely): recorded and flagged, never fitted (MR-WI024-6).

## Traceability

**Sources (all verified at this spec):**
- Stellaris design paper — `knowledge/concept_research/09-qi-stellarator-hts/iter-01/sources/stellaris-design-details/images/`: Table 6 `page_020_table_0.png` (35.5 W/m³ winding-pack heating; TBR 1.074); Table 7 `page_021_table_0.png` (winding-pack material fractions 9/35/12/36/8%); Table 8 `page_022_table_0.png` (per-unique-coil turns, cross-section side lengths 360→300 mm, no-casing masses 24.2→17.0 t, total energy 110.58 GJ); Table 2 `page_002_table_0.png` (48 coils, B₀ 9.0 T, peak conductor 24.9 T, 15.4 MA, 111 GJ).
- Published PDF `knowledge/concept_research/09-qi-stellarator-hts/iter-02/sources/publikationen-1000179851-172386752/tmpissrtbos/raw.pdf` (registered in `SOURCE_INDEX.md`): §2.8 (35.5 W/m³, 20 K, EU DEMO ~50 W/m³ reference, cryo-plant qualitative efficiency remark); §2.9 (20 mm × 20 mm turn cell; square winding pack; 25 m typical circumference; 48 = 4 × 12 coils, 6 unique; 20 K supercritical He 15–20 bar; 10 W/joint → ~7.5 kW coil-set steady-state, "negligible"; the future-studies deferral of total coil/case/structure nuclear heating); conclusion (parasitic-electricity deferral).
- 1costingFE @ `0254385`: `src/costingfe/data/defaults/steady_state_stellarator.yaml:17-24` (the six parasitic defaults); `src/costingfe/types.py:229-231`, `layers/physics.py:294-324` (slot semantics and the recirc sum); `defaults.py:601-616` (`recirc_power_factor = 0` for SC; `cryo_temp_k = 20.0` for rebco); `layers/tokamak.py:182-186` (copper-only resistive recirc model); `model.py:1229-1233` (cryoplant as CAS21 building-cost driver only); `data/defaults/steady_state_dipole.yaml:52-53` (the machine-specific eta_cryo comment — shape reference only).

**Downstream impacts:** WI-018 instance + staged twin, `mfe_power_balance.sysml` (design-dependent), oracle/runner, regenerated pipeline artifacts, `VALIDATION_MATRIX.md` (SV-031; SV-016 flag at close), `.project/CURRENT_WORK.md` headline, the STALE-BASIS recompute item (sequenced after, consumes the settled p_net).

**Applicable project rules:** MR-4 (citations), PROTOCOL.md §3 (clean-room — this spec read only admissible sources), no-fallbacks (all unsourced links surfaced as options, none chosen), capture-fidelity (provenance graded per link; extraction errata surfaced, sources not silently corrected).

## Related Artifacts

- Alignment brief: `work/orchestration/recirc-power-derivation.md`
- Epic: `work/backlog/epic-mfe-cost-modeling.md` (Item WI-024)
- Evidence authority record: `work/completed/20260718_WI-023_magnet-field-errata-B9/spec.md` §Sweep Findings; executed baseline in that item's `plan.md` Implementation Record; audit `work/analysis/20260718-105435_audit_WI-023_magnet-field-errata-B9.md`
- Current stopgap binding: `models/designs/stellarator_09/stellarator_plant.sysml:434-454`
- Design: `work/active/WI-024_recirc-power-derivation/design.md` (to be created after the owner checkpoint)
- Plan: `work/active/WI-024_recirc-power-derivation/plan.md` (to be created)
