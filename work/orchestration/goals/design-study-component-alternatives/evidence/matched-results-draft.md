# Matched results draft — verification blocked

[AGENT] **Unreleased native diagnostics.** All 498 cases completed, but study verification failed. The retained diagnostic finds six cases with numerical mismatches and zero predicate disagreements. Two mismatches occur in efficiency scenarios that satisfy every native constraint. No result below is presented as a fully verified study result or a technology recommendation. See [diagnosis](cooler-verification-diagnosis.md) and the record’s `results/verification-diagnostics.json`.

The record is `exploration/component_alternatives/studies/20260926-design-study-component-alternatives/`. [Analysis script](analyze-matched-study.py) reads native `results/cases.json`; it performs accounting and plotting only. [Summary](matched-study-summary.json), [plot data JSON](plot-data.json) and [CSV](plot-data.csv) retain exact case IDs, aliases, native statuses, all failed predicates and numerical mismatch channels. The figures carry the blocked-verification caption.

## What the native diagnostics show

The supplied steam cycle produces more net electricity in these three matched comparisons. Its connecting hardware strongly affects the conditional cost result. With the least-cost passing connector from the declared catalog, the first two price differences are inside the predeclared 5 USD/net MWh materiality band. At 3000 MW the nominal Brayton price advantage exceeds that band, but quote sensitivities reverse it. Steam’s 378–542 MW native output advantage exceeds the separate 5 MW materiality threshold. The numerical verification stop still prevents study release.

| Selected source MW | Steam connector: circuits × pumps, pump design kg/s | Steam net MW | Brayton net MW | Fixed 14-circuit steam cost | Selected-connector steam cost | Tested Brayton cost | Steam minus Brayton |
|---:|---|---:|---:|---:|---:|---:|---:|
| 2500 | 10 × 4, 225 | 937.58 | 559.49 | 45.31 | 33.76 | 33.77 | -0.006 |
| 2800 | 11 × 4, 225 | 1060.28 | 518.10 | 40.07 | 32.41 | 36.47 | -4.060 |
| 3000 | 14 × 3, 250 | 1144.00 | 682.83 | 37.13 | 37.11 | 27.67 | +9.446 |

Costs are hypothetical common-USD2025 scenario values per net MWh. The 2500 MW difference is only −0.0061 USD/MWh; it is a practical tie. The 2800 MW difference, −4.0601, is also below materiality. Holding the same 14-circuit/four-pump connector adds 11.5467, 7.6592 and 0.0191 USD/MWh at the three source powers, without changing the native steam net output. The underlying steam turbine/generator offer remains unchanged.

Selected Brayton cases are `gas-q2500-m2000-r1.5-ua25-25-25`, `gas-q2800-m1750-r1.8-ua25-25-25` and `gas-q3000-m2000-r1.65-ua25-25-25`. Selected steam cases are `steam-q2500-n10-k4-pump225`, `steam-q2800-n11-k4-pump225` and `steam-q3000-n14-k3-pump250`. These are discrete tested offers, not continuous optima. The drop in selected Brayton net output at 2800 MW accompanies a different admissible flow/ratio choice in the finite catalog; it is not a monotonic technology-performance curve.

[Output and failed-offer figure](matched-output.svg) · [Cost decomposition figure](matched-cost.svg) · [Sensitivity figure](matched-sensitivity.svg). PNG copies have the same names.

## Heat and electricity accounting

Both branches receive exactly the same source heat and temperatures within each pair. Delivered heat includes recovered upstream circulation work. Source-return temperature varies between the chosen source scenarios.

| Reactor / delivered heat MW | Return K | Branch | Gross MW | Included electric loads MW | Net MW | Rejected heat MW |
|---|---:|---|---:|---:|---:|---:|
| 2500 / 2598.424 | 565.276 | steam | 960.275 | 22.696 | 937.579 | 1660.845 |
| 2500 / 2598.424 | 565.276 | gas | 566.911 | 7.418 | 559.493 | 2038.931 |
| 2800 / 2938.453 | 563.261 | steam | 1085.936 | 25.653 | 1060.283 | 1878.169 |
| 2800 / 2938.453 | 563.261 | gas | 524.610 | 6.511 | 518.099 | 2420.354 |
| 3000 / 3170.448 | 561.787 | steam | 1171.673 | 27.670 | 1144.003 | 2026.446 |
| 3000 / 3170.448 | 561.787 | gas | 696.310 | 13.476 | 682.834 | 2487.614 |

At 2800 MW, steam’s 25.653 MW loads comprise 8.640 cycle pumping, 5.318 salt pumping, 11.594 water pumping and 0.100 control actuation. Brayton’s turbine produces 3037.297 MW shaft work; compressors consume 2501.980 MW. The remaining 535.317 MW shaft power loses 10.706 MW in generation, producing 524.610 MW gross electricity. Water circulation and actuation then consume 6.411 and 0.100 MW, leaving 518.099 MW net. The source loop’s 138.453 MW circulation electricity is upstream and excluded equally from the conversion metric; its recovered heat is already in the shared delivered duty. These accounting entries must not be charged twice.

## Capital, service, replacements and energy denominator

| Source MW | Branch | Capital BUSD2025 | Service PV BUSD2025 | Replacement PV BUSD2025 | Accounted PV BUSD2025 | Discounted net energy million MWh |
|---:|---|---:|---:|---:|---:|---:|
| 2500 | steam | 2.547678 | 0.622260 | 0.453325 | 3.623306 | 107.318354 |
| 2500 | gas | 1.540674 | 0.473679 | 0.148218 | 2.162570 | 64.041417 |
| 2800 | steam | 2.764816 | 0.673004 | 0.495065 | 3.932929 | 121.363511 |
| 2800 | gas | 1.540674 | 0.473679 | 0.148218 | 2.162570 | 59.303311 |
| 3000 | steam | 3.415420 | 0.825237 | 0.619284 | 4.859985 | 130.946271 |
| 3000 | gas | 1.540674 | 0.473679 | 0.148218 | 2.162570 | 78.159419 |

Steam salt makeup adds 0.000043538 BUSD2025 PV in each selected case; gas has none. At 2800 MW the 0.495065 BUSD steam replacement total contains 0.004027 salt-machine, 0.280449 bundle and 0.210589 generic conversion replacements. Those disjoint terms are retained separately in the summary. Gas capital and nominal recurring/replacement allowances are constant across its three selected offers; its changing cost per MWh is therefore an energy-denominator effect. Steam’s connector capital changes with the selected inventory. Full account-level capital amounts are retained in the plot data.

## Sensitivity and unresolved cost frontier

The ±3 percentage-point efficiency cases are assumed performance variations, not validated off-design maps. Their native steam-minus-gas cost gaps span −6.489 to +4.429, −21.832 to +4.706, and +4.007 to +13.104 USD/MWh at 2500, 2800 and 3000 MW. The 3000 MW gas-minus-3-point and both-minus-3-point cases have numerical mismatches and are specifically marked with diamonds in the sensitivity figure. Their native differences are diagnostic values, not admitted sensitivity bounds.

Branch quote factors of 0.5 and 1.5 can reverse the nominal signs. At 3000 MW, halving the steam quote changes the native gap from +9.446 to −9.112 USD/MWh; increasing the gas quote by 50% changes it to −4.389, inside materiality. Opposed quote scenarios span −33.771 to +33.759, −38.496 to +30.376, and −22.946 to +41.837 across the three source powers. The ±50% joint service/replacement allowance gives gaps +1.043/−1.055, −2.457/−5.663 and +9.287/+9.604. Unknown equipment scope is still unknown under every finite multiplier.

Adding the same source-service PV charge to both branches favors steam’s larger electricity denominator. At +0.5 BUSD, the native gaps become −3.154, −8.371 and +6.867 USD/MWh. At +2 BUSD they become −12.600, −21.306 and −0.870. The last value is inside materiality, not a material steam advantage. The 3000 MW nominal equality occurs at about 1.8314 BUSD of common added PV charge. No fuel price, reactor expense or fuel qualification is inferred.

Let unknown additional costs be `X_S` and `X_B`, both in BUSD2025. The native-accounting equality frontiers are:

| Source MW | Cost-correction equality |
|---:|---|
| 2500 | `X_S = 1.675765 X_B +0.000653` |
| 2800 | `X_S = 2.046488 X_B +0.492746` |
| 3000 | `X_S = 1.675374 X_B -1.236871` |

These follow only from native accounted PV costs and discounted energies: `X_S = (E_S/E_B)(K_B+X_B) − K_S`. They expose missing-cost sensitivity; they do not authenticate the assumed installed scopes.

## Failures and completeness

Of 498 unique native cases, 83 satisfy all stored native predicates and 415 do not. There are no execution refusals in this selected native window. The gas catalog has 14/375 passing cases: 322 have at least one cooler with no admissible root in its water-property window, and 39 have other equipment/coupling failures without that no-root condition. No-root cases can also fail other predicates; the full lists remain in plot data. These are calculation-validity failures, distinct from a numerically completed cooler whose flow, power or duty exceeds purchased capacity.

The steam connector catalog has 21/72 passing cases, including three aliases of gas-anchor rows; the alias map prevents duplicate counting in the 498 unique total. All 48 price/efficiency/recurring/source-charge cases satisfy native predicates, but two have numerical mismatches. Of the six smaller-controller tests, all three 500 kg/s gas offers fail; all three 500 kg/s steam offers pass the implemented constraints. A smaller offer is not presumed insufficient.

The six mismatching case IDs are `c0035`, `c0040`, `c0160`, `c0206`, `c0480` and `c0484`, all under this study’s candidate-ID prefix. The last two are the otherwise-passing 3000 MW negative gas/both efficiency cases. The four gas-catalog mismatches are also marked in the output figure. Zero predicate disagreements does not cure the numerical verification failure. Independent review requires a numerical repair/new identity or explicit tolerance authority; neither has been carried out.

## Scope limits

This is the supplied steam offer versus tested gas offers, with unequal supported operating freedom. Steam temperature/reheat/condenser settings remain limited by inherited equipment conditions. The primary loss law and controller allowance are imposed pressure-service assumptions, not qualified branch hydraulics or valve curves. Cooling water/site service, several procurement scopes, quotes and off-design efficiencies remain conditional. The source-loop scenarios do not demonstrate reactor/plasma turndown. Reactor equipment, source fuel and upstream circulation costs are excluded, so these values are not whole-plant LCOE. The requested fully verified comparison remains unmet.
