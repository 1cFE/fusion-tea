# Replay the repaired matched comparison

The current record is `exploration/component_alternatives/studies/20260926-design-study-component-alternatives-b/`. Its predecessor, without the `-b` suffix, preserves the original failed executable, all 498 cases, six numerical failures and attribution correction. Never execute into either retained results directory. The route refuses an existing results directory.

## Verify the repaired native store

From the repository root, with the repaired package at executable `36f653faacc301e76132a9364c1b1024e6d0b3d28742138fcc4759aeef7b3986`:

```bash
.codex-test/run bash -c 'PYTHONPATH="$PWD:$STOP_PARSER_TEAX_ROOT/packages/teax-simkit" python scripts/study/verify.py --package exploration/component_alternatives/component_alternatives_tea --manifest exploration/component_alternatives/studies/20260926-design-study-component-alternatives-b/manifest.json --identity exploration/component_alternatives/studies/20260926-design-study-component-alternatives-b/preparation/package_identity.json --store exploration/component_alternatives/studies/20260926-design-study-component-alternatives-b/results/native/20260926-design-study-component-alternatives-b.db --sample-size 498 --out /tmp/component-alternatives-repaired-verification.json'
```

This reads the retained native store and independently checks every case. The record's `results/execution-context.json` carries exact execution and verification commands. `preparation/` contains fresh baseline and integration receipts; its verification summary covers the integration baseline only. The full study summary is `results/verification_summary.json`.

## Re-execute in a fresh record

Create a fresh repository-local scratch record and copy the new record's `proposed-points.json` into it. Choose a path that has no `results/` directory. Substitute that path for `FRESH_RECORD` below:

```bash
.codex-test/run bash -c 'PYTHONPATH="$PWD:$STOP_PARSER_TEAX_ROOT/packages/teax-simkit" python -m exploration.component_alternatives.studies.execute_study --record FRESH_RECORD --integration-return work/orchestration/goals/design-study-component-alternatives/evidence/integration-repaired/integration_return.json'
```

The study-local route composes all 490 inputs and calls stock PreparedListStrategy, StudyRunner and Store. It runs no physical solve. The three fresh `*-scan.json` files document the unchanged oracle's pre-execution scan of 501 offers, with three duplicate aliases consolidated into 498 exact native points. `window.json` records that finite catalog; it establishes no continuous optimum.

## Reproduce the figures in a fresh directory

```bash
.codex-test/run python work/orchestration/goals/design-study-component-alternatives/evidence/verified-comparison/analyze-verified.py --out-dir /tmp/component-alternatives-repaired-figures
```

The renderer checks complete stock verification, exact case coverage and fingerprint before reporting stored outputs. It performs only reporting arithmetic. Every plotted point retains its native ID, evidence digest, chosen inputs and all predicate verdicts. The unchanged assembly diagram and renderer remain `reviewed-comparison-boundary.svg`, `reviewed-comparison-boundary.png` and `render-reviewed-boundary.py` in this evidence directory.

## Focused numerical regressions

See WI-096 `numerical-repair/report.md` for the kept 15-run regression and nine high-precision local checks. Use new output directories. They cover all six original failures and nearby sensitive offers while preserving the original independent oracle and tolerances. Full-study verification remains the wider acceptance evidence.

## Preserved predecessor

The original blocked snapshot remains `1e8a19872852e19390eba76445e11a866c5da8fb9f791122b6b64d6e16b66641`. Its `sealed-package.tar.gz`, native store, cases and failure diagnostics are unchanged. Replaying that executable requires its archived bytes or a separate checkout at `49c20e69`; the live package now carries the authorized repair. Extract archives only into a fresh scratch directory. Do not substitute the repaired package when interpreting the predecessor's identity.

The old cooler-only attribution was corrected by its retained addendum. The repair's diagnosis and independent review now isolate all six causes: four cooler-root accuracy defects and two cases with network-root propagation plus smaller local bypass error. Old diagnostic figures remain in their original locations; verified figures live in `verified-comparison/`.

## Current seal and review

Verified snapshot SHA256: `ea6b9de7cf242c88f764a9a997aadd1b6d813560b5c0953e84e63a7aeef9928e`. Independent final assurance checks all 720 new artifacts and all 635 predecessor artifacts with zero changes. The archived initial economic review remains immutable; external `repaired-results-review.md` adds final hash assurance. Run `.codex-test/run python work/orchestration/goals/design-study-component-alternatives/evidence/check-repaired-record.py` for record hashes, exact sample coverage, native findings joins and top-level record links.
