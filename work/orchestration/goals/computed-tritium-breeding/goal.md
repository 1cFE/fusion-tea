# Goal: computed tritium breeding

## Status

`grounded` — 2026-09-18. [OWNER] The initiating prompt specifies the slug and authorizes grounding and research, implementation, generation, targeted studies and independent review. Formal closure remains owner-held.

## Question

[OWNER-VERBATIM] “Can we calculate tritium production from the modeled blanket configuration, verify that calculation, and make insufficient breeding constrain the design?”

## Consumer

[OWNER] The project owner needs the existing R2c.P3 modeling target met before the ARIES comparison. The answer must explain actual calculated quantities, influential choices, checks, grade, adequacy and uncertainty to an engineer unfamiliar with this project.

## Answered when

- [OWNER] Achieved tritium breeding ratio (TBR, tritium atoms produced per tritium atom burned) follows explicit blanket/build choices through a defensible physical model in SysML and the generated executable. A reduced model requires justified sources, validation, applicability and uncertainty; scaling one published TBR by invented geometry is insufficient.
- [OWNER] Calculated production is compared with an explicitly justified requirement affecting design feasibility. Resolve or surface the 1.05 floor versus approximately 1.190 fuel-cycle requirement, keeping production, recovery, losses and reserves distinct.
- [OWNER] Verify software separately from predictive physics using independent source results or benchmark calculations. A focused study preserves failed cases and reports affected plant quantities, uncertainty and extrapolation.
- [OWNER] A fresh independent assessment against the unchanged rubric demonstrates P2 “TBR computed from blanket configuration” and P3 “computed TBR vs floor pushes back on blanket/build choices.” An inadequate blanket may still satisfy this modeling target.
- [OWNER] If evidence or tools cannot support P3, report the exact missing inputs, tested or rejected methods and concrete next step. This is a useful blocker, not closure of the gap.

## Invariants

- [OWNER] ARIES remains sealed under `knowledge/holdout/aries-cs/PROTOCOL.md`. Do not read `.project/concepts/stellarator-mbse-demo.md` or barred derivatives.
- [OWNER] Preserve the published r2 archive and historical results. Identify new model versions and studies separately. Preserve unrelated work; no merge or push.
- [OWNER] Keep rubric targets, physical limits and acceptance requirements unchanged. Do not tune to restore passing designs or silently change blanket technology or plant concept.
- [OWNER] Include only dependencies necessary for achieved breeding and its adequacy check; broader inventory, processing-cost and other rubric gaps remain outside scope.
- [OWNER] Investigate the earlier deferral rather than treating it as proof of impossibility. Research admissible existing sources first and review the proposed physical method before substantial implementation.

## Grounding evidence

- `.project/active/demo-depth-rubric/rubric.md@dc0f0b6dc6512b29e1307da647f3a508a1f5356d` — unchanged target.
- `work/analysis/20260918-192403_stellarator-depth-reassessment.md` and sibling `.cells.json` — unpinned; no native digest; owner-specified current assessment.
- `work/orchestration/goals/plant-closure/goal.md@e78099cb93ab36b57debf70045cc9c4e7bcfcdd8` — earlier computed-breeding deferral and fuel semantics conflict.
- `work/orchestration/goals/pre-reveal-feasible-neighborhood/answer.md@e78099cb93ab36b57debf70045cc9c4e7bcfcdd8` — conditional passing neighborhood under existing screens.
- [OWNER] Starting evidence: achieved TBR is held at 1.074, checked against 1.05; separate fuel-cycle assumptions imply approximately 1.190. Passing the old check does not demonstrate self-sufficiency.

## Limits

[INHERITED: GOAL_RUNBOOK.md] Explicit default bounds apply.

| Limit | This goal |
|---|---|
| Retry cap | 2 retries (3 attempts) |
| Checkpoint revision cap | 2 revisions (3 submissions) |
| Round limit | 6 rounds |
| Pins and studies | At most one promoted pin and one committed study per round |
| Time or iteration limit | No additional limit; research requests carry explicit search/capture bounds |

## Reserved gates

[OWNER] Material scientific or scope decisions, reveal, replacement of the frozen comparison, major scope changes and formal goal closure remain the owner's. Research and technical execution already have authorization. Unresolved semantics that change scientific meaning must be surfaced before dependent implementation.

## Close rule

[OWNER] Only the owner formally closes this goal after considering the technical answer and independent evidence. A documented blocker does not close the breeding gap.

## Amendments
