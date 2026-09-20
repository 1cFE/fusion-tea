# Independent numerical coverage repair

[NEED] The owner requires explicit verification/disposition of all comparison-relevant unmapped outputs. Fresh inventory is `scope-evidence/mapping.json`. All 22 influence accounting, geometry, sizing or engineering interpretation; none will be excused merely because baseline bytes reproduce.

[INFERRED] Extend the existing independent `exploration/stellarator_e2e/verify_stellaris.py` result dictionary and `studies/oracle_entry.py` map, without importing generated implementations or changing scientific calculations. Most required values are already independently computed local variables. Use unique output-map keys; one result may expose separate aliases for multiple native producers. Retain the historical oracle result names consumed by older tests. Remove the duplicate mapping of `fuel_handling` and `processing_cost` to one channel by retaining canonical `processing_cost`; assert the old result alias agrees with that value in regression coverage.

| Native missing channels | Independent expected value and claim |
|---|---|
| `cas70_calc__cas70`, `cas70_calc__annual_total` | Independently calculated annual O&M + replacements, then fuel. These feed cost/LCOE claims. |
| `cas71_calc__levelized`, `cas80_calc__levelized` | Existing independent growing-annuity calculation for O&M and fuel. |
| `cas71_calc__crf`, `cas80_calc__crf` | Existing independent financial capital-recovery factor. Separately test by summing discounted unit payments rather than importing native factors. |
| `heat_transport__cooling_guard__cost_mode`, `...__energy_mode` | Explicit validated binary design inputs; these are passthrough controls, not physical predictions. Verify invalid mode rejection independently. |
| `heat_transport__cooling_selection__consumables_annual`, `...__replacement_annual`, `...__shipping_exclusion` | Independently computed cooling cost mode times the corresponding equipment ledger amount. Verify inactive mode removes each effect and does not remove diagnostics. |
| `magnet__coil_length__c_coil`, `magnet__wp_sizing__wp_side`, `magnet__wp_volume__vol_cold_total` | Existing independent bore-based length, current/density pack side and summed winding/extra-cold volume. They affect material cost, current/fit and refrigeration. |
| `rb__blanket_vol`, `...__outer_radius`, `...__r_coil`, `...__shield_vol`, `...__structure_vol`, `...__vessel_vol`, `...__wall_area` | Existing independent toroidal annulus calculations and cumulative radii. They affect blanket/facility/material costs and engineering geometry. |
| `replacement_cost_per_event__replacement_cost_per_event` | Existing independent blanket-plus-divertor bundle cost times module count. It affects lifecycle cost. |

[INFERRED] Keep a coverage regression that requires every current native numeric channel to have one unique oracle-map producer and actually compares all mapped values at the entering baseline and justified bounded off-default inputs. Include distinct cost-only/energy modes, zero-discount financial boundary and permitted geometry change when the final physical interface supports them. A missing map must fail explicitly. Do not relax strict engineering predicates to accommodate scalar rounding. Exact conductor-boundary treatment is separately reviewed in regression diagnosis.

[INFERRED] No new source or scientific equation is proposed. Existing independently implemented formulas supply the expected values; their physical/source limitations persist. Final substantive review must verify the mapping against native producers and the independent calculation, not just the map count. Coordinator owns both oracle files; regression worker owns tests/route repairs after release.
