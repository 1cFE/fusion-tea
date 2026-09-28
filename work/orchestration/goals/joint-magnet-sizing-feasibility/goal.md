# Goal: Joint magnet sizing and feasibility

[AGENT] Grounded from the native template on 2026-09-15. The owner explicitly authorizes autonomous grounding, engineering decisions, implementation where necessary, studies and independent review. The descriptive slug is an execution choice under that authorization.

## Status

`grounded` — [OWNER] initiating request supplies the question, evidence, answer contract and authority to proceed without routine parameter or workflow questions.

## Question

[OWNER-VERBATIM] Can a magnet carry the required current at the selected operating margin, fit inside an explicitly allocated casing, and satisfy the existing plant constraints under one consistent set of construction and performance assumptions?

## Consumer

[OWNER] The model owner needs a bounded answer about joint conductor inventory, geometry, plant feasibility and cost. A supported finding of no feasible sampled design is successful.

## Answered when

- [OWNER] One physical conductor inventory consistently drives current capacity, pack geometry and procurement; independent choices, derived quantities and held assumptions are identified.
- [OWNER] Report required tape quantity and pack/cavity dimensions at reference and relevant off-design points; explicitly resolve geometry/field/sizing feedback with tolerances, residuals and retained failures.
- [OWNER] Evaluate every existing predicate and report current margin, fit and combined plant feasibility separately. Establish whether any sampled default-performance design passes.
- [OWNER] State precisely which assumptions enable enhanced-performance passes. If no default case passes, quantify limiting requirements and required changes within the investigated model.
- [OWNER] Report cost consequences and a cheapest sampled feasible choice only if one exists. Preserve manufacturing omissions and uncertain price bases.
- [OWNER] Native model, generated package and independent oracle agree on new or changed calculations. Finish implementation if needed, a bounded study, independent review and a written answer distinguishing internal sizing consistency, conditional feasibility and engineering qualification.

## Invariants

- [AGENT] Entering package and all historical evidence are identified at c4d720db886213de94bf2dc4c3131a3453dca690. Attribute changes against this entering state; prior studies retain their historical findings.
- [OWNER] Calculate tape capacity at actual field and selected allowable operating fraction. Reference current density is an inventory coordinate only, never a free performance improvement.
- [OWNER] Distinguish coil ampere-turns, turn current and parallel tape capacity; include consequences of any turn/current variation.
- [OWNER] Required cavity is a design requirement, compared with independently declared allocation; exact current sizing closure is conditional consistency, not qualification.
- [OWNER] Preserve all acceptance limits, including operating fraction, field limits and fit clearances. Never tune normalization or orientation to recover reference feasibility.
- [OWNER] Keep default material/orientation assumptions separate from enhanced scenarios; unmet evidence remains a threshold, not achieved capability.
- [OWNER] Reuse existing evidence; research only missing facts material to calculation or interpretation. Preserve source quarantine. Do not merge or push.
- [OWNER] Detailed structural certification, full 3D interference, quench protection, complete field-angle mapping and new factory-cost models remain outside scope unless a narrow essential dependency is identified. Missing physical dependencies are disclosed.
- [OWNER] Use bounded stages: reproduce reference/prior cases; solve or bracket tape/pack requirements; explore geometry/plant tradeoffs over justified bounds; evaluate a few separate performance/construction sensitivities. Finite samples imply neither global infeasibility nor global optimum.

## Grounding evidence

All entries identify the entering revision c4d720db886213de94bf2dc4c3131a3453dca690.

- [INHERITED] `work/orchestration/goals/magnet-manufacturing-cost-completeness/answer.md@c4d720db886213de94bf2dc4c3131a3453dca690`.
- [INHERITED] `work/orchestration/goals/absolute-conductor-current-margin/answer.md@c4d720db886213de94bf2dc4c3131a3453dca690`.
- [INHERITED] `work/orchestration/goals/winding-pack-casing-fit/answer.md@c4d720db886213de94bf2dc4c3131a3453dca690`.
- [INHERITED] `work/orchestration/goals/tape-procurement-consistency/answer.md@c4d720db886213de94bf2dc4c3131a3453dca690`.
- [INHERITED] `work/orchestration/goals/magnet-coil-realism/answer.md@c4d720db886213de94bf2dc4c3131a3453dca690`.

## Limits

[AGENT] Native defaults and bounded study design apply.

| Limit | This goal |
|---|---|
| Retry cap | 2 retries (3 attempts) |
| Checkpoint revision cap | 2 revisions (3 submissions) |
| Round limit | 6 rounds |
| Time or iteration limit | No wall-clock limit; numerical bounds and iteration caps declared before execution |

[INHERITED: runbook] At most one promoted pin and one committed study per round.

## Reserved gates

- [OWNER] Source quarantine, scope limits and acceptance criteria remain binding; merge and push prohibited.
- [AGENT] Routine parameter, engineering, research and workflow choices are delegated by the initiating request. A conflict with the question or an invalidating missing dependency is surfaced with dependent conclusions parked.
- [INHERITED: runbook] Formal goal closure and native item archival remain owner-held. Independent review is required for new/reinterpreted math and coupled integration.

## Close rule

[INHERITED: runbook] Recommend owner-held closure once the answer contract and independent review are complete, including a supported adverse or conditional answer. Autonomous technical execution does not require manufacturing qualification to force a pass.

## Amendments

None.
