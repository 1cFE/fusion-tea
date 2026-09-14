# Goal: magnet-design-transfer

## Status

`grounded` — 2026-09-13. [OWNER-VERBATIM] “approved, please begin” approves the proposed slug and grounding contract. Agent-originated provisions remain [AGENT], ratified by owner 2026-09-13.

## Question

> Within a documented geometry and conductor-technology range, do magnet sizing, operating limits, and component costs respond consistently enough to support a defensible design-point transfer?

[OWNER-VERBATIM] Current request. Execution order: “WI-040 first, then WI-038”.

## Consumer

[AGENT] The model owner needs to know which magnet conclusions can be transferred away from the reference design point, over what range, and with what evidence and limitations.

## Answered when

[AGENT] A reviewed evidence packet answers the question affirmatively over a stated range, negatively with a demonstrated inconsistency, or inconclusively with the missing evidence identified. It includes the following:

- A documented geometry and conductor-technology range. Each boundary is identified as source-supported, an engineering assumption, or an exploration boundary; a sweep boundary alone does not establish engineering validity.
- Audited WI-040 winding-pack material costs, followed by audited WI-038 conductor-grade consequences, or a native blocker explaining why either item cannot be completed within its scope.
- A committed study on an integrated package that measures the reference point and transfers within the documented range. It follows geometry/current/conductor changes through pack sizing, peak field, stress/strain and applicable conductor limits, material quantities and component costs. The study reports invalid or unevaluable cases and explains unexpected trends.
- Reference-point reconciliation and checks of component cost accounting that identify omitted or overlapping material costs. Numerical tolerances and expected relationships are declared before execution and justified in native artifacts.
- A concise transfer claim stating what the evidence supports, where it stops, and which inherited geometry or conductor assumptions remain unverified. A fresh reviewer checks the claim against the evidence.

## Invariants

- [OWNER] WI-040 precedes WI-038.
- [AGENT] Each round uses at most one promoted package pin and one committed study. Comparisons identify the actual current executable and semantic identity; historical study values remain evidence for their own pins.
- [AGENT] Component costs use declared units, price basis and accounting boundaries. Changes to sizing, limits or prices are traced to their sources or explicitly identified assumptions. Values are not tuned to obtain a preferred design point.
- [AGENT] Transfer consistency means the applicable relationships and accounting remain coherent at the stated points. Numerical consistency alone does not establish conductor qualification or coil-configuration feasibility.
- [INHERITED: CLAUDE.md] Source quarantine, native modeling ownership, and source-image verification apply. Existing committed study records remain intact; new evidence is recorded through the study workflow.

## Grounding evidence

- [INHERITED] `work/backlog/epic-mfe-cost-modeling.md@0b5de53407443f386b2efd2a120fa4837a928690`, WI-040 and WI-038 entries: winding-pack material cost omission, conductor-grade follow-up, and established sequence. The WI-041 entry records completion of the earlier wall-load prerequisite.
- [INHERITED] `work/completed/20260903_WI-036_winding-pack-sizing/design.md@f937be2c04b43d3ebf00317ec300f4e35aaea93c`: existing winding-pack sizing and cost-account seam.
- [INHERITED] `work/orchestration/goals/minor-radius/goal.md@0b5de53407443f386b2efd2a120fa4837a928690`: inherited geometry-response forms and the unresolved sourced geometry-bound premise. Its historical package and verdict counts do not describe the current package.
- [INHERITED] `work/analysis/20260913-171817_fusion-audit-current-assessment.md@28b64ad97466e124e97c12d70d08f6d0512663d6`, F14: conductor operating margins, a sourced geometry interval, pack/casing fit and the casing basis remain open. This is evidence of limitations, not authorization to implement every listed capability.

## Limits

| Limit | This goal |
|---|---|
| Retry cap | [AGENT] 2 retries (3 attempts) |
| Checkpoint revision cap | [AGENT] 2 revisions (3 submissions) |
| Round limit | [AGENT] 6 rounds |
| Time or iteration limit | [AGENT] No additional time limit; study size is bounded in its native protocol before execution. |

[AGENT] Initial implementation scope is WI-040 then WI-038. Research and validation needed to establish their basis are included. If a defensible transfer requires a separate geometry/configuration model or another capability beyond these items, surface the missing evidence and obtain an owner scope ruling before implementing it.

## Reserved gates

- [AGENT] Owner confirms this slug and grounding contract before a round starts.
- [AGENT] Owner holds expansion beyond the two named work items, acceptance of unsupported engineering premises, and changes to the question or answer standard.
- [INHERITED: work/orchestration/GOAL_RUNBOOK.md] Merge, push, item close, archive and goal close remain owner-held unless separately authorized. Routine native work, integration and required fresh reviews proceed within the grounded scope.

## Close rule

[INHERITED: work/orchestration/GOAL_RUNBOOK.md] The owner closes the goal after a written round result and fresh review establish the answer or present the bounded negative/inconclusive outcome and remaining decisions.

## Amendments

None.

