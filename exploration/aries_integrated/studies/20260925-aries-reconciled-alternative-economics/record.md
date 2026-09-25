# Record: 20260925-aries-reconciled-alternative-economics

## 1. Study header

- **Study id:** `20260925-aries-reconciled-alternative-economics`
- **Package:** `aries_integrated` (WI-092 identity, unchanged since round 2 of the prior goal: executable `f739dbce67699b7adfae7c1adf5599ab7c30e85987caad53e0f8affd9b880ce4`, semantic `78dd23bf4c4a2d431ce8223d973db08e955e6f378175623ced8b976db4231f93`; integration candidate `work/orchestration/goals/aries-reference-heat-electricity-reconciliation/evidence/integration-attempt2/integration_return.json` reused without re-pin)
- **Date executed:** `2026-09-25`
- **Executor:** Claude coordinator of goal `aries-reconciled-alternative-economics` (round 1, T-004); executor reporting, not an independent administrator reading.
- **Mode:** execute
- **Arms:** single arm, `arm-economics`

Arms are variants of the same question, run to be compared. Two studies asking different
questions of the same package are two records, not two arms of one.

## 2. Intake

[OWNER-VERBATIM] From `work/orchestration/goals/aries-reconciled-alternative-economics/evidence/owner-brief.md`:

> What does this explicitly modified plant cost, what is its LCOE under stated fuel-supply assumptions, and what explains its economic differences from the published ARIES estimate?

> This is a fresh economic assessment. The 891 MW configuration is a modeled alternative, not a reconstructed ARIES reference. Agreement with the published LCOE is not a tuning target.

> Retain separately named scenarios covering: No breeding credit, with required external tritium purchases. The previously used assumed new-tritium-feed scenario, with its quantity, price, availability and accounting meaning stated explicitly.

> Separate a comparison using aligned accounting conventions from our independently evaluated alternative. [...] Never substitute published electricity or cost totals into a result described as an independent prediction. Any diagnostic substitution must be separately labeled.

> Choose a small set of uncertainties that could materially change the economic conclusion, including the changed equipment's cost and tritium-supply assumptions. Justify the ranges. The purpose is to determine which conclusions survive those assumptions, not to optimize until the result resembles published ARIES economics. Retain failed cases and explain where numerical evaluability or scientific support ends.

[AGENT] Executor additions: the study runs on the unchanged WI-092 package identity. Canonical bases are the verbatim stored input maps of four sealed cases (the canonical alternative `resized-compressor-1700-network-scaledflows-0.85` and its unscaled control from `20260925-aries-flow-scaling-check`; `nominal-calculated` and `nominal-source-assumed` from `20260925-aries-revised-reference-network`), replayed bit-exactly on this package at the goal's T-001. Every other case composes declared changes on a named base: the two fuel scenarios with the WI-091 meanings; an aligned-convention ladder (L1–L8) toward the published economics in which every substitution of a published quantity is a labelled diagnostic (the existing `source_finance` branch read at our net and at the supplied 1000 MW; target-derived O&M; 47 calendar years; the source replacement cadence and event price; self-sufficient tritium at no charge; discount-rate steps); and one-at-a-time sensitivities whose ranges are justified in the goal's `evidence/comparison-basis.md` § 4, including the bounds for the costs the audit graded unresolved (recuperator, cycle-side transport, PbLi pumping) and two adverse controls. Tolerances and materiality were declared in that file before execution. Nothing is tuned to the published 77.6 USD2004/MWh; no axis sizes equipment from demand.

## 3. Objective and result

- **LCOE objective channel(s):** `aries_integrated_plant__lifecycle_price__evaluate__lcoe` (the independent alternative, USD2004/MWh) with its eleven contribution channels `aries_integrated_plant__lifecycle_accounts__evaluate__*_lcoe`; `aries_integrated_plant__source_lifecycle_price__evaluate__lcoe` (the separately labelled source-conditioned diagnostic branch: supplied 1000 MW net unless the `source_net_power` axis sets our net, and the already-financed 5,055,773,960 USD2004 capital); `cost_ledger__evaluate__overnight`, `lifecycle_accounts__evaluate__financed_capital`, `cost_ledger__evaluate__annual_operating`, `lifecycle_accounts__evaluate__external_shortfall`, `plant_ledger__evaluate__net_electric`.
- **LCOE result:** the canonical 891 MW alternative gives **685.695 USD2004/MWh under `no-breeding-credit`** (tritium purchases 627.323, 91.5% of the total; financed capital 44.329; O&M 10.551; dated replacements 1.568; overhaul 0.722; terminal 0.544 less salvage 0.109; consumables 0.754; deuterium 0.014) and **238.028 under `assumed-new-tritium-feed-100`** (tritium 175.135 for the residual 38.730 kg/year purchase; supply service 4.522; everything else unchanged). Both points satisfy every evaluated check. Overnight capital 4359.272 MUSD2004 (direct 2925.686), financed 5046.402 after one midpoint construction adjustment of 687.130; annual delivered electricity 6,634,398 MWh at 0.85; annual operating cost 4237.0 MUSD2004/year (no credit; O&M 70.0, external tritium 4161.9 for 138.730 kg/year at 30 MUSD/kg, deuterium 0.092, consumables 5.0) or 1237.0 (feed100, plus the 30 MUSD/year service charge outside that channel); six dated blanket/divertor/LiPb events of 72.231 MUSD2004 (PV 178.455); an other-equipment overhaul of 217.964 at year 20; gross terminal 435.927 less salvage 87.185 at year 40. The source-conditioned branch reads 611.193 (no credit) and 212.322 (feed100); it is a diagnostic, never the prediction.

**Over the studied space.** Against the 423 MW assumed baseline the alternative is cheaper per MWh without breeding credit (1119.408 → 685.695, Δ -433.713: tritium -369.369, capital -48.827, O&M -11.668, the other seven contributions -3.849 together) and **more expensive under the fixed 100 kg/year feed** (176.687 → 238.028, Δ 61.342: tritium 130.687 because the fixed feed covers 34.063 kg/year less of the larger makeup, supply -5.001, capital -48.827, O&M -11.668, the rest -3.849); the ordering is set by the supply assumption, not by the plant. The unscaled-mapping control differs by 0.019 USD2004/MWh (capital 0.018: the two pump purchases). The changed equipment itself is worth little: the compressor rating moves the LCOE by 0.076 per 100 MW and its E4 price range by ±0.650. The aligned-convention ladder (§ 6, `results/attribution.md` § C) reduces the gap to the published 77.6 USD2004/MWh from 160.428 (feed100, our conventions) to a band that brackets it: with self-sufficient tritium, target-derived O&M, 47 calendar years and the source replacement cadence, our LCOE is 59.313 at 5 % real (31.885 / 46.008 / 84.687 / 104.898 at 0 / 3 / 8 / 10 %) and the branch at 1000 MW gives 53.058 (30.659 / 42.740 / 70.745 / 83.404); the source's rate is not printed and no rate is designated as the match. Capital scope is a near-wash (the branch at our net differs from our own accounting by 0.267: our direct × 1.49 × 1.1576 against the source's × 1.93); the denominator (1000 against 891.002 MW) is worth -25.974 at feed100 and -6.491 in the aligned case. The sensitivities (§ 6) show tritium price and feed moving the result by hundreds of USD2004/MWh, availability and the discount rate by tens, and the bounds on the unresolved recuperator, cycle-side and PbLi-pumping costs by 4.89, 9.33 and 8.29 at their upper values.

## 4. Constraint outcomes

Every generated constraint identity appears below; there are no indeterminate statuses. "Satisfied" means the evaluated scalar check passes, not scientific feasibility. Three of 64 cases fail exactly one check each; 61 satisfy all 14.

| `constraint_id` | `source_local_identity` | Status | Note |
|---|---|---|---|
| `aries_integrated_plant__compressor_capacity__capacity_ok__a45f9cf05e8aa7ab` | `capacity_ok` | satisfied / violated | Violated in 1 of 64: `adverse-compressor-rating-1600-feed100` (demand 1667.033 MW on the inherited 1600 MW rating, margin -67.033; adverse control). |
| `aries_integrated_plant__divertor_capacity__capacity_ok__be7081920ad8e8ed` | `capacity_ok` | satisfied | All 64. |
| `aries_integrated_plant__divertor_pump__capacity_ok__d6730c7060447f4c` | `capacity_ok` | satisfied | All 64. |
| `aries_integrated_plant__fuel_capacity__capacity_ok__8eb5888bfe62cd64` | `capacity_ok` | satisfied | All 64. |
| `aries_integrated_plant__fuel_inventory__capacity_ok__37f4667fbfb616d0` | `capacity_ok` | satisfied | All 64. |
| `aries_integrated_plant__generator_capacity__capacity_ok__60b43f15d48ff161` | `capacity_ok` | satisfied | All 64. |
| `aries_integrated_plant__he_capacity__capacity_ok__db2733d1d5baf3cf` | `capacity_ok` | satisfied | All 64. |
| `aries_integrated_plant__he_pump__capacity_ok__fcee5ee009fe5180` | `capacity_ok` | satisfied / violated | Violated in 1 of 64: `adverse-he-pump-capacity-3261-feed100` (capacity 3261 kg/s against the 3359 kg/s operating flow, margin -98.0; adverse control). |
| `aries_integrated_plant__pbli_capacity__capacity_ok__55a012a287da9395` | `capacity_ok` | satisfied | All 64. |
| `aries_integrated_plant__pbli_pump__capacity_ok__79d116aa320dd4fb` | `capacity_ok` | satisfied | All 64. |
| `aries_integrated_plant__plant_ledger__balances_ok__9af2e85b5e4e5535` | `balances_ok` | satisfied | All 64. |
| `aries_integrated_plant__plant_ledger__heat_removal_ok__695378663bcd8d07` | `heat_removal_ok` | satisfied / violated | Violated in 1 of 64: `original-source-assumed-no-credit` (158.726 MW unremoved; the retained original failing case). |
| `aries_integrated_plant__rejection_capacity__capacity_ok__295420bc9fb25608` | `capacity_ok` | satisfied | All 64. |
| `aries_integrated_plant__turbine_capacity__capacity_ok__089f9e8e61919ec1` | `capacity_ok` | satisfied | All 64. |

## 5. Framing

**As proposed at intake.** [AGENT] Every axis is sensitivity-framed: the study measures response to declared assumption, scenario and price changes on fixed hardware and, in the ladder, to labelled substitutions of published conventions (one-at-a-time from named bases, cumulatively in the stated order, and combined); it searches for no boundary and no optimum. No axis sizes equipment; the adverse controls keep the failing selections visible. Revised after the fresh pre-execution review r1 (`…/evidence/pre-execution-review.md`): two cumulative ladder designs added, two O&M case names corrected, the ladder's reporting order fixed in `…/evidence/comparison-basis.md` § 2.

| Axis | Framing proposed | Why |
|---|---|---|
| `source_net_power` | sensitivity | Lyon Table IV prints 1000 MW net (the branch default); role source; no search. |
| `annual_om` | sensitivity | E7/F8 allowance 70 M [35, 140]; role assumed; no search. |
| `plant_years` | sensitivity | F3 40 [30, 60]; role assumed; no search. |
| `replacement_life` | sensitivity | E8 5 [2, 8]; role assumed; no search. |
| `replacement_factor` | sensitivity | E8 1 [0.5, 2]; role assumed; no search. |
| `new_feed` | sensitivity | F7: 0 (no credit), 100 (named scenario), 50, 150; role assumed; no search. |
| `supply_service` | sensitivity | F7: 0 or 30 M (named scenario); role assumed; no search. |
| `tritium_price` | sensitivity | E6 30 M [10 M, 100 M]; role assumed; no search. |
| `availability` | sensitivity | E7/F3 0.85 [0.75, 0.95]; role assumed; no search. |
| `discount` | sensitivity | F1 0.05 [0, 0.10]; role assumed; no search. |
| `construction` | sensitivity | F2 6 [0, 10]; role assumed; no search. |
| `terminal` | sensitivity | F4 0.10 [0.05, 0.20]; role assumed; no search. |
| `compressor_price` | sensitivity | E4 [0.5, 1.5] on the changed equipment; role assumed; no search. |
| `cycle_side_price` | sensitivity | E4 [0.5, 1.5] applied jointly to the cycle-side allowances sized for the 1253 MW gross source plant, plus a 2.0 corner; role assumed; no search. |
| `conversion_services_price` | sensitivity | [ASSUMED] recuperator bound: NTU 4 -> 19 (x 4.75) with capacity rate x 1.214 gives a UA-proportional x 5.8; role assumed; no search. |
| `secondary_transport_price` | sensitivity | Flow-proportional proxy 1700/1400 = 1.214 and the E4 upper bound 1.5; role assumed; no search. |
| `pbli_pump_mode` | sensitivity | 0 cubic proxy (baseline); role operating; no search. |
| `pbli_pump_fixed_power` | sensitivity | [ASSUMED] order-of-magnitude bound 10 and 30 MW for PbLi MHD pumping that E3 leaves unmodelled; role operating; no search. |
| `compressor_rating` | sensitivity | 1700 (the declared alternative); role purchased; no search. |
| `he_pump_capacity` | sensitivity | 3359 (declared mapping value); role purchased; no search. |
| `estimate_mode` | sensitivity | 0 selected-quantity estimates; role accounting; no search. |

**As judged after the run.**

| Axis | Framing judged | Changed? | Why |
|---|---|---|---|
| `source_net_power` | sensitivity | no | observed response recorded in § 6; no boundary was sought or found; the two adverse controls and the retained original case are the only violated points, each by the check its input targets. |
| `annual_om` | sensitivity | no | observed response recorded in § 6; no boundary was sought or found; the two adverse controls and the retained original case are the only violated points, each by the check its input targets. |
| `plant_years` | sensitivity | no | observed response recorded in § 6; no boundary was sought or found; the two adverse controls and the retained original case are the only violated points, each by the check its input targets. |
| `replacement_life` | sensitivity | no | observed response recorded in § 6; no boundary was sought or found; the two adverse controls and the retained original case are the only violated points, each by the check its input targets. |
| `replacement_factor` | sensitivity | no | observed response recorded in § 6; no boundary was sought or found; the two adverse controls and the retained original case are the only violated points, each by the check its input targets. |
| `new_feed` | sensitivity | no | observed response recorded in § 6; no boundary was sought or found; the two adverse controls and the retained original case are the only violated points, each by the check its input targets. |
| `supply_service` | sensitivity | no | observed response recorded in § 6; no boundary was sought or found; the two adverse controls and the retained original case are the only violated points, each by the check its input targets. |
| `tritium_price` | sensitivity | no | observed response recorded in § 6; no boundary was sought or found; the two adverse controls and the retained original case are the only violated points, each by the check its input targets. |
| `availability` | sensitivity | no | observed response recorded in § 6; no boundary was sought or found; the two adverse controls and the retained original case are the only violated points, each by the check its input targets. |
| `discount` | sensitivity | no | observed response recorded in § 6; no boundary was sought or found; the two adverse controls and the retained original case are the only violated points, each by the check its input targets. |
| `construction` | sensitivity | no | observed response recorded in § 6; no boundary was sought or found; the two adverse controls and the retained original case are the only violated points, each by the check its input targets. |
| `terminal` | sensitivity | no | observed response recorded in § 6; no boundary was sought or found; the two adverse controls and the retained original case are the only violated points, each by the check its input targets. |
| `compressor_price` | sensitivity | no | observed response recorded in § 6; no boundary was sought or found; the two adverse controls and the retained original case are the only violated points, each by the check its input targets. |
| `cycle_side_price` | sensitivity | no | observed response recorded in § 6; no boundary was sought or found; the two adverse controls and the retained original case are the only violated points, each by the check its input targets. |
| `conversion_services_price` | sensitivity | no | observed response recorded in § 6; no boundary was sought or found; the two adverse controls and the retained original case are the only violated points, each by the check its input targets. |
| `secondary_transport_price` | sensitivity | no | observed response recorded in § 6; no boundary was sought or found; the two adverse controls and the retained original case are the only violated points, each by the check its input targets. |
| `pbli_pump_mode` | sensitivity | no | observed response recorded in § 6; no boundary was sought or found; the two adverse controls and the retained original case are the only violated points, each by the check its input targets. |
| `pbli_pump_fixed_power` | sensitivity | no | observed response recorded in § 6; no boundary was sought or found; the two adverse controls and the retained original case are the only violated points, each by the check its input targets. |
| `compressor_rating` | sensitivity | no | observed response recorded in § 6; no boundary was sought or found; the two adverse controls and the retained original case are the only violated points, each by the check its input targets. |
| `he_pump_capacity` | sensitivity | no | observed response recorded in § 6; no boundary was sought or found; the two adverse controls and the retained original case are the only violated points, each by the check its input targets. |
| `estimate_mode` | sensitivity | no | observed response recorded in § 6; no boundary was sought or found; the two adverse controls and the retained original case are the only violated points, each by the check its input targets. |

## 6. Per-axis account

One pair of subsections per axis; every axis is sensitivity-framed, so the feasible-structure half is discharged by the same nil for all of them: **feasible structure (search framing) — Applies: not applicable — every axis is sensitivity-framed; no boundary was sought.** The observed responses below are LCOE differences in USD2004/MWh (and relative to the base) from `results/attribution.md` § C and § D; **no boundary claim is made for any axis**, and monotonicity is not claimed between sampled points. Violations: `compressor_capacity/capacity_ok` at the 1600 MW rating; `he_pump/capacity_ok` at 3261 kg/s; `plant_ledger/heat_removal_ok` in the retained original case; nowhere else in the swept space.

#### `source_net_power` — feasible structure (search framing)
**Applies:** not applicable — this axis is sensitivity-framed.

#### `source_net_power` — observed response (sensitivity framing)
**Applies:** yes.

branch at our net against our own accounting: +0.267 (no credit), +0.267 (feed100), +0.236 (aligned); denominator 1000 against 891.002 MW at source capital: -74.769, -25.974, -6.491. No boundary claim is made.

#### `annual_om` — feasible structure (search framing)
**Applies:** not applicable — this axis is sensitivity-framed.

#### `annual_om` — observed response (sensitivity framing)
**Applies:** yes.

L3 target-derived 80.893 MUSD/year: +1.642 on feed100; sensitivity 35 / 140 MUSD/year: -5.276 (-2.2%) / +10.551 (+4.4%). No boundary claim is made.

#### `plant_years` — feasible structure (search framing)
**Applies:** not applicable — this axis is sensitivity-framed.

#### `plant_years` — observed response (sensitivity framing)
**Applies:** yes.

L4 47 years: -2.190; 30 / 60 years: +5.648 (+2.4%) / -4.435 (-1.9%). No boundary claim is made.

#### `replacement_life` — feasible structure (search framing)
**Applies:** not applicable — this axis is sensitivity-framed.

#### `replacement_life` — observed response (sensitivity framing)
**Applies:** yes.

L5 source cadence 2.907 FPY at the source event price: +1.481 (11 events at 40 years), +1.489 on the 47-year case (13 events); 2 / 3.767 (fluence-scaled) / 8 FPY: +2.817 (+1.2%) / +0.685 (+0.3%) / -0.652 (-0.3%). No boundary claim is made.

#### `replacement_factor` — feasible structure (search framing)
**Applies:** not applicable — this axis is sensitivity-framed.

#### `replacement_factor` — observed response (sensitivity framing)
**Applies:** yes.

varied only with the source cadence (1.038330); its own response is inside the L5 figures. No boundary claim is made.

#### `new_feed` — feasible structure (search framing)
**Applies:** not applicable — this axis is sensitivity-framed.

#### `new_feed` — observed response (sensitivity framing)
**Applies:** yes.

0 → 100 kg/year (the two scenarios): -447.667; L6 feed = makeup at no charge: -627.323 from no credit; at the 30 MUSD/year service: 50 / makeup / 150 kg/year: +226.094 (+95.0%) / -175.135 (-73.6%) / -175.135 (-73.6%) (the purchase floor is reached at the makeup; excess feed is curtailed without credit). No boundary claim is made.

#### `supply_service` — feasible structure (search framing)
**Applies:** not applicable — this axis is sensitivity-framed.

#### `supply_service` — observed response (sensitivity framing)
**Applies:** yes.

10 / 100 MUSD/year at 100 kg/year: -3.015 (-1.3%) / +10.551 (+4.4%). No boundary claim is made.

#### `tritium_price` — feasible structure (search framing)
**Applies:** not applicable — this axis is sensitivity-framed.

#### `tritium_price` — observed response (sensitivity framing)
**Applies:** yes.

10 / 100 MUSD/kg: -421.325 (-61.4%) / +1474.637 (+215.1%) (no credit; the initial 10 kg stock moves overnight by ∓298 / +1,043 MUSD as well), -119.866 (-50.4%) / +419.530 (+176.3%) (feed100). No boundary claim is made.

#### `availability` — feasible structure (search framing)
**Applies:** not applicable — this axis is sensitivity-framed.

#### `availability` — observed response (sensitivity framing)
**Applies:** yes.

0.75 / 0.95: +7.846 (+1.1%) / -6.195 (-0.9%) (no credit), -51.843 (-21.8%) / +40.927 (+17.2%) (feed100: lower availability lowers the LCOE because the fixed 100 kg/year feed then covers more of the smaller makeup, the supply-threshold effect of the prior goals). No boundary claim is made.

#### `discount` — feasible structure (search framing)
**Applies:** not applicable — this axis is sensitivity-framed.

#### `discount` — observed response (sensitivity framing)
**Applies:** yes.

3 / 8 / 10 %: -12.900 (-5.4%) / +24.643 (+10.4%) / +44.427 (+18.7%) (feed100); on the aligned case 0 / 3 / 8 / 10 %: 31.885 / 46.008 / 84.687 / 104.898 against 77.6. No boundary claim is made.

#### `construction` — feasible structure (search framing)
**Applies:** not applicable — this axis is sensitivity-framed.

#### `construction` — observed response (sensitivity framing)
**Applies:** yes.

0 / 10 years: -6.036 (-2.5%) / +4.544 (+1.9%). No boundary claim is made.

#### `terminal` — feasible structure (search framing)
**Applies:** not applicable — this axis is sensitivity-framed.

#### `terminal` — observed response (sensitivity framing)
**Applies:** yes.

0.05 / 0.20: -0.272 (-0.1%) / +0.544 (+0.2%). No boundary claim is made.

#### `compressor_price` — feasible structure (search framing)
**Applies:** not applicable — this axis is sensitivity-framed.

#### `compressor_price` — observed response (sensitivity framing)
**Applies:** yes.

0.5 / 1.5: -0.650 (-0.3%) / +0.650 (+0.3%) (overnight ∓62.2 MUSD). No boundary claim is made.

#### `cycle_side_price` — feasible structure (search framing)
**Applies:** not applicable — this axis is sensitivity-framed.

#### `cycle_side_price` — observed response (sensitivity framing)
**Applies:** yes.

0.5 / 1.5 / 2.0 jointly with the compressor, conversion-services and secondary-transport factors: -4.666 (-2.0%) / +4.666 (+2.0%) / +9.332 (+3.9%) (overnight ∓447 / +894 MUSD). No boundary claim is made.

#### `conversion_services_price` — feasible structure (search framing)
**Applies:** not applicable — this axis is sensitivity-framed.

#### `conversion_services_price` — observed response (sensitivity framing)
**Applies:** yes.

2 / 4 / 6 (the recuperator bound): +0.978 (+0.4%) / +2.934 (+1.2%) / +4.890 (+2.1%) (overnight +94 / +281 / +469 MUSD). No boundary claim is made.

#### `secondary_transport_price` — feasible structure (search framing)
**Applies:** not applicable — this axis is sensitivity-framed.

#### `secondary_transport_price` — observed response (sensitivity framing)
**Applies:** yes.

1.214 / 1.5: +0.286 (+0.1%) / +0.668 (+0.3%). No boundary claim is made.

#### `pbli_pump_mode` — feasible structure (search framing)
**Applies:** not applicable — this axis is sensitivity-framed.

#### `pbli_pump_mode` — observed response (sensitivity framing)
**Applies:** yes.

switched to 1 only with the fixed-power axis; response inside that axis. No boundary claim is made.

#### `pbli_pump_fixed_power` — feasible structure (search framing)
**Applies:** not applicable — this axis is sensitivity-framed.

#### `pbli_pump_fixed_power` — observed response (sensitivity framing)
**Applies:** yes.

10 / 30 MW: +2.699 (+1.1%) / +8.291 (+3.5%) with net −9.989 / −29.989 MW (no heat recovery); the only sensitivity that moves the physical result. No boundary claim is made.

#### `compressor_rating` — feasible structure (search framing)
**Applies:** not applicable — this axis is sensitivity-framed.

#### `compressor_rating` — observed response (sensitivity framing)
**Applies:** yes.

1600 MW adverse control: the screen fails (margin −67.033 MW) and the LCOE falls by 0.076 because the smaller purchase is booked; retained as a failure, never relabelled. No boundary claim is made.

#### `he_pump_capacity` — feasible structure (search framing)
**Applies:** not applicable — this axis is sensitivity-framed.

#### `he_pump_capacity` — observed response (sensitivity framing)
**Applies:** yes.

3261 kg/s adverse control: the screen fails (margin −98 kg/s); LCOE -0.009; retained as a failure. No boundary claim is made.

#### `estimate_mode` — feasible structure (search framing)
**Applies:** not applicable — this axis is sensitivity-framed.

#### `estimate_mode` — observed response (sensitivity framing)
**Applies:** yes.

fixed-budget mode: every purchase at its reference amount, overnight −9.063 MUSD, LCOE -0.095; the disclosed nonresponse, not a hardware-cost law. No boundary claim is made.

## 7. Axis groups

`axes.json` declares 21 groups (24 entry keys), disjoint, every key a package input; the `cycle_side_price` group ties four price factors as one correlated scenario (a declared tie: the same E4 uncertainty applied jointly, declared by the executor); the compressor, conversion-services and secondary-transport factors are separate axes and are set to the group's value in the corner designs. The preflight sibling scan warns that the six other `*__selected_rating` keys and the two other `*__selected_flow_capacity` keys are undeclared siblings; deliberate (only the compressor rating and the He pump capacity are adverse controls).

| Axis | Entry key | Provenance | Note |
|---|---|---|---|
| `source_net_power` | `aries_integrated_plant__source_finance__net_power` | fan_out | MW; source |
| `annual_om` | `aries_integrated_plant__annual_om__selected_amount` | fan_out | USD2004/year; assumed |
| `plant_years` | `aries_integrated_plant__cost_schedule__plant_years` | fan_out | calendar years; assumed |
| `replacement_life` | `aries_integrated_plant__cost_schedule__replacement_life_fpy` | fan_out | full-power years; assumed |
| `replacement_factor` | `aries_integrated_plant__cost_schedule__replacement_factor` | fan_out | dimensionless; assumed |
| `new_feed` | `aries_integrated_plant__fuel_inventory__annual_recovery_kg` | fan_out | kg/calendar year; assumed |
| `supply_service` | `aries_integrated_plant__finance__supply_service_annual` | fan_out | USD2004/year; assumed |
| `tritium_price` | `aries_integrated_plant__fuel_inventory__tritium_price` | fan_out | USD2004/kg; assumed |
| `availability` | `aries_integrated_plant__cost_schedule__availability` | fan_out | dimensionless; assumed |
| `discount` | `aries_integrated_plant__finance__discount_rate` | fan_out | real/year; assumed |
| `construction` | `aries_integrated_plant__finance__construction_years` | fan_out | calendar years; assumed |
| `terminal` | `aries_integrated_plant__finance__terminal_fraction` | fan_out | dimensionless; assumed |
| `compressor_price` | `aries_integrated_plant__compressor_equipment__price_factor` | fan_out | dimensionless; assumed |
| `cycle_side_price` | `aries_integrated_plant__turbine_equipment__price_factor` | fan_out | dimensionless; assumed |
| `cycle_side_price` | `aries_integrated_plant__generator_equipment__price_factor` | fan_out | dimensionless; assumed |
| `cycle_side_price` | `aries_integrated_plant__electrical_equipment__price_factor` | fan_out | dimensionless; assumed |
| `cycle_side_price` | `aries_integrated_plant__heat_rejection_equipment__price_factor` | fan_out | dimensionless; assumed |
| `conversion_services_price` | `aries_integrated_plant__conversion_services__price_factor` | fan_out | dimensionless; assumed |
| `secondary_transport_price` | `aries_integrated_plant__secondary_transport__price_factor` | fan_out | dimensionless; assumed |
| `pbli_pump_mode` | `aries_integrated_plant__pbli_pump__pump_mode` | fan_out | code; operating |
| `pbli_pump_fixed_power` | `aries_integrated_plant__pbli_pump__fixed_power` | fan_out | MW; operating |
| `compressor_rating` | `aries_integrated_plant__compressor_capacity__selected_rating` | fan_out | MW; purchased |
| `he_pump_capacity` | `aries_integrated_plant__he_pump__selected_flow_capacity` | fan_out | kg/s; purchased |
| `estimate_mode` | `aries_integrated_plant__cost_accounts__estimate_mode` | fan_out | code; accounting |

## 8. Indicators and rulings

[OWNER] The owner brief (`…/evidence/owner-brief.md` § 2 and § 6) authorizes clearly identified assumptions with sensitivity ranges where performance maps or price data are missing, and a bounded sensitivity study with justified ranges whose purpose is to find which conclusions survive, "not to optimize until the result resembles published ARIES economics". That authorization is the ruling for every `no_constraint_response` axis below; the model-development finding beside each is required before execution and is not discharged by the ruling. All 21 proposed axes were traced; none was declined.

| Axis | Indicator | Ruling | Note |
|---|---|---|---|
| `source_net_power` | no_constraint_response (0 of 14 constraints on a possible path) | Authorized sensitivity only (owner brief § 2, § 6) | The source-conditioned branch substitutes a supplied denominator and already-financed capital; nothing physical responds. Swept as declared. |
| `annual_om` | no_constraint_response (0 of 14 constraints on a possible path) | Authorized sensitivity only (owner brief § 2, § 6) | Fixed allowance; no staffing or maintenance model responds. Swept as declared. |
| `plant_years` | no_constraint_response (0 of 14 constraints on a possible path) | Authorized sensitivity only (owner brief § 2, § 6) | Financial assumption; no financing, liability or service-life evidence responds; no engineering optimum. Swept as declared. |
| `replacement_life` | no_constraint_response (0 of 14 constraints on a possible path) | Authorized sensitivity only (owner brief § 2, § 6) | Selected life; no damage or fluence model responds. Swept as declared. |
| `replacement_factor` | no_constraint_response (0 of 14 constraints on a possible path) | Authorized sensitivity only (owner brief § 2, § 6) | Event price factor; no procurement model. Swept as declared. |
| `new_feed` | constraints_reachable (1 of 14 constraints on a possible path) | Authorized sensitivity only (owner brief § 2, § 6) | Net extracted breeder feed has no qualified capability or extraction-cost model; exhaust recycling is already credited. Swept as declared. |
| `supply_service` | no_constraint_response (0 of 14 constraints on a possible path) | Authorized sensitivity only (owner brief § 2, § 6) | Incremental assumed service cost has no price-versus-capability relation. Swept as declared. |
| `tritium_price` | constraints_reachable (1 of 14 constraints on a possible path) | Authorized sensitivity only (owner brief § 2, § 6) | Assumed price; no market model. Swept as declared. |
| `availability` | constraints_reachable (1 of 14 constraints on a possible path) | Authorized sensitivity only (owner brief § 2, § 6) | Supplied availability has no outage or reliability response. Swept as declared. |
| `discount` | no_constraint_response (0 of 14 constraints on a possible path) | Authorized sensitivity only (owner brief § 2, § 6) | Financial assumption; no financing, liability or service-life evidence responds; no engineering optimum. Swept as declared. |
| `construction` | no_constraint_response (0 of 14 constraints on a possible path) | Authorized sensitivity only (owner brief § 2, § 6) | Financial assumption; no financing, liability or service-life evidence responds; no engineering optimum. Swept as declared. |
| `terminal` | no_constraint_response (0 of 14 constraints on a possible path) | Authorized sensitivity only (owner brief § 2, § 6) | Financial assumption; no financing, liability or service-life evidence responds; no engineering optimum. Swept as declared. |
| `compressor_price` | no_constraint_response (0 of 14 constraints on a possible path) | Authorized sensitivity only (owner brief § 2, § 6) | Supplied price factor has no calibrated market or equipment-quality response. Swept as declared. |
| `cycle_side_price` | no_constraint_response (0 of 14 constraints on a possible path) | Authorized sensitivity only (owner brief § 2, § 6) | Fixed source-scope allowances; no response to gross power or flow. Swept as declared. |
| `conversion_services_price` | no_constraint_response (0 of 14 constraints on a possible path) | Authorized sensitivity only (owner brief § 2, § 6) | The 0.95 recuperator has no purchase, rating or screen (audit item 1). Swept as declared. |
| `secondary_transport_price` | no_constraint_response (0 of 14 constraints on a possible path) | Authorized sensitivity only (owner brief § 2, § 6) | Fixed allowance; no response to cycle flow (audit item 2). Swept as declared. |
| `pbli_pump_mode` | constraints_reachable (10 of 14 constraints on a possible path) | Authorized sensitivity only (owner brief § 2, § 6) | Mode switch; no hydraulic model. Swept as declared. |
| `pbli_pump_fixed_power` | constraints_reachable (10 of 14 constraints on a possible path) | Authorized sensitivity only (owner brief § 2, § 6) | No PbLi hydraulic or MHD model; no heat recovery (pbli_recovery 0). Swept as declared. |
| `compressor_rating` | constraints_reachable (1 of 14 constraints on a possible path) | Authorized sensitivity only (owner brief § 2, § 6) | Scalar screen and linear cost; no compressor map. Swept as declared. |
| `he_pump_capacity` | constraints_reachable (1 of 14 constraints on a possible path) | Authorized sensitivity only (owner brief § 2, § 6) | Scalar screen and linear cost; no pump map. Swept as declared. |
| `estimate_mode` | no_constraint_response (0 of 14 constraints on a possible path) | Authorized sensitivity only (owner brief § 2, § 6) | Mode switch; not a hardware-cost law. Swept as declared. |

**Not derivable, disclosed in every record.** These are not decidable from the indicator run and no indicator output claims them: monotonicity of any channel in any axis; identity of the same physical quantity across differing key names; intra-module operand dependency. `constraints_reachable` is a *possible* path and never a statement that a constraint responds. `unresisted` is the agent's recorded judgment, never a tool output.

**Model-development findings.** Every `no_constraint_response` axis carries one, in addition to the ruling.

| Axis | What should push back and is not modeled | Finding id |
|---|---|---|
| `source_net_power` | The source-conditioned branch substitutes a supplied denominator and already-financed capital; nothing physical responds. | `20260925-aries-reconciled-alternative-economics#4` |
| `annual_om` | Fixed allowance; no staffing or maintenance model responds. | `20260925-aries-reconciled-alternative-economics#3` |
| `plant_years` | Financial assumption; no financing, liability or service-life evidence responds; no engineering optimum. | `20260925-aries-reconciled-alternative-economics#1` |
| `replacement_life` | Selected life; no damage or fluence model responds. | `20260925-aries-reconciled-alternative-economics#3` |
| `replacement_factor` | Event price factor; no procurement model. | `20260925-aries-reconciled-alternative-economics#3` |
| `supply_service` | Incremental assumed service cost has no price-versus-capability relation. | `20260925-aries-reconciled-alternative-economics#3` |
| `discount` | Financial assumption; no financing, liability or service-life evidence responds; no engineering optimum. | `20260925-aries-reconciled-alternative-economics#1` |
| `construction` | Financial assumption; no financing, liability or service-life evidence responds; no engineering optimum. | `20260925-aries-reconciled-alternative-economics#1` |
| `terminal` | Financial assumption; no financing, liability or service-life evidence responds; no engineering optimum. | `20260925-aries-reconciled-alternative-economics#1` |
| `compressor_price` | Supplied price factor has no calibrated market or equipment-quality response. | `20260925-aries-reconciled-alternative-economics#2` |
| `cycle_side_price` | Fixed source-scope allowances; no response to gross power or flow. | `20260925-aries-reconciled-alternative-economics#2` |
| `conversion_services_price` | The 0.95 recuperator has no purchase, rating or screen (audit item 1). | `20260925-aries-reconciled-alternative-economics#2` |
| `secondary_transport_price` | Fixed allowance; no response to cycle flow (audit item 2). | `20260925-aries-reconciled-alternative-economics#2` |
| `estimate_mode` | Mode switch; not a hardware-cost law. | `20260925-aries-reconciled-alternative-economics#4` |

## 9. Preflight results

From `preparation/preflight_results.json` (run on the unchanged live manifest with its six reviewed absolute tolerances after the r1 revision of the configuration; the identity and baseline gates read `preparation/package_identity.json` and `preparation/baseline_result.json`, deposited by the route at step 5; the pre-revision preparation is retained under `preparation-r1/`).

| Gate | Outcome | Detail |
|---|---|---|
| Declared-group key validation | pass | 24 declared keys across 21 groups, all package inputs |
| Suffix-sibling scan (warnings only) | pass (8 sibling warnings, deliberate) | warnings: 138 |
| Identity | pass | kind sealed, digest f739dbce67699b7adfae7c1adf5599ab7c30e85987caad53e0f8affd9b880ce4 recomputed from 0 allowed-modified file(s) and 0 declared source(s); every other sealed artifact matches |
| Manifest / package fingerprint match | pass | both recorded package fingerprints match the package on disk |
| Baseline gate against the pinned headline | pass | aries_integrated_plant__lifecycle_price__evaluate__lcoe reproduces at relative deviation 0.000e+00; 2/2 pinned verdicts match |
| Package cleanliness | pass | package tree is byte-untouched (git clean) |

## 10. Execution route and why

- **Route:** study-local direct-API (stock `StudyRunner` with `PreparedListStrategy` over complete declared input maps, through `alternative_economics_support.py`, which reuses the reconciliation composer `reconciliation_support.proposals` and the retained predecessor executor `20260922-aries-integrated-lcoe/execute_study.py`).
- **Why this route:** the declared cases are named full maps composed on canonical bases (the verbatim stored inputs of four sealed cases, checked against this package's executable fingerprint) and on each other; the strict loader, fingerprints, store lease and full-map exporter are reused unchanged; the live manifest and the round-2 integration CANDIDATE are reused without re-pin because the package identity is unchanged (as the round-3 flow-scaling study did). The route loaded and gated at steps 5–6 before this rationale was written.

**Glue disclosure.** glue ledger: none. No adapter on this route, so nothing is harness-supplied.

## 11. Study definition and window provenance

The candidate set was scanned with the package-owned independent oracle before execution (`oracle-window-scan.json`: 64 of 64 evaluated, 0 refused), so every declared point is inside the oracle's domain, including the two adverse controls and the fixed-budget mode. Windows are declared per axis in `axis-plan.json` (`config.json`) and are **engineered**: the E1–E10 and F1–F9 assumption ranges of WI-090/WI-091, three derived applicability points (47 calendar years = 40 full-power years at 0.85; 2.907407 FPY and 1.038330 = the source replacement cadence and event price; 3.7673 FPY = the baseline's 5 FPY life fluence-scaled to this configuration's +32.7 % neutron power), two `[ASSUMED]` bounds for costs the audit graded unresolved (recuperator: NTU 4 → 19 with capacity rate × 1.214, factors 2/4/6 on the conversion-services allowance; PbLi pumping 10/30 MW), and the flow-proportional 1.214 on secondary transport. The only sourced values are the published 1000 MW net (the source branch's default) and, as a diagnostic, 138.7304019114013 kg/year (this case's own gross makeup) for self-sufficient tritium. An engineered window costs any claim about behaviour outside it; the ladder's substitutions are labelled diagnostics and license no independent-prediction claim.

## 12. Cross-fingerprint correlation and what it means

single fingerprint — no cross-arm correlation needed (one arm, one store, one package identity `f739dbce…`).

## 13. Verification

All 64 stored cases were verified against the package-owned independent oracle (`scripts/study/verify.py`, sample size 64, stratified over the four observed verdict combinations): 364 numeric channels per case at relative 1e-9 or a declared absolute tolerance, and all 14 predicates re-derived exactly (`results/verification_summary.json`, outcome `pass`; `not_independently_verified: 0`). Ten absolute tolerances apply: the six inherited (`residual_magnitude` 1e-7 MW, `idc` two ULP, the four unmet-heat channels 1e-7 MW) and four declared for this study (`curtailed_feed` and `external_shortfall` under `lifecycle_accounts` and `source_lifecycle_accounts`, 1e-9 kg/year). The largest relative deviation reported is 8.29e+03 at `{'case_id': '20260925-aries-reconciled-alternative-economics:c0002', 'channel': 'plant_ledger__evaluate__residual_magnitude', 'value': 7.539028956671245e-09}`, a near-zero residual channel passing its declared absolute tolerance, as in the prior records.

**Attempt history (finding #10).** Attempt 1 executed all 64 points and its all-point verification refused `lifecycle_accounts__evaluate__curtailed_feed` in `diag-L8-aligned-discount-0.08` (store 0.0, oracle 6.8e-15 kg/year, relative deviation 1.0 with no absolute tolerance declared; `results-attempt1/verify-refused.log`). At exact feed equality the package's float64 `max(feed − makeup, 0)` is exactly 0.0 while the checker's Decimal sum exposes the float64 rounding error (about one ulp). An absolute tolerance of 1e-9 kg/year on the four channels of that class was declared (`…/evidence/curtailed-tolerance-declaration.md`), independently reviewed (`…/evidence/curtailed-tolerance-review.md`: FINDINGS, one wording correction applied, no second review needed) and added to the record and live manifests; indicators and preflight were re-run on the amended manifest (`indicators-attempt1.json`, `preparation/preflight_results-attempt1.json` retain the earlier runs); the 64 points were re-executed into fresh `results/` (attempt 1 retained under `results-attempt1/`), and `results/attempt-comparison.json` shows every input, every one of 35,264 stored channels and every verdict identical between the attempts. `preparation-provenance.json` keeps the manifest sha256 from before the amendment; `indicators.json` and `results/manifest_used.json` carry the amended manifest.

**Not covered.** Inputs fed identically to the package and the oracle are not independently verified (the summary lists none as such because every compared channel is an output); the oracle's lifecycle arithmetic is an independent re-derivation of the same WI-091 equations, so agreement verifies numerical translation, not the financial convention or any scientific assumption; the four-channel tolerance makes differences below 1e-9 kg/year on those channels invisible by declaration.

## 14. Review outcomes

| Lens | Verdict | Disposition |
|---|---|---|
| Replay of the canonical configuration on the live package (coordinator, goal T-001) | bit-exact on 551 channels × 4 cases; verdicts identical | the configuration identity is fixed; `…/evidence/replay-alternative.json` |
| Equipment and cost binding audit (fresh worker, goal T-002) | 25 items graded; six inconsistencies named; no binding change required | unresolved costs bounded by declared sensitivities; `…/evidence/equipment-cost-audit.md` |
| Interim single-counting, adequacy and fuel checks (coordinator, goal T-003) | sixteen identities hold; oracle re-derives 364 channels; fuel demand recalculated from first principles | `…/evidence/interim-checks.md` |
| Pre-execution review of the comparison basis and configuration (fresh, goal C-001) | r1 FINDINGS (three correct-before-execution, four notes) → r2 PASS on the diff | corrections applied before execution; `…/evidence/pre-execution-review.md` |
| Curtailed-feed tolerance declaration (fresh) | FINDINGS: sound; one wording correction, objectively verifiable | applied; `…/evidence/curtailed-tolerance-review.md` |
| Round-1 review of this reading | pending at the round result | goal trail |

## 15. Findings

Each finding gets an id used verbatim in `DISCOVERY_LOG.md` (the study id followed by `#` and the number); #1–#4 are the model-development findings recorded before execution (§ 8).

| Id | Kind | Finding | Disposition | Home |
|---|---|---|---|---|
| `20260925-aries-reconciled-alternative-economics#1` | model | Finance axes (`discount`, `construction`, `terminal`, `plant_years`): no financing, liability or service-life evidence responds; the source's own rate is not printed, so the aligned residual against 77.6 is reported at every swept rate and none is designated. | Declared seam; owner-authorized sensitivity; the rate stays unresolved in the answer. | `work/orchestration/goals/aries-reconciled-alternative-economics/answer.md` |
| `20260925-aries-reconciled-alternative-economics#2` | model | Price factors (`compressor_price`, `cycle_side_price`, `conversion_services_price`, `secondary_transport_price`): the fixed source-scope allowances and the linear law have no market or equipment-quality response; the 0.95 recuperator has no purchase, rating or screen; the cycle-side transport does not respond to 1700 kg/s. | Declared seam; bounds swept (recuperator ×6: +4.890; cycle side ×2: +9.332); a recuperator hardware representation offered to the owner as a follow-up. | `work/orchestration/goals/aries-reconciled-alternative-economics/evidence/equipment-cost-audit.md` |
| `20260925-aries-reconciled-alternative-economics#3` | model | O&M, replacement life and factor, supply service: allowances without staffing, damage/fluence or extraction-cost models; the replacement schedule does not see the alternative's +32.7 % neutron power (fluence-scaled life 3.767 FPY: +0.685). | Declared seam; applicability points swept. | `work/orchestration/goals/aries-reconciled-alternative-economics/evidence/comparison-basis.md` |
| `20260925-aries-reconciled-alternative-economics#4` | model | `source_net_power` and `estimate_mode`: the source-conditioned branch and the fixed-budget mode are diagnostic substitutions with no physical response. | Declared seam; every such case labelled diagnostic. | `record.md § 5` |
| `20260925-aries-reconciled-alternative-economics#5` | model | The alternative's economics are set by the tritium supply assumption, not by the changed equipment: no-credit 685.695 (tritium 91.5%), feed100 238.028; the compressor and pump purchases change direct capital by 6.083 MUSD2004 (+0.076 USD/MWh per 100 MW of rating; ±0.650 over E4). | Result; answer § 3–4. | `work/orchestration/goals/aries-reconciled-alternative-economics/answer.md` |
| `20260925-aries-reconciled-alternative-economics#6` | model | Under the fixed 100 kg/year feed the 891 MW alternative is +61.342 USD2004/MWh above the 423 MW baseline (tritium +130.687 because the feed covers 34.063 kg/year less of the larger makeup) while it is -433.713 below it without credit; availability 0.75 lowers the feed100 LCOE by 51.843 for the same reason: the ranking is a supply-threshold effect, as the prior design-studies goal found. | Result; answer § 3; not a physical ranking. | `work/orchestration/goals/aries-reconciled-alternative-economics/answer.md` |
| `20260925-aries-reconciled-alternative-economics#7` | model | Aligned-convention ladder: capital scope is a near-wash (+0.267: direct × 1.49 × 1.1576 ≈ × 1.93); the denominator is worth -6.491 in the aligned case; target-derived O&M +1.642, 47 years -2.190, source cadence +1.489, self-sufficient tritium -627.323 from no credit; combined 59.313 (branch 53.058) at 5 %, 31.885–104.898 over 0–10 % (branch 30.659–83.404), bracketing 77.6; interaction of the steps +0.000. | Result; the residual is unresolved with the missing evidence named (source financing rate and schedule, decommissioning conversion, independent O&M, tritium treatment). | `work/orchestration/goals/aries-reconciled-alternative-economics/answer.md` |
| `20260925-aries-reconciled-alternative-economics#8` | model | Unresolved-bounded costs: recuperator ×6 +4.890, cycle side ×2 +9.332, PbLi pumping 30 MW +8.291 (net −29.989 MW): each material in the aligned comparison (≥ 1.0) and immaterial to the fuel-dominated conclusion. | Reported as unresolved with the missing evidence named (recuperator geometry/price, cycle-side applicability, PbLi hydraulics). | `work/orchestration/goals/aries-reconciled-alternative-economics/answer.md` |
| `20260925-aries-reconciled-alternative-economics#9` | model | The adverse controls stay failures (rating 1600 MW: `compressor_capacity` violated by 67.033 MW; He pump 3261 kg/s: `he_pump` violated by 98 kg/s) with a slightly lower LCOE from the smaller booked purchase; the fixed-budget mode leaves every purchase at its reference amount (−0.095). | Retained unrelabelled; the MR-7 insufficient/sufficient evidence for this configuration. | `record.md § 4` |
| `20260925-aries-reconciled-alternative-economics#10` | process | All-point verification refused `curtailed_feed` at exact feed equality (store 0.0, oracle 6.8e-15 kg/year: float64 against Decimal); a 1e-9 kg/year absolute tolerance on the four curtailed-feed / external-shortfall channels was declared, independently reviewed and applied to the record and live manifests; the points were re-executed bit-identically (L-008 class). | Process note; tooling seam (relative-only rule on exact-zero difference channels); the class is now declared for later studies. | `exploration/aries_integrated/studies/manifest.json` |
| `20260925-aries-reconciled-alternative-economics#11` | process | Second and third studies on the same package identity reused the round-2 canonical replay receipt, the live manifest and the integration candidate without re-pin; canonical bases taken verbatim from two sealed stores and checked against the executable fingerprint. | Process note. | `results/execution-context.json` |

## 16. Snapshot

- **File:** `snapshot.json`
- **sha256:** `ccc56f3bae83993bd25138334de6c96202df5fa608fe643b346464f83738eca1`
- **Schema version:** `1`

No snapshot content is restated here. (`snapshot.json` records the package at repo commit `e8a91dc7704b4f9aa3baf281ea1b66d64fc4617b` git-clean, the three fingerprints, the amended manifest content used with ten absolute tolerances, the single arm `arm-economics` with its store compatibility tuple, the verification command and tool digest, 327 hashed record artifacts including attempt 1, 64 cases with [551] numeric outputs each, 364 verified channels and 14 exact verdicts per case, and 61 cases with every scoped check satisfied.)

## 17. What this record does not contain

- No reproduction of the ARIES operating point or of its economics: 891 MW is a modeled alternative (not an upper bound, not the reference); every rung of the ladder that touches a published quantity is a labelled diagnostic and licenses no independent-prediction claim; no rung is called the match.
- No optimum, no monotonicity claim, no probability: every window is engineered and every axis is sensitivity-framed.
- No vendor price, compressor map, recuperator geometry, hydraulic or MHD law, breeding capability, market tritium price or decommissioning estimate: the recuperator, cycle-side transport and PbLi pumping are bounded, not priced; the source's financing rate and schedule, decommissioning conversion and independent O&M amount are not recovered.
- No scientific qualification: the six support flags stay 0; a finite LCOE upgrades none of them.
- No change to any model, package, assembly, frozen record, the Stellaris models or the six shared library files; the only repository change outside this record and its two thin modules is the reviewed four-entry tolerance addition to the live manifest.
- No claim that the fixed 100 kg/year feed is achievable or that its ranking of the 891 MW and 423 MW plants is physical.


## Addendum 2026-09-25 — corrections on the round-1 review (`…/evidence/round1-review.md`)

- § 3, § 6 (`pbli_pump_fixed_power`) and finding #8: the PbLi pumping bound +8.291 USD2004/MWh is stated on the feed100 base (238.028) and is a pure denominator effect (overnight unchanged; 246.319 / 238.028 = 891.0017 / 861.0127); on the aligned combined case (59.313) the same 30 MW is worth ≈ +2.1, and on the source branch (supplied 1000 MW) ≈ 0. The recuperator and cycle-side bounds are capital and the same on any base.
- § 2 and MR-7 disclosure: the He and PbLi pump capacities of the canonical case (3359 and 27,666 kg/s) are supplied choices set equal to the operating flows, as WI-090 set the baseline's; their screen margins are 0 by that choice, not by sizing.
- § 13 attempt history: the retry kept task, inputs and meaning identical; its scope was not identical, because the live manifest's tolerance list was amended (a deliberate, recorded deviation from the goal task's written scope; the record manifest and `results/manifest_used.json` carry the amended list).
