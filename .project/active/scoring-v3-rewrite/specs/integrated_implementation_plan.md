# Integrated Implementation Plan: Seven Scoring Axes + Weight-Adjustment UI

**Status:** Plan for analyst review before implementation
**Owner:** Mallory
**Created:** 2026-05-19
**Target repo:** `1cFE/fusion-tea` (current main, after PR #18 merge)
**Target slices:** `exploration/scoring_v2/` (existing framework, restructured) + new `tools/score_explorer/` (new UI)

This document is an implementation plan tailored to the existing `scoring_v2` framework. It does not propose code yet — it lays out the integration sequence, the structural changes needed, and the risks worth surfacing before any code is written.

**Key architectural choice**: the existing three-dimension framework (Economic Potential / Technical Feasibility / Manufacturability & Scale-Out) is being **replaced** with seven peer axes, each producing an independent 1-5 score. A single weighted-average composite combines them.

---

## Companion specs (required reading for implementation)

Each axis has its own detailed spec or plan that this integrated plan references. Claude Code will need all of them to implement the slices below. The acceptance bars in each slice cite predicted scores defined in these specs.

| # | Axis | Latest spec/plan file | Format |
|---|---|---|---|
| 1 | Modularity | `modularity_implementation_spec.md` (canonical implementation spec; replaces existing scoring_v2 modularity), with `modularity_matrix_v5.md` as the calibration reference (matrix of per-concept scores) | Both
| 2 | Supply Chain | `supply_chain_implementation_spec.md` | Full implementation spec (supersedes earlier `supply_chain_scoring_plan.md`) |
| 3 | Plant Complexity | `plant_complexity_scoring_plan.md` | Planning doc (needs conversion to implementation-spec format before Slice 3 — see "What to do before any code lands") |
| 4 | Customization | `customization_implementation_spec.md` | Full implementation spec |
| 5 | Upper Capacity Factor | `upper_cf_implementation_spec.md` | Full implementation spec |
| 6 | Technical Feasibility | `technical_feasibility_implementation_spec.md` | Full implementation spec (with citations + no-data handling) |
| 7 | Data Availability | `data_availability_implementation_spec.md` | Full implementation spec (downstream of gap reports) |

Each implementation spec follows the same structure: Summary, Changes Summary table, Change A/B/C/D sections (default.yaml / rulebook.py / lookup metadata / diagnostics / tests), Predicted Scores table, Open Questions. They are designed to hand directly to Claude Code with the integrated plan as the orchestration layer.

---

## What's already in place

A quick inventory of the repo state on the current main (after PR #18 merge):

**Framework architecture**:
- `exploration/scoring_v2/score.py` — CLI driver. Loads schema, validates features, evaluates embeddings, applies weights, emits `scores/table.csv`. **Determinism guarantees**: byte-identical reruns, schema fail-loud, no LLM imports in score path.
- `exploration/scoring_v2/embeddings/rulebook.py` — 12 registered embeddings (slice 1 + slice 2 modularity). Each is a pure function with `@embedding(name, inputs=[...])`.
- `exploration/scoring_v2/lib/schema.py` + `lib/feature_io.py` + `lib/extractors/*.py` — schema loading, feature file IO, three extractors (taxonomy, manual, cost_model).
- `exploration/scoring_v2/schema.yaml` — feature schema (single source of truth).
- `exploration/scoring_v2/weights/default.yaml` + `weights/slice1.yaml` — weight matrices currently keyed by `dimension → embedding_name → weight`.
- `exploration/scoring_v2/features/*.yaml` — 40 concept feature files.
- `exploration/scoring_v2/scores/table.csv` — current output (3-dimension format).
- `tests/scoring_v2/` — framework tests covering determinism, schema validation, no-LLM, embedding behavior.

**Current dimensional structure**:
- Three top-level dimensions: `economic_potential`, `technical_feasibility`, `manufacturability_scale_out`.
- Only `manufacturability_scale_out` is wired (5 modularity embeddings).
- `economic_potential` and `technical_feasibility` are empty placeholders.

**Concept count**: 40.

---

## Architectural decision: collapse dimensions to peer axes

The existing `score.py` uses two layers: embeddings aggregate into dimensions, dimensions are the outputs. Path B collapses this to one layer: **embeddings aggregate into axis scores, axis scores are the outputs**. A single weighted-average composite combines axes.

### Before (current code)

```yaml
# weights/default.yaml — two-level structure
manufacturability_scale_out:
  min_viable_device_scale:        0.15
  hardware_topology_complexity:   0.15
  unit_multiplicity:              0.10
  subsystem_stack_burden:         0.10
  component_modularity_aggregate: 0.50
```

```csv
# scores/table.csv — three dimension columns
concept_id,name,economic_potential,technical_feasibility,manufacturability_scale_out,ep_evidence,tf_evidence,mso_evidence
```

### After (Path B)

```yaml
# weights/default.yaml — single-level axis structure + composite
modularity:
  axis_weight: 1.0                # how much modularity contributes to the composite
  embedding_weights:              # within-axis blend
    min_viable_device_scale:        0.30
    hardware_topology_complexity:   0.30
    unit_multiplicity:              0.20
    subsystem_stack_burden:         0.20
    component_modularity_aggregate: 0.00   # disabled in v1; re-enable when capex shares are stable

supply_chain:
  axis_weight: 1.0
  embedding_weights:
    supply_chain_score: 1.0       # single embedding produces the axis score directly
  bottleneck_severity_weights:    # within-embedding tunable
    helium3:    3.0
    tritium:    1.0
    lithium6:   1.0
    # ...

# ... five more axes follow same shape ...

composite:
  formula: weighted_average
  null_handling: skip             # null axis scores excluded from average rather than substituted
```

```csv
# scores/table.csv — seven axis columns + composite + evidence per axis
concept_id,name,modularity,supply_chain,plant_complexity,customization,upper_cf,technical_feasibility,data_availability,composite,modularity_evidence,supply_chain_evidence,...
```

### Why this is cleaner

- **One layer of weights**: the user adjusts `axis_weight` for each of the seven axes. Done.
- **Within-axis weights** are deeper detail (bottleneck severities, subsystem severities) that the user can access via an "Advanced" expansion.
- **Composite is a simple weighted average**: `composite = sum(axis_weight[i] * axis_score[i]) / sum(axis_weight[i])`, restricted to non-null axis scores per concept.
- **The UI maps 1:1** to seven sliders. No two-tier hierarchy to explain.
- **Honest about how axes co-vary**: the framework no longer pretends that "economic potential" is meaningfully separable from "manufacturability" when both depend on the same architectural choices.

### Migration cost

The dimension layer goes away entirely. Specifically:

- `score.py` — replace `DIMENSIONS` constant with `AXES = ["modularity", "supply_chain", "plant_complexity", "customization", "upper_cf", "technical_feasibility", "data_availability"]`. Replace `_score_dimension` with `_score_axis` that takes embedding weights from each axis's block. Add `_compute_composite` for the weighted-average step.
- `weights/default.yaml` + `weights/slice1.yaml` — restructure to the axis-keyed shape. Existing modularity weights move under `modularity.embedding_weights`. The previous two-level structure (dimension → embedding) becomes one-level (axis → its single score, with within-axis weights as nested blocks).
- `tests/scoring_v2/test_score_framework.py` — replace the assertion that checks `economic_potential / technical_feasibility / manufacturability_scale_out` columns with checks for the seven axis columns + composite.
- Downstream artifacts referencing the old column names — grep `.project/`, `exploration/concept_analysis/`, and `tools/` for references to `economic_potential` / `technical_feasibility` / `manufacturability_scale_out` as column names before this lands.

This is ~½ day of refactoring on top of Slice 1's other infrastructure work. Not free, but smaller than the conceptual cleanup it buys.

---

## Schema reconciliation (Slice 0 in detail)

Before any new axis can be wired, the scoring schema needs to match the v3 ontology (`exploration/concept_analysis/table.csv`). Here's the gap.

### v3 ontology columns vs current `scoring_v2/schema.yaml`

| v3 Column | In `scoring_v2/schema.yaml`? | Used by axes |
|---|---|---|
| Confinement Family | ✓ `confinement_family` | Modularity, Supply Chain, Plant Complexity, Tech Feasibility |
| MFE Topology | ✓ `mfe_topology` | Modularity, derived `confinement_concept` |
| IFE Driver | ✓ `ife_driver` | Modularity, derived `confinement_concept` |
| MIF Method | ✓ `mif_method` | Modularity, derived `confinement_concept` |
| Non-Standard Mechanism | **✗ MISSING** | Tech Feasibility (exotic concepts) |
| Tokamak Shape | ✓ `tokamak_shape` | Modularity, derived `confinement_concept` |
| Stellarator Type | ✓ `stellarator_type` | Modularity, derived `confinement_concept` |
| Laser Approach | **✗ MISSING** | Tech Feasibility (laser ICF sub-families) |
| Fuel | ✓ `fuel` | Supply Chain, Plant Complexity, Customization, Upper CF, Tech Feasibility |
| Primary Heating | **✗ MISSING** | Plant Complexity (NBI vs RF aux), Supply Chain (KDP for lasers) |
| Heating Type | **✗ MISSING (redundant?)** | Probably duplicative of Primary Heating |
| Energy Capture | ✓ `energy_capture` | Plant Complexity, Customization, Upper CF |
| Magnet Type | ✓ `magnet_type` | Plant Complexity (cryoplant tier) |
| Blanket Config | **✗ MISSING** | Supply Chain (Li-6, Be, V, FLiBe), Plant Complexity (liquid metal), Upper CF (non-renewable) |
| Operation Mode | ✓ `operation_mode` | Plant Complexity, Upper CF |
| Repetition Rate | **✗ MISSING** | Plant Complexity (target factory severity) |
| Driver Technology | ✓ `driver_technology` | Diagnostics only |
| Driver Type | **✗ MISSING (redundant?)** | Probably duplicative of Driver Technology |

### Legacy features that should retire

The current schema has two features that came from pre-v3 ontology and aren't used by any of the new axes:
- `tritium_breeding` (dropped from `table.csv` by ontology v3)
- `neutron_management` (also dropped)

Per the schema file's comment: "Values for concepts 01-36 came from the pre-v3 taxonomy and remain authoritative." Both are confirmed orphans (no embedding references them) and are retired in Slice 0.

### New non-v3 features needed

Two features that aren't in the differentiation table but are needed:
- `confinement_concept` (derived) — a synthetic concatenation of `confinement_family`, `mfe_topology`, `tokamak_shape`, `stellarator_type`, `ife_driver`, `laser_approach`, `mif_method`, `non_standard_mechanism`, used as a composite key for the achieved triple product lookup in the Tech Feasibility axis.
- `gap_report_path` (manual) — points to the concept's `gap_report.md` for the Data Availability axis.

### Final schema delta proposal

| Action | Feature | Source | Used by |
|---|---|---|---|
| **Add** | `primary_heating` | v3 col (taxonomy extractor) | Plant Complexity, Supply Chain |
| **Add** | `blanket_config` | v3 col (taxonomy extractor) | Supply Chain, Plant Complexity, Upper CF |
| **Add** | `repetition_rate` | v3 col (taxonomy extractor) | Plant Complexity |
| **Add** | `laser_approach` | v3 col (taxonomy extractor) | Tech Feasibility |
| **Add** | `non_standard_mechanism` | v3 col (taxonomy extractor) | Tech Feasibility |
| **Add** | `confinement_concept` | derived (concatenation rule) | Tech Feasibility, Plant Complexity |
| **Add** | `gap_report_path` | manual extractor | Data Availability |
| **Retire** | `tritium_breeding` | (pre-v3 orphan, dropped from `table.csv` by ontology v3) | None |
| **Retire** | `neutron_management` | (pre-v3 orphan, dropped from `table.csv` by ontology v3) | None |
| **Keep** | `heating_type` | (v3 column, partially overlaps with `primary_heating` but not retired per analyst direction) | Not currently used by any axis; kept in schema for completeness |
| **Keep** | `driver_type` | (v3 column, partially overlaps with `driver_technology` but kept per analyst direction; categorical disambiguator for Supply Chain in particular) | Supply Chain (DPSSL Laser / Gas Laser disambiguation) |

**Net change**: +5 v3 features + 1 derived + 1 manual = +7 features added. 2 pre-v3 orphans retired (`tritium_breeding`, `neutron_management`). `heating_type` and `driver_type` kept per analyst direction. Net **+5 features in the schema**.

### Goal of Slice 0

After Slice 0:
- Every concept's feature file has a complete v3-ontology-aligned feature block.
- Each concept's feature set is directly traceable to a v3 column or to a documented derived/manual rule.
- The schema is the **single source of truth** for what features exist.
- No orphan features remain.

This is what you asked for in your point #1: "each concept should have a transparent list of features that can be directly traced to the final scores."

---

## Implementation sequence

Nine slices, ordered to minimize churn and give clear acceptance gates.

### Slice 0: Schema reconciliation (~1 day)

**Goal**: rectify scoring schema with v3 ontology. Surface 5 missing columns, derive `confinement_concept`, add `gap_report_path`, retire 2 pre-v3 orphans.

**Files touched**:
- `exploration/scoring_v2/schema.yaml` — add 7 new feature definitions, retire 2 pre-v3 orphans (`tritium_breeding`, `neutron_management`)
- `exploration/scoring_v2/lib/extractors/taxonomy.py` — extend to pull the 5 new v3 columns from `table.csv`
- `exploration/scoring_v2/lib/extractors/manual.py` — extend to handle `gap_report_path`
- **NEW** `exploration/scoring_v2/lib/extractors/derived.py` — derives `confinement_concept` from the seven sub-columns. Pure function over already-extracted features.
- `exploration/scoring_v2/features/*.yaml` — 40 files; populate new features by re-running extractors
- `tests/scoring_v2/test_extract.py` — extend to cover the new features
- `tests/scoring_v2/test_score_framework.py` — verify no regression in slice-1/2 modularity scoring

**Acceptance bar**: schema validates against all 40 feature files; existing modularity scoring produces identical output; the 5 new v3 features have non-`Unknown` values for ≥ 90% of concepts; `confinement_concept` and `gap_report_path` are populated for all 40.

**Open questions for Slice 0**:
- How should `confinement_concept` handle concepts where multiple sub-columns are populated (e.g., a tokamak that's also "Compact" — both `mfe_topology = Tokamak` and `tokamak_shape = Compact` are set)? The derivation rule needs to be deterministic and documented. The Tech Feasibility spec's lookup table assumes this is resolved.
- For MFE/Open-Linear topology specifically: Z-pinch and magnetic mirror both file here. The `confinement_concept` derivation must disambiguate by `Driver Type` (Magnetic → Mirror, Magnetic pinch → Z-pinch) so the Tech Feasibility lookup resolves correctly.

---

### Slice 1: Axis-based scoring infrastructure (~1 day)

**Goal**: refactor `score.py` from three-dimensions to seven peer axes with a composite. Restructure `weights/default.yaml` to match.

**Files touched**:
- `exploration/scoring_v2/score.py`:
  - Replace `DIMENSIONS` constant with `AXES = ["modularity", "supply_chain", "plant_complexity", "customization", "upper_cf", "technical_feasibility", "data_availability"]`
  - Replace `_score_dimension` with `_score_axis` (takes axis name, reads `embedding_weights` from that axis's block in `weights/default.yaml`)
  - Add `_compute_composite` for the weighted-average step
  - Add null-handling logic: when an axis returns null, exclude it from composite (rescale remaining weights to sum to original total within that concept)
  - Update CSV output: 7 axis columns + composite + 7 evidence columns + composite evidence
- `exploration/scoring_v2/weights/default.yaml` — restructure to axis-keyed shape:
  ```yaml
  composite:
    formula: weighted_average
    null_handling: skip

  modularity:
    axis_weight: 1.0
    embedding_weights:
      min_viable_device_scale:        0.30
      hardware_topology_complexity:   0.30
      unit_multiplicity:              0.20
      subsystem_stack_burden:         0.20
      component_modularity_aggregate: 0.00
  
  supply_chain:
    axis_weight: 1.0
    embedding_weights:
      supply_chain_score: 1.0   # placeholder; landed in Slice 2

  # ... five more placeholders ...
  ```
- `exploration/scoring_v2/weights/slice1.yaml` — restructure similarly (keep as reference config)
- `tests/scoring_v2/test_score_framework.py` — rewrite the column-set assertion for the new shape
- Documentation pass: grep `.project/` for hardcoded references to the old dimension names

**Acceptance bar**: `score.py` runs without errors; the existing modularity scoring produces the same values as before (just under a renamed column); the other six axis columns produce null (no embeddings registered yet); composite column reflects modularity-only weighted average.

**Design decision: null-handling**. When an axis is null (e.g., Data Availability with no gap report), the composite skips it and rescales remaining axis weights. The CSV records which axes were included via a `composite_axes_included` column. Concepts with all-null axes get null composite.

---

### Slice 1b: Modularity replacement (~1 day)

**Companion spec**: `modularity_implementation_spec.md` (replaces existing scoring_v2 modularity), with `modularity_matrix_v5.md` as the calibration target.

**Goal**: replace the existing 12-embedding modularity implementation with the v5 three-component formula. This is a destructive replacement; the previous slices 1 and 2 of modularity work get retired.

**Files touched**:
- `exploration/scoring_v2/embeddings/rulebook.py` — delete the 12 existing modularity embeddings; add 6 new embeddings per the v5 spec
- `exploration/scoring_v2/weights/default.yaml` — restructure `modularity` block with new embedding_weights (0.50/0.25/0.25) and 5 sub-table lookups (mvs, vessel, magnet/driver, blanket, unit_count)
- `exploration/scoring_v2/lookup_modularity.yaml` — NEW, metadata for the lookup tables
- `exploration/scoring_v2/schema.yaml` — add `unit_count_estimate` feature; retire 4 unused capex shares (`w_bop`, `w_fuel_cycle`, `w_aux`, `w_civil`)
- `exploration/scoring_v2/lib/extractors/cost_model.py` — trim to stop emitting retired capex shares
- `exploration/scoring_v2/features/*.yaml` — 39 files: add `unit_count_estimate` (manual values from v5 matrix), remove 4 retired capex shares, update modularity diagnostic block
- `exploration/scoring_v2/scripts/populate_modularity_diagnostics.py` — NEW
- `tests/scoring_v2/test_modularity.py` — replace existing modularity tests with new ones anchored to v5 predicted scores

**Acceptance bar**: scores match the v5 predicted distribution within rounding tolerance. Specifically:
- Top scorers: 08 Helion = 5.00, 37 NearStar = 5.00, 07 Pacific MagLIF = 4.93, 14 General Fusion = 4.88
- Bottom scorers: 33 BEST = 1.91, 36 Helical Fusion = 2.03, 16 Acceleron = 2.54, 38 SHINE = 2.54
- 01 CFS ARC anchored to 3.71 (mvs=3, pmod=4.84, um=4)
- All 39 concepts in [1.0, 5.0]
- mvs lookup covers all 39 concepts (no defensive fallback to 1.0)

**Why this slice runs before slices 2-7**: the modularity replacement touches the same rulebook.py file and weights/default.yaml structure that the new axes will extend. Landing modularity first establishes the clean axis-keyed pattern under Path B; the other six axes then layer in. Running modularity in parallel with another axis would create merge friction in those shared files.

---

### Slice 2: Supply Chain axis (~1 day)

**Companion spec**: `supply_chain_implementation_spec.md` (canonical reference for embedding logic, severity weights, predicted scores, and acceptance criteria).

Reference implementation pattern for the next four axes. Same structure: severity-weighted bottleneck sum, `max(1, 5 - weight)` formula.

**Files touched**:
- `exploration/scoring_v2/embeddings/rulebook.py` — add `_supply_chain_bottleneck_weight` and `_supply_chain_score` embeddings + 2 helpers
- `exploration/scoring_v2/weights/default.yaml` — populate `supply_chain.bottleneck_severity_weights`
- **NEW** `exploration/scoring_v2/lookup_bottlenecks.yaml` — per-bottleneck metadata (descriptions, no weights)
- `exploration/scoring_v2/features/*.yaml` — populate `supply_chain_diagnostics` block via populate script
- **NEW** `exploration/scoring_v2/scripts/populate_supply_chain_diagnostics.py`
- **NEW** `tests/scoring_v2/test_supply_chain.py`

**Acceptance bar**: scores match predicted distribution from the supply chain spec (5.0 for 7 concepts, 4.5 for 3, 3.0 for 1, 2.0 for ~20, 1.5 for 7, 1.0 for Xcimer alone).

---

### Slice 3: Plant Complexity axis (~1 day)

**Companion spec**: `plant_complexity_scoring_plan.md`. Note: this is currently a planning document rather than a full implementation spec. Before Slice 3 starts, convert it to the same implementation-spec format used by the other six axes (Change A/B/C/D structure, explicit weights YAML, embedding code, populate script, tests). The technical content is complete; only the format needs alignment.

Same pattern, 15 subsystem flags.

**Files**: `_plant_complexity_subsystem_weight`, `_plant_complexity_score`, `lookup_plant_subsystems.yaml`, `populate_plant_complexity_diagnostics.py`, `test_plant_complexity.py`.

**Acceptance bar**: scores match predicted distribution (5.0 for Helion + LPP DPF; 4.0 for SHINE; 3.5 for TAE/Pale Blue/Sonofusion; 3.0 for hb11/NearStar; 2.5 for Avalanche; 2.0 for Proxima QI/OpenStar/Pacific MagLIF/First Light; 1.5 for Realta/GenFu MTF/OpenStar; 1.0 for 8 D-T concepts with full subsystem stack).

---

### Slice 4: Customization axis (~½ day)

**Companion spec**: `customization_implementation_spec.md` (full spec; port of C5 logic from `fusion-tea-scoring` branch).

Simpler — two sub-factors (thermal rejection, fuel safety), rescaled to 1-5.

**Files**: `_thermal_rejection_score`, `_fuel_safety_score`, `_customization_score`, `lookup_customization.yaml`, `populate_customization_diagnostics.py`, `test_customization.py`.

**Acceptance bar**: scores match predicted distribution (6 at 5.0, 2 at 4.33, 1 at 3.0, 4 at 2.33, 26 at 1.67).

---

### Slice 5: Upper Capacity Factor axis (~½ day)

**Companion spec**: `upper_cf_implementation_spec.md` (full spec).

Same pattern as supply chain. Three penalties: pulsed operation, neutronic fuel, non-renewable blanket.

**Files**: `_operational_penalty_weight`, `_upper_cf_score`, `lookup_upper_cf_penalties.yaml`, `populate_upper_cf_diagnostics.py`, `test_upper_cf.py`.

**Acceptance bar**: scores match predicted distribution (4 at 5.0, 4 at 4.5, 3 at 4.0, 23 at 3.5, 5 at 3.0).

---

### Slice 6: Technical Feasibility axis (~1 day)

**Companion spec**: `technical_feasibility_implementation_spec.md` (full spec with 20 numbered citations for triple product data and explicit no-data flooring for 6 concepts).

More complex than the others — two coupled lookup tables (required by fuel, achieved by family), log-scale bucket mapping, six concepts default to floor via the "no data" treatment.

**Files**: `_triple_product_gap`, `_technical_feasibility_score`, `lookup_triple_product.yaml` (with citations), `populate_technical_feasibility_diagnostics.py`, `test_technical_feasibility.py`.

**Acceptance bar**: scores match predicted distribution (1 at 5.0 — Inertia DPSSL; 3 at 4.0; 5 at 3.0; ~10 at 2.0; ~20 at 1.0).

---

### Slice 7: Data Availability axis (~1 day)

**Companion spec**: `data_availability_implementation_spec.md` (full spec; uses simple blocking-marker counting with bracket schedule).

Different from the others — reads `gap_report.md`, not just feature data. Embedding does file I/O (the documented exception to the framework's pure-function pattern).

**Files**:
- Embeddings: `_gap_report_blocking_count` (file I/O), `_data_availability_score` (bucket map)
- `weights/default.yaml` — `data_availability.blocking_count_brackets`
- **NEW** `gap_report_id_mapping.yaml` — maps matrix IDs to gap report directory IDs
- `populate_data_availability_diagnostics.py`
- `test_data_availability.py`

**Cross-branch dependency**: gap reports live on `fusion-tea-scoring` branch. Recommend merging the analysis directory into the scoring branch *before* starting Slice 7. Three integration options discussed in the data availability spec.

**Acceptance bar**: scores match predicted distribution (7 at 5.0, 10 at 4.0, 10 at 3.0, 10 at 2.0, 1 at 1.0, 3+ null for concepts without reports).

---

### Slice 8: Weight Explorer UI (~2-3 days)

Single-page web UI for adjusting axis weights and viewing rankings in real time.

**Architecture**:
```
tools/score_explorer/
├── index.html              # Single-page app
├── score_explorer.jsx      # React (Recharts/shadcn) implementation
├── data/
│   ├── concepts.json       # Generated from scores/table.csv + per-axis diagnostic blocks
│   └── weights.json        # Generated from weights/default.yaml (initial values)
└── build.py                # NEW. Builds data/*.json from scoring_v2 output.
```

**UI components**:

1. **Seven axis weight sliders** — one per axis. All slider movements trigger immediate client-side composite re-computation (no server round-trip).

2. **Ranking table** — sortable, filterable list of 40 concepts. Columns: name, fuel, confinement family, seven axis scores (with mini-bar showing relative score), composite. Color-coded by tier.

3. **Concept detail panel** — clicking a concept expands a panel showing the diagnostic block for each axis (e.g., for Plant Complexity, what subsystems triggered; for Tech Feasibility, achieved vs required TP).

4. **Preset weight profiles** — three saved profiles:
   - "Equal weights" (all 1.0)
   - "Physics-first" (Technical Feasibility 2.0, others 1.0)
   - "Commercial-readiness-first" (Modularity + Supply Chain + Plant Complexity 1.5, others 1.0)

5. **Advanced expansion per axis** — within-axis weights (e.g., bottleneck severities for Supply Chain). Editable via a sub-form. Changes here trigger a "save & re-score" because they require Python embedding recomputation.

6. **Export** — download current rankings as CSV + JSON snapshot of the active weight matrix.

**What's client-side vs. server-side**:

| Action | Where | Latency |
|---|---|---|
| Adjust axis weight slider | Client-side | <100ms (instant re-rank) |
| Adjust within-axis weight (advanced) | Server-side (Python re-run) | ~2-5 sec |
| Switch preset profile | Client-side | <100ms |
| Filter/sort table | Client-side | <100ms |
| Click concept for detail | Client-side | <100ms |

**Why composition-only client-side**: per-axis scores depend on Python embedding logic. Within-axis weight changes (e.g., tritium severity 1.0 → 1.5) require re-running embeddings. The "save & re-score" pattern handles this: write new weights to `weights/default.yaml`, run `score.py`, reload data.

**Frontend stack**: Plain HTML + vanilla React + Recharts (CDN-loaded, no build step). Keeps the tool dependency-free.

**Acceptance bar**:
- UI loads in <2 seconds, shows all 40 concepts ranked
- Adjusting any axis weight slider re-ranks within 100ms (client-side)
- Clicking a concept shows its diagnostic block for each axis
- "Save & re-score" writes weights and reloads within ~5 seconds
- Concepts with null axis scores are clearly marked (not silently scored as 0)

---

### Slice 9: Cross-axis consistency review (~½ day, no code)

After all seven axes land, sit down with the predicted scores side-by-side for all 40 concepts and look for cross-axis inconsistencies:

- Does any concept score 5.0 on every axis? (If yes, the framework lacks differentiation.)
- Does any concept score 1.0 on every axis? (Probably Sonofusion. Check the framework agrees with your gut.)
- Are there concepts that score very differently across axes in surprising ways? (E.g., Helion scoring 5.0 on customization but 2.0 on tech feasibility — that's the framework correctly identifying architectural advantage but physics gap.)
- Are within-axis weight calibrations consistent? (Is "1 critical bottleneck (3.0)" in supply chain comparable to "1 critical subsystem (2.0)" in plant complexity?)

This is where you can recommend recalibration of within-axis weights based on cross-axis comparison. Easy iteration via `weights/default.yaml` edits.

---

## Determinism + purity audit

Worth tracking how the seven axes compare on the framework's determinism guarantees:

| Axis | Pure function of features? | Reads only feature file? | Failure mode |
|---|---|---|---|
| Modularity | Yes | Yes | Schema fail-loud |
| Supply Chain | Yes | Yes | Schema fail-loud |
| Plant Complexity | Yes | Yes | Schema fail-loud |
| Customization | Yes | Yes | Unknown fuel → D-T default; TBD energy → thermal default (documented) |
| Upper CF | Yes | Yes | Schema fail-loud |
| Technical Feasibility | Yes | Yes | Missing achieved TP → null, score floor 1.0 |
| **Data Availability** | **No — reads gap_report file** | **No — reads external file** | Missing file → null score (skipped in composite) |

Data Availability is the deliberate framework exception. Mark clearly in code comments. The other six maintain the pure-function property.

Determinism guarantees hold for axes 1-6 (byte-identical reruns on unchanged inputs). For Data Availability, determinism holds *given a stable gap_report.md*.

---

## Risks and open questions

### Risks worth surfacing

**1. Dimension-removal grep.** Path B removes three columns (`economic_potential`, `technical_feasibility`, `manufacturability_scale_out`) from the output CSV. Any downstream artifact (report, chart, analysis script) that references these names breaks. Worth a one-pass grep before Slice 1 lands.

**2. Schema migration friction.** Slice 0 is a coordinated change. If it lands wrong, every subsequent axis breaks. Plan: write it as a standalone PR, verify modularity scoring is unaffected, then layer the axes on top.

**3. Gap report cross-branch dependency.** Slice 7 needs gap reports from `fusion-tea-scoring`. Resolve via merge before starting Slice 7.

**4. Null score handling in composite.** When an axis is null, the composite must skip it cleanly. The CSV output needs to show *which* axes were included per concept. The UI needs to indicate "null" vs "low score" distinctly. This is a non-trivial UX detail.

**5. Concept ID drift.** 40 concepts now; could shift. Never hard-code concept ID lists in embeddings; always derive from the feature file glob.

**6. Within-axis weight retuning.** Slice 9's review may surface that within-axis calibrations need adjustment. Easy to iterate via `default.yaml`, but worth budgeting time for it.

### Open questions for the analyst

**Q1. Legacy slice1.yaml — keep or retire?** The old `weights/slice1.yaml` exists for verifying slice-1 acceptance bars. Under Path B it needs restructuring (or retirement). Recommend restructuring under the new schema for regression safety, then retiring once Slice 1 lands cleanly.

**Q2. Modularity replacement (resolved).** The existing 12-embedding modularity implementation in `scoring_v2` is being **replaced** with the v5 three-component formula (mvs, percent_mod, unit_multiplicity). See `modularity_implementation_spec.md` for the full replacement spec. Within-axis tuning surfaces three top-level weights (0.50 / 0.25 / 0.25 per v5 calibration) plus sub-tables for mvs/vessel/magnet-driver/blanket/unit-count lookups.

**Q3. Within-axis weight UI — primary or "advanced"?** The seven axis weights are the primary UI knob. Within-axis weights (bottleneck severities, etc.) are deeper. Two options:
- (a) **Hidden behind "Advanced" expansion**: cleaner default UI; analyst clicks to access
- (b) **Visible alongside axis weights**: more complete view; cluttered

Recommend (a) — the UI's value is fast iteration on axis weights; within-axis tuning is rarer and warrants the explicit interaction.

**Q4. Composite null handling.** When some axes are null for a concept:
- (a) **Skip null axes, rescale remaining weights** — what I've recommended. Composite is "weighted average of non-null axes."
- (b) **Substitute floor 1.0** — every concept has all 7 scores; the composite is always over 7 values.
- (c) **Refuse to composite** — concepts with any null axis get null composite, can't be ranked.

Recommend (a). (b) penalizes concepts unfairly for analyst incomplete work. (c) is too restrictive — most analyses produce a useful composite even when one axis is missing.

**Q5. Composite formula — weighted average vs alternatives.** Path B uses `composite = sum(w_i * score_i) / sum(w_i)`. Alternatives:
- **Geometric mean** — penalizes concepts that are weak on any single axis (more conservative). Useful if any axis can be a deal-breaker.
- **Lexicographic** — rank by axis A first, then break ties by axis B. Useful if axes have priority order.
- **Min** — composite = the weakest axis score. Hardest-line-conservative.

Recommend weighted average for v1. Geometric mean could be added later as a toggle in the UI.

**Q6. Multiple weight profiles in the UI.** The UI lets users adjust weights. Should saved profiles be:
- (a) Committed to `weights/default.yaml` (one canonical state per repo)
- (b) Saved to local user-specific file (each analyst keeps their own)
- (c) Just session-local (cleared on refresh)

Recommend (a) for v1. The explicit "Save & re-score" button writes to `weights/default.yaml`. Add (b) as named profiles in `weights/profiles/{analyst}.yaml` later if useful.

---

## Files touched summary

```
exploration/scoring_v2/schema.yaml                                  # extend with 7 new features, retire orphans (Slice 0)
exploration/scoring_v2/lib/extractors/taxonomy.py                   # extend for 5 new v3 columns (Slice 0)
exploration/scoring_v2/lib/extractors/derived.py                    # NEW — derives confinement_concept (Slice 0)
exploration/scoring_v2/lib/extractors/manual.py                     # extend for gap_report_path (Slice 0)
exploration/scoring_v2/features/*.yaml                              # 40 files; new features + 7 diagnostic blocks (all slices)
exploration/scoring_v2/score.py                                     # restructure: 3 dimensions → 7 axes + composite (Slice 1)
exploration/scoring_v2/weights/default.yaml                         # restructure to axis-keyed shape (Slice 1) + add 7 axis blocks
exploration/scoring_v2/weights/slice1.yaml                          # restructure or retire (Slice 1)
exploration/scoring_v2/embeddings/rulebook.py                       # add ~15 new embeddings + helpers (Slices 2-7)
exploration/scoring_v2/lookup_bottlenecks.yaml                      # NEW (Slice 2)
exploration/scoring_v2/lookup_plant_subsystems.yaml                 # NEW (Slice 3)
exploration/scoring_v2/lookup_customization.yaml                    # NEW (Slice 4)
exploration/scoring_v2/lookup_upper_cf_penalties.yaml               # NEW (Slice 5)
exploration/scoring_v2/lookup_triple_product.yaml                   # NEW (Slice 6)
exploration/scoring_v2/gap_report_id_mapping.yaml                   # NEW (Slice 7)
exploration/scoring_v2/scripts/populate_*.py                        # 6 NEW populate scripts
tests/scoring_v2/test_*.py                                          # 6 NEW test files, plus updates to test_score_framework.py
tools/score_explorer/                                               # NEW directory (Slice 8) — UI
.project/active/scoring-v2-{axis}-slice/                            # 6 NEW slice work directories
```

**Total new files**: ~30 new; ~50 existing modified (mostly feature YAML).

**Total estimated effort**: ~10-12 days for slices 0-7 (including Slice 1b modularity replacement), plus 2-3 days for Slice 8, plus ½ day for Slice 9. Roughly **13-16 person-days**.

---

## Recommended sequencing

Natural session breakpoints if you do this across multiple sittings:

**Session 1 (2-3 days): Schema + infrastructure + modularity replacement**
- Slice 0 (schema reconciliation with v3 ontology)
- Slice 1 (axis-based scoring refactor; 3 dimensions → 7 axes + composite)
- Slice 1b (modularity replacement — destructive rewrite to v5 formula)
- Verify all 39 modularity scores match v5 predicted distribution before moving on

**Session 2 (2-3 days): Three easy axes**
- Slice 2 (Supply Chain) — pattern reference
- Slice 4 (Customization)
- Slice 5 (Upper Capacity Factor)

**Session 3 (2-3 days): Two harder axes**
- Slice 3 (Plant Complexity)
- Slice 6 (Technical Feasibility)

**Session 4 (1-2 days): Data Availability + cross-branch resolution**
- Merge analysis directory into scoring branch
- Slice 7 (Data Availability)

**Session 5 (2-3 days): UI**
- Slice 8 (Weight Explorer)

**Session 6 (½ day): Calibration review**
- Slice 9 (cross-axis consistency)
- Recalibrate within-axis weights based on findings

---

## What to do before any code lands

Before Slice 0:

1. **Run grep** for downstream references to the old dimension names (`economic_potential`, `technical_feasibility`, `manufacturability_scale_out`) — anything that breaks needs migration.

2. **Audit `table.csv` enum values** for the 5 columns being added to the schema. The schema needs the actual values used, not theoretical possibilities.

3. **Standardize the gap_report.md format** so blocking gaps can be counted deterministically. The current 34 gap reports use inconsistent formatting (`**blocking**` in some, plain `blocking` in tables in others), which produces incorrect counts for the Data Availability axis. See the Data Availability spec's "Prerequisite: Standardize gap_report format upstream" section for the structured summary block to add to every gap report. Required before Slice 7.

4. **Put predicted scores from all 7 axes side-by-side in a spreadsheet** (40 concepts × 7 axes = 280 cells). Walk through the top-5 and bottom-5 per axis. If anything looks wrong, fix the spec before the code.

5. **Convert `plant_complexity_scoring_plan.md` to implementation-spec format** matching the structure of the other six axis specs. The technical content is complete; only the format needs alignment (Change A/B/C/D sections, explicit YAML weights, embedding code, populate script, tests).

The schema work in Slice 0, the gap report standardization, the calibration check above, and the plant complexity format conversion are the prerequisites. Everything else builds on them.

---

## Upload package for Claude Code handoff

When handing this work to Claude Code, upload the following files together:

```
integrated_implementation_plan.md           (this file — the orchestration map)
modularity_implementation_spec.md           (Slice 1b — replaces existing scoring_v2 modularity)
modularity_matrix_v5.md                     (modularity calibration target / predicted scores)
supply_chain_implementation_spec.md         (Slice 2)
plant_complexity_scoring_plan.md            (Slice 3 — convert format before handoff per prereq 5)
customization_implementation_spec.md        (Slice 4)
upper_cf_implementation_spec.md             (Slice 5)
technical_feasibility_implementation_spec.md (Slice 6)
data_availability_implementation_spec.md    (Slice 7)
```

Without the per-axis specs, Claude Code would have to reinvent the embedding logic for each axis with no calibration target — the integrated plan alone doesn't contain the severity weights, lookup tables, predicted scores, or citations.
