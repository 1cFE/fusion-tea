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
