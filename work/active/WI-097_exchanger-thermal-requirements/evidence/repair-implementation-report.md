# WI-097 numerical repair implementation

2026-09-27. [AGENT] Implements the independently approved remedy in [numerical-repair-review.md](numerical-repair-review.md). Round 3 remains preserved as prerequisite evidence. Round 4 must verify the unchanged 1277 input maps under the repaired executable before scientific reporting resumes.

## Change

The controlled closure evaluates the counterflow denominator as `(1-Cr) + Cr*(-expm1(-NTU*(1-Cr)))`. It uses the analytic equal-capacity limit only at `Cr == 1`. This removes cancellation and the approximate equality branch's discontinuity while preserving the intended effectiveness equation. See the [investigation](numerical-repair-investigation.md) for high-precision diagnosis and comparison against a denominator-only repair.

The physical equations, bypass residual target of 1e-10 MW, 100-iteration budget, cycle tolerances, inputs, constraints, equipment, pricing and independent oracle are unchanged. The production diff contains the owned closure body, its generated copy and the generated package contract's body hash and executable fingerprint. SysML sources, staged sources, snapshot and census remain byte-identical.

## Build and evidence identity

The stock generator reached a fixed point after smart regeneration and preserved handwritten completions. The repaired executable fingerprint is `668b903599f995fd6e9038d61a2401144d79f1db13f221b4a663df7cb24a2a23`. Build receipts are [repair-build/build-hashes.json](repair-build/build-hashes.json); the rerunnable wrapper is [repair-build.py](repair-build.py). It redirects build logs into a fresh directory to preserve the original build evidence.

The failed Round 3 store, original 18-case development receipt and original oracle verification retain their recorded hashes in [repair-preservation.json](repair-preservation.json). Every corrected development case uses a fresh output directory. The implementation did not edit independent oracle files or execute the main study.

## Native replay and regression results

[repair-native-controls.json](repair-native-controls.json) contains 20 evaluated cases: exact complete input maps from the original 18 development controls and the two failed study maps. [repair-native-run.py](repair-native-run.py) reproduces this replay and checks full input-map equality and preservation hashes.

- All seven legacy replays preserve every previously recorded output and all 35 verdicts bit-for-bit. Historical 551-channel and 14-predicate comparison also passes.
- Every original control retains its complete verdict set. Equipment purchase outputs remain exact. Existing partial-transfer, original-UA, zero-conductance, hot-cap and actuator-limit failures retain their intended failed states.
- Both formerly failed maps, c0621 and c1085, evaluate and satisfy all 35 native predicates.
- Fifteen high-precision conductance fixtures cover both sides of capacity equality. Nine independently constructed near-equality duty roots and both captured failed trial states meet the unchanged 1e-10 MW root residual.
- All 56 tests pass: 29 existing equation, native, accounting and requirement-boundary tests plus 27 kept repair regressions. The existing tests read freshly replayed controls and write their artifacts under `repair-validation/`; the original receipt files remain unchanged. See [repair-validation.log](repair-validation.log) and [repair-validation.py](repair-validation.py).

The near-boundary requirement mutations remain comparison-binding fixtures. They are not study candidates or claims about independent certification exactly on a thermal constraint.

## Remaining integration evidence

All 20 corrected development cases pass the unchanged independent oracle on 435 channels and 35 predicates; see [repair-oracle-verification.json](repair-oracle-verification.json). Oracle source bytes and all 44 absolute tolerance classes remain unchanged. The coordinator owns the repaired package commit, refreshed study metadata, integration gates and exact 1277-map Round 4 replay. The implementation is ready for that sequence; its development tests alone do not certify the full study.
