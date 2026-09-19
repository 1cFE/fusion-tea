# Trail: Fuel inventory and startup

## Round 1 — residence-and-startup-accounting

### Strategy revision — 2026-09-19

- **Approach:** Extend existing conserved tritium flows with stage residence inventory and a bounded startup condition, using admissible process evidence and explicit scenario assumptions.
- **Assumptions:** Existing burn/exhaust/recovery semantics can remain intact; justified residence ranges can support useful conditional estimates.
- **Abandonment conditions:** Evidence cannot support represented stages, startup cannot be accounted without double counting, or a material reinterpretation requires owner judgment.
- **Intended model increment:** Computed inventory, external startup stock and operating/calendar throughput with a costing interface, preserving achieved-breeding ownership.
- **Intended study question:** Which operating, residence, recovery and reserve assumptions drive stock and processing demand, and does uncertainty prevent a useful estimate?

### T-001 scope

- **Objective:** Establish current stream accounting and an admissible physical basis for stage inventory/startup before substantial implementation.
- **Why now:** The current fuel calculation explicitly leaves inventory dormant; computed breeding now consumes that interface.
- **Scope:** Trace existing equations, draw streams/storage, research admissible process evidence and obtain a fresh source/math/design check. Exclude changes to production equations in this task.
- **Inputs:** `goal.md`; preserved owner prompt; current fuel, breeding and lifecycle implementations; registered sources and prior fuel research.
- **Done when:** A reviewed accounting design supports implementation, or specific evidence/semantic gaps are established.
- **Stop when:** A prerequisite, strategy blocker, owner gate or declared limit is reached.

### T-001 start — 2026-09-19

T-001 · native research and accounting design · expected source register, flow diagram and independent pre-implementation review. Research may run alongside coordinator equation tracing: researcher owns its request/source receipts and research report; coordinator owns the goal trail and proposed accounting. These tasks have disjoint writes; integration waits for research.

### T-001 return — 2026-09-19

- **Outcome:** COMPLETE.
- **Evidence:** `knowledge/research/pending/20260919-074901_fuel-inventory-residence-startup.md`; native REQ-fuel-inventory-01 registered return; `evidence/current-trace.md`; `work/active/WI-069_fuel-inventory-and-startup/design.md`; independent `evidence/math-precheck.md` and `evidence/source-design-review.md` (current additions unpinned; no native digest).
- **Reading:** Source scenarios support a conditional stage-stock and bounded startup calculation. The fresh reviewer releases implementation without claiming physical process qualification.
- **Decision:** Source provides combined cleanup/separation residence only · use one processor at exhaust flow and apply inherited recovery loss at its outlet, preserving existing permanent-loss semantics · execution detail · coordinator, independently reviewed · WI-069 design and flow diagram.
- **Decision:** Plasma stock can be integrated from its existing density profile · prefill that computed stock and feed hardware at t=0, with empty processor/breeding stages · execution detail · coordinator, independently reviewed · WI-069 startup design.
- **Decision:** Residence evidence transfers imperfectly to helium/PbLi · use disclosed source scenarios and assumption sensitivities, retain unsupported retention/bypass/permeation as limits · execution detail · coordinator, independently reviewed · research/design; no physical self-sufficiency claim.

### T-002 scope

- **Objective:** Implement and verify the released fuel inventory/startup model and executable package with a costing throughput interface.
- **Why now:** T-001 source/math/design review passes; entering consumer and static evidence are captured.
- **Scope:** WI-069 canonical/twin models, generated implementation/seed custody, independent oracle/mappings, native metadata and affected tests. Costs and achieved-breeding production method remain outside scope.
- **Inputs:** `goal.md`; WI-069 spec/design; source-design-review and proposed ABI; entering revision and native receipts.
- **Done when:** Audited implementation reproduces named outputs and preserved interfaces, with source/math/domain and regression evidence ready for native integration.
- **Stop when:** A prerequisite, strategy blocker, owner gate or declared limit is reached.

### T-002 start — 2026-09-19

T-002 · WI-069 model/native executable implementation · expected verified and audited package. Parallel implementation/oracle work is authorized with disjoint ownership: fuel_author owns canonical/twin models, generated package, strict seeds and author tests; independent oracle author owns oracle_fuel_inventory.py, verifier/mapping changes and oracle tests. Coordinator owns goal trail, metadata/census/snapshot/manifest and integration. Both implement the same reviewed contract; integration is sequential after both return. No researcher or implementer independently certifies their own work.

### T-002 return — 2026-09-19

- **Outcome:** COMPLETE.
- **Evidence:** WI-069 `audit.md` PASS; `evidence/author-validation.md`, `oracle-regressions.log`, `oracle-native-off-reference.json`, `strict-inventory-baseline.json`, `repin-final.log`, `static-classification.md` and exact generation receipts; goal `evidence/audit-review.md`. Candidate executable `e19b63a03be3a00ebd5cec4ce4ed06a082f5bb7ed89b736aed06feaea8d1e319`; local commit follows (current additions unpinned; no native digest).
- **Reading:** The integrated calculation and independent oracle agree, including off-reference scenarios and preserved generic behavior. Static L2/L6 failures remain disclosed; executable evidence resolves the three new pure-EXPOSE diagnostics. No process qualification or grade is inferred from software agreement alone.
- **Decision:** Audit found applicability, late-decay cancellation and extreme-input refusal defects · repair those numerical/domain paths and verify the changed cases before release · execution detail · authors with independent reviewer acceptance · WI-069 implementation/oracle/tests and audit.
- **Decision:** Computing stock activates existing decay demand · retain the consequent required-breeding increase and unchanged costs, rather than restoring the old held-stock expectation · execution detail · coordinator and authors, independently reviewed · computed I_total consumer and affected regression.

### T-003 scope

- **Objective:** Prove one native integration candidate and execute a focused, verified inventory/startup/throughput study against that exact version.
- **Why now:** WI-069 independently audited implementation is ready; supported assumptions and off-reference behavior are verified.
- **Scope:** Local candidate commit, native integration, sensitivity framing/window scan, stock native study, immutable evidence and executor synthesis. No model changes, cost implementation, frozen-r2 replacement or physical self-sufficiency claim.
- **Inputs:** `goal.md`; audited WI-069; `evidence/study-candidates.md`; source/design/audit reviews and declared source/assumption limits.
- **Done when:** One committed native study records all cases, independent verification, uncertainty/drivers and correctly routed findings, or a native blocker is documented.
- **Stop when:** A prerequisite, strategy blocker, owner gate or declared limit is reached.

### T-003 start — 2026-09-19

T-003 · integration and native run-study · expected one verified pin and `exploration/stellarator_e2e/studies/20260919-fuel-inventory-and-startup/`. Coordinator owns commits/integration; study author may prepare records and scripts independently, but no study case executes before the integration candidate and framing release. No package or oracle changes are authorized inside this study task; route any discovered semantic fix back to a scoped native task.
