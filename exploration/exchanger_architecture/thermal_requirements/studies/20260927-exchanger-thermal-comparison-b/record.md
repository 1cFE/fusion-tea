# Thermally consistent exchanger architecture comparison

## 1. Study header

**Study id:** 20260927-exchanger-thermal-comparison-b. **Package:** exchanger_architecture_thermal_tea. **Executed:** 2026-09-27. **Executor:** goal coordinator, with separate oracle verification and reporting authors. **Mode:** execute. **Arms:** one architecture arm on the corrected executable. This replaces the preserved failed attempt by replaying its exact 1277 input maps.

## 2. Intake

Owner intake is retained verbatim in [owner-brief.md](owner-brief.md), [owner-supplement-r2.md](owner-supplement-r2.md) and [owner-supplement-r3.md](owner-supplement-r3.md).

> The goal need not deliver a physically qualified plant recommendation. It does need to establish that its preferred cases satisfy the thermal requirements it claims to represent.

> you are very intelligent. I trust your judgement. please make your best calls, document it, and proceed until you have strong study results.

[AGENT] Adopt source-informed N-R aggregate returns and 30 K at all six actual primary terminals. These remain agent-selected requirements under delegated authority; the source does not uniquely prescribe all six. Use fixed priced A/B inventories, physical primary bypass, common flow freedom and supplied network split. The full contract and cost omissions are in r3-study-contract.md and r3-cost-boundary.md. Their Round 3 labels identify original preparation; this unchanged-meaning execution is Round 4.

## 3. Objective and result

Qualified objectives are `aries_integrated_plant__plant_ledger__evaluate__net_electric` and `aries_integrated_plant__lifecycle_price__evaluate__lcoe`. Rank complete passing operations at common source and offer; the represented cost numerator is common within main matched pairs.

All 1277 maps completed; 535 satisfy every engineering predicate and positive net. At 1835.451283 MW supplied fusion, offer B gives series 497.768342 MW / 951.505200 USD2004/MWh versus network 528.427310 MW / 896.299560 USD2004/MWh. The executed zero-tritium-price endpoints give 95.960966 versus 90.393381 USD2004/MWh. Source, hardware and prices are conditional inputs. The main network gain survives fine flow/split refinement; extra network pressure loss can reverse it. Original equipment fails the adopted thermal contract. See [results analysis](results/reporting/r3-results-analysis.md) and complete [paired data](results/reporting/r3-data/pairs.csv).

## 4. Constraint outcomes

All verdicts are determinate. Counts cover every completed map, including intended failure controls. The selected main operations satisfy all 35 predicates. Exact violated-case IDs and observed input locations are in [axis-violations.json](results/axis-violations.json).

| constraint_id | source_local_identity | Satisfied | Violated |
|---|---|---:|---:|
| `aries_integrated_plant__compressor_capacity__capacity_ok__a45f9cf05e8aa7ab` | `capacity_ok` | 1260 | 17 |
| `aries_integrated_plant__divertor_capacity__capacity_ok__be7081920ad8e8ed` | `capacity_ok` | 1277 | 0 |
| `aries_integrated_plant__divertor_pump__capacity_ok__d6730c7060447f4c` | `capacity_ok` | 1277 | 0 |
| `aries_integrated_plant__fuel_capacity__capacity_ok__8eb5888bfe62cd64` | `capacity_ok` | 1277 | 0 |
| `aries_integrated_plant__fuel_inventory__capacity_ok__37f4667fbfb616d0` | `capacity_ok` | 1277 | 0 |
| `aries_integrated_plant__generator_capacity__capacity_ok__60b43f15d48ff161` | `capacity_ok` | 1277 | 0 |
| `aries_integrated_plant__he_capacity__capacity_ok__db2733d1d5baf3cf` | `capacity_ok` | 1277 | 0 |
| `aries_integrated_plant__he_pump__capacity_ok__fcee5ee009fe5180` | `capacity_ok` | 1277 | 0 |
| `aries_integrated_plant__heat_exchangers__divertor_cold_approach_ok__e70598993d392f74` | `divertor_cold_approach_ok` | 1263 | 14 |
| `aries_integrated_plant__heat_exchangers__divertor_control_ok__14c1c0f314a994fd` | `divertor_control_ok` | 1271 | 6 |
| `aries_integrated_plant__heat_exchangers__divertor_hot_approach_ok__5e95ef937d10cc33` | `divertor_hot_approach_ok` | 1199 | 78 |
| `aries_integrated_plant__heat_exchangers__divertor_hot_cap_ok__cd5f29bd8533c481` | `divertor_hot_cap_ok` | 1259 | 18 |
| `aries_integrated_plant__heat_exchangers__divertor_required_hot_ok__712add8be60bd1ae` | `divertor_required_hot_ok` | 1259 | 18 |
| `aries_integrated_plant__heat_exchangers__divertor_return_ok__f69c5310bdcc41d7` | `divertor_return_ok` | 867 | 410 |
| `aries_integrated_plant__heat_exchangers__divertor_state_ok__416e01681b16be81` | `divertor_state_ok` | 1277 | 0 |
| `aries_integrated_plant__heat_exchangers__he_cold_approach_ok__eab4f3486f0aa140` | `he_cold_approach_ok` | 1191 | 86 |
| `aries_integrated_plant__heat_exchangers__he_control_ok__f48454bb1d6f0e91` | `he_control_ok` | 1269 | 8 |
| `aries_integrated_plant__heat_exchangers__he_hot_approach_ok__7a2967e855192aeb` | `he_hot_approach_ok` | 932 | 345 |
| `aries_integrated_plant__heat_exchangers__he_hot_cap_ok__05ebd6dad2e4adc1` | `he_hot_cap_ok` | 1277 | 0 |
| `aries_integrated_plant__heat_exchangers__he_required_hot_ok__3371b55ff752c6e4` | `he_required_hot_ok` | 1277 | 0 |
| `aries_integrated_plant__heat_exchangers__he_return_ok__ae5f4d6db630fc8e` | `he_return_ok` | 932 | 345 |
| `aries_integrated_plant__heat_exchangers__he_state_ok__d5b9d58030392fe5` | `he_state_ok` | 1277 | 0 |
| `aries_integrated_plant__heat_exchangers__pbli_cold_approach_ok__667d6ca45c6e61de` | `pbli_cold_approach_ok` | 1231 | 46 |
| `aries_integrated_plant__heat_exchangers__pbli_control_ok__0c3b021e2e8589fb` | `pbli_control_ok` | 1276 | 1 |
| `aries_integrated_plant__heat_exchangers__pbli_hot_approach_ok__85855c74bdb13305` | `pbli_hot_approach_ok` | 934 | 343 |
| `aries_integrated_plant__heat_exchangers__pbli_hot_cap_ok__73a44108fcb5be1c` | `pbli_hot_cap_ok` | 1277 | 0 |
| `aries_integrated_plant__heat_exchangers__pbli_required_hot_ok__aa9057b8ce236e6b` | `pbli_required_hot_ok` | 1277 | 0 |
| `aries_integrated_plant__heat_exchangers__pbli_return_ok__100f6bf9ad61a22c` | `pbli_return_ok` | 726 | 551 |
| `aries_integrated_plant__heat_exchangers__pbli_state_ok__4664e5e1ddbb7ac5` | `pbli_state_ok` | 1277 | 0 |
| `aries_integrated_plant__pbli_capacity__capacity_ok__55a012a287da9395` | `capacity_ok` | 1277 | 0 |
| `aries_integrated_plant__pbli_pump__capacity_ok__79d116aa320dd4fb` | `capacity_ok` | 1277 | 0 |
| `aries_integrated_plant__plant_ledger__balances_ok__9af2e85b5e4e5535` | `balances_ok` | 1277 | 0 |
| `aries_integrated_plant__plant_ledger__heat_removal_ok__695378663bcd8d07` | `heat_removal_ok` | 663 | 614 |
| `aries_integrated_plant__rejection_capacity__capacity_ok__295420bc9fb25608` | `capacity_ok` | 1277 | 0 |
| `aries_integrated_plant__turbine_capacity__capacity_ok__089f9e8e61919ec1` | `capacity_ok` | 1277 | 0 |

## 5. Framing

| Axis | Proposed | Judged after execution | Changed? | Basis |
|---|---|---|---|---|
| source_mode | sensitivity | sensitivity | No | Legacy baseline and supplied source boundary; no plasma sustainment claim. |
| source_load | search | search | No | Matched loads 1650,1835.4512830147435,1950,2000 MW; old leaders and source-cap boundary controls. |
| architecture | search | search | No | Series and series-then-parallel secondary connections. |
| flow | search | search | No | Common broad flow scan; independently refine every sampled feasible component. |
| split | search | search | No | Network split .1–.9 initially, local refinement to .0005; series inert placeholder .85. |
| control_mode | sensitivity | sensitivity | No | Legacy0 control and main1 explicit primary bypass. |
| offer | sensitivity | sensitivity | No | Explicit original,A,B areas/prices, common price multiplier and inherited linear price sensitivity; coordinated offers, no physical identity asserted. |
| approach | sensitivity | sensitivity | No | Main30K, labelled15/45K engineering requirements. |
| conductance | sensitivity | sensitivity | No | Correlated U multipliers .8/1.2 at fixed area; not a resizing law. |
| pressure_loss | sensitivity | sensitivity | No | Common .02/.08 and differential network-loss comparison against baseline .045. |
| pump_mode | sensitivity | sensitivity | No | Coordinated explicit fixed-power scenarios. |
| pump_power | sensitivity | sensitivity | No | Each pump own reference power multiplied by .8/1.2; recovered heat recomputed. |
| bypass_limit | sensitivity | sensitivity | No | Main mathematical range1; assumed limits.25/.5, no actuator rating claim. |
| return_convention | sensitivity | sensitivity | No | Main aggregate targets; alternate post-pump-source reading subtracts booked recovered heat/Ch from aggregate return. |
| tritium_price | sensitivity | sensitivity | No | Zero-price accounting endpoint reprices initial stock and annual purchases. |

## 6. Per-axis account

#### source_mode — feasible structure (search framing)

**Applies:** not applicable — this axis is sensitivity-framed.

#### source_mode — observed response (sensitivity framing)

**Applies:** yes.

The calculated-source legacy control preserves the historical mode. Main comparisons supply source power. Neither establishes required plasma heating or sustainment.

Observed violations for `source_mode`, with each qualified predicate, native case IDs and all declared keys' values or observed extrema, are indexed under this axis in [axis-violations.json](results/axis-violations.json). These are locations of actual sampled failures; axis association alone does not establish causality. No uncertainty boundary is claimed.

#### source_load — feasible structure (search framing)

**Applies:** yes.

The N-R divertor return/flow/hot cap gives an analytic upper source bound of 2005.036667 MW. Native original/A/B controls bracket 2005/2005.04 MW and reject old 2200/2300 leaders. Main selected A/B points pass at four declared loads except no sampled B-series pass at 1650 MW. This absence is sampled, not a proof.

Observed violations for `source_load`, with each qualified predicate, native case IDs and all declared keys' values or observed extrema, are indexed under this axis in [axis-violations.json](results/axis-violations.json). These are locations of actual sampled failures; axis association alone does not establish causality.

#### source_load — observed response (sensitivity framing)

**Applies:** not applicable — this axis is search-framed.

#### architecture — feasible structure (search framing)

**Applies:** yes.

Seven matched main pairs favor the network by 30.659–44.742 MW; B at 1650 MW has a network-only sampled pass. Seven passing equal-flow controls have exactly equal net output. The advantage is access to lower passing flow, not an additional cycle-efficiency term.

Observed violations for `architecture`, with each qualified predicate, native case IDs and all declared keys' values or observed extrema, are indexed under this axis in [axis-violations.json](results/axis-violations.json). These are locations of actual sampled failures; axis association alone does not establish causality.

#### architecture — observed response (sensitivity framing)

**Applies:** not applicable — this axis is search-framed.

#### flow — feasible structure (search framing)

**Applies:** yes.

Every selected passing search group has a lower native failing neighbor 0.00625 kg/s away at its selected split. Complete failed predicates and inputs locate each boundary witness. Main nominal B selected flows are 1290.783398 series and 1245.934766 network kg/s. These are local sampled transitions, not global optima.

Observed violations for `flow`, with each qualified predicate, native case IDs and all declared keys' values or observed extrema, are indexed under this axis in [axis-violations.json](results/axis-violations.json). These are locations of actual sampled failures; axis association alone does not establish causality.

#### flow — observed response (sensitivity framing)

**Applies:** not applicable — this axis is search-framed.

#### split — feasible structure (search framing)

**Applies:** yes.

Local split refinement reaches 0.0005, then 0.00025 for six unstable cost targets. The additional receipt supersedes earlier split-halving changes where applicable. Final stability meets 0.2 MW /0.1 USD2004/MWh. Nominal B selected split is 0.741. Failure components and outer-edge checks remain visible.

Observed violations for `split`, with each qualified predicate, native case IDs and all declared keys' values or observed extrema, are indexed under this axis in [axis-violations.json](results/axis-violations.json). These are locations of actual sampled failures; axis association alone does not establish causality.

#### split — observed response (sensitivity framing)

**Applies:** not applicable — this axis is search-framed.

#### control_mode — feasible structure (search framing)

**Applies:** not applicable — this axis is sensitivity-framed.

#### control_mode — observed response (sensitivity framing)

**Applies:** yes.

The legacy path remains exact in regression and in two retained study controls, while the added thermal predicates expose missing return/approach compliance. Main physical primary bypass enforces aggregate return; actual pre-mix exchanger outlets determine cold approaches.

Observed violations for `control_mode`, with each qualified predicate, native case IDs and all declared keys' values or observed extrema, are indexed under this axis in [axis-violations.json](results/axis-violations.json). These are locations of actual sampled failures; axis association alone does not establish causality. No uncertainty boundary is claimed.

#### offer — feasible structure (search framing)

**Applies:** not applicable — this axis is sensitivity-framed.

#### offer — observed response (sensitivity framing)

**Applies:** yes.

All original-inventory controls fail. A/B are explicit area/price pairs, each 174.9771 million USD2004 total assumed purchase. The nominal B network produces more net than A at the same assumed cost; no procurement ranking is established. Half/double purchase and extrapolated linear-area scenarios preserve matched nominal architecture preference.

Observed violations for `offer`, with each qualified predicate, native case IDs and all declared keys' values or observed extrema, are indexed under this axis in [axis-violations.json](results/axis-violations.json). These are locations of actual sampled failures; axis association alone does not establish causality. No uncertainty boundary is claimed.

#### approach — feasible structure (search framing)

**Applies:** not applicable — this axis is sensitivity-framed.

#### approach — observed response (sensitivity framing)

**Applies:** yes.

Main six-terminal minima are 30 K. Labelled 15 K and 45 K scenarios use B at N only; 45 K has no passing sampled operation in either architecture. All main preferred terminal gaps exceed 33.8327 K.

Observed violations for `approach`, with each qualified predicate, native case IDs and all declared keys' values or observed extrema, are indexed under this axis in [axis-violations.json](results/axis-violations.json). These are locations of actual sampled failures; axis association alone does not establish causality. No uncertainty boundary is claimed.

#### conductance — feasible structure (search framing)

**Applies:** not applicable — this axis is sensitivity-framed.

#### conductance — observed response (sensitivity framing)

**Applies:** yes.

At fixed B area and N source, U×0.8 retains a 19.4144 MW paired network gain. U×1.2 has a network pass and no sampled series pass, so a paired allowance is undefined. Constant U versus active primary flow remains unsupported physics.

Observed violations for `conductance`, with each qualified predicate, native case IDs and all declared keys' values or observed extrema, are indexed under this axis in [axis-violations.json](results/axis-violations.json). These are locations of actual sampled failures; axis association alone does not establish causality. No uncertainty boundary is claimed.

#### pressure_loss — feasible structure (search framing)

**Applies:** not applicable — this axis is sensitivity-framed.

#### pressure_loss — observed response (sensitivity framing)

**Applies:** yes.

At B/N, common 2% and 8% loss retain29.9380/31.7701 MW network gains. Network8% compared with series 4.5% instead loses6.5866 MW and increases LCOE12.7593 USD2004/MWh. The assumed differential is a scenario, not a hydraulic prediction.

Observed violations for `pressure_loss`, with each qualified predicate, native case IDs and all declared keys' values or observed extrema, are indexed under this axis in [axis-violations.json](results/axis-violations.json). These are locations of actual sampled failures; axis association alone does not establish causality. No uncertainty boundary is claimed.

#### pump_mode — feasible structure (search framing)

**Applies:** not applicable — this axis is sensitivity-framed.

#### pump_mode — observed response (sensitivity framing)

**Applies:** yes.

Pump perturbations use coordinated fixed-power mode to make the .8/1.2 scenarios explicit. The native model recomputes recovered friction heat and coupled return/hot states; legacy modes are retained controls.

Observed violations for `pump_mode`, with each qualified predicate, native case IDs and all declared keys' values or observed extrema, are indexed under this axis in [axis-violations.json](results/axis-violations.json). These are locations of actual sampled failures; axis association alone does not establish causality. No uncertainty boundary is claimed.

#### pump_power — feasible structure (search framing)

**Applies:** not applicable — this axis is sensitivity-framed.

#### pump_power — observed response (sensitivity framing)

**Applies:** yes.

At B/N, multiplying the three reference pump powers by .8/1.2 retains30.0581/31.2932 MW network gains. Recovered heat is charged once; these are not post hoc net-power subtractions.

Observed violations for `pump_power`, with each qualified predicate, native case IDs and all declared keys' values or observed extrema, are indexed under this axis in [axis-violations.json](results/axis-violations.json). These are locations of actual sampled failures; axis association alone does not establish causality. No uncertainty boundary is claimed.

#### bypass_limit — feasible structure (search framing)

**Applies:** not applicable — this axis is sensitivity-framed.

#### bypass_limit — observed response (sensitivity framing)

**Applies:** yes.

No sampled B/N operation passes when each branch bypass is limited to .25 or .5. Nominal main B needs blanket-He bypass .68872 in series and .63229 in the network. The main limit 1 denotes the mathematical control domain; no valve rating is claimed.

Observed violations for `bypass_limit`, with each qualified predicate, native case IDs and all declared keys' values or observed extrema, are indexed under this axis in [axis-violations.json](results/axis-violations.json). These are locations of actual sampled failures; axis association alone does not establish causality. No uncertainty boundary is claimed.

#### return_convention — feasible structure (search framing)

**Applies:** not applicable — this axis is sensitivity-framed.

#### return_convention — observed response (sensitivity framing)

**Applies:** yes.

The alternative post-pump source reading subtracts booked pump heat/Ch from aggregate return targets and retains delivered duty. At B/N the reselected gain is29.3195 MW. It is a separate labelled convention, not a replacement of the main returns.

Observed violations for `return_convention`, with each qualified predicate, native case IDs and all declared keys' values or observed extrema, are indexed under this axis in [axis-violations.json](results/axis-violations.json). These are locations of actual sampled failures; axis association alone does not establish causality. No uncertainty boundary is claimed.

#### tritium_price — feasible structure (search framing)

**Applies:** not applicable — this axis is sensitivity-framed.

#### tritium_price — observed response (sensitivity framing)

**Applies:** yes.

The zero-price endpoint changes startup tritium stock and annual purchases consistently. At nominal B the paired LCOEs become95.960966/90.393381 USD2004/MWh. No breeding or supply-availability claim follows; deuterium remains charged.

Observed violations for `tritium_price`, with each qualified predicate, native case IDs and all declared keys' values or observed extrema, are indexed under this axis in [axis-violations.json](results/axis-violations.json). These are locations of actual sampled failures; axis association alone does not establish causality. No uncertainty boundary is claimed.


## 7. Axis groups

| Axis | Entry key | Provenance | Interpretation |
|---|---|---|---|
| source_mode | `aries_integrated_plant__source__producer_mode` | fan_out | Supplied operating/scenario choice. |
| source_load | `aries_integrated_plant__source__reference_fusion_mw` | fan_out | Supplied operating/scenario choice. |
| architecture | `aries_integrated_plant__heat_exchangers__network_mode` | fan_out | Supplied operating/scenario choice. |
| flow | `aries_integrated_plant__cycle__selected_flow` | fan_out | Supplied operating/scenario choice. |
| split | `aries_integrated_plant__heat_exchangers__pbli_split_fraction` | fan_out | Supplied operating/scenario choice. |
| control_mode | `aries_integrated_plant__heat_exchangers__control_mode` | fan_out | Supplied operating/scenario choice. |
| offer | `aries_integrated_plant__he_hx__selected_area` | fan_out | Supplied operating/scenario choice. |
| offer | `aries_integrated_plant__he_hx__price_factor` | tie | Agent-declared coordinated scenario; no cross-key physical equality asserted. |
| offer | `aries_integrated_plant__pbli_hx__selected_area` | tie | Agent-declared coordinated scenario; no cross-key physical equality asserted. |
| offer | `aries_integrated_plant__pbli_hx__price_factor` | tie | Agent-declared coordinated scenario; no cross-key physical equality asserted. |
| offer | `aries_integrated_plant__divertor_hx__selected_area` | tie | Agent-declared coordinated scenario; no cross-key physical equality asserted. |
| offer | `aries_integrated_plant__divertor_hx__price_factor` | tie | Agent-declared coordinated scenario; no cross-key physical equality asserted. |
| approach | `aries_integrated_plant__heat_exchangers__he_hot_approach` | fan_out | Supplied operating/scenario choice. |
| approach | `aries_integrated_plant__heat_exchangers__he_cold_approach` | tie | Agent-declared coordinated scenario; no cross-key physical equality asserted. |
| approach | `aries_integrated_plant__heat_exchangers__pbli_hot_approach` | tie | Agent-declared coordinated scenario; no cross-key physical equality asserted. |
| approach | `aries_integrated_plant__heat_exchangers__pbli_cold_approach` | tie | Agent-declared coordinated scenario; no cross-key physical equality asserted. |
| approach | `aries_integrated_plant__heat_exchangers__divertor_hot_approach` | tie | Agent-declared coordinated scenario; no cross-key physical equality asserted. |
| approach | `aries_integrated_plant__heat_exchangers__divertor_cold_approach` | tie | Agent-declared coordinated scenario; no cross-key physical equality asserted. |
| conductance | `aries_integrated_plant__he_hx__assumed_u` | fan_out | Supplied operating/scenario choice. |
| conductance | `aries_integrated_plant__pbli_hx__assumed_u` | tie | Agent-declared coordinated scenario; no cross-key physical equality asserted. |
| conductance | `aries_integrated_plant__divertor_hx__assumed_u` | tie | Agent-declared coordinated scenario; no cross-key physical equality asserted. |
| pressure_loss | `aries_integrated_plant__pressure_loss__loss_fraction` | fan_out | Supplied operating/scenario choice. |
| pump_mode | `aries_integrated_plant__he_pump__pump_mode` | fan_out | Supplied operating/scenario choice. |
| pump_mode | `aries_integrated_plant__pbli_pump__pump_mode` | tie | Agent-declared coordinated scenario; no cross-key physical equality asserted. |
| pump_mode | `aries_integrated_plant__divertor_pump__pump_mode` | tie | Agent-declared coordinated scenario; no cross-key physical equality asserted. |
| pump_power | `aries_integrated_plant__he_pump__fixed_power` | fan_out | Supplied operating/scenario choice. |
| pump_power | `aries_integrated_plant__pbli_pump__fixed_power` | tie | Agent-declared coordinated scenario; no cross-key physical equality asserted. |
| pump_power | `aries_integrated_plant__divertor_pump__fixed_power` | tie | Agent-declared coordinated scenario; no cross-key physical equality asserted. |
| bypass_limit | `aries_integrated_plant__heat_exchangers__he_max_bypass` | fan_out | Supplied operating/scenario choice. |
| bypass_limit | `aries_integrated_plant__heat_exchangers__pbli_max_bypass` | tie | Agent-declared coordinated scenario; no cross-key physical equality asserted. |
| bypass_limit | `aries_integrated_plant__heat_exchangers__divertor_max_bypass` | tie | Agent-declared coordinated scenario; no cross-key physical equality asserted. |
| return_convention | `aries_integrated_plant__heat_exchangers__he_required_return` | fan_out | Supplied operating/scenario choice. |
| return_convention | `aries_integrated_plant__heat_exchangers__pbli_required_return` | tie | Agent-declared coordinated scenario; no cross-key physical equality asserted. |
| return_convention | `aries_integrated_plant__heat_exchangers__divertor_required_return` | tie | Agent-declared coordinated scenario; no cross-key physical equality asserted. |
| tritium_price | `aries_integrated_plant__fuel_inventory__tritium_price` | fan_out | Supplied operating/scenario choice. |

Exact coupling rules are retained in manifest.json ties and axes.json; offer ties coordinate price with preselected area, never with demand.

## 8. Indicators and rulings

| Axis | Indicator | Ruling and disposition |
|---|---|---|
| source_mode | constraints_reachable | Execute declared sensitivity scope under delegated judgment. |
| source_load | constraints_reachable | Execute declared search scope under delegated judgment. |
| architecture | constraints_reachable | Execute declared search scope under delegated judgment. |
| flow | constraints_reachable | Execute declared search scope under delegated judgment. |
| split | constraints_reachable | Execute declared search scope under delegated judgment. |
| control_mode | constraints_reachable | Execute declared sensitivity scope under delegated judgment. |
| offer | constraints_reachable | Sensitivity assumption under owner-delegated judgment; missing procurement/fuel support remains a finding. |
| approach | constraints_reachable | Execute declared sensitivity scope under delegated judgment. |
| conductance | constraints_reachable | Execute declared sensitivity scope under delegated judgment. |
| pressure_loss | constraints_reachable | Execute declared sensitivity scope under delegated judgment. |
| pump_mode | constraints_reachable | Execute declared sensitivity scope under delegated judgment. |
| pump_power | constraints_reachable | Execute declared sensitivity scope under delegated judgment. |
| bypass_limit | constraints_reachable | Execute declared sensitivity scope under delegated judgment. |
| return_convention | constraints_reachable | Execute declared sensitivity scope under delegated judgment. |
| tritium_price | constraints_reachable | Sensitivity assumption under owner-delegated judgment; missing procurement/fuel support remains a finding. |

No proposed axis was declined; none produced no_constraint_response. The conditional no_constraint_response finding obligation is therefore not triggered. Agent judgment nevertheless identifies unresisted price assumptions and records findings#2/#3 below. Reachability is a possible graph path, not an actual response. Monotonicity, physical identity across keys and intra-module operand dependency are not derivable from the indicators.

## 9. Preflight results

| Gate | Outcome | Detail |
|---|---|---|
| declared_keys | pass | 35 declared keys across 15 groups, all package inputs |
| sibling_scan | pass | warnings: 35 |
| identity | pass | kind sealed, digest 668b903599f995fd6e9038d61a2401144d79f1db13f221b4a663df7cb24a2a23 recomputed from 0 allowed-modified file(s) and 0 declared source(s); every other sealed artifact matches |
| manifest_currency | pass | both recorded package fingerprints match the package on disk |
| baseline_headline | pass | aries_integrated_plant__lifecycle_price__evaluate__lcoe reproduces at relative deviation 0.000e+00; 24/24 pinned verdicts match |
| package_clean | pass | package tree is byte-untouched (git clean) |

Identity and baseline read preparation/package_identity.json and preparation/baseline_result.json. They were copied byte-for-byte from the successful integration, with source/destination hashes and exact manifest/axes match in preparation/integration-reuse.json. All six gates ran. The 35 suffix-sibling warnings are unrelated price-factor inputs held fixed by the declared three-HX offer scope. Native integration separately passes all ten gates in results/integration_return_used.json. No gate was waived.

## 10. Execution route and why

**Route:** study-local direct API using stock strict loader, PreparedEvaluator, StudyDefinition, PreparedListStrategy, StudyRunner and StudyStore. Coordinated complete input maps across many tied keys justify the direct definition; integration exercised and verified the route before main execution.

**Glue ledger: none.** No adapter supplies missing physical outputs. The native model supplies thermal/control/price quantities. The harness proposes explicit maps and exports exact stored outputs without evaluation; results/export-proof.json proves native evidence unchanged during export. Derived break-even curves are reporting arithmetic with named native parents, not new executed plant candidates.

## 11. Study definition and window provenance

The window is **engineered**. The retained independent scan evaluated 91,234 maps, seeded 697 development passes, searched common broad flows and network splits, refined every observed feasible component and same-status failed intervals, then checked local leaders and outer edges. Initial stages, additional refinement and final financial/control proposals are retained in oracle-selection.json, oracle-refinement-receipt.json and proposal-finalization.json. Full scan bytes are recoverable from prior-attempt/oracle-scan.json.gz and its base inputs; initial/refined proposal history remains in the immutable predecessor.

The negative B-series 1650 check used 1 kg/s spacing without finding a pass. Nonpositive-net points were excluded from native LCOE execution because its positive-energy domain is undefined there; their independent scan outcomes remain visible. No unexpected oracle refusal was converted to an engineering failure. This sampling cannot exclude smaller unseen feasible islands or establish global optimality.

Round4 rechecked all 1277 unchanged full maps and 46 original outer-edge witnesses independently before execution; oracle-window-recheck.json retains that evidence. All selected native operations and lower-flow failure neighbors executed. Scouting-only intermediate stages are labelled in reporting, not claimed as native results. axis-plan.json preserves the original pre-execution false authorization flag; actual release after model integration is recorded in results/execution-context.json and goal T-008. No map or search window changed after the numerical defect.

## 12. Cross-fingerprint correlation and what it means

Single executable fingerprint within this record: no cross-arm correlation is needed. Comparison with the previous failed attempt does cross a numerical-repair fingerprint. results/prior-attempt-correlation.json proves 1277 exact full input maps, identical full constraint catalog including qualified definitions/local identities/predicate IR, unchanged verdicts on all 1275 previously completed maps, unchanged tolerance on independently verified channels, and exact legacy study outputs. Both previously failing cases now complete. Controlled floating-point changes and algorithm diagnostics are disclosed.

The preserved attempt at ca25c49c includes its own original executable archive, source bytes and partial verification. Its archive and attempt digest are referenced in prior-attempt.json. This correlation licenses reuse of the unchanged scientific scan and direct input-matched numerical comparisons; it does not change the earlier failed record into a completed study or relax any thermal requirement.

## 13. Verification

**PASS for all 1277 maps**, with total=completed=sampled 1277,435 independently calculated channels and35 re-derived predicates each. Every executed input matches its declared full map. The independent thermal oracle solves energy/LMTD/log-gap equations with Brent roots; native thermal execution uses effectiveness/NTU and bisection. The oracle and all 44 absolute tolerance classes plus relative 1e-9 remained unchanged during repair. The complete summary and log are in results/verification_summary.json and results/verification.log.

Independent recalculation covers actual thermal states, aggregate returns, six terminal gaps, duty residuals, all engineering predicates and lifecycle outputs. Supplied inputs, common structural bindings, predicate definitions and algorithm iteration diagnostics are not independent physical evidence. This verifies the implemented conditional model, not source sustainment, fluid-property adequacy, constant-U applicability, procurement, valve design or plant operation.

Model-level validator limitations remain: 105 inherited literal warnings and 498 baseline plus 37 new pure-EXPOSE expression diagnostics. Stock generated execution and independent verification cover the affected paths; no all-level validator pass is claimed.

## 14. Review outcomes

| Lens | Verdict | Disposition |
|---|---|---|
| Original-source interpretation | PASS, reused | r2-source-review.md; adopted local requirement remains agent-originated. |
| Thermal design/MR-7/implementation | PASS, reused | WI-097 independent design and implementation reviews; selected equipment/control roles unchanged. Exact source copies ship under results/sources/. |
| Study framing/refinement/cost protocol | PASS, reused | r3-protocol-review.md; common search freedom, refinement and full-map retention followed. |
| Stable numerical remedy and repaired executable | PASS | WI-097 numerical-repair-review.md; unchanged physics/oracle/tolerance, high-precision and regression controls. |
| Integrated thermal comparison and economics | PASS | Independent probe checks all 1277 maps, 15 main preferred thermal states, 90 selections, 44 pairs, 328 allowance coordinates, 60 financial parents and native failure brackets. See results/reviews/r4-final-review.md and probe receipts. |

No additional source research or changed interpretation occurred in Round4. The continuing reviewer reuses its earlier accepted scopes and checks the new integrated evidence. A subsequent narrow delivery check covers only final seal hashes and exact replay. The reviewer-requested diagram caption now states explicit bypass return control; historical diagram bytes remain unchanged.

## 15. Findings

| Id | Kind | Finding | Disposition | Home |
|---|---|---|---|---|
| 20260927-exchanger-thermal-comparison-b#1 | model | Constant U, ideal mixing and mathematical bypass domain lack geometry/actuator qualification. | Declared conditional-model seam; thermal states verified within stated assumptions. | r3-study-contract.md |
| 20260927-exchanger-thermal-comparison-b#2 | model | Explicit revised exchanger prices are assumed budgets; smaller-area calibration flags remain and procurement is unqualified. | Retain explicit area/price selections and price sensitivities; no vendor cost claim. | r3-cost-boundary.md |
| 20260927-exchanger-thermal-comparison-b#3 | model | Supplied source and tritium price lack sustainment, breeding and supply resistance. | Retain supplied-source boundary and executed zero-price accounting endpoint. | r3-study-contract.md |
| 20260927-exchanger-thermal-comparison-b#4 | model | Incremental bypass/manifold/control/maintenance and hydraulic scope is unresolved beyond retained budgets. | Two-sided break-even allowances and coupled pressure-loss/pump scenarios; no free-hardware claim. | results/reporting/r3-data/break-even.csv |

Predecessor finding20260927-exchanger-thermal-comparison#1 is resolved by the reviewed stable numerical repair and complete exact-map verification; the original failed attempt is preserved. All current seams are declared limitations of this conditional result, not deferred prerequisites for its thermal consistency.

## 16. Snapshot

- **File:** `snapshot.json`
- **sha256:** `3b927ef10a9bf69549c5e807cd9b4fc6bca5d6c2da17665bc613fd09157584cc`
- **Schema version:** `1`

## 17. What this record does not contain

No complete piping layout, valve/actuator or exchanger-geometry qualification, measured U-versus-flow law, vendor quotations, source-sustainment or breeding/supply model, uncertainty distribution, global optimum proof or physical plant recommendation. The record includes reproducible conditional economics and explicit thermal acceptance. Earlier scan checkpoint/proposal versions and the original failed native tree remain in the separately committed predecessor; this record includes the full final scan archive, exact current proposals, predecessor references and archived old executable. Runtime symlink aliases and Python caches are omitted from the seal.
