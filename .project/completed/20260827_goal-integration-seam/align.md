# Align — Goal Harness Item 3 (Verified Package Integration Seam)

**Date**: 2026-08-26 · **Owner**: Reid W · **Orchestrator**: Fable (`/_my_orchestrate`)

Owner rulings at launch (`[OWNER 2026-08-26]`):

1. **Branch**: stay in this worktree; new branch `feat/goal-integration-seam` based on the current `feat/run-study-first-consumer` tip (`990501af`), which carries Item 1's ADR home and Item 2's merged seam.
2. **Reserved gates**: none beyond standing defaults (merge/push, item close stay owner-held). "Just get it done — you are responsible for quality and alignment to the concept / concept design."

Orchestrator readings recorded at Align (`[AGENT]`, unchallenged):

- Entry-surface shape, return-artifact format/location, and the SC1 test-fixture strategy (obtaining a "known audited model change" without minting new model work) are design decisions, recorded in `design.md`.
- The known parser limitation (calc-then-compare constraints unparseable by `scripts/study/indicators.py:469` / `verify.py:193`; BACKLOG Flagged row) stays out of scope; the seam surfaces the native gate result as-is.
- Changes inside pinned sysml-codegen / teax / agentic-mbse are upstream filings only, never in-repo edits; the seam is a fusion-tea-side wrapper invoking existing gates in their authoritative order.
- Item 3 does not touch GOAL_RUNBOOK, DISCOVERY_LOG, or the run-study runbook; its operator doc is its own deliverable. Decisions of record are filed in Item 1's ADR home (`.project/adr/`).
- `spec_review` and `design_review` run as fresh stage sessions.
