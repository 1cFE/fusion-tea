# Spec — Scoring Framework v3 Rewrite (7 Peer Axes + Composite + UI)

**Status:** Draft — P0 prereqs in flight
**Owner:** Mallory
**Created:** 2026-05-20
**Scale:** Standard (multi-PR, ~13-16 person-days)
**Branch root:** `main` @ `7b5e8a9`; each phase PRs off main as `feat/...` or `prep/...`

## Purpose

Replace the existing 3-dimension scoring framework (`economic_potential`,
`technical_feasibility`, `manufacturability_scale_out`) in `exploration/scoring_v2/`
with a peer-axis model: **7 independent axes** (Modularity, Supply Chain, Plant
Complexity, Customization, Upper Capacity Factor, Technical Feasibility, Data
Availability) plus a **weighted-average composite**. Replace the existing
modularity implementation with the **v5 three-component formula**. Build a
**Weight Explorer UI** for interactive axis-weight adjustment.

Sources of truth (uploaded 2026-05-20):
- `integrated_implementation_plan.md` — orchestration map
- `modularity_implementation_spec.md` + `modularity_matrix_v5.md` *(pending upload)*
- `supply_chain_implementation_spec.md`
- `plant_complexity_scoring_plan.md` *(needs conversion to impl-spec format — P0)*
- `customization_implementation_spec.md`
- `upper_cf_implementation_spec.md`
- `technical_feasibility_implementation_spec.md`
- `data_availability_implementation_spec.md`

## In scope

1. Collapse 3 dimensions → 7 peer axes in `score.py`, `weights/default.yaml`,
   `scores/table.csv`.
2. Schema reconciliation against v0.3.0 ontology: +7 features, retire 2 orphans.
3. Replace modularity with v5 formula: delete 12 old embeddings + 4 retired
   capex shares; add 6 new embeddings + 1 manual feature (`unit_count_estimate`).
4. Build 6 new axis scorers (Supply Chain, Plant Complexity, Customization,
   Upper CF, Technical Feasibility, Data Availability) following the same
   penalty-stack / lookup-table pattern.
5. Composite with null-axis-skip + weight rescaling.
6. Score Explorer UI under `tools/score_explorer/` (single-page HTML+React).
7. Cross-axis calibration review and within-axis weight tuning.

## Out of scope

- Modeling-pipeline changes (analyses/, concept_research/, gap_check pipeline).
  The scoring framework consumes the outputs but does not modify them.
- Adding new concepts beyond the current 40 (Pranos already dropped, 37–39
  already on main).
- Modifying the v0.3.0 ontology (`schema.md`) — the 7 added features either
  already exist there or are derived/manual.
- R2 reconciliation (carryover from earlier renumber work).
- Windows env-fixes (`paths.py`, `cost_model.py` utf-8) — orthogonal local-only
  modifications.

## Requirements

- **R1** All 7 axis scores deterministic, in `[1.0, 5.0]` ∪ `{null}`, byte-identical
  reruns on unchanged inputs.
- **R2** Composite uses weighted average, skipping null axes and rescaling
  remaining weights; CSV records `composite_axes_included` per concept.
- **R3** Each axis's per-concept scores match its companion spec's predicted-scores
  table within rounding tolerance (the **calibration target**).
- **R4** `tests/scoring_v2/predicted_scores.yaml` is the single source of truth
  for per-axis predicted scores; `test_spec_conformance.py` parameterizes over it.
- **R5** Determinism + no-LLM invariants preserved for axes 1–6;
  Data Availability is the documented framework exception (reads
  `gap_report.md` from the analysis pipeline).
- **R6** Every concept's feature file contains all 7 `{axis}_diagnostics`
  blocks, each matching its spec's mandated structure.
- **R7** UI loads all 40 concepts ranked, client-side re-rank in <100 ms on
  axis-weight slider change, "save & re-score" round-trip in <5 s.
- **R8** Cross-axis sanity: no concept scores 5.0 (or 1.0) on every axis;
  per-axis score distribution non-degenerate (≥3 distinct values across 40).
- **R9** Composite null handling honest: concepts with all-null axes get null
  composite (not 0, not floor); UI distinguishes null from low.
- **R10** Schema fail-loud: missing required feature or unknown enum value
  raises rather than silently defaulting.

## Acceptance bar

- 8 PRs (P0–P7) land on main; each axis spec's predicted scores reproduced.
- `test_spec_conformance.py` (10 conformance test classes) passes.
- `score.py` produces 40-row CSV with 7 axis cols + composite + 7 evidence cols
  + composite_axes_included.
- UI ranks 40 concepts, slider response <100 ms, save-and-re-score <5 s.
- Cross-axis sanity (R8) holds.

## Prereqs (P0)

1. Grep audit of old dimension column names (`economic_potential`,
   `technical_feasibility`, `manufacturability_scale_out`) — identify
   downstream breakage in `.project/`, `tools/`, scripts.
2. Convert `plant_complexity_scoring_plan.md` to impl-spec format matching
   the other six axis specs.
3. Consolidate per-axis predicted scores from 6 specs into
   `tests/scoring_v2/predicted_scores.yaml` (Modularity column pending v5 matrix).
4. **NOT in P0**: gap-report format standardization (deferred to P5 per
   2026-05-20 decision).
5. **Pending upload**: `modularity_matrix_v5.md` — required to populate
   modularity predicted scores for all 40 concepts.

## Risks

| # | Risk | Mitigation |
|---|---|---|
| 1 | Dimension column removal breaks downstream consumers | P0 grep audit; address before P2 lands |
| 2 | Slice 1b destructive replacement (12 → 6 embeddings) | Test-driven: v5 acceptance tests authored first, refactor until green |
| 3 | Cross-axis calibration drift after week-1 work | Slice 9 review + within-axis weight retuning |
| 4 | Spec drift from v5 matrix vs. v3 ontology (renumbering) | `predicted_scores.yaml` keys on v3 IDs; v5 matrix's old IDs translated per spec's mapping table |
| 5 | Data Availability null-handling UX | UI explicitly marks "null" vs "low"; composite formula skips nulls |
| 6 | Gap-report format inconsistency (deferred to P5) | Document interim behavior; Data Availability scores marked unreliable until P5 standardization lands |

## Open decisions

| Decision | Resolution (2026-05-20) |
|---|---|
| Per-concept v5 score strictness | Strict — every of 40 concepts must reproduce v5 matrix within rounding |
| Gap-report standardization timing | Deferred to P5 (Data Availability axis ships with null scores for unconforming reports interim) |
| Branch model | Each P*N* PR off main directly; Reid's pattern |
| Plan authoring | Author work item now + start P0; defer code on scoring_v2 until P1 |
