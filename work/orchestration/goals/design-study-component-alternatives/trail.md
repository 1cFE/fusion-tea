# Trail: Matched steam and helium Brayton component alternatives

## Round 1 — supported-common-boundary-screen

### Strategy revision — 2026-09-26

- **Approach:** [AGENT] Audit the steam interface, Brayton return closure and cost inventories against C-1 and C-3; choose the largest physically defensible common boundary before numerical economic ranking.
- **Assumptions:** Existing definitions may support a matched isolated-loop comparison with modest integration. Compatibility in MW alone is insufficient.
- **Abandonment conditions:** A missing physical relationship or unsupported equipment/cost boundary requiring a major new model invalidates this strategy; preserve a bounded negative and state economic criteria unmet.
- **Intended model increment:** None during the audit; later justified additive assembly only if evidence supports it. MR-7 quantities remain chosen/calculated as explicitly recorded in the comparison contract.
- **Intended study question:** Can either source boundary support a fair steam/Brayton performance-and-cost study using existing definitions and bounded repairs?

### T-001 scope

- **Objective:** Establish source/interface/cost readiness and exact gaps for a matched component comparison.
- **Why now:** The predecessor established partial reuse, deferred C-3 and exposed fixed steam and missing-cost assumptions.
- **Scope:** Read-only bounded audits, goal-owned evidence and a recorded screen if needed; no shared model/package changes or external retrieval.
- **Inputs:** `goal.md`, owner brief, compatibility map, WI-093 report, parameter-study return closure, existing reviewed bodies and source traces.
- **Done when:** A supported comparison boundary and inventory are identified, or specific blocking gaps establish a bounded negative.
- **Stop when:** A prerequisite, strategy blocker, owner gate or declared limit is established.

### T-001 start — 2026-09-26

T-001 · existing native model and study evidence · expected steam-interface-audit.md, brayton-interface-audit.md, cost-audit.md and screening assessment.

Parallelism judgment: the three audits answer independent questions and may invalidate only subsequent integration scope, not each other's read-only investigation. Each worker owns its named evidence file; the coordinator owns the goal/trail and integrates sequentially. Workers preserve all other edits.

### T-001 return — 2026-09-26

- **Outcome:** COMPLETE.
- **Evidence:** `evidence/steam-interface-audit.md`, `evidence/brayton-interface-audit.md`, `evidence/cost-audit.md` (unpinned; no native digest at return); comparison contract and fresh feasibility review in preparation.
- **Reading:** A supplied Stellaris-like isolated source is viable in principle. Duty variation at fixed temperatures preserves steam's offered temperature conditions. Costs need disjoint package treatment, and Brayton cooling needs finite heat-transfer and pumping evaluation. The audits do not establish an economic ranking or justify declaring a major-model blocker.
- **Decision:** Trigger: the source-interface and inventory gaps are identified. Decision/reason: pursue a bounded native design with explicit roles and cooler/accounting checks because existing thermodynamics can support it. Tier: execution detail. Decided by: coordinator, using audits and pending fresh review. Changed: `comparison-contract.md`; no model/package changed.

### T-002 scope

- **Objective:** Specify and design the smallest physically checked matched conversion-subsystem assembly and its cost boundary.
- **Why now:** T-001 supports an isolated source but exposes missing Brayton cooling and ambiguous aggregate cost treatment.
- **Scope:** Native WI-096 spec/design and bounded package diagnostic controls; implementation only after applicable fresh design review. Preserve all shared packages and historical studies. No major new physical model or external source access.
- **Inputs:** `goal.md`, `comparison-contract.md`, three audits, fresh feasibility review, MR-7, existing steam, Brayton, counterflow and water-rejection definitions.
- **Done when:** A reviewed design can execute a conditional fair comparison, or an exact unsupported interface/cost dependency establishes a bounded negative.
- **Stop when:** Required physical behavior exceeds a modest justified extension, a reserved owner gate or a declared limit is reached.

### T-002 start — 2026-09-26

T-002 · native WI-096 Matched Conversion Subsystems · expected native spec/design, independent design review and diagnostic receipts. Process deviation: `pm add-item` registered WI-096 immediately before this start entry; no modeling work had started. The coordinator records this ordering error rather than implying the start preceded that native side effect.

### Checkpoint C-001.r1 — 2026-09-26

- **Reviewer:** fresh non-author `/root/feasibility_review`; brief `evidence/feasibility-review-brief.md`.
- **Reading reviewed:** three bounded audits and `comparison-contract.md`; no main-study reading yet.
- **Dispositions reviewed:** run native readiness diagnostics and design a supplied-source conversion assembly; do not infer a major-physics blocker from missing current checks.
- **Verdict:** FINDINGS, release bounded diagnostics and design only; main study remains unreleased. `evidence/feasibility-review.md` identifies source-return, cooler terminal/capacity, generator-loss rejection and monetary-basis conditions.
- **Revision:** first submission. The coordinator applies the conditions in the WI-096 author brief. Native diagnostic results are in `evidence/readiness-screen.md` and `.json`; 822 retained Brayton outputs replay exactly, two steam refusals are preserved, and temperature/rating failures reproduce. The proposed new assembly remains MR-7 unverified until design and behavior checks.

### Checkpoint C-002.r3 — 2026-09-26

- **Reviewer:** same fresh non-author `/root/feasibility_review`; native design review evidence reused, no duplicate critic.
- **Reading reviewed:** final WI-096 spec SHA256 `8995a896c3c6469ff8dc7e501f71ab32bdfcb8b2a3c68bf60215dd5cb8e08eff`, design SHA256 `a3af34cb5b56e76d7f472d4e3ed414b12eab36c5bb3b5edabca630101775d154`, original loop/exchanger/pump/property/cost sources and STUDY_POLICY §§3–5.
- **Dispositions reviewed:** implement the matched conversion design with external source-heat and Brayton-ratio matching policies.
- **Verdict:** FINDINGS, no implementation release. `evidence/design-review.md` records all three native submissions: initial findings; conditional pass after the first revision; final source-coupling revision with newly identified policy conflict. This goal checkpoint records that native review sequence at return, not three invented prior trail events.
- **Changes:** pump count/ratings, variable-property cooler integration, disjoint cost assumptions and source-loop consistency were corrected. The coordinator's final policy check exposed that the external equality solves conflict with STUDY_POLICY §5.3; the reviewer confirmed the conflict. Public-input replay preserves MR-7 roles but does not discharge the physical-closure rule. Prior agent-reviewed ratio-search practice is not an owner waiver.
- **Remaining uncertainty:** separate model-owned source, ratio and water solves would trigger the policy's third-handwritten-rung tripwire. That is a design-scope decision, not proof of major new physical modeling. No implementation, integration seam or main study has run. MR-7 proposed hardware roles are compliant; executed behavior is unverified.

### T-002 return — 2026-09-26

- **Outcome:** OWNER_GATE.
- **Evidence:** WI-096 `spec.md` and `design.md`; `evidence/design-review.md`, `source-coupling-probe.json`, `monetary-basis.md`, `currency-conversion.md`, and retained native readiness controls. The spec/design hashes above identify the reviewed state; earlier controls are committed in `55eb24b8058057b218f6519565b78165a83dddf9`.
- **Reading:** Source/exchanger consistency has a bounded numerical demonstration and the component/accounting design is explicit. A compliant main-study closure remains unresolved. The task has not delivered an implementation-ready design, and the economic comparison remains unmet.
- **Decision:** Trigger: final permitted design submission has an unresolved study-policy conflict. Decision/reason: stop dependent implementation at the declared review cap; recommend an additional model-owned-closure design revision only if the owner permits continuation. Tier: reserved gate. Decided by: coordinator applying the runbook cap and independent verdict. Changed: `answer.md`, `candidate-ledger.md`, `evidence/findings-log.md`, and the stop record below; no model/package/study changed.

### Stop — 2026-09-26

- **Kind:** cap.
- **Unresolved disposition:** implementation and study release for the external source-heat and Brayton-ratio equality solves.
- **Limit reached:** two corrective design revisions, three submissions. The final submission returned FINDINGS. No mechanical retry was consumed, and no new round is opened to evade the cap.
- **Owner decision needed:** whether to allow another design revision addressing model-owned closure and the handwritten-solve tripwire, or retain this partial result. The proposed remedy is not permission to waive the physical-closure policy or begin implementation before review.
- **Parked work:** WI-096 implementation, generated package, integration, main comparison study, sensitivity cases, economic ranking and result plots. Reporting and reproducibility of already executed diagnostics are completed in the partial-result artifacts.
- **Handoff:** `answer.md` states established evidence and unmet criteria; `evidence/replay.md` names diagnostic commands; `evidence/partial-result-review.md` checks reporting only. Formal goal and item closure remain owner-held.

### Owner continuation — 2026-09-26

[OWNER] `evidence/owner-direction-fourth-submission.md` extends the exhausted design cap by one submission. The earlier cap stop is lifted only for that revision and independent review. No policy exception, automatic sizing or silent change in variable roles is authorized. If the design passes within bounded scope, continue implementation, integration, study and final review autonomously. Otherwise stop with the exact unresolved requirement; no new round may bypass the cap. Formal closure remains owner-held.

### T-003 scope

- **Objective:** Resolve the physical-equality ownership, MR-7 roles and bounded-scope assessment in WI-096's final authorized design revision.
- **Why now:** The owner permits one extra submission after the external-closure policy finding.
- **Scope:** Native spec/design correction and bounded design diagnostics, followed by the same independent reviewer's recheck. No implementation before a passing review. Preserve all historical diagnostics and original model/package bytes.
- **Inputs:** `goal.md`, owner continuation, final submission-3 review, WI-096 spec/design, original component definitions/bodies, MR-7 and STUDY_POLICY §§3–5.
- **Done when:** Submission 4 passes independent review within authorized scope, or an exact remaining requirement establishes the mandated stop.
- **Stop when:** Review fails; scope requires a major physical model or policy exception; another owner gate is reached.

### T-003 start — 2026-09-26

T-003 · WI-096 final design revision and independent review · expected revised spec/design with equality/role table, full addition/solver census, review verdict and exact evidence. The continuing author owns native spec/design; the independent reviewer owns its review. Coordinator owns trail and contract. These stages are sequential because the review depends on the finished design.

### Checkpoint C-002.r4 — 2026-09-26

- **Reviewer:** continuing independent `/root/feasibility_review`; owner-authorized fourth submission, brief `evidence/fourth-submission-brief.md`.
- **Reading reviewed:** spec SHA256 `b7e021efe1c9bca12431879c5eddc541966469ef0a824283ee3629a65c78068c`, design SHA256 `ec7d08e01ec0702e33ac6589dfaaa1a4eec5edad565c5be7bf9dc22c92c03f91`, comparison contract, original component bodies and separate retained fourth-submission probes.
- **Dispositions reviewed:** keep chosen source power, flow, pressure ratios and installed offers; reuse model-owned primary bypass controls; add the reviewed finite-water-cooler calculation and bounded algebra/accounting.
- **Verdict:** PASS for conditional design and bounded implementation scope; `evidence/design-review-fourth-submission.md`. No policy exception is required. No fifth design submission is authorized.
- **Evidence and limits:** independent checks reproduced 12 source-control cases, a failed steam source retaining its 25.5988938 MW deficit, gas source/controller joins and three cooler profile integrals. Five substantive new/modified bodies are counted; only one is a newly written R3 closure, used three times. Existing network and bypass algorithms remain unchanged. MR-7 design roles are compliant; implementation is unverified. Imposed controller pressure service, actual hydraulics, prices and low-grade loss cooling remain conditional.

### T-003 return — 2026-09-26

- **Outcome:** COMPLETE.
- **Evidence:** C-002.r4 and its exact reviewed identities; owner direction; `evidence/fourth-submission-control-probe.{py,json}`, `fourth-submission-thermal-probe.{py,json}` and `fourth-submission-thermal-revised-offer-probe.json`.
- **Reading:** Physical equalities now have model owners while chosen source heat/pressure ratio/equipment remain visible. The existing control action admits sufficient hardware and retains failures. The complete extension fits the reviewed bounded scope without a solver-policy waiver.
- **Decision:** Trigger: fourth-submission independent PASS within authorized scope. Decision/reason: release native implementation because the owner explicitly authorized autonomous downstream execution after this gate. Tier: execution detail. Decided by: coordinator under owner direction and independent review. Changed: revised WI-096 spec/design, comparison contract and implementation brief; no new model/package exists yet.

### T-004 scope

- **Objective:** Implement and validate the reviewed matched conversion package, preserving chosen equipment and failed physical cases.
- **Why now:** C-002.r4 passes the design and scope gate under the owner's continuation.
- **Scope:** WI-096 plan/implementation and acceptance evidence; isolated additive models/package and study support; model-family source registration. No broad study, original-package mutation or unreviewed additional physics/solver.
- **Inputs:** `goal.md`, owner continuation, exact submission-4 spec/design, independent review, comparison contract and `evidence/implementation-brief.md`.
- **Done when:** Native package, design-role behavior checks, independent numerical checks, six-level validation and preservation evidence are ready for independent integration review, or an exact scope/model dependency is established.
- **Stop when:** Another coupled solve, major physical model, changed scientific premise or policy exception is needed; an owner gate is reached.

### T-004 start — 2026-09-26

T-004 · WI-096 implementation through native model workflow · expected checklist, additive SysML definitions/assembly, isolated generated package, body/census/fixed-point evidence, complete input/output/check interface and verification report. Continuing author owns implementation paths in the updated brief; coordinator owns trail, commits and dated studies. Original 13,215-file preservation baseline applies.

### T-005 scope

- **Objective:** Independently assess whether the implemented conversion package and proposed study meet the reviewed physical, accounting, MR-7 and bounded-scope requirements.
- **Why now:** The corrected native development runs independently reproduce 872 scalar channels and all 84 predicates; remaining author work concerns two constraint-label identities and validation reporting.
- **Scope:** Substantive integration and study-framing review against original evidence. No main-study execution, new design submission, toolkit waiver or formal closure. The stock integration seam remains a subsequent executable gate.
- **Inputs:** `goal.md`, fourth-submission PASS, `evidence/integration-review-brief.md`, WI-096 implementation and validation receipts, package/source commits `b5269722` and `b4c896ce`, and declared study offers/axes. The final label-only correction and its exact identity map must be checked before a release verdict.
- **Done when:** The independent reviewer records PASS for the actual final implementation and study framing, or names exact unresolved requirements.
- **Stop when:** A major physical model, extra coupled solve, policy exception or unreviewed scientific premise is required; a required review fails with an unresolved design-level dependency.

### T-005 start — 2026-09-26

T-005 · independent integration review by continuing non-author `/root/feasibility_review` · expected `evidence/implementation-integration-review.md`. The reviewer owns only that artifact and reads the native evidence. T-004's author finishes the two label corrections and reporting in parallel; these changes leave the physical equations and reviewed choices unchanged. Coordinator supplies the final exact identities for the reviewer's release check and integrates task returns sequentially. No study point is released during this overlap.

### T-004 return — 2026-09-26

- **Outcome:** COMPLETE, ready for substantive integration review; main study not released.
- **Evidence:** WI-096 `report.md` SHA256 `bbdb17cd99cbe71bcd064ada3bb2f0d58564e369f80ef10b4bb92bdc32b34534`, completed `plan.md`, `evidence/independent-verification-final.json`, `constraint-identity-check.json`, `implementation-census-final.json`, `validation-detail.md/.json`; package commits `b5269722`, `b4c896ce`, `d323fc07`; goal `evidence/original-preservation-after-implementation.json`.
- **Reading:** The isolated model contains the reviewed five substantive additions/variants and one new iterative cooler calculation. All required coupled physical calculations are model-owned. Source power, ratios and equipment remain chosen. The final native interface has 490 inputs, 876 scalar channels and 84 executing constraints. Seventeen evaluated development cases independently match 872 scalar channels and all 84 predicates; four solver iteration counts are diagnostic-only. One expected water-property refusal and all earlier failed attempts remain retained. Regeneration is an exact fixed point; all 13,215 original protected files are unchanged.
- **Validation limits:** The six-level validator is not wholly green. It retains 72 L2 literal warnings and 766 L6 alias diagnostics, mapped individually to generated/native evidence; a widened diagnostic scan is retained separately. Independent review must assess that disposition. Native checks establish behavior, not hydraulic, off-design machinery or procurement qualification.
- **MR-7:** Implementation role/behavior evidence is compliant with the reviewed direction: no source-power or ratio solve, no equipment demand-to-purchase sizing. Controller flow/fraction and cooler water flow are calculated operating states under the reviewed rationale. Independent integration assessment remains T-005.
- **Decision:** Trigger: completed native implementation and independent numerical/predicate evidence. Decision/reason: accept T-004's bounded implementation handoff and continue T-005 because the owner authorized downstream work after the fourth-design PASS. Tier: execution detail. Decided by: coordinator. Changed: new model/package, tests/model_families.py append, native WI-096 evidence, and study interface/manifest preparation. No original model/package was changed and no integration candidate or main study has been promoted.
- **Corrective evidence:** Eighteen omitted Boolean guards were expressed through supported existing numeric screens; ledger residual comparisons now consume model-produced magnitudes; two assertion labels were lowercased to align native identities. Recorded regressions preserve prior numerical results and physical verdict meanings. These are implementation/tooling representation repairs within the reviewed design, with no new physical relationship or policy exception.

### T-005 return — 2026-09-26

- **Outcome:** COMPLETE.
- **Evidence:** `evidence/implementation-integration-review.md`, independent `/root/feasibility_review`, reviewing WI-096 at `29dcb5d8` and the exact current executable/semantic identities.
- **Reading:** PASS for implementation and proposed study framing. The reviewer independently replayed 14,824 scalar comparisons and 1,428 predicates, checked the final identity map, modeled choices, source joins, retained failures, selected energy/cost arithmetic and the static-diagnostic disposition. No unresolved implementation requirement, extra physical solve or policy exception remains. MR-7 implementation is compliant within the reviewed conditional scope.
- **Decision:** Trigger: substantive independent integration PASS. Decision/reason: proceed to the stock integration seam and declared study under the owner's autonomous continuation. Tier: execution detail. Decided by: coordinator under the independent verdict. Changed: review artifact and one study-plan wording correction identifying frontier coefficients as transparent report arithmetic from native cost/energy outputs. Formal closure and final economic-result review remain outstanding.

### T-006 scope

- **Objective:** Execute and verify the matched comparison and its declared sensitivities on one native integrated package identity.
- **Why now:** T-005 passes the substantive implementation and framing gate; the fourth-design scope and owner continuation authorize downstream work.
- **Scope:** Stock integration seam, full declared-axis preflight, independent oracle scan, explicit bounded offer list, stock native study execution, numerical/predicate verification, record/report/figure preparation and immutable evidence sealing. No external physical root, new design revision, original-package mutation, equal-optimization claim or whole-plant LCOE claim.
- **Inputs:** `goal.md`, T-005 review, WI-096 at `29dcb5d8`, current package/interface/manifest, the 43-axis declaration and draft study record/plan. All prior failure evidence remains retained.
- **Done when:** One integrated identity supports a verified, interpretable matched study with retained failures and sensitivity evidence, ready for final independent result review; or a precise bounded negative or dependency is established.
- **Stop when:** Native gates refuse for an unresolved model/scientific reason; another coupled physical calculation, major model or policy exception is needed; the declared cap or another owner gate applies.

### T-006 start — 2026-09-26

T-006 · native integration and study `exploration/component_alternatives/studies/20260926-design-study-component-alternatives/` · expected stock CANDIDATE, pinned preflight, scanned window, complete stored/verified cases and evidence-linked report/figures. Coordinator owns the study and goal evidence. The model author has returned; the independent reviewer remains available for final results and concrete corrective checks.

### T-006 return — 2026-09-26

- **Outcome:** MECHANICAL_FAILURE, attempt 1. Stock integration passed all ten gates; all 501 oracle proposals evaluated. Main native execution stopped before creating a store because the direct launcher lacked the documented TEAx `PYTHONPATH` (`ModuleNotFoundError: simkit`).
- **Evidence:** Study `preparation/execution-attempt1/`; complete 498-point deduplicated list and all scan evidence retained. No model or proposal changed.
- **Retry:** Add the documented sealed-runner import path. This changes process environment only; task, input list, package, scope and meaning remain identical.

### T-006 start — 2026-09-26

T-006 retry 1 of 2 · execute the same 498 proposals using `.codex-test/run bash -c` with the documented repository and TEAx import roots. Integration already verified this exact runtime revision. No seam or model repair is involved.

### T-006 return — 2026-09-26

- **Outcome:** PREREQUISITE. Integration passed and all 498 native cases completed. Full numerical verification failed; no verified economic study is released.
- **Evidence:** Native record `results/cases.json`, `results/verification-attempt1-failure.json`, `results/verification-diagnostics.json`, `results/verification-blocker.json`; independent `evidence/verification-failure-review.md`.
- **Reading:** 83 cases pass all 84 implemented engineering predicates. Independent post-failure diagnostics cover 872 channels and 84 predicates for each of 498 cases: six cases exceed unchanged numerical tolerances, with zero predicate disagreements. Two affected cases are otherwise-passing efficiency sensitivities. No case has been deleted or reclassified to evade verification.
- **Exact dependency:** The finite-water-cooler calculation must meet the predeclared 1e−9 verification accuracy in its derived water flow, pump loads and propagated outputs throughout the executed window. In case c0206, its 1e−10 MW/K UA residual stopping rule does not ensure that accuracy near a small water temperature rise. A 60-digit independent check confirms the oracle for this isolated case. This diagnosis does not identify the causes of all six mismatches.
- **Required action outside this authorization:** Repair native numerical accuracy and validate a new executable identity, or obtain explicit tolerance authority. No such repair, exception or new round is performed. The fourth design and integration PASS evidence remain valid for their recorded scope, but do not discharge the failed main-study verification.

### Stop — 2026-09-26

- **Kind:** required review findings / verification prerequisite.
- **Trigger:** Independent numerical failure review returns FINDINGS / stop. Owner direction requires stopping on unresolved review requirements and prohibits another round to bypass the exhausted design cap.
- **Unresolved requirement:** All required scalar outputs must satisfy the unchanged verification contract; six cases do not. Case c0206 is the independently diagnosed cooler example. The two predicate-passing sensitivity cases disagree on bypass flow and helium hot-bound margin; their causes were not independently isolated. The promoted package and every native result remain unchanged.
- **Work remaining in this turn:** Preserve and seal the blocked attempt, write an explicitly partial answer and diagnostic figures, obtain narrow final assurance of those claims, and commit only owned files. These records do not resume model/study execution. Formal closure remains owner-held.

### Round 1 result — 2026-09-26

- **Strategy:** `supported-common-boundary-screen`, continued under the owner's one-submission extension. One exact package identity was promoted and one blocked study attempt is retained. No second round was opened.
- **Outcome:** Partial. The fourth design and native implementation satisfy the reviewed physical roles, MR-7 and bounded-scope requirements. Ten integration gates passed. The matched study executed all 498 declared unique points but failed its full numerical verification gate. Independent review confirmed the exact cooler accuracy dependency; technical work stopped.
- **Native evidence:** WI-096 implementation at `29dcb5d8`; goal design and implementation review artifacts; integration `CANDIDATE`; `exploration/component_alternatives/studies/20260926-design-study-component-alternatives/` blocked record and snapshot. The snapshot explicitly denies release and retains the failed-verification evidence instead of fabricating a passing summary. Exact native outputs, six numeric mismatch cases, 84-predicate results, all chosen inputs, plots/data and package bytes are preserved.
- **Counts and limits:** 498 completed, 83 passing all native checks, 415 failed engineering combinations, six numeric mismatch cases, zero independent predicate disagreements. Two numerical mismatches occur in otherwise-passing efficiency sensitivities. The selected steam offer versus tested Brayton offers is a conversion-subsystem comparison; price, hydraulics and operating-map qualification remain conditional. No whole-plant or equal-optimization claim is made.
- **Retry classification:** One environment-only retry corrected a missing TEAx import root before any first-attempt point executed. Same package, scope and complete input list. The subsequent numerical failure was classified as a prerequisite, not a mechanical retry or permission to change tolerances.
- **Dispositions:** Seven native findings have first-sighting rows and concrete homes in the study register/discovery log. Numerical accuracy is blocked for owner disposition; remaining scientific/cost limits are declared seams, and the import-path failure is resolved. No follow-up modeling was executed.
- **Artifacts:** Updated answer, candidate ledger, proposed passage, equality explanation, diagnostic figures/data/renderer and replay. The owner's article and unrelated work remain untouched. Final preservation passes all 13,215 original protected files. Formal goal and item closure remain owner-held.
- **Proposed learning delta:** (1) Model-owned controls can preserve chosen source/ratio/equipment roles while reporting deficient offers. (2) A local heat-transfer residual tolerance does not guarantee downstream flow/power accuracy near a small temperature rise; broader verification can fail after a development PASS. (3) Connecting-equipment selection materially changes the conditional comparison, but this blocked attempt cannot release a technology ranking. These are agent interpretations awaiting final assurance, not settled owner decisions.
- **Recommendation:** Retain the partial result and exact unresolved verification requirement for the owner. Do not continue the model or open a new round under this exhausted continuation.

### Round 1 review — 2026-09-26

- **Reviewer:** continuing independent non-author `/root/feasibility_review`.
- **Verdict:** PASS for faithful blocked-result reporting only. Numerical study verification remains FAILED; economic completion remains unmet. No model repair, tolerance exception, further round or formal closure is authorized.
- **Evidence:** `evidence/final-assurance-review.md`, reviewing retained record/report commit `49c20e69` and the subsequent cause-attribution correction. The snapshot remains `1e8a19872852e19390eba76445e11a866c5da8fb9f791122b6b64d6e16b66641`; the reviewer independently rehashed all 635 artifacts with zero mismatches.
- **Checks:** Native counts, every plotted identity/status, three nominal comparisons, fixed-connector costs, correction frontiers, common-charge equality, materiality and all three figures. The one environment-only retry preserves scope/inputs/package; the accuracy failure is a prerequisite stop. Prior design, implementation and numerical-failure reviews supply valid coverage without a repeated whole-model audit.
- **Corrected finding:** Earlier reporting attributed all six numerical mismatches to cooler stopping accuracy. That cause was independently established only for c0206. Current goal prose is corrected; the sealed finding is corrected by an immutable-record addendum and a joined discovery row. Other mismatch causes remain unisolated.
- **Findings and learning:** All seven native findings have concrete dispositions/homes. The numerical dependency remains blocked for owner disposition; qualification limitations remain declared seams; the launch issue is resolved. The three proposed agent learning statements are accepted with the isolated-cause qualification and appended to `learnings.md`.
- **Recommendation:** Retain this partial result and exact unmet verification requirement. Formal goal/WI-096 closure remains with the owner. No new round is opened.

## Round 2 — bounded-numerical-repair

### Strategy revision — 2026-09-26

[OWNER] The new direction authorizes a bounded numerical repair, its new executable, complete study replay and independent reviews; no tolerance waiver or physical-domain expansion. Direction: `evidence/owner-direction-numerical-repair.md`.

[AGENT] Isolate every scalar discrepancy against unchanged independent evidence, repair only demonstrated native numerical accuracy defects, and compare the same explicit offers on one repaired identity. The assumption is that the six mismatches are numerical rather than substantive physical-model failures. A substantive physics dependency stops dependent repair and is surfaced to the owner. Original blocked executable/cases/diagnostics remain sealed at study commit `49c20e69`, with reporting correction `0485f590`. MR-7 variable roles and selected equipment do not change. The question remains selected steam versus tested Brayton conversion-subsystem cost per net MWh at matched source conditions.

### T-007 scope

- **Objective:** Isolate all six numerical failures and repair confirmed native accuracy defects with focused regressions and preserved historical evidence.
- **Why now:** Owner explicitly authorizes this repair and necessary new executable after the prior verification stop.
- **Scope:** WI-096 numerical-repair supplement, goal-owned native body variants/build outputs, targeted numerical checks and validation. Preserve oracle, tolerances, original libraries/packages, old sealed study, all design inputs and physical domains. No technology branch or substantive physics change.
- **Inputs:** `goal.md`, owner direction, blocked study at `49c20e69`, correction `0485f590`, independent failure review, WI-096 reviewed design/report and actual native implementations.
- **Done when:** All six causes are individually evidenced; confirmed native defects are repaired and focused failure/nearby-case regressions pass, ready for independent review; or an exact non-numerical dependency is established.
- **Stop when:** Substantive physical-model change, oracle/tolerance change, unsupported domain extension or owner-reserved decision is required.

### T-007 start — 2026-09-26

T-007 · continuing model author owns `work/active/WI-096_matched-conversion-subsystems/numerical-repair/`, goal-owned native bodies/build/package outputs and focused regressions. Coordinator owns goal records and study metadata/execution. No independent scientific work depends on the repaired identity before independent review. The prior reviewer remains separate from authoring. Exact ownership and requirements are in `evidence/numerical-repair-brief.md`.
