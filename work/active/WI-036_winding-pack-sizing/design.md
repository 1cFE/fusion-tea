---
Status: active
Created: 2026-09-03
Updated: 2026-09-03
Related Artifacts:
  Spec: work/active/WI-036_winding-pack-sizing/spec.md
---

# WI-036 Design: Winding-Pack Sizing — Current-Sized Pack, Cold Volume into the Cryo Chain, and a Computed Conductor-Strain Check

**Approved 2026-09-03** `[AGENT] (approval delegated by the owner 2026-09-02: "no gates. USE YOUR BEST JUDGEMENT ALONG THE WAY!")`. Architecture follows from goal `priced-levers` T-001 (the sizing relation, image-verified) and T-002 (the two-check criterion). Every quantitative basis below is verified against the Stellaris table **images** or the raw PDF, never the markdown extraction — Table 8's markdown is garbled and the image governs.

## Overview

Today the winding pack is a single held number that reaches only the stress calc: widen it and nothing costs more. Afterward the pack is sized by the current it carries, its cold volume drives the cryoplant, its length responds to machine size, and the conductor carries its own strain check alongside the structure's stress check.

## Physics and engineering bases (image-verified)

All from `knowledge/concept_research/09-qi-stellarator-hts/iter-01/sources/stellaris-design-details/images/page_022_table_0.png` (Table 8) and the iter-02 raw PDF unless stated.

| quantity | printed value | use |
|---|---|---|
| Coil 0 total amp-turns | 15.4 MA | D1 anchor pair |
| Coil 0 cross-section side | 360 mm | D1 anchor pair |
| Winding-pack current density `j_WP`, coils 0–5 | 119, 112, 120, 112, 122, 124 A/mm² | D1 default and design range |
| Cross-section sides, coils 0–5 | 360, 360, 340, 340, 320, 300 mm | D2 set factor |
| Typical coil circumference | 25 m (raw PDF sec. 2.9) | D3 anchor |
| Winding-pack peak von Mises | ~600 MPa (raw PDF p. 24) | D4 anchor pair |
| HTS stack peak strain | < 0.2% (raw PDF p. 24) | D4 anchor pair |
| REBCO irreversible strain, SuperOx at 4.2 K / 19 T | 0.45–0.47% | D5 limit basis |
| No discernible strain effect below | 0.4% strain / 600 MPa | D5 limit basis |

The last two are from `knowledge/sources/electro_mechanical_properties_of_rebco_coated_conductors/output.md:173,197` (Barth, Mondonico & Senatore 2015), verified in the registered extraction.

## Design decisions

**D1 — The pack is sized by current, through a settable winding-pack current density.** Winding-pack cross-sectional area equals coil current divided by `j_WP`; `wp_side` becomes its square root and stops being an entry point. `j_WP` is bound as the float64 that reproduces the printed pair (15.4 MA, 360 mm) exactly — **118.8271604938 A/mm²**, printed as 119 — following the `peak_ratio` / `k_link` / `k_sigma` convention already used across this instance for a fact derived from a printed pair. The design range across the source's own six coils is 112–124 A/mm², and `j_WP` is the design lever this item exists to expose.

Consequence for the stress channel: substituting into the existing form gives σ = k_sigma·B_peak·√(I_coil·j_WP), so stress now grows as the square root of current rather than linearly. That is the relief the sizing chain buys, and it is a consequence of the two sourced relations rather than a new assumption.

**D2 — Cold volume through a set-distribution factor, not a per-coil representation.** The model carries one winding pack (the worst coil); the machine has six unique sizes. Rather than introduce per-coil geometry — a much larger change with no cost consequence of its own — total cold volume is `f_wp_vol · n_coils · wp_side² · c_coil`, with `f_wp_vol` a held sourced fact from the six printed sides: **0.8780864197530865**, the ratio of the printed total (136.56 m³) to the worst-coil-uniform reference (48 × 0.36² × 25 = 155.52 m³). This reproduces the currently held `vol_cold_cryo` **exactly** at the design point and is the same shape as the existing `f_set` coil-current distribution factor. It also moves the six-cross-section arithmetic out of a doc comment and into model content, which is the defect T-001 named.

**D3 — Winding length responds to machine size through a held shape factor.** `c_coil` becomes `k_coil · R`, with `k_coil` = **1.9685039370078741** (25 m / 12.7 m), reproducing the printed 25 m exactly at the design point. This is the trade the WI-036 mint record predicted — "one held constant traded for a smaller one" — and it is the honest limit of what the source supports: per-coil circumferences are unprinted, so the *shape* stays held while the *scale* responds. The residual held quantity is `k_coil`, named here rather than buried.

**D4 — The conductor's strain operand, and what it honestly means.** Conductor strain is `f_cond · σ_wp / E_wp`, where `E_wp` = 200 GPa (316LN at 20 K) and `f_cond` is a load-sharing factor calibrated from the source's own reported pair: the winding pack peaks at ~600 MPa von Mises while the HTS stack strain stays below 0.2%, giving `f_cond` = **0.6666666667**. The tape stack sees less strain than the pack average because the soldered Cu jacket offloads it; this factor is that offloading, taken from the design's own two numbers rather than assumed.

Both anchors are printed *bounds* taken as values ("<0.2%", and our `σ_wp` anchor is itself the "<650" bound), so the operand is conservative in the direction of over-estimating strain. That double conservatism is disclosed, not corrected — correcting it would require numbers the source does not print.

**D5 — The conductor limit is settable, defaulted at 0.4%, and it does not bind first.** `eps_cond_allow` defaults to **0.004** — the upper end of the 0.2–0.4% band practitioners enforce, and the strain below which the registered measurements report no discernible effect on any manufacturer's tape. At the design point the operand reads **0.217%**; at the 800 MPa stress fence it reads **0.267%**; the conductor constraint would bind at σ_wp = 1200 MPa.

So with the sourced load-sharing, **the structure binds before the conductor**, which is what a sound magnet design should show — and the model now shows it instead of assuming it. The margin is not large: SuperOx, the tape this design specifies, is the weakest of five measured at 0.45–0.47% irreversible strain, so the default sits at 0.4% against a 0.45% failure, and a designer choosing the conservative 0.2% that other projects use would find the conductor binding first. That is exactly why the limit is settable.

**D6 — Cost lands through the cryo channel only.** A wider pack at constant current buys no additional superconductor — ampere-metres are set by current and length — so the existing ampere-metre-proportional winding-pack cost is correct to be cross-section blind and is **not** changed. The cost consequence arrives through the live chain that was waiting for an input: computed cold volume → cryoplant heat load → cryoplant electrical → `cryoplant_capital`. Winding length entering through D3 does move the ampere-metre term, correctly.

**D7 — Tolerances.**

| Stage | Expected | Tolerance | Basis |
|---|---|---|---|
| `j_WP` × side² vs printed amp-turns, six coils | within 1% | 1% | Table 8 image; the relation closes at −0.58%…+0.52% |
| `wp_side` at the design point | 0.360000 m | exact to float64 | printed pair convention |
| `vol_cold_cryo` at the design point | 136.56 m³ | 0.01 m³ | printed six sides |
| `c_coil` at the design point | 25.0 m | exact to float64 | printed pair convention |
| Conductor strain at the design point | 0.217% | reported, not asserted | D4 composition |

**D8 — What this does not do (decision record).**

- **`sigma_allow` is not changed**, in either direction (MR-WI036-6). Its stress category is stated in D4's neighbourhood: the operand descends from a printed row titled "Peak stress on WP", so it is a peak quantity, and the ITER criteria carry 666 MPa primary membrane / 1.0–1.333 GPa peak. No feasible region is opened by re-categorising it.
- **Transverse conductor limits are declared, not valued** (MR-WI036-7). Delamination in through-thickness tension is measured at 3.6 MPa and transverse compression at ~200 MPa on bare tape — two orders of magnitude apart from the axial limit. This model computes no through-thickness stress, so it asserts no such constraint and must not imply it checks one. Named gap at the disclosure surface.
- **`vol_cold_cryo` is not retired.** D2 gives it a computed default; the setter is preserved, per the standing `[OWNER 2026-08-27]` WI-032 ruling.
- **`k_sigma` stays anchored at `wp_side` = 0.36.** It is a stress *concentration* factor, not a size factor, so it remains meaningful off its anchor point — but it was back-solved at that point and this design says so rather than letting a reader assume it was independently sourced.
- **The radial build is not touched.** `coil_t = 0.30` remains inconsistent with the 0.36 m pack; recorded as a known defect for its own item.
- **The pack's non-conductor mass has no cost home.** 85% of the winding pack is steel, insulation, copper and helium, and only the conductor is costed. Disclosed here; expanding the cost account is outside this item.

## Risks

1. **The conductor operand is a composition standing in for a finite-element result** — von Mises is not uniaxial stress, and a pack-level stress is not local tape stress. Mitigation: `f_cond` is calibrated from the source's own reported pair rather than assumed, both anchors are conservative bounds, and the operand is reported at the design point rather than tuned. Medium.
2. **Strain limits are bracketed, not measured, at 20 K.** The registered source measures 4.2 K and 77 K and states the irreversible limits are identical between them; the one paper measuring through 20 K is paywalled and recorded as a queued gap. Medium-low.
3. **Sizing changes the baseline's verdict set.** `wp_side` at the design point is unchanged by construction, so the baseline should not move — but any residual float difference propagates into stress. Mitigation: the design-point reproductions in D7 are exact-to-float64 by construction, and a headline check catches the rest. Low.
4. **Committed studies that held `wp_side` become non-replayable as written.** Mitigation: MR-WI036-11 restatement recorded before regeneration; the fixture and suite surface is named in the implementation task's scope rather than discovered. Medium.

## Files

- **New:** a winding-pack sizing calc (library); a cold-volume calc (library); a conductor-strain calc and its constraint def (library).
- **Touched:** `models/library/analyses/mfe_magnet_field.sysml` (stress consumes computed `wp_side`); `models/library/analyses/mfe_cryo_plant.sysml` wiring; `models/library/analyses/mfe_viability.sysml` (new constraint def); `models/designs/generic_mfe/mfe_plant.sysml` (calc usages, assert); `models/designs/stellarator_09/stellarator_plant.sysml` (rebinds: `j_WP`, `f_wp_vol`, `k_coil`, `E_wp`, `f_cond`, `eps_cond_allow`; `wp_side` and `c_coil` become computed, `vol_cold_cryo` keeps its setter).
- **Not in this item:** `sigma_allow`, `B_max` and its cost consequence (WI-038), heating structure (WI-039), `coil_t` reconciliation, any new cost account.
