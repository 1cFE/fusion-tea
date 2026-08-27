# Brief: spec stage — Goal Harness Item 1 (Lean Goal Contract and Operator Runbook)

**From**: orchestrator (Fable), running `/_my_orchestrate` for epic GSTH Item 1
**Date**: 2026-08-25
**Item location**: `.project/active/goal-harness-contract/`

## What this item is

Epic: `.project/backlog/epic_goal_strategy_task_harness.md`, Item 1. Read that item in full — it is the requirements source. Primary design authority: `.project/concepts/goal-strategy-task-harness-design.md` (approved concept-design). Owner rulings live in `.project/concepts/goal-strategy-task-harness-design-review.md` § Resolutions and `...-review-2.md` § Resolutions.

Objective `[INHERITED: epic GSTH Item 1]`: establish the smallest durable goal contract that a human or goal agent can operate without mirroring native workflow state. Four deliverable groups:

1. **Architecture records** — file the seven approved decisions (Strategy and Task, Round Boundary, Lean-First Persistence, Finding Disposition, Review Topology, Goal Evidence Seam, split Supersession) in a repository-native ADR home; amend CLAUDE.md so goal inputs may cite `.project/` evidence while each PM stays mutable only through native operations (`[OWNER]`). The decisions and their provenance grades are already written in the design's "Recorded Rulings and ADR Candidates" table — filing, not re-deciding.
2. **Lean artifact contract** — conventions for `goal.md`, `trail.md`, `learnings.md`: grounding, one active task, write-ahead start, six-value task return, five decision fields, round limits, `RoundResult`, `RoundReview` (`[INHERITED: design]`). Plus one lightweight fresh non-author checkpoint over a study reading and proposed dispositions before any semantic follow-up task executes; routine native stages get no separate goal critics (`[OWNER 2026-08-25]`, epic product-lens F2 disposition).
3. **Writer ownership** — amend `.claude/skills/run-study/runbook.md` step 14, the administrator prohibition, and the `exploration/stellarator_e2e/studies/DISCOVERY_LOG.md` header so: executor writes first sightings, goal agent appends joined `<study-id>#<n>` disposition rows, administrator stays read-only (`[OWNER]`, review 1 resolution C1).
4. **Operating surface** — `work/orchestration/GOAL_RUNBOOK.md` plus the smallest fusion-tea-owned instructions/templates for a human and a goal agent to follow the same contract (`[INHERITED: design]`).

## Owner rulings from today's Align (`[OWNER 2026-08-25]`)

- Work happens on the current branch `feat/run-study-first-consumer`. No child branch. Do not wait for Run-Study Item 6 Phase 4 or Item 7 — the Phase 4 gate applies only to *closing* Item 6.
- When editing `.claude/skills/run-study/runbook.md`, **preserve Item 6's pending runbook findings** (#6, #10, #11 — see `.project/active/run-study-first-consumer/plan.md` Phase 3/4 notes). Phase 4 will land those sentences; do not clobber or pre-empt them.
- No reserved gates beyond the standing defaults (merge/push and item close stay owner-held).
- The parallel Item 2 agent (research seam) works in a separate worktree; stay out of `scripts/zotero_*`, research entry surfaces, and `knowledge/` registry files. Where the runbook describes the research seam, cite it as pending native repair per the design's seam table.

## Hard boundary (`[OWNER]`, review 1 resolution P2/M4)

Out of scope, no exceptions without a recorded observed failure: task-envelope files, machine event ledger, content digests, idempotency/effect-query machinery, reconciliation, concurrent goal runs, unattended dispatch. Also out: replacing/mirroring any native workflow state; automating owner-reserved gates, close, archive, commits, pushes.

## Orchestrator's reading (agent-grade, challengeable)

- `[AGENT]` "Contract and documentation tests" means lightweight consistency checks (e.g., pytest asserting the three writer-ownership homes agree, templates parse/exist), not goal-agent machinery.
- `[AGENT]` This is a contracts-and-documentation item; no executable goal-agent code is in scope.

## Success criteria

Use the epic Item 1 success criteria verbatim as the spec's acceptance basis. Note the epic-level criterion that the pre-execution disposition checkpoint and post-round `RoundReview` have **distinct timing and responsibilities** — the spec must keep them separate.

## What the spec stage should produce

`.project/active/goal-harness-contract/spec.md` — requirements, scope, out-of-scope, acceptance criteria, with provenance grades preserved per `claude-pack/rules/capture-fidelity.md`. Do not overwrite any existing spec elsewhere. Defer mechanism choices (ADR home location, template paths, test harness shape) to design.
