# Stage brief: spec revision — GSTH Item 3 (after spec_review verdict: Revise)

**From**: orchestrator (`/_my_orchestrate`), 2026-08-26. The original spec author's session is gone; you are a fresh session amending the committed `.project/active/goal-integration-seam/spec.md` in place. Do not rewrite it — amend surgically, preserving its structure, provenance grades, and the product-lens resolutions already recorded in `product-lens.md`.

## Inputs

- The spec: `.project/active/goal-integration-seam/spec.md`
- The review (all findings, must-fix and advisory): `.project/active/goal-integration-seam/spec_review.md`
- Referents the review checked: `tests/test_dependency_provenance.py`, `.project/completed/20260821_stellarator-model-migration/plan.md`, `.project/active/run-study-first-consumer/plan.md`, `scripts/study/preflight.py`
- Align rulings: `align.md` (same dir)

## Instructions

Fix all four must-fix findings and the advisory items (they are cheap; skip one only with a recorded reason). Verify each review claim against the cited file before acting on it — the reviewer is fresh too. Orchestrator steering, recorded as `[AGENT]`:

1. **L1-1 (teax pin)**: State the true producer coverage. Where no producer exists (teax revision), the spec must not pretend one does, and R-B2's "invoke, never reimplement" cannot apply to a gate nobody owns: either (a) require the seam to perform the pin comparison itself as the migration's hand pattern did — this is not duplicate verification, because there is no native implementation to duplicate — with the gap recorded against its proper home per R-F5, or (b) name it an explicit open question for design with the fail-closed default stated. Choose one and record why.
2. **L1-2 (order provenance)**: Correct the order to what the referent actually proved, and re-grade what is inference as `[INFERRED]` rather than `[HARD] as proven`. If the authoritative order is genuinely settled by producer data-dependencies rather than by the referent's incidental sequence, say that — that is a legitimate basis, but it must be stated as the basis.
3. **L3-1 (re-run determinism)**: State the determinism assumption explicitly. Define the contract under non-determinism: a re-run on unchanged inputs must never silently mint a second conflicting identity — it returns the same identity or a `BLOCKER` (R-D3's fingerprint-mismatch seen from the other side). Amend the "safe to call twice" prose to match. Flag it as a candidate de-risk check for design (verify regeneration is byte-stable onto its own output before building on it).
4. **L1-3**: Narrow the motivating example to the true version; fix the R-C9 echo.
5. Advisory: fix citations, cite `preflight.py:368-370` `DID_NOT_RUN` as R-A6 precedent, mark the Non-Goals boundary note's agent grade visibly, tighten R-A4's provenance to what the epic actually says, fix R-A2 singular-gate wording, give SC4 a test shape in R-G1, give SC6 an evidence form (learn from the sibling audit's failure mode), fix § F numbering.

Then append a short "Resolutions" block to `spec_review.md` recording each finding → what changed (or why not). Do not commit; the orchestrator commits. End with `ARTIFACT: .project/active/goal-integration-seam/spec.md`.
