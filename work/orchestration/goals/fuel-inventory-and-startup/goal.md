# Goal: Fuel inventory and startup

## Status

`grounded` — 2026-09-19. [OWNER] Ground and proceed under the preserved [owner prompt](evidence/owner-prompt.md); slug explicitly supplied by owner.

## Question

[OWNER-VERBATIM] “Can we calculate the tritium held throughout the fuel system, the stock needed to start operation, and the processing throughput from explicit operating and fuel-system assumptions?”

## Consumer

[OWNER] The stellarator demo owner needs R10.P2 before the ARIES comparison, and a named throughput interface for the fuel-processing cost goal.

## Answered when

[OWNER-VERBATIM] “Tritium inventory, startup requirement, and processing throughput forward-computed, verified.” [OWNER] All nine required results and deliverables in [the preserved prompt](evidence/owner-prompt.md) govern this goal: explicit streams and loss semantics, residence-based operating inventory, non-duplicated startup supply, operating versus calendar throughput, model/package integration, independent verification, focused study and fresh unchanged-rubric grade. A documented blocker does not close the gap.

## Invariants

- [OWNER] Keep ARIES sealed under `knowledge/holdout/aries-cs/PROTOCOL.md`; exclude `.project/concepts/stellarator-mbse-demo.md` and barred sources.
- [OWNER] Preserve the published r2 archive and historical results. Identify each new model version and study separately.
- [OWNER] Preserve required-breeding arithmetic unless a justified correction is separately recorded. Surface material loss/recovery reinterpretation before dependent conclusions.
- [OWNER] Do not tune recovery, losses or reserves for self-sufficiency or small startup stock. Breeding owns achieved production; this goal owns inventory/startup and throughput. Exclude processing capital costs and P3 full self-sufficiency design.
- [OWNER] Inventory is stock, throughput is flow. Operating capacity does not scale down with annual availability. Computed inventory establishes neither external supply availability nor adequate breeding.

## Grounding evidence

- [OWNER] `.project/active/demo-depth-rubric/rubric.md@dc0f0b6dc6512b29e1307da647f3a508a1f5356d`, unchanged R10.P2 target.
- [OWNER] `work/analysis/20260918-192403_stellarator-depth-reassessment.md` and companion `.cells.json` — unpinned; no native digest.
- [INHERITED] `work/orchestration/goals/plant-closure/` and `work/orchestration/goals/pre-reveal-feasible-neighborhood/@e36fe456805655fe404d49a5fd4d83f9f8c814a4` provide flow/calendar history.
- [INHERITED] `work/orchestration/goals/computed-tritium-breeding/answer.md@e36fe456805655fe404d49a5fd4d83f9f8c814a4` records subsequently computed breeding, conditional recovery and dormant inventory.
- [AGENT] Entry checkout `e36fe456805655fe404d49a5fd4d83f9f8c814a4`; pre-existing unrelated edits preserved. No throughput-cost goal directory exists at grounding.

## Limits

| Limit | This goal |
|---|---|
| Retry cap | 2 retries (3 attempts) |
| Checkpoint revision cap | 2 revisions (3 submissions) |
| Round limit | 6 rounds |
| Time or iteration limit | No additional limit |

[AGENT] Runbook default numerical limits adopted as execution detail within the owner's authorization.

## Reserved gates

[OWNER] Material scientific or scope decisions needing owner judgment; reveal, replacement of frozen comparison, major scope/plant-concept changes and formal goal closure. No merge or push. Research, implementation, generation, targeted studies and fresh independent review are authorized.

## Close rule

[OWNER] Only the owner formally closes the goal, on the reviewed answer and fresh R10.P grade.

## Amendments
