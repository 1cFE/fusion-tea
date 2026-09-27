# Verified matched conversion comparison

[AGENT] Reporting analysis of the retained native record. Stock verification passes all 498 unchanged input maps, with 872 scalar channels and 84 independently rederived predicates per case. 83 cases satisfy all implemented checks. This report reads stored results and runs no model or oracle.

The comparison is the selected steam offer versus tested Brayton offers at matched source conditions. Steam’s fixed 14-circuit connector and least-cost passing connector are shown separately. The original selected anchors remain cost minima in their exact finite passing catalogs. The comparison does not establish equally optimized technologies or whole-plant LCOE.

| Source MW | Steam circuits × pumps / pump kg/s | Steam net MW | Brayton net MW | Fixed steam USD/net MWh | Selected steam | Tested Brayton | Steam minus Brayton |
| ---: | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| 2500 | 10 × 4 / 225 | 937.579 | 559.493 | 45.309 | 33.762 | 33.768 | -0.006 |
| 2800 | 11 × 4 / 225 | 1060.283 | 518.099 | 40.065 | 32.406 | 36.466 | -4.060 |
| 3000 | 14 × 3 / 250 | 1144.003 | 682.834 | 37.133 | 37.114 | 27.669 | +9.446 |

Steam produces 378.086, 542.184 and 461.168 MW more net electricity in the three selected comparisons. Its cost differences at 2500 and 2800 MW are below the 5 USD2025/net MWh materiality threshold. At 3000 MW the nominal tested Brayton offer is cheaper by 9.446 USD/net MWh; quote scenarios reverse that sign. These conclusions apply to this selected steam offer and the tested passing catalogs.

Power materiality is 5 MW; cost materiality is 5 USD2025 per net MWh. Price scenarios and component efficiencies are conditional assumptions. The lines connect selected discrete offers, not a continuous optimum or a reactor turndown trajectory.

## Accounting

| Source MW | Branch | Gross MW | Electric loads MW | Net MW | Rejected MW | Capital BUSD | Service PV BUSD | Replacement PV BUSD | Discounted energy million MWh |
| ---: | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 2500 | steam | 960.275 | 22.696 | 937.579 | 1660.845 | 2.547678 | 0.622260 | 0.453325 | 107.318354 |
| 2500 | gas | 566.911 | 7.418 | 559.493 | 2038.931 | 1.540674 | 0.473679 | 0.148218 | 64.041417 |
| 2800 | steam | 1085.936 | 25.653 | 1060.283 | 1878.169 | 2.764816 | 0.673004 | 0.495065 | 121.363511 |
| 2800 | gas | 524.610 | 6.511 | 518.099 | 2420.354 | 1.540674 | 0.473679 | 0.148218 | 59.303311 |
| 3000 | steam | 1171.673 | 27.670 | 1144.003 | 2026.446 | 3.415420 | 0.825237 | 0.619284 | 130.946271 |
| 3000 | gas | 696.310 | 13.476 | 682.834 | 2487.614 | 1.540674 | 0.473679 | 0.148218 | 78.159419 |

Delivered source heat includes recovered upstream circulation work. Upstream circulation electricity and costs are excluded equally. Net electricity plus rejection closes the conversion boundary for passing cases. Full capital accounts, salt makeup, disjoint machine/bundle/conversion replacement terms and pumping/generator losses are retained in plot-data.json.

## Failure classification and coverage

Water inlet 20 <= T < 60 C; pumped inlet/outlet remain in retained property range. Outlet bracket: pumped inlet + 1e-7 C to min(hot gas,60 C) - 1e-7 C. Lower and upper UA bounds are native outputs; no domain extrapolation.

| Role | Status counts |
| --- | --- |
| adverse_controller_offer | equipment_or_coupling_insufficient: 3, pass: 3, total: 6 |
| gas_catalog | equipment_or_coupling_insufficient: 39, cooler_upper_no_root: 233, pass: 14, cooler_lower_no_root: 78, cooler_mixed_bounds: 11, total: 375 |
| sensitivity | pass: 48, total: 48 |
| steam_connector_catalog | pass: 21, equipment_or_coupling_insufficient: 51, total: 72 |

Across the 498 cases, 464 cooler occurrences exceed their upper UA bound; 464 of these have a 60 °C property ceiling. There are 153 lower-bound occurrences. Multiple cooler occurrences can belong to one case. In `20260926-design-study-component-alternatives-b:c0001`, `water_pre` has selected UA 25.000 MW/K above the retained upper bound 23.469432 MW/K. In `20260926-design-study-component-alternatives-b:c0050`, `water_pre` has selected UA 20.000 MW/K below its lower bound 21.507403 MW/K.

A lower no-root result means the selected UA lies below the native lower bracket value, near the infinite-water-flow limit. An upper no-root result means selected UA exceeds the native upper bracket value. Where that upper temperature is 60 °C, the current property range limits the calculation; it does not prove the purchased equipment physically cannot work. A hot-gas terminal limit is identified separately in each cooler receipt. Neither class is ranked as an admissible offer. Solved coolers can independently fail purchased flow, power or duty capacity. Those margins, all failed predicates, and overlapping failure reasons remain visible in plot-data.json.

The water-property limits restrict tested candidate coverage and any ranking. No property range, equipment offer or physical domain was expanded. A passing case does not qualify machine maps, site hydraulics, or vendor quotes.

## Sensitivities and missing-cost frontiers

The sensitivity figure retains every efficiency, price, recurring-cost and common-source-PV case, including failed controller offers. It compares cost differences against the ±5 USD/net MWh band. Common source-service charges are accounting scenarios; no reactor fuel price is inferred.

| Source MW | Efficiency gap range USD/net MWh | Branch quote gap range | Common-PV equality BUSD | Missing-cost equality, X in BUSD2025 |
| ---: | ---: | ---: | ---: | --- |
| 2500 | -6.489 to +4.429 | -33.771 to +33.759 | -0.000966 | X_S = 1.675765 X_B +0.000653 |
| 2800 | -21.832 to +4.706 | -38.496 to +30.376 | -0.470856 | X_S = 2.046488 X_B +0.492746 |
| 3000 | +4.007 to +13.104 | -22.946 to +41.837 | 1.831386 | X_S = 1.675374 X_B -1.236871 |

At 3000 MW the efficiency scenarios retain the nominal cost sign: steam minus Brayton spans +4.007 to +13.104 USD/net MWh. The low end falls below the 5 USD/net MWh materiality threshold. The quote scenarios cross zero, so a material nominal advantage is not a price-independent technology ranking.

The negative common-PV equality values at 2500 and 2800 MW are algebraic extrapolations. There is no crossover for a nonnegative common charge under these held assumptions; added common cost favors steam’s larger energy denominator. They are not negative fuel prices. At 3000 MW equality occurs at +1.831386 BUSD2025; the +2 BUSD scenario gives about −0.870 USD/net MWh, within materiality.

The frontier follows directly from native present-value costs K and discounted net energies E: `X_S = (E_S/E_B)(K_B + X_B) - K_S`. It shows the cost corrections that would erase the comparison; it does not validate omitted purchase scopes. Reactor equipment, source fuel and upstream circulation costs remain excluded. Cooling-water site service, imposed pressure-service losses, off-design efficiencies, procurement scope and quotes remain conditional.

## Numerical repair comparison

All 498 new input maps are exactly identical to the preserved old record. Changed scalar channels are listed separately from engineering verdict changes in matched-study-summary.json. Changed engineering-status cases: 0.

- Largest absolute change in Steam net MW: +0, case `20260926-design-study-component-alternatives-b:c0000`.
- Largest absolute change in Brayton net MW: -2.22681815e-05, case `20260926-design-study-component-alternatives-b:c0206`.
- Largest absolute change in Steam USD/net MWh: +0, case `20260926-design-study-component-alternatives-b:c0000`.
- Largest absolute change in Brayton USD/net MWh: +1.53834378e-07, case `20260926-design-study-component-alternatives-b:c0040`.

Old blocked figures and data remain unchanged. Numerical verification now covers the repaired executable; physical-domain and price limitations remain.

## Evidence and replay

[Summary](matched-study-summary.json) · [Exact plot data](plot-data.json) · [CSV](plot-data.csv) · [Output and failed offers](matched-output.svg) · [Cost decomposition](matched-cost.svg) · [Sensitivity](matched-sensitivity.svg). Figures also have PNG copies. Every plotted point retains its native candidate ID, input parameters, fingerprint, evidence digest, verification status and actual constraint verdicts.

Record: `exploration/component_alternatives/studies/20260926-design-study-component-alternatives-b`. Stock verification SHA-256: `8150abe4c4a1ea5366dc2e9aeece5d0a583d952d1bcdc22e1ebf53cec96f2c01`. Executable fingerprint: `36f653faacc301e76132a9364c1b1024e6d0b3d28742138fcc4759aeef7b3986`.

Reproduce with `.codex-test/run python work/orchestration/goals/design-study-component-alternatives/evidence/verified-comparison/analyze-verified.py`. The renderer refuses to generate results until the stock verification receipt covers all 498 exact native case IDs and the current recorded fingerprint.
