# Design: Similarity Metric v2 — Hierarchical Classification + Dimension Weights

**Status:** Draft
**Owner:** Reid W
**Created:** 2026-04-12 17:04 PDT
**Updated:** 2026-04-12 17:30 PDT
**Branch:** 13-16-17b
**Commit:** 3e14589

---

## Overview

Add a hierarchical classification dimension to the similarity engine and introduce dimension-level weights, so "what kind of machine is this" dominates the similarity signal while cross-cutting design attributes provide secondary differentiation.

## Related Artifacts

- **Spec:** `.project/active/similarity-metric-v2/spec.md`
- **Research:** `.project/research/20260412-similarity-metric-improvements.md`
- **Primary code:** `exploration/concept_explorer/similarity.py`
- **Tests:** `exploration/concept_explorer/tests/test_similarity.py`
- **Taxonomy model:** `exploration/concept_explorer/taxonomy_models.py`

---

## Research Findings

### Existing Code Structure

**`similarity.py`** has a clean separation:
- **Lines 23-28**: `SIMILARITY_DIMENSIONS` dict — 4 dimensions, 9 fields. Module-level constant. Easy to add to.
- **Lines 138-196**: `compare_pair()` — iterates dimensions, computes per-dimension `matches/comparable`, then flat `total_matches / total_comparable` for overall. This is the main function to modify.
- **Lines 308-337**: `compute_similarity_matrix()` — builds NxN matrix by calling `compare_pair()` for each pair. Also builds per-dimension sub-matrices from `comp.dimensions`. Needs to handle the new "classification" dimension in `by_dimension`.
- **Lines 340-405**: `compute_constellation()` — pure function of the matrix. No changes needed.

**`taxonomy_models.py`** already has the full hierarchy:
- `ConceptTaxonomy` (line 185) has all 8 hierarchy fields: `confinement_family`, `mfe_topology`, `ife_driver`, `mif_method`, `non_standard_mechanism`, `tokamak_shape`, `stellarator_type`, `laser_approach`
- `_validate_hierarchy()` (line 219) enforces the tree structure — exactly one level-2 field per family, level-3 only for applicable topologies. This validation guarantees we can rely on field presence/absence to navigate the tree.

**Hierarchy tree** (from enums + validator):
```
ConfinementFamily
├── MFE → mfe_topology
│   ├── Tokamak → tokamak_shape (optional)
│   ├── Stellarator → stellarator_type (optional)
│   ├── Open/Linear (no level-3)
│   ├── Compact Toroid (no level-3)
│   └── Dipole (no level-3)
├── IFE → ife_driver
│   └── Laser → laser_approach (optional)
│   [Projectile, Heavy ion beam, Acoustic have no level-3]
├── MIF → mif_method (no level-3)
└── NONSTANDARD → non_standard_mechanism (no level-3)
```

**Key insight**: Level-3 is optional even when structurally valid (e.g., a tokamak may have `tokamak_shape=None`). The spec handles this correctly — level-3 N/A yields 0.75, not a penalty.

### Data Model Constraints

- `PairComparison` has `overall_matches: int` and `overall_comparable: int`. With weighted scoring, these fields lose precise meaning (the overall score is no longer `matches/comparable`). **Decision needed**: keep them as legacy aggregate counts, or repurpose.
- `DimensionScore` has `matches: int`, `comparable: int`, `matched_fields`, `mismatched_fields`. For the classification dimension, `comparable` is always 1 and `matches` is 0 or 1 (or fractional, which doesn't fit `int`). Need to adapt — see design below.

### Test Impact

Existing tests use:
- **Absolute thresholds**: `> 0.5`, `< 0.5` — these will shift but likely still hold since same-type scores go up and cross-type go down
- **Relative comparisons**: "stellarators more similar than cross-family" — will still hold, more strongly
- **Structural tests**: matrix shape, symmetry, diagonal=1.0, dimension keys — the `by_dimension` key assertion on line 239 needs updating to include "classification"

---

## Proposed Design

### 1. Module-Level Constants

Add at the top of `similarity.py` (after `SIMILARITY_DIMENSIONS`):

```python
# Hierarchy tree structure — derived from taxonomy_models._validate_hierarchy().
# Update both if hierarchy changes.

# Family → level-2 field name
_FAMILY_TO_LEVEL2: dict[str, str] = {
    "MFE": "mfe_topology",
    "IFE": "ife_driver",
    "MIF": "mif_method",
    "NONSTANDARD": "non_standard_mechanism",
}

# Topology/driver → level-3 field name (only where level-3 exists)
_LEVEL2_TO_LEVEL3: dict[str, str] = {
    "Tokamak": "tokamak_shape",
    "Stellarator": "stellarator_type",
    "Laser": "laser_approach",
}

DIMENSION_WEIGHTS: dict[str, float] = {
    "classification": 0.30,
    "plasma_physics": 0.25,
    "engineering": 0.15,
    "fuel_cycle": 0.15,
    "operations": 0.15,
}

# Consistency check: every dimension must have a weight and vice versa
assert set(DIMENSION_WEIGHTS.keys()) == set(SIMILARITY_DIMENSIONS.keys()) | {"classification"}, (
    "DIMENSION_WEIGHTS keys must match SIMILARITY_DIMENSIONS keys + 'classification'"
)
```

The `_FAMILY_TO_LEVEL2` and `_LEVEL2_TO_LEVEL3` dicts encode the tree structure from the enums. They're small, static, and derived directly from the `_validate_hierarchy()` logic in `taxonomy_models.py:219-285`. The module-level assertion ensures `DIMENSION_WEIGHTS` stays in sync with `SIMILARITY_DIMENSIONS` — if a dimension is added to one but not the other, the module fails to import.

### 2. Hierarchy Classification Function

New private function in `similarity.py`:

```python
def _compute_classification_score(a: ConceptTaxonomy, b: ConceptTaxonomy) -> tuple[float, list[str], list[str]]:
    """Walk the taxonomy hierarchy tree and return (score, matched_levels, mismatched_levels).
    
    Scoring:
      different family         → 0.0
      same family, diff L2     → 0.5
      same family+L2, L3 N/A  → 0.75
      same family+L2, diff L3  → 0.75
      same family+L2+L3       → 1.0
    """
```

Returns `(score, matched_fields, mismatched_fields)` where the field lists use descriptive names like `"confinement_family"`, `"mfe_topology"`, `"tokamak_shape"` — same strings used in the taxonomy model. This keeps the `DimensionScore.matched_fields` / `mismatched_fields` informative.

**Algorithm**:
1. Compare `confinement_family`. If different → `(0.0, [], ["confinement_family"])`
2. Get level-2 field for this family from `_FAMILY_TO_LEVEL2`. Compare values. If different → `(0.5, ["confinement_family"], ["<level2_field>"])`
3. Check if level-3 exists for this level-2 value (via `_LEVEL2_TO_LEVEL3`). If no level-3 field defined → `(0.75, ["confinement_family", "<level2>"], [])`
4. Get level-3 values. If either is None → `(0.75, ["confinement_family", "<level2>"], [])`
5. If level-3 values match → `(1.0, ["confinement_family", "<level2>", "<level3>"], [])`
6. If level-3 values differ → `(0.75, ["confinement_family", "<level2>"], ["<level3>"])`

### 3. Modified `compare_pair()`

The existing loop over `SIMILARITY_DIMENSIONS` stays unchanged. After it, add the classification dimension and compute the weighted overall:

```python
def compare_pair(a: ConceptTaxonomy, b: ConceptTaxonomy) -> PairComparison:
    # ... existing dimension loop (unchanged) ...
    
    # Classification dimension
    cls_score, cls_matched, cls_mismatched = _compute_classification_score(a, b)
    # For classification, comparable = total hierarchy levels evaluated (1–3),
    # matches = levels that matched. Derived from the field lists so
    # matches ≤ comparable always holds. The score field carries the
    # authoritative tree-walk value (0.0/0.5/0.75/1.0) — note that
    # matches/comparable ≠ score for this dimension (e.g., 2/2 → 0.75, not 1.0).
    dim_scores.append(DimensionScore(
        dimension="classification",
        matches=len(cls_matched),
        comparable=len(cls_matched) + len(cls_mismatched),
        score=cls_score,
        matched_fields=cls_matched,
        mismatched_fields=cls_mismatched,
    ))
    
    # Weighted overall score
    weighted_sum = 0.0
    weight_sum = 0.0
    for ds in dim_scores:
        w = DIMENSION_WEIGHTS.get(ds.dimension, 0.0)
        if ds.comparable > 0:
            weighted_sum += w * ds.score
            weight_sum += w
    overall = weighted_sum / weight_sum if weight_sum > 0 else 0.0
    
    return PairComparison(
        concept_a_id=a.concept_id,
        concept_b_id=b.concept_id,
        overall_score=overall,
        overall_matches=total_matches,      # legacy: design-dimension matches only
        overall_comparable=total_comparable, # legacy: design-dimension comparable only
        dimensions=dim_scores,
    )
```

**`overall_matches` / `overall_comparable`**: These remain as aggregate counts of the 4 design-attribute dimensions (not including classification). The classification score is fractional (0.0/0.5/0.75/1.0), so it doesn't map to integer match counts. The `overall_score` is the authoritative metric; the match/comparable fields are retained for backward compatibility but no longer derive the overall score. This is an acceptable semantic shift — the fields were always secondary to `overall_score` in API consumers (the frontend uses `overall_score` exclusively).

**Docstring update required**: `PairComparison.overall_matches` and `overall_comparable` must be annotated to clarify they reflect design-attribute dimensions only and do not derive `overall_score`. Similarly, `DimensionScore.score`'s docstring ("matches / comparable, or 0.0 if comparable == 0") must note that the classification dimension uses a tree-walk score instead.

### 4. Modified `compute_similarity_matrix()`

Update `similarity.py:308-337` to include `"classification"` in `by_dimension`:

```python
def compute_similarity_matrix(registry: ConceptRegistry) -> SimilarityMatrix:
    n = len(registry.concepts)
    concept_ids = [c.concept_id for c in registry.concepts]

    overall = [[0.0] * n for _ in range(n)]
    # All dimensions including classification
    all_dim_names = list(DIMENSION_WEIGHTS.keys())
    by_dimension: dict[str, list[list[float]]] = {
        d: [[0.0] * n for _ in range(n)] for d in all_dim_names
    }

    for i in range(n):
        overall[i][i] = 1.0
        for d in all_dim_names:
            by_dimension[d][i][i] = 1.0
        for j in range(i + 1, n):
            comp = compare_pair(registry.concepts[i], registry.concepts[j])
            overall[i][j] = comp.overall_score
            overall[j][i] = comp.overall_score
            for ds in comp.dimensions:
                by_dimension[ds.dimension][i][j] = ds.score
                by_dimension[ds.dimension][j][i] = ds.score

    return SimilarityMatrix(
        concept_ids=concept_ids,
        overall=overall,
        by_dimension=by_dimension,
    )
```

The key change: `all_dim_names` is derived from `DIMENSION_WEIGHTS.keys()` instead of `SIMILARITY_DIMENSIONS.keys()`, so it includes `"classification"`. This is safe because the module-level assertion (section 1) guarantees `DIMENSION_WEIGHTS` keys stay in sync with `SIMILARITY_DIMENSIONS` keys + `"classification"`.

### 5. Diagnostic Script

New file: `scripts/similarity_diagnostic.py`

Standalone script that:
1. Loads `concept_registry.json`
2. Runs `compare_pair()` on a reference set of pairs (from the research doc)
3. Prints a formatted table: concept A, concept B, score, expected range, PASS/FAIL
4. Exits 0 if all pass, 1 if any fail

Reference pairs and expected ranges (from spec acceptance criteria):

| Pair | Slugs | Expected |
|------|-------|----------|
| Two compact HTS tokamaks | `hts-compact-tokamak` vs `compact-hts-tokamak-china` | > 0.75 |
| Two QI stellarators | `qi-stellarator-hts` vs `large-scale-stellarator` | > 0.75 |
| Two MIF concepts | `magnetized-target-fusion` vs `frc-compression-fusion` | > 0.40 |
| Two mirrors diff fuel | `open-magnetic-mirror-dt` vs `axisymmetric-mirror-dhe3` | > 0.45 |
| Two dipoles diff fuel | `levitated-dipole-dt` vs `levitated-dipole-dd` | > 0.40 |
| Tokamak vs Laser IFE | `hts-compact-tokamak` vs `laser-icf-fast-ignition-d-t` | < 0.35 |
| Tokamak vs Electrostatic | `hts-compact-tokamak` vs `electrostatic-iec` | < 0.20 |
| Two indirect drive lasers | `laser-icf-indirect-drive-dt` vs `laser-icf-indirect-drive-dt-2` | > 0.95 |

The script uses the same `compare_pair()` function the server uses — it's a true end-to-end check.

### 6. Test Updates

In `test_similarity.py`:

- **`TestSimilarityMatrix.test_has_dimension_matrices`** (line 236): Update expected keys to include `"classification"`:
  ```python
  assert set(matrix.by_dimension.keys()) == {
      "classification", "plasma_physics", "engineering", "fuel_cycle", "operations"
  }
  ```

- **Existing threshold tests**: The `> 0.5` and `< 0.5` thresholds should still pass (same-type scores go up, cross-type stay low), but verify after implementation.

- **New tests to add**:
  - `test_classification_dimension_present`: verify `compare_pair()` returns a dimension with `dimension="classification"`
  - `test_classification_same_subtype`: two compact tokamaks → classification score = 1.0
  - `test_classification_same_topology`: compact tok vs spherical tok → classification score = 0.75
  - `test_classification_same_family`: tokamak vs stellarator → classification score = 0.5
  - `test_classification_different_family`: tokamak vs laser IFE → classification score = 0.0
  - `test_weighted_overall_higher_for_same_type`: two compact HTS tokamaks score > 0.75
  - `test_weighted_overall_lower_for_cross_family`: tokamak vs electrostatic < 0.20

---

## Potential Risks

1. **Slug lookup failures in diagnostic script**: If concept slugs change, the script fails. Mitigated by using slugs that match `concept_registry.json` and failing loudly with the missing slug name.

2. **`overall_matches`/`overall_comparable` semantic drift**: These fields no longer derive the overall score. Any downstream code that recomputes `matches/comparable` expecting it to equal `overall_score` would break. Checked: the frontend uses `overall_score` directly; the bridge logic in `explain_difference()` uses `compare_pair().overall_score`; no code divides `overall_matches / overall_comparable`.

3. **MDS constellation shape change**: Expected and desired per spec. The variance_explained may shift — if it drops significantly, that's a signal the new metric introduces noise, not signal. Worth checking but not a blocker.

---

## Integration Strategy

- **No frontend changes**: The constellation and neighborhood views consume `overall_score` and `by_dimension` — both continue to work. The new `"classification"` key in `by_dimension` is additive.
- **Server startup**: `compute_similarity_matrix()` is called at startup. The new classification computation adds ~38x38 = 1444 tree walks (each ~3 comparisons) — negligible overhead.
- **API contracts**: `PairComparison` and `SimilarityMatrix` shapes are unchanged (FR-7). The `dimensions` list gains one entry; `by_dimension` gains one key. Both are additive.

---

## Validation Approach

1. **Unit tests**: New classification-specific tests + updated existing tests (see section 6)
2. **Diagnostic script**: Run `uv run python scripts/similarity_diagnostic.py` to verify all reference pairs meet expected ranges
3. **Visual check**: Start server, open constellation view, confirm concepts cluster by confinement family
4. **Full test suite**: `uv run python -m pytest exploration/concept_explorer/tests/test_similarity.py`

---

**Next Step:** After approval → `/_my_plan` or `/_my_implement`
