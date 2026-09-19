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
