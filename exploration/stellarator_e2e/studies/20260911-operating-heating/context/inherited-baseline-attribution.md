# Production baseline and cost attribution

[AGENT] Production matches the deposited independent conservation and explicit financial formulas. Every common scalar from T-015 is compared in `baseline-attribution.json`; the table below contains every changed scalar, regardless of materiality. The original first-attempt generated-body failure remains in `attempt-1-preserved-auto-body/`. Correcting that body restores the unchanged required-minus-installed diagnostic, reducing the prototype's 73 changed scalars to 72.

Heating procurement remains $264145000 at baseline and rises to $316974000 under the 120 MW reserve control. Online source, loop, gross/net, divertor heat, calendar and annual accounts remain exactly invariant under reserve. The signed diagnostic changes from -0.920399212073221 to -10.920399212073221 MW. The f_alpha_fast=0.96 demand control holds procurement and fusion fixed. Its retained alpha gain equals its auxiliary reduction, so divertor absorbed heat stays fixed.

The baseline is a diagnostic operating point with divertor peak 10.517841546 MW/m^2 above the 10 MW/m^2 bound. Seventeen assertions are satisfied and one violated. The coupling=0.8 control additionally violates installed capacity. Zero efficiency rejects execution; negative and over-one values remain explicitly violated diagnostics.

## Independent financial bridge

Capital charges are evaluated directly from overnight capital, discount rate, construction time and operating life. They are never inferred from LCOE. Each bridge uses old annual energy for the capital/annual contributions and the new numerator for the energy contribution. The checked residual is floating-point roundoff.

| LCOE | Capital effect $/MWh | Annual effect $/MWh | Energy effect $/MWh | Total change $/MWh | Residual |
|---|---:|---:|---:|---:|---:|
| headline | 0.00247929168711 | 0.00438032137948 | -0.347151456721 | -0.340291843655 | 1.90403248723e-14 |
| comparison | 0.00242572481021 | 0.00438032137948 | -0.340562462069 | -0.333756415879 | 9.54791801178e-15 |

## Reviewed cost coverage

`cost-operand-coverage.json` records the actual generated input bindings and baseline/reserve/demand outputs for all selected cost, rollup, annual, calendar and LCOE modules. Every recorded input binding is identical to entering revision 546218a5. The unchanged authored cost, lifecycle, loop and DCF files are verified byte-for-byte in the focused cost test. The two pre-production classification tables in `../design.md` govern these classifications; no additional cost operand was found.

Installed ECRH capacity and the direct NBI/ICRF/LHCD procurement inputs are unchanged. Blanket, shield and divertor capital retain thermal sizing; structure, vessel, supplies, electric and miscellaneous plant retain gross sizing; turbine retains cycle-output sizing. Buildings combine fixed/fusion, thermal and gross terms; preconstruction land and O&M staffing follow net power. Remote handling follows gross; coolant follows net and thermal; auxiliary cooling follows thermal, while its cryoplant term stays fixed with geometry. Waste and I&C follow thermal; fuel handling, other reactor equipment and owner costs follow net. Supplementary costs retain their capital-based and net-based terms.

The power-core subtotal adds heating and other equipment; installation follows the core plus remote handling; CAS22 includes both. BOP and geometry-based CAS27/CAS28 stay fixed under reserve. CAS2x, contingency, CAS20, CAS30 and supplementary shipping/tax/insurance pass the reserve increase through their existing formulas. Spares follow unchanged BOP; startup/decommissioning follow unchanged net power. Overnight and IDC follow those totals. Replacement event costs follow blanket plus divertor; calendar dates depend on the unchanged neutron load. CAS71 follows staffing, CAS72 discounts dated events, CAS80 follows annual fusion time, and each LCOE uses its unchanged capital and annual-energy convention.

| Generated cost/rollup module | Classification | Bindings |
|---|---|---|
| `winding_pack_cost` | reviewed design-point sizing or dependent capital rollup | Unchanged; exact operands in companion JSON |
| `heating_cost` | installed procurement | Unchanged; exact operands in companion JSON |
| `magnet_cost` | reviewed design-point sizing or dependent capital rollup | Unchanged; exact operands in companion JSON |
| `magnet_structure_cost` | reviewed design-point sizing or dependent capital rollup | Unchanged; exact operands in companion JSON |
| `magnet_capital_rollup` | reviewed design-point sizing or dependent capital rollup | Unchanged; exact operands in companion JSON |
| `vessel_cost` | reviewed design-point sizing or dependent capital rollup | Unchanged; exact operands in companion JSON |
| `blanket_cost` | reviewed design-point sizing or dependent capital rollup | Unchanged; exact operands in companion JSON |
| `fuel_handling` | reviewed design-point sizing or dependent capital rollup | Unchanged; exact operands in companion JSON |
| `owner` | reviewed design-point sizing or dependent capital rollup | Unchanged; exact operands in companion JSON |
| `other_rpe` | reviewed design-point sizing or dependent capital rollup | Unchanged; exact operands in companion JSON |
| `electric_cost` | reviewed design-point sizing or dependent capital rollup | Unchanged; exact operands in companion JSON |
| `heat_rejection_cost` | reviewed design-point sizing or dependent capital rollup | Unchanged; exact operands in companion JSON |
| `remote_handling` | reviewed design-point sizing or dependent capital rollup | Unchanged; exact operands in companion JSON |
| `coolant` | reviewed design-point sizing or dependent capital rollup | Unchanged; exact operands in companion JSON |
| `aux_cooling` | reviewed design-point sizing or dependent capital rollup | Unchanged; exact operands in companion JSON |
| `buildings_cost` | reviewed design-point sizing or dependent capital rollup | Unchanged; exact operands in companion JSON |
| `misc_cost` | reviewed design-point sizing or dependent capital rollup | Unchanged; exact operands in companion JSON |
| `om_cost` | reviewed design-point sizing or dependent capital rollup | Unchanged; exact operands in companion JSON |
| `cas71_calc` | calendar/annual/financial propagation | Unchanged; exact operands in companion JSON |
| `shield_cost` | reviewed design-point sizing or dependent capital rollup | Unchanged; exact operands in companion JSON |
| `divertor_cost` | reviewed design-point sizing or dependent capital rollup | Unchanged; exact operands in companion JSON |
| `power_supplies_cost` | reviewed design-point sizing or dependent capital rollup | Unchanged; exact operands in companion JSON |
| `turbine_cost` | reviewed design-point sizing or dependent capital rollup | Unchanged; exact operands in companion JSON |
| `structure_cost` | reviewed design-point sizing or dependent capital rollup | Unchanged; exact operands in companion JSON |
| `precon_cost` | reviewed design-point sizing or dependent capital rollup | Unchanged; exact operands in companion JSON |
| `waste` | reviewed design-point sizing or dependent capital rollup | Unchanged; exact operands in companion JSON |
| `inc_cost` | reviewed design-point sizing or dependent capital rollup | Unchanged; exact operands in companion JSON |
| `powercore_capital` | reviewed design-point sizing or dependent capital rollup | Unchanged; exact operands in companion JSON |
| `reactor_equipment_subtotal` | reviewed design-point sizing or dependent capital rollup | Unchanged; exact operands in companion JSON |
| `installation` | reviewed design-point sizing or dependent capital rollup | Unchanged; exact operands in companion JSON |
| `cas22_capital` | reviewed design-point sizing or dependent capital rollup | Unchanged; exact operands in companion JSON |
| `bop_capital` | reviewed design-point sizing or dependent capital rollup | Unchanged; exact operands in companion JSON |
| `replacement_cost_per_event` | reviewed design-point sizing or dependent capital rollup | Unchanged; exact operands in companion JSON |
| `calendar` | calendar/annual/financial propagation | Unchanged; exact operands in companion JSON |
| `fuel_calc` | reviewed design-point sizing or dependent capital rollup | Unchanged; exact operands in companion JSON |
| `cas80_calc` | calendar/annual/financial propagation | Unchanged; exact operands in companion JSON |
| `cas70_calc` | calendar/annual/financial propagation | Unchanged; exact operands in companion JSON |
| `special_materials_capital` | reviewed design-point sizing or dependent capital rollup | Unchanged; exact operands in companion JSON |
| `cas23_to_28_capital` | reviewed design-point sizing or dependent capital rollup | Unchanged; exact operands in companion JSON |
| `cas2x_pre_contingency` | reviewed design-point sizing or dependent capital rollup | Unchanged; exact operands in companion JSON |
| `contingency` | reviewed design-point sizing or dependent capital rollup | Unchanged; exact operands in companion JSON |
| `cas20_capital` | reviewed design-point sizing or dependent capital rollup | Unchanged; exact operands in companion JSON |
| `indirect` | reviewed design-point sizing or dependent capital rollup | Unchanged; exact operands in companion JSON |
| `supplementary` | reviewed design-point sizing or dependent capital rollup | Unchanged; exact operands in companion JSON |
| `overnight_capital` | reviewed design-point sizing or dependent capital rollup | Unchanged; exact operands in companion JSON |
| `idc` | calendar/annual/financial propagation | Unchanged; exact operands in companion JSON |
| `cas90_1cfe_calc` | calendar/annual/financial propagation | Unchanged; exact operands in companion JSON |
| `lcoe_1cfe_calc` | calendar/annual/financial propagation | Unchanged; exact operands in companion JSON |
| `total_capital` | reviewed design-point sizing or dependent capital rollup | Unchanged; exact operands in companion JSON |
| `lcoe_calc` | calendar/annual/financial propagation | Unchanged; exact operands in companion JSON |

## Every changed scalar against T-015

| Scalar | Before | After | Delta |
|---|---:|---:|---:|
| `divheat__q_target_peak_area_scaled` | 10.5353291311 | 10.517841546 | -0.0174875850294 |
| `divheat__p_heat_abs` | 554.491006898 | 553.570607686 | -0.920399212073 |
| `divheat__f_rad_edge_in_range` | 0.138199202732 | 0.138320175679 | 0.000120972947582 |
| `divheat__q_target_margin` | -0.535329131066 | -0.517841546037 | 0.0174875850294 |
| `divheat__p_target_nonrad` | 55.4491006898 | 55.3570607686 | -0.0920399212073 |
| `divheat__f_rad_edge` | 0.834366262156 | 0.83418531434 | -0.000180947815897 |
| `divheat__p_sep` | 334.769361674 | 333.848962462 | -0.920399212073 |
| `divheat__q_target_peak` | 10.5353291311 | 10.517841546 | -0.0174875850294 |
| `source_heat__q_source` | 3126.85267629 | 3125.93227708 | -0.920399212073 |
| `primary_loop__p_loop_margin` | 7699503.22517 | 7699680.10354 | 176.878361561 |
| `primary_loop__q_recovered_total` | 175.436542688 | 175.280934404 | -0.15560828335 |
| `primary_loop__p_elec` | 175.436542688 | 175.280934404 | -0.15560828335 |
| `primary_loop__p_pump_total` | 175.436542688 | 175.280934404 | -0.15560828335 |
| `primary_loop__T_comp_in` | 561.928713879 | 561.935365845 | 0.00665196553314 |
| `primary_loop__dp_loop` | 300496.774825 | 300319.896464 | -176.878361561 |
| `primary_loop__mdot_loop` | 215.045849928 | 214.982550486 | -0.0632994423863 |
| `primary_loop__w_fluid` | 175.436542688 | 175.280934404 | -0.15560828335 |
| `primary_loop__capacity_margin` | 10.0319278497 | 10.0952272921 | 0.0632994423863 |
| `primary_loop__q_ihx` | 3302.28921898 | 3301.21321149 | -1.07600749542 |
| `primary_loop__mdot` | 3010.64189899 | 3009.7557068 | -0.886192193408 |
| `primary_loop__r_comp` | 1.03902807312 | 1.03900420439 | -2.38687297027e-05 |
| `pb__p_the` | 1358.4183136 | 1357.97569086 | -0.442622735449 |
| `pb__p_et` | 1358.4183136 | 1357.97569086 | -0.442622735449 |
| `pb__q_eng` | 3.92545815782 | 3.94710166389 | 0.0216435060712 |
| `pb__p_th` | 3302.28921898 | 3301.21321149 | -1.07600749542 |
| `pb__p_net` | 1012.3648699 | 1013.93193255 | 1.56706265411 |
| `pb__rec_frac` | 0.25474733389 | 0.253350454372 | -0.00139687951747 |
| `vessel_cost__cost` | 120865534.16 | 120841903.153 | -23631.0065871 |
| `blanket_cost__cost` | 718554642.709 | 718414154.607 | -140488.102031 |
| `fuel_handling__cost` | 121036732.907 | 121167851.338 | 131118.431282 |
| `owner__cost` | 41453933.767 | 41486005.1053 | 32071.3382209 |
| `other_rpe__cost` | 11613616.8353 | 11627996.1962 | 14379.3609595 |
| `electric_cost__cost` | 117367342.295 | 117329099.69 | -38242.6043428 |
| `heat_rejection_cost__cost` | 115778260.018 | 115740535.195 | -37724.8227895 |
| `remote_handling__cost` | 166690819.009 | 166663659.791 | -27159.2177014 |
| `coolant__cost` | 207374687.83 | 207627772.786 | 253084.956467 |
| `aux_cooling__aux_cost` | 3632518.14088 | 3631334.53264 | -1183.60824497 |
| `aux_cooling__cost` | 20332977.8315 | 20331794.2232 | -1183.60824497 |
| `buildings_cost__cost` | 652430848.368 | 652383020.903 | -47827.4655453 |
| `misc_cost__cost` | 71439219.112 | 71415941.5823 | -23277.5296572 |
| `om_cost__annual_om` | 55238372.908 | 55281108.7446 | 42735.8366099 |
| `cas71_calc__levelized` | 79490564.2944 | 79552063.1328 | 61498.8383776 |
| `shield_cost__cost` | 452151730.956 | 452063328.579 | -88402.3771285 |
| `divertor_cost__cost` | 109033211.401 | 109015446.435 | -17764.9659575 |
| `power_supplies_cost__cost` | 92733911.133 | 92712758.8117 | -21152.3213483 |
| `turbine_cost__cost` | 275541570.73 | 275451789.134 | -89781.5956584 |
| `structure_cost__cost` | 34161183.1492 | 34155617.2097 | -5565.93947768 |
| `precon_cost__cost` | 18515408.6024 | 18517354.6787 | 1946.07634835 |
| `waste__cost` | 6472486.86921 | 6470377.89451 | -2108.97469103 |
| `inc_cost__cost` | 81847329.9412 | 81829994.1835 | -17335.7577624 |
| `powercore_capital__powercore_capital` | 7192677213.51 | 7192380208.79 | -297004.712531 |
| `reactor_equipment_subtotal__reactor_equipment_subtotal` | 7359368032.52 | 7359043868.59 | -324163.930233 |
| `installation__cost` | 1030311524.55 | 1030266141.6 | -45382.9502326 |
| `cas22_capital__cas22_capital` | 8838357389.28 | 8838365796.81 | 8407.52754784 |
| `bop_capital__bop_capital` | 580126392.154 | 579937365.601 | -189026.552448 |
| `replacement_cost_per_event__replacement_cost_per_event` | 827587854.109 | 827429601.041 | -158253.067989 |
| `calendar__replacement_pv` | 1715096517.33 | 1714768553.02 | -327964.317525 |
| `calendar__cas72_annual` | 138213460.006 | 138187030.542 | -26429.4648293 |
| `cas70_calc__cas70` | 217704024.301 | 217739093.674 | 35069.3735483 |
| `cas70_calc__annual_total` | 218496530.266 | 218531599.639 | 35069.3735483 |
| `cas23_to_28_capital__cas23_to_28_capital` | 608941434.214 | 608752407.661 | -189026.552448 |
| `cas2x_pre_contingency__cas2x_pre_contingency` | 10099729671.9 | 10099501225.4 | -228446.490446 |
| `contingency__cost` | 1009972967.19 | 1009950122.54 | -22844.6490446 |
| `cas20_capital__cas20_capital` | 11109702639 | 11109451347.9 | -251291.139492 |
| `indirect__cost` | 2962587370.41 | 2962520359.44 | -67010.9705315 |
| `supplementary__cost` | 822952998.553 | 823425194.495 | 472195.941371 |
| `overnight_capital__overnight_capital` | 14955212350.4 | 14955400261.6 | 187911.245916 |
| `idc__cost` | 4224478411.22 | 4224531491.51 | 53080.2895341 |
| `cas90_1cfe_calc__cas90` | 1545622298.93 | 1545641719.57 | 19420.6411185 |
| `lcoe_1cfe_calc__lcoe` | 220.346320496 | 220.01256408 | -0.333756415879 |
| `total_capital__total_capital` | 14955212350.4 | 14955400261.6 | 187911.245916 |
| `lcoe_calc__lcoe` | 224.609524728 | 224.269232884 | -0.340291843655 |

## Unchanged scalars

83 common scalars are unchanged. The full exact list and values are retained in the companion JSON. Geometry, fusion, plasma sustainment, coil/casing/cold-volume quantities and source-held efficiencies do not depend on installed reserve or the repaired downstream heating route. Procurement remains installed; calendar timing remains neutron-fluence-driven. The installed-capacity diagnostic retains its original meaning. New operating outputs and efficiency assertions have no historical counterpart.
