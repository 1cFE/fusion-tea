# Goal: Explicit primary-loop cooling-system sizing

## Status

`grounded` — 2026-09-16. [OWNER] Confirmed the proposed `primary-loop-sizing` slug and draft grounding contract in the initiating conversation.

## Question

[OWNER] What explicitly sized cooling system can meet the primary-loop heat-removal requirement with consistent flow, pressure drop, pumping power and cost, while retaining the existing coolant and independent plant constraints?

## Consumer

[OWNER] The model owner needs an explanation and price for the required cooling-system accommodation, with quantified requirements and evidence gaps where a sizing option cannot be supported.

## Answered when

- [OWNER] The existing required-flow and allowable-flow calculations are traced through coolant properties, temperature rise, loop count and equipment assumptions. Source-backed limits are distinguished from a fixed reference configuration.
- [OWNER] Supported sizing choices, such as additional parallel loops or changed flow area, are modeled with their pumping, equipment and cost consequences. These are candidate options to investigate, not requirements to implement unsupported geometry laws.
- [OWNER] The reference and the informative case requiring 245.27 kg/s per loop against 225.08 kg/s allowed are revisited. The result explains and prices the required cooling-system accommodation rather than simply raising the limit.
- [OWNER] Where evidence cannot support an option, a quantified capacity requirement and explicit evidence gap are valid results.
- [AGENT] Changed calculations have native validation, source/math review and integrated comparison evidence. The answer separates demonstrated capabilities, conditional sizing scenarios and unpriced requirements; unsupported cost estimates are not reported as established prices.

## Invariants

- [OWNER] Keep the existing coolant technology. Changing coolant technology belongs to a separate goal.
- [OWNER] Preserve the divertor limit and all magnet constraints. Report primary-loop capacity separately from combined feasibility.
- [INHERITED: entering model] Entering revision is `b9ddffb77527b982d438d41685c296e69a4a34de`. Preserve matched entering evaluations for attribution; changed cooling-system consequences may alter power and economic results.
- [AGENT] Hold unrelated physics, financial assumptions and acceptance criteria fixed in matched comparisons. Distinguish source reconstruction from plant-reference evaluation and the informative case.
- [INHERITED: CLAUDE.md] Preserve source quarantine and use native modeling, research, integration and study workflows. Unrelated worktree edits remain untouched.

## Grounding evidence

The following tracked paths are cited at `b9ddffb77527b982d438d41685c296e69a4a34de`; the statements below are entering-code observations, not fresh source validation.

- `models/library/analyses/mfe_primary_loop.sysml`: existing primary-loop calculation.
- `models/designs/stellarator_09/stellarator_plant.sysml`: helium properties, 200 K temperature rise, 8 MPa pressure, fourteen held loops, 225.07777777777778 kg/s reference flow, reference pressure loss and calibrated compressor efficiency. Primary and intermediate coolant cost bases currently use plant power scaling.
- `work/orchestration/goals/divertor-peak-heat-load/answer.md`: informative case requires 245.272965 kg/s per loop; divertor peak remains 11.156873 MW/m² against the preserved 10 MW/m² limit.
- `work/orchestration/goals/divertor-peak-heat-load/evidence/entering/native-cases.json`: retained entering case outputs.
- `work/orchestration/goals/joint-magnet-sizing-feasibility/answer.md`: joint-sizing context and separate magnet constraints.
- `work/orchestration/goals/plant-closure/goal.md`: prior loop/cycle scope and representative-circuit basis.

## Limits

[AGENT] Proposed default execution bounds:

| Limit | This goal |
|---|---|
| Retry cap | 2 retries (3 attempts) |
| Checkpoint revision cap | 2 revisions (3 submissions) |
| Round limit | 6 rounds |
| Time or iteration limit | At most one promoted pin and one committed study per round; bounded research and study scopes recorded before execution |

## Reserved gates

[INHERITED: GOAL_RUNBOOK.md] Unresolved scientific interpretations that change comparison meaning, merge, push, native item close/archive and formal goal closure remain owner-held. [AGENT] Routine engineering choices within the stated scope proceed with evidence and the required independent review. A premise conflict is surfaced before dependent work.

## Close rule

[INHERITED: GOAL_RUNBOOK.md] The owner closes the goal after the answer contract has been met and required review coverage recorded. [AGENT] Technical completion may recommend closure; a quantified evidence gap may satisfy the owner's accepted bounded-negative outcome.

## Amendments

None.
