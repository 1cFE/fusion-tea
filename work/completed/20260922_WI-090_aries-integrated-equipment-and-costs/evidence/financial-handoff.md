# Prompt 03 financial handoff: native owner and channel map

[AGENT] This map describes the delivered assumed integrated baseline, `nominal-calculated`. Every baseline number below is read directly from [baseline-execution.json](baseline-execution.json), including public inputs and native outputs. It introduces no prices, equations, economic ranking or new modeling decisions. The uncertainty ranges retain their [AGENT] status from [design.md](../design.md), assumptions E1–E10.

The executable fingerprint is `01f8f89c42a98621ff4c6868156d9b7938b7c80102f1c8321b35504ffcc7a021`. Full scenario inputs and entry groups are in the same receipt. All money is USD2004; capital is dollars, annual expenses are dollars per calendar year, and import price is dollars per MWh. Numeric values preserve the recorded floating-point precision. Quantities remain selected hardware or declared scenario inputs unless explicitly labeled calculated.

## Capital boundary

Use the provisional overnight output as its declared overnight scenario. The printed source direct and inclusive figures are separate comparison alternatives. The source inclusive factor includes financing/escalation and cannot be relabeled overnight or added to the provisional capital. Initial T stock and initial LiPb already belong to direct capital. Source child discrepancies remain explicit; they are not installation estimates.

| Quantity | Exact native output ID and baseline USD2004 | Scope |
| --- | --- | --- |
| Selected source-scope direct subtotal | `aries_integrated_plant__direct_source_scope__evaluate__total` = 2619603000 | Before initial T stock; includes the declared core discrepancy. |
| Initial T stock | `aries_integrated_plant__fuel_inventory__purchase__amount` = 300000000 | Included once in provisional direct capital; purchased stock, not recurring throughput. |
| Provisional direct | `aries_integrated_plant__cost_ledger__evaluate__direct` = 2919603000 | Includes all selected capital leaves and initial T stock. |
| Indirect | `aries_integrated_plant__indirect_cost__evaluate__cost` = 583920600 | Separate addition to direct. |
| Contingency | `aries_integrated_plant__contingency__evaluate__cost` = 700704720 | Separate addition on the declared direct-plus-indirect basis. |
| Owner/commissioning | `aries_integrated_plant__owner_commissioning__evaluate__amount` = 145980150 | Separate allowance; not an independently sourced breakdown. |
| Provisional overnight | `aries_integrated_plant__cost_ledger__evaluate__overnight` = 4350208470 | Direct plus the preceding additions; excludes financing/escalation. |
| Printed source direct | `aries_integrated_plant__source_budget__evaluate__direct_total` = 2619572000 | Eight printed parents only; do not add selected detail. |
| Source inclusive | `aries_integrated_plant__source_budget__evaluate__inclusive_capital` = 5055773960 | Source comparison containing interest/escalation and other inclusive additions. |
| Provisional-minus-source direct | `aries_integrated_plant__cost_ledger__evaluate__direct_difference` = 300031000 | Diagnostic difference; not another expense. |

The source comparison parent controls are independent of selected equipment prices. Changing one changes source comparisons, not the selected inventory or its purchase estimate.

| Source scope | Exact public parameter key and baseline USD2004 |
| --- | --- |
| 20 land | `aries_integrated_plant__source_budget__account_1` = 12929000 |
| 21 facilities | `aries_integrated_plant__source_budget__account_2` = 336133000 |
| 22 reactor equipment | `aries_integrated_plant__source_budget__account_3` = 1538817000 |
| 23 turbine plant | `aries_integrated_plant__source_budget__account_4` = 314558000 |
| 24 electric plant | `aries_integrated_plant__source_budget__account_5` = 138764000 |
| 25 miscellaneous | `aries_integrated_plant__source_budget__account_6` = 70958000 |
| 26 special materials/LiPb | `aries_integrated_plant__source_budget__account_7` = 151327000 |
| 27 heat rejection | `aries_integrated_plant__source_budget__account_8` = 56086000 |
| Inclusive multiplier, dimensionless | `aries_integrated_plant__source_budget__inclusive_multiplier` = 1.9299999999999999 |

## Annual operating amounts and export

Annual operating total already contains O&M, external T purchase, deuterium, the consumables allowance and any imported electricity. Do not add its component channels again. Recirculating electric demands already reduce net export; they are not a second positive-operation electricity bill. The zero-recovery-credit baseline is a deliberately pessimistic supplied boundary, not a prediction of zero breeding.

| Quantity | Exact native output ID and recorded baseline | Units / treatment |
| --- | --- | --- |
| Annual operating total | `aries_integrated_plant__cost_ledger__evaluate__annual_operating` = 3215100712.8571219 | USD2004/year; excludes scheduled replacement |
| Fixed annual O&M | `aries_integrated_plant__annual_om__evaluate__annual_om` = 70000000 | USD2004/year; excludes fuel, replacement and depreciation |
| External T purchase cost | `aries_integrated_plant__fuel_inventory__annual__annual_cost` = 3140031210.6973915 | USD2004/year |
| Deuterium purchase cost | `aries_integrated_plant__fuel_inventory__deuterium__annual_fuel` = 69502.159730437081 | USD2004/year; no LiPb double count |
| External T requirement | `aries_integrated_plant__fuel_inventory__annual__annual_external` = 104.66770702324638 | kg/year |
| T burn | `aries_integrated_plant__fuel_inventory__annual__annual_burn` = 87.483603061730122 | kg/year, productive time |
| T unrecovered loss | `aries_integrated_plant__fuel_inventory__annual__annual_loss` = 16.621884581728743 | kg/year, productive time |
| T stock decay | `aries_integrated_plant__fuel_inventory__annual__annual_decay` = 0.56221937978751124 | kg/year, all calendar time |
| Supplied annual T recovery | `aries_integrated_plant__fuel_inventory__annual__annual_recovery` = 0 | kg/year; explicit supply boundary, breeding unsupported |
| Net electric export | `aries_integrated_plant__plant_ledger__evaluate__net_electric` = 423.10679410931664 | MW; assumed integrated baseline |
| Annual export | `aries_integrated_plant__cost_ledger__evaluate__annual_export_mwh` = 3150453.1889379714 | MWh/year |
| Annual import | `aries_integrated_plant__cost_ledger__evaluate__annual_import_mwh` = 0 | MWh/year; distinct from export |
| Annual import cost | `aries_integrated_plant__cost_ledger__evaluate__annual_import_cost` = 0 | USD2004/year; already included in annual operating total |

Consumables have an input owner but no standalone named output: `aries_integrated_plant__cost_ledger__consumables` = 5000000 USD2004/year. The native annual total consumes this amount directly. Availability is `aries_integrated_plant__cost_schedule__availability` = 0.84999999999999998 and import price is `aries_integrated_plant__cost_ledger__import_price` = 50 USD2004/MWh. These exact public keys, rather than a fabricated output alias, are the handoff for those selections.

## Replacement and calendar boundary

The nominal event schedule and annual reserve are alternative financial representations. Use event count, interval and per-event cost, or use the reserve; do not charge both. Initial purchase is excluded, as is an event exactly at the selected end of plant life. Nominal replacement scope is blanket/divertor plus selected LiPb makeup, not all permanent plant inventory. The printed source replacement comparison is a diagnostic alternative, not an additional expense.

| Quantity | Exact native output ID and baseline | Units |
| --- | --- | --- |
| Event cost | `aries_integrated_plant__replacement__evaluate__event_cost` = 72231350 | USD2004/event |
| Event interval | `aries_integrated_plant__replacement__evaluate__interval_years` = 5.882352941176471 | calendar years |
| Event count | `aries_integrated_plant__replacement__evaluate__event_count` = 6 | count |
| First event | `aries_integrated_plant__replacement__evaluate__first_event_year` = 5.882352941176471 | calendar year |
| Last event | `aries_integrated_plant__replacement__evaluate__last_event_year` = 35.294117647058826 | calendar year |
| Undiscounted lifetime replacement | `aries_integrated_plant__replacement__evaluate__lifetime_total` = 433388100 | USD2004 |
| Annual replacement reserve | `aries_integrated_plant__replacement__evaluate__annual_reserve` = 12279329.5 | USD2004/year |

Schedule controls: `aries_integrated_plant__cost_schedule__plant_years` = 40 calendar years; `aries_integrated_plant__cost_schedule__replacement_life_fpy` = 5 full-power years; `aries_integrated_plant__cost_schedule__replacement_factor` = 1 event price factor; `aries_integrated_plant__cost_schedule__lipb_makeup_fraction` = 0.050000000000000003 fraction of selected LiPb inventory per event. Availability uses the single key listed above; it is an assumed productive fraction, not a reliability prediction.

| Source diagnostic | Exact native output ID and baseline |
| --- | --- |
| Rounded source lifetime replacement USD2004 | `aries_integrated_plant__source_replacement_comparison__cost__amount` = 975000000 |
| Source replacement lifetime mass kg | `aries_integrated_plant__source_replacement_comparison__mass__amount` = 10946000 |
| Rounded-minus-printed replacement USD2004 | `aries_integrated_plant__source_replacement_comparison__evaluate__difference` = 9000000 |
| Known dry-mass-minus-printed source kg | `aries_integrated_plant__inventory_comparison__evaluate__difference` = 1333700 |
| VF-coil mass availability flag | `aries_integrated_plant__inventory_comparison__support__amount` = 0 |
| LiPb material-price-minus-source USD2004 | `aries_integrated_plant__lipb_comparison__evaluate__difference` = -334000 |
| Fuel account parent-minus-children USD2004 | `aries_integrated_plant__source_reconciliation__fuel_gap_calc__difference` = 1000 |

## Selected inventory and capability ownership

Selected quantities do not resize from operating demand. The blanket mass includes the blanket/divertor/FW/back aggregate; the divertor target package does not add a second mass. VF mass and conductor composition remain unavailable. LiPb belongs once to special-material inventory, with only the declared fraction entering replacements.

| Selected owner | Exact public parameter key and baseline | Units |
| --- | --- | --- |
| Modular winding pack | `aries_integrated_plant__magnet_inventory__selected_winding_mass` = 627200 | kg |
| Modular structure | `aries_integrated_plant__magnet_inventory__selected_structure_mass` = 3465000 | kg |
| Blanket/divertor aggregate | `aries_integrated_plant__blanket_inventory__selected_mass` = 662500 | kg |
| Shield/back | `aries_integrated_plant__shield_inventory__selected_shield_mass` = 3280000 | kg |
| Manifold | `aries_integrated_plant__shield_inventory__selected_manifold_mass` = 1305000 | kg |
| Vessel | `aries_integrated_plant__vacuum_equipment__selected_vessel_mass` = 1440000 | kg |
| Cryostat | `aries_integrated_plant__vacuum_equipment__selected_cryostat_mass` = 1333000 | kg |
| Primary support | `aries_integrated_plant__primary_support__selected_mass` = 2909000 | kg |
| LiPb core | `aries_integrated_plant__lipb_inventory__selected_core_mass` = 3532000 | kg |
| LiPb external multiplier | `aries_integrated_plant__lipb_inventory__external_mass_factor` = 2.5 | dimensionless total multiplier |
| Selected T stock | `aries_integrated_plant__fuel_inventory__selected_tritium_kg` = 10 | kg |
| Divertor target package | `aries_integrated_plant__divertor_inventory__selected_quantity` = 1 | one package |
| VF-coil package | `aries_integrated_plant__vf_coils__selected_quantity` = 1 | one package |

| Calculated inventory / stock diagnostic | Exact native output ID and baseline | Units |
| --- | --- | --- |
| Modular winding plus structure | `aries_integrated_plant__magnet_inventory__inventory__total` = 4092200 | kg |
| Shield plus manifolds | `aries_integrated_plant__shield_inventory__inventory__total` = 4585000 | kg |
| Vessel plus cryostat | `aries_integrated_plant__vacuum_equipment__inventory__total` = 2773000 | kg |
| Total LiPb | `aries_integrated_plant__lipb_inventory__inventory__amount` = 8830000 | kg |
| Selected stock in atoms | `aries_integrated_plant__fuel_inventory__atoms__atoms` = 1.9966983940220532e+27 | T atoms |
| Required processing-hold stock | `aries_integrated_plant__fuel_inventory__annual__required_stock` = 0.062009000289971965 | kg; limited processing screen |
| Stock adequacy margin | `aries_integrated_plant__fuel_inventory__screen__margin` = 9.9379909997100278 | kg |
| Required breeding diagnostic | `aries_integrated_plant__fuel__evaluate__tbr_required` = 1.1954625833424144 | ratio; does not establish achieved breeding |

### Blanket helium thermal equipment

| Role | Exact key / output ID and baseline | Units |
| --- | --- | --- |
| Selected exchanger area | `aries_integrated_plant__he_hx__selected_area` = 50000 | m²; price follows purchased area |
| Assumed heat-transfer coefficient | `aries_integrated_plant__he_hx__assumed_u` = 1000 | W/(m² K); uncertainty leaves area fixed |
| Calculated conductance | `aries_integrated_plant__he_hx__evaluate__ua` = 50 | MW/K |
| Selected pump capacity | `aries_integrated_plant__he_pump__selected_flow_capacity` = 3261 | kg/s |
| Operating flow | `aries_integrated_plant__heat_exchangers__he_flow` = 3261 | kg/s; separate from purchased capacity |
| Pump efficiency | `aries_integrated_plant__he_pump__efficiency` = 0.80000000000000004 | dimensionless assumed operating characteristic |
| Pump capacity margin | `aries_integrated_plant__he_pump__screen__margin` = 0 | kg/s |
| Pump electrical demand | `aries_integrated_plant__he_pump__evaluate__electric` = 156 | MW; enters net power and recovered heat |

### LiPb thermal equipment

| Role | Exact key / output ID and baseline | Units |
| --- | --- | --- |
| Selected exchanger area | `aries_integrated_plant__pbli_hx__selected_area` = 50000 | m²; price follows purchased area |
| Assumed heat-transfer coefficient | `aries_integrated_plant__pbli_hx__assumed_u` = 1000 | W/(m² K); uncertainty leaves area fixed |
| Calculated conductance | `aries_integrated_plant__pbli_hx__evaluate__ua` = 50 | MW/K |
| Selected pump capacity | `aries_integrated_plant__pbli_pump__selected_flow_capacity` = 26860 | kg/s |
| Operating flow | `aries_integrated_plant__heat_exchangers__pbli_flow` = 26860 | kg/s; separate from purchased capacity |
| Pump efficiency | `aries_integrated_plant__pbli_pump__efficiency` = 0.80000000000000004 | dimensionless assumed operating characteristic |
| Pump capacity margin | `aries_integrated_plant__pbli_pump__screen__margin` = 0 | kg/s |
| Pump electrical demand | `aries_integrated_plant__pbli_pump__evaluate__electric` = 0.01 | MW; enters net power and recovered heat |

### Divertor helium thermal equipment

| Role | Exact key / output ID and baseline | Units |
| --- | --- | --- |
| Selected exchanger area | `aries_integrated_plant__divertor_hx__selected_area` = 50000 | m²; price follows purchased area |
| Assumed heat-transfer coefficient | `aries_integrated_plant__divertor_hx__assumed_u` = 1000 | W/(m² K); uncertainty leaves area fixed |
| Calculated conductance | `aries_integrated_plant__divertor_hx__evaluate__ua` = 50 | MW/K |
| Selected pump capacity | `aries_integrated_plant__divertor_pump__selected_flow_capacity` = 500 | kg/s |
| Operating flow | `aries_integrated_plant__heat_exchangers__divertor_flow` = 500 | kg/s; separate from purchased capacity |
| Pump efficiency | `aries_integrated_plant__divertor_pump__efficiency` = 0.80000000000000004 | dimensionless assumed operating characteristic |
| Pump capacity margin | `aries_integrated_plant__divertor_pump__screen__margin` = 0 | kg/s |
| Pump electrical demand | `aries_integrated_plant__divertor_pump__evaluate__electric` = 10 | MW; enters net power and recovered heat |

### Purchased ratings and actual demands

| Owner / units | Selected rating input | Calculated actual demand output | Calculated capacity margin output |
| --- | --- | --- | --- |
| he / MW heat | `aries_integrated_plant__he_capacity__selected_rating` = 1500 | `aries_integrated_plant__he_coolant__evaluate__delivered_heat` = 896.54516614018905 | `aries_integrated_plant__he_capacity__evaluate__margin` = 603.45483385981095 |
| pbli / MW heat | `aries_integrated_plant__pbli_capacity__selected_rating` = 1800 | `aries_integrated_plant__pbli_coolant__evaluate__delivered_heat` = 1039.5261886482303 | `aries_integrated_plant__pbli_capacity__evaluate__margin` = 760.47381135176965 |
| divertor / MW heat | `aries_integrated_plant__divertor_capacity__selected_rating` = 800 | `aries_integrated_plant__divertor_coolant__evaluate__delivered_heat` = 304.31769245221153 | `aries_integrated_plant__divertor_capacity__evaluate__margin` = 495.68230754778847 |
| compressor / MW shaft | `aries_integrated_plant__compressor_capacity__selected_rating` = 1600 | `aries_integrated_plant__plant_ledger__evaluate__compressor_demand` = 1372.8509484278607 | `aries_integrated_plant__compressor_capacity__evaluate__margin` = 227.14905157213934 |
| turbine / MW shaft | `aries_integrated_plant__turbine_capacity__selected_rating` = 3500 | `aries_integrated_plant__turbine__evaluate__shaft_produced` = 2041.5804655934276 | `aries_integrated_plant__turbine_capacity__evaluate__margin` = 1458.4195344065724 |
| generator / MW electric | `aries_integrated_plant__generator_capacity__selected_rating` = 1800 | `aries_integrated_plant__plant_ledger__evaluate__gross_electric` = 655.35492682225561 | `aries_integrated_plant__generator_capacity__evaluate__margin` = 1144.6450731777445 |
| rejection / MW heat | `aries_integrated_plant__rejection_capacity__selected_rating` = 2500 | `aries_integrated_plant__plant_ledger__evaluate__cycle_rejection` = 1571.6595300826027 | `aries_integrated_plant__rejection_capacity__evaluate__margin` = 928.34046991739729 |
| fuel / T atoms/s | `aries_integrated_plant__fuel_capacity__selected_rating` = 3e+22 | `aries_integrated_plant__fuel__evaluate__exhaust_rate` = 1.2381327129390006e+22 | `aries_integrated_plant__fuel_capacity__evaluate__margin` = 1.7618672870609994e+22 |

The corresponding purchase owners are listed by exact output ID below. Enlarging these scalar ratings changes purchased class, margin and cost; it does not invent a machine efficiency benefit. Exchanger area is the explicit hardware alternative with a modeled finite thermal response.

## Capital leaves and exact price-factor controls

Each row is one capital leaf in the declared direct boundary. All baseline price factors below are 1. Their accepted package-price sensitivity interval is [0.5, 1.5] (E4), an engineering scenario range, not a confidence interval. E4 also declares [0.5, 2] for explicitly labeled source-scope uncertainty; the implementation has no separate scope multiplier, so that alternative uses the same named price-factor control with its interpretation recorded. Do not apply two independent multipliers accidentally to the same uncertainty. These price factors are estimates, not selected quantity or demand controls.

| Cost owner | Exact public price-factor key / baseline | Exact native purchase output / baseline USD2004 | Cost response class |
| --- | --- | --- | --- |
| auxiliary_cooling | `aries_integrated_plant__auxiliary_cooling__price_factor` = 1 | `aries_integrated_plant__auxiliary_cooling__purchase__cost` = 3735000 | Fixed one-package allowance |
| blanket_inventory | `aries_integrated_plant__blanket_inventory__price_factor` = 1 | `aries_integrated_plant__blanket_inventory__purchase__capital` = 59347000 | Selected-inventory estimate |
| compressor_equipment | `aries_integrated_plant__compressor_equipment__price_factor` = 1 | `aries_integrated_plant__compressor_equipment__purchase__capital` = 78639500 | Selected-inventory estimate |
| conversion_services | `aries_integrated_plant__conversion_services__price_factor` = 1 | `aries_integrated_plant__conversion_services__purchase__cost` = 62911600 | Fixed one-package allowance |
| divertor_duty_equipment | `aries_integrated_plant__divertor_duty_equipment__price_factor` = 1 | `aries_integrated_plant__divertor_duty_equipment__purchase__capital` = 32403166.666666672 | Selected-inventory estimate |
| divertor_hx | `aries_integrated_plant__divertor_hx__price_factor` = 1 | `aries_integrated_plant__divertor_hx__purchase__capital` = 58325700.000000007 | Selected-inventory estimate |
| divertor_inventory | `aries_integrated_plant__divertor_inventory__price_factor` = 1 | `aries_integrated_plant__divertor_inventory__purchase__cost` = 5318000 | Fixed one-package allowance |
| divertor_pump | `aries_integrated_plant__divertor_pump__price_factor` = 1 | `aries_integrated_plant__divertor_pump__purchase__capital` = 19441900 | Selected-inventory estimate |
| electrical_equipment | `aries_integrated_plant__electrical_equipment__price_factor` = 1 | `aries_integrated_plant__electrical_equipment__purchase__cost` = 138764000 | Fixed one-package allowance |
| facilities | `aries_integrated_plant__facilities__price_factor` = 1 | `aries_integrated_plant__facilities__purchase__cost` = 336133000 | Fixed one-package allowance |
| fuel_processing_equipment | `aries_integrated_plant__fuel_processing_equipment__price_factor` = 1 | `aries_integrated_plant__fuel_processing_equipment__purchase__capital` = 16590000 | Selected-inventory estimate |
| fuel_services | `aries_integrated_plant__fuel_services__price_factor` = 1 | `aries_integrated_plant__fuel_services__purchase__cost` = 38689000 | Fixed one-package allowance |
| generator_equipment | `aries_integrated_plant__generator_equipment__price_factor` = 1 | `aries_integrated_plant__generator_equipment__purchase__capital` = 47183699.999999993 | Selected-inventory estimate |
| he_duty_equipment | `aries_integrated_plant__he_duty_equipment__price_factor` = 1 | `aries_integrated_plant__he_duty_equipment__purchase__capital` = 32403166.666666672 | Selected-inventory estimate |
| he_hx | `aries_integrated_plant__he_hx__price_factor` = 1 | `aries_integrated_plant__he_hx__purchase__capital` = 58325700.000000007 | Selected-inventory estimate |
| he_pump | `aries_integrated_plant__he_pump__price_factor` = 1 | `aries_integrated_plant__he_pump__purchase__capital` = 19441900 | Selected-inventory estimate |
| heat_rejection_equipment | `aries_integrated_plant__heat_rejection_equipment__price_factor` = 1 | `aries_integrated_plant__heat_rejection_equipment__purchase__capital` = 56086000 | Selected-inventory estimate |
| heating_equipment | `aries_integrated_plant__heating_equipment__price_factor` = 1 | `aries_integrated_plant__heating_equipment__purchase__cost` = 66427000.000000007 | Fixed one-package allowance |
| impurity_control | `aries_integrated_plant__impurity_control__price_factor` = 1 | `aries_integrated_plant__impurity_control__purchase__cost` = 6561000 | Fixed one-package allowance |
| instrumentation_control | `aries_integrated_plant__instrumentation_control__price_factor` = 1 | `aries_integrated_plant__instrumentation_control__purchase__cost` = 44558000 | Fixed one-package allowance |
| lipb_inventory | `aries_integrated_plant__lipb_inventory__price_factor` = 1 | `aries_integrated_plant__lipb_inventory__purchase__capital` = 151327000 | Selected-inventory estimate |
| magnet_inventory | `aries_integrated_plant__magnet_inventory__price_factor` = 1 | `aries_integrated_plant__magnet_inventory__purchase__capital` = 204208000 | Selected-inventory estimate |
| magnet_power_supplies | `aries_integrated_plant__magnet_power_supplies__price_factor` = 1 | `aries_integrated_plant__magnet_power_supplies__purchase__cost` = 70624000 | Fixed one-package allowance |
| miscellaneous_equipment | `aries_integrated_plant__miscellaneous_equipment__price_factor` = 1 | `aries_integrated_plant__miscellaneous_equipment__purchase__cost` = 70958000 | Fixed one-package allowance |
| other_reactor_equipment | `aries_integrated_plant__other_reactor_equipment__price_factor` = 1 | `aries_integrated_plant__other_reactor_equipment__purchase__cost` = 60723000 | Fixed one-package allowance |
| pbli_duty_equipment | `aries_integrated_plant__pbli_duty_equipment__price_factor` = 1 | `aries_integrated_plant__pbli_duty_equipment__purchase__capital` = 32403166.666666672 | Selected-inventory estimate |
| pbli_hx | `aries_integrated_plant__pbli_hx__price_factor` = 1 | `aries_integrated_plant__pbli_hx__purchase__capital` = 58325700.000000007 | Selected-inventory estimate |
| pbli_pump | `aries_integrated_plant__pbli_pump__price_factor` = 1 | `aries_integrated_plant__pbli_pump__purchase__capital` = 19441900 | Selected-inventory estimate |
| primary_piping | `aries_integrated_plant__primary_piping__price_factor` = 1 | `aries_integrated_plant__primary_piping__purchase__cost` = 58325700 | Fixed one-package allowance |
| primary_support | `aries_integrated_plant__primary_support__price_factor` = 1 | `aries_integrated_plant__primary_support__purchase__capital` = 73126000 | Selected-inventory estimate |
| secondary_transport | `aries_integrated_plant__secondary_transport__price_factor` = 1 | `aries_integrated_plant__secondary_transport__purchase__cost` = 85933000 | Fixed one-package allowance |
| shield_inventory | `aries_integrated_plant__shield_inventory__price_factor` = 1 | `aries_integrated_plant__shield_inventory__purchase__capital` = 228627000 | Selected-inventory estimate |
| site_land | `aries_integrated_plant__site_land__price_factor` = 1 | `aries_integrated_plant__site_land__purchase__cost` = 12929000 | Fixed one-package allowance |
| turbine_equipment | `aries_integrated_plant__turbine_equipment__price_factor` = 1 | `aries_integrated_plant__turbine_equipment__purchase__capital` = 125823200 | Selected-inventory estimate |
| unallocated_source_scope | `aries_integrated_plant__unallocated_source_scope__price_factor` = 1 | `aries_integrated_plant__unallocated_source_scope__purchase__cost` = 28396000 | Fixed one-package allowance |
| vacuum_equipment | `aries_integrated_plant__vacuum_equipment__price_factor` = 1 | `aries_integrated_plant__vacuum_equipment__purchase__capital` = 137135000 | Selected-inventory estimate |
| vf_coils | `aries_integrated_plant__vf_coils__price_factor` = 1 | `aries_integrated_plant__vf_coils__purchase__cost` = 13358000 | Fixed one-package allowance |
| waste_equipment | `aries_integrated_plant__waste_equipment__price_factor` = 1 | `aries_integrated_plant__waste_equipment__purchase__cost` = 6655000 | Fixed one-package allowance |

Initial T stock is the separate capital output already listed above; its price control is in the following table. The operating consumables allowance is not a capital leaf. Source budget comparison parents are not extra leaves.

The chosen estimate mode is `aries_integrated_plant__cost_accounts__estimate_mode` = 0. Mode 0 uses selected-inventory estimates; mode 1 fixes those estimates to their reference budgets while retaining the price factors. Fixed one-package allowances remain fixed in either mode and support one package only. Actual thermal calculations remain live in mode 1. The source eight-parent alternative is separately reported, not selected by this mode.

## Financial uncertainty inputs already accepted

| Assumption | Exact public input / recorded baseline | Accepted range | Units and basis |
| --- | --- | --- | --- |
| T unit price | `aries_integrated_plant__fuel_inventory__tritium_price` = 30000000 | [10000000, 100000000] | USD2004/kg; E6 |
| Deuterium unit price | `aries_integrated_plant__fuel_inventory__deuterium_price` = 1000 | [100, 10000] | USD2004/kg; E6 |
| Initial T stock | `aries_integrated_plant__fuel_inventory__selected_tritium_kg` = 10 | [1, 30] | kg; E6 |
| Processing residence | `aries_integrated_plant__fuel_inventory__process_residence_s` = 1000 | [100, 10000] | s; E6; affects required stock, not selected stock |
| Supplied annual recovery | `aries_integrated_plant__fuel_inventory__annual_recovery_kg` = 0 | [0, 200]; separate named scenario 100 | kg/year; accepted no-credit and supplied-recovery alternatives, support remains 0 |
| Annual O&M | `aries_integrated_plant__annual_om__selected_amount` = 70000000 | [35000000, 140000000] | USD2004/year; E7 |
| Availability | `aries_integrated_plant__cost_schedule__availability` = 0.84999999999999998 | [0.7, 0.95] | dimensionless; E7 |
| Plant horizon | `aries_integrated_plant__cost_schedule__plant_years` = 40 | 40 held; no E7 sweep range declared | calendar years |
| Replacement life | `aries_integrated_plant__cost_schedule__replacement_life_fpy` = 5 | [2, 8] | full-power years; E8 |
| Replacement price factor | `aries_integrated_plant__cost_schedule__replacement_factor` = 1 | [0.5, 2] | dimensionless; E8 |
| LiPb event makeup | `aries_integrated_plant__cost_schedule__lipb_makeup_fraction` = 0.050000000000000003 | [0, 0.2] | fraction; E8 |
| Indirect fraction | `aries_integrated_plant__indirect_cost__fraction` = 0.20000000000000001 | [0.1, 0.3] | fraction of direct; E9 |
| Contingency fraction | `aries_integrated_plant__contingency__fraction` = 0.20000000000000001 | [0.1, 0.4] | fraction of direct plus indirect; E9 |
| Owner/commissioning fraction | `aries_integrated_plant__owner_commissioning__fraction` = 0.050000000000000003 | [0.02, 0.1] | fraction of direct; E9 |
| Annual consumables | `aries_integrated_plant__cost_ledger__consumables` = 5000000 | [1000000, 15000000] | USD2004/year; E10 |
| Import electricity price | `aries_integrated_plant__cost_ledger__import_price` = 50 | [20, 100] | USD2004/MWh; E10 |

The selected mass inputs above have E5 [0.5, 1.5] × nominal inventory sensitivity. This does not authorize scaling fixed one-package counts. Each exchanger area has the E2 [5000, 75000] m² capability-test interval; U has [500, 1500] W/(m² K) at fixed area. Pump operating flow and purchased flow capacity each have E3 [0.5, 1.5] × their separate baseline values; pump efficiency has [0.6, 0.9]. Thermal assumptions retain their accepted study meaning and are not cost-free economic optimization controls.

## Support limits and mapping findings

Every scientific support output below is 0 in the recorded baseline. Assumed scalar capacity-screen support is a different quantity. A positive scalar margin or supplied T recovery cannot upgrade these scientific flags.

| Scientific support | Exact native output ID and baseline |
| --- | --- |
| Magnet/conductor | `aries_integrated_plant__plant_ledger__evaluate__supported_magnet` = 0 |
| Breeding | `aries_integrated_plant__plant_ledger__evaluate__supported_breeding` = 0 |
| Deposition model | `aries_integrated_plant__plant_ledger__evaluate__supported_deposition` = 0 |
| Hydraulics | `aries_integrated_plant__plant_ledger__evaluate__supported_hydraulics` = 0 |
| Materials | `aries_integrated_plant__plant_ledger__evaluate__supported_materials` = 0 |
| Machine maps | `aries_integrated_plant__plant_ledger__evaluate__supported_machine_map` = 0 |

Mapping findings: consumables, availability, horizon and several source-reference values are exposed public inputs rather than duplicate output channels; this map names their actual keys. There is no single reactor-equipment or conversion-package price-factor input: uncertainty on those grouped accounts is a declared vector of the exact leaf controls above. There is no separate source-scope multiplier. Replacement events are scalar count/interval/cost channels, not an emitted dated cashflow array. These are interface limits, not missing amounts supplied by this handoff. No financing rate, discount rate, sales price, inflation conversion or LCOE channel is introduced here.

All referenced keys were checked against the final baseline receipt: 99 distinct input keys and 114 distinct output IDs. The map preserves source-case failures and the assumed status of the 423.1 MW baseline; it makes no ranking or optimum claim.
