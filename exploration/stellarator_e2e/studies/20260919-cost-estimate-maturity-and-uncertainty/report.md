# Conditional estimate-uncertainty results

[AGENT] Executor analysis. The 36 source cases give headline LCOE **244.882–290.376 USD/MWh**, with nominal **271.584 USD/MWh**. This is a finite conditional source-interpretation/model-analogy envelope at one fixed design. It is not a confidence interval, a complete plant uncertainty range or the price of a feasible plant. The separate 36 contingency diagnostics and 2 downtime stresses are excluded from that headline envelope.

## Estimate and result scope

The audited candidate executable is `b032da4a3971979792bc024bf9cd1a41a2d83d340bad5b59ef3e1a9aeaa77236` with semantic fingerprint `ea1555ea133db8ed7ba1c638b29ddf540ba99d811bfcf7d9ef9454b626d3a28a` and integration pin `e48d5218b6e3be2775a94269a461dccd259fccc5fc41fed7c135dc1336bfe284`. Complete inputs, source qualifications, account amounts and evidence are retained under preparation/. The retained reference has 14 cooling circuits. All money is mixed-source-year; cooling uses an approximate annual-CPI purchasing-power conversion of January 2017 source prices. The historical r2 archive and other design identities are separate.

## Costs and electricity

| Quantity | Unit | Nominal | Source minimum | Source maximum | Nominal zero-contingency diagnostic |
|---|---|---:|---:|---:|---:|
| Direct before contingency | million USD | 12,219.310 | 10,840.822 | 13,189.028 | 12,219.310 |
| CAS29 contingency | million USD | 1,221.931 | 1,084.082 | 1,318.903 | 0.000 |
| Indirect | million USD | 3,584.331 | 3,179.974 | 3,868.782 | 3,258.483 |
| Supplementary | million USD | 834.314 | 784.446 | 869.456 | 781.625 |
| Overnight capital | billion USD | 17.918 | 15.948 | 19.304 | 16.318 |
| Construction interest diagnostic | billion USD | 5.061 | 4.505 | 5.453 | 4.609 |
| Comparison financed capital | billion USD | 22.980 | 20.452 | 24.757 | 20.927 |
| Headline annual capital | million USD/year | 1,892.738 | 1,684.583 | 2,039.174 | 1,723.677 |
| Routine O&M levelized | million USD/year | 79.360 | 79.360 | 79.360 | 79.360 |
| Cooling replacement equivalent | million USD/year | 55.674 | 50.779 | 59.169 | 55.674 |
| All replacement equivalent | million USD/year | 194.000 | 189.106 | 197.496 | 194.000 |
| Fuel expense levelized | million USD/year | 0.793 | 0.793 | 0.793 | 0.793 |
| Total noncapital expense | million USD/year | 274.153 | 269.259 | 277.649 | 274.153 |
| Annual electricity | MWh/year | 7,978,704.890 | 7,978,704.890 | 7,978,704.890 | 7,978,704.890 |
| Headline LCOE |  USD/MWh | 271.584 | 244.882 | 290.376 | 250.395 |
| Comparison LCOE |  USD/MWh | 266.459 | 240.320 | 284.854 | 245.728 |

The table gives each output’s own minimum/maximum over the 36 cases. It does not imply all extrema belong to the same scenario. results/points.csv contains the complete input combinations and exact outputs. Overnight capital includes direct contingency and its downstream charges; CAS60 is separately reported and is not added a second time in the headline financing formula.

## What changes the result

The common fabrication rate changes exchanger and both pipe supply bills, dependent installation/delivery exclusions and future bundle replacements together. Civil TN interpretation changes all affected reinforcement rates together; containment date changes both that row’s equipment and installation; sheet inclusion changes only the extra stock charge at fixed physical stock and winding effort. These are finite alternatives with no probability weights.

| Single driver, other source assumptions nominal | LCOE minimum | LCOE maximum | Span USD/MWh |
|---|---:|---:|---:|
| fabrication | 245.287 | 290.368 | 45.082 |
| tonne | 271.193 | 271.584 | 0.391 |
| containment | 271.580 | 271.592 | 0.012 |
| sheet | 271.575 | 271.584 | 0.009 |

The source cases use fabrication rates of 240, 310 and 360 USD (2017)/kg; TN conversions of 907.18474 and 1,000 kg; containment CPI values of 65.2, 82.4 and 96.5; and sheet rates of 0 and 61.67720668774671 USD/m². The minimum headline case combines 240, 1,000, 96.5 and 0 respectively; the maximum combines 360, 907.18474, 65.2 and 61.67720668774671. Exact unrounded single-driver spans are retained in results/attribution.json.

This attribution describes the selected finite cases only. Exposure to a common source does not measure the fraction of total uncertainty captured. No continuous interval extrema are claimed; replacing discrete source cases with arbitrary intermediate models requires an additional argument.

## Contingency diagnostic

At nominal source assumptions, native removal of direct contingency changes overnight capital from 17.918 to 16.318 billion USD and LCOE from 271.584 to 250.395 USD/MWh. All dependent indirect, freight, tax/insurance and finance terms are recomputed. It is not equivalent to subtracting CAS29 from final capital. Supplementary contingency remains 0. This diagnostic does not recommend changing the retained 10% policy or imply that its allowance covers every omitted risk. No further uncertainty uplift is added.

Across all 36 matched source pairs, removing direct contingency reduces overnight capital by 1.420–1.728 billion USD and headline LCOE by 18.797–22.872 USD/MWh. Annual noncapital expense and electricity are unchanged within every matched pair.

## Separate electricity-denominator stresses

| Unplanned downtime input | Availability | Annual electricity MWh | Annual noncapital expense USD | LCOE USD/MWh |
|---:|---:|---:|---:|---:|
| 0 | 0.902777778 | 7,978,704.890 | 274,152,877.125 | 271.584 |
| 0.05 | 0.857638889 | 7,579,769.646 | 269,020,624.677 | 285.201 |
| 0.1 | 0.812500000 | 7,180,834.401 | 263,608,207.892 | 300.292 |

These 0.05/0.10 inputs are engineered downtime stresses, not evidence-supported reliability bounds. The live calendar propagates annual electricity and expense effects; running fuel-processing capacity remains distinct from annual processed mass. None belongs in the source envelope.

## Engineering failures and verification

All 74 proposals are retained. Whole-plant passing count is 0. Predicate failure counts are `{'divertor_heat_ok': 74, 'reference_conductor_current_ok': 74, 'tbr_ok': 74, 'wp_fit_ok': 74}`. The salt-pump equation-range screen is satisfied in this 14-circuit case, while the salt/conversion temperature-interface screen remains unsatisfied; motor/manufacturing qualification remains unresolved. Both numerical screens are retained in results/summary.json; authored predicates do not cover every qualification gap.

Independent-software checks pass 69116 mapped scalar comparisons and 1850 predicate comparisons. Account/dependency checks pass 2887 checks; exact shared-output comparison reproduces the retained WI-070 nominal. Generic verification passes. There are 22 native numeric channels outside the oracle map; preparation/coverage.json names them. Shared source assumptions and transport data are not independently validated by numerical agreement. Static-validation and integration read-set limitations remain in the retained audit/integration evidence.

The original failures persist: peak divertor target heat exceeds its limit; the breeding lower-bound estimate falls below required TBR despite its higher mean; reference conductor operating current exceeds the permitted margin; and the required winding pack does not fit the casing cavity. Exact authored operators and source identities are retained in results/predicate-catalog.json, with operand outputs in results/all-native-channels.csv.

## Maturity and unquantified remainder

The reviewed generic AACE 17R-97 Class 5 judgment is provisional conceptual project maturity, using the historical matrix reproduced by DOE with its edition stated. Account detail varies: cooling/facilities have explicit but unqualified quantities; magnets/fuel have incomplete manufacturing/process coverage; other systems and project services retain factors. Software detail is not an engineering-completion percentage. No class-derived accuracy band is applied.

The source cases leave target fabrication transfer, pressure-qualified geometry, routing, procurement, magnet tape/winding/support uncertainty, civil productivity, conventional equipment, project execution, routine O&M, component reliability and unavailable equipment costs unbounded. Missing equipment is retained as unpriced or coverage unresolved in preparation/references/uncertainty-register.md, with evidence/action and domain roles. It is not modeled as a zero-cost random variable. This study does not independently certify R12.S.
