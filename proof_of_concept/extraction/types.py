"""Type definitions and mapping registries for SysML visualization extraction.

This module provides:
1. Output data types (TypedDicts) for renderer-agnostic visualization data
2. Mapping registries that translate syside metatypes to visualization categories

The mapping registries centralize the translation logic between SysML/syside
concepts and simplified visualization categories, making it easy to extend
as syside support expands.
"""

from dataclasses import dataclass
from enum import Enum
from typing import TypedDict

import syside


# =============================================================================
# Visualization Categories (renderer-facing)
# =============================================================================


class ElementCategory(str, Enum):
    """Simplified element categories for visualization styling.

    These categories abstract away SysML metatypes into visualization-friendly
    groupings that can be styled consistently across different renderers.
    """

    PART = "part"
    ATTRIBUTE = "attribute"
    CALCULATION = "calculation"
    # Add new categories here as visualization needs expand


class EdgeCategory(str, Enum):
    """Edge categories for visualization styling."""

    CONTAINMENT = "containment"
    # Future: DEPENDENCY = "dependency", FLOW = "flow", etc.


# =============================================================================
# Output TypedDicts
# =============================================================================


class StructuralNode(TypedDict):
    """A node in the structural (containment) view.

    Attributes:
        id: Qualified path (e.g., "coffee_maker.brewing.heater")
        name: Usage name (declared or derived from redefines)
        type_name: Definition name (e.g., "Coffee Maker")
        element_type: ElementCategory value (e.g., "part")
        parent: Parent node ID (qualified path) or None for root
        depth: Hierarchy depth (0 = root)
        multiplicity: [lower, upper] bounds or None
    """

    id: str
    name: str
    type_name: str
    element_type: str
    parent: str | None
    depth: int
    multiplicity: list[int] | None


class ContainmentEdge(TypedDict):
    """An edge representing containment relationship.

    Attributes:
        id: Edge ID in format "parent_path->child_path"
        source: Parent node ID (qualified path)
        target: Child node ID (qualified path)
        edge_type: EdgeCategory value (e.g., "containment")
    """

    id: str
    source: str
    target: str
    edge_type: str


class StructuralViewResult(TypedDict):
    """Result of structural view extraction.

    Attributes:
        nodes: List of nodes in the structural hierarchy
        edges: List of containment edges
        metadata: View metadata (view type, root, counts)
    """

    nodes: list[StructuralNode]
    edges: list[ContainmentEdge]
    metadata: dict


# =============================================================================
# Element Type Mapping Registry
# =============================================================================


@dataclass(frozen=True)
class ElementTypeMapping:
    """Maps a syside metatype to a visualization category.

    Attributes:
        syside_type: The syside class (e.g., syside.PartUsage)
        category: The visualization category
        include_in_structural: Whether to include in structural view
    """

    syside_type: type
    category: ElementCategory
    include_in_structural: bool = True


# Registry: Add new mappings here as syside/SysML support expands
ELEMENT_TYPE_REGISTRY: list[ElementTypeMapping] = [
    ElementTypeMapping(syside.PartUsage, ElementCategory.PART, include_in_structural=True),
    ElementTypeMapping(
        syside.AttributeUsage, ElementCategory.ATTRIBUTE, include_in_structural=False
    ),
    ElementTypeMapping(
        syside.CalculationUsage, ElementCategory.CALCULATION, include_in_structural=False
    ),
    # Future: ItemUsage, ConnectionUsage, etc.
]


def get_element_category(element) -> ElementCategory | None:
    """Look up visualization category for a syside element.

    Args:
        element: A syside AST element

    Returns:
        The ElementCategory for this element, or None if not mapped (should be skipped)
    """
    for mapping in ELEMENT_TYPE_REGISTRY:
        if element.isinstance(mapping.syside_type):
            return mapping.category
    return None


def should_include_in_structural(element) -> bool:
    """Check if element should be included in structural view.

    Args:
        element: A syside AST element

    Returns:
        True if the element should appear in the structural view
    """
    for mapping in ELEMENT_TYPE_REGISTRY:
        if element.isinstance(mapping.syside_type):
            return mapping.include_in_structural
    return False


# =============================================================================
# Edge Type Mapping Registry
# =============================================================================


@dataclass(frozen=True)
class EdgeTypeMapping:
    """Maps a relationship type to a visualization edge category.

    Attributes:
        relationship: The relationship type (e.g., "ownership")
        category: The visualization edge category
    """

    relationship: str
    category: EdgeCategory


EDGE_TYPE_REGISTRY: list[EdgeTypeMapping] = [
    EdgeTypeMapping("ownership", EdgeCategory.CONTAINMENT),
    # Future: EdgeTypeMapping("dependency", EdgeCategory.DEPENDENCY),
]


def get_edge_category(relationship: str) -> EdgeCategory:
    """Look up edge category for a relationship type.

    Args:
        relationship: The relationship type string

    Returns:
        The EdgeCategory for this relationship (defaults to CONTAINMENT)
    """
    for mapping in EDGE_TYPE_REGISTRY:
        if mapping.relationship == relationship:
            return mapping.category
    # Default fallback
    return EdgeCategory.CONTAINMENT
