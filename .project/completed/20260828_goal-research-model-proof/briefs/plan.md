# Brief to /_my_plan — GSTH Item 5: Research-to-Model Round Proof

Write `.project/active/goal-research-model-proof/plan.md`. Do NOT run git commits.
Finish with `ARTIFACT: <path>`.

## Contract and design

- Spec (the contract): `.project/active/goal-research-model-proof/spec.md`
- Design (approved after review, revision applied 2026-08-27): `design.md` in the same
  dir — its § Next-Stage Handoff lists what is FIXED for you (slug, one round,
  spec-model ceiling, session choreography, D8 mapping home, request shape, commit
  sequence, ten invariants, grounding-brief may/may-not lists). Do not reopen those.
- Reviews: `spec-review.md`, `design-review.md` (both applied). `align.md` = owner
  rulings, settled.

## What the plan must be

A phased execution plan with checkboxes, following the design's § The commit sequence
(phases 0–9) — each phase naming: the commits it lands, the session(s) it runs (per
design § Sessions), the artifacts produced, and its verification step. Match Item 4's
plan as the shape reference (`.project/completed/20260827_goal-cold-pickup-proof/plan.md`).

Structural requirements:

1. **Owner pause points are explicit phase boundaries.** Gate (a) after grounding turn 1,
   gate (b) after the seam return, gate (c) if the close is a judgment call. Mark each
   as "WAIT: owner ruling" — the run parks there; the plan must be resumable at each.
2. **Draft the two sensitive brief texts IN the plan, verbatim**, per design:
   - the grounding brief (session 01), checked against § The grounding guard's
     may/may-not lists and Invariant 3's fence — this is the de-risk-first item;
   - the T-002 resume brief carrying D5's operator ruling, checked for what it may
     name only AFTER T-001's return is on disk.
   Include a self-check step: grep the drafted grounding brief against the Invariant 3
   denial list before it is committed.
3. **Conditional branches are phases too**: the C-001.r2 route-change resubmission (now
   likely, per M1), the BLOCKER-new-task path, the no-prerequisite (T-001 COMPLETE)
   path, and the queue/park closes. Each names which covering-branch row it lands on.
4. **Verification phase**: the ten invariant checks and two ancestry predicates as
   concrete commands with expected shapes, per design § Validation Approach; the
   verification_record.md build; § Failures and § Hardening verdict.
5. **The flip and bookkeeping phase**: the four runbook edits (R-G1–G4, exact lines in
   design), the CURRENT_WORK strike-plus-pointer (C1 wording), freshness record close,
   operator notes.
6. Every phase carries its evidence commit(s) so the trail stays auditable; briefs
   committed before their runs, transcripts after (design § Sessions / brief fence).

Operational constraints (design § Implementation Notes — carry them into the phases
that need them): direct `claude -p --output-format stream-json --verbose` teed to
`~/goal-proof-logs-item5/`; never orchestrate-stage.sh; date-anchored predicates;
fence sweeps on tool-call inputs; `set -a; source ~/1cfe/agentic-mbse/.env; set +a`
before tests/models; `pm approve-research` empty-insight refusal is a known upstream
defect — record in § Failures if hit.

Budget: design's realistic ceiling is ~9 sessions + one substantive judgment inside 8h
execute; the plan phases should show where the flex is (conditional sessions).
