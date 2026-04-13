"""Similarity engine for concept taxonomy comparison.

Computes pairwise categorical similarity between fusion concepts,
decomposed by functional dimension. Includes nearest-neighbor ranking,
bridge concept identification, full similarity matrix, and classical
MDS projection for 2D constellation visualization.

See design.md DD-4 for the similarity metric rationale.
"""

from __future__ import annotations

import numpy as np
from pydantic import BaseModel

from exploration.concept_explorer.models import ConfinementFamily
from exploration.concept_explorer.taxonomy_models import ConceptRegistry, ConceptTaxonomy

# ---------------------------------------------------------------------------
# Dimension definitions
# ---------------------------------------------------------------------------

SIMILARITY_DIMENSIONS: dict[str, list[str]] = {
    "plasma_physics": ["fuel", "primary_heating", "plasma_state"],
    "engineering": ["magnet_type", "energy_capture"],
    "fuel_cycle": ["tritium_breeding", "neutron_management"],
    "operations": ["operation_mode", "repetition_rate"],
}

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

# Sentinel values that indicate "unknown / not yet determined"
_TBD_SENTINELS = {"TBD", "Unknown"}


# ---------------------------------------------------------------------------
# Result models
# ---------------------------------------------------------------------------


class DimensionScore(BaseModel):
    """Similarity score for one functional dimension."""

    dimension: str
    matches: int
    comparable: int
    score: float  # matches / comparable, or 0.0 if comparable == 0
    matched_fields: list[str]
    mismatched_fields: list[str]


class PairComparison(BaseModel):
    """Full comparison between two concepts."""

    concept_a_id: str
    concept_b_id: str
    overall_score: float
    overall_matches: int
    overall_comparable: int
    dimensions: list[DimensionScore]


class DifferenceBridge(BaseModel):
    """For a mismatched field, which other concept matches the query."""

    dimension: str
    mismatched_field: str
    query_value: str
    similar_value: str
    bridge_concept_id: str
    bridge_concept_name: str
    bridge_overall_similarity: float


class SimilarityResult(BaseModel):
    """A single entry in a nearest-neighbor ranking."""

    concept_id: str
    concept_name: str
    confinement_family: ConfinementFamily
    comparison: PairComparison
    bridges: list[DifferenceBridge]


class ConceptSimilarityReport(BaseModel):
    """Complete similarity report for one concept."""

    query_concept_id: str
    query_concept_name: str
    nearest: list[SimilarityResult]


class SimilarityMatrix(BaseModel):
    """Full pairwise similarity matrix."""

    concept_ids: list[str]
    overall: list[list[float]]
    by_dimension: dict[str, list[list[float]]]


class ConstellationPoint(BaseModel):
    """A single concept's position in the 2D MDS projection."""

    concept_id: str
    name: str
    confinement_family: ConfinementFamily
    x: float
    y: float


class ConstellationData(BaseModel):
    """Full 2D projection of all concepts."""

    points: list[ConstellationPoint]
    variance_explained: float


# ---------------------------------------------------------------------------
# Helper
# ---------------------------------------------------------------------------


def _is_tbd(value: object) -> bool:
    """Check if a value is a TBD/Unknown sentinel."""
    if value is None:
        return False  # None = N/A, not TBD
    return str(value) in _TBD_SENTINELS


def _get_field(concept: ConceptTaxonomy, field: str) -> object:
    """Get a field value, returning None for N/A and the value for everything else."""
    return getattr(concept, field, None)


# ---------------------------------------------------------------------------
# Core algorithm
# ---------------------------------------------------------------------------


def _compute_classification_score(
    a: ConceptTaxonomy, b: ConceptTaxonomy,
) -> tuple[float, list[str], list[str]]:
    """Walk the taxonomy hierarchy tree and return (score, matched_levels, mismatched_levels).

    Scoring:
      different family         → 0.0
      same family, diff L2     → 0.5
      same family+L2, L3 N/A  → 0.75
      same family+L2, diff L3  → 0.75
      same family+L2+L3       → 1.0
    """
    # Level 1: confinement family
    if str(a.confinement_family) != str(b.confinement_family):
        return (0.0, [], ["confinement_family"])

    # Level 2: topology / driver / method / mechanism
    l2_field = _FAMILY_TO_LEVEL2[str(a.confinement_family)]
    val_a_l2 = getattr(a, l2_field, None)
    val_b_l2 = getattr(b, l2_field, None)

    if str(val_a_l2) != str(val_b_l2):
        return (0.5, ["confinement_family"], [l2_field])

    # Level 3: subtype (only exists for some level-2 values)
    l3_field = _LEVEL2_TO_LEVEL3.get(str(val_a_l2))
    if l3_field is None:
        # No level-3 defined for this topology/driver
        return (0.75, ["confinement_family", l2_field], [])

    val_a_l3 = getattr(a, l3_field, None)
    val_b_l3 = getattr(b, l3_field, None)

    if val_a_l3 is None or val_b_l3 is None:
        # Level-3 not specified for one or both
        return (0.75, ["confinement_family", l2_field], [])

    if str(val_a_l3) == str(val_b_l3):
        return (1.0, ["confinement_family", l2_field, l3_field], [])

    return (0.75, ["confinement_family", l2_field], [l3_field])


def compare_pair(a: ConceptTaxonomy, b: ConceptTaxonomy) -> PairComparison:
    """Compare two concepts across all similarity dimensions.

    Design-attribute dimensions (plasma_physics, engineering, fuel_cycle, operations):
    - If either concept has None (N/A) or TBD/Unknown: skip (not comparable)
    - If both have values: match (1) or mismatch (0)

    Classification dimension: tree-walk score (0.0/0.5/0.75/1.0) from
    ``_compute_classification_score()``.

    Overall score is a weighted average across dimensions with non-zero
    comparable fields, using ``DIMENSION_WEIGHTS``. ``overall_matches`` and
    ``overall_comparable`` reflect design-attribute dimensions only (legacy;
    do not derive overall_score from them).
    """
    total_matches = 0
    total_comparable = 0
    dim_scores: list[DimensionScore] = []

    for dim_name, fields in SIMILARITY_DIMENSIONS.items():
        matches = 0
        comparable = 0
        matched_fields: list[str] = []
        mismatched_fields: list[str] = []

        for field in fields:
            val_a = _get_field(a, field)
            val_b = _get_field(b, field)

            # Skip if either is N/A (None) or TBD
            if val_a is None or val_b is None:
                continue
            if _is_tbd(val_a) or _is_tbd(val_b):
                continue

            comparable += 1
            if str(val_a) == str(val_b):
                matches += 1
                matched_fields.append(field)
            else:
                mismatched_fields.append(field)

        score = matches / comparable if comparable > 0 else 0.0
        total_matches += matches
        total_comparable += comparable

        dim_scores.append(
            DimensionScore(
                dimension=dim_name,
                matches=matches,
                comparable=comparable,
                score=score,
                matched_fields=matched_fields,
                mismatched_fields=mismatched_fields,
            )
        )

    # Classification dimension (tree-walk, always comparable)
    cls_score, cls_matched, cls_mismatched = _compute_classification_score(a, b)
    dim_scores.append(
        DimensionScore(
            dimension="classification",
            matches=len(cls_matched),
            comparable=len(cls_matched) + len(cls_mismatched),
            score=cls_score,
            matched_fields=cls_matched,
            mismatched_fields=cls_mismatched,
        )
    )

    # Weighted overall score across all dimensions
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
        overall_matches=total_matches,
        overall_comparable=total_comparable,
        dimensions=dim_scores,
    )


def find_nearest(
    query: ConceptTaxonomy,
    registry: ConceptRegistry,
    top_n: int = 5,
) -> list[SimilarityResult]:
    """Find the top-N most similar concepts to the query concept."""
    results: list[tuple[float, ConceptTaxonomy, PairComparison]] = []

    for concept in registry.concepts:
        if concept.concept_id == query.concept_id:
            continue
        comparison = compare_pair(query, concept)
        results.append((comparison.overall_score, concept, comparison))

    # Sort by score descending, then by name for stability
    results.sort(key=lambda x: (-x[0], x[1].name))

    out: list[SimilarityResult] = []
    for _score, concept, comparison in results[:top_n]:
        bridges = explain_difference(query, concept, registry)
        out.append(
            SimilarityResult(
                concept_id=concept.concept_id,
                concept_name=concept.name,
                confinement_family=concept.confinement_family,
                comparison=comparison,
                bridges=bridges,
            )
        )
    return out


def explain_difference(
    query: ConceptTaxonomy,
    similar: ConceptTaxonomy,
    registry: ConceptRegistry,
) -> list[DifferenceBridge]:
    """For dimensions where query and similar differ, find which other
    concepts match query in those dimensions.

    This is the "70% like A, but in the 30% different, more like B and C" query.

    Uses greedy diverse selection: iterates fields in dimension order and
    prefers bridge concepts not yet used by a previous field. Falls back to
    the highest-scoring candidate when all candidates are already used.
    """
    comparison = compare_pair(query, similar)

    # Stage 1: collect all candidates per mismatched field, sorted by score desc
    fields_in_order: list[tuple[str, str, str, str]] = []  # (dimension, field, query_val, similar_val)
    candidates_by_field: dict[str, list[tuple[float, ConceptTaxonomy]]] = {}

    for dim_score in comparison.dimensions:
        for field in dim_score.mismatched_fields:
            query_val = _get_field(query, field)
            similar_val = _get_field(similar, field)
            if query_val is None or similar_val is None:
                continue

            fields_in_order.append((dim_score.dimension, field, str(query_val), str(similar_val)))
            candidates: list[tuple[float, ConceptTaxonomy]] = []
            for candidate in registry.concepts:
                if candidate.concept_id in (query.concept_id, similar.concept_id):
                    continue
                cand_val = _get_field(candidate, field)
                if cand_val is None or _is_tbd(cand_val):
                    continue
                if str(cand_val) == str(query_val):
                    cand_score = compare_pair(query, candidate).overall_score
                    candidates.append((cand_score, candidate))
            candidates.sort(key=lambda x: -x[0])
            candidates_by_field[field] = candidates

    # Stage 2: greedy diverse selection
    used_concept_ids: set[str] = set()
    bridges: list[DifferenceBridge] = []

    for dimension, field, query_val, similar_val in fields_in_order:
        candidates = candidates_by_field[field]
        if not candidates:
            continue

        # Prefer an unused concept
        selected: tuple[float, ConceptTaxonomy] | None = None
        for score, concept in candidates:
            if concept.concept_id not in used_concept_ids:
                selected = (score, concept)
                break

        # Fallback: reuse the best candidate
        if selected is None:
            selected = candidates[0]

        used_concept_ids.add(selected[1].concept_id)
        bridges.append(
            DifferenceBridge(
                dimension=dimension,
                mismatched_field=field,
                query_value=query_val,
                similar_value=similar_val,
                bridge_concept_id=selected[1].concept_id,
                bridge_concept_name=selected[1].name,
                bridge_overall_similarity=selected[0],
            )
        )

    return bridges


def compute_similarity_matrix(registry: ConceptRegistry) -> SimilarityMatrix:
    """Compute full pairwise similarity matrix for all concepts."""
    n = len(registry.concepts)
    concept_ids = [c.concept_id for c in registry.concepts]

    # Overall matrix
    overall = [[0.0] * n for _ in range(n)]
    # Per-dimension matrices (all dimensions including classification)
    dim_names = list(DIMENSION_WEIGHTS.keys())
    by_dimension: dict[str, list[list[float]]] = {
        d: [[0.0] * n for _ in range(n)] for d in dim_names
    }

    for i in range(n):
        overall[i][i] = 1.0
        for d in dim_names:
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


def compute_constellation(
    matrix: SimilarityMatrix,
    registry: ConceptRegistry,
) -> ConstellationData:
    """Project the similarity matrix to 2D via classical MDS.

    1. D = 1 - similarity (distance matrix)
    2. Double-center D^2 (subtract row/col means, add grand mean)
    3. Eigendecompose -> top 2 eigenvectors * sqrt(eigenvalues)
    """
    sim = np.array(matrix.overall)
    n = sim.shape[0]

    # Distance matrix
    dist = 1.0 - sim
    dist_sq = dist ** 2

    # Double centering: B = -0.5 * H @ D^2 @ H, where H = I - (1/n) * 11^T
    row_mean = dist_sq.mean(axis=1, keepdims=True)
    col_mean = dist_sq.mean(axis=0, keepdims=True)
    grand_mean = dist_sq.mean()
    B = -0.5 * (dist_sq - row_mean - col_mean + grand_mean)

    # Eigendecomposition (B is symmetric)
    eigenvalues, eigenvectors = np.linalg.eigh(B)

    # eigh returns ascending order; we want the top 2
    idx = np.argsort(eigenvalues)[::-1]
    eigenvalues = eigenvalues[idx]
    eigenvectors = eigenvectors[:, idx]

    # Take top 2 positive eigenvalues
    top2_vals = eigenvalues[:2]
    top2_vecs = eigenvectors[:, :2]

    # Clamp negative eigenvalues to small positive for sqrt
    top2_vals_clamped = np.maximum(top2_vals, 1e-10)
    coords = top2_vecs * np.sqrt(top2_vals_clamped)

    # Variance explained: sum of top 2 / sum of all positive eigenvalues
    positive_eigenvalues = eigenvalues[eigenvalues > 0]
    total_variance = positive_eigenvalues.sum()
    if total_variance > 0:
        variance_explained = float(top2_vals_clamped.sum() / total_variance)
    else:
        variance_explained = 0.0

    # Build points
    id_to_concept = {c.concept_id: c for c in registry.concepts}
    points: list[ConstellationPoint] = []
    for i, cid in enumerate(matrix.concept_ids):
        concept = id_to_concept[cid]
        points.append(
            ConstellationPoint(
                concept_id=cid,
                name=concept.name,
                confinement_family=concept.confinement_family,
                x=float(coords[i, 0]),
                y=float(coords[i, 1]),
            )
        )

    return ConstellationData(
        points=points,
        variance_explained=variance_explained,
    )
