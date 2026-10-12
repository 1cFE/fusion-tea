# Plant-closure validation investigation

The 120 original failures reduce to seven demonstrated causes. The repaired and pruned battery has **130 passes / zero failures**, down from 250 to 130 cases. Eight older writers now reject invalid published values, and the plant writer validates all native rows before opening its target. No test is skipped, marked xfail, or given regenerated numerical expectations.

**All nine production writer repairs are applied**, authorized by the owner's “yes, proceed” after the frozen-code boundary question. The [repair patch](evidence/publication-repair.patch) and its 38 passing preparatory synthetic checks are retained. Original code copies and hashes are under `evidence/original-code/` and `evidence/original-code-sha256.json`. Original failure evidence and code copies pass the [preservation check](evidence/preservation-check.json). This task changed no runtime, model, generated package, frozen result, domain source or goal state. A concurrent financial merge changed the generated package during validation; its separately owned changes were preserved.

## Complete accounting

[Failure mapping CSV](failure-mapping.csv) and [JSON](failure-mapping.json) contain exactly 120 unique original test IDs, their cause, disposition and replacement tests. The original logs establish the first failing operation for every member; `broad.xml` independently contains the same 97 historical failures. Matching names was used only for accounting. The corrected fixtures and native publication probes establish the diagnoses below.

| Group | Original failures | Actual first failure | Diagnosis and disposition |
|---|---:|---|---|
| G1 | 20 | Stress-fence and sustainment-fence exports do not raise | Production writers used `outputs.get()` and published blanks/NaN/infinities. Consolidate the ten-case matrix per writer to three later-case checks. Six replacement checks pass after fixing production. |
| G2 | 22 | Priced-levers and first wall-and-heating exports require `arms, path` | Broken fixture concealed the same production defect. Supply the actual arm map. Both complete-value checks now pass; six invalid-value checks pass after fixing production. |
| G3 | 44 | Second wall-and-heating, stored-energy, burn-control and minor-radius exports require `arms, oracle, path` | Broken fixture omitted arm/oracle data and initialized run context. Repair that context without running an oracle. Four complete-value checks pass; twelve invalid-value checks pass after fixing the same production defect. |
| G4 | 11 | Model-owned-radius definition has `channels()`, not `CHANNELS` | Obsolete fixture API. Its actual execution script builds and validates all rows before calling the writer. Replace with native publication checks: three refusal cases and a value/identity case all pass. |
| G5 | 11 | Operating-heating definition has `labelled_proposals()`, not `proposals()` | Obsolete fixture API. Actual execution also joins proposal IDs to persisted candidate IDs before validating rows. Replace with native publication checks: all four pass. |
| G6 | 11 | Plant definition has `channels()`, not `CHANNELS` | Obsolete fixture API concealed a production publication defect. Actual writer opened the target before validating cases. Replace with native publication checks: positive and three refusal/preservation cases all pass after fixing production. |
| G7 | 1 | Trail contains `work/narratives/` | Obsolete text prohibition. The cited trail records an earlier test failure concerning a narrative; it does not adopt that narrative as goal authority. Delete the test. |

G1–G3 protect an economically consequential result: a supposedly complete CSV must not contain a missing or invalid required scalar. All eight writer bodies were exercised with complete synthetic values and with absent, null and NaN fuel values. Before the fix, they accepted the invalid data; the applied repair rejects it before publication. The original first/later and signed-infinity variants follow the same unconditional `.get()` assignment; there is no per-value branch in that assignment. The repaired fixture's positive controls pass every writer's declared channel values, including zero.

G2 and G3 are not diagnosed from their TypeErrors alone. The fixture now supplies the exporter's arm map and, where required, oracle operands, calibration, baseline magnet and empty historical joins. The minor-radius fixture satisfies its stored-energy/casing consistency relations; the stored-energy and burn-control fixtures satisfy their thermal-energy relation. Those are synthetic publication inputs, not assertions about scientific truth. An initial fixture error using an unavailable `MU0` constant was corrected; the failed attempt is retained. Refusal checks still demand the offending channel in the error and preserve the prior CSV bytes, so an unrelated precondition error cannot count as a pass.

**Supported-workflow scope:** the current route accepts persisted cases for export, and the minor-radius study explicitly provides `run_export_only`. These public writer functions remain callable and have not been retired. Their input-to-CSV defect is demonstrated without model execution. A fresh replay of their older proposal sets against today's package is not certified: several use retired inputs such as `availability`, `p_input`, or independent magnet radius. The retained checks protect publication/re-export, not a promise that historical sweeps run on the latest package. There is no evidence justifying deletion of the invalid-value protection merely because the producing study is old.

The execution wrapper in `studies/study_route.py` checks declared required channels before successful persistence and on resume. Before the fix, eight older `run()` functions did not declare their extended `CHANNELS`, so that wrapper only protected the route's default subset. Their local exporters must still validate every declared value. The applied patch both passes the full map to `run_points` and replaces `.get()` publication with `required_outputs`. Nonfinite results remain persisted and are refused at export, preserving the owner's 2026-09-05 rule in `.project/research/20260905_numeric-evidence-fix.md`.

## The eleven plant failures

`20260912-plant-closure/study.py` supplies proposals, a channel map through `channels()`, and `run()`. `execution/execute.py` owns publication. No supported lifecycle contract requires a constant called `CHANNELS` or a function called `export`; neither is added.

The actual publication section calls `required_outputs`, so it rejects absent, null and nonfinite values. **It rejects them too late.** It opens `native-points.csv` in write mode and emits the header before checking the first case. A bad first case leaves a header-only file. A bad later case leaves the preceding apparently successful rows. A pre-existing labelled `points.csv` remains unchanged alongside the newly truncated native file. A fresh directory gains the partial native file and no labelled file.

[Plant invalid-value matrix](evidence/plant-invalid-matrix.json) exercises all five forms (absent, null, NaN, positive and negative infinity), first and later cases, with and without previous files: 20 observations. Every invalid value raises, but every attempt leaves a misleading partial native artifact. The execution summary is also written before publication and only reports completed execution states; it does not attest complete publication. Prior verification artifacts are not invalidated by this failed attempt. No new successful verification certificate is produced by the probed publication section.

The native tests compile the **unchanged publication sections of the actual scripts** and supply synthetic returned cases. This avoids invoking import-time model execution or writing into a frozen directory. It certifies those sections, not a full execution-script run. Radius and operating-heating build all rows before writing; both pass identical invalid-value tests. Their execution-time case dumps remain diagnostic evidence, distinct from successful points publication.

The applied plant repair validates and constructs every native row before opening its target, using the existing route writer. It also labels the execution summary's publication state `pending`, setting it to `complete` only at the end. Its existing catalogue/headline assertions become explicit errors. This prevents the demonstrated invalid-value partial publication; it does not claim multi-file atomicity for disk failures or process interruption.

## Retention and pruning

- **Local exporter matrix: 154 → 44 cases.** Eleven direct exporters retain complete-value preservation and three invalid-value checks each. Three native scripts move to their actual publication paths. Remove redundant first-versus-later and positive-versus-negative-infinity multiplication across writers. Later-case checks catch partial-validation errors; the shared validator separately retains all five invalid-value forms.
- **Native publication: 12 cases**, covering each script's values/candidate identity and absent/null/NaN rejection before replacing evidence. Add **five shared validator cases** for the full invalid-value family.
- **Goal-document checks: 29 → 2 cases.** Retain ADR register/provenance/promotion-link integrity and narrative evidence-link resolution. Delete exact heading order, stage-name matrices, phrase presence/absence, paragraph/line limits, required sample slugs and the narrative-path prohibition. These asserted editorial form without proving agent behavior or authority. Historical goal documents remain untouched.
- **Record and numeric-evidence tests retained unchanged.** They protect record joins, stores and arm references, missing comparisons, persisted numerical values, execution-failure evidence, resume validation and avoiding re-evaluation for presentation-only changes. This investigation does not certify broader model tests outside the focused failure census.

Protection lost: automated notices of prose/layout drift, plus repeated invalid-value permutations at every writer. That tradeoff is acceptable because phrase matching does not establish correct interpretation, while the shared numeric validator and later-case integration checks preserve the substantive invalid-publication risk. Native section tests do not cover all execution-script setup or multi-file interruption behavior; those limits remain explicit. No numerical calculation or package/result identity assertion was relaxed to obtain a pass.

## Validation and limits

All Python used `.codex-test/run`; no dependency installation, synchronization, sweep, quarantined source access or frozen-store mutation occurred. The pre-repair retained run reported 103 passed / 27 failed; its logs remain intact. The first applied run reported 129 passed / one failure because the concurrent financial merge `bc75b11d` changed the executable fingerprint during a resume test. The bound fingerprint `cbdb2a36…` exactly matches `HEAD^1`'s seal, and the attempted reopen fingerprint `1a7c216d…` exactly matches the merge's seal. The store correctly rejected that identity change. No assertion was relaxed. The numeric module then passed all 16 tests, and the final entire retained battery passed all 130 tests against the merged package.

Exact final command:

```bash
.codex-test/run python -m pytest tests/study/test_records.py tests/study/test_numeric_evidence.py tests/study/test_study_publication_fail_closed.py tests/study/test_native_publication.py tests/orchestration/test_goal_contract.py -q --tb=short --junitxml=.project/active/plant-closure-validation/evidence/final.xml
```

Final evidence: `evidence/final.log` and `evidence/final.xml`. The applied run interrupted by the changing package remains at `evidence/applied.log` / `applied.xml`. Its numeric follow-up used `.codex-test/run python -m pytest tests/study/test_numeric_evidence.py -q --tb=short --junitxml=.project/active/plant-closure-validation/evidence/numeric-after-merge.xml` and is recorded beside it.

Diagnostic commands used before applying repairs:

```bash
.codex-test/run python -m pytest tests/study/test_study_publication_fail_closed.py -q --tb=short
.codex-test/run python -m pytest tests/study/test_study_publication_fail_closed.py -q -k 20260904 --tb=short
.codex-test/run python -m pytest tests/study/test_native_publication.py -q --tb=short
.codex-test/run python .project/active/plant-closure-validation/evidence/check_proposed_repair.py
```

The pre-repair entire retained run used the final command with `evidence/retained.xml`; logs include `repaired-fixture.log`, `wall-fixture.log`, `native-publication-before.log`, and `retained.log`. The stricter publication-only follow-up reported 44 passed / 27 failed in `final-publication.log`. All original attempts remain evidence, including the corrected test collection and fixture errors.

There are no remaining blockers for these bounded publication repairs. This result does not certify historical sweeps against today's package, the scientific limitations in the consolidated plant grade, or multi-file atomicity under disk failure/process interruption. No compatibility symbols, model sweep or expected-value regeneration were added. Production, test and document whitespace checks pass. Raw failure logs, XML excerpts and patch context retain their original whitespace.
