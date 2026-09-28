# Independent replacement r2 archive assurance

2026-09-17. Reviewer: `/root/clean_coordinator/r2_review`, fresh non-author. [AGENT] **PASS** for the corrected replacement archive and its bounded reproduction contract. No scientific source reinterpretation, new physical evaluation, production edit, reveal, merge or push occurred. The excluded mixed-source note and barred sources were not opened.

## Archive identity and actual extraction

The final `package/freeze/r2-build-c/comparison-freeze.tar.gz` and `r2-build-d` archive bytes are identical: SHA256 `fa42cb32c1a51989871ba15a3bf2c51ca0a88c9a506b27c8e314c88b42960a21`, **27,470,925 bytes**, **1,498 indexed files** plus the embedded index. Index SHA256 is `d219611a3de4c049ff2365ca94af01639070deaa352210a6936ede9c59a75057`. Membership is unique and consists solely of regular relative files. Every indexed byte was verified, including after extraction. The only `knowledge/holdout/` archive member is its protocol. No excluded mixed-source note, credential/environment filename, runtime import link or cache directory is included.

A separate local clone at `/tmp/r2-independent-review/tree` was checked out at recorded base `fe104e8d9db72e5abf86a29262583ce744f62307`, then overlaid with the actual archive. The extracted builder reproduced the final archive **byte-for-byte**, without new source retrieval or missing assets. Historical r1 remains SHA256 `fdf6e14572f10c9254df1e297394f9eccb0060e3947283ea0f8cf569fc63f533`.

The initial reviewed A/B archive was SHA256 `b5c8ba5107a5b5a1ab72b57a9fcd68abcb5c9c61105d5d256c81e7ca176ddbb5`. The corrected C/D archive differs in exactly `package/freeze-procedure.md` and its embedded index. Code, tests, rules, models and numerical evidence are byte-identical between these candidates. The test results below therefore apply unchanged to final C/D.

## Verification evidence

- The native launcher supplied the pinned interpreter and environment. Subprocesses ran that interpreter with the extracted checkout as cwd and on PYTHONPATH. **97 tests passed**: the two comparison/execution files contribute84; dependency provenance, read-set coverage and reference-profile mapping contribute13. Receipt: `independent-tests.log`.
- Extracted `check_lineage.py` passes at the recorded base, with **12 actual indicator read paths**, two negative read-set guards, source continuity and the sealed executable identity `f52729e684f513d1b210c75f523340085786440fa2828490309b96493755fd14`. Receipt: `independent-lineage.json`.
- Extracted accounting reproduces its retained receipt byte-for-byte: **1,022 equations across73 native cases and219 passthrough aliases**, all passing.
- Both extracted selected-mode checks reproduce their retained receipts byte-for-byte. Each preserves **224/226 scalar agreement,19/20 oracle predicate agreement and20/20 native-operand agreement**. The two scalar misses are current margin and current-margin fraction; the predicate miss is the exact reference-conductor-current boundary. The inventory reserve remains1.0. Adverse native verdicts are preserved.
- Direct SQLite joins verify each completed candidate, requested-input JSON and content-addressed evidence digest. Every artifact's digest matches its filename. Its executable fingerprint, **242 numeric outputs and20 verdicts** agree with the retained native result; report statuses also agree with the response verdicts. These checks inspected actual stores and payloads, rather than trusting custody summaries.
- Both exports and the synthetic reporter reproduce their retained bytes. Each export preserves **174 rows:166 mapped,5 absent producers and3 structural evidence requirements**, all with null reference values and no independent credit. All20 predicates remain present. The Table5 control preserves six fixed conditioned keys and explicit supplied field/volume metadata; those declarations do not add native observed rows.
- A deliberate one-byte addition to the extracted input-rules file causes `sha256sum -c COMPARISON-SHA256SUMS` to fail for that exact path. The original bytes were restored and all indexed files checked again.

Structured verification is retained in `independent-verification.json`. Detailed check logs, reproduced receipts, store-join scratch JSON and the rebuilt archives remain under `/tmp/r2-independent-review/`.

## Interface and resolved finding

The forward interface holds exact profiles0.35/1.2, keeps seven independent keys, retains approximate forward geometry/current defaults, and selects sizing1/reserve1 with live loop/cycle/calendar. The separately grouped Table5 seam supplies its fixed source geometry/current/profile keys and refuses overlapping independent assignments. Export metadata and conditioned reporter rules deny supplied quantities independent prediction credit. Existing missing-input, missing-reference, boundary, source-energy/radiation, conductor/fit and conditional-coolant limits remain explicit. The underlying numerical model/package is unchanged.

One procedure finding was repaired before PASS. Post-reveal step7 originally required the same blind inputs for every conditioned seam, conflicting with the Table5 overlap refusal. The corrected final bytes distinguish general-purpose seams from the dedicated Stellaris Table5 control, show empty `values` and `conditioned_values` for that control, and preserve the refusal. The final archive's only content change is this instruction repair.

During reviewer scratch inspection, opening a WAL-mode database with `mode=ro` created empty WAL/SHM sidecars. An initial scratch rebuild included those additional files. Removing only those reviewer-created sidecars and reopening with `immutable=1` restored exact archive reproduction. Neither candidate archive nor source store was altered. No missing-runtime or archive-membership prerequisite prevented reproduction.

## Limits

This PASS certifies the frozen interface, archive integrity, stored-evidence joins and specified reproduction checks. It does not establish physical feasibility, source ignition equivalence, manufactured hardware qualification or coolant correspondence. The16 native numeric channels outside the226-channel oracle mapping remain outside that independent numerical comparison. Historical integration gates are reused through source/seal continuity; no new physical model run or broad inherited test suite was performed. Pinned wheels and licensed runtime remain external prerequisites. Owner-authorized scientific goal closure is not reopened; reveal remains separately owner-triggered.
