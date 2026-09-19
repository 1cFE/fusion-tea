# Trail: Throughput-based fuel-processing costs

## Round 1 — applicable-throughput-cost-basis

### Strategy revision — 2026-09-19

- **Approach:** Consume the completed inventory goal's running-flow interface and identify an admissible process-cost basis matching the represented architecture.
- **Assumptions:** Existing verified fuel flows can drive an aggregate S2 estimate without changing loss assumptions or process technology.
- **Abandonment conditions:** No applicable cost basis, an unavailable capacity quantity, or a material technology/scope decision requiring the owner.
- **Intended model increment:** Replace overlapping power-proxy process capital with a source-supported throughput relationship in plant capital and LCOE.
- **Intended study question:** How do actual flow drivers change processing capital and LCOE, separately from price uncertainty and process assumptions?

### T-001 scope

- **Objective:** Establish the exact upstream capacity interface and process/account boundaries, and determine whether admissible sources support costing them.
- **Why now:** The upstream inventory goal has closed but its verified flows have not yet replaced the old cost proxy.
- **Scope:** Native internal-first research and read-only model tracing; new sources through research seam; no scientific implementation before fresh source/interface review.
- **Inputs:** goal.md and its grounding evidence, upstream throughput interface, registered sources and clean cost implementations.
- **Done when:** A cited capacity/account map and cost-source applicability assessment support a positive approach or concrete evidence gap.
- **Stop when:** Prerequisite, strategy blocker, owner gate or declared limit.

### T-001 start — 2026-09-19

T-001 · native research and current-model inspection · evidence/current-trace.md and native research report. Source research may run independently of the coordinator's current-flow/account inspection; the researcher owns its request, source registrations and research report, while the coordinator owns the goal records and current trace. Neither changes model files.

### T-001 return — 2026-09-19

- **Outcome:** COMPLETE.
- **Evidence:** evidence/current-trace.md, evidence/entering-evidence.json, evidence/entering-fuel-tests.log, evidence/interface-review.md, evidence/source-review.md; knowledge/research/pending/20260919-091411_throughput-based-fuel-processing-cost-applicability.md and its native request/run receipts (all currently unpinned; no native digest).
- **Reading:** The existing interface is usable as a conditional operating isotope-load producer. Native research registered original historical process-cost sources, but the fresh source review does not yet accept transfer to this plant. Source registration and interface validation do not satisfy the processing-cost target.
- **Decision:** Verified producer and independent interface PASS · reuse WI-069 quantities rather than duplicate mass balance · execution detail · coordinator · evidence/current-trace.md.
- **Decision:** Source review FINDINGS on process/feed/scale transfer · hold scientific implementation and investigate the specific transfer premise · execution detail · coordinator following fresh reviewer · evidence/source-review.md; no model changes.
- **Decision:** A challenge-page capture passed registry quality checks · reject its evidentiary use and retain truthful native receipts · execution detail · researcher and coordinator · native research report's acquisition-defect section; no registry internals rewritten.

### T-002 scope

- **Objective:** Determine whether reactor-scale conventional cleanup and cryogenic isotope-separation designs support the process/feed/capacity transfer identified by the source review.
- **Why now:** T-001 located a real reactor-oriented cost law but left its connection to the current functional processor unsupported.
- **Scope:** A new, narrower native research question about engineering process applicability near the actual operating isotope load, not another broad cost search. Preserve current architecture and losses; no direct internal recycling, invented train replication or model edits. Source review is reused for original price/exponent checks.
- **Inputs:** goal.md; T-001 report; evidence/source-review.md findings1–3; verified WI-069 interface.
- **Done when:** A reasoned source-supported transfer proposal resolves those findings, or bounded evidence establishes the concrete missing process specification and next step.
- **Stop when:** Prerequisite, strategy blocker, material owner-held technology choice or declared limit.

### T-002 start — 2026-09-19

T-002 · native targeted engineering research · source-supported transfer proposal or bounded negative, owned by the continuing research agent. Six additional targeted searches and at most two captures are authorized for this narrower question. No implementation proceeds on a merely plausible extrapolation.

### T-002 return — 2026-09-19

- **Outcome:** OWNER_GATE.
- **Evidence:** knowledge/research/pending/20260919-092112_conventional-reactor-fuel-processing-transfer.md and native request/run at `66548f14`; evidence/source-review-r2.md, evidence/proposed-cost-scope.md, evidence/proposed-price-example.json, evidence/proposed-price-review.md and evidence/current-r10s-grade.md (goal evidence awaiting its local checkpoint).
- **Reading:** Independent review accepts the joined historical cost method and larger conventional reactor-process design as a conditional conceptual transfer. Selecting that process and unverified feed condition as the plant cost basis is a material owner decision. A reviewed numerical scope example is prepared; source qualification alone leaves the executed grade unchanged.
- **Decision:** New process/feed premise would control plant capital · ask the owner to adopt the conditional conventional scenario; do not implement before that decision · reserved gate · owner decides, fresh reviewer identified gate and coordinator requested ruling · pending question; answer.md and proposed-cost-scope.md make the choice reviewable.
- **Decision:** Raw price years and four source equipment rows can be made concrete without selecting the plant technology · prepare a limited purchasing-power example and independent accounting/arithmetic check · execution detail · coordinator, reviewed by source reviewer · evidence/proposed_price_example.py and linked output/review; no model or study changes.

### Round 1 result — 2026-09-19

- **Intent:** Unmet as an implemented throughput-cost increment; met as an applicable conditional source-basis investigation with an explicit adoption decision.
- **Task sequence:** T-001 COMPLETE; T-002 OWNER_GATE.
- **Last semantic outcome:** OWNER_GATE.
- **Stop reason:** The last outcome OWNER_GATE plus an unresolved reserved scientific decision closes this round.
- **Evidence refs:** Both native research reports/request runs@66548f14; answer.md and linked independent interface, source, price and current-grade evidence.
- **Learning delta:** Verified operating isotope throughput is available; reactor-oriented historical costing can be transferred conditionally using larger conventional process-design evidence, but neither source acceptance nor a price example changes the executed grade.
- **Finding dispositions:** No new native study ran and no committed study finding was reinterpreted or changed; no discovery-log row minted or amended. This round's source applicability findings are routed through the owner-held scenario decision in answer.md.

### Round 1 review — 2026-09-19

- **Reviewer:** Coordinator check with independent source/interface/price/grade coverage reused; no additional round critic would cover a distinct unresolved risk.
- **Verdict:** OWNER_GATE.
- **Checks:** Native research reports and receipts resolve at `66548f14`; original-source checks, producer identity and tests support the recorded claims. T-002 answered the specific transfer uncertainty without implementing a new technology or modifying losses. No native mechanical retry or study execution occurred; acquisition transport/quality defects remain in truthful receipts. No touched study disposition remains unrouted. Source and price limitations remain explicit. Model and executable producer paths retain the audited upstream version. Corrective local-controls and limited-containment wording was applied after price review; no numerical proposal changed.
- **Learning delta:** Accepted only within the conditional research scope; recorded in learnings.md. R10.S1 remains the actual current grade.
- **Next:** Owner adoption decision. The goal remains open; a resolved gate permits a new round, not reopening this closed round or claiming completion.

### Owner ruling — 2026-09-19

[OWNER-VERBATIM] “yes, adopt and continue”. The material process/feed adoption gate is resolved. [AGENT] (ratified by owner, 2026-09-19) Adopt the reviewed conditional conventional process and its declared scope from evidence/proposed-cost-scope.md@8014aa19. Fresh source, interface and price reviews remain applicable: their sources and producer files have not changed. Other reserved decisions remain owner-held. The prior round stays closed.

## Round 2 — integrated-conventional-processing-cost

### Strategy revision — 2026-09-19

- **Approach:** Replace the legacy fuel-handling power proxy with the adopted source-row aggregate driven by WI-069 running D+T exhaust throughput, preserving explicit cost and process assumptions.
- **Assumptions:** The owner-adopted source-conditioned conventional scenario applies; the reviewed four-row historical price scope is distinct from existing civil, fuel-purchase and startup allowances.
- **Abandonment conditions:** A newly found source/account overlap cannot be resolved within the adopted scope, or an interface/runtime limitation requires a separately owned prerequisite.
- **Intended model increment:** An executed throughput-driven processing account with explicit capacity margin, price assumptions and truthful applicability, integrated once into plant capital and LCOE.
- **Intended study question:** How do burn fraction, recovery, operating demand, availability and separately varied price/capacity assumptions affect processing demand, cost and LCOE without hiding failed plant cases?

### T-003 scope

- **Objective:** Implement and verify the adopted processing-cost relationship through a native modeling item, including final account reconciliation and independent design/integration review.
- **Why now:** The owner has accepted the conditional process basis; original-source and interface uncertainties are covered by retained independent reviews.
- **Scope:** Native model requirements/design, affected model and generated consumers, meaningful source/domain/accounting regressions and review. Preserve generic legacy behavior, actual upstream producer ownership, all fuel losses, historical studies and r2. The author owns the modeling item and its model/runtime/oracle/test changes; coordinator owns goal records and subsequent integration/study execution.
- **Inputs:** goal.md; approved scenario evidence/proposed-cost-scope.md@8014aa19; source and price reviews; native research@66548f14; WI-069 producer@956444b5; owner ruling above.
- **Done when:** A reviewed native item supports generated execution of the complete throughput-to-capital-to-LCOE chain, with accounting overlap resolved and relevant checks recorded.
- **Stop when:** Prerequisite, strategy blocker, new material reserved decision or declared limit. Source/design review findings are resolved before dependent implementation.

### T-003 start — 2026-09-19

T-003 · native modeling PM item registration and continuing author · expected spec/design/implementation evidence and independently reviewed candidate. The coordinator may prepare a study protocol and inspect integration procedures read-only while the author works; no overlapping package generation or source/PM mutation.

### T-004 scope

- **Objective:** Prepare and execute the focused native throughput/price sensitivity study against the reviewed integrated candidate.
- **Why now:** The adopted model design fixes the intended study questions; preparation can proceed without executing a changing producer.
- **Scope:** Study-local protocol, scripts, complete native record and discovery-log rows only. The continuing interface reviewer becomes study author and will not supply final independent certification. No producer, shared route, historical record or git edits. Package-dependent steps wait for coordinator release.
- **Inputs:** goal.md, owner prompt result 7 and adoption ruling; evidence/study-proposal.md and study-executor-brief.md; eventual audited integration candidate.
- **Done when:** A verified, frozen native study explains demand, price and process-assumption effects with failures and omitted costs visible.
- **Stop when:** Missing integration candidate for dependent execution, new owner-held decision, scientific premise surprise or native mechanical refusal.

### T-004 start — 2026-09-19

T-004 · exploration/stellarator_e2e/studies/20260919-throughput-based-fuel-processing-costs/ · expected prepared protocol followed by released native execution and frozen record. Parallel preparation with T-003 is safe because file ownership is disjoint; revised ABI changes can invalidate prepared declarations, so all package-derived keys and execution wait for the integrated candidate. Root deposited initial intake/protocol and reusable inactive lifecycle scripts; the delegated author continues them.

### T-003 execution allocation — 2026-09-19

Independent design review passed in evidence/design-review.md; coordinator released implementation. While production author changes model/seeds/generation and integrated accounting, the study author separately implements oracle_fuel_processing.py and source/domain reference tests under evidence/oracle-author-brief.md. These writes are disjoint, with a fixed dict API in the brief and proposed ABI. The source/design reviewer remains non-author for substantive integration audit and final grading. This parallel arithmetic implementation changes no scientific scope or native task outcome.

### T-003 return — 2026-09-19

- **Outcome:** COMPLETE.
- **Evidence:** work/active/WI-070_throughput-based-fuel-processing-costs/audit.md and evidence/author-validation.md; goal evidence/implementation-review.md and implementation-review/checks.json. Reviewed executable `3e3bf467fd98ad927cf12409f1c36807b92e9e8eaa4fd598a2fcd79c00ae698f`; semantic `37ca31ff0412f56a67301fa4e714b1dba2e74df6788348ce97dd5ee64d98d62f`.
- **Reading:** Non-author audit passes the source-to-throughput-to-total implementation. Seven fresh native cases pass 6,538 mapped comparisons; 176 reviewer tests pass. Author checks pass 172 source/domain, 263 affected and 13 family tests; suites overlap and are not summed as unique tests. Static L2 fails unchanged and L6 adds three known unsupported-dot instances; these are disclosed, not passes. S2 grading still requires integrated study evidence.
- **Decision:** Package-local controls overlap was not historically disaggregated · assign included local controls only to C220500 and distinct supervisory/plasma functions only to C220700, preserving its coefficient as an uncalibrated residual allowance · execution detail · coordinator, independently reviewed · design/account docs and both modeled account boundaries.
- **Decision:** Source direct installation reached generic freight · remove its contingency-loaded amount from freight while preserving other reviewed project allowances · execution detail · author proposed, coordinator released, independent audit passed · shipping/supplementary consumers and exact account identity tests.
- **Decision:** Native conditional price is verified without changing fuel physics · accept the audited candidate for native integration, retaining explicit scientific/monetary limits · execution detail · coordinator relying on independent audit · candidate commit follows; no formal goal closure.

### T-005 scope

- **Objective:** Obtain the native integration candidate for the audited WI-070 package and release that exact producer for T-004.
- **Why now:** Implementation audit passed with exact model/package/seed identities and no open findings.
- **Scope:** Explicitly scoped local candidate commit, native ten-gate integration and study candidate authorization. No new model semantics, historical study edits, merge or push.
- **Inputs:** goal.md; T-003 audited identities and native item audit; current package manifest, model snapshot, census and retained toolchain revision.
- **Done when:** Native integration returns CANDIDATE with all gates passing and the study release names that exact pin.
- **Stop when:** Native refusal, changed semantic premise, missing dependency or reserved owner decision. Mechanical retries follow the runbook cap.

### T-005 start — 2026-09-19

T-005 · audited WI-070 local commit and evidence/round2/integration/ · expected exact-pin integration return. T-004 remains paused until this return; model mutation is stopped.

### T-005 return — 2026-09-19

- **Outcome:** COMPLETE.
- **Evidence:** Audited model commit `2a50d3ec40e587af25beadaa9bd26c305b9ac11d`; evidence/round2/integration/integration_return.json. All ten gates pass. Regeneration changes no generated byte; all 133 handwritten files are preserved; census has 489 public entries.
- **Reading:** Native integration accepts the reviewed semantic/executable identity. The manifest gate explicitly did not run assert_read_set_covered; that limitation remains and is not claimed covered by another check.
- **Decision:** All required native integration gates passed · promote the sole round candidate for the focused sensitivity study · execution detail · coordinator · study preparation/integration-return.json and execution-release.json. Candidate indicator pin is `50c9d4b9b3bf16fdb00e5c726011f2b434bfa0ba8970569795372a12364c312b`; audited executable remains `3e3bf467fd98ad927cf12409f1c36807b92e9e8eaa4fd598a2fcd79c00ae698f`. Axis ruling and window release remain sequential obligations before dependent native points.

### T-004 return — 2026-09-19

- **Outcome:** MECHANICAL_FAILURE.
- **Evidence:** First native attempt retained by executor under study results/attempt-1/. Fifteen active-method cases executed; five legacy controls were rejected at route admission before model evaluation.
- **Reading:** The stock route's Boolean allowlist does not include the newly introduced processing_enabled input. The generated Boolean field accepts numeric 0/1, as used by its emitted default representation. JSON false was refused by route validation; this is an input-representation mismatch, not a physical or source-domain refusal.
- **Decision:** Preserve all original proposals, results and rejected store rows · retry the same twenty physical/monetary points with legacy selection encoded 0.0 through the existing accepted numeric route · execution detail · coordinator · study proposal encoding and fresh attempt store only. No shared route/model change; old attempt remains evidence. This is retry 1 of the two permitted retries.

### T-004 start — 2026-09-19

T-004 retry 1 · same audited candidate, scope and twenty cases · preserve attempt 1 and run a new native store after replacing Boolean false with equivalent numeric 0.0 for legacy account selection. Original axis authorization applies; record a new exact proposal hash in window-release.json and the mechanical representation correction before execution. No semantic model or scientific window change.
