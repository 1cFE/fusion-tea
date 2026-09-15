# Final mechanical and answer assurance

## Initial verdict — 2026-09-15

**Two concrete record/answer gaps remain; numerical interpretation and the six landed dispositions pass.** Final test results and the round-result completion statement are pending coordinator return. This bounded review reuses the accepted source, model, integration and T-007 numerical reviews; no model execution or regression battery was repeated.

## Checked

- At freeze commit `77bcc96e`, all 233 unique preparation, review, execution and result artifact hashes listed in `snapshot.json` match their current local bytes. The preserved final manifest matches the snapshot's manifest digest.
- The copied `reviews/postexecution-review.md` is byte-identical to the independent goal evidence review. Record §14 now points to that copy and explicitly separates pending snapshot/regression gates.
- The six final discovery rows match the approved dispositions. Each carries status, responsible actor and concrete evidence home. The missing cryogenic inventory closes only for the implemented terms; hardware qualification remains open in the named new seam. No unsupported repair credit or reopened historical defect was found.
- Goal Answered when (a) is supported by the reused WI-058/WI-059 implementation and integration reviews. The committed final study supplies (b)'s required transects, 108 matched points, component channels, comparison cases and sampled feasible geometry. The numerical answer remains supported by the T-007 review.

## Corrections needed

1. **Answer claim-site context and demo coverage.** The frozen `answer.md` omits the goal invariant's held transport/wall-calibration context beside geometry claims and the stored-energy basis/coupling context for feasibility readings. Add the held ash transport ratio 8 and suppression 0.5; wall calibration anchored to 4.05 MW/m² at 2700 MW, R = 12.7 m, a = 1.3 m; and the geometry-scaled WI-042 thermal stored-energy basis with source efficiency 0.5 and coupling 1.0. The standalone demo paragraph also needs the requested fatter-bore cost response and explicit residuals for unprinted per-coil circumference, absolute conductor margin and cross-section-dependent winding effort, by reference where concise. Evidence: goal §Answered when (c) and §Invariants; frozen native input file `preparation/package-inputs/stellarator_plant_params.json`; `work/orchestration/goals/stored-energy-basis/learnings.md` L-004–L-006. This requires a prose correction only.
2. **Snapshot runtime-artifact retention.** Of the listed result artifacts, 181 exist locally but are absent from `77bcc96e`: 179 native JSON artifacts and the baseline/study SQLite databases under ignored `_work` directories. Committed CSV and comparison artifacts support the numerical reading, but a fresh checkout cannot replay every named snapshot hash. Preserve those artifacts in a durable record/archive home or explicitly state the runtime retention limit. Do not claim that every snapshot artifact is committed. This does not require rerunning the study or changing frozen numerical results.

## Remaining completion gates

The coordinator reports 54 record/goal checks passing. The full study/goal-contract suite is running in `evidence/round3-final-tests.log`; its outcome has not yet been reviewed. Final assurance can be appended here after the scoped corrections and test/round-result return. No additional source or numerical review is needed absent a changed result or failure.

## Focused correction recheck — 2026-09-15

**Both identified gaps are resolved. PASS for answer coverage and committed artifact preservation; final suite and round-result assurance remain pending.**

The corrected answer states the held transport, heating efficiencies, WI-042 stored-energy basis and full wall-peak calibration beside its geometry comparison and again in its demo section. The demo now includes the 28.57% winding-procurement increase, total magnet capital change, and explicit per-coil circumference, fit, absolute-margin and cross-section-effort limits with the transfer reference. The numerical claims remain unchanged and retain the earlier review's support.

Commit `c2774de7` preserves the previously ignored 181 artifacts. A direct `git show HEAD:<path>` hash replay checked all 233 unique snapshot-listed artifacts against their frozen SHA-256 values at that HEAD: all exist in the commit and all match. This closes the fresh-checkout preservation gap without changing the frozen snapshot or numerical results. No further correction is required from this focused pass.

## Final round assurance — 2026-09-15

**PASS for the bounded technical completion of Round 3 and goal Answered when (a)–(c).** No further model or numerical work is required by this review. The coordinator may record the accepted learnings and final technical status under the owner's delegated completion instruction. This verdict does not authorize merge, push or unrelated archival work.

The T-007 return and Round 3 result accurately distinguish the frozen study, additive native-artifact preservation and answer correction. Their numerical reading, six landed discovery dispositions and conditional engineering scope match the earlier independent reviews. L-004 and L-005 remain accepted in the bounded forms in `T-007_postexecution_review.md`: refrigeration below 1% applies to nominal named anchors, and zero flips applies to the 159 immediate-entering comparison rows. The proposed learning summaries do not establish an upper bound or general geometry invariance.

The native integration return at `evidence/T-007_integration-r2/integration_return.json` records CANDIDATE with all ten named gates passing and the same semantic/executable fingerprints carried into the study. The trail distinguishes the first request's omitted expected-fingerprint flags from a package defect and names the repaired lineage request. This is consistent with the retained retry evidence and does not disguise an intervening model change.

Read the completed `round3-final-tests.log`: 975 passed, one skipped, two failed and nine warnings in 1061.20 seconds. The two failures concern the injected pipeline line's old hardcoded number and the old nine-group census. Reviewed both corrective diffs: the first derives the actual injected line while retaining exact key-path and token checks; the second expects ten input groups and requires the new magnet-cost file. The complete affected files then pass 52 tests in `round3-consumer-recheck.log`. This is adequate focused verification of these test-only repairs. The trail correctly makes no claim of a clean full-suite rerun.

Residual limitations remain explicit: Level 6 static validation fails with 267 diagnostics, including four added diagnostics on two generated-and-verified EXPOSE references; ten Level 2 literal warnings remain. The study suite's nine warnings report Pydantic serialization of numeric `1.0` for the Boolean inventory control in test fixtures. These are disclosed warnings and scanner residue, not passing results. The native integration manifest gate also explicitly states that `assert_read_set_covered` was not run; its PASS covers the named identity/pin checks only. None of these results qualifies the outstanding physical or cost seams.

No additional concrete gap was found in this completion pass. The final accepted learning entries should preserve the earlier review's evidence, scope and implications; the coordinator owns that landing and final status.

The study record's append-only final preservation/validation addendum was also checked. It accurately names the two preservation commits, qualifies §§3/6 geometry with the retained transport, wall and stored-energy assumptions, and distinguishes the original suite receipt from the 52-test corrective recheck. It changes no frozen snapshot or numerical conclusion. PASS for the addendum.
