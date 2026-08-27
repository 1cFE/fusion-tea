# Stage brief: audit — GSTH Item 3 (Verified Package Integration Seam)

**From**: orchestrator (`/_my_orchestrate`), 2026-08-26. Fresh session; you did not build any of this. Item home: `.project/active/goal-integration-seam/`.

## What you are auditing

The implemented integration seam: `scripts/integrate.py`, `tests/study/test_integrate_*.py`, the `integration_workspace` conftest fixture, `docs/integration_seam_operator_guide.md`, ADR-009 in `.project/adr/`, and the BACKLOG filings. Ten phase commits `b0b19a0e..9151f853` (Phase 4 = `fa5245f0`). Contract: `spec.md` (SC1–SC6, R-A..R-G). Architecture: `design.md` (round-2 APPROVED; D19–D21 added during implementation). Execution record: `plan.md` (per-phase notes, deviations). Reviews/spikes in the same dir.

## Your duties

1. **SC6 — the operator-guide walk (this is on you by construction).** Work ONLY from `docs/integration_seam_operator_guide.md`: assemble a real integration request, invoke the seam, read the return, distinguish CANDIDATE from BLOCKER, and act on one blocker. Record in the audit **every point where you had to read source or guess**. This walk is SC6's evidence; the sibling seam's audit failed its analogue (SC7/SC9), so be honest, not generous. Environment: `~/1cfe/agentic-mbse/.env` + `.venv/integration.env` via `uv run --env-file` (the guide should tell you this — if it doesn't, that's a finding).
2. **Verify the implement report's claims**: run the focused suite and the regression gate; confirm 341/1 and 392/14/0 (or explain drift); confirm `git diff --stat fa5245f0^..HEAD -- scripts/study/ tests/models/ tests/test_dependency_provenance.py` empty (R-B2).
3. **Audit against spec and design**: every SC and every R-clause lands or its absence is recorded (D17's stated non-coverage, the gate-5 refusal boundary); the ten-gate sequence and stop rule match design; no gate thinned, mocked, or reimplemented (R-G4, R-B1); no hardening machinery (R-F2); return schema matches design; condition slugs match the D14+plan set; deviations D19–D21 are sound and honestly graded.
4. **Code quality**: placeholder/TODO hunt, dead code, error-path honesty (the seam-internal-error bug was fixed — check the fix is real), test hermeticity (R-G3: no test writes a tracked file — verify, don't trust).
5. **Filings**: ADR-009 filed per `.project/adr/README.md` and indexed; the six filings exist where the plan says; the unrelated `tests/scoring_v2` failures are filed, out of scope here, and NOT silently absorbed anywhere.

Verdict: POSITIVE or Needs Work with findings ranked (blockers vs lower). Write `.project/active/goal-integration-seam/audit.md`; commit nothing. End with `ARTIFACT: <path>`.
