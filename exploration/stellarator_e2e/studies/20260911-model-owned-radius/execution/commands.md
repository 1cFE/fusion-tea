# Execution and check commands

All Python invocations used `.codex-test/run`. Commands needing TEAx or repository imports used the following documented launcher configuration; no installation, synchronization or runtime mutation occurred:

```bash
.codex-test/run bash -c 'export PYTHONPATH="$PWD:$STOP_PARSER_TEAX_ROOT/packages/teax-simkit" STUDY_REQUIRE_TEAX=1; python COMMAND'
```

The launcher-selected runtime and repository identities are in results/runtime.json. Paths below are relative to this record unless shown repository-relative. Logs retain the original successful and failed attempts. Command outcomes do not certify physical validity.

| Stage | Command after launcher/configuration | Outcome and evidence |
|---|---|---|
| Explicit basis capture | `python exploration/stellarator_e2e/studies/20260911-model-owned-radius/preparation/capture.py` | Success; 29 initially copied explicit paths, context/provenance.json. No generic preservation scan. |
| Native indicators | `python scripts/study/indicators.py --package exploration/stellarator_e2e/generated --manifest exploration/stellarator_e2e/studies/manifest.json --groups exploration/stellarator_e2e/studies/20260911-model-owned-radius/axes.json --out exploration/stellarator_e2e/studies/20260911-model-owned-radius/indicators.json` | Success before review/points; 13/18 constraints, 14/14 objectives. |
| Record opening | `python exploration/stellarator_e2e/studies/20260911-model-owned-radius/preparation/open-record.py` | Success before points. |
| Fresh pre-execution review | Native `spawn_agent`, task `/root/pre_execution_critique`, `fork_turns=none`; later follow-up for deposited schema inspection | Positive after objective F1/F2 dispositions; reviews/pre-execution-review.md. |
| Preparatory baseline and native preflight | `python exploration/stellarator_e2e/studies/20260911-model-owned-radius/execution/baseline.py` | Exit 0; baseline-attempt-1.log; complete direct native evidence, no store; all six gates pass. |
| Oracle scan and window freeze | `python exploration/stellarator_e2e/studies/20260911-model-owned-radius/execution/scan.py` | Exit 0; scan-attempt-1.log. Seven finite points retained before ordinary native execution. |
| One native lifecycle study | `python exploration/stellarator_e2e/studies/20260911-model-owned-radius/execution/execute.py` | Exit 0; study-attempt-1.log. Seven completed cases in one store. |
| Every oracle channel, verdict, frozen control and analytic ratio | `python exploration/stellarator_e2e/studies/20260911-model-owned-radius/execution/verify-all.py` | Exit 0; verify-all-attempt-1.log and complete result ledgers. |
| Native verification | `python scripts/study/verify.py --package exploration/stellarator_e2e/generated --manifest exploration/stellarator_e2e/studies/manifest.json --identity exploration/stellarator_e2e/studies/20260911-model-owned-radius/results/package_identity.json --store exploration/stellarator_e2e/studies/20260911-model-owned-radius/results/store/20260911-model-owned-radius.db --sample-size 7 --out exploration/stellarator_e2e/studies/20260911-model-owned-radius/results/verification_summary.json` | Exit 0; native-verification-attempt-1.log; all seven sampled, 25 generic channels, all eighteen verdicts rederived. |
| Support capture/fixed-input checks | `python exploration/stellarator_e2e/studies/20260911-model-owned-radius/execution/capture-support.py` | Exit 0; capture-support.log. Forty explicit copied artifacts and all effective input groups checked. |
| Report attempt 1 | `.codex-test/run python exploration/stellarator_e2e/studies/20260911-model-owned-radius/execution/report.py` | Exit 1; report-attempt-1.log. Missing repository PYTHONPATH caused ModuleNotFoundError before report execution. No model or numeric evidence changed. |
| Report attempt 2 | Configured launcher, `python exploration/stellarator_e2e/studies/20260911-model-owned-radius/execution/report.py` | Exit 0; report-attempt-2.log. Invocation corrected only; same script and native numerical evidence. |
| Record-specific publication checks | `python exploration/stellarator_e2e/studies/20260911-model-owned-radius/execution/publication-check.py` | Exit 0; publication-check.log. 478 synthetic damaged-copy controls; no model/store execution. |
| Current native publication checks | `python -m pytest tests/study/test_study_publication_fail_closed.py::test_export_resolves_an_opaque_constraint_id_through_the_catalog tests/study/test_study_publication_fail_closed.py::test_export_refuses_incomplete_or_unknown_case_data_without_replacing_csv -q` | Exit 0; native-publication-tests.log. Six pass; no historical local-study parametrizations or native model execution. |
| Diagnostic index | `python exploration/stellarator_e2e/studies/20260911-model-owned-radius/execution/diagnostic-summary.py` | Exit 0; diagnostic-summary.log. Retained evidence indexed, not rerun. |
| Fresh final review | Native `spawn_agent`, task `/root/final_study_critique`, `fork_turns=none` | Review and subsequent dispositions in reviews/. No synthesis or model execution authorized. |

Read-only file/JSON inspection and source-revision queries also used the launcher when Python was involved. The directory's scripts are task-local evidence builders/checkers, not changes to current study consumers or shared tools. There was one failed reporting invocation and no failed numerical study attempt. This does not overwrite historical failed attempts, which remain in copied certificates and their original homes.

Final publication steps (no model re-execution):

- `.codex-test/run python exploration/stellarator_e2e/studies/20260911-model-owned-radius/execution/finalize.py` resolves metadata, records review dispositions and appends only this record's six discovery rows. It is idempotent for registration; repeated metadata refresh incorporates later check receipts without altering numerical evidence.
- Configured launcher: `python -m pytest tests/study/test_records.py -k 20260911-model-owned-radius -q -o cache_dir=exploration/stellarator_e2e/studies/20260911-model-owned-radius/execution/pytest-cache`. Three native record checks pass; all 37 other parametrizations are deselected. Evidence: native-record-tests.log.
- `.codex-test/run python exploration/stellarator_e2e/studies/20260911-model-owned-radius/execution/validate-record.py` checks fixed headings, resolved fingerprints, every inventoried digest, numerical result inventory completeness, store identity and copied-source provenance. Evidence: record-validation.log. A final read-only rerun verifies the snapshot after that receipt is included.

The finalized executor record is intentionally uncommitted. The parent owns the single freeze commit and the separate administrator dispatch. No goal/CURRENT_WORK, model/package/current-consumer/shared-tool, historical-study or source artifact was authored or changed by this task. Only this new record and its appended native discovery rows are deliverables.
