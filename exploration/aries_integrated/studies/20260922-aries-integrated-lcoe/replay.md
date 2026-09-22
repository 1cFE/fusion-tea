# Replay

Use an isolated checkout at execution commit `f4ea479506cae17d2a9aafe0f914346c555193e7`, the final retained record-local executor and oracle sources, sealed package and licensed runtime. Restore a fresh copy of this record's complete proposals and preparation metadata without its `results/` directory. Never execute against this frozen record. Package identities and runtime provenance are in results/integration_return_used.json; actual execution commands are also in results/execution-context.json.

## Original execution and verification

```bash
.codex-test/run bash -c 'PYTHONPATH="$PWD:$STOP_PARSER_TEAX_ROOT/packages/teax-simkit" STUDY_REQUIRE_TEAX=1 python exploration/aries_integrated/studies/20260922-aries-integrated-lcoe/execute_study.py --record exploration/aries_integrated/studies/20260922-aries-integrated-lcoe --integration-return work/orchestration/goals/aries-integrated-lcoe/evidence/integration-attempt1/integration_return.json'
.codex-test/run bash -c 'PYTHONPATH="$PWD:$STOP_PARSER_TEAX_ROOT/packages/teax-simkit" STUDY_REQUIRE_TEAX=1 python -m scripts.study.verify --package exploration/aries_integrated/aries_integrated --manifest exploration/aries_integrated/studies/manifest.json --identity exploration/aries_integrated/studies/20260922-aries-integrated-lcoe/results/package_identity.json --store exploration/aries_integrated/studies/20260922-aries-integrated-lcoe/results/native/20260922-aries-integrated-lcoe.db --sample-size 64 --out exploration/aries_integrated/studies/20260922-aries-integrated-lcoe/results/verification_summary.json'
.codex-test/run python exploration/aries_integrated/studies/20260922-aries-integrated-lcoe/analyze_results.py
```

Execution occurred once: 64 completed native cases, 64 distinct started/committed attempts and no retry. Exact full numeric matching and persistent-evidence hash preservation succeeded. There was no export recovery or evaluator rerun. Before verification, copy the new preparation/package_identity.json to results/package_identity.json. Collect retained native integration receipts under results/integration, but use this study's actual new identity/baseline/preflight documents for those three filenames and identify their provenance. The stock all-point verifier consumes the final manifest's channel-specific residual/IDC tolerances.

Preparation replay is in replay-preparation.md. Frozen diagnostics are separate preserved evidence: author stock-runtime refusal attempts plus isolated diagnostic documents/runtime sources in diagnostics/. Do not rerun them as successful study points. The diagnostic baseline matches all 546 available numeric outputs; each retained full document carries 14 predicate records. Negative integrated power blocks integrated LCOE while independent source-comparison arithmetic can remain available. The diagnostic runtime is explicitly distinct from stock StudyRunner.

Reporting-only replay can rerun analyze_results.py against copied native JSON and a quiescent native store. It uses SQLite URI mode=ro&immutable=1, validates 64 complete input maps and single attempts, and never loads an evaluator. Do not delete a nonempty WAL or open the original immutable store through a mutable connection. Snapshot/archive/commit remain coordinator-owned; final record corrections use addenda after freezing.
