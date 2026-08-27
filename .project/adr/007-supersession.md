---
status: accepted
date: 2026-08-25
deciders: [Reid W]
grade: "[AGENT] task-as-authority-unit half; [OWNER] 2026-08-23 finding-obligation half"
supersedes: none
amends: none
---

# ADR-007: The task is the authority unit; the finding stays the traceability unit

## Context

The predecessor design treated a finding as the thing that authorized follow-up work — findings queued up and pulled work along behind them. The concept design replaced that with the task, and in doing so quietly retired an owner-settled obligation: prior concept criterion 4, that the discovery log carries finding → disposition → what changed across rounds with no dangling dispositions. The review refused the silent retirement and required the candidate be **split** (`.project/concepts/goal-strategy-task-harness-design-review.md` § ADR Candidate Assessment, "Supersession — reshape"). The owner then ruled the second half on 2026-08-23.

## Decision

Two separate things, filed together because they were entangled in one candidate.

**(i) The task is the orchestration authority unit.** `[AGENT]` — what may be worked on next is decided by the round's strategy and recorded in a task scope, not derived from a finding queue. A finding does not authorize work.

**(ii) The finding remains the traceability unit, and its cross-round obligation holds.** `[OWNER]` 2026-08-23 — criterion 4 of `study-driven-model-development.md` holds as settled. Every open discovery row a round's evidence touches gets a joined disposition; nothing dangles. The mechanism is ADR-004.

## Rationale

The two words were doing different jobs and the single candidate hid that. "What am I authorized to do next" and "where did this finding end up" are separate questions with separate answers, and collapsing them is what produced a finding-as-work-queue in the first place — a queue that orders work by discovery order rather than by strategy.

Separating them costs nothing and keeps both properties: strategy chooses the work, and every finding still has to land somewhere visible.

The split also fixes a provenance error. Half of this decision is an agent inference and half is owner-settled; filing it as one agent-grade row would have made an owner ruling challengeable by re-derivation, which is exactly the failure the split prevents.

## Rejected alternatives

- **Finding-as-authorization queues** — orders work by discovery order instead of strategy, and grants authority to something no one scoped.
- **Filing the candidate unsplit at `[AGENT]` grade** — retires an owner-settled criterion under an agent grade. The review refused it, and correctly.

## Affected seams

- Task selection: driven by strategy and evidence, recorded in the task scope (ADR-001).
- Finding disposition: ADR-004 and the discovery log's five textual homes.
- `work/orchestration/GOAL_RUNBOOK.md` — both halves appear, in different sections, and the runbook does not conflate them.

## Consequences

A round's task sequence and its disposition accounting are read separately, and a reader who wants to know "why was this worked on" looks at the strategy and scope, while a reader who wants to know "what happened to this finding" looks at the discovery log.

This record also retro-resolves the deleted predecessor review's parked decision — who writes a finding's state after the study logs it — in the direction that review recommended: the goal round writes the disposition, the executor keeps the sighting.
