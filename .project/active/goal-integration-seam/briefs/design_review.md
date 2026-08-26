# Stage brief: design_review — GSTH Item 3 (Verified Package Integration Seam)

**From**: orchestrator (`/_my_orchestrate`), 2026-08-26. Fresh session; you did not author the design.

## Review target

`.project/active/goal-integration-seam/design.md` (committed). Against: `spec.md` (the contract, revised through spec_review), `spec_review.md` § Resolutions, `align.md`, `spike_regen_determinism.md`, epic `epic_goal_strategy_task_harness.md` § Item 3, concept-design `goal-strategy-task-harness-design.md` § Native seams.

## Orchestrator rulings already made (do not relitigate; check the design honors them)

- Prove-don't-perform ACCEPTED (design § Surfaced; commit trail). Review the *derivation and consequences*, not whether to take it.
- L2-1 baseline execution inside the seam; L2-2 one shared entry surface.

## What I need from you

Review as an architecture check: does every spec requirement (R-A1..R-G4, SC1–SC6) land somewhere concrete in the design; are D1–D12 sound with honest rejected alternatives; is the per-producer detection table (Architecture) correct against the actual producer code (verify exit-code/junit claims against `preflight.py`, `verify.py`, `manifest.py`, pytest behavior); is the restore path (D7) actually bounded and safe; does the workspace fixture (D10) truly keep git-backed gates meaningful; is the return schema sufficient for R-A2/R-E2/R-E3 and for Item 6's consumption; any hardening-path machinery smuggled in against R-F2; any producer edit against R-B2. Flag anything the plan stage would have to guess.

B2 (snapshot recapture stability) is being measured by a parallel spike — note it as pending rather than re-arguing it.

Split findings into must-fix (blocks plan) and advisory. Write the review to `.project/active/goal-integration-seam/design_review.md`; end with `ARTIFACT: <path>`.
