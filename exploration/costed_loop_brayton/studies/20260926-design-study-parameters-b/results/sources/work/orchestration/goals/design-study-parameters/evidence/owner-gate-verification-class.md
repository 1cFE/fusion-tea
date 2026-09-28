# Owner gate G-001: a verifier refusal outside the declared tolerance classes

Raised 2026-09-26 by the round agent (T-005). Contract `comparison-contract.md` § 9: "every stored point against the package-owned oracle at relative deviation < 1e-9, or an absolute class declared in the new package's manifest before execution … No class is added or relaxed after a result is seen; a refusal outside them is an owner gate." § 12 names this as a condition that changes the conclusion. This is that case.

## What happened

All 272 kept points of study `20260926-design-study-parameters` executed through the stock lifecycle (272 of 272 completed, package tree clean). The all-point verification (`scripts/study/verify.py`, sample size 272, stratified by verdict combination) refused on one channel of one case:

| Case | Channel | Store | Oracle | Absolute | Relative |
|---|---|---|---|---|---|
| `s1-turb0.90-f2500-r1.4500` (candidate `c0211`) | `heat_exchangers__evaluate__he_hot_bound_margin` | 0.3631786747627075 K | 0.363178674230312 K | 5.32e-10 K | 1.466e-09 |

The verifier's own text is in `t005-verify.log`. The channel is the difference between the helium source limit (773.15 K) and the computed helium hot-side temperature at a point that sits 0.36 K from the bound (the turbine-efficiency 0.90 case at 2,500 kg/s / 1.45). The two temperatures agree to about 3e-10 K (the oracle solves the closure with a Brent root, the package with its native iteration; the worker's report names the 2.7e-10 K root difference); dividing that by a 0.36 K margin gives the 1.5e-9 relative figure. No other channel on any case is outside the rule: the coordinator's full comparison (every stored case, every catalogued channel) finds exactly this one, with the next-worst undeclared channel at 9.6e-10 relative (`he_unmet` on `s1-comp0.85-f2250-r1.5183`, 2.8 MW unmet, absolute 2.7e-9 MW). Every verdict re-derives identically from the oracle's operands (272 of 272).

## What the owner has to decide

Whether to declare an absolute class for the three hot-bound margin channels (`he_hot_bound_margin`, `pbli_hot_bound_margin`, `divertor_hot_bound_margin`) of, proposed, 1e-6 K, on the same basis as the ARIES closure classes (a temperature difference fixed by a root solve terminating at 1e-8 MW; the ARIES manifest declares 1e-7 MW classes for `unmet_heat`, `he_unmet`, `pbli_unmet` and `divertor_unmet` on the same body, which the contract's § 9 transcription also omitted from this package's manifest), then re-run the verifier and seal the record; or to leave the study unsealed on this channel.

The proposal is the round agent's and is executed only after the ruling. Under it, the coordinator's comparison shows all 272 cases would pass every channel; the reading of the study does not change under either ruling, because no stored value moves, only whether the record may carry the "verified" seal.

## What is parked

The study's seal (`snapshot.json`, `sealed-package.tar.gz`, a passing `results/verification_summary.json`) and the claim "verified" in the answer. Everything else in T-005 (the readout of stored channels, the figures, the record's other sections, the answer draft) is independent of the ruling and continues, marked provisional.

## To resume after a ruling in favour

1. Add the class to `exploration/costed_loop_brayton/studies/manifest.json` `absolute_tolerances` (and to the record's `manifest.json` copy, which is the same file), with the basis text; the manifest pin (`53f48a7e…`, the indicator-input fingerprint) does not include the manifest itself, so the package identity is unchanged.
2. Re-run the verifier command in `results/execution-context.json` with `--out results/verification_summary.json`.
3. Run the freeze (`evidence/freeze-study.py --record …`) and commit the record.
