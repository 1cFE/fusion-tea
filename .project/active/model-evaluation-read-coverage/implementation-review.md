# Independent implementation review: baseline file-read coverage

Date: 2026-09-20. Reviewer: continuing non-author integration reviewer. Scope: `scripts/integrate.py`, `scripts/study/read_coverage.py`, `tests/study/test_read_coverage.py`, and the operator-guide diff. No scientific model edits, reference observations or comparison were consulted.

## Verdict

**PASS for code acceptance after correction, 2026-09-20. Full committed integration seam remains pending.** The reviewer independently reran the 55 focused tests on the corrected implementation and checked the final stock receipt against the current observer and integration source bytes. Actual cache hashes/source joins, tool-source identity entries, static manifest reference coverage, receipt token/digest validation and native route-error classification implement the principal approved design decisions. The original output lifecycle blocker below is resolved; its failed-attempt evidence remains retained.

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
