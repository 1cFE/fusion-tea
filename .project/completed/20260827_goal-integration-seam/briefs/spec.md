# Stage brief: spec — GSTH Item 3 (Verified Package Integration Seam)

**From**: orchestrator (`/_my_orchestrate`), 2026-08-26. **Item home**: `.project/active/goal-integration-seam/`.

## Work item

Epic: `.project/backlog/epic_goal_strategy_task_harness.md` § Item 3 — read it in full; it is the requirements source. Objective: turn audited model work into exactly one verified, study-ready candidate pin and fingerprint, or a named blocker.

The manual sequence this seam wraps is proven and distributed across work-item plans and shell commands: regeneration → handwritten-preservation → model-family spine → census/snapshot → manifest re-pin → preflight → verification. The seam must invoke each existing producer-owned gate in its authoritative order — never reimplement one — and fail closed on dirty/drifted inputs, unverifiable output, fingerprint mismatch, missing declared keys/constraints, and ambiguous candidate lineage. Re-running on unchanged inputs must not mint a second conflicting candidate identity. The return is a concise, citable integration record a goal agent or human can consume without re-deriving the sequence.

## Intent from the concept (why this exists)

The goal harness (concept-design `.project/concepts/goal-strategy-task-harness-design.md` § Native seams) defines an `integrate` seam: invoke with audited item(s) + expected lineage; native return is a verified candidate pin and fingerprint; the goal question it answers is "Is there one study-ready candidate?" Until this repair exists, goal rounds must reconstruct the hand pattern, and epic Item 6 (integration-to-study closure) cannot run. The customer is a goal task (or a human on the same runbook) that requests integration and receives one authoritative candidate reference. Alignment to that concept intent is the quality bar.

## Required reading (per epic item)

- `.project/concepts/goal-strategy-task-harness-design.md` § Native seams and § Validation and Handoff
- `.project/active/run-study-first-consumer/plan.md` — current manual integration referent
- `.project/completed/20260821_stellarator-model-migration/plan.md` — sealed-package migration and verification path
- `scripts/study/manifest.py`, `preflight.py`, `verify.py`, `identity.py` — existing gates
- `tests/models/test_model_family_spines.py`, `tests/test_dependency_provenance.py` — lineage and generated-tree checks

## Constraints and provenance

- Out of scope (epic, owner-ratified): changing sysml-codegen/teax/the model/study semantics to make a candidate pass; auto-commit/push/close; selecting among multiple valid designs; goal-side effects ledger, idempotency wrapper, duplicate verification.
- `[OWNER 2026-08-26]` (align.md): no reserved gates beyond standing defaults; branch is `feat/goal-integration-seam` in this worktree.
- `[AGENT]` orchestrator readings (align.md, unchallenged — do not treat as owner intent): entry-surface shape, return-artifact format/home, and SC1 fixture strategy are deferred to design; the calc-then-compare parser limitation (`scripts/study/indicators.py:469` / `verify.py:193`, BACKLOG Flagged row) stays unfixed and is surfaced as-is; pinned-tool changes are upstream filings only; ADRs go to `.project/adr/`.
- Success criteria: the five checkboxes in epic Item 3 — carry them into the spec as testable acceptance criteria.

## Instructions

Write `spec.md` at the item home. Requirements and acceptance criteria only — defer mechanism, thresholds, and file formats to design (per project rule: no design-shaped decisions in spec). Grade provenance per capture-fidelity. What the epic cannot settle, decide and record as `[INFERRED]`. End with `ARTIFACT: <path>`.
