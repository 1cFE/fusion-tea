# Brief — spec_review stage — GSTH Item 4 (goal-cold-pickup-proof)

Review `.project/active/goal-cold-pickup-proof/spec.md` — the spec for GSTH epic Item 4
(`.project/backlog/epic_goal_strategy_task_harness.md` § Item 4). You are a fresh reviewer;
the authoring session is not yours.

## Context

Item 4 is a **proof item**: kept evidence that Item 1's lean goal contract
(`work/orchestration/GOAL_RUNBOOK.md`, `work/orchestration/goal-templates/`, `.project/adr/`)
works cold — cold grounding + ungrounded-draft refusal, interrupted-task resume from disk,
bounded no-pin/no-study closure with a fresh RoundReview catching one seeded drift. Out of
scope: solving the chosen finding, using Item 2/3's native seams, hardening machinery.
Align decisions (owner-settled, do not reopen): question delegated → orchestrator picked
discovery row `20260823-magnet-technology-ab#2`; orchestrator plays operator and owes
operator-notes; same branch; reserved gates as in `align.md`.

## What to check hardest

1. **Epic fidelity**: every epic § Item 4 success criterion and scope bullet is carried,
   none silently narrowed or widened. The epic's "treating a clean-boundary handoff as proof
   of interruption recovery" exclusion must have teeth in the criteria.
2. **Provenance**: owner-grade vs agent-grade markings survive per
   `claude-pack/rules/capture-fidelity.md`; the spec must not present the orchestrator's
   question pick or operationalizations as owner intent.
3. **The § "A predicted prose failure" move**: the spec claims the epic's grounding gate
   spans five field classes while `GOAL_RUNBOOK.md:72` defends one, and turns that into a
   measured outcome under the owner's hardening rule instead of narrowing the criterion.
   Verify the premise against Item 1's actual artifacts and judge whether the spec's handling
   is right — it should not quietly assign Item 1 repair work to this item, nor assume the
   gate works.
4. **Testability**: each success criterion must be checkable on disk by an auditor who did
   not run the proof. Freshness of cold sessions must be auditable from kept inputs.
5. **Scope discipline**: deferred-to-design list is design work, not unstated requirements.

Produce your findings with severities; must-fix findings will be fed back to the authoring
session. End with `ARTIFACT: <path>` for your review record
(`.project/active/goal-cold-pickup-proof/spec-review.md`).
