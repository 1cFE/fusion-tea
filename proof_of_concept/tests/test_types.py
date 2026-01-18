"""Tests for extraction types module.

Validates that type definitions and mapping registries are correctly defined.
"""

import pytest


def test_element_category_enum():
    """ElementCategory enum has expected values."""
    from proof_of_concept.extraction.types import ElementCategory

    assert ElementCategory.PART.value == "part"
    assert ElementCategory.ATTRIBUTE.value == "attribute"
    assert ElementCategory.CALCULATION.value == "calculation"


def test_edge_category_enum():
    """EdgeCategory enum has expected values."""
    from proof_of_concept.extraction.types import EdgeCategory

    assert EdgeCategory.CONTAINMENT.value == "containment"


def test_element_type_registry_exists():
    """ELEMENT_TYPE_REGISTRY is populated."""
    from proof_of_concept.extraction.types import ELEMENT_TYPE_REGISTRY

    assert len(ELEMENT_TYPE_REGISTRY) >= 1


def test_element_type_registry_has_part_mapping():
    """Registry includes PartUsage mapping."""
    from proof_of_concept.extraction.types import (
        ELEMENT_TYPE_REGISTRY,
        ElementCategory,
    )
    import syside

    part_mappings = [m for m in ELEMENT_TYPE_REGISTRY if m.syside_type is syside.PartUsage]
    assert len(part_mappings) == 1
    assert part_mappings[0].category == ElementCategory.PART
    assert part_mappings[0].include_in_structural is True


def test_edge_type_registry_exists():
    """EDGE_TYPE_REGISTRY is populated."""
    from proof_of_concept.extraction.types import EDGE_TYPE_REGISTRY

    assert len(EDGE_TYPE_REGISTRY) >= 1


def test_get_edge_category_default():
    """get_edge_category returns CONTAINMENT for unknown relationships."""
    from proof_of_concept.extraction.types import EdgeCategory, get_edge_category

    result = get_edge_category("unknown_relationship")
    assert result == EdgeCategory.CONTAINMENT


def test_get_edge_category_ownership():
    """get_edge_category returns CONTAINMENT for ownership."""
    from proof_of_concept.extraction.types import EdgeCategory, get_edge_category

    result = get_edge_category("ownership")
    assert result == EdgeCategory.CONTAINMENT
