---
Status: complete
Created: 2026-07-18
Updated: '2026-07-18'
Related Artifacts:
  Spec: ./spec.md
---

> Process note: the owner checkpoint ran after `/spec-model` (2026-07-18) and ratified Option (a) — cryo-electrical derivation only — and delegated slot placement, the double-counting resolution, the COP treatment (form and value), the winding-volume route, and the unprinted-loads treatment to this design ([OWNER-VERBATIM]: "spec should capture the outcomes — how the model is built should be done with the expertise of SysML modeling"). This design resolves all four with documented bases. **One flagged deviation for the orchestrator: the handshake injection surface changes (D7) — the spec's "handshake_1costingfe.py unedited" bar cannot hold under any structure that actually models the chain; a successor bar is proposed below and must be seen before implement (MR-WI024-4).**

# WI-024 Design: Recirculating-Power Derivation — Cryoplant Electrical Chain

**Required Reading: `knowledge/holdout/aries-cs/PROTOCOL.md`** — demo model-development session; §3 barred paths not read. Physics from the admissible Stellaris sources (Table 6/8 images + iter-02 raw.pdf, all re-verified this session); engineering/cost from 1costingFE @ `0254385`.

## Overview

One new library calc def, `'Cryoplant Electrical Power'` (new file `models/library/analyses/mfe_cryo_plant.sysml`), computes the cryoplant wall-plug electrical power from the cold-mass heat load:

```
p_cold = (q_nuc * vol_cold * 1e-6 + p_fixed) * f_uplift        [MW at T_cold]
cop    = f_carnot * T_cold / (T_amb - T_cold)                  [Carnot x fraction]
p_elec = p_cold / cop + p_direct                               [MW wall-plug]
```

The generic plant (`mfe_plant.sysml`) gains a `cryo_elec` calc usage fed by seven new dormant-default plant attributes, and the power balance's `in p_cryo = p_cryo` rewires to `in p_cryo = cryo_elec.p_elec` — the derived cryoplant electrical lands in the **p_cryo slot** (D1). The recirculating-sum formula in `mfe_power_balance.sysml` is untouched.

The Stellaris instance binds the chain: q_nuc = 35.5 W/m³ (SOURCED, Table 6 image), vol_cold = 136.56 m³ (COMPUTED, Table 8 cross-sections × 8-fold symmetry × 25 m printed circumference), p_fixed = 0.0075 MW (SOURCED, §2.9 joint losses), f_uplift = 1.0 (explicit lower-bound seam, D6), T_cold = 20 K (SOURCED), T_amb = 300 K (standard-ambient assumption), f_carnot = 0.20 (THE assumption parameter, D4), p_direct = 0.0 (the 1costingFE 0.8 MW generic default is retired — same physical quantity, D2). `p_tf` stays 0.0 but its doc is rescoped from "deferral stopgap" to a modeled zero: superconducting coils draw no steady-state resistive drive power; the ~7.5 kW joint dissipation is counted as heat at 20 K inside this chain.

Derived value: **p_cryo = 0.8643516 MW** (vs the 0.8 default it replaces). Expected headline movement (oracle-exact, computed this session): p_net 915.145 → **915.081 MW**, q_eng 6.6093 → **6.6067**, rec_frac 0.15130 → **0.15136**, LCOE 201.458 → **201.472 $/MWh**; V, p_fus, p_th, p_et, all capital accounts unchanged (capital was p_tf/p_cryo-invariant, WI-023-verified).

The whole architecture was spiked end-to-end this session on a scratch copy of the staged models: parse (L1–L3 clean), snapshot classification (8 literal leaves + 1 chain, exactly as designed), V11 bridge (exactly 3 offenders, package emitted), and the generated module executed bit-equal to the oracle mirror at both the Stellaris point and the handshake identity point.

## Research Findings

**Source verification (this session, per MR-WI024-2/5 — images and raw.pdf only, never extracted table text):**

- Table 8 image (`iter-01/sources/stellaris-design-details/images/page_022_table_0.png`): cross-section side lengths **360/360/340/340/320/300 mm**, turns 324/324/289/289/256/225, no-casing masses 24.2/25.4/21.6/21.5/19.0/17.0 t, total energy 110.58 GJ (2.76 GJ per coil) — all re-read from the image this session.
- Table 6 image (`page_020_table_0.png`): "Mean cryogenic nuclear heating (winding pack) [W/m³] **35.5**".
- raw.pdf §2.9 (text extracted from the PDF this session): "a typical circumference of **25 m**"; "Each turn is sized at **20 mm × 20 mm**"; "10 W per joint … approximately **7.5 kW** steady-state losses for the entire stellarator coil set … negligible"; "**48 coils divided into four periods, with each period containing 12 coils: six independent and six mirrored**" (→ each unique coil appears **8** times); "The coils are cooled to **20 K** using supercritical helium"; the lower-bound deferral verbatim: "this steady state electrical power should be smaller than the total nuclear heating of the coils, the coil cases, and the remaining 20 K cooled parts of the support structure, which will be examined in future studies".
- raw.pdf §2.8: 20 K operation "offers an increase in efficiency of the cryogenic plant" (qualitative only — no COP number anywhere, confirming spec link A4).
- 1costingFE @ `0254385` (re-read this session): `defaults.py:610-614` — `rebco_hts` has `cryo_temp_k=20.0`, `recirc_power_factor=0.0` (SC coils draw no resistive power in 1cfe's own physics); `steady_state_dipole.yaml:52-53` — 1cfe's own `p_cryo` slot is "Cryogenic **wall-plug** power" computed from heat load × eta_cryo (slot-semantics witness only; the dipole value is inadmissible); `steady_state_stellarator.yaml:14-24` — `p_cool = 15.0` and `p_cryo = 0.8` carried **side by side**, so in 1cfe's intent they are disjoint loads.

**Codegen mechanics (verified against the committed `stellarator.snapshot.json` and by spike):**

- pb's parasitic inputs are `literal` bindings (settable leaves in `system_design.json`) because the instance redefines the plant attributes with literals; calc-output bindings are `chain` (wired channels, not settable). Every recirc-sum slot is currently a leaf the handshake injects — so **any** structure that computes a slot value in a calc removes that slot's leaf. There is no placement that both models the chain at pipeline time and keeps the handshake injection map unchanged (the basis for D7).
- Instance-level calc usages are proven (`wall_load_calc`, WI-018), and attribute-mediated chains at plant level are proven (`blanket_cost.p_th` → `stellaris.p_th`).

**End-to-end spike (scratch copy of the staged tree + the exact edits below; no repo file touched):**

1. Parse: L1/L2/L3 all pass on the prototype package (0 errors, 0 warnings).
2. Snapshot: `cryo_elec` module appears with all 8 inputs classified `literal` (baked instance values), and `pb.p_cryo` classifies `chain → cryo_elec.p_elec`. No other binding changes.
3. Bridge: **exactly 3 V11 offenders** (the known rollup keys), bridged, package emitted. Generated-inputs key diff vs committed: +8 `cryo_elec__*` leaves, −`pb__p_cryo`, −3 `mfe_plant__MFE_Power_Plant__p_th/p_the/p_et` (the last three are the known regen-reset of the post-run harness-glue fields, re-added by runner glue — WI-023 record).
4. The generated `cryoplant_electrical_power_impl.py` is **AUTO_IMPLEMENTED = True** (pure arithmetic — no new handwritten function; `IMPLEMENTATION_BACKLOG.md` still lists exactly 1 function, DT_Fusion_Power).
5. Executed in the pipeline exec venv: Stellaris point returns `0.8643515999999999`, **bit-equal** to the oracle mirror; handshake identity point (heat inputs zeroed, `p_direct = 0.8`) returns exactly `0.8` (see D7).

**Snapshot-flow gotcha found and resolved this session:** running `sysml-codegen snapshot` with `--design-path-filter stellarator_09` drops the analyses/generic-plant design-attribute groups from the snapshot and produces 8 spurious V11 offenders (the 4 BOP `power`/`n_mod` references lose their dangling-schema coverage). The WI-022/023 flow used **no filter**. The regen command at implement must be plain `sysml-codegen snapshot -m <staged models> -o stellarator.snapshot.json`. (First observed as an 11-offender bridge abort; a control run on the unedited tree reproduced it, and the unfiltered snapshot restored the exact 3-offender baseline — this is a flag error, not toolchain drift. sysml-codegen HEAD `6db3212` verified working.)

**Expected headline is oracle-exact, computed this session** (scratch copy of `verify_stellaris.py`; the unmodified oracle first reproduced the WI-023 baseline to the cent):

| quantity | WI-023 baseline | WI-024 expected | moved by |
|---|---|---|---|
| p_cryo (slot input) | 0.8 (1cfe default) | **0.8643516** (derived) | the chain |
| p_net [MW] | 915.145439 | **915.081088** | recirc +0.0644 |
| q_eng | 6.609268 | **6.606662** | recirc |
| rec_frac | 0.151303 | **0.151362** | recirc |
| LCOE [$/MWh] | 201.457898 | **201.472065** | denominator energy ↓ |
| V / p_fus / p_th / p_et | 425.0 / 2748.06 / 3238.12 / 1078.29 | unchanged | — |
| total / magnet capital | $12.6015B / $6.3235B | unchanged | — (capital reads no parasitic slot) |

Direction is honest: LCOE up. q_eng 6.607 still sits far below SV-016's ~10–40 band — recorded and flagged at close, never fitted (MR-WI024-6).

## Design Decisions

**D1 — placement: the derived cryoplant electrical lands in the `p_cryo` slot; `p_tf` stays 0.0 as a modeled zero.** Semantic grounds (the owner's delegation asked for exactly this): 1costingFE's own `p_cryo` slot is the cryoplant wall-plug electrical — its dipole defaults document the slot as "Cryogenic wall-plug power" computed from heat load × plant efficiency (`steady_state_dipole.yaml:52-53`, semantics witness only), which is precisely what Chain A derives. `p_coils`/`p_tf` is electrical power delivered **to** the coils, which 1cfe's own physics sets to zero for superconductors (`recirc_power_factor = 0.0`, `defaults.py:611-614`; `tokamak.py:182-186`). Putting a refrigeration wall-plug load in the coil-drive slot would mislabel the physics and leave `p_cryo` carrying a generic default for the same quantity. This also matches the owner's recorded non-binding lean toward `p_cryo`. Moving forward, the semantics stay clean: `p_tf` = coil electrical drive (zero for SC concepts, computable for copper), `p_cryo` = cryoplant wall-plug (derived here).

**D2 — double-counting resolution: `p_cryo = 0.8` retired (replaced by the derivation); `p_tfcool = 15.0` kept with a documented disjoint reading; `p_tf = 0.0` rescoped from stopgap to modeled zero.**
- The 1cfe `p_cryo = 0.8` generic default and the derived chain output are the **same physical quantity** (cryoplant wall-plug electrical) — coexisting would double-count by construction, so the default is dropped and the slot takes the machine-specific derivation. The retirement is recorded in the instance's `p_direct = 0.0` binding doc (D3 keeps the additive direct term for concepts that specify cryo electrical directly).
- `p_tfcool` (1cfe `p_cool`, "Cooling power"): 1cfe's own stellarator defaults carry `p_cool = 15.0` **and** `p_cryo = 0.8` side by side (`steady_state_stellarator.yaml:20,24`), so in the source's intent they are disjoint — `p_cool` is read as the non-cryogenic cooling-system electrical (component/room-temperature cooling loops), not the 20 K refrigeration. No admissible evidence supports re-scoping 15 MW away, and dropping it would be an invented 15 MW optimism (no-fallbacks). Kept at 15.0; its doc now states the post-WI-024 coverage and the residual: `p_cool`'s upstream composition is undocumented, so any cryo-compressor share it contains would overlap the derived `p_cryo` — an overlap whose direction is conservative (recirc overstated, LCOE up), documented rather than silently resolved.
- `p_tf`: the only printed steady-state coil electrical dissipation is the ~7.5 kW joint loss, which this chain counts as heat at 20 K (`p_fixed`); as direct electrical it is negligible (§2.9, PDF-confirmed) and 1cfe's SC model agrees (factor 0). The doc rewrite turns WI-023's "known-optimistic stopgap pending WI-024" into a settled statement with those citations. The other slots (`p_pump`, `p_trit`, `p_house`, `f_sub`) are untouched (ratified Option (a)).

**D3 — structure: library calc def + generic-plant usage + chain wiring; additive `p_direct` instead of a conditional bypass.** ADR-002 routes any reusable, non-trivial calculation to a library calc def (`MODELING_PROCESS.md` §2.2.1 — an instance expression may not compute on calc outputs or reach through dotted paths), and MR-3/AD-007 put concept-agnostic definitions in the library: every MFE concept has a cryoplant, and the calc carries no Stellaris numbers. The usage lives in the generic plant (the `fusion`/`rb` idiom — plant attributes with dormant defaults, instance overrides), keeping the whole construct set inside what is already proven through the bridge: literal leaf bindings, one calc-to-calc chain, pure-arithmetic auto-codegen module (spike-proven end to end, including AUTO_IMPLEMENTED). The dormant path needs no conditional: a concept that binds nothing gets `p_elec = 0/cop + 0 = 0`; a 0D concept that knows its cryo electrical directly binds `p_cryo` (the direct term) and leaves the chain dormant — the additive form replaces WI-022's sentinel-bypass pattern without introducing a conditional (which would have forced the whole calc `manual_required`). `f_carnot` defaults 1.0 (dormant-safe, the WI-022 `T_i0 = 1.0` precedent — mode is selected by the heat inputs, never by the efficiency). Rejected: instance-local calc usage with `:>> p_cryo = cryo.p_elec` (identical handshake cost, but the instance-level chain-redefinition classifier path is unproven, and the chain is generically useful); extending 'MFE Power Balance Calc' in place (touches the 1cfe-faithful sum the spec keeps out of scope, and a bypass conditional would de-automate the whole power balance); static instance expression baked at snapshot (violates ADR-002's calc-output rule and leaves the chain unexecuted at pipeline time).

**D4 — COP treatment: Carnot-at-T_cold × fraction-of-Carnot; f_carnot = 0.20.** The Carnot form splits the treatment into pure arithmetic (COP_carnot = T_cold/(T_amb − T_cold) — COMPUTED, and reusable at any temperature by any concept) plus exactly one dimensionless assumption with a well-understood engineering meaning. A direct specific-power parameter (form i) would bury the temperature dependence inside the assumption and not generalize across concepts. Value: **f_carnot = 0.20**, an explicit assumption sanctioned by the spec's Checkpoint Ruling 2 (design ruling, 2026-07-18). Engineering basis, stated in words per the ruling: general cryogenic engineering practice — large-scale cryogenic refrigeration plants typically achieve roughly 15–30% of Carnot efficiency, degrading at smaller capacity; 0.20 sits at the conservative (higher-power) end of that band. At 20 K / 300 K it yields COP = 0.20 × 20/280 = 1/70, i.e. a specific power of 70 W_e per W at 20 K — inside the spec's own order-of-magnitude illustration band (30–70). No admissible machine-specific value exists (§2.8 is qualitative; W7-X and the 1cfe dipole `eta_cryo` comment are value-inadmissible, shape only — this value was set without them). T_amb = 300 K is a standard-ambient reference assumption (same ruling); T_cold = 20 K is SOURCED (§2.8/2.9, corroborated by 1cfe `cryo_temp_k = 20.0` for rebco_hts).

**D5 — winding-pack volume: COMPUTED, bound as the literal 136.56 m³ with the full arithmetic and cross-checks in the binding doc.** The computed route wins over an assumption parameter because every input is printed and two independent witnesses agree: Table 8's six cross-section side lengths (0.36/0.36/0.34/0.34/0.32/0.30 m, square winding pack per §2.9) are reproduced **exactly** by turns × (20 mm)² for all six coils, and the §2.9 symmetry statement (48 = 4 periods × (6 independent + 6 mirrored)) fixes the ×8 multiplier. Arithmetic: Σ side² = 2×0.36² + 2×0.34² + 0.32² + 0.30² = 0.6828 m²; × 8 × 25 m = **136.56 m³**. The 25 m circumference is printed but explicitly "typical" — the documented weak link (per-coil circumferences are not printed; the coils span ~7×5×10 m, so per-coil variation of a few percent is plausible and flows linearly into p_cold). Cross-check bounding the plausibility: Table 8 no-casing masses total 128.7 t × 8 = 1029.6 t → implied density 1029.6e3/136.56 ≈ 7540 kg/m³, consistent with the Table 7 material mix (steel 36%, copper 35%, solder 12%, tape 9%, He 8%). The mass-based route was rejected as primary (needs assumed handbook densities → assumption-grade); it serves as the cross-check instead. Bound as a literal (not an in-model expression) because ADR-002 permits only same-part-sibling arithmetic in designs and the decimal arithmetic is exact as stated — the doc carries the derivation, the grade is COMPUTED.

**D6 — unprinted heat loads: excluded (lower bound), expressed as the explicit seam f_uplift = 1.0.** The paper itself defers casing/cold-structure/support nuclear heating, current-lead and radiation loads to future studies (§2.9, quoted verbatim in the binding doc), so the printed-loads total (≈12.35 kW) is a knowing lower bound. No admissible basis exists for an uplift value, and inventing one (e.g. "2×") would put an unsourced number in the middle of an otherwise sourced chain — worse than an honest, loudly documented bound (the WI-023 honesty pattern, and spec Assumption 2 anticipates exactly this). The exclusion is implemented as an explicit multiplier bound to 1.0 rather than omitted structure, so the gap has a name, a doc, and an owner-adjustable seam; the citation is the design ruling (2026-07-18), not a fake source. Consequence stated plainly: the derived 0.864 MW understates the true cryoplant load by the unprinted-loads factor; the model's claim is "derived from what the source prints, with stated assumptions".

**D7 — handshake safety, re-derived for this structure (MR-WI024-4) — FLAGGED DEVIATION: the injection surface changes.** The WI-023 argument ("instance rebinds can't leak — the handshake injects the leaves") does not extend here and no honest structure preserves it: wiring the chain into the recirc sum necessarily converts the `pb__p_cryo` leaf into a chain-wired channel (spike-verified), and every recirc slot is handshake-injected, so this holds for any slot choice. The Anchor A reproduction argument under the new structure: the handshake's injection map gains the identity path — zero the three heat inputs and feed 1cfe's `pb["p_cryo"]` through the additive `p_direct` term. The chain then computes `((0×0)×1e-6 + 0)×f_uplift/cop + p_cryo_1cfe`, which is bit-exact `p_cryo_1cfe` in IEEE arithmetic (multiplication by zero, division of exact zero, addition to zero are all exact) — **executed proof in the spike: the generated module returned exactly 0.8**. Every downstream float therefore matches the WI-023 record bit for bit, and `handshake_comparison.json` (which records no injected key names) stays byte-identical. Required edit, confined to `set_1cfe_inputs`: replace line 219's `f"{P}pb__p_cryo": pb["p_cryo"]` with `f"{P}cryo_elec__q_nuc": 0.0, f"{P}cryo_elec__vol_cold": 0.0, f"{P}cryo_elec__p_fixed": 0.0, f"{P}cryo_elec__p_direct": pb["p_cryo"]` (the baked f_uplift/T/f_carnot values are inert at zero heat — documented in the edit comment). All other injections (`pb__p_tf` line 216, `magnet__B` line 271, the rest of the pb leaves) are untouched — the spike's generated-key diff shows no other surface change. **Proposed successor bar** (replaces "handshake_1costingfe.py unedited"; owner/orchestrator sees this before implement): *handshake edited only within the `set_1cfe_inputs` injection map (no comparison-logic change), and `git diff exploration/stellarator_e2e/handshake_comparison.json` empty after the run (SV-025/026 byte-identical).* Precedent: WI-021 moved the injection surface the same way when volumes became computed (direct volume injections → `rb__*` leaves).

## Proposed Design

### 1. Library calc def (new file `models/library/analyses/mfe_cryo_plant.sysml`; staged twin `exploration/stellarator_e2e/models/analyses/mfe_cryo_plant.sysml`, identical)

```sysml
package mfe_cryo_plant {
    private import ScalarValues::*;

    calc def 'Cryoplant Electrical Power' {
        doc /*
        Cryoplant wall-plug electrical power [MW] from the cold-mass heat
        load (WI-024). Steady-state refrigeration power balance:
            p_cold = (q_nuc * vol_cold * 1e-6 + p_fixed) * f_uplift
            COP    = f_carnot * T_cold / (T_amb - T_cold)   (Carnot x fraction)
            p_elec = p_cold / COP + p_direct
        p_direct is an additive direct term for concepts that specify the
        cryoplant electrical outright (no chain); with zero heat inputs the
        calc passes p_direct through exactly. f_uplift names the seam for
        heat loads missing from the inventory (>= 1). Dormant-safe defaults:
        an unbound concept computes p_elec = 0; f_carnot defaults 1.0 (not 0)
        so the dormant COP stays defined — the mode is selected by the heat
        inputs, never by the efficiency (WI-022 T_i0 precedent).
        Output feeds the power-balance p_cryo slot ("cryogenic system
        power"), which 1costingFE's own defaults document as the cryoplant
        wall-plug electrical.
        **Source**: /home/reid/1cfe/1costingfe/src/costingfe/layers/physics.py
        **Ref**: physics.py:321-323 (p_cryo in the recirculating sum);
            steady_state_dipole.yaml:52-53 (slot semantics: "Cryogenic
            wall-plug power" = heat load x plant efficiency — semantics
            witness only, value inadmissible)
        **Basis**: reversed-Carnot reference cycle x fraction-of-Carnot;
            concept-agnostic (MR-3) — all values bound by instances
        */

        in attribute q_nuc : Real default 0.0;     // volumetric nuclear heating at the cold mass [W/m^3]
        in attribute vol_cold : Real default 0.0;  // heated cold-mass volume [m^3]
        in attribute p_fixed : Real default 0.0;   // fixed cold-mass heat loads [MW] (joints, leads)
        in attribute f_uplift : Real default 1.0;  // unprinted-loads multiplier [1] (>= 1)
        in attribute T_cold : Real default 20.0;   // cold-mass operating temperature [K]
        in attribute T_amb : Real default 300.0;   // heat-rejection (ambient) temperature [K]
        in attribute f_carnot : Real default 1.0;  // fraction-of-Carnot plant efficiency [1] (dormant-safe 1.0)
        in attribute p_direct : Real default 0.0;  // directly-specified cryoplant electrical [MW] (additive)

        attribute p_cold : Real = (q_nuc * vol_cold * 1.0e-6 + p_fixed) * f_uplift;
        attribute cop_carnot : Real = T_cold / (T_amb - T_cold);
        attribute cop : Real = f_carnot * cop_carnot;

        out attribute p_elec : Real = p_cold / cop + p_direct;
    }
}
```

(Parse-checked this session: L1/L2/L3 clean. The spike snapshot compiled it FULLY_COMPILABLE — auto-codegen, no handwritten stub.)

### 2. Generic plant (`models/designs/generic_mfe/mfe_plant.sysml` + staged twin, identical)

- Add `private import mfe_cryo_plant::*;` to the import block.
- Re-doc the existing `attribute p_cryo : Real` → `attribute p_cryo : Real default 0.0;  // directly-specified cryoplant electrical [MW] (additive direct term, WI-024)` (the `default 0.0` keeps 0D concepts' dormant path explicit; the comment "cryogenic pumping" was never 1cfe's semantics — `types.py:231` says "Cryogenic system power").
- Add the seven chain attributes (dormant defaults mirroring the calc def):

```sysml
// Cryoplant heat-load chain (WI-024). Dormant by default: a concept that
// knows its cryo electrical directly binds p_cryo (the direct term) and
// leaves these unbound; a concept deriving it binds the chain and zeroes
// p_cryo.
attribute q_nuc_cryo : Real default 0.0;
attribute vol_cold_cryo : Real default 0.0;
attribute p_fixed_cryo : Real default 0.0;
attribute f_uplift_cryo : Real default 1.0;
attribute T_cold_cryo : Real default 20.0;
attribute T_amb_cryo : Real default 300.0;
attribute f_carnot_cryo : Real default 1.0;

calc cryo_elec : 'Cryoplant Electrical Power' {
    in q_nuc = q_nuc_cryo;
    in vol_cold = vol_cold_cryo;
    in p_fixed = p_fixed_cryo;
    in f_uplift = f_uplift_cryo;
    in T_cold = T_cold_cryo;
    in T_amb = T_amb_cryo;
    in f_carnot = f_carnot_cryo;
    in p_direct = p_cryo;
}
```

- Rewire one pb binding: `in p_cryo = p_cryo;` → `in p_cryo = cryo_elec.p_elec;` (the only power-balance-block change; the calc def and sum formula untouched).

### 3. Stellaris instance (`models/designs/stellarator_09/stellarator_plant.sysml` + staged twin, identical regions)

**p_tf doc rewrite (:434-454)** — from deferral stopgap to modeled zero. Content: superconducting coil set, steady-state DC operation — no resistive drive power (1cfe's own SC model: `recirc_power_factor = 0.0`, `defaults.py:611-614`); the one printed steady-state electrical dissipation, ~7.5 kW joint losses, is carried as heat at 20 K inside the WI-024 cryo chain (`p_fixed_cryo`), not as coil electrical; current-lead and power-supply standing losses are not printed in any admissible source and are part of the chain's documented lower bound. One history line compresses the WI-023 phantom-111 story. MR-4 cite: raw.pdf §2.9 (joints "negligible") + `defaults.py:611-614`; Basis: modeled zero for a superconducting coil set — coil-adjacent parasitic load carried by the derived p_cryo.

**p_cryo region rewrite (:464-466)** — replaces the 0.8 binding with the direct-term zero plus the seven chain bindings:

```sysml
:>> p_cryo = 0.0 {    // direct cryo-electrical term [MW] — zeroed; chain derives the slot (WI-024).
    doc /*
    The 1costingFE generic default 0.8 MW (steady_state_stellarator.yaml:24)
    is retired: it and the WI-024 derivation are the same physical quantity
    (cryoplant wall-plug electrical — 1cfe's own dipole defaults document
    the p_cryo slot as "Cryogenic wall-plug power"), so coexisting would
    double-count. The power-balance p_cryo slot now receives
    cryo_elec.p_elec, derived from the winding-pack heat load below.
    **Source**: /home/reid/1cfe/1costingfe/src/costingfe/data/defaults/steady_state_dipole.yaml
    **Ref**: steady_state_dipole.yaml:52-53 (slot semantics witness); steady_state_stellarator.yaml:24 (the retired generic default)
    **Basis**: double-counting resolution, WI-024 design D2 (2026-07-18)
    */
}
:>> q_nuc_cryo = 35.5 {   // winding-pack mean nuclear heating [W/m^3].
    doc /* **Source**: stellaris-design-details.md **Ref**: Table 6 image (images/page_020_table_0.png: "Mean cryogenic nuclear heating (winding pack) [W/m^3] 35.5"); sec. 2.8 raw.pdf (magnets at 20 K; EU DEMO ~50 W/m^3 as viability reference) **Basis**: Stellaris winding-pack volumetric nuclear heating at 20 K */
}
:>> vol_cold_cryo = 136.56 {  // total winding-pack volume [m^3] (COMPUTED).
    doc /*
    Computed from sourced geometry (WI-024 design D5): six unique square
    winding-pack cross-sections (Table 8 image side lengths 360/360/340/340/
    320/300 mm) x 8 occurrences each (sec. 2.9: 48 coils = 4 periods x
    (6 independent + 6 mirrored)) x 25 m typical circumference (sec. 2.9,
    printed but approximate — per-coil circumferences are not printed; the
    documented weak link). Sum of side^2 = 2x0.36^2 + 2x0.34^2 + 0.32^2
    + 0.30^2 = 0.6828 m^2; x8 x25 = 136.56 m^3. Cross-checks: each side^2
    equals turns x (20 mm)^2 exactly (sec. 2.9 unit cell; Table 8 turns
    row); Table 8 no-casing masses (128.7 t x 8 = 1029.6 t) imply
    ~7540 kg/m^3, consistent with the Table 7 material mix.
    **Source**: stellaris-design-details.md
    **Ref**: Table 8 image (images/page_022_table_0.png: side lengths, turns, masses); raw.pdf sec. 2.9 (square winding pack; 20 mm x 20 mm unit cell; 25 m typical circumference; 48 = 4 x (6+6) symmetry); Table 7 image (images/page_021_table_0.png: material fractions)
    **Basis**: cross-section x circumference x symmetry; mass cross-checked
    */
}
:>> p_fixed_cryo = 0.0075 {  // resistive-joint losses [MW] at 20 K.
    doc /* **Source**: knowledge/concept_research/09-qi-stellarator-hts/iter-02/sources/publikationen-1000179851-172386752/tmpissrtbos/raw.pdf **Ref**: sec. 2.9 (10 W per joint -> ~7.5 kW steady-state for the entire coil set, "negligible ... within the cooling capacity of existing cryocooler designs") **Basis**: printed coil-set joint dissipation, counted as heat at 20 K */
}
:>> f_uplift_cryo = 1.0 {   // unprinted-loads multiplier — explicit lower bound (WI-024 D6).
    doc /*
    Bound 1.0 = printed loads only, a KNOWING LOWER BOUND: the paper defers
    casing, coil-case, and 20 K support-structure nuclear heating ("will be
    examined in future studies", sec. 2.9 raw.pdf), and current-lead /
    radiation loads are unprinted. No admissible uplift value exists; the
    parameter names the seam so the owner can raise it. Cited to the design
    ruling, not a source.
    **Source**: WI-024 design ruling (D6, 2026-07-18; sanctioned by spec Checkpoint Ruling 2)
    **Ref**: raw.pdf sec. 2.9 (the future-studies deferral)
    **Basis**: explicit assumption parameter — exclude-with-documented-bound
    */
}
:>> T_cold_cryo = 20.0 {    // coil operating temperature [K].
    doc /* **Source**: raw.pdf **Ref**: sec. 2.9 ("cooled to 20 K using supercritical helium at 15-20 bar"; Top set to 20 K); sec. 2.8; corroborated by 1costingFE defaults.py:611 (rebco_hts cryo_temp_k = 20.0) **Basis**: Stellaris HTS coil operating temperature */
}
:>> T_amb_cryo = 300.0 {    // heat-rejection reference temperature [K].
    doc /* **Source**: WI-024 design ruling (D4, 2026-07-18) **Ref**: standard ambient reference for the Carnot COP **Basis**: explicit assumption parameter (standard engineering reference) */
}
:>> f_carnot_cryo = 0.20 {  // fraction-of-Carnot plant efficiency — THE assumption (WI-024 D4).
    doc /*
    Explicit owner-visible assumption (spec Checkpoint Ruling 2 delegated
    value-setting to design; ruled 2026-07-18): no admissible source prints
    a 20 K COP or specific power (sec. 2.8 is qualitative; W7-X and the
    1costingFE dipole eta_cryo comment are value-inadmissible, shape only).
    Basis, general cryogenic engineering practice: large cryoplants achieve
    roughly 15-30% of Carnot; 0.20 taken at the conservative end. Yields
    COP = 0.20 x 20/280 = 1/70, i.e. 70 W_e per W at 20 K.
    **Source**: WI-024 design ruling (D4, 2026-07-18)
    **Ref**: spec sec. Evidence link A4 (the no-admissible-value finding)
    **Basis**: explicit assumption parameter — fraction of Carnot, general practice band
    */
}
```

**p_tfcool doc extension (:455-457)** — binding stays 15.0; the doc gains the post-WI-024 coverage statement (MR-WI024-3): 1cfe carries `p_cool` and `p_cryo` side by side, so this slot is read as the non-cryogenic cooling-system electrical, disjoint from the derived 20 K cryoplant wall-plug now in `p_cryo`; upstream composition undocumented — any cryo-compressor share would overlap the derived term, a conservative-direction residual, documented here so no future reader re-discovers the question.

**Headline doc block + mapping-traps note (:49-70)** — re-baselined to the executed WI-024 numbers at implement (expected: p_net 915.081, rec_frac 0.15136, q_eng 6.6067, LCOE 201.472; capital lines unchanged); history line appended (WI-024 derived the cryo parasitic load, retired the 0.8 default, rescoped p_tf to a modeled zero). The WI-023 p_tf forward-pointer sentences resolve to their settled statements.

**STALE BASIS blocks (:510, :557)** — append the WI-024 move in the established style (p_net 915.145 → 915.081, negligible at the stated precision; recompute still the Stage-3 pass-through item).

### 4. Oracle + runner (`exploration/stellarator_e2e/`)

- `verify_stellaris.py`: add the chain inputs to `IN` (q_nuc_cryo 35.5, vol_cold_cryo 136.56, p_fixed_cryo 0.0075, f_uplift_cryo 1.0, T_cold_cryo 20.0, T_amb_cryo 300.0, f_carnot_cryo 0.20, p_cryo_direct 0.0) and mirror the generated impl's statement forms verbatim (the spike's generated body: `cop_carnot = T_cold/(T_amb - T_cold)`; `cop = f_carnot * cop_carnot`; `p_cold = ((q_nuc * vol_cold) * 1e-06 + p_fixed) * f_uplift`; `p_cryo = p_cold/cop + p_direct`), feeding the recirc sum where the 0.8 literal sat. Bit-equality of mirror vs generated module verified in the spike.
- `run_stellaris.py`: add `cryo=f"{P}cryo_elec__p_elec"` to `CH` and a per-channel bit-exact check of the derived p_cryo vs the oracle (SV-031's "computed output" witness); rewrite the WI-023 headline comment for WI-024; retarget the headline asserts (p_net 915.1, rec_frac 0.151, q_eng 6.61, LCOE 201.5 — all inside existing tolerance bands, retargeted for the record with the WI-024 story).
- `handshake_1costingfe.py`: the D7 injection-map edit only (successor bar; flagged deviation).

### 5. Regen

Snapshot from the staged models with **no `--design-path-filter`** (the flag gotcha above) → `bridge_v11_generate.py` from `~/1cfe/sysml-codegen` (HEAD `6db3212` verified working this session). Post-regen checks: exactly 3 bridged offenders; `system_design.json` carries the 8 `cryo_elec__*` leaves and no `pb__p_cryo`; pipeline yaml wires `p_cryo: float …cryo_elec__p_elec.root`; `cryoplant_electrical_power_impl.py` AUTO_IMPLEMENTED; `IMPLEMENTATION_BACKLOG.md` still exactly 1 function; WI-022 `dt_fusion_power_impl.py` content-hash unchanged (`preserve_handwritten=True` confirmed still set at `bridge_v11_generate.py:108`). Known regen-resets (3 bridge keys, 4 BOP wirings, 3 glue schema fields) re-applied by runner glue on execute — diff `generated/` after a run, not straight after regen.

## Cross-File Bindings

| binding | file | change |
|---|---|---|
| `in q_nuc = q_nuc_cryo` (+6 more) | `mfe_plant.sysml` cryo_elec block | new plant attributes, dormant defaults (D3) |
| `in p_direct = p_cryo` | `mfe_plant.sysml` cryo_elec block | existing plant attribute becomes the additive direct term |
| `in p_cryo = cryo_elec.p_elec` | `mfe_plant.sysml` pb block | the one rewired pb input (was `= p_cryo`) |
| `:>> p_cryo = 0.0` + 7 chain literals | `stellarator_plant.sysml` | instance bindings with MR-4 citations (above) |
| handshake `cryo_elec__*` injection | `handshake_1costingfe.py` | D7 successor injection (replaces `pb__p_cryo`; flagged) |
| `import mfe_cryo_plant::*` | `mfe_plant.sysml` | new library import |

Dataflow stays unidirectional: instance literals → cryo_elec → pb → LCOE denominator. No cycles (L3-verified on the prototype); no other consumer reads `p_cryo` (grep-verified: only the pb sum and the instance binding).

## Validation Plan

1. **L1–L3** after each edit; full **L1–L6** after all model edits: L1 = 0 over the 22-file canonical set (21 + the new library file), offender list exactly the 6 pre-existing (`mfe_plant.sysml:329/335/340`, `ife_plant.sysml:33/41`, `hif_plant.sysml:205`) — compare the offender list, not level-summary flags.
2. **Mirroring**: full-file diff canonical vs staged — only the known viability-assert divergence remains; the new library file byte-identical in both trees.
3. **Regen** per §5 above (no design-path-filter; 3 offenders; auto-impl; WI-022 impl survival content-verified).
4. **Execute**: `run_stellaris.py` (exec venv `/home/reid/1cfe/fusion-tea/exploration/pipeline_spike/.venv-exec/bin/python`) bit-exact vs the updated oracle at rel 1e-9 on every channel including the new derived-p_cryo channel; headline at the Research Findings table's values (p_cryo 0.8643516, p_net 915.081088, q_eng 6.606662, LCOE 201.472065; capital unchanged to the cent).
5. **Handshake**: run under the D7 successor bar — `handshake_1costingfe.py` edited only in the injection map, `git diff handshake_comparison.json` empty (byte-identical to the WI-023 record). Gate only after the orchestrator/owner has seen the D7 deviation.
6. **Regressions**: IFE `run_anchors.py` 252.30/68.69/270.12 $/MWh, Meier 4.735 c/kWh (no IFE file touched); pytest tally unchanged (2 failed + 18 errors pre-existing); viability constraints unchanged (none reads p_cryo).
7. **Close-out**: SV-031 → passing with executed values; q_eng 6.6067 recorded against SV-016 (still below the ~10–40 band — flagged for the owner, band untouched, MR-WI024-6); headline recorded in the work item and `.project/CURRENT_WORK.md`.

## Validation Report (design-stage)

- **Prototype parse: PASS** — L1/L2/L3 zero errors/warnings on the calc def + mock-plant stencil (scratchpad, no repo file touched).
- **Snapshot classification: PASS** — spike on a scratch copy of the staged tree with the exact edits: `cryo_elec` all-literal leaves; `pb.p_cryo` chain → `cryo_elec.p_elec`; no other binding change.
- **Bridge/emission: PASS** — exactly 3 V11 offenders, bridged, package emitted at sysml-codegen HEAD `6db3212`; cryo module AUTO_IMPLEMENTED; backlog still 1 function. (First attempt produced 11 offenders — root-caused to my `--design-path-filter stellarator_09` flag, reproduced on the unedited tree as a control, resolved by the unfiltered snapshot; recorded as a regen-flow gotcha, not toolchain drift.)
- **Numeric: PASS** — generated module bit-equal to the oracle mirror at the Stellaris point (0.8643515999999999) and exactly 0.8 at the handshake identity point (D7's executed proof). Full-headline oracle run reproduced the WI-023 baseline to the cent first, then computed the expected WI-024 point (table above).
- **Key-diff: PASS** — generated inputs move by exactly the designed surface: +8 cryo leaves, −pb__p_cryo, −3 known glue fields.

## Implementation Checklist

1. **Library** — new `mfe_cryo_plant.sysml` (canonical + staged, identical). L1–L3.
2. **Generic plant** — import + 7 attributes + p_cryo re-doc + cryo_elec usage + pb rewire (canonical + staged). L1.
3. **Instance** — p_tf doc rewrite; p_cryo region (direct-term zero + 7 cited bindings); p_tfcool coverage doc; headline + mapping-traps refresh; STALE BASIS appends (canonical + staged). Full L1–L6 offender-list compare; mirroring diff.
4. **Regen** — unfiltered snapshot + bridge; post-regen checks per §5 (incl. WI-022 impl content hash).
5. **Oracle + runner** — chain mirror in `verify_stellaris.py`; CH channel + asserts in `run_stellaris.py`; execute bit-exact.
6. **Handshake** — D7 injection-map edit (after orchestrator/owner sign-off on the deviation); run; `handshake_comparison.json` empty git diff; IFE + pytest regressions.
7. **Close-out** — SV-031 passing with executed values; SV-016 flag; headline records; `/status` close (owner holds close).

## Risks

| risk | likelihood | impact | mitigation |
|---|---|---|---|
| Handshake successor bar not accepted | — (decision) | blocks phase 6 | flagged deviation (D7) with executed bit-exactness proof; the alternative — not modeling the chain — contradicts the ratified scope |
| Regen run with the design-path-filter flag → 8 spurious offenders | medium (easy to repeat) | medium | gotcha documented here and in the plan; control check: bridge must report exactly 3 offenders before proceeding |
| sysml-codegen HEAD moves before implement | low | medium | spike verified at `6db3212`; re-run the unedited-tree control snapshot+bridge first if HEAD changed |
| Oracle/impl statement-form drift (bit-exactness) | low | medium | oracle mirrors the generated statement forms verbatim (spike-proven bit-equal); runner gates every channel at rel 1e-9 |
| Regen clobbers the WI-022 handwritten impl | low | high | `preserve_handwritten=True` confirmed still set; content hash checked post-regen (WI-023 pattern) |
| Circumference approximation biases vol_cold | certain (bounded) | low | printed-but-approximate 25 m documented as the weak link; mass cross-check (~7540 kg/m³) bounds plausibility; error flows linearly into a ~0.86 MW term |
| Derived value understates the true cryo load | certain (by construction) | low, documented | D6 lower-bound treatment: f_uplift seam + verbatim deferral quote in the binding doc |
| q_eng still below SV-016 band | certain | — | recorded and flagged at close, never fitted (MR-WI024-6) |
