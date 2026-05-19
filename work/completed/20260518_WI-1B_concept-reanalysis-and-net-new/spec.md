---
Status: complete
Scale: standard
Epic: "Stage-1-Taxonomy / concept-downselect"
Owner: mallory
Created: 2026-05-18
Updated: 2026-05-18
---

# WI-1B — Workstream-1B: split-reanalysis + 3 net-new concepts

Modeling-PM work item (per CLAUDE.md MBSE workflow). Brings the renumbered
36-concept corpus to the full **39** by producing source-traced research +
analysis + cost model for 5 concepts. Prerequisite: Workstream-1 renumber
(applied locally, verified). Driven by `scripts/renumber/reanalyze.txt`.

## Targets (5)

| new id | concept | company | kind |
|---|---|---|---|
| 17-laser-icf-direct-drive-fast-ignition | Direct-Drive Fast Ignition | Focused Energy | **split-reanalyze** (was shared 17 dossier) |
| 27-laser-icf-hybrid-direct-drive | Hybrid Direct Drive | Xcimer Energy | **split-reanalyze** (was shared 17 dossier) |
| 37-magnetized-target-inertial-fusion | MTIF | NearStar Fusion | **net-new** |
| 38-accelerator-driven-fusion | Particle Accelerator-Driven | SHINE Technologies | **net-new** |
| 39-cs-free-spherical-tokamak-pb11 | CS-free p-B11 Spherical Tokamak | ENN Energy | **net-new** |

## Requirements

- **R1** Each target ends with: a `table.csv` row (taxonomy columns), a Phase-1a
  dossier, ≥1 source-traced research source, `analyses/{id}/` (analysis.md,
  model_setup.py, model_output.txt, synthesis.md), and a regenerated
  `features/{id}.yaml`. Corpus loads as 39 via `run_analysis.py status`.
- **R2** All quantitative values carry MR-4 citations (Source/Ref/Basis).
- **R3** Split targets (17, 27) must be **differentiated** — distinct dossiers
  and sources, not the shared-seed copy. Xcimer (e-beam KrF excimer) vs Focused
  Energy (DPSSL + proton fast ignition) are architecturally distinct.
- **R4** Net-new (37/38/39) require genuine domain research (NearStar MTIF;
  SHINE accelerator/spallation-driven; ENN CS-free p-B11 ST) — real sources,
  not fabricated. Honest low-confidence where undisclosed.
- **R5** Integrate into all Workstream-1 cascade surfaces (table.csv,
  features, scoring.py `_C2`/`_HERITAGE` maps, explorer, SOURCE_INDEX) and
  re-run the renumber `verify` (now expecting 39).
- **R6** No git commit (user: work locally). LLM spend is bounded by approved
  parameters (model, max-passes, --research on/off).

## Known blockers / risks (must be acknowledged at gate)

- **Cost-model paths**: `COSTINGFE_DIR` fixed (local clone). `FREEFORM_EXEMPLAR_PATH`
  (tea-models) NOT available → any **freeform-mapped** target fails the
  cost-model step. Need to confirm which of the 5 map costingfe vs freeform.
- **Cost/scale**: pipeline map estimates ~1–2M tokens / ~$3–5 / long runtime
  per concept for 3–5 analyze↔assess↔model iterations; `--research` adds
  web-search + extraction passes. 5 concepts = multi-hour autonomous spend.
- **`claude -p` autonomy**: the loop calls Claude as a subprocess; this is an
  autonomous, web-touching, long-running operation requiring explicit go.
- **No Phase-1a dossiers** for the 5 (net-new have none; split share old 17).
- **MR-4 research judgment**: net-new sourcing is genuine research, not
  mechanical — quality bar, not just runtime.

## Acceptance

- [ ] 5 targets analyzed, cost-modeled (or freeform-gap flagged), feature-extracted.
- [ ] Corpus = 39; `run_analysis.py status` clean; renumber `verify` green @ 39.
- [ ] MR-4 citations present; low-confidence honestly tagged.
- [ ] Split 17/27 dossiers demonstrably distinct.
