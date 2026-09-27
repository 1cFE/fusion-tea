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
