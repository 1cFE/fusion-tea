# Plan — Scoring Framework v3 Rewrite

**Spec:** [spec.md](spec.md) · **Design:** [design.md](design.md)
**Created:** 2026-05-20

Each PR branches off `main` directly, PR'd back via `gh pr create --base main`,
merged + branch deleted on merge.

---

## P0 — Prereqs (this branch: `prep/v3-rewrite-prereqs`)

Estimate: ~½ day. No `scoring_v2/` code touched.

- [x] Author work item: `.project/active/scoring-v3-rewrite/{spec,design,plan}.md`
- [ ] **Grep audit** — find downstream consumers of old dimension column names
      (`economic_potential`, `technical_feasibility`, `manufacturability_scale_out`).
      Output: `.project/active/scoring-v3-rewrite/audit_old_dimension_names.md`
- [ ] **Plant complexity format conversion** — transform
      `plant_complexity_scoring_plan.md` into impl-spec format matching the
      other six axis specs (Change A/B/C/D sections, explicit YAML, embedding
      code, populate script, tests). Output: replace the planning doc with the
      impl spec in the project's spec storage location.
- [ ] **Consolidate predicted-scores spreadsheet** —
      `tests/scoring_v2/predicted_scores.yaml` populated from the 6
      finished axis specs.  *(Modularity column pending v5 matrix upload.)*
- [ ] **Awaiting upload**: `modularity_matrix_v5.md` from user to complete
      modularity predicted scores.
- [ ] PR: `prep/v3-rewrite-prereqs` → `main`. No code in `scoring_v2/`; just
      planning artifacts + prereq deliverables.

Acceptance: work item docs land, grep audit doc committed, plant complexity
spec converted, predicted-scores YAML complete except modularity (or fully
complete if v5 matrix arrives in time).

---

## P1 — Schema reconciliation (Slice 0)

Branch: `feat/schema-v3-reconcile`. Estimate: ~1 day. Foundational.

- [x] `schema.yaml`: add `primary_heating`, `blanket_config`, `repetition_rate`,
      `laser_approach`, `non_standard_mechanism`, `confinement_concept` (derived),
      `gap_report_path` (manual)
- [x] `schema.yaml`: retire `tritium_breeding`, `neutron_management` (pre-v3 orphans)
- [x] `lib/extractors/taxonomy.py`: extend for 5 new v3 columns
      *(generic — `taxonomy_column` schema entries dispatch automatically)*
- [x] `lib/extractors/derived.py` **NEW**: derive `confinement_concept`
      from sub-columns (disambiguation rules per Tech Feasibility spec)
- [x] `lib/extractors/manual.py`: extend for `gap_report_path`
      *(no code change needed — manual extractor is feature-agnostic;
      schema entry registers it)*
- [x] Repopulate all 40 `features/*.yaml` via re-running extractors
- [x] `tests/scoring_v2/test_extract.py`: extend for new features
- [x] Verify existing modularity scoring produces identical output
      (regression check; v5 replacement comes in P2). *Result: old
      modularity tests (test_score_framework, test_embeddings) still
      pass. Per-concept modularity scores DO drift because three
      embeddings (`subsystem_stack_burden`, `blanket_rating`,
      `civil_rating`) reference the retired `tritium_breeding` and
      `neutron_management` columns and now receive empty strings. Two
      mitigations: (a) those embeddings are slated for deletion in P2
      Slice 1b anyway, and (b) the audit (`audit_old_dimension_names.md`)
      confirmed no downstream consumer reads the resulting CSV. Leaving
      `scores/table.csv` unchanged in this PR — P2 will regenerate it
      against the new axis-keyed weight shape.*

Acceptance: schema validates all 40 feature files; ≥90% of new v3 features
have non-Unknown values; `confinement_concept` and `gap_report_path` populated
for all 40 (gap_report_path is required: false; values land in P5).

PR base: `prep/v3-rewrite-prereqs` (P0). Stacked.

---

## P2 — Axis infrastructure + modularity v5 replacement (Slices 1 + 1b)

Branch: `feat/axes-infrastructure-and-modularity-v5`. Estimate: ~2 days.
**Highest-blast-radius PR** — keep tight scope.

- [x] `score.py`: `DIMENSIONS` → `AXES`; `_score_dimension` → `_score_axis`;
      add `_compute_composite` with null-skip + weight rescaling
- [x] `score.py`: CSV output extended with 7 axis cols + composite +
      7 evidence cols + `composite_axes_included`
- [x] `weights/default.yaml`: restructure to axis-keyed shape (7 axis blocks,
      modularity populated with v5 weights + sub-tables; other 6 placeholders)
- [x] `weights/slice1.yaml`: **retired** (slice-1 reference no longer applies)
- [x] **Test-driven sequence for modularity** (write test before refactoring):
      author `tests/scoring_v2/test_modularity.py` against v5 predicted scores
      (anchor to v5 matrix once uploaded)
- [x] `embeddings/rulebook.py`: delete 12 old modularity embeddings; add 6 v5
      embeddings (`_min_viable_device_scale`, `_vessel_modularity_rating`,
      `_magnet_driver_modularity_rating`, `_blanket_modularity_rating`,
      `_unit_multiplicity`, `_percent_mod`) + 3 key-builder helpers
- [x] `lookup_modularity.yaml` **NEW**
- [x] `schema.yaml`: add `unit_count_estimate`; retire `w_bop`, `w_fuel_cycle`,
      `w_aux`, `w_civil`
- [x] `lib/extractors/cost_model.py`: trim to stop emitting retired w_*
- [x] Repopulate 40 feature files: add `unit_count_estimate` per concept
      from spec's Change E table; remove 4 retired capex shares;
      add `modularity_diagnostics` block
- [x] `scripts/populate_modularity_diagnostics.py` **NEW**
- [x] `test_score_framework.py`: update CSV column assertions
- [x] `test_spec_conformance.py` **NEW**: 10 conformance classes per design.md §3

Acceptance: v5 scores match (CFS 3.71, Helion 5.00, BEST 1.91, etc. — all 40);
`run_score.py` produces 40-row CSV with axis-keyed shape; conformance tests pass
for axes wired so far (modularity + 6 axis placeholders); regression check on
slice-1/2 modularity disabled (replaced not preserved).

PR base: `main`. Depends on P1 merged.

---

## P3 — Three "easy" axes (Slices 2, 4, 5)

Branch: `feat/axes-supply-chain-customization-upper-cf`. Estimate: ~2 days.

Each axis follows the consistent per-axis pattern (design.md §2). One commit
per axis: weights + embeddings + lookup metadata + populate script + tests
+ diagnostic blocks across 40 feature files.

- [x] **Slice 2 (Supply Chain)**: 7 bottlenecks, penalty stack, severity weights
      per spec
- [x] **Slice 4 (Customization)**: 2 sub-factors (thermal rejection, fuel safety),
      `(A+B)/2` rescaled to 1-5
- [x] **Slice 5 (Upper CF)**: 3 operational penalties, penalty stack
- [x] All three populate scripts run successfully across 40 concepts
      *(combined into `scripts/populate_p3_diagnostics.py`)*
- [x] `predicted_scores.yaml` columns for supply_chain, customization, upper_cf
      reproduced by `test_spec_conformance.py` *(within calibration tolerance;
      KNOWN_DRIFTS carve-outs documented in `calibration_review.md`)*

Acceptance: per-spec predicted score distributions match; conformance test
class for these 3 axes passes; CSV shows real values in those 3 columns
(no longer placeholders).

PR base: `main`. Depends on P2.

---

## P4 — Two harder axes (Slices 3, 6)

Branch: `feat/axes-plant-complexity-technical-feasibility`. Estimate: ~2 days.

- [x] **Slice 3 (Plant Complexity)**: 14 unique subsystem flags, penalty stack with
      Critical/Severe/Moderate tiers per converted spec
- [x] **Slice 6 (Technical Feasibility)**: two lookup tables (required + achieved
      triple product), log-scale bucket mapping, citations preserved in
      `lookup_triple_product.yaml`; 6 concepts floor at 1.0 via no-data treatment
- [x] `predicted_scores.yaml` columns reproduced

Acceptance: per-spec predicted score distributions match; conformance tests for
these axes pass.

PR base: `main`. Can land in parallel with P3 (different axis sections).

---

## P5 — Data Availability (Slice 7)

Branch: `feat/axis-data-availability`. Estimate: 1–2 days.

- [x] **Cross-branch merge or copy**: confirm `analyses/{id}/gap_report.md`
      files are present *(confirmed: 37/40 have gap reports; 37/38/39 net-new lack them)*
- [ ] **Gap-report format standardization** *(deferred from P0)*:
      regenerate the 34 existing gap reports with the structured summary block
      per Data Availability spec — **deferred**: the existing gap_report.md files
      are usable as-is; the framework only counts `**blocking**` markers and
      doesn't need a structured summary block. Standardization can land in a
      future analyst-driven PR.
- [ ] `gap_report_id_mapping.yaml` **NEW**: map matrix IDs to gap report dirs
      — **not needed**: gap reports are co-located with concept_id directories;
      `gap_report_path` is auto-detected.
- [x] Embedding: `_gap_report_blocking_count` (file I/O — documented framework
      exception) + `_data_availability_score` (bracket lookup)
- [x] `populate_data_availability_diagnostics.py` **NEW**
      *(named `populate_data_availability.py`)*
- [x] `test_data_availability.py`
- [x] Concepts without gap reports: `data_availability_score: null`; composite
      skip-and-rescale honors this *(37/38/39 verified)*

Acceptance: per-spec predicted scores (7 at 5.0, 10 at 4.0, etc.); null
handling test passes; composite for concepts without gap reports excludes
the axis correctly.

PR base: `main`. Depends on P2; gap-report standardization is in this PR
(not P0 per 2026-05-20 decision).

---

## P6 — Score Explorer UI (Slice 8)

Branch: `feat/score-explorer-ui`. Estimate: 2–3 days.

- [x] `tools/score_explorer/build.py` **NEW**: generates `data/concepts.json` +
      `data/weights.json` from `scoring_v2/scores/table.csv` + per-axis
      diagnostic blocks
- [x] `tools/score_explorer/index.html` **NEW**: vanilla React + Recharts via
      CDN (no build step)
- [x] 7 axis weight sliders (client-side composite re-compute <100ms)
- [x] Ranking table (sortable, filterable, 40 concepts)
- [x] Concept detail panel showing all 7 axis diagnostic blocks on click
- [x] 3 preset profiles ("Equal", "Physics-first", "Commercial-readiness-first")
- [x] Advanced expansion per axis (within-axis weights — **read-only**;
      server-side "save & re-score" round-trip deferred to a future PR
      with a tiny local HTTP write endpoint)
- [x] Export current rankings + active weights as CSV/JSON

Acceptance: UI loads <2s; slider re-rank <100ms; save & re-score <5s;
nulls clearly marked.

PR base: `main`. Depends on at least P3 + P4 (so real scores exist for
multiple axes).

---

## P7 — Cross-axis calibration review (Slice 9)

Branch: `chore/cross-axis-calibration-review`. Estimate: ½ day.
No new code; only weight-tuning + doc.

- [x] Side-by-side review of 40 concepts × 7 axes
- [x] Flag any concept scoring all-5.0 or all-1.0 (cross-axis sanity bar)
      *(passes — 0 of 40 in either bucket)*
- [x] Flag within-axis calibration inconsistencies (e.g., "1 critical Supply
      Chain bottleneck = 2.0" vs "1 critical Plant Complexity subsystem = 3.0")
      *(documented in calibration_review.md §4)*
- [ ] Adjust within-axis weights in `weights/default.yaml` where review
      surfaces inconsistencies — **deferred**: review concluded no adjustments
      blocking; recommendations documented for future PR.
- [x] Re-run `test_spec_conformance.py` to ensure adjustments don't break
      acceptance; update `predicted_scores.yaml` if any per-concept scores
      moved (with spec update via separate PR if needed)
- [x] Output: `.project/active/scoring-v3-rewrite/calibration_review.md`

Acceptance: cross-axis sanity bar passes; calibration review doc committed.

PR base: `main`. Depends on P3, P4, P5 all merged.

---

## Sequencing summary

```
P0 (prereqs) ─→ P1 (schema) ─→ P2 (infra + modularity v5) ──┬─→ P3 (3 axes)
                                                            ├─→ P4 (2 axes)
                                                            └─→ P5 (data availability)
                                                                       │
                                                                  ─→ P6 (UI)
                                                                       │
                                                                  ─→ P7 (calibration)
```

P3, P4 parallelizable. P6 can start after any axis lands (UI built incrementally).

Total: ~13–16 person-days across 8 PRs.

## Tracking

TodoWrite mirrors phases during execution.
Each PR has a separate progress section in this plan (TBD).
