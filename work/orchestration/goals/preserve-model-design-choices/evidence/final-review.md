# Final independent integrated review

**PASS — the owner's technical completion criteria are met for the declared, independently reviewed scope.** The repaired model preserves supplied magnet, facility, processor and cooling design choices through native evaluation and represented inventory/cost. No confirmed MR-7 violation or required repair acceptance check remains open in that scope. Formal goal closure remains owner-held.

[AGENT] Independent non-author review, 2026-09-20. This final assessment incorporates the source, architecture, inventory, acceptance and regression reviews preserved in [implementation-review.md](implementation-review.md). It supersedes that document's interim unverified integration status; it does not erase its findings or their corrections. No reference papers, revealed observations, original reference request or quarantined material were opened by this reviewer. No reference comparison or reference-based tuning informed this verdict.

[OWNER-VERBATIM] “As soon as you start introducing ‘sizing’, then you are basically pre-defining which design parameters are ‘free’ and which are ‘derived’. this is explicitly what we wanted to avoid.” The review checks this intent against actual bindings and downstream behavior. MR-7's application rules and the bounded evaluation contracts remain agent interpretations, not additional owner-originated requirements.

## Completion evidence

| Owner criterion | Independent finding |
|---|---|
| Complete scoped inventory | Parsed model traversal and entering 511-input census are supplemented by explicit residual contracts and a reconciled current census. I checked 609 unique union rows: 499 retained, 98 introduced and 12 retired; 597 current inputs, zero unconsumed current inputs and resolving review references. The native seam independently re-derives all 597 entries and checks canonical/generated family correspondence. |
| Repair confirmed selection violations | Supplied pack side, installed turns and structural masses replace mandatory magnet selection; room/partition/parcel/position/package choices replace demand-grown facilities; supplied processor rating replaces exhaust×margin; selected cooling price points and purchased stocks replace demand-matched procurement. Hydraulic calibration is separate from the offered flow ceiling. Actual downstream part, thermal, inventory and price bindings were reviewed. |
| Applicable native behavior | Tests exercise supported insufficient/sufficient supplies, meaningful current/fit/material/room/parcel/flow/fill predicates, unchanged selected hardware under changed demand, and inventory/cost propagation. Conductor conditions outside 20–32 T refuse explicitly. Two deliberately tiny-negative supplied-pack cases remain strictly negative in both native and independent results and return exactly `violated`. All review-requested assertion gaps are closed. |
| Residual policies/proxies | R01–R15 have approved bounded meanings. Fuel maintained stock and startup are explicitly policy/requirement analyses; calendar replacement is a declared scenario. Thermal/steam/water/vacuum closures do not claim installed equipment. Demand-based and hybrid prices disclose their assumptions and missing installed-capacity evaluation. No absent pump map or storage/structure qualification is manufactured. |
| Regression and integration | Composite regression evidence resolves every failure from the broad sweep. The corrected native integration returns CANDIDATE with all ten gates passing. Numeric coverage independently compares all 1,149 current numeric channels and derives all 34 predicates across six scenarios. Historical evidence is preserved, with explicit test-only migration rather than silently changing frozen expectations. |

## Regression result and evidence integrity

The retained `WI-075/integration/model-regression-sweep.log` records **2,440 passed, 5 failed, 13 skipped and 1 xfailed**. All five failures are exactly the previously reviewed stale assumptions in the dormant-facility and operating-heating tests. Their complete affected-file reruns report **42 passed** and **9 passed** in `facilities-final.log` and `operating-heating-final.log`. Those corrections change tests only; they preserve exact old scope while checking the six new predicate shapes, independent flow-rating formal and retained coordinate identities. No production/package/shared-fixture change requires rerunning unaffected tests. This is accepted composite evidence, not a claim that the original full sweep was green. Skips and the existing expected failure are not counted as passes.

Additional retained evidence includes the 108-test mixed local/native acceptance batch, strengthened 61- and 68-test batches, two strict-boundary passes, 13 numeric-coverage tests and 102 stock-route tests. These counts overlap and must not be added as unique coverage. I inspected the consequential test assertions and migration logic rather than relying on totals. Retired-producer projection is explicitly enumerated; exact surviving comparisons and independent current predicate checks remain. Optional selection helpers execute in a separate test-generated package, outside the supplied-design evaluator.

The first integration attempt correctly refused an obsolete axis declaration naming retired ampere-turn current. The versioned current declaration is explicit about operating amperes per turn and leaves the old fixture unchanged. The corrected seam's ten passing gates include pinned dependencies, requested TEAx revision, byte-preserving regeneration, 138 preserved handwritten files, recaptured snapshot/census, model-family spine, manifest, six preflight gates, oracle/verdict verification and lineage.

I independently hashed all **13 retained seam artifacts** and their original native counterparts against `WI-075/integration/seam-retention.json`; all matched, including the retained store and committed snapshot. The native documents preserve their scratch paths, and that index supplies durable byte-identical locations. The seam's baseline verification checks one executed case, reports no verdict mismatches or unverified listed predicates, and has worst checked-channel relative deviation `2.409591420195442e-15`. Full numeric coverage comes from the separate six-scenario test suite, not an exaggerated interpretation of this single baseline.

## Accepted identity and remaining limits

The source checkpoint named by the successful seam is `b11567eb693a4fd6f45a487f75dc5244fb433774`.

- Candidate pin: `84b82ef338093eb6d6f142360b3ded2b575b6f79397e6a719a6cb6dcf0154bc6`.
- Semantic fingerprint: `5a76ffbe2c1457b8abd5e8e9203331959baf68af65d7e12f9f49bb09d0bf071c`.
- Executable fingerprint: `04d3af1627885ce7a68d726b1d36026777eccc5d4976b15d693b6c8ec438f227`.

The integration return explicitly says `assert_read_set_covered` was not run and is covered by nothing else in that gate. Preserve this existing tooling limitation in the delivery record; the ten-gate pass does not establish read-set completeness. The verification summary's local TEAx revision field is unrecorded, while the enclosing native seam independently checks the requested TEAx revision. Neither limitation is evidence of a remaining design-selection defect or missing behavioral acceptance in this repair.

The model still cannot qualify arbitrary pump/compressor off-design operation, complete coolant inventory, arbitrary exchanger/pipe performance, supplied support strength, arbitrary facility topology, offered active fuel stock or actual vacuum equipment. Generic direct-heating consistency remains outside the active stellarator contract. These are explicit absent capabilities, not confirmed unresolved selection violations hidden behind a completed label. A passing represented-flow/fill/fit check must not be promoted to full equipment qualification. Whole-plant feasibility and lower cost were never acceptance conditions.

## Learning dispositions and round recommendation

Approve the proposed learnings with these precise bounds:

- Audit actual generated public roles and consumers. In this emitter, the tested negative-literal coordinate declarations became constants; signed offset inputs restored translation freedom. Do not generalize this observation to every SysML toolchain.
- Explicit chosen-design contracts can restore the reviewed freedoms without a universal inverse solver. This does not prove that every future analysis direction is supported.
- Keep physical inadequacy, unsupported empirical evaluation and conditional price applicability distinct in both outputs and acceptance tests.
- Missing performance maps, structural qualification, offered-stock evaluation and arbitrary topology remain named capability limits. They must not be filled with invented approximations to obtain a passing result.

The round has a supported technical answer and no remaining remediation blocker within its approved scope. Recommend recording technical completion, the exact candidate identity and the retained limits, then returning the formal closure decision to the owner. This review does not authorize closure, archival, merge/push or a new comparison.
