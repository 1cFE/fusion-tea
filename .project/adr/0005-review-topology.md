---
id: 0005
title: One fresh round critic, plus one pre-execution disposition checkpoint
date: 2026-08-25
owner: Reid W
status: active
amended_by: []
superseded_by: null
provenance: "[AGENT] inference (topology; owner may override) + [OWNER 2026-08-25] (pre-execution checkpoint placement)"
seams: []
supersedes: null
promoted_to: null
---

## Decision

As amended for the owner's 2026-09-14 process-simplification request, review coverage follows `work/orchestration/GOAL_RUNBOOK.md` § Review scope and evidence reuse. Independent reviews are required for concrete source/math, design, and integration risks; routine work may close with a reasoned coordinator check. Coverage includes native evidence, goal and strategy fidelity, task scope, retries, touched-finding dispositions, learnings, and carry-forward. Native, study, checkpoint, and round reviews reuse valid evidence rather than checking the same claim in separate sessions. [AGENT] This risk-based topology implements the owner's request; the historical title and rationale below describe the earlier mechanism.

Review of uncovered triggered risks in a study reading and proposed dispositions occurs before dependent semantic follow-up executes. This preserves the pre-execution placement from `[OWNER 2026-08-25]` (`.project/backlog/epic_goal_strategy_task_harness.md` § Product-Lens), while the 2026-09-14 request removes unconditional additional sessions. A required independent reviewer must be a fresh non-author. Reuse that reviewer for corrective diffs. The declared cap still stops unresolved dependent work; it never permits execution. Owner-reserved scientific decisions remain owner-held.

The two responsibilities have different timing: reasoning before dependent execution and remaining result coverage after closure. They need separate sessions only when the risks or evidence demand them.

## Why

The input concept placed a fresh critic at each native stage. Under the lean-first ruling (ADR-003) that is roughly nine reviews per routine round, duplicating technical reviews the native workflows already run. The review settled the direction by implication of the scale ruling and graded it agent-level, owner may override (`.project/concepts/goal-strategy-task-harness-design-review.md` § Resolutions, M1/P3 and P4).

Duplicate criticism is expensive and it teaches agents that reviews are ceremony. One standing critic at the round boundary is where independent judgment actually changes an outcome — that is the point at which a strategy is abandoned or continued.

The pre-execution checkpoint exists because the round review is too late for one specific failure: dispositions that are wrong get *executed* before anyone independent has read them, and the follow-up work then compounds on a misread. Placing one lightweight fresh reader at that seam is the smallest thing that catches it.

Owner criterion 5 also asks that, after dispositions execute, something checks each landed and the finding moved. That responsibility sits inside the round review, which already accounts for every touched discovery row and what changed. Recording that placement is what keeps criterion 5 from going homeless while the topology stays collapsed. That placement is an `[AGENT]` inference the owner may override.

## Invariants established

- `work/orchestration/GOAL_RUNBOOK.md` § The pre-execution disposition checkpoint, § The fresh review, and the table that puts the two side by side.
- `work/orchestration/goal-templates/trail.md` — the checkpoint entry and round review headings.
- Native review coverage, cited rather than repeated; stages may be brief or skipped when their responsibilities are satisfied or inapplicable.

Task scope and retry classification remain *recorded* checks — written at the time, audited at round end, not gated in the moment. The checkpoint's cap and the retry cap are declared limits carried in each goal's own `Limits` section.

## Rejected alternatives

- **Per-stage fresh critics** — nine reviews a round, duplicating native technical review, unaffordable under lean-first.
- **A third critic for the post-execution disposition audit** — the round review already walks the touched rows; a separate critic would read the same evidence twice.
- **Deferring required pre-execution coverage until closure** — allows an unchecked scientific interpretation to compound through follow-up work.
