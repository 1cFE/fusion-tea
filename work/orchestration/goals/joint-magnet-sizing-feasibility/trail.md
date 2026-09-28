# Trail: Joint magnet sizing and feasibility

## Round 1 — inventory-derived-sizing

### Strategy revision — 2026-09-15

- **Approach:** Derive required inventory from actual-field tape capacity; express it through the existing physical inventory coordinate if sufficient, and compare resulting pack demand against independent allocations with every existing plant consequence.
- **Assumptions:** Existing fixed-construction inventory law may support coherent sizing without changing production equations. Default performance is held; enhanced scenarios remain separate.
- **Abandonment conditions:** An unmodeled dependency invalidates the intended comparison or the existing coordinate cannot represent one consistent inventory.
- **Intended model increment:** Only behavior required for coherent joint sizing; none if a reviewed study-level inversion of existing equations suffices.
- **Intended study question:** Does any bounded sampled default-performance geometry accommodate current-sized inventory and satisfy all existing predicates, and what limits/costs result?

### T-001 scope

- **Objective:** Map coupled requirements, variable roles, existing evidence and the simplest consistent sizing formulation.
- **Why now:** Separate historical fit and current failures do not answer joint sizing.
- **Scope:** Read current equations, original admitted evidence and prior records; derive interfaces and missing-dependency limits. No production changes or scientific sweep yet.
- **Inputs:** goal.md; entering current, fit, procurement, thermal/support and manufacturing models and their audited sources.
- **Done when:** A traceable map and reviewed formulation determine whether production changes are necessary.
- **Stop when:** Prerequisite, strategy blocker, owner gate or declared limit.

### T-001 start — 2026-09-15

T-001 · existing model/evidence assessment · evidence/coupled-requirements.md.

### T-001 return — 2026-09-15

- **Outcome:** COMPLETE.
- **Evidence:** evidence/coupled-requirements.md; evidence/coupled-dependencies.md (assessment in progress); work/active/WI-064_current-driven-magnet-inventory-sizing/spec.md, unpinned; no native digest yet.
- **Reading:** Existing allocation-first field calculation permits acyclic current sizing. A native derived-density selector is necessary to internalize inventory demand under STUDY_POLICY; no outer solve or new empirical law is needed.
- **Decision:** Missing current-driven inventory behavior · register WI-064 with optional sizing and mode0 preservation · execution detail · coordinator under owner autonomy · native item/spec. Scope selected-field ceiling remains24.9T in principal comparisons; historical30T cases are controls only.

### T-002 scope

- **Objective:** Implement and verify optional native current-driven tape/pack sizing with preserved entering behavior.
- **Why now:** T-001 identifies the missing causal calculation and acyclic insertion point.
- **Scope:** WI-064 native model/generated/oracle consumers, focused tests, affected regression, metadata and independent coupled audit; no acceptance changes or new material normalization.
- **Inputs:** goal.md; WI-064 spec; entering revision c4d720db886213de94bf2dc4c3131a3453dca690; T-001 map and inherited source reviews.
- **Done when:** Reviewed native/generated/oracle agreement and current-package preservation support integration.
- **Stop when:** Prerequisite, strategy blocker, owner gate or declared limit.

### T-002 start — 2026-09-15

T-002 · WI-064 · reviewed specification, implementation and independent audit; focused source/design reviewer dispatched before implementation.

### T-002 return — 2026-09-15

- **Outcome:** COMPLETE.
- **Evidence:** work/active/WI-064_current-driven-magnet-inventory-sizing/audit.md@a8589d6b; evidence/implementation-review.md@a8589d6b.
- **Reading:** Optional native sizing closes current-driven inventory and preserves the entering mode. Fresh independent coupled review PASS; static L2/L6 limitations remain explicit.
- **Decision:** Reviewed calculation and consumer evidence · proceed to native integration · execution detail · coordinator · audited WI-064 at a8589d6b. No acceptance change.

### T-003 scope

- **Objective:** Obtain one reproducible study-ready candidate for reviewed WI-064.
- **Why now:** Implementation and independent audit are complete.
- **Scope:** Native integration seam, exact expected lineage and all ten gates; no semantic model changes.
- **Inputs:** goal.md; WI-064@a8589d6b; current manifest and sealed runtime.
- **Done when:** Native CANDIDATE or named blocker.
- **Stop when:** Prerequisite, strategy blocker, owner gate or declared limit.

### T-003 start — 2026-09-15

T-003 · scripts/integrate.py · evidence/T-003_integration/integration_return.json.

### T-003 return — 2026-09-15

- **Outcome:** COMPLETE.
- **Evidence:** evidence/T-003_integration/integration_return.json (pending local evidence commit); audited implementation a8589d6b.
- **Reading:** All ten native gates pass. Candidate pin0a1c038663c848e11cff933215a8d15eb96b6650319003b9cf092ecbbc40e52c, executable8e4aa8eaebf2667a74565e6e66fc9ce5947c6d27ccfc210f8452e82d87fba45f. Inherited assert_read_set_covered omission remains disclosed, with no claimed substitute.
- **Decision:** CANDIDATE · promote this sole Round1 pin and release bounded study preparation/scan · execution detail · coordinator · study20260915-joint-magnet-sizing.

### T-004 scope

- **Objective:** Establish bounded default-performance joint sizing/fit/plant feasibility and separated scenario/cost consequences.
- **Why now:** Reviewed native inventory sizing and integrated package are available.
- **Scope:** Native run-study on one pin; reference/prior controls, bounded geometry scan, fixed prepared-list native cases, small performance/construction sensitivities and independent verification. No acceptance relaxation.
- **Inputs:** goal.md; T-003 candidate; exploration/stellarator_e2e/studies/20260915-joint-magnet-sizing/protocol.md; current existing source reviews.
- **Done when:** Frozen native study record with all predicates, retained refusals, sizing residuals, entering attribution and qualified synthesis.
- **Stop when:** Prerequisite, strategy blocker, owner gate or declared limit.

### T-004 start — 2026-09-15

T-004 · native run-study · exploration/stellarator_e2e/studies/20260915-joint-magnet-sizing/.

### T-004 return — 2026-09-15

- **Outcome:** BOUNDED_NEGATIVE.
- **Evidence:** `exploration/stellarator_e2e/studies/20260915-joint-magnet-sizing/record.md`, `report.md`, `synthesis.md`; snapshot SHA256 `330e0ac2411ce50ff59bd109bcce8c18a5c3d97141cb013a7b870c1689990154`; native implementation `a8589d6b`. The frozen evidence commit is joined below before fresh review.
- **Reading:** All 347 native cases completed; 75,646 scalar and 6,940 predicate comparisons agree. Of 324 default current-sized cases, 324 pass current, 154 pass fit and none passes the other eighteen predicates or all twenty. Sixteen performance scenarios and two shape diagnostics also have no combined pass. The one historical 30 T/orientation-3 control pass is outside main-limit acceptance. No default or enhanced cheapest feasible choice exists in this sample.
- **Decision:** Bounded negative technical answer meets the owner's successful adverse-result contract · commission final frozen-evidence/disposition/round assurance · execution detail · coordinator · answer.md and evidence/final-review-brief.md. Required space is not available-space evidence; current closure is conditional consistency. Wider search remains possible, not required to force a pass.

### Round 1 result — 2026-09-15

- **Intent:** Met within the bounded investigation. One native current-derived inventory now drives capacity, pack and procurement; independent allocation and existing consequences are evaluated coherently. No sampled default joint-feasible region was found.
- **Task sequence:** T-001 coupled map/source-design review → T-002 WI-064 implementation and independent coupled audit → T-003 ten-gate integration candidate → T-004 fixed native cohort, frozen evidence and executor reading.
- **Last semantic outcome and stop reason:** BOUNDED_NEGATIVE. Stop this strategy because the scoped stages and answer contract are complete; the owner explicitly accepts a supported adverse result. No retry limit or owner gate was used to truncate the scientific work.
- **Evidence:** answer.md; the T-004 native record/report/synthesis and snapshot above; WI-064 audit; evidence/source-design-review.md, implementation-review.md and window-review.md; evidence/finding-dispositions.md. One promoted pin and one frozen study only.
- **Proposed learning delta:** L-001 allocation-first acyclic sizing and reevaluation of allocation; L-002 exact-current closure and physical reserve; L-003 finite no-pass reading separated from qualification. Exact proposed statements are in evidence/finding-dispositions.md. None is accepted before fresh review.
- **Finding dispositions:** Thirty-one prior IDs plus seven new sightings have explicit proposed model-extension or declared-seam dispositions. Executor first sightings are appended; reviewed joined updates remain pending. No prior adverse finding is overwritten.
- **Retries and boundedness:** Routine harness/path/receipt repairs retained the same task meaning. The exact multiplier-one sign difference is retained as a diagnostic outside the predeclared 1.01-reserve cohort, not silently corrected. The justified oracle refinement and sensitivity selection occurred before the one fixed native execution; 347 unique cases remain below the 400 cap.
- **Remaining uncertainty:** Construction and local-angle performance, >24 T extrapolation, physical accommodation, missing field/shape/casing physics, detailed qualification and factory/price completeness. No global infeasibility or optimum. Final fresh review checks scientific meaning, artifacts, every touched disposition and proposed learnings; formal goal closure/archive remain owner-held.

### Round 1 review — 2026-09-15

- **Reviewer and verdict:** Fresh nonauthor reviewer; **PASS**. [Final review](evidence/final-review.md) covers frozen study `02af7123`, snapshot `330e0ac2411ce50ff59bd109bcce8c18a5c3d97141cb013a7b870c1689990154`, the bounded answer, all 38 finding dispositions and three learning deltas.
- **Checks and reused evidence:** Reused source/design, coupled implementation and fixed-window reviews at unchanged scope. Independently checked all 511 artifact hashes and 518 required retained files, native store joins, 5,552 sizing/fit/threshold identities, 75,646 current scalar and 73,564 entering-attribution comparisons, and 6,940 exact predicates. Fresh frozen-oracle replays cover five varied current points and all five entering controls. The prepared-list digest exactly matches the preexecution approval.
- **Corrections:** Clarified that the retention sensitivity is one joint 0.9³ scenario. Clarified reference versus set-effective tape normalization. Preserved historical closed/resolved findings as closed/resolved, with no new work owed. Frozen numerical evidence is unchanged.
- **Finding dispositions:** Seven committed executor sightings and 38 accepted joined updates are in `exploration/stellarator_e2e/studies/DISCOVERY_LOG.md`. No first sighting was edited. Earlier adverse findings remain historical evidence. Open material, geometry and manufacturing limits remain declared seams.
- **Learning delta:** L-001, L-002 and L-003 accepted and appended to learnings.md. No qualification, global infeasibility or global optimum claim accepted.
- **Remaining uncertainty and recommendation:** The bounded negative answer satisfies the contract. Technical execution is complete; recommend owner-held formal goal closure and WI-064 archival. No additional round is necessary to force a pass. No merge or push.
- **Coordinator completion check:** After appending accepted dispositions, all 68 study-record/template/goal-contract tests pass. All 42 local presentation links checked in goal artifacts and current-work state resolve. Changes after independent PASS only publish accepted joins and clarify review status; native code and frozen study evidence are unchanged. Earlier completed/resolved findings retain their status. Additional scientific review would duplicate valid coverage.
