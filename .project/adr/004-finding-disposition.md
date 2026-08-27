---
status: accepted
date: 2026-08-25
deciders: [Reid W]
grade: "[OWNER] 2026-08-23"
supersedes: none
amends: exploration/stellarator_e2e/studies/DISCOVERY_LOG.md:3
---

# ADR-004: A goal round dispositions every discovery row its evidence touched, by appending a joined row

## Context

`exploration/stellarator_e2e/studies/DISCOVERY_LOG.md` is the authoritative cross-study finding record. Study execution writes a first-sighting row per finding; nothing consumed those rows afterwards, and twenty-two rows sat in the log with six of them `unrouted`. The concept design retired the cross-round disposition obligation under an agent grade, which the review refused (`.project/concepts/goal-strategy-task-harness-design-review.md` C1). The owner ruled option (a) on 2026-08-23: criterion 4 of `study-driven-model-development.md` **holds as settled**.

## Decision

Every open discovery row a round's evidence touches receives a disposition recording `model fix | research | declared seam | upstream filing`, its status, the responsible task or owner, and what changed or the concrete next reference. **No touched row returns as `unrouted`.**

The study executor writes first-sighting rows. A goal round records dispositions by **appending** a row joined by `<study-id>#<n>`; it never edits a first-sighting row and never mints a finding id. The administrator role stays read-only and never appends.

Row kind is positional: for a given id, the earliest row in file order is the sighting, later rows are disposition updates, and the newest row is that finding's current state. No column marks it.

## Rationale

A finding with no consumer is a silent loss of the study's most expensive output. Giving the obligation to the round result and its fresh review puts the accounting where someone is already reading the round's evidence, so it costs one checklist line rather than a new procedure.

Appending rather than editing keeps the log append-only, which is what makes git's history of it meaningful, and keeps the executor's original sighting intact as written. The disposition is delivered as an appended row under the same id — one mechanism that satisfies both the design's "appends disposition rows" and the epic's "receives a joined disposition update". That reconciliation of the two texts is an orchestrator execution detail (2026-08-25), challengeable by re-deriving it against those two sources.

## Rejected alternatives

- **A shadow finding log owned by the goal layer** — two records of the same finding, guaranteed to disagree.
- **Silent retirement of the obligation** — the review caught this: an owner-settled criterion cannot be superseded by an agent-grade row.
- **Editing the first-sighting row in place** — destroys the executor's original account and breaks the append-only reading of the log.

## Affected seams

- `.claude/skills/run-study/runbook.md` step 14 — the sole-writer sentence.
- `.claude/skills/run-study/runbook.md` § administrator prohibition — the administrator stays read-only.
- `.claude/skills/run-study/runbook.md` § `DISCOVERY_LOG.md` — the one-row-per-finding rule and its schema table.
- `exploration/stellarator_e2e/studies/DISCOVERY_LOG.md` header — the writer rule and the cardinality rule.
- `tests/study/test_records.py::test_findings_join_the_discovery_log` — the join must tolerate multiple rows under one id by intent, not by accident.

## Consequences

A goal round may append only under an id a committed record's § 15 already carries; a row citing an unknown id fails the join test for that record. A finding the goal round discovers itself is therefore not a discovery-log row — it goes to `learnings.md`, a native work item, the research seam, or an ADR, and the trail cites that home.

The one-row-per-finding rule is amended in scope: one row per finding *sighting*, plus joined disposition rows under the same id. "Never a second copy of the finding's account" is untouched — a disposition row carries a disposition, not a restatement.
