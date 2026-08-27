# Stage brief: spec_review — GSTH Item 3 (Verified Package Integration Seam)

**From**: orchestrator (`/_my_orchestrate`), 2026-08-26. Fresh session; you did not author the spec.

## Review target

`.project/active/goal-integration-seam/spec.md` (committed). Companion ledger: `product-lens.md` in the same dir (a lens pass already ran and its four findings were fixed in the spec — do not repeat it; review the spec on its own terms).

## Context

- Requirements source: `.project/backlog/epic_goal_strategy_task_harness.md` § Item 3.
- Concept intent: `.project/concepts/goal-strategy-task-harness-design.md` § Native seams (the `integrate` row) and § Validation and Handoff.
- Owner rulings: `.project/active/goal-integration-seam/align.md` (`[OWNER 2026-08-26]`: no reserved gates beyond merge/push/close; entry-surface shape, return format/home, SC1 fixture strategy delegated to design).
- Manual referents the seam wraps: `.project/completed/20260821_stellarator-model-migration/plan.md` Phases 2–3; `.project/active/run-study-first-consumer/plan.md` Phase 3.
- Existing gates: `scripts/study/manifest.py`, `preflight.py`, `verify.py`, `identity.py`; `tests/models/test_model_family_spines.py`; `tests/test_dependency_provenance.py`.
- Sibling precedent: `.project/active/goal-research-seam/spec.md` (Item 2, same contract shape, already audited).

## What I need from you

Review the spec as a requirements contract: completeness against epic Item 3, testability of SC1–SC6, spec/design boundary discipline (no mechanism smuggled in), provenance-grade fidelity (capture-fidelity laws), internal consistency (return classes vs. requirement clauses), and whether a design session could proceed without guessing. Verify cited code behavior where a claim is load-bearing (e.g., R-B1's authoritative order, the claim that preflight/verify need executed results).

Return findings split into **must-fix** (blocks design) and **advisory**. If clean, say so plainly. End with `ARTIFACT: <path>` if you write a review file (write it to `.project/active/goal-integration-seam/spec_review.md`), or your findings in prose.
