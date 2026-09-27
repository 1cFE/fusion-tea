# Correction: scope of the diagnosed numerical cause

[AGENT] 2026-09-26. Final independent assurance identified an overstatement in the original record's §15 finding `20260926-design-study-component-alternatives#1`. The sealed snapshot remains `1e8a19872852e19390eba76445e11a866c5da8fb9f791122b6b64d6e16b66641`; this addendum changes no snapshot, indicator, result, model or tolerance.

**Corrected finding:** Six cases exceed the predeclared numerical verification tolerances, including two cases that satisfy all native engineering predicates. Native cooler stopping accuracy was independently diagnosed as a cause only for case `c0206`. The causes of the remaining mismatches were not independently isolated.

The two otherwise-passing sensitivity cases, `c0480` and `c0484`, disagree on bypass flow and helium hot-bound margin. Their mismatches must not be attributed to the cooler on the present evidence. Exact channels and values remain in `results/verification-diagnostics.json`.

The disposition is unchanged: verification is blocked. All required scalar outputs must meet the unchanged contract. The exact cooler diagnosis is in `results/verification-failure-review.md`; it is sufficient to establish an unresolved native accuracy requirement, without asserting one common cause for all six cases. No follow-up modeling or policy exception is authorized by this correction.
