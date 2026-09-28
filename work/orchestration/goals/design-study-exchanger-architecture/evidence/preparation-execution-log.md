# Exchanger study preparation and execution log

[AGENT] 2026-09-26. Preparation agent owns the new goal preparation paths and this log. The original ARIES package, models, scripts, manifest and historical records are unchanged.

## Preparation completed

- Corrected the thermal audit source selector labels from direct implementation evidence: 0 supplied, 1 calculated. Exact calculated anchor is 1835.4512830147435 MW; inherited pressure loss is 0.045.
- `prepare-study.py prepare`: 625 initial unique maps and one alias; 432 main, 192 uncertainty, one calculated N control. No physical arithmetic in the composer. It validates complete finite maps and declared-key coverage, preserves search/sensitivity roles and records aliases.
- `scripts/study/indicators.py`: all ten groups valid and `no_constraint_response=false`. Reachability is not observed response; actual fuel-price resistance and supply qualification are absent.
- `prepare-study.py baseline`: native pinned baseline and identity emitted to record preparation/. All six stock preflight gates pass.
- `prepare-study.py scan`: 648 unique independent-oracle evaluations, zero refusals, zero nonpositive-net exclusions. Adds 22 zero-price paired controls at 11 loads and one unique network-extra-loss control. The second topology-loss control aliases an existing uncertainty point. Two aliases total.
- `exploration/exchanger_architecture/control_replay.py`: all 551 original native outputs and 14 verdicts equal the sealed N row exactly; supplied power preserves 549 downstream outputs and all verdicts. Only the two source-mode echoes differ.
- Corrected price endpoint authority to AGENT-selected within owner-authorized fuel sensitivity. Retained earlier indicator/preflight receipts as attempt1; regenerated current receipts. No physics, input map or proposal changed.
- Filled the native 17-section record before execution, including per-axis framing/applicability, missing fuel resistance, return/approach limitations and numerical verification coverage.

## Prepared native execution

Record: `exploration/exchanger_architecture/studies/20260926-design-study-exchanger-architecture/`. Native main execution awaits coordinator release. The wrapper calls the unchanged prior full-map exporter, strict loader and StudyRunner.

```bash
.codex-test/run bash -c 'PYTHONPATH="$PWD:$STOP_PARSER_TEAX_ROOT/packages/teax-simkit" python exploration/exchanger_architecture/execute_study.py --record exploration/exchanger_architecture/studies/20260926-design-study-exchanger-architecture --integration-return work/orchestration/goals/aries-reference-heat-electricity-reconciliation/evidence/integration-attempt2/integration_return.json'
```

After native execution, verify all 648 cases with the stock verifier at the unchanged manifest tolerances. Verify source identity and package cleanliness again; export all 551 channels and 14 predicates. Primary hot/return and terminal differences remain native diagnostics outside the independent 364-channel oracle catalog. No independent scientific qualification is claimed.

## Native execution and verification completed

[AGENT] The coordinator completed T002 and explicitly released T003 on the unchanged 648-map set. Native execution completed all 648 cases, exporting 551 outputs and 14 predicates each. There are 397 cases passing every implemented predicate and 251 retaining engineering failures. All 648 points pass the independent 364-channel comparison and exact 14-predicate rederivation at the unchanged tolerances. The largest reported relative error is the near-zero residual channel: native 2.6177531253779307e-9 MW against an oracle value near zero, within the predeclared 1e-7 MW absolute tolerance. No tolerance or scope changed. Post-execution package-clean check passes.

Logs are preparation/native-execution.log and preparation/native-verification.log in the record. results/execution-context.json retains exact commands and execution-time identity; results/execution-completion.json records completion and evidence digests. The costs/reporting agent was notified only after verification passed. Record and results ownership now returns to the coordinator for final narrative, independent result review and seal.
