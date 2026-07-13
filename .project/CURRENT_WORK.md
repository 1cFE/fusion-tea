# Current Work

**Last Updated**: 2026-06-28

---

## Active Work

### EXPLORER-UX-V3 — Phase 1 verified; migration complete; pick next Phase-2 item

**Status**: Phase 1 + Themes A/B1/F all merged to `main`; 1costingfe v0.1.0 migration complete and Phase 1 re-verified. **Next: pick the next Phase-2 item by leverage (top candidate D1).**
**Epic**: `.project/backlog/epic_explorer_ux_v3.md` (see its "Post-merge status" + "1costingfe v0.1.0 migration" sections)

What's merged:
- **Phase 1** — Item 1 (slider/tornado/headline coherence), Item 2 (override-inspection surface), FU1 (CAS header hint). Override-overlay UX = PR #52; built on rework infra #44.
- **Theme A** — identity & shared spine. PR #58. **Theme B1** — ontology matrix home page. PR #59. **Theme F1** — cost landscape page. PR #64.

**1costingfe v0.1.0 migration (2026-06-28) — done.** Library on `1costingfe@0254385`; all explorer data regenerated (Option A: re-enable the gated solvers from the fusion-tea side). FR-SO1 holds for 33/33 served concepts; tests 19/20. The "concept 01 override moves the headline only 1.26%" scare is **resolved and benign** — the override behaves as designed; the recalibration raised the bare baseline under a frozen-by-design override (~19% at native scale, ~1.26% at the 1 GWe headline). Nothing broke. Full writeup: `reports/2026-06-28_1costingfe-v0.1.0-migration.md`.

**Small non-blocking loose ends**: concept 27 stale data (routing-config fix); FR-SO1 test's stale `>5%` assertion; Item 2-FU (re-extract 37 & 39); spike/override-policy doc cleanup.

**Unbuilt Phase-2 candidates** (pick by leverage): **D1** (per-account override decomposition — top candidate), C1 (Design Space Viz rebrand), C2 (comparables entry), B2/B3, D2/D3, E1–E3.

### Explorer Web Hosting — separate deployment track (in progress)

**Status**: On `feat/explorer-web-hosting` (current branch). Not epic work.
**Location**: `.project/active/explorer-web-hosting/` (spec/design/plan/RUNBOOK)

Railway container deployment of the concept_explorer: slim serving manifest (`requirements-serve.txt`), `Dockerfile` + `railway.toml`, `scripts/smoke_explorer.py`, operator runbook. Plus a separate static "score explorer" published from `docs/` with a CNAME. 5 commits ahead of `main`.

### Compute OOM — debounce + cache quantization (implemented, ready to PR)

**Status**: Implemented on `feat/compute-oom-debounce-quantize` (off `feat/explorer-web-hosting`). PR back into the hosting branch to trigger the Railway rebuild.
**Location**: `.project/active/compute-oom-debounce-and-quantize/` (spec + design w/ impl notes)

Fixes the Railway OOM-kill under multi-user slider load. Layer 1 (client): `tornado.js` debounce 200→400ms + `AbortController` in `concept_page.js:onSliderChange` (at most one in-flight compute/client; abort detected via `controller.signal.aborted`, indicator-hide guarded against superseded requests). Layer 2 (server): `_quantize_sig` rounds override floats to 4 sig figs before the `_compute_cached` LRU key so nearby slider positions share a `forward()`. Verified: 15/15 compute tests, parity gate 33/33 @1e-5, browser drag (6 events→1 request, headline updates, no error flash, 0 console errors). FR-SO1 untouched (no-op path sends empty overrides → nothing to quantize). Out of scope: `forward()` semaphore.

### Compute OOM — Layer 3 forward() semaphore (implemented, ready to PR)

**Status**: Implemented on `feat/compute-concurrency-semaphore` (off `main`). PR into `main`.
**Location**: `.project/active/compute-concurrency-semaphore/` (spec + design w/ impl notes)

Caps peak transient memory (Layer 3, complements debounce+quantize). Adds module-level `_MAX_CONCURRENT_FORWARD = 2` + `threading.Semaphore` in `server.py`; wraps only the `_forward_with_overrides` call inside `_compute_cached` in acquire/try-finally/release. Bounds concurrent JAX allocation to 2×per-forward regardless of user count; cache hits bypass it (`@lru_cache` returns before the body). No nesting with `_MODULE_LOAD_LOCK` (module load releases its lock before the semaphore is acquired) → deadlock-free. Verified: 21/21 previously-passing tests in `test_state_and_compute.py` + `test_slider_override_semantics.py` still pass. 1 pre-existing failure (`test_fr_so1_noop_compute_matches_stored_headline`, override-magnitude data drift) confirmed identical on base `bd4c403d` — not from this change. Parity gate + Railway multi-tab smoke deferred to deploy.

### Batch Pipeline Run (unblocked, not started)

**Status**: Plan drafted, ready to start
**Location**: `.project/active/batch-pipeline-run/`

Run all concepts through the now-hardened pipeline to approval. Unblocked by the 2026-04-11 pipeline-hardening archival.

### Concept Explorer (merged)

**Status**: Merged and functional
**Location**: `exploration/concept_explorer/`

4-page interactive explorer (Index, Concept Profile, Comparison, Taxonomy) with FastAPI backend. Extracts data from pipeline artifacts. 140+ tests. See `exploration/concept_explorer/README.md`. The `explorer-merge` work item was archived 2026-04-11.

## Paused / Deferred

- **`traceability-system`** — Spec + plan written, on hold awaiting prioritization.
- **`loop-dry-run-symmetry`** — Spec only (2026-04-10). Small follow-up from pipeline-hardening audit. LOW complexity.

---

## Recently Completed

### [2026-04-11] Pipeline Hardening, Explorer Merge, Source Cleanup

Archived 7 items + cleaned up 2 superseded/orphan dirs. See `.project/completed/CHANGELOG.md` for details.

Key outcomes:
- Analysis pipeline hardened against silent corruption, transient API errors, and validation gaps (`pipeline-hardening`, `output-validation-retry`)
- Feedback routing now reaches model-setup agent directly instead of via analysis prose (`feedback-routing-fix`)
- Cross-concept landscape context injected into analysis prompts (`concept-landscape-context`)
- 21 NO-verdict `.orig.md` files re-sourced against real HTML (`orig-md-research`)
- `ralph/concept-explorer` merged into `design-space-explore` (`explorer-merge`)
- `source-replacement` closed out
- Deleted: `extraction-interface-gap/` (empty orphan), `step-runner-validation-retry/` (superseded by pipeline-hardening Phase 5)
- Also picked up a lingering prior-session archival of `common-output-interface/` (staged to `completed/20260407_*` but never committed)

### [2026-04-05] Analysis Pipeline Bulk Archival

Archived 13 completed items. See `.project/completed/CHANGELOG.md` for full details.

### [2026-03-29] Concept Taxonomy & Interactive Explorer
4 work items archived (2 complete, 2 superseded).

### [2026-03-06] Project Cleanup

Archived 9 active items and 4 epics.

---

## Up Next

1. Knock out `loop-dry-run-symmetry` (small, well-scoped)
2. Kick off `batch-pipeline-run` on all concepts
3. Traceability system implementation (when prioritized)
