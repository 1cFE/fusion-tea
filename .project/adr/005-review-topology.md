---
status: accepted
date: 2026-08-25
deciders: [Reid W]
grade: "[AGENT] inference; owner may override"
supersedes: none
amends: none
---

# ADR-005: One fresh round critic, plus one pre-execution disposition checkpoint

## Context

The input concept placed a fresh critic at each native stage. Under the lean-first ruling (ADR-003) that is roughly nine reviews per routine round, duplicating technical reviews the native workflows already run. The review settled the direction by implication of the scale ruling and graded it agent-level, owner may override (`.project/concepts/goal-strategy-task-harness-design-review.md` § Resolutions, M1/P3 and P4).

## Decision

The fresh `RoundReview` is the standing independent critic of the goal layer. It checks native evidence by citation, goal and strategy fidelity, every recorded task scope, retry classification, touched-finding dispositions, the learning delta, and the constraints carried forward. Native technical reviews stay native and the round review consumes their evidence rather than repeating it.

One further check sits before the round review, and it is the owner's placement, not this record's inference — `[OWNER 2026-08-25]`, from `.project/backlog/epic_goal_strategy_task_harness.md` § Product-Lens and `.project/concepts/goal-driven-model-development-harness.md` § Owner's Words ("critic placement"): **a lightweight fresh non-author checkpoint reads a study reading and its proposed dispositions before any semantic follow-up task executes**, and the author revises through it until it passes or a declared cap is hit. Hitting the cap writes a recorded stop the owner can see; it does not silently permit execution. Routine native stages get no separate goal critics.

The two checks are distinct. The checkpoint runs *before* follow-up execution over *the reading and its proposed dispositions*. The round review runs *after the round closes* over *the whole round*.

## Rationale

Duplicate criticism is expensive and it teaches agents that reviews are ceremony. One standing critic at the round boundary is where independent judgment actually changes an outcome — that is the point at which a strategy is abandoned or continued.

The pre-execution checkpoint exists because the round review is too late for one specific failure: dispositions that are wrong get *executed* before anyone independent has read them, and the follow-up work then compounds on a misread. Placing one lightweight fresh reader at that seam is the smallest thing that catches it.

Owner criterion 5 also asks that, after dispositions execute, something checks each landed and the finding moved. That responsibility sits inside the round review, which already accounts for every touched discovery row and what changed. Recording that placement is what keeps criterion 5 from going homeless while the topology stays collapsed. That placement is an `[AGENT]` inference the owner may override.

## Rejected alternatives

- **Per-stage fresh critics** — nine reviews a round, duplicating native technical review, unaffordable under lean-first.
- **A third critic for the post-execution disposition audit** — the round review already walks the touched rows; a separate critic would read the same evidence twice.
- **No pre-execution checkpoint** — leaves the one failure the round review cannot catch in time.

## Affected seams

- `work/orchestration/GOAL_RUNBOOK.md` § The pre-execution disposition checkpoint, § The fresh `RoundReview`, and the table that puts the two side by side.
- `work/orchestration/goal-templates/trail.md` — the checkpoint entry and round review headings.
- Native review stages, which are unchanged and are cited rather than repeated.

## Consequences

Task scope and retry classification remain *recorded* checks — written at the time, audited at round end, not gated in the moment. The checkpoint's cap and the retry cap are declared limits carried in each goal's own `Limits` section.
