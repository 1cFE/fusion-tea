# Study tools and consumers repair — 2026-10-08

[AGENT] **Scoped repair PASS, independently reviewed:** complete `tests/study` run exits zero with 1,863 passed, one existing skip and one existing strict XFAIL in 3,843.04 seconds. A separately collected supplemental regression passes once. All 110 original failed/error nodes reconcile to 109 passes and the one pre-existing expected failure. [Machine attribution and hashed receipts](20261008-study-repair-attribution.json), [independent final review](20261008-study-repair-review.md). The full branch gate remains FAILED; the other 62 recorded October 7 failures and repository-wide style policy are outside this batch.

[OWNER] Requested subagents to fix the first failure group, use agent judgment, ask only when owner judgment is needed and update the report as work proceeds. Source: session instruction on October 8. [INFERRED] Scope is the 86 failures and 24 setup errors under `tests/study/` from the completed October 7 gate. Scoring, model-only guards, codegen acceptance and earlier comparison-candidate test modules remain outside this repair batch.

## Requirements and boundaries

- [NEED] Repair the first study-tools/consumers failure group with delegated work and report progress. Source: owner instruction.
- [INFERRED] Align live consumers with their intended current package, preserve historical tests against explicit historical evidence, and fix actual tool incompatibilities when reproduction proves them. Do not weaken assertions merely to remove failures.
- [INHERITED: CLAUDE.md and session runtime instructions] Use `uv run --no-sync`; preserve `.venv`, source quarantine, native PM and modeling ownership boundaries. No dependency synchronization.
- [INFERRED] Preserve model, oracle, sealed package/study and historical receipt bytes. A required scientific or sealed-evidence change is surfaced with dependent conclusions parked.
- [INFERRED] Verify all originally failing/error study nodes and appropriate neighboring tests. Use focused runs first; after integration run the coherent study suite. A fresh non-author reviewer assesses fixes against these requirements.

## Plan and delegation

- [x] Repair indicator graph/catalog mapping and live declaration/preflight fixture consumers. Owner: graph worker; `scripts/study/indicators.py` and graph/declaration-oriented study tests plus `tests/study/conftest.py`.
- [x] Repair numerical-oracle consumer expectations and current/historical target selection. Owner: oracle worker; domain, financial, primary-loop, major-radius, winding consumer and verification study tests.
- [x] Repair native publication/failure-path and integration environment expectations. Owner: route worker; mechanical-failure, native-publication, integrate-preconditions and read-set-coverage study tests; related source changes only after ownership coordination.
- [x] Integrate worker evidence, rerun original failure/error identities and coherent study suite, obtain independent review, update gate/current work and commit the repair. All authored repair changes and reports ship together in the repair commit.

## Evidence and progress

Entering commit: `582f6f932`. Entering completed-gate receipt: [October 7 inventory](20261007-pre-pr-test-retry.json). Three workers are being assigned separate ownership. No fix or passing rerun is yet claimed. The parent owns this report, shared plan and final integration records; worker-specific notes live beside it.

### Initial diagnosis

Graph worker reproduced a tool defect: catalog constraint IDs retain UA capitalization while pipeline module names lowercase it. The published evaluation channel can identify the actual producer without altering the catalog identity. Numeric worker identified retired magnet aliases, missing MR-7 coverage deltas and an older contingency-cost basis; current expected values will be grounded in reviewed receipts and independent formulas. Route worker found failure-path tests blocked by the shared graph defect, an obsolete “current minus changes” derivation of an 18-predicate historical fixture, and an environment test that removed the explicit TEAx root while leaving its import path available. Workers are repairing within assigned ownership; no scientific or sealed-evidence edits are authorized by these findings.

### Route batch complete and review correction

Route worker passes all four owned modules: 57 tests, including every eleven originally failing node. Mechanical and read-set refusal assertions remain unchanged. [Route report](20261008-study-repair-routes.md). The independent reviewer found the initial graph mapping would accept a numeric producer with matching operand names; the graph worker is adding an explicit constraint-evaluation type guard and adversarial tests before acceptance. Numeric work is still in progress; 119 oracle checks passed in its first bounded batch, with twelve remaining alias/replay details being corrected.

### Bounded regression-fixture improvement

[AGENT] The integration-success fixture's comment promises one invocation shared by eight read-only assertions, but its function scope performs eight identical full-gate invocations. For efficient coherent regression, the parent extracted the unchanged workspace generator into a context manager, retained function-isolated workspaces for refusal/mutation tests, and added a module-isolated success workspace. The success fixture now uses module scope and a module-owned temporary output directory. All eight assertions and package-preservation guards remain unchanged. Independent review and a real success-path execution are required before accepting this test-only improvement.

### Independent graph and fixture checks

Reviewer confirms the strengthened graph join refuses malformed evaluation channels, numeric outputs, missing producers and duplicate producers. Independent adversarial batch passes eight checks. Historical graph tests materialize immutable `d7383342e` bytes and check their pinned digests; generic current tests use the live supplied-design declaration. The workspace scope improvement preserves the original context cleanup and all eight read-only assertions; mutation/refusal fixtures remain function-isolated. No final integrated PASS is claimed while numerical and runtime batches continue.

The legacy single-point CLI test already declared a strict expected failure after its refusal guards. Its setup guard expected an older assessed count; it now checks the complete current catalog count and exact refusal while retaining the eight deviations and anchor checks. This resolves an ERROR to its previously declared XFAIL, not to a passing historical CLI calibration.

### Graph batch complete; numeric final rerun pending

Graph author's final graph/catalog batch passes 86 checks; the reviewer independently passes eight adversarial mapping checks. Export-corrected native/preflight checks pass 31 cases with no environment skips; single-point setup still awaits its final runtime check of the existing expected refusal. Graph report explicitly maps two renamed nodes to their historical targets. Numerical coherent batch has progressed through roughly 475 tests with three failures; subsequent code corrections and additional live fixed-offer/operand assertions require a rerun because that process imported the earlier files. Native stored-result verification is still running. No incomplete batch is promoted to a final passing result.

### Graph acceptance and numeric correction receipts

Graph worker finishes with 86 graph checks passing, 31 exported runtime/preflight checks passing, and the final single-point module yielding five passes plus its pre-existing strict XFAIL. The exact historical CLI refusal, nine anchors and eight deviations are checked before that expected-failure marker. No new skip/xfail marker was introduced. [Graph report](20261008-study-repair-graph.md).

The coherent numeric author batch ended with 503 passed, three failed and one skipped in 419.87 seconds. Two failures were exact historical violated-set assertions encountering later reviewed predicates; their repair preserves exact historical-screen checks and independently checks all current predicates. The winding failure was exact arithmetic reconstruction: a derived density of 118.82716049382721 differed from the retained literal 118.8271604938272. Using that independently cited literal reproduces the historical one-bit rounding behavior without relaxing tolerances. Fourteen final targeted controls pass so far; current offer/operand verification nodes remain in progress. [Numerical report](20261008-study-repair-oracles.md).

### Numerical acceptance and integrated-run preparation

Final numeric targeted batch passes all sixteen checks in 87.85 seconds, closing the three earlier failures and covering the added independent offer/predicate checks. No tolerances were relaxed. The reviewer records a provisional scoped code-review PASS with coherent regression and original-node attribution still pending. Parent fixtures and the production graph tool pass targeted Ruff checks. Numeric author is mechanically formatting touched tests and removing new style debt; exact arithmetic/assertion preservation is required. The seven numeric files had 239 inherited lint diagnostics versus 271 after repair; baseline comparison found 44 added diagnostic signatures, chiefly long lines and import placement. Repository-wide style acceptance remains separate from this study repair.

### Coherent study regression started

Numeric style pass checks seven formatted files and exact executable AST equality excluding imports/docstrings. Residual numeric lint debt is 83 inherited diagnostics versus 239 at entry, with zero added signatures; report and receipts preserve that limit. Independent reviewer verifies the arithmetic and assertions are unchanged after cleanup.

The parent starts the complete `tests/study` suite with TEAx required and the working project key: `bash /tmp/fusion-tea-study-repair-tests.sh -q -ra --tb=short --junitxml=/tmp/20261008-study-suite.xml tests/study`. The helper sources `.venv/integration.env`, uses `uv run --no-sync`, explicitly sets the project license before pytest, and serializes read-only archive aliases. No browser overlay is used. Log: `/tmp/20261008-study-suite.log`; source hashes: `/tmp/20261008-study-suite-source-hashes.json`. No completed-suite verdict is claimed yet.

### Original-case attribution gap closed

The original numerical failure inventory includes eleven public retired-input cases. Ten map directly by unchanged invalid local/value to retired-entry tests; the combined current/density payload initially lacked an identical public rerun. Parent required the exact combined payload rather than silently crediting two separate cases. Numeric author appended one standalone public regression, preserving all existing source definitions and inputs, and independently ran it without nesting the active archive wrapper: one pass in 0.12 seconds. It verifies the exact sorted two-key refusal, precedence before magnitude conversion, and parameter restoration. [Numerical attribution](20261008-study-oracle-node-attribution.json) records the direct replacement and supplemental timing. Reviewer verifies the prior module source matches the coherent run's captured hash after removing only the append. This new test was added after coherent-suite collection and will be credited separately, not included in that suite's test count.

### Historical replay environment prerequisite

Historical graph tests require Git object `d7383342e265f30cac60fba2f6851ebeb3dd0f7b`. The documented plain clone includes it; this checkout is non-shallow and the object is an ancestor of HEAD. Existing model/evolution tests already require older Git objects. There is no pytest/PR checkout workflow to adjust; the lone workflow dispatches visualization notifications. A deliberately shallow clone running focused study tests needs the pinned history made available before pytest. The fixture does not fetch or silently skip. This prerequisite is explicit so a missing-history error is not confused with a model/tool regression.

### Final source and static checks

All twenty changed Python files pass `ruff format --check`. The thirteen non-numeric production/fixture/test files pass `ruff check`; the seven numeric files retain the documented 83 inherited diagnostics with no added signatures. `git diff --check` passes. Independent reviewer confirms all captured source hashes remain unchanged except the approved supplemental function; removing that append recovers the original winding-test source bytes. Protected tracked model, package, study, oracle and work-item paths remain unchanged. The complete study run is still active without reported failures; expensive repeated integration verification is consuming CPU. Its final outcome and original-node reconciliation remain pending.

### Complete regression and original-node reconciliation

The coherent suite finishes with exit zero: **1,863 passed, one skipped, one xfailed, 79 warnings in 3,843.04 seconds (1:04:03)**. The skip is the pre-existing optional proof-of-life store at `exploration/stellarator_e2e/study/_work/availability_sweep.db`; the strict XFAIL is the disclosed historical nine-anchor/twenty-predicate CLI incompatibility. No new skip or XFAIL marker was added. The final formatted source was collected; the only later source addition is the separately tested combined-retired-input function, one pass in 0.12 seconds.

[Original-node attribution](20261008-study-repair-attribution.json) maps every one of the 86 original failures and 24 setup errors to actual collected outcomes or the explicitly separate supplement. The results are 109 passes and one pre-existing XFAIL, with no missing attribution. Retired public-input replacements retain the original input values; historical graph renames bind their explicit historical target. Unchanged node names do not imply unchanged fixture targets; the worker reports explain each reconciliation.

Temporary archive aliases are removed after the coherent wrapper exits. Protected tracked paths remain unchanged. The broader gate has not been rerun and retains its October 7 failed result. The 62 remaining recorded failures are scoring (44), model-only guards (4), codegen (6) and earlier comparison-candidate tests (8). Repository-wide style exceptions remain unaccepted. These are separate remaining branch-gate work, not reopened modeling deliverables.

### Final independent acceptance

Fresh reviewer records scoped PASS after independently parsing the final XML and reconciling all original nodes. All eight shared integration-success assertions pass. The reviewer verifies the four artifact hashes, embedded collected-source hashes, approved supplemental append, protected-path preservation and alias/workspace cleanup. [Final review](20261008-study-repair-review.md). No unresolved scoped finding remains. All repair source and authored reports are committed together; no PR or push is performed.
