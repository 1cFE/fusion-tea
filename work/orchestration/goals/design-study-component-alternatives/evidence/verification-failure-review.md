# Verification failure assessment

**Verdict: FINDINGS — stop dependent completion.** No demonstrable oracle bug was found. The all-case verification requirement remains unmet; this case's failed engineering predicates do not waive numerical verification. No model, oracle, inputs, pin or tolerances were changed.

[AGENT] Independent reviewer `/root/feasibility_review`, 2026-09-26. Scope: [verification-failure-review-brief.md](verification-failure-review-brief.md), case `c0206`, `gas-q2800-m2250-r1.35-ua25-25-25`. I inspected the retained mismatch, native outputs, implemented cooler and independent oracle, then isolated the cooler with identical native gas inputs.

The native cooler stops at UA residual `5.8467009012e-11 MW/K`, satisfying its `1e-10` stopping criterion. Water warms only about `0.0288422535 K`. Flow therefore strongly amplifies outlet-temperature error.

Independent 60-digit Decimal bisection used the single crossed property interval, `h(25)=104.82922` and `h(25.5)=106.92006 kJ/kg`, and the exact counterflow relation `UA=Q ln(g₂/g₁)/(g₂−g₁)`. With the native gas tuple:

| Quantity | Result |
| --- | ---: |
| Decimal outlet | 25.0905566208551465 °C |
| Decimal flow | 7213405.989193004 kg/s |
| Oracle flow at identical inputs | 7213405.989185534 kg/s |
| Native flow | 7213405.915089925 kg/s |

The oracle differs from this independent result by roughly `1.04e-12` relative; native differs by `1.0273e-8`. Thus the failure persists after eliminating upstream disagreement. Full-oracle flow disagreement is `1.1963e-8`; annual-energy disagreement is `2.0015e-8` against the unchanged `1e-9` requirement.

**Exact unmet requirement:** independently verify all required outputs within declared tolerances, including this completed failed case. Resolution needs improved native numerical accuracy and revalidation of the resulting executable, or new tolerance authority. Copying native stopping behavior into the oracle would not fix its accuracy. Neither route is authorized here. Preserve the 498 completed cases and 83 predicate-passing cases as partial evidence; do not call the full study numerically verified. Under the coordinator's recorded pin/cap constraints, stop rather than open another round.

## Full diagnostic scope

The subsequent `results/verification-diagnostics.json` covers all 498 cases, each with 872 scalar channels and 84 predicates. It records six cases with numerical mismatches and zero cases with predicate mismatches. Four numerical-mismatch cases already fail engineering checks. The other two, `sensitivity-q3000-gas-eta-0.03` and `sensitivity-q3000-both-eta-0.03`, satisfy all native predicates but each has two numerical mismatches. Thus numerical failure is not confined to otherwise-rejected cases. This diagnostic inventory does not release verification; the stop verdict above remains unchanged. No further numerical repair or model work was performed.
