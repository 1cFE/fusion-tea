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
