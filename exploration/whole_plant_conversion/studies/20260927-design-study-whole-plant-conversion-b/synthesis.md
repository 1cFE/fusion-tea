# Executor reading of the sealed whole-plant study

[AGENT] Reader: Codex coordinator /root, the executor. Date: 2026-09-27. Evidence is read only from this committed record directory at commit a7bd94ed9a9746e1866400f60be5792eab6842d8. This reading adds no independent-review authority.

Snapshot SHA256: `5db4b78627cadca525c02e29bf98e9c6bad173baf372e25cce9a4bf3effb124e`.

## What the study set out to do

Compare steam and helium Brayton by complete declared plant electricity and lifecycle cost, using the same supplied reactor within each pair and freshly selecting admitted equipment. The boundary and original intent are retained in [record.md](record.md) and [owner brief](owner-brief.md).

## What it found

The recorded nominal minima favor steam at the two supported source conditions. These are finite-catalog results in USD2025, not global technology optima.

| Source MW | Branch | Net export MW | Whole-plant LCOE USD2025/MWh |
|---:|---|---:|---:|
| 2500 | gas | 285.883 | 875.313 |
| 2500 | steam | 663.969 | 408.164 |
| 2800 | gas | 204.460 | 1230.284 |
| 2800 | steam | 746.645 | 370.701 |
| 3000 | gas | unsupported | unsupported |
| 3000 | steam | unsupported | unsupported |

[Native rankings](results/presentation/native-ranking.json) retain exact selected case identities. [Study conclusion](study-conclusion.md) explains the complete account boundary and the combined efficiency/quote scenario that reverses preference at 2,800 MW. The nominal 2,800 MW Brayton selection differs because the 2,500 MW winner fails source adequacy. Both 3,000 MW branches fail selected upstream hardware checks.

Executor interpretation: steam’s extra capital buys a larger electrical denominator over which to spread common reactor expenses. The conditional Brayton reversal makes the useful decision a combination of equipment performance and price, rather than a universal technology ranking. This interpretation follows the recorded native contributions and sensitivities; it adds no new calculation.

## Framing verdict per axis

All 90 proposed framings survive the recorded review. Search applies only to finite offers; coordinated sensitivities do not isolate individual marginal effects. Exact values and decline reasons are in [axis assessment](results/axis-assessment.json) and [axes](axes.json).

| Axis | Recorded framing | Executed? | Reading |
|---|---|---|---|
| `auxiliary_rejection_account_price_factor` | sensitivity | yes | Conditional coordinated response |
| `blanket_account_price_factor` | sensitivity | yes | Conditional coordinated response |
| `compressor_1_efficiency` | sensitivity | yes | Conditional coordinated response |
| `compressor_1_selected_ratio` | search | yes | Finite offered choices only |
| `compressor_2_efficiency` | sensitivity | yes | Conditional coordinated response |
| `compressor_2_selected_ratio` | search | yes | Finite offered choices only |
| `compressor_3_efficiency` | sensitivity | yes | Conditional coordinated response |
| `compressor_3_selected_ratio` | search | yes | Finite offered choices only |
| `compressor_equipment_price_factor` | sensitivity | yes | Conditional coordinated response |
| `conversion_services_price_factor` | sensitivity | yes | Conditional coordinated response |
| `cryogenic_demand_extra_cold_W` | sensitivity | yes | Conditional coordinated response |
| `cryogenic_demand_q_nuc_W_m3` | sensitivity | yes | Conditional coordinated response |
| `cryoplant_account_price_factor` | sensitivity | yes | Conditional coordinated response |
| `cycle_selected_flow` | search | yes | Finite offered choices only |
| `cycle_turbine_efficiency` | sensitivity | yes | Conditional coordinated response |
| `digital_twin_account_price_factor` | sensitivity | yes | Conditional coordinated response |
| `divertor_account_price_factor` | sensitivity | yes | Conditional coordinated response |
| `facilities_account_price_factor` | sensitivity | yes | Conditional coordinated response |
| `finance_availability` | sensitivity | yes | Conditional coordinated response |
| `finance_commissioning_rate` | sensitivity | yes | Conditional coordinated response |
| `finance_contingency_rate` | sensitivity | yes | Conditional coordinated response |
| `finance_freight_rate` | sensitivity | yes | Conditional coordinated response |
| `finance_general_spares_rate` | sensitivity | yes | Conditional coordinated response |
| `finance_indirect_rate` | sensitivity | yes | Conditional coordinated response |
| `finance_insurance_rate` | sensitivity | yes | Conditional coordinated response |
| `finance_rate` | sensitivity | yes | Conditional coordinated response |
| `finance_tax_rate` | sensitivity | yes | Conditional coordinated response |
| `fuel_accounts_tbr` | sensitivity | yes | Conditional coordinated response |
| `fuel_accounts_tritium_price` | sensitivity | yes | Conditional coordinated response |
| `fuel_processing_account_price_factor` | sensitivity | yes | Conditional coordinated response |
| `gas_boundary_bypass_flow_rating` | sensitivity | yes | Conditional coordinated response |
| `gas_ledger_annual_service_fraction` | sensitivity | yes | Conditional coordinated response |
| `gas_ledger_capital9` | sensitivity | yes | Conditional coordinated response |
| `gas_ledger_controller_capital` | sensitivity | yes | Conditional coordinated response |
| `gas_ledger_replacement_fraction` | sensitivity | yes | Conditional coordinated response |
| `generator_equipment_price_factor` | sensitivity | yes | Conditional coordinated response |
| `he_duty_equipment_price_factor` | sensitivity | yes | Conditional coordinated response |
| `he_hx_price_factor` | sensitivity | yes | Conditional coordinated response |
| `heat_rejection_equipment_price_factor` | sensitivity | yes | Conditional coordinated response |
| `heating_account_price_factor` | sensitivity | yes | Conditional coordinated response |
| `installation_account_price_factor` | sensitivity | yes | Conditional coordinated response |
| `land_account_price_factor` | sensitivity | yes | Conditional coordinated response |
| `magnet_account_price_factor` | sensitivity | yes | Conditional coordinated response |
| `miscellaneous_account_price_factor` | sensitivity | yes | Conditional coordinated response |
| `other_reactor_account_price_factor` | sensitivity | yes | Conditional coordinated response |
| `owner_account_price_factor` | sensitivity | yes | Conditional coordinated response |
| `pbl_initial_account_price_factor` | sensitivity | yes | Conditional coordinated response |
| `power_supplies_account_price_factor` | sensitivity | yes | Conditional coordinated response |
| `primary_circulators_account_price_factor` | sensitivity | yes | Conditional coordinated response |
| `primary_helium_account_price_factor` | sensitivity | yes | Conditional coordinated response |
| `primary_loop_eta_drive` | sensitivity | yes | Conditional coordinated response |
| `primary_loop_n_loops` | sensitivity | declined | No response claim |
| `primary_pipes_account_price_factor` | sensitivity | yes | Conditional coordinated response |
| `primary_spares_account_price_factor` | sensitivity | yes | Conditional coordinated response |
| `reactor_controls_account_price_factor` | sensitivity | yes | Conditional coordinated response |
| `recuperator_hardware_ua` | search | yes | Finite offered choices only |
| `remote_handling_account_price_factor` | sensitivity | yes | Conditional coordinated response |
| `shared_electrical_account_price_factor` | sensitivity | yes | Conditional coordinated response |
| `shield_account_price_factor` | sensitivity | yes | Conditional coordinated response |
| `source_basis_heating_source_efficiency` | sensitivity | yes | Conditional coordinated response |
| `source_basis_q_source_MW` | sensitivity | yes | Conditional coordinated response |
| `source_installation_allowance_account_price_factor` | sensitivity | yes | Conditional coordinated response |
| `source_installation_allowance_account_quote_USD2025` | sensitivity | yes | Conditional coordinated response |
| `steam_boundary_bypass_flow_rating` | sensitivity | yes | Conditional coordinated response |
| `steam_cycle_condenser_temperature_C` | sensitivity | declined | No response claim |
| `steam_cycle_eta_hp` | sensitivity | yes | Conditional coordinated response |
| `steam_cycle_eta_lp` | sensitivity | yes | Conditional coordinated response |
| `steam_cycle_reheat_temperature_C` | sensitivity | declined | No response claim |
| `steam_cycle_steam_temperature_C` | sensitivity | declined | No response claim |
| `steam_ledger_annual_service_fraction` | sensitivity | yes | Conditional coordinated response |
| `steam_ledger_capital3` | sensitivity | yes | Conditional coordinated response |
| `steam_ledger_capital4` | sensitivity | yes | Conditional coordinated response |
| `steam_ledger_controller_capital` | sensitivity | yes | Conditional coordinated response |
| `steam_ledger_replacement_fraction` | sensitivity | yes | Conditional coordinated response |
| `steam_operating_import_price` | sensitivity | yes | Conditional coordinated response |
| `steam_operating_residual_MW` | sensitivity | yes | Conditional coordinated response |
| `steam_transport_costscale` | sensitivity | yes | Conditional coordinated response |
| `steam_transport_n_loops` | search | yes | Finite offered choices only |
| `steam_transport_salt_pumps_per_circuit` | search | yes | Finite offered choices only |
| `steam_transport_secondary_head` | sensitivity | declined | No response claim |
| `steam_transport_selected_salt_design_flow_kg_s` | search | yes | Finite offered choices only |
| `steam_whole_magnet_life` | sensitivity | yes | Conditional coordinated response |
| `steam_whole_routine_fraction` | sensitivity | yes | Conditional coordinated response |
| `structure_account_price_factor` | sensitivity | yes | Conditional coordinated response |
| `turbine_equipment_price_factor` | sensitivity | yes | Conditional coordinated response |
| `vessel_account_price_factor` | sensitivity | yes | Conditional coordinated response |
| `waste_account_price_factor` | sensitivity | yes | Conditional coordinated response |
| `water_ic1_ua` | search | yes | Finite offered choices only |
| `water_ic2_ua` | search | yes | Finite offered choices only |
| `water_pre_ua` | search | yes | Finite offered choices only |

## Constraint structure

All 125 identities and their full failed-case sets are recoverable from [constraint summary](results/constraint-summary.json). Counts include both branches in each paired assembly. Ranking applies the shared and selected branch predicates; an unused alternative need not pass. Scientific qualification flags remain separate and zero. Every stored point passed numerical verification, including physically inadmissible points.

| Native constraint | Branch | Satisfied | Violated | Other |
|---|---|---:|---:|---:|
| `whole_plant_conversion__plant__compressor_capacity__capacity_ok__add1463eda59a898` | gas | 2436 | 60 | 0 |
| `whole_plant_conversion__plant__cryogenic_demand__cold_margin_w_ok__7dcadae371ddbe6d` | shared | 2444 | 52 | 0 |
| `whole_plant_conversion__plant__cryogenic_demand__domain_supported_ok__e5d086f806f615c2` | shared | 2496 | 0 | 0 |
| `whole_plant_conversion__plant__cryogenic_demand__intercept_margin_w_ok__c8cb8040676afc38` | shared | 2496 | 0 | 0 |
| `whole_plant_conversion__plant__fuel_accounts__domain_supported_ok__94a59fec46208105` | shared | 2496 | 0 | 0 |
| `whole_plant_conversion__plant__fuel_accounts__processing_margin_ok__860e81215fb2b47f` | shared | 2496 | 0 | 0 |
| `whole_plant_conversion__plant__fuel_accounts__stock_margin_ok__84c447972f804892` | shared | 2496 | 0 | 0 |
| `whole_plant_conversion__plant__gas_actual_approach__cold_gap_ok__7e84344c8ebe1f06` | gas | 2496 | 0 | 0 |
| `whole_plant_conversion__plant__gas_actual_approach__hot_gap_ok__5e9b6647fc4988da` | gas | 2496 | 0 | 0 |
| `whole_plant_conversion__plant__gas_boundary__added_dp_margin_ok__cb2dbaa41d101ab2` | gas | 2496 | 0 | 0 |
| `whole_plant_conversion__plant__gas_boundary__bypass_flow_margin_ok__44eb1a31c631c4dc` | gas | 2494 | 2 | 0 |
| `whole_plant_conversion__plant__gas_boundary__bypass_fraction_margin_ok__c17576ed428ad624` | gas | 2496 | 0 | 0 |
| `whole_plant_conversion__plant__gas_boundary__controller_capacity_ok_ok__b340a8d5e92452b2` | gas | 2494 | 2 | 0 |
| `whole_plant_conversion__plant__gas_boundary__exchanger_flow_margin_ok__396e8f7ff4b4cd78` | gas | 2496 | 0 | 0 |
| `whole_plant_conversion__plant__gas_boundary__pressure_margin_ok__57cdec1e34d967ce` | gas | 2496 | 0 | 0 |
| `whole_plant_conversion__plant__gas_boundary__source_adequate_ok__665dcdd55c247bde` | gas | 2016 | 480 | 0 |
| `whole_plant_conversion__plant__gas_boundary__temperature_margin_ok__c3287e1bc91fd77f` | gas | 2496 | 0 | 0 |
| `whole_plant_conversion__plant__gas_boundary__total_flow_margin_ok__b1cac73884dab807` | gas | 2496 | 0 | 0 |
| `whole_plant_conversion__plant__gas_ledger__balance__d86d965fca008ca2` | gas | 1754 | 742 | 0 |
| `whole_plant_conversion__plant__gas_ledger__net_positive__41d28cae11b1dbd6` | gas | 2469 | 27 | 0 |
| `whole_plant_conversion__plant__gas_loss_duty_capacity__capacity_requirement__d56ff09d5df0acbc` | gas | 2496 | 0 | 0 |
| `whole_plant_conversion__plant__gas_loss_electric_capacity__capacity_requirement__ba3fad80f3006552` | gas | 2496 | 0 | 0 |
| `whole_plant_conversion__plant__gas_loss_flow_capacity__capacity_requirement__111ef92c45f0ac07` | gas | 2496 | 0 | 0 |
| `whole_plant_conversion__plant__gas_loss_water__cooling_approach_ok_required__8223dadecc4964f5` | gas | 2496 | 0 | 0 |
| `whole_plant_conversion__plant__gas_operating__annual_net_grid_mwh_ok__1220a0098a3e5f94` | gas | 2361 | 135 | 0 |
| `whole_plant_conversion__plant__gas_operating__auxiliary_margin_mw_ok__15f9aaa632609eef` | gas | 2496 | 0 | 0 |
| `whole_plant_conversion__plant__gas_operating__domain_supported_ok__e50b966764ec28c8` | gas | 2496 | 0 | 0 |
| `whole_plant_conversion__plant__gas_operating__net_export_mw_ok__58d3569ea9297329` | gas | 2362 | 134 | 0 |
| `whole_plant_conversion__plant__gas_overheads__domain_supported_ok__37ebb2bb65f0bc13` | gas | 2496 | 0 | 0 |
| `whole_plant_conversion__plant__gas_whole__domain_supported_ok__bab43aa2eeeee822` | gas | 2496 | 0 | 0 |
| `whole_plant_conversion__plant__gas_whole__economic_defined_ok__5a084f6c1d99295a` | gas | 2361 | 135 | 0 |
| `whole_plant_conversion__plant__gas_whole__outage_margin_ok__25e59eb98c7fca29` | gas | 2471 | 25 | 0 |
| `whole_plant_conversion__plant__generator_capacity__capacity_ok__13f54fade9ec1f3f` | gas | 2496 | 0 | 0 |
| `whole_plant_conversion__plant__he_capacity__capacity_ok__86fcc614bddbfd3c` | gas | 2496 | 0 | 0 |
| `whole_plant_conversion__plant__primary_offer__electric_margin_mw_ok__fbb614dc306d8b9a` | shared | 2496 | 0 | 0 |
| `whole_plant_conversion__plant__primary_offer__flow_margin_kg_s_ok__8bc805379860ec62` | shared | 2496 | 0 | 0 |
| `whole_plant_conversion__plant__primary_offer__inventory_supported_ok__ef44640d09918a5a` | shared | 2496 | 0 | 0 |
| `whole_plant_conversion__plant__primary_offer__pressure_margin_pa_ok__76becfa8174fdcbd` | shared | 2347 | 149 | 0 |
| `whole_plant_conversion__plant__recuperator_duty_capacity__capacity_requirement__751eb0b036d86809` | gas | 2496 | 0 | 0 |
| `whole_plant_conversion__plant__rejection_capacity__capacity_requirement__af7714dda178b8f0` | gas | 2496 | 0 | 0 |
| `whole_plant_conversion__plant__salt_electric_capacity__capacity_requirement__98e5361921299b30` | steam | 2390 | 106 | 0 |
| `whole_plant_conversion__plant__salt_fill_capacity__capacity_requirement__5ccc7cbd0819713b` | steam | 2496 | 0 | 0 |
| `whole_plant_conversion__plant__salt_flow_capacity__capacity_requirement__dd3ff75af1205c2a` | steam | 2390 | 106 | 0 |
| `whole_plant_conversion__plant__salt_shaft_capacity__capacity_requirement__b2367d578fc2f1ec` | steam | 2390 | 106 | 0 |
| `whole_plant_conversion__plant__source_basis__divertor_margin_ok__77e857f8e82a3790` | shared | 2347 | 149 | 0 |
| `whole_plant_conversion__plant__source_basis__domain_supported_ok__a7d99ff729662eb5` | shared | 2496 | 0 | 0 |
| `whole_plant_conversion__plant__source_basis__fusion_envelope_margin_ok__118a84d76a05a76c` | shared | 2496 | 0 | 0 |
| `whole_plant_conversion__plant__source_basis__heating_coupled_margin_ok__26addbd9a09afc2d` | shared | 2496 | 0 | 0 |
| `whole_plant_conversion__plant__source_basis__heating_wall_margin_ok__7038060d9c96b5f8` | shared | 2471 | 25 | 0 |
| `whole_plant_conversion__plant__source_checks__flow_ok__04e751f9ce97000b` | shared | 2496 | 0 | 0 |
| `whole_plant_conversion__plant__source_checks__pressure_ok__e9cb76bbd569aa90` | shared | 2496 | 0 | 0 |
| `whole_plant_conversion__plant__steam_actual_approach__cold_gap_ok__f8487fc350489be6` | steam | 2496 | 0 | 0 |
| `whole_plant_conversion__plant__steam_actual_approach__hot_gap_ok__8e52cd2d280b334c` | steam | 2496 | 0 | 0 |
| `whole_plant_conversion__plant__steam_boundary__added_dp_margin_ok__36cb21eac5ff1b89` | steam | 2496 | 0 | 0 |
| `whole_plant_conversion__plant__steam_boundary__bypass_flow_margin_ok__d79c6541885ab47e` | steam | 2496 | 0 | 0 |
| `whole_plant_conversion__plant__steam_boundary__bypass_fraction_margin_ok__e91d0e0192e4dffd` | steam | 2496 | 0 | 0 |
| `whole_plant_conversion__plant__steam_boundary__controller_capacity_ok_ok__f143197b782aea8e` | steam | 2496 | 0 | 0 |
| `whole_plant_conversion__plant__steam_boundary__exchanger_flow_margin_ok__6737739807166519` | steam | 2496 | 0 | 0 |
| `whole_plant_conversion__plant__steam_boundary__pressure_margin_ok__a08fe8a322365c4f` | steam | 2496 | 0 | 0 |
| `whole_plant_conversion__plant__steam_boundary__source_adequate_ok__d29edbaf0da24311` | steam | 2459 | 37 | 0 |
| `whole_plant_conversion__plant__steam_boundary__temperature_margin_ok__5fbec511bdeb34e1` | steam | 2496 | 0 | 0 |
| `whole_plant_conversion__plant__steam_boundary__total_flow_margin_ok__d3ffa1c793b06886` | steam | 2496 | 0 | 0 |
| `whole_plant_conversion__plant__steam_condensate_electric_capacity__capacity_requirement__b4edc0272db0ccfd` | steam | 2459 | 37 | 0 |
| `whole_plant_conversion__plant__steam_condensate_flow_capacity__capacity_requirement__9f500cb802e73b3a` | steam | 2459 | 37 | 0 |
| `whole_plant_conversion__plant__steam_condensate_pressure_capacity__capacity_requirement__81d8ff0ab723193e` | steam | 2459 | 37 | 0 |
| `whole_plant_conversion__plant__steam_condenser_capacity__capacity_requirement__21565c442e22d191` | steam | 2459 | 37 | 0 |
| `whole_plant_conversion__plant__steam_conditions__supported_required__f55a3b19d079007e` | steam | 2459 | 37 | 0 |
| `whole_plant_conversion__plant__steam_cycle__main_admission_ok_required__9e7307c18ac5420b` | steam | 2496 | 0 | 0 |
| `whole_plant_conversion__plant__steam_cycle__main_ua_available_required__281cb99c36b65283` | steam | 2496 | 0 | 0 |
| `whole_plant_conversion__plant__steam_cycle__reheat_admission_ok_required__46e7006e3a4fafe2` | steam | 2496 | 0 | 0 |
| `whole_plant_conversion__plant__steam_cycle__reheat_ua_available_required__34a9b54f6c90ff27` | steam | 2496 | 0 | 0 |
| `whole_plant_conversion__plant__steam_feed_electric_capacity__capacity_requirement__b9644c9b953bc0ac` | steam | 2459 | 37 | 0 |
| `whole_plant_conversion__plant__steam_feed_flow_capacity__capacity_requirement__5d9d76d0749190a1` | steam | 2459 | 37 | 0 |
| `whole_plant_conversion__plant__steam_feed_pressure_capacity__capacity_requirement__5e891902fcc36704` | steam | 2459 | 37 | 0 |
| `whole_plant_conversion__plant__steam_gross_capacity__capacity_requirement__9cde1cfefe9e4edb` | steam | 2459 | 37 | 0 |
| `whole_plant_conversion__plant__steam_hp_flow_capacity__capacity_requirement__5cc6b8ef933d65f8` | steam | 2459 | 37 | 0 |
| `whole_plant_conversion__plant__steam_hp_shaft_capacity__capacity_requirement__a3fe202eb6d52755` | steam | 2459 | 37 | 0 |
| `whole_plant_conversion__plant__steam_ledger__balance__e1489f8b74e321d3` | steam | 2496 | 0 | 0 |
| `whole_plant_conversion__plant__steam_ledger__net_positive__02f91f11a35b318a` | steam | 2496 | 0 | 0 |
| `whole_plant_conversion__plant__steam_lp_flow_capacity__capacity_requirement__a3fe0741c9ecff1c` | steam | 2459 | 37 | 0 |
| `whole_plant_conversion__plant__steam_lp_shaft_capacity__capacity_requirement__5eb83cc804af4b97` | steam | 2459 | 37 | 0 |
| `whole_plant_conversion__plant__steam_main_ua_capacity__capacity_requirement__7df245597c1c6a96` | steam | 2459 | 37 | 0 |
| `whole_plant_conversion__plant__steam_operating__annual_net_grid_mwh_ok__e95e0d4ecf3512d0` | steam | 2496 | 0 | 0 |
| `whole_plant_conversion__plant__steam_operating__auxiliary_margin_mw_ok__95e4e54a80aa3248` | steam | 2496 | 0 | 0 |
| `whole_plant_conversion__plant__steam_operating__domain_supported_ok__8292960083cc99b1` | steam | 2496 | 0 | 0 |
| `whole_plant_conversion__plant__steam_operating__net_export_mw_ok__f2f015c4f9fa63ae` | steam | 2496 | 0 | 0 |
| `whole_plant_conversion__plant__steam_overheads__domain_supported_ok__79a050b3100a6489` | steam | 2496 | 0 | 0 |
| `whole_plant_conversion__plant__steam_reheat_ua_capacity__capacity_requirement__14e2137308151f37` | steam | 2459 | 37 | 0 |
| `whole_plant_conversion__plant__steam_rejection_capacity__capacity_requirement__550b287c6e69de07` | steam | 2496 | 0 | 0 |
| `whole_plant_conversion__plant__steam_transport__design_motor_base_ok_required__f884c33dd8381ddf` | steam | 2496 | 0 | 0 |
| `whole_plant_conversion__plant__steam_transport__design_motor_factor_ok_required__388250a54e30378f` | steam | 2496 | 0 | 0 |
| `whole_plant_conversion__plant__steam_transport__design_pump_size_ok_required__0aad92e0e5d98e78` | steam | 2496 | 0 | 0 |
| `whole_plant_conversion__plant__steam_transport__design_pump_type_ok_required__9883fd28033f69dd` | steam | 2496 | 0 | 0 |
| `whole_plant_conversion__plant__steam_transport__ihx_capacity_ok_required__98f15d4abb4b4604` | steam | 2459 | 37 | 0 |
| `whole_plant_conversion__plant__steam_transport__motor_base_ok_required__b639a4539ef58c7f` | steam | 2496 | 0 | 0 |
| `whole_plant_conversion__plant__steam_transport__motor_factor_ok_required__c7270c7cda57bab6` | steam | 2444 | 52 | 0 |
| `whole_plant_conversion__plant__steam_transport__pump_size_ok_required__b7783d5e6b21b1ec` | steam | 2496 | 0 | 0 |
| `whole_plant_conversion__plant__steam_transport__pump_type_ok_required__ddc3748fb76b74c1` | steam | 2422 | 74 | 0 |
| `whole_plant_conversion__plant__steam_transport__salt_flow_regime_ok_required__4214cdcb871abc4e` | steam | 2496 | 0 | 0 |
| `whole_plant_conversion__plant__steam_transport__salt_head_ok_required__12b011d2b9b50c5e` | steam | 2496 | 0 | 0 |
| `whole_plant_conversion__plant__steam_water__cooling_approach_ok_required__8456fcd9f50ebe3a` | steam | 2496 | 0 | 0 |
| `whole_plant_conversion__plant__steam_water_electric_capacity__capacity_requirement__e3f37a33f8f86544` | steam | 2496 | 0 | 0 |
| `whole_plant_conversion__plant__steam_water_flow_capacity__capacity_requirement__682b9c0979ad7556` | steam | 2496 | 0 | 0 |
| `whole_plant_conversion__plant__steam_whole__domain_supported_ok__d85812a4b8cd9e3f` | steam | 2496 | 0 | 0 |
| `whole_plant_conversion__plant__steam_whole__economic_defined_ok__aec3d165702acb63` | steam | 2496 | 0 | 0 |
| `whole_plant_conversion__plant__steam_whole__outage_margin_ok__90418a10014fb429` | steam | 2471 | 25 | 0 |
| `whole_plant_conversion__plant__supplied_core__current_margin_ok__c67cdc1d2fb0a885` | shared | 2496 | 0 | 0 |
| `whole_plant_conversion__plant__supplied_core__field_margin_t_ok__4c34d4933dff04fb` | shared | 2496 | 0 | 0 |
| `whole_plant_conversion__plant__supplied_core__fit_margin_ok__d3fcebf466168c53` | shared | 2496 | 0 | 0 |
| `whole_plant_conversion__plant__supplied_core__identity_supported_ok__121f94d9fa90b835` | shared | 2496 | 0 | 0 |
| `whole_plant_conversion__plant__supplied_core__strain_margin_ok__2d8a80d5407aa7bd` | shared | 2496 | 0 | 0 |
| `whole_plant_conversion__plant__supplied_core__stress_margin_pa_ok__edd9f45610c1547b` | shared | 2496 | 0 | 0 |
| `whole_plant_conversion__plant__turbine_capacity__capacity_ok__ee860596098e7f44` | gas | 2496 | 0 | 0 |
| `whole_plant_conversion__plant__water_ic1__duty_margin_ok__dfd546f8f5ee868f` | gas | 2496 | 0 | 0 |
| `whole_plant_conversion__plant__water_ic1__evaluation_defined_ok__1371e750cffff108` | gas | 2121 | 375 | 0 |
| `whole_plant_conversion__plant__water_ic1__flow_margin_ok__1dd1c3a1e5784553` | gas | 2488 | 8 | 0 |
| `whole_plant_conversion__plant__water_ic1__power_margin_ok__5b880ab5fc02b1dc` | gas | 2488 | 8 | 0 |
| `whole_plant_conversion__plant__water_ic2__duty_margin_ok__143f9ca6200e6779` | gas | 2496 | 0 | 0 |
| `whole_plant_conversion__plant__water_ic2__evaluation_defined_ok__b931519f56a159d1` | gas | 2121 | 375 | 0 |
| `whole_plant_conversion__plant__water_ic2__flow_margin_ok__6696de4f3ee21d56` | gas | 2488 | 8 | 0 |
| `whole_plant_conversion__plant__water_ic2__power_margin_ok__4251efdd4ccb0c52` | gas | 2488 | 8 | 0 |
| `whole_plant_conversion__plant__water_pre__duty_margin_ok__43a051525223b723` | gas | 2496 | 0 | 0 |
| `whole_plant_conversion__plant__water_pre__evaluation_defined_ok__84c4b3b2eb329ee0` | gas | 1839 | 657 | 0 |
| `whole_plant_conversion__plant__water_pre__flow_margin_ok__e81a241fb624b075` | gas | 2484 | 12 | 0 |
| `whole_plant_conversion__plant__water_pre__power_margin_ok__88cf3aa259145f02` | gas | 2487 | 9 | 0 |

## Findings carried forward

The [final review](supporting/final-results-review.md) accepts the stated scope and dispositions. This executor reading proposes carrying them forward unchanged; formal closure remains owner-held.

| Finding | Recorded issue | Proposed disposition |
|---|---|---|
| 20260927-design-study-whole-plant-conversion-b#1 | The common source is supplied; plasma sustainment and global manufactured fit are not qualified. | Declared seam: retain this condition at every whole-plant conclusion; no reactor qualification claim. |
| 20260927-design-study-whole-plant-conversion-b#2 | The selected primary and divertor offers cannot support the 3000 MW source condition. | Declared seam: preserve failed cases and exclude this source from paired preference; no automatic hardware resizing. |
| 20260927-design-study-whole-plant-conversion-b#3 | Transferred nuclear heating is not a validated bound for the changed magnet/blanket geometry. | Declared seam: vary demand at fixed cryoplant and retain the native capacity bracket; updated transport remains future research. |
| 20260927-design-study-whole-plant-conversion-b#4 | Generated descriptive CAS codes disagree with the accepted account categories; executable membership is correct. | Declared seam: use the explicit reviewed mapping for this report; correct metadata before using generic CAS rollups. |
| 20260927-design-study-whole-plant-conversion-b#5 | The finite equipment window has uncaught edges and the technologies have different modeled operating freedoms. | Declared seam: report finite-catalog minima and conditional scenarios; no equal global technology optimization claim. |
| 20260927-design-study-whole-plant-conversion-b#6 | The first oracle scan overlapped in-place regeneration and read temporarily absent input defaults. | Corrected execution: retain invalid scan, serialize regeneration and scanning, and use the zero-refusal replacement scan. |
| 20260927-design-study-whole-plant-conversion-b#7 | The static validator reports inherited literal/alias diagnostics on the compiled assembly. | Declared seam: retain raw exit1 and reviewed identity-level dispositions with zero unresolved diagnostics; do not call static validation green. |
| 20260927-design-study-whole-plant-conversion-b#8 | Equipment price and common reactor account stresses are explicit assumptions rather than established market uncertainty intervals. | Declared seam: report conditional preference and native thresholds; do not present engineered endpoints as credible confidence bounds. |
| 20260927-design-study-whole-plant-conversion-b#9 | Independent high-precision adjudication found that the cooler oracle stopped too early at one near-pinch failed offer. | Model fix: independently reviewed tighter Brent convergence; original failure retained, controls and replacement study require unchanged acceptance tolerances. |
| 20260927-design-study-whole-plant-conversion-b#10 | The original ±1e-5 W/m³ cryogenic bracket produced nearly cancelled margins that failed relative verification. | Declared seam: preserve the failed first record; use the separately reviewed ±0.01 W/m³ diagnostic resolution and retain both sides of the native capacity failure. |

## What the record does not support

The record supports a numerically verified conditional whole-plant comparison. It does not establish plasma sustainment, updated neutron transport, manufactured global reactor fit, vendor qualification, empirical price confidence bounds, equal global optimization freedoms or a passing 3,000 MW plant. Static validation retains explicitly reviewed diagnostics. Original source PDFs and the complete historical predecessor/failed-study stores are not bundled, as disclosed in record section 17. The recorded receipts preserve their stated narrower scope.

No required study fact was missing from this reading. [Replay instructions](REPLAY.md) specify a fresh complete execution; this synthesis does not claim to have run that command. The [native replay comparison](results/native-replay-comparison.json) separately records exact agreement with earlier native executions.
