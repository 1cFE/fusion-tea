# Paired integrated design study support

[AGENT] Preparation implements T-002 under the coordinator's brief. The reviewed package, oracle and stock StudyRunner remain unchanged. `design_support.py` prepares complete maps, scans the independent oracle and calls the predecessor's reviewed numeric-map executor. `design_reporting.py` reads stored native outputs and performs presentation arithmetic only. New study artifacts use exclusive creation; execute refuses an existing results directory.

The local response record is `20260922-aries-integrated-local-response`. Its configuration declares 24 unique native maps: baseline; six modest OAT designs; two insufficient-area controls; three preserved source controls; each in no-credit and feed100/service30m scenarios. Seven indicator groups include declined cycle flow and three independent compressor ratios. The independent oracle evaluated all 24 proposed maps without refusal. Indicators find possible constraint paths for every declared group; these are not response or qualification claims. Native candidate execution awaits coordinator review release.

## Configuration and reuse

Each configuration has `study_id`, `axes` and `designs`. An axis supplies `axis`, complete `keys` entries with `key` and `provenance`, `units`, `role`, `framing`, `window_provenance`, `basis` and `missing_response`. `declined: true` traces an axis without permitting it in a proposal. Each design supplies `name`, `values` mapping axis names to numeric settings, and `classification`. Optional `canonical_base` selects a fingerprint-matched predecessor source receipt. The baseline is automatic. Every map receives the two fixed fuel scenarios. Duplicate complete maps fail visibly, so callers remove redundant baseline designs before preparation. Axis groups assign one scalar across their explicitly declared fanout/tie members; differing coordinated values require separate independent axes.

For future coupled and robustness records, the coordinator supplies explicit designs and audited groups. No grid, domain, operating optimum or uncertainty distribution is inferred. Assumed-role axes are sensitivity-only. Feed and service cannot be declared axes. Membership validation checks existing entry keys; the dependency audit remains responsible for establishing complete physical groups and legitimate roles.

Preparation copies the live manifest to `record/manifest.json` without mutation. Current groups are singletons and require no new manifest ties. A future tie needs a reviewed local manifest update and matching indicators before execution. The coordinator owns the seventeen-section record, framing rulings, preflight, execution authorization, findings, freeze and commit. Baseline/source/scientific-limit interpretation remains in those artifacts.

## Commands

Run from repository root. These commands target the local response record; set `DESIGN_RECORD` to a fresh record for replay. Preparation and scan shown below already ran and must not overwrite their original artifacts.

```bash
DESIGN_RECORD=exploration/aries_integrated/studies/20260922-aries-integrated-local-response
.codex-test/run python -m exploration.aries_integrated.studies.design_support prepare --record "$DESIGN_RECORD" --config "$DESIGN_RECORD/config.json"
.codex-test/run python -m exploration.aries_integrated.studies.design_support scan --record "$DESIGN_RECORD"
.codex-test/run python -m scripts.study.indicators --package exploration/aries_integrated/aries_integrated --manifest "$DESIGN_RECORD/manifest.json" --groups "$DESIGN_RECORD/axes.json" --out "$DESIGN_RECORD/indicators.json"
.codex-test/run python -m scripts.study.preflight gates --package exploration/aries_integrated/aries_integrated --manifest "$DESIGN_RECORD/manifest.json" --groups "$DESIGN_RECORD/axes.json" --identity work/orchestration/goals/aries-integrated-design-studies/evidence/baseline-replay/package_identity.json --baseline-result work/orchestration/goals/aries-integrated-design-studies/evidence/baseline-replay/baseline_result.json --out "$DESIGN_RECORD/preflight_results.json"
```

After release, use the already valid predecessor CANDIDATE; the executor checks its executable, semantic and indicator identities. No integration rerun is implied.

```bash
.codex-test/run bash -c 'PYTHONPATH="$PWD:$STOP_PARSER_TEAX_ROOT/packages/teax-simkit" STUDY_REQUIRE_TEAX=1 python -m exploration.aries_integrated.studies.design_support execute --record exploration/aries_integrated/studies/20260922-aries-integrated-local-response --integration-return work/orchestration/goals/aries-integrated-lcoe/evidence/integration-attempt1/integration_return.json'
```

Before verification, copy the actual current baseline replay identity into `results/package_identity.json`. Retain the baseline replay and preflight alongside it with their true provenance. Set sample size to the complete declared count (24 for the local study).

```bash
.codex-test/run bash -c 'PYTHONPATH="$PWD:$STOP_PARSER_TEAX_ROOT/packages/teax-simkit" STUDY_REQUIRE_TEAX=1 python -m scripts.study.verify --package exploration/aries_integrated/aries_integrated --manifest exploration/aries_integrated/studies/20260922-aries-integrated-local-response/manifest.json --identity exploration/aries_integrated/studies/20260922-aries-integrated-local-response/results/package_identity.json --store exploration/aries_integrated/studies/20260922-aries-integrated-local-response/results/native/20260922-aries-integrated-local-response.db --sample-size 24 --out exploration/aries_integrated/studies/20260922-aries-integrated-local-response/results/verification_summary.json'
MPLCONFIGDIR=/tmp/aries-design-matplotlib .codex-test/run python -m exploration.aries_integrated.studies.design_reporting --record "$DESIGN_RECORD" --out "$DESIGN_RECORD/results/design-summary.json" --plots-dir "$DESIGN_RECORD/plots"
```

## Record completion and replay

Freeze must retain the record-local manifest/groups/config/proposals, indicators, oracle scan, preflight and actual baseline identity, full native store and exported cases, all-point verification, execution-context commands, integration return, scientific-support outputs, paired reporting summary and PNG/PDF plots. Copy both support modules and the predecessor `20260922-aries-integrated-lcoe/execute_study.py`: the execution wrapper imports that exact reviewed implementation. The coordinator's `work/orchestration/goals/aries-integrated-design-studies/evidence/freeze-study.py` owns immutable snapshot/archive production. Its source capture must include these dependencies and the record-local manifest rather than silently reverting to live groups.

Report every attempted case and adverse predicate, retain source controls as their own category, and keep density as an operating diagnostic. Native contribution differences separate supply scenarios at identical physical inputs; the nonfuel/nonsupply subtotal excludes tritium, deuterium and supply service and is explicitly presentation arithmetic. Neither quantity proves physical feasibility. All plotted cases retain the scientific-qualification limitation. Paired physical comparisons need matched-baseline changes in electricity, capital and gross makeup before discussing the supplied-feed purchase threshold.

Replay executes only in a fresh record/worktree with the sealed package and retained licensed runtime. Preserve the original results and WAL files. Reporting alone can read copied native JSON without importing an evaluator. Initial support checks validated all 24 map pairs, declined-axis refusal, required-output refusal and baseline account/plot extraction using copied predecessor outputs; these checks do not certify new native candidate response.
