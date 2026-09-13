# Verification

Status: Oracle implementation verified; native package acceptance pending. Independent audit has not run.

The entering oracle is recorded at `dab391ed`. Before edits, `.codex-test/run python -m pytest tests/study/test_domain_consumers.py -q` returned 21 failed and five passed; `tests-before.txt` records every failed identity. All 21 failures are new tests exposing the two existing oracle defects, including unintended division/type errors and missing rejection. No historical expectation was changed.

After the six-line guard correction, the same 26 tests passed. One additional explicit original counterexample was then added: R=12.7 with a 13 m coil centre, constructed through the existing oracle radial-build parameters (`coil_t=20`). The final command `.codex-test/run python -m pytest tests/study/test_domain_consumers.py -q --tb=short` is recorded in `tests-after.txt`.

Four valid controls in `oracle-before.json` cover baseline, R=14, changed cold/ambient temperatures, and zero cold load plus 2 MW direct electrical power. Full oracle output maps remain exactly equal. Field normalization and refrigeration energy balance are also independently checked by multiplied-through identities. The input mapping remains exactly 99 entries and output mapping is unchanged. Ambient temperature is tested through the oracle parameter interface; its qualified adapter key remains unsupported and is explicitly rejected.

No package-dependent acceptance has been attempted while native regeneration is in flight. The oracle itself does not publish full-plant engineering verdicts. Existing baseline and R=14 verdict checks will run after the native author signals stability. Broad historical suites are not claimed passing by these focused checks.
