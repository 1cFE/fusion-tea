# WI-051 implementation evidence

[AGENT] Phase 1: applied exactly the revised source patch in canonical and twin files. Entering regression: 364 passed, 13 skipped, exit 0; per-node results and reasons in `entering-tests.xml` and `entering-tests.log`. Structural and freshness tests: 12 passed, exit 0 (`phase1-tests.log`). Native checkpoints/differential are recorded in `commands.md` and `phase1-differential.log`; phase completion requires their successful differential. No independent audit claim.

[AGENT] Phase 2: source/snapshot packages byte-identical; four manual bodies and 65 freshly generated bodies. Full 247→246 contract delta, 246 exact surviving parameter records/defaults, exactly five changed operands and nine authoritative R edges. Published package and fresh census/snapshot. Focused tests 27 passed (`phase2-tests.xml`); L1/L3 pass and L2/L6 have no added/removed diagnostics (`phase2-differential.log`).

[AGENT] Phase 3 first kept-test attempt: 59 passed, two failed. Both failures were test lookup mistakes: coil centre is the emitted `rb__r_coil_centre`, while outer build is a derived geometry control, and the frozen baseline component case is named `valid`. `test_mfe_major_radius-attempt-1.py`, `phase3-tests-attempt-1.log` and XML preserve the failures. The correction uses actual published names and the retained outer-build sum; no expected value, source or production equation changed. The complete production acceptance execution itself passed before those test lookups. `native-attempt-1.py` preserves that executed probe before extending it to typed peak-component inputs and explicit upper-bound results.

[AGENT] Phase 3 complete: final acceptance (`acceptance-attempt-2/`) and all 64 kept tests pass (`phase3-tests-attempt-2.xml`). L1/L3 pass; L2/L6 differential unchanged. Native strict loader, typed input schema, actual production helper/single functions and baseline CLI all executed. Every original/final package hash remains exact.

[AGENT] Native PM rejected the initial attempt to place item-specific `MR-051-01` in its validated project-requirement field (`trace-generic-attempt-1.log`, exit 1, no mutation). Following the existing native trace convention, the successful two rows carry MR-051-01/03/08 in Source_Location with the exact T-021 path/revision/sections; Requirement is empty. No PR or DI was invented or promoted.

[AGENT] Final regression attempt 1: 427 passed, 13 inherited skips, one current-model expectation failure (`test_mfe_operating_heating.py::test_stellarator_operating_heat_has_no_public_demand_input`). It still asserted 247 on a freshly generated current family. The proved sole retirement makes 246 correct. Only that count and its WI-051 explanation changed; the original file is retained as `test_mfe_operating_heating-entering.py`. This is the bounded current-model expectation correction authorized by Phase 4; historical controls stay unchanged.

[AGENT] The first location-aware differential attempt failed in its location parser because native file URIs retain two leading slashes after stripping the root (`final-evidence-attempt-1.log`). The corrected parser strips those URI slashes while retaining logical file and mapping only identical source lines to their entering line. Original script is `final_evidence-attempt-1.py`. No diagnostic expectation changed. A preliminary read-only introspection also found issues are strings, not dataclasses; `vars()` raised TypeError and no files were changed.

[AGENT] The second final-evidence invocation started before pytest finished writing its XML and failed with FileNotFoundError (`final-evidence-attempt-2.log`). It did not change test expectations or production. The same script is rerun only after the successful final pytest exit. Final model regression is 428 passed / 13 skipped, exit 0 (`final-tests-attempt-2.log` and XML): all 364 entering passes and 13 entering skips are retained, with 64 added WI-051 passes.

[AGENT] Final-evidence attempt 3 correctly refused a blanket protected-equality claim: concurrent parent commits `2a55615b` and `4fc05302` added nine pending STEP research files and changed the goal trail. `protection-diff.json` retains their entering/current hashes, and `concurrent-parent-changes.json` proves those changes against the parent git objects. No WI-051 command changed those paths. The final comparison permits only this exact independently committed delta and the one bounded current-model count correction. Original prototype/revision/review/frozen evidence and excluded study consumers remain byte-identical.

[AGENT] `git diff --check` reports CRLF on the two rows appended by native `trace-element`; pre-existing native rows also use CRLF. The mandated native PM output is retained, with no hand edit or shared-tool repair. This is a formatting limitation, not a model diagnostic or an independent audit verdict.

[AGENT] Final-evidence attempt 4 exposed an incorrect bookkeeping assumption: the entering trail was already modified by the parent (visible in `entering-status.txt`), so its hash does not equal the planning commit. Its exact captured hash equals the subsequently committed `2a55615b` trail; the final trail equals `4fc05302`. The comparison now checks those actual git objects. `final_evidence-attempt-4.py` and its log preserve the failed assumption. This changes provenance accounting only, not protection expectations or production.

## Final requirement and evidence map

[AGENT] Exact expanded pytest node IDs (including every parametrized case) are in [requirement-test-nodes.json](requirement-test-nodes.json). All listed test nodes passed in `final-tests-attempt-2.xml`; required WI-051 nodes were not skipped. Expected/actual payloads and reports are retained in `acceptance-attempt-2/`. The following table links the production evidence; each row preserves the spec’s authority grade.

| Requirement | SV | Production evidence and test coverage |
|---|---|---|
| MR-051-01 | SV-083 passing | `test_current_contract_edges_and_fresh_package_agreement`; complete native/direct parity nodes; `edges.json`, `contract-checks.json`, acceptance outputs. |
| MR-051-02 | SV-084 passing | Four standalone nodes, geometry/anchor node and typed peak controls; `standalone.json`, `checks.json`, exact unchanged library hashes and source binding tests. |
| MR-051-03 | SV-083/085 passing | Complete census and exact surviving records; all 20 path/case retired-key nodes; native/schema/direct/CLI records. |
| MR-051-04 | SV-086 passing | `test_complete_native_and_direct_parity[baseline]`; 158 exact scalars, 177 exact raw outputs, full serialized reports; immutable controls and corrected helper history. |
| MR-051-05 | SV-087 passing | `test_complete_native_and_direct_parity[R14]` and independent ratios; complete cost/finance outputs and unchanged fixed JSON controls. |
| MR-051-06 | SV-088 passing | All 15 unified invalid path/case nodes and five component controls; preserved original plant-zero/magnet-zero; explicit upper-bound counterexamples, F07 open. |
| MR-051-07 | SV-089 pending audit | Freshness/seed refusal tests, strict load, twin/source and independent family source/snapshot tests, current census, full per-node regression; `generation.json`, `final-identities.json`, `regression-diff.json`. |
| MR-051-08 | SV-089 pending audit | Attached structured citation test and `citation-attachments.json`; native trace rows; `full-validation-diff.json`, `protection-diff.json` and concurrent parent git verification. Independent assessment remains. |
| MR-051-09 | SV-089 pending audit | `consumer-handoff.md` gives exact identities, interfaces, expected/actual behavior and separate coding migration. Current-study compatibility incomplete; independent audit outstanding. |

## Final result and limits

[AGENT] Implementation is ready for the parent’s fresh independent native audit. The final location-aware differential has no added/removed L2 or L6 finding; L1/L3/L4/L5 pass and L2/L6 remain FAIL (10/229). Final regression is 428 passed / 13 skipped; zero existing outcome/skip-reason changes and 64 new passes. The failed stale-count attempt is retained separately, not erased by the final comparison.

[AGENT] `final-evidence-attempt-5.log` passed all production, source, snapshot, diagnostics, per-node and protected-surface checks. Four manual hashes are exact, every other body was freshly generated, and all 69 implementation ASTs match entering bodies after removing only docstrings (`generated-body-delta.json`). Native regeneration updates stale generated documentation and source line metadata; no library equation was changed. The final semantic/executable identities are measured, not copied from the prototype.

[AGENT] No source, premise, scope or capability blocker remains within this implementation boundary. Current-study compatibility is explicitly incomplete; source/finance/supported-scope decisions, F07 residual acceptance and all later integration/study work remain outside this item. No self-audit or item-completion certification is supplied.
