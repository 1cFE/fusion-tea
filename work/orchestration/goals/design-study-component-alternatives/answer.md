# Matched conversion comparison: verification blocked

**The fourth design passed review, implementation and integration completed, and all 498 matched-study cases executed. The economic comparison remains incomplete because numerical verification failed.** Independent review confirmed the native cooler accuracy problem and required a stop. No model repair, tolerance exception or additional round followed. Formal goal and WI-096 closure remain with the owner.

## Exact unresolved requirement

The model must reproduce required scalar outputs within the predeclared verification tolerances: normally relative error below 1e−9, with named absolute classes declared before execution. Six cases fail this requirement. Two are efficiency sensitivities that pass all implemented engineering checks. Every case is retained.

The clearest failure is `gas-q2800-m2250-r1.35-ua25-25-25`. Its precooler water warms by only about 0.02884 K. A tiny outlet-temperature error therefore produces a larger relative error in calculated water flow and pumping demand. The native cooler meets its local UA residual stopping criterion, but its flow differs from an independent 60-digit result by about 1.03e−8 relative. The oracle agrees with that independent result to about 1.04e−12. This is a native numerical accuracy shortfall, not a demonstrated oracle error. See the [independent failure review](evidence/verification-failure-review.md).

Resolving it requires improved native numerical accuracy and revalidation of a new executable, or explicit new tolerance authority. Neither was taken. The original failed cases, package identity and verification thresholds remain unchanged.

## What the authorized revision achieved

The [engineering equality explanation](evidence/engineering-equalities.md) identifies chosen inputs, calculated operating states and checks. Source heat, compressor ratios and purchased equipment remain explicit designer choices. Model-owned bypass controllers calculate the operating split or report insufficient heat transfer. Finite water cooling calculates required flow and pumping demand; recuperator effectiveness follows installed conductance and gas flow.

These are substantive physical additions. The reviewed scope counted five new or modified bodies, including one newly written iterative cooler calculation used three times. The [fourth design review](evidence/design-review-fourth-submission.md) accepted the scope and MR-7 roles without a solver-policy waiver. The [implementation review](evidence/implementation-integration-review.md) passed the exact implemented design and development evidence. All ten stock integration gates passed. The broader study then exposed the numerical limitation above.

The static validator is not wholly green: 72 literal-screen warnings and 766 alias diagnostics were individually mapped to native evidence and accepted within the implementation review. They are separate from the subsequent numerical failure.

## What the retained native outputs show

**The following values are unreleased diagnostics, not a verified economic result or procurement recommendation.** They compare the selected steam offer with tested Brayton offers at matched source conditions, using conversion-subsystem cost per net MWh. They do not compare equally optimized technologies or whole-plant LCOE.

| Chosen reactor heat, MW | Selected steam cost, USD2025/net MWh | Best tested passing Brayton cost | Steam minus Brayton | Diagnostic interpretation |
|---:|---:|---:|---:|---|
| 2500 | 33.762 | 33.768 | −0.006 | Indistinguishable at the declared materiality |
| 2800 | 32.406 | 36.466 | −4.060 | Inside the 5 USD/net MWh materiality band |
| 3000 | 37.114 | 27.669 | +9.446 | Nominal Brayton advantage; conditional and unreleased |

The selected steam connecting hardware uses 10, 11 and 14 exchanger circuits, respectively. The same 14-circuit steam hardware at all source levels costs 45.309, 40.065 and 37.133 USD/net MWh. This shows why explicit connecting-equipment selection matters: holding excess hardware at lower source duty can dominate the apparent technology difference. The steam turbine offer itself remains fixed.

There are 83 cases passing all 84 implemented engineering checks and 415 with failed checks. Of 375 gas catalog combinations, only 14 pass. Many failures occur because the finite-water cooler has no supported root inside its retained property range; this does not prove that a larger real cooler is physically worse. Other cases exceed offered equipment or fail source matching. Failed offers never enter the ranking. All 48 declared efficiency/price/service/common-charge sensitivities executed, but the two numerical failures prevent releasing the full sensitivity result.

The [diagnostic figures and detailed decomposition](evidence/matched-results-draft.md) retain net output, internal loads, capital, service, replacements, common-source-charge effects and price sensitivity. [Plot data](evidence/plot-data.json) joins every point to its native case and check status. The [candidate ledger](candidate-ledger.md) includes rejected approaches and the changed/reused inventory.

## Boundary and practical limits

Both branches use the same calculated primary source state at each chosen reactor duty: 14 original helium paths, 8 MPa nominal source pressure, 773.15 K hot supply, and the inherited circulation law with the reviewed pressure-service assumption. Delivered heat includes recovered primary circulation work. Required return conditions are shared within each pair.

The subsystem includes connecting heat exchangers, salt transport where required, conversion machinery, controllers, water pumping and heat rejection. Reactor equipment, fuel and upstream primary circulation costs and electricity remain outside the metric. Finance is common: USD2025, 85% availability, 5% real discount and 30 calendar years. The illustrative common upstream present-value charge is a denominator sensitivity, not a fuel-market model.

Installed prices and scope, controller/site hydraulics, machine efficiency maps and some service allowances remain conditional. A price multiplier cannot qualify missing hardware scope. Even after numerical repair, those limitations would prevent an unconditional technology recommendation.

## Completion assessment

| Requested outcome | State |
|---|---|
| Physical equalities, variable roles and bounded scope | Explained; independently reviewed |
| MR-7 compliant implementation and native integration | Completed on the retained identity |
| Matched source scenarios and explicit equipment offers | 498 native cases completed; failed cases retained |
| Verified performance/economic comparison | **Unmet: six numerical mismatch cases** |
| Price/efficiency sensitivity and causal decomposition | Executed; retained as unreleased diagnostics |
| Sealed evidence, figures, data, renderer and replay | Supplied for the blocked attempt |
| Final independent assurance | Failure assessment completed; blocked-record assurance recorded in the trail |
| Formal goal/work-item closure | Owner-held |

[Study record](../../../../exploration/component_alternatives/studies/20260926-design-study-component-alternatives/record.md) · [Replay](evidence/replay.md) · [Proposed passage](proposed-passage.md) · [Trail](trail.md).
