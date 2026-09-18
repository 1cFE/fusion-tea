# Trail: Installed cooling equipment costs

## Round 1 — source-supported-equipment-accounts

### Strategy revision — 2026-09-18

- **Approach:** [AGENT] Trace existing heat-transport accounts and retained requirements, then use the simplest admissible equipment-based method that covers installed and lifecycle scope.
- **Assumptions:** Existing hydraulic calculations can supply conceptual equipment demands; admissible sources may support separate helium equipment estimates.
- **Abandonment conditions:** Evidence cannot support helium equipment applicability or installed boundaries without an owner-held scientific/scope decision.
- **Intended model increment:** Separate quantity-driven cooling subaccounts replacing overlapping aggregate estimates.
- **Intended study question:** How do complete cooling costs change reference and selected-design economics, and how do circuit count, demand and layout assumptions affect those results?

### T-001 scope

- **Objective:** Establish current account boundaries, verify starting cases, and identify admissible source methods and gaps.
- **Why now:** R7.S2 lacks separately sized cooling cost accounts despite calculated hydraulics.
- **Scope:** Read-only model/retained-record tracing and native research; write boundary and research evidence. No model implementation.
- **Inputs:** `goal.md`; retained source/study records named there; current models and registered clean sources.
- **Done when:** A checked boundary map and source-applicability basis support design, or bounded evidence identifies what is missing.
- **Stop when:** Strategy blocker, owner gate or declared limit.

### T-001 start — 2026-09-18

T-001 · native research and retained-model inspection · account-boundary map, starting-case verification and source-method assessment. Independent tracing tasks may run in parallel: account tracing owns its evidence report; source research owns its research artifacts. Neither changes models or the other's files; coordinator owns the goal trail.

### T-001 evidence checkpoint — 2026-09-18

[AGENT] `evidence/account-boundary-map.md` and `evidence/starting-cases.json` establish the entering account map and historical scenarios. Both are unpinned; no native digest. Fresh physical-source review is deposited at `evidence/sizing-source-review.md` (unpinned; no native digest); it is not a combined implementation approval. Native source acquisition remains in flight under `REQ-COOL-INSTALL-01`.

**Decision:** Trigger: the entering checkout includes computed breeding after the supplied September 18 reassessment. Decision and reason: retain historical scenarios verbatim but replay them against current execution and preserve new breeding failures; this isolates cooling attribution without undoing later work. Tier: execution detail. Decided by: coordinator. Changed: `evidence/replay_starting_cases.py`, `evidence/entering-replay.json` and its log. The first diagnostic invocation lacked the documented teax-simkit import path; correcting that environment path allowed unchanged inputs to execute. This is a diagnostic command correction, not a changed scientific case or a task-level retry.

[AGENT] Entering regression evidence is `evidence/entering-cooling-tests.log`: 131 passes and six failures, before any model changes. This targeted batch is separate from the supplied assessment's eight failures; neither establishes today's full-suite status.

### T-002 scope

- **Objective:** Capture the authorized equipment-cost implementation contract in native modeling PM.
- **Why now:** The boundary map identifies affected interfaces and owner requirements are sufficient to record acceptance before choosing equations.
- **Scope:** Native item registration and specification only; substantial implementation remains gated on the requested fresh review.
- **Inputs:** `goal.md`, owner initiating prompt and `evidence/account-boundary-map.md`.
- **Done when:** Native work item records sizing, source, accounting, lifecycle and validation acceptance with explicit unresolved evidence.
- **Stop when:** Material scope ambiguity or native PM failure.

### T-002 start — 2026-09-18

T-002 · native modeling PM · registered equipment-cost spec. Runs independently of T-001 acquisition: coordinator owns work-item records; research worker owns research records; no shared edits.

### T-002 return — 2026-09-18

- **Outcome:** COMPLETE.
- **Evidence:** `work/active/WI-067_installed-cooling-equipment-costs/spec.md`, native registration in `work/BACKLOG.md` — unpinned; no native digest.
- **Reading:** The owner contract is captured before implementation; source applicability and concrete design remain unresolved under T-001.
- **Decision:** Trigger: cohesive equipment-cost integration needs native ownership. Decision and reason: register WI-067 as one standard item with a short source-gated specification. Tier: execution detail. Decided by: coordinator. Changed: native WI-067 registration and spec; no model/package change.

### T-001 return — 2026-09-18

- **Outcome:** STRATEGY_BLOCKER.
- **Evidence:** `evidence/source-methods.md`; native pending research `knowledge/research/pending/20260918-143536_installed-helium-cooling-cost-methods.md`; initial REGISTERED return and continuation OPERATOR_QUEUE return under `knowledge/research/requests/runs/REQ-COOL-INSTALL-01*/`; `evidence/sizing-source-review.md`, `evidence/accounting-preimplementation-review.md`, `evidence/final-review-and-grade.md`; `answer.md`. All new artifacts unpinned; no native digest at this entry.
- **Reading:** The account boundary and physical anchors are established, but none of the acquired evidence supports a transferable installed helium equipment price. Four original cost sources remain queued. The low-temperature installed methodology cannot be treated as a helium cost model. Independent review holds substantial implementation and grades current R7.S2; the goal is not answered.
- **Decision:** Trigger: acquired source evidence fails the proposed installed-cost basis and required preimplementation gate. Decision and reason: retain WI-067 as unimplemented and end this strategy round with named source/engineering prerequisites; do not substitute unsupported multipliers or rename the aggregate. Tier: execution detail. Decided by: coordinator with independent source/accounting assessment. Changed: research evidence, native specification and diagnostic replay only; models/package/old prices unchanged.
- **Decision:** Trigger: research worker exceeded the initial six-query snapshot before discovering that changing the request did not update the open run. Decision and reason: preserve the deviation and start an explicitly authorized prospective continuation; do not claim the first bound was observed. Tier: execution detail. Decided by: coordinator. Changed: request/run records and pending report disclose initial eleven actual queries; continuation retained nineteen under its twenty-query cap.

### Round 1 result — 2026-09-18

- **Intent:** Unmet. No separate installed cooling estimate, generated increment or equipment-cost study was produced. Current R7.S remains below target.
- **Task sequence:** T-001 source/account trace started; independent T-002 native contract capture COMPLETE; T-001 concluded STRATEGY_BLOCKER after acquisition and independent review.
- **Last semantic outcome:** STRATEGY_BLOCKER: source applicability and installed boundaries cannot be established from acquired evidence; relevant originals are inaccessible in this run.
- **Stop reason:** STRATEGY_BLOCKER plus the required preimplementation hold → strategy blocker closes this round. No claim of literature exhaustion or impossible S3 follows. No pin was promoted and no study was committed.
- **Evidence refs:** `answer.md`, `evidence/final-review-and-grade.md`, `evidence/source-methods.md`, `evidence/preservation.json`, `evidence/entering-replay.json`, `evidence/entering-cooling-tests.log`, WI-067 spec and native research returns (new artifacts unpinned; no native digest until checkpoint commit). Rubric remains `.project/active/demo-depth-rubric/rubric.md@dc0f0b6dc6512b29e1307da647f3a508a1f5356d`.
- **Learning delta:** Proposed: current coolant rollup needs scope replacement and explicit lifecycle interfaces; available physical source anchors do not supply installed price; historical selected-case cooling/economics replay exactly while newer breeding changes full-plant verdicts. Bounded source retrieval failures establish next evidence, not source nonexistence.
- **Finding dispositions:** Six touched prior findings are proposed in `evidence/finding-dispositions.md`; append accepted updates under their existing IDs after review. No new study ID is minted.
- **Cited-ref liveness:** Read current native records and git history. The owner’s intervening breeding-goal close changed administrative records only; this task's model/package and historical study inputs remain unchanged, as `evidence/preservation.json` confirms. No external mutation invalidated the task's scientific evidence.
- **Carry forward:** Owner-held formal closure, reveal and frozen-comparison replacement remain untouched. Next round needs accessible original cost evidence and a reviewed conceptual transfer/design. Native acquisition queue is the concrete next route; no permission request or unsolicited external contact was made.

### Round 1 review — 2026-09-18

- **Reviewer:** Fresh non-author `equipment_review`; original physical, accounting and final grade reviews plus post-result corrective/closure check in `evidence/final-review-and-grade.md`. Coordinator reuses that coverage rather than commissioning duplicate review.
- **Verdict:** FINDINGS. The bounded blocker report and round closure are accepted; substantial implementation remains held and R7.S3 remains unmet.
- **Checks:** The reviewer confirms corrected answer values/claims, exact rubric grade, current executable/replay identity, scope, query-limit deviation, task-versus-command retry distinction, six proposed finding dispositions and learning delta. Coordinator verifies unchanged model/package/historical paths and archive via `evidence/preservation.json`; entering failures remain disclosed and no full-suite pass is claimed.
- **Accepted dispositions:** Appended six rows under existing study finding IDs in `exploration/stellarator_e2e/studies/DISCOVERY_LOG.md`; first sightings and frozen records unchanged. `evidence/finding-dispositions.md` is accepted by this review. No finding is marked fixed by the unsuccessful source acquisition.
- **Next:** Keep goal and WI-067 open. A later round starts from accessible original equipment-cost evidence and a concrete reviewed transfer/accounting design. Formal goal closure is not recommended.

### Verification note — 2026-09-18

[AGENT] After accepted disposition rows were appended, the native join test returned 26 passes and one failure on the unchanged computed-tritium-breeding record, whose finding IDs the existing parser does not recognize before it reaches log membership. Both touched prior study records pass. `evidence/discovery-join-tests.log` preserves this separate existing consumer failure; no parser or breeding-record change was made. Two goal-contract tests pass. The answer discloses all three distinct scoped batches; none is reported as a clean full suite.

### Evidence checkpoint — 2026-09-18

The Round 1 evidence is committed at `1031e7ff`: `work/orchestration/goals/installed-cooling-equipment-costs/@1031e7ff`, `work/active/WI-067_installed-cooling-equipment-costs/spec.md@1031e7ff`, `knowledge/research/pending/20260918-143536_installed-helium-cooling-cost-methods.md@1031e7ff`, both `REQ-COOL-INSTALL-01` request/run trees at that revision, the registered INL source and native index/manifest at that revision, and accepted discovery-log rows at that revision. This supplies pinned citations for the earlier explicitly unpinned entries. It is a research/diagnostic checkpoint, not a promoted executable pin or committed equipment-cost study. Source-extraction and test-log whitespace is retained verbatim. The context note in `.project/CURRENT_WORK.md` remains uncommitted with the owner's pre-existing edits. No goal/item closure, merge or push occurred.

## Round 2 — independent-conceptual-cost-method

### Strategy revision — 2026-09-18

- **Approach:** [AGENT] Pursue original helium-reactor estimates and independently published equipment-based methods in parallel. Build a concrete conceptual reference estimate where source applicability supports it; use explicit justified layout/topology/lifecycle scenarios instead of demanding a qualified plant design.
- **Assumptions:** Failure to retrieve particular reports does not establish absence of an admissible conceptual cost method. A different reference technology may be useful only with a defensible transfer.
- **Abandonment conditions:** Neither route provides an applicable source basis, or a required technology/scope choice reaches an owner gate. Ordinary round closure alone is not a reason to pause.
- **Intended model increment:** Reviewed independent pump, piping and exchanger cost accounts with installation/lifecycle boundaries, if the concrete estimate survives review.
- **Intended study question:** Separate the effect of missing costs from changed circuit count, demand and layout on the retained reference and selected-design cases.

### T-003 scope

- **Objective:** Recover original helium equipment cost methods through genuinely alternate routes and assess applicability.
- **Why now:** Four known reports were inaccessible in Round 1, but conceptual methods remain untested.
- **Scope:** Native source acquisition, original-table checks, evidence report; no model changes or external messaging. Own REQ-COOL-R2-ORIGINALS request/run and evidence/round2/originals report.
- **Inputs:** Round 1 source-methods and queue at1031e7ff; goal.md and quarantine protocol.
- **Done when:** Checked original method with boundaries or precise retained acquisition/application gap.
- **Stop when:** Declared search/capture limits, material gate or source contamination.

### T-003 start — 2026-09-18

Native research · alternate original recovery · new source/method evidence. Parallel with T-004: separate requests and report ownership, no shared model edits; source registry writes coordinated through native lock.

### T-004 scope

- **Objective:** Establish an independent published conceptual estimating route for gas circulators, high-pressure exchangers and fabricated installed piping.
- **Why now:** This route tests whether the particular inaccessible reactor reports are actually necessary.
- **Scope:** Native research and source applicability; explicit pressure/temperature/material/scale and installation/lifecycle treatment. Own REQ-COOL-R2-METHODS and evidence/round2/methods report. No model changes.
- **Inputs:** goal.md; existing account map and sizing-source-review at1031e7ff; quarantine protocol.
- **Done when:** One concrete reference estimate can be assembled, or exact missing terms and investigated methods are documented.
- **Stop when:** Declared acquisition limits, material gate or source contamination.

### T-004 start — 2026-09-18

Native research · independent published estimating methods · source-supported candidate equations, domains and price boundaries. Coordinator owns integration, target equipment assumptions, goal trail and reviewer dispatch.

### T-005 scope

- **Objective:** Turn reviewed thermal requirements into a concrete conceptual equipment specification and account/verification design for source-method comparison.
- **Why now:** Cost-source applicability cannot be judged from thermal duty alone.
- **Scope:** Native WI-067 design and diagnostic arithmetic; no production equations or installed prices. Coordinator owns WI-067 design and evidence/round2/reference-sizing files. Parallel source work cannot invalidate retained demand inputs; competing source technologies remain alternatives, not silently adopted choices.
- **Inputs:** WI-067 spec; reviewed Round1 sizing source and entering replay at1031e7ff.
- **Done when:** Per-machine requirements and conditional exchanger sizing are explicit; pipe/layout and lifecycle missing inputs are named; concrete source methods can be matched against this basis.
- **Stop when:** A material scientific choice is unavoidable, or unsupported source quantities would be needed to claim a result.

### T-005 start — 2026-09-18

Native design-model workflow · WI-067 design and reference specification · conditional physical sizing and account/test contract, with cost acceptance pending T-003/T-004.

### T-003 return — 2026-09-18

- **Outcome:** COMPLETE.
- **Evidence:** `evidence/round2/originals.md`; native `REQ-COOL-R2-ORIGINALS` registered return; two registered original reports, paths and source hashes in that report. New evidence unpinned; no native digest for report.
- **Reading:** Original sources clarify conceptual cost-transfer and replaceable-internals boundaries; they do not establish an isolated helium circulator price. Source registration is not equipment-cost acceptance.

### T-004 return — 2026-09-18

- **Outcome:** COMPLETE.
- **Evidence:** `evidence/round2/methods.md`, `methods-diagnostic.json`; native `REQ-COOL-R2-METHODS` registered return with four sources. New reports unpinned; no native digest.
- **Reading:** Independent methods supply explicit nuclear stainless fabrication and process installation categories. Generic gas-machine and modular-exchanger prices remain conditional/off-family diagnostics. Source applicability and overlap normalization require independent review before scientific implementation.

### T-005 return — 2026-09-18

- **Outcome:** COMPLETE.
- **Evidence:** WI-067 `design.md`; `evidence/round2/reference-sizing.json`, `reference_sizing.py`, `reference-review.md`. New records unpinned; no native digest.
- **Reading:** Independent arithmetic matches the four cases. The design now distinguishes required exchanger area from installed geometry and prevents a silent price reduction under unchanged hydraulic losses. This is a reviewed reference specification, not a released cost implementation.

### T-006 scope

- **Objective:** Resolve the remaining low-ratio/high-casing helium circulator price-method applicability gap through novel primary-source routes.
- **Why now:** The independent handbook route has a concrete service-family mismatch, and original whole-system estimates cannot isolate a machine price.
- **Scope:** New bounded native research request; no model changes. Researcher owns request/run and `evidence/round2/circulator-transfer.md`; coordinator owns design integration. Independent reviewer concurrently assesses the acquired method transfers.
- **Inputs:** `evidence/round2/circulator-followup-brief.md`, methods/originals reports and registered originals, exact retained machine specifications.
- **Done when:** A defensible conceptual machine estimate is available or the remaining acquisition/engineering blocker is precisely established.
- **Stop when:** Prospective15-query/3-capture limit, contamination or material owner gate.

### T-006 start — 2026-09-18

Native research · helium circulator transfer · narrower source-applicability question following T-003/T-004. Previously registered PROCESS acc2261 was inspected: its combined pumps/pipes thermal-power allowance cannot supply separate equipment estimates. No additional source fetch was needed for that rejection. This task continues the current conceptual-method strategy without a routine approval pause.

### T-007 scope

- **Objective:** Assemble the independently requested conditional quantity/price ledger and expose exactly which installed estimate terms are still unsupported.
- **Why now:** The fresh source review accepts explicit conceptual analogies rather than requiring vendor qualification, but the acquired methods have not yet been reconciled into a concrete scope ledger.
- **Scope:** WI-067 design supplement and diagnostic ledger only. No production price replacement or generated package. Coordinator owns these files while T-006 searches the remaining machinery gap.
- **Inputs:** `evidence/round2/method-review.md`, corrected methods report, registered ANL/NETL/Seider/CPI sources and reference sizing.
- **Done when:** Four-case machine purchase and explicit pipe-layout quantities are priced where supported, raw years preserved, installation categories assigned, and omitted scope is null rather than silently zero.
- **Stop when:** Reviewer rejects a transfer or source evidence cannot price a necessary term.

### T-007 start — 2026-09-18

Native design-model workflow · conditional quantity and accounting ledger · focused independent source/design review follows. Existing source equations and deliberately assumed layout sensitivities are diagnostic; this task does not claim an installed plant result.

### T-006 return — 2026-09-18

- **Outcome:** COMPLETE.
- **Evidence:** `evidence/round2/circulator-transfer.md`, native `REQ-COOL-CIRCULATOR-TRANSFER` registered return, three original sources and image checks; `evidence/round2/new-source-review.md`. New reports unpinned; registered source hashes are in the native receipts.
- **Reading:** Original helium price anchors now exist. Independent review accepts explicit conceptual transfer methods for a concrete design, with historical scale/package uncertainties. The prior absence of an inspectable helium component price is resolved; no calibrated target quote or complete installation claim follows.
- **Decision:** Trigger: source research and fresh review found usable component methods. Decision and reason: continue into a concrete quantity and accounting design; no routine round pause. Tier: execution detail. Decided by: coordinator. Changed: WI-067 candidate design and T-007 scope continuation.

### T-007 evidence and material decision — 2026-09-18

[AGENT] Additional existing-source inspection found an explicit ANL exchanger component-mass and installation method (`evidence/round2/hx-method-check.md`, accepted in `new-source-review.md`). This resolves the need to force a large exchanger into a small-equipment area correlation. `conditional-ledger.json` retains the earlier partial machine/main-pipe diagnostic; unresolved entries are null. WI-067 `primary-candidate.md` now specifies a reviewable construction and price scope; it is not an implementation release.

**Decision:** Trigger: completing intermediate pumps, pipes and inventory requires a coolant choice absent from the current plant model; source HITEC temperatures were only a conditional thermal reference. Decision and reason: ask the owner whether to adopt a HITEC270–465°C intermediate scenario while preserving primary helium. This is a material scientific choice reserved in the initiating prompt. Tier: reserved gate. Decided by: pending owner. Changed: asynchronous owner question; dependent intermediate-technology adoption is parked. Independent primary equipment design/review continues.

[AGENT] A source-reading correction was resolved before adopting installation parameters: ORNL Table3.2 installation is27%of hardware including procurement, not35%;35%is its separate engineering row. The independent reviewer corrected `new-source-review.md` against the original image. No production parameter had been written from the mistaken reading.

### T-007 return — 2026-09-18

- **Outcome:** OWNER_GATE.
- **Evidence:** WI-067 `primary-candidate.md`; `evidence/round2/conditional-ledger.json`, `primary-hardware-estimate.json`, associated diagnostic scripts and `candidate-review.md`; current `answer.md`. New artifacts unpinned; no native digest for reports.
- **Reading:** The concrete primary candidate and source transfers are independently checked and remain partial. The current model has no selected intermediate coolant, and its aggregate cannot be declared disjoint from the new exchanger price by relabeling. The requested material technology choice is pending; dependent full account reconciliation and production replacement remain parked. Other explicit primary quantity/lifecycle omissions are retained for the next design task, not asserted complete.
- **Decision:** Trigger: completing the intermediate equipment requires an architecture absent from the existing model. Decision and reason: retain the current model and ask for the explicitly recommended HITEC scenario, under the owner's scientific-decision reservation. Tier: reserved gate. Decided by: owner, pending. Changed: asynchronous question and documented candidate; no model/package change.

### Round 2 result — 2026-09-18

- **Intent:** Research/design strategy materially advanced; goal remains unmet. Usable original helium references and finished nuclear exchanger/pipe methods replace the prior source-access-only blockage. No cost replacement, promoted pin or native equipment-cost study occurred.
- **Task sequence:** T-003 original recovery COMPLETE; T-004 independent methods COMPLETE; T-005 concrete specification COMPLETE; T-006 helium transfer COMPLETE; T-007 conditional ledger OWNER_GATE after independent source, arithmetic and accounting review.
- **Last semantic outcome:** OWNER_GATE: select or leave undecided the intermediate coolant before a complete equipment/accounting design is adopted.
- **Stop reason:** An unresolved owner-held scientific decision, not an ordinary round boundary. The asynchronous question recommends HITEC270–465°C secondary service with primary helium retained. No automatic owner answer or approval is inferred from elapsed time.
- **Evidence refs:** WI-067 `design.md` and `primary-candidate.md`; `evidence/round2/{originals,methods,hx-method-check,circulator-transfer,reference-review,method-review,new-source-review,candidate-review}.md`; diagnostic ledgers; three new native research request/run trees; current `answer.md`. New records unpinned; registered source identities are in native receipts.
- **Learning delta:** Proposed in `evidence/round2/dispositions.md`: usable conceptual source transfer is now possible; original equipment/rating/installation boundaries matter; intermediate technology and allowance scope cannot be silently settled. No claim of qualified equipment, calibrated uncertainty, complete installed cost or new plant economics.
- **Finding dispositions:** Six prior IDs are addressed in `evidence/round2/dispositions.md`; retain first sightings and append accepted updates only. No finding is marked fixed and no study ID is minted.
- **Cited-ref liveness:** Coordinator inspected current model/package/historical path changes; none occurred during this research round. New native source registrations and candidate records are intended task writes. The frozen comparison and existing scientific inputs remain unchanged; no external mutation invalidated the evidence.
- **Carry forward:** Owner's no-routine-pause instruction remains in force. After the scientific decision, continue the concrete design, complete equipment/lifecycle scope, obtain ledger release, implement and run the focused native study. Current independent R7.S2 assessment remains applicable. Formal goal/item closure, reveal, frozen replacement, merge and push remain untouched.

### Round 2 review — 2026-09-18

- **Reviewer:** Continuing fresh non-author `equipment_review`; focused coverage in `reference-review.md`, `method-review.md`, `new-source-review.md`, `candidate-review.md`, and post-result `closure-review.md` under `evidence/round2/`.
- **Verdict:** FINDINGS. Conditional methods/candidate and the bounded round result are accepted. Production replacement remains held; the intermediate technology is a material owner decision and other scope/lifecycle gaps remain explicit. Goal closure is not recommended.
- **Checks:** Original image and independent arithmetic reviews cover source interpretation, sizing, price years, source/extrapolation boundaries and installation denominators. Coordinator confirms unchanged production/historical paths and archive in `evidence/round2/preservation.json`. The answer and six proposed prior-finding dispositions were checked after the round result. No mechanical task retry, independent implementation pass or native equipment-cost study is claimed.
- **Accepted dispositions:** `evidence/round2/dispositions.md`; append its six updates under the existing IDs. No cooling gap is marked fixed. Other unrelated findings remain unchanged.
- **Accepted learning delta:** Append the three proposals from `dispositions.md` to `learnings.md`. They supersede source-access-only next steps without claiming complete costing.
- **Next:** Owner answers the intermediate-fluid choice; next round continues within existing authorization. No routine round confirmation, formal goal/item closure, reveal, merge or push.

### Round 2 verification note — 2026-09-18

[AGENT] After appending accepted disposition rows, the native discovery join check returns26passes and the same existing breeding-record parse failure as Round1. Both touched historical studies pass. `evidence/round2/discovery-join-tests.log` retains the result. The two checks in `tests/orchestration/test_goal_contract.py` pass, but their actual coverage is repository ADR/register coherence and narrative links, not this equipment model. Local answer links were separately checked. `preservation.json` confirms the unchanged frozen archive and scientific paths. No full-suite result is claimed.

### Round 2 evidence checkpoint — 2026-09-18

Round2 evidence is committed at `05737d88`: goal records and `evidence/round2/`, WI-067 design/candidate, three new native request/run trees, nine registered source extractions and their native index/manifest entries, and accepted discovery dispositions. This pins the previously unpinned references above. Original image/extraction artifacts are retained without rewriting their source content. The checkpoint contains no production model or package change and is not a promoted study pin. `.project/CURRENT_WORK.md` retains the context update alongside unrelated uncommitted owner work. No merge, push, reveal, archive or formal goal closure occurred.

### Owner ruling — 2026-09-18

[OWNER-VERBATIM] “yes. proceed”. The owner approves the proposed HITEC270–465°C intermediate scenario with primary helium retained. The Round2 material gate is resolved. Existing authority covers further source work, implementation, generation, studies and independent review without routine round confirmation. Prior evidence remains at05737d88; no intervening scientific model/package changes were found.

## Round 3 — integrated-helium-hitec-equipment

### Strategy revision — 2026-09-18

- **Approach:** [AGENT] Complete a simple explicit helium/HITEC equipment and accounting design using the reviewed component methods, replace both aggregate cooling allowances without overlap, and test the generated cost/performance response.
- **Assumptions:** The approved secondary scenario and existing conceptual fabrication methods can support equipment estimates with explicit uncertainty and lifecycle assumptions; vendor qualification is not the target.
- **Abandonment conditions:** A necessary transfer lacks defensible evidence after bounded review, the integration seam has an independent prerequisite, or a newly material owner decision arises.
- **Intended model increment:** Separately sized primary circulators, secondary pumps, piping, exchanger and inventory accounts; installation, spares/replacement and preserved energy coupling.
- **Intended study question:** At matched retained plant inputs, how much do separately accounted cooling equipment and lifecycle costs change capital and electricity cost, and how do circuit count, demand and stated assumptions affect requirements, costs and checks?

### T-008 scope

- **Objective:** Complete the approved HITEC scenario's thermophysical, pump/pipe/inventory and remaining lifecycle source basis.
- **Why now:** Round2 methods were primary-only; the owner has selected the intermediate fluid.
- **Scope:** Native bounded research and explicit candidate equations; no production model edits. Researcher owns round3 secondary-methods evidence and its request/run. Coordinator owns combined account design; independent reviewer retains non-author status.
- **Inputs:** Owner ruling; Round2 source/candidate reviews; current account map; registered clean sources.
- **Done when:** One concrete conceptual secondary-loop and remaining equipment/lifecycle method is reviewable, with raw price boundaries and explicit assumptions.
- **Stop when:** Prospective source limits, unsupported critical transfer or material owner gate.

### T-008 start — 2026-09-18

Native research · helium/HITEC completion · secondary-methods and residual primary scopes. Parallel with coordinator accounting/interface design because files are separate; unresolved source assumptions are not adopted before review.

### T-009 scope

- **Objective:** Complete the combined helium/HITEC equipment, accounting and lifecycle design and obtain independent implementation release.
- **Why now:** Owner selected HITEC and the primary conceptual methods have independent source checks; remaining decisions are concrete account ownership and secondary interfaces.
- **Scope:** WI-067 design/plan and diagnostic equations only before release; coordinator owns these files. T-008 owns separate source research and does not edit models. Preserve scientific and historical production outputs.
- **Inputs:** Goal and owner ruling; Round2 primary candidate and reviews; Round3 criterion guidance, secondary source methods and CAS23 implementation trace.
- **Done when:** Reviewer can accept a specific equipment ledger and its model/study verification contract or identify a bounded prerequisite.
- **Stop when:** Material owner decision, unsupported principal equipment method, or unavailable required independent review.

### T-009 start — 2026-09-18

Native design-model and plan-model · WI-067 combined design, accounting convention, persistent implementation checklist and independent preimplementation review.

### T-008 return — 2026-09-18

- **Outcome:** COMPLETE. Registered four clean original sources and supplied HITEC properties, exact generic-liquid pump/motor equations and ranges, salt inventory price scope, industrial operating/maintenance observations and a salt-to-steam thermal reference. Evidence: `evidence/round3/secondary-methods.md`; `REQ-COOL-HITEC-COMPLETION` native request/run.
- **Reading:** A conceptual secondary equipment estimate is possible. Hot-salt pump construction and procurement-scale transfer remain assumptions. Salt-to-steam evidence is retained for Row8, not silently charged within the new Row7 total.
- **Decision:** Failed text/plain extraction triggered one additional capture of the same screened code as renderedHTML. Reason: recover authoritative equations without another research question. Tier: execution detail. Decider: coordinator. Changed: request/run amendment and registered SSC source, with extraction limitation retained.
- **Decision:** Independent boundary review supports Row7 ending at the salt supply/return interface. Reason: preserve cooling scope and single equipment owner without unsupported CAS23 deductions or turbine redesign. Tier: execution detail with explicit inherited price uncertainty. Decider: coordinator after non-author review. Changed: WI-067 combined design and `evidence/round3/accounting-convention-review.md`; steam generator assigned Row8 with price inclusion unverified.
- **Decision:** Existing480°C efficiency-fit argument exceeds465°C salt supply. Reason: the new intermediate scenario does not validate that inherited conversion fit. Tier: premise surprise, surfaced in commentary and design. Decider: coordinator retains the numerical fit solely as a labeled surrogate and requires a failed physical-interface screen. Changed: combined design; physical whole-plant feasibility conclusions remain parked.

### T-009 return — 2026-09-18

- **Outcome:** COMPLETE. Fresh non-author review released the corrected Row7 conceptual design. Evidence: WI-067 `combined-design.md`, `plan.md`, and `evidence/round3/combined-design-review.md`.
- **Reading:** Principal independently sized equipment and lifecycle coverage are adequate to implement. Auxiliary omissions, unresolved conversion interface and source applicability remain explicit limits; S3 awaits executable evidence.
- **Decision:** Corrected inventory boundary, CPI2021 value, exact pump ranges, secondary energy identities and conversion-surrogate meaning after review. Reason: reproducible quantities and honest operating/price scope. Tier: execution detail, with conversion premise surprise already surfaced. Decider: coordinator with independent corrective release. Changed: combined design; no production model change yet.

### T-010 scope

- **Objective:** Implement and verify the released equipment and lifecycle accounts in the native model and generated executable.
- **Why now:** T-009 obtained the required preimplementation release.
- **Scope:** WI-067 canonical models, generated package, oracle, affected consumers and targeted tests. Delegate new equipment analysis/manual implementation separately from coordinator-owned plant wiring, generation, regression and records. Preserve unrelated work and historical studies.
- **Inputs:** Released combined design and corrections, T-008 methods, primary source reviews, entering package and test evidence.
- **Done when:** Independent quantities/source checks, native generation, account/energy identities and relevant regressions support a reviewable implementation and integration pin.
- **Stop when:** Unsupported semantic premise, native tooling prerequisite, material owner gate or exhausted mechanical retry limit.

### T-010 start — 2026-09-18

Native implement-model · canonical cooling equipment/lifecycle accounts and generated executable. Separate analysis/manual-body authorship from plant wiring and generation because their interface can be fixed before integration; coordinator integrates sequentially.

### T-010 progress — 2026-09-18

[AGENT] Canonical child equipment accounts, native manual implementation, plant energy/cost/lifecycle consumers and independent oracle are implemented. Fresh native generation is repeatable. The98-test targeted batch passed; the expanded consumer batch has71passes and the same six entering stale-contract failures, with new four-case native coverage reaching all358 mapped outputs. Evidence: WI-067 `evidence/verification-status.md` and its linked logs. Independent implementation review found one invalid-mode defect; the new scenario guard is tested and awaits narrow corrective review. No study pin has been promoted and no S3 grade is claimed yet. Study preparation is delegated to `r2_originals`, owning only the new study directory while the coordinator finishes the audited pin. No study points may run before the native integration release.
