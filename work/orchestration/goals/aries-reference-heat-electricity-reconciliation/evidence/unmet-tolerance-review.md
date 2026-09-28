# Review — unmet-heat absolute tolerance declaration

**Verdict: PASS.** A `1e-7` MW absolute tolerance on the four named unmet-heat channels is justified by the solvers' termination tolerances and conceals no real disagreement and no verdict difference.

## Recomputed worst |store − oracle|, 27 cases

| channel | worst | case |
|---|---|---|
| unmet_heat | 4.843e-09 MW | combined-source-thermal |
| he_unmet | 3.942e-09 MW | network-c3-0.70 |
| pbli_unmet | 3.580e-09 MW | combined-source-thermal |
| divertor_unmet | 1.264e-09 MW | combined-source-thermal |
| accepted_heat (undeclared) | 4.843e-09 MW | combined-source-thermal |
| turbine_temperature (undeclared) | 2.140e-09 K | nominal-calculated |

Stored unmet values strictly between 0 and 1 MW: none. Smallest positive: 2.028448680648353 MW (`network-c2-0.85`, `he_unmet`). 61 of 108 entries are exactly 0 on both sides, no zero/nonzero mismatch. Only the refused relative deviation (`1.609e-09`) exceeds `1e-9`; the next is `1.489e-10`.

## Findings

1. (note) Termination supports the claim. Native bisection stops at |residual| ≤ 1e-8 MW or a 1e-10 K bracket (`network_heat_driven_closure_impl.py:91`); the checker's `brentq` uses `xtol=1e-11` K (`oracle_entry.py:133`), so the gap is set by the native side, at order 1e-8 MW. The observed worst is 20x under 1e-7, which is 10x under the 1e-6 MW engineering floor. Same allowance as the reviewed `residual_magnitude` precedent (manifest, T-005).
2. (note) Verdict parity holds: `heat_removal_ok` is `satisfied` exactly where all four stored unmet channels are 0, `violated` where the per-case maximum is at least 40.01 MW. No operand lies within 1e-7 MW of any threshold below 2.03 MW.
3. (note) The bracket-width exit admits residuals up to the 1e-6 MW contract in principle; 1e-7 is not a blanket waiver, and a point beyond it still refuses.
4. (note) Three entries carry basis "Same as unmet_heat". Copy the full basis into each so every entry is self-describing.
5. (note) Log `c0009` and declaration `network-c2-0.85` are the same case (`candidate_id`).

The declaration touches only the manifest tolerance list; store and oracle share executable fingerprint `f739dbce…`.

## Not covered

Did not run the model or verifier. Did not verify the `heat_removal_ok` threshold, that it is the only predicate reading these channels, or that the manifest loader accepts the terse basis strings (that source lies outside the brief). The amended manifest and re-execution remain to be verified.

fresh tolerance reviewer, 2026-09-25
