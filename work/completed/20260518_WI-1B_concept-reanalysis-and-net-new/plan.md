# WI-1B Plan

Spec: [spec.md](spec.md). Phased; **🔒 gate before each LLM-expensive phase**.
No git commit (work locally). LLM spend bounded by approved params.

## Phase A — Prep (cheap, mostly non-LLM) — needs approval to start
- [ ] Confirm costingfe-vs-freeform mapping for the 5 (freeform → blocked by
      missing tea-models exemplar; decide: skip cost-model / provide exemplar /
      env-point `FREEFORM_EXEMPLAR_PATH`).
- [ ] Add `table.csv` rows for 37/38/39 (taxonomy cols: family/topology/fuel/
      magnet/driver…), confidence-tagged. Verify selfcheck/loader → 39.
- [ ] Create Phase-1a dossiers: 37/38/39 (new); 17/27 (split — distinct, not
      shared-seed). Seed `knowledge/concept_research/{rid}/iter-01/sources/`.
- [ ] Decide research mode (see gate).

## Phase B — Split-reanalyze 17 & 27 (LLM) — 🔒 gate
- [ ] `run_analysis.py analyze 17 27 --force` (clears shared-seed iters; cold
      start on differentiated dossiers) with approved model/max-passes/research.
- [ ] review → synthesize. Verify distinct dossiers (R3).
- Smaller/cheaper than net-new; validates paths + pipeline end-to-end first.

## Phase C — Net-new 37/38/39 (LLM, research-heavy) — 🔒 gate
- [ ] Source research per concept (NearStar MTIF / SHINE / ENN p-B11 ST),
      MR-4-cited. `run_analysis.py analyze 37 38 39` with approved params.
- [ ] review → synthesize.

## Phase D — Integrate to 39 & verify (mostly mechanical)
- [ ] `extract.py --bulk-taxonomy` + `--bulk-cost-model`; regenerate
      scoring_v2 scores; seed_registry; SOURCE_INDEX --reindex.
- [ ] Add 37/38/39 to scoring.py `_C2`/`_HERITAGE` maps (manual — they encode
      category/lineage; not derivable mechanically).
- [ ] Extend renumber `verify` expected set to 39; run; broadened sweep clean.
- [ ] Update memory + work-item status.

## Outcome (2026-05-19) — COMPLETE, local/uncommitted

renumber `verify` **5/5 PASS @ 39**. analyses/features/table/scores = 39.

| id | result | LCOE | assess |
|---|---|---|---|
| 17 Focused Energy | split-reanalyzed | 309.8 | PASS |
| 27 Xcimer | split-reanalyzed | 197.4 | PASS |
| 39 ENN p-B11 ST | net-new, sourced (arXiv 2401.11338) | 50.8 | PASS (iter2) |
| 38 SHINE | net-new, sourced | **inf** (honest: not a power plant) | PASS |
| 37 NearStar MTIF | net-new, sourced | 60.0 (baseline) | **did not converge** |

Curated sources written directly to `concept_research/{37,38,39}/iter-01/sources/`
(agentic-mbse `extract` version mismatch — `--save-source` unsupported — bypassed).
Phase D: features regenerated (39; 28 w/ cost models), 37/38/39 added to
`scoring.py` `_C2_CONCEPT_MAP`/`_HERITAGE_MAP`, scores + seed_registry regenerated,
broadened verify extended to count `new` and run green.

**Known debt:** 37 non-convergence (under-specified early-stage); 38 inf-LCOE
(WS-2 scoring must handle non-finite); explorer `concept_registry.json`=38 (LLM
`extract_explorer_data` for 37/38/39 deferred). Env fixes uncommitted; pipeline
requires `PYTHONUTF8=1` on Windows.

## Out of scope / deferred
- Workstream-2 modularity A–E (separate, runs now that corpus = 39).
- Explorer per-concept LLM extraction for 37/38/39 (deferred).
- Rewriting `iter-*/` history, phase_1a legacy, add_ids.py.
