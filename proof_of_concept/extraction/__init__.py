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

__all__ = [
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
]
