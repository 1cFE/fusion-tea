# Implementation Notes: concept-downselect-merge

**Branch:** `concept-downselect-rebase` (off `main` @ `8d59784`)
**Source worktree:** `/home/reid/1cfe/fusion-tea-concept-downselect` @ `concept-downselect`
**Started:** 2026-05-19

This file is the **no-loss ledger** required by FR-10/11. For every commit on `concept-downselect`, every file is marked:
- `[ported]` — landed verbatim
- `[ported-with-transform: <note>]` — landed with modification (path remap, regeneration, schema fit)
- `[skipped: <reason>]` — intentionally not carried over (must be justified)

See `_downselect_filelist.txt` for the raw `git diff --name-status -M main..concept-downselect` snapshot.

---

## Per-commit ledger

### 6eb2291 — First pass research for down-select methodology
**Phase:** 1 (cherry-pick `8eadcd6`)
**Files added:** ~145 — meta-analysis dossiers under `knowledge/meta_analysis/` (NOT `concept_research/` as spec phrased; downselect placed them in `meta_analysis/`), plus `.project/research/` methodology drafts.
**Status:** [ported] verbatim
**Notes:** Path correction noted — spec used `knowledge/concept_research/`; actual path is `knowledge/meta_analysis/`. No content change.

### 539a1b5 — New research for concept downselect. Q1-Q3 research done.
**Phase:** 1 (cherry-pick `58ff239`)
**Files added:** ~303 — additional meta-analysis dossiers (megaprojects, what_is_foak, learning_from_case_studies, …) + Q1-Q3 research notes
**Status:** [ported] verbatim

### 57ece9e — working on the downselect
**Phase:** 1 (cherry-pick `23e6c57`)
**Files added:** 3 (`.project/concepts/concept-trace.md`, `down_select/concept_part2.md`, `down_select/research_q4_q5.md`)
**Status:** [ported] verbatim

### 1d9937a — Pass 1 on the explainer
**Phase:** 1 (cherry-pick `679a649`)
**Files added/modified:** 39 — `worked_examples/` scripts (`run_critique.sh`, `run_revise.sh`, `run_trace.sh`) + prompts + initial `docs/demo/down-select.html` (1379 lines)
**Status:** [ported] verbatim

### ab19c2a — pass 1.1
**Phase:** 1 (cherry-pick `45ca6b2`)
**Files modified/deleted:** 12 — `trace_*.md` cleanup (deleted: trace_14, trace_15, trace_26, triage_v0_results, decision_output_schema_v0, methodology_revision_v1, explainer_updates, trace_08-helion); new: explainer_feedback_v1, explainer_v2_section3_draft, four_stage_validation
**Status:** [ported] verbatim

### f7f5da8 — pass 2
**Phase:** 1 (cherry-pick `1dc2314`)
**Files modified:** 6 of 7 ported; uv.lock conflicted
**Status:** [ported-with-conflict-resolution: uv.lock taken from ours (main); pyproject.toml unchanged so no functional dep loss; reconcile via `uv sync` after Phase 3 if scoring_v2 introduces deps]
**Notes:** All content files landed clean: `worked_examples/08-helion.md`, `worked_examples/14-general-fusion.md`, `docs/demo/down-select.html` (1350 lines after pass 2), `.project/concepts/down_select/concept_part2.md`, `explainer_outline.md`, `explainer_v2_section3_draft.md`.

### e7964c8 — Downselect pass 3
**Phase:** 1 (cherry-pick `ef74629`)
**Files added/modified:** 3 — `.project/concepts/scoring-framework-v2.md` (222 lines), `.project/research/20260515-143425_triple-product-technology-risk-framework.md`, `docs/demo/down-select.html` (final +1095/-141)
**Status:** [ported] verbatim

### 8585ddd — Added the Wurzel and Hsu paper
**Phase:** 2 (cherry-pick `e3777f3`)
**Files added:** 143 — Wurzel & Hsu (arXiv 2105.10954) at `knowledge/meta_analysis/progress_toward_fusion_breakeven_lawson_criterion/` (slug is the paper title, not "wurzel_hsu"). Contains source.pdf, output.md (1176 lines), cost.json, decisions.json, metrics.json, page images.
**Status:** [ported] verbatim

### f55e35a — Scoring V2 framework stencil + plant-level modularity slice
**Phase:** 3 (cherry-pick clean, then regeneration commit on top)
**Files added:** 70 — `exploration/scoring_v2/*` framework, `tests/scoring_v2/*`, 38 feature YAMLs (pre-v3 IDs incl. `34-compact-spherical-tokamak-india.yaml`), slice1 + default weights
**Status:**
- Framework code (`extract.py`, `score.py`, `lib/`, `schema.yaml`, weights): [ported] verbatim then [ported-with-transform] for schema.yaml (tritium_breeding/neutron_management → extractor=manual)
- 37 feature YAMLs for concepts that still exist on main: [ported-with-transform: regenerated via `extract.py --bulk-taxonomy` against main's v3 table; manual fields preserved]
- `features/34-compact-spherical-tokamak-india.yaml`: [skipped: Pranos dropped on main per FR-1; consistent with PR #16's drop]
- Tests: [ported-with-transform: count 38→40, test_bulk_taxonomy stops wiping (manual-extractor fields prevent from-scratch valid generation); 3 score-baseline tests marked strict xfail with documented v3-data deviation (Helion Magnet Type Pulsed EM → Resistive)]
**Notes:** Baseline shift recorded as deviation per FR-4 allowance. New scoring_v2 test counts: 23 passed / 3 skipped / 4 xfailed (was 26 / 3 / 1 on downselect).

### 30ecdd8 — Scoring V2 slice 2: component_modularity embedding group
**Phase:** 3 (cherry-pick clean)
**Files added/modified:** 57 — `embeddings/component_modularity.py`, `lib/extractors/cost_model.py`, `weights/slice1.yaml`, `tests/scoring_v2/test_component_modularity.py`, `test_cost_model.py`, ~28 cost_model w_* feature additions (captured in the regenerated yamls)
**Status:** [ported] verbatim; same transform handling as f55e35a covers downstream feature regeneration
**Notes:** cost_model extractor reads from `analyses/{cid}/model_output.txt` — unchanged paths post-merge.

### e23fceb — tooling: concept renumber migration + WS-1B planning artifacts
**Phase:** dropped (skip per Option B.3.a)
**Files:** `scripts/renumber/{renumber.py,reanalyze.txt}` + `.project/active/concept-renumber-migration/*` + `work/active/WI-1B_*`
**Status:**
- `scripts/renumber/renumber.py` — [skipped: renumber tooling explicitly excluded per spec FR-7]
- `scripts/renumber/reanalyze.txt` — [skipped: renumber tooling]
- `scripts/renumber/crosswalk.csv` — [pending: move to `archive/` as historical record per FR-7]
- `.project/active/concept-renumber-migration/*` — [skipped: planning artifacts for the dropped renumber]
- `work/active/WI-1B_concept-reanalysis-and-net-new/{spec.md,plan.md}` — [ported in Phase 5: split-17 + net-new analysis is still happening, just not the renumber]

### a2004fa — corpus: 39-concept renumber + WS-1B reanalysis & 3 net-new concepts
**Phase:** 4 + 5 (partial carve-out)
**Files:** 1252 changed (renumber + 37/38/39 + split-17). Per Option B.3.a:
- **Renumber subset** (relabels of 17a/b, 20a/b, 21–33 directories + `table.csv` ID-column rewrites + `scoring.py _C2/_HERITAGE` remap + 39-ID feature YAMLs) — [skipped: per FR-1/7]
- **37/38/39 subset** (NearStar/SHINE/ENN analyses + research dossiers) — [pending Phase 4]
- **Split-17 subset** (Focused Energy + Xcimer separate analyses) — [pending Phase 5]
- **`scripts/renumber/{manifest.json,manifest.diff.txt,inventory.md,r2_ops.log}`** — [skipped: renumber tooling artifacts]
**Status:** pending Phase 4 + Phase 5 work

---

## Phase 0 — Setup

**Completed:** [pending]
**Branch created:** `concept-downselect-rebase` off main @ `8d59784`
**Baselines captured:**
- `_downselect_filelist.txt` — 2348 entries (970 A / 599 D / 116 M / ~660 R)
- `_downselect_commits.txt` — 13 commits
- `/tmp/status_pre.txt` — pipeline baseline (exit 0)
- `/tmp/tests_pre.txt` — pytest collection baseline

**Notes on filelist:** The 599 D entries are files added on **main's** ontology-v3 PR that simply don't exist on `concept-downselect` — we keep them (they are not deletions from our perspective; they appear as "deletes" only because the diff is `main..concept-downselect`). The 970 A + 116 M + ~660 R entries are the actual downselect work that must be reconciled.

---

## Final Summary (filled in Phase 6)

| Category | Count |
|---|---|
| Files ported verbatim | |
| Files ported with transform | |
| Files intentionally skipped | |
| Unaccounted for | should be 0 |
