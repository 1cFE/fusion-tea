# Comparison-candidate test repair — 2026-10-08

[OWNER] Requested fixing the eight remaining recorded comparison-candidate failures. [INHERITED: 20261008-scoring-repair.md] Explorer API, production formulas, published data, model packages, independent oracles, sealed comparison evidence and runtime dependencies remain protected. Parallel owner-authored API-gate work is outside this repair.

[AGENT] **Scoped regression PASS, independently reviewed:** 149 tests pass, with all eight original failed identities preserved and passing. No failures, skips, expected failures or retired tests. [Independent final review](20261008-comparison-candidate-review.md) passes; [machine attribution](20261008-comparison-candidate-attribution.json) records source hashes, protected hashes and original-node outcomes.

## Requirements

- [INFERRED] Preserve useful checks that reject inconsistent power accounting, missing predicate coverage, invalid numerical results and loss of failed-run evidence.
- [INFERRED] Correct obsolete fixture/package joins without changing the comparison's accounting rules, tolerances, acceptance criteria or sealed evidence.
- [INFERRED] Run historical comparison checks against their exact contract where needed to exercise still-useful failure behavior; avoid new historical calibration tests.
- [OWNER] Important changes to comparison acceptance require owner judgment. No such change is currently required.
- [INHERITED: CLAUDE.md and prior repair reports] Use `uv run --no-sync`, the retained runtime and temporary test outputs. Preserve owner edits and stage only this repair.

## Plan

- [x] Reproduce all eight original failures and determine their actual refusal causes.
- [x] Repair bounded fixtures/guards while retaining current accounting and failure evidence checks.
- [x] Run the complete candidate module and adjacent fixed-point comparison tests, reconciling all eight original identities.
- [x] Independently review, update status/gate reports and commit only repair files.

[AGENT] Coordinator owns `tests/test_current_comparison_candidate.py`, this report, attribution and status updates. Protected candidate implementation/evidence are unchanged. Entry commit `eb5e7b1ce`. All eight original failures pass; no test is retired.

## Causes and repair

[AGENT] The original module reproduces eight failures and 79 passes in 0.51 seconds. Three power-account checks compare the retained WI-073 case's semantic fingerprint with the later live package. One manifest check compares the frozen candidate's predicate inventory with predicates added by later modeling. Four failure-injection tests never reach their stubbed native route: the real frozen-input integrity guard refuses changed live input bytes at `inputs/mfe_account_costs_params.json` first. That refusal is correct and is retained.

[AGENT] A module-scoped temporary fixture restores only the candidate's model contract and declared input JSON files from exact base `5fc805015609d8cdc47f00b2f6e16866af6233a2`. Every byte is checked against the retained candidate identity's source hashes; each input file is also checked against its rule hash, and the contract's semantic fingerprint must match. This is a minimal unit-test fixture for still-used guard behavior, not a full package replay or scientific execution. The accounting and manifest checks now join their own candidate contract. Positive baseline accounting must still pass before each one-megawatt mutation must fail the named balance, with unchanged tolerances and equations.

[AGENT] Failure-injection tests retain their explicit synthetic lineage/native stubs and execute the unchanged production adapter against matching frozen input bytes. NaN and both infinities reach the intended result-validation path, retaining raw and tagged canonical failure receipts. A synthetic calculation exception reaches native execution and retains the named error. A new changed-input control proves the input hash guard still refuses before the native route is called. A paired finite-result control reaches completion and retains its canonical receipt. Neither control claims real model execution or physical acceptance.

## Qualification

```bash
bash /tmp/fusion-tea-study-repair-tests.sh -q -ra --tb=short --junitxml=/tmp/20261008-comparison-candidate-suite.xml tests/test_current_comparison_candidate.py tests/test_compare_fixed_point.py
```

[AGENT] Exit 0: **149 passed in 0.79 seconds**, comprising 89 candidate checks and 60 fixed-point comparison checks. All eight original failure IDs pass unchanged. No exclusions, marker filters, skip/expected-failure additions, tolerance relaxation or historical calibration tests. The runner uses the retained runtime and project license with `uv run --no-sync`; temporary archive aliases are removed after completion. Log `/tmp/20261008-comparison-candidate-suite.log`; JUnit `/tmp/20261008-comparison-candidate-suite.xml`.

[AGENT] Both captured test-source hashes and all 202 protected-file hashes match. Production candidate code and records, API/data, model/oracle/generated package and dependencies are unchanged. The thirty other original test functions retain their executable syntax apart from mechanical import ordering. Formatting and `git diff --check` pass. Lint retains four inherited findings (`F401`, two `E402`, `E731`), reduced from 89 with no added diagnostic signatures; no whole-repository lint PASS is claimed.

[AGENT] Joining all four repair receipts against the normalized October 7 inventory accounts for all 172 original failure/error identities: 169 pass, one has its existing expected-failure disposition and two obsolete scoring tests are retired under owner direction. A fresh full-repository qualification and the repository-wide style disposition remain pending. The parallel explorer API-gate work and its separately reported red suite are outside this repair. No PR, push or new modeling acceptance.
