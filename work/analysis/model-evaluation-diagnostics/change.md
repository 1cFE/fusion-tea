# Domain diagnostic correction

[NEED] Improve failure diagnostics without extending empirical coverage or altering supplied designs. Source: owner request, work/orchestration/goals/model-evaluation-domain-readiness/goal.md.

[AGENT] Process: quick-model, with model-validation selecting native/regression checks. This enforces the existing primary-loop declaration `p_loop_in > dp_loop` before its compressor pressure ratio and fractional power. The actual case has positive 100000 Pa discharge pressure and calculated 300319.8964637657 Pa loss; its negative suction produces complex values. Guard finite positive supplied pressure, finite nonnegative calculated loss and strictly positive suction. Reject with supplied pressure, calculated loss, suction, Pa and calculation identity. This is a numerical-domain refusal; no completed plant result or physical-adequacy verdict is manufactured.

[AGENT] Conductor guards retain their exact comparisons: fixed 20 K, fixed 56 micrometre composite thickness, 4–6 mm width, 20–32 T, and explicit permission above 24 T. Add actual values and units to existing messages. No new source interpretation or scientific extension is proposed.

| Quantity | Unit | Existing and retained role | Consumers |
|---|---|---|---|
| Primary discharge pressure | Pa | Supplied operating condition | Primary-loop ratio, suction, compression work |
| Loop pressure loss | Pa | Calculated from required flow and held loss law | Compressor ratio and pressure margin |
| Suction pressure | Pa | Calculated discharge minus loss; positive-domain prerequisite | Compressor temperature/work, IHX duty, downstream power/economics |
| Peak conductor field | T | Calculated from supplied turns/current/geometry | Conditional REBCO performance and current margin |
| Conductor temperature/construction | K, m | Supplied condition/design | Conditional REBCO applicability |

[AGENT] Affected definitions: models/library/analyses/mfe_primary_loop.sysml and its canonical execution twin; generated handwritten primary coolant loop and REBCO current bodies. No public parameter or consumer binding changes. Native generation retains all other normative bodies; old seeds and integration records remain untouched. Applicable tests: pressure boundary/negative/nonfinite cases, independent valid-state heat/work conservation, existing conductor tests, baseline all-channel equality and native refusal with fixed hardware. New seed inventory/fresh regeneration, current manifest identity and supported integration are required. Fresh coverage/integration review checks the executed correction; no separate scientific expansion review applies because the equation and empirical support are unchanged.

## Executed checks

[AGENT] Two fresh native generations match exactly, retaining 52 normative bodies with only the two authorized manual-body deltas. `regeneration.log`, `candidate-seeds.json`, `seed-delta.json` and `package-hashes.json` bind the result. The semantic fingerprint and indicator input pin are unchanged; executable fingerprint is `83ea3b6cf99f5fda6045e7e03b5d430ede91abbe8aa41262c2f9f5aba8663d23`.

[AGENT] `.codex-test/run python -m pytest tests/models/test_primary_loop_domains.py tests/models/test_conductor_current.py -q` passes 157 tests; original float-as-Boolean warnings remain. `check_and_pin.py` confirms exact equality for all 1,352 numeric channels and 68 responses against the retained WI-080 baseline. `native_acceptance.py` exercises three unsupported conditions through the supported evaluator: nonpositive compressor suction, conductor field and conductor temperature. All refuse with offending values and calculation identity. Their native failure records expose no retained upstream partial artifacts; no partial values or completed plant result are invented. These are deterministic repair-acceptance checks, separate from the capped entering-domain exploration.

[AGENT] No empirical extension or new performance model was introduced. A lower-pressure case remains unsupported; the repair replaces an uncontrolled complex-output schema error with an explicit domain refusal. Final independent coverage review and committed native seam acceptance remain pending.

## Current regression consumer correction

The first committed full seam at `02925b74` stopped at model-family-spine: one failure and six fixture errors all arise because `tests/models/current_mfe_regressions.py` still selects WI-080's old normative-body hashes. Its current-generation helper now uses the same native recipe with this diagnostic repair's independently reviewed candidate-seeds.json. Historical WI-080 files and assertions remain unchanged. This is a fixture identity correction, not a waived test or new model change. The failed seam remains under .project/active/model-evaluation-read-coverage/integration-final/. A new checkpoint and separate corrected integration attempt are required.
