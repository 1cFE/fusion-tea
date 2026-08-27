# Align — GSTH Item 4: Goal Grounding, Cold-Pickup Resume, and Round-Review Proof

**Date**: 2026-08-26
**Mode**: `/_my_orchestrate`, owner present at launch
**Epic**: `.project/backlog/epic_goal_strategy_task_harness.md` § Item 4

## Reading of the work (confirmed)

A proof item, not a build item. The deliverable is kept evidence that Item 1's lean goal
contract works cold:

1. **Cold grounding** — a fresh non-builder co-develops and grounds a real goal from an
   operator question; a deliberately ungrounded draft is rejected before any task starts,
   with the missing fields named.
2. **Interrupted resume** — a bounded task with a write-ahead start is intentionally ended
   without a task return; a second fresh session resolves it from the goal directory and
   native filesystem facts, without repeating the completed native effect.
3. **Bounded closure + fresh review** — the round closes with no promoted pin and no
   committed study (bounded-negative, owner gate, or declared limit); one scope or
   comparison-meaning drift is seeded; a fresh `RoundReview` must catch it, account for
   every touched discovery row, and accept or correct the learning delta.

Any prose failure is recorded; no hardening mechanism is promoted without that evidence.
Out of scope: solving the chosen finding; using Item 2/3's native seams (manual patterns
allowed); unattended dispatch.

## Owner decisions

1. **Operator question**: delegated — "you pick" `[OWNER 2026-08-26]`. Orchestrator's
   recorded call `[AGENT]`: ground the proof goal on discovery row
   `20260823-magnet-technology-ab#2` — should `vol_cold_cryo` be computed from the
   ampere-turns the model already carries plus DI-010's J_eng, instead of held?
   Basis: richest grounding chain available (study record + DI-010 + WI-031 approved
   research), and a round on it can close honestly on an owner gate or declared limit
   without doing model work.
2. **Operator role**: orchestrator plays the operator in the co-development
   `[OWNER 2026-08-26]`. The owner wants the orchestrator's **notes on how the exchange
   works** as part of the evidence — add an operator-notes artifact to the deliverables.
   Provenance in `goal.md` must mark operator-side content as orchestrator-operationalized
   (`[AGENT]`), never as owner intent.
3. **Branch**: continue on `feat/goal-integration-seam`, no child branch
   `[OWNER 2026-08-26]`.
4. **Reserved gates in the proof goal** (`[AGENT]` default, ratified by owner 2026-08-26):
   merge, push, item close, archive owner-held per the runbook; plus any model or
   knowledge mutation beyond the goal directory needs owner sign-off.

## Flags recorded at Align

- Item 1 is audited and gate-CLEAR but not owner-closed; Item 4 builds on its artifacts
  as they stand.
- `work/orchestration/goals/` does not exist yet — this item creates the first real goal
  directory.
- No provenance conflicts or suspect `[HARD]` constraints found.

## Planned route

spec → spec_review → design → design_review → plan → implement (proof runs via cold
headless sessions) → audit. Orchestrator deviates if the work warrants.
