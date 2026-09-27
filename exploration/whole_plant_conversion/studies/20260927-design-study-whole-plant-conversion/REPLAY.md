# Replay this study

Use the sealed record as the authority for the 2,496 complete input points. The replay command creates a fresh native store through the same `execute_study` and `StudyRunner` lifecycle, runs the stock independent verifier on every case, and compares the replayed inputs, outputs, predicates, states, and executable identity exactly with the original cases. Candidate identifiers and store paths belong to the new run.

## Required checkout and runtime

Use a checkout whose generated package and executable study sources match this record. `sealed-package.tar.gz` contains the generated `whole_plant_conversion_tea` directory. `results/sources/` retains the study, oracle, tool, model, and supporting source files under their original repository paths. `snapshot.json` records the archive and source hashes, package fingerprints, manifest, tool revisions, and original execution commit. If the working tree has advanced, restore the recorded files in a separate checkout before replaying. Preserve this sealed record.

The current sealed runtime is selected by `.codex-test/run`. It sources the established license and integration environment, selects the existing `.venv`, and disables environment synchronization. The command below adds the repository and the sealed TEAx simkit source directory to `PYTHONPATH`. A different machine needs an equivalent licensed runtime and the recorded dependencies; the record does not contain credentials or dependency installers.

## Check replay inputs

Run from the repository root. This command checks the released snapshot, every declared artifact hash, the original proposal hash, complete-point identities, live executable source hashes, archive/live package byte equality, strict-loader fingerprints, indicator pin, and the selected TEAx revision. It does not create the replay directory or evaluate study points. The source record must have its final `snapshot.json` before this check can pass.

```bash
.codex-test/run bash -c 'PYTHONPATH="$PWD:$STOP_PARSER_TEAX_ROOT/packages/teax-simkit" python -m exploration.whole_plant_conversion.studies.replay --record exploration/whole_plant_conversion/studies/20260927-design-study-whole-plant-conversion --out exploration/whole_plant_conversion/studies/replay-whole-plant-001 --check-only'
```

## Execute and verify all points

Use a fresh repository-local output path. The command refuses an existing directory, a directory inside the sealed record, or a directory containing the sealed record. It copies the frozen proposals and supporting interpretation metadata, executes all points, and sets the stock verifier's sample size to the complete case count. This repeats the full native study and verification workload.

```bash
.codex-test/run bash -c 'PYTHONPATH="$PWD:$STOP_PARSER_TEAX_ROOT/packages/teax-simkit" python -m exploration.whole_plant_conversion.studies.replay --record exploration/whole_plant_conversion/studies/20260927-design-study-whole-plant-conversion --out exploration/whole_plant_conversion/studies/replay-whole-plant-001'
```

A successful run writes `replay-summary.json`, `results/cases.json`, a new store under `results/native/`, and `results/verification_summary.json` in the replay directory. `verification.log` retains the stock verifier output. The command also rechecks that every original sealed artifact and the original snapshot stayed unchanged. A failure keeps the new evidence for inspection; retry with another fresh path after resolving the cause.

## Rebuild presentation separately

To reproduce tables and plots from the sealed native cases, render into a different fresh directory. This command reads the sealed evidence and does not execute the model or change the study record.

```bash
.codex-test/run bash -c 'PYTHONPATH="$PWD:$STOP_PARSER_TEAX_ROOT/packages/teax-simkit" python -m exploration.whole_plant_conversion.studies.report_results --record exploration/whole_plant_conversion/studies/20260927-design-study-whole-plant-conversion --out exploration/whole_plant_conversion/studies/render-whole-plant-001'
```

Replay verifies the numerical evidence and declared comparisons. The recorded supplied-source, nuclear heating, finite-catalog, and qualification limits continue to apply.
