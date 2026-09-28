# Goal: Bounded feasibility and design-point transfer

## Status

`grounded` — 2026-09-16. [OWNER] Requested grounding and pursuit, supplied evidence and answer contract, and delegated slug choice. [AGENT] Slug: `bounded-feasibility-transfer`.

## Question

[OWNER] What bounded feasible region, if any, can the current model establish under defensible fixed assumptions, and which stellarator design-point changes can it represent consistently before the sealed ARIES comparison?

## Consumer

[OWNER] The project owner preparing a blind fixed-design-point comparison, who needs feasibility, transfer support and comparison readiness reported distinctly.

## Answered when

- [OWNER] A bounded search identifies combined passes and a sampled local neighborhood if found, or the closest informative rejections and simultaneous deficits without claiming global infeasibility.
- [OWNER] A model-side transfer contract identifies independent inputs, predictions, held anchors, boundaries, applicability, unsupported substitutions and missing dependencies, with reference/smaller/larger holdout-blind checks.
- [OWNER] A concise readiness assessment names only remaining work necessary before a blind fixed-point comparison. A constraint-violating prediction remains visible; feasibility establishes neither accuracy nor technology transfer.
- [OWNER] Evidence reuse, selected variables, justified bounds, expected responses, budget and stopping rules precede expensive execution; all predicates and failed cases are retained. Combined passes receive native/oracle verification and neighborhood checks.

## Invariants

- [OWNER] Preserve the sealed quarantine; do not reveal or use ARIES-specific design/cost information. The acceptance specification and protocol retain authority.
- [OWNER] Material-performance assumptions, calibration constants and acceptance limits stay fixed in the main search. No arbitrary orientation, radiation, divertor-area, field-ceiling or operating-allowance knob. Any admitted alternative transport scenario is separate.
- [OWNER] Current-sized inventory is purchased material; casing accommodation is declared independently. Additional cooling equipment is not economically free. Conditional modeled costs and break-even requirements stay separate from economic-optimum claims.
- [OWNER] Preserve prior current/fit/divertor/loop findings and their limits. No prior study establishes global infeasibility.
- [AGENT] Package: use the current unchanged WI-065 package and native identity gates; no model change is initially intended. Any later change requires its native workflow and separate lineage.
- [INHERITED: ratified acceptance specification] B-2/B-3/B-4 axes and explicit ratio bands remain unchanged; supplied inputs cannot count as independent predictions. C220107 remains excluded or footnoted.

## Grounding evidence

Tracked paths below are cited at `a3ea15e88ee6c48de44d5880751636e7c9615776` (entering HEAD).

- `work/orchestration/goals/primary-loop-sizing/answer.md` — sixteen-loop accommodation and installed-price/qualification gap.
- `work/orchestration/goals/divertor-peak-heat-load/answer.md` — default peak, conditional area diagnostic and power-account validity.
- `work/orchestration/goals/joint-magnet-sizing-feasibility/answer.md` — current-sizing, fit feedback and retained rejections.
- `work/orchestration/goals/absolute-conductor-current-margin/answer.md`, `work/orchestration/goals/winding-pack-casing-fit/answer.md`, `work/orchestration/goals/tape-procurement-consistency/answer.md`, `work/orchestration/goals/magnet-manufacturing-cost-completeness/answer.md` — conductor construction, performance and accounting limits.
- `.project/completed/20260821_demo-anchor-acceptance-spec/spec.md`, `knowledge/holdout/aries-cs/PROTOCOL.md` — comparison and quarantine authority.
- `.project/active/aries-comparison-preparation/draft.md` — unpinned; no native digest. [OWNER] Reuse relevant principles but reassess stale inventory and proposed work.

## Limits

| Limit | This goal |
|---|---|
| Retry cap | 2 retries (3 attempts) |
| Checkpoint revision cap | 2 revisions (3 submissions) |
| Round limit | 6 rounds |
| Initial evaluation budget | [AGENT] At most 500 independent-oracle evaluations and 80 native unique cases, including baseline, controls and local refinement; allocation by stage recorded before execution. |
| Stopping rule | [AGENT] Stop refinement on exhausted budget, unsupported dependency, or adequately sampled local pass/rejection tradeoff; never enlarge bounds or change fixed assumptions silently. |

## Reserved gates

[OWNER / INHERITED: runbook] Reveal, quarantine exceptions, changed acceptance meaning, unresolved scientific premise conflicts, merge/push, archive/item closure and formal goal closure remain owner-held. [AGENT] Native study custody commits are authorized by the invoked run-study workflow. No current request authorizes reveal.

## Close rule

[INHERITED: runbook] Owner closes after reviewing the bounded result, transfer contract and readiness assessment with required independent coverage. An evidence-supported negative result is acceptable.

## Amendments
