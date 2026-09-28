# Goal: Installed cooling equipment costs

## Status

`closed` — 2026-09-18, by explicit owner authorization recorded below. Closed on the independently reviewed R7.S3 result and its stated engineering and cost limitations.

[AGENT] Technical answer completed on 2026-09-18: independent R7.S=3, PASS; see `answer.md`, frozen study `5b956a82`, and `evidence/round3/final-review-and-grade.md`. The owner has formally closed the goal.

## Question

[OWNER-VERBATIM] “Can we size and separately cost the cooling system’s pumps, piping and heat exchangers from the plant’s calculated heat-removal requirements, including installation and appropriate lifecycle costs?”

## Consumer

[OWNER] The project owner needs the existing R7.S3 target met before the ARIES comparison, with a plain engineering account of quantities, costs, boundaries and uncertainty.

## Answered when

[OWNER] A fresh independent assessment applies unchanged R7.S3 at `.project/active/demo-depth-rubric/rubric.md@dc0f0b6dc6512b29e1307da647f3a508a1f5356d`: “Pumps, piping, heat exchangers as separately sized subaccounts.” Source-supported procurement, fabrication, installation and appropriate lifecycle treatment must feed the executable Cost Account Structure and electricity cost. Physical sizing, source applicability, account ownership and generated execution must be verified. A focused native study must retain reference, selected design, matched demand/circuit comparisons, sensitivities and failures. A documented source/tool blocker is useful but does not satisfy this answer contract.

## Invariants

- [OWNER] Keep ARIES sealed; follow `knowledge/holdout/aries-cs/PROTOCOL.md`. Exclude `.project/concepts/stellarator-mbse-demo.md` and all barred derivatives.
- [OWNER] Preserve the published r2 archive and historical results. Identify new packages and studies separately. Keep helium cooling, rubric targets, physical limits and acceptance requirements unchanged.
- [OWNER] Separate equipment requirements from qualified equipment; calculated quantities from layout assumptions; purchased prices from installed scope; missing costs from design changes. Assign each cost once. Do not infer an optimum from added circuits or lower LCOE.
- [OWNER] Scope is cooling equipment and necessary interfaces, not turbine redesign, facilities-gap closure or complete plant-layout qualification. Preserve unrelated work. No merge or push.
- [OWNER] Use native research, modeling, integration and study workflows with `.codex-test/run`. Obtain a fresh source/sizing/accounting/verification-plan review before substantial implementation and a fresh final R7.S assessment.

## Grounding evidence

- [OWNER] `.project/active/demo-depth-rubric/rubric.md@dc0f0b6dc6512b29e1307da647f3a508a1f5356d` is the target authority.
- [OWNER] `work/analysis/20260918-192403_stellarator-depth-reassessment.md` and companion `.cells.json` — unpinned; no native digest. Starting assessment reports P3/S2 and existing consumer-check failures.
- [OWNER] `work/orchestration/goals/primary-loop-sizing/` and `exploration/stellarator_e2e/studies/20260916-primary-loop-sizing/` at entering checkout `58e292c38a715ce34f0bc3df8af8ab81948f19af` retain calculated cooling requirements and the unresolved installed-price gap.
- [OWNER] `work/orchestration/goals/pre-reveal-feasible-neighborhood/` and `exploration/stellarator_e2e/studies/20260917-pre-reveal-feasible-neighborhood/` at entering checkout `58e292c38a715ce34f0bc3df8af8ab81948f19af` retain the latest selected design and fourteen-circuit control. Confirm numerical claims from records before use.

## Limits

[AGENT] Runbook defaults adopted as execution limits, not owner-originated scientific constraints.

| Limit | This goal |
|---|---|
| Retry cap | 2 retries (3 attempts) |
| Checkpoint revision cap | 2 revisions (3 submissions) |
| Round limit | 6 rounds |
| Time or iteration limit | None beyond declared bounded tasks |

## Reserved gates

[OWNER] Material scientific or scope decisions, coolant technology changes, reveal, replacement of the frozen comparison, major scope changes and formal goal closure remain owner-held. Native item close/archive remain owner-held under the runbook. Research, implementation, generation, targeted studies and independent review are authorized.

## Close rule

[OWNER] Only the owner formally closes the goal. Recommend closure only with evidence satisfying the answer contract; report an unresolved blocker as a gap, never completion.

## Amendments

### Amendment 2026-09-18 — amends execution interpretation of Reserved gates

[OWNER-VERBATIM] “next time, do not pause between rounds”. Continue automatically across rounds while authorized useful work remains; an ordinary round boundary does not require owner confirmation. Reserved scientific/scope decisions and formal closure remain owner-held.

### Amendment 2026-09-18 — intermediate coolant decision

[OWNER-VERBATIM] “yes. proceed”, replying to the explicit request to adopt HITEC molten salt at270–465°C in the intermediate loop while retaining primary helium. [AGENT] The proposed HITEC scenario is ratified by the owner; its detailed geometry, pressure, price and lifecycle assumptions still require engineering review. This resolves the Round2 material gate and does not authorize reveal, frozen-comparison replacement or formal goal closure.

### Amendment 2026-09-18 — owner closure

[OWNER-VERBATIM] “ok close the goal”. [OWNER] Formally close installed-cooling-equipment-costs on the reviewed R7.S3 answer. The accepted limitations remain part of that answer. See the owner closure entry in `trail.md`; final evidence commit `a89809de`, frozen study `5b956a82`.
