# Brief — /implement-model — WI-027 Demo Constraint Execution (STELLARATOR-DEMO Item 2)

Execute `work/active/WI-027_demo-constraint-execution/plan.md` phase-by-phase, filling the plan's Implementation Record as you go. Spec (MR-1…8), design (D1–D6), and plan are settled — implement them; do not improvise the pin, the recapture recipe, or the adapter shapes.

## Required reading, in order

1. `knowledge/holdout/aries-cs/PROTOCOL.md` — §3 barred paths absolute.
2. `work/active/WI-027_demo-constraint-execution/plan.md` — the phases and their gates. Then spec.md and design.md for the bars each gate serves.
3. `work/orchestration/demo-constraint-execution.md` — standing bars, environment facts (exec venv path, `SYSIDE_LICENSE_KEY` via `set -a && source .env && set +a`, IFE anchor values, pytest tally).

## Execution posture

- **Phase gates are hard**: a phase that fails its gate stops the run. Diagnose, and if the fix is within the phase's own scope, fix and re-gate; if it requires deviating from a settled design decision, moving a numeric channel, adding a validation offender, or touching canonical `models/` — **STOP and report the state precisely** (what failed, evidence paths, your diagnosis). Surface-to-orchestrator, never silent-fix. A non-satisfied verdict at the design point is a finding to report, not tune away.
- **The original successor bar binds**: `handshake_1costingfe.py` at most injection-map edits (none expected this item), and `git diff exploration/stellarator_e2e/handshake_comparison.json` must be **empty** at the end. If the regen at the new pin moves the comparison JSON at all, that is a stop-and-report event (it would mean the pin bump moved numerics — design says it must not).
- Commit nothing — the orchestrator commits. Leave the tree in its end state and report.
- Python via `uv run` (repo tooling) and the exec venv the brief names for pipeline execution. All work in this worktree; the sysml-codegen repo is read/checkout-at-pin only per the design.
- Fill the plan's Implementation Record per phase: what ran, gate evidence (exact numbers/paths), deviations (should be none).

End with ARTIFACT: work/active/WI-027_demo-constraint-execution/plan.md (the filled Implementation Record) and a summary of every gate's measured result.
