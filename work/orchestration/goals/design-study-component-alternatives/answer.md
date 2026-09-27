# Verified matched conversion comparison

**The bounded numerical repair is complete, and all 498 original study cases now pass the unchanged independent verification contract.** The result supports a conditional comparison of the selected steam offer versus tested helium Brayton offers at matched source conditions. At 2500 and 2800 MW source heat, the nominal cost differences fall inside the declared 5 USD2025/net MWh materiality band. At 3000 MW, the tested Brayton offer has a nominal 9.446 USD/net MWh advantage, but quote assumptions can reverse it. There is no unconditional technology recommendation.

## What the verified offers show

| Chosen reactor heat, MW | Selected steam net MW | Tested Brayton net MW | Steam USD2025/net MWh | Brayton USD2025/net MWh | Steam minus Brayton |
|---:|---:|---:|---:|---:|---:|
| 2500 | 937.579 | 559.493 | 33.762 | 33.768 | −0.006 |
| 2800 | 1060.283 | 518.099 | 32.406 | 36.466 | −4.060 |
| 3000 | 1144.003 | 682.834 | 37.114 | 27.669 | +9.446 |

These are conversion-subsystem costs per net MWh. The steam turbine offer is held at its supported temperatures; its connecting equipment is selected from explicit offers. Gas flow, pressure ratio and service equipment vary within the tested catalog. The branches have different supported operating freedoms, so these results do not establish equal optimization or whole-plant LCOE.

Steam generates 378–542 MW more net electricity at the selected points. Its larger capital and recurring costs offset much of that benefit. At 2500 MW, for example, steam delivers 937.579 MW net from 960.275 MW gross, after 22.696 MW of internal electrical loads. Brayton delivers 559.493 MW from 566.911 MW gross, after 7.418 MW of loads. Steam capital is 2.548 billion USD2025, versus 1.541 billion for Brayton. The resulting costs per net MWh are nearly equal.

The connecting hardware materially affects the comparison. Selected steam connectors use 10 circuits ×4 salt pumps at 225 kg/s design flow, 11×4 at 225 kg/s, and 14×3 at 250 kg/s. Holding the larger 14×4 connector at all source duties would instead give steam costs of 45.309, 40.065 and 37.133 USD/net MWh. The lower-duty improvement therefore comes from a declared equipment choice, with its price and capacity checks retained. No hardware is automatically resized.

The selected gas offers use 2000 kg/s at stage ratio 1.5, 1750 kg/s at 1.8, and 2000 kg/s at 1.65. Each uses 25/25/25 MW/K cooler conductance and 60 MW/K recuperator conductance. These remain the least-cost passing gas offers in the exact finite catalog after numerical repair.

## Sensitivity and exclusions

All 48 declared efficiency, price, recurring-cost and common-charge sensitivities now verify. At 3000 MW, efficiency scenarios retain a positive steam-minus-Brayton cost gap of 4.007–13.104 USD/net MWh, but part of that range falls below the 5 USD materiality threshold. Branch quote scenarios span −22.946 to+41.837 and reverse the preference. A common upstream present-value charge of about 1.831 billion USD2025 would erase the nominal 3000 MW advantage because steam spreads that common cost over more net electricity. This is an accounting sensitivity, not a fuel-price or whole-plant model.

Only 14 of 375 gas catalog offers pass every engineering check. The excluded offers comprise:

- **39 equipment or coupling failures with solved coolers:** offered ratings or source/return requirements fail.
- **233 with only upper cooler-root exclusions:** at least one cooler cannot find a solution below the retained 60°C water-property ceiling.
- **78 with only lower cooler-root exclusions:** selected conductance is below the model's lower bracket near the infinite-water-flow limit.
- **11 with both lower and upper exclusions across their coolers.**

These categories prioritize cooler validity; other failures can overlap and remain visible in the full predicate data. All 464 individual upper-root exclusions in this catalog occur at the 60°C property ceiling. They are unsupported calculation ranges, not proof that the physical equipment cannot operate. A lower conductance exclusion is a modeled heat-transfer limitation. Solved coolers separately check purchased flow, power and duty ratings. The comparison ranks only supported passing offers, so these exclusions substantially limit catalog coverage. No property range was extended to create more passing candidates.

Steam has 21 passing connecting-equipment offers out of 72 tested. Across the complete deduplicated study, 83 cases pass all 84 engineering predicates and 415 fail one or more. All 498 cases, including those failures, pass numerical verification. Failed offers never enter the economic ranking.

## What the repair changed

Independent diagnosis isolated every original discrepancy. Four cases had cooler root errors amplified into water flow, pumping, small capacity margins or net energy. Two efficiency cases had heater-network root errors propagated into the hot-side margin and bypass flow, plus smaller local bypass error. The latter were not cooler failures.

The three existing bisections now resolve their brackets to adjacent representable floating-point values and select the endpoint with the smaller equation residual. Focused regressions test the required outputs against unchanged independent evidence: 15 assembled cases and nine high-precision local cases. Full replay then verifies 434,256 scalar comparisons and 41,832 exact predicate comparisons. No input map, physical equation, property range, equipment offer, oracle, tolerance or engineering verdict changed. The original failed executable and evidence remain sealed.

The repair adds zero physical closures. Across the full work item, seven new or modified handwritten definitions are now disclosed, including the two local numerical variants. The [repair review](evidence/numerical-repair-review.md) passes this bounded scope. The earlier [engineering equality explanation](evidence/engineering-equalities.md) and [design review](evidence/design-review-fourth-submission.md) retain the physical variable roles and MR-7 rationale. Adjacent-float convergence and this verification do not promise uniform relative accuracy for arbitrary near-zero outputs outside the tested cases.

## Boundary and qualification

Both branches receive the same calculated source conditions at each chosen reactor duty: 14 original helium paths, 8 MPa nominal pressure and 773.15 K hot supply. The shared return state follows the inherited primary circulation law and reviewed pressure-service assumption. Delivered heat includes recovered primary circulation work. The subsystem includes connecting exchangers, salt transport where required, conversion machinery, controllers, water pumping and heat rejection. Upstream reactor equipment, fuel, primary circulation electricity and its costs remain outside the metric. Finance is common: USD2025, 85% availability, 5% real discount and 30 years.

Installed prices, scope allowances, pressure service, site hydraulics and machine efficiency maps remain conditional. The static validator retains 72 literal warnings and 766 alias diagnostics with their independently reviewed native-evidence dispositions. Numerical acceptance does not remove those disclosed qualification limits.

## Evidence and completion

The [verified report](evidence/verified-comparison/report.md) contains the accounting, sensitivity and cost-correction details. Publication figures show [net output and failed offers](evidence/verified-comparison/matched-output.svg), [cost contributions](evidence/verified-comparison/matched-cost.svg), and [sensitivities](evidence/verified-comparison/matched-sensitivity.svg), with PNG copies, exact data and a reproducible renderer. The [assembly diagram](evidence/reviewed-comparison-boundary.svg) shows the common boundary.

The [new native record](../../../../exploration/component_alternatives/studies/20260926-design-study-component-alternatives-b/record.md), [candidate ledger](candidate-ledger.md), [replay instructions](evidence/replay.md), and [final independent review](evidence/repaired-results-review.md) carry the completion evidence. Independent repair and final economic reviews both PASS. The new snapshot is `ea6b9de7cf242c88f764a9a997aadd1b6d813560b5c0953e84e63a7aeef9928e`; all 720 artifact hashes were checked. The authorized technical work is complete. Formal goal and WI-096 closure remain with the owner.
