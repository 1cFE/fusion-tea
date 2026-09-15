# Magnet coil realism — completed technical answer

All three intended model corrections are implemented. Winding procurement follows the coil bore, refrigeration includes explicit lead/radiation/support loads at two temperature stages, and the steel account prices a total support-mass fit. The final native study confirms the effects. The cheapest sampled fully feasible geometry remains **R = 12.7 m, a = 1.7 m**, with a higher price.

## Design point

| Quantity | Entering Round 3 package | Final package |
|---|---:|---:|
| LCOE, $/MWh | 142.51 | 146.31 |
| Refrigeration electricity, MW | 0.864 | 2.138 |
| Magnet support cost, $M | 54.4 | 209.1 |
| Total magnet capital, $M | 1,624.8 | 1,779.5 |

The final design point still satisfies **17 of 18 predicates**. Its inherited divertor-heat violation remains. Cold refrigeration uses 1.535 MW and intercept refrigeration uses 0.602 MW. Separate direct lead/joint electricity adds 0.0503 MW. Refrigeration accounts for **0.619%** of the plant's recirculating electricity.

The total-support fit gives 11,615.6 tonnes at the unchanged 111 GJ anchor. The inherited 48 × 63 tonne casing convention remains a diagnostic; it is not added to the total.

## Sampled machine and larger bore

Among nominal samples satisfying all eighteen predicates, the cheapest machine remains R = 12.7 m, a = 1.7 m, with aspect ratio 7.47. Its price is **$135.51/MWh at 100 MW installed heating** and **$141.76/MWh at 220 MW**. Refrigeration uses 2.125 MW, or **0.797%** of recirculating electricity, at both points.

The unrestricted price minima on the cheap minor-radius columns sit at a = 2.1 m and fail existing predicates. Assumption-altered cases are excluded from the nominal geometry minima.

At fixed design major radius and current, increasing plasma minor radius from 1.3 to 2.2 m increases winding procurement by 28.57%, from $1,570.4M to $2,019.0M. Total magnet capital rises from $1,779.5M to $2,328.5M. The final inventory/structure increment causes **zero verdict flips across the 159 matched entering-Round-1 arm rows**. All 108 older magnet-transfer coordinates are also compared by source case ID as historical references; their five all-predicate passes retain the extrapolated conductor-envelope limitation.

## Engineering choices and limits

[AGENT] Source-backed equations use declared device assumptions: twelve terminal leads at 50 kA, a 77 K intercept, conceptual cryostat surfaces and support paths, 316 conductivity as a 316LN proxy, and 20%-of-Carnot refrigeration. Fixed conductivity means support a cold-temperature approximation of 10–30 K around the nominal 20 K case.

The inherited fabricated-steel estimate is $18/kg all-in, tested at $9/$36 per kg. The old primary-structure amount becomes an explicitly chosen nonmagnet budget; its zero alternative is shown. The separate 15 MW cooling slot remains a provisional noncryogenic allowance, also tested at zero. Neither allowance has a sourced equipment partition.

Nominal structure nuclear heating is zero. The 35.5 W/m³ sensitivity uses winding deposition as a proxy; it is not a qualified steel rate or upper bound. Detailed cryostat geometry, local support stress/fit, configuration-specific geometry, absolute conductor margin and winding effort versus cross-section remain unqualified. The eighteen predicates do not certify those missing capabilities.

## Demo paragraph

The magnet now follows the coil the model builds: winding length scales with bore, refrigeration includes leads, radiation and support conduction at 20 K and 77 K, and structural cost uses the source's total-support mass shape. At the design point this gives $146.31/MWh and 2.14 MW of refrigeration, 0.62% of recirculating power; the existing divertor limit still fails. The cheapest sampled machine satisfying all 18 limits remains R = 12.7 m, a = 1.7 m, at $135.51/MWh with 100 MW installed heating. Its refrigeration uses 0.80% of recirculating power. These results use declared thermal geometry, refrigeration and steel-price assumptions; detailed cryostat/support qualification and structure nuclear deposition remain outside the demonstrated claim.

## Evidence

- [WI-059 acceptance plan](../../../active/WI-059_coil-thermal-and-total-support-inventory/plan.md), SV-105/SV-106 and [native integration candidate](evidence/T-007_integration-r2/integration_return.json).
- [Final study record](../../../../exploration/stellarator_e2e/studies/20260915-coil-inventory/record.md), [analysis](../../../../exploration/stellarator_e2e/studies/20260915-coil-inventory/results/analysis.json) and [all-point verification](../../../../exploration/stellarator_e2e/studies/20260915-coil-inventory/results/oracle-all-points.json).
- Attributed changes use the immediately entering package. Older-package comparisons remain references under the owner's approved amendment.
