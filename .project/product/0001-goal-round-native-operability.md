---
id: 0001
title: A non-builder runs a goal round from the runbook and native records alone
date: 2026-08-30
owner: Reid W
status: active
amended_by: []
superseded_by: null
supersedes: null
provenance: "[AGENT] (ratified by owner, 2026-08-30)"
surfaces: [goal-layer, research-seam, integration-seam, study-route]
checked: 2026-08-30 @ a384e26b
---

## Promise

A fresh operator or agent who is not the builder can ground an operator-chosen question into `work/orchestration/goals/{goal}/`, run bounded rounds through the native research, modeling, integration, and study workflows, resume an interrupted task from its write-ahead start and filesystem facts, and close the round with every touched discovery finding carrying a joined disposition — using `work/orchestration/GOAL_RUNBOOK.md` and native records alone. An ungrounded goal cannot start; the reading and proposed dispositions pass an independent checkpoint before semantic follow-up work executes; no manual seam and no separate control plane is involved.

## Authority

- `.project/concepts/goal-driven-model-development-harness.md` § Owner's Words, § Success Criteria — `[OWNER]`; the stated need this promise implements.
- `.project/concepts/goal-strategy-task-harness-design.md` — concept-design; `[AGENT]`, ratified through the two concept-design reviews (owner resolutions in `goal-strategy-task-harness-design-review.md` and `-review-2.md`).
- `.project/completed/20260830_epic_goal_strategy_task_harness.md` § Success Criteria — the epic contract; all criteria ticked at epic close 2026-08-30.
- `work/orchestration/GOAL_RUNBOOK.md` — the operating contract itself; every seam row it lists is native as of `c4c7d723`.
- `.project/adr/` 0001–0005 and 0009 — the mechanism decisions (strategy/task shape, round boundary, lean persistence, finding disposition, review topology, integration fixed-point); cited, not restated.

## Evidence

- Live proofs, kept in full: `.project/completed/20260827_goal-cold-pickup-proof/` (cold grounding, ungrounded rejection, mid-task kill and resume, fresh round review), `.project/completed/20260828_goal-research-model-proof/` (the pre-execution checkpoint refused then passed on a live round), `.project/completed/20260830_goal-integration-study-proof/` (`integrate → study.execute → study.read → dispositions → fresh review` live; hand and goal-agent routes byte-identical on native identity per its `route_equivalence.md`).
- Three goals grounded and closed under the contract: `work/orchestration/goals/cryo-volume-basis/`, `p-pump-basis/`, `p-pump-fence/`.
- Full regression 2026-08-29: 574 passed / 14 skipped (`.project/completed/20260830_goal-integration-study-proof/epic_evidence.md` § 1).

## Scope

Three declared limits, recorded in `epic_evidence.md` § 3 and not worked around: the research seam's request/return bookkeeper (`scripts/research_seam.py` open → log → close) has never run end to end in a live round (its write door has — two registrations); `assert_read_set_covered` at integrate gate 6 has no live evidence and nothing else covers it (filed); route equivalence fixture-substituted `study.execute`, so hand production of the study points themselves is unproven by design.
