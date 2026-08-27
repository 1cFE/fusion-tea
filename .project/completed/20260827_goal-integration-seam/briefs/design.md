# Stage brief: design — GSTH Item 3 (Verified Package Integration Seam)

**From**: orchestrator (`/_my_orchestrate`), 2026-08-26. Item home: `.project/active/goal-integration-seam/`.

## Inputs

- **Spec (the contract)**: `spec.md` — revised through spec_review; read it whole. The review and resolutions: `spec_review.md`. Lens ledger: `product-lens.md`. Align rulings: `align.md`.
- Referents: `work/completed/20260822_WI-030_computed-beta-peak-field/plan.md` (most recent full-sequence run), `.project/completed/20260821_stellarator-model-migration/plan.md` Phases 2–3, `.project/active/run-study-first-consumer/plan.md` Phase 3.
- Producers: `scripts/study/manifest.py`, `preflight.py`, `verify.py`, `identity.py`; `tests/models/test_model_family_spines.py`; `tests/test_dependency_provenance.py`.
- Sibling design precedent: `.project/active/goal-research-seam/design.md` (Item 2 — same seam family; its audit findings and fix pass are instructive, especially hermetic test paths and operator-guide accuracy).

## Orchestrator rulings you inherit (recorded `[AGENT]`, committed `55a32ca8`)

1. **Baseline execution inside the seam is accepted** (spec Non-Goals boundary note / L2-1): executing the baseline point and gate-required probe runs is the seam's business; a study is not. WI-030 precedent `plan.md:194`.
2. **One shared entry surface** (L2-2): human and goal agent reach the same entry point; no distinct second operator surface in the first build. Design chooses its shape (CLI script in `scripts/` per sibling precedent is the natural answer, but that's yours to decide and record).
3. Standing spec deferrals are yours to settle and record: return-artifact format/home, SC1 fixture strategy, blocker-taxonomy detection per producer (R-A6; `preflight.py:368-377` is the native shape to match), rollback-vs-ordering for R-C8, what the seam runs verification against (within ruling 1), teax expected-revision source (R-B1.1b: caller-supplied vs seam-recorded).

## Spike finding (regeneration in-place determinism, R-D4)

**CONFIRMED** (spike `spike_regen_determinism.md`, committed): the pinned `generate --smart-regen --preserve-handwritten` run in place on the sealed package changes zero bytes across two runs; both fingerprints hold (semantic `1ca93d0c…`, executable `7447efea…`); runtime ~1.8s. Consequences for design: R-B4 needs no regeneration exemption — re-running the full sequence is idempotent and R-D1's same-identity CANDIDATE is the unchanged-inputs path. `--preserve-handwritten` never opens the 58 handwritten files; the 95 generated files rewrite byte-identically but their mtimes move — do not build any mtime-based change detection. `SYSIDE_LICENSE_KEY` unset is a could-not-run (R-A6) precondition at the generate gate; `STOP_PARSER_TEAX_ROOT` is not needed at generate, only downstream. Claim scope: this package, this pin — a codegen bump is R-B1.1a's business.

## Design expectations

- Architecture true to the spec's grain: a fusion-tea-side orchestrating caller over the eight gates in R-B1 order, stopping at first refusal at producer grain, emitting one CANDIDATE/BLOCKER return. No producer edits (R-B2), no hardening-path machinery (R-F2).
- Decide and record every open question as a numbered design decision with rationale and provenance grade; if evidence is thin, say so rather than hedge.
- Test design per R-G1–G4 and SC-shapes: success path, real-producer gate failure, re-run identity stability, SC4 stock-route hand-off (R-G1a), hermeticity (R-G3 — learn from Item 2's F3).
- File any decisions of record as ADRs in `.project/adr/` (Item 1's home; ADR-008 was Item 2's precedent).
- Plan for the ~8h execute estimate; if your design clearly exceeds it, say so with the driver rather than thinning quality silently.

Write `design.md` at the item home. End with `ARTIFACT: <path>`.
