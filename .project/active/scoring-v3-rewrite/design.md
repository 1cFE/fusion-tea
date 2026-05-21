# Design — Scoring Framework v3 Rewrite

**Spec:** [spec.md](spec.md) · **Plan:** [plan.md](plan.md)
**Created:** 2026-05-20

## 1. Axis-based scoring model

### Before (current main, post-rebase)
```
weights/default.yaml:
  economic_potential: {}              # placeholder
  technical_feasibility: {}           # placeholder
  manufacturability_scale_out:
    {embedding_name: weight}          # 5 modularity embeddings

scores/table.csv columns:
  concept_id, name,
  economic_potential, technical_feasibility, manufacturability_scale_out,
  ep_evidence, tf_evidence, mso_evidence
```

### After
```
weights/default.yaml:
  composite:
    formula: weighted_average
    null_handling: skip                # rescale remaining weights

  modularity:
    axis_weight: 1.0
    embedding_weights:                 # within-axis blend (v5: 0.50/0.25/0.25)
      min_viable_device_scale: 0.50
      percent_mod: 0.25
      unit_multiplicity: 0.25
    # Plus sub-tables for advanced tuning (mvs_lookup, vessel_lookup, …)

  supply_chain:
    axis_weight: 1.0
    embedding_weights: {supply_chain_score: 1.0}
    bottleneck_severity_weights: {…}

  # plant_complexity, customization, upper_cf,
  # technical_feasibility, data_availability — same pattern

scores/table.csv columns:
  concept_id, name,
  modularity, supply_chain, plant_complexity, customization,
  upper_cf, technical_feasibility, data_availability,
  composite,
  modularity_evidence, … (7 evidence cols), composite_evidence,
  composite_axes_included            # JSON list of included axes per concept
```

### Composite formula

```
included = {axis : score(concept, axis) is not None}
if not included:
    composite = None
else:
    rescaled = {axis : axis_weight[axis] for axis in included}
    norm = sum(rescaled.values())
    composite = sum(score[a] * rescaled[a] for a in included) / norm
```

This honestly excludes null axes rather than substituting floor (1.0) — and
records *which* axes contributed so the UI can show "5 of 7 axes" badges.

## 2. Per-axis pattern (consistent across all 7)

| Element | Location | Notes |
|---|---|---|
| Axis registration | `weights/default.yaml` `{axis}:` block | `axis_weight` (composite) + `embedding_weights` (within-axis blend) + axis-specific sub-tables (severity weights, lookup tables) |
| Embeddings | `embeddings/rulebook.py` | `@embedding(name, inputs=[...])` decorated pure functions returning float 1.0–5.0 or None |
| Lookup metadata | `lookup_{axis}.yaml` | Descriptions, tier names, rationale (no numerical weights — those live in `weights/default.yaml`) |
| Per-concept diagnostics | `features/*.yaml` `{axis}_diagnostics:` block | What fired, what weight, derived score — populated by per-axis populate script |
| Populate script | `scripts/populate_{axis}_diagnostics.py` | Idempotent; reads features + weights, writes diagnostic block |
| Acceptance tests | `tests/scoring_v2/test_{axis}.py` | Trigger rule tests + per-concept score anchors + weight-tuning tests |

Penalty-stack axes (Supply Chain, Plant Complexity, Upper CF, Data Availability):
`score = max(1.0, 5.0 - severity_weight_sum)` or bucket lookup.

Lookup-based axes (Modularity, Customization, Technical Feasibility):
multi-table dispatch with category-level lookup keys.

## 3. Spec-conformance test framework

New file: `tests/scoring_v2/test_spec_conformance.py`. Single source of truth
for predicted scores: `tests/scoring_v2/predicted_scores.yaml`, structured as:

```yaml
modularity:
  "01-hts-compact-tokamak": 3.71
  "08-frc-w-direct-conversion": 5.00
  # … all 40 concepts
supply_chain:
  "01-hts-compact-tokamak": 2.0
  # … all 40 concepts
# … 7 axes
```

`TestSpecPredictedScoresLand` parameterizes over this file:

```python
@pytest.mark.parametrize("axis,concept_id,expected", _expand_predicted_scores())
def test_predicted_score_matches(axis, concept_id, expected):
    actual = _score(concept_id, axis)
    assert abs(actual - expected) < 0.05  # rounding tolerance
```

Updating predicted scores = edit one YAML, not 7 test files. Spec changes
propagate via re-export.

### Other conformance test classes (full list in [spec.md §"Acceptance bar"])

`TestAxisRegistryConformance`, `TestEmbeddingRegistryConformance`,
`TestSchemaConformance`, `TestDiagnosticBlockConformance`,
`TestCsvOutputConformance`, `TestDeterminismConformance`,
`TestNullHandlingConformance`, `TestNoLlmInScorePath`,
`TestCrossAxisSanity`, `TestSpecPredictedScoresLand`.

## 4. PR / commit chunking

8 PRs, each branched off `main` directly, PR'd back via `gh pr create`,
deleted on merge (Reid's pattern).

| PR | Branch | Slices | Days | Depends on |
|---|---|---|---|---|
| P0 | `prep/v3-rewrite-prereqs` | (prereqs) | ½ | — |
| P1 | `feat/schema-v3-reconcile` | 0 | 1 | P0 |
| P2 | `feat/axes-infrastructure-and-modularity-v5` | 1, 1b | 2 | P1 |
| P3 | `feat/axes-supply-chain-customization-upper-cf` | 2, 4, 5 | 2 | P2 |
| P4 | `feat/axes-plant-complexity-technical-feasibility` | 3, 6 | 2 | P2 (parallel with P3) |
| P5 | `feat/axis-data-availability` | 7 | 1–2 | P2 + gap-report standardization |
| P6 | `feat/score-explorer-ui` | 8 | 2–3 | P5 (or any axis lands) |
| P7 | `chore/cross-axis-calibration-review` | 9 | ½ | P3, P4, P5 all merged |

P3 and P4 can land in parallel (touch different axis sections of
`weights/default.yaml` + different parts of `rulebook.py`); merge conflicts
limited to a few shared files.

## 5. Files touched (summary)

```
# New
exploration/scoring_v2/lib/extractors/derived.py
exploration/scoring_v2/lookup_modularity.yaml
exploration/scoring_v2/lookup_bottlenecks.yaml
exploration/scoring_v2/lookup_plant_subsystems.yaml
exploration/scoring_v2/lookup_customization.yaml
exploration/scoring_v2/lookup_upper_cf_penalties.yaml
exploration/scoring_v2/lookup_triple_product.yaml
exploration/scoring_v2/gap_report_id_mapping.yaml
exploration/scoring_v2/scripts/populate_*_diagnostics.py   # ×7
tests/scoring_v2/test_*.py                                 # ×6 new
tests/scoring_v2/test_spec_conformance.py
tests/scoring_v2/predicted_scores.yaml
tools/score_explorer/                                      # ×~10 files
.project/active/scoring-v3-rewrite/                        # this work item

# Modified
exploration/scoring_v2/score.py                  # 3 dims → 7 axes + composite
exploration/scoring_v2/schema.yaml               # +7 features, retire 2 orphans + 4 capex shares
exploration/scoring_v2/embeddings/rulebook.py    # del 12 modularity, add ~20 new
exploration/scoring_v2/weights/default.yaml      # restructure to axis-keyed
exploration/scoring_v2/weights/slice1.yaml       # restructure or retire
exploration/scoring_v2/lib/extractors/taxonomy.py # +5 new v3 columns
exploration/scoring_v2/lib/extractors/manual.py  # +gap_report_path
exploration/scoring_v2/lib/extractors/cost_model.py # trim 4 retired w_*
exploration/scoring_v2/features/*.yaml           # 40 files: new diagnostic blocks
tests/scoring_v2/test_score_framework.py         # CSV columns assertion
```

Total: ~30 new + ~55 modified.

## 6. Rollback

Per-PR: `gh pr close --delete-branch <number>`; commits remain reachable by
SHA for ~90 days. Each PR is independent so rollback is bounded to that
slice's axis.

Slice 1b is the highest-blast-radius rollback because it touches the schema
and removes embeddings other axes might depend on. Mitigation: P2 lands as
the smallest possible PR (just the axis infrastructure + v5 modularity, no
new axes layered in).
