# Comparison basis, tolerances and sensitivity ranges — declared before the study executes (T-004)

Revised 2026-09-25 after the fresh pre-execution review r1 (`pre-execution-review.md`); corrections are marked `[r1]`. No tolerance or materiality line in § 3 changed.

[AGENT] Written 2026-09-25 by the round-1 coordinator before any study point runs, from the reviewed source boundary (`exploration/aries_integrated/studies/20260922-aries-integrated-lcoe/source-evidence/source-boundary.md`, read against `work/active/WI-088_aries-source-budget-cost-contribution/evidence/lyon-p707.png`, `lyon-p709.png`, `lyon-p716.png` in the WI-091 design review), the WI-091 convention (F1–F9), the configuration record and the equipment/cost audit. Nothing here is tuned to the published 77.6; every substitution of a published quantity is a labelled diagnostic, never an independent prediction. Provenance grades: `[SOURCE]` printed in Lyon 2008; `[DERIVED]` arithmetic on printed values; `[ASSUMED]` an agent convention or bound.

## 1. Accounting basis of the published figure against our alternative

| Item | Published ARIES (Lyon 2008, Table VII p716, Table III p707, text p707/p709) | Our alternative (WI-091 convention on the 891 MW case) | Aligned-convention step in the study (diagnostic) | Status |
|---|---|---|---|---|
| Currency year | `[SOURCE]` year-2004 dollars; 77.6 mills/kWh = 77.6 USD2004/MWh | constant USD2004 | none needed | aligned |
| Net versus gross | `[SOURCE]` cost of electricity per net kWh at 1000 MW net (1253 MW gross; Table VII p716, Table IV p708 and p707 text `[r1]`); 7,446,000 MWh/year at 85 % | per net MWh at 891.0017 MW net (1143.013 gross); 6,634,398 MWh/year at 0.85 | the existing `source_finance` branch with `source_finance__net_power` at 1000 MW (denominator and capital substituted together) and at 891.0017 MW (capital only), so the denominator and capital-scope effects separate | aligned by substitution; labelled |
| Availability | `[SOURCE]` 85 %; the O&M cost separately "include[s] a factor 0.85" (p707 wording; `[r1]`) | 0.85 productive fraction | none (the O&M credit is not applied a second time) | aligned |
| Lifetime | `[SOURCE]` "40 full-power years", and Eq. 7 multiplies life by availability; p709 also says 40 full-power years | 40 calendar years | `cost_schedule__plant_years` 47 `[DERIVED]`: 40 / 0.85 = 47.06 calendar years; the model requires an integer, so 47 (39.95 FPY) | ambiguity retained; step labelled |
| Financing and construction | `[SOURCE]` direct × 1.93 inclusive of construction services, engineering, owner costs, contingencies, interest and escalation during construction; a high borrowed-capital rate inherited from 1990s studies, value not stated | 5 % real; six-year construction as one midpoint adjustment (× 1.1576 on overnight); overnight = direct × 1.49 (20 % indirect, 20 % contingency, 5 % owner) | the `source_finance` branch takes 5,055,773,960 USD2004 (2,619,572,000 × 1.93) as already financed with a second financing guarded at exactly zero; the discount rate is swept 0–10 % because the source rate is not printed | rate unresolved; scope aligned by substitution |
| Capital scope and contingency | `[SOURCE]` Table III eight parents 2,619.572 MUSD2004 (Table VII rounds to 2620); contingency inside the 1.93 | direct 2,925.686 MUSD2004 = source-scope leaves 2,619.603 (0.031 core excess retained) + initial tritium stock 300.000 + changed purchases 6.083 | same branch (capital substituted); the 300 MUSD stock and the 6.083 MUSD changed purchases are part of the capital-scope difference and are reported separately | aligned by substitution; labelled |
| Fuel | `[SOURCE]` Eq. 7's fuel is deuterium; no tritium purchase, stock or supply charge appears | no-credit: 138.730 kg/year purchased at 30 MUSD2004/kg; feed100: 100 kg/year new usable feed with a 30 MUSD2004/year service charge, 38.730 kg/year still purchased | `fuel_inventory__annual_recovery_kg` = 138.7304019114013 (the case's own gross makeup) with `finance__supply_service_annual` 0: "self-sufficient tritium at no charge, as the source's fuel description implies"; a diagnostic, not a breeding claim | supply capability unsupported in every case; step labelled |
| O&M | `[SOURCE]` ≈ 14 % of CoE with the 0.85 credit; `[DERIVED]` 77.6 × 0.14 × 7,446,000 = 80,893,344 USD2004/year, target-derived, not independently reported | 70,000,000 USD2004/year allowance (E7/F8), referenced to a 1000 MW plant | `annual_om__selected_amount` 80,893,344 (target-derived; labelled) | step labelled; independent amount unknown |
| Replacements | `[SOURCE]` 842 t and 75 MUSD2004 "for each time" (p709 wording `[r1]`), 13 operating replacements, 966 MUSD2004 printed (975 rounded); `[DERIVED]` E8: cadence 15.7 / 5.4 = 2.907407 FPY | 6 events × 72,231,350 USD2004 (5 FPY selected life at 0.85 → every 5.882 calendar years), dated, no reserve | `cost_schedule__replacement_life_fpy` 2.907407 with `replacement_factor` 75,000,000 / 72,231,350 = 1.038329 `[DERIVED]`: at 40 calendar years the model gives ceil(40 / 3.42048) − 1 = 11 events; with 47 years, ceil(47 / 3.42048) − 1 = 13, the source's count | step labelled; the source figure is undiscounted |
| Decommissioning | `[SOURCE]` 0.5 mills/kWh in 1992 dollars, including waste disposal | gross terminal 10 % of overnight at year 40 less 2 % salvage (F4/F5) | none: no deflator or timing is printed, so the source amount cannot be converted; terminal fraction swept 0.05–0.2 | unresolved |
| Physical output | `[SOURCE]` 2436 MW fusion, 1253 gross, 1000 net at 43 % | 2436 MW supplied, 1143.013 gross, 891.0017 net at 0.3907 (Q1, unresolved in the prior goal) | never substituted into the independent alternative; the branch at 1000 MW is the labelled diagnostic | the output gap is attributed, not closed |

## 2. The aligned-convention ladder (every step a labelled diagnostic substitution on the canonical case) `[r1]`

L0 the independent alternative under each fuel scenario (no substitution). L1 the `source_finance` branch read at our net (capital scope only; designs `diag-L1-*`). L2 the branch at the supplied 1000 MW (capital scope and denominator), read from the `alt-canonical-*` cases' own branch channel (no separate design; the branch default is 1000 MW). L3 O&M 80,893,344 (target-derived from 77.6 itself; every rung that inherits it carries that label). L4 47 calendar years. L5 the source replacement cadence and event price (11 events at 40 years; 13 at 47). L6 self-sufficient tritium at no charge. L7 the combination L3 + L4 + L5 + L6 on our capital and our net, read through the branch at our net and at 1000 MW. L8 discount rate 0, 3, 8 and 10 % on L7.

Reporting order, fixed here: (a) one-at-a-time, each step from its named base (L3, L4 and L5 from `alt-canonical-feed100`; L5 also from L4 as `diag-L5-source-cadence-47y-feed100`; L6 from `alt-canonical-no-credit`); (b) cumulative in the stated order from `alt-canonical-feed100`: C1 = L3, C2 = L3 + L4, C3 = L3 + L4 + L5, C4 = L3 + L4 + L5 + L6 (= L7); (c) the combined case against the sum of the one-at-a-time steps, with the difference reported as the interaction. Because the tritium purchase dominates the no-credit numerator, a step's effect depends on its base, so (a) and (b) are both reported and neither is presented as the other. (d) The residual against 77.6 is reported at every swept discount rate (0, 3, 5, 8, 10 %); the source's rate is not printed, so no rate is designated as the published one and no rung is called the match. The gap that remains is reported as unresolved with the missing evidence named (the source's financing rate and schedule, its decommissioning conversion, its independent O&M amount, its treatment of tritium).

## 3. Tolerances and materiality, declared before execution and not relaxed afterwards

| Quantity | Rule |
|---|---|
| Study verification | every stored case against the package-owned oracle: relative 1e-9 on nonzero channels; the live manifest's six reviewed absolute tolerances (`residual_magnitude` 1e-7 MW, `idc` two ULP, the four unmet-heat channels 1e-7 MW); every verdict re-derived exactly |
| Replay of canonical bases | bit-exact against the sealed stores (T-001 rule) |
| LCOE differences reported but not separated as causes | below 0.1 USD2004/MWh |
| A material LCOE difference (must be explained, bounded or marked unresolved) | ≥ 1.0 USD2004/MWh (1.3 % of the published 77.6) in the aligned comparison; ≥ 1 % of the alternative's own LCOE in the independent assessment |
| Material capital difference | ≥ 10 MUSD2004 overnight |
| Net electricity | the prior goal's budget ±15 MW is inherited, not re-derived; the alternative's output is fixed by T-001 |
| Fuel quantities | agreement between package, oracle and first-principles arithmetic at relative 1e-9 (T-003) |

## 4. Sensitivity ranges and their justification

| Axis (entry keys) | Values | Basis | What it bounds |
|---|---|---|---|
| Compressor price factor (`compressor_equipment__price_factor`) | 0.5, 1.5 | E4 package-price range | the changed equipment's own price uncertainty |
| Cycle-side correlated factor (`turbine_equipment`, `generator_equipment`, `electrical_equipment`, `heat_rejection_equipment` `__price_factor`) with the compressor, `conversion_services` and `secondary_transport` factors set to the same value in the corner designs | 0.5, 1.5, 2.0 | E4 range and a 2.0 corner for correlated underestimate of the whole cycle side at 1143 MW gross | the fixed source-scope allowances (sized for the 1253 MW gross ARIES plant) applied to this configuration |
| `conversion_services__price_factor` | 2, 4, 6 | `[ASSUMED]` recuperator bound: balanced counterflow NTU = ε/(1 − ε) rises 4 → 19 (× 4.75) and the cycle capacity rate × 1700/1400 = 1.214, so a UA-proportional recuperator would cost ≈ 5.8× its baseline share; the whole 62.912 MUSD allowance scaled by 6 is the upper proxy | the unpurchased 0.95 recuperator (audit item 1) |
| `secondary_transport__price_factor` | 1.214, 1.5 | flow-proportional proxy (1700/1400) and the E4 upper bound | cycle-side transport at the higher flow (audit item 2) |
| Tritium price (`fuel_inventory__tritium_price`) | 1e7, 1e8 USD2004/kg | E6 range | the dominant no-credit term, both scenarios |
| New feed (`fuel_inventory__annual_recovery_kg`) at 30 MUSD/year service | 50, 138.7304019114013 (= gross makeup, purchases zero), 150 (curtailed) | F7 range around the named 100 kg/year; the makeup value shows the purchase floor | the unsupported supply assumption |
| Service charge (`finance__supply_service_annual`) at 100 kg/year | 1e7, 1e8 USD2004/year | F7 range | the unsupported supply cost |
| Availability (`cost_schedule__availability`) | 0.75, 0.95 | E7/F3 | energy and fuel against the fixed calendar feed, both scenarios |
| Discount rate (`finance__discount_rate`) | 0.03, 0.08, 0.10 (0 in the ladder) | F1 | the unknown source rate |
| Construction (`finance__construction_years`) | 0, 10 | F2 | the midpoint financing |
| Terminal fraction (`finance__terminal_fraction`) | 0.05, 0.2 | F4 | the unconvertible source decommissioning |
| Plant years (`cost_schedule__plant_years`) | 30, 60 (47 in the ladder) | F3 | the FPY/calendar ambiguity |
| O&M (`annual_om__selected_amount`) | 35e6, 140e6 | E7/F8 | the allowance |
| Replacement life (`cost_schedule__replacement_life_fpy`) | 2, 3.7673466400138413 `[DERIVED]` (5 × 1468.361 / 1948.8: the baseline's 5 FPY at the alternative's +32.7 % neutron power), 8 (2.907407 in the ladder) | E8 range plus the fluence-scaled applicability point | the selected life's applicability to this configuration |
| PbLi pump electric (`pbli_pump__pump_mode` 1 with `pbli_pump__fixed_power`) | 10, 30 MW | `[ASSUMED]` order-of-magnitude bound for MHD pumping that E3 leaves unmodelled (the baseline's 0.01 MW is a placeholder); the model's unchanged input `pbli_recovery` 0 means none of it returns as heat (not set by the study) `[r1]` | an unresolved auxiliary load; changes net electricity, so it is thermal, not only cost |
| Compressor rating (`compressor_capacity__selected_rating`) | 1600 | adverse control; the screen fails by 67.033 MW | that inadequacy stays visible |
| He pump capacity (`he_pump__selected_flow_capacity`) | 3261 | adverse control; the screen fails by 98 kg/s | same |
| Estimate mode (`cost_accounts__estimate_mode`) | 1 | the fixed-budget nonresponse | that the fixed-budget mode is not a hardware-cost law |
| Source branch net (`source_finance__net_power`) | 891.0016527219543, 1000 | the ladder's L1/L2 | capital scope against denominator |

Every axis is sensitivity-framed; none searches for an optimum; none sizes equipment from demand; the adverse cases are retained unrelabelled.
