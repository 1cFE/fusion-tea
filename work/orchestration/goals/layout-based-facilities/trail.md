# Trail: layout-based facilities

## Round 1 — equipment-and-maintenance-layout

### Strategy revision — 2026-09-18

- **Approach:** [AGENT] Inventory current accounts and equipment/calendar evidence; use the simplest defensible parameterized facility layout supported by admissible source evidence, with explicit assumed clearances and process durations.
- **Assumptions:** Existing reactor/component geometry and replacement schedules can supply useful size and demand drivers; applicable sources may establish facility and handling cost boundaries.
- **Abandonment conditions:** Source evidence cannot justify essential facility/cost transfers; the necessary removal concept changes the plant concept; or capacity conflicts require an owner scientific decision.
- **Intended model increment:** Layout-driven buildings and maintenance facilities replace grouped power estimates where justified, with missing scope separately identified and priced only on an explicit basis.
- **Intended study question:** How do equipment dimensions and maintenance demand change facility size, capacity, plant cost and electricity cost under matched assumptions?

### T-001 scope

- **Objective:** Establish current facility accounts, equipment dimensions, maintenance inputs and admissible internal source coverage.
- **Why now:** The assessment predates completed cooling-equipment work; implementation must start from the actual entering model.
- **Scope:** Read-only model/history/source inventory and native evidence reports; no model changes or external acquisition yet.
- **Inputs:** `goal.md`, original prompt, assessment references, current model, cooling and plant-closure records, source registry; quarantine applies.
- **Done when:** Account/envelope/calendar map and specific evidence gaps support a defensible next task.
- **Stop when:** Barred-source exposure, conflicting active file ownership or a material premise decision needs escalation.

### T-001 start — 2026-09-18

Inventory current accounts and evidence · `evidence/inventory.md`, `evidence/internal-sources.md` · bounded fresh readers with disjoint output ownership. Readers may run in parallel because both are read-only on shared native state; neither may implement changes or acquire/register sources. Coordinator owns all goal records and integration.

### T-002 scope

- **Objective:** Establish an admissible original basis for volume/function facility costs and their installation/services/shielding boundaries.
- **Why now:** T-001 preliminary evidence identifies registered PROCESS defaults with mixed model vintages and inconsistent unit labels; adopting the numbers without tracing actual equations would be unsound.
- **Scope:** Native bounded research acquisition for building cost methods and primary reference basis; no model edits or invented rate calibration.
- **Inputs:** `goal.md`, registered PROCESS cost-variable source and T-001 source-reader findings; quarantine applies.
- **Done when:** Registered evidence supports applicable rates/boundaries with limitations, or a concrete source gap is documented.
- **Stop when:** Acquisition cap, barred candidate, required owner decision or seam prerequisite.

### T-002 start — 2026-09-18

Facility cost-source acquisition · `knowledge/research/requests/REQ-LBF-01.json` · native source/run receipts and `evidence/cost-source-basis.md`. Independent of T-001 read-only inventory; sole registry writer is the cost researcher, coordinator does not register concurrently.

### T-001 return — 2026-09-18

- **Outcome:** COMPLETE.
- **Evidence:** `evidence/inventory.md`, `evidence/internal-sources.md`, `evidence/entering-state.json` (unpinned; no native digest).
- **Reading:** Current facility costs remain power-based after cooling and breeding advances. Source sector-splitting functions support a conceptual layout, while processing times, storage duration and some external equipment envelopes require explicit assumptions. Fourteen is the current circuit count; eighteen is a separately retained study case.
- **Decision:** Evidence supports a bounded native modeling item; [AGENT] coordinator chooses one cohesive facility-layout/capacity/account outcome, with substantial implementation parked pending source/design review. Tier: execution detail. New item/spec follows in T-003.

### T-003 scope

- **Objective:** Specify and design an executable conceptual facility layout, maintenance-capacity screen and cost-account replacement.
- **Why now:** T-001 established available equipment/calendar interfaces and missing inputs; T-002 is resolving the cost-source basis.
- **Scope:** Native work registration, written requirements, explicit proposed layout/capacity equations and assumption table, and a fresh preimplementation review. No substantial implementation until source interpretation and design are reviewed.
- **Inputs:** `goal.md`, T-001 reports, original Stellaris section2.11/Figure54 and relevant radial-build/calendar interfaces; incorporate T-002 when available.
- **Done when:** Reviewer confirms a defensible conceptual design with recorded limitations or identifies a concrete blocking scientific/scope decision.
- **Stop when:** Essential source/geometry/capacity evidence fails or owner judgment is required.

### T-003 start — 2026-09-18

Native facility modeling specification/design · new standard item under `work/active/` · spec, design, persistent implementation checklist and independent source/design review. Requirements can be captured while T-002 runs; cost-dependent conclusions remain provisional until its return.

### T-002 return — 2026-09-18

- **Outcome:** COMPLETE.
- **Evidence:** `evidence/cost-source-basis.md`; `knowledge/research/requests/runs/REQ-LBF-01/20260919T011531965807/return.json`; `knowledge/research/pending/20260918-182124_layout-based-facilities-cost-source-basis.md` (new records unpinned; no native digest).
- **Reading:** Acquisition establishes historical methods and actual boundaries, including a million-fold documentation-unit trap. It does not establish calibrated absolute construction prices. The source reader recommends a commodity method whose reference rows remain missing; independent source review is pending.
- **Decision:** [AGENT] Coordinator pursues the specific missing civil quantity/price rows while layout design continues. Tier: execution detail. Scientific interpretation of historical rates remains provisional; no price method released for implementation.

### T-004 scope

- **Objective:** Acquire original civil quantity/cost reference rows for an installed commodity-based facility estimate.
- **Why now:** T-002 traced the MIT CANES method to missing EEDB/NCET supplemental Account21 data; these could price concrete, reinforcement and formwork without an arbitrary enclosed-volume multiplier.
- **Scope:** Native bounded acquisition of reference quantities, material/labor prices, units, year and services/equipment exclusions. No model edits or resumption of exhausted historical-method searches.
- **Inputs:** `goal.md`, T-002 source report and registered MIT CANES report; specific request REQ-LBF-02.
- **Done when:** Applicable civil rows and exact scope are registered or a bounded specific evidence gap is returned.
- **Stop when:** Request cap, barred candidate, unavailable primary data or required owner decision.

### T-004 start — 2026-09-18

Civil reference-data acquisition · `knowledge/research/requests/REQ-LBF-02.json` · native receipts and `evidence/civil-cost-basis.md`. Sole registry writer remains the cost researcher; independent design and review read stable sources and own different outputs.

### T-004 return — 2026-09-18

- **Outcome:** COMPLETE.
- **Evidence:** `evidence/civil-cost-basis.md`; `knowledge/research/requests/runs/REQ-LBF-02/20260919T012251395930/return.json`; pending services-addendum research report (unpinned; no native digest).
- **Reading:** Exact primary civil quantity/labor/material rows are recovered from pinned source HTML and byte-verified against original CSV. Installed structural commodity rates are available; ordinary-services reference volumes and some unit/applicability details remain explicit gaps.
- **Decision:** [AGENT] Coordinator selects the commodity method for proposed structural pricing in WI-068/design.md, subject to fresh review. Tier: execution detail. The historical whole-building-volume rate is superseded before implementation; the separately sourced ventilation transfer remains provisional.

### T-003 return — 2026-09-18

- **Outcome:** COMPLETE.
- **Evidence:** `work/active/WI-068_layout-based-facilities/spec.md`, `design.md`, `layout-capacity-design.md`, `evidence/layout_capacity_probe.py` and its executed JSON, and `review.md` final preimplementation release. Source reports and native registrations are cited in those artifacts; new records unpinned at return, no native digest.
- **Reading:** Independent review accepts the conceptual source transfers, capacity/event rules, route/opening geometry and account boundaries after B1–B3 repairs. Initial demand, shared cooling transport, late inventory, concrete/formwork ownership and loaded shipping subtraction are explicit. The released design does not qualify actual transport loads, shielding, nonaxisymmetric clashes or complete procurement scope.
- **Decision:** Trigger: positive independent design release. [AGENT] Coordinator proceeds to native implementation because the required conceptual basis is now reviewable and the remaining uncertainties are declared claim limits. Tier: execution detail. Changed: WI-068 design, review and plan; implementation scope below. No owner-reserved gate is exercised.

### T-005 scope

- **Objective:** Implement and independently verify the released facility layout/capacity/commodity-cost design in the actual native model and executable accounts.
- **Why now:** T-003's fresh review released the concrete design after its bounded capacity, route and accounting repairs.
- **Scope:** Canonical/staging model, physical facility components, handwritten implementations, generation, independent oracle/consumer maps, affected regressions, substantive integrated review and a committed package ready for native integration. Study execution and formal closure are separate tasks.
- **Inputs:** `goal.md`, owner prompt, WI-068 spec/design/layout/review/plan, original source registrations and the deposited implementation/oracle/generation briefs.
- **Done when:** Reviewed integrated behavior satisfies the native item acceptance evidence and fixed-point generation/metadata prerequisites, with remaining qualification gaps explicit.
- **Stop when:** A material premise/scope surprise, unresolvable native prerequisite or owner-held decision blocks faithful implementation.

### T-005 start — 2026-09-18

Native WI-068 facility implementation and verification · `work/active/WI-068_layout-based-facilities/`, canonical/staging models and executable package · exact contract, generation/validation evidence and independent integrated review. Continuing layout author owns production models/generation/spine contracts; source researcher owns independent oracle/consumer maps; coordinator owns study-route contract, commits and goal records. Parallel authoring follows a shared published interface and disjoint files; coordinator integrates sequentially. See `evidence/implementation-brief.md` and `evidence/oracle-brief.md` for ownership.

### T-005 implementation checkpoint — 2026-09-18

[AGENT] Canonical model and account wiring transferred to the coordinator during integration; the continuing layout author retained manual facility bodies, geometry tests and generation contracts. The independent oracle author retained separate equations and oracle/consumer maps. The generated candidate passed 836 scalar comparisons, 24 author tests and 39 facility-account/retained-cooling tests; the final spine/oracle run passed 31 tests. These checks are scoped software evidence, not a construction qualification.

The substantive reviewer then reproduced three acceptance gaps: waste-package yield below one reduced storage without authorization; oversized cooling machines could pass a narrower common route; and late initial cooling field deliveries were absent from readiness. The candidate is held for bounded corrective implementation and independent recheck. Production defaults, calendar and physical requirements remain the authority. No native integration candidate or study result has been promoted.

### T-006 scope

- **Objective:** Promote one reviewed native integration candidate and execute the focused facility-response study against it.
- **Why now:** Implementation and its substantive audit have reached bounded repairs; study preparation can proceed independently while release remains held.
- **Scope:** Native integration, qualified axis declaration/indicators, owner-reserved framing ruling, matched and diagnostic cases, immutable native store, independent numerical verification and evidence-linked interpretation. No reveal, archive replacement or formal goal closure.
- **Inputs:** WI-068 reviewed implementation and corrected audit release, actual package identities, owner prompt, study policy and native study runbook.
- **Done when:** One accepted candidate and one committed focused study preserve all scalar/predicate outcomes and support fresh independent R9.S grading.
- **Stop when:** Audit hold, native mechanical refusal, required owner framing decision or material scientific surprise prevents dependent execution.

### T-006 start — 2026-09-18

[AGENT] Study preparation opened at `exploration/stellarator_e2e/studies/20260918-layout-based-facilities/`. No study point has run. Provisional full-group indicators identify construction-rate and ton-unit assumptions as `no_constraint_response`; the coordinator asked the owner to permit those as cost sensitivities only or omit them. Their ruling remains pending. Dependent execution is held; T-005 corrective work continues.

### T-005 return — 2026-09-18

- **Outcome:** COMPLETE.
- **Evidence:** WI-068 `audit.md` final release, `evidence/author-validation.md`, `evidence/final-affected-regressions.log`, complete static delta/classification and fresh-generation/repin receipts. Repaired executable `21d2bda3596ab0df38356bac9e404680ca6a836099a89dc0a2e8f6f73edb9208`; semantic `a913cbcf04a82403d8a7c51e13fc09718596d3dc1557b06c7b583481476cdc4d`.
- **Reading:** Independent audit resolves A1–A3, including fixed door takeoff, actual failed native predicates and unchanged cost/physical control behavior. Forty-three author tests, 307 affected regressions, 836 independent scalar comparisons and exact fresh generation pass. Static L2/L6 failures remain classified; qualifications and missing procurement scope remain explicit.
- **Decision:** [AGENT] Coordinator accepts the corrected implementation release and proceeds to the native integration seam under T-006. Tier: execution detail. The scoped model commit containing this return is the audited work reference. No study point, final grade or owner-held closure is implied.

### T-006 integration checkpoint — 2026-09-18

[AGENT] Accepted native CANDIDATE on the first seam attempt, audited work `work/active/WI-068_layout-based-facilities@f1e70c48`. All ten gates pass. Integration pin `8ee44a9bd02728033cbfe707c024fd0511fd82dc33d22e88091ba45c8a9220aa`; executable `21d2bda3596ab0df38356bac9e404680ca6a836099a89dc0a2e8f6f73edb9208`; semantic `a913cbcf04a82403d8a7c51e13fc09718596d3dc1557b06c7b583481476cdc4d`; TEAx revision `8d877460ac4f6f264561d916e40c1708adb13397`. Evidence: `evidence/integration/integration_return.json` and its deposited baseline, verification and gate receipts. The seam explicitly does not check `assert_read_set_covered`; that known integration limitation remains disclosed.

The study's final42-group indicators and48 candidate proposals are prepared at the accepted pin. Construction-price multiplier and source-ton interpretation remain the only `no_constraint_response` axes. Owner ruling is still pending; no study baseline, oracle scan or candidate execution has run. The definition guards point execution on that ruling. Other implementation, review and integration work is complete. Fresh R9.S grading follows the executed study, not this checkpoint.

### T-006 owner ruling — 2026-09-19

[OWNER-VERBATIM] “yes run both”. The owner approves construction-price and ton-unit sensitivity execution, following the explicit explanation that these affect costs without establishing physical feasibility or an optimum. The two required rulings are captured in the study preparation. [AGENT] Resume the accepted candidate through native study execution and independent grading; no model or physical requirement changes.

### T-006 mechanical retry 1 — 2026-09-19

The native study baseline and all preflight gates pass. Independent scan attempt1 evaluates47 of48 unchanged proposals and refuses `no-sector-replacement` because the supported first-wall fluence-limit input is absent from the oracle public override map. Classification: MECHANICAL_FAILURE, bounded verification-interface repair; scientific scope, package identity and cases remain unchanged. Original scan retained in `results/oracle-scan-attempt1.json`. The independent oracle author owns the added mapping and checks; no production model or accepted integration pin changes. Retry only after confirming the mapping reaches the existing lifetime operand.

### T-006 start — 2026-09-19

Verification retry2 after bounded checker correction. Trigger: one no-event outage-margin scalar disagreed among40128 comparisons; all1200 predicate statuses agreed. [AGENT] The independent reviewer accepts the existing production horizon sentinel when no recurring campaign exists, with required/allowed values retained as hypothetical and initial readiness still enforced. The coordinator accepts the oracle correction and explicit contract clarification; tier: execution detail. Package, native cases, inputs and physical criterion remain unchanged, so this is a MECHANICAL_FAILURE repair to the verification implementation. Failed evidence is retained; rerun the independent scan and verification only, not native execution. Evidence: study `reviews/no-event-verification-repair.md`, oracle42-test return, amended facility contract.

### T-006 retry notation amendment — 2026-09-19

[AGENT] The earlier “T-006 mechanical retry 1” entry records the first retry start, before the mapper repair. It should have used the canonical `T-006 start` heading. This amendment preserves chronology rather than rewriting it. Retry 1 repaired the supported operand map; retry 2 repaired the no-event checker branch. Both retained the same task, package, proposals and conceptual criterion. The pre-commit CSV arm-column correction was record assembly, not another native execution or verification retry; the rejected candidate snapshot and original export are retained.

### T-006 return — 2026-09-19

- **Outcome:** COMPLETE.
- **Evidence:** Native candidate pin `8ee44a9bd02728033cbfe707c024fd0511fd82dc33d22e88091ba45c8a9220aa`; immutable study `exploration/stellarator_e2e/studies/20260918-layout-based-facilities/@5f97d5f2`; snapshot SHA256 `af668e7ac5f57041787b6e5d5c08aa3ccf5bc2de006062e681daf9323e547455`; substantive independent `evidence/final-review-and-grade.md`. The actual native execution used repository `3fa479ed`; checker correction `0e6a2b2b` changed no package or native case. The snapshot records both identities and source digests.
- **Reading:** All 48 cases completed; 40,128 scalar and 1,200 predicate comparisons pass. Both matched controls reproduce 380 entering outputs and preserve 662 physical/calendar/layout outputs plus all 25 predicates. Twenty cases fail facility screens; no whole-plant pass is claimed. The independent unchanged-rubric grade is R9.S3, PASS. Price and historical-tonne assumptions were run only after the owner's explicit ruling.
- **Decision:** Trigger: executed response and independent acceptance support the required conceptual increment. [AGENT] Coordinator accepts the study and seven finding dispositions because they retain demonstrated behavior, source uncertainty and failed cases without changing scientific scope. Tier: execution detail. Changed: committed study, `answer.md`, `study-reading.md`, WI-068 plan and joined discovery rows. Formal closure and archival remain owner-held.

### C-001 disposition checkpoint — 2026-09-19

[AGENT] PASS using the continuing independent non-author review in `evidence/final-review-and-grade.md`, also captured in the committed study. All seven proposed findings are accepted: procurement uncertainty, TN ambiguity, qualifications/provisionals, adverse logistics, unpriced scope and two resolved checker-interface defects. Every finding retains its original ID and concrete home; the discovery log receives joined disposition rows. No semantic follow-up is proposed. The three AGENT learning deltas are accepted for the round check. This review also covers the actual source/account/layout increment and executed response; another session would duplicate that coverage.

### Round 1 result — 2026-09-19

- **Intent:** Met. The unchanged R9.S3 target is independently supported by the actual layout-driven building set, hot-cell functions, handling routes/capacity, scoped sourced costs and executed response. The eight owner results are mapped in `evidence/completion-check.md`.
- **Task sequence:** T-001 inventoried current accounts and upstream evidence; T-002 and T-004 acquired and examined original cost sources; T-003 specified and independently reviewed the design; T-005 implemented, generated and independently audited the native package; T-006 promoted one candidate and committed one focused study.
- **Last semantic outcome:** COMPLETE. Stop reason derived from that outcome and the goal's answered-when criterion: the requested technical answer is demonstrated; recommend owner-held formal closure. No further technical round is required for this target.
- **Evidence:** Model `f1e70c48`, integration checkpoint `517fb9a6`, checker repairs `3fa479ed` and `0e6a2b2b`, frozen study `5f97d5f2`, final independent grade, `answer.md` and preserved r2/rubric checks. No historical study, rubric, maintenance requirement or availability interface was rewritten.
- **Finding dispositions:** Seven joined rows retain procurement/source/qualification/logistics/unpriced-scope limits and resolve the two checker defects. No open touched finding is left unrouted; continuing evidence homes are the goal, WI-068 and named oracle/contract files.
- **Learning delta:** Accept proposed L-001 through L-003 after the closure coverage check: controlled cost comparisons, dated shared-resource logistics and behavioral counterexamples beyond equation agreement. These remain AGENT findings, not owner-originated requirements.

### Round 1 review — 2026-09-19

**Coordinator check; existing independent review reused, no additional review session required.** The continuing non-author reviewer supplied substantial original-source/design/account assurance, repaired native integration audit, final 48-case interpretation and fresh unchanged-rubric R9.S3 grading. The final custody addendum verifies committed study `5f97d5f2`, all 213 file hashes, the schema-only CSV repair and all 48 native-store joins. Source/model/scope/environment identities remain applicable; no uncovered scientific or integration change followed those reviews.

The coordinator checked the written result against all six task scopes and the eight owner deliverables. Both execution/checker retries kept package, inputs, scope and scientific meaning; the pre-commit export correction changed metadata only. One pin and one study were promoted. Every touched finding has its accepted disposition and responsible home in the appended discovery rows. No native artifact moved outside its recorded task; historical studies, rubric and r2 remain unchanged. All three proposed AGENT learnings are accepted and appended to `learnings.md` now.

The technical question is answered at the requested conceptual level. Recommend owner-held formal closure when the owner accepts the delivered answer. No next technical round is needed to support R9.S3. Physical qualification, source-unit resolution and complete installed handling/services procurement remain explicit future engineering work. No reveal, replacement-freeze, archival, merge or push was performed.

## Goal closure — 2026-09-19

[OWNER-VERBATIM] “please close the goal”. The owner authorizes formal closure following the delivered answer and independent R9.S3 PASS. [AGENT] Coordinator marks the goal closed on the completed Round 1 result and review, committed study `5f97d5f2` and final answer/review checkpoint `f5362b26`. The technical target is met; the recorded physical-qualification and incomplete-procurement limitations remain. This owner decision exercises the formal goal-close gate. Goal status, answer and current-work summary are updated; frozen study evidence remains unchanged. Item archival and other reserved gates are separate.
