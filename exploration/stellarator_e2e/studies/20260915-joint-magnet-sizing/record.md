# Joint magnet sizing native study

## 1. Study header

**Study id:** 20260915-joint-magnet-sizing. **Package:** stellarator_tea. **Date executed:** 2026-09-15 (local). **Executor:** goal coordinator. **Mode:** execute. **Arms:** arm-native.

## 2. Intake

Owner goal and scope are retained verbatim in preparation/owner-study-intake.txt.

> Can a magnet carry the required current at the selected operating margin, fit inside an explicitly allocated casing, and satisfy the existing plant constraints under one consistent set of construction and performance assumptions?

[AGENT] Protocol.md declares allocation-first native sizing, held criteria, staged bounds, scenario separation and limits. Runtime arithmetic lives in the native model; the harness supplies prepared independent inputs only.

## 3. Objective and result

**LCOE channel:** `stellarator_09__stellaris__lcoe_calc__lcoe`. No sampled default-performance case satisfies all20 predicates; there is no cheapest default feasible choice. Historical30T and enhanced-performance controls are excluded from that ranking. Full priced quantities and all cases are in results/analysis.json. Manufacturing remainder and mixed price bases remain unresolved. Finite samples imply no global optimum or global infeasibility.

## 4. Constraint outcomes

| constraint_id | source_local_identity | Status | Count/locations |
| --- | --- | --- | --- |
| stellarator_09__stellaris__wp_stress_ok__f38a102195da1dd0 | wp_stress_ok | satisfied | 347/347 satisfied; all point locations in native-cases.json |
| stellarator_09__stellaris__cond_strain_ok__251d4c803804ab60 | cond_strain_ok | satisfied | 347/347 satisfied; all point locations in native-cases.json |
| stellarator_09__stellaris__recirc_ok__afc3be66f0a3421b | recirc_ok | satisfied / violated | 346/347 satisfied; all point locations in native-cases.json |
| stellarator_09__stellaris__cycle_domain_ok__ba3fa9c3653b3fd3 | cycle_domain_ok | satisfied | 347/347 satisfied; all point locations in native-cases.json |
| stellarator_09__stellaris__beta_ok__82b78aad420730d5 | beta_ok | satisfied | 347/347 satisfied; all point locations in native-cases.json |
| stellarator_09__stellaris__heating_couple_positive_ok__697e87be76f504b7 | heating_couple_positive_ok | satisfied | 347/347 satisfied; all point locations in native-cases.json |
| stellarator_09__stellaris__divertor_heat_ok__26b4658f9fdfd7b7 | divertor_heat_ok | satisfied / violated | 85/347 satisfied; all point locations in native-cases.json |
| stellarator_09__stellaris__heating_source_upper_ok__14ddae450a8eda6f | heating_source_upper_ok | satisfied | 347/347 satisfied; all point locations in native-cases.json |
| stellarator_09__stellaris__net_positive__484521d56c02667a | net_positive | satisfied | 347/347 satisfied; all point locations in native-cases.json |
| stellarator_09__stellaris__burn_hold_ok__03c3f94b878e5b58 | burn_hold_ok | satisfied / violated | 157/347 satisfied; all point locations in native-cases.json |
| stellarator_09__stellaris__wall_load_ok__ab2c790419af93bb | wall_load_ok | satisfied / violated | 253/347 satisfied; all point locations in native-cases.json |
| stellarator_09__stellaris__tbr_ok__2cd198f674d413e4 | tbr_ok | satisfied | 347/347 satisfied; all point locations in native-cases.json |
| stellarator_09__stellaris__heating_couple_upper_ok__6cc9307cc149d650 | heating_couple_upper_ok | satisfied | 347/347 satisfied; all point locations in native-cases.json |
| stellarator_09__stellaris__peak_field_ok__49c6b8228a73cac5 | peak_field_ok | satisfied / violated | 182/347 satisfied; all point locations in native-cases.json |
| stellarator_09__stellaris__reference_conductor_current_ok__3cf239a7cdc0f2f0 | reference_conductor_current_ok | satisfied / violated | 343/347 satisfied; all point locations in native-cases.json |
| stellarator_09__stellaris__sustainment_ok__77add152ed8eafce | sustainment_ok | satisfied / violated | 272/347 satisfied; all point locations in native-cases.json |
| stellarator_09__stellaris__loop_capacity_ok__d77f6027ceb27852 | loop_capacity_ok | satisfied / violated | 109/347 satisfied; all point locations in native-cases.json |
| stellarator_09__stellaris__wp_fit_ok__a25ca6a0161f6339 | wp_fit_ok | satisfied / violated | 167/347 satisfied; all point locations in native-cases.json |
| stellarator_09__stellaris__heating_source_positive_ok__1e184791591370e5 | heating_source_positive_ok | satisfied | 347/347 satisfied; all point locations in native-cases.json |
| stellarator_09__stellaris__loop_pressure_ok__5905ab54f5e8a945 | loop_pressure_ok | satisfied | 347/347 satisfied; all point locations in native-cases.json |

Current, fit, other18 and all20 outcomes are reported separately in analysis.json. Domain refusals in initial-oracle-scan.json and final-selection.json have no inferred predicate verdict. Exact-boundary native/oracle sign disagreement remains separately in exact-boundary-diagnostic.json.

## 5. Framing

**As proposed:**

| Axis | Framing | Reason |
| --- | --- | --- |
| magnet__casing__assembly_clearance | sensitivity | Held historical control, inventory mode/reserve or separately labeled performance/shape scenario |
| magnet__casing__interior_y | search | Physical geometry/current/allocation choice |
| magnet__casing__wall_thickness | sensitivity | Held historical control, inventory mode/reserve or separately labeled performance/shape scenario |
| magnet__coil__I_coil | search | Physical geometry/current/allocation choice |
| magnet__coil__coil_t | search | Physical geometry/current/allocation choice |
| magnet__winding_pack__B_max | sensitivity | Held historical control, inventory mode/reserve or separately labeled performance/shape scenario |
| magnet__winding_pack__cabling_factor | sensitivity | Held historical control, inventory mode/reserve or separately labeled performance/shape scenario |
| magnet__winding_pack__degradation_factor | sensitivity | Held historical control, inventory mode/reserve or separately labeled performance/shape scenario |
| magnet__winding_pack__fit_aspect_ratio | sensitivity | Held historical control, inventory mode/reserve or separately labeled performance/shape scenario |
| magnet__winding_pack__ground_insulation | sensitivity | Held historical control, inventory mode/reserve or separately labeled performance/shape scenario |
| magnet__winding_pack__internal_build_y | sensitivity | Held historical control, inventory mode/reserve or separately labeled performance/shape scenario |
| magnet__winding_pack__inventory_multiplier | sensitivity | Held historical control, inventory mode/reserve or separately labeled performance/shape scenario |
| magnet__winding_pack__j_wp | sensitivity | Held historical control, inventory mode/reserve or separately labeled performance/shape scenario |
| magnet__winding_pack__material_factor | sensitivity | Held historical control, inventory mode/reserve or separately labeled performance/shape scenario |
| magnet__winding_pack__orientation_factor | sensitivity | Held historical control, inventory mode/reserve or separately labeled performance/shape scenario |
| magnet__winding_pack__sharing_factor | sensitivity | Held historical control, inventory mode/reserve or separately labeled performance/shape scenario |
| magnet__winding_pack__sizing_mode | sensitivity | Held historical control, inventory mode/reserve or separately labeled performance/shape scenario |
| plasma__R | search | Physical geometry/current/allocation choice |
| plasma__a | search | Physical geometry/current/allocation choice |

**As judged:**

| Axis | Framing | Changed | Reason |
| --- | --- | --- | --- |
| magnet__casing__assembly_clearance | sensitivity | no | Finite observed response retained; no continuous-boundary or qualification claim |
| magnet__casing__interior_y | search | no | Finite observed response retained; no continuous-boundary or qualification claim |
| magnet__casing__wall_thickness | sensitivity | no | Finite observed response retained; no continuous-boundary or qualification claim |
| magnet__coil__I_coil | search | no | Finite observed response retained; no continuous-boundary or qualification claim |
| magnet__coil__coil_t | search | no | Finite observed response retained; no continuous-boundary or qualification claim |
| magnet__winding_pack__B_max | sensitivity | no | Finite observed response retained; no continuous-boundary or qualification claim |
| magnet__winding_pack__cabling_factor | sensitivity | no | Finite observed response retained; no continuous-boundary or qualification claim |
| magnet__winding_pack__degradation_factor | sensitivity | no | Finite observed response retained; no continuous-boundary or qualification claim |
| magnet__winding_pack__fit_aspect_ratio | sensitivity | no | Finite observed response retained; no continuous-boundary or qualification claim |
| magnet__winding_pack__ground_insulation | sensitivity | no | Finite observed response retained; no continuous-boundary or qualification claim |
| magnet__winding_pack__internal_build_y | sensitivity | no | Finite observed response retained; no continuous-boundary or qualification claim |
| magnet__winding_pack__inventory_multiplier | sensitivity | no | Finite observed response retained; no continuous-boundary or qualification claim |
| magnet__winding_pack__j_wp | sensitivity | no | Finite observed response retained; no continuous-boundary or qualification claim |
| magnet__winding_pack__material_factor | sensitivity | no | Finite observed response retained; no continuous-boundary or qualification claim |
| magnet__winding_pack__orientation_factor | sensitivity | no | Finite observed response retained; no continuous-boundary or qualification claim |
| magnet__winding_pack__sharing_factor | sensitivity | no | Finite observed response retained; no continuous-boundary or qualification claim |
| magnet__winding_pack__sizing_mode | sensitivity | no | Finite observed response retained; no continuous-boundary or qualification claim |
| plasma__R | search | no | Finite observed response retained; no continuous-boundary or qualification claim |
| plasma__a | search | no | Finite observed response retained; no continuous-boundary or qualification claim |

## 6. Per-axis account

### magnet__casing__assembly_clearance

**Feasible structure applies:** not applicable: sensitivity-framed. Observed values: [0.002].

**Observed response applies:** yes. Paired scenario quantities and verdict locations are in analysis.json; no boundary claim is made.

| Value | Cases | Current passes | Fit passes | All 20 passes | LCOE range, $/MWh |
| --- | --- | --- | --- | --- | --- |
| 0.002 | 347 | 343 | 167 | 1 | 139.200–232.317 |

These aggregates mix other coordinates and historical controls; they are not isolated causal effects or default-only feasibility counts. See report.md for the separate default cohort and paired sensitivities.

### magnet__casing__interior_y

**Feasible structure applies:** yes. The prepared sample and endpoint results locate passing/failing coordinates, not a continuous boundary. Observed values: [0.4, 0.45, 0.5, 0.55, 0.6, 0.65, 0.75].

**Observed response applies:** not applicable: search-framed. Per-point responses remain in native-cases.json.

| Value | Cases | Current passes | Fit passes | All 20 passes | LCOE range, $/MWh |
| --- | --- | --- | --- | --- | --- |
| 0.4 | 73 | 69 | 2 | 1 | 141.681–195.107 |
| 0.45 | 1 | 1 | 0 | 0 | 164.050–164.050 |
| 0.5 | 1 | 1 | 0 | 0 | 164.050–164.050 |
| 0.55 | 65 | 65 | 0 | 0 | 142.918–196.804 |
| 0.6 | 69 | 69 | 32 | 0 | 144.163–198.511 |
| 0.65 | 74 | 74 | 69 | 0 | 139.200–232.317 |
| 0.75 | 64 | 64 | 64 | 0 | 145.415–200.226 |

These aggregates mix other coordinates and historical controls; they are not isolated causal effects or default-only feasibility counts. See report.md for the separate default cohort and paired sensitivities.

### magnet__casing__wall_thickness

**Feasible structure applies:** not applicable: sensitivity-framed. Observed values: [0.025].

**Observed response applies:** yes. Paired scenario quantities and verdict locations are in analysis.json; no boundary claim is made.

| Value | Cases | Current passes | Fit passes | All 20 passes | LCOE range, $/MWh |
| --- | --- | --- | --- | --- | --- |
| 0.025 | 347 | 343 | 167 | 1 | 139.200–232.317 |

These aggregates mix other coordinates and historical controls; they are not isolated causal effects or default-only feasibility counts. See report.md for the separate default cohort and paired sensitivities.

### magnet__coil__I_coil

**Feasible structure applies:** yes. The prepared sample and endpoint results locate passing/failing coordinates, not a continuous boundary. Observed values: [14600000.0, 15000000.0, 15400000.0, 15800000.0, 16200000.0, 17000000.0, 18000000.0].

**Observed response applies:** not applicable: search-framed. Per-point responses remain in native-cases.json.

| Value | Cases | Current passes | Fit passes | All 20 passes | LCOE range, $/MWh |
| --- | --- | --- | --- | --- | --- |
| 14600000.0 | 12 | 12 | 12 | 0 | 156.100–232.317 |
| 15000000.0 | 12 | 12 | 12 | 0 | 153.638–223.164 |
| 15400000.0 | 91 | 90 | 52 | 0 | 139.200–216.273 |
| 15800000.0 | 12 | 12 | 12 | 0 | 154.338–208.195 |
| 16200000.0 | 88 | 88 | 43 | 0 | 144.534–201.554 |
| 17000000.0 | 68 | 65 | 20 | 1 | 145.030–183.430 |
| 18000000.0 | 64 | 64 | 16 | 0 | 150.411–180.858 |

These aggregates mix other coordinates and historical controls; they are not isolated causal effects or default-only feasibility counts. See report.md for the separate default cohort and paired sensitivities.

### magnet__coil__coil_t

**Feasible structure applies:** yes. The prepared sample and endpoint results locate passing/failing coordinates, not a continuous boundary. Observed values: [0.3, 0.45, 0.5, 0.55, 0.6, 0.65, 0.7, 0.75].

**Observed response applies:** not applicable: search-framed. Per-point responses remain in native-cases.json.

| Value | Cases | Current passes | Fit passes | All 20 passes | LCOE range, $/MWh |
| --- | --- | --- | --- | --- | --- |
| 0.3 | 69 | 68 | 0 | 0 | 141.681–195.107 |
| 0.45 | 64 | 64 | 0 | 0 | 142.918–196.804 |
| 0.5 | 5 | 2 | 2 | 1 | 145.030–162.231 |
| 0.55 | 1 | 1 | 0 | 0 | 162.836–162.836 |
| 0.6 | 69 | 69 | 31 | 0 | 144.163–198.511 |
| 0.65 | 74 | 74 | 69 | 0 | 139.200–232.317 |
| 0.7 | 1 | 1 | 1 | 0 | 164.658–164.658 |
| 0.75 | 64 | 64 | 64 | 0 | 145.415–200.226 |

These aggregates mix other coordinates and historical controls; they are not isolated causal effects or default-only feasibility counts. See report.md for the separate default cohort and paired sensitivities.

### magnet__winding_pack__B_max

**Feasible structure applies:** not applicable: sensitivity-framed. Observed values: [24.9, 30.0].

**Observed response applies:** yes. Paired scenario quantities and verdict locations are in analysis.json; no boundary claim is made.

| Value | Cases | Current passes | Fit passes | All 20 passes | LCOE range, $/MWh |
| --- | --- | --- | --- | --- | --- |
| 24.9 | 343 | 342 | 165 | 0 | 139.200–232.317 |
| 30.0 | 4 | 1 | 2 | 1 | 145.030–153.877 |

These aggregates mix other coordinates and historical controls; they are not isolated causal effects or default-only feasibility counts. See report.md for the separate default cohort and paired sensitivities.

### magnet__winding_pack__cabling_factor

**Feasible structure applies:** not applicable: sensitivity-framed. Observed values: [0.9, 1.0].

**Observed response applies:** yes. Paired scenario quantities and verdict locations are in analysis.json; no boundary claim is made.

| Value | Cases | Current passes | Fit passes | All 20 passes | LCOE range, $/MWh |
| --- | --- | --- | --- | --- | --- |
| 0.9 | 4 | 4 | 0 | 0 | 166.950–180.426 |
| 1.0 | 343 | 339 | 167 | 1 | 139.200–232.317 |

These aggregates mix other coordinates and historical controls; they are not isolated causal effects or default-only feasibility counts. See report.md for the separate default cohort and paired sensitivities.

### magnet__winding_pack__degradation_factor

**Feasible structure applies:** not applicable: sensitivity-framed. Observed values: [0.9, 1.0].

**Observed response applies:** yes. Paired scenario quantities and verdict locations are in analysis.json; no boundary claim is made.

| Value | Cases | Current passes | Fit passes | All 20 passes | LCOE range, $/MWh |
| --- | --- | --- | --- | --- | --- |
| 0.9 | 4 | 4 | 0 | 0 | 166.950–180.426 |
| 1.0 | 343 | 339 | 167 | 1 | 139.200–232.317 |

These aggregates mix other coordinates and historical controls; they are not isolated causal effects or default-only feasibility counts. See report.md for the separate default cohort and paired sensitivities.

### magnet__winding_pack__fit_aspect_ratio

**Feasible structure applies:** not applicable: sensitivity-framed. Observed values: [0.8, 1.0, 1.25].

**Observed response applies:** yes. Paired scenario quantities and verdict locations are in analysis.json; no boundary claim is made.

| Value | Cases | Current passes | Fit passes | All 20 passes | LCOE range, $/MWh |
| --- | --- | --- | --- | --- | --- |
| 0.8 | 1 | 1 | 1 | 0 | 155.114–155.114 |
| 1.0 | 345 | 341 | 165 | 1 | 139.200–232.317 |
| 1.25 | 1 | 1 | 1 | 0 | 155.114–155.114 |

These aggregates mix other coordinates and historical controls; they are not isolated causal effects or default-only feasibility counts. See report.md for the separate default cohort and paired sensitivities.

### magnet__winding_pack__ground_insulation

**Feasible structure applies:** not applicable: sensitivity-framed. Observed values: [0.003].

**Observed response applies:** yes. Paired scenario quantities and verdict locations are in analysis.json; no boundary claim is made.

| Value | Cases | Current passes | Fit passes | All 20 passes | LCOE range, $/MWh |
| --- | --- | --- | --- | --- | --- |
| 0.003 | 347 | 343 | 167 | 1 | 139.200–232.317 |

These aggregates mix other coordinates and historical controls; they are not isolated causal effects or default-only feasibility counts. See report.md for the separate default cohort and paired sensitivities.

### magnet__winding_pack__internal_build_y

**Feasible structure applies:** not applicable: sensitivity-framed. Observed values: [0.025].

**Observed response applies:** yes. Paired scenario quantities and verdict locations are in analysis.json; no boundary claim is made.

| Value | Cases | Current passes | Fit passes | All 20 passes | LCOE range, $/MWh |
| --- | --- | --- | --- | --- | --- |
| 0.025 | 347 | 343 | 167 | 1 | 139.200–232.317 |

These aggregates mix other coordinates and historical controls; they are not isolated causal effects or default-only feasibility counts. See report.md for the separate default cohort and paired sensitivities.

### magnet__winding_pack__inventory_multiplier

**Feasible structure applies:** not applicable: sensitivity-framed. Observed values: [1.0, 1.01].

**Observed response applies:** yes. Paired scenario quantities and verdict locations are in analysis.json; no boundary claim is made.

| Value | Cases | Current passes | Fit passes | All 20 passes | LCOE range, $/MWh |
| --- | --- | --- | --- | --- | --- |
| 1.0 | 5 | 1 | 2 | 1 | 144.747–153.877 |
| 1.01 | 342 | 342 | 165 | 0 | 139.200–232.317 |

These aggregates mix other coordinates and historical controls; they are not isolated causal effects or default-only feasibility counts. See report.md for the separate default cohort and paired sensitivities.

### magnet__winding_pack__j_wp

**Feasible structure applies:** not applicable: sensitivity-framed. Observed values: [95.06172839506176, 118.8271604938272, 142.59259259259264].

**Observed response applies:** yes. Paired scenario quantities and verdict locations are in analysis.json; no boundary claim is made.

| Value | Cases | Current passes | Fit passes | All 20 passes | LCOE range, $/MWh |
| --- | --- | --- | --- | --- | --- |
| 95.06172839506176 | 1 | 0 | 0 | 0 | 153.877–153.877 |
| 118.8271604938272 | 344 | 342 | 165 | 0 | 139.200–232.317 |
| 142.59259259259264 | 2 | 1 | 2 | 1 | 145.030–145.030 |

These aggregates mix other coordinates and historical controls; they are not isolated causal effects or default-only feasibility counts. See report.md for the separate default cohort and paired sensitivities.

### magnet__winding_pack__material_factor

**Feasible structure applies:** not applicable: sensitivity-framed. Observed values: [1.0, 1.1, 1.35].

**Observed response applies:** yes. Paired scenario quantities and verdict locations are in analysis.json; no boundary claim is made.

| Value | Cases | Current passes | Fit passes | All 20 passes | LCOE range, $/MWh |
| --- | --- | --- | --- | --- | --- |
| 1.0 | 339 | 335 | 161 | 1 | 139.200–232.317 |
| 1.1 | 4 | 4 | 3 | 0 | 152.220–163.399 |
| 1.35 | 4 | 4 | 3 | 0 | 146.861–157.205 |

These aggregates mix other coordinates and historical controls; they are not isolated causal effects or default-only feasibility counts. See report.md for the separate default cohort and paired sensitivities.

### magnet__winding_pack__orientation_factor

**Feasible structure applies:** not applicable: sensitivity-framed. Observed values: [1.0, 2.0, 3.0].

**Observed response applies:** yes. Paired scenario quantities and verdict locations are in analysis.json; no boundary claim is made.

| Value | Cases | Current passes | Fit passes | All 20 passes | LCOE range, $/MWh |
| --- | --- | --- | --- | --- | --- |
| 1.0 | 342 | 338 | 163 | 0 | 141.681–232.317 |
| 2.0 | 4 | 4 | 3 | 0 | 139.200–148.349 |
| 3.0 | 1 | 1 | 1 | 1 | 145.030–145.030 |

These aggregates mix other coordinates and historical controls; they are not isolated causal effects or default-only feasibility counts. See report.md for the separate default cohort and paired sensitivities.

### magnet__winding_pack__sharing_factor

**Feasible structure applies:** not applicable: sensitivity-framed. Observed values: [0.9, 1.0].

**Observed response applies:** yes. Paired scenario quantities and verdict locations are in analysis.json; no boundary claim is made.

| Value | Cases | Current passes | Fit passes | All 20 passes | LCOE range, $/MWh |
| --- | --- | --- | --- | --- | --- |
| 0.9 | 4 | 4 | 0 | 0 | 166.950–180.426 |
| 1.0 | 343 | 339 | 167 | 1 | 139.200–232.317 |

These aggregates mix other coordinates and historical controls; they are not isolated causal effects or default-only feasibility counts. See report.md for the separate default cohort and paired sensitivities.

### magnet__winding_pack__sizing_mode

**Feasible structure applies:** not applicable: sensitivity-framed. Observed values: [0.0, 1.0].

**Observed response applies:** yes. Paired scenario quantities and verdict locations are in analysis.json; no boundary claim is made.

| Value | Cases | Current passes | Fit passes | All 20 passes | LCOE range, $/MWh |
| --- | --- | --- | --- | --- | --- |
| 0.0 | 5 | 1 | 2 | 1 | 144.747–153.877 |
| 1.0 | 342 | 342 | 165 | 0 | 139.200–232.317 |

These aggregates mix other coordinates and historical controls; they are not isolated causal effects or default-only feasibility counts. See report.md for the separate default cohort and paired sensitivities.

### plasma__R

**Feasible structure applies:** yes. The prepared sample and endpoint results locate passing/failing coordinates, not a continuous boundary. Observed values: [12.7, 13.1, 13.5, 14.25, 15.0].

**Observed response applies:** not applicable: search-framed. Per-point responses remain in native-cases.json.

| Value | Cases | Current passes | Fit passes | All 20 passes | LCOE range, $/MWh |
| --- | --- | --- | --- | --- | --- |
| 12.7 | 109 | 105 | 50 | 1 | 143.457–212.261 |
| 13.1 | 26 | 26 | 25 | 0 | 139.200–220.788 |
| 13.5 | 84 | 84 | 42 | 0 | 141.681–232.317 |
| 14.25 | 64 | 64 | 24 | 0 | 142.966–185.444 |
| 15.0 | 64 | 64 | 26 | 0 | 147.371–200.226 |

These aggregates mix other coordinates and historical controls; they are not isolated causal effects or default-only feasibility counts. See report.md for the separate default cohort and paired sensitivities.

### plasma__a

**Feasible structure applies:** yes. The prepared sample and endpoint results locate passing/failing coordinates, not a continuous boundary. Observed values: [1.15, 1.25, 1.3, 1.35, 1.45, 1.5, 1.7, 1.9].

**Observed response applies:** not applicable: search-framed. Per-point responses remain in native-cases.json.

| Value | Cases | Current passes | Fit passes | All 20 passes | LCOE range, $/MWh |
| --- | --- | --- | --- | --- | --- |
| 1.15 | 15 | 15 | 15 | 0 | 195.660–232.317 |
| 1.25 | 15 | 15 | 15 | 0 | 174.955–192.684 |
| 1.3 | 77 | 73 | 29 | 1 | 144.747–200.226 |
| 1.35 | 27 | 27 | 20 | 0 | 144.534–178.566 |
| 1.45 | 21 | 21 | 20 | 0 | 139.200–166.950 |
| 1.5 | 64 | 64 | 24 | 0 | 147.610–168.513 |
| 1.7 | 64 | 64 | 22 | 0 | 141.681–169.474 |
| 1.9 | 64 | 64 | 22 | 0 | 141.890–177.609 |

These aggregates mix other coordinates and historical controls; they are not isolated causal effects or default-only feasibility counts. See report.md for the separate default cohort and paired sensitivities.

## 7. Axis groups

| Axis | Qualified entry key | Provenance |
| --- | --- | --- |
| magnet__casing__assembly_clearance | stellarator_09__stellaris__magnet__casing__assembly_clearance | fan_out |
| magnet__casing__interior_y | stellarator_09__stellaris__magnet__casing__interior_y | fan_out |
| magnet__casing__wall_thickness | stellarator_09__stellaris__magnet__casing__wall_thickness | fan_out |
| magnet__coil__I_coil | stellarator_09__stellaris__magnet__coil__I_coil | fan_out |
| magnet__coil__coil_t | stellarator_09__stellaris__magnet__coil__coil_t | fan_out |
| magnet__winding_pack__B_max | stellarator_09__stellaris__magnet__winding_pack__B_max | fan_out |
| magnet__winding_pack__cabling_factor | stellarator_09__stellaris__magnet__winding_pack__cabling_factor | fan_out |
| magnet__winding_pack__degradation_factor | stellarator_09__stellaris__magnet__winding_pack__degradation_factor | fan_out |
| magnet__winding_pack__fit_aspect_ratio | stellarator_09__stellaris__magnet__winding_pack__fit_aspect_ratio | fan_out |
| magnet__winding_pack__ground_insulation | stellarator_09__stellaris__magnet__winding_pack__ground_insulation | fan_out |
| magnet__winding_pack__internal_build_y | stellarator_09__stellaris__magnet__winding_pack__internal_build_y | fan_out |
| magnet__winding_pack__inventory_multiplier | stellarator_09__stellaris__magnet__winding_pack__inventory_multiplier | fan_out |
| magnet__winding_pack__j_wp | stellarator_09__stellaris__magnet__winding_pack__j_wp | fan_out |
| magnet__winding_pack__material_factor | stellarator_09__stellaris__magnet__winding_pack__material_factor | fan_out |
| magnet__winding_pack__orientation_factor | stellarator_09__stellaris__magnet__winding_pack__orientation_factor | fan_out |
| magnet__winding_pack__sharing_factor | stellarator_09__stellaris__magnet__winding_pack__sharing_factor | fan_out |
| magnet__winding_pack__sizing_mode | stellarator_09__stellaris__magnet__winding_pack__sizing_mode | fan_out |
| plasma__R | stellarator_09__stellaris__plasma__R | fan_out |
| plasma__a | stellarator_09__stellaris__plasma__a | fan_out |

Complete public attribute groups, no new physical-identity ties. Inherited historical controls that stay constant are retained in declarations; they are not newly relaxed acceptance axes.

## 8. Indicators and rulings

| Axis | Indicator | Ruling |
| --- | --- | --- |
| magnet__casing__assembly_clearance | constraints_reachable | Owner delegated routine engineering/scenario choices; framing per §5 |
| magnet__casing__interior_y | constraints_reachable | Owner delegated routine engineering/scenario choices; framing per §5 |
| magnet__casing__wall_thickness | constraints_reachable | Owner delegated routine engineering/scenario choices; framing per §5 |
| magnet__coil__I_coil | constraints_reachable | Owner delegated routine engineering/scenario choices; framing per §5 |
| magnet__coil__coil_t | constraints_reachable | Owner delegated routine engineering/scenario choices; framing per §5 |
| magnet__winding_pack__B_max | constraints_reachable | Owner delegated routine engineering/scenario choices; framing per §5 |
| magnet__winding_pack__cabling_factor | constraints_reachable | Owner delegated routine engineering/scenario choices; framing per §5 |
| magnet__winding_pack__degradation_factor | constraints_reachable | Owner delegated routine engineering/scenario choices; framing per §5 |
| magnet__winding_pack__fit_aspect_ratio | constraints_reachable | Owner delegated routine engineering/scenario choices; framing per §5 |
| magnet__winding_pack__ground_insulation | constraints_reachable | Owner delegated routine engineering/scenario choices; framing per §5 |
| magnet__winding_pack__internal_build_y | constraints_reachable | Owner delegated routine engineering/scenario choices; framing per §5 |
| magnet__winding_pack__inventory_multiplier | constraints_reachable | Owner delegated routine engineering/scenario choices; framing per §5 |
| magnet__winding_pack__j_wp | constraints_reachable | Owner delegated routine engineering/scenario choices; framing per §5 |
| magnet__winding_pack__material_factor | constraints_reachable | Owner delegated routine engineering/scenario choices; framing per §5 |
| magnet__winding_pack__orientation_factor | constraints_reachable | Owner delegated routine engineering/scenario choices; framing per §5 |
| magnet__winding_pack__sharing_factor | constraints_reachable | Owner delegated routine engineering/scenario choices; framing per §5 |
| magnet__winding_pack__sizing_mode | constraints_reachable | Owner delegated routine engineering/scenario choices; framing per §5 |
| plasma__R | constraints_reachable | Owner delegated routine engineering/scenario choices; framing per §5 |
| plasma__a | constraints_reachable | Owner delegated routine engineering/scenario choices; framing per §5 |

No proposed group reports no_constraint_response. Indicators do not establish monotonicity, physical identity across different keys, or intra-module operand dependency. constraints_reachable means a possible path only; unresisted would be an agent judgment. Missing shape/cavity physics remains a finding despite conservative reachability.

## 9. Preflight results

All native gates passed; results/preflight_results.json retains each outcome and actual command provenance. Identity and baseline use package_identity.json and baseline_result.json. Package-clean evidence exists before/after execution. Integration retains the inherited assert_read_set_covered omission, with no substitute coverage claimed.

| Gate | Outcome | Detail |
| --- | --- | --- |
| declared_keys | pass | 19 declared keys across 19 groups, all package inputs |
| sibling_scan | pass | pass |
| identity | pass | kind sealed, digest 8e4aa8eaebf2667a74565e6e66fc9ce5947c6d27ccfc210f8452e82d87fba45f recomputed from 0 allowed-modified file(s) and 0 declared source(s); every other sealed artifact matches |
| manifest_currency | pass | both recorded package fingerprints match the package on disk |
| baseline_headline | pass | stellarator_09__stellaris__lcoe_calc__lcoe reproduces at relative deviation 0.000e+00; 20/20 pinned verdicts match |
| package_clean | pass | package tree is byte-untouched (git clean) |

## 10. Execution route and why

Study-local direct-API StudyRunner plus PreparedListStrategy on the stock strict loader. Coordinated allocation configurations and staged selected sensitivities need a prepared list. The baseline exercised this route before preflight. Every cohort point goes through native lifecycle and complete scalar publication. **Glue ledger: none.** No caller arithmetic supplies model outputs, no outer sizing solve, and no adaptive native search.

## 11. Study definition and window provenance

The engineered initial scan and retained refusal coordinates are in initial-oracle-scan.json. final-selection.json and reviews/window-selection.md explain refinements, separate sensitivities and the fixed native cohort. Endpoint diagnostics in edge-scan.json record caught/uncaught/unsupported edges from the selected anchor. Bounds are engineering assumptions supported by source-anchored geometry and existing domain guards, not proof of available space or physical feasibility limits. Required pack sizes motivated independently declared allocation ranges. A wider search could find additional designs or lower sampled cost; it cannot establish missing angle/construction/3D/structural/manufacturing evidence.

## 12. Cross-fingerprint correlation and what it means

Single executed fingerprint; no cross-arm correlation is needed. results/entering-all-points.json evaluates the frozen entering independent oracle at matched coordinates, and comparison-entering.json attributes changes. This is not older-native reexecution. Mode0 preservation and mode1 physical changes are separated; historical studies remain unchanged. All twenty predicate definitions are identical.

## 13. Verification

All-point comparison: 75646 scalar and 6940 independently derived predicate comparisons; outcome pass. Generic stratified verification is retained in verification_summary.json. sizing-residuals.json reports actual count/area/current closure; allocation precedes field so no numerical iteration or convergence failure exists in this model. Exact-boundary diagnostic disagreement is retained without relaxing acceptance. Native-store joins and every artifact digest are checked. Unmapped older channels are listed explicitly in oracle-all-points.json. Agreement certifies the stated computation, not measured conductor capability or unmodeled geometry.

## 14. Review outcomes

Independent source/math/interface, oracle/protocol and coupled implementation reviews are copied into preparation/ and reviews/. Coordinator window and release checks reuse that coverage. Final frozen-study/goal assurance is commissioned externally after this executor freeze and will be joined in the goal trail. The executor does not self-certify independent study review.

## 15. Findings

| Id | Kind | Finding | Disposition | Home |
| --- | --- | --- | --- | --- |
| `20260915-joint-magnet-sizing#1` | model | Current-driven inventory: Native minimum current sizing consistently drives pack, procurement and capacity; exact current closure is conditional consistency. | Proposed model extension / declared seam; goal review owns acceptance | work/orchestration/goals/joint-magnet-sizing-feasibility/goal.md |
| `20260915-joint-magnet-sizing#2` | model | Default joint feasibility: No sampled default-performance case satisfies all20 predicates; there is no cheapest default feasible choice. | Proposed model extension / declared seam; goal review owns acceptance | work/orchestration/goals/joint-magnet-sizing-feasibility/goal.md |
| `20260915-joint-magnet-sizing#3` | model | Accommodation and missing physics: Required cavity is compared with declared space; casing strength/thermal geometry, pack self-field and full3D interference remain unqualified. | Proposed model extension / declared seam; goal review owns acceptance | work/orchestration/goals/joint-magnet-sizing-feasibility/goal.md |
| `20260915-joint-magnet-sizing#4` | model | Performance and construction: Material/orientation/retention scenarios and required gain thresholds are conditional; no exact construction or local angle qualification. | Proposed model extension / declared seam; goal review owns acceptance | work/orchestration/goals/joint-magnet-sizing-feasibility/goal.md |
| `20260915-joint-magnet-sizing#5` | model | Cost completeness: Priced quantities respond to inventory/geometry, but manufacturing remainder, supplier premiums and mixed-year price bases remain unresolved. | Proposed model extension / declared seam; goal review owns acceptance | work/orchestration/goals/joint-magnet-sizing-feasibility/goal.md |
| `20260915-joint-magnet-sizing#6` | model | Numerical boundary and refusals: Exact multiplier1 native/oracle current signs differ at roundoff; diagnostic retained separately. Unsupported-field proposals carry no physical feasibility verdict. | Proposed model extension / declared seam; goal review owns acceptance | work/orchestration/goals/joint-magnet-sizing-feasibility/goal.md |
| `20260915-joint-magnet-sizing#7` | model | Finite search limits: Finite engineered sample and caught/uncaught endpoints establish no global infeasibility or optimum; H1 assessed on the default cohort in report.md. | Proposed model extension / declared seam; goal review owns acceptance | work/orchestration/goals/joint-magnet-sizing-feasibility/goal.md |

## 16. Snapshot

File: snapshot.json. SHA256: 330e0ac2411ce50ff59bd109bcce8c18a5c3d97141cb013a7b870c1689990154. Schema version1. It retains resolved lineage, windows, tools, artifacts and native store compatibility.

## 17. What this record does not contain

No independently qualified tape/cable product, local field-angle map, detailed support/casing certification,3D assembly verification or complete factory quote. Frozen entering oracle is retained, but the older native runtime was not reexecuted. Final fresh assurance lives in the goal evidence after this executor freeze. Source witness excerpts are retained; complete original source PDFs and full generated runtime distribution are not duplicated.

**END OF RECORD**
