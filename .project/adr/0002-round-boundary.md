---
id: 0002
title: One agent pursues one strategy for a round; a fresh agent reviews it and authors the next
date: 2026-08-25
owner: Reid W
status: active
amended_by: []
superseded_by: null
provenance: "[OWNER] purpose; [AGENT] mechanism"
seams: []
supersedes: null
promoted_to: null
---

## Decision

A round is one agent's bounded pursuit of one strategy. It ends in a written `RoundResult`, even when intent was not met, and a closure coverage record. Under the owner's 2026-09-14 process-simplification request, independent review follows `work/orchestration/GOAL_RUNBOOK.md` § Review scope and evidence reuse; routine closure may be a coordinator check with cited evidence and a reason no additional review is needed. Required independent reviewers are fresh non-authors and return `PASS | FINDINGS | OWNER_GATE`. No review reopens a closed round. The coordinator or reviewer may propose the next strategy; the owner retains the close rule. [AGENT] Trigger selection and coverage reuse implement the owner's request; the historical title and rationale below describe the earlier mechanism.

## Why

A goal run is a sequence of attempts, and each attempt is a judgment about whether its own work succeeded. The question was who makes that judgment. Decided in `.project/concepts/goal-strategy-task-harness-design.md` § Recorded Rulings and ADR Candidates; the purpose is the owner's, the mechanism is the design's.

An agent asked to review its own round defends it. Handing the review and the next strategy to an agent who did not do the work limits self-defense at the one point where it costs most: the moment a strategy should be abandoned. The same freshness is what makes the round result honest about unmet intent — a failed attempt is a legitimate result, not something the next round has to rediscover.

The mandatory result is what makes rounds finite. Without it, a round that went nowhere leaves no record and the run's history has a hole exactly where its hardest judgment was.

## Invariants established

- `work/orchestration/GOAL_RUNBOOK.md` § Opening and closing a round, § The fresh review.
- `work/orchestration/goal-templates/trail.md` — the round result and round review headings.
- `learnings.md`: the result proposes the learning delta; closure accepts or corrects it using the required review coverage before append.

Every closed round carries a result and closure coverage record. Account for task scopes, retry classification, touched-finding dispositions, cited-ref liveness, learning delta, and carry-forward. Reuse valid native or checkpoint evidence; independent review covers uncovered triggered risks. Coupled architecture, multiple model families, or failed coverage require substantive independent integration review (see ADR-005).

## Rejected alternatives

- **Perpetual same-agent pursuit** — the agent that chose the strategy is the worst judge of when to abandon it, and a run with no round boundary has no natural point at which anything is re-grounded.
