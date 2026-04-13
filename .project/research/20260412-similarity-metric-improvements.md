---
date: 2026-04-12T10:00:00-05:00
researcher: Claude
topic: "Concept explorer similarity metric — missing taxonomy data and weighting"
tags: [research, similarity, concept-explorer, taxonomy]
status: complete
last_updated: 2026-04-12
---

# Research: Similarity Metric Improvements

**Date**: 2026-04-12
**Researcher**: Claude
**Research Type**: Architecture / Feasibility

## Research Question

The concept explorer's similarity map doesn't align with domain intuition. Two compact HTS tokamaks score only 0.571 similarity. Two QI stellarators score 0.625. Two magnetic mirrors with different fuel score 0.333. What's wrong, and how should the metric be improved?

## Summary

- **The similarity engine ignores the entire hierarchical classification** (confinement_family, mfe_topology, tokamak_shape, stellarator_type, ife_driver, laser_approach, mif_method, non_standard_mechanism) — 8 fields that encode "what kind of machine this is"
- **All 9 used fields have equal weight**, so `repetition_rate` counts the same as `fuel`
- **Variable comparability distorts scores**: cross-family pairs often have 6-7 comparable fields vs 8 for same-family, inflating or deflating ratios unpredictably
- These three issues combine to produce counter-intuitive results where structurally similar concepts (same topology, same shape) can score lower than structurally dissimilar ones

## Detailed Findings

### Problem 1: Missing Hierarchical Fields

The similarity engine uses only cross-cutting design attributes:

```
SIMILARITY_DIMENSIONS = {
    "plasma_physics": ["fuel", "primary_heating", "plasma_state"],
    "engineering": ["magnet_type", "energy_capture"],
    "fuel_cycle": ["tritium_breeding", "neutron_management"],
    "operations": ["operation_mode", "repetition_rate"],
}
```

**Not used** (8 fields):
- `confinement_family` (MFE/IFE/MIF/NONSTANDARD)
- `mfe_topology` (Tokamak/Stellarator/Open-Linear/Compact Toroid/Dipole)
- `tokamak_shape` (Compact/Spherical/Negative triangularity/Standard)
- `stellarator_type` (Planar coil/QI/Modular/Helical coil)
- `ife_driver` (Laser/Projectile/Heavy ion beam/Acoustic)
- `laser_approach` (6 subtypes)
- `mif_method` (FRC compression/Magnetized target)
- `non_standard_mechanism` (Electrostatic/Muon-catalyzed/Plasma focus)

These fields are the primary way domain experts classify fusion concepts. Not including them is like comparing cars without knowing if they're sedans or trucks.

**Impact**: Two compact HTS tokamaks (CFS #01 vs Energy Singularity #28) score only 0.571 because the metric doesn't know they're both compact tokamaks. It only sees that they share fuel, heating, plasma_state (3/3), one of two engineering fields (1/2), differ on tritium_breeding (0/1), and differ on operation_mode (0/1).

### Problem 2: Flat Weighting

Every comparable field contributes equally to `overall_score = total_matches / total_comparable`. This means:

| Field | Domain importance | Current weight |
|-------|------------------|----------------|
| `fuel` | Fundamental physics choice (determines neutronics, blanket, entire fuel cycle) | 1/9 |
| `confinement_family` | Top-level machine classification | **not used** |
| `repetition_rate` | Engineering detail, often unknown | 1/9 |
| `tritium_breeding` | Important but many concepts have TBD | 1/9 |

A mismatch on `repetition_rate` counts the same as a mismatch on `fuel`. Intuitively, two D-T tokamaks with different rep rates should be much more similar than two pulsed machines with different fuel.

### Problem 3: Variable Comparability

The N/A and TBD exclusion rules mean different pairs have different denominators:

| Pair | Comparable fields | Notes |
|------|-------------------|-------|
| Two stellarators | 8/9 | Both have most fields populated, rep_rate null |
| Two MIF concepts | 8/9 | Both have most fields |
| Tokamak vs Laser IFE | 7/9 | IFE has null magnet_type |
| Two mirrors (diff fuel) | 6/9 | Several TBD/null fields |

This isn't inherently wrong, but it interacts badly with flat weighting. A pair with 3/6 comparable = 0.500 looks the same as 4/8 = 0.500, but the first has much less information.

### Concrete Counter-Intuitive Results

| Pair | Score | Intuitive? | Why wrong |
|------|-------|------------|-----------|
| Two compact HTS tokamaks (01 vs 28) | 0.571 | Should be ~0.9 | Doesn't know they're both compact tokamaks |
| Two QI stellarators (09 vs 10) | 0.625 | Should be ~0.85 | Doesn't know they're both QI stellarators |
| QI vs Planar stellarator (09 vs 05) | 0.750 | Should be ~0.7 | Actually not too bad — stellarator identity captured by shared field values |
| Two MIF concepts (07 vs 08) | 0.250 | Should be ~0.5 | Doesn't know they're both MIF; differ on fuel, heating, everything else |
| Two mirrors, diff fuel (11 vs 06) | 0.333 | Should be ~0.55 | Doesn't know they're both Open/Linear MFE |
| Two dipoles, diff fuel (12 vs 19) | 0.286 | Should be ~0.5 | Doesn't know they're both dipoles |
| Compact tok vs Spherical tok (01 vs 21) | 0.625 | Should be ~0.75 | Doesn't know they're both tokamaks |
| Two indirect drive lasers (26 vs 30) | 1.000 | Correct | Identical on all cross-cutting fields |

### What the Hierarchical Fields Would Add

The hierarchy is a tree:
```
ConfinementFamily
├── MFE → MFETopology
│   ├── Tokamak → TokamakShape
│   ├── Stellarator → StellaratorType
│   ├── Open/Linear
│   ├── Compact Toroid
│   └── Dipole
├── IFE → IFEDriver
│   └── Laser → LaserApproach
├── MIF → MIFMethod
└── NONSTANDARD → NonStandardMechanism
```

The challenge: these are **sparse** fields. A tokamak has `confinement_family=MFE, mfe_topology=Tokamak, tokamak_shape=Compact` but null for `ife_driver`, `laser_approach`, `mif_method`, etc. Two tokamaks both have null `ife_driver` — that's not a meaningful match, it's structural absence.

**Naive approach** (just add all 8 fields): Would inflate similarity between any same-family pair due to shared nulls, and wouldn't properly handle the tree structure.

## Proposed Approach: Hierarchical Similarity + Dimension Weights

### A. Hierarchical Classification Score

Instead of adding individual hierarchy fields to the flat comparison, compute a **hierarchical classification similarity** that walks the tree:

```python
HIERARCHY_SCORES = {
    "same_family": 0.5,        # Both MFE
    "same_topology": 0.75,     # Both Tokamak (implies same family)
    "same_subtype": 1.0,       # Both Compact Tokamak (implies same topology)
    "different_family": 0.0,   # MFE vs IFE
}
```

**Algorithm**:
1. If `confinement_family` differs → 0.0
2. If same family, check level 2 (mfe_topology / ife_driver / mif_method / non_standard_mechanism)
   - If level 2 differs → 0.5 (same family, different topology)
   - If level 2 matches → check level 3 (tokamak_shape / stellarator_type / laser_approach)
     - If level 3 N/A for both or either → 0.75 (no further distinction available)
     - If level 3 matches → 1.0
     - If level 3 differs → 0.75 (same topology, different variant)

This produces a single 0-1 score for the "classification" dimension. It naturally handles the sparseness problem because it only walks the relevant branch.

**Cross-family partial credit**: One could argue MFE↔MIF should score higher than MFE↔NONSTANDARD (MIF shares some magnetic confinement physics). This is debatable and could be a refinement, but the tree-walk approach above is a clean first implementation.

### B. Dimension Weights

Replace the flat `total_matches / total_comparable` with weighted dimension scores:

```python
DIMENSION_WEIGHTS = {
    "classification": 0.30,   # NEW: hierarchical classification
    "plasma_physics": 0.25,   # fuel, primary_heating, plasma_state
    "engineering": 0.15,      # magnet_type, energy_capture
    "fuel_cycle": 0.15,       # tritium_breeding, neutron_management
    "operations": 0.15,       # operation_mode, repetition_rate
}
```

**Rationale for weights**:
- **Classification (0.30)**: The single most important factor — "what kind of machine is this?" This is what domain experts use first when comparing concepts.
- **Plasma physics (0.25)**: Fuel choice and heating method are fundamental physics decisions that drive most of the cost structure.
- **Engineering, Fuel cycle, Operations (0.15 each)**: Important but more interchangeable across concepts. Two tokamaks with different blankets are still very similar machines.

The overall score becomes:
```
overall = sum(weight_d * score_d for d in dimensions) / sum(weight_d for d in dimensions where comparable > 0)
```

Note: dimensions with 0 comparable fields are excluded from the weighted average (their weight redistributes to others), preserving the current TBD/N/A handling.

### C. Optional: Within-Dimension Field Weights

For finer control, fields within a dimension could also be weighted:

```python
FIELD_WEIGHTS = {
    "fuel": 2.0,              # Most fundamental choice
    "primary_heating": 1.0,
    "plasma_state": 1.0,
    "magnet_type": 1.5,       # Major engineering differentiator
    "energy_capture": 1.0,
    "tritium_breeding": 1.0,
    "neutron_management": 1.0,
    "operation_mode": 1.5,    # Steady-state vs pulsed is fundamental
    "repetition_rate": 0.5,   # Often unknown, least discriminating
}
```

This adds complexity. Recommend starting with dimension-level weights only and adding field weights if dimension weights alone don't resolve the intuition gaps.

### D. Projected Impact

With the proposed changes, estimated scores (rough calculation):

| Pair | Current | Estimated | Change |
|------|---------|-----------|--------|
| Two compact HTS tokamaks | 0.571 | ~0.85 | +0.28 |
| Two QI stellarators | 0.625 | ~0.83 | +0.21 |
| Two MIF (magnetized target) | 0.250 | ~0.50 | +0.25 |
| Two mirrors (diff fuel) | 0.333 | ~0.55 | +0.22 |
| Two dipoles (diff fuel) | 0.286 | ~0.52 | +0.23 |
| Tokamak vs Laser IFE | 0.429 | ~0.28 | -0.15 |
| Tokamak vs Electrostatic | 0.143 | ~0.10 | -0.04 |
| Two indirect drive lasers | 1.000 | ~1.00 | 0.00 |

The pattern: same-type concepts move up significantly, cross-type concepts move down slightly. This matches domain intuition.

## Code References

- `exploration/concept_explorer/similarity.py:23-28` — `SIMILARITY_DIMENSIONS` dict (the 4 dimensions, 9 fields)
- `exploration/concept_explorer/similarity.py:138-196` — `compare_pair()` core algorithm
- `exploration/concept_explorer/similarity.py:187` — flat `total_matches / total_comparable` scoring
- `exploration/concept_explorer/similarity.py:308-337` — `compute_similarity_matrix()` (builds overall + per-dimension matrices)
- `exploration/concept_explorer/similarity.py:340-405` — `compute_constellation()` (MDS projection)
- `exploration/concept_explorer/taxonomy_models.py:185-286` — `ConceptTaxonomy` model with all available fields
- `exploration/concept_explorer/taxonomy_models.py:219-285` — `_validate_hierarchy()` — existing tree validation logic (can inform hierarchy walk)
- `exploration/concept_explorer/data/concept_registry.json` — 38 concepts with full taxonomy data
- `exploration/concept_explorer/tests/test_similarity.py` — existing tests (threshold-based, will need updating)

## Feasibility Assessment

**Complexity**: Low-medium. The hierarchical score is ~30 lines of new code. Dimension weights are a small change to `compare_pair()` and `compute_similarity_matrix()`.

**Risks**:
- Test thresholds in `test_similarity.py` will need updating (e.g., "QI stellarators score > 0.5" → "> 0.7")
- The constellation MDS projection will change shape — need to verify it still looks reasonable
- Frontend (`neighborhood_graph.js`, `constellation.js`) reads similarity scores but doesn't hardcode thresholds, so should adapt automatically
- The `SimilarityMatrix.by_dimension` dict will gain a "classification" key — downstream consumers need to handle this

**Dependencies**: None. The hierarchy data is already in `ConceptTaxonomy` and `concept_registry.json`.

**Breaking changes**: The API response shapes don't change (still `PairComparison` with `DimensionScore` list), but the numerical values will shift. Any cached/serialized similarity data would need regeneration.

## Recommendations

1. **Start with classification dimension + dimension weights** (proposals A + B above). This addresses the two biggest problems (missing hierarchy, flat weighting) with minimal code change.

2. **Defer within-dimension field weights** (proposal C) until after evaluating A+B. They may not be needed.

3. **Add a diagnostic script** that prints the comparison table from this research (the "intuitive?" column) as a regression test. When tweaking weights, run it to verify intuition alignment.

4. **Consider making weights configurable** (a dict constant at module top, not hardcoded in the algorithm). This allows tuning without code changes and could eventually be exposed as a UI control.

5. **Update test expectations** to reflect the new score ranges. The existing tests use relative comparisons ("stellarators more similar than cross-family") which should still pass, but absolute thresholds will shift.

## Open Questions

1. **Cross-family partial credit**: Should MFE↔MIF score higher than MFE↔NONSTANDARD at the classification level? There's a physics argument for it (MIF uses magnetic fields), but it adds subjective judgment to the metric.

2. **Confidence as a factor**: Should `confidence` (high/medium/low) affect similarity? A low-confidence concept with many TBD fields already gets fewer comparable dimensions, but should it be explicitly downweighted?

3. **Weight tuning methodology**: How to systematically validate weights beyond spot-checking? Could survey domain experts or use a small set of "ground truth" similarity judgments as a calibration set.

4. **driver_technology**: This free-text field is currently unused. It could be valuable but would require semantic similarity (not exact match) — likely not worth the complexity.
