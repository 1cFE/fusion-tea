---
status: accepted
date: 2026-08-25
deciders: [Reid W]
grade: "[OWNER] purpose; [AGENT] mechanism"
supersedes: none
amends: none
---

# ADR-002: One agent pursues one strategy for a round; a fresh agent reviews it and authors the next

## Context

A goal run is a sequence of attempts, and each attempt is a judgment about whether its own work succeeded. The question was who makes that judgment. Decided in `.project/concepts/goal-strategy-task-harness-design.md` § Recorded Rulings and ADR Candidates; the purpose is the owner's, the mechanism is the design's.

## Decision

A round is one agent's bounded pursuit of one strategy. It ends in a mandatory `RoundResult` — recorded even when the intent was not met — and is then reviewed by a fresh agent who did not do the work. The reviewer returns `PASS | FINDINGS | OWNER_GATE` and never resumes the closed round. After a pass, that fresh agent either recommends the owner-held close or writes the next strategy.

## Rationale

An agent asked to review its own round defends it. Handing the review and the next strategy to an agent who did not do the work limits self-defense at the one point where it costs most: the moment a strategy should be abandoned. The same freshness is what makes the round result honest about unmet intent — a failed attempt is a legitimate result, not something the next round has to rediscover.

The mandatory result is what makes rounds finite. Without it, a round that went nowhere leaves no record and the run's history has a hole exactly where its hardest judgment was.

## Rejected alternatives

- **Perpetual same-agent pursuit** — the agent that chose the strategy is the worst judge of when to abandon it, and a run with no round boundary has no natural point at which anything is re-grounded.

## Affected seams

- `work/orchestration/GOAL_RUNBOOK.md` § Opening and closing a round, § The fresh `RoundReview`.
- `work/orchestration/goal-templates/trail.md` — the round result and round review headings.
- `learnings.md`: the result *proposes* the learning delta; the fresh review accepts or corrects it before append.

## Consequences

Every closed round carries exactly one result and one review, by different agents. The review's scope is the whole round — task scopes, retry classification, touched-finding dispositions, cited-ref liveness, learning delta, carry-forward — which is also where the post-execution audit of finding dispositions lives (see ADR-005).
