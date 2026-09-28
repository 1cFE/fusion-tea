# Author implementation handoff

Status: completed for the documented bounded contract; independent final evidence acceptance and all ten corrected integration gates pass. No model or parameter edits in this workstream. MR-7 quantity roles and consumers are unchanged.

## Changes

Gate 6 now resolves pipeline references and invokes the existing manifest membership assertion. Gate 7 observes the actual baseline route subprocess from import, checks declared package/source/metadata reads, records actual cached-bytecode and runtime read hashes, and rejects uncovered or changed observed dependencies. The parent requires a structurally valid receipt with a fresh invocation token. Caught violations cannot produce a candidate. A route error with no read violation keeps the baseline producer's `could_not_run` classification.

The receipt's `baseline-read-dependencies/v1` canonical digest binds the exact declared and observed identities and is recorded in gate 7 detail. It is separate from the sealed executable and indicator pin. Runtime and bytecode first-observation hashes are observed identities, not prior-run drift rejection or proof of bytecode/source equivalence. Native reads, directory metadata, TOCTOU, pre-opened handles, environment/network, post-observer execution and unexecuted branches remain explicit limits.

Review should check the bounded implementation refinements recorded in `design.md`: exact teax installation metadata declarations, scratch placement under fresh output TMPDIR, directory metadata exclusion, and atomic output admission only from newly created files to absent destinations. Old output append/read-write and rename-overwrite do not acquire admission.

## Test commands and results

All commands used the prescribed `.codex-test/run` environment. Counts below are successive runs, not additive certification.

- `.codex-test/run python -m pytest tests/study/test_read_coverage.py -q`: `test-attempt-1.txt` retains 20 failed / 3 passed. Corrections: allow write-only integer fdopen used by Python cache creation, and register the new closed-set refusal slug.
- Same command: `test-attempt-2.txt` records 23 passed.
- `.codex-test/run python -m pytest tests/study/test_read_coverage.py tests/study/test_integrate_guide_contract.py tests/study/test_integrate_preconditions.py tests/study/test_integrate_internal_error.py -q`: `test-attempt-3.txt` records 52 passed in 137.20 seconds.
- Same expanded command after additional output/metadata tests: `test-attempt-4.txt` records 56 passed in 139.15 seconds. It started before the final route-error-classification and lifecycle changes. Session 30209 has already been collected (polling returned unknown process ID); the durable log records completion.
- `.codex-test/run python -m pytest tests/study/test_read_coverage.py tests/study/test_integrate_guide_contract.py -q`: final focused run `test-attempt-5.txt` records 40 passed in 13.14 seconds, including clean route exception classification.
- `git diff --check -- scripts/integrate.py scripts/study/read_coverage.py tests/study/test_read_coverage.py tests/study/test_integrate_guide_contract.py docs/integration_seam_operator_guide.md`: passed.

Tests exercise actual undeclared package/route/external reads, symlink escape, mutation before and after reads, bytecode import and cache mutation, sourceless cache refusal, unsupported child/descriptor reads, new/old output handling, atomic rename, stale/missing/malformed/caught-violation receipts, static membership and tooling identity inclusion.

## Real stock baseline probes

Every probe called `scripts.integrate.execute_baseline` under `.codex-test/run python -`, with a `SimpleNamespace` request naming `exploration/stellarator_e2e/studies:study_route.execute_baseline`, `exploration/stellarator_e2e/generated`, `exploration/stellarator_e2e/studies/manifest.json`, its fresh `stock-probe-N` output directory here, and `seam_env()`. This exercises the same route driver used by gate 7; it is not a full ten-gate seam invocation.

Probe 1 refused undeclared `teax_simkit.egg-info/entry_points.txt`; probe 2 refused new temporary scratch outside the output directory; probe 3 refused a directory handle; probe 4 refused an atomic output rename destination. Their `.txt` logs and `read_coverage.json` receipts remain unchanged. Probe 5 completed after the bounded fixes. Probe 6 completed on the final implementation with the dependency digest and corrected route-error handling. Probe outputs and failed-attempt custody remain in this directory.

Probe 6 receipt: `stock-probe-6/read_coverage.json`, outcome pass, 1,571 observed paths and 5,126 exact declarations. Dependency digest `94e0dcb3686fa1256dd8c32b3c4dcdf744c531a1585669bb9f74a72f4e6ca2f7`. Observed categories: 447 sealed artifacts, one package contract, one manifest, 46 declared sources, one dependency metadata file, 468 bytecode files, 606 runtime files, one new output. Sealed package identity is independently recorded in `stock-probe-6/package_identity.json`; baseline results and store are retained alongside it. This is one baseline's evidence, not full-space coverage.

## Remaining work

Fresh reviewer must inspect final code, tests and refinements. Coordinator owns commits, the final exact-checkpoint full integration invocation, final regression selection and goal state. The adapter hashes study tooling and must refresh its synthetic evidence only after this implementation is stable. No published archive or historical integration evidence was edited. No commit, comparison execution, publication, push or merge occurred in this workstream.

## Implementation-review correction

The independent reviewer blocked the first implementation on a reproduced lifecycle bypass (`implementation-review.md`, original probe `/tmp/read-review-9fd7khh9`). The author added real rename, replace, unlink, hardlink, symlink and directory-prefix counterexamples before fixing code. `.codex-test/run python -m pytest tests/study/test_read_coverage.py -k 'admission or descendant' -q` retained 7 failures, 3 passes and 29 deselections in `lifecycle-before-fix.txt`.

Admission now follows current content location and revokes source/destination descendants for moves/deletion. Hardlink creation cannot preserve stale admission. The current stock SQLite route now requires a fresh output database and absent sidecars at first connection; reconnects use only this invocation's admitted store. Thread-local audit recursion suppression prevents unrelated threads from being skipped. These refinements remain pending the same independent reviewer's release.

Successive focused reruns use `.codex-test/run python -m pytest tests/study/test_read_coverage.py tests/study/test_integrate_guide_contract.py -q`: `lifecycle-after-fix.txt` has 49 passes; `lifecycle-sqlite-final.txt` has 52 passes; final `lifecycle-sqlite-sidecars-final.txt` has 55 passes in 19.42 seconds. Counts are not additive. `git diff --check` passes.

Final stock probe 8 completes with the corrected observer and records the newly admitted SQLite store. Receipt: `stock-probe-8/read_coverage.json`; dependency digest `b953bc207be1060cd966f2df099d08fd3a3197389ed690b9e23823a8c22b3cb0`. Probe 7 is also retained but precedes the sidecar check. Earlier successful receipts describe their own tooling bytes and are not promoted as final evidence. Root owns refreshing adapter evidence and the committed full seam after independent release. No further tooling edits are planned before review.

## Final checkpoint checks — 2026-09-20

The continuing independent reviewer released the corrected observer after 55 focused passes and stock-probe-8 receipt verification; tooling is committed at `02925b74`. The first full seam, retained in `integration-final/`, stopped on a stale current-generation test seed selector (one failure and six fixture errors). The reviewer verified the replacement 52-entry inventory and unchanged native checks. That selector correction is committed at `d94f8774`; the historical WI-080 inventory is untouched. `corrected-invocation.json` names the distinct rerun and checkpoint.

The broad `tests/study/test_integrate*.py` selection was interrupted because it repeatedly executes the expensive full seam. Its incomplete dot output and a failure marker remain in `final-regression.txt`; no completed pass total is claimed. `interrupted-regression.json` identifies the retained temporary workspace. Final focused command: `.codex-test/run python -m pytest tests/study/test_read_coverage.py tests/study/test_integrate_guide_contract.py tests/study/test_integrate_preconditions.py tests/study/test_integrate_internal_error.py tests/test_model_evaluation_adapter.py -q`. Result: **96 passed in 162.99 seconds**, recorded in `focused-final-regression.txt`. This count includes the same adapter and read-coverage tests already reported separately; counts must not be added.

Development stock probes 1–8 changed implementation or test setup between attempts; they are retained implementation experiments, not eight identical goal retries. The committed full seam has one corrective rerun. Review submissions retained the original rejection and corrective same-reviewer acceptance. No failed attempt has been relabeled as a successful candidate.

The corrected full seam at `d94f8774` completed as **CANDIDATE, exit 0, all ten gates pass**. `integration-corrected/integration_return.json` records tool-source digest `8ef5c6bdad4c34eb8a89029f74eac3398676bcae64dbd1d341c0537ca568b002`; `read_coverage.json` records baseline dependency digest `002f454aef425be6148c6795b94a45b62102523b206baf94bdd672bc872d078b`. The static manifest membership receipt and dynamic baseline receipt are both present. Verification re-derives every verdict and confirms numerical oracle parity. This is the final executed seam; independent evidence acceptance is recorded in implementation-review.md. The model still has failed engineering checks and scientific coverage limits.

The retained interrupted broad-suite failure was recovered after final acceptance. interrupted-lineage-failure/ contains its exact native return and JUnit: all seven diagnostics identify the same stale seed fixture, before the intended lineage check. Independent review confirms that attribution. The broad suite and its negative-lineage case remain uncertified; this does not add a test pass.
