# Replay of the partial result

Use the repository's prescribed `.codex-test/run` launcher from its root. It supplies the existing sealed environment. Original packages and historical studies remain unchanged. This record has no new matched package, main-study store, integration candidate or economic result to replay.

## Native readiness controls

Choose a fresh external work directory. The script refuses to reuse one. It copies both existing packages there, evaluates through their native routes and compares all retained Brayton outputs against the prior sealed study.

```bash
.codex-test/run python work/orchestration/goals/design-study-component-alternatives/evidence/readiness-screen.py --work /tmp/component-readiness-replay --out /tmp/component-readiness-replay.json
```

Expected: seven completed evaluations, two retained steam-interface refusals, and 822 exact Brayton output comparisons. Failures and qualified predicate identities are in `readiness-screen.json`; passing implemented checks do not establish omitted cooling or equipment qualification. The native receipt was committed in `55eb24b8058057b218f6519565b78165a83dddf9`.

## Source-loop diagnostic

`source-coupling-probe.json` retains the original primary-loop body's path and SHA256, every fixed input, search bracket, iteration count, located source heat, loop output and independent exchanger residual. The accompanying script replays this bounded diagnostic into a new output path. It does not implement a compliant main-study closure.

```bash
.codex-test/run python work/orchestration/goals/design-study-component-alternatives/evidence/source-coupling-probe.py --out /tmp/component-source-replay.json
```

The script records the replay checkout's HEAD in `revision`. That metadata field changes after a commit; numerical inputs, outputs and source-body identity should still match the retained receipt. The reviewer reproduced the original receipt before the final reporting commit.

## Proposed assembly figure

The diagram has no plotted numerical points. Its labels describe the comparison boundary in WI-096's unimplemented design. Rebuild the SVG and PNG together:

```bash
MPLCONFIGDIR=/tmp/component-figure-cache .codex-test/run python work/orchestration/goals/design-study-component-alternatives/evidence/render-boundary.py
```

The missing performance/cost plots are recorded as unmet deliverables. No diagnostic whole-plant output is substituted for a matched subsystem result.
