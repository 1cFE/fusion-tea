# Spec — GSTH Item 6: Integration-to-Study Closure and Route Equivalence

**Status**: Active
**Owner**: Reid W
**Created**: 2026-08-29
**Branch**: `feat/wi033-p-pump-rebase` (owner-ruled: one PR ships WI-033 + Item 6)
**Requirement source**: `.project/backlog/epic_goal_strategy_task_harness.md` § Item 6 — the epic block (Scope 1–5, Success Criteria 1–7, Out of Scope, Deliverables) is the spec. This file records only what the 2026-08-29 Align added or changed. Orchestrated run; spec authored by the orchestrator per the lean-shape ruling below.

## Align rulings (2026-08-29, owner present)

1. **Goal for the round** `[OWNER 2026-08-29]`: ground a **new successor goal** on the open tail of discovery row `20260821-power-cycle-ab#3` — "where the `recirc_ok` fence moves and what LCOE does still need a package run" (`exploration/stellarator_e2e/studies/DISCOVERY_LOG.md:33`). `p-pump-basis` stays closed; it is not reopened. § Question and § Answered when are the owner's own sentences, collected before the round opens (reserved gate).
2. **PR routing** `[OWNER 2026-08-28, reaffirmed 2026-08-29]`: Item 6 runs on `feat/wi033-p-pump-rebase`; its integrate run regenerates and commits the package through the seam; one PR ships WI-033 + Item 6 (pre_pr option (a), `.project/reports/2026-08-28-pre-pr-wi033-p-pump-rebase.md`). The battery's 21 designed reds are expected to go green at that point and this is verified before the final gate. *Amendment 2026-08-29 (plan D2, orchestrator):* "regenerates and commits the package through the seam" was this spec's loose phrasing — ADR-009 bars the seam from performing or committing (prove, don't perform). The precise reading, which delivers the owner's stated outcome: Item 6 regenerates natively, commits, and the seam proves the fixed point and returns the pin. Surfaced in plan § D2, not resolved silently.
3. **Epic amendment** `[OWNER 2026-08-29]`: Item 6's discharged Current State lines amended by a dated note citing WI-033's record; original lines kept as history.
4. **Reserved gates** `[OWNER 2026-08-29]`: goal grounding wording; goal close ruling; push/PR/merge; any ruling an adverse or inconclusive study reading requests (the round closes on it regardless — repair is next-round). Everything else is execution detail, decided and recorded loudly.
5. **Route-equivalence human route** `[OWNER 2026-08-29]`: a hand-operated session follows `work/orchestration/GOAL_RUNBOOK.md` step by step; owner supervises at checkpoints. The isolation design — no duplicate external effects, no second committed study, no second promoted pin — is the plan's one real design question (no separate design.md).
6. **Lean shape** `[OWNER 2026-08-29]`: spec (this file) → plan → implement → audit. Deviation from the epic deliverables list: no `design.md`; its content (route-equivalence isolation method) lives in `plan.md`. No spec_review/design_review — the round's own independent mechanisms (pre-execution critic where applicable, fresh administrator, fresh `RoundReview`, route-equivalence comparison) plus the final audit carry the criticism.

## Success criteria

The seven epic § Item 6 criteria govern verbatim. One honesty obligation added:

8. `epic_evidence.md` states plainly that the research seam's request/return bookkeeper (`scripts/research_seam.py` open → log → close) has never run end-to-end; the WI-033 flip evidence covers the seam's write door only. Carried from WI-033 verification record § 4 `[OWNER 2026-08-28]`. The round does not force a research disposition just to exercise the bookkeeper.

## Out of scope

As the epic block, plus: reopening `p-pump-basis`; any research registration (both sources this thread needs are already registered).
