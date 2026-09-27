# Whole-plant steam versus helium Brayton conversion study

**BLOCKED AT NUMERICAL VERIFICATION.** Retained native execution and draft presentation; no released economic conclusion.

## 1. Study header

- **Study id:** `20260927-design-study-whole-plant-conversion`
- **Package:** whole_plant_conversion
- **Date executed:** 2026-09-27
- **Executor:** Codex coordinator /root
- **Mode:** execute
- **Arms:** arm-whole-plant-offers

## 2. Intake

The complete owner-provided goal and scope are retained verbatim in [owner-brief.md](owner-brief.md), including its explicitly agent-proposed starting strategy.

> For one consistently specified reactor concept, how does selecting the modeled steam or helium Brayton conversion system change net electricity exported, whole-plant LCOE and the assumptions under which each choice is preferable?

[AGENT] This execution uses the reviewed supplied-source inventory, a finite equipment catalog and engineered sensitivity scenarios. The owner authorized conditional modeling assumptions and required complete plant power/cost scope. The chosen ranges are not empirical uncertainty bounds. [Configuration](supporting/configuration.md), [comparison contract](supporting/comparison-contract.md) and [pre-execution framing](pre-execution-framing.md) retain that authority and the applicable reporting bands.

## 3. Objective and result

The objective channels are `whole_plant_conversion__plant__steam_whole__evaluate__lcoe_USD2025_MWh` and the corresponding `gas_whole` channel. They are native whole-plant lifecycle costs per exported MWh in real 2025 USD. The native ledger includes startup fuel, operating imports, source and conversion service, replacements and terminal events. Annual net grid delivery after standby imports is also reported and must remain positive.

| Source MW | Branch | Net export MW | Initial capital billion USD2025 | Financed capital billion USD2025 | LCOE USD2025/MWh | Native case |
|---:|---|---:|---:|---:|---:|---|
| 2500 | gas | 285.883396 | 16.962956 | 20.618579 | 875.312561 | `nominal::gas-q2500-m2000-r1.5-ua25-25-25` |
| 2500 | steam | 663.969189 | 18.406924 | 22.373732 | 408.163805 | `nominal::gas-q2500-m2000-r1.5-ua25-25-25` |
| 2800 | gas | 204.460262 | 16.962956 | 20.618579 | 1230.283623 | `nominal::gas-q2800-m1750-r1.8-ua25-25-25` |
| 2800 | steam | 746.644668 | 18.721604 | 22.756227 | 370.701372 | `nominal::gas-q2800-m1750-r1.8-ua25-25-25` |
| 3000 | gas | — | — | — | unsupported | No passing offer |
| 3000 | steam | — | — | — | unsupported | No passing offer |

These are provisional extracted minima over admitted native catalog members. Verification failed; they are retained evidence, not released conclusions. The full paired scenario results, exact signed differences, strict ordering and ±5 USD2025/MWh reporting classifications are in [matched-pairs.csv](results/presentation/matched-pairs.csv). The power reporting band is ±5 MW. Neither band is a physical constraint or statistical interval. [Study conclusion](study-conclusion.md) explains the preference, combined-assumption reversal and native threshold confirmations.

## 4. Constraint outcomes

Every executing identity is listed below. Counts cover all stored points, including the alternative branch in a paired computational assembly. Ranking requires its own branch and all shared predicates; it does not require an unused alternative to pass. The [complete constraint summary](results/constraint-summary.json) links every failed identity to its exact native case. Source, nuclear-transport and global-construction qualification flags are separate, deliberately zero conditions on the scientific interpretation; passing equipment checks does not qualify them.

| constraint_id | source_local_identity | Branch | Satisfied | Violated | Other |
|---|---|---|---:|---:|---:|
| `whole_plant_conversion__plant__compressor_capacity__capacity_ok__add1463eda59a898` | `capacity_ok` | gas | 2436 | 60 | 0 |
| `whole_plant_conversion__plant__cryogenic_demand__cold_margin_w_ok__7dcadae371ddbe6d` | `cold_margin_w_ok` | shared | 2444 | 52 | 0 |
| `whole_plant_conversion__plant__cryogenic_demand__domain_supported_ok__e5d086f806f615c2` | `domain_supported_ok` | shared | 2496 | 0 | 0 |
| `whole_plant_conversion__plant__cryogenic_demand__intercept_margin_w_ok__c8cb8040676afc38` | `intercept_margin_w_ok` | shared | 2496 | 0 | 0 |
| `whole_plant_conversion__plant__fuel_accounts__domain_supported_ok__94a59fec46208105` | `domain_supported_ok` | shared | 2496 | 0 | 0 |
| `whole_plant_conversion__plant__fuel_accounts__processing_margin_ok__860e81215fb2b47f` | `processing_margin_ok` | shared | 2496 | 0 | 0 |
| `whole_plant_conversion__plant__fuel_accounts__stock_margin_ok__84c447972f804892` | `stock_margin_ok` | shared | 2496 | 0 | 0 |
| `whole_plant_conversion__plant__gas_actual_approach__cold_gap_ok__7e84344c8ebe1f06` | `cold_gap_ok` | gas | 2496 | 0 | 0 |
| `whole_plant_conversion__plant__gas_actual_approach__hot_gap_ok__5e9b6647fc4988da` | `hot_gap_ok` | gas | 2496 | 0 | 0 |
| `whole_plant_conversion__plant__gas_boundary__added_dp_margin_ok__cb2dbaa41d101ab2` | `added_dp_margin_ok` | gas | 2496 | 0 | 0 |
| `whole_plant_conversion__plant__gas_boundary__bypass_flow_margin_ok__44eb1a31c631c4dc` | `bypass_flow_margin_ok` | gas | 2494 | 2 | 0 |
| `whole_plant_conversion__plant__gas_boundary__bypass_fraction_margin_ok__c17576ed428ad624` | `bypass_fraction_margin_ok` | gas | 2496 | 0 | 0 |
| `whole_plant_conversion__plant__gas_boundary__controller_capacity_ok_ok__b340a8d5e92452b2` | `controller_capacity_ok_ok` | gas | 2494 | 2 | 0 |
| `whole_plant_conversion__plant__gas_boundary__exchanger_flow_margin_ok__396e8f7ff4b4cd78` | `exchanger_flow_margin_ok` | gas | 2496 | 0 | 0 |
| `whole_plant_conversion__plant__gas_boundary__pressure_margin_ok__57cdec1e34d967ce` | `pressure_margin_ok` | gas | 2496 | 0 | 0 |
| `whole_plant_conversion__plant__gas_boundary__source_adequate_ok__665dcdd55c247bde` | `source_adequate_ok` | gas | 2016 | 480 | 0 |
| `whole_plant_conversion__plant__gas_boundary__temperature_margin_ok__c3287e1bc91fd77f` | `temperature_margin_ok` | gas | 2496 | 0 | 0 |
| `whole_plant_conversion__plant__gas_boundary__total_flow_margin_ok__b1cac73884dab807` | `total_flow_margin_ok` | gas | 2496 | 0 | 0 |
| `whole_plant_conversion__plant__gas_ledger__balance__d86d965fca008ca2` | `balance` | gas | 1754 | 742 | 0 |
| `whole_plant_conversion__plant__gas_ledger__net_positive__41d28cae11b1dbd6` | `net_positive` | gas | 2469 | 27 | 0 |
| `whole_plant_conversion__plant__gas_loss_duty_capacity__capacity_requirement__d56ff09d5df0acbc` | `capacity_requirement` | gas | 2496 | 0 | 0 |
| `whole_plant_conversion__plant__gas_loss_electric_capacity__capacity_requirement__ba3fad80f3006552` | `capacity_requirement` | gas | 2496 | 0 | 0 |
| `whole_plant_conversion__plant__gas_loss_flow_capacity__capacity_requirement__111ef92c45f0ac07` | `capacity_requirement` | gas | 2496 | 0 | 0 |
| `whole_plant_conversion__plant__gas_loss_water__cooling_approach_ok_required__8223dadecc4964f5` | `cooling_approach_ok_required` | gas | 2496 | 0 | 0 |
| `whole_plant_conversion__plant__gas_operating__annual_net_grid_mwh_ok__1220a0098a3e5f94` | `annual_net_grid_mwh_ok` | gas | 2361 | 135 | 0 |
| `whole_plant_conversion__plant__gas_operating__auxiliary_margin_mw_ok__15f9aaa632609eef` | `auxiliary_margin_mw_ok` | gas | 2496 | 0 | 0 |
| `whole_plant_conversion__plant__gas_operating__domain_supported_ok__e50b966764ec28c8` | `domain_supported_ok` | gas | 2496 | 0 | 0 |
| `whole_plant_conversion__plant__gas_operating__net_export_mw_ok__58d3569ea9297329` | `net_export_mw_ok` | gas | 2362 | 134 | 0 |
| `whole_plant_conversion__plant__gas_overheads__domain_supported_ok__37ebb2bb65f0bc13` | `domain_supported_ok` | gas | 2496 | 0 | 0 |
| `whole_plant_conversion__plant__gas_whole__domain_supported_ok__bab43aa2eeeee822` | `domain_supported_ok` | gas | 2496 | 0 | 0 |
| `whole_plant_conversion__plant__gas_whole__economic_defined_ok__5a084f6c1d99295a` | `economic_defined_ok` | gas | 2361 | 135 | 0 |
| `whole_plant_conversion__plant__gas_whole__outage_margin_ok__25e59eb98c7fca29` | `outage_margin_ok` | gas | 2471 | 25 | 0 |
| `whole_plant_conversion__plant__generator_capacity__capacity_ok__13f54fade9ec1f3f` | `capacity_ok` | gas | 2496 | 0 | 0 |
| `whole_plant_conversion__plant__he_capacity__capacity_ok__86fcc614bddbfd3c` | `capacity_ok` | gas | 2496 | 0 | 0 |
| `whole_plant_conversion__plant__primary_offer__electric_margin_mw_ok__fbb614dc306d8b9a` | `electric_margin_mw_ok` | shared | 2496 | 0 | 0 |
| `whole_plant_conversion__plant__primary_offer__flow_margin_kg_s_ok__8bc805379860ec62` | `flow_margin_kg_s_ok` | shared | 2496 | 0 | 0 |
| `whole_plant_conversion__plant__primary_offer__inventory_supported_ok__ef44640d09918a5a` | `inventory_supported_ok` | shared | 2496 | 0 | 0 |
| `whole_plant_conversion__plant__primary_offer__pressure_margin_pa_ok__76becfa8174fdcbd` | `pressure_margin_pa_ok` | shared | 2347 | 149 | 0 |
| `whole_plant_conversion__plant__recuperator_duty_capacity__capacity_requirement__751eb0b036d86809` | `capacity_requirement` | gas | 2496 | 0 | 0 |
| `whole_plant_conversion__plant__rejection_capacity__capacity_requirement__af7714dda178b8f0` | `capacity_requirement` | gas | 2496 | 0 | 0 |
| `whole_plant_conversion__plant__salt_electric_capacity__capacity_requirement__98e5361921299b30` | `capacity_requirement` | steam | 2390 | 106 | 0 |
| `whole_plant_conversion__plant__salt_fill_capacity__capacity_requirement__5ccc7cbd0819713b` | `capacity_requirement` | steam | 2496 | 0 | 0 |
| `whole_plant_conversion__plant__salt_flow_capacity__capacity_requirement__dd3ff75af1205c2a` | `capacity_requirement` | steam | 2390 | 106 | 0 |
| `whole_plant_conversion__plant__salt_shaft_capacity__capacity_requirement__b2367d578fc2f1ec` | `capacity_requirement` | steam | 2390 | 106 | 0 |
| `whole_plant_conversion__plant__source_basis__divertor_margin_ok__77e857f8e82a3790` | `divertor_margin_ok` | shared | 2347 | 149 | 0 |
| `whole_plant_conversion__plant__source_basis__domain_supported_ok__a7d99ff729662eb5` | `domain_supported_ok` | shared | 2496 | 0 | 0 |
| `whole_plant_conversion__plant__source_basis__fusion_envelope_margin_ok__118a84d76a05a76c` | `fusion_envelope_margin_ok` | shared | 2496 | 0 | 0 |
| `whole_plant_conversion__plant__source_basis__heating_coupled_margin_ok__26addbd9a09afc2d` | `heating_coupled_margin_ok` | shared | 2496 | 0 | 0 |
| `whole_plant_conversion__plant__source_basis__heating_wall_margin_ok__7038060d9c96b5f8` | `heating_wall_margin_ok` | shared | 2471 | 25 | 0 |
| `whole_plant_conversion__plant__source_checks__flow_ok__04e751f9ce97000b` | `flow_ok` | shared | 2496 | 0 | 0 |
| `whole_plant_conversion__plant__source_checks__pressure_ok__e9cb76bbd569aa90` | `pressure_ok` | shared | 2496 | 0 | 0 |
| `whole_plant_conversion__plant__steam_actual_approach__cold_gap_ok__f8487fc350489be6` | `cold_gap_ok` | steam | 2496 | 0 | 0 |
| `whole_plant_conversion__plant__steam_actual_approach__hot_gap_ok__8e52cd2d280b334c` | `hot_gap_ok` | steam | 2496 | 0 | 0 |
| `whole_plant_conversion__plant__steam_boundary__added_dp_margin_ok__36cb21eac5ff1b89` | `added_dp_margin_ok` | steam | 2496 | 0 | 0 |
| `whole_plant_conversion__plant__steam_boundary__bypass_flow_margin_ok__d79c6541885ab47e` | `bypass_flow_margin_ok` | steam | 2496 | 0 | 0 |
| `whole_plant_conversion__plant__steam_boundary__bypass_fraction_margin_ok__e91d0e0192e4dffd` | `bypass_fraction_margin_ok` | steam | 2496 | 0 | 0 |
| `whole_plant_conversion__plant__steam_boundary__controller_capacity_ok_ok__f143197b782aea8e` | `controller_capacity_ok_ok` | steam | 2496 | 0 | 0 |
| `whole_plant_conversion__plant__steam_boundary__exchanger_flow_margin_ok__6737739807166519` | `exchanger_flow_margin_ok` | steam | 2496 | 0 | 0 |
| `whole_plant_conversion__plant__steam_boundary__pressure_margin_ok__a08fe8a322365c4f` | `pressure_margin_ok` | steam | 2496 | 0 | 0 |
| `whole_plant_conversion__plant__steam_boundary__source_adequate_ok__d29edbaf0da24311` | `source_adequate_ok` | steam | 2459 | 37 | 0 |
| `whole_plant_conversion__plant__steam_boundary__temperature_margin_ok__5fbec511bdeb34e1` | `temperature_margin_ok` | steam | 2496 | 0 | 0 |
| `whole_plant_conversion__plant__steam_boundary__total_flow_margin_ok__d3ffa1c793b06886` | `total_flow_margin_ok` | steam | 2496 | 0 | 0 |
| `whole_plant_conversion__plant__steam_condensate_electric_capacity__capacity_requirement__b4edc0272db0ccfd` | `capacity_requirement` | steam | 2459 | 37 | 0 |
| `whole_plant_conversion__plant__steam_condensate_flow_capacity__capacity_requirement__9f500cb802e73b3a` | `capacity_requirement` | steam | 2459 | 37 | 0 |
| `whole_plant_conversion__plant__steam_condensate_pressure_capacity__capacity_requirement__81d8ff0ab723193e` | `capacity_requirement` | steam | 2459 | 37 | 0 |
| `whole_plant_conversion__plant__steam_condenser_capacity__capacity_requirement__21565c442e22d191` | `capacity_requirement` | steam | 2459 | 37 | 0 |
| `whole_plant_conversion__plant__steam_conditions__supported_required__f55a3b19d079007e` | `supported_required` | steam | 2459 | 37 | 0 |
| `whole_plant_conversion__plant__steam_cycle__main_admission_ok_required__9e7307c18ac5420b` | `main_admission_ok_required` | steam | 2496 | 0 | 0 |
| `whole_plant_conversion__plant__steam_cycle__main_ua_available_required__281cb99c36b65283` | `main_ua_available_required` | steam | 2496 | 0 | 0 |
| `whole_plant_conversion__plant__steam_cycle__reheat_admission_ok_required__46e7006e3a4fafe2` | `reheat_admission_ok_required` | steam | 2496 | 0 | 0 |
| `whole_plant_conversion__plant__steam_cycle__reheat_ua_available_required__34a9b54f6c90ff27` | `reheat_ua_available_required` | steam | 2496 | 0 | 0 |
| `whole_plant_conversion__plant__steam_feed_electric_capacity__capacity_requirement__b9644c9b953bc0ac` | `capacity_requirement` | steam | 2459 | 37 | 0 |
| `whole_plant_conversion__plant__steam_feed_flow_capacity__capacity_requirement__5d9d76d0749190a1` | `capacity_requirement` | steam | 2459 | 37 | 0 |
| `whole_plant_conversion__plant__steam_feed_pressure_capacity__capacity_requirement__5e891902fcc36704` | `capacity_requirement` | steam | 2459 | 37 | 0 |
| `whole_plant_conversion__plant__steam_gross_capacity__capacity_requirement__9cde1cfefe9e4edb` | `capacity_requirement` | steam | 2459 | 37 | 0 |
| `whole_plant_conversion__plant__steam_hp_flow_capacity__capacity_requirement__5cc6b8ef933d65f8` | `capacity_requirement` | steam | 2459 | 37 | 0 |
| `whole_plant_conversion__plant__steam_hp_shaft_capacity__capacity_requirement__a3fe202eb6d52755` | `capacity_requirement` | steam | 2459 | 37 | 0 |
| `whole_plant_conversion__plant__steam_ledger__balance__e1489f8b74e321d3` | `balance` | steam | 2496 | 0 | 0 |
| `whole_plant_conversion__plant__steam_ledger__net_positive__02f91f11a35b318a` | `net_positive` | steam | 2496 | 0 | 0 |
| `whole_plant_conversion__plant__steam_lp_flow_capacity__capacity_requirement__a3fe0741c9ecff1c` | `capacity_requirement` | steam | 2459 | 37 | 0 |
| `whole_plant_conversion__plant__steam_lp_shaft_capacity__capacity_requirement__5eb83cc804af4b97` | `capacity_requirement` | steam | 2459 | 37 | 0 |
| `whole_plant_conversion__plant__steam_main_ua_capacity__capacity_requirement__7df245597c1c6a96` | `capacity_requirement` | steam | 2459 | 37 | 0 |
| `whole_plant_conversion__plant__steam_operating__annual_net_grid_mwh_ok__e95e0d4ecf3512d0` | `annual_net_grid_mwh_ok` | steam | 2496 | 0 | 0 |
| `whole_plant_conversion__plant__steam_operating__auxiliary_margin_mw_ok__95e4e54a80aa3248` | `auxiliary_margin_mw_ok` | steam | 2496 | 0 | 0 |
| `whole_plant_conversion__plant__steam_operating__domain_supported_ok__8292960083cc99b1` | `domain_supported_ok` | steam | 2496 | 0 | 0 |
| `whole_plant_conversion__plant__steam_operating__net_export_mw_ok__f2f015c4f9fa63ae` | `net_export_mw_ok` | steam | 2496 | 0 | 0 |
| `whole_plant_conversion__plant__steam_overheads__domain_supported_ok__79a050b3100a6489` | `domain_supported_ok` | steam | 2496 | 0 | 0 |
| `whole_plant_conversion__plant__steam_reheat_ua_capacity__capacity_requirement__14e2137308151f37` | `capacity_requirement` | steam | 2459 | 37 | 0 |
| `whole_plant_conversion__plant__steam_rejection_capacity__capacity_requirement__550b287c6e69de07` | `capacity_requirement` | steam | 2496 | 0 | 0 |
| `whole_plant_conversion__plant__steam_transport__design_motor_base_ok_required__f884c33dd8381ddf` | `design_motor_base_ok_required` | steam | 2496 | 0 | 0 |
| `whole_plant_conversion__plant__steam_transport__design_motor_factor_ok_required__388250a54e30378f` | `design_motor_factor_ok_required` | steam | 2496 | 0 | 0 |
| `whole_plant_conversion__plant__steam_transport__design_pump_size_ok_required__0aad92e0e5d98e78` | `design_pump_size_ok_required` | steam | 2496 | 0 | 0 |
| `whole_plant_conversion__plant__steam_transport__design_pump_type_ok_required__9883fd28033f69dd` | `design_pump_type_ok_required` | steam | 2496 | 0 | 0 |
| `whole_plant_conversion__plant__steam_transport__ihx_capacity_ok_required__98f15d4abb4b4604` | `ihx_capacity_ok_required` | steam | 2459 | 37 | 0 |
| `whole_plant_conversion__plant__steam_transport__motor_base_ok_required__b639a4539ef58c7f` | `motor_base_ok_required` | steam | 2496 | 0 | 0 |
| `whole_plant_conversion__plant__steam_transport__motor_factor_ok_required__c7270c7cda57bab6` | `motor_factor_ok_required` | steam | 2444 | 52 | 0 |
| `whole_plant_conversion__plant__steam_transport__pump_size_ok_required__b7783d5e6b21b1ec` | `pump_size_ok_required` | steam | 2496 | 0 | 0 |
| `whole_plant_conversion__plant__steam_transport__pump_type_ok_required__ddc3748fb76b74c1` | `pump_type_ok_required` | steam | 2422 | 74 | 0 |
| `whole_plant_conversion__plant__steam_transport__salt_flow_regime_ok_required__4214cdcb871abc4e` | `salt_flow_regime_ok_required` | steam | 2496 | 0 | 0 |
| `whole_plant_conversion__plant__steam_transport__salt_head_ok_required__12b011d2b9b50c5e` | `salt_head_ok_required` | steam | 2496 | 0 | 0 |
| `whole_plant_conversion__plant__steam_water__cooling_approach_ok_required__8456fcd9f50ebe3a` | `cooling_approach_ok_required` | steam | 2496 | 0 | 0 |
| `whole_plant_conversion__plant__steam_water_electric_capacity__capacity_requirement__e3f37a33f8f86544` | `capacity_requirement` | steam | 2496 | 0 | 0 |
| `whole_plant_conversion__plant__steam_water_flow_capacity__capacity_requirement__682b9c0979ad7556` | `capacity_requirement` | steam | 2496 | 0 | 0 |
| `whole_plant_conversion__plant__steam_whole__domain_supported_ok__d85812a4b8cd9e3f` | `domain_supported_ok` | steam | 2496 | 0 | 0 |
| `whole_plant_conversion__plant__steam_whole__economic_defined_ok__aec3d165702acb63` | `economic_defined_ok` | steam | 2496 | 0 | 0 |
| `whole_plant_conversion__plant__steam_whole__outage_margin_ok__90418a10014fb429` | `outage_margin_ok` | steam | 2471 | 25 | 0 |
| `whole_plant_conversion__plant__supplied_core__current_margin_ok__c67cdc1d2fb0a885` | `current_margin_ok` | shared | 2496 | 0 | 0 |
| `whole_plant_conversion__plant__supplied_core__field_margin_t_ok__4c34d4933dff04fb` | `field_margin_t_ok` | shared | 2496 | 0 | 0 |
| `whole_plant_conversion__plant__supplied_core__fit_margin_ok__d3fcebf466168c53` | `fit_margin_ok` | shared | 2496 | 0 | 0 |
| `whole_plant_conversion__plant__supplied_core__identity_supported_ok__121f94d9fa90b835` | `identity_supported_ok` | shared | 2496 | 0 | 0 |
| `whole_plant_conversion__plant__supplied_core__strain_margin_ok__2d8a80d5407aa7bd` | `strain_margin_ok` | shared | 2496 | 0 | 0 |
| `whole_plant_conversion__plant__supplied_core__stress_margin_pa_ok__edd9f45610c1547b` | `stress_margin_pa_ok` | shared | 2496 | 0 | 0 |
| `whole_plant_conversion__plant__turbine_capacity__capacity_ok__ee860596098e7f44` | `capacity_ok` | gas | 2496 | 0 | 0 |
| `whole_plant_conversion__plant__water_ic1__duty_margin_ok__dfd546f8f5ee868f` | `duty_margin_ok` | gas | 2496 | 0 | 0 |
| `whole_plant_conversion__plant__water_ic1__evaluation_defined_ok__1371e750cffff108` | `evaluation_defined_ok` | gas | 2121 | 375 | 0 |
| `whole_plant_conversion__plant__water_ic1__flow_margin_ok__1dd1c3a1e5784553` | `flow_margin_ok` | gas | 2488 | 8 | 0 |
| `whole_plant_conversion__plant__water_ic1__power_margin_ok__5b880ab5fc02b1dc` | `power_margin_ok` | gas | 2488 | 8 | 0 |
| `whole_plant_conversion__plant__water_ic2__duty_margin_ok__143f9ca6200e6779` | `duty_margin_ok` | gas | 2496 | 0 | 0 |
| `whole_plant_conversion__plant__water_ic2__evaluation_defined_ok__b931519f56a159d1` | `evaluation_defined_ok` | gas | 2121 | 375 | 0 |
| `whole_plant_conversion__plant__water_ic2__flow_margin_ok__6696de4f3ee21d56` | `flow_margin_ok` | gas | 2488 | 8 | 0 |
| `whole_plant_conversion__plant__water_ic2__power_margin_ok__4251efdd4ccb0c52` | `power_margin_ok` | gas | 2488 | 8 | 0 |
| `whole_plant_conversion__plant__water_pre__duty_margin_ok__43a051525223b723` | `duty_margin_ok` | gas | 2496 | 0 | 0 |
| `whole_plant_conversion__plant__water_pre__evaluation_defined_ok__84c4b3b2eb329ee0` | `evaluation_defined_ok` | gas | 1839 | 657 | 0 |
| `whole_plant_conversion__plant__water_pre__flow_margin_ok__e81a241fb624b075` | `flow_margin_ok` | gas | 2484 | 12 | 0 |
| `whole_plant_conversion__plant__water_pre__power_margin_ok__88cf3aa259145f02` | `power_margin_ok` | gas | 2487 | 9 | 0 |

## 5. Framing

The proposed and judged framing coincide. Search means selecting among the finite declared equipment/operating offers, not locating a continuous or global optimum. Sensitivity means observing conditional scenario responses. Coordinated scenario changes do not establish a separate marginal effect of each participating attribute.

| Axis | Proposed | Judged | Changed? | Execution |
|---|---|---|---|---|
| `auxiliary_rejection_account_price_factor` | sensitivity | sensitivity | no | executed |
| `blanket_account_price_factor` | sensitivity | sensitivity | no | executed |
| `compressor_1_efficiency` | sensitivity | sensitivity | no | executed |
| `compressor_1_selected_ratio` | search | search | no | executed |
| `compressor_2_efficiency` | sensitivity | sensitivity | no | executed |
| `compressor_2_selected_ratio` | search | search | no | executed |
| `compressor_3_efficiency` | sensitivity | sensitivity | no | executed |
| `compressor_3_selected_ratio` | search | search | no | executed |
| `compressor_equipment_price_factor` | sensitivity | sensitivity | no | executed |
| `conversion_services_price_factor` | sensitivity | sensitivity | no | executed |
| `cryogenic_demand_extra_cold_W` | sensitivity | sensitivity | no | executed |
| `cryogenic_demand_q_nuc_W_m3` | sensitivity | sensitivity | no | executed |
| `cryoplant_account_price_factor` | sensitivity | sensitivity | no | executed |
| `cycle_selected_flow` | search | search | no | executed |
| `cycle_turbine_efficiency` | sensitivity | sensitivity | no | executed |
| `digital_twin_account_price_factor` | sensitivity | sensitivity | no | executed |
| `divertor_account_price_factor` | sensitivity | sensitivity | no | executed |
| `facilities_account_price_factor` | sensitivity | sensitivity | no | executed |
| `finance_availability` | sensitivity | sensitivity | no | executed |
| `finance_commissioning_rate` | sensitivity | sensitivity | no | executed |
| `finance_contingency_rate` | sensitivity | sensitivity | no | executed |
| `finance_freight_rate` | sensitivity | sensitivity | no | executed |
| `finance_general_spares_rate` | sensitivity | sensitivity | no | executed |
| `finance_indirect_rate` | sensitivity | sensitivity | no | executed |
| `finance_insurance_rate` | sensitivity | sensitivity | no | executed |
| `finance_rate` | sensitivity | sensitivity | no | executed |
| `finance_tax_rate` | sensitivity | sensitivity | no | executed |
| `fuel_accounts_tbr` | sensitivity | sensitivity | no | executed |
| `fuel_accounts_tritium_price` | sensitivity | sensitivity | no | executed |
| `fuel_processing_account_price_factor` | sensitivity | sensitivity | no | executed |
| `gas_boundary_bypass_flow_rating` | sensitivity | sensitivity | no | executed |
| `gas_ledger_annual_service_fraction` | sensitivity | sensitivity | no | executed |
| `gas_ledger_capital9` | sensitivity | sensitivity | no | executed |
| `gas_ledger_controller_capital` | sensitivity | sensitivity | no | executed |
| `gas_ledger_replacement_fraction` | sensitivity | sensitivity | no | executed |
| `generator_equipment_price_factor` | sensitivity | sensitivity | no | executed |
| `he_duty_equipment_price_factor` | sensitivity | sensitivity | no | executed |
| `he_hx_price_factor` | sensitivity | sensitivity | no | executed |
| `heat_rejection_equipment_price_factor` | sensitivity | sensitivity | no | executed |
| `heating_account_price_factor` | sensitivity | sensitivity | no | executed |
| `installation_account_price_factor` | sensitivity | sensitivity | no | executed |
| `land_account_price_factor` | sensitivity | sensitivity | no | executed |
| `magnet_account_price_factor` | sensitivity | sensitivity | no | executed |
| `miscellaneous_account_price_factor` | sensitivity | sensitivity | no | executed |
| `other_reactor_account_price_factor` | sensitivity | sensitivity | no | executed |
| `owner_account_price_factor` | sensitivity | sensitivity | no | executed |
| `pbl_initial_account_price_factor` | sensitivity | sensitivity | no | executed |
| `power_supplies_account_price_factor` | sensitivity | sensitivity | no | executed |
| `primary_circulators_account_price_factor` | sensitivity | sensitivity | no | executed |
| `primary_helium_account_price_factor` | sensitivity | sensitivity | no | executed |
| `primary_loop_eta_drive` | sensitivity | sensitivity | no | executed |
| `primary_loop_n_loops` | sensitivity | sensitivity | no | declined with reason in axes.json |
| `primary_pipes_account_price_factor` | sensitivity | sensitivity | no | executed |
| `primary_spares_account_price_factor` | sensitivity | sensitivity | no | executed |
| `reactor_controls_account_price_factor` | sensitivity | sensitivity | no | executed |
| `recuperator_hardware_ua` | search | search | no | executed |
| `remote_handling_account_price_factor` | sensitivity | sensitivity | no | executed |
| `shared_electrical_account_price_factor` | sensitivity | sensitivity | no | executed |
| `shield_account_price_factor` | sensitivity | sensitivity | no | executed |
| `source_basis_heating_source_efficiency` | sensitivity | sensitivity | no | executed |
| `source_basis_q_source_MW` | sensitivity | sensitivity | no | executed |
| `source_installation_allowance_account_price_factor` | sensitivity | sensitivity | no | executed |
| `source_installation_allowance_account_quote_USD2025` | sensitivity | sensitivity | no | executed |
| `steam_boundary_bypass_flow_rating` | sensitivity | sensitivity | no | executed |
| `steam_cycle_condenser_temperature_C` | sensitivity | sensitivity | no | declined with reason in axes.json |
| `steam_cycle_eta_hp` | sensitivity | sensitivity | no | executed |
| `steam_cycle_eta_lp` | sensitivity | sensitivity | no | executed |
| `steam_cycle_reheat_temperature_C` | sensitivity | sensitivity | no | declined with reason in axes.json |
| `steam_cycle_steam_temperature_C` | sensitivity | sensitivity | no | declined with reason in axes.json |
| `steam_ledger_annual_service_fraction` | sensitivity | sensitivity | no | executed |
| `steam_ledger_capital3` | sensitivity | sensitivity | no | executed |
| `steam_ledger_capital4` | sensitivity | sensitivity | no | executed |
| `steam_ledger_controller_capital` | sensitivity | sensitivity | no | executed |
| `steam_ledger_replacement_fraction` | sensitivity | sensitivity | no | executed |
| `steam_operating_import_price` | sensitivity | sensitivity | no | executed |
| `steam_operating_residual_MW` | sensitivity | sensitivity | no | executed |
| `steam_transport_costscale` | sensitivity | sensitivity | no | executed |
| `steam_transport_n_loops` | search | search | no | executed |
| `steam_transport_salt_pumps_per_circuit` | search | search | no | executed |
| `steam_transport_secondary_head` | sensitivity | sensitivity | no | declined with reason in axes.json |
| `steam_transport_selected_salt_design_flow_kg_s` | search | search | no | executed |
| `steam_whole_magnet_life` | sensitivity | sensitivity | no | executed |
| `steam_whole_routine_fraction` | sensitivity | sensitivity | no | executed |
| `structure_account_price_factor` | sensitivity | sensitivity | no | executed |
| `turbine_equipment_price_factor` | sensitivity | sensitivity | no | executed |
| `vessel_account_price_factor` | sensitivity | sensitivity | no | executed |
| `waste_account_price_factor` | sensitivity | sensitivity | no | executed |
| `water_ic1_ua` | search | search | no | executed |
| `water_ic2_ua` | search | search | no | executed |
| `water_pre_ua` | search | search | no | executed |

## 6. Per-axis account

The [axis assessment](results/axis-assessment.json) retains exact observed values for every declared key. The [native scenario rankings](results/presentation/scenario-summary.json), [case ledger](results/presentation/attempted-case-ledger.csv) and [window edge rereading](window.json) carry the response, failed locations and finite feasible structure. An edge marked not_caught remains open; no continuous feasible limit is inferred. The separately declared cryogenic brackets are held-equipment boundary diagnostics, not a neutronics uncertainty interval.

#### `auxiliary_rejection_account_price_factor` — feasible structure (search framing)

**Applies:** not applicable — sensitivity-framed

The study does not make a search claim for this attribute.

#### `auxiliary_rejection_account_price_factor` — observed response (sensitivity framing)

**Applies:** yes

The native scenario table and case ledger record this attribute’s coordinated changes, response and any violated checks. The axis assessment lists its actual values. No independent marginal response or general feasible-region boundary is claimed.

#### `blanket_account_price_factor` — feasible structure (search framing)

**Applies:** not applicable — sensitivity-framed

The study does not make a search claim for this attribute.

#### `blanket_account_price_factor` — observed response (sensitivity framing)

**Applies:** yes

The native scenario table and case ledger record this attribute’s coordinated changes, response and any violated checks. The axis assessment lists its actual values. No independent marginal response or general feasible-region boundary is claimed.

#### `compressor_1_efficiency` — feasible structure (search framing)

**Applies:** not applicable — sensitivity-framed

The study does not make a search claim for this attribute.

#### `compressor_1_efficiency` — observed response (sensitivity framing)

**Applies:** yes

The native scenario table and case ledger record this attribute’s coordinated changes, response and any violated checks. The axis assessment lists its actual values. No independent marginal response or general feasible-region boundary is claimed.

#### `compressor_1_selected_ratio` — feasible structure (search framing)

**Applies:** yes

The finite admitted offers and failed native cases are retained in the linked case ledger. Observed choices are in the axis assessment; relevant edge checks are in window.json. No global optimum is claimed.

#### `compressor_1_selected_ratio` — observed response (sensitivity framing)

**Applies:** not applicable — search-framed

No separate sensitivity claim is made for this search-framed attribute; its coordinated scenario context remains recorded.

#### `compressor_2_efficiency` — feasible structure (search framing)

**Applies:** not applicable — sensitivity-framed

The study does not make a search claim for this attribute.

#### `compressor_2_efficiency` — observed response (sensitivity framing)

**Applies:** yes

The native scenario table and case ledger record this attribute’s coordinated changes, response and any violated checks. The axis assessment lists its actual values. No independent marginal response or general feasible-region boundary is claimed.

#### `compressor_2_selected_ratio` — feasible structure (search framing)

**Applies:** yes

The finite admitted offers and failed native cases are retained in the linked case ledger. Observed choices are in the axis assessment; relevant edge checks are in window.json. No global optimum is claimed.

#### `compressor_2_selected_ratio` — observed response (sensitivity framing)

**Applies:** not applicable — search-framed

No separate sensitivity claim is made for this search-framed attribute; its coordinated scenario context remains recorded.

#### `compressor_3_efficiency` — feasible structure (search framing)

**Applies:** not applicable — sensitivity-framed

The study does not make a search claim for this attribute.

#### `compressor_3_efficiency` — observed response (sensitivity framing)

**Applies:** yes

The native scenario table and case ledger record this attribute’s coordinated changes, response and any violated checks. The axis assessment lists its actual values. No independent marginal response or general feasible-region boundary is claimed.

#### `compressor_3_selected_ratio` — feasible structure (search framing)

**Applies:** yes

The finite admitted offers and failed native cases are retained in the linked case ledger. Observed choices are in the axis assessment; relevant edge checks are in window.json. No global optimum is claimed.

#### `compressor_3_selected_ratio` — observed response (sensitivity framing)

**Applies:** not applicable — search-framed

No separate sensitivity claim is made for this search-framed attribute; its coordinated scenario context remains recorded.

#### `compressor_equipment_price_factor` — feasible structure (search framing)

**Applies:** not applicable — sensitivity-framed

The study does not make a search claim for this attribute.

#### `compressor_equipment_price_factor` — observed response (sensitivity framing)

**Applies:** yes

The native scenario table and case ledger record this attribute’s coordinated changes, response and any violated checks. The axis assessment lists its actual values. No independent marginal response or general feasible-region boundary is claimed.

#### `conversion_services_price_factor` — feasible structure (search framing)

**Applies:** not applicable — sensitivity-framed

The study does not make a search claim for this attribute.

#### `conversion_services_price_factor` — observed response (sensitivity framing)

**Applies:** yes

The native scenario table and case ledger record this attribute’s coordinated changes, response and any violated checks. The axis assessment lists its actual values. No independent marginal response or general feasible-region boundary is claimed.

#### `cryogenic_demand_extra_cold_W` — feasible structure (search framing)

**Applies:** not applicable — sensitivity-framed

The study does not make a search claim for this attribute.

#### `cryogenic_demand_extra_cold_W` — observed response (sensitivity framing)

**Applies:** yes

The native scenario table and case ledger record this attribute’s coordinated changes, response and any violated checks. The axis assessment lists its actual values. No independent marginal response or general feasible-region boundary is claimed.

#### `cryogenic_demand_q_nuc_W_m3` — feasible structure (search framing)

**Applies:** not applicable — sensitivity-framed

The study does not make a search claim for this attribute.

#### `cryogenic_demand_q_nuc_W_m3` — observed response (sensitivity framing)

**Applies:** yes

The native scenario table and case ledger record this attribute’s coordinated changes, response and any violated checks. The axis assessment lists its actual values. No independent marginal response or general feasible-region boundary is claimed.

#### `cryoplant_account_price_factor` — feasible structure (search framing)

**Applies:** not applicable — sensitivity-framed

The study does not make a search claim for this attribute.

#### `cryoplant_account_price_factor` — observed response (sensitivity framing)

**Applies:** yes

The native scenario table and case ledger record this attribute’s coordinated changes, response and any violated checks. The axis assessment lists its actual values. No independent marginal response or general feasible-region boundary is claimed.

#### `cycle_selected_flow` — feasible structure (search framing)

**Applies:** yes

The finite admitted offers and failed native cases are retained in the linked case ledger. Observed choices are in the axis assessment; relevant edge checks are in window.json. No global optimum is claimed.

#### `cycle_selected_flow` — observed response (sensitivity framing)

**Applies:** not applicable — search-framed

No separate sensitivity claim is made for this search-framed attribute; its coordinated scenario context remains recorded.

#### `cycle_turbine_efficiency` — feasible structure (search framing)

**Applies:** not applicable — sensitivity-framed

The study does not make a search claim for this attribute.

#### `cycle_turbine_efficiency` — observed response (sensitivity framing)

**Applies:** yes

The native scenario table and case ledger record this attribute’s coordinated changes, response and any violated checks. The axis assessment lists its actual values. No independent marginal response or general feasible-region boundary is claimed.

#### `digital_twin_account_price_factor` — feasible structure (search framing)

**Applies:** not applicable — sensitivity-framed

The study does not make a search claim for this attribute.

#### `digital_twin_account_price_factor` — observed response (sensitivity framing)

**Applies:** yes

The native scenario table and case ledger record this attribute’s coordinated changes, response and any violated checks. The axis assessment lists its actual values. No independent marginal response or general feasible-region boundary is claimed.

#### `divertor_account_price_factor` — feasible structure (search framing)

**Applies:** not applicable — sensitivity-framed

The study does not make a search claim for this attribute.

#### `divertor_account_price_factor` — observed response (sensitivity framing)

**Applies:** yes

The native scenario table and case ledger record this attribute’s coordinated changes, response and any violated checks. The axis assessment lists its actual values. No independent marginal response or general feasible-region boundary is claimed.

#### `facilities_account_price_factor` — feasible structure (search framing)

**Applies:** not applicable — sensitivity-framed

The study does not make a search claim for this attribute.

#### `facilities_account_price_factor` — observed response (sensitivity framing)

**Applies:** yes

The native scenario table and case ledger record this attribute’s coordinated changes, response and any violated checks. The axis assessment lists its actual values. No independent marginal response or general feasible-region boundary is claimed.

#### `finance_availability` — feasible structure (search framing)

**Applies:** not applicable — sensitivity-framed

The study does not make a search claim for this attribute.

#### `finance_availability` — observed response (sensitivity framing)

**Applies:** yes

The native scenario table and case ledger record this attribute’s coordinated changes, response and any violated checks. The axis assessment lists its actual values. No independent marginal response or general feasible-region boundary is claimed.

#### `finance_commissioning_rate` — feasible structure (search framing)

**Applies:** not applicable — sensitivity-framed

The study does not make a search claim for this attribute.

#### `finance_commissioning_rate` — observed response (sensitivity framing)

**Applies:** yes

The native scenario table and case ledger record this attribute’s coordinated changes, response and any violated checks. The axis assessment lists its actual values. No independent marginal response or general feasible-region boundary is claimed.

#### `finance_contingency_rate` — feasible structure (search framing)

**Applies:** not applicable — sensitivity-framed

The study does not make a search claim for this attribute.

#### `finance_contingency_rate` — observed response (sensitivity framing)

**Applies:** yes

The native scenario table and case ledger record this attribute’s coordinated changes, response and any violated checks. The axis assessment lists its actual values. No independent marginal response or general feasible-region boundary is claimed.

#### `finance_freight_rate` — feasible structure (search framing)

**Applies:** not applicable — sensitivity-framed

The study does not make a search claim for this attribute.

#### `finance_freight_rate` — observed response (sensitivity framing)

**Applies:** yes

The native scenario table and case ledger record this attribute’s coordinated changes, response and any violated checks. The axis assessment lists its actual values. No independent marginal response or general feasible-region boundary is claimed.

#### `finance_general_spares_rate` — feasible structure (search framing)

**Applies:** not applicable — sensitivity-framed

The study does not make a search claim for this attribute.

#### `finance_general_spares_rate` — observed response (sensitivity framing)

**Applies:** yes

The native scenario table and case ledger record this attribute’s coordinated changes, response and any violated checks. The axis assessment lists its actual values. No independent marginal response or general feasible-region boundary is claimed.

#### `finance_indirect_rate` — feasible structure (search framing)

**Applies:** not applicable — sensitivity-framed

The study does not make a search claim for this attribute.

#### `finance_indirect_rate` — observed response (sensitivity framing)

**Applies:** yes

The native scenario table and case ledger record this attribute’s coordinated changes, response and any violated checks. The axis assessment lists its actual values. No independent marginal response or general feasible-region boundary is claimed.

#### `finance_insurance_rate` — feasible structure (search framing)

**Applies:** not applicable — sensitivity-framed

The study does not make a search claim for this attribute.

#### `finance_insurance_rate` — observed response (sensitivity framing)

**Applies:** yes

The native scenario table and case ledger record this attribute’s coordinated changes, response and any violated checks. The axis assessment lists its actual values. No independent marginal response or general feasible-region boundary is claimed.

#### `finance_rate` — feasible structure (search framing)

**Applies:** not applicable — sensitivity-framed

The study does not make a search claim for this attribute.

#### `finance_rate` — observed response (sensitivity framing)

**Applies:** yes

The native scenario table and case ledger record this attribute’s coordinated changes, response and any violated checks. The axis assessment lists its actual values. No independent marginal response or general feasible-region boundary is claimed.

#### `finance_tax_rate` — feasible structure (search framing)

**Applies:** not applicable — sensitivity-framed

The study does not make a search claim for this attribute.

#### `finance_tax_rate` — observed response (sensitivity framing)

**Applies:** yes

The native scenario table and case ledger record this attribute’s coordinated changes, response and any violated checks. The axis assessment lists its actual values. No independent marginal response or general feasible-region boundary is claimed.

#### `fuel_accounts_tbr` — feasible structure (search framing)

**Applies:** not applicable — sensitivity-framed

The study does not make a search claim for this attribute.

#### `fuel_accounts_tbr` — observed response (sensitivity framing)

**Applies:** yes

The native scenario table and case ledger record this attribute’s coordinated changes, response and any violated checks. The axis assessment lists its actual values. No independent marginal response or general feasible-region boundary is claimed.

#### `fuel_accounts_tritium_price` — feasible structure (search framing)

**Applies:** not applicable — sensitivity-framed

The study does not make a search claim for this attribute.

#### `fuel_accounts_tritium_price` — observed response (sensitivity framing)

**Applies:** yes

The native scenario table and case ledger record this attribute’s coordinated changes, response and any violated checks. The axis assessment lists its actual values. No independent marginal response or general feasible-region boundary is claimed.

#### `fuel_processing_account_price_factor` — feasible structure (search framing)

**Applies:** not applicable — sensitivity-framed

The study does not make a search claim for this attribute.

#### `fuel_processing_account_price_factor` — observed response (sensitivity framing)

**Applies:** yes

The native scenario table and case ledger record this attribute’s coordinated changes, response and any violated checks. The axis assessment lists its actual values. No independent marginal response or general feasible-region boundary is claimed.

#### `gas_boundary_bypass_flow_rating` — feasible structure (search framing)

**Applies:** not applicable — sensitivity-framed

The study does not make a search claim for this attribute.

#### `gas_boundary_bypass_flow_rating` — observed response (sensitivity framing)

**Applies:** yes

The native scenario table and case ledger record this attribute’s coordinated changes, response and any violated checks. The axis assessment lists its actual values. No independent marginal response or general feasible-region boundary is claimed.

#### `gas_ledger_annual_service_fraction` — feasible structure (search framing)

**Applies:** not applicable — sensitivity-framed

The study does not make a search claim for this attribute.

#### `gas_ledger_annual_service_fraction` — observed response (sensitivity framing)

**Applies:** yes

The native scenario table and case ledger record this attribute’s coordinated changes, response and any violated checks. The axis assessment lists its actual values. No independent marginal response or general feasible-region boundary is claimed.

#### `gas_ledger_capital9` — feasible structure (search framing)

**Applies:** not applicable — sensitivity-framed

The study does not make a search claim for this attribute.

#### `gas_ledger_capital9` — observed response (sensitivity framing)

**Applies:** yes

The native scenario table and case ledger record this attribute’s coordinated changes, response and any violated checks. The axis assessment lists its actual values. No independent marginal response or general feasible-region boundary is claimed.

#### `gas_ledger_controller_capital` — feasible structure (search framing)

**Applies:** not applicable — sensitivity-framed

The study does not make a search claim for this attribute.

#### `gas_ledger_controller_capital` — observed response (sensitivity framing)

**Applies:** yes

The native scenario table and case ledger record this attribute’s coordinated changes, response and any violated checks. The axis assessment lists its actual values. No independent marginal response or general feasible-region boundary is claimed.

#### `gas_ledger_replacement_fraction` — feasible structure (search framing)

**Applies:** not applicable — sensitivity-framed

The study does not make a search claim for this attribute.

#### `gas_ledger_replacement_fraction` — observed response (sensitivity framing)

**Applies:** yes

The native scenario table and case ledger record this attribute’s coordinated changes, response and any violated checks. The axis assessment lists its actual values. No independent marginal response or general feasible-region boundary is claimed.

#### `generator_equipment_price_factor` — feasible structure (search framing)

**Applies:** not applicable — sensitivity-framed

The study does not make a search claim for this attribute.

#### `generator_equipment_price_factor` — observed response (sensitivity framing)

**Applies:** yes

The native scenario table and case ledger record this attribute’s coordinated changes, response and any violated checks. The axis assessment lists its actual values. No independent marginal response or general feasible-region boundary is claimed.

#### `he_duty_equipment_price_factor` — feasible structure (search framing)

**Applies:** not applicable — sensitivity-framed

The study does not make a search claim for this attribute.

#### `he_duty_equipment_price_factor` — observed response (sensitivity framing)

**Applies:** yes

The native scenario table and case ledger record this attribute’s coordinated changes, response and any violated checks. The axis assessment lists its actual values. No independent marginal response or general feasible-region boundary is claimed.

#### `he_hx_price_factor` — feasible structure (search framing)

**Applies:** not applicable — sensitivity-framed

The study does not make a search claim for this attribute.

#### `he_hx_price_factor` — observed response (sensitivity framing)

**Applies:** yes

The native scenario table and case ledger record this attribute’s coordinated changes, response and any violated checks. The axis assessment lists its actual values. No independent marginal response or general feasible-region boundary is claimed.

#### `heat_rejection_equipment_price_factor` — feasible structure (search framing)

**Applies:** not applicable — sensitivity-framed

The study does not make a search claim for this attribute.

#### `heat_rejection_equipment_price_factor` — observed response (sensitivity framing)

**Applies:** yes

The native scenario table and case ledger record this attribute’s coordinated changes, response and any violated checks. The axis assessment lists its actual values. No independent marginal response or general feasible-region boundary is claimed.

#### `heating_account_price_factor` — feasible structure (search framing)

**Applies:** not applicable — sensitivity-framed

The study does not make a search claim for this attribute.

#### `heating_account_price_factor` — observed response (sensitivity framing)

**Applies:** yes

The native scenario table and case ledger record this attribute’s coordinated changes, response and any violated checks. The axis assessment lists its actual values. No independent marginal response or general feasible-region boundary is claimed.

#### `installation_account_price_factor` — feasible structure (search framing)

**Applies:** not applicable — sensitivity-framed

The study does not make a search claim for this attribute.

#### `installation_account_price_factor` — observed response (sensitivity framing)

**Applies:** yes

The native scenario table and case ledger record this attribute’s coordinated changes, response and any violated checks. The axis assessment lists its actual values. No independent marginal response or general feasible-region boundary is claimed.

#### `land_account_price_factor` — feasible structure (search framing)

**Applies:** not applicable — sensitivity-framed

The study does not make a search claim for this attribute.

#### `land_account_price_factor` — observed response (sensitivity framing)

**Applies:** yes

The native scenario table and case ledger record this attribute’s coordinated changes, response and any violated checks. The axis assessment lists its actual values. No independent marginal response or general feasible-region boundary is claimed.

#### `magnet_account_price_factor` — feasible structure (search framing)

**Applies:** not applicable — sensitivity-framed

The study does not make a search claim for this attribute.

#### `magnet_account_price_factor` — observed response (sensitivity framing)

**Applies:** yes

The native scenario table and case ledger record this attribute’s coordinated changes, response and any violated checks. The axis assessment lists its actual values. No independent marginal response or general feasible-region boundary is claimed.

#### `miscellaneous_account_price_factor` — feasible structure (search framing)

**Applies:** not applicable — sensitivity-framed

The study does not make a search claim for this attribute.

#### `miscellaneous_account_price_factor` — observed response (sensitivity framing)

**Applies:** yes

The native scenario table and case ledger record this attribute’s coordinated changes, response and any violated checks. The axis assessment lists its actual values. No independent marginal response or general feasible-region boundary is claimed.

#### `other_reactor_account_price_factor` — feasible structure (search framing)

**Applies:** not applicable — sensitivity-framed

The study does not make a search claim for this attribute.

#### `other_reactor_account_price_factor` — observed response (sensitivity framing)

**Applies:** yes

The native scenario table and case ledger record this attribute’s coordinated changes, response and any violated checks. The axis assessment lists its actual values. No independent marginal response or general feasible-region boundary is claimed.

#### `owner_account_price_factor` — feasible structure (search framing)

**Applies:** not applicable — sensitivity-framed

The study does not make a search claim for this attribute.

#### `owner_account_price_factor` — observed response (sensitivity framing)

**Applies:** yes

The native scenario table and case ledger record this attribute’s coordinated changes, response and any violated checks. The axis assessment lists its actual values. No independent marginal response or general feasible-region boundary is claimed.

#### `pbl_initial_account_price_factor` — feasible structure (search framing)

**Applies:** not applicable — sensitivity-framed

The study does not make a search claim for this attribute.

#### `pbl_initial_account_price_factor` — observed response (sensitivity framing)

**Applies:** yes

The native scenario table and case ledger record this attribute’s coordinated changes, response and any violated checks. The axis assessment lists its actual values. No independent marginal response or general feasible-region boundary is claimed.

#### `power_supplies_account_price_factor` — feasible structure (search framing)

**Applies:** not applicable — sensitivity-framed

The study does not make a search claim for this attribute.

#### `power_supplies_account_price_factor` — observed response (sensitivity framing)

**Applies:** yes

The native scenario table and case ledger record this attribute’s coordinated changes, response and any violated checks. The axis assessment lists its actual values. No independent marginal response or general feasible-region boundary is claimed.

#### `primary_circulators_account_price_factor` — feasible structure (search framing)

**Applies:** not applicable — sensitivity-framed

The study does not make a search claim for this attribute.

#### `primary_circulators_account_price_factor` — observed response (sensitivity framing)

**Applies:** yes

The native scenario table and case ledger record this attribute’s coordinated changes, response and any violated checks. The axis assessment lists its actual values. No independent marginal response or general feasible-region boundary is claimed.

#### `primary_helium_account_price_factor` — feasible structure (search framing)

**Applies:** not applicable — sensitivity-framed

The study does not make a search claim for this attribute.

#### `primary_helium_account_price_factor` — observed response (sensitivity framing)

**Applies:** yes

The native scenario table and case ledger record this attribute’s coordinated changes, response and any violated checks. The axis assessment lists its actual values. No independent marginal response or general feasible-region boundary is claimed.

#### `primary_loop_eta_drive` — feasible structure (search framing)

**Applies:** not applicable — sensitivity-framed

The study does not make a search claim for this attribute.

#### `primary_loop_eta_drive` — observed response (sensitivity framing)

**Applies:** yes

The native scenario table and case ledger record this attribute’s coordinated changes, response and any violated checks. The axis assessment lists its actual values. No independent marginal response or general feasible-region boundary is claimed.

#### `primary_loop_n_loops` — feasible structure (search framing)

**Applies:** not applicable — sensitivity-framed

The study does not make a search claim for this attribute.

#### `primary_loop_n_loops` — observed response (sensitivity framing)

**Applies:** yes

This declared attribute was held fixed. Its decline reason is retained in axes.json; no observed response or boundary is claimed.

#### `primary_pipes_account_price_factor` — feasible structure (search framing)

**Applies:** not applicable — sensitivity-framed

The study does not make a search claim for this attribute.

#### `primary_pipes_account_price_factor` — observed response (sensitivity framing)

**Applies:** yes

The native scenario table and case ledger record this attribute’s coordinated changes, response and any violated checks. The axis assessment lists its actual values. No independent marginal response or general feasible-region boundary is claimed.

#### `primary_spares_account_price_factor` — feasible structure (search framing)

**Applies:** not applicable — sensitivity-framed

The study does not make a search claim for this attribute.

#### `primary_spares_account_price_factor` — observed response (sensitivity framing)

**Applies:** yes

The native scenario table and case ledger record this attribute’s coordinated changes, response and any violated checks. The axis assessment lists its actual values. No independent marginal response or general feasible-region boundary is claimed.

#### `reactor_controls_account_price_factor` — feasible structure (search framing)

**Applies:** not applicable — sensitivity-framed

The study does not make a search claim for this attribute.

#### `reactor_controls_account_price_factor` — observed response (sensitivity framing)

**Applies:** yes

The native scenario table and case ledger record this attribute’s coordinated changes, response and any violated checks. The axis assessment lists its actual values. No independent marginal response or general feasible-region boundary is claimed.

#### `recuperator_hardware_ua` — feasible structure (search framing)

**Applies:** yes

The finite admitted offers and failed native cases are retained in the linked case ledger. Observed choices are in the axis assessment; relevant edge checks are in window.json. No global optimum is claimed.

#### `recuperator_hardware_ua` — observed response (sensitivity framing)

**Applies:** not applicable — search-framed

No separate sensitivity claim is made for this search-framed attribute; its coordinated scenario context remains recorded.

#### `remote_handling_account_price_factor` — feasible structure (search framing)

**Applies:** not applicable — sensitivity-framed

The study does not make a search claim for this attribute.

#### `remote_handling_account_price_factor` — observed response (sensitivity framing)

**Applies:** yes

The native scenario table and case ledger record this attribute’s coordinated changes, response and any violated checks. The axis assessment lists its actual values. No independent marginal response or general feasible-region boundary is claimed.

#### `shared_electrical_account_price_factor` — feasible structure (search framing)

**Applies:** not applicable — sensitivity-framed

The study does not make a search claim for this attribute.

#### `shared_electrical_account_price_factor` — observed response (sensitivity framing)

**Applies:** yes

The native scenario table and case ledger record this attribute’s coordinated changes, response and any violated checks. The axis assessment lists its actual values. No independent marginal response or general feasible-region boundary is claimed.

#### `shield_account_price_factor` — feasible structure (search framing)

**Applies:** not applicable — sensitivity-framed

The study does not make a search claim for this attribute.

#### `shield_account_price_factor` — observed response (sensitivity framing)

**Applies:** yes

The native scenario table and case ledger record this attribute’s coordinated changes, response and any violated checks. The axis assessment lists its actual values. No independent marginal response or general feasible-region boundary is claimed.

#### `source_basis_heating_source_efficiency` — feasible structure (search framing)

**Applies:** not applicable — sensitivity-framed

The study does not make a search claim for this attribute.

#### `source_basis_heating_source_efficiency` — observed response (sensitivity framing)

**Applies:** yes

The native scenario table and case ledger record this attribute’s coordinated changes, response and any violated checks. The axis assessment lists its actual values. No independent marginal response or general feasible-region boundary is claimed.

#### `source_basis_q_source_MW` — feasible structure (search framing)

**Applies:** not applicable — sensitivity-framed

The study does not make a search claim for this attribute.

#### `source_basis_q_source_MW` — observed response (sensitivity framing)

**Applies:** yes

The native scenario table and case ledger record this attribute’s coordinated changes, response and any violated checks. The axis assessment lists its actual values. No independent marginal response or general feasible-region boundary is claimed.

#### `source_installation_allowance_account_price_factor` — feasible structure (search framing)

**Applies:** not applicable — sensitivity-framed

The study does not make a search claim for this attribute.

#### `source_installation_allowance_account_price_factor` — observed response (sensitivity framing)

**Applies:** yes

The native scenario table and case ledger record this attribute’s coordinated changes, response and any violated checks. The axis assessment lists its actual values. No independent marginal response or general feasible-region boundary is claimed.

#### `source_installation_allowance_account_quote_USD2025` — feasible structure (search framing)

**Applies:** not applicable — sensitivity-framed

The study does not make a search claim for this attribute.

#### `source_installation_allowance_account_quote_USD2025` — observed response (sensitivity framing)

**Applies:** yes

The native scenario table and case ledger record this attribute’s coordinated changes, response and any violated checks. The axis assessment lists its actual values. No independent marginal response or general feasible-region boundary is claimed.

#### `steam_boundary_bypass_flow_rating` — feasible structure (search framing)

**Applies:** not applicable — sensitivity-framed

The study does not make a search claim for this attribute.

#### `steam_boundary_bypass_flow_rating` — observed response (sensitivity framing)

**Applies:** yes

The native scenario table and case ledger record this attribute’s coordinated changes, response and any violated checks. The axis assessment lists its actual values. No independent marginal response or general feasible-region boundary is claimed.

#### `steam_cycle_condenser_temperature_C` — feasible structure (search framing)

**Applies:** not applicable — sensitivity-framed

The study does not make a search claim for this attribute.

#### `steam_cycle_condenser_temperature_C` — observed response (sensitivity framing)

**Applies:** yes

This declared attribute was held fixed. Its decline reason is retained in axes.json; no observed response or boundary is claimed.

#### `steam_cycle_eta_hp` — feasible structure (search framing)

**Applies:** not applicable — sensitivity-framed

The study does not make a search claim for this attribute.

#### `steam_cycle_eta_hp` — observed response (sensitivity framing)

**Applies:** yes

The native scenario table and case ledger record this attribute’s coordinated changes, response and any violated checks. The axis assessment lists its actual values. No independent marginal response or general feasible-region boundary is claimed.

#### `steam_cycle_eta_lp` — feasible structure (search framing)

**Applies:** not applicable — sensitivity-framed

The study does not make a search claim for this attribute.

#### `steam_cycle_eta_lp` — observed response (sensitivity framing)

**Applies:** yes

The native scenario table and case ledger record this attribute’s coordinated changes, response and any violated checks. The axis assessment lists its actual values. No independent marginal response or general feasible-region boundary is claimed.

#### `steam_cycle_reheat_temperature_C` — feasible structure (search framing)

**Applies:** not applicable — sensitivity-framed

The study does not make a search claim for this attribute.

#### `steam_cycle_reheat_temperature_C` — observed response (sensitivity framing)

**Applies:** yes

This declared attribute was held fixed. Its decline reason is retained in axes.json; no observed response or boundary is claimed.

#### `steam_cycle_steam_temperature_C` — feasible structure (search framing)

**Applies:** not applicable — sensitivity-framed

The study does not make a search claim for this attribute.

#### `steam_cycle_steam_temperature_C` — observed response (sensitivity framing)

**Applies:** yes

This declared attribute was held fixed. Its decline reason is retained in axes.json; no observed response or boundary is claimed.

#### `steam_ledger_annual_service_fraction` — feasible structure (search framing)

**Applies:** not applicable — sensitivity-framed

The study does not make a search claim for this attribute.

#### `steam_ledger_annual_service_fraction` — observed response (sensitivity framing)

**Applies:** yes

The native scenario table and case ledger record this attribute’s coordinated changes, response and any violated checks. The axis assessment lists its actual values. No independent marginal response or general feasible-region boundary is claimed.

#### `steam_ledger_capital3` — feasible structure (search framing)

**Applies:** not applicable — sensitivity-framed

The study does not make a search claim for this attribute.

#### `steam_ledger_capital3` — observed response (sensitivity framing)

**Applies:** yes

The native scenario table and case ledger record this attribute’s coordinated changes, response and any violated checks. The axis assessment lists its actual values. No independent marginal response or general feasible-region boundary is claimed.

#### `steam_ledger_capital4` — feasible structure (search framing)

**Applies:** not applicable — sensitivity-framed

The study does not make a search claim for this attribute.

#### `steam_ledger_capital4` — observed response (sensitivity framing)

**Applies:** yes

The native scenario table and case ledger record this attribute’s coordinated changes, response and any violated checks. The axis assessment lists its actual values. No independent marginal response or general feasible-region boundary is claimed.

#### `steam_ledger_controller_capital` — feasible structure (search framing)

**Applies:** not applicable — sensitivity-framed

The study does not make a search claim for this attribute.

#### `steam_ledger_controller_capital` — observed response (sensitivity framing)

**Applies:** yes

The native scenario table and case ledger record this attribute’s coordinated changes, response and any violated checks. The axis assessment lists its actual values. No independent marginal response or general feasible-region boundary is claimed.

#### `steam_ledger_replacement_fraction` — feasible structure (search framing)

**Applies:** not applicable — sensitivity-framed

The study does not make a search claim for this attribute.

#### `steam_ledger_replacement_fraction` — observed response (sensitivity framing)

**Applies:** yes

The native scenario table and case ledger record this attribute’s coordinated changes, response and any violated checks. The axis assessment lists its actual values. No independent marginal response or general feasible-region boundary is claimed.

#### `steam_operating_import_price` — feasible structure (search framing)

**Applies:** not applicable — sensitivity-framed

The study does not make a search claim for this attribute.

#### `steam_operating_import_price` — observed response (sensitivity framing)

**Applies:** yes

The native scenario table and case ledger record this attribute’s coordinated changes, response and any violated checks. The axis assessment lists its actual values. No independent marginal response or general feasible-region boundary is claimed.

#### `steam_operating_residual_MW` — feasible structure (search framing)

**Applies:** not applicable — sensitivity-framed

The study does not make a search claim for this attribute.

#### `steam_operating_residual_MW` — observed response (sensitivity framing)

**Applies:** yes

The native scenario table and case ledger record this attribute’s coordinated changes, response and any violated checks. The axis assessment lists its actual values. No independent marginal response or general feasible-region boundary is claimed.

#### `steam_transport_costscale` — feasible structure (search framing)

**Applies:** not applicable — sensitivity-framed

The study does not make a search claim for this attribute.

#### `steam_transport_costscale` — observed response (sensitivity framing)

**Applies:** yes

The native scenario table and case ledger record this attribute’s coordinated changes, response and any violated checks. The axis assessment lists its actual values. No independent marginal response or general feasible-region boundary is claimed.

#### `steam_transport_n_loops` — feasible structure (search framing)

**Applies:** yes

The finite admitted offers and failed native cases are retained in the linked case ledger. Observed choices are in the axis assessment; relevant edge checks are in window.json. No global optimum is claimed.

#### `steam_transport_n_loops` — observed response (sensitivity framing)

**Applies:** not applicable — search-framed

No separate sensitivity claim is made for this search-framed attribute; its coordinated scenario context remains recorded.

#### `steam_transport_salt_pumps_per_circuit` — feasible structure (search framing)

**Applies:** yes

The finite admitted offers and failed native cases are retained in the linked case ledger. Observed choices are in the axis assessment; relevant edge checks are in window.json. No global optimum is claimed.

#### `steam_transport_salt_pumps_per_circuit` — observed response (sensitivity framing)

**Applies:** not applicable — search-framed

No separate sensitivity claim is made for this search-framed attribute; its coordinated scenario context remains recorded.

#### `steam_transport_secondary_head` — feasible structure (search framing)

**Applies:** not applicable — sensitivity-framed

The study does not make a search claim for this attribute.

#### `steam_transport_secondary_head` — observed response (sensitivity framing)

**Applies:** yes

This declared attribute was held fixed. Its decline reason is retained in axes.json; no observed response or boundary is claimed.

#### `steam_transport_selected_salt_design_flow_kg_s` — feasible structure (search framing)

**Applies:** yes

The finite admitted offers and failed native cases are retained in the linked case ledger. Observed choices are in the axis assessment; relevant edge checks are in window.json. No global optimum is claimed.

#### `steam_transport_selected_salt_design_flow_kg_s` — observed response (sensitivity framing)

**Applies:** not applicable — search-framed

No separate sensitivity claim is made for this search-framed attribute; its coordinated scenario context remains recorded.

#### `steam_whole_magnet_life` — feasible structure (search framing)

**Applies:** not applicable — sensitivity-framed

The study does not make a search claim for this attribute.

#### `steam_whole_magnet_life` — observed response (sensitivity framing)

**Applies:** yes

The native scenario table and case ledger record this attribute’s coordinated changes, response and any violated checks. The axis assessment lists its actual values. No independent marginal response or general feasible-region boundary is claimed.

#### `steam_whole_routine_fraction` — feasible structure (search framing)

**Applies:** not applicable — sensitivity-framed

The study does not make a search claim for this attribute.

#### `steam_whole_routine_fraction` — observed response (sensitivity framing)

**Applies:** yes

The native scenario table and case ledger record this attribute’s coordinated changes, response and any violated checks. The axis assessment lists its actual values. No independent marginal response or general feasible-region boundary is claimed.

#### `structure_account_price_factor` — feasible structure (search framing)

**Applies:** not applicable — sensitivity-framed

The study does not make a search claim for this attribute.

#### `structure_account_price_factor` — observed response (sensitivity framing)

**Applies:** yes

The native scenario table and case ledger record this attribute’s coordinated changes, response and any violated checks. The axis assessment lists its actual values. No independent marginal response or general feasible-region boundary is claimed.

#### `turbine_equipment_price_factor` — feasible structure (search framing)

**Applies:** not applicable — sensitivity-framed

The study does not make a search claim for this attribute.

#### `turbine_equipment_price_factor` — observed response (sensitivity framing)

**Applies:** yes

The native scenario table and case ledger record this attribute’s coordinated changes, response and any violated checks. The axis assessment lists its actual values. No independent marginal response or general feasible-region boundary is claimed.

#### `vessel_account_price_factor` — feasible structure (search framing)

**Applies:** not applicable — sensitivity-framed

The study does not make a search claim for this attribute.

#### `vessel_account_price_factor` — observed response (sensitivity framing)

**Applies:** yes

The native scenario table and case ledger record this attribute’s coordinated changes, response and any violated checks. The axis assessment lists its actual values. No independent marginal response or general feasible-region boundary is claimed.

#### `waste_account_price_factor` — feasible structure (search framing)

**Applies:** not applicable — sensitivity-framed

The study does not make a search claim for this attribute.

#### `waste_account_price_factor` — observed response (sensitivity framing)

**Applies:** yes

The native scenario table and case ledger record this attribute’s coordinated changes, response and any violated checks. The axis assessment lists its actual values. No independent marginal response or general feasible-region boundary is claimed.

#### `water_ic1_ua` — feasible structure (search framing)

**Applies:** yes

The finite admitted offers and failed native cases are retained in the linked case ledger. Observed choices are in the axis assessment; relevant edge checks are in window.json. No global optimum is claimed.

#### `water_ic1_ua` — observed response (sensitivity framing)

**Applies:** not applicable — search-framed

No separate sensitivity claim is made for this search-framed attribute; its coordinated scenario context remains recorded.

#### `water_ic2_ua` — feasible structure (search framing)

**Applies:** yes

The finite admitted offers and failed native cases are retained in the linked case ledger. Observed choices are in the axis assessment; relevant edge checks are in window.json. No global optimum is claimed.

#### `water_ic2_ua` — observed response (sensitivity framing)

**Applies:** not applicable — search-framed

No separate sensitivity claim is made for this search-framed attribute; its coordinated scenario context remains recorded.

#### `water_pre_ua` — feasible structure (search framing)

**Applies:** yes

The finite admitted offers and failed native cases are retained in the linked case ledger. Observed choices are in the axis assessment; relevant edge checks are in window.json. No global optimum is claimed.

#### `water_pre_ua` — observed response (sensitivity framing)

**Applies:** not applicable — search-framed

No separate sensitivity claim is made for this search-framed attribute; its coordinated scenario context remains recorded.

## 7. Axis groups

All groups are actual qualified source attributes expanded to their emitted input keys. Each group has one emitted key with fan_out provenance. There are no cross-attribute ties. Equal ratios, prices and efficiency changes are coordinated choices, not asserted physical identities.

| Axis | Entry key | Provenance |
|---|---|---|
| `auxiliary_rejection_account_price_factor` | `whole_plant_conversion__plant__auxiliary_rejection_account__price_factor` | fan_out |
| `blanket_account_price_factor` | `whole_plant_conversion__plant__blanket_account__price_factor` | fan_out |
| `compressor_1_efficiency` | `whole_plant_conversion__plant__compressor_1__efficiency` | fan_out |
| `compressor_1_selected_ratio` | `whole_plant_conversion__plant__compressor_1__selected_ratio` | fan_out |
| `compressor_2_efficiency` | `whole_plant_conversion__plant__compressor_2__efficiency` | fan_out |
| `compressor_2_selected_ratio` | `whole_plant_conversion__plant__compressor_2__selected_ratio` | fan_out |
| `compressor_3_efficiency` | `whole_plant_conversion__plant__compressor_3__efficiency` | fan_out |
| `compressor_3_selected_ratio` | `whole_plant_conversion__plant__compressor_3__selected_ratio` | fan_out |
| `compressor_equipment_price_factor` | `whole_plant_conversion__plant__compressor_equipment__price_factor` | fan_out |
| `conversion_services_price_factor` | `whole_plant_conversion__plant__conversion_services__price_factor` | fan_out |
| `cryogenic_demand_extra_cold_W` | `whole_plant_conversion__plant__cryogenic_demand__extra_cold_W` | fan_out |
| `cryogenic_demand_q_nuc_W_m3` | `whole_plant_conversion__plant__cryogenic_demand__q_nuc_W_m3` | fan_out |
| `cryoplant_account_price_factor` | `whole_plant_conversion__plant__cryoplant_account__price_factor` | fan_out |
| `cycle_selected_flow` | `whole_plant_conversion__plant__cycle__selected_flow` | fan_out |
| `cycle_turbine_efficiency` | `whole_plant_conversion__plant__cycle__turbine_efficiency` | fan_out |
| `digital_twin_account_price_factor` | `whole_plant_conversion__plant__digital_twin_account__price_factor` | fan_out |
| `divertor_account_price_factor` | `whole_plant_conversion__plant__divertor_account__price_factor` | fan_out |
| `facilities_account_price_factor` | `whole_plant_conversion__plant__facilities_account__price_factor` | fan_out |
| `finance_availability` | `whole_plant_conversion__plant__finance__availability` | fan_out |
| `finance_commissioning_rate` | `whole_plant_conversion__plant__finance__commissioning_rate` | fan_out |
| `finance_contingency_rate` | `whole_plant_conversion__plant__finance__contingency_rate` | fan_out |
| `finance_freight_rate` | `whole_plant_conversion__plant__finance__freight_rate` | fan_out |
| `finance_general_spares_rate` | `whole_plant_conversion__plant__finance__general_spares_rate` | fan_out |
| `finance_indirect_rate` | `whole_plant_conversion__plant__finance__indirect_rate` | fan_out |
| `finance_insurance_rate` | `whole_plant_conversion__plant__finance__insurance_rate` | fan_out |
| `finance_rate` | `whole_plant_conversion__plant__finance__rate` | fan_out |
| `finance_tax_rate` | `whole_plant_conversion__plant__finance__tax_rate` | fan_out |
| `fuel_accounts_tbr` | `whole_plant_conversion__plant__fuel_accounts__tbr` | fan_out |
| `fuel_accounts_tritium_price` | `whole_plant_conversion__plant__fuel_accounts__tritium_price` | fan_out |
| `fuel_processing_account_price_factor` | `whole_plant_conversion__plant__fuel_processing_account__price_factor` | fan_out |
| `gas_boundary_bypass_flow_rating` | `whole_plant_conversion__plant__gas_boundary__bypass_flow_rating` | fan_out |
| `gas_ledger_annual_service_fraction` | `whole_plant_conversion__plant__gas_ledger__annual_service_fraction` | fan_out |
| `gas_ledger_capital9` | `whole_plant_conversion__plant__gas_ledger__capital9` | fan_out |
| `gas_ledger_controller_capital` | `whole_plant_conversion__plant__gas_ledger__controller_capital` | fan_out |
| `gas_ledger_replacement_fraction` | `whole_plant_conversion__plant__gas_ledger__replacement_fraction` | fan_out |
| `generator_equipment_price_factor` | `whole_plant_conversion__plant__generator_equipment__price_factor` | fan_out |
| `he_duty_equipment_price_factor` | `whole_plant_conversion__plant__he_duty_equipment__price_factor` | fan_out |
| `he_hx_price_factor` | `whole_plant_conversion__plant__he_hx__price_factor` | fan_out |
| `heat_rejection_equipment_price_factor` | `whole_plant_conversion__plant__heat_rejection_equipment__price_factor` | fan_out |
| `heating_account_price_factor` | `whole_plant_conversion__plant__heating_account__price_factor` | fan_out |
| `installation_account_price_factor` | `whole_plant_conversion__plant__installation_account__price_factor` | fan_out |
| `land_account_price_factor` | `whole_plant_conversion__plant__land_account__price_factor` | fan_out |
| `magnet_account_price_factor` | `whole_plant_conversion__plant__magnet_account__price_factor` | fan_out |
| `miscellaneous_account_price_factor` | `whole_plant_conversion__plant__miscellaneous_account__price_factor` | fan_out |
| `other_reactor_account_price_factor` | `whole_plant_conversion__plant__other_reactor_account__price_factor` | fan_out |
| `owner_account_price_factor` | `whole_plant_conversion__plant__owner_account__price_factor` | fan_out |
| `pbl_initial_account_price_factor` | `whole_plant_conversion__plant__pbl_initial_account__price_factor` | fan_out |
| `power_supplies_account_price_factor` | `whole_plant_conversion__plant__power_supplies_account__price_factor` | fan_out |
| `primary_circulators_account_price_factor` | `whole_plant_conversion__plant__primary_circulators_account__price_factor` | fan_out |
| `primary_helium_account_price_factor` | `whole_plant_conversion__plant__primary_helium_account__price_factor` | fan_out |
| `primary_loop_eta_drive` | `whole_plant_conversion__plant__primary_loop__eta_drive` | fan_out |
| `primary_loop_n_loops` | `whole_plant_conversion__plant__primary_loop__n_loops` | fan_out |
| `primary_pipes_account_price_factor` | `whole_plant_conversion__plant__primary_pipes_account__price_factor` | fan_out |
| `primary_spares_account_price_factor` | `whole_plant_conversion__plant__primary_spares_account__price_factor` | fan_out |
| `reactor_controls_account_price_factor` | `whole_plant_conversion__plant__reactor_controls_account__price_factor` | fan_out |
| `recuperator_hardware_ua` | `whole_plant_conversion__plant__recuperator_hardware__ua` | fan_out |
| `remote_handling_account_price_factor` | `whole_plant_conversion__plant__remote_handling_account__price_factor` | fan_out |
| `shared_electrical_account_price_factor` | `whole_plant_conversion__plant__shared_electrical_account__price_factor` | fan_out |
| `shield_account_price_factor` | `whole_plant_conversion__plant__shield_account__price_factor` | fan_out |
| `source_basis_heating_source_efficiency` | `whole_plant_conversion__plant__source_basis__heating_source_efficiency` | fan_out |
| `source_basis_q_source_MW` | `whole_plant_conversion__plant__source_basis__q_source_MW` | fan_out |
| `source_installation_allowance_account_price_factor` | `whole_plant_conversion__plant__source_installation_allowance_account__price_factor` | fan_out |
| `source_installation_allowance_account_quote_USD2025` | `whole_plant_conversion__plant__source_installation_allowance_account__quote_USD2025` | fan_out |
| `steam_boundary_bypass_flow_rating` | `whole_plant_conversion__plant__steam_boundary__bypass_flow_rating` | fan_out |
| `steam_cycle_condenser_temperature_C` | `whole_plant_conversion__plant__steam_cycle__condenser_temperature_C` | fan_out |
| `steam_cycle_eta_hp` | `whole_plant_conversion__plant__steam_cycle__eta_hp` | fan_out |
| `steam_cycle_eta_lp` | `whole_plant_conversion__plant__steam_cycle__eta_lp` | fan_out |
| `steam_cycle_reheat_temperature_C` | `whole_plant_conversion__plant__steam_cycle__reheat_temperature_C` | fan_out |
| `steam_cycle_steam_temperature_C` | `whole_plant_conversion__plant__steam_cycle__steam_temperature_C` | fan_out |
| `steam_ledger_annual_service_fraction` | `whole_plant_conversion__plant__steam_ledger__annual_service_fraction` | fan_out |
| `steam_ledger_capital3` | `whole_plant_conversion__plant__steam_ledger__capital3` | fan_out |
| `steam_ledger_capital4` | `whole_plant_conversion__plant__steam_ledger__capital4` | fan_out |
| `steam_ledger_controller_capital` | `whole_plant_conversion__plant__steam_ledger__controller_capital` | fan_out |
| `steam_ledger_replacement_fraction` | `whole_plant_conversion__plant__steam_ledger__replacement_fraction` | fan_out |
| `steam_operating_import_price` | `whole_plant_conversion__plant__steam_operating__import_price` | fan_out |
| `steam_operating_residual_MW` | `whole_plant_conversion__plant__steam_operating__residual_MW` | fan_out |
| `steam_transport_costscale` | `whole_plant_conversion__plant__steam_transport__costscale` | fan_out |
| `steam_transport_n_loops` | `whole_plant_conversion__plant__steam_transport__n_loops` | fan_out |
| `steam_transport_salt_pumps_per_circuit` | `whole_plant_conversion__plant__steam_transport__salt_pumps_per_circuit` | fan_out |
| `steam_transport_secondary_head` | `whole_plant_conversion__plant__steam_transport__secondary_head` | fan_out |
| `steam_transport_selected_salt_design_flow_kg_s` | `whole_plant_conversion__plant__steam_transport__selected_salt_design_flow_kg_s` | fan_out |
| `steam_whole_magnet_life` | `whole_plant_conversion__plant__steam_whole__magnet_life` | fan_out |
| `steam_whole_routine_fraction` | `whole_plant_conversion__plant__steam_whole__routine_fraction` | fan_out |
| `structure_account_price_factor` | `whole_plant_conversion__plant__structure_account__price_factor` | fan_out |
| `turbine_equipment_price_factor` | `whole_plant_conversion__plant__turbine_equipment__price_factor` | fan_out |
| `vessel_account_price_factor` | `whole_plant_conversion__plant__vessel_account__price_factor` | fan_out |
| `waste_account_price_factor` | `whole_plant_conversion__plant__waste_account__price_factor` | fan_out |
| `water_ic1_ua` | `whole_plant_conversion__plant__water_ic1__ua` | fan_out |
| `water_ic2_ua` | `whole_plant_conversion__plant__water_ic2__ua` | fan_out |
| `water_pre_ua` | `whole_plant_conversion__plant__water_pre__ua` | fan_out |

## 8. Indicators and rulings

All 90 declared groups, including five declined groups, report constraints_reachable in [indicators.json](indicators.json); subset is false. None reports no_constraint_response, so no additional owner ruling is required. The owner explicitly requested price, performance, common cost/load, fuel and availability sensitivities. A reachable path is a possible dependency, not proof of physical or economic resistance.

**Not derivable:** monotonicity of a channel in an axis; identity of the same physical quantity across differing key names; intra-module operand dependency. No indicator output or report claims these. Engineered price and efficiency scenarios remain sensitivities even where a domain/economic predicate is reachable.

There are no no_constraint_response model-development findings. Other material limitations and discoveries are registered in §15.

## 9. Preflight results

The [native integration return](integration/integration_return.json) records all ten gates passing. The same frozen package, full axis declaration, manifest, baseline and environment are used by this study; that valid evidence is reused. [Preflight results](preparation/preflight_results.json), [package identity](preparation/package_identity.json), [baseline result](preparation/baseline_result.json) and [Python read coverage](preparation/read_coverage.json) retain the actual receipts.

| Gate | Outcome | Evidence |
|---|---|---|
| Declared-group key validation | pass | Full 90-group declaration and native preflight |
| Suffix-sibling scan | pass; warnings remain interpretive | Exact tool output in preparation/preflight_results.json |
| Baseline headline reproduction | pass | Complete 637-input baseline and native result |
| Manifest/package fingerprints | pass | Integration manifest and lineage gates |
| Package cleanliness | pass | Integration and stock main route before/after checks |
| Python read coverage | pass | Fresh baseline observer receipt; limits retained in integration documentation |

The first oracle preparation attempt overlapped in-place regeneration and encountered temporary missing default inputs. Its complete evidence is retained in preparation-attempt-01-invalid and has no physical or ranking authority. The replacement scan ran after integration completed and had zero refusals. No native main-study attempt was discarded.

## 10. Execution route and why

**Route:** study-local direct API using the stock strict loader, PreparedEvaluator, StudyRunner, PreparedListStrategy, StudyStore and StudyQuery. Coordinated equipment tuples and scenario blocks require a prepared point list. The route was exercised by integration before execution. Every main point carries complete inputs, scalar outputs and all native verdicts in the store.

**Glue ledger: none.** No runtime adapter or external physics solver supplies a missing model relationship. Oracle scans choose candidate inputs before execution; report code only joins, selects, decomposes and plots native outputs. The cost plot normalizes published cost PV components by published energy PV; the headline remains the native LCOE channel.

## 11. Study definition and window provenance

The stable-package independent scan evaluated 3900 complete points, with zero refusals, before fixing 2496 unique native proposals and 2651 catalog/scenario aliases. The final definitions, values, brackets and input-source hashes are frozen in [window.json](window.json), [proposed-points.json](proposed-points.json) and [candidate-freeze.json](preparation/candidate-freeze.json).

The window is engineered. It retains the predecessor catalog but rereads its edges from currently passing whole-plant anchors. Failure pruning in common/quote scenarios is justified by an invariant failed predicate or an explicit changed-point oracle evaluation. Both admission audits retain every decision; no newly admitted offer was omitted. Changed performance rescans the full affected catalog. The 3000 MW source has no passing shared equipment basis and is retained as unsupported. Hypothetical performance/price interactions and native strict-zero/reporting-band brackets are part of the predeclared list.

## 12. Cross-fingerprint correlation and what it means

Single fingerprint for all main-study points; no cross-arm correlation is needed. The predecessor is historical context with a narrower cost/power boundary and 0.85 availability, compared with 0.80 here. Its 498 controls exactly reproduce 872 inherited channels and 84 predicates under legacy finance; new whole-plant conditions and outputs are additional scope. Six selected predecessor native receipts and the historical verification/summary are retained under supporting/predecessor. The report does not reuse those winners as the new whole-plant answer or interpret the boundary/finance/reranking difference as a pure cost addition.

## 13. Verification

The stock verifier aborted at its first mismatch: case c2438, cryogenic cold margin, native 0.003072599989536684 W versus oracle 0.0030725999968126416 W. Relative deviation 2.368e-9 exceeds the declared 1e-9 tolerance; the absolute error is 7.276e-12 W and this channel has zero absolute tolerance. Four inherited solver-iteration diagnostics are excluded. It uses the existing relative and predeclared absolute numerical tolerances; physical inequalities are not relaxed. [Failure receipt](results/verification-blocker.json) retains the exact command and failure; the stock tool did not emit a summary. snapshot.json marks this attempt blocked and unreleased.

Numerical agreement checks implementation of the declared equations. It does not establish vendor performance, source heating transport, plasma sustainment or global manufactured reactor fit. Fixed captured constants and qualification flags that agree by construction are not independent empirical validations. Earlier independent source/accounting and native behavior reviews are retained with their actual scope.

## 14. Review outcomes

| Lens | Verdict | Disposition |
|---|---|---|
| Source, full account/power boundary and MR-7 | independent PASS | Exact frozen implementation identity; supporting/implementation-integration-review.md |
| Pre-execution framing, range and admission | coordinator checked | Existing source/math review applies; complete stable-package scan, explicit materiality and admission audit retained |
| Final whole-plant reranking, claims and presentation | independent FINDINGS: verification blocks release | supporting/final-results-review.md; exact native evidence, assumptions and findings assessed |

No duplicate source review is claimed. The same independent reviewer reused valid implementation coverage and inspected the new execution and draft ranking paths. Its FINDINGS disposition blocks release.

## 15. Findings

| Id | Kind | Finding | Disposition | Home |
|---|---|---|---|
| 20260927-design-study-whole-plant-conversion#1 | model | The common source is supplied; plasma sustainment and global manufactured fit are not qualified. | Declared seam: retain this condition at every whole-plant conclusion; no reactor qualification claim. | work/active/WI-098_whole-plant-conversion-comparison/configuration.md |
| 20260927-design-study-whole-plant-conversion#2 | model | The selected primary and divertor offers cannot support the 3000 MW source condition. | Declared seam: preserve failed cases and exclude this source from paired preference; no automatic hardware resizing. | exploration/whole_plant_conversion/studies/20260927-design-study-whole-plant-conversion/results/constraint-summary.json |
| 20260927-design-study-whole-plant-conversion#3 | model | Transferred nuclear heating is not a validated bound for the changed magnet/blanket geometry. | Declared seam: vary demand at fixed cryoplant and retain the native capacity bracket; updated transport remains future research. | work/active/WI-098_whole-plant-conversion-comparison/configuration.md |
| 20260927-design-study-whole-plant-conversion#4 | model | Generated descriptive CAS codes disagree with the accepted account categories; executable membership is correct. | Declared seam: use the explicit reviewed mapping for this report; correct metadata before using generic CAS rollups. | work/active/WI-098_whole-plant-conversion-comparison/report.md |
| 20260927-design-study-whole-plant-conversion#5 | model | The finite equipment window has uncaught edges and the technologies have different modeled operating freedoms. | Declared seam: report finite-catalog minima and conditional scenarios; no equal global technology optimization claim. | exploration/whole_plant_conversion/studies/20260927-design-study-whole-plant-conversion/ANNEX.md |
| 20260927-design-study-whole-plant-conversion#6 | process | The first oracle scan overlapped in-place regeneration and read temporarily absent input defaults. | Corrected execution: retain invalid scan, serialize regeneration and scanning, and use the zero-refusal replacement scan. | work/orchestration/goals/design-study-whole-plant-conversion/trail.md |
| 20260927-design-study-whole-plant-conversion#7 | model | The static validator reports inherited literal/alias diagnostics on the compiled assembly. | Declared seam: retain raw exit1 and reviewed identity-level dispositions with zero unresolved diagnostics; do not call static validation green. | work/active/WI-098_whole-plant-conversion-comparison/evidence/validation-detail.json |
| 20260927-design-study-whole-plant-conversion#8 | model | Equipment price and common reactor account stresses are explicit assumptions rather than established market uncertainty intervals. | Declared seam: report conditional preference and native thresholds; do not present engineered endpoints as credible confidence bounds. | work/active/WI-098_whole-plant-conversion-comparison/configuration.md |
| 20260927-design-study-whole-plant-conversion#9 | model | The near-capacity cryogenic bracket fails unchanged stock numerical verification because a 7.276e-12 W difference exceeds the relative tolerance on a 0.00307 W residual. | Declared seam: this attempt is blocked and retained; review a wider diagnostic bracket in a new round, without changing model, oracle or tolerances. | work/orchestration/goals/design-study-whole-plant-conversion/evidence/final-results-review.md |

## 16. Snapshot

- **File:** snapshot.json
- **sha256:** 038545e8b98042063409aa72884c182327b7a87ec7aa5d5a8c6a726ec44de0fb
- **Schema version:** 1

The snapshot resolves values and artifact digests and marks released false. The sealed package and frozen source bundle make the result independent of later live model, manifest or report changes.

## 17. What this record does not contain

The record retains six selected predecessor native cases and its verification/summary, not the full predecessor 498-case store. It retains the reviewed development report and verification receipts rather than every raw development run. Original background PDFs are not bundled; their stated authority, assumptions and calculations are retained in the copied configuration, design and source audit. The whole-plant main store, complete inputs, all native outputs/verdicts, report data, renderer, replay instructions, scan history and required identities are included.

**END OF RECORD**
