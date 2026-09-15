# Goal: Winding-pack/casing fit

## Status

`grounded` — 2026-09-15. [OWNER] The initiating request authorizes grounding and autonomous pursuit through implementation, study, independent review and answer. [AGENT] Slug and routine workflow choices use that explicit delegation.

## Question

Can an explicitly defined, independently based casing interior accommodate the calculated winding-pack envelope, insulation and assembly clearances, and how does adding that geometric screen change sampled feasibility and the cheapest feasible choice?

## Consumer

[OWNER] The model owner needs enlarged winding packs to face a meaningful available-space test before a model pass is interpreted as geometrically feasible.

## Answered when

- [OWNER] Required and available dimensions have explicit definitions, units and provenance; bare pack, insulated pack, casing interior and exterior are distinguished.
- [OWNER] Insulation and clearance count exactly once. Interpretable margins and a native predicate propagate reference density, current and selected envelope through pack sizing.
- [OWNER] Positive margin, exact boundary, oversized rejection and invalid geometry are tested. Native model, generated package and independent oracle agree.
- [OWNER] A bounded native study covers reference and relevant enlarged packs, including earlier passes where useful. The answer reports losses of feasibility and effect on the sampled cheapest feasible choice against the entering package.
- [OWNER] Any reference failure is explained without tuning to force a pass; procurement, thermal accounting and total-support pricing remain coherent.
- [OWNER] Evidence and assumptions receive independent review. Where device-specific geometry is unavailable, the answer delivers a conditional screen and identifies qualifying measurements.

## Invariants

- [OWNER] Preserve existing predicates and report their feasibility separately from feasibility including fit. Attribute increments against the entering package; older studies are historical references.
- [OWNER] Available space has a basis independent of calculated pack size. Do not infer cavity dimensions from aggregate support mass or thermal surface allowance without justification.
- [OWNER] Use the simplest defensible evidence-supported geometry. Square equivalence alone establishes neither real nonplanar-coil shape nor orientation.
- [OWNER] Keep absolute conductor-current margin, detailed stress, full three-dimensional interference and manufacturing-effort estimates as separate follow-ups. This screen is geometric, not structural certification.
- [OWNER] Preserve source quarantine. Do not merge or push.
- [AGENT] Freeze one candidate per round; hold unchanged physical/economic inputs in matched entering comparisons. Scenario dimensions are engineering assumptions unless admissible source evidence qualifies them.

## Grounding evidence

All paths below are entering revision `55f7f82d35da3ec374a1cdc815c0c0aef3a1d3aa`.

- `work/orchestration/goals/tape-procurement-consistency/answer.md@55f7f82d35da3ec374a1cdc815c0c0aef3a1d3aa` establishes physical tape procurement and three eighteen-predicate passes with unknown fit.
- `work/orchestration/goals/magnet-coil-realism/answer.md@55f7f82d35da3ec374a1cdc815c0c0aef3a1d3aa` establishes thermal inventory and aggregate support pricing.
- `work/orchestration/goals/magnet-design-transfer/transfer-claim.md@55f7f82d35da3ec374a1cdc815c0c0aef3a1d3aa` limits geometric transfer.
- `work/completed/20260914_WI-038_conductor-grade-lever/design.md@55f7f82d35da3ec374a1cdc815c0c0aef3a1d3aa` and its `audit.md`; `work/completed/20260914_WI-040_winding-pack-mass-cost/design.md@55f7f82d35da3ec374a1cdc815c0c0aef3a1d3aa` and its `audit.md`; `work/active/WI-059_coil-thermal-and-total-support-inventory/design.md@55f7f82d35da3ec374a1cdc815c0c0aef3a1d3aa` and the independent reviews cited by the coil-realism answer anchor the affected model chain.

## Limits

| Limit | This goal |
|---|---|
| Retry cap | 2 retries (3 attempts) |
| Checkpoint revision cap | 2 revisions (3 submissions) |
| Round limit | 6 rounds |
| Study limit | At most 150 unique native cases per round; refine only on concrete uncovered evidence |

[AGENT] Limits size the bounded execution; they are not owner-originated numerical requirements.

## Reserved gates

[OWNER] Merge and push are prohibited; source reveal is not authorized. [INHERITED: GOAL_RUNBOOK.md] Native item archive and formal goal close remain owner-held. [OWNER] Routine parameters and workflow choices, missing-evidence research, and explicitly conditional engineering assumptions are delegated; do not stop for these choices.

## Close rule

[INHERITED: GOAL_RUNBOOK.md] Recommend owner-held administrative close after the answered-when contract is implemented, studied, independently reviewed and answered. Technical delivery proceeds autonomously under the initiating request.

## Amendments
