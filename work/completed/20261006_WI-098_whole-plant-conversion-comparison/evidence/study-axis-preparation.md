# Study axis preparation

[AGENT] Prepared 2026-09-27 from the final native package and coordinator-owned candidate generators. This deposit checks attribute identity, input coverage and graph reachability. It does not authorize execution or establish observed physical response.

## Result

- All 637 public contract entries match the complete evaluated baseline map used to enumerate candidates.
- All 85 candidate attributes touched by the six generators are declared. Five additional public attributes are declined and traced. All 90 groups are nonempty, contain one actual `design_attribute` entry with `fan_out` provenance, and have no duplicate keys or invented physical ties.
- Every qualified attribute occurs in the authored assembly. Every declared entry has native pipeline consumers. Downstream bindings reuse the same public key; no separate consumer keys were mistaken for extra axes.
- Stock indicators passed all 90 groups, with no warnings. Every group has possible constraint paths; none reports `no_constraint_response`. These are graph results, not measured constraint responses.
- The actual baseline is `whole-baseline2500` in `development-final/native/cases.json`, at executable `6915694e74919ebb764445dfc7f0782eda85a9de29fa44c4b55ffa415c1eb30f`. Its steam offer is 10 circuits, four pumps per circuit, 225 kg/s selected pump flow, with shared availability 0.80. The gas catalog's 14-circuit/250 kg/s steam offer is a separate candidate configuration.

The generator coverage check enumerated chosen input maps only. It did not execute the model or calculate physical/economic outputs. Counts below are per supplied anchor, not a final study total.

| Generator | Rows inspected |
|---|---:|
| `gas_catalog` | 375 |
| `steam_catalog` | 24 |
| `sensitivity_catalog` | 14 |
| `adverse_controller_catalog` | 2 |
| `common_scenarios` | 44 |
| `joint_efficiency_scenarios` | 2 |

## Method and replay

Read the run-study skill, canonical runbook, `modeling_project/STUDY_POLICY.md` and predecessor axis/annex formats. Enumerate `gas_catalog`, `steam_catalog`, `sensitivity_catalog`, `adverse_controller_catalog`, `common_scenarios` and `joint_efficiency_scenarios` using the actual baseline's complete effective inputs. Union every `chosen`/`choices` key, including choices whose selected value happens to equal the baseline. Check every key against `contracts/model_contract.json`; locate the corresponding qualified part attribute in the authored assembly; inspect its input references in `pipelines/pipeline.yaml`. The declared groups contain the complete generated key set for each selected attribute.

The stock validation command was:

```bash
.codex-test/run python scripts/study/indicators.py --package exploration/whole_plant_conversion/whole_plant_conversion_tea --manifest exploration/whole_plant_conversion/studies/manifest.json --groups exploration/whole_plant_conversion/studies/axes.json --out /tmp/wi098-indicators.json
```

It exited 0. The temporary complete report is available to the coordinator for deposit into the study record; the command is the reproducible route if that temporary file is unavailable. The table below retains the per-group result and exact source location. The coordinator owns the manifest, study record, permanent indicator deposit, preflight and execution decision.

Monotonicity, same-quantity identity across differing key names and intra-module operand dependence are not derivable. `constraints_reachable` means a possible module path only. In particular, price and service assumptions retain sensitivity framing despite paths to numerical-domain and economic predicates.

## Attribute census

All keys have prefix `whole_plant_conversion__plant__`; the qualified attribute is that key with `__` replaced by `::`. The suffix column gives the complete remaining key, not an alias. Source lines refer to `models/designs/whole_plant_conversion/plant.sysml`. “Proposed” means present in the candidate generators; it is not an owner ruling or an executed point. Each row uses `fan_out`, with one emitted key and zero declared ties.

| Input suffix | Source line | Candidate functions / disposition | Direct consumers | Reachable constraints |
|---|---:|---|---:|---:|
| `auxiliary_rejection_account__price_factor` | 3219 | common_scenarios | 1 | 8 |
| `blanket_account__price_factor` | 3112 | common_scenarios | 1 | 8 |
| `compressor_1__efficiency` | 85 | joint_efficiency_scenarios, sensitivity_catalog | 1 | 42 |
| `compressor_1__selected_ratio` | 84 | gas_catalog | 1 | 42 |
| `compressor_2__efficiency` | 118 | joint_efficiency_scenarios, sensitivity_catalog | 1 | 38 |
| `compressor_2__selected_ratio` | 117 | gas_catalog | 1 | 38 |
| `compressor_3__efficiency` | 151 | joint_efficiency_scenarios, sensitivity_catalog | 1 | 34 |
| `compressor_3__selected_ratio` | 150 | gas_catalog | 1 | 34 |
| `compressor_equipment__price_factor` | 462 | sensitivity_catalog | 1 | 11 |
| `conversion_services__price_factor` | 557 | gas_catalog, sensitivity_catalog | 1 | 11 |
| `cryogenic_demand__extra_cold_W` | 2824 | common_scenarios | 1 | 17 |
| `cryogenic_demand__q_nuc_W_m3` | 2823 | common_scenarios | 1 | 17 |
| `cryoplant_account__price_factor` | 3210 | common_scenarios | 1 | 8 |
| `cycle__selected_flow` | 74 | gas_catalog | 11 | 42 |
| `cycle__turbine_efficiency` | 79 | joint_efficiency_scenarios, sensitivity_catalog | 2 | 34 |
| `digital_twin_account__price_factor` | 3300 | common_scenarios | 1 | 8 |
| `divertor_account__price_factor` | 3103 | common_scenarios | 1 | 8 |
| `facilities_account__price_factor` | 3077 | common_scenarios | 1 | 8 |
| `finance__availability` | 2699 | common_scenarios | 8 | 24 |
| `finance__commissioning_rate` | 2707 | common_scenarios | 2 | 8 |
| `finance__contingency_rate` | 2701 | common_scenarios | 2 | 8 |
| `finance__freight_rate` | 2703 | common_scenarios | 2 | 8 |
| `finance__general_spares_rate` | 2704 | common_scenarios | 2 | 8 |
| `finance__indirect_rate` | 2702 | common_scenarios | 2 | 8 |
| `finance__insurance_rate` | 2706 | common_scenarios | 2 | 8 |
| `finance__rate` | 2697 | common_scenarios | 4 | 21 |
| `finance__tax_rate` | 2705 | common_scenarios | 2 | 8 |
| `fuel_accounts__tbr` | 2859 | common_scenarios | 3 | 11 |
| `fuel_accounts__tritium_price` | 2870 | common_scenarios | 1 | 11 |
| `fuel_processing_account__price_factor` | 3237 | common_scenarios | 1 | 8 |
| `gas_boundary__bypass_flow_rating` | 1075 | adverse_controller_catalog | 1 | 9 |
| `gas_ledger__annual_service_fraction` | 2577 | sensitivity_catalog | 1 | 11 |
| `gas_ledger__capital9` | 2565 | sensitivity_catalog | 1 | 11 |
| `gas_ledger__controller_capital` | 2567 | adverse_controller_catalog, sensitivity_catalog | 2 | 11 |
| `gas_ledger__replacement_fraction` | 2578 | sensitivity_catalog | 1 | 11 |
| `generator_equipment__price_factor` | 500 | sensitivity_catalog | 1 | 11 |
| `he_duty_equipment__price_factor` | 538 | sensitivity_catalog | 1 | 11 |
| `he_hx__price_factor` | 179 | sensitivity_catalog | 1 | 11 |
| `heat_rejection_equipment__price_factor` | 519 | sensitivity_catalog | 1 | 11 |
| `heating_account__price_factor` | 3094 | common_scenarios | 1 | 8 |
| `installation_account__price_factor` | 3166 | common_scenarios | 1 | 8 |
| `land_account__price_factor` | 3068 | common_scenarios | 1 | 8 |
| `magnet_account__price_factor` | 3085 | common_scenarios | 1 | 8 |
| `miscellaneous_account__price_factor` | 3273 | common_scenarios | 1 | 8 |
| `other_reactor_account__price_factor` | 3246 | common_scenarios | 1 | 8 |
| `owner_account__price_factor` | 3291 | common_scenarios | 1 | 8 |
| `pbl_initial_account__price_factor` | 3282 | common_scenarios | 1 | 8 |
| `power_supplies_account__price_factor` | 3148 | common_scenarios | 1 | 8 |
| `primary_circulators_account__price_factor` | 3175 | common_scenarios | 1 | 8 |
| `primary_helium_account__price_factor` | 3202 | common_scenarios | 1 | 8 |
| `primary_loop__eta_drive` | 37 | common_scenarios | 1 | 100 |
| `primary_loop__n_loops` | 31 | declined | 2 | 100 |
| `primary_pipes_account__price_factor` | 3184 | common_scenarios | 1 | 8 |
| `primary_spares_account__price_factor` | 3193 | common_scenarios | 1 | 8 |
| `reactor_controls_account__price_factor` | 3255 | common_scenarios | 1 | 8 |
| `recuperator_hardware__ua` | 572 | gas_catalog | 1 | 34 |
| `remote_handling_account__price_factor` | 3157 | common_scenarios | 1 | 8 |
| `shared_electrical_account__price_factor` | 3264 | common_scenarios | 1 | 8 |
| `shield_account__price_factor` | 3121 | common_scenarios | 1 | 8 |
| `source_basis__heating_source_efficiency` | 2714 | common_scenarios | 1 | 24 |
| `source_basis__q_source_MW` | 2711 | gas_catalog | 2 | 108 |
| `source_installation_allowance_account__price_factor` | 3309 | common_scenarios | 1 | 8 |
| `source_installation_allowance_account__quote_USD2025` | 3308 | common_scenarios | 1 | 8 |
| `steam_boundary__bypass_flow_rating` | 979 | adverse_controller_catalog | 1 | 44 |
| `steam_cycle__condenser_temperature_C` | 1178 | declined | 2 | 33 |
| `steam_cycle__eta_hp` | 1179 | joint_efficiency_scenarios, sensitivity_catalog | 1 | 32 |
| `steam_cycle__eta_lp` | 1180 | joint_efficiency_scenarios, sensitivity_catalog | 1 | 32 |
| `steam_cycle__reheat_temperature_C` | 1177 | declined | 2 | 33 |
| `steam_cycle__steam_temperature_C` | 1176 | declined | 2 | 33 |
| `steam_ledger__annual_service_fraction` | 2463 | sensitivity_catalog | 1 | 10 |
| `steam_ledger__capital3` | 2450 | sensitivity_catalog | 1 | 10 |
| `steam_ledger__capital4` | 2451 | sensitivity_catalog | 1 | 10 |
| `steam_ledger__controller_capital` | 2459 | adverse_controller_catalog, sensitivity_catalog | 2 | 10 |
| `steam_ledger__replacement_fraction` | 2464 | sensitivity_catalog | 1 | 10 |
| `steam_operating__import_price` | 3520 | common_scenarios | 2 | 14 |
| `steam_operating__residual_MW` | 3516 | common_scenarios | 2 | 14 |
| `steam_transport__costscale` | 610 | sensitivity_catalog | 1 | 59 |
| `steam_transport__n_loops` | 594 | gas_catalog, steam_catalog | 2 | 59 |
| `steam_transport__salt_pumps_per_circuit` | 583 | gas_catalog, steam_catalog | 1 | 59 |
| `steam_transport__secondary_head` | 599 | declined | 1 | 59 |
| `steam_transport__selected_salt_design_flow_kg_s` | 586 | gas_catalog, steam_catalog | 1 | 59 |
| `steam_whole__magnet_life` | 3565 | common_scenarios | 2 | 6 |
| `steam_whole__routine_fraction` | 3563 | common_scenarios | 2 | 6 |
| `structure_account__price_factor` | 3130 | common_scenarios | 1 | 8 |
| `turbine_equipment__price_factor` | 481 | sensitivity_catalog | 1 | 11 |
| `vessel_account__price_factor` | 3139 | common_scenarios | 1 | 8 |
| `waste_account__price_factor` | 3228 | common_scenarios | 1 | 8 |
| `water_ic1__ua` | 1600 | gas_catalog | 1 | 15 |
| `water_ic2__ua` | 1654 | gas_catalog | 1 | 15 |
| `water_pre__ua` | 1708 | gas_catalog | 1 | 15 |

The three steam temperature inputs, salt-pump head and primary path count are the five declined public axes. Their reasons are in `axes.json` and `ANNEX.md`. Reactor geometry and magnet excitation are immutable capture inputs outside this package's public contract; fusion power is a calculated output. Their declined broader search is recorded in the annex without fabricating keys or pretending an absent input can be traced by stock indicators.

## Input identities

The following files were hashed before and after preparation; all were unchanged during the mapping and validation. A later change to either candidate generator requires repeating coverage checks before execution.

| File | SHA256 |
|---|---|
| `exploration/whole_plant_conversion/studies/proposals.py` | `fb4ba469cf08648eb9e27694eff6e6726306f2908008666b7a2a0d6159445971` |
| `exploration/whole_plant_conversion/studies/scenarios.py` | `fe7bfc8ef4bbb52fc75785158e1db1bd01569cfa85e6904ab05e1ea88db0fd43` |
| `models/designs/whole_plant_conversion/plant.sysml` | `5572bcef980cc12d9001857f4bd266fa5e8872be98cd4d3606ca845d705e7078` |
| `exploration/whole_plant_conversion/whole_plant_conversion_tea/contracts/model_contract.json` | `2020f070504a8628726f6365cad480b011e182262c3d6297bf0f7a924f282fd8` |
| `exploration/whole_plant_conversion/whole_plant_conversion_tea/pipelines/pipeline.yaml` | `953fa13ff436bd9c4dd40f895f14b871ebdfb4f797f1e60cd4bd08e9b78045ac` |
| `exploration/whole_plant_conversion/studies/axes.json` | `cc2f53a5b61fcaaa8dc8178718b56711d7f32880f45fcc3b75e2e342d7c0dd6b` |

## Handoff

Prepared `exploration/whole_plant_conversion/studies/axes.json` and `ANNEX.md`. The annex records the actual baseline, stock route, four oracle API exports, finite engineered catalog, no validity mask, no calculation glue, immutable hardware, declined geometry/fusion search and conditional source limits. It directs cost-category traceability to the accepted configuration rather than incorrect descriptive CAS labels. The native package and model sources were not changed.

Updated the native report and plan with `evidence/conversion-controls/comparison.json` and `evidence/independent-verification/controls-summary.json`: all 498 controls pass, inherited 872-channel/84-predicate comparison has exactly zero numerical difference, and independent whole-plant verification covers 1192 channels and 125 predicates per case. Independent integration and main-study conclusions remain separate gates.
