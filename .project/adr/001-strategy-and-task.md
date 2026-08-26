---
status: accepted
date: 2026-08-25
deciders: [Reid W]
grade: "[AGENT] ratified by owner; coarse grain inferred from lean-first ruling"
supersedes: none
amends: none
---

# ADR-001: A goal round authorizes one bounded task at a time, under one revisable strategy

## Context

The goal layer sits above the native coding and modeling workflows and decides what work is authorized next. The question was how much work one authorization covers, and whether a round may plan its tasks ahead. Decided in `.project/concepts/goal-strategy-task-harness-design.md` § Recorded Rulings and ADR Candidates, with the coarse grain settled by implication of the lean-first ruling (`.project/concepts/goal-strategy-task-harness-design-review.md` § Resolutions, M1/P3 and P4).

## Decision

A round runs under one `StrategyRevision` — approach, assumptions, abandonment conditions, intended model increment, intended study question — and that revision contains no future task list. At most one task is active at a time. A task is one bounded objective, not one native stage: it may advance a work item across several native stages until it reaches its objective or a genuine stop. Each task records a six-line scope — Objective, Why now, Scope, Inputs, Done when, Stop when — written before work begins.

Strategy is revisable; authorization is not carried forward. Every successor task gets its own recorded scope.

## Rationale

One recorded bounded task at a time prevents stale authority. An agent that holds an open-ended mandate keeps acting on a premise the evidence may already have overtaken, and nothing in the record shows when that happened. Re-recording a scope per task forces the premise to be restated at each step, where a reader — or the fresh round review — can see it.

The grain is coarse because the lean-first ruling makes it so. A prose-and-native-facts loop cannot carry roughly nine scope reviews per round; one bounded objective per task, with per-stage *stop points* preserved, is the consistent reading. Native stage boundaries are not goal events.

## Rejected alternatives

- **Forward task plans inside the strategy** — a plan written before the evidence arrives is authority granted in advance, which is the stale authority this record exists to prevent.
- **Per-native-stage goal tasks** — re-encodes native sequencing at the goal layer and imposes a scope review per stage; too heavy for the lean first build, and the native workflows already own stage state.

## Affected seams

- `work/orchestration/GOAL_RUNBOOK.md` § Running one task — the scope, write-ahead, return sequence.
- `work/orchestration/goal-templates/trail.md` — the six-line scope heading is the contract.
- The round review, which checks every recorded task scope after the round closes.

## Consequences

Scope is a reviewable record, not a technical sandbox. Nothing stops a same-round agent from exceeding its recorded scope; the fresh reviewer sees it afterwards. An unresolved owner gate is the one bound that prevents execution outright.

`PREREQUISITE` is discovered as a return, never predicted in a scope, so a task that hits missing evidence ends and another scoped task may follow in the same round.
