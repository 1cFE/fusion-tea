# Record: 20260926-design-study-parameters

## 1. Study header

- **Study id:** `20260926-design-study-parameters`
- **Package:** `costed_loop_brayton_tea` (`exploration/costed_loop_brayton/costed_loop_brayton_tea`, executable `a4c7a87136fe3ea373fb02a899ed8262a800a7443891db986411f00f26c8aeea`, semantic `76c68dde7a4de41987be07ecd3ac3bdf814c6ef1895f3ad8d2250275cf9bdee7`, manifest pin `53f48a7e563b7cacf81a0ca2fc14ab5c5a146aab2360482effb33031a0e0fd51`)
- **Date executed:** 2026-09-26
- **Executor:** goal `design-study-parameters`, round 1 agent (Claude session; coordinator)
- **Mode:** execute
- **Arms:** single arm (`arm-flow-ratio`), one store, three declared blocks: the I-R grid (100 stored points), the I-A grid at the same points (100), the sensitivities S1–S6 at the anchors (72)

## 2. Intake

The owner's goal and scope, verbatim (`work/orchestration/goals/design-study-parameters/evidence/owner-brief.md`):

> For a plant assembled using the expanded library, which operating choices improve net electricity and LCOE, and which equipment or thermal limit stops the improvement?

> Proposed starting question: how should cycle mass flow and compressor pressure ratio be chosen together for the Stellaris helium-loop/ARIES Brayton combination? Prior cases suggest that lowering pressure ratio increases calculated electricity but can make heat removal fail. Turn that observation into a fair performance-and-cost study, not a collection of impressive invalid outputs.

Executor's additions, marked as the executor's own: the study runs on the WI-094 costed variant of the WI-093 C-1 assembly under the fresh-reviewed comparison contract (`…/evidence/comparison-contract.md` v2), whose § 11 declares the grid, § 5 the two priced inventories (I-R, the WI-093 re-selected ratings, the main block; I-A, the ARIES-selected ratings, a recorded alternative) and § 10 the sensitivities; every case is a complete input map composed on the manifest baseline by declared axis values (`config.json`, `axis-plan.json`); nothing is optimized and no rating is changed from a demand (MR-7). The declared extra anchor `screen-best-passing` (2,500 kg/s / 1.45) was added at preparation r2 with its reason (§ 11).

## 3. Objective and result

- **LCOE objective channel(s):** `costed_loop_brayton__plant__lifecycle_price__evaluate__lcoe` (the manifest headline; equal to `costed_loop_brayton__plant__lifecycle_accounts__evaluate__lcoe_sum`), constant USD2004 per MWh, no-breeding-credit convention on every point except the S5 cases.
- **LCOE result:** 1,113.379 USD2004/MWh at `ir-f2250-r1.5183` (2,250 kg/s, stage ratio 1.5183), the lowest among the 52 I-R points that satisfy every check, against 1,559.438 at the starting point `ir-f2500-r1.5183` (Δ −446.059, of which tritium purchases −407.981 and the plant side −38.069); 1,118.836 at `ir-f2750-r1.3750`, 2.9 MW of net apart from the first and within the 5 MW materiality, so the two form one best band. The I-R passing LCOE range is 1,113.379 to 19,082.213 (at 3,000 kg/s / 1.55, net 35.2 MW). The ARIES-selected inventory I-A prices the same operating points 8 to 11 USD/MWh lower (booked purchases 461,372,866.67 against 812,309,488.89) but satisfies every check at none of them. Under the named-feed convention (S5) the best passing point's LCOE is 445.790.

The LCOE is read, not optimized: within one inventory every numerator term is a constant of the sweep (contract § 6, reviewed), so the LCOE ranking of operating points is the ranking by net electricity and the tritium term carries most of the delta; the absolute figure is conditional on the rest-of-plant constant and the fuel convention.

## 4. Constraint outcomes

Every executing constraint by qualified identity; statuses aggregated over the 272 stored points (per-point verdicts in `results/cases.json` and `cases.csv`; the 56 points the oracle scan refused were never stored, § 11).

| `constraint_id` | `source_local_identity` | Status | Note |
|---|---|---|---|
| `costed_loop_brayton__plant__checks__heat_removal_ok__177997e14a28cae1` | `heat_removal_ok` | violated at 109 of 272 (I-R 44, I-A 44, sensitivities 21) | the lower-ratio edge at every flow up to 3,500 kg/s: unmet source heat when the heater inlet (after recuperation) rises above what the 773 K source can deliver through the 50 MW/K exchanger; independent of the inventory |
| `costed_loop_brayton__plant__checks__loop_capacity_ok__9c561de0cd1f50b3` | `loop_capacity_ok` | satisfied at all 272 | constant margin 10.095 kg/s (the loop is upstream of both swept inputs) |
| `costed_loop_brayton__plant__checks__net_positive__987a4d032b5440a8` | `net_positive` | satisfied at all 272 | the 55 nonpositive-net points of the candidate range were refused by the scan and never stored |
| `costed_loop_brayton__plant__compressor_capacity__capacity_ok__6e46ae5b5c0061be` | `capacity_ok` | violated at 83 (I-R 4, I-A 79) | I-R (3,200 MW): the upper-ratio edge at 2,250 / 1.80, 2,500 / 1.80, 2,750 / 1.70, 3,000 / 1.60 (margins −16.8, −374.3, −307.5, −147.0 MW); I-A (1,600 MW): violated wherever the three-stage demand exceeds 1,600 MW |
| `costed_loop_brayton__plant__fuel_inventory__capacity_ok__9d250853407ea035` | `capacity_ok` | satisfied at all 272 | required stock 0.090 kg against the chosen 10 kg; constant |
| `costed_loop_brayton__plant__generator_capacity__capacity_ok__866bb648afde20fc` | `capacity_ok` | satisfied at all 272 | 3,600 (I-R) and 1,800 MW (I-A) both above the highest gross (860.3 MW) |
| `costed_loop_brayton__plant__he_capacity__capacity_ok__5bc3ff690032908b` | `capacity_ok` | violated at 100 (I-A 100) | the 1,500 MW helium-duty package against the constant 3,301.2 MW delivered duty (margin −1,801.2 at every I-A point); I-R's 3,500 MW keeps +198.8 |
| `costed_loop_brayton__plant__rejection_capacity__capacity_ok__839b61a7b3fe128c` | `capacity_ok` | violated at 52 (I-A 52) | 2,500 MW rejection against 2,415–2,621 MW rejected; I-R's 5,000 MW never binds |
| `costed_loop_brayton__plant__turbine_capacity__capacity_ok__583bf29eadcd21ed` | `capacity_ok` | violated at 5 (I-A 5) | 3,500 MW turbine against the highest expander outputs at 4,000 kg/s / 1.30–1.35 and 3,500 / 1.40–1.425 |

## 5. Framing

**As proposed at intake.**

| Axis | Framing proposed | Why |
|---|---|---|
| `cycle_flow` | search | the question asks which flow and ratio to choose together; the contract's grid is engineered around the screen's boundary |
| `stage_ratio` | search | as above; one value applied to the three stages as the declared equal-stage scenario |
| `compressor_rating`, `turbine_rating`, `generator_rating`, `rejection_rating`, `he_duty_rating` | sensitivity | the two declared inventories; a rating is a priced selection, never sized from demand |
| `compressor_efficiency`, `turbine_efficiency` | sensitivity | S1, the fixed-efficiency treatment's first-order effect |
| `aux_heat`, `aux_cryo`, `aux_fuel_base`, `aux_control`, `aux_other`, `fuel_exhaust_term` | sensitivity | S2, constants of the balance |
| `pump_law_dp_ref` | sensitivity | S3, the loop's pump law constant |
| `equipment_price_factor`, `rest_of_plant_price_factor` | sensitivity | S4, prices |
| `tritium_feed`, `supply_service` | sensitivity | S5, the fuel convention |
| `exchanger_area` | sensitivity | S6, the one declared priced hardware alternative |

**As judged after the run.**

| Axis | Framing judged | Changed? | Why |
|---|---|---|---|
| `cycle_flow` | search | no | a feasible structure was found: at each flow a passing ratio band bounded below by heat removal and above by the compressor rating or nonpositive net; the best passing band lies at 2,250–2,750 kg/s |
| `stage_ratio` | search | no | the lowest passing ratio falls with flow (1.70 at 2,000 to 1.20 at 4,000); the ridge of net sits one step on the failing side of the heat-removal boundary at every flow |
| the five rating axes | sensitivity | no | I-A admits no passing point; violations located, no boundary claim |
| `compressor_efficiency`, `turbine_efficiency` | sensitivity | no | compressor 0.85 and turbine 0.90 move the boundary up by one grid step at 2,250 kg/s (the best point fails by 2.8 and 70.7 MW unmet); 2,500 / 1.45 passes under every level; no boundary claim |
| the six S2 axes | sensitivity | no | constant shifts of net (±32.5, −1.8, −50.2 MW) with no verdict change at any passing anchor |
| `pump_law_dp_ref` | sensitivity | no | ×2 fails every anchor except the starting point (the friction heat the loop delivers cannot be removed at the boundary); ×0.5 makes 2,250 / 1.50 pass |
| `equipment_price_factor`, `rest_of_plant_price_factor` | sensitivity | no | LCOE only; no channel of the balance moves |
| `tritium_feed`, `supply_service` | sensitivity | no | LCOE only (−665 to −935 USD/MWh); no ranking change |
| `exchanger_area` | sensitivity | no | 75,000 m² moves the boundary at 2,500 kg/s from 1.45 to 1.40 (671.6 MW passing); a located response, not a boundary claim |

## 6. Per-axis account

#### `cycle_flow` — feasible structure (search framing)
**Applies:** yes

Active constraints: `heat_removal_ok` below a flow-dependent ratio, the I-R compressor rating (3,200 MW) above it at 2,250–3,000 kg/s, and nonpositive net (refused, never stored) above it at 3,250–4,000 kg/s. Lowest passing ratio per flow: 1.70 (2,000), 1.5183 (2,250), 1.45 (2,500), 1.375 (2,750), 1.325 (3,000), 1.30 (3,250), 1.25 (3,500), 1.20 (4,000, the grid edge). Best passing net per flow: 441.6, 597.5, 575.6, 594.6, 581.4, 533.0, 539.2, 476.3 MW. The constrained best on the grid is the band {2,250 / 1.5183 at 597.481 MW, 2,750 / 1.375 at 594.567 MW}; the electricity-only best is 2,500 / 1.425 at 620.008 MW with 7.775 MW of source heat unremoved. Located to the grid's resolution (250 kg/s); no interpolated optimum is claimed.

#### `cycle_flow` — observed response (sensitivity framing)
**Applies:** not applicable — this axis is search-framed

#### `stage_ratio` — feasible structure (search framing)
**Applies:** yes

At every flow the net rises as the ratio falls until heat removal fails; the passing band's lower edge is the heat-removal boundary (unmet 7.8 MW one step below it at 2,500 kg/s, 46.4 at 2,250, 51.7 at 2,750), its upper edge the compressor rating (2,250–3,000) or the net-positive edge (3,250–4,000, refused) or the grid edge (2,000). The heater inlet at the best band is 453.3 K (2,250 / 1.5183, helium hot-bound margin 0.70 K) and 476.8 K (2,750 / 1.375, margin 8.63 K); at the electricity-only best it is 472.8 K with the margin exhausted. Recuperator bypass engages only at the high-ratio corner (2,000 / 1.80 to 3,000 / 1.55–1.60), inside the passing band's upper part.

#### `stage_ratio` — observed response (sensitivity framing)
**Applies:** not applicable — this axis is search-framed

#### `compressor_rating`, `turbine_rating`, `generator_rating`, `rejection_rating`, `he_duty_rating` — feasible structure (search framing)
**Applies:** not applicable — these axes are sensitivity-framed

#### `compressor_rating`, `turbine_rating`, `generator_rating`, `rejection_rating`, `he_duty_rating` — observed response (sensitivity framing)
**Applies:** yes

I-A (1,600 / 3,500 / 1,800 / 2,500 / 1,500 MW) at the same 100 points: no point passes. The helium-duty package is violated at all 100 (−1,801.2 MW: the 1,500 MW package against the 3,301.2 MW duty the loop delivers, a constant of the sweep), the compressor at 79, rejection at 52, the turbine at 5; violated-screen sets: {compressor, helium duty, rejection} × 47, {heat removal, compressor, helium duty} × 23, {heat removal, helium duty} × 21, {compressor, helium duty, rejection, turbine} × 5, {compressor, helium duty} × 4. I-R (3,200 / 7,000 / 3,600 / 5,000 / 3,500) fails only the compressor screen, at the four upper-edge points. The booked purchase stays the selected rating's price in every violated case (I-A overnight 4,350,208,470.00 at every point; I-R 4,873,104,037.11). No boundary claim is made; the violations are located.

#### `compressor_efficiency`, `turbine_efficiency` — feasible structure (search framing)
**Applies:** not applicable — these axes are sensitivity-framed

#### `compressor_efficiency`, `turbine_efficiency` — observed response (sensitivity framing)
**Applies:** yes

Compressor 0.85: net −95.0 to −107.5 MW at the anchors; 2,250 / 1.5183 fails heat removal by 2.778 MW (the hotter compressor exit raises the heater inlet), 2,500 / 1.45 and the starting point still pass. Compressor 0.92: +65.8 to +74.5 MW, every passing anchor still passes, 2,250 / 1.50 still fails (42.0 MW unmet). Turbine 0.90: −41.6 to −91.5 MW; 2,250 / 1.5183 fails by 70.7 MW unmet, 2,500 / 1.45 passes (533.6 MW; its helium hot-bound margin is the 0.363 K of § 13). Turbine 0.95: +26.3 to +59.4 MW; 2,250 / 1.50 passes (658.9 MW). Located violations: `s1-comp0.85-f2250-r1.5183`, `s1-comp0.85-f2250-r1.5000`, `s1-turb0.90-f2250-r1.5183`, `s1-turb0.90-f2250-r1.5000`, `s1-comp0.92-f2250-r1.5000`. No boundary claim is made; the uniform offsets cannot test a distance-dependent penalty (contract § 8 a).

#### `aux_heat`, `aux_cryo`, `aux_fuel_base`, `aux_control`, `aux_other`, `fuel_exhaust_term` — feasible structure (search framing)
**Applies:** not applicable — these axes are sensitivity-framed

#### `aux_heat`, `aux_cryo`, `aux_fuel_base`, `aux_control`, `aux_other`, `fuel_exhaust_term` — observed response (sensitivity framing)
**Applies:** yes

Register ×0.5 / ×1.5: net +32.500 / −32.500 MW at every anchor, identical at all four; LCOE −57 to −110 / +64 to +129 USD/MWh (larger at the starting point because its net is lower). The wired fuel term: −1.789 MW everywhere, +3.3 to +6.6 USD/MWh. The Stellaris-equivalent register (100 MW wall-plug heating, 2.14 cryogenic, 13.02 cooling-water pumping): −50.160 MW everywhere, +101 to +208 USD/MWh. No verdict changes at any passing anchor; the only violations are the anchor `2,250 / 1.50`'s own (46.421 MW unmet, unchanged). No boundary claim is made.

#### `pump_law_dp_ref` — feasible structure (search framing)
**Applies:** not applicable — this axis is sensitivity-framed

#### `pump_law_dp_ref` — observed response (sensitivity framing)
**Applies:** yes

×0.5 (pump 87.6 MW instead of 175.3): +24.7 MW at the starting point and the best point, +27.2 at 2,500 / 1.45, and 2,250 / 1.50 passes at 657.8 MW (+58.4: less friction heat to remove). ×2 (350.6 MW): −49.8 MW at the starting point, which still passes because its heat-removal slack absorbs the extra friction heat; the three boundary anchors fail heat removal (unmet 174.1, 224.2, 103.3 MW) and lose 126 to 178 MW of net. Located violations: `s3-dp2-f2250-r1.5183`, `s3-dp2-f2250-r1.5000`, `s3-dp2-f2500-r1.4500`. No boundary claim is made; the law is the Stellaris relation with its constants, not a hydraulic model.

#### `equipment_price_factor`, `rest_of_plant_price_factor` — feasible structure (search framing)
**Applies:** not applicable — these axes are sensitivity-framed

#### `equipment_price_factor`, `rest_of_plant_price_factor` — observed response (sensitivity framing)
**Applies:** yes

Equipment ×0.5 / ×1.5: LCOE −9.4 to −13.2 / +9.4 to +13.2 USD/MWh, net unchanged, no verdict change. Rest-of-plant ×0.5 / ×2: −25.0 to −35.0 / +49.9 to +70.1. Neither reorders the operating points. No boundary claim is made; these axes reach no check (§ 8).

#### `tritium_feed`, `supply_service` — feasible structure (search framing)
**Applies:** not applicable — these axes are sensitivity-framed

#### `tritium_feed`, `supply_service` — observed response (sensitivity framing)
**Applies:** yes

Feed 100 kg/year with 30 MUSD/year service: LCOE 624.389 at the starting point (−935.0), 445.790 at 2,250 / 1.5183 (−667.6), 462.723 at 2,500 / 1.45 (−692.9); the plant-side LCOE and every balance channel unchanged; the ranking unchanged. No boundary claim is made.

#### `exchanger_area` — feasible structure (search framing)
**Applies:** not applicable — this axis is sensitivity-framed

#### `exchanger_area` — observed response (sensitivity framing)
**Applies:** yes

75,000 m² (UA 75 MW/K, purchase 87,488,550 at ratio 1.5, not extrapolated): along the 2,500 kg/s column the lowest passing ratio moves from 1.45 to 1.40 (671.624 MW, LCOE 991.070; 1.425 passes at 625.286; 1.375 fails by 79.2 MW unmet); 2,250 / 1.50 passes at 632.540 MW. At the points that already passed, net is unchanged and LCOE rises 0.68 to 0.95 USD/MWh for the larger purchase. Located violations: `s6-hx75000-f2500-r1.3000` to `-r1.3750`. No boundary claim is made; it is a labelled alternative inventory, never a resize.

## 7. Axis groups

Every declared qualified entry key (`axes.json`, 31 keys in 21 groups), prefix `costed_loop_brayton__plant__` omitted.

| Axis | Entry key | Provenance | Note |
|---|---|---|---|
| `cycle_flow` | `cycle__selected_flow` | fan_out | |
| `stage_ratio` | `compressor_1__selected_ratio`, `compressor_2__selected_ratio`, `compressor_3__selected_ratio` | fan_out | one value applied to three chosen inputs as a declared equal-stage scenario, not a tie (annex § Declared ties) |
| `compressor_rating` | `compressor_capacity__selected_rating` | fan_out | |
| `turbine_rating` | `turbine_capacity__selected_rating` | fan_out | |
| `generator_rating` | `generator_capacity__selected_rating` | fan_out | |
| `rejection_rating` | `rejection_capacity__selected_rating` | fan_out | |
| `he_duty_rating` | `he_capacity__selected_rating` | fan_out | |
| `compressor_efficiency` | `compressor_1__efficiency`, `compressor_2__efficiency`, `compressor_3__efficiency` | fan_out | one value to three stages, a declared scenario |
| `turbine_efficiency` | `cycle__turbine_efficiency` | fan_out | |
| `aux_heat` | `electrical__auxiliary_heat` | fan_out | coupled MW at 0.5 wall-plug efficiency |
| `aux_cryo` | `electrical__cryo` | fan_out | |
| `aux_fuel_base` | `electrical__fuel_base` | fan_out | |
| `aux_control` | `electrical__control` | fan_out | |
| `aux_other` | `electrical__other_electric` | fan_out | |
| `fuel_exhaust_term` | `electrical__fuel_exhaust` | fan_out | atoms/s; 0 in the main block |
| `pump_law_dp_ref` | `primary_loop__dp_loop_ref` | fan_out | |
| `equipment_price_factor` | `compressor_equipment__price_factor`, `turbine_equipment__price_factor`, `generator_equipment__price_factor`, `heat_rejection_equipment__price_factor`, `he_duty_equipment__price_factor`, `he_hx__price_factor`, `conversion_services__price_factor` | fan_out | one factor on the seven priced items |
| `rest_of_plant_price_factor` | `rest_of_plant__price_factor` | fan_out | |
| `tritium_feed` | `fuel_inventory__annual_recovery_kg` | fan_out | |
| `supply_service` | `finance__supply_service_annual` | fan_out | |
| `exchanger_area` | `he_hx__selected_area` | fan_out | |

## 8. Indicators and rulings

`indicators.json` (study-indicators/v1, subset false, manifest digest `a6d84577cba97eeb…`, pin `53f48a7e…`). No axis was declined.

| Axis | Indicator | Ruling | Note |
|---|---|---|---|
| `cycle_flow`, `stage_ratio`, `compressor_efficiency`, `turbine_efficiency`, `exchanger_area` | constraints_reachable (6 of 9: heat removal, net positive, the four rating screens downstream of the cycle) | swept | the search axes and the cycle-side assumptions |
| `pump_law_dp_ref` | constraints_reachable (8 of 9, the loop screen included) | swept | |
| `aux_heat`, `aux_cryo`, `aux_fuel_base`, `aux_control`, `aux_other`, `fuel_exhaust_term` | constraints_reachable (3 of 9: net positive and the two generator-side screens) | swept | |
| `compressor_rating`, `turbine_rating`, `generator_rating`, `rejection_rating`, `he_duty_rating` | constraints_reachable (its own screen) | swept as the I-A block | |
| `tritium_feed` | constraints_reachable (the stock screen) | swept | the screen never responds in fact (feed enters the annual accounts, not the stock) |
| `equipment_price_factor` | no_constraint_response | coordinator ruling: swept as a price axis; the owner was not present | it enters cost only |
| `rest_of_plant_price_factor` | no_constraint_response | coordinator ruling: swept as a price axis | as above |
| `supply_service` | no_constraint_response | coordinator ruling: swept with the named feed | as above |

**Not derivable, disclosed in every record.** These are not decidable from the indicator run and no indicator output claims them: monotonicity of any channel in any axis; identity of the same physical quantity across differing key names; intra-module operand dependency. `constraints_reachable` is a *possible* path and never a statement that a constraint responds. `unresisted` is the agent's recorded judgment, never a tool output.

**Model-development findings.**

| Axis | What should push back and is not modeled | Finding id |
|---|---|---|
| `equipment_price_factor` | no cost-side check exists: nothing bounds a purchase by a budget or an affordability rule, so a price factor can never violate anything | `20260926-design-study-parameters#8` |
| `rest_of_plant_price_factor` | as above; the rest-of-plant is an `[ASSUMED]` constant with no function-level check | `20260926-design-study-parameters#8` |
| `supply_service` | as above; the service cost has no price-versus-capability relationship (the ARIES lifecycle study's own disclosure) | `20260926-design-study-parameters#8` |

## 9. Preflight results

`preparation/preflight_results.json` (`scripts/study/preflight.py gates`, outcome pass). The identity and baseline gates read `preparation/package_identity.json` and `preparation/baseline_result.json`, deposited by the route at step 5.

| Gate | Outcome | Detail |
|---|---|---|
| Declared-group key validation | pass | 31 declared keys across 21 groups, all package inputs |
| Suffix-sibling scan (warnings only) | pass | none |
| Baseline gate against the pinned headline | pass | `lifecycle_price__evaluate__lcoe` 1,559.4383607658922 reproduces at relative deviation 0; 4 of 4 pinned verdicts match |
| Manifest / package fingerprint match | pass | both recorded package fingerprints match the package on disk (`manifest_currency`); identity kind sealed, digest `a4c7a871…` recomputed from 0 allowed-modified files |
| Package cleanliness | pass | package tree byte-untouched (git clean), before and after execution |

## 10. Execution route and why

- **Route:** study-local direct-API (`StudyRunner` + `PreparedListStrategy` through `exploration/costed_loop_brayton/studies/study_route.py`, the ARIES route with this package's names)
- **Why this route:** the study is three coordinated blocks (two inventories at the same operating points, plus sensitivity levels at anchors chosen from the scan), not a Cartesian grid, so the `teax-study` CLI's grid form does not express it; the route was exercised and gated at steps 5–6 before this rationale was written. The stock strict loader loads the package with no adapter.

**Glue disclosure.** Glue ledger: none. No adapter on this route, so nothing is harness-supplied; every input of every case is a declared value composed on the manifest baseline.

## 11. Study definition and window provenance

The window is the contract's (§ 11), engineered from the 54-point screen `…/evidence/screen-flow-ratio.md` on the uncosted C-1 package: flow 2,000–4,000 kg/s in 250 kg/s steps (4,000 as the +60 % edge), ratio 1.20–1.80 refined to 0.025 between 1.30 and 1.50 where the screen located the heat-removal boundary. Before any native point ran, every composed point (328: 128 I-R, 128 I-A, 72 sensitivity) was scanned with the package-owned oracle (`oracle-window-scan.json`): 56 were refused, 55 by the lifecycle body's guard on nonpositive net (3,250 kg/s at ratio ≥ 1.50, 3,500 at ≥ 1.45, 4,000 at ≥ 1.375, 2,750 / 1.80, 3,000 / 1.70–1.80, and the same on I-A) and one by the Brayton conditioning guard (4,000 / 1.80: the recuperator hot side colder than the precooler target). Those are reported as the scanned edge and were never stored. The sensitivity anchors were chosen from the same scan by the declared rule: the starting point, the best passing I-R point (2,250 / 1.5183), its ratio-step-lower (2,250 / 1.50) and flow-step-higher neighbour (2,500 / 1.5183, which is the starting point, so the two labels share one case), plus the declared extra anchor `screen-best-passing` (2,500 / 1.45) added at preparation r2 (r1 retained under `preparation-r1/`, 313 composed, 257 kept, same manifest, same scan values). The native run confirmed every scan value to the verification rule except the one channel of § 13.

The window is engineered, not sourced: it costs the claim its generality outside 2,000–4,000 kg/s and 1.20–1.80, and the boundary is located to the grid's resolution (0.025 in ratio between 1.30 and 1.50, 250 kg/s in flow) as a band, not a line.

## 12. Cross-fingerprint correlation and what it means

Single arm, single store, single package identity: executable `a4c7a87136fe3ea373fb02a899ed8262a800a7443891db986411f00f26c8aeea`, semantic `76c68dde7a4de41987be07ecd3ac3bdf814c6ef1895f3ad8d2250275cf9bdee7`, indicator-input fingerprint equal to the live manifest pin `53f48a7e…` (preflight `manifest_currency` pass; the T-004 integration CANDIDATE names the same three). No cross-arm correlation is needed: nil, single fingerprint.

## 13. Verification

**Outcome: REFUSED, on one channel of one case; parked under owner gate G-001.** `scripts/study/verify.py` over all 272 completed cases of the one store (`--sample-size 272`, stratified by verdict combination then filled) compared every catalogued channel against the package-owned oracle at relative deviation below 1e-9 or the manifest's six declared absolute classes and stopped at `s1-turb0.90-f2500-r1.4500` (candidate `c0211`), channel `heat_exchangers__evaluate__he_hot_bound_margin`: store 0.3631786747627075 K, oracle 0.363178674230312 K, absolute 5.32e-10 K, relative 1.466e-9, no declared class (`…/evidence/t005-verify.log`; the tool wrote no summary file). The contract § 9 forbids adding a class after a result is seen and makes the refusal an owner gate (§ 12); the decision and the proposal (a 1e-6 K class for the three hot-bound margin channels, on the closure root-termination basis the ARIES classes use) are in `…/evidence/owner-gate-verification-class.md`. The coordinator's own full comparison (every stored case, every catalogued channel, the same rule and classes) finds exactly that one deviation; the next-worst undeclared channel is `he_unmet` at 9.6e-10 relative on `s1-comp0.85-f2250-r1.5183` (2.778 MW unmet, absolute 2.7e-9 MW); every verdict re-derives identically from the oracle's operands on all 272 cases. No stored value moves under either ruling; what is parked is the seal.

**Not covered.** Values fed identically to both sides (every swept and held input) are not independently verified; the oracle checks the implementation of the model's assumptions, not their scientific qualification; the glue ledger is empty so nothing is harness-supplied; the 56 refused points have no stored values to verify and are reported from the oracle alone; the oracle's refusal wording for nonpositive net (`nonpositive net electricity: LCOE undefined`) differs from the body's (`LCOE undefined for nonpositive net electricity`) and was matched by condition, not text.

## 14. Review outcomes

| Lens | Verdict | Disposition |
|---|---|---|
| Comparison contract (fresh reviewer, goal T-002) | FINDINGS on v1 (the fuel-term control conflict), PASS on v2 | `…/evidence/contract-review.md`; the S2 wired-term case is an input override, the main block keeps the term at 0 |
| WI-094 design (fresh reviewer, goal T-003) | PASS, five notes applied | `…/evidence/design-review.md` |
| WI-094 implementation on executed evidence (fresh reviewer, goal T-004) | PASS, three notes | `…/evidence/implementation-review.md`; dispositions in `work/active/WI-094_costed-loop-brayton/report.md` |
| Integration seam (T-004) | CANDIDATE, ten gates | `…/evidence/integration-t004/integration_return.json` |
| Pre-execution checkpoint (coordinator, goal C-001.r1) | PASS to execute as a coordinator check; no uncovered trigger; extra anchor declared | goal trail |
| All-point verification against the oracle (executor) | REFUSED on one channel of one case; owner gate G-001 | § 13 |
| Round-1 review of this reading | pending at the round result | goal trail |

## 15. Findings

| Id | Kind | Finding | Disposition | Home |
|---|---|---|---|---|
| `20260926-design-study-parameters#1` | model | The heat-removal check is the limit that stops the improvement: at every flow up to 3,500 kg/s the lowest passing ratio is set by the heater inlet reaching what the 773 K source can deliver through the 50 MW/K exchanger, and the ridge of net lies one grid step on the failing side (electricity-only best 2,500 / 1.425 at 620.0 MW with 7.8 MW unmet against the best passing band 597.5 / 594.6 MW). | reported in the goal answer; the exchanger is the limiting equipment | goal `design-study-parameters` answer |
| `20260926-design-study-parameters#2` | model | A 75,000 m² exchanger (priced 87,488,550, not extrapolated) moves the boundary at 2,500 kg/s from 1.45 to 1.40 and buys +74 MW of passing net (671.6 MW, LCOE 991) for +0.7 USD/MWh at unchanged net: the exchanger area is the priced hardware lever the operating sweep cannot substitute for. | offered as a declared alternative inventory; a modeling item would be needed to make the area a chosen design variable with its own screen | goal answer; candidate modeling item (not opened) |
| `20260926-design-study-parameters#3` | model | The fixed-efficiency treatment's first-order effect is one grid step of boundary: compressor 0.85 or turbine 0.90 fails the best passing point (2,250 / 1.5183) by 2.8 and 70.7 MW unmet, while 2,500 / 1.45 passes under every S1 level; no off-design map exists to test a distance-dependent penalty. | the operating claim is scoped to near the design flow; the missing map is named | goal answer; documented seam (contract § 8 a) |
| `20260926-design-study-parameters#4` | model | The loop pump law couples the friction heat to the heat-removal limit: dp ×2 fails every boundary anchor (103–224 MW unmet, −126 to −178 MW net) while the starting point, with heat-removal slack, loses only 49.8 MW; dp ×0.5 makes 2,250 / 1.50 pass. | reported; the pump law is a declared assumption, not a hydraulic model | goal answer; documented seam (contract § 8 g) |
| `20260926-design-study-parameters#5` | model | The ARIES-selected inventory I-A passes at none of the 100 points (helium-duty package 1,500 MW against the constant 3,301 MW duty; compressor 1,600 MW at 79 points); its 8–11 USD/MWh lower LCOE is the price of ratings that do not support the operation. Hardware selection precedes the sweep (MR-7). | reported; no resize | goal answer |
| `20260926-design-study-parameters#6` | process | The verifier's relative rule refuses a near-zero difference channel (a 0.363 K hot-bound margin) at 1.5e-9 while the underlying temperatures agree to 3e-10 K; the manifest's class transcription from the contract omitted the ARIES `unmet` classes and had none for the margins. | owner gate G-001 raised; no class added after the result | owner gate `…/evidence/owner-gate-verification-class.md`; policy rule (`modeling_project/STUDY_POLICY.md`, candidate note) |
| `20260926-design-study-parameters#7` | process | The contract's anchor rule (best point plus its two neighbours) produced a flow-step-higher neighbour equal to the starting point on the refined grid, leaving three distinct anchors; an extra declared anchor at the screen's best point was added at preparation r2 with r1 retained. | recorded; the composer records anchors and duplicates in `axis-plan.json` | runbook step 7 (recorded in this record § 11) |
| `20260926-design-study-parameters#8` | model | Three price and convention axes (`equipment_price_factor`, `rest_of_plant_price_factor`, `supply_service`) reach no check: no cost-side constraint exists in the package. | disclosed; no ruling needed from the owner for this study | unrouted |

## 16. Snapshot

- **File:** `snapshot.json`
- **sha256:** not written: the seal is parked under owner gate G-001 (§ 13); an addendum will carry the digest after the ruling and the re-verification
- **Schema version:** 1 (when written)

No snapshot content is restated here.

## 17. What this record does not contain

- The seal: no `snapshot.json`, no `sealed-package.tar.gz`, no passing `results/verification_summary.json`; the verification outcome is the refusal of § 13 and the coordinator's own comparison, which is not the tool's verdict.
- Native values for the 56 refused points; they exist only as the oracle scan's refusals.
- Any interpolated optimum or boundary line; the grid resolution is the claim's resolution.
- Off-design machine maps, a hydraulic pump model, a blanket-inlet requirement, heat-rejection pumping, or any cost-side check (§ 8, contract § 8).
- A sourced window; the window is engineered (§ 11).
- The round's reading of what these results mean for the owner's question; that is the goal's `answer.md`.
