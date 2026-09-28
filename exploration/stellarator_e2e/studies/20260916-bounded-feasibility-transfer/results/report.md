# Bounded physical-screen result

All 71 selected native cases completed. None passes all twenty predicates. 10 cases have invalid divertor power accounts and remain in the evidence.

The coordinator-selected closest sampled rejection is shown below. Selection uses normalized authored margins, not physical distance to feasibility. This point is a local tradeoff, not an optimum.

| Quantity | Native value |
|---|---|
| R_m | 11.8765625 |
| a_m | 1.426953125 |
| current_MAturn | 13.963453125 |
| radial_exterior_m | 0.58 |
| transverse_cavity_m | 0.6 |
| loops | 16 |
| LCOE_dollars_MWh | 150.158357858 |
| total_capital_dollars | 10441741422.4 |
| Signed burn_hold_ok margin | 11.7064092373 |
| Signed sustainment_ok margin | 38.2935907627 |
| Signed peak_field_ok margin | -0.587340411267 |
| Signed wp_fit_ok margin | 0.0162811271656 |
| Signed divertor_heat_ok margin | -0.201678792381 |
| Signed loop_capacity_ok margin | 31.6076992931 |
| Signed wall_load_ok margin | -0.0112851272355 |

Signed margins use the authored operands and units. Negative field/divertor/wall margins are simultaneous deficits; passing burn, sustainment, fit and loop margins do not erase them.

| Transfer anchor | R m | a m | MA-turn | Failed predicates |
|---|---|---|---|---|
| control-allocated-current-sized-reference | 12.7 | 1.3 | 15.4 | divertor_heat_ok, peak_field_ok |
| transfer-smaller | 12.3 | 1.25906 | 14.915 | divertor_heat_ok, peak_field_ok, sustainment_ok |
| transfer-larger | 13.1 | 1.34094 | 15.885 | divertor_heat_ok, peak_field_ok |

Single-input transfer contrasts, every individual predicate, all equipment duties/counts and conditional costs are in case-summary.csv. Full native outputs are in native-cases.json. The sixteen oracle-unmapped channels are enumerated in oracle-all-points.json.

All 16046 mapped scalar and 1420 predicate comparisons pass. Generic verification additionally samples all observed verdict combinations.

Six exact matched-loop pairs are recorded in analysis.json under matched_loop_headroom. Their headroom is an annual omitted-cost budget, not installed capital or a net saving. Conditional 2N circulators/N IHXs carry duties but no qualification or added-equipment quote.

The engineered finite search establishes neither global infeasibility nor predictive accuracy. No feasible neighborhood was found. Held transport/material/source-profile assumptions and unsupported geometry/cost dependencies remain in record.md and protocol.md.
