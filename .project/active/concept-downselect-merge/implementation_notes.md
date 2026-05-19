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
**Phase:** 1
**Files added:** ~145 (research dossiers under `knowledge/concept_research/`, methodology drafts under `.project/research/`)
**Status:** pending
**Notes:**

### 539a1b5 — New research for concept downselect. Q1-Q3 research done.
**Phase:** 1
**Files added:** ~303
**Status:** pending
**Notes:**

### 57ece9e — working on the downselect
**Phase:** 1
**Files added:** 3 (`.project/concepts/concept-trace.md`, `down_select/concept_part2.md`, `down_select/research_q4_q5.md`)
**Status:** pending
**Notes:**

### 1d9937a — Pass 1 on the explainer
**Phase:** 1
**Files added/modified:** 39 (worked_examples scripts/md, `docs/demo/down-select.html`)
**Status:** pending
**Notes:**

### ab19c2a — pass 1.1
**Phase:** 1
**Files modified/deleted:** 12 (trace/triage cleanup)
**Status:** pending
**Notes:**

### f7f5da8 — pass 2
**Phase:** 1
**Files modified:** 7 (worked_examples expansions; `docs/demo/down-select.html`; `uv.lock`)
**Status:** pending
**Notes:**

### e7964c8 — Downselect pass 3
**Phase:** 1
**Files modified/added:** 3 (`scoring-framework-v2.md`, triple-product risk research, `down-select.html`)
**Status:** pending
**Notes:**

### 8585ddd — Added the Wurzel and Hsu paper
**Phase:** 2
**Files added:** 143 (Wurzel/Hsu PDF + extraction outputs under `knowledge/concept_research/`)
**Status:** pending
**Notes:**

### f55e35a — Scoring V2 framework stencil + plant-level modularity slice
**Phase:** 3
**Files added:** 70 (`exploration/scoring_v2/*`, `tests/scoring_v2/*`, 38 feature YAMLs in old-ID scheme, slice1 weights)
**Status:** pending — feature YAMLs to be regenerated (transform) against main IDs
**Notes:**

### 30ecdd8 — Scoring V2 slice 2: component_modularity embedding group
**Phase:** 3
**Files added/modified:** 57 (component_modularity embedding, cost_model extractor, w_* weight features, expanded tests)
**Status:** pending — feature regeneration covers most; cost_model extractor copied as-is
**Notes:**

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
