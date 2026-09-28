# Installed cooling equipment study results

All 34 native candidates are retained; 0 satisfy every whole-plant predicate. The default baseline is recorded separately. This is an engineered sensitivity study, not a feasible design or an optimum.

Verification status: all-point pass; generic pass. The original boundary mismatch and refusal remain in results/verification-boundary-attempt/. The reviewed oracle correction preserves authored operation order and all native negative verdicts; it changes no native case or physical limit.

## Retained case and mode comparisons

| Proposal | LCOE, $/MWh | Net MW | Total capital, $million | Selected cooling account, $million | Primary pump electric MW | Selected salt pump electric MW | Failed predicates |
|---|---:|---:|---:|---:|---:|---:|---|
| lhs-0224-legacy | 150.429542 | 1010.112 | 9,465.696 | 205.073 | 86.776 | 0.000 | tbr_ok |
| lhs-0224-costonly | 309.554789 | 1010.112 | 20,900.547 | 8,205.337 | 86.776 | 0.000 | tbr_ok |
| lhs-0224-full | 310.632663 | 1006.725 | 20,903.392 | 8,205.337 | 86.776 | 5.455 | tbr_ok |
| anchor-loops-14-legacy | 156.051613 | 975.844 | 9,490.637 | 199.772 | 143.796 | 0.000 | tbr_ok |
| anchor-loops-14-costonly | 285.387559 | 975.844 | 18,426.327 | 6,451.833 | 143.796 | 0.000 | tbr_ok |
| anchor-loops-14-full | 286.438023 | 972.393 | 18,429.199 | 6,451.833 | 143.796 | 5.558 | tbr_ok |
| r2-forward-legacy | 162.871143 | 1003.739 | 10,204.510 | 205.518 | 166.241 | 0.000 | divertor_heat_ok;reference_conductor_current_ok;tbr_ok;wp_fit_ok |
| r2-forward-costonly | 288.906574 | 1003.739 | 19,152.259 | 6,466.056 | 166.241 | 0.000 | divertor_heat_ok;reference_conductor_current_ok;tbr_ok;wp_fit_ok |
| r2-forward-full | 289.997120 | 1000.101 | 19,155.285 | 6,466.056 | 166.241 | 5.860 | divertor_heat_ok;reference_conductor_current_ok;tbr_ok;wp_fit_ok |
| r2-table5-legacy | 162.946993 | 1003.767 | 10,214.050 | 205.464 | 164.995 | 0.000 | divertor_heat_ok;reference_conductor_current_ok;tbr_ok;wp_fit_ok |
| r2-table5-costonly | 288.958707 | 1003.767 | 19,160.808 | 6,465.308 | 164.995 | 0.000 | divertor_heat_ok;reference_conductor_current_ok;tbr_ok;wp_fit_ok |
| r2-table5-full | 290.046540 | 1000.139 | 19,163.835 | 6,465.308 | 164.995 | 5.844 | divertor_heat_ok;reference_conductor_current_ok;tbr_ok;wp_fit_ok |

Equipment diagnostics remain enabled in legacy mode; its installed diagnostic total does not mean that equipment cost is selected into the legacy accounts. Cost-only and full modes select new accounts. The full mode also selects secondary electric demand and recovered shaft heat.

Default baseline (separate authored case): LCOE 270.823875 dollars/MWh and net electric 1008.898406 MW; total capital 17,860.732 million dollars; primary/salt pump electric demand 175.281/5.975 MW. It is not selected18.

Selected full CAS72 total: 185012683.07 dollars/year. Cooling adds 63243147.38 dollars/year to existing calendar replacements of 121769535.68 dollars/year.

## Selected eighteen-circuit equipment

The raw quantities and source scope are preserved in analysis.json and points.csv. Machine quantities are per machine, exchanger geometry and duty per exchanger, salt flow per circuit, and aggregate costs/masses plant totals according to preparation/equipment-interface.json.

| Quantity | Value | Unit / basis |
|---|---:|---|
| Active helium circulators | 36.000000 | machines, plant |
| Helium mass flow | 78.287507 | kg/s per circulator |
| Helium inlet volume flow | 11.764360 | m³/s per circulator |
| Helium circulator shaft power | 2.410455 | MW per circulator |
| Helium circulator electric power | 2.410455 | MW per circulator |
| Helium suction pressure | 7,840,697.495422 | Pa |
| Intermediate heat exchangers | 18.000000 | exchangers, plant |
| Intermediate exchanger heat duty | 167.439719 | MW per exchanger |
| Installed heat-transfer area | 10,310.691255 | m² per exchanger |
| Required heat-transfer area | 5,824.088563 | m² per exchanger |
| Exchanger steel mass | 481,541.041508 | kg per exchanger |
| Helium piping mass | 6,261,252.685871 | kg, plant |
| Salt piping mass | 462,448.480133 | kg, plant |
| Helium inventory with reserve | 21,268.553475 | kg, plant |
| Salt inventory with reserve | 2,068,394.120214 | kg, plant |
| Active salt pumps | 36.000000 | pumps, plant |
| Salt mass flow | 275.213213 | kg/s per pump |
| Salt pump shaft power | 0.143942 | MW per pump |
| Salt pump shaft power for price correlation | 193.029914 | hp per pump |
| Salt pump motor electric power | 203.189383 | hp per pump |
| Salt pump electric power | 5.454659 | MW, plant |
| Salt pump shaft heat | 5.181926 | MW, plant |
| Salt straight-pipe head loss | 0.905392 | m of salt |
| Head remaining for other salt components | 39.094608 | m of salt |
| Salt outlet minus cycle-fit temperature | 15.000000 | K |
| Modeled helium volume before reserve | 3,364.562444 | m³, plant |
| Helium pipe internal volume | 2,257.562444 | m³, plant |
| Helium exchanger internal volume | 1,107.000000 | m³, plant |
| Modeled salt volume before reserve | 999.079901 | m³, plant |
| Salt pipe internal volume | 226.194671 | m³, plant |
| Salt exchanger internal volume | 772.885230 | m³, plant |
| Modeled versus source helium inventory volume | 1.913858 | dimensionless ratio |

## Selected cost breakdown

Equipment costs below are millions of 2025 US dollars using the stated CPI purchasing-power proxy. Procurement includes source-specific fabricated or vendor package scope; field installation is separate. The inherited whole-plant total capital uses its existing mixed basis.

| Cost component | Value | Unit / scope |
|---|---:|---|
| Helium circulators: vendor packages | 350.258884 | million USD2025 |
| Helium circulators: field installation | 109.228233 | million USD2025 |
| Helium circulators: first design fee | 0.641825 | million USD2025 |
| Helium circulator spare | 9.729413 | million USD2025 |
| Salt pumps: purchased packages | 2.345713 | million USD2025 |
| Salt pumps: field installation | 0.731511 | million USD2025 |
| Salt pump spare | 0.065159 | million USD2025 |
| Exchangers: fabricated purchase | 3,528.947294 | million USD2025 |
| Exchangers: field installation | 91.752630 | million USD2025 |
| Helium piping: fabricated purchase | 2,549.180515 | million USD2025 |
| Helium piping: field installation | 1,274.590258 | million USD2025 |
| Salt piping: fabricated purchase | 188.279361 | million USD2025 |
| Salt piping: field installation | 94.139681 | million USD2025 |
| Helium circulators: installed account | 460.128942 | million USD2025 |
| Helium piping: installed account | 3,823.770773 | million USD2025 |
| Exchangers: installed account | 3,620.699924 | million USD2025 |
| Salt pumps: installed account | 3.077224 | million USD2025 |
| Salt piping: installed account | 282.419042 | million USD2025 |
| Initial fluid inventory | 5.446311 | million USD2025 |
| Initial spares | 9.794572 | million USD2025 |
| All purchase scope including inventory/spares/design | 6,634.894476 | million USD2025 |
| All field installation | 1,570.442311 | million USD2025 |
| Total seven equipment accounts | 8,205.336788 | million USD2025 |
| Eligible delivered basis for downstream freight | 6,626.395468 | million USD2025 |
| Additional annual cooling replacements | 63.243147 | million USD2025/year |
| Annual fluid makeup | 0.005446 | million USD2025/year |
| Machine event purchase | 352.604597 | million USD2025 |
| Machine event installation | 109.959744 | million USD2025 |
| Machine event removal | 109.959744 | million USD2025 |
| Bundle event purchase | 908.623985 | million USD2025 |
| Bundle event installation | 23.624224 | million USD2025 |
| Bundle event removal | 21.806976 | million USD2025 |
| Machine events | 2.000000 | events strictly before plant horizon |
| Bundle events | 1.000000 | events strictly before plant horizon |
| Salt price raw | 1.230000 | 2011 USD/kg |
| Salt price year | 2,011.000000 | source calendar year |
| Salt unit price | 1.760502 | 2025 USD/kg, CPI proxy |
| Helium price raw | 14.000000 | 2024 USD/standard m³ |
| Helium price year | 2,024.000000 | source calendar year |

## Local sensitivities

| Proposal | LCOE, $/MWh | Change vs selected full | Installed cooling, million USD2025 | Total capital, $million | Primary / salt pump MW | Net MW | Failed predicates |
|---|---:|---:|---:|---:|---:|---:|---|
| heat_transport__n_loops-12 | 277.963671 | -32.668992 | 5,572.306 | 17,201.524 | 196.163 / 5.653 | 940.862 | loop_capacity_ok;tbr_ok |
| heat_transport__n_loops-16 | 297.756711 | -12.875952 | 7,329.281 | 19,664.267 | 109.935 / 5.497 | 992.782 | tbr_ok |
| heat_transport__n_loops-20 | 324.443385 | +13.810722 | 9,080.393 | 22,144.855 | 70.240 / 5.425 | 1016.682 | tbr_ok |
| plasma__n_e0-4.794618463038878e+20 | 319.342284 | +8.709621 | 8,195.335 | 20,771.200 | 78.796 / 5.273 | 970.731 | tbr_ok |
| plasma__n_e0-4.990317175815975e+20 | 302.497846 | -8.134818 | 8,215.350 | 21,036.388 | 95.372 / 5.639 | 1042.862 | tbr_ok |
| heat_transport__equipment_layout_multiplier-0.5 | 271.612338 | -39.020325 | 6,151.224 | 17,962.441 | 86.776 / 5.455 | 1006.725 | tbr_ok |
| heat_transport__equipment_layout_multiplier-2 | 388.673313 | +78.040649 | 12,313.562 | 26,785.296 | 86.776 / 5.455 | 1006.725 | tbr_ok |
| heat_transport__equipment_machine_life-20 | 307.686737 | -2.945926 | 8,205.337 | 20,903.392 | 86.776 / 5.455 | 1006.725 | tbr_ok |
| heat_transport__equipment_machine_life-30 | 306.189178 | -4.443485 | 8,205.337 | 20,903.392 | 86.776 / 5.455 | 1006.725 | tbr_ok |
| heat_transport__equipment_bundle_life-30 | 307.132545 | -3.500118 | 8,205.337 | 20,903.392 | 86.776 / 5.455 | 1006.725 | tbr_ok |
| heat_transport__equipment_tube_wall-0.001 | 304.520008 | -6.112655 | 7,935.929 | 20,518.917 | 86.776 / 5.455 | 1006.725 | tbr_ok |
| heat_transport__equipment_tube_wall-0.002 | 316.375973 | +5.743310 | 8,458.466 | 21,264.637 | 86.776 / 5.455 | 1006.725 | tbr_ok |
| heat_transport__equipment_shell_wall-0.1 | 289.967655 | -20.665008 | 7,113.956 | 19,345.869 | 86.776 / 5.455 | 1006.725 | tbr_ok |
| heat_transport__equipment_shell_wall-0.3 | 332.743244 | +22.110580 | 9,373.062 | 22,569.869 | 86.776 / 5.455 | 1006.725 | tbr_ok |
| heat_transport__equipment_accessory_mass-5000 | 309.780455 | -0.852208 | 8,167.783 | 20,849.799 | 86.776 / 5.455 | 1006.725 | tbr_ok |
| heat_transport__equipment_accessory_mass-20000 | 312.337080 | +1.704417 | 8,280.445 | 21,010.579 | 86.776 / 5.455 | 1006.725 | tbr_ok |
| heat_transport__equipment_makeup_fraction-0 | 310.631679 | -0.000984 | 8,205.337 | 20,903.392 | 86.776 / 5.455 | 1006.725 | tbr_ok |
| heat_transport__equipment_makeup_fraction-0.01 | 310.641523 | +0.008860 | 8,205.337 | 20,903.392 | 86.776 / 5.455 | 1006.725 | tbr_ok |
| heat_transport__equipment_inventory_reserve-0 | 310.623103 | -0.009560 | 8,204.842 | 20,902.679 | 86.776 / 5.455 | 1006.725 | tbr_ok |
| heat_transport__equipment_inventory_reserve-1 | 310.718708 | +0.086044 | 8,209.793 | 20,909.817 | 86.776 / 5.455 | 1006.725 | tbr_ok |
| heat_transport__equipment_saltprice_source_choice-1 | 310.682376 | +0.049712 | 8,207.911 | 20,907.104 | 86.776 / 5.455 | 1006.725 | tbr_ok |
| heat_transport__equipment_removal_multiplier-0 | 309.699239 | -0.933424 | 8,205.337 | 20,903.392 | 86.776 / 5.455 | 1006.725 | tbr_ok |

## Equipment diagnostic flags

These are Boolean equipment diagnostics, distinct from the twenty authored whole-plant acceptance predicates. A failed flag is retained even when it does not change the predicate verdict.

| Proposal | False equipment flags |
|---|---|
| lhs-0224-legacy | cycle_interface_ok; helium_price_transfer_validated; inventory_complete; inventory_source_volume_ok; pressure_qualified; salt_bulk_scale_ok; salt_pump_transfer_validated |
| lhs-0224-costonly | cycle_interface_ok; helium_price_transfer_validated; inventory_complete; inventory_source_volume_ok; pressure_qualified; salt_bulk_scale_ok; salt_pump_transfer_validated |
| lhs-0224-full | cycle_interface_ok; helium_price_transfer_validated; inventory_complete; inventory_source_volume_ok; pressure_qualified; salt_bulk_scale_ok; salt_pump_transfer_validated |
| anchor-loops-14-legacy | cycle_interface_ok; helium_price_transfer_validated; inventory_complete; inventory_source_volume_ok; motor_factor_ok; pressure_qualified; pump_type_ok; salt_bulk_scale_ok; salt_pump_transfer_validated |
| anchor-loops-14-costonly | cycle_interface_ok; helium_price_transfer_validated; inventory_complete; inventory_source_volume_ok; motor_factor_ok; pressure_qualified; pump_type_ok; salt_bulk_scale_ok; salt_pump_transfer_validated |
| anchor-loops-14-full | cycle_interface_ok; helium_price_transfer_validated; inventory_complete; inventory_source_volume_ok; motor_factor_ok; pressure_qualified; pump_type_ok; salt_bulk_scale_ok; salt_pump_transfer_validated |
| r2-forward-legacy | cycle_interface_ok; helium_price_transfer_validated; inventory_complete; inventory_source_volume_ok; motor_factor_ok; pressure_qualified; pump_type_ok; salt_bulk_scale_ok; salt_pump_transfer_validated |
| r2-forward-costonly | cycle_interface_ok; helium_price_transfer_validated; inventory_complete; inventory_source_volume_ok; motor_factor_ok; pressure_qualified; pump_type_ok; salt_bulk_scale_ok; salt_pump_transfer_validated |
| r2-forward-full | cycle_interface_ok; helium_price_transfer_validated; inventory_complete; inventory_source_volume_ok; motor_factor_ok; pressure_qualified; pump_type_ok; salt_bulk_scale_ok; salt_pump_transfer_validated |
| r2-table5-legacy | cycle_interface_ok; helium_price_transfer_validated; inventory_complete; inventory_source_volume_ok; motor_factor_ok; pressure_qualified; pump_type_ok; salt_bulk_scale_ok; salt_pump_transfer_validated |
| r2-table5-costonly | cycle_interface_ok; helium_price_transfer_validated; inventory_complete; inventory_source_volume_ok; motor_factor_ok; pressure_qualified; pump_type_ok; salt_bulk_scale_ok; salt_pump_transfer_validated |
| r2-table5-full | cycle_interface_ok; helium_price_transfer_validated; inventory_complete; inventory_source_volume_ok; motor_factor_ok; pressure_qualified; pump_type_ok; salt_bulk_scale_ok; salt_pump_transfer_validated |
| heat_transport__n_loops-12 | cycle_interface_ok; helium_price_transfer_validated; ihx_capacity_ok; inventory_complete; inventory_source_volume_ok; motor_factor_ok; pressure_qualified; pump_type_ok; salt_bulk_scale_ok; salt_pump_transfer_validated |
| heat_transport__n_loops-16 | cycle_interface_ok; helium_price_transfer_validated; inventory_complete; inventory_source_volume_ok; pressure_qualified; pump_type_ok; salt_bulk_scale_ok; salt_pump_transfer_validated |
| heat_transport__n_loops-20 | cycle_interface_ok; helium_price_transfer_validated; inventory_complete; inventory_source_volume_ok; pressure_qualified; salt_bulk_scale_ok; salt_pump_transfer_validated |
| plasma__n_e0-4.794618463038878e+20 | cycle_interface_ok; helium_price_transfer_validated; inventory_complete; inventory_source_volume_ok; pressure_qualified; salt_bulk_scale_ok; salt_pump_transfer_validated |
| plasma__n_e0-4.990317175815975e+20 | cycle_interface_ok; helium_price_transfer_validated; inventory_complete; inventory_source_volume_ok; pressure_qualified; salt_bulk_scale_ok; salt_pump_transfer_validated |
| heat_transport__equipment_layout_multiplier-0.5 | cycle_interface_ok; helium_price_transfer_validated; inventory_complete; inventory_source_volume_ok; pressure_qualified; salt_bulk_scale_ok; salt_pump_transfer_validated |
| heat_transport__equipment_layout_multiplier-2 | cycle_interface_ok; helium_price_transfer_validated; inventory_complete; inventory_source_volume_ok; pressure_qualified; salt_bulk_scale_ok; salt_pump_transfer_validated |
| heat_transport__equipment_machine_life-20 | cycle_interface_ok; helium_price_transfer_validated; inventory_complete; inventory_source_volume_ok; pressure_qualified; salt_bulk_scale_ok; salt_pump_transfer_validated |
| heat_transport__equipment_machine_life-30 | cycle_interface_ok; helium_price_transfer_validated; inventory_complete; inventory_source_volume_ok; pressure_qualified; salt_bulk_scale_ok; salt_pump_transfer_validated |
| heat_transport__equipment_bundle_life-30 | cycle_interface_ok; helium_price_transfer_validated; inventory_complete; inventory_source_volume_ok; pressure_qualified; salt_bulk_scale_ok; salt_pump_transfer_validated |
| heat_transport__equipment_tube_wall-0.001 | cycle_interface_ok; helium_price_transfer_validated; inventory_complete; inventory_source_volume_ok; pressure_qualified; salt_bulk_scale_ok; salt_pump_transfer_validated |
| heat_transport__equipment_tube_wall-0.002 | cycle_interface_ok; helium_price_transfer_validated; inventory_complete; inventory_source_volume_ok; pressure_qualified; salt_bulk_scale_ok; salt_pump_transfer_validated |
| heat_transport__equipment_shell_wall-0.1 | cycle_interface_ok; helium_price_transfer_validated; inventory_complete; inventory_source_volume_ok; pressure_qualified; salt_bulk_scale_ok; salt_pump_transfer_validated |
| heat_transport__equipment_shell_wall-0.3 | cycle_interface_ok; helium_price_transfer_validated; inventory_complete; inventory_source_volume_ok; pressure_qualified; salt_bulk_scale_ok; salt_pump_transfer_validated |
| heat_transport__equipment_accessory_mass-5000 | cycle_interface_ok; helium_price_transfer_validated; inventory_complete; inventory_source_volume_ok; pressure_qualified; salt_bulk_scale_ok; salt_pump_transfer_validated |
| heat_transport__equipment_accessory_mass-20000 | cycle_interface_ok; helium_price_transfer_validated; inventory_complete; inventory_source_volume_ok; pressure_qualified; salt_bulk_scale_ok; salt_pump_transfer_validated |
| heat_transport__equipment_makeup_fraction-0 | cycle_interface_ok; helium_price_transfer_validated; inventory_complete; inventory_source_volume_ok; pressure_qualified; salt_bulk_scale_ok; salt_pump_transfer_validated |
| heat_transport__equipment_makeup_fraction-0.01 | cycle_interface_ok; helium_price_transfer_validated; inventory_complete; inventory_source_volume_ok; pressure_qualified; salt_bulk_scale_ok; salt_pump_transfer_validated |
| heat_transport__equipment_inventory_reserve-0 | cycle_interface_ok; helium_price_transfer_validated; inventory_complete; inventory_source_volume_ok; pressure_qualified; salt_bulk_scale_ok; salt_pump_transfer_validated |
| heat_transport__equipment_inventory_reserve-1 | cycle_interface_ok; helium_price_transfer_validated; inventory_complete; inventory_source_volume_ok; pressure_qualified; salt_bulk_scale_ok; salt_pump_transfer_validated |
| heat_transport__equipment_saltprice_source_choice-1 | cycle_interface_ok; helium_price_transfer_validated; inventory_complete; inventory_source_volume_ok; pressure_qualified; salt_bulk_scale_ok; salt_pump_transfer_validated |
| heat_transport__equipment_removal_multiplier-0 | cycle_interface_ok; helium_price_transfer_validated; inventory_complete; inventory_source_volume_ok; pressure_qualified; salt_bulk_scale_ok; salt_pump_transfer_validated |

## Applicability and boundaries

The 480°C source-fit temperature exceeds the 465°C salt interface. Lower-cost cases do not resolve this physical interface failure. The current breeding screen and all pump source applicability checks remain visible. Helium cost scaling, nuclear fabrication transfer, salt-pump fluid transfer, reserve, geometry and lifecycle assumptions remain conditional; these cases are not vendor quotations or pressure-qualified hardware.

The CPI proxy converts cited equipment prices to 2025 purchasing power and does not rebase inherited whole-plant accounts. Existing CAS71 staffing covers routine cooling work as an ownership assumption. Replacements retain modeled availability; coincident maintenance is assumed, not demonstrated. Steam-generator CAS23 coverage, full in-vessel inventories, drain/expansion and trace-heating auxiliaries remain unresolved scope.

Independent equation agreement verifies software implementation. It does not validate the shared transport data or physical applicability of source transfers. Every authored predicate and required numeric channel is retained. See oracle-all-points.json, verification_summary.json and points.csv for exact coverage.
