# Goal: Absolute conductor-current margin

## Status

`grounded` — 2026-09-15. [OWNER] The initiating request supplies the question, evidence, success criteria and autonomous execution authority. [AGENT] Slug selected under that authority: `absolute-conductor-current-margin`.

## Question

Can an admissible explicit tape-to-cable performance basis establish estimated conductor critical current, operating fraction and allowable-fraction margin for the modeled inventory?

## Consumer

[OWNER] The model owner needs a bounded engineering estimate with traceable assumptions, not conductor qualification.

## Answered when

[OWNER] Absolute normalization and its temperature, field, orientation, tape dimensions and applicability are traceable, with measured behavior distinguished from interpolation/extrapolation. Tape quantity, assembly capacity and turn current are consistent; series turns do not count as parallel capacity. Expose estimated critical current, operating/critical current, allowable-fraction margin and a native predicate. Test pass, exact boundary, fail and unsupported inputs. Demonstrate coherent current, actual peak field and inventory propagation while procurement and fit share the same inventory. Native model, generated package and independent oracle agree. A bounded study evaluates reference and relevant previous passes, material, orientation and degradation sensitivity. Independently review and answer, distinguishing numerical consistency, supported performance and qualification gaps.

[OWNER] If admissible evidence cannot support absolute normalization, complete an evidence assessment naming the missing basis and defensible alternative without inventing a performance claim. Report reference failure without tuning. Assess and explicitly decide whether the selected-field-envelope predicate remains independent or is redundant. Report entering predicates, current margin and combined feasibility separately.

## Invariants

- [OWNER] Preserve the nominal fit failure; do not enlarge its cavity or relax assumptions to recover feasibility.
- [OWNER] Attribute increments against the entering package; older results are historical references. [AGENT] Entering checkout is `a45925ec066c2403c72c2702e323a965e2666a3c`; capture native identity and results before implementation.
- [OWNER] Investigate whether existing density/envelope sizing already includes margin; avoid double allowance or circular passing by construction. Revise only the necessary surface if evidence conflicts.
- [OWNER] Preserve source quarantine. Prefer coherent measured data and a simple supported relation; explicit scenarios cover incomplete angular/degradation evidence. Absolute normalization cannot be inferred from desired design-point pass.
- [OWNER] No automatic conductor resize or new-machine optimization to recover feasibility.

## Grounding evidence

All references below are entering tracked evidence at `a45925ec066c2403c72c2702e323a965e2666a3c`.

- `work/orchestration/goals/winding-pack-casing-fit/answer.md` — nineteen-predicate entering screen and nominal fit failure.
- `work/orchestration/goals/tape-procurement-consistency/answer.md` — physical composite tape quantity and density interpretation.
- `work/orchestration/goals/magnet-coil-realism/answer.md` — bore inventory and prior passes.
- `work/orchestration/goals/magnet-design-transfer/transfer-claim.md` — selected-envelope limitation.
- `work/orchestration/goals/tape-procurement-consistency/evidence/tape-basis-research.md` — construction sources and inventory arithmetic.

## Limits

| Limit | This goal |
|---|---|
| Retry cap | 2 retries (3 attempts) |
| Checkpoint revision cap | 2 revisions (3 submissions) |
| Round limit | 6 rounds |
| Time or iteration limit | No additional limit; bounded evidence search and study recorded in native tasks |

[OWNER] Detailed stress/strain degradation, quench protection, full 3D angle mapping and new manufacturing-cost models remain follow-ups unless a narrow element is necessary for this estimate.

## Reserved gates

[OWNER] Do not merge or push. Source quarantine remains binding. Routine parameter, research and workflow judgments are delegated; record agent-originated assumptions. [INHERITED: GOAL_RUNBOOK.md] Formal goal closure and native item archival remain owner-held.

## Close rule

[INHERITED: GOAL_RUNBOOK.md] Recommend owner-held closure once the supported estimate or bounded evidence alternative is independently reviewed and answered; continue autonomous technical execution to that point.

## Amendments
