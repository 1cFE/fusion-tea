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

### T-003 integration and framing release — 2026-09-19

- **Evidence:** Native `evidence/integration/integration_return.json` returns CANDIDATE with all ten gates passing for audited commit `956444b5d440238857911a0406e6d3f51ddcbf2e`, pin `9aaca3257606b22dd48d92b0074ee4076836e5b0fefd9b593369aa0915c4f1c2`. The manifest gate explicitly does not run read-set coverage. Baseline and all six study preflight gates pass; the independent oracle scan supports all 26 declared cases.
- **Decision:** All 15 public axes have conservative graph paths to constraints, but graph reachability is not process qualification · retain all 26 finite assumption cases as sensitivities, including the grouped missing process-equipment/reliability/supply coupling finding · execution detail under owner authorization · coordinator, after reviewing `reviews/proposed-framing.md` and every candidate · study `reviews/coordinator-framing.md` and `preparation/execution-release.json`.
- **Release:** One complete declared window, no optimization. Startup extension and shutdown duration are observation durations; ideal recovery, zero decay and online extraction are limiting diagnostics. Native execution follows the successful scan. Any unexpected refusal or premise conflict returns before repair.

### T-003 mechanical verification retries — 2026-09-19

- **Retry 1:** The reporting caller expected 914 scalar entries but the store also publishes 14 Boolean flags. Assert the exact declared numeric set and retain Boolean outputs. The original refusal is in the study's `results/verify-phase-before-count-fix.log`.
- **Retry 2:** Stringified point keys distinguished declared integer times from runtime-normalized floats. Normalize numeric keys without rounding or changing point values. The original refusal is in `results/verify-phase-before-point-key-fix.log`.
- **Classification:** Both repairs change only study verification/export joins. The same 26 cases, native store, model, package, window and objective remain fixed; native execution was not repeated. These are the two permitted mechanical retries. Final classification confirms 892 numeric outputs plus 14 Boolean flags in the 906-channel oracle map, with 22 inherited numeric outputs unmapped and every new inventory output mapped.

### T-003 return — 2026-09-19

- **Outcome:** COMPLETE.
- **Evidence:** Study `exploration/stellarator_e2e/studies/20260919-fuel-inventory-and-startup/` frozen in local commit `3529f6c8`; `record.md`, `report.md`, `synthesis.md`, retained SQLite store and `snapshot.json` SHA256 `bcaf7f5723775c2e030be9635b0c3096bab43189b97ac5b3f94dd0cd6cae821a`. Integration evidence is in the same commit. Root `evidence/study-record-tests.log`: 3 passed; executor custody: 478 artifact hashes, 26 points and all 17 record sections resolve.
- **Reading:** All 26 native cases completed, with 23,556 mapped scalar comparisons and 650 independently re-derived predicate comparisons passing. No case passes every whole-plant screen. Source/policy scenarios provide useful conditional stock and startup estimates; no qualified complete-plant inventory or self-sufficiency is inferred.
- **Decision:** Retain all four study findings and proposed dispositions in record §15 · source/process coupling limits, distinct initial and recurring supply, running/calendar capacity, and preserved plant failures · proposed learning delta for final fresh review · coordinator · goal learnings after review, with existing costing interface retained.

### Round 1 result — 2026-09-19

- **Intent:** Met for the declared strategy: represented inventory, bounded startup requirement and processing throughput are forward-computed and independently verified. Final R10.P grade remains pending fresh review; formal goal closure remains owner-held.
- **Task sequence:** T-001 established and independently reviewed source/accounting evidence; T-002 implemented and audited WI-069; T-003 integrated one candidate and froze one verified study.
- **Last semantic outcome:** Valid committed study reading, including source uncertainty and adverse whole-plant screens.
- **Stop reason:** A valid study reading closes this round under the runbook. No second pin, study or follow-up semantic implementation is opened.
- **Answer evidence:** `answer.md` is the coordinator's draft synthesis; authoritative model candidate `956444b5`, study/integration `3529f6c8`, original-source/design review, implementation audit and native verification receipts cited above.
- **Proposed learning delta:** (1) Explicit residence scenarios permit useful conditional represented-boundary estimates, but do not qualify actual PbLi residence, retention, supply or reserve reliability. (2) Reference working/reserve/total stocks are 2.380/2.038/4.418 kg T; conservative startup is 4.400 kg, without double-counting internally filled stages. (3) Reference running capacity is 7.743 kg T/day or 12.912 kg D+T/day; calendar downtime changes annual flow while maintained inventory decays throughout the year. (4) The selected cases span 1.091–10.531 kg held and 1.087–10.515 kg startup, not statistical bounds; ongoing deficit and failed whole-plant predicates remain visible.
- **Finding dispositions:** Study findings `#1`–`#4` are proposed for acceptance as conditional scope, accounting and interpretation learnings. Their durable destination is `learnings.md` after review. They require no dependent implementation within this P2 goal. Costing receives `evidence/throughput-interface.md`; physical process qualification and P3 remain outside the authorized increment.
- **Carried uncertainty:** Source transfer to helium/PbLi; unrepresented retention/permeation/bypass/detritiation; abstract decay-replenishment access; no external tritium procurement proof or complete process pricing. Static L2/L6 diagnostics and the native manifest read-set coverage limitation remain disclosed.

### Round 1 review — 2026-09-19

- **Reviewer and verdict:** Fresh non-author `fuel_final_grade`, PASS; unchanged rubric R10.P = 2. Evidence: `evidence/final-review-and-grade.md`. The reviewer independently checks the final administrative joins after accepting the scientific result and all four learning dispositions.
- **Checks:** Source/accounting and implementation review reuse is valid for the unchanged candidate. Independent checks cover original equations/bindings, retained source boundaries, all 26 startup trajectories, 1,820 new-output CSV/native joins, 23,556 mapped scalar comparisons, 650 predicates, snapshot/audit hashes and unchanged model/package/study revisions. Native goal scopes, two mechanical study retries and one-pin/one-study bounds remain respected.
- **Corrections:** The draft answer's stale required-breeding value is corrected to 1.191670 from the retained native reference. The current audit's stale unmapped count is corrected to 22 numeric outputs, with 892 numeric plus 14 Boolean mapped scalars. These are administrative evidence corrections; frozen study copies and all executable results remain unchanged.
- **Learning disposition:** Accept all four Round 1 proposed learnings into `learnings.md`. Append joined `declared seam` dispositions under the committed study's four finding IDs in `exploration/stellarator_e2e/studies/DISCOVERY_LOG.md`. No finding remains unrouted; no semantic follow-up is required for the stated P2 target.
- **Remaining uncertainty:** The conditional physical boundary, source transfers, initial-state/decay-access assumptions, missing procurement evidence, static diagnostics and manifest read-set coverage limitation remain explicit. No P3 or complete-cost claim is accepted.
- **Recommendation:** The reviewed answer supports owner-held goal closure on R10.P2. The goal remains grounded pending that decision. Reveal, frozen comparison replacement, merge and push are not performed.

## Goal closure — 2026-09-19

[OWNER-VERBATIM] “great, please close the goal”. The owner authorizes formal closure following the delivered answer and independent R10.P2 PASS. [AGENT] Coordinator marks the goal closed on the completed Round 1 result and review, model candidate `956444b5`, committed study `3529f6c8` and final answer/review checkpoint `6836eb44`. The target is met; the recorded physical-boundary, source-transfer, supply and process-design limitations remain. Goal status, answer and current-work summary are updated. Existing independent review is reused because closure changes no scientific claim or executable evidence. Frozen study evidence remains unchanged; item archival and other reserved gates are separate.
