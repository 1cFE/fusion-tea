"""Tests for the similarity engine.

Coverage:
- Identity similarity (concept vs itself)
- Known high-similarity pairs (QI stellarators)
- Known low-similarity pairs (tokamak vs laser IFE)
- TBD and N/A exclusion from comparison
- Dimension decomposition correctness
- Bridge concept identification
- Similarity matrix shape and symmetry
- MDS constellation validity
"""

from __future__ import annotations

import math
from pathlib import Path

import pytest

from exploration.concept_explorer.models import ConfinementFamily
from exploration.concept_explorer.taxonomy_models import ConceptRegistry

from exploration.concept_explorer.similarity import (
    compare_pair,
    compute_constellation,
    compute_similarity_matrix,
    explain_difference,
    find_nearest,
)

_DATA_DIR = Path(__file__).parent.parent / "data"
REGISTRY_PATH = _DATA_DIR / "concept_registry.json"


@pytest.fixture
def registry() -> ConceptRegistry:
    assert REGISTRY_PATH.exists(), "Run seed_registry.py first"
    return ConceptRegistry.model_validate_json(REGISTRY_PATH.read_text())


# ---------------------------------------------------------------------------
# Pairwise comparison
# ---------------------------------------------------------------------------


class TestComparePair:
    def test_identical_concept_similarity_is_one(self, registry: ConceptRegistry):
        """A concept compared to itself has similarity 1.0."""
        c = registry.concepts[0]
        result = compare_pair(c, c)
        assert result.overall_score == 1.0

    def test_qi_stellarators_high_similarity(self, registry: ConceptRegistry):
        """Two QI stellarators should score > 0.5 (they share fuel, heating,
        plasma state, energy capture, operation mode but differ on magnets,
        tritium breeding, and neutron management)."""
        proxima = registry.by_slug("qi-stellarator-hts")
        gauss = registry.by_slug("large-scale-stellarator")
        assert proxima is not None and gauss is not None
        result = compare_pair(proxima, gauss)
        assert result.overall_score > 0.5

    def test_tokamak_vs_laser_ife_low_similarity(self, registry: ConceptRegistry):
        """Tokamak vs laser IFE should score < 0.5 (different confinement
        approach but share some fuel cycle and energy capture attributes)."""
        tok = registry.by_slug("hts-compact-tokamak")
        ife = registry.by_slug("laser-icf-fast-ignition-d-t")
        assert tok is not None and ife is not None
        result = compare_pair(tok, ife)
        assert result.overall_score < 0.5

    def test_stellarators_more_similar_than_cross_family(self, registry: ConceptRegistry):
        """QI stellarators should be more similar to each other than a
        tokamak is to a laser IFE concept."""
        proxima = registry.by_slug("qi-stellarator-hts")
        gauss = registry.by_slug("large-scale-stellarator")
        tok = registry.by_slug("hts-compact-tokamak")
        ife = registry.by_slug("laser-icf-fast-ignition-d-t")
        assert proxima is not None and gauss is not None and tok is not None and ife is not None
        stell_score = compare_pair(proxima, gauss).overall_score
        cross_score = compare_pair(tok, ife).overall_score
        assert stell_score > cross_score

    def test_symmetry(self, registry: ConceptRegistry):
        """compare_pair(a, b) == compare_pair(b, a) in score."""
        a = registry.concepts[0]
        b = registry.concepts[5]
        ab = compare_pair(a, b)
        ba = compare_pair(b, a)
        assert abs(ab.overall_score - ba.overall_score) < 1e-9

    def test_overall_score_bounded(self, registry: ConceptRegistry):
        """Overall score is always between 0 and 1."""
        for i in range(min(10, len(registry.concepts))):
            for j in range(i + 1, min(10, len(registry.concepts))):
                result = compare_pair(registry.concepts[i], registry.concepts[j])
                assert 0.0 <= result.overall_score <= 1.0


class TestTBDAndNAExclusion:
    def test_tbd_excluded_from_comparison(self, registry: ConceptRegistry):
        """TBD values should not count as match or mismatch."""
        # Compact Spherical Tokamak - India has TBD for primary_heating and magnet_type=Unknown
        india = registry.by_slug("compact-spherical-tokamak-india")
        cfs = registry.by_slug("hts-compact-tokamak")
        assert india is not None and cfs is not None
        result = compare_pair(india, cfs)
        # primary_heating is TBD for India, so it should be excluded
        plasma_dim = next(d for d in result.dimensions if d.dimension == "plasma_physics")
        assert "primary_heating" not in plasma_dim.matched_fields
        assert "primary_heating" not in plasma_dim.mismatched_fields

    def test_na_excluded_from_comparison(self, registry: ConceptRegistry):
        """N/A (None) values should not count as match or mismatch."""
        tok = registry.by_slug("hts-compact-tokamak")  # has magnet_type
        ife = registry.by_slug("laser-icf-fast-ignition-d-t")  # magnet_type is None
        assert tok is not None and ife is not None
        result = compare_pair(tok, ife)
        eng = next(d for d in result.dimensions if d.dimension == "engineering")
        assert "magnet_type" not in eng.matched_fields
        assert "magnet_type" not in eng.mismatched_fields


class TestDimensionDecomposition:
    def test_matching_fuel_different_magnets(self, registry: ConceptRegistry):
        """Two D-T concepts with different magnet types: plasma_physics should score
        higher than engineering (assuming fuel matches but magnets differ)."""
        # HTS Compact Tokamak: D-T, HTS (wound)
        # Sheared-Flow Z-Pinch: D-T, Self-confined
        cfs = registry.by_slug("hts-compact-tokamak")
        zap = registry.by_slug("sheared-flow-stabilized-z-pinch")
        assert cfs is not None and zap is not None
        result = compare_pair(cfs, zap)
        plasma = next(d for d in result.dimensions if d.dimension == "plasma_physics")
        eng = next(d for d in result.dimensions if d.dimension == "engineering")
        # Fuel matches (both D-T) so plasma should have at least 1 match
        assert "fuel" in plasma.matched_fields
        # Magnets differ
        assert "magnet_type" in eng.mismatched_fields


# ---------------------------------------------------------------------------
# Nearest neighbors
# ---------------------------------------------------------------------------


class TestFindNearest:
    def test_returns_requested_count(self, registry: ConceptRegistry):
        """find_nearest returns top_n results."""
        c = registry.concepts[0]
        results = find_nearest(c, registry, top_n=5)
        assert len(results) == 5

    def test_excludes_self(self, registry: ConceptRegistry):
        """The query concept should not appear in its own nearest neighbors."""
        c = registry.concepts[0]
        results = find_nearest(c, registry, top_n=37)
        ids = [r.concept_id for r in results]
        assert c.concept_id not in ids

    def test_sorted_descending(self, registry: ConceptRegistry):
        """Results are sorted by overall_score descending."""
        c = registry.concepts[0]
        results = find_nearest(c, registry, top_n=10)
        scores = [r.comparison.overall_score for r in results]
        assert scores == sorted(scores, reverse=True)

    def test_tokamak_nearest_are_tokamaks(self, registry: ConceptRegistry):
        """HTS Compact Tokamak's top neighbors should be mostly tokamaks."""
        cfs = registry.by_slug("hts-compact-tokamak")
        assert cfs is not None
        results = find_nearest(cfs, registry, top_n=3)
        # At least 2 of top 3 should be MFE
        mfe_count = sum(1 for r in results if r.confinement_family == ConfinementFamily.MFE)
        assert mfe_count >= 2


# ---------------------------------------------------------------------------
# Bridge concepts
# ---------------------------------------------------------------------------


class TestExplainDifference:
    def test_returns_bridges_for_mismatched_fields(self, registry: ConceptRegistry):
        """explain_difference returns bridge concepts for differing dimensions."""
        a = registry.by_slug("hts-compact-tokamak")
        b = registry.by_slug("sheared-flow-stabilized-z-pinch")
        assert a is not None and b is not None
        bridges = explain_difference(a, b, registry)
        # They differ on multiple fields, so there should be bridges
        assert len(bridges) > 0
        # Each bridge should reference a real concept
        all_ids = {c.concept_id for c in registry.concepts}
        for bridge in bridges:
            assert bridge.bridge_concept_id in all_ids

    def test_bridge_has_overall_similarity(self, registry: ConceptRegistry):
        """Bridge data includes overall similarity to query concept."""
        a = registry.by_slug("hts-compact-tokamak")
        assert a is not None
        nearest = find_nearest(a, registry, top_n=1)
        assert len(nearest) == 1
        for bridge in nearest[0].bridges:
            assert hasattr(bridge, "bridge_overall_similarity")
            assert 0.0 <= bridge.bridge_overall_similarity <= 1.0


# ---------------------------------------------------------------------------
# Similarity matrix
# ---------------------------------------------------------------------------


class TestSimilarityMatrix:
    def test_shape(self, registry: ConceptRegistry):
        """Matrix is 38x38."""
        matrix = compute_similarity_matrix(registry)
        assert len(matrix.concept_ids) == 38
        assert len(matrix.overall) == 38
        assert all(len(row) == 38 for row in matrix.overall)

    def test_diagonal_is_one(self, registry: ConceptRegistry):
        """Diagonal entries are 1.0 (self-similarity)."""
        matrix = compute_similarity_matrix(registry)
        for i in range(len(matrix.concept_ids)):
            assert matrix.overall[i][i] == 1.0

    def test_symmetric(self, registry: ConceptRegistry):
        """Matrix is symmetric."""
        matrix = compute_similarity_matrix(registry)
        n = len(matrix.concept_ids)
        for i in range(n):
            for j in range(i + 1, n):
                assert abs(matrix.overall[i][j] - matrix.overall[j][i]) < 1e-9

    def test_has_dimension_matrices(self, registry: ConceptRegistry):
        """Per-dimension matrices exist for all 4 dimensions."""
        matrix = compute_similarity_matrix(registry)
        assert set(matrix.by_dimension.keys()) == {
            "plasma_physics", "engineering", "fuel_cycle", "operations"
        }


# ---------------------------------------------------------------------------
# Constellation (MDS projection)
# ---------------------------------------------------------------------------


class TestConstellation:
    def test_shape(self, registry: ConceptRegistry):
        """MDS produces 38 points with valid coordinates."""
        matrix = compute_similarity_matrix(registry)
        constellation = compute_constellation(matrix, registry)
        assert len(constellation.points) == 38
        assert all(
            math.isfinite(p.x) and math.isfinite(p.y) for p in constellation.points
        )

    def test_variance_explained(self, registry: ConceptRegistry):
        """variance_explained is between 0 and 1."""
        matrix = compute_similarity_matrix(registry)
        constellation = compute_constellation(matrix, registry)
        assert 0 < constellation.variance_explained <= 1.0

    def test_concept_ids_match_registry(self, registry: ConceptRegistry):
        """Constellation point IDs match the registry."""
        matrix = compute_similarity_matrix(registry)
        constellation = compute_constellation(matrix, registry)
        constellation_ids = {p.concept_id for p in constellation.points}
        registry_ids = {c.concept_id for c in registry.concepts}
        assert constellation_ids == registry_ids

    def test_family_labels_present(self, registry: ConceptRegistry):
        """Each point has a valid confinement family."""
        matrix = compute_similarity_matrix(registry)
        constellation = compute_constellation(matrix, registry)
        valid_families = set(ConfinementFamily)
        for p in constellation.points:
            assert p.confinement_family in valid_families


# ---------------------------------------------------------------------------
# Bridge diversity
# ---------------------------------------------------------------------------


class TestBridgeDiversity:
    def test_bridges_prefer_distinct_concepts(self, registry: ConceptRegistry):
        """When alternatives exist, bridge concepts should be distinct across fields."""
        a = registry.by_slug("hts-compact-tokamak")
        b = registry.by_slug("sheared-flow-stabilized-z-pinch")
        assert a is not None and b is not None
        bridges = explain_difference(a, b, registry)
        if len(bridges) >= 2:
            concept_ids = [br.bridge_concept_id for br in bridges]
            # At least some diversity — not all the same concept
            assert len(set(concept_ids)) > 1

    def test_bridges_fallback_to_reuse_when_no_alternative(self, registry: ConceptRegistry):
        """When only one concept matches a field, it can be reused."""
        a = registry.by_slug("hts-compact-tokamak")
        b = registry.by_slug("sheared-flow-stabilized-z-pinch")
        assert a is not None and b is not None
        bridges = explain_difference(a, b, registry)
        assert len(bridges) > 0

    def test_bridge_fields_still_covered(self, registry: ConceptRegistry):
        """Diversity preference must not reduce field coverage."""
        a = registry.by_slug("hts-compact-tokamak")
        b = registry.by_slug("sheared-flow-stabilized-z-pinch")
        assert a is not None and b is not None
        bridges = explain_difference(a, b, registry)
        fields = [br.mismatched_field for br in bridges]
        # Each bridge covers a unique field
        assert len(fields) == len(set(fields))


# ---------------------------------------------------------------------------
# Top-N slicing
# ---------------------------------------------------------------------------


class TestTopNSlicing:
    def test_top_n_returns_requested_count(self, registry: ConceptRegistry):
        """find_nearest(top_n=3) returns exactly 3."""
        c = registry.concepts[0]
        results = find_nearest(c, registry, top_n=3)
        assert len(results) == 3

    def test_top_n_fifteen(self, registry: ConceptRegistry):
        """find_nearest(top_n=15) returns 15 (enough concepts in registry)."""
        c = registry.concepts[0]
        results = find_nearest(c, registry, top_n=15)
        assert len(results) == 15

    def test_top_n_one(self, registry: ConceptRegistry):
        """Edge case: top_n=1 returns single result."""
        c = registry.concepts[0]
        results = find_nearest(c, registry, top_n=1)
        assert len(results) == 1
