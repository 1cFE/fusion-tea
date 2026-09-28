# Blocked study attempt — thermally consistent exchanger comparison

## 1. Study header

**Blocked attempt, 2026-09-27.** Executor: goal coordinator. Package exchanger_architecture_thermal_tea, Round3 executable cd16e8deb2f579e4cb1afcaf0fedbfc53498ba125783fbf8e17af14ffb4cbcc7. One architecture arm. The native execution prerequisite failed; this is not a completed or accepted comparison.

## 2. Intake

Owner intake is retained verbatim in owner-brief.md, owner-supplement-r2.md and owner-supplement-r3.md. Latest direction: “you are very intelligent. I trust your judgement. please make your best calls, document it, and proceed until you have strong study results.”

[AGENT] The conditional N-R returns, six local 30 K minima, explicit A/B offers and search/sensitivity choices are documented in r3-study-contract.md and r3-cost-boundary.md. Their agent provenance is preserved.

## 3. Objective and result

The intended objective is net electricity and conditional LCOE, with complete thermal/equipment acceptance. Qualified channels are `aries_integrated_plant__plant_ledger__evaluate__net_electric` and `aries_integrated_plant__lifecycle_price__evaluate__lcoe`. **No accepted ranking or LCOE result is delivered by this failed attempt.** 1275 maps completed; two finite cases raised a numerical bypass-solver exception. Full stored outputs remain under results/.

## 4. Constraint outcomes

Constraint counts apply only to completed cases; the two execution failures have no native verdict. These counts are evidence, not a preferred-case certification.

| constraint_id | source_local_identity | satisfied | violated |
|---|---|---:|---:|
| `aries_integrated_plant__compressor_capacity__capacity_ok__a45f9cf05e8aa7ab` | `capacity_ok` | 1258 | 17 |
| `aries_integrated_plant__divertor_capacity__capacity_ok__be7081920ad8e8ed` | `capacity_ok` | 1275 | 0 |
| `aries_integrated_plant__divertor_pump__capacity_ok__d6730c7060447f4c` | `capacity_ok` | 1275 | 0 |
| `aries_integrated_plant__fuel_capacity__capacity_ok__8eb5888bfe62cd64` | `capacity_ok` | 1275 | 0 |
| `aries_integrated_plant__fuel_inventory__capacity_ok__37f4667fbfb616d0` | `capacity_ok` | 1275 | 0 |
| `aries_integrated_plant__generator_capacity__capacity_ok__60b43f15d48ff161` | `capacity_ok` | 1275 | 0 |
| `aries_integrated_plant__he_capacity__capacity_ok__db2733d1d5baf3cf` | `capacity_ok` | 1275 | 0 |
| `aries_integrated_plant__he_pump__capacity_ok__fcee5ee009fe5180` | `capacity_ok` | 1275 | 0 |
| `aries_integrated_plant__heat_exchangers__divertor_cold_approach_ok__e70598993d392f74` | `divertor_cold_approach_ok` | 1261 | 14 |
| `aries_integrated_plant__heat_exchangers__divertor_control_ok__14c1c0f314a994fd` | `divertor_control_ok` | 1269 | 6 |
| `aries_integrated_plant__heat_exchangers__divertor_hot_approach_ok__5e95ef937d10cc33` | `divertor_hot_approach_ok` | 1197 | 78 |
| `aries_integrated_plant__heat_exchangers__divertor_hot_cap_ok__cd5f29bd8533c481` | `divertor_hot_cap_ok` | 1257 | 18 |
| `aries_integrated_plant__heat_exchangers__divertor_required_hot_ok__712add8be60bd1ae` | `divertor_required_hot_ok` | 1257 | 18 |
| `aries_integrated_plant__heat_exchangers__divertor_return_ok__f69c5310bdcc41d7` | `divertor_return_ok` | 865 | 410 |
| `aries_integrated_plant__heat_exchangers__divertor_state_ok__416e01681b16be81` | `divertor_state_ok` | 1275 | 0 |
| `aries_integrated_plant__heat_exchangers__he_cold_approach_ok__eab4f3486f0aa140` | `he_cold_approach_ok` | 1189 | 86 |
| `aries_integrated_plant__heat_exchangers__he_control_ok__f48454bb1d6f0e91` | `he_control_ok` | 1267 | 8 |
| `aries_integrated_plant__heat_exchangers__he_hot_approach_ok__7a2967e855192aeb` | `he_hot_approach_ok` | 930 | 345 |
| `aries_integrated_plant__heat_exchangers__he_hot_cap_ok__05ebd6dad2e4adc1` | `he_hot_cap_ok` | 1275 | 0 |
| `aries_integrated_plant__heat_exchangers__he_required_hot_ok__3371b55ff752c6e4` | `he_required_hot_ok` | 1275 | 0 |
| `aries_integrated_plant__heat_exchangers__he_return_ok__ae5f4d6db630fc8e` | `he_return_ok` | 930 | 345 |
| `aries_integrated_plant__heat_exchangers__he_state_ok__d5b9d58030392fe5` | `he_state_ok` | 1275 | 0 |
| `aries_integrated_plant__heat_exchangers__pbli_cold_approach_ok__667d6ca45c6e61de` | `pbli_cold_approach_ok` | 1229 | 46 |
| `aries_integrated_plant__heat_exchangers__pbli_control_ok__0c3b021e2e8589fb` | `pbli_control_ok` | 1274 | 1 |
| `aries_integrated_plant__heat_exchangers__pbli_hot_approach_ok__85855c74bdb13305` | `pbli_hot_approach_ok` | 932 | 343 |
| `aries_integrated_plant__heat_exchangers__pbli_hot_cap_ok__73a44108fcb5be1c` | `pbli_hot_cap_ok` | 1275 | 0 |
| `aries_integrated_plant__heat_exchangers__pbli_required_hot_ok__aa9057b8ce236e6b` | `pbli_required_hot_ok` | 1275 | 0 |
| `aries_integrated_plant__heat_exchangers__pbli_return_ok__100f6bf9ad61a22c` | `pbli_return_ok` | 724 | 551 |
| `aries_integrated_plant__heat_exchangers__pbli_state_ok__4664e5e1ddbb7ac5` | `pbli_state_ok` | 1275 | 0 |
| `aries_integrated_plant__pbli_capacity__capacity_ok__55a012a287da9395` | `capacity_ok` | 1275 | 0 |
| `aries_integrated_plant__pbli_pump__capacity_ok__79d116aa320dd4fb` | `capacity_ok` | 1275 | 0 |
| `aries_integrated_plant__plant_ledger__balances_ok__9af2e85b5e4e5535` | `balances_ok` | 1275 | 0 |
| `aries_integrated_plant__plant_ledger__heat_removal_ok__695378663bcd8d07` | `heat_removal_ok` | 661 | 614 |
| `aries_integrated_plant__rejection_capacity__capacity_ok__295420bc9fb25608` | `capacity_ok` | 1275 | 0 |
| `aries_integrated_plant__turbine_capacity__capacity_ok__089f9e8e61919ec1` | `capacity_ok` | 1275 | 0 |

## 5. Framing

| Axis | Proposed | Judged | Reason |
|---|---|---|---|
| source_mode | sensitivity | unchanged, provisional | Native completeness prerequisite failed; no reframing justified. |
| source_load | search | unchanged, provisional | Native completeness prerequisite failed; no reframing justified. |
| architecture | search | unchanged, provisional | Native completeness prerequisite failed; no reframing justified. |
| flow | search | unchanged, provisional | Native completeness prerequisite failed; no reframing justified. |
| split | search | unchanged, provisional | Native completeness prerequisite failed; no reframing justified. |
| control_mode | sensitivity | unchanged, provisional | Native completeness prerequisite failed; no reframing justified. |
| offer | sensitivity | unchanged, provisional | Native completeness prerequisite failed; no reframing justified. |
| approach | sensitivity | unchanged, provisional | Native completeness prerequisite failed; no reframing justified. |
| conductance | sensitivity | unchanged, provisional | Native completeness prerequisite failed; no reframing justified. |
| pressure_loss | sensitivity | unchanged, provisional | Native completeness prerequisite failed; no reframing justified. |
| pump_mode | sensitivity | unchanged, provisional | Native completeness prerequisite failed; no reframing justified. |
| pump_power | sensitivity | unchanged, provisional | Native completeness prerequisite failed; no reframing justified. |
| bypass_limit | sensitivity | unchanged, provisional | Native completeness prerequisite failed; no reframing justified. |
| return_convention | sensitivity | unchanged, provisional | Native completeness prerequisite failed; no reframing justified. |
| tritium_price | sensitivity | unchanged, provisional | Native completeness prerequisite failed; no reframing justified. |

## 6. Per-axis account

#### source_mode — feasible structure (search framing)

**Applies:** not applicable — sensitivity-framed.

#### source_mode — observed response (sensitivity framing)

**Applies:** yes; native cases and failure locations remain in results/cases.json. No uncertainty boundary or robustness claim is accepted.

#### source_load — feasible structure (search framing)

**Applies:** yes; independent sampled structure remains in oracle-selection.json and oracle-scan-summary.json, but no accepted native boundary result follows from this attempt.

#### source_load — observed response (sensitivity framing)

**Applies:** not applicable — search-framed.

#### architecture — feasible structure (search framing)

**Applies:** yes; independent sampled structure remains in oracle-selection.json and oracle-scan-summary.json, but no accepted native boundary result follows from this attempt.

#### architecture — observed response (sensitivity framing)

**Applies:** not applicable — search-framed.

#### flow — feasible structure (search framing)

**Applies:** yes; independent sampled structure remains in oracle-selection.json and oracle-scan-summary.json, but no accepted native boundary result follows from this attempt.

#### flow — observed response (sensitivity framing)

**Applies:** not applicable — search-framed.

#### split — feasible structure (search framing)

**Applies:** yes; independent sampled structure remains in oracle-selection.json and oracle-scan-summary.json, but no accepted native boundary result follows from this attempt.

#### split — observed response (sensitivity framing)

**Applies:** not applicable — search-framed.

#### control_mode — feasible structure (search framing)

**Applies:** not applicable — sensitivity-framed.

#### control_mode — observed response (sensitivity framing)

**Applies:** yes; native cases and failure locations remain in results/cases.json. No uncertainty boundary or robustness claim is accepted.

#### offer — feasible structure (search framing)

**Applies:** not applicable — sensitivity-framed.

#### offer — observed response (sensitivity framing)

**Applies:** yes; native cases and failure locations remain in results/cases.json. No uncertainty boundary or robustness claim is accepted.

#### approach — feasible structure (search framing)

**Applies:** not applicable — sensitivity-framed.

#### approach — observed response (sensitivity framing)

**Applies:** yes; native cases and failure locations remain in results/cases.json. No uncertainty boundary or robustness claim is accepted.

#### conductance — feasible structure (search framing)

**Applies:** not applicable — sensitivity-framed.

#### conductance — observed response (sensitivity framing)

**Applies:** yes; native cases and failure locations remain in results/cases.json. No uncertainty boundary or robustness claim is accepted.

#### pressure_loss — feasible structure (search framing)

**Applies:** not applicable — sensitivity-framed.

#### pressure_loss — observed response (sensitivity framing)

**Applies:** yes; native cases and failure locations remain in results/cases.json. No uncertainty boundary or robustness claim is accepted.

#### pump_mode — feasible structure (search framing)

**Applies:** not applicable — sensitivity-framed.

#### pump_mode — observed response (sensitivity framing)

**Applies:** yes; native cases and failure locations remain in results/cases.json. No uncertainty boundary or robustness claim is accepted.

#### pump_power — feasible structure (search framing)

**Applies:** not applicable — sensitivity-framed.

#### pump_power — observed response (sensitivity framing)

**Applies:** yes; native cases and failure locations remain in results/cases.json. No uncertainty boundary or robustness claim is accepted.

#### bypass_limit — feasible structure (search framing)

**Applies:** not applicable — sensitivity-framed.

#### bypass_limit — observed response (sensitivity framing)

**Applies:** yes; native cases and failure locations remain in results/cases.json. No uncertainty boundary or robustness claim is accepted.

#### return_convention — feasible structure (search framing)

**Applies:** not applicable — sensitivity-framed.

#### return_convention — observed response (sensitivity framing)

**Applies:** yes; native cases and failure locations remain in results/cases.json. No uncertainty boundary or robustness claim is accepted.

#### tritium_price — feasible structure (search framing)

**Applies:** not applicable — sensitivity-framed.

#### tritium_price — observed response (sensitivity framing)

**Applies:** yes; native cases and failure locations remain in results/cases.json. No uncertainty boundary or robustness claim is accepted.

## 7. Axis groups

| Axis | Entry key | Provenance |
|---|---|---|
| source_mode | `aries_integrated_plant__source__producer_mode` | fan_out |
| source_load | `aries_integrated_plant__source__reference_fusion_mw` | fan_out |
| architecture | `aries_integrated_plant__heat_exchangers__network_mode` | fan_out |
| flow | `aries_integrated_plant__cycle__selected_flow` | fan_out |
| split | `aries_integrated_plant__heat_exchangers__pbli_split_fraction` | fan_out |
| control_mode | `aries_integrated_plant__heat_exchangers__control_mode` | fan_out |
| offer | `aries_integrated_plant__he_hx__selected_area` | fan_out |
| offer | `aries_integrated_plant__he_hx__price_factor` | tie |
| offer | `aries_integrated_plant__pbli_hx__selected_area` | tie |
| offer | `aries_integrated_plant__pbli_hx__price_factor` | tie |
| offer | `aries_integrated_plant__divertor_hx__selected_area` | tie |
| offer | `aries_integrated_plant__divertor_hx__price_factor` | tie |
| approach | `aries_integrated_plant__heat_exchangers__he_hot_approach` | fan_out |
| approach | `aries_integrated_plant__heat_exchangers__he_cold_approach` | tie |
| approach | `aries_integrated_plant__heat_exchangers__pbli_hot_approach` | tie |
| approach | `aries_integrated_plant__heat_exchangers__pbli_cold_approach` | tie |
| approach | `aries_integrated_plant__heat_exchangers__divertor_hot_approach` | tie |
| approach | `aries_integrated_plant__heat_exchangers__divertor_cold_approach` | tie |
| conductance | `aries_integrated_plant__he_hx__assumed_u` | fan_out |
| conductance | `aries_integrated_plant__pbli_hx__assumed_u` | tie |
| conductance | `aries_integrated_plant__divertor_hx__assumed_u` | tie |
| pressure_loss | `aries_integrated_plant__pressure_loss__loss_fraction` | fan_out |
| pump_mode | `aries_integrated_plant__he_pump__pump_mode` | fan_out |
| pump_mode | `aries_integrated_plant__pbli_pump__pump_mode` | tie |
| pump_mode | `aries_integrated_plant__divertor_pump__pump_mode` | tie |
| pump_power | `aries_integrated_plant__he_pump__fixed_power` | fan_out |
| pump_power | `aries_integrated_plant__pbli_pump__fixed_power` | tie |
| pump_power | `aries_integrated_plant__divertor_pump__fixed_power` | tie |
| bypass_limit | `aries_integrated_plant__heat_exchangers__he_max_bypass` | fan_out |
| bypass_limit | `aries_integrated_plant__heat_exchangers__pbli_max_bypass` | tie |
| bypass_limit | `aries_integrated_plant__heat_exchangers__divertor_max_bypass` | tie |
| return_convention | `aries_integrated_plant__heat_exchangers__he_required_return` | fan_out |
| return_convention | `aries_integrated_plant__heat_exchangers__pbli_required_return` | tie |
| return_convention | `aries_integrated_plant__heat_exchangers__divertor_required_return` | tie |
| tritium_price | `aries_integrated_plant__fuel_inventory__tritium_price` | fan_out |

Declared ties coordinate scenarios, not physical equality. Exact interpretations remain in axes.json and manifest.json.

## 8. Indicators and rulings

All fifteen groups have `constraints_reachable`; no group reports `no_constraint_response`. This is only graph reachability. Monotonicity, cross-key physical identity and intra-module dependencies are not derivable. The agent still treats price assumptions as unresisted procurement/fuel sensitivities, authorized by delegated owner judgment. Missing procurement, source sustainment and control/hydraulic qualification remain explicit in the contract.

## 9. Preflight results

All study preflight gates pass in preparation/preflight.json. The model integration passed all ten gates, copied in results/integration_return_used.json. Those prerequisites did not guarantee complete execution over the refined candidate set.

## 10. Execution route and why

Stock strict loader, PreparedEvaluator, StudyDefinition, PreparedListStrategy, StudyRunner and StudyStore. Coordinated full input maps require the direct-API definition. Glue ledger: none. results/export-proof.json preserves exact full-map matching and unchanged native export evidence. The exporter correctly rejects the incomplete execution.

## 11. Study definition and window provenance

The engineered window was selected from an independent scan of 91,234 maps, retaining all 697 known development passing seeds and refining every observed component. Two matched catalogues share flow freedom; the network adds a supplied split. Final selected resolutions meet 0.2 MW / 0.1 USD2004 per MWh stability targets, with final split spacing as fine as 0.00025 and final flow probes 0.00625 kg/s. No sampled passing outer edge remains. The 1 kg/s negative series check still found no offer-B pass at 1650 MW. These are retained scouting results, not global proofs or accepted native architecture outcomes. The exact scan/selection/proposals and exclusions are retained, with lossless compression described below.

## 12. Cross-fingerprint correlation and what it means

Single executable fingerprint; cross-fingerprint correlation is not applicable inside this attempt. The next round must explicitly correlate the same 1277 complete input maps against a corrected executable; it cannot overwrite this store or silently retry this pin.

## 13. Verification

results/verification-attempt.json reports numeric PASS for every completed row: 1275 of 1277 total, 435 independent channels and 35 predicates each, unchanged 1e-9 relative and declared absolute classes. The two failed rows are not sampled by the stock verifier; this is not an all-point verification pass. Independently recomputed failed states are finite and satisfy the unchanged engineering predicates. Failure checks and later repair review belong to WI-097; the next study must verify all 1277 executions.

## 14. Review outcomes

Source, design, preparation and implementation reviews passed within their declared scopes. r3-failure-review.md approves retaining this attempt and using Round4 for unchanged-meaning repair. A numerical remedy requires its own independent review. No ranking is approved by the partial verification receipt.

## 15. Findings

| Finding id | Kind | Finding | Disposition | Home |
|---|---|---|---|---|
| 20260927-exchanger-thermal-comparison#1 | model | Two finite supplied maps fail native bypass convergence; complete study execution is unmet. | model fix: Round4 T-007 reviewed stable evaluation and exact-map replay, pending | work/active/WI-097_exchanger-thermal-requirements |

## 16. Snapshot

`attempt-snapshot.json` hashes the blocked attempt, archived original executable, original source bytes, retained native store and completed-case verification. A successful-study snapshot is deliberately absent because execution failed. It is a failure-preservation record, not a completed-study seal. lossless-compression.json maps compressed files to exact original byte hashes; decompressing restores every original scan/proposal/checkpoint byte.

## 17. What this record does not contain

No accepted preferred architecture, complete native execution/verification, completed-study snapshot, vendor price qualification, actuator rating, piping design, source sustainment, breeding/fuel-supply model or plant recommendation. Those omissions are explicit; the preserved two numerical failures cannot be treated as engineering rejections.
