---
Status: implemented
Created: 2026-09-15
Updated: 2026-09-15
Related Artifacts: spec.md; design.md; evidence/baseline.json
---
# WI-060 implementation report

Selected tape procurement now follows full composite tape volume divided by width and thickness. The native interface exposes tape metres and an explicit dollars/tape-metre price. Field-envelope scaling enters pack volume once; the grade calculation carries no price. Legacy ampere-metre comparison accounts and conductor-metre winding operations retain their meanings.

The design point contains 12.2904 m³ tape, or 36,578,571.43 m at 6 mm × 56 μm. At the declared $20/m scenario, tape costs $731,571,428.57 instead of $804 million: a $72,428,571.43 reduction predicted before implementation. The resulting LCOE is $144.7383011344/MWh and total capital $8,904,384,837.76. This price is an independent assumption, not a supplier quote or old-total fit. Cross-source tape construction, fixed composition, unqualified current margin and continuous inventory remain explicit limitations.

## Evidence available

- Independent source/math/interface PASS: goal evidence/design-review.md; completion review remains separate.
- Fresh generation: evidence/generation-final.log and regenerate.py prove two fresh packages byte-identical to production. Twenty manual bodies are preserved; two changed bodies are declared in changed-seeds.json.
- Baseline: evidence/repin.log and baseline.json compare 179 mapped native/oracle scalars; producer manifest and census are refreshed. Package has 292 inputs, 195 numeric channels and eighteen predicates.
- Tape-specific checks: evidence/tape-scaling-final.log, 21 passed. Includes density/envelope combinations, dimensions, distinct current/volume set factors, count/current, price, legacy isolation and invalid arithmetic.
- Existing component batch: evidence/component-tests.log initially 235 passed and two stale-expectation failures; repaired expectation checks pass within evidence/tape-tests.log, whose nine new-test failures were an incorrect request for an EXPOSE alias through the canonical-output-only evidence route. Corrected tape tests pass separately.
- Native validation: evidence/validate-complete.log reports L1/L3/L4/L5 passing and L2/L6 failing. Compared with WI-059's retained complete log, the only text difference is 471→473 validated bindings. L2 reports ten literal-binding warnings and no unbound/undefined/self-named inputs; L6 retains existing scanner findings. This is not a claim that all native validator levels pass.
- Current consumer checks: 58 domain/winding checks pass; the broader batch reports 405 passed and two failures, repaired by the 17-check operand rerun and one clean-radius rerun. Logs are consumer-domain-winding.log, consumer-other.log, consumer-operands-recheck.log and consumer-radius-clean-recheck.log.
- Native traceability entry added; SV-107 registered and marked passing for the 21 tape checks. Native PM offers no active-status transition operation, so the add-item registry status remains backlog while active spec/stage files identify actual work. No manual registry edit was made.

## Regression repairs and final handoff

The full model suite reported 904 passed, thirteen inherited skips, one stale-economic-expectation failure and 46 errors from a shared CLI fixture (evidence/model-suite.log). The CLI still expected four WI-059 economic anchors; native/oracle values agreed. Updated the live runner anchors from the checked native baseline. The coil thermal replay now excludes only the changed tape/capital channels and retired effective-price channel. Historical records remain untouched.

The complete affected radius and coil thermal files now pass all 97 checks (evidence/model-recheck-final.log). A final one-test replay check passes after narrowing its explicit exclusion list (evidence/replay-final.log). A standalone radius test also gained its explicit sealed simkit path; the complete original run already passed that test through earlier fixture setup. The separate operating-heating file passed nine checks. No remaining observed test failure is unresolved; the full suite was not repeated after these bounded repairs.

The public migration receipt (evidence/contract-migration.json) proves exact equality of all eighteen predicate expressions. It records three added tape inputs, one removed grade-price output and one added tape-length output. Total contract outputs remain 214 (195 numeric plus structured assertions). Native evidence publishes canonical calculation channel names; the model's tape-length EXPOSE is an internal/model capture alias, not a second canonical route output.

Implementation checkpoint: 9e22a0a6. The follow-up commit includes the final live-consumer repairs and evidence. The package remains unchanged from that checkpoint. Independent integrated review and the coordinator-owned integration/study remain the next steps. This report supplies implementation evidence and does not self-certify independent review.

## Integration prerequisite correction

T-004 integration refused the stale tracked instance-graph snapshot: the preparation recipe refreshed the census and manifest but omitted snapshot capture. T-005 adds the native `capture_instance_graph_snapshot` producer call to evidence/repin.py and refreshes exploration/stellarator_e2e/stellarator.snapshot.json. The resulting snapshot exactly matches T-004's independent recapture. Tool authority is unchanged. Attribute count changes 435→438: three tape inputs and the tape-length EXPOSE enter; the effective-price attribute leaves.

Evidence/snapshot-repair.json records both snapshot hashes, exact recapture equality and unchanged hashes for all 309 watched model/package files. Evidence/snapshot-repair.log records the executed native producer. No model, generated package or runtime changed. The integration seam still owns its rerun and acceptance.
