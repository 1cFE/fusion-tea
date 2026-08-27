# Stage brief: plan — GSTH Item 3 (Verified Package Integration Seam)

**From**: orchestrator (`/_my_orchestrate`), 2026-08-26. Item home: `.project/active/goal-integration-seam/`.

## Inputs

- **Design (approved)**: `design.md` — round-2 APPROVED, lens CLEAR. The contract: `spec.md`. Reviews: `spec_review.md`, `design_review.md` (read the Resolutions and round-2 verdict). Spikes: `spike_regen_determinism.md` (B1), `spike_snapshot_stability.md` (B2) — both CONFIRMED, both bets are now facts.
- Align: `align.md`. Sibling plan precedent: `.project/active/goal-research-seam/plan.md` (Item 2 — nine phases, one commit each, worked well).

## Constraints for the plan

- Effort: design reports 14–15h; phase it honestly. One commit per phase, each phase leaving the tree green (tests passing, `verify`-clean where applicable).
- Absorb the two round-2 advisory residuals: (1) gate 0 checks `--out-dir` resolves outside the package root; (2) the gate-5 test-coverage boundary is echoed in plan.md where `/_my_audit` will see it without reading the design.
- The three R-F5 filings (spine suite takes no package argument; verify.py writes no summary on failure; census derivation has no importable home) and the teax-pin BACKLOG row are plan deliverables — put them in a phase, not a footnote.
- The ADR from design Appendix A ("Integration is a fixed-point proof, not a transformation") is filed in `.project/adr/` per that home's README during implementation.
- Operator guide (docs/integration_seam_operator_guide.md) is a phase of its own with the D14 condition→goal-class mapping, D16 env vars, D18 exit codes, and the surfaced prove-don't-perform boundary in operator words.
- Environment for test phases: `set -a; source ~/1cfe/agentic-mbse/.env; set +a` (SYSIDE key); `STOP_PARSER_TEAX_ROOT` + wheel vars per `tests/study/conftest.py:239-270`; `tests/test_dependency_provenance.py` needs `STOP_PARSER_WHEEL_TARGET` exported.
- Regression gate at the end: `pytest tests/models tests/study tests/test_dependency_provenance.py` green and `git diff --stat -- scripts/study/ tests/models/ tests/test_dependency_provenance.py` empty (R-B2/R-G2).

Write `plan.md` at the item home: phased, checkboxed, each phase with validation and its commit point. End with `ARTIFACT: <path>`.
