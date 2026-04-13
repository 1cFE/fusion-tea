# Spec: Similarity Metric v2 — Hierarchical Classification + Dimension Weights

**Status:** Draft
**Owner:** Reid W
**Created:** 2026-04-12 16:58 PDT
**Complexity:** LOW
**Branch:** TBD

---

## Business Goals

### Why This Matters

The concept explorer's similarity map is the primary tool for visually exploring relationships between fusion concepts. The current metric ignores the hierarchical classification fields (confinement family, topology, subtype) and weights all attributes equally, producing counter-intuitive distances. Two compact HTS tokamaks score only 0.571 similarity; two magnetic mirrors score 0.333. Users who see these distances lose trust in the tool and miss real structural patterns.

### Success Criteria

- [ ] Same-type concept pairs (same topology + subtype) score noticeably higher than before
- [ ] Cross-family pairs score noticeably lower than same-family pairs
- [ ] The constellation map visually clusters concepts by confinement approach, with meaningful variation within clusters
- [ ] A diagnostic script confirms intuition alignment across a reference set of pairs

### Priority

Medium-high. The explorer UX epic (EXPLORER-UX-V2) is complete, so the comparison infrastructure works — but the underlying similarity data is misleading. This undermines the value of the constellation and neighborhood views.

---

## Problem Statement

### Current State

The similarity engine (`similarity.py`) computes pairwise scores using 9 cross-cutting design fields across 4 equally-weighted dimensions:

```
plasma_physics: [fuel, primary_heating, plasma_state]
engineering:    [magnet_type, energy_capture]
fuel_cycle:     [tritium_breeding, neutron_management]
operations:     [operation_mode, repetition_rate]
```

**8 hierarchical classification fields are ignored**: confinement_family, mfe_topology, tokamak_shape, stellarator_type, ife_driver, laser_approach, mif_method, non_standard_mechanism.

**All fields have equal weight**: a mismatch on `repetition_rate` counts the same as a mismatch on `fuel`.

### Desired Outcome

The similarity metric incorporates "what kind of machine is this" as the dominant signal, with design attributes providing secondary differentiation. Scores align with domain expert intuition: same-type concepts cluster tightly, cross-family concepts are distant, and within-family variation reflects real engineering differences.

---

## Scope

### In Scope

1. New "classification" dimension using hierarchical tree-walk scoring
2. Dimension-level weights (classification > plasma_physics > others)
3. Weighted overall score formula replacing flat `total_matches / total_comparable`
4. Updated test expectations
5. Diagnostic script for intuition-checking reference pairs

### Out of Scope

- Within-dimension field weights (deferred — evaluate after dimension weights ship)
- Cross-family partial credit (e.g., MFE↔MIF scoring higher than MFE↔NONSTANDARD)
- `confidence` field as a similarity factor
- `driver_technology` semantic similarity
- Frontend changes (constellation and neighborhood views consume scores via existing API)
- Weight tuning UI or configurability beyond module-level constants

### Edge Cases & Considerations

- **TBD/N/A in hierarchy fields**: The tree-walk algorithm inherently handles this — it only walks the relevant branch (e.g., a tokamak's `ife_driver` is null, but the algorithm never checks it)
- **Classification dimension always has comparable=1**: Unlike design attribute dimensions, the hierarchy always produces a score (every concept has a confinement_family). This means it never gets excluded from the weighted average.
- **Concepts with many TBD design fields**: These already have fewer comparable fields in design dimensions. Adding a classification dimension that's always comparable will anchor their scores more, which is desirable — a TBD-heavy tokamak should still be close to other tokamaks.
- **MDS projection will change shape**: The constellation map will look different after the metric change. This is expected and desired, not a regression.

---

## Requirements

### Functional Requirements

> Requirements below are from user's request unless marked [INFERRED].

1. **FR-1**: Add a "classification" similarity dimension that computes a 0-1 score by walking the taxonomy hierarchy tree:
   - Different confinement_family → 0.0
   - Same family, different level-2 (topology/driver/method/mechanism) → 0.5
   - Same family, same level-2, level-3 differs or N/A → 0.75
   - Same family, same level-2, same level-3 → 1.0

2. **FR-2**: Add dimension-level weights to the overall score calculation:
   - classification: 0.30
   - plasma_physics: 0.25
   - engineering: 0.15
   - fuel_cycle: 0.15
   - operations: 0.15

3. **FR-3**: The overall score formula MUST be:
   ```
   overall = sum(weight_d * score_d for d in dimensions where comparable > 0)
            / sum(weight_d for d in dimensions where comparable > 0)
   ```
   Dimensions with 0 comparable fields are excluded and their weight redistributes proportionally.

4. **FR-4**: The classification dimension MUST appear in `PairComparison.dimensions` as a `DimensionScore` with `dimension="classification"`, `comparable=1`, and `matched_fields`/`mismatched_fields` reflecting the hierarchy levels compared.

5. **FR-5**: The `SimilarityMatrix.by_dimension` dict MUST include a `"classification"` key with the pairwise classification scores.

6. **FR-6**: Weights MUST be defined as module-level constants (dicts at the top of `similarity.py`), not hardcoded inline.

7. **FR-7**: [INFERRED] Existing API response shapes (`PairComparison`, `DimensionScore`, `SimilarityResult`, `SimilarityMatrix`, `ConstellationData`) MUST NOT change structurally. Only numerical values change.

8. **FR-8**: A diagnostic script MUST exist that prints a reference comparison table (the pairs from the research document) showing current scores vs expected ranges, as a quick intuition-check tool.

### Non-Functional Requirements

- Similarity matrix computation SHOULD remain fast enough for server startup precomputation (currently ~38x38 = 703 pairs, each doing field comparisons — adding a tree walk is negligible).

---

## Acceptance Criteria

### Core Functionality

- [ ] Two compact HTS tokamaks (01 vs 28) score > 0.75
- [ ] Two QI stellarators (09 vs 10) score > 0.75
- [ ] Two MIF concepts (07 vs 08) score > 0.40
- [ ] Two magnetic mirrors with different fuel (11 vs 06) score > 0.45
- [ ] Two dipoles with different fuel (12 vs 19) score > 0.40
- [ ] Tokamak vs Laser IFE (01 vs 17b) score < 0.35
- [ ] Tokamak vs Electrostatic (01 vs 13) score < 0.20
- [ ] Two indirect drive lasers (26 vs 30) score > 0.95
- [ ] `compare_pair(a, a)` still returns 1.0 for any concept
- [ ] `compare_pair(a, b) == compare_pair(b, a)` (symmetry preserved)

### Ordering Invariants

- [ ] Same-topology pairs score higher than cross-topology same-family pairs (on average)
- [ ] Same-family pairs score higher than cross-family pairs (on average)
- [ ] Stellarators more similar to each other than a tokamak is to a laser IFE (existing test, should still pass)

### Diagnostic Script

- [ ] Script runs standalone (e.g., `uv run python scripts/similarity_diagnostic.py`)
- [ ] Prints reference pair table with concept names, scores, and pass/fail against expected ranges
- [ ] Exit code 0 if all pairs within expected ranges, non-zero otherwise

### Quality & Integration

- [ ] All existing tests in `test_similarity.py` pass (with updated thresholds where needed)
- [ ] Server starts and serves constellation + similarity API endpoints without error
- [ ] `SimilarityMatrix.by_dimension` includes "classification" key
- [ ] No changes to frontend code required

---

## Related Artifacts

- **Research:** `.project/research/20260412-similarity-metric-improvements.md`
- **Design:** `.project/active/similarity-metric-v2/design.md` (to be created)
- **Code:** `exploration/concept_explorer/similarity.py` (primary file to modify)
- **Tests:** `exploration/concept_explorer/tests/test_similarity.py`
- **Data:** `exploration/concept_explorer/data/concept_registry.json` (read-only, no changes needed)

---

**Next Steps:** After approval, proceed to `/_my_design`
