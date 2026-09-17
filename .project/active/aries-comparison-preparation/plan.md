# Comparison preparation implementation plan

**Status:** Preparation complete; owner accepted conditional scope and closed the goal on 2026-09-16. Reveal remains unauthorized. **Date:** 2026-09-16. Requirements: `spec.md`.

- [x] Capture owner requirements, grounding evidence and shared manifest/reporting interface.
- [x] Map actual producers and reconcile model-side accounting/normalization against retained numerical evidence.
- [x] Declare input-selection/applicability rules, selected mode and conditioned seams; complete AACE provenance and coolant disposition packet.
- [x] Implement deterministic reporting and meaningful synthetic/adverse tests, then integrate with the actual manifest.
- [x] Verify lineage and indicator read-set coverage; freeze model/package, procedure, assumptions and supporting artifacts reproducibly.
- [x] Obtain independent integrated review, repair findings, and issue the readiness or named-decision-blocked verdict.

## Execution choices

[AGENT] Manifest/accounting, applicability/provenance and reporting can proceed in parallel under the spec's shared interface. They own separate files. The coordinator integrates after returns and owns lineage/freeze, the goal trail and readiness. No new physical evaluation is planned; existing evidence is inspected first.

[AGENT] Selected forward mode will be current-driven magnet sizing, live helium loop/cycle and live lifecycle calendar, with current model defaults otherwise frozen and permitted independent reference inputs explicitly enumerated before reveal. This choice uses the latest represented current requirement and preserves its conditional technology, constraints and scope; it is not chosen by reference agreement. Applicability work must bind the exact package keys and state unsupported inputs.

## Implementation notes — 2026-09-16

[AGENT] Manifest has 174 rows and 14 disjoint equations. Retained 71 cases plus one selected-mode case yield 1,008 passing accounting checks; 216 passthrough equalities verify the no-credit aliases. The current package seal and all 12 actual indicator read paths pass; dependency/read-set tests pass 3+6. Current reporting and adapter/exporter suites pass 78 tests.

[AGENT] Exactly one native physical evaluation was added because no retained case matched defaults plus sizing_mode=1. It completed with 242 numeric outputs and 20 constraints; divertor, pack fit and exact-boundary conductor-current violations remain. Strict oracle comparison passes 224/226 scalars and 19/20 predicates; the two failed scalar comparisons are near-zero current margins, and all 20 native-operand predicate reconstructions agree. A postprocessing attempt initially omitted non-stellarator input groups when reconstructing predicates; corrected to read all ten input files, without rerunning native physics. The same-point oracle was invoked twice during that mechanical correction.

[AGENT] Independent native review found two defects: three passthrough quantities received independent prediction credit, and failed execution could show physical_feasibility=true from stale constraints. Both have bounded repairs and regression tests; reviewer recheck accepted (OWNER_GATE for the retained coolant decision). No model or original study changed.

[AGENT] Freeze r1 contains 785 indexed files. Two builds match SHA256 fdf6e14572f10c9254df1e297394f9eccb0060e3947283ea0f8cf569fc63f533. A separate extracted tree passes all 78 comparison tests; integrity verifies every file and rejects deliberate tampering. Final independent review reproduced the archive from the recorded base checkout, passed all 87 tests, and reproduced accounting/synthetic receipts byte-identically. OWNER_GATE remains solely for coolant comparison meaning.

[OWNER] Accepted the frozen conditional helium scenario and closed the preparation goal. Unsupported correspondence and affected downstream quantities remain unresolved or incompatible where equivalence is unestablished. See `work/orchestration/goals/aries-fixed-point-comparison-readiness/readiness.md`. This administrative decision is external to the unchanged r1 freeze; the historical independent OWNER_GATE is resolved.
