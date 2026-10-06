# Six-case diagnosis and bounded repair

[AGENT] Three existing bisections stopped at local heat or UA residuals too early to control sensitive downstream outputs. The repair resolves each existing root bracket to adjacent floating-point values and chooses the endpoint with the smaller equation residual. It retains equations, physical domains, feasibility branches, original iteration caps and engineering predicates. This is floating-point numerical resolution, not a new physical closure or a relaxed verification tolerance.

| Case | Mechanism | Independent evidence |
| --- | --- | --- |
| c0035 | Cooler temperature error amplifies into water flow, then subtracting flow from its rating amplifies relative margin error. | 65-digit piecewise integration at exact native and oracle tuples |
| c0040 | Cooler flow/power error propagates into the small net-electric remainder, annual energy and its cost denominator. | Same independent tuple decomposition |
| c0160 | Cooler flow error is small relative to flow but large relative to the near-zero negative capacity margin. | Same independent tuple decomposition |
| c0206 | Water rise is only about 0.02884 K; residual-only stopping amplifies temperature error into 7.2 million kg/s flow, pumping power and negative net energy. | Same independent tuple decomposition and prior Decimal replay |
| c0480 | Network root error changes a small positive hot-bound margin and the controller inlet. The local controller adds a smaller bypass-flow error. | Independent 65-digit and 70-digit roots |
| c0484 | Same gas tuple and numerical causes as c0480; the separate steam efficiency change does not cause the mismatch. | Independent roots and bit-exact sealed replay |

The reviewer-owned `work/orchestration/goals/design-study-component-alternatives/evidence/numerical-repair-review/isolate_original.py` and `.json` retain all six high-precision calculations. The local `gas-root-diagnosis.py/.json/.md` retain exact tuples, sealed-body replay, local/upstream decomposition and nearby efficiency cases. At c0480/c0484 the hot-margin native error is about -4.216e-10 K; propagated bypass error is about -2.116e-8 kg/s and local controller error +3.814e-9 kg/s. The accurate full bypass differs from the unchanged oracle by about 1.45e-10 kg/s, within its existing relative contract.

The network and controller changes are goal-local copies of original bodies. The original bodies remain unchanged. The cooler is already goal-local. All three use endpoint selection only after the midpoint no longer separates the bracket. No assertion threshold, input, output schema, property table, independent oracle or tolerance class changes. Fresh regressions must demonstrate output accuracy and identical predicate outcomes; adjacent-float convergence alone does not certify that result.
