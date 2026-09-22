# Replay

Use a separate checkout at execution commit `bd9b9aec5fabda5e9a14d53df84f108d52f7f183`, the retained sealed package and source copies, and the licensed runtime described by `results/integration_return_used.json`. Restore the final record-local recovery/report scripts. Never overwrite this frozen record or its original native evidence. Create the same record path in the replay checkout with retained proposals and metadata but without `results/`.

The approved113 proposals contain three integer mode assignments. The original unchanged wrapper completes the native study, then rejects the normalized float representations during export. This failure is expected for this exact frozen source/proposal pair. Inspect the store and ensure113 completed rows/113 attempts with exact full numeric map matches before recovering; do not rerun the evaluator or edit the proposals. Inspect a quiescent, fully checkpointed database with SQLite URI `mode=ro&immutable=1`; opening the original with a normal SQLite/native-store connection can create or remove transient sidecars. The corrected record-local export queries a disposable copy, checks original persistent hashes before/after, and preserves every output and verdict. It requires no live SQLite sidecars; do not remove a nonempty WAL to satisfy that guard.

## Original execution command (one invocation)

```bash
.codex-test/run bash -c 'PYTHONPATH="$PWD:$STOP_PARSER_TEAX_ROOT/packages/teax-simkit" STUDY_REQUIRE_TEAX=1 python -m exploration.aries_integrated.studies.execute_study --record exploration/aries_integrated/studies/20260922-aries-integrated-cost-uncertainty --integration-return work/orchestration/goals/aries-integrated-equipment-costs/evidence/integration-attempt1/integration_return.json'
```

## Successful export recovery command

The same command was invoked twice during this study: the first script version failed on an ephemeral sidecar check; the retained final version succeeds using a disposable copy. Both failures are documented in results/export-failures.txt and the prior recovery script is retained. A fresh replay uses only the final script once after inspecting the completed original store. No evaluation is performed by this command.

```bash
.codex-test/run bash -c 'PYTHONPATH="$PWD:$STOP_PARSER_TEAX_ROOT/packages/teax-simkit" STUDY_REQUIRE_TEAX=1 python exploration/aries_integrated/studies/20260922-aries-integrated-cost-uncertainty/export_stored_results.py'
```

Copy the new preparation/package_identity.json to results/package_identity.json before verification. Copy all three NEW preparation identity/baseline/preflight documents into results/integration; identify other copied integration artifacts as reused from the retained CANDIDATE. The historical preflight must not replace the new study preflight.

## All-point verification and reporting

```bash
.codex-test/run bash -c 'PYTHONPATH="$PWD:$STOP_PARSER_TEAX_ROOT/packages/teax-simkit" STUDY_REQUIRE_TEAX=1 python -m scripts.study.verify --package exploration/aries_integrated/aries_integrated --manifest exploration/aries_integrated/studies/manifest.json --identity exploration/aries_integrated/studies/20260922-aries-integrated-cost-uncertainty/results/package_identity.json --store exploration/aries_integrated/studies/20260922-aries-integrated-cost-uncertainty/results/native/20260922-aries-integrated-cost-uncertainty.db --sample-size 113 --out exploration/aries_integrated/studies/20260922-aries-integrated-cost-uncertainty/results/verification_summary.json'
.codex-test/run python exploration/aries_integrated/studies/20260922-aries-integrated-cost-uncertainty/analyze_results.py
.codex-test/run python exploration/aries_integrated/studies/20260922-aries-integrated-cost-uncertainty/write_readout.py
```

The snapshot/archive is coordinator-owned. The recovered JSON/CSV rows originate entirely from the original native store and evidence artifacts; the recovery is transport repair, not physical glue or substituted calculations.
