# Plant comparison contract — REBCO versus Nb₃Sn across explicit confinement and coil-geometry assumptions (r1)

Round 2 of goal `magnet-material-comparison`. Status: **r1, for independent review.** Authority: the owner's Round 2 brief ([owner-brief-round2.md](owner-brief-round2.md)) as refined by the owner's ruling of 2026-09-30 (goal.md Amendment 2): “Across explicit assumptions about confinement and coil geometry, when does each material give lower LCOE—and are those conditions supported by evidence?” Evidence base: [plant-chain-audit.md](plant-chain-audit.md) (chain, deficiencies D1–D8, account map, seam), [sources/field-term.md](sources/field-term.md), [sources/plasma-validity.md](sources/plasma-validity.md), [sources/nb3sn-stellarator.md](sources/nb3sn-stellarator.md), and Round 1's [comparison-contract.md](comparison-contract.md) (r3) for the conductor definitions. Every choice below is `[AGENT]` unless marked otherwise; the reviewer is asked to challenge each against the cited evidence.

## 1. What is compared, and what the answer looks like

One plant model, the Stellaris plant (`exploration/stellarator_e2e`, isolated derived package per § 9), evaluates supplied plant designs for each conductor material. Two axes of **explicit assumptions** span the map: a confinement assumption (§ 3.1) and a coil-geometry assumption (§ 3.2). In each assumption cell, a bounded search (§ 5) proposes supplied designs per material; the plant evaluates each as supplied (MR-7); the **best supported design** per material is the lowest-LCOE design that passes every check in § 7. The answer per cell is: which material's best supported design has the lower LCOE, by how much, decomposed by account (§ 8); the REBCO tape price at which the cell's preference changes (§ 8); and the evidence label of the cell's assumptions (§ 3). Failed and unsupported designs are retained and reported as such, never as "expensive".

Matched-duty connection to Round 1: the Stellaris reference winding (9.0 T axis, 24.9 T peak under the anchored ratio, 48 × 308 turns at 50 kA) is one REBCO design point in the anchored cell; Round 1's anchor-S pairs are the same duty on a fixed envelope. The plant-level comparison at that duty, with the Nb₃Sn winding at the highest field it supports on the same coil set, is reported first, before the map.

## 2. Plant model, what it computes, what it does not

Chain (audit § 2): ampere-turns and R set the axis field (`B_axis = μ0 k_link N I/(2π R)`); the peak field is `B_axis × peak_ratio × bore factor`, where the bore factor `[R/(R − a_coil)]` normalized to the anchor responds to the radial allocation `coil_t`; the field reaches the plasma through the ISS04 confinement time (required heating, ash) and beta; fusion power reads density, temperature and volume; heating draw, cryogenics and coil drive enter net electricity; magnet capital follows the supplied winding; every other account follows the radial build and supplied power classes; LCOE is the plant's DCF over overnight capital, O&M, replacements and net energy.

Held facts the map does not move (all Stellaris-anchored; audit § 2): `k_link` 0.7731, `n_coils` 48, the profile exponents, `Ti/Te`, the ash and impurity factors, the wall-load calibration, the divertor shadow, the achieved TBR, the DCF finance parameters, the winding-operations rate, the supplied power-class prices. **Stated limit:** every held fact is anchored at one point; away from it the model's outputs are the anchored shape's prediction. The map's evidence labels (§ 3) carry this.

Not computed, and not claimed (audit D2, D7): a casing mass or transverse-cavity cost response; equipment response to field or stored energy beyond what the supplied-design policy (§ 5) supplies with a stated basis; structural adequacy; a fully qualified magnet or plasma.

## 3. The assumption axes and their evidence labels

Evidence labels used throughout: **[S]** directly supported at the Stellaris design point (printed in the Stellaris paper or reproduced from it); **[A]** sourced analogue: a printed value for another configuration (HELIAS line, ITER/DEMO), not this coil set; **[D]** derived from sourced values with stated arithmetic and caveats; **[U]** assumption with no source at this field or geometry, labelled as such.

### 3.1 Confinement

| Value | Label | Evidence |
|---|---|---|
| `f_ren` 1.0 | [S] at 9.0 T | Stellaris Table 4/5: f_ren 1.0 at both operating points, ⟨β⟩ 3 % (plasma-validity.md § Evidence). No validity band printed; at fields below 9 T this is **[U]**. |
| `f_ren` 1.4 | [A] | Lion 2023 Table 4.3 conservative Helias 5 at 5.81 T: f_ren 1.38 at β 5 %; W7-X best transient ≈ 1.4; Warmer 2016 Nb₃Sn window cap ≤ 1.5. |
| `f_ren` 1.8 | [A] | Lion 2023 Table 4.3 advanced Helias 5 at 5.86 T: f_ren 1.77; Warmer 2016 NbTi window cap ≤ 1.8; Beidler HSR5/22 τE ratio 1.69 (derived). |
| `beta_limit` 0.05 | [A] | PROCESS input in the model (audit § 2c); HELIAS designs 4.5–5 %; not field-dependent in any source. Held on every cell; a 0.045 variant on the two anchored cells only. |

The model applies `f_ren` as a multiplier on ISS04 τE at every design point of a cell, for both materials alike. The ISS04 density exponent stays the model's 0.54 (Stellaris eq. A.7); the printed 0.52 of Lion 2021 is a recorded discrepancy (plasma-validity.md § Equations), not a variant, until the journal paper is obtained.

### 3.2 Coil geometry

| Value | Label | Evidence |
|---|---|---|
| `peak_ratio` 2.7667, bore factor as modeled, no pack term | [S] at the Stellaris pack (0.1296 m²), [U] at any other pack area | Stellaris Table 2 (24.9 T at 9.0 T); Table 8 per-coil peaks 24.6→19.5 T at packs 0.130→0.090 m² (field-term.md § Evidence). The pack term of Lion 2021 eq. 39 is omitted because a0, a1 are unprinted (audit D1). |
| `peak_ratio` 2.12 | [A] | HELIAS 5-B: 12.5 T on coils at 5.9 T axis (Schauer 2013 Table 1); every HELIAS-line and ITER/DEMO design sits at 2.0–2.2 (nb3sn-stellarator.md § Evidence). A different coil set; applied here to the Stellaris plant as an explicit assumption that a coil set with that ratio exists for this configuration. |
| pack-size arm: `peak_ratio(A_wp) = 2.7667 + 0.064 × (R/√A_wp − 35.3)` | [D] | The three-point Helias-5 fit of field-term.md § Gaps (ratio ≈ 0.15 + 0.064 R/√A_wp), re-anchored at the Stellaris point; poorly conditioned and possibly mixing coil sets. Floor: the exact Ampère bound `B_peak ≥ μ0 I_coil/(4√A_wp)` is checked on every case and reported. |

The arm makes the peak field respond to the supplied pack area (a bigger Nb₃Sn pack lowers the ratio, a smaller REBCO pack raises it), which is the mechanism the owner's "winding-space capability" names; it is the only such response available and it carries the [D] label into every cell that uses it. `B_max` (the plant's ceiling check) is set per material to the material's law limit (§ 4), not to Stellaris's 24.9 T design envelope, because the map asks what each material supports; the 24.9 T envelope is reported as a separate flag on REBCO cases.

Cells: {anchored, HELIAS-class, pack-size arm} × {1.0, 1.4, 1.8} = nine cells; two beta-limit variants on the anchored-geometry cells.

## 4. The materials in the plant

Round 1's conductor definitions (`models/library/analyses/magnet_conductor_alternatives.sysml`; contract r3 §§ 3–4) are used for both materials in the plant's material instances; the plant's own REBCO law stays in the untouched reference instance only (§ 9).

| | Nb₃Sn | REBCO |
|---|---|---|
| Law | ITER-form strand Jc(B, T, ε), WST TFCN5-6 median, −0.3 % intrinsic strain (variant −0.6 %) | Molodyk 20 K shape 8–20 T, T* 22 K, degradation 0.90 |
| Supply / conductor temperature | 4.5 K / 5.2 K | 20 K / 20.7 K |
| Acceptance rule | Tcs − T ≥ 1.5 K (reference family) | I/Ic ≤ 0.80 (reference family) |
| Status bands | supported ≤ 12 T; edge 13 T; law-only 14 T; unsupported ≥ 16 T (Round 1) | supported ≤ 20 T; **extrapolated 20–25 T** (power-law continuation anchored at 20 T, `shape_mode` 1, `B_law_max` 25 T, `alpha` 0.6); unsupported > 25 T |
| `B_max` for the ceiling check | 13.0 T (edge admitted, flagged) | 25.0 T |
| Construction rule | P (EU DEMO layer-1 calibrated) | C (Stellaris Table 7); common-P as a variant on two cells |
| Price | 8 USD2021/m strand (5.4 / 13.5 variants) | 80 USD2021/m of 4 mm tape (market); 30 (target); 10 (volume) |
| Manufacturing | plant winding-operations rate on conductor length, both | same |

The REBCO extrapolated band is new in this contract: the Stellaris reference at 24.9 T lies above the 20 T measured extent of the Molodyk shape and above the plant law's own 24 T flag, so any REBCO case at the reference duty is labelled `extrapolated` in the results and in the map. Tape width 4 mm at Round 1's tape properties is the basis; the plant's 6 mm × 20 $/m basis is retired inside the material instances (§ 6).

## 5. Supplied designs: variables, ranges, and the offer policy

Each design is a supplied set of plant inputs; the model calculates requirements and checks them; nothing is resized inside the model. A declared policy (a study script, as Round 1's `offer_policy.py`) proposes the supplied values from rules stated here. Every rule is `[AGENT]`.

**Design variables per material and cell:**

| Variable | Grid | Rule |
|---|---|---|
| Target axis field `B_axis` | Nb₃Sn: the values that put `B_peak` at 10, 11, 12 T under the cell's ratio and the design's bore factor (13 T edge as a flagged extra); REBCO: `B_peak` 18, 20, 22, 24.9 T (24.9 = Stellaris reference; 22–24.9 extrapolated) | ampere-turns `N_turns × I_turn` from `B_axis` at the design's R (`k_link`, `n_coils` held); turn current 50 kA held (Round 1 anchor S; variant 86 kA on one cell, HELIAS 5-B cable); turns = ampere-turns / 50 kA, rounded up |
| Major and minor radius (R, a) | (12.7, 1.3) reference; (15.0, 1.5); (18.0, 1.8); (22.0, 2.2) [A: HELIAS 5-B is R 22, a 1.8] | fixed aspect ratio ≈ 9.8–10 except the HELIAS point; the radial build's held stack (1.70 m) and the swept `coil_t` set `a_coil` |
| Operating point | `T_i0` 14.63 keV held; `n_e0` set by the policy to the **matched fusion power** 2,653 MW (the reference's `p_fus`) at the design's volume, if attainable with `beta ≤ beta_limit`; otherwise `n_e0` at `beta = beta_limit` and the case carries `power_short = 1` | fusion power is the plant's supplied power class (turbine, BOP, heat transport all supplied at the reference class), so matched power keeps the non-magnet equipment comparable; density is a supplied choice per design, checked by beta, sustainment, wall load, divertor and burn-hold |
| Winding element count | Round 1 offer policy: smallest count meeting the acceptance rule at the design's `B_peak` and conductor temperature (insufficient ⌊0.9 n⌋ and generous ⌈1.2 n⌉ on the reference-cell designs only) | supplied; checked by `acceptance_ok` |
| Pack side `wp_side` | `√(turns × gross_turn_area)` from the construction rule at the design's current and field, rounded up to 5 mm | supplied; checked by the new `pack_area_ok` (turns × gross area ≤ wp_side²) |
| Radial allocation `coil_t`, transverse interior `interior_y` | `wp_side × (1 + internal) + 2 × ground + 2 × clearance + 2 × wall`, rounded up to 10 mm; same for `interior_y` | supplied; checked by `wp_fit_ok`; `coil_t` moves the bore factor and the radial build (costs) — the field/geometry feedback the model has; transverse space has no cost response (stated limit) |
| Structure mass `m_support` | `11,615.6 t × (W_mag / 111 GJ)` [U: stored-energy scaling anchored at the reference; PROCESS-style, coefficient not sourced]; variants ×0.5 and ×2 on the two anchored cells | supplied; priced by the plant's structure account |
| Installed heating `p_wallplug_heat` | `max(100 MW, 1.1 × p_aux_required / 0.5)` rounded up to 10 MW, priced at the plant's ECRH capital per MW | supplied; checked by `sustainment_ok` |
| Cryo ratings (cold, 77 K) | from Round 1's cold-load calc at the design (nuclear, radiation, conduction, leads, joints) with the fixed rating list; capital and efficiency from the Green laws at the supplied rating (both materials); 20 K by input-power equivalence | supplied; checked by `capacity_ok` |
| Stress and strain | plant's `sigma_wp = k_sigma I_coil B_peak / wp_side` against 800 MPa; strain against the material's allowable (REBCO 0.4 %; Nb₃Sn 0.3 % [A: HSR50a jacket strain < 0.3 %]) | checked |

Size of the search: 9 cells × 2 materials × 3–4 fields × 4 sizes ≈ 250 designs, plus the MR-7 insufficient/generous offers (≈ 48), the beta, strain, construction, structure-mass and turn-current variants on the anchored cells (≈ 60), and price as a post-processing axis (§ 8). About 360 evaluated cases. Bounds are engineering choices around the reference and the HELIAS analogue, not physical acceptance limits.

## 6. Accounting: one basis inside the plant

Nothing from Round 1's annualization is added to the plant (audit § 4). In the material instances:

- **Conductor purchase** = supplied element count × turns × coils × turn length × price per metre (Round 1 basis, USD2021), replacing the plant's composition-implied tape metres at 20 $/m of 6 mm tape. The composition fractions become consequences of the construction rule (copper, steel, insulation areas per turn) and are priced at the plant's unit prices. Helium inventory keeps the plant's basis.
- **Winding operations** stay the plant's always-on rate on conductor length, both materials (Round 1's manufacturing allowance is not used).
- **Refrigeration**: Round 1's cold-load and staged-refrigeration calcs replace the plant's 0.20-Carnot chain and supplied 31.48 M$ package price for both materials; the 77 K intercept stage is common; cold-stage and intercept electricity enter the plant's recirculating power exactly where the plant's cryo electricity enters today.
- **Structure**: the plant's account on the supplied `m_support` (§ 5).
- **Everything else** (blanket, vessel, buildings, heat transport, conversion, heating capital, fuel cycle, O&M, replacements, availability, DCF): the plant's, unchanged, for both materials.
- **Money year**: conductor prices are USD2021 by declaration; the plant's other accounts are its mixed-year basis (stated limit, common to both materials). No CPI adjustment is applied to the plant's accounts.

The untouched reference instance keeps every plant basis, so its outputs must reproduce today's pin bit-for-bit (§ 9).

## 7. Checks, statuses, and what "supported" means

Per design, every plant predicate is evaluated (the current 67 verdicts) plus the magnet checks from Round 1 (`acceptance_ok`, `copper_ok`, `steel_ok`, `capacity_ok`, conductor `supported` status) and the new `pack_area_ok`. Statuses:

- **unsupported**: the conductor status is `unsupported` at the design's field/temperature, or the REBCO band is `extrapolated` above 25 T, or the plasma point is outside the model's stated domain (`R − a_coil ≤ 0`, non-convergence). No ranking.
- **failed**: any magnet, plasma, power-balance or wall/divertor check is violated. No ranking; the failing checks are named.
- **supported**: all checks pass except the four reference-common screens `facility_occupancy_ok`, `water_electric_capacity_ok`, `tbr_ok`, `divertor_heat_ok`, which fail at the published reference on the current model for reasons unrelated to the magnet (audit § 5); their margins are reported for every supported design, and a design that fails one of them by more than the reference does is downgraded to **failed**. `[AGENT] — the reviewer is asked to rule on this treatment.`
- Flags carried on supported designs: `extrapolated` (REBCO 20–25 T; Nb₃Sn edge 13 T), `green_extrapolated`, `power_short`, `above_stellaris_envelope` (REBCO `B_peak` > 24.9 T).

"Best supported design" per material and cell is the supported design with the lowest LCOE. If a material has no supported design in a cell, the cell reports "no supported design" with the nearest failed design's failing checks, and no preference.

## 8. Reporting

- **Per cell**: the two best supported designs (all supplied inputs, all flags), LCOE of each, the difference, and the LCOE decomposition by account group (conductor purchase; other winding materials and operations; structure; refrigeration capital and electricity; heating capital and draw; blanket/vessel/buildings and other radial-build accounts; conversion and BOP; fuel cycle and O&M; net electricity) as differences REBCO − Nb₃Sn.
- **Break-even REBCO price per cell**: LCOE is linear in the tape price at a fixed design; from the best REBCO design's LCOE at 80 USD/m and its conductor purchase, solve for the price at which it equals the best Nb₃Sn design's LCOE; report also at 30 and 10 USD/m, and note when the best REBCO design changes with price (re-select at each price).
- **The map**: a 3 × 3 table (geometry × confinement) with, per cell, the winner at 80/30/10 USD/m, the LCOE gap, and the evidence label of the cell ([S]/[A]/[D]/[U] of its two assumptions, with the REBCO extrapolation flag where the winning REBCO design is above 20 T).
- **Interaction**: for the anchored and pack-arm geometries, the break-even price against field and against size, to show whether higher field or reduced size changes the value of a lower REBCO price.
- **Matched-duty connection** (§ 1) reported before the map.
- **Retained cases**: every failed and unsupported design with its reasons, distinguished from supported-but-dearer designs.

## 9. Package, verification and review

- **Package**: an isolated derived package `exploration/stellarator_materials/` built from the `stellarator_e2e` sources plus Round 1's conductor library and a new variants file, per the audit's seam proposal (§ 6 steps 1–8): a gated REBCO-law completion (value-neutral at `enabled = 1`), `default` seams on the cryoplant, the `'Nb3Sn Magnet System'` and `'Round1 REBCO Magnet System'` variants with the supplied count and `pack_area_ok`, `'Staged Cryoplant'`, and a design file with three instances (reference, REBCO-material, Nb₃Sn-material). Regression: the reference instance reproduces the current `stellarator_e2e` pin bit-for-bit; `exploration/stellarator_e2e/**` and the Stellaris design file stay byte-identical.
- **Verification**: the existing plant oracles for the unchanged channels and predicates; Round 1's oracle for the conductor, area, inventory, cold-load and refrigeration channels; a new independent oracle (separate author) for the material-instance bindings, `pack_area_ok`, the staged cryo insertion into the power balance, the peak-ratio arm and the structure-mass rule; every recorded channel of every case compared at 1e−9 relative.
- **Review**: this contract (fresh reviewer) before the design; the design (fresh reviewer) before implementation; the study reading and this map (fresh reviewer) before the answer.

## 10. Stated limits (carried into the answer)

1. Coil geometry other than the anchored ratio is an assumption about a coil set that has not been designed for this configuration; the pack-size arm is a derived slope with heavy caveats.
2. Confinement enhancement above 1.0 is a sourced assumption from other configurations; no source supports any f_ren at 4–5 T for this configuration.
3. Every plasma, wall and divertor held fact is anchored at the Stellaris point; outputs away from it are the anchored shape's predictions (D8).
4. Transverse cavity, casing mass and equipment beyond the supplied policy have no cost response (D2, D7); the structure-mass rule is an unsourced scaling.
5. Conductor prices are USD2021 inside a mixed-year plant; the REBCO reference duty is extrapolated above the measured 20 T; Nb₃Sn edge cases at 13 T are flagged.
6. A supported design is a screening pass, not a qualified reactor.
