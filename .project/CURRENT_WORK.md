# Current Work

**Last Updated**: 2026-06-06

---

## Active Work

### Explorer Identity & Shared Spine — Theme A (implementation complete)

**Status**: All 4 phases complete (A1 identity + A3 caveat + A2 palette/facets); awaiting `/_my_audit_implementation`
**Location**: `.project/active/explorer-identity-spine/`
**Branch**: `feat/concept-explorer-omit-list`

Cross-cutting "spine" for the EXPLORER-UX-V3 Phase 2+ vision (blocks B1 matrix + C1 constellation). Three single-source-of-truth conversions: A1 canonical `Name (Fuel)` + visible `#code`, A2 ontology palette/facet model, A3 one honest-caveat device.

- **Phase 1 done (2026-06-06)**: `resolve_identity()` in `server.py` is the single identity authority (CSV-backed registry), stamped onto both served `ConceptData` and the taxonomy registry at load. De-risk audit: 35/36 served names clean; concept 35 (`PoloMac`, D-D) composes its suffix from the structured fuel (**Option 1**, user-confirmed). 14 new tests in `tests/test_identity.py`; no regressions.
- **Phase 2 done (2026-06-06)**: `static/js/concept_label.js` (`window.conceptLabel`) is the one front-end naming helper; every spec-enumerated surface renders `#code Name (Fuel)` through it (cards, hero/breadcrumb/sticky/title, compare chips/picker/placeholder/landscape, constellation hover, taxonomy card + neighbor tables, parameter links). 19 grep-guard tests; browser-verified clean (composed `#35 … (D-D)` and `#17a`/`#20b` suffix variants all live).
- **Phase 3 done (2026-06-07)**: A3 honest-caveat. `static/js/caveat_marker.js` (`window.caveatMarker`) is the one caveat device; `fit_grade` loaded from `tables/archetype_fit.csv` and stamped onto ConceptData + manifest. 5 duplicated low-grounding markers consolidated (now also flag archetype-fit "None"); honest "not recorded" variant wired. 18 tests; browser-verified.
- **Phase 4 done (2026-06-07)**: A2 palette/facets. `static/css/explorer.css` `:root` gains `--onto-*` dimension tokens (traceable to the PNG generator `phase_1a/generate_ontology_chart.py`); `static/js/ontology_palette.js` reads them via getComputedStyle (CSS = single authority, zero JS hex), exporting `ontologyPalette` / `facetModel` (10 facets) / `filterState`. 5 duplicated `FAMILY_COLORS` dicts deleted + re-sourced. Zero visual change verified. 14 tests.
- **Done**: all of Theme A. Next is `/_my_audit_implementation` then `/_my_wrap_up`. Total new tests across the 4 phases: 65 (test_identity 14 + test_identity_frontend 19 + test_caveat 18 + test_palette 14); suite 292 green (excl. pre-existing manual/adapter).
- **Theme A unblocks** B1 (ontology matrix) and C1 (constellation rebrand), which import `conceptLabel`, `caveatMarker`, `ontologyPalette`, `facetModel`, `filterState`.

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
