# Trail: Whole-plant steam versus helium Brayton conversion

Append-only, newest last. Native artifacts carry implementation state.

## Round 1 — common-stellaris-inventory

### Strategy revision — 2026-09-27

- **Approach:** [AGENT] Extend the verified matched conversion branches with the strongest compatible existing Stellaris inventory and explicit whole-plant accounting. Reuse prior controls and numerical evidence, then rerank a finite catalog with native system results.
- **Assumptions:** [AGENT] Retained models/sources can support a conditional common reactor inventory and close the missing power/fuel/cost boundary without changing the component question.
- **Abandonment conditions:** Material inventory incompatibility or missing source condition that cannot be honestly bounded; comparison-meaning change, unresolved owner gate, or declared cap.
- **Intended model increment:** Isolated whole-plant assembly with disjoint account mapping, complete net export and lifecycle cost; choices retained under MR-7.
- **Intended study question:** Does the preferred conversion choice change when complete reactor power and lifecycle costs are included, and which assumptions reverse it?

### T-001 scope

- **Objective:** Establish a traceable compatible upstream inventory and exact conversion interfaces for the whole-plant assembly.
- **Why now:** The verified predecessor explicitly omits reactor/fuel and primary circulation scope.
- **Scope:** Read retained evidence; deposit accounting and interface assessments and a proposed configuration/role map. No production model edits or baseline changes. Two independent read-only investigations may run concurrently because neither changes shared state; coordinator integrates their conclusions before design.
- **Inputs:** goal.md; predecessor answer/trail/contracts/reviews and WI-096; existing Stellaris and ARIES integration evidence named in owner brief.
- **Done when:** A concrete reusable boundary with sources, unknowns and model entry points, or a named material prerequisite, is recorded.
- **Stop when:** Prerequisite, strategy blocker, reserved owner gate or declared cap.

### T-001 start — 2026-09-27

T-001 · retained native model/study evidence · evidence/upstream-accounting.md and evidence/conversion-interfaces.md; coordinator owns trail and shared integration.

### T-002 scope

- **Objective:** Specify and implement the isolated whole-plant assembly with independently reviewed source, power, cost and variable-role boundaries.
- **Why now:** The owner brief already establishes the missing whole-plant behavior; T-001 evidence will resolve the detailed design.
- **Scope:** Native work-item registration/specification may proceed alongside T-001 because owner requirements are independent of its findings. Dependent design and implementation wait for T-001 evidence and independent design review. Own new whole-plant model/package and native work-item files; preserve existing models and studies.
- **Inputs:** goal.md@2c8db9db; evidence/owner-brief.md@2c8db9db; T-001 assessments when returned; MR-1–7.
- **Done when:** Reviewed native generated package, complete power/cost inventory, variable-role record, development verification and exact preservation evidence support integration.
- **Stop when:** Prerequisite, strategy blocker, owner gate or declared cap.

### T-002 start — 2026-09-27

T-002 · native modeling PM · registered work item, specification, design/plan, isolated model/package and reviewed verification.

### T-001 return — 2026-09-27

- **Outcome:** COMPLETE — bounded investigation, not model qualification.
- **Evidence:** evidence/upstream-accounting.md and evidence/conversion-interfaces.md (unpinned; no native digest until task commit); native WI-080 baseline and repaired WI-096 sealed record cited there. Existing package/runtime provenance check: three tests passed.
- **Reading:** Exact source/return/conversion outputs and active fixed reactor accounts are available. The original whole-reactor totals contain replaced equipment and dormant accounts; reuse requires disjoint remapping. Supplied source heat differs from fusion heat and includes no recovered circulator work until the primary-loop calculation. At unchanged primary/divertor offers, 3000 MW fails additional upstream limits. Known magnet current/fit and empirical field limitations prevent calling the inherited core physically adequate.
- **Decision:** Trigger: missing complete plant boundary. Decision: proceed with WI-098 detailed design of isolated supplied-source plant accounting, because the owner explicitly permits a conditional source and modeling assumptions. Tier: execution detail. Decided by: coordinator [AGENT]. Changed: WI-098 spec/plan, evidence/design-author-brief.md.
- **Decision:** Trigger: inherited material core defects and missing coil-replacement costs. Decision: preserve these qualifications and submit the proposed conditional interpretation to independent boundary review before implementation; no complete-plant result or passing-core claim is released. Tier: premise surprise. Decided by: coordinator [AGENT], surfaced in conversation. Changed: evidence/boundary-review-brief.md; author brief and design task carry the finding.
- **Decision:** Trigger: independent upstream and conversion read-only work complete. Decision: integrate their findings sequentially through one design author; reviewer separately checks original evidence and awaits the completed design. Tier: execution detail. Decided by: coordinator [AGENT]. Changed: T-002 assignments. No model or historical evidence changed.

### T-002 design submission r1 — 2026-09-27

[AGENT] Complete design/configuration submitted for the first independent review. The fixed alternative uses 48 kA excitation, the larger selected winding pack and a separately priced 40/60 kW cryoplant. The previous 50 kA offer remains failed evidence at 4d42eff9. Reviewer: boundary_review, continuing its original-evidence checks. Scope is the complete source/power/cost/role boundary in evidence/boundary-review-brief.md. Submission 1 of 3; no dependent model implementation or main study has executed. Evidence: work/active/WI-098_whole-plant-conversion-comparison/{design.md,configuration.md}, currently unpinned.

### T-002 design review r1 — 2026-09-27

- **Evidence:** Design/configuration r1 at 276cfe48; independent evidence/boundary-review.md, unpinned; no native digest. Verdict FINDINGS, MR-7 unverified pending a precise source-input migration and executed behavior.
- **Decision:** Trigger: omitted major overhead/supplementary scopes and incomplete source/fuel interfaces. Decision: correct F1–F3 in the native design and return to the same reviewer before implementation. Tier: execution detail. Decided by: coordinator [AGENT]. Changed: author assignment for WI-098 design.md/configuration.md, revision 1 of 2.
- **Decision:** Trigger: conditional 48 kA source interpretation. Decision: retain the proposed conditional interpretation because independent review found it inside the owner's supplied-source authority; exact native hardware capture and its component checks remain mandatory. Tier: premise surprise. Decided by: coordinator [AGENT], using the independent review. Changed: no model or study execution released by this finding.

### T-002 design submission r2 — 2026-09-27

[AGENT] Revised complete design/configuration submitted to boundary_review. Corrective scope: disjoint CAS29/30/50 accounts, exact single-source/finance migration, explicit D/Li6 purchase and refill equations, positive-integer operating horizon and capture-key identity. Submission 2 of 3. Native design files remain frozen during review. Reversible conversion-oracle namespace preparation has completed without changed arithmetic; new equations and native hardware execution remain paused.

### T-002 design review r2 — 2026-09-27

- **Evidence:** Accepted design/configuration at 81423599; evidence/boundary-review-r2.md, unpinned; no native digest. Independent verdict PASS for implementation. MR-7 compliant at design level; executed behavior remains unverified.
- **Decision:** Trigger: F1–F3 resolved by independent corrective review. Decision: release exact48kA capture and isolated native implementation, with independent numerical work in parallel because it owns distinct files and uses the same accepted contract. Tier: execution detail. Decided by: coordinator [AGENT]. Changed: evidence/implementation-brief.md and evidence/verifier-brief.md assignments. Integration audit remains required before the main study.
- **Decision:** Trigger: gas transport overhead includes inseparable helium stock. Decision: retain it as an explicitly disclosed installed-cost proxy rather than inventing a finer quote split. Tier: execution detail. Decided by: coordinator [AGENT], following the review's nonblocking clarification. Changed: implementation/reporting brief clarification; no source or physical equation change.

### T-002 capture premise check — 2026-09-27

- **Evidence:** WI-098/evidence/magnet-capture retains the exact selected offer and all raw full-model failures. The source investigator and fresh reviewer independently found that the retained volumetric nuclear-heating input is not calculated from fusion power and is not a proven upper bound for the enlarged winding pack.
- **Decision:** Trigger: evidence contradicts the design's claimed conservative nuclear envelope. Decision: park that conclusion and dependent ranking; obtain focused source review and correct the native design to state the transferred heating assumption at its actual authority. Tier: premise surprise. Decided by: coordinator [AGENT], surfaced in conversation. Changed: evidence/capture-review-brief.md; implementation and verifier assignments. Unaffected account/source algebra may proceed; no selected hardware changed and no failure waived.

### T-002 capture correction review — 2026-09-27

- **Evidence:** evidence/capture-boundary-review.md and capture-boundary-review-r2.md; independent source and arithmetic probes in evidence/boundary-review. The final corrective disposition is PASS with exact accepted design/configuration hashes. Native selected48kA arithmetic independently matches93 channels in WI-098/evidence/independent-verification/capture-check.json.
- **Decision:** Trigger: unsupported conservative-envelope claim and duplicate coil heat in the auxiliary sink. Decision: release the corrected dynamic cryogenic-demand calculation with fixed equipment, explicit transferred heating assumptions and finite nonnegative demand guards; remove duplicate sink heat while retaining coil electrical consumption. Tier: premise surprise. Decided by: coordinator [AGENT], using focused independent PASS. Changed: WI-098 design/configuration and implementation/oracle assignments. No empirical transport qualification is claimed; native heating-scenario and integration checks remain required before ranking.

### T-002 selected cryoplant role correction — 2026-09-27

- **Evidence:** evidence/cryoplant-offer-proposal.md and independent evidence/cryoplant-offer-review.md, verdict PASS. The first development run remains retained in WI-098/evidence/development; the corrected final run uses a separate directory.
- **Decision:** Trigger: fixed captured ratings prevented the accepted insufficient/sufficient selected-capacity tests through the new assembly. Decision: release explicit selected cold/intercept ratings and quote, preserving the captured offer as reference and the baseline purchase unchanged. Tier: execution detail. Decided by: coordinator [AGENT], after focused MR-7 review. Changed: native design/bindings and declared small/default/large development offers. No demand-sized purchase or physical equation change.
- **Decision:** Trigger: independent arithmetic found the generated capture margin used a stress calibration in place of the actual allowable. Decision: correct that operand to the original selected allowable, preserve the first native run, and verify the final executable without changing tolerances. Tier: execution detail. Decided by: coordinator [AGENT]. Changed: native captured-offer implementation; final development and control verification remain pending.

### T-003 scope

- **Objective:** Integrate one reviewed package and run a verified finite whole-plant equipment and sensitivity study that answers the paired component question.
- **Why now:** Final development and 498 control checks establish numerical parity; independent complete-boundary review is concluding.
- **Scope:** Prepare record, interface, axes and scan code while review concludes. Dependent oracle scan, integration promotion and main native execution wait for its PASS. One promoted pin and one committed study in this round; at most 3000 unique complete main points. The coordinator owns manifest/record/report; conversion owns axes/annex; upstream owns scan code; reviewer owns assurance. These preparations have separate files and do not alter the frozen package.
- **Inputs:** goal.md@2c8db9db; model/package d7d8a1e5; WI-098 report, final native and independent control evidence; implementation-integration review when returned; comparison-contract.md and study-preparation-notes.md.
- **Done when:** Native CANDIDATE and all study gates pass, reranked native results and assumptions are independently reviewed, and a sealed reproducible study supports the required explanation and figures.
- **Stop when:** Prerequisite, strategy blocker, owner gate, verification failure or declared cap.

### T-003 start — 2026-09-27

T-003 · native integration and run-study · exploration/whole_plant_conversion/studies/20260927-design-study-whole-plant-conversion/; preparatory record/interface work only until independent boundary PASS.

### T-002 return — 2026-09-27

- **Outcome:** COMPLETE — reviewed isolated model implementation, with formal item closure retained by owner.
- **Evidence:** Model/package d7d8a1e5; WI-098/report.md and final independent verification; evidence/implementation-integration-review.md PASS at executable 6915694e74919ebb764445dfc7f0782eda85a9de29fa44c4b55ffa415c1eb30f, semantic bb284160ba12996bc129ba91c1838aed3281d54dc0e729fe03ca02a9d413d6e3. Final 32 evaluated development cases and 498 controls agree across 1192 outputs and 125 predicates; 3 expected refusals and 88 behavior checks retained. The 498 old controls match 872 inherited outputs and 84 predicates exactly. Preservation confirms 54169 prior files unchanged.
- **Reading:** The supplied 2500/2800 MW source pairs pass implemented equipment checks with complete declared whole-plant power and lifecycle accounting. The 3000 MW source fails selected primary/divertor limits. Static validator remains exit 1 with all 72 literal and 1174 alias/readiness diagnostics explicitly mapped and independently reviewed. Scientific transport/plasma/global-fit qualifications remain unresolved and explicit.
- **MR-7:** Compliant in the reviewed offers/domains. Actual native demand-only, small/default/large cryoplant, stock/processing/primary/auxiliary capacity and source-only tests preserve selected purchases and reject insufficient equipment. Role/binding review covers affected consumers; no autosizing purchase is introduced.
- **Decision:** Trigger: independent complete-boundary and executed-role PASS. Decision: release T-003 independent scan, stock integration and gated main study, because the implementation satisfies the bounded contract. Tier: execution detail. Decided by: coordinator [AGENT] using independent reviewer evidence. Changed: T-003 release; no package changes.
- **Decision:** Trigger: unused generated CAS metadata tags differ from the reviewed categories. Decision: retain frozen numerical package and use configuration.md explicit mapping in reports, because exact membership equations drive accounting and no executable consumer reads the tags. Tier: execution detail. Decided by: coordinator [AGENT] following reviewer N1 disposition. Changed: reporting requirement and study finding; metadata defect retained as a declared seam.

### T-003 preparation interruption — 2026-09-27

- **Evidence:** Initial oracle scan in the study preparation directory reports 223 unknown-input errors while the integration seam regenerates the package in place. The oracle reads current default-input files for each point; temporary removal during regeneration explains the missing full input set. This is coordinator scheduling interference, not a physical refusal or a native study verification failure.
- **Decision:** Trigger: overlapping read and regeneration invalidated oracle scan evidence. Decision: preserve the initial attempt, wait for integration completion and rerun the same scan on the stable package; no oracle equation or tolerance changes. Tier: execution detail. Decided by: coordinator [AGENT], surfaced in conversation. Changed: scan scheduling and retained attempt designation. No main point has executed and no pin has been promoted. This consumes the first mechanical preparation retry when restarted; the declared cap remains two retries.

### T-003 start — 2026-09-27

T-003 preparation retry 1 of 2 · same finite study scope and input catalog · integration has completed and no regeneration will overlap package readers. The invalid first oracle scan remains retained; the replacement scan uses the returned native CANDIDATE on the stable package. Admission checking and threshold planning remain within the original 3000-point cap.

### T-003 integration candidate — 2026-09-27

- **Evidence:** evidence/integration/integration_return.json, CANDIDATE with all ten gates passing. Pin `89acea93750da8794f74883315fb0ff658d6213d0d4b2ffcaf2b1edb320deeae`; executable `6915694e74919ebb764445dfc7f0782eda85a9de29fa44c4b55ffa415c1eb30f`; semantic `bb284160ba12996bc129ba91c1838aed3281d54dc0e729fe03ca02a9d413d6e3`; TEAx `8d877460ac4f6f264561d916e40c1708adb13397`. The manifest covers all 637 inputs and 1192 independently compared scalar channels; all 125 baseline predicates reproduce and rederive.
- **Decision:** Trigger: native integration fixed-point and verification PASS. Decision: promote this one candidate for Round 1 and complete the independent scan before main native execution. Tier: execution detail. Decided by: coordinator [AGENT]. Changed: T-003 accepted integration identity; this is the round's only promoted pin.

### T-003 main execution release — 2026-09-27

- **Evidence:** Study preparation/candidate-freeze.json and window.json; 2496 unique complete points, 2651 aliases, 3900 independent oracle evaluations and no refusals. Code d4455af3. Proposed-points SHA256 `55782d25a4c7a6818547e9fe1b587deb79bd3d6ef8535b07ec858e14ab6e1217`. All 90 declared groups have indicator coverage; the accepted integration supplies the same baseline and all preflight gates.
- **Decision:** Trigger: stable-package scan and admission audits completed. Decision: execute the fixed list through stock StudyRunner and verify all 2496 cases, because it covers the requested finite catalogs and material sensitivities within the 3000-point cap. Tier: execution detail. Decided by: coordinator [AGENT]. Changed: study root proposed-points.json/window.json copied from frozen preparation; execution-context.json records exact commands and revision. No endpoint or physical interpretation changed.
- **Decision:** Trigger: an algebraic economic crossing falls inside the inherited reporting band. Decision: retain its strict sign bracket and separately confirm the ±5 USD2025/MWh band boundaries, so numerical ordering is not presented as material preference. Tier: execution detail. Decided by: coordinator [AGENT] applying comparison-contract.md. Changed: frozen proposal list and native-only reporting code; the band remains a presentation convention, not a constraint.

### T-003 return — 2026-09-27

- **Outcome:** STRATEGY_BLOCKER — the selected near-zero cryogenic diagnostic spacing does not support the declared numerical verification contract. All 2,496 native cases completed, but stock verification aborted at case c2438. No economic conclusion is released from this attempt.
- **Evidence:** Study verification.log and results/verification-blocker.json; evidence/final-results-review.md, independent FINDINGS. Native cold margin 0.003072599989536684 W versus oracle 0.0030725999968126416 W exceeds the relative tolerance; absolute difference 7.276e-12 W. The all-case forensic inspection is separate diagnostic work and cannot promote this failed run.
- **Decision:** Trigger: stock numerical verification failure. Decision: preserve and seal this attempt as blocked, close Round 1, and review revised diagnostic spacing before another study. Tier: execution detail. Decided by: coordinator [AGENT], with independent failure disposition. Changed: failed study record and round status; no model, oracle, tolerance or physical constraint change.

### Round 1 result — 2026-09-27

- **Intent:** Unmet. The complete assembly and all-case execution exist; verified economic evidence remains missing.
- **Task sequence:** T-001 COMPLETE source/interface investigation; T-002 COMPLETE reviewed isolated implementation; T-003 STRATEGY_BLOCKER at stock numerical verification.
- **Last semantic outcome and stop reason:** STRATEGY_BLOCKER: the near-capacity diagnostic spacing fails the unchanged numerical contract. This closes the round; it is not a mechanical retry or an accepted economic reading.
- **Evidence:** Model/package d7d8a1e5; integration CANDIDATE at 3deafc4e; blocked study 20260927-design-study-whole-plant-conversion; evidence/final-results-review.md FINDINGS.
- **Proposed learning delta:** Relative-only comparison of a nearly cancelled capacity margin needs a predeclared diagnostic spacing that resolves the margin numerically. This does not justify changing physical inequalities or verification tolerances.
- **Finding dispositions:** Study findings #1–8 remain the recorded declared seams or corrected scheduling issue. Finding #9 blocks release and routes to a separately reviewed next-round spacing proposal. Full discrepancy inspection remains required before that decision. One preparation mechanical retry was used; the main failure is a changed-input follow-up, not another mechanical retry.

### Round 1 review — 2026-09-27

- **Reviewer and verdict:** Independent boundary_review; PASS for failed-round closure coverage only, evidence/round-1-review.md. The economic release remains blocked by evidence/final-results-review.md FINDINGS.
- **Coverage:** Native blocked record committed at 275ba13c, snapshot 038545e8b98042063409aa72884c182327b7a87ec7aa5d5a8c6a726ec44de0fb. Scope, one preparation retry, unchanged requested comparison and finding routing checked. Prior source/boundary/MR-7 reviews remain valid for the frozen implementation.
- **Learning:** Accept the bounded diagnostic-spacing lesson below. Do not assume the first failure is the only failure. The completed all-case forensic scan subsequently identifies 11 scalar mismatches across five cases, including one cooler case, with zero predicate mismatches; evidence/verification-failure-r1/discrepancies.json. That diagnostic cannot turn the failed run into a pass.
- **Recommendation:** Continue a new round with independent numerical diagnosis and reviewed corrections. Formal goal/item closure is not recommended yet.

## Round 2 — resolve-numerical-verification

### Strategy revision — 2026-09-27

- **Approach:** [AGENT] Resolve all diagnosed numerical discrepancies using independently justified accuracy corrections and predeclared diagnostic spacing; retain every catalog offer and repeat the complete native study.
- **Assumptions:** [AGENT] The discrepancy set reflects numerical conditioning rather than a changed physical or economic comparison. Independent high-precision adjudication must establish which implementation requires correction.
- **Abandonment conditions:** A physical-model inconsistency, unresolved interpretation, repeated unreviewed mismatch or declared cap. No failing catalog offer is removed to obtain verification.
- **Intended model increment:** None unless adjudication proves a native numerical implementation defect. Package-owned oracle accuracy may be repaired only with independent mathematical evidence; verification tolerances remain unchanged. Reuse unchanged source, cost, role and preservation reviews.
- **Intended study question:** The original complete whole-plant preference and conditional thresholds, with a numerically resolved cryogenic capacity bracket.

### T-004 scope

- **Objective:** Independently diagnose all 11 discrepancies and review the bounded numerical correction before any new main study.
- **Scope:** Upstream owns forensic/high-precision probes and any approved package-owned oracle correction; conversion owns native solver diagnosis and any approved native body correction. Root owns round/record/integration; boundary_review owns independent adjudication. Distinct files permit concurrent investigation; dependent mutations wait for reviewed diagnosis. Preserve sealed Round 1, unchanged tolerance definitions and all equipment selections.
- **Inputs:** Blocked study at 275ba13c; evidence/verification-failure-r1; exact native/oracle sources and accepted comparison contract.
- **Done when:** Independent review accepts a concrete correction, targeted native checks support it, and exact package/oracle identity is ready for integration.
- **Stop when:** Unresolved scientific interpretation, material prerequisite or declared cap. This is a changed-input/correction task, not a mechanical retry of T-003.

### T-004 start — 2026-09-27

T-004 · independent numerical adjudication · evidence/verification-failure-r1 and evidence/numerical-repair-r2-proposal.md; no model or oracle mutation released yet.

### T-004 correction review — 2026-09-27

- **Evidence:** evidence/numerical-repair-r2-proposal.md and evidence/numerical-repair-r2-review.md, independent PASS for bounded implementation. The 80-digit reference identifies insufficient independent Brent stopping accuracy at c1868; native output is already accurate. All five failing input maps and original errors remain in the sealed first record and forensic diagnosis.
- **Decision:** Trigger: independently adjudicated oracle stopping error and cancellation-sensitive diagnostic spacing. Decision: tighten only the package-owned oracle's Brent stopping precision and predeclare four replacement cryogenic points at capacity ±0.01 W/m³. Retain the native body, plant equations, all catalog offers and acceptance tolerances. Tier: execution detail. Decided by: coordinator [AGENT] using focused independent PASS. Changed: upstream assignment for oracle_thermal.py, scan_catalog.py and new validation receipts. No main study is released yet.
- **Required checks:** Original 2496-point diagnostic must retain exactly eight known cryogenic discrepancies and no others; four new native points, legacy controls and complete replacement native verification must pass. An oracle correction never retroactively releases the old failed record.

### T-004 return — 2026-09-27

- **Outcome:** COMPLETE — exact reviewed correction and pre-main regression gates passed. Native model/package and acceptance tolerances are unchanged.
- **Evidence:** evidence/numerical-repair-r2-validation/validation-summary.json and reviewed-changes.diff. Original 2496-point diagnostic retains exactly eight old cryogenic margin discrepancies, with zero others and zero predicate mismatches. All 498 controls pass; development gives 32 evaluated passes and three consistent refusals. Four wider cryogenic points pass stock numerical verification across 1192 scalars and 125 predicates, while retaining the expected lower-pass/upper-cold-capacity-failure behavior.
- **Reading:** Independent high-precision adjudication supports a numerical accuracy change to the package-owned oracle only. This does not alter native economic outputs or release the original failed record. New main execution and verification remain required.
- **Decision:** Trigger: reviewed correction and all required local checks passed. Decision: run native integration on the committed correction, then regenerate and freeze the replacement point list before a new complete study. Tier: execution detail. Decided by: coordinator [AGENT] under numerical-repair-r2-review.md. Changed: T-005 scope; regeneration and package readers remain sequential.

### T-005 scope

- **Objective:** Complete the original whole-plant engineering answer using the corrected verifier and reviewed cryogenic diagnostic spacing, a fresh native record, figures and independent final assurance.
- **Scope:** One integration candidate and one committed replacement study in this round, at most 3000 complete native points. Same source, cost, equipment and reporting contract. Root owns integration, execution and narrative; upstream owns replacement preparation; conversion owns native report rendering; boundary_review owns final assurance. No preparation reader overlaps in-place integration regeneration.
- **Inputs:** T-004 reviewed correction and regression, unchanged native package and original comparison contract, sealed failed first study and inherited catalog.
- **Done when:** Complete all-case numerical verification, reviewed native reranking/figures/conclusion and sealed replayable evidence satisfy the owner endpoint.
- **Stop when:** Numerical verification failure, material prerequisite, reserved owner gate or declared cap.

### T-005 start — 2026-09-27

T-005 · native integration and replacement run-study · exploration/whole_plant_conversion/studies/20260927-design-study-whole-plant-conversion-b/.

### T-005 integration candidate — 2026-09-27

- **Evidence:** evidence/integration-r2/integration_return.json: all ten gates PASS, CANDIDATE on corrected-oracle commit ae6819d1. Native executable 6915694e74919ebb764445dfc7f0782eda85a9de29fa44c4b55ffa415c1eb30f and semantic bb284160ba12996bc129ba91c1838aed3281d54dc0e729fe03ca02a9d413d6e3 are unchanged. Pin 89acea93750da8794f74883315fb0ff658d6213d0d4b2ffcaf2b1edb320deeae is reused with fresh integration and corrected-verifier provenance.
- **Decision:** Trigger: corrected-oracle regression and native integration PASS. Decision: promote this candidate as Round 2’s only pin and release replacement preparation on the now-stable package. Tier: execution detail. Decided by: coordinator [AGENT], using independent correction acceptance. Changed: replacement record integration receipts; no package changes. Main execution awaits a frozen reviewed list.

### T-005 reporting sample preservation — 2026-09-27

- **Evidence:** Replacement preparation/original-point-comparison.json initially found 60 changed complete maps: four reviewed cryogenic inputs and 56 reporting-band quote maps caused by secant sample-location shifts of about 1.7e-15 in the path parameter. All anchors, aliases, base catalog and algebraic-zero brackets are unchanged. Recomputed planning evidence is retained separately.
- **Decision:** Trigger: tighter oracle convergence moved engineered reporting samples by roundoff. Decision: retain their original declared sample locations, which remain valid straddling brackets and already passed corrected-oracle regression. Restore only those reporting quote maps and refresh their preparation metadata; retain both the recomputed and selected planning evidence. Tier: execution detail. Decided by: coordinator [AGENT], following independent investigator recommendation; focused reviewer confirmation requested before final freeze. Changed: replacement preparation helper and provenance. No model, acceptance tolerance, equipment offer or case retention change. Main execution remains unreleased.

### T-005 main execution release — 2026-09-27

- **Evidence:** evidence/final-results-review-r2/preparation-acceptance.md independent PASS. Frozen replacement preparation has 2496 complete points, 2651 aliases, 3956 oracle evaluations and zero refusals. Exactly 2492 original maps and all noncryogenic memberships/anchors are unchanged; four cryogenic inputs match the separately stock-verified replacements. The original reporting sample locations and both bracket signs remain preserved. All prepared-artifact and code hashes pass independent checks.
- **Decision:** Trigger: exact frozen preparation and all correction/integration gates accepted. Decision: execute and independently verify every replacement point through the native route. Tier: execution detail. Decided by: coordinator [AGENT], using independent preparation acceptance. Changed: replacement execution release at code17919e73 and proposal SHA256 5ca2398ee367b5438e667c3ee9c74f0e8c90919f2bb0416f31015c7a315b1992. No endpoint, package or acceptance tolerance change.

### T-005 return — 2026-09-27

- **Outcome:** COMPLETE — the original whole-plant engineering/economic question is answered on verified native evidence. Formal goal/item closure remains with the owner.
- **Evidence:** Sealed study committed at a7bd94ed9a9746e1866400f60be5792eab6842d8; snapshot 5db4b78627cadca525c02e29bf98e9c6bad173baf372e25cce9a4bf3effb124e. All 2,496 cases pass stock independent verification of 1,192 scalar channels and 125 predicates. evidence/final-results-review-r2.md independently passes actual whole-plant reranking, complete declared accounts, conclusions and presentation. evidence/replay-preflight-r2.log passes all 2,803 artifact hashes and exact source/archive/package checks; it explicitly executes no study. evidence/native-replay-comparison.json independently confirms all native outputs/verdicts, including iteration counters, reproduce 2,492 original cases and four reviewed replacement probes exactly.
- **Reading:** answer.md and proposed-article.md present the conditional engineering answer. Steam wins nominally at 2,500 and 2,800 MW source heat; the declared combined efficiency/quote scenario reverses preference at 2,800 MW. The selected primary/divertor hardware makes 3,000 MW unsupported. Complete capital, fuel, service, imports, replacement and terminal costs are included. Study synthesis.md is an executor reading restricted to the committed record, not a new independent review.
- **MR-7:** Compliant within the declared model and catalog, reusing the frozen implementation review and actual main-case predicates. Selected equipment remains supplied and insufficient selections fail. No automatic purchase or resizing was introduced by the numerical correction or report.
- **Decision:** Trigger: all-case native verification and independent final conclusion review PASS. Decision: release the conditional whole-plant answer and preserve all failed cases and qualifications, because the owner endpoint is met on the declared supported pairs. Tier: execution detail. Decided by: coordinator [AGENT] using independent review. Changed: sealed replacement study, answer, figures and proposed article; no native package or acceptance-tolerance changes.

### Checkpoint C-001.r1 — 2026-09-27

- **Reading:** Committed replacement study synthesis.md, executor reading stamped with snapshot 5db4b78627cadca525c02e29bf98e9c6bad173baf372e25cce9a4bf3effb124e.
- **Dispositions:** Carry findings #1–10 forward as independently reviewed in supporting/final-results-review.md and findings.json. The failed first study stays blocked; its finding #9 now routes to the reviewed replacement result rather than erasing its failure.
- **Reviewer/verdict:** Coordinator disposition check, reusing boundary_review's substantive independent final PASS. No new independent verdict is claimed. The synthesis adds no physics, evidence, range or interpretation that changes the reviewed conclusion, and no semantic follow-up is proposed.
- **Changes:** Joined dispositions appended under the same discovery IDs. Formal owner close is recommended after round coverage; no new modeling or study task is released.

### Round 2 result — 2026-09-27

- **Intent:** Met. The complete declared plant comparison, fresh equipment ranking, material sensitivities, explanation, article, SVG/PNG figures, data, renderer, native store, verification and replay instructions are delivered.
- **Task sequence:** T-004 COMPLETE independent numerical adjudication/correction; T-005 COMPLETE replacement whole-plant study and final assurance.
- **Last semantic outcome and stop reason:** COMPLETE; the goal is answered and a valid committed study reading exists. This closes Round 2 under the runbook; formal goal/item closure remains owner-held.
- **Evidence:** a7bd94ed sealed record; answer.md; evidence/final-results-review-r2.md; replay preflight; native replay comparison; executor synthesis.
- **Proposed learning delta:** Complete plant costs can reverse the useful component preference by changing the cost per net MWh. An accurate native solver must not be changed to match a less accurate oracle; independently adjudicate the discrepancy first. A capacity diagnostic must resolve its residual under the fixed verification contract. Keep conditional technology and price scenarios distinct from empirical uncertainty bounds.
- **Finding dispositions:** Replacement #1–8 remain explicit scientific, metadata, validation, finite-catalog or pricing limits and the corrected preparation process. #9 is the independently justified oracle accuracy fix; #10 is the reviewed wider diagnostic resolution. All remain visible in the sealed record and joined discovery rows. No unresolved finding blocks the conditional answer.

### Round 2 review — 2026-09-27

- **Reviewer/verdict:** Coordinator closure check; additional independent review skipped because all triggered source, account, MR-7, numerical, ranking and presentation risks already have valid substantive coverage in evidence/implementation-integration-review.md, evidence/numerical-repair-r2-review.md, evidence/final-results-review-r2/correction-acceptance.md, preparation-acceptance.md and evidence/final-results-review-r2.md. This is a coverage check after the round result, not a new independent PASS.
- **Checks:** T-004 and T-005 stayed within their recorded scopes. Round 2 promoted one unchanged executable pin with fresh oracle provenance and committed one replacement study. There was no Round 2 mechanical retry. Four cryogenic input changes and the oracle convergence correction were explicit strategy work, not relabeled retries. The failed Round 1 record and all 2,725 hashed artifacts are unchanged. All 54,169 protected baseline files are unchanged. All cited main results are committed; the seal and replay preflight confirm exact identities. No native artifact moved outside its task.
- **Discoveries:** All ten replacement findings and the first record's numerical blocker have joined dispositions in exploration/whole_plant_conversion/studies/DISCOVERY_LOG.md. Their homes resolve to retained evidence. Reviewed limitations remain stated in the answer and study; repaired numerical and preparation issues retain their failed history.
- **Learning:** Accept the proposed delta with its finite-catalog and conditional-model limits; append it to learnings.md. No general fusion-cost or global technology superiority claim follows.
- **Recommendation:** Owner may formally close this goal and WI-098. The intended engineering endpoint is complete; no further modeling task is needed to answer the declared question. Future vendor, plasma or neutron-transport qualification would be new scope.
