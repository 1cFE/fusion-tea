# Replay the final thermal comparison

The native record is `exploration/exchanger_architecture/thermal_requirements/studies/20260927-exchanger-thermal-comparison-b/`. Its snapshot pins the executable, all input maps, stored outputs, oracle, tools and source bytes. The previous failed record is preserved separately; use the `-b` record for completed results.

## Exact native replay

From the repository root, with this worktree's documented runtime and pinned TEAx checkout, choose a destination that does not exist:

```bash
.codex-test/run bash -c 'PYTHONPATH="$PWD:$STOP_PARSER_TEAX_ROOT/packages/teax-simkit" python work/orchestration/goals/design-study-exchanger-architecture/evidence/r4-replay-native.py --destination /tmp/exchanger-thermal-delivery-replay'
```

This executes a fresh baseline and all 1,277 exact input maps through the stock native route, then compares inputs, every stored output, every verdict, execution state and executable fingerprint exactly. It writes `replay-comparison.json` under the new destination and never writes into the sealed record. A different destination is required for another run. The script checks the live package is clean and matches the sealed integration identity; it fails if the package has moved. The record's `sealed-package.tar.gz` and `results/sources/` retain the exact executable and supporting code for restoration into a separate compatible checkout.

## Independent verification

The exact command used for all-point verification is retained in the record's `results/execution-context.json`, with tool/source digests and sampling evidence in `snapshot.json` and `results/verification_summary.json`. To repeat verification without modifying the sealed record, change only `--out` to a fresh path under `/tmp`. Use `--sample-size 1277` to cover the complete store. Numerical verification compares 435 channels and re-derives all 35 predicates; it is separate from exact replay of every stored output.

## Recreate figures and tables

```bash
.codex-test/run python work/orchestration/goals/design-study-exchanger-architecture/evidence/r3-render-results.py --record exploration/exchanger_architecture/thermal_requirements/studies/20260927-exchanger-thermal-comparison-b --verification exploration/exchanger_architecture/thermal_requirements/studies/20260927-exchanger-thermal-comparison-b/results/verification_summary.json --out /tmp/exchanger-thermal-report-replay
```

The renderer reads verified stored results and their parent identities. It performs no new plant evaluations. Historical `r3-` filenames are retained, while the content explicitly identifies Round 4. The sealed record includes a standalone copy of the renderer, data, reading and four SVG/PNG figure pairs under `results/reporting/`.

## Preserved numerical repair evidence

`results/prior-attempt-correlation.json` proves the same 1,277 maps across the failed and repaired executable, unchanged predicates for the 1,275 previously completed cases, and successful recovery of both prior failures. Scientific equations, independent oracle and tolerances remain unchanged. The failed attempt is committed at `ca25c49c`; repaired implementation and audit are `bf1fae9f` and `0c60dc4a`.
