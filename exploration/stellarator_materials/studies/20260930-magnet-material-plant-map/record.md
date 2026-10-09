# REBCO versus Nb₃Sn on the Stellaris plant across confinement and coil-geometry assumptions

**Executed and verified against three integration `CANDIDATE` pins, under contract r5a's tolerance clause.**
- Every one of the 2,921 declared cases ran on its unit through the stock lifecycle. Of these, 2,917 evaluated and 4 REBCO designs are domain refusals, which the oracle refuses too.
- Every independently compared channel and every verdict agrees with the oracle. Two published static-load channels have no oracle leg; they have identity checks only (§ 13).
- The first run of the Nb₃Sn seam refused at gate 8. It was verified at relative 1e−9 only, and the package's Tcs root solver holds 1e−10 K, which is about 1e−8 relative on margins sized at allowance. The coordinator restored Round 1's absolute clause as contract r5a § 9 (commit `97fabad31`). The REBCO and Nb₃Sn seams were then re-run on the amended manifests and returned `CANDIDATE`. The refused run is kept under `integration-r3-nb3sn/blocker-run/`.
- This record is the executor's factual deposit. The goal-level interpretation is the coordinator's.

## 1. Study header

- **Study id:** `20260930-magnet-material-plant-map`
- **Package:** `exploration/stellarator_materials` (three units: `stellarator_materials_reference_tea`, `stellarator_materials_rebco_tea`, `stellarator_materials_nb3sn_tea`)
- **Date executed:** 2026-09-30
- **Executor:** T-017 study executor, brief `work/orchestration/goals/magnet-material-comparison/evidence/briefs/t017-study-execute.md`, resumed on the coordinator's r5a ruling; repository HEAD `97fabad31` at execution
- **Mode:** execute
- **Arms:** `arm-reference`, `arm-rebco`, `arm-nb3sn` (one per unit; each unit is its own package and fingerprint)

## 2. Intake

The owner's goal and scope, in their own words, verbatim.

> Across explicit assumptions about confinement and coil geometry, when does each material give lower LCOE—and are those conditions supported by evidence?

[OWNER-VERBATIM] `work/orchestration/goals/magnet-material-comparison/goal.md` Amendment 2 (owner ruling of 2026-09-30).

[AGENT] Scope, in the executor's words: the declared case set of `exploration/stellarator_materials/studies/declare_cases.py` (`studies/cases.json`, 2,921 cases, sha256 `f07133ac…5e583`, present and matching, not regenerated), run against plant contract r5 with the r5a verification clause. Every case is retained whatever its status. The reference unit's pinned point and the REBCO unit's basis-bridge point supply the basis bridge of contract § 6.

## 3. Objective and result

- **LCOE objective channel(s):** `stellarator_09_materials__rebco_material__lcoe_calc__lcoe`, `stellarator_09_materials__nb3sn_material__lcoe_calc__lcoe` (USD/MWh at the plant's mixed money year; conductor prices USD2021); `stellarator_09__stellaris__lcoe_calc__lcoe` on the reference arm.
- **LCOE result:** in every cell where both materials have a supported design (8 of 9), Nb₃Sn's best supported design has the lower LCOE at 80 USD/m tape. The gap is 82.1–181.0 USD/MWh. The REBCO break-even tape price is 5.7–37.7 USD/m. Anchored × f_ren 1.0 has no supported Nb₃Sn design, so that cell reports no preference.

All values are from `results/summary.json` (package values). They are statuses and ranks under contract r5 § 7: supported means every check passes except the two open plant gaps, `tbr_ok` and `divertor_heat_ok`. The best design is the lowest-LCOE supported base design, meaning variant `none`, reference or companion offer, REBCO at 80 and Nb₃Sn at 8 USD/m. Across all cells the supported base designs span 429.7–3,662.2 USD/MWh for REBCO (171 designs) and 307.7–899.1 for Nb₃Sn (104).

| Cell | Best supported REBCO (LCOE) | Best supported Nb₃Sn (LCOE) | REBCO − Nb₃Sn | Break-even (USD/m) | Winner at 80 / 30 / 10 | Divertor-passing subset |
|---|---|---|---|---|---|---|
| anchored × 1.0 | 24.9 T, R 12.7 (587.2) | none (nearest: 13 T, R 22/a 2.2, failed `recirc_ok`, 609.4) | none | none | no preference | REBCO 20 T R 18 (608.1); no Nb₃Sn |
| anchored × 1.4 | 18 T, R 12.7 (429.7) | 13 T, R 22/a 1.8 (347.6) | +82.1 | 37.66 | Nb₃Sn / REBCO / REBCO | same pair, +82.1 |
| anchored × 1.8 | 18 T, R 12.7 (481.1) | 13 T, R 22/a 1.8, companion (348.7) | +132.4 | 26.20 | Nb₃Sn / Nb₃Sn / REBCO | same pair, +132.4 |
| HELIAS × 1.0 | 20 T, R 12.7 (533.0) | 13 T, R 22/a 2.2 (390.0) | +143.0 | 33.18 | Nb₃Sn / REBCO / REBCO | +143.8 (REBCO 18 T R 15) |
| HELIAS × 1.4 | 18 T, R 12.7 (469.4) | 12 T, R 15 (324.4) | +145.0 | 19.53 | Nb₃Sn / Nb₃Sn / REBCO | same pair, +145.0 |
| HELIAS × 1.8 | 12 T equal duty, R 12.7 (470.9) | 11 T, R 18, companion (321.1) | +149.8 | 5.68 | Nb₃Sn / Nb₃Sn / Nb₃Sn | same pair, +149.8 |
| arm × 1.0 | 24.9 T, R 12.7 (558.5) | 13 T, R 18 (378.2) | +180.3 | 28.34 | Nb₃Sn / Nb₃Sn / REBCO | +172.3 (Nb₃Sn 13 T R 22/a 2.2) |
| arm × 1.4 | 12 T equal duty, R 12.7, B_peak 20.67 T (466.2) | 13 T, R 12.7 (309.9) | +156.3 | 13.36 | Nb₃Sn / Nb₃Sn / REBCO | +169.9 (REBCO 20 T R 12.7) |
| arm × 1.8 | 12 T equal duty, R 12.7, B_peak 20.67 T (488.7) | 12 T, R 12.7 (307.7) | +181.0 | 11.10 | Nb₃Sn / Nb₃Sn / REBCO | same pair, +181.0 |

**What the break-even and winner columns mean:**
- The break-even is the highest tape price at which some supported base REBCO design reaches the cell's best Nb₃Sn LCOE. Each design's slope comes from its 80 and 30 USD/m evaluations.
- The 10 USD/m evaluation confirms the affine law on every design (worst relative residual 1.0e−15).
- One package evaluation at each solved price reproduces the target LCOE to 7.4e−16 relative, with the oracle agreeing on every channel (`results/breakeven_verification.json`, 16 evaluations including the variant cells).
- The winner at each price uses the best REBCO design re-selected at that price.

**Flags on the best designs** (`summary.json` cells), by material:
- REBCO at 24.9 T (anchored × 1.0, arm × 1.0) is `beyond_law_extents` and `above_stellaris_envelope`. REBCO at 20–22 T is `extrapolated`.
- The best Nb₃Sn design is a 13 T edge design (`extrapolated`, `envelope_flag`) in 5 of the 8 comparable cells. In all three arm cells it is also `arm_extrapolated` (R/√A_wp 17.3–21.6).

Across all 17 best designs:
- 8 are `power_short`, below matched fusion power.
- 10 violate the 0.04 beta verdict.
- 4 fail the divertor screen: REBCO anchored × 1.0, HELIAS × 1.0 and arm × 1.4, and Nb₃Sn arm × 1.0.
- Every design fails `tbr_ok`.

**Decomposition of REBCO − Nb₃Sn** (USD/MWh; per contract § 8 group at the REBCO design's energy, plus one net-electricity term; the terms sum to the difference to 1e−12):

| Cell | Conductor | Other winding | Structure | Refrig. capital | Radial build | Packages | CAS22 tail | Buildings | Multipliers and owner | O&M and replacements | Net electricity |
|---|---|---|---|---|---|---|---|---|---|---|---|
| anchored × 1.4 | 69.6 | −6.2 | −1.1 | −0.5 | −23.6 | −7.1 | 5.3 | −9.7 | 11.8 | 4.5 | 39.0 |
| anchored × 1.8 | 88.2 | −7.8 | −1.4 | −0.6 | −32.2 | −28.9 | 5.8 | −12.5 | 3.8 | −4.5 | 122.5 |
| HELIAS × 1.0 | 114.6 | −8.1 | −2.0 | −0.7 | −28.6 | 0.0 | 10.6 | −12.2 | 32.7 | 6.6 | 29.9 |
| HELIAS × 1.4 | 104.2 | 1.0 | 0.9 | −0.5 | −5.0 | 6.9 | 14.3 | −2.6 | 53.1 | 3.8 | −31.0 |
| HELIAS × 1.8 | 74.6 | −9.5 | −2.3 | −1.0 | −35.8 | −69.4 | 1.8 | −12.3 | −26.2 | −19.2 | 249.0 |
| arm × 1.0 | 143.5 | −3.6 | −0.5 | −0.7 | −14.6 | −0.2 | 17.4 | −6.1 | 60.1 | 3.7 | −18.4 |
| arm × 1.4 | 91.5 | −2.3 | −1.0 | −0.5 | −0.3 | 0.1 | 12.3 | −0.3 | 43.7 | −0.1 | 13.3 |
| arm × 1.8 | 113.5 | −0.7 | −0.2 | −0.6 | −0.4 | 0.0 | 15.7 | −0.3 | 56.1 | 0.0 | −2.2 |

Three groups are left out of the table because they are small: heating capital and fuel-cycle capital (within ±0.4) and fuel (CAS80, within ±0.1). "O&M and replacements" is CAS71 plus CAS72. The electricity drivers of the net-electricity term are reported per cell in `summary.json`: net power, refrigeration electricity (REBCO about 1.5 MW, Nb₃Sn 6.7–9.9 MW) and heating wall-plug power.

**Before the map (contract § 8):**
- **Basis bridge.** Reference instance 318.74 USD/MWh against the REBCO-material instance at the same supplied design, 412.43, a difference of +93.70. By group: conductor purchase +57.44, multipliers and owner +28.77, CAS22 tail +8.04, refrigeration capital −0.34, net electricity −0.21 (net power 850.07 against 850.63 MW). The bridge count is `1.5 × parallel_tapes_set` = 170.609 (A6); the 0.991 `f_set/f_wp_vol` factor is reported, not absorbed.
- **Equal duty.**
  - There are 189 base pairs (variant `none`): REBCO at the Nb₃Sn design's turns and current, same cell, target and size. The policy acceptance checks shared turns and current on 217 recorded pairs.
  - 27 pairs have both designs supported, all at the same operating point.
  - REBCO is dearer in all 27, by 122.8–370.7 USD/MWh.
  - Mean terms: conductor purchase 151.5, multipliers and owner 74.9, CAS22 tail 21.0, net electricity −3.8. Every other group is within ±1.
  - The capital-proportional multipliers and CAS22 tail carry up to 38 % of a pair's difference (finding #11).
- **Own highest field on the reference coil set** (anchored × 1.0, R 12.7). REBCO at 24.9 T is supported at 587.2. Nb₃Sn at 12 T fails `net_positive` and `recirc_ok`: it is power-short with negative net power, and its LCOE is −196.9, which is not an LCOE ranking. No decomposition is made.

**Variants** (`summary.json` `design_variants`, `reevaluation_variants`):
- **CPI 2021→2026:** Nb₃Sn wins all 8 comparable cells.
- **`k_link` 0.95 (HELIAS cells):** break-even 35.56 / 17.68 / 18.32 USD/m at f_ren 1.0 / 1.4 / 1.8, against base 33.18 / 19.53 / 5.68.
- **86 kA (HELIAS cells):** break-even 52.01 / 19.63 / 4.28.
- **Common-P (arm cells, REBCO on construction P, against the base Nb₃Sn best):** at f_ren 1.0 all 7 designs are capacity-limited (the cryo list is exhausted). Break-even 14.99 at 1.4 and 15.34 at 1.8, against 13.36 and 11.10.
- **Nb₃Sn strain −0.6 % (anchored cells):** f_ren 1.0 has no supported design; the best is 400.8 at 1.4 (base 347.6) and 404.4 at 1.8 (base 348.7).
- **Structure mass ×0.5 / ×2:**
  - HELIAS × 1.0: REBCO 530.0 / 538.8 (base 533.0), Nb₃Sn 385.8 / 398.4 (base 390.0).
  - HELIAS × 1.8: REBCO 469.1 / 474.6 (base 470.9), Nb₃Sn 319.0 / 325.3 (base 321.1).
- **Purchase exponent 0.5 / 1.0 (HELIAS × 1.8):** REBCO 472.2 / 469.3, Nb₃Sn 321.2 / 321.0.
- **Nb₃Sn price 5.4 / 13.5 (anchored cells):** best designs 335.7 / 372.7 (anchored × 1.4, base 347.6) and 336.3 / 374.9 (anchored × 1.8, base 348.7). Anchored × 1.0 still has no supported Nb₃Sn design.

## 4. Constraint outcomes

Every executing constraint, by qualified identity, with its outcome over the executed cases (`results/verification_summary.json` verdict counts, re-derived from the oracle; REBCO 2,111 evaluated cases, Nb₃Sn 806). Qualified ids are the unit prefix `stellarator_09_materials__rebco_material__` or `stellarator_09_materials__nb3sn_material__` plus the suffix shown; the reference arm's 67 ids (prefix `stellarator_09__stellaris__`) and their pinned statuses are in `results/baseline_result_reference.json`. No verdict was indeterminate on either side.

| `source_local_identity` | definition | REBCO `constraint_id` suffix | REBCO sat / viol | Nb₃Sn sat / viol | reference at pin |
|---|---|---|---|---|---|
| `acceptance_ok` | `magnet_conductor_alternatives::'Conductor Acceptance'` | `magnet__acceptance_ok__998be97e16fad569` (Nb₃Sn `…0f682bc3436c0794`) | 2097 / 14 | 798 / 8 | not in reference |
| `ampere_floor_ok` | `magnet_material_variants::'Ampere Floor'` | `magnet__ampere_floor_ok__527f82db402c44d5` (Nb₃Sn `…bbe387e1eb85f9b9`) | 1762 / 349 | 806 / 0 | not in reference |
| `beta_ok` | `mfe_viability::'Beta Limit'` | `beta_ok__35a0c2df4310d104` (Nb₃Sn `…a6d1355f00db8834`) | 2111 / 0 | 806 / 0 | satisfied |
| `burn_hold_ok` | `mfe_viability::'Burn Hold'` | `burn_hold_ok__b5da7626bab05382` (Nb₃Sn `…8a46a7e0aeda985a`) | 1971 / 140 | 771 / 35 | satisfied |
| `capacity_ok` | `magnet_conductor_alternatives::'Refrigerator Capacity'` | `cryoplant__capacity_ok__a7ae0d27f2e7a69e` (Nb₃Sn `…8830dacf5e39e904`) | 2090 / 21 | 804 / 2 | not in reference |
| `cold_stage_capacity_ok` | `mfe_viability::'Offered Equipment Capacity'` | `cold_stage_capacity_ok__3bc0a73db9d3e213` (Nb₃Sn `…53d0507e047820a1`) | 2090 / 21 | 804 / 2 | satisfied |
| `cond_strain_ok` | `mfe_viability::'Conductor Strain Limit'` | `cond_strain_ok__347e1ae0d46e036c` (Nb₃Sn `…404dca1f50a13e3a`) | 2111 / 0 | 806 / 0 | satisfied |
| `condensate_electric_capacity_ok` | `mfe_viability::'Offered Equipment Capacity'` | `condensate_electric_capacity_ok__d94728038066f7cb` (Nb₃Sn `…886bd4436560bb81`) | 2111 / 0 | 806 / 0 | satisfied |
| `condensate_flow_capacity_ok` | `mfe_viability::'Offered Equipment Capacity'` | `condensate_flow_capacity_ok__2853033437fa7007` (Nb₃Sn `…ced096a46a13bff0`) | 2111 / 0 | 806 / 0 | satisfied |
| `condensate_pressure_rise_capacity_ok` | `mfe_viability::'Offered Equipment Capacity'` | `condensate_pressure_rise_capacity_ok__79f16d6e8bc1b15b` (Nb₃Sn `…4758ab1d486197ab`) | 2111 / 0 | 806 / 0 | satisfied |
| `condenser_rejection_capacity_ok` | `mfe_viability::'Offered Equipment Capacity'` | `condenser_rejection_capacity_ok__1cdb674fdf5b2141` (Nb₃Sn `…27ac304fc5982908`) | 2111 / 0 | 806 / 0 | satisfied |
| `cooling_water_heat_direction` | `mfe_matched_steam_cycle::'Active Steam Heat Direction'` | `cooling_water_heat_direction__77d713899c16e2ab` (Nb₃Sn `…96754d6cc5733ef5`) | 2111 / 0 | 806 / 0 | satisfied |
| `copper_ok` | `magnet_conductor_alternatives::'Protection Copper Allowance'` | `magnet__copper_ok__4c832191ef5eb0d7` (Nb₃Sn `…be9121bc3fcdea7a`) | 2111 / 0 | 798 / 8 | not in reference |
| `cycle_domain_ok` | `mfe_viability::'Cycle Fit Domain'` | `cycle_domain_ok__bca3373bdd5bb090` (Nb₃Sn `…76acde2a26a78109`) | 2111 / 0 | 806 / 0 | satisfied |
| `direct_electric_capacity_ok` | `mfe_viability::'Offered Equipment Capacity'` | `direct_electric_capacity_ok__2ca22857e50ae9a8` (Nb₃Sn `…a285e66b19ed2cb4`) | 2111 / 0 | 806 / 0 | satisfied |
| `divertor_heat_ok` | `mfe_viability::'Divertor Target Heat Limit'` | `divertor_heat_ok__4848b02ea1557c2d` (Nb₃Sn `…84770e9a36dc1b57`) | 1300 / 811 | 495 / 311 | violated |
| `electric_gross_capacity_ok` | `mfe_viability::'Offered Equipment Capacity'` | `electric_gross_capacity_ok__6d466b03bfce1ad5` (Nb₃Sn `…488a485d1eb1e88b`) | 2111 / 0 | 806 / 0 | satisfied |
| `facility_capacity_ok` | `mfe_facilities::'Facility Nonnegative Margin'` | `facility_capacity_ok__c0747ad3c5d93311` (Nb₃Sn `…6d4fb7d42a36d0a7`) | 2111 / 0 | 806 / 0 | satisfied |
| `facility_geometry_ok` | `mfe_facilities::'Facility Nonnegative Margin'` | `facility_geometry_ok__0258a993c78f2ff1` (Nb₃Sn `…14b78dfe909c8501`) | 2111 / 0 | 806 / 0 | satisfied |
| `facility_initial_ready` | `mfe_facilities::'Facility Nonnegative Margin'` | `facility_initial_ready__d38e32e55e61fdc5` (Nb₃Sn `…bd8b5a0e4ec512f7`) | 2111 / 0 | 806 / 0 | satisfied |
| `facility_material_capacity_ok` | `mfe_facilities::'Facility Nonnegative Margin'` | `facility_material_capacity_ok__b001b53a93bea9e7` (Nb₃Sn `…c7de34bf2e881cc4`) | 2111 / 0 | 806 / 0 | satisfied |
| `facility_occupancy_ok` | `mfe_facilities::'Facility Nonnegative Margin'` | `facility_occupancy_ok__23c7d3c0c97b254a` (Nb₃Sn `…e81ea8f8cf26823a`) | 2111 / 0 | 806 / 0 | violated |
| `facility_outage_ok` | `mfe_facilities::'Facility Nonnegative Margin'` | `facility_outage_ok__12cedaf5124fff79` (Nb₃Sn `…93bfd834822ee642`) | 2111 / 0 | 806 / 0 | satisfied |
| `facility_parcel_ok` | `mfe_facilities::'Facility Nonnegative Margin'` | `facility_parcel_ok__09e54f5187da2c9f` (Nb₃Sn `…99f0ef2cd6538d03`) | 2111 / 0 | 806 / 0 | satisfied |
| `facility_replacement_ready` | `mfe_facilities::'Facility Nonnegative Margin'` | `facility_replacement_ready__b4650f2585ff4e4a` (Nb₃Sn `…7aa76b338808935e`) | 2111 / 0 | 806 / 0 | satisfied |
| `facility_routes_ok` | `mfe_facilities::'Facility Nonnegative Margin'` | `facility_routes_ok__31d1e5a5efc9b026` (Nb₃Sn `…50ce1d1c00491ff5`) | 2111 / 0 | 806 / 0 | satisfied |
| `feedwater_electric_capacity_ok` | `mfe_viability::'Offered Equipment Capacity'` | `feedwater_electric_capacity_ok__ec4b1f09526dad32` (Nb₃Sn `…c45a8ca67324291d`) | 2111 / 0 | 806 / 0 | satisfied |
| `feedwater_flow_capacity_ok` | `mfe_viability::'Offered Equipment Capacity'` | `feedwater_flow_capacity_ok__9871a398794bd034` (Nb₃Sn `…3bcdd6d04c7a0abb`) | 2111 / 0 | 806 / 0 | satisfied |
| `feedwater_pressure_rise_capacity_ok` | `mfe_viability::'Offered Equipment Capacity'` | `feedwater_pressure_rise_capacity_ok__2c733f473a68f18e` (Nb₃Sn `…92e4f80e79613b88`) | 2111 / 0 | 806 / 0 | satisfied |
| `fuel_processing_capacity_ok` | `mfe_fuel_cycle::'Fuel Processing Capacity'` | `fuel_processing_capacity_ok__4ccc57f69813cb74` (Nb₃Sn `…d36667b777c42fe9`) | 2111 / 0 | 806 / 0 | satisfied |
| `heating_couple_positive_ok` | `mfe_heating_chain::'Heating Efficiency Positive'` | `heating_couple_positive_ok__3969a43f5fda8071` (Nb₃Sn `…31dbd874e3b68e88`) | 2111 / 0 | 806 / 0 | satisfied |
| `heating_couple_upper_ok` | `mfe_heating_chain::'Heating Efficiency Upper'` | `heating_couple_upper_ok__d388de0d1f5a62b5` (Nb₃Sn `…0e4c29c53a56780e`) | 2111 / 0 | 806 / 0 | satisfied |
| `heating_source_positive_ok` | `mfe_heating_chain::'Heating Efficiency Positive'` | `heating_source_positive_ok__622599bd0a938078` (Nb₃Sn `…d489a4b936f894ba`) | 2111 / 0 | 806 / 0 | satisfied |
| `heating_source_upper_ok` | `mfe_heating_chain::'Heating Efficiency Upper'` | `heating_source_upper_ok__6811904a62eebc34` (Nb₃Sn `…91d002eb84ef7479`) | 2111 / 0 | 806 / 0 | satisfied |
| `helium_electric_capacity_ok` | `mfe_viability::'Offered Equipment Capacity'` | `helium_electric_capacity_ok__cb84e81c1d9f4ff2` (Nb₃Sn `…b6ae0d7d280eacb4`) | 2111 / 0 | 806 / 0 | satisfied |
| `helium_flow_capacity_ok` | `mfe_viability::'Offered Equipment Capacity'` | `helium_flow_capacity_ok__bf55136c825f0dde` (Nb₃Sn `…631fba08153122f2`) | 2111 / 0 | 806 / 0 | satisfied |
| `helium_pressure_rise_capacity_ok` | `mfe_viability::'Offered Equipment Capacity'` | `helium_pressure_rise_capacity_ok__800684f4fbfd04ab` (Nb₃Sn `…4bbd03d1c0fdffdc`) | 2111 / 0 | 806 / 0 | satisfied |
| `helium_pumping_capacity_ok` | `mfe_viability::'Offered Equipment Capacity'` | `helium_pumping_capacity_ok__b3df6c4ada78f0e8` (Nb₃Sn `…e41cbf588edbe7d8`) | 2111 / 0 | 806 / 0 | satisfied |
| `hp_flow_capacity_ok` | `mfe_viability::'Offered Equipment Capacity'` | `hp_flow_capacity_ok__ae582a956a8ee301` (Nb₃Sn `…cc7e78dbd3c706de`) | 2111 / 0 | 806 / 0 | satisfied |
| `hp_shaft_capacity_ok` | `mfe_viability::'Offered Equipment Capacity'` | `hp_shaft_capacity_ok__b373b1d4ff3823c8` (Nb₃Sn `…06729372362a4c6b`) | 2111 / 0 | 806 / 0 | satisfied |
| `ihx_capacity_ok` | `mfe_viability::'Intermediate Exchanger Capacity'` | `ihx_capacity_ok__e64acdb414b82e94` (Nb₃Sn `…e4869509b6443c3b`) | 2111 / 0 | 806 / 0 | satisfied |
| `intercept_stage_capacity_ok` | `mfe_viability::'Offered Equipment Capacity'` | `intercept_stage_capacity_ok__d3b9b3c84a8d0f8c` (Nb₃Sn `…94f24b6c7d86d868`) | 2111 / 0 | 806 / 0 | satisfied |
| `loop_capacity_ok` | `mfe_viability::'Loop Capacity'` | `loop_capacity_ok__d6532a89816fb7e2` (Nb₃Sn `…a12ef69878182648`) | 2111 / 0 | 806 / 0 | satisfied |
| `loop_pressure_ok` | `mfe_viability::'Loop Pressure Margin'` | `loop_pressure_ok__aef108bdfd08fc32` (Nb₃Sn `…f97fa1dc432c78ba`) | 2111 / 0 | 806 / 0 | satisfied |
| `lp_flow_capacity_ok` | `mfe_viability::'Offered Equipment Capacity'` | `lp_flow_capacity_ok__fbaebe15b4b2669f` (Nb₃Sn `…b9357da3012ec632`) | 2111 / 0 | 806 / 0 | satisfied |
| `lp_shaft_capacity_ok` | `mfe_viability::'Offered Equipment Capacity'` | `lp_shaft_capacity_ok__734f3bc0941a792d` (Nb₃Sn `…ef6a20387b2fc647`) | 2111 / 0 | 806 / 0 | satisfied |
| `magnet_pf_electric_capacity_ok` | `mfe_viability::'Offered Equipment Capacity'` | `magnet_pf_electric_capacity_ok__b38a37482abd8213` (Nb₃Sn `…ca95b633e7cc10d5`) | 2111 / 0 | 806 / 0 | satisfied |
| `magnet_tf_electric_capacity_ok` | `mfe_viability::'Offered Equipment Capacity'` | `magnet_tf_electric_capacity_ok__f8a1bf91be445766` (Nb₃Sn `…e99855ae6bf1b46e`) | 2111 / 0 | 806 / 0 | satisfied |
| `main_UA_capacity_ok` | `mfe_viability::'Offered Equipment Capacity'` | `main_UA_capacity_ok__c2196a4dedc17d72` (Nb₃Sn `…5ee8c284f5da46ad`) | 2111 / 0 | 806 / 0 | satisfied |
| `matched_main_heat_direction` | `mfe_matched_steam_cycle::'Active Steam Heat Direction'` | `matched_main_heat_direction__d54ab1b7234536a0` (Nb₃Sn `…67f41575de96bd94`) | 2111 / 0 | 806 / 0 | satisfied |
| `matched_reheat_heat_direction` | `mfe_matched_steam_cycle::'Active Steam Heat Direction'` | `matched_reheat_heat_direction__8bc64e6763926d8f` (Nb₃Sn `…9cff90d247be59e3`) | 2111 / 0 | 806 / 0 | satisfied |
| `net_positive` | `mfe_viability::'Net Power Positive'` | `net_positive__f137773a88435534` (Nb₃Sn `…2ff2061dd70a24f7`) | 1693 / 418 | 482 / 324 | satisfied |
| `pack_area_ok` | `magnet_conductor_alternatives::'Winding Fit'` | `magnet__pack_area_ok__4d2ccf27ef95a21a` (Nb₃Sn `…51632f8f2a7b1d5f`) | 2098 / 13 | 798 / 8 | not in reference |
| `peak_field_ok` | `mfe_viability::'Conductor Peak Field Limit'` | `peak_field_ok__d2be7a2c6d0ebc66` (Nb₃Sn `…1fcd44510d5ceb9a`) | 2111 / 0 | 579 / 227 | satisfied |
| `recirc_ok` | `mfe_viability::'Economic Recirculating Threshold'` | `recirc_ok__5d4235cfd9f4768c` (Nb₃Sn `…097dfc7574999504`) | 1362 / 749 | 338 / 468 | satisfied |
| `reference_conductor_current_ok` | `mfe_conductor_current::'Reference Conductor Current Margin'` | `reference_conductor_current_ok__0dd0d2cb1e851094` (Nb₃Sn `…ed9bbbfb7399171f`) | 2097 / 14 | 798 / 8 | violated |
| `reheat_UA_capacity_ok` | `mfe_viability::'Offered Equipment Capacity'` | `reheat_UA_capacity_ok__a8194f424b087b57` (Nb₃Sn `…3832be39603086f5`) | 2111 / 0 | 806 / 0 | satisfied |
| `represented_coolant_fill_ok` | `mfe_viability::'Represented Coolant Fill'` | `represented_coolant_fill_ok__bc6a51fed9b48ceb` (Nb₃Sn `…81ed94010b513177`) | 2111 / 0 | 806 / 0 | satisfied |
| `salt_electric_capacity_ok` | `mfe_viability::'Offered Equipment Capacity'` | `salt_electric_capacity_ok__99532fdbf4beb4d1` (Nb₃Sn `…320f302447d67a70`) | 2111 / 0 | 806 / 0 | satisfied |
| `salt_flow_capacity_ok` | `mfe_viability::'Offered Equipment Capacity'` | `salt_flow_capacity_ok__891f3985476a4a75` (Nb₃Sn `…090e097c99199295`) | 2111 / 0 | 806 / 0 | satisfied |
| `salt_head_capacity_ok` | `mfe_viability::'Offered Equipment Capacity'` | `salt_head_capacity_ok__88b673b363c69f34` (Nb₃Sn `…a3f15f8c47fee4d0`) | 2111 / 0 | 806 / 0 | satisfied |
| `salt_shaft_capacity_ok` | `mfe_viability::'Offered Equipment Capacity'` | `salt_shaft_capacity_ok__569c89a5b855b295` (Nb₃Sn `…316c1c5c7f51a07c`) | 2111 / 0 | 806 / 0 | satisfied |
| `steel_ok` | `magnet_conductor_alternatives::'Structural Steel Allowance'` | `magnet__steel_ok__3833f52286c5bd91` (Nb₃Sn `…3f894fc95501d96d`) | 2111 / 0 | 806 / 0 | not in reference |
| `sustainment_ok` | `mfe_viability::'Sustainment Limit'` | `sustainment_ok__60ca4f2cb2aaa5bd` (Nb₃Sn `…1a778604648c352e`) | 2111 / 0 | 806 / 0 | satisfied |
| `tbr_ok` | `mfe_tritium_breeding::'Computed TBR Adequacy'` | `tbr_ok__8ce4a3c0d3818607` (Nb₃Sn `…d57174176b5d2862`) | 0 / 2111 | 0 / 806 | violated |
| `turbine_gross_capacity_ok` | `mfe_viability::'Offered Equipment Capacity'` | `turbine_gross_capacity_ok__887d77cd5a478001` (Nb₃Sn `…946403aa70c1c824`) | 2111 / 0 | 806 / 0 | satisfied |
| `wall_load_ok` | `mfe_viability::'Neutron Wall Load Limit'` | `wall_load_ok__bb886accb1fe4358` (Nb₃Sn `…41289e190845d753`) | 1832 / 279 | 782 / 24 | satisfied |
| `water_electric_capacity_ok` | `mfe_viability::'Offered Equipment Capacity'` | `water_electric_capacity_ok__c74614e39b597493` (Nb₃Sn `…d2e2ee4a515ad778`) | 2111 / 0 | 806 / 0 | violated |
| `water_flow_capacity_ok` | `mfe_viability::'Offered Equipment Capacity'` | `water_flow_capacity_ok__2a464637ca64c033` (Nb₃Sn `…71de9e2671863dbc`) | 2111 / 0 | 806 / 0 | satisfied |
| `water_head_capacity_ok` | `mfe_viability::'Offered Equipment Capacity'` | `water_head_capacity_ok__ab846ad3af228cf2` (Nb₃Sn `…148d2392c7e3b09e`) | 2111 / 0 | 806 / 0 | satisfied |
| `water_rejection_capacity_ok` | `mfe_viability::'Offered Equipment Capacity'` | `water_rejection_capacity_ok__b282501b0da7ba05` (Nb₃Sn `…f150ed41745d4a0f`) | 2111 / 0 | 806 / 0 | satisfied |
| `wp_fit_ok` | `mfe_winding_pack_fit::'Winding Pack Fits Casing'` | `wp_fit_ok__63e3c00c99928ca9` (Nb₃Sn `…11c66596aad579df`) | 2111 / 0 | 806 / 0 | violated |
| `wp_stress_ok` | `mfe_viability::'Winding Pack Stress Limit'` | `wp_stress_ok__fdb21f48452667e8` (Nb₃Sn `…c61cade8f669c8f2`) | 2037 / 74 | 806 / 0 | satisfied |

`peak_field_ok` is the supplied `B_max` envelope, carried as `envelope_flag`; `tbr_ok` and `divertor_heat_ok` are open plant gaps carried with their margins (contract r5 § 7). The four refused REBCO cases carry no verdicts. The reference column is its one pinned point.

**Statuses** (re-derived from the recorded verdicts, recorded inputs and the design's operating-point class; `statuses.py`; identical to the oracle scan's on every case):

| | failed | supported | ignited | capacity-limited | unsupported |
|---|---|---|---|---|---|
| REBCO (2,115) | 1,158 | 792 | 140 | 21 | 4 (domain refusals) |
| Nb₃Sn (806) | 480 | 289 | 35 | 2 | 0 |

**Checks named in the reasons of failed and capacity-limited cases** (a case can name several; `summary.json` `flags_and_failed_checks`):
- REBCO: `recirc_ok` 734, `net_positive` 406, `ampere_floor_ok` 330, `wall_load_ok` 246, `wp_stress_ok` 70, `acceptance_ok` and `reference_conductor_current_ok` 14 each (the MR-7 insufficient offers), `pack_area_ok` 13, `capacity_ok` and `cold_stage_capacity_ok` 21 each.
- Nb₃Sn: `recirc_ok` 468, `net_positive` 324, `wall_load_ok` 20, `acceptance_ok`, `reference_conductor_current_ok`, `copper_ok` and `pack_area_ok` 8 each, `capacity_ok` and `cold_stage_capacity_ok` 2 each.

MR-7: all 22 insufficient offers fail `acceptance_ok`. All 22 generous offers pass it, and 21 of them fail `pack_area_ok`, so every MR-7 offer is `failed`.

## 5. Framing

**As proposed at intake.**

| Axis | Framing proposed | Why |
|---|---|---|
| `assumption-confinement` | sensitivity | The owner's question asks for the map across confinement assumptions; the cells are values of an assumption, not a design search. |
| `assumption-geometry` | sensitivity | Same: the three geometry assumptions (anchored, HELIAS-class, pack-size arm) span the map. |
| `duty` | search | Turns, current, size and allocation walk the designs across fit, stress, Ampère-floor, wall-load and power-balance verdicts; statuses are the point. |
| `operating-point` | search | The ladder temperature and density decide matched, ignited and power-short designs and the recirculating-power and divertor margins. |
| `winding-offer` | search | Element count and pack are sized at the acceptance and pack-area boundaries (MR-7 insufficient and generous offers straddle them). |
| `plant-offer` | search | Re-supplied ratings, classes and facilities decide the capacity and facility screens (capacity-limited designs). |
| `economic-assumptions` | sensitivity | Prices and the CPI factor move LCOE at fixed designs; the break-even price is the reported response. |
| `conductor-assumptions` | sensitivity | Nb₃Sn intrinsic strain (−0.6 % variant) moves the conductor law at fixed design intent. |

**As judged after the run.**

| Axis | Framing judged | Changed? | Why |
|---|---|---|---|
| `assumption-confinement` | sensitivity | no | Statuses and LCOE move with f_ren; no boundary is claimed in f_ren, which has three values. |
| `assumption-geometry` | sensitivity | no | Three discrete geometry assumptions; responses reported per cell. |
| `duty` | search | no | Verdict structure is present: `recirc_ok`, `net_positive`, `ampere_floor_ok`, `wall_load_ok`, `wp_stress_ok` all bind somewhere. |
| `operating-point` | search | no | Matched, ignited (175) and power-short (1,804) designs; the ladder choice decides divertor and recirculating-power margins. |
| `winding-offer` | search | no | Acceptance and pack area sit at allowance by construction; the MR-7 offers flip `acceptance_ok` as designed. |
| `plant-offer` | search | no | Re-supply leaves every package and facility screen satisfied except the exhausted cryo list (23 capacity-limited). |
| `economic-assumptions` | sensitivity | no | No verdict moves with price; LCOE is affine in tape price (residual ≤ 1e−15). |
| `conductor-assumptions` | sensitivity | no | Strain −0.6 % raises the best Nb₃Sn LCOE by 53–56 USD/MWh in the anchored cells; no boundary claim. |

## 6. Per-axis account

#### `assumption-confinement` — feasible structure (search framing)
**Applies:** not applicable — this axis is sensitivity-framed.

#### `assumption-confinement` — observed response (sensitivity framing)
**Applies:** yes

Supported base designs at f_ren 1.0 / 1.4 / 1.8:
- Nb₃Sn: anchored 0 / 6 / 12, HELIAS 6 / 16 / 20, arm 7 / 14 / 23.
- REBCO: anchored 15 / 18 / 21, HELIAS 14 / 14 / 12, arm 11 / 24 / 42.

Ignited designs appear at f_ren 1.4 and 1.8 in every geometry (10–52 per cell), and in 4 REBCO designs at HELIAS × 1.0. The best designs' LCOE does not fall monotonically with f_ren (anchored REBCO 587.2 / 429.7 / 481.1). No boundary claim is made. Violations by location are in § 4 and `results/cases.csv`.

#### `assumption-geometry` — feasible structure (search framing)
**Applies:** not applicable — this axis is sensitivity-framed.

#### `assumption-geometry` — observed response (sensitivity framing)
**Applies:** yes

At each f_ren the arm cell has the lowest best Nb₃Sn LCOE: 378.2 / 309.9 / 307.7 at f_ren 1.0 / 1.4 / 1.8, against HELIAS 390.0 / 324.4 / 321.1 and anchored none / 347.6 / 348.7. Those arm designs are `arm_extrapolated` (R/√A_wp 17.3–21.6). REBCO's equal-duty designs on the arm reach B_peak 20.67 T at 12 T targets. `ampere_floor_ok` fails only on REBCO (349 cases), in anchored (126) and HELIAS (223) cells and never under the arm. `wp_stress_ok` fails only on REBCO. No boundary claim is made.

#### `duty` — feasible structure (search framing)
**Applies:** yes

Active constraints (oracle-scan verdicts over all evaluated cases):
- `recirc_ok` and `net_positive` fail most often at small R and low field. `recirc_ok` fails on 142 of 174 Nb₃Sn cases at 10 T against 100 of 228 at 13 T, and on 204 of 260 REBCO cases at 10 T against 39 of 277 at 24.9 T.
- `wall_load_ok` fails only at R 10 and 11 (REBCO 279 cases at 12–24.9 T, Nb₃Sn 24 at 12–13 T).
- `ampere_floor_ok` fails on REBCO, mostly at 10–12 T targets (327 of 349), more often at larger R.
- `wp_stress_ok` fails on REBCO at 22–24.9 T and R 18–22 (74 cases).

The constrained optimum per cell is the best supported design of § 3: R 12.7 for REBCO in every cell, R 12.7–22 for Nb₃Sn. The grid has seven sizes and discrete fields, so optima are grid points, not located boundaries.

#### `duty` — observed response (sensitivity framing)
**Applies:** not applicable — this axis is search-framed.

#### `operating-point` — feasible structure (search framing)
**Applies:** yes

`burn_hold_ok` is violated on exactly the ignited designs (REBCO 140, Nb₃Sn 35). `divertor_heat_ok` passes on REBCO 1,300 and Nb₃Sn 495 evaluated cases; no single heating level separates passing from failing designs. Matched designs sit on the temperature ladder at 13–18 keV, 620 of 938 at 13 keV.

#### `operating-point` — observed response (sensitivity framing)
**Applies:** not applicable — this axis is search-framed.

#### `winding-offer` — feasible structure (search framing)
**Applies:** yes

`acceptance_ok`, `copper_ok` and `pack_area_ok` sit at allowance on the policy's designs: near-threshold acceptance on REBCO 2,083 and Nb₃Sn 790, pack area on 1,303 and 754. MR-7 insufficient offers fail acceptance (22 of 22). Generous offers pass acceptance (22 of 22), and 21 of 22 fail `pack_area_ok`.

#### `winding-offer` — observed response (sensitivity framing)
**Applies:** not applicable — this axis is search-framed.

#### `plant-offer` — feasible structure (search framing)
**Applies:** yes

After re-supply every package, facility and IHX screen is satisfied on every evaluated case. The only exceptions are the cold-stage capacity checks at the top of Round 1's cryo list (REBCO common-P at arm × 1.0: 21 cases; Nb₃Sn 86 kA at HELIAS × 1.0: 2), which are filed capacity-limited. Twenty-five re-supplied quantities carry no cost response (`free_capacity`, finding #12).

#### `plant-offer` — observed response (sensitivity framing)
**Applies:** not applicable — this axis is search-framed.

#### `economic-assumptions` — feasible structure (search framing)
**Applies:** not applicable — this axis is sensitivity-framed.

#### `economic-assumptions` — observed response (sensitivity framing)
**Applies:** yes

LCOE is affine in the tape price at a fixed design. REBCO's slope sets break-even prices of 5.7–37.7 USD/m (§ 3). The winner changes to REBCO between 80 and 30 USD/m in 2 of the 8 comparable cells and between 30 and 10 USD/m in 5 more. HELIAS × 1.8 stays Nb₃Sn at 10 USD/m. The CPI variant leaves Nb₃Sn the winner everywhere. No verdict or status differs between a design and its price or CPI re-evaluations (1,806 compared). No boundary claim is made.

#### `conductor-assumptions` — feasible structure (search framing)
**Applies:** not applicable — this axis is sensitivity-framed.

#### `conductor-assumptions` — observed response (sensitivity framing)
**Applies:** yes

At −0.6 % strain the Nb₃Sn designs are re-sized: the best 13 T design at R 22/a 1.8 carries 1,209 elements against 506 at −0.3 %. Anchored × 1.0 still has no supported design. The best LCOE rises 53–56 USD/MWh at f_ren 1.4 and 1.8. No boundary claim is made.

## 7. Axis groups

Declared per unit in `axes_reference.json`, `axes_rebco.json` and `axes_nb3sn.json` (`declare_axes.py`). There is one file per unit because each unit is a separate package with its own key prefix, and `preflight.py` validates a declaration against one package. Every key has provenance `fan_out`; there are no ties. The complete expansion is in those files; the table gives each group's attributes after the unit prefix.

| Axis | Entry key (suffix after the unit prefix) | Provenance | Note |
|---|---|---|---|
| `assumption-confinement` | `plasma__f_ren`, `beta_limit` | fan_out | 2 keys per unit |
| `assumption-geometry` | `magnet__coil__peak_ratio`, `magnet__coil__arm_slope`, `magnet__coil__arm_x_ref`, `magnet__coil__k_link` | fan_out | 4 keys per unit |
| `duty` | `magnet__coil__reference_turns`, `magnet__coil__turn_current`, `plasma__R`, `plasma__a`, `magnet__coil__coil_t`, `magnet__casing__interior_y` | fan_out | 6 keys per unit |
| `operating-point` | `plasma__n_e0`, `plasma__T_i0` | fan_out | 2 keys per unit |
| `winding-offer` | `magnet__n_elements`, `magnet__winding_pack__wp_side`, `magnet__winding_pack__B_max`, the 13 construction keys `magnet__{cu_space, steel_area, misc_area, solder_area, ins_fraction, cabling_factor, cable_void, J_cu_rule, cu_void, cu_per_kA_rule, steel_per_kA_rule, B_steel_ref, steel_B_scaling}` | fan_out | 16 keys per material unit; 2 on the reference |
| `plant-offer` | every other key of the design § 5.1 varied family plus the 15 held plant keys the policy re-supplies (facility positions, receipt leads, parcel offsets, service teams, IHX count) | fan_out | 184 keys per unit |
| `economic-assumptions` | `magnet__element_price_per_m`, `cryoplant__usd2015_to_2021` | fan_out | material units only |
| `conductor-assumptions` | `magnet__conductor__eps_intrinsic_in` | fan_out | Nb₃Sn only; [AGENT] addition (the strain variant moves it; no brief group names it), accepted by the coordinator |

Totals: reference 200 keys in 6 groups, REBCO 216 in 7, Nb₃Sn 217 in 8. `declare_axes.py` checks that every key any declared case moves off the package default lies in exactly one group. The reference unit's groups are declared for the seam's gates and declined: the reference is pinned and only its baseline point runs.

## 8. Indicators and rulings

The indicator reports are `indicators_{unit}.json`, from `scripts/study/indicators.py` over every declared group of every unit. They were run through the record-local shim `run_indicators.py`, accepted by the coordinator:
- The stock tool refused all three packages ("constraint … has no matching module in the pipeline"). It finds a constraint's module by its id, and codegen lower-cases the module names of `main_UA_capacity_ok` and `reheat_UA_capacity_ok` (finding #1).
- The shim also registers each such module under its constraint id, only where the module name is exactly the id lower-cased.
- The reachability trace reads the untouched `deps` and `producer` maps, so no trace result changes. The aliases are in `indicators_{unit}.aliases.json`.
- The material units' reports were regenerated after the r5a manifest change. Their group results are identical to the pre-r5a reports, which are kept in `superseded/`; only the cited manifest digest differs.

| Axis | Indicator | Ruling | Note |
|---|---|---|---|
| `assumption-confinement` | constraints_reachable (53 of 67 reference, 53 of 73 per material) | none needed | swept (cells) |
| `assumption-geometry` | constraints_reachable (57/67; 62/73) | none needed | swept (cells) |
| `duty` | constraints_reachable (61/67; 67/73) | none needed | swept |
| `operating-point` | constraints_reachable (53/67; 53/73) | none needed | swept |
| `winding-offer` | constraints_reachable (61/67; 67/73) | none needed | swept |
| `plant-offer` | constraints_reachable (56/67; 61/73) | none needed | swept |
| `economic-assumptions` | constraints_reachable (5/73) | none needed | swept; no verdict moved in any price or CPI re-evaluation (§ 6) |
| `conductor-assumptions` | constraints_reachable (5/73) | none needed | Nb₃Sn only; swept |

No group reported `no_constraint_response`, so no ruling under the owner brief's delegated study authority was required and no model-development finding follows from the indicators.

**Not derivable, disclosed in every record.** These are not decidable from the indicator run and no indicator output claims them: monotonicity of any channel in any axis; identity of the same physical quantity across differing key names; intra-module operand dependency. `constraints_reachable` is a *possible* path and never a statement that a constraint responds. `unresisted` is the agent's recorded judgment, never a tool output.

**Model-development findings.** Not applicable: no axis reported `no_constraint_response`.

| Axis | What should push back and is not modeled | Finding id |
|---|---|---|
| none | not applicable: every axis reaches at least five constraints | none |

## 9. Preflight results

`scripts/study/preflight.py gates` ran per unit. It read `results/package_identity_{unit}.json` and `results/baseline_result_{unit}.json`, which `run_baseline.py` deposited through `route_entry.py`, and wrote `results/preflight_results_{unit}.json`; the material units were re-run on the r5a manifests. All six gates passed on all three units, and again inside every seam run.

| Gate | Outcome | Detail |
|---|---|---|
| Declared-group key validation | pass (all three) | 200 / 216 / 217 declared keys, all package inputs |
| Suffix-sibling scan (advisory) | pass, 1 warning per unit | reference: undeclared `stellarator_09__stellaris__cryoplant__purchase_cost_per_module` beside `plant-offer`'s declared purchase-cost keys. Material units: undeclared `…__magnet__winding_pack__cabling_factor` beside the declared `magnet__cabling_factor` of `winding-offer`. Not merged: they are keys of different calcs. |
| Executable identity, recomputed | pass (all three) | sealed digests `86648d36…52a1c2a`, `f441442c…4fe6`, `6ccbab50…eeba482` recomputed; every other sealed artifact matches |
| Baseline gate against the pinned headline | pass (all three) | reference 318.7377471541504 at relative 0 and 67/67 verdicts; REBCO 412.4334208430638 at relative 0 and 73/73; Nb₃Sn −196.89511818207214 against the oracle's −196.89511818207208 at relative 2.9e−16 and 73/73 |
| Manifest / package fingerprint match | pass (all three) | both recorded package fingerprints match the package on disk |
| Package cleanliness | pass (all three) | package tree byte-untouched (git clean) |

## 10. Execution route and why

- **Route:** study-local direct-API with a prepared list. `exploration/stellarator_materials/studies/study_route.py:run_points` uses the stock `ProvisionalPackageLoader`, `PreparedEvaluator`, `StudyRunner`, `PreparedListStrategy`, `StudyStore` and `StudyQuery`, with one store per unit (`execute_study.py`).
- **Why this route:** the cases are coordinated designs (each sets up to 195 keys at once), not a Cartesian grid, so the `teax-study` CLI cannot express them. One case also evaluates one of three packages. The route was first exercised at the three baselines, then gated by preflight and by the seam's gate 7 on every unit before the declared cases ran.

`route_entry.py` adapts only the call signature the seam uses, `callable(out, package_dir=, manifest_path=)`, to `run_points`. The package route's own `execute_baseline(name, out_dir)` reads the unit's stock manifest, and the Nb₃Sn unit has none.

**Glue disclosure.** Glue ledger: none. No adapter supplies a value the model does not compute; the three-unit split is a route fact (design K21). One value-neutral case-to-proposal mapping is disclosed. Every Nb₃Sn case carries `magnet__eps_min = −0.01`, a package constant rather than an entry key, so it is dropped from each proposal after checking it equals the constant (finding #4); the oracle holds the same value. The break-even verification (§ 3) adds 16 evaluations of declared REBCO designs with only `magnet__element_price_per_m` changed, in a separate store.

## 11. Study definition and window provenance

**Candidate set:** the declared case list, not a swept window.
- Before execution every case was evaluated with the independent oracle (`oracle_scan.py`), on the same proposal the package would receive, and its contract § 7 status derived from the oracle's own values (`statuses.py`). Per-case rows are in `results/oracle_scan.json` (machine-local); counts are in `results/oracle_scan_summary.json`.
- The scan fixed nothing, and the executed list equals the declared list.
- The scan's status counts equal the executed counts of § 4 on every case: failed 1,638, supported 1,081, ignited 175, capacity-limited 23, unsupported 4.

**Status labels against the policy:** 133 re-evaluation cases of ignited (119) and capacity-limited (14) designs carry the policy label `failed`. Contract § 7 applied to the held design gives `ignited` or `capacity-limited`, and the record's derivation is used (finding #6, accepted).

**Near-threshold** (a status-deciding operand within 0.02 × its scale of the threshold; [AGENT] rule in `statuses.py`):
- Acceptance: REBCO 2,083, Nb₃Sn 790; pack area: 1,303 and 754. Both are at allowance by construction.
- Divertor: 257 and 72; wall load: 129 and 10; recirculating power: 19 and 6; net power: 4 and 6.
- REBCO only: Ampère floor 73, stress 12.

The window is engineered: it is the contract's declared design grid and variants, not a sourced operating envelope, and no continuous boundary or optimum in any axis is claimed from it. No validity mask is applied.

**Integration pins** (`scripts/integrate.py`, teax `8d877460ac4f6f264561d916e40c1708adb13397`, out-dirs `work/orchestration/goals/magnet-material-comparison/evidence/integration-r3-{unit}/`). One staged source tree yields three unit fingerprints:

| Unit | Class | Audited work | Pin | Semantic fingerprint | Executable fingerprint |
|---|---|---|---|---|---|
| reference | CANDIDATE, ten gates pass | `WI-100@899fb6a3b` | `4229205b12ed80f3da3430bf075efc79364c88ce5bec768e785e9c1db4a859fc` | `a2b225a5eb30edfd8d23fe99f127169bbb45b80b5feca563f30fc7d6f4db7a9a` | `86648d368246011bc881accdee635c14fca656d5042031dfce7fb498052a1c2a` |
| rebco | CANDIDATE, ten gates pass | `WI-100@97fabad31` | `f3884b47541a2122a44572759b6df9122869ad12212fbe383c228f3fcc5c6e75` | `6b920b065e17ff3baca4b92d177bffa235647bddd9a7fc8ddb16535fd4e0ae7e` | `f441442c116ed0bdb1cd438ccfd282146b312b20db928039da61b59719624fe6` |
| nb3sn | CANDIDATE, ten gates pass | `WI-100@97fabad31` | `804bc4d45e7e5c7ad019906c2fe5c542dff8aa87bee69e7eeff2e66b04cb8f99` | `8b2212e2a2baa972b52d6eee7d392c8e711b367221724a56530f75a6bd5972b7` | `6ccbab50fa407d545fe40529f29d35680e0c153090880599a28142c06eeba482` |

Earlier runs, kept for the record:
- The Nb₃Sn BLOCKER (gate 8 `verification-refused`, at `@899fb6a3b` on the pre-r5a manifest) is in `integration-r3-nb3sn/blocker-run/`.
- The first REBCO CANDIDATE (`@899fb6a3b`, pre-r5a manifest) is in `integration-r3-rebco/first-run/`. REBCO was re-run so that its CANDIDATE names the manifest bytes the study used.
- The reference manifest did not change, so its first CANDIDATE stands.
- Commit `97fabad31` changed only the contract and the trail; no package or WI-100 byte differs between the audited commits.

## 12. Cross-fingerprint correlation and what it means

The arms span three fingerprints (§ 11).
- **How constraints were matched.** Across arms they were matched by `definition_qualified_name` plus `source_local_identity`, never by constraint id: ids carry the unit prefix and a hash.
- **REBCO against Nb₃Sn.** Both material units carry the same 73 definitions with identical `predicate_ir`.
- **Reference against the material units.** The reference's 67 definitions are among them, again with identical `predicate_ir`. The material units add six checks: `acceptance_ok`, `copper_ok`, `steel_ok`, `pack_area_ok`, `ampere_floor_ok` and `capacity_ok`. The one operand re-pointing (E6: `reference_conductor_current_ok` reads `magnet__conductor__acceptance_margin` in material units) is in the operand binding, not the IR.
- **What the correlation licenses:** comparing a verdict of the same definition across the two material arms, and the basis bridge between the reference and REBCO arms at one supplied design.
- **What it does not license:** reading the reference's `reference_conductor_current_ok` as the same quantity as the material units' version.

## 13. Verification

**Passed on every case for the independently compared channels, under contract r5a § 9: within 1e−9 relative or 1e−9 absolute per unit, whichever is looser.** Constants and the two static-load channels without an oracle leg are excluded as listed below. Results are in `results/verification_summary.json`, from `verify_all.py`, which covers every stored case without sampling.

- **Channels.** Comparisons run on 1,423 REBCO and 1,422 Nb₃Sn non-constant channels: 3,003,953 and 1,146,132 comparisons, with 0 disagreements.
  - The absolute clause was needed only by these channels: the Nb₃Sn Tcs-derived margins (`magnet__conductor__acceptance_margin` and `temp_rule_margin`, 685 cases each, at most 4.46e−11 K), Nb₃Sn `magnet__area__cu_margin` (74 cases, at most 2.3e−13 mm² per turn), and on both units the five closure residuals of the matched cycle and cooling water (at most 1.4e−12 MW or kg/s, against oracle values near zero).
  - Every other channel agrees to relative 1.3e−11 (REBCO) and 4.3e−11 (Nb₃Sn).
- **Verdicts.** All 73 constraints of every evaluated case were re-derived from the oracle's operands through the package's predicate IR and published bindings, and also compared with the oracle's own Kleene verdict: 0 mismatches, 0 indeterminate.
- **Refusals.** The four REBCO refusals are refused by both sides. Package: "SustainmentError: non-positive fuel density…". Oracle: "RuntimeError: oracle sustainment: non-positive fuel".
- **Statuses.** Re-derived statuses equal the oracle scan's on all 2,921 cases.
- **Baselines** (`results/verification_baselines.json`). All 1,353 / 1,423 / 1,422 channels of the three pinned points agree.
- **Stock verifier** (`scripts/study/verify.py`, every stored case sampled, the manifests' four declared absolute tolerances).
  - REBCO passes on 2,111 rows in 43 strata, 110 channels and 73 re-derived verdicts; worst 1.25e−11 relative (`acceptance_margin`).
  - Nb₃Sn passes on 806 rows in 30 strata, 110 channels and 73 verdicts; worst `acceptance_margin` at 1.9e−6 relative, inside its declared absolute tolerance.
  - The reference passes on its one baseline row, 104 channels and 67 verdicts; worst 2.4e−15.
- **Break-even verification.** 16 evaluations at the solved prices: LCOE reproduces the target to 7.4e−16, and the oracle agrees on every channel.
- **Policy acceptance** (`policy_acceptance.py`, `results/policy_acceptance.json`, on the package's own values for all 885 evaluated recorded designs; the four refused designs have no values). Outcome: pass, 0 failures.
  - The package reproduces the policy's recorded `p_fus`, `p_aux_required` and `B_peak` exactly (worst deviation 0), `beta` under the r5a clause, 18,585 recorded expectation channels under the r5a clause, and all 885 violated-verdict lists.
  - 341 matched designs are within 0.5 %, and 544 power-short designs are below matched power. 660 own-sized designs are within 0.1 T of target.
  - The policy's re-supply rules hold on every recorded design: heating, structure mass, cold and intercept ratings from the list, screened ratings at 1.05 × demand (24,780 checks), offered states (6,195), purchased masses (1,770), purchase costs at exponent 0.7 (3,540), the IHX count and cooling facilities, and the magnet sized to its checks.
  - The 22 power classes use the r5a clause: 834 of 19,470 comparisons differ from the package's recomputed powers at ≤ 3.8e−15 (finding #14).
  - MR-7 offers and 217 equal-duty turn and current pairs hold.

**What verification did not cover:**
- **Constant channels** (excluded): `cryoplant__nist_k_{a,d,g,i}__nist_k_*` on both material units and `magnet__eps_min__eps_min` on Nb₃Sn.
- **No oracle leg:** `cryoplant__static_loads__nuclear_density_eff` and `cryoplant__static_loads__q_structure_nuclear`. The executor's identity checks hold on all 2,917 evaluated cases: input `q_nuc_structure` = 0, `q_structure_nuclear` = 0, `nuclear_density_eff` = the winding pack's `q_nuc_cryo` (finding #5).
- **Values fed identically to both sides** are verified only as arithmetic given those values: the declared supplied design and the held plant and material facts.
- **The oracle's choices.** The oracle composes the plant oracle's function-level pieces with re-derived inline equations. Where both it and the package re-derive a plant equation from the same SysML, an error common to both readings would not show.
- **The policy acceptance** is the package reproducing the oracle-evaluated policy record; it does not independently check the policy's search (for example Q29's four unsearched refused designs).

## 14. Review outcomes

| Lens | Verdict | Disposition |
|---|---|---|
| Contract review and recheck (reused coverage) | `evidence/plant-contract-review.md`: r1 REVISE, r2 RELEASE, r5 RELEASE; r5a is a coordinator correction of the § 9 tolerance clause (`97fabad31`) | Valid for this study: r5/r5a is the governing contract and the case set was declared under r5. |
| Field-relations check (reused coverage) | `evidence/check-field-relations.md`: both relations PASS WITH CORRECTIONS, applied in r4 | Valid: the Ampère floor and arm relations are unchanged in r5. |
| Design review and recheck (reused coverage) | `evidence/design-review-wi100.md`: PASS WITH CORRECTIONS; recheck PASS WITH CORRECTIONS (D1–D18 resolved, remaining R-items left to the coordinator); coordinator amendments A1–A8 in design § 9 | Valid: seam gates 2–6 pass on all three units at the audited commits. |
| Pre-execution framing critique | not triggered: no new or reinterpreted source or math; no axis reported `no_constraint_response` | Coordinator check sufficient (`modeling_project/STUDY_POLICY.md` § 11). |
| Verification tolerance (premise conflict) | contract r5 § 9 as written refused a package that reproduced the oracle within its root solver's stated precision | Surfaced, study stopped; coordinator ruled r5a; resolved (finding #2). |
| Executor deviations | indicators shim, per-unit axes and oracle modules, the `conductor-assumptions` group, the `eps_min` drop, the § 7 status derivation over the policy's labels on re-evaluations | Accepted by the coordinator and recorded in the trail. |

## 15. Findings

| Id | Kind | Finding | Disposition | Home |
|---|---|---|---|---|
| `20260930-magnet-material-plant-map#1` | process | The indicators tool refuses all three WI-100 packages: it finds a constraint's module by id, and codegen lower-cases the `main_UA_capacity_ok` and `reheat_UA_capacity_ok` module names. | Indicators produced through the disclosed alias shim `run_indicators.py`; tool fix not routed to an item. | `scripts/study/indicators.py` |
| `20260930-magnet-material-plant-map#2` | process | Contract r5 § 9's relative-1e−9 clause could not be met on the two Nb₃Sn Tcs-derived margin channels (package bisection 1e−10 K against oracle Brent 1e−13 K, margins ≈ 1e−3 K). | Ruled: r5a (`97fabad31`) restores 1e−9 absolute per unit; manifests declare it; seam re-run CANDIDATE; every case verified. | `work/orchestration/goals/magnet-material-comparison/evidence/plant-contract.md` § 9 |
| `20260930-magnet-material-plant-map#3` | process | The stock manifests name a nonexistent oracle module and no Nb₃Sn manifest exists; `verify.py` reads one module's bindings as a package's whole table; `oracle_glue` imports the plant seam as top-level `oracle_entry`. | Record binds `oracle_entry.py` by dotted name with one `oracle_{unit}.py` per unit and writes all three manifests. | `exploration/stellarator_materials/studies/rebco/manifest.json` |
| `20260930-magnet-material-plant-map#4` | process | Every Nb₃Sn case carries `magnet__eps_min`, a package constant the route refuses as an entry key. | Dropped after an equality check against the package constant; disclosed in § 10. | `exploration/stellarator_materials/studies/declare_cases.py` |
| `20260930-magnet-material-plant-map#5` | process | Two A2 channels (`cryoplant__static_loads__nuclear_density_eff`, `cryoplant__static_loads__q_structure_nuclear`) have no oracle leg. | Not independently verified; identity checks hold on all 2,917 evaluated cases. | `exploration/stellarator_materials/oracle-reuse.json` |
| `20260930-magnet-material-plant-map#6` | process | The policy's `status_expected` reads `failed` on 133 re-evaluations of ignited and capacity-limited designs. | Statuses re-derived by the record; accepted by the coordinator. | `exploration/stellarator_materials/studies/offer_policy.py` |
| `20260930-magnet-material-plant-map#7` | model | Anchored × f_ren 1.0 has no supported Nb₃Sn design (0 of 135); the nearest fails only `recirc_ok`; REBCO has 15 supported base designs there. | Fact of the run; the cell reports no preference. | `unrouted` |
| `20260930-magnet-material-plant-map#8` | model | Four HELIAS × 1.8 REBCO designs (22–24.9 T, R ≥ 18 m) are refused by the sustainment solve (non-positive fuel density) in both package and oracle; no Nb₃Sn case was refused. | Filed `unsupported (domain refusal)`; the policy searched no other operating point for them (Q29). | `exploration/stellarator_materials/studies/offer_policy.py` |
| `20260930-magnet-material-plant-map#9` | model | The best supported Nb₃Sn design sits at the 13 T edge (`extrapolated`, `envelope_flag`) in 5 of the 8 comparable cells and is `arm_extrapolated` in all three arm cells. | Flags carried per design; the evidence labels of the map are the coordinator's. | `work/orchestration/goals/magnet-material-comparison/evidence/plant-contract.md` § 3.2 |
| `20260930-magnet-material-plant-map#10` | model | 8 of the 17 best supported designs are power-short and 10 of 17 violate the 0.04 beta verdict, so cell rankings compare designs at different fusion power. | Reported per design; ranking rule unchanged (contract § 7, Q22). | `work/orchestration/goals/magnet-material-comparison/evidence/plant-contract.md` § 7 |
| `20260930-magnet-material-plant-map#11` | model | Equal-duty pair differences reach non-magnet accounts: capital-proportional multipliers and the CAS22 tail carry up to 38 % of the difference. | Reported with the decomposition. | `work/orchestration/goals/magnet-material-comparison/evidence/plant-contract.md` § 1 |
| `20260930-magnet-material-plant-map#12` | model | Every evaluated design names 25 re-supplied quantities with no cost response (`free_capacity`). | Stated limit carried per design. | `work/orchestration/goals/magnet-material-comparison/evidence/plant-contract.md` § 10 |
| `20260930-magnet-material-plant-map#13` | model | `tbr_ok` fails on every evaluated design; `divertor_heat_ok` fails on 4 of the 17 best supported designs; every comparable cell's winner is unchanged on the divertor-passing subset. | Open plant gaps carried with margins (contract r5 § 7). | `work/orchestration/goals/magnet-material-comparison/evidence/plant-contract.md` § 7 |
| `20260930-magnet-material-plant-map#14` | process | The policy's power-class read-back is exact against the oracle's powers; against the package's recomputed powers 834 of 19,470 comparisons differ at ≤ 3.8e−15. | Record's acceptance applies the r5a clause and counts the misses. | `tests/study/test_stellarator_materials_policy.py` |

**Homes a finding may route to:** tool, runbook step, policy rule, skill, modeling item, research round, documented seam. `unrouted` is a stated state, not a blank.

## 16. Snapshot

- **File:** `snapshot.json`
- **sha256:** d494d0e92768ff6ed2498c32f9d24fc1cee9e8562cf863e269f92a01eed46de7
- **Schema version:** `1`

The round's pin set is the § 11 table: three `CANDIDATE`s from one staged source tree (reference `4229205b…59fc`, REBCO `f3884b47…6e75`, Nb₃Sn `804bc4d4…8f99`), recorded with their fingerprints under `arms[].integration`. No snapshot content is restated here.

## 17. What this record does not contain

- **No goal-level interpretation.** The record has no map labels ([S]/[A]/[D]/[U] per best design), no comparison label, no policy-assumption column and no proposed narrative. These are the coordinator's (contract § 8).
- **No figures or figure data.** `results/cases.csv` and `results/summary.json` are the data a renderer would read.
- **No interaction analysis.** The contract's break-even against field, size and f_ren is not given beyond the per-cell and per-variant break-even prices in `summary.json`.
- **No CPI-scaled break-even price.** The CPI variant reports winners and LCOE gaps only.
- **No break-even for strain or structure-mass variants**, and none for the purchase-exponent variant, which has a single cell.
- **Nothing on an unselected material instance.** Each unit carries one material instance (K21), so none exists.
- **Machine-local artifacts are not in git.** These are the native stores, the full per-case exports (`results/cases_{unit}.json`), `results/oracle_scan.json` and `results/oracle_verification.json`; their digests are in `snapshot.json`.
- **Executor did not commit** (brief t017: do not commit). The coordinator completed snapshot resolution on 2026-10-04 and commits this record through runbook step 15. Goal-level interpretation and review are separate later artifacts.
