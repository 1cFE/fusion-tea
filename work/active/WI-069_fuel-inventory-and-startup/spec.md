---
Status: active
Scale: standard
Epic: standalone
Owner: agent
Created: 2026-09-19
Updated: 2026-09-19
---
# WI-069: Fuel inventory and startup

## Contract

[NEED] Forward-compute and verify tritium operating inventory, external startup stock and processing throughput for R10.P2. Source: `work/orchestration/goals/fuel-inventory-and-startup/evidence/owner-prompt.md`, required results 1–9. Keep stage stocks distinct from rates; demonstrate responses to fusion power, burn fraction, recovery, residence times and reserves. Provide named unit-defined outputs for downstream fuel-processing costs. Obtain fresh unchanged-rubric grading.

[NEED] Preserve existing required-breeding arithmetic unless a correction is separately justified; preserve achieved-breeding ownership, ARIES quarantine, frozen r2 and historical studies. No fuel-processing price implementation or full self-sufficiency design. Formal goal closure remains owner-held.

[INHERITED] Required reading: `knowledge/holdout/aries-cs/PROTOCOL.md`, `modeling_project/REQUIREMENTS.md`, `modeling_project/MODELING_PROCESS.md` and `.project/codex-test-setup.md`. Existing equations/interfaces and proposed flow/storage diagram are traced in goal `evidence/current-trace.md`. Quantitative source facts and declared assumptions must retain their distinct authority.

## Acceptance conditions

- [NEED] Each represented process has a stream, stock calculation and documented residence/hold-up basis; no unexplained aggregate inventory.
- [NEED] Startup states what is prefilled, what is initially empty and when recycle/bred streams arrive. No duplicate system fill, reserve or blanket purchase. Initial external supply and continuing makeup are separate; any timing approximation and decay bound are explicit.
- [NEED] Operating processing capacities use full-power flow; annual amounts use the existing productive calendar. Shutdown stock and decay remain visible.
- [NEED] Verify conservation, units, meaningful limits, invalid inputs, hand/reference cases and integrated package outputs. Report inherited regressions separately.
- [NEED] A native focused assumption study supports the answer and fresh R10.P grade. Source uncertainty and unqualified external supply/breeding remain stated.

## Scope and integration

[AGENT] Canonical and exploration SysML, generated package, independent oracle/mappings, strict manual seeds if needed, snapshot/census/manifest and targeted tests are affected. Keep generic defaults dormant unless the reviewed design selects a safe specialized activation. Inventory drives the existing I_total interface; break execution cycles by calculating stock from independent power/energy inputs rather than a downstream fuel output if necessary. Costs remain unchanged.

## Persistent execution plan

- [x] Trace existing streams and consumers; deposit initial diagram and proposed startup accounting.
- [x] Retrieve and register admissible residence/startup evidence; record source/assumption ranges. Source scenarios and policy choices are separated in `design.md` and `knowledge/research/pending/20260919-074901_fuel-inventory-residence-startup.md`.
- [x] Complete source/math/interface design and fresh preimplementation review. Goal `evidence/source-design-review.md` records independent PASS and the release conditions.
- [x] Implement model and executable package with inventory/throughput interfaces and domain checks. Five canonical/twin pairs, seven physical stock occurrences, 28-input/70-output manual calculation, and 35 checked seeds; evidence in `evidence/generation-repair.log` and `tests/models/test_fuel_inventory.py`.
- [x] Verify independent numerical cases, affected consumers and invalid inputs; classify static diagnostics. Final author domain tests: 75 passed; affected oracle tests: 195 passed; 700 off-reference scalar comparisons pass. `evidence/static-classification.md` retains inherited L2/L6 failures and the three new runtime-resolved EXPOSE diagnostics.
- [x] Regenerate, recapture, repin and pass independent audit/native integration. Independent `audit.md` PASS; goal `evidence/integration/integration_return.json` returns CANDIDATE for commit `956444b5d440238857911a0406e6d3f51ddcbf2e`, with the native gate's explicit read-set coverage limitation retained.
- [x] Execute and verify one focused native study; obtain fresh R10.P grade and goal answer. Study `20260919-fuel-inventory-and-startup@3529f6c8` retains 26 cases; all 23,556 mapped scalar and 650 predicate comparisons pass. Fresh non-author `fuel_final_grade` assigns R10.P = 2, PASS; goal `answer.md` and `evidence/final-review-and-grade.md` contain the answer and limits. Formal goal closure remains owner-held.

## Verification registry and release

SV-115 and SV-116 were updated to passing through native PM after all 26 study cases completed and 23,556 scalar / 650 predicate comparisons passed (`exploration/stellarator_e2e/studies/20260919-fuel-inventory-and-startup/results/oracle-all-points.json`). `evidence/verification-plan.md` maps the claim coverage. Independent original-source/math/design release: goal `evidence/source-design-review.md`, PASS for conditional implementation. Fresh final review separately assigns R10.P = 2. The source-scenario register is the parameter table in `design.md` and the native pending research report it cites; no source insight is promoted as owner-approved knowledge.
