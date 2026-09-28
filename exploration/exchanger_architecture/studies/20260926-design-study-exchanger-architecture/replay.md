# Replay instructions

Run from `/home/reid/1cfe/fusion-tea`. Use the licensed pinned runtime through `.codex-test/run`. The native record retains its input maps, route/oracle/support sources and sealed package archive. No command below writes into the sealed record.

## Reverify all stored cases

```bash
.codex-test/run bash -c 'PYTHONPATH="$PWD:$STOP_PARSER_TEAX_ROOT/packages/teax-simkit" STUDY_REQUIRE_TEAX=1 python -m scripts.study.verify --package exploration/aries_integrated/aries_integrated --manifest exploration/exchanger_architecture/studies/20260926-design-study-exchanger-architecture/manifest.json --identity exploration/exchanger_architecture/studies/20260926-design-study-exchanger-architecture/preparation/package_identity.json --store exploration/exchanger_architecture/studies/20260926-design-study-exchanger-architecture/results/native/20260926-design-study-exchanger-architecture.db --sample-size 648 --out /tmp/exchanger-architecture-verification.json'
```

Expected: all 648 cases; 364 oracle scalar channels and 14 independently rederived native predicates per case; zero mismatches. The current oracle does not verify native primary hot/return temperatures or terminal differences. Package identity is checked before verification; a changed live package must be restored from the sealed archive in an isolated checkout with the retained support sources.

## Execute every retained full input map again

Choose a destination that does not already exist. The wrapper runs the stock native lifecycle, writes a fresh SQLite store and compares complete inputs, outputs and predicates against the sealed exports. Its new candidate IDs are retained. It refuses reuse of an existing destination.

```bash
.codex-test/run bash -c 'PYTHONPATH="$PWD:$STOP_PARSER_TEAX_ROOT/packages/teax-simkit" STUDY_REQUIRE_TEAX=1 python work/orchestration/goals/design-study-exchanger-architecture/evidence/replay-native.py --destination /tmp/exchanger-architecture-replay'
```

Delivery check: this wrapper was executed against all 648 cases in `/tmp/exchanger-architecture-delivery-replay`; exact equality passed for all stored numerical outputs, inputs, predicates, state and executable identity. Receipt: `delivery-replay-comparison.json`. This requires the original sealed package and retained runtime identity. The original preparation, execution and verification commands are also in the native record's `results/execution-context.json`.

## Render figures from stored results

```bash
MPLCONFIGDIR=/tmp/exchanger-matplotlib .codex-test/run python work/orchestration/goals/design-study-exchanger-architecture/evidence/render-results.py --record exploration/exchanger_architecture/studies/20260926-design-study-exchanger-architecture --verification exploration/exchanger_architecture/studies/20260926-design-study-exchanger-architecture/results/verification_summary.json --out /tmp/exchanger-architecture-figures
```

The renderer creates the requested output directory. It reads stored outputs and performs only selection and presentation arithmetic. It refuses absent or partial verification. SVG/PNG figures and CSV source data are written to the requested output directory; no physical model is run. Figure lines join sampled cases and never imply a continuously optimized boundary.
