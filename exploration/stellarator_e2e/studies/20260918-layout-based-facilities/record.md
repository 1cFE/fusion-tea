## 1. Study header

**Study:** `20260918-layout-based-facilities`. **Package:** `stellarator_e2e`. **Executed:** 2026-09-19. **Mode:** execute. **Executor:** coordinator, with this AGENT executor report generated from retained artifacts. **Arms:** one released package, 48 purposeful scenarios plus the separately executed pinned baseline. This is not an independent reviewer verdict.

## 2. Intake

[OWNER-VERBATIM] “Run a focused study showing how facility sizes and costs respond to equipment size and maintenance demand. Use matched cases to distinguish adding missing scope from changing the design. Report plant-cost and electricity-cost consequences, important assumptions and infeasible layouts. Do not optimize on unsupported clearance or throughput assumptions.”

The exact complete intake is preserved in [owner-prompt.md](preparation/owner-prompt.md). The owner subsequently ruled [OWNER-VERBATIM] “yes run both” on construction-rate and source-tonne sensitivities; see [the captured ruling](preparation/owner-ruling.md). [AGENT] The finite scenario list and its engineering levels are executor choices, not sourced confidence intervals.

## 3. Objective and result

**Objective channel:** `stellarator_09__stellaris__lcoe_calc__lcoe` (model dollars/MWh). Default14 layout LCOE is 273.454649; selected18 layout is 314.182417. Their matched legacy-cost results are 270.823875 and 310.632663 respectively. All 48 candidates are retained, including 20 with facility failures. 0/48 satisfy all 25 modeled plant predicates. These are modeled screening results. No optimum, licensed design or qualified whole-plant operating point is claimed.

See [report.md](report.md) for the scoped capital, geometry and logistics consequences. All numbers below are read from [native case exports](results/interpreted-cases.json); proposal IDs join to [inputs and scenario purposes](preparation/proposals.json).

## 4. Constraint outcomes

| constraint_id | source_local_identity | Observed status | Violated cases |
|---|---|---|---|
| `stellarator_09__stellaris__wp_stress_ok__f38a102195da1dd0` | `wp_stress_ok` | satisfied | none |
| `stellarator_09__stellaris__cond_strain_ok__251d4c803804ab60` | `cond_strain_ok` | satisfied | none |
| `stellarator_09__stellaris__recirc_ok__afc3be66f0a3421b` | `recirc_ok` | satisfied | none |
| `stellarator_09__stellaris__cycle_domain_ok__ba3fa9c3653b3fd3` | `cycle_domain_ok` | satisfied | none |
| `stellarator_09__stellaris__beta_ok__82b78aad420730d5` | `beta_ok` | satisfied | none |
| `stellarator_09__stellaris__heating_couple_positive_ok__697e87be76f504b7` | `heating_couple_positive_ok` | satisfied | none |
| `stellarator_09__stellaris__divertor_heat_ok__26b4658f9fdfd7b7` | `divertor_heat_ok` | satisfied, violated | `default14-legacy`, `default14-layout`, `R-13.334999999999999`, `a-1.2349999999999999`, `a-1.3650000000000002`, `circuits-12`, `circuits-18`, `circuits-22`, `default14-fixed-space`, `teams-1`, `teams-4`, `tasks-0.25`, `tasks-0.75`, `sector-hold6-mode0`, `cooling-hold16-mode0`, `long-process-mode0`, `sector-hold6-mode1`, `cooling-hold16-mode1`, `long-process-mode1`, `late-component_receipt_lead_days`, `late-initial_receipt_lead_days`, `late-cooling_receipt_lead_days`, `late-cooling_initial_receipt_lead_days`, `three-machine-stations`, `narrow-cooling_aisle_width`, `narrow-cooling_cross_width`, `provisional_envelope_scale-0.8`, `provisional_envelope_scale-1.2`, `nuclear_wall-1`, `nuclear_wall-3`, `conventional_wall-0.2`, `conventional_wall-0.5`, `civil_rate_multiplier-0.5`, `civil_rate_multiplier-2.0`, `rebar-100-75`, `rebar-200-150`, `metric-tonne`, `no-cooling-replacement`, `no-sector-replacement`, `lower-packing-mode0`, `lower-packing-mode1`, `wide_helium`, `long_salt`, `slow_initial_delivery` |
| `stellarator_09__stellaris__facility_capacity_ok__8acbe7a714e6a4d9` | `facility_capacity_ok` | satisfied, violated | `selected18-fixed-space`, `sector-hold6-mode0`, `cooling-hold16-mode0`, `long-process-mode0`, `three-machine-stations`, `lower-packing-mode0` |
| `stellarator_09__stellaris__facility_outage_ok__9b00e5bd8ea45722` | `facility_outage_ok` | satisfied, violated | `teams-1`, `tasks-0.75`, `lower-packing-mode0`, `lower-packing-mode1` |
| `stellarator_09__stellaris__heating_source_upper_ok__14ddae450a8eda6f` | `heating_source_upper_ok` | satisfied | none |
| `stellarator_09__stellaris__net_positive__484521d56c02667a` | `net_positive` | satisfied | none |
| `stellarator_09__stellaris__burn_hold_ok__03c3f94b878e5b58` | `burn_hold_ok` | satisfied | none |
| `stellarator_09__stellaris__wall_load_ok__ab2c790419af93bb` | `wall_load_ok` | satisfied, violated | `R-13.334999999999999` |
| `stellarator_09__stellaris__tbr_ok__2cd198f674d413e4` | `tbr_ok` | violated | `default14-legacy`, `default14-layout`, `selected18-legacy`, `selected18-layout`, `R-12.065`, `R-13.334999999999999`, `a-1.2349999999999999`, `a-1.3650000000000002`, `circuits-12`, `circuits-18`, `circuits-22`, `default14-fixed-space`, `selected18-fixed-space`, `teams-1`, `teams-4`, `tasks-0.25`, `tasks-0.75`, `sector-hold6-mode0`, `cooling-hold16-mode0`, `long-process-mode0`, `sector-hold6-mode1`, `cooling-hold16-mode1`, `long-process-mode1`, `late-component_receipt_lead_days`, `late-initial_receipt_lead_days`, `late-cooling_receipt_lead_days`, `late-cooling_initial_receipt_lead_days`, `three-machine-stations`, `narrow-cooling_aisle_width`, `narrow-cooling_cross_width`, `provisional_envelope_scale-0.8`, `provisional_envelope_scale-1.2`, `nuclear_wall-1`, `nuclear_wall-3`, `conventional_wall-0.2`, `conventional_wall-0.5`, `civil_rate_multiplier-0.5`, `civil_rate_multiplier-2.0`, `rebar-100-75`, `rebar-200-150`, `metric-tonne`, `no-cooling-replacement`, `no-sector-replacement`, `lower-packing-mode0`, `lower-packing-mode1`, `wide_helium`, `long_salt`, `slow_initial_delivery` |
| `stellarator_09__stellaris__heating_couple_upper_ok__6cc9307cc149d650` | `heating_couple_upper_ok` | satisfied | none |
| `stellarator_09__stellaris__peak_field_ok__49c6b8228a73cac5` | `peak_field_ok` | satisfied, violated | `R-12.065`, `a-1.3650000000000002` |
| `stellarator_09__stellaris__reference_conductor_current_ok__3cf239a7cdc0f2f0` | `reference_conductor_current_ok` | satisfied, violated | `default14-legacy`, `default14-layout`, `R-12.065`, `R-13.334999999999999`, `a-1.2349999999999999`, `a-1.3650000000000002`, `circuits-12`, `circuits-18`, `circuits-22`, `default14-fixed-space`, `teams-1`, `teams-4`, `tasks-0.25`, `tasks-0.75`, `sector-hold6-mode0`, `cooling-hold16-mode0`, `long-process-mode0`, `sector-hold6-mode1`, `cooling-hold16-mode1`, `long-process-mode1`, `late-component_receipt_lead_days`, `late-initial_receipt_lead_days`, `late-cooling_receipt_lead_days`, `late-cooling_initial_receipt_lead_days`, `three-machine-stations`, `narrow-cooling_aisle_width`, `narrow-cooling_cross_width`, `provisional_envelope_scale-0.8`, `provisional_envelope_scale-1.2`, `nuclear_wall-1`, `nuclear_wall-3`, `conventional_wall-0.2`, `conventional_wall-0.5`, `civil_rate_multiplier-0.5`, `civil_rate_multiplier-2.0`, `rebar-100-75`, `rebar-200-150`, `metric-tonne`, `no-cooling-replacement`, `no-sector-replacement`, `lower-packing-mode0`, `lower-packing-mode1`, `wide_helium`, `long_salt`, `slow_initial_delivery` |
| `stellarator_09__stellaris__facility_routes_ok__a3dca4061c7bcc9b` | `facility_routes_ok` | satisfied, violated | `circuits-22`, `cooling-hold16-mode1`, `narrow-cooling_aisle_width`, `narrow-cooling_cross_width`, `wide_helium`, `long_salt` |
| `stellarator_09__stellaris__sustainment_ok__77add152ed8eafce` | `sustainment_ok` | satisfied, violated | `R-13.334999999999999`, `a-1.2349999999999999` |
| `stellarator_09__stellaris__loop_capacity_ok__d77f6027ceb27852` | `loop_capacity_ok` | satisfied, violated | `R-13.334999999999999`, `circuits-12` |
| `stellarator_09__stellaris__wp_fit_ok__a25ca6a0161f6339` | `wp_fit_ok` | satisfied, violated | `default14-legacy`, `default14-layout`, `R-12.065`, `R-13.334999999999999`, `a-1.2349999999999999`, `a-1.3650000000000002`, `circuits-12`, `circuits-18`, `circuits-22`, `default14-fixed-space`, `teams-1`, `teams-4`, `tasks-0.25`, `tasks-0.75`, `sector-hold6-mode0`, `cooling-hold16-mode0`, `long-process-mode0`, `sector-hold6-mode1`, `cooling-hold16-mode1`, `long-process-mode1`, `late-component_receipt_lead_days`, `late-initial_receipt_lead_days`, `late-cooling_receipt_lead_days`, `late-cooling_initial_receipt_lead_days`, `three-machine-stations`, `narrow-cooling_aisle_width`, `narrow-cooling_cross_width`, `provisional_envelope_scale-0.8`, `provisional_envelope_scale-1.2`, `nuclear_wall-1`, `nuclear_wall-3`, `conventional_wall-0.2`, `conventional_wall-0.5`, `civil_rate_multiplier-0.5`, `civil_rate_multiplier-2.0`, `rebar-100-75`, `rebar-200-150`, `metric-tonne`, `no-cooling-replacement`, `no-sector-replacement`, `lower-packing-mode0`, `lower-packing-mode1`, `wide_helium`, `long_salt`, `slow_initial_delivery` |
| `stellarator_09__stellaris__facility_replacement_ready__00706bc8dbdf6938` | `facility_replacement_ready` | satisfied, violated | `late-component_receipt_lead_days`, `late-cooling_receipt_lead_days` |
| `stellarator_09__stellaris__heating_source_positive_ok__1e184791591370e5` | `heating_source_positive_ok` | satisfied | none |
| `stellarator_09__stellaris__loop_pressure_ok__5905ab54f5e8a945` | `loop_pressure_ok` | satisfied | none |
| `stellarator_09__stellaris__facility_initial_ready__d3a5b04c428ef75f` | `facility_initial_ready` | satisfied, violated | `teams-1`, `late-initial_receipt_lead_days`, `late-cooling_initial_receipt_lead_days`, `lower-packing-mode0`, `lower-packing-mode1`, `slow_initial_delivery` |

Every qualified predicate and its exact case outcome is retained in the native store and [case export](results/interpreted-cases.json). Numeric facility margins are separately reported; satisfied predicates do not override zero qualification disclosures.

## 5. Framing

**As proposed:** All 42 groups are sensitivity-framed, including retained selected18 comparison context. **As judged after execution:** Sensitivity remains the appropriate framing for every group. Named failures locate tested conflicts; they do not establish an optimized boundary or a physical confidence interval. Multi-input cases are coordinated scenarios, not isolated causal effects.

## 6. Per-axis account

#### `blanket__first_wall__fluence_limit` — feasible structure (search framing)

**Applies:** not applicable; sensitivity-framed.

#### `blanket__first_wall__fluence_limit` — observed response (sensitivity framing)

**Applies:** yes. Resolved levels: `{'blanket__first_wall__fluence_limit': [18.0, 180.0]}`. Cases: `no-sector-replacement`. LCOE 229.448559–229.448559 dollars/MWh; gross building area 87,842.423–87,842.423 m². Reported ranges describe the named cases; coordinated cases change more than one input and are not isolated single-axis effects. No boundary claim. Facility failures: No facility predicate fails in these named cases. Full plant failures at these same locations are listed by qualified identity in §4.

#### `buildings__civil_rate_multiplier` — feasible structure (search framing)

**Applies:** not applicable; sensitivity-framed.

#### `buildings__civil_rate_multiplier` — observed response (sensitivity framing)

**Applies:** yes. Resolved levels: `{'buildings__civil_rate_multiplier': [0.5, 1.0, 2.0]}`. Cases: `civil_rate_multiplier-0.5`, `civil_rate_multiplier-2.0`. LCOE 267.658290–285.047368 dollars/MWh; gross building area 100,059.551–100,059.551 m². Reported ranges describe the named cases; coordinated cases change more than one input and are not isolated single-axis effects. No boundary claim. Facility failures: No facility predicate fails in these named cases. Full plant failures at these same locations are listed by qualified identity in §4.

#### `buildings__component_hold_days` — feasible structure (search framing)

**Applies:** not applicable; sensitivity-framed.

#### `buildings__component_hold_days` — observed response (sensitivity framing)

**Applies:** yes. Resolved levels: `{'buildings__component_hold_days': [365.25, 2191.5]}`. Cases: `sector-hold6-mode0`, `sector-hold6-mode1`. LCOE 273.454649–276.974299 dollars/MWh; gross building area 100,059.551–122,050.381 m². Reported ranges describe the named cases; coordinated cases change more than one input and are not isolated single-axis effects. No boundary claim. Facility failures: `sector-hold6-mode0`: facility_capacity_ok Full plant failures at these same locations are listed by qualified identity in §4.

#### `buildings__component_install_days` — feasible structure (search framing)

**Applies:** not applicable; sensitivity-framed.

#### `buildings__component_install_days` — observed response (sensitivity framing)

**Applies:** yes. Resolved levels: `{'buildings__component_install_days': [0.25, 0.5, 0.75]}`. Cases: `tasks-0.25`, `tasks-0.75`. LCOE 272.668069–274.239453 dollars/MWh; gross building area 95,172.700–104,946.402 m². Reported ranges describe the named cases; coordinated cases change more than one input and are not isolated single-axis effects. No boundary claim. Facility failures: `tasks-0.75`: facility_outage_ok Full plant failures at these same locations are listed by qualified identity in §4.

#### `buildings__component_material_fraction` — feasible structure (search framing)

**Applies:** not applicable; sensitivity-framed.

#### `buildings__component_material_fraction` — observed response (sensitivity framing)

**Applies:** yes. Resolved levels: `{'buildings__component_material_fraction': [0.25, 0.5]}`. Cases: `lower-packing-mode0`, `lower-packing-mode1`. LCOE 273.454649–278.141490 dollars/MWh; gross building area 100,059.551–129,380.657 m². Reported ranges describe the named cases; coordinated cases change more than one input and are not isolated single-axis effects. No boundary claim. Facility failures: `lower-packing-mode0`: facility_capacity_ok, facility_outage_ok, facility_initial_ready; `lower-packing-mode1`: facility_outage_ok, facility_initial_ready Full plant failures at these same locations are listed by qualified identity in §4.

#### `buildings__component_receipt_lead_days` — feasible structure (search framing)

**Applies:** not applicable; sensitivity-framed.

#### `buildings__component_receipt_lead_days` — observed response (sensitivity framing)

**Applies:** yes. Resolved levels: `{'buildings__component_receipt_lead_days': [30.0, 90.0]}`. Cases: `late-component_receipt_lead_days`. LCOE 273.454649–273.454649 dollars/MWh; gross building area 100,059.551–100,059.551 m². Reported ranges describe the named cases; coordinated cases change more than one input and are not isolated single-axis effects. No boundary claim. Facility failures: `late-component_receipt_lead_days`: facility_replacement_ready Full plant failures at these same locations are listed by qualified identity in §4.

#### `buildings__component_remove_days` — feasible structure (search framing)

**Applies:** not applicable; sensitivity-framed.

#### `buildings__component_remove_days` — observed response (sensitivity framing)

**Applies:** yes. Resolved levels: `{'buildings__component_remove_days': [0.25, 0.5, 0.75]}`. Cases: `tasks-0.25`, `tasks-0.75`. LCOE 272.668069–274.239453 dollars/MWh; gross building area 95,172.700–104,946.402 m². Reported ranges describe the named cases; coordinated cases change more than one input and are not isolated single-axis effects. No boundary claim. Facility failures: `tasks-0.75`: facility_outage_ok Full plant failures at these same locations are listed by qualified identity in §4.

#### `buildings__conventional_rebar_density` — feasible structure (search framing)

**Applies:** not applicable; sensitivity-framed.

#### `buildings__conventional_rebar_density` — observed response (sensitivity framing)

**Applies:** yes. Resolved levels: `{'buildings__conventional_rebar_density': [75.0, 100.0, 150.0]}`. Cases: `rebar-100-75`, `rebar-200-150`. LCOE 272.080339–274.921890 dollars/MWh; gross building area 100,059.551–100,059.551 m². Reported ranges describe the named cases; coordinated cases change more than one input and are not isolated single-axis effects. No boundary claim. Facility failures: No facility predicate fails in these named cases. Full plant failures at these same locations are listed by qualified identity in §4.

#### `buildings__conventional_wall` — feasible structure (search framing)

**Applies:** not applicable; sensitivity-framed.

#### `buildings__conventional_wall` — observed response (sensitivity framing)

**Applies:** yes. Resolved levels: `{'buildings__conventional_wall': [0.2, 0.3, 0.5]}`. Cases: `conventional_wall-0.2`, `conventional_wall-0.5`. LCOE 273.357667–273.649983 dollars/MWh; gross building area 99,699.292–100,784.988 m². Reported ranges describe the named cases; coordinated cases change more than one input and are not isolated single-axis effects. No boundary claim. Facility failures: No facility predicate fails in these named cases. Full plant failures at these same locations are listed by qualified identity in §4.

#### `buildings__cooling_aisle_width` — feasible structure (search framing)

**Applies:** not applicable; sensitivity-framed.

#### `buildings__cooling_aisle_width` — observed response (sensitivity framing)

**Applies:** yes. Resolved levels: `{'buildings__cooling_aisle_width': [5.0, 6.0]}`. Cases: `narrow-cooling_aisle_width`. LCOE 273.373349–273.373349 dollars/MWh; gross building area 97,940.151–97,940.151 m². Reported ranges describe the named cases; coordinated cases change more than one input and are not isolated single-axis effects. No boundary claim. Facility failures: `narrow-cooling_aisle_width`: facility_routes_ok Full plant failures at these same locations are listed by qualified identity in §4.

#### `buildings__cooling_bundle_process_days` — feasible structure (search framing)

**Applies:** not applicable; sensitivity-framed.

#### `buildings__cooling_bundle_process_days` — observed response (sensitivity framing)

**Applies:** yes. Resolved levels: `{'buildings__cooling_bundle_process_days': [5.0, 400.0]}`. Cases: `long-process-mode0`, `long-process-mode1`. LCOE 273.454649–273.506009 dollars/MWh; gross building area 100,059.551–100,947.451 m². Reported ranges describe the named cases; coordinated cases change more than one input and are not isolated single-axis effects. No boundary claim. Facility failures: `long-process-mode0`: facility_capacity_ok Full plant failures at these same locations are listed by qualified identity in §4.

#### `buildings__cooling_cross_width` — feasible structure (search framing)

**Applies:** not applicable; sensitivity-framed.

#### `buildings__cooling_cross_width` — observed response (sensitivity framing)

**Applies:** yes. Resolved levels: `{'buildings__cooling_cross_width': [13.0, 17.0]}`. Cases: `narrow-cooling_cross_width`. LCOE 273.432638–273.432638 dollars/MWh; gross building area 99,374.351–99,374.351 m². Reported ranges describe the named cases; coordinated cases change more than one input and are not isolated single-axis effects. No boundary claim. Facility failures: `narrow-cooling_cross_width`: facility_routes_ok Full plant failures at these same locations are listed by qualified identity in §4.

#### `buildings__cooling_hold_days` — feasible structure (search framing)

**Applies:** not applicable; sensitivity-framed.

#### `buildings__cooling_hold_days` — observed response (sensitivity framing)

**Applies:** yes. Resolved levels: `{'buildings__cooling_hold_days': [365.25, 5844.0]}`. Cases: `cooling-hold16-mode0`, `cooling-hold16-mode1`. LCOE 273.454649–273.897443 dollars/MWh; gross building area 100,059.551–107,709.151 m². Reported ranges describe the named cases; coordinated cases change more than one input and are not isolated single-axis effects. No boundary claim. Facility failures: `cooling-hold16-mode0`: facility_capacity_ok; `cooling-hold16-mode1`: facility_routes_ok Full plant failures at these same locations are listed by qualified identity in §4.

#### `buildings__cooling_initial_receipt_lead_days` — feasible structure (search framing)

**Applies:** not applicable; sensitivity-framed.

#### `buildings__cooling_initial_receipt_lead_days` — observed response (sensitivity framing)

**Applies:** yes. Resolved levels: `{'buildings__cooling_initial_receipt_lead_days': [1.0, 180.0]}`. Cases: `late-cooling_initial_receipt_lead_days`. LCOE 273.454649–273.454649 dollars/MWh; gross building area 100,059.551–100,059.551 m². Reported ranges describe the named cases; coordinated cases change more than one input and are not isolated single-axis effects. No boundary claim. Facility failures: `late-cooling_initial_receipt_lead_days`: facility_initial_ready Full plant failures at these same locations are listed by qualified identity in §4.

#### `buildings__cooling_machine_process_days` — feasible structure (search framing)

**Applies:** not applicable; sensitivity-framed.

#### `buildings__cooling_machine_process_days` — observed response (sensitivity framing)

**Applies:** yes. Resolved levels: `{'buildings__cooling_machine_process_days': [2.0, 200.0]}`. Cases: `long-process-mode0`, `long-process-mode1`. LCOE 273.454649–273.506009 dollars/MWh; gross building area 100,059.551–100,947.451 m². Reported ranges describe the named cases; coordinated cases change more than one input and are not isolated single-axis effects. No boundary claim. Facility failures: `long-process-mode0`: facility_capacity_ok Full plant failures at these same locations are listed by qualified identity in §4.

#### `buildings__cooling_machine_stations` — feasible structure (search framing)

**Applies:** not applicable; sensitivity-framed.

#### `buildings__cooling_machine_stations` — observed response (sensitivity framing)

**Applies:** yes. Resolved levels: `{'buildings__cooling_machine_stations': [2.0, 3.0]}`. Cases: `three-machine-stations`. LCOE 273.454649–273.454649 dollars/MWh; gross building area 100,059.551–100,059.551 m². Reported ranges describe the named cases; coordinated cases change more than one input and are not isolated single-axis effects. No boundary claim. Facility failures: `three-machine-stations`: facility_capacity_ok Full plant failures at these same locations are listed by qualified identity in §4.

#### `buildings__cooling_receipt_lead_days` — feasible structure (search framing)

**Applies:** not applicable; sensitivity-framed.

#### `buildings__cooling_receipt_lead_days` — observed response (sensitivity framing)

**Applies:** yes. Resolved levels: `{'buildings__cooling_receipt_lead_days': [1.0, 90.0]}`. Cases: `late-cooling_receipt_lead_days`. LCOE 273.454649–273.454649 dollars/MWh; gross building area 100,059.551–100,059.551 m². Reported ranges describe the named cases; coordinated cases change more than one input and are not isolated single-axis effects. No boundary claim. Facility failures: `late-cooling_receipt_lead_days`: facility_replacement_ready Full plant failures at these same locations are listed by qualified identity in §4.

#### `buildings__facilities_capacity_mode` — feasible structure (search framing)

**Applies:** not applicable; sensitivity-framed.

#### `buildings__facilities_capacity_mode` — observed response (sensitivity framing)

**Applies:** yes. Resolved levels: `{'buildings__facilities_capacity_mode': [0.0, 1.0]}`. Cases: `default14-fixed-space`, `sector-hold6-mode0`, `cooling-hold16-mode0`, `long-process-mode0`, `sector-hold6-mode1`, `cooling-hold16-mode1`, `long-process-mode1`, `lower-packing-mode0`, `lower-packing-mode1`. LCOE 273.454649–278.141490 dollars/MWh; gross building area 100,059.551–129,380.657 m². Reported ranges describe the named cases; coordinated cases change more than one input and are not isolated single-axis effects. No boundary claim. Facility failures: `sector-hold6-mode0`: facility_capacity_ok; `cooling-hold16-mode0`: facility_capacity_ok; `long-process-mode0`: facility_capacity_ok; `cooling-hold16-mode1`: facility_routes_ok; `lower-packing-mode0`: facility_capacity_ok, facility_outage_ok, facility_initial_ready; `lower-packing-mode1`: facility_outage_ok, facility_initial_ready Full plant failures at these same locations are listed by qualified identity in §4.

#### `buildings__facilities_cost_mode` — feasible structure (search framing)

**Applies:** not applicable; sensitivity-framed.

#### `buildings__facilities_cost_mode` — observed response (sensitivity framing)

**Applies:** yes. Resolved levels: `{'buildings__facilities_cost_mode': [0.0, 1.0]}`. Cases: `default14-legacy`, `default14-layout`. LCOE 270.823875–273.454649 dollars/MWh; gross building area 100,059.551–100,059.551 m². Reported ranges describe the named cases; coordinated cases change more than one input and are not isolated single-axis effects. No boundary claim. Facility failures: No facility predicate fails in these named cases. Full plant failures at these same locations are listed by qualified identity in §4.

#### `buildings__initial_receipt_lead_days` — feasible structure (search framing)

**Applies:** not applicable; sensitivity-framed.

#### `buildings__initial_receipt_lead_days` — observed response (sensitivity framing)

**Applies:** yes. Resolved levels: `{'buildings__initial_receipt_lead_days': [20.0, 180.0]}`. Cases: `late-initial_receipt_lead_days`. LCOE 273.454649–273.454649 dollars/MWh; gross building area 100,059.551–100,059.551 m². Reported ranges describe the named cases; coordinated cases change more than one input and are not isolated single-axis effects. No boundary claim. Facility failures: `late-initial_receipt_lead_days`: facility_initial_ready Full plant failures at these same locations are listed by qualified identity in §4.

#### `buildings__nuclear_rebar_density` — feasible structure (search framing)

**Applies:** not applicable; sensitivity-framed.

#### `buildings__nuclear_rebar_density` — observed response (sensitivity framing)

**Applies:** yes. Resolved levels: `{'buildings__nuclear_rebar_density': [100.0, 150.0, 200.0]}`. Cases: `rebar-100-75`, `rebar-200-150`. LCOE 272.080339–274.921890 dollars/MWh; gross building area 100,059.551–100,059.551 m². Reported ranges describe the named cases; coordinated cases change more than one input and are not isolated single-axis effects. No boundary claim. Facility failures: No facility predicate fails in these named cases. Full plant failures at these same locations are listed by qualified identity in §4.

#### `buildings__nuclear_wall` — feasible structure (search framing)

**Applies:** not applicable; sensitivity-framed.

#### `buildings__nuclear_wall` — observed response (sensitivity framing)

**Applies:** yes. Resolved levels: `{'buildings__nuclear_wall': [1.0, 2.0, 3.0]}`. Cases: `nuclear_wall-1`, `nuclear_wall-3`. LCOE 271.537713–275.485619 dollars/MWh; gross building area 95,244.888–105,082.214 m². Reported ranges describe the named cases; coordinated cases change more than one input and are not isolated single-axis effects. No boundary claim. Facility failures: No facility predicate fails in these named cases. Full plant failures at these same locations are listed by qualified identity in §4.

#### `buildings__provisional_envelope_scale` — feasible structure (search framing)

**Applies:** not applicable; sensitivity-framed.

#### `buildings__provisional_envelope_scale` — observed response (sensitivity framing)

**Applies:** yes. Resolved levels: `{'buildings__provisional_envelope_scale': [0.8, 1.0, 1.2]}`. Cases: `provisional_envelope_scale-0.8`, `provisional_envelope_scale-1.2`. LCOE 273.194404–273.761427 dollars/MWh; gross building area 98,164.111–102,285.231 m². Reported ranges describe the named cases; coordinated cases change more than one input and are not isolated single-axis effects. No boundary claim. Facility failures: No facility predicate fails in these named cases. Full plant failures at these same locations are listed by qualified identity in §4.

#### `buildings__sector_service_teams` — feasible structure (search framing)

**Applies:** not applicable; sensitivity-framed.

#### `buildings__sector_service_teams` — observed response (sensitivity framing)

**Applies:** yes. Resolved levels: `{'buildings__sector_service_teams': [1.0, 2.0, 4.0]}`. Cases: `teams-1`, `teams-4`. LCOE 273.454649–273.454649 dollars/MWh; gross building area 100,059.551–100,059.551 m². Reported ranges describe the named cases; coordinated cases change more than one input and are not isolated single-axis effects. No boundary claim. Facility failures: `teams-1`: facility_outage_ok, facility_initial_ready Full plant failures at these same locations are listed by qualified identity in §4.

#### `buildings__tonne_interpretation_kg` — feasible structure (search framing)

**Applies:** not applicable; sensitivity-framed.

#### `buildings__tonne_interpretation_kg` — observed response (sensitivity framing)

**Applies:** yes. Resolved levels: `{'buildings__tonne_interpretation_kg': [907.18474, 1000.0]}`. Cases: `metric-tonne`. LCOE 273.063353–273.063353 dollars/MWh; gross building area 100,059.551–100,059.551 m². Reported ranges describe the named cases; coordinated cases change more than one input and are not isolated single-axis effects. No boundary claim. Facility failures: No facility predicate fails in these named cases. Full plant failures at these same locations are listed by qualified identity in §4.

#### `heat_transport__equipment_bundle_life` — feasible structure (search framing)

**Applies:** not applicable; sensitivity-framed.

#### `heat_transport__equipment_bundle_life` — observed response (sensitivity framing)

**Applies:** yes. Resolved levels: `{'heat_transport__equipment_bundle_life': [15.0, 30.0]}`. Cases: `no-cooling-replacement`. LCOE 266.135542–266.135542 dollars/MWh; gross building area 94,158.431–94,158.431 m². Reported ranges describe the named cases; coordinated cases change more than one input and are not isolated single-axis effects. No boundary claim. Facility failures: No facility predicate fails in these named cases. Full plant failures at these same locations are listed by qualified identity in §4.

#### `heat_transport__equipment_machine_life` — feasible structure (search framing)

**Applies:** not applicable; sensitivity-framed.

#### `heat_transport__equipment_machine_life` — observed response (sensitivity framing)

**Applies:** yes. Resolved levels: `{'heat_transport__equipment_machine_life': [10.0, 30.0]}`. Cases: `no-cooling-replacement`. LCOE 266.135542–266.135542 dollars/MWh; gross building area 94,158.431–94,158.431 m². Reported ranges describe the named cases; coordinated cases change more than one input and are not isolated single-axis effects. No boundary claim. Facility failures: No facility predicate fails in these named cases. Full plant failures at these same locations are listed by qualified identity in §4.

#### `heat_transport__n_loops` — feasible structure (search framing)

**Applies:** not applicable; sensitivity-framed.

#### `heat_transport__n_loops` — observed response (sensitivity framing)

**Applies:** yes. Resolved levels: `{'heat_transport__n_loops': [12.0, 14.0, 18.0, 22.0]}`. Cases: `circuits-12`, `circuits-18`, `circuits-22`. LCOE 266.589599–321.962095 dollars/MWh; gross building area 96,358.591–114,863.391 m². Reported ranges describe the named cases; coordinated cases change more than one input and are not isolated single-axis effects. No boundary claim. Facility failures: `circuits-22`: facility_routes_ok Full plant failures at these same locations are listed by qualified identity in §4.

#### `magnet__casing__interior_y` — feasible structure (search framing)

**Applies:** not applicable; sensitivity-framed.

#### `magnet__casing__interior_y` — observed response (sensitivity framing)

**Applies:** yes. Resolved levels: `{'magnet__casing__interior_y': [0.4, 0.65]}`. Cases: `selected18-legacy`, `selected18-layout`, `selected18-fixed-space`. LCOE 310.632663–314.333483 dollars/MWh; gross building area 102,194.160–104,152.731 m². Retained context changes several plasma/magnet/circuit inputs together; this is not an isolated response to this axis. No boundary claim. Facility failures: `selected18-fixed-space`: facility_capacity_ok Full plant failures at these same locations are listed by qualified identity in §4.

#### `magnet__coil__I_coil` — feasible structure (search framing)

**Applies:** not applicable; sensitivity-framed.

#### `magnet__coil__I_coil` — observed response (sensitivity framing)

**Applies:** yes. Resolved levels: `{'magnet__coil__I_coil': [12217184.408047015, 15400000.0]}`. Cases: `selected18-legacy`, `selected18-layout`, `selected18-fixed-space`. LCOE 310.632663–314.333483 dollars/MWh; gross building area 102,194.160–104,152.731 m². Retained context changes several plasma/magnet/circuit inputs together; this is not an isolated response to this axis. No boundary claim. Facility failures: `selected18-fixed-space`: facility_capacity_ok Full plant failures at these same locations are listed by qualified identity in §4.

#### `magnet__coil__coil_t` — feasible structure (search framing)

**Applies:** not applicable; sensitivity-framed.

#### `magnet__coil__coil_t` — observed response (sensitivity framing)

**Applies:** yes. Resolved levels: `{'magnet__coil__coil_t': [0.3, 0.65]}`. Cases: `selected18-legacy`, `selected18-layout`, `selected18-fixed-space`. LCOE 310.632663–314.333483 dollars/MWh; gross building area 102,194.160–104,152.731 m². Retained context changes several plasma/magnet/circuit inputs together; this is not an isolated response to this axis. No boundary claim. Facility failures: `selected18-fixed-space`: facility_capacity_ok Full plant failures at these same locations are listed by qualified identity in §4.

#### `magnet__winding_pack__inventory_multiplier` — feasible structure (search framing)

**Applies:** not applicable; sensitivity-framed.

#### `magnet__winding_pack__inventory_multiplier` — observed response (sensitivity framing)

**Applies:** yes. Resolved levels: `{'magnet__winding_pack__inventory_multiplier': [1.0, 1.01]}`. Cases: `selected18-legacy`, `selected18-layout`, `selected18-fixed-space`. LCOE 310.632663–314.333483 dollars/MWh; gross building area 102,194.160–104,152.731 m². Retained context changes several plasma/magnet/circuit inputs together; this is not an isolated response to this axis. No boundary claim. Facility failures: `selected18-fixed-space`: facility_capacity_ok Full plant failures at these same locations are listed by qualified identity in §4.

#### `magnet__winding_pack__sizing_mode` — feasible structure (search framing)

**Applies:** not applicable; sensitivity-framed.

#### `magnet__winding_pack__sizing_mode` — observed response (sensitivity framing)

**Applies:** yes. Resolved levels: `{'magnet__winding_pack__sizing_mode': [0.0, 1.0]}`. Cases: `selected18-legacy`, `selected18-layout`, `selected18-fixed-space`. LCOE 310.632663–314.333483 dollars/MWh; gross building area 102,194.160–104,152.731 m². Retained context changes several plasma/magnet/circuit inputs together; this is not an isolated response to this axis. No boundary claim. Facility failures: `selected18-fixed-space`: facility_capacity_ok Full plant failures at these same locations are listed by qualified identity in §4.

#### `plasma__R` — feasible structure (search framing)

**Applies:** not applicable; sensitivity-framed.

#### `plasma__R` — observed response (sensitivity framing)

**Applies:** yes. Resolved levels: `{'plasma__R': [11.251748216682868, 12.065, 12.7, 13.334999999999999]}`. Cases: `R-12.065`, `R-13.334999999999999`. LCOE 277.660879–281.427547 dollars/MWh; gross building area 97,010.209–103,153.611 m². Reported ranges describe the named cases; coordinated cases change more than one input and are not isolated single-axis effects. No boundary claim. Facility failures: No facility predicate fails in these named cases. Full plant failures at these same locations are listed by qualified identity in §4.

#### `plasma__T_i0` — feasible structure (search framing)

**Applies:** not applicable; sensitivity-framed.

#### `plasma__T_i0` — observed response (sensitivity framing)

**Applies:** yes. Resolved levels: `{'plasma__T_i0': [14.035595515748351, 14.63]}`. Cases: `selected18-legacy`, `selected18-layout`, `selected18-fixed-space`. LCOE 310.632663–314.333483 dollars/MWh; gross building area 102,194.160–104,152.731 m². Retained context changes several plasma/magnet/circuit inputs together; this is not an isolated response to this axis. No boundary claim. Facility failures: `selected18-fixed-space`: facility_capacity_ok Full plant failures at these same locations are listed by qualified identity in §4.

#### `plasma__a` — feasible structure (search framing)

**Applies:** not applicable; sensitivity-framed.

#### `plasma__a` — observed response (sensitivity framing)

**Applies:** yes. Resolved levels: `{'plasma__a': [1.2349999999999999, 1.3, 1.3650000000000002, 1.4908855301929713]}`. Cases: `a-1.2349999999999999`, `a-1.3650000000000002`. LCOE 257.313911–295.342338 dollars/MWh; gross building area 97,554.028–100,123.871 m². Reported ranges describe the named cases; coordinated cases change more than one input and are not isolated single-axis effects. No boundary claim. Facility failures: No facility predicate fails in these named cases. Full plant failures at these same locations are listed by qualified identity in §4.

#### `plasma__alpha_T` — feasible structure (search framing)

**Applies:** not applicable; sensitivity-framed.

#### `plasma__alpha_T` — observed response (sensitivity framing)

**Applies:** yes. Resolved levels: `{'plasma__alpha_T': [1.19, 1.2]}`. Cases: `selected18-legacy`, `selected18-layout`, `selected18-fixed-space`. LCOE 310.632663–314.333483 dollars/MWh; gross building area 102,194.160–104,152.731 m². Retained context changes several plasma/magnet/circuit inputs together; this is not an isolated response to this axis. No boundary claim. Facility failures: `selected18-fixed-space`: facility_capacity_ok Full plant failures at these same locations are listed by qualified identity in §4.

#### `plasma__alpha_n` — feasible structure (search framing)

**Applies:** not applicable; sensitivity-framed.

#### `plasma__alpha_n` — observed response (sensitivity framing)

**Applies:** yes. Resolved levels: `{'plasma__alpha_n': [0.33, 0.35]}`. Cases: `selected18-legacy`, `selected18-layout`, `selected18-fixed-space`. LCOE 310.632663–314.333483 dollars/MWh; gross building area 102,194.160–104,152.731 m². Retained context changes several plasma/magnet/circuit inputs together; this is not an isolated response to this axis. No boundary claim. Facility failures: `selected18-fixed-space`: facility_capacity_ok Full plant failures at these same locations are listed by qualified identity in §4.

#### `plasma__n_e0` — feasible structure (search framing)

**Applies:** not applicable; sensitivity-framed.

#### `plasma__n_e0` — observed response (sensitivity framing)

**Applies:** yes. Resolved levels: `{'plasma__n_e0': [4.8924678194274265e+20, 5.06e+20]}`. Cases: `selected18-legacy`, `selected18-layout`, `selected18-fixed-space`. LCOE 310.632663–314.333483 dollars/MWh; gross building area 102,194.160–104,152.731 m². Retained context changes several plasma/magnet/circuit inputs together; this is not an isolated response to this axis. No boundary claim. Facility failures: `selected18-fixed-space`: facility_capacity_ok Full plant failures at these same locations are listed by qualified identity in §4.

#### `buildings__cooling_field_cycle_days` — feasible structure (search framing)

**Applies:** not applicable; sensitivity-framed.

#### `buildings__cooling_field_cycle_days` — observed response (sensitivity framing)

**Applies:** yes. Resolved levels: `{'buildings__cooling_field_cycle_days': [0.2, 1.0]}`. Cases: `slow_initial_delivery`. LCOE 273.454649–273.454649 dollars/MWh; gross building area 100,059.551–100,059.551 m². Reported ranges describe the named cases; coordinated cases change more than one input and are not isolated single-axis effects. No boundary claim. Facility failures: `slow_initial_delivery`: facility_initial_ready Full plant failures at these same locations are listed by qualified identity in §4.

#### `buildings__helium_package_width` — feasible structure (search framing)

**Applies:** not applicable; sensitivity-framed.

#### `buildings__helium_package_width` — observed response (sensitivity framing)

**Applies:** yes. Resolved levels: `{'buildings__helium_package_width': [3.0, 8.0]}`. Cases: `wide_helium`. LCOE 273.964664–273.964664 dollars/MWh; gross building area 113,912.831–113,912.831 m². Reported ranges describe the named cases; coordinated cases change more than one input and are not isolated single-axis effects. No boundary claim. Facility failures: `wide_helium`: facility_routes_ok Full plant failures at these same locations are listed by qualified identity in §4.

#### `buildings__salt_package_length` — feasible structure (search framing)

**Applies:** not applicable; sensitivity-framed.

#### `buildings__salt_package_length` — observed response (sensitivity framing)

**Applies:** yes. Resolved levels: `{'buildings__salt_package_length': [3.0, 10.0]}`. Cases: `long_salt`. LCOE 273.970492–273.970492 dollars/MWh; gross building area 109,470.351–109,470.351 m². Reported ranges describe the named cases; coordinated cases change more than one input and are not isolated single-axis effects. No boundary claim. Facility failures: `long_salt`: facility_routes_ok Full plant failures at these same locations are listed by qualified identity in §4.

## 7. Axis groups

| Axis | Complete public entry key | Provenance | Meaning |
|---|---|---|---|
| blanket__first_wall__fluence_limit | stellarator_09__stellaris__blanket__first_wall__fluence_limit | fan_out | AGENT sensitivity proposal; complete single authored public entry and native fan-out. Coordinated task/rebar scenarios are design scenarios, not physical identity ties. Retained selected18 context is comparison context, not independently searched. |
| buildings__civil_rate_multiplier | stellarator_09__stellaris__buildings__civil_rate_multiplier | fan_out | AGENT sensitivity proposal; complete single authored public entry and native fan-out. Coordinated task/rebar scenarios are design scenarios, not physical identity ties. Retained selected18 context is comparison context, not independently searched. |
| buildings__component_hold_days | stellarator_09__stellaris__buildings__component_hold_days | fan_out | AGENT sensitivity proposal; complete single authored public entry and native fan-out. Coordinated task/rebar scenarios are design scenarios, not physical identity ties. Retained selected18 context is comparison context, not independently searched. |
| buildings__component_install_days | stellarator_09__stellaris__buildings__component_install_days | fan_out | AGENT sensitivity proposal; complete single authored public entry and native fan-out. Coordinated task/rebar scenarios are design scenarios, not physical identity ties. Retained selected18 context is comparison context, not independently searched. |
| buildings__component_material_fraction | stellarator_09__stellaris__buildings__component_material_fraction | fan_out | AGENT sensitivity proposal; complete single authored public entry and native fan-out. Coordinated task/rebar scenarios are design scenarios, not physical identity ties. Retained selected18 context is comparison context, not independently searched. |
| buildings__component_receipt_lead_days | stellarator_09__stellaris__buildings__component_receipt_lead_days | fan_out | AGENT sensitivity proposal; complete single authored public entry and native fan-out. Coordinated task/rebar scenarios are design scenarios, not physical identity ties. Retained selected18 context is comparison context, not independently searched. |
| buildings__component_remove_days | stellarator_09__stellaris__buildings__component_remove_days | fan_out | AGENT sensitivity proposal; complete single authored public entry and native fan-out. Coordinated task/rebar scenarios are design scenarios, not physical identity ties. Retained selected18 context is comparison context, not independently searched. |
| buildings__conventional_rebar_density | stellarator_09__stellaris__buildings__conventional_rebar_density | fan_out | AGENT sensitivity proposal; complete single authored public entry and native fan-out. Coordinated task/rebar scenarios are design scenarios, not physical identity ties. Retained selected18 context is comparison context, not independently searched. |
| buildings__conventional_wall | stellarator_09__stellaris__buildings__conventional_wall | fan_out | AGENT sensitivity proposal; complete single authored public entry and native fan-out. Coordinated task/rebar scenarios are design scenarios, not physical identity ties. Retained selected18 context is comparison context, not independently searched. |
| buildings__cooling_aisle_width | stellarator_09__stellaris__buildings__cooling_aisle_width | fan_out | AGENT sensitivity proposal; complete single authored public entry and native fan-out. Coordinated task/rebar scenarios are design scenarios, not physical identity ties. Retained selected18 context is comparison context, not independently searched. |
| buildings__cooling_bundle_process_days | stellarator_09__stellaris__buildings__cooling_bundle_process_days | fan_out | AGENT sensitivity proposal; complete single authored public entry and native fan-out. Coordinated task/rebar scenarios are design scenarios, not physical identity ties. Retained selected18 context is comparison context, not independently searched. |
| buildings__cooling_cross_width | stellarator_09__stellaris__buildings__cooling_cross_width | fan_out | AGENT sensitivity proposal; complete single authored public entry and native fan-out. Coordinated task/rebar scenarios are design scenarios, not physical identity ties. Retained selected18 context is comparison context, not independently searched. |
| buildings__cooling_hold_days | stellarator_09__stellaris__buildings__cooling_hold_days | fan_out | AGENT sensitivity proposal; complete single authored public entry and native fan-out. Coordinated task/rebar scenarios are design scenarios, not physical identity ties. Retained selected18 context is comparison context, not independently searched. |
| buildings__cooling_initial_receipt_lead_days | stellarator_09__stellaris__buildings__cooling_initial_receipt_lead_days | fan_out | AGENT sensitivity proposal; complete single authored public entry and native fan-out. Coordinated task/rebar scenarios are design scenarios, not physical identity ties. Retained selected18 context is comparison context, not independently searched. |
| buildings__cooling_machine_process_days | stellarator_09__stellaris__buildings__cooling_machine_process_days | fan_out | AGENT sensitivity proposal; complete single authored public entry and native fan-out. Coordinated task/rebar scenarios are design scenarios, not physical identity ties. Retained selected18 context is comparison context, not independently searched. |
| buildings__cooling_machine_stations | stellarator_09__stellaris__buildings__cooling_machine_stations | fan_out | AGENT sensitivity proposal; complete single authored public entry and native fan-out. Coordinated task/rebar scenarios are design scenarios, not physical identity ties. Retained selected18 context is comparison context, not independently searched. |
| buildings__cooling_receipt_lead_days | stellarator_09__stellaris__buildings__cooling_receipt_lead_days | fan_out | AGENT sensitivity proposal; complete single authored public entry and native fan-out. Coordinated task/rebar scenarios are design scenarios, not physical identity ties. Retained selected18 context is comparison context, not independently searched. |
| buildings__facilities_capacity_mode | stellarator_09__stellaris__buildings__facilities_capacity_mode | fan_out | AGENT sensitivity proposal; complete single authored public entry and native fan-out. Coordinated task/rebar scenarios are design scenarios, not physical identity ties. Retained selected18 context is comparison context, not independently searched. |
| buildings__facilities_cost_mode | stellarator_09__stellaris__buildings__facilities_cost_mode | fan_out | AGENT sensitivity proposal; complete single authored public entry and native fan-out. Coordinated task/rebar scenarios are design scenarios, not physical identity ties. Retained selected18 context is comparison context, not independently searched. |
| buildings__initial_receipt_lead_days | stellarator_09__stellaris__buildings__initial_receipt_lead_days | fan_out | AGENT sensitivity proposal; complete single authored public entry and native fan-out. Coordinated task/rebar scenarios are design scenarios, not physical identity ties. Retained selected18 context is comparison context, not independently searched. |
| buildings__nuclear_rebar_density | stellarator_09__stellaris__buildings__nuclear_rebar_density | fan_out | AGENT sensitivity proposal; complete single authored public entry and native fan-out. Coordinated task/rebar scenarios are design scenarios, not physical identity ties. Retained selected18 context is comparison context, not independently searched. |
| buildings__nuclear_wall | stellarator_09__stellaris__buildings__nuclear_wall | fan_out | AGENT sensitivity proposal; complete single authored public entry and native fan-out. Coordinated task/rebar scenarios are design scenarios, not physical identity ties. Retained selected18 context is comparison context, not independently searched. |
| buildings__provisional_envelope_scale | stellarator_09__stellaris__buildings__provisional_envelope_scale | fan_out | AGENT sensitivity proposal; complete single authored public entry and native fan-out. Coordinated task/rebar scenarios are design scenarios, not physical identity ties. Retained selected18 context is comparison context, not independently searched. |
| buildings__sector_service_teams | stellarator_09__stellaris__buildings__sector_service_teams | fan_out | AGENT sensitivity proposal; complete single authored public entry and native fan-out. Coordinated task/rebar scenarios are design scenarios, not physical identity ties. Retained selected18 context is comparison context, not independently searched. |
| buildings__tonne_interpretation_kg | stellarator_09__stellaris__buildings__tonne_interpretation_kg | fan_out | AGENT sensitivity proposal; complete single authored public entry and native fan-out. Coordinated task/rebar scenarios are design scenarios, not physical identity ties. Retained selected18 context is comparison context, not independently searched. |
| heat_transport__equipment_bundle_life | stellarator_09__stellaris__heat_transport__equipment_bundle_life | fan_out | AGENT sensitivity proposal; complete single authored public entry and native fan-out. Coordinated task/rebar scenarios are design scenarios, not physical identity ties. Retained selected18 context is comparison context, not independently searched. |
| heat_transport__equipment_machine_life | stellarator_09__stellaris__heat_transport__equipment_machine_life | fan_out | AGENT sensitivity proposal; complete single authored public entry and native fan-out. Coordinated task/rebar scenarios are design scenarios, not physical identity ties. Retained selected18 context is comparison context, not independently searched. |
| heat_transport__n_loops | stellarator_09__stellaris__heat_transport__n_loops | fan_out | AGENT sensitivity proposal; complete single authored public entry and native fan-out. Coordinated task/rebar scenarios are design scenarios, not physical identity ties. Retained selected18 context is comparison context, not independently searched. |
| magnet__casing__interior_y | stellarator_09__stellaris__magnet__casing__interior_y | fan_out | AGENT sensitivity proposal; complete single authored public entry and native fan-out. Coordinated task/rebar scenarios are design scenarios, not physical identity ties. Retained selected18 context is comparison context, not independently searched. |
| magnet__coil__I_coil | stellarator_09__stellaris__magnet__coil__I_coil | fan_out | AGENT sensitivity proposal; complete single authored public entry and native fan-out. Coordinated task/rebar scenarios are design scenarios, not physical identity ties. Retained selected18 context is comparison context, not independently searched. |
| magnet__coil__coil_t | stellarator_09__stellaris__magnet__coil__coil_t | fan_out | AGENT sensitivity proposal; complete single authored public entry and native fan-out. Coordinated task/rebar scenarios are design scenarios, not physical identity ties. Retained selected18 context is comparison context, not independently searched. |
| magnet__winding_pack__inventory_multiplier | stellarator_09__stellaris__magnet__winding_pack__inventory_multiplier | fan_out | AGENT sensitivity proposal; complete single authored public entry and native fan-out. Coordinated task/rebar scenarios are design scenarios, not physical identity ties. Retained selected18 context is comparison context, not independently searched. |
| magnet__winding_pack__sizing_mode | stellarator_09__stellaris__magnet__winding_pack__sizing_mode | fan_out | AGENT sensitivity proposal; complete single authored public entry and native fan-out. Coordinated task/rebar scenarios are design scenarios, not physical identity ties. Retained selected18 context is comparison context, not independently searched. |
| plasma__R | stellarator_09__stellaris__plasma__R | fan_out | AGENT sensitivity proposal; complete single authored public entry and native fan-out. Coordinated task/rebar scenarios are design scenarios, not physical identity ties. Retained selected18 context is comparison context, not independently searched. |
| plasma__T_i0 | stellarator_09__stellaris__plasma__T_i0 | fan_out | AGENT sensitivity proposal; complete single authored public entry and native fan-out. Coordinated task/rebar scenarios are design scenarios, not physical identity ties. Retained selected18 context is comparison context, not independently searched. |
| plasma__a | stellarator_09__stellaris__plasma__a | fan_out | AGENT sensitivity proposal; complete single authored public entry and native fan-out. Coordinated task/rebar scenarios are design scenarios, not physical identity ties. Retained selected18 context is comparison context, not independently searched. |
| plasma__alpha_T | stellarator_09__stellaris__plasma__alpha_T | fan_out | AGENT sensitivity proposal; complete single authored public entry and native fan-out. Coordinated task/rebar scenarios are design scenarios, not physical identity ties. Retained selected18 context is comparison context, not independently searched. |
| plasma__alpha_n | stellarator_09__stellaris__plasma__alpha_n | fan_out | AGENT sensitivity proposal; complete single authored public entry and native fan-out. Coordinated task/rebar scenarios are design scenarios, not physical identity ties. Retained selected18 context is comparison context, not independently searched. |
| plasma__n_e0 | stellarator_09__stellaris__plasma__n_e0 | fan_out | AGENT sensitivity proposal; complete single authored public entry and native fan-out. Coordinated task/rebar scenarios are design scenarios, not physical identity ties. Retained selected18 context is comparison context, not independently searched. |
| buildings__cooling_field_cycle_days | stellarator_09__stellaris__buildings__cooling_field_cycle_days | fan_out | Reviewer counterexample; AGENT sensitivity, no optimization. |
| buildings__helium_package_width | stellarator_09__stellaris__buildings__helium_package_width | fan_out | Reviewer counterexample; AGENT sensitivity, no optimization. |
| buildings__salt_package_length | stellarator_09__stellaris__buildings__salt_package_length | fan_out | Reviewer counterexample; AGENT sensitivity, no optimization. |

Native model fan-out carries each complete authored public input. Coordinated task-duration and rebar cases do not assert identity between different physical quantities.

## 8. Indicators and rulings

| Axis | Indicator | Ruling | Interpretation |
|---|---|---|---|
| blanket__first_wall__fluence_limit | constraints_reachable | No sound-negative ruling condition | 5 possible predicate paths |
| buildings__civil_rate_multiplier | no_constraint_response | OWNER: sensitivity; “yes run both” | Missing procurement/price resistance; finding#1 |
| buildings__component_hold_days | constraints_reachable | No sound-negative ruling condition | 5 possible predicate paths |
| buildings__component_install_days | constraints_reachable | No sound-negative ruling condition | 5 possible predicate paths |
| buildings__component_material_fraction | constraints_reachable | No sound-negative ruling condition | 5 possible predicate paths |
| buildings__component_receipt_lead_days | constraints_reachable | No sound-negative ruling condition | 5 possible predicate paths |
| buildings__component_remove_days | constraints_reachable | No sound-negative ruling condition | 5 possible predicate paths |
| buildings__conventional_rebar_density | constraints_reachable | No sound-negative ruling condition | 5 possible predicate paths |
| buildings__conventional_wall | constraints_reachable | No sound-negative ruling condition | 5 possible predicate paths |
| buildings__cooling_aisle_width | constraints_reachable | No sound-negative ruling condition | 5 possible predicate paths |
| buildings__cooling_bundle_process_days | constraints_reachable | No sound-negative ruling condition | 5 possible predicate paths |
| buildings__cooling_cross_width | constraints_reachable | No sound-negative ruling condition | 5 possible predicate paths |
| buildings__cooling_field_cycle_days | constraints_reachable | No sound-negative ruling condition | 5 possible predicate paths |
| buildings__cooling_hold_days | constraints_reachable | No sound-negative ruling condition | 5 possible predicate paths |
| buildings__cooling_initial_receipt_lead_days | constraints_reachable | No sound-negative ruling condition | 5 possible predicate paths |
| buildings__cooling_machine_process_days | constraints_reachable | No sound-negative ruling condition | 5 possible predicate paths |
| buildings__cooling_machine_stations | constraints_reachable | No sound-negative ruling condition | 5 possible predicate paths |
| buildings__cooling_receipt_lead_days | constraints_reachable | No sound-negative ruling condition | 5 possible predicate paths |
| buildings__facilities_capacity_mode | constraints_reachable | No sound-negative ruling condition | 5 possible predicate paths |
| buildings__facilities_cost_mode | constraints_reachable | No sound-negative ruling condition | 5 possible predicate paths |
| buildings__helium_package_width | constraints_reachable | No sound-negative ruling condition | 5 possible predicate paths |
| buildings__initial_receipt_lead_days | constraints_reachable | No sound-negative ruling condition | 5 possible predicate paths |
| buildings__nuclear_rebar_density | constraints_reachable | No sound-negative ruling condition | 5 possible predicate paths |
| buildings__nuclear_wall | constraints_reachable | No sound-negative ruling condition | 5 possible predicate paths |
| buildings__provisional_envelope_scale | constraints_reachable | No sound-negative ruling condition | 5 possible predicate paths |
| buildings__salt_package_length | constraints_reachable | No sound-negative ruling condition | 5 possible predicate paths |
| buildings__sector_service_teams | constraints_reachable | No sound-negative ruling condition | 5 possible predicate paths |
| buildings__tonne_interpretation_kg | no_constraint_response | OWNER: sensitivity; “yes run both” | Source-unit ambiguity; finding#2 |
| heat_transport__equipment_bundle_life | constraints_reachable | No sound-negative ruling condition | 7 possible predicate paths |
| heat_transport__equipment_machine_life | constraints_reachable | No sound-negative ruling condition | 7 possible predicate paths |
| heat_transport__n_loops | constraints_reachable | No sound-negative ruling condition | 10 possible predicate paths |
| magnet__casing__interior_y | constraints_reachable | No sound-negative ruling condition | 1 possible predicate paths |
| magnet__coil__I_coil | constraints_reachable | No sound-negative ruling condition | 21 possible predicate paths |
| magnet__coil__coil_t | constraints_reachable | No sound-negative ruling condition | 13 possible predicate paths |
| magnet__winding_pack__inventory_multiplier | constraints_reachable | No sound-negative ruling condition | 11 possible predicate paths |
| magnet__winding_pack__sizing_mode | constraints_reachable | No sound-negative ruling condition | 11 possible predicate paths |
| plasma__R | constraints_reachable | No sound-negative ruling condition | 21 possible predicate paths |
| plasma__T_i0 | constraints_reachable | No sound-negative ruling condition | 16 possible predicate paths |
| plasma__a | constraints_reachable | No sound-negative ruling condition | 21 possible predicate paths |
| plasma__alpha_T | constraints_reachable | No sound-negative ruling condition | 16 possible predicate paths |
| plasma__alpha_n | constraints_reachable | No sound-negative ruling condition | 16 possible predicate paths |
| plasma__n_e0 | constraints_reachable | No sound-negative ruling condition | 16 possible predicate paths |

Indicators do not establish monotonicity, physical identity across different key names or intra-module operand dependency. `constraints_reachable` denotes a possible path, not observed resistance. `unresisted` is an agent judgment. The two sound-negative axes retain their model-development findings despite the owner ruling; no physical feasibility claim is made from their price response.

## 9. Preflight results

| Gate | Outcome | Detail |
|---|---|---|
| declared_keys | pass | 42 declared keys across 42 groups, all package inputs |
| sibling_scan | pass | pass |
| identity | pass | kind sealed, digest 21d2bda3596ab0df38356bac9e404680ca6a836099a89dc0a2e8f6f73edb9208 recomputed from 0 allowed-modified file(s) and 0 declared source(s); every other sealed artifact matches |
| manifest_currency | pass | both recorded package fingerprints match the package on disk |
| baseline_headline | pass | stellarator_09__stellaris__lcoe_calc__lcoe reproduces at relative deviation 0.000e+00; 25/25 pinned verdicts match |
| package_clean | pass | package tree is byte-untouched (git clean) |

The identity gate reads [package_identity.json](results/package_identity.json); the baseline gate reads [baseline_result.json](results/baseline_result.json). Before/after package cleanliness receipts and the full gate output are retained in results/. No gate outcome is inferred from successful execution alone.

## 10. Execution route and why

**Route:** study-local direct API, using stock PreparedListStrategy, StudyRunner, CandidateBridge and StudyStore through the captured package route. The purposeful coordinated list is not a Cartesian optimization grid. The pinned baseline, preflight and all retained cases exercised this route. Glue ledger: none; no external solve or harness physics supplies missing model equations. Facility ledgers are deterministic replay of the production helper from native-bound inputs, checked against native scalar outputs; they add inspectability, not independent validation.

## 11. Study definition and window provenance

The engineered list contains 48 purposeful cases. The first scan refused one supported fluence-limit override because its oracle entry mapping was absent; the bounded mapping repair changed no equations or production package. The original refusal and repair are retained in results/oracle-scan-attempt1.json and reviews/oracle-map-repair.md. The coordinator retained the independently scanned candidates in [proposals.json](preparation/proposals.json) and documented the decision in [window-selection.md](reviews/window-selection.md). Default14 and selected18 cost-only pairs separate accounting selection from physical design changes. Dedicated equipment, stock/resource, receipt, route and construction scenarios expose response and failures. Levels are assumptions selected to make those mechanisms visible, not valid engineering ranges; no feasible anchor or optimum is inherited from a historical study.

## 12. Cross-fingerprint correlation and what it means

Single released fingerprint; no cross-arm fingerprint correlation is required. Legacy/layout selectors run within that one package. Saved selected18 inputs define comparison context; historical outputs and verdicts are not inherited or rewritten. Source/cost uncertainty comparisons do not substitute for a changed plant design.

## 13. Verification

Independent verification reports pass: 40128 scalar comparisons and 1200 exact predicate comparisons across the retained cases. Scalar tolerance is relative 1e-9 and absolute 1e-9. The generic verifier result is preserved in [verification_summary.json](results/verification_summary.json), with its unedited log. All declared numeric channels are present; channels absent from the captured oracle map are native evidence only.

The original no-event outage-margin verification failure is retained with the before-no-event-repair suffix. The independently reviewed conditional repair aligns the inactive-check sentinel while retaining initial demand and hypothetical required/allowed outage diagnostics; it changed no production package and reused the same native cases. See reviews/no-event-verification-repair.md.

This checks implementation agreement, not independent physical validation of shared source data, assumptions, historical civil/ventilation transfer, load/shielding adequacy or the maintenance procedure. Production replay ledgers and plots are not an independent oracle. The captured Boolean-default serialization warnings do not alter the numeric equality or predicate evidence.

Matched control verification passed: default14: 380 entering comparisons, 662 exactly unchanged physical/layout channels and all 25 predicates identical; selected18: 380 entering comparisons, 662 exactly unchanged physical/layout channels and all 25 predicates identical. See [matched-control-checks.json](results/matched-control-checks.json). This verifies unchanged channels within each selector pair and reproduction of entering outputs; it does not qualify the unchanged physical assumptions.

## 14. Review outcomes

| Review | Evidence and disposition |
|---|---|
| Coordinator release | Accepted integration CANDIDATE and execution release are captured in preparation/. |
| Owner scientific ruling | Two no_constraint_response axes authorized as sensitivity; owner-ruling.md preserves the quote. |
| Independent implementation/source assurance | Captured integrated-audit.md, design-review.md and source-review.md preserve their actual scope and limits; this report does not add a new reviewer verdict. |
| Final study review / fresh R9.S grade | Independent non-author review: PASS, R9.S = 3 against the unchanged rubric. All seven findings and three proposed goal learnings accepted; see reviews/final-review.md. Frozen-artifact custody is checked separately after snapshot creation. |

## 15. Findings

| ID | Kind | Finding | Proposed disposition | Home |
|---|---|---|---|---|
| `20260918-layout-based-facilities#1` | model | Construction-price sensitivity has no modeled resistance | Owner authorized sensitivity only (yes run both); retain procurement/transfer uncertainty. No price optimum or physical admissibility claim. | work/active/WI-068_layout-based-facilities |
| `20260918-layout-based-facilities#2` | model | Source-tonne interpretation is unresolved by physical constraints | Owner authorized US-short-ton/metric-tonne sensitivity only; resolve the source-unit convention through source evidence, not cost optimization. | work/active/WI-068_layout-based-facilities |
| `20260918-layout-based-facilities#3` | model | Conceptual layout remains unqualified | Retain explicit qualification disclosures and provisional provenance; require actual upstream dimensions and engineering qualification before construction/maintenance claims. | work/orchestration/goals/layout-based-facilities |
| `20260918-layout-based-facilities#4` | model | Logistics failures persist under supported stress scenarios | Retain every failure and its named margin; no reduction in demanded maintenance and no silent calendar adjustment. These scenarios test assumptions, not a qualified feasibility boundary. | work/orchestration/goals/layout-based-facilities |
| `20260918-layout-based-facilities#5` | model | Priced facility scope is narrower than a complete installed facility | Report the actual scoped cost and overlaps avoided. Preserve the missing services/handling procurement scope as explicit work, not zero-cost equipment or a complete facility quotation. | work/active/WI-068_layout-based-facilities |
| `20260918-layout-based-facilities#6` | process | Supported fluence override was missing from the oracle entry map | Resolved by mapping repair 3fa479ed and 41 oracle tests; no equation or production-package change. The failed scan is retained and is not treated as final native evidence. | exploration/stellarator_e2e/studies/oracle_entry.py; tests/models/test_facilities_oracle.py |
| `20260918-layout-based-facilities#7` | process | Independent zero-event outage margin missed the inactive-check sentinel | Resolved by the reviewed oracle conditional repair and explicit contract clarification; 42 oracle tests pass and 842 default outputs remain unchanged. Failed verification is retained. The same 48 native cases were rescanned and reverified; no production model or package identity changed. | exploration/stellarator_e2e/oracle_facilities.py; work/active/WI-068_layout-based-facilities/evidence/facility-contract.md |

Executor findings were accepted by the independent reviewer and registered in the discovery log. [proposed-findings.json](proposed-findings.json) carries their evidence and full wording. The coordinator registered the findings; the report author did not edit external registers.

Before the first record commit, the native record-contract check found that the CSV export omitted its arm identifier. The coordinator added only `arm_id=arm-native`; all 48 rows retain their exact prior input, output and predicate fields. The original CSV and rejected uncommitted snapshot candidate are preserved in preparation/. See reviews/export-schema-repair.md. No native case or store changed.

## 16. Snapshot

- **File:** `snapshot.json`
- **sha256:** `af668e7ac5f57041787b6e5d5c08aa3ccf5bc2de006062e681daf9323e547455`
- **Schema version:** `1`

## 17. What this record does not contain

No licensed/site/seismic/shielding/loading qualification, validated radioactive-component procedure, complete handling machine design, vendor quotation, independently sized conventional equipment, cooling field-outage model, optimum is provided. Whole-plant screen results remain model results. Missing engineering qualification and priced scope are disclosed even where numerical predicates pass. The provisional support-equipment envelope scale was varied only from 0.8 to 1.2; this does not cover the broader 0.5/1/2 scenario suggested in the design. The independent review supports conceptual R9.S3 and does not qualify construction or operation.
