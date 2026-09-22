# Native cost results

[AGENT executor] All amounts below are read from stored native outputs. Differences and ordering summarize these outputs; no caller recomputes plant costs. Money is USD2004. Capital, annual operating expense, lifetime scheduled replacements and the alternative annual reserve are separate boundaries.

## Baseline and leaf contributions

| Metric | Native value |
| --- | ---: |
| net_MW | 423.106794109 |
| unmet_MW | 0 |
| direct_USD2004 | 2919603000 |
| overnight_USD2004 | 4350208470 |
| annual_operating_USD2004 | 3215100712.86 |
| annual_export_MWh | 3150453.18894 |
| annual_T_USD2004 | 3140031210.7 |
| annual_external_T_kg | 104.667707023 |
| annual_OM_USD2004 | 70000000 |
| annual_D_USD2004 | 69502.1597304 |
| annual_import_USD2004 | 0 |
| replacement_event_USD2004 | 72231350 |
| replacement_events | 6 |
| replacement_interval_years | 5.88235294118 |
| replacement_last_year | 35.2941176471 |
| lifetime_replacement_USD2004 | 433388100 |
| annual_reserve_USD2004 | 12279329.5 |
| source_direct_USD2004 | 2619572000 |
| source_inclusive_USD2004 | 5055773960 |
| he_hx_USD2004 | 58325700 |
| he_UA_MW_K | 50 |

The following 39 purchase leaves include initial tritium stock once. Their order is contribution size, not evidence of price certainty. Source eight-parent comparison amounts are excluded from this purchase list.

| Purchased owner | Native USD2004 |
| --- | ---: |
| facilities | 336133000 |
| fuel_inventory | 300000000 |
| shield_inventory | 228627000 |
| magnet_inventory | 204208000 |
| lipb_inventory | 151327000 |
| electrical_equipment | 138764000 |
| vacuum_equipment | 137135000 |
| turbine_equipment | 125823200 |
| secondary_transport | 85933000 |
| compressor_equipment | 78639500 |
| primary_support | 73126000 |
| miscellaneous_equipment | 70958000 |
| magnet_power_supplies | 70624000 |
| heating_equipment | 66427000 |
| conversion_services | 62911600 |
| other_reactor_equipment | 60723000 |
| blanket_inventory | 59347000 |
| divertor_hx | 58325700 |
| he_hx | 58325700 |
| pbli_hx | 58325700 |
| primary_piping | 58325700 |
| heat_rejection_equipment | 56086000 |
| generator_equipment | 47183700 |
| instrumentation_control | 44558000 |
| fuel_services | 38689000 |
| divertor_duty_equipment | 32403166.6667 |
| he_duty_equipment | 32403166.6667 |
| pbli_duty_equipment | 32403166.6667 |
| unallocated_source_scope | 28396000 |
| divertor_pump | 19441900 |
| he_pump | 19441900 |
| pbli_pump | 19441900 |
| fuel_processing_equipment | 16590000 |
| vf_coils | 13358000 |
| site_land | 12929000 |
| waste_equipment | 6655000 |
| impurity_control | 6561000 |
| divertor_inventory | 5318000 |
| auxiliary_cooling | 3735000 |

## One-factor finite changes

All 100 economic endpoint rows compare against the same baseline. Windows differ, so absolute delta rankings reflect these assumptions and window sizes. No derivative, probability, optimum or generalized monotonicity is established.

| Case | Δ overnight USD2004 | Δ annual operating USD2004/year | Δ lifetime replacements USD2004 |
| --- | ---: | ---: | ---: |
| auxiliary_cooling_price-low | -2782575 | 0 | 0 |
| auxiliary_cooling_price-high | 2782575 | 0 | 0 |
| blanket_inventory_price-low | -44213515 | 0 | -178041000 |
| blanket_inventory_price-high | 44213515 | 0 | 178041000 |
| compressor_equipment_price-low | -58586427.5 | 0 | 0 |
| compressor_equipment_price-high | 58586427.5 | 0 | 0 |
| conversion_services_price-low | -46869142 | 0 | 0 |
| conversion_services_price-high | 46869142 | 0 | 0 |
| divertor_duty_equipment_price-low | -24140359.1667 | 0 | 0 |
| divertor_duty_equipment_price-high | 24140359.1667 | 0 | 0 |
| divertor_hx_price-low | -43452646.5 | 0 | 0 |
| divertor_hx_price-high | 43452646.5 | 0 | 0 |
| divertor_inventory_price-low | -3961910 | 0 | -15954000 |
| divertor_inventory_price-high | 3961910 | 0 | 15954000 |
| divertor_pump_price-low | -14484215.5 | 0 | 0 |
| divertor_pump_price-high | 14484215.5 | 0 | 0 |
| electrical_equipment_price-low | -103379180 | 0 | 0 |
| electrical_equipment_price-high | 103379180 | 0 | 0 |
| facilities_price-low | -250419085 | 0 | 0 |
| facilities_price-high | 250419085 | 0 | 0 |
| fuel_processing_equipment_price-low | -12359550 | 0 | 0 |
| fuel_processing_equipment_price-high | 12359550 | 0 | 0 |
| fuel_services_price-low | -28823305 | 0 | 0 |
| fuel_services_price-high | 28823305 | 0 | 0 |
| generator_equipment_price-low | -35151856.5 | 0 | 0 |
| generator_equipment_price-high | 35151856.5 | 0 | 0 |
| he_duty_equipment_price-low | -24140359.1667 | 0 | 0 |
| he_duty_equipment_price-high | 24140359.1667 | 0 | 0 |
| he_hx_price-low | -43452646.5 | 0 | 0 |
| he_hx_price-high | 43452646.5 | 0 | 0 |
| he_pump_price-low | -14484215.5 | 0 | 0 |
| he_pump_price-high | 14484215.5 | 0 | 0 |
| heat_rejection_equipment_price-low | -41784070 | 0 | 0 |
| heat_rejection_equipment_price-high | 41784070 | 0 | 0 |
| heating_equipment_price-low | -49488115 | 0 | 0 |
| heating_equipment_price-high | 49488115 | 0 | 0 |
| impurity_control_price-low | -4887945 | 0 | 0 |
| impurity_control_price-high | 4887945 | 0 | 0 |
| instrumentation_control_price-low | -33195710 | 0 | 0 |
| instrumentation_control_price-high | 33195710 | 0 | 0 |
| lipb_inventory_price-low | -112738615 | 0 | -22699050 |
| lipb_inventory_price-high | 112738615 | 0 | 22699050 |
| magnet_inventory_price-low | -152134960 | 0 | 0 |
| magnet_inventory_price-high | 152134960 | 0 | 0 |
| magnet_power_supplies_price-low | -52614880 | 0 | 0 |
| magnet_power_supplies_price-high | 52614880 | 0 | 0 |
| miscellaneous_equipment_price-low | -52863710 | 0 | 0 |
| miscellaneous_equipment_price-high | 52863710 | 0 | 0 |
| other_reactor_equipment_price-low | -45238635 | 0 | 0 |
| other_reactor_equipment_price-high | 45238635 | 0 | 0 |
| pbli_duty_equipment_price-low | -24140359.1667 | 0 | 0 |
| pbli_duty_equipment_price-high | 24140359.1667 | 0 | 0 |
| pbli_hx_price-low | -43452646.5 | 0 | 0 |
| pbli_hx_price-high | 43452646.5 | 0 | 0 |
| pbli_pump_price-low | -14484215.5 | 0 | 0 |
| pbli_pump_price-high | 14484215.5 | 0 | 0 |
| primary_piping_price-low | -43452646.5 | 0 | 0 |
| primary_piping_price-high | 43452646.5 | 0 | 0 |
| primary_support_price-low | -54478870 | 0 | 0 |
| primary_support_price-high | 54478870 | 0 | 0 |
| secondary_transport_price-low | -64020085 | 0 | 0 |
| secondary_transport_price-high | 64020085 | 0 | 0 |
| shield_inventory_price-low | -170327115 | 0 | 0 |
| shield_inventory_price-high | 170327115 | 0 | 0 |
| site_land_price-low | -9632105 | 0 | 0 |
| site_land_price-high | 9632105 | 0 | 0 |
| turbine_equipment_price-low | -93738284 | 0 | 0 |
| turbine_equipment_price-high | 93738284 | 0 | 0 |
| unallocated_source_scope_price-low | -21155020 | 0 | 0 |
| unallocated_source_scope_price-high | 42310040 | 0 | 0 |
| vacuum_equipment_price-low | -102165575 | 0 | 0 |
| vacuum_equipment_price-high | 102165575 | 0 | 0 |
| vf_coils_price-low | -9951710 | 0 | 0 |
| vf_coils_price-high | 9951710 | 0 | 0 |
| waste_equipment_price-low | -4957975 | 0 | 0 |
| waste_equipment_price-high | 4957975 | 0 | 0 |
| fuel_inventory_tritium_price-low | -298000000 | -2093354140.46 | 0 |
| fuel_inventory_tritium_price-high | 1043000000 | 7326739491.63 | 0 |
| fuel_inventory_selected_tritium_kg-low | -402300000 | -15179923.2543 | 0 |
| fuel_inventory_selected_tritium_kg-high | 894000000 | 33733162.7873 | 0 |
| fuel_inventory_deuterium_price-low | 0 | -62551.9437575 | 0 |
| fuel_inventory_deuterium_price-high | 0 | 625519.437574 | 0 |
| annual_om_selected_amount-low | 0 | -35000000 | 0 |
| annual_om_selected_amount-high | 0 | 70000000 | 0 |
| cost_ledger_consumables-low | 0 | -4000000 | 0 |
| cost_ledger_consumables-high | 0 | 10000000 | 0 |
| indirect_cost_fraction-low | -350352360 | 0 | 0 |
| indirect_cost_fraction-high | 350352360 | 0 | 0 |
| contingency_fraction-low | -350352360 | 0 | 0 |
| contingency_fraction-high | 700704720 | 0 | 0 |
| owner_commissioning_fraction-low | -87588090 | 0 | 0 |
| owner_commissioning_fraction-high | 145980150 | 0 | 0 |
| cost_schedule_replacement_life_fpy-low | 0 | 0 | 722313500 |
| cost_schedule_replacement_life_fpy-high | 0 | 0 | -144462700 |
| cost_schedule_replacement_factor-low | 0 | 0 | -216694050 |
| cost_schedule_replacement_factor-high | 0 | 0 | 433388100 |
| cost_schedule_lipb_makeup_fraction-low | 0 | 0 | -45398100 |
| cost_schedule_lipb_makeup_fraction-high | 0 | 0 | 136194300 |
| cost_schedule_availability-low | 0 | -551158964.376 | -72231350 |
| cost_schedule_availability-high | 0 | 367439309.584 | 72231350 |

## Recovery, mode and combined scenarios

Supplied recovery has no incremental recovery-cost or qualification law at fixed installed scope. It is an independently supplied boundary scenario, not purchased-capability optimization. Combined corners coordinate the declared assumptions; they are not probability bounds. No-credit and 100 kg/year boundaries remain separate.

| Case | Overnight USD2004 | Annual operating USD2004/year | External T kg/year | Lifetime replacement USD2004 | Alternative reserve USD2004/year |
| --- | ---: | ---: | ---: | ---: | ---: |
| recovery-100 | 4350208470 | 215100712.857 | 4.66770702325 | 433388100 | 12279329.5 |
| recovery-200 | 4350208470 | 75069502.1597 | 0 | 433388100 | 12279329.5 |
| fixed-budget-nominal | 4350208470 | 3215100712.86 | 104.667707023 | 433388100 | 12279329.5 |
| adequate-area-mode-0 | 4393661116.5 | 3215100712.86 | 104.667707023 | 433388100 | 12279329.5 |
| adequate-area-mode-1 | 4350208470 | 3215100712.86 | 104.667707023 | 433388100 | 12279329.5 |
| combined-low-recovery-0 | 1623355845 | 893907253.092 | 85.7901529385 | 48498750 | 1414546.875 |
| combined-low-recovery-100 | 1623355845 | 36005723.7073 | 0 | 48498750 | 1414546.875 |
| combined-high-recovery-0 | 13331716800 | 11959761810 | 118.039850211 | 5126241600 | 135275820 |
| combined-high-recovery-100 | 13331716800 | 1959761809.99 | 18.0398502115 | 5126241600 | 135275820 |

## Observed sampled ranges

These extrema describe only the 110 sampled assumed-baseline points. The three source-conditioned failing controls are excluded. They are not guarantees over the continuous input window.

| Metric | Observed minimum | Case | Observed maximum | Case |
| --- | ---: | --- | ---: | --- |
| direct_USD2004 | 1319801500 | combined-low-recovery-0 | 6943602500 | combined-high-recovery-0 |
| overnight_USD2004 | 1623355845 | combined-low-recovery-0 | 13331716800 | combined-high-recovery-0 |
| annual_operating_USD2004 | 36005723.7073 | combined-low-recovery-100 | 11959761810 | combined-high-recovery-0 |
| lifetime_replacement_USD2004 | 48498750 | combined-low-recovery-0 | 5126241600 | combined-high-recovery-0 |
| annual_reserve_USD2004 | 1414546.875 | combined-low-recovery-0 | 135275820 | combined-high-recovery-0 |

## Constraints and support

All conditional baseline-family points retain the same net output and zero import cost; import-tariff sensitivity is unexercised. The unchanged source-conditioned failures are diagnostic controls with incomplete/constraint-failing net values, not usable generating alternatives. All scientific support flags remain zero.

| Exact constraint | Status counts |
| --- | --- |
| `aries_integrated_plant__compressor_capacity__capacity_ok__a45f9cf05e8aa7ab` | {'satisfied': 113} |
| `aries_integrated_plant__divertor_capacity__capacity_ok__be7081920ad8e8ed` | {'satisfied': 113} |
| `aries_integrated_plant__divertor_pump__capacity_ok__d6730c7060447f4c` | {'satisfied': 113} |
| `aries_integrated_plant__fuel_capacity__capacity_ok__8eb5888bfe62cd64` | {'satisfied': 113} |
| `aries_integrated_plant__fuel_inventory__capacity_ok__37f4667fbfb616d0` | {'satisfied': 113} |
| `aries_integrated_plant__generator_capacity__capacity_ok__60b43f15d48ff161` | {'satisfied': 113} |
| `aries_integrated_plant__he_capacity__capacity_ok__db2733d1d5baf3cf` | {'satisfied': 113} |
| `aries_integrated_plant__he_pump__capacity_ok__fcee5ee009fe5180` | {'satisfied': 113} |
| `aries_integrated_plant__pbli_capacity__capacity_ok__55a012a287da9395` | {'satisfied': 113} |
| `aries_integrated_plant__pbli_pump__capacity_ok__79d116aa320dd4fb` | {'satisfied': 113} |
| `aries_integrated_plant__plant_ledger__balances_ok__9af2e85b5e4e5535` | {'satisfied': 112, 'violated': 1} |
| `aries_integrated_plant__plant_ledger__heat_removal_ok__695378663bcd8d07` | {'satisfied': 110, 'violated': 3} |
| `aries_integrated_plant__rejection_capacity__capacity_ok__295420bc9fb25608` | {'satisfied': 113} |
| `aries_integrated_plant__turbine_capacity__capacity_ok__089f9e8e61919ec1` | {'satisfied': 113} |
