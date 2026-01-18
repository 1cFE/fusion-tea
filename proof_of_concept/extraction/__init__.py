"""Extraction package for SysML model visualization data extraction."""

from .types import (
    ElementCategory,
    EdgeCategory,
    StructuralNode,
    ContainmentEdge,
    StructuralViewResult,
    ELEMENT_TYPE_REGISTRY,
    EDGE_TYPE_REGISTRY,
    get_element_category,
    should_include_in_structural,
    get_edge_category,
)
from .visualization import (
    extract_structural_view,
    load_model,
    to_cytoscape,
    to_dot,
)

__all__ = [
    # Types
    "ElementCategory",
    "EdgeCategory",
    "StructuralNode",
    "ContainmentEdge",
    "StructuralViewResult",
    "ELEMENT_TYPE_REGISTRY",
    "EDGE_TYPE_REGISTRY",
    "get_element_category",
    "should_include_in_structural",
    "get_edge_category",
    # Extraction functions
    "extract_structural_view",
    "load_model",
    "to_cytoscape",
    "to_dot",
]
