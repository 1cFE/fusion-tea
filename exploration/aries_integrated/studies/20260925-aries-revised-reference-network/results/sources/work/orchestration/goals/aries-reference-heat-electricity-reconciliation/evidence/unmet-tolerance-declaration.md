# Declared absolute comparison tolerance for the unmet-heat channels (2026-09-25)

[AGENT] Numerical-verification declaration for the round-2 study `20260925-aries-revised-reference-network`; requires focused independent review before use. It changes no model equation, input, point, verdict rule or package byte.

## Observed refusal

All-point verification (`scripts/study/verify.py`, 27 of 27 stored cases) refused one channel: `aries_integrated_plant__heat_exchangers__evaluate__he_unmet` in `network-c2-0.85` (store `2.028448680648353` MW, oracle `2.0284486773855406` MW; relative deviation `1.609e-09` against the `1e-9` rule; absolute error `3.263e-09` MW; no absolute tolerance declared). Log: `t004-verify-attempt1.log`. Every other channel on every case agreed.

## Why it is numerical

- The four unmet-heat channels (`unmet_heat`, `he_unmet`, `pbli_unmet`, `divertor_unmet`) are differences of order-1000 MW delivered and transferred duties fixed by a root solve on the turbine inlet temperature. The native closure terminates at `|residual| ≤ 1e-8` MW or a `1e-10` K bracket (`exploration/aries_integrated/native_completions/network_heat_driven_closure_impl.py:91`); the independent checker uses `brentq` with `xtol=1e-11` K (`exploration/aries_integrated/studies/oracle_entry.py:133`). Two correct solvers therefore agree on these channels only to the order of `1e-8` MW.
- Across all 27 points the largest store-versus-oracle absolute difference on the four channels is `4.84e-09` MW (`unmet_heat`, `combined-source-thermal`); on `accepted_heat` it is `4.84e-09` MW and on `turbine_temperature` `2.14e-09` K. The refused case is the only one whose unmet value is small enough (2.03 MW) for `1e-9` relative to demand less than the solver accuracy (`2e-9` MW). Round 1 had no unmet value below ≈ 16 MW, so its relative rule never met this class.
- Verdict parity is unaffected: the only predicate reading these channels is `heat_removal_ok`, and every stored unmet value is either exactly `0` or at least `2.03` MW, so no verdict lies within `1e-7` MW of its threshold.

## Declaration (proposed manifest entries)

Absolute tolerance `1e-7` MW on exactly these four channels, the same allowance the earlier goal declared and had independently reviewed for `residual_magnitude` (T-005, `.project/active/study-residual-tolerance/review.md`): it exceeds the `1e-8` MW native termination by a rounding allowance and stays below the model's minimum `1e-6` MW engineering balance tolerance. Undeclared channels keep the strict relative rule; the verifier still reports the actual relative deviation and re-derives every verdict exactly.

```json
[
  {"channel": "aries_integrated_plant__heat_exchangers__evaluate__unmet_heat", "value": 1e-07, "units": "MW", "basis": "Difference of order-1000 MW duties fixed by a root solve terminating at 1e-8 MW; below the 1e-6 MW engineering balance tolerance; declared for the round-2 reconciliation study and independently reviewed (unmet-tolerance-review.md)"},
  {"channel": "aries_integrated_plant__heat_exchangers__evaluate__he_unmet", "value": 1e-07, "units": "MW", "basis": "Same as unmet_heat"},
  {"channel": "aries_integrated_plant__heat_exchangers__evaluate__pbli_unmet", "value": 1e-07, "units": "MW", "basis": "Same as unmet_heat"},
  {"channel": "aries_integrated_plant__heat_exchangers__evaluate__divertor_unmet", "value": 1e-07, "units": "MW", "basis": "Same as unmet_heat"}
]
```

## Procedure after review

Amend the live manifest `exploration/aries_integrated/studies/manifest.json` (tolerance list only; pin and fingerprints unchanged), rerun indicators and preflight on the amended manifest, keep attempt 1's results as `results-attempt1/`, re-execute the same 27 declared points into fresh `results/`, compare the two executions channel for channel, and verify all 27 points. Attempt 1's refusal log is retained.
