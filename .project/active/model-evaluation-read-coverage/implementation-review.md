# Independent implementation review: baseline file-read coverage

Date: 2026-09-20. Reviewer: continuing non-author integration reviewer. Scope: `scripts/integrate.py`, `scripts/study/read_coverage.py`, `tests/study/test_read_coverage.py`, and the operator-guide diff. No scientific model edits, reference observations or comparison were consulted.

## Verdict

**PASS for final bounded integration acceptance, 2026-09-20.** The corrected committed seam at `d94f8774a64b117207c0419272aa5aadb31e23f7` returns CANDIDATE with all ten gates passing. The reviewer independently reran the 55 focused tests during code review and has now verified the final receipts, source identity and baseline/verification joins. Actual cache hashes/source joins, tool-source identity entries, static manifest reference coverage, receipt token/digest validation and native route-error classification implement the principal approved design decisions. The original output lifecycle blocker is resolved; failed-attempt evidence remains retained. Exact final evidence and remaining limits appear below.

## Reproduced counterexample

Independent subprocess probe at `/tmp/read-review-9fd7khh9` used the actual route driver and observer. The output directory initially contains `old.json` with undeclared old content. The route executes:

```python
(out / 'temp.json').write_text('new')
(out / 'temp.json').rename(out / 'final.json')
(out / 'old.json').rename(out / 'temp.json')
assert (out / 'temp.json').read_text() == 'old untracked content'
```

Observed result: exit 0, receipt outcome `pass`, no violations. The final read is categorized `new-output`. The old contents therefore bypass initial dependency declaration, and the output exception excludes them from final dependency checking. This is a deterministic Python-audited rename sequence, not a concurrent mutation or native-read limitation.

Cause: the `os.rename` branch adds destination admission but never revokes source admission or invalidates destination admission when the incoming source is unadmitted. The `created` set describes paths that were ever created, not paths still containing this invocation's new output.

Required correction: make output admission follow the lifecycle of admitted contents. Revoke moved-away source admission and invalidate a destination when unadmitted contents replace it. Account for deletion/recreation and equivalent hardlink/symlink replacement paths, or conservatively refuse unsupported mutations. Preserve the successful fresh atomic-output route. Keep negative tests using real opens and rename operations for the reproduced sequence and related replacement paths.

## Remaining acceptance

After the correction, independently recheck the focused tests and final code. The reported author focused passes and stock baseline success do not exercise this counterexample. The coordinator's expanded regression result and full committed seam remain required evidence; this review has not independently certified either. The committed seam must identify the final observer tooling bytes.

The observer remains a cooperative baseline Python-open check with the documented native C/SQLite, directory metadata, pre-opened handle, environment/network, unexecuted branch and TOCTOU limits. No whole-design-space or universal filesystem guarantee follows. MR-7 remains compliant for the reviewed tooling-only diff; no physical equations, supplied choices or cost bindings change.

## Resolution and independent recheck — 2026-09-20

The author corrected admission to follow the current file lifecycle. Rename revokes source and destination admission, including descendants for directory moves; only an admitted regular source moving to an absent permitted output destination transfers admission. Removal revokes admission. Hardlink/symlink events invalidate destination admission and cannot turn old contents into new output. Symlink reads classify the resolved target. Failed mutations conservatively revoke admission because audit events precede the syscall. Creation-attempt evidence is now separate from current admission.

The reproduced sequence is covered by the real subprocess rename test, with sibling tests for replace, hardlink, symlink, unlink and directory moves. Fresh atomic output and genuine deletion/recreation still pass. The author retained seven failing counterexamples before the fix in `lifecycle-before-fix.txt`; these were useful negative evidence, not passing certification.

Independent command: `.codex-test/run python -m pytest tests/study/test_read_coverage.py tests/study/test_integrate_guide_contract.py -q`. Result: **55 passed in 19.29 seconds**. This includes the original bypass and its related mutation cases, cached imports, actual undeclared/changed reads, and integration receipt/refusal cases. No full suite was rerun by this reviewer.

Inspection also confirms thread-local recursion suppression, so one thread's internal hashing does not intentionally suppress another thread's audit events. This is code inspection, not a concurrency stress certification. SQLite connection admission now requires an absent database and absent known sidecars under the invocation output root; an existing or replaced store refuses, and newly admitted stores may reconnect. These checks constrain stock store reuse; native SQLite content reads and arbitrary native SQL access remain outside observation as stated in the receipt.

The reviewer loaded `stock-probe-8/read_coverage.json`, independently recomputed its canonical dependency digest and validated its structure/token/outcome with the current validator. Result: valid, digest `b953bc207be1060cd966f2df099d08fd3a3197389ed690b9e23823a8c22b3cb0`. Its declared hashes for `scripts/study/read_coverage.py` and `scripts/integrate.py` match the current files. Its admitted SQLite store is the fresh stock-probe-8 baseline store. This receipt establishes that baseline probe, not completion of all ten integration gates.

The `validation-summary.md` correction section faithfully distinguishes successive test runs and final probe 8 from earlier failed and superseded attempts. The observer's dependency digest identifies declarations and observed bytes separately from the executable seal and manifest pin. Broad runtime declarations, first-observation bytecode identities, TOCTOU windows and post-observer execution retain their stated limits. No unresolved code blocker remains within that bounded contract.

**Release:** coordinator may commit the corrected tooling and run the full seam at that exact checkpoint. Final goal acceptance still requires that committed seam and refreshed dependent adapter evidence. Earlier tool identities and receipts must remain attributed to their original attempts.

## Current regression fixture correction — 2026-09-20

**PASS for the narrow correction and a fresh committed seam attempt.** The full seam at `02925b74` failed before reaching read observation: retained `integration-final/junit/model-family-spine.xml` records one failure and six fixture errors, each with the old normative REBCO seed hash rejection. This is not evidence that the later gates passed.

The reviewer inspected the corrective diff in `tests/models/current_mfe_regressions.py` and `work/analysis/model-evaluation-diagnostics/change.md`, the WI-080 wrapper and the native WI-040 recipe. The helper now returns that same native recipe with the diagnostic repair's explicit seed manifest. It does not weaken inventory equality, reject-symlink/hash checks, fresh-destination checks or post-generation seed preservation. Returning the native recipe also ensures its generation function reads the selected seed manifest; setting an attribute on the old wrapper alone would not change the recipe constructed inside its wrapper call.

Independent read-only Python checks found 52 old and 52 corrected seed entries, exactly the two changes recorded in `seed-delta.json`, and all 52 corrected hashes matching their current generated bodies. The affected entries are the reviewed REBCO diagnostic body and primary-loop domain guard. The imported helper selects the retained WI-040 recipe, exposes the expected inventory/generation functions and points to the diagnostic seed file. No historical seed receipt, test assertion or scientific body changes in this narrow diff.

The failed seam is retained separately. Approval here is for the fixture correction, not retroactive acceptance of that failed attempt. Commit the correction and rerun the full seam into a fresh evidence directory. Final integration acceptance remains pending its result.

## Final committed integration evidence acceptance — 2026-09-20

**PASS for the scoped Python baseline read-identity gate.** Reviewed `corrected-invocation.json`, `corrected-integration.log`, and `integration-corrected/` at checkpoint `d94f8774a64b117207c0419272aa5aadb31e23f7`. The invocation command matches the returned command exactly. The return is CANDIDATE, exit 0, no blocker, all ten gates pass. JUnit evidence records three dependency-provenance passes and thirteen model-family-spine passes with no failures, errors or skips. The initial failed `integration-final/` attempt remains a separate record.

The reviewer independently hashed all seven tool-source files from the named git checkpoint, checked them against the return, and recomputed the current source digest: `8ef5c6bdad4c34eb8a89029f74eac3398676bcae64dbd1d341c0537ca568b002`. The observer and indicator parser are included. No test rerun was needed after this identity check; the independent 55-test run above remains the code-review evidence.

The actual dynamic receipt validates with a successful outcome, no violations and dependency digest `002f454aef425be6148c6795b94a45b62102523b206baf94bdd672bc872d078b`, which matches Gate 7 detail. It contains 5,126 declarations and 1,293 observed paths: 447 sealed package artifacts, one package contract, one manifest, 46 declared sources, one dependency metadata file, 190 bytecode files, 606 runtime files and one new output. The reviewer recomputed the digest and validated the receipt structure. Gate 6's static receipt exactly matches independently re-resolved pipeline references plus model contract; the reviewer reran the membership assertion and manifest pin recomputation successfully. The originally missing integration assertion is now executed, and the dynamic claim is supported for this baseline.

Executable identity `83ea3b6cf99f5fda6045e7e03b5d430ede91abbe8aa41262c2f9f5aba8663d23` agrees across candidate, package identity, baseline and verification. Semantic identity is `6f51a9963348754694563855957d9bf9bfdfb90c61bd9228c9bd8868286fac90`; manifest pin is `b60bcb940398d1df39bf779394ebab46ea309e31e8c00034d3dedee39832c9d3`. Preflight input hashes match the deposited baseline and identity documents; all six preflight checks pass. The retained executed store exists. Verification passes 112 mapped channel checks and rederives all 67 constraints with no verdict mismatch or listed unverified constraint; worst relative channel deviation is `2.409591420195442e-15`. This is the verifier's selected mapping, not a claim that every model output was independently checked here.

Final focused regression evidence records 96 passes in 162.99 seconds for the named read-coverage, integration guide/preconditions/internal-error and adapter selection in `validation-summary.md`. That reported completed run is distinct from the reviewer's 55-test rerun; their overlapping counts must not be summed. The broad `test_integrate*.py` run was interrupted with exit 130 and a partial failure marker, subsequently identified below as the corrected stale fixture, as retained in `interrupted-regression.json` and `final-regression.txt`; no completed broad-suite total or broad-suite PASS is certified. The separately completed focused selection and exact-checkpoint full seam supply the bounded acceptance evidence.

**Limits remain:** native C/SQLite content reads, directory metadata, mmap/direct syscalls, pre-opened handles, environment/network reads and execution after observer deactivation are outside observation. Runtime and bytecode first-observation hashes record those bytes; they do not attest the runtime installation, reject all prior-run drift or prove bytecode/source equivalence. Concurrent/transient mutation windows remain. Unexecuted branches and other design points are untested by this receipt. This is a cooperative baseline check, not universal file-read coverage or a sandbox. Stock verification still reports its teax revision as unrecorded; the seam independently records the expected revision, without silently repairing that verifier field.

Passing tooling gates does not establish plant feasibility: the baseline has 61 satisfied and six violated predicates (divertor heat, facility occupancy, reference conductor current, breeding, water electrical capacity and winding-pack fit). This tooling/fixture work remains MR-7 compliant because it changes no supplied design, physical relationship, selection policy or cost consumer. No reference comparison, empirical extension or publication is approved by this review. The committed-seam condition for this read-coverage workstream is discharged; adapter and overall readiness judgments remain in their respective independent reviews.

## Recovered interrupted-run failure — 2026-09-20

The reviewer inspected `interrupted-lineage-failure/integration_return.json` and its retained `junit/model-family-spine.xml`, and verified both against their recorded SHA256 hashes and the original temporary files. The native return stops at model-family-spine. All six fixture errors and one failure name the same mismatched normative REBCO seed as the independently corrected stale fixture. The negative-lineage test therefore stopped before reaching its intended lineage assertion. This identifies the partial failure's cause; it does not certify that negative test or the interrupted broad suite. Final bounded acceptance and its limits are unchanged.
