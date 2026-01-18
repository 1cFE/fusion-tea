"""Structural view extraction from SysML models.

This module provides the extract_structural_view() function that transforms
a parsed syside SysML model into a renderer-agnostic ViewResult data structure.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass
from pathlib import Path

import syside

logger = logging.getLogger(__name__)

from .types import (
    ContainmentEdge,
    EdgeCategory,
    ElementCategory,
    StructuralNode,
    StructuralViewResult,
    get_element_category,
    should_include_in_structural,
)


@dataclass
class _ExtractionConfig:
    """Configuration for extraction."""

    max_depth: int
    include_multiplicity: bool
    exclude_stdlib: bool


def _find_root_part(model, root_name: str | None):
    """Find the root PartUsage to start extraction.

    Args:
        model: Parsed syside model
        root_name: Name of root part, or None to auto-detect

    Returns:
        The root PartUsage element, or None if not found
    """
    # Collect all top-level PartUsages (those owned by a Package or document root)
    candidates = []

    for part in model.nodes(syside.PartUsage, include_subtypes=True):
        # Skip parts owned by definitions (they're nested, not top-level)
        owner = part.owner
        if owner and owner.isinstance(syside.Definition):
            continue

        name = part.declared_name or ""
        if root_name:
            # Looking for specific name
            if name == root_name:
                return part
        else:
            # Collecting candidates for auto-detect
            if name:  # Skip anonymous parts
                candidates.append(part)

    # Auto-detect: return first candidate (if any)
    if not root_name and candidates:
        return candidates[0]

    return None


def _build_qualified_path(element_name: str, parent_path: str | None) -> str:
    """Build qualified path ID for an element.

    Examples:
        _build_qualified_path("coffee_maker", None) → "coffee_maker"
        _build_qualified_path("brewing", "coffee_maker") → "coffee_maker.brewing"
    """
    if parent_path:
        return f"{parent_path}.{element_name}"
    return element_name


def _build_edge_id(source_path: str, target_path: str) -> str:
    """Build edge ID from source and target paths.

    Example: "coffee_maker->coffee_maker.brewing"
    """
    return f"{source_path}->{target_path}"


def _is_stdlib_element(element) -> bool:
    """Check if element is from SysML standard library.

    Filters out standard library elements like 'start', 'done', and
    elements from Base:: or Occurrences:: namespaces.
    """
    name = element.declared_name or ""
    if name in ("start", "done"):
        return True
    qname = str(element.qualified_name) if element.qualified_name else ""
    return qname.startswith("Base::") or qname.startswith("Occurrences::")


def _get_multiplicity(element) -> list[int] | None:
    """Extract multiplicity as [lower, upper] or None.

    Args:
        element: A syside element with potential multiplicity

    Returns:
        [lower, upper] list if multiplicity is defined, else None
    """
    if not hasattr(element, "declared_multiplicity"):
        return None

    mult = element.declared_multiplicity
    if mult is None:
        return None

    if not mult.has_cached_bounds:
        return None

    # WORKAROUND: syside bug - cached_upper_bound returns value+1
    # See: .project/research/20260118-220500_syside-multiplicity-caching-bug.md
    #
    # Strategy:
    # - lower_bound: cached value is correct, use as-is
    # - upper_bound: if expression has .value (LiteralInteger), use it
    #                otherwise, use cached_upper_bound - 1

    lower = mult.cached_lower_bound

    # Try to get correct upper bound from expression first
    if mult.upper_bound and hasattr(mult.upper_bound, "value"):
        upper = mult.upper_bound.value
    elif mult.cached_upper_bound is not None:
        # Fall back to cached - 1 (workaround for off-by-one bug)
        upper = mult.cached_upper_bound - 1
    else:
        # Unbounded (*)
        return [lower, -1]

    return [lower, upper]


def _get_element_name(element) -> str:
    """Get the name of an element, checking redefinitions if needed.

    Args:
        element: A syside element

    Returns:
        The element's name (declared, or from redefined feature, or "(anonymous)")
    """
    # First try declared name
    if element.declared_name:
        return element.declared_name

    # Check redefinitions for name
    if hasattr(element, "owned_redefinitions"):
        for redef in element.owned_redefinitions:
            rf = redef.redefined_feature
            if rf:
                name = rf.declared_name or getattr(rf, "name", None)
                if name:
                    return name

    # Log warning for anonymous elements
    element_type = type(element).__name__
    logger.warning(f"Anonymous element encountered: {element_type}")
    return "(anonymous)"


def _get_type_name(element) -> str:
    """Get the type name for a usage element.

    Args:
        element: A syside usage element

    Returns:
        The type definition name, or empty string if untyped
    """
    if hasattr(element, "types"):
        types = list(element.types)
        if types:
            type_def = types[0]
            return type_def.declared_name or getattr(type_def, "name", "") or ""
    return ""


def _extract_node(
    element,
    parent_path: str | None,
    depth: int,
    nodes: list[StructuralNode],
    edges: list[ContainmentEdge],
    visited: set[str],
    config: _ExtractionConfig,
) -> None:
    """Recursively extract a node and its children.

    This follows the proven pattern from explore_ast.py - critically, it follows
    typing relationships to get children from PartDefinitions.

    Args:
        element: Current syside element to process
        parent_path: Qualified path of parent, or None for root
        depth: Current depth in hierarchy
        nodes: List to append nodes to
        edges: List to append edges to
        visited: Set of visited element IDs to prevent cycles
        config: Extraction configuration
    """
    # Check depth limit
    if depth > config.max_depth:
        return

    # Only process elements that should be in structural view
    if not should_include_in_structural(element):
        return

    # Skip stdlib elements if configured
    if config.exclude_stdlib and _is_stdlib_element(element):
        return

    # Get element name
    name = _get_element_name(element)

    # Build qualified path ID
    node_id = _build_qualified_path(name, parent_path)

    # Avoid infinite loops via visited set
    if node_id in visited:
        return
    visited.add(node_id)

    # Get type info
    type_name = _get_type_name(element)
    type_def = None
    if hasattr(element, "types"):
        types = list(element.types)
        if types:
            type_def = types[0]

    # Get element category
    category = get_element_category(element)
    if category is None:
        syside_type = type(element).__name__
        logger.warning(f"Unmapped syside type: {syside_type} (element: {name})")
        element_type = "unknown"
    else:
        element_type = category.value

    # Get multiplicity
    multiplicity = None
    if config.include_multiplicity:
        multiplicity = _get_multiplicity(element)

    # Create node
    node = StructuralNode(
        id=node_id,
        name=name,
        type_name=type_name,
        element_type=element_type,
        parent=parent_path,
        depth=depth,
        multiplicity=multiplicity,
    )
    nodes.append(node)

    # Create containment edge if has parent
    if parent_path:
        edge = ContainmentEdge(
            id=_build_edge_id(parent_path, node_id),
            source=parent_path,
            target=node_id,
            edge_type=EdgeCategory.CONTAINMENT.value,
        )
        edges.append(edge)

    # Recurse into children - CRITICAL: follow typing to get nested parts
    # This is the key pattern from explore_ast.py:562-565
    if type_def and type_def.isinstance(syside.PartDefinition):
        for feature in type_def.owned_features:
            if feature.isinstance(syside.PartUsage):
                _extract_node(
                    feature,
                    node_id,
                    depth + 1,
                    nodes,
                    edges,
                    visited,
                    config,
                )


def extract_structural_view(
    model,
    root: str | None = None,
    max_depth: int = 10,
    include_multiplicity: bool = True,
    exclude_stdlib: bool = True,
) -> StructuralViewResult:
    """Extract structural (containment) view from SysML model.

    Args:
        model: Parsed syside model object
        root: Name of root part to start from (None = auto-detect)
        max_depth: Maximum hierarchy depth to traverse
        include_multiplicity: Whether to include multiplicity info
        exclude_stdlib: Whether to filter out standard library elements

    Returns:
        StructuralViewResult with nodes, edges, and metadata
    """
    nodes: list[StructuralNode] = []
    edges: list[ContainmentEdge] = []
    visited: set[str] = set()

    config = _ExtractionConfig(
        max_depth=max_depth,
        include_multiplicity=include_multiplicity,
        exclude_stdlib=exclude_stdlib,
    )

    # Find root element
    root_element = _find_root_part(model, root)
    if root_element is None:
        # Return empty result if no root found
        return StructuralViewResult(
            nodes=nodes,
            edges=edges,
            metadata={
                "view": "structural",
                "root": root,
                "total_nodes": 0,
                "max_depth": 0,
                "error": "Root element not found",
            },
        )

    # Extract starting from root
    _extract_node(
        root_element,
        parent_path=None,
        depth=0,
        nodes=nodes,
        edges=edges,
        visited=visited,
        config=config,
    )

    # Compute actual max depth
    actual_max_depth = max((n["depth"] for n in nodes), default=0)

    # Get actual root name
    root_name = nodes[0]["name"] if nodes else root

    return StructuralViewResult(
        nodes=nodes,
        edges=edges,
        metadata={
            "view": "structural",
            "root": root_name,
            "total_nodes": len(nodes),
            "max_depth": actual_max_depth,
        },
    )


# =============================================================================
# Model Loading (POC Item 3)
# =============================================================================


def load_model(path: str | Path):
    """Load a SysML model from path using syside.

    Args:
        path: Path to model directory or single .sysml file

    Returns:
        Parsed syside model object

    Raises:
        ValueError: If path doesn't exist or model has errors
    """
    path = Path(path)

    if not path.exists():
        raise ValueError(f"Model path not found: {path}")

    if path.is_dir():
        files = syside.collect_files_recursively(str(path))
    else:
        files = [str(path)]

    model, diagnostics = syside.try_load_model(files)

    if diagnostics.contains_errors():
        raise ValueError(f"Model has errors: {diagnostics}")

    return model


# =============================================================================
# Format Converters (POC Item 3)
# =============================================================================


def _format_label(name: str, multiplicity: list[int] | None) -> str:
    """Format node label with multiplicity notation.

    Args:
        name: Element name
        multiplicity: [lower, upper] bounds or None

    Returns:
        Label string, e.g., "heater [2]" or "pump"
    """
    if multiplicity is None:
        return name
    lower, upper = multiplicity
    if lower == upper:
        return f"{name} [{lower}]"
    upper_str = "*" if upper == -1 else str(upper)
    return f"{name} [{lower}..{upper_str}]"


def to_cytoscape(view_result: StructuralViewResult) -> dict:
    """Convert structural view to Cytoscape.js elements format.

    Args:
        view_result: Output from extract_structural_view()

    Returns:
        Dict with "elements" key containing list of node data objects.
        Each node has: id, label, name, type_name, element_type, parent, depth, multiplicity.
        No edges are included (Cytoscape uses parent property for hierarchy).
    """
    elements = []

    for node in view_result["nodes"]:
        elements.append(
            {
                "data": {
                    "id": node["id"],
                    "label": _format_label(node["name"], node.get("multiplicity")),
                    "name": node["name"],
                    "type_name": node["type_name"],
                    "element_type": node["element_type"],
                    "parent": node["parent"],
                    "depth": node["depth"],
                    "multiplicity": node.get("multiplicity"),
                }
            }
        )

    return {"elements": elements}


def _escape_dot_id(id_str: str) -> str:
    """Escape ID for DOT format (replace dots with underscores)."""
    return id_str.replace(".", "_")


def _build_dot_label(node: StructuralNode) -> str:
    """Build DOT node label with name, multiplicity, and type."""
    name = node["name"]
    mult = node.get("multiplicity")
    type_name = node["type_name"]

    if mult:
        lower, upper = mult
        if lower == upper:
            name_part = f"{name} [{lower}]"
        else:
            upper_str = "*" if upper == -1 else str(upper)
            name_part = f"{name} [{lower}..{upper_str}]"
    else:
        name_part = name

    if type_name:
        return f"{name_part} : {type_name}"
    return name_part


def to_dot(view_result: StructuralViewResult) -> str:
    """Convert structural view to DOT format for Graphviz.

    Args:
        view_result: Output from extract_structural_view()

    Returns:
        DOT format string with digraph, subgraphs for compound nodes,
        and node labels including type names.
    """
    nodes = view_result["nodes"]

    # Build parent->children mapping
    children_map: dict[str | None, list[StructuralNode]] = {}
    node_by_id: dict[str, StructuralNode] = {}

    for node in nodes:
        node_by_id[node["id"]] = node
        parent = node["parent"]
        if parent not in children_map:
            children_map[parent] = []
        children_map[parent].append(node)

    def has_children(node_id: str) -> bool:
        return node_id in children_map and len(children_map[node_id]) > 0

    def emit_node_or_cluster(node: StructuralNode, indent: int) -> list[str]:
        """Recursively emit a node as either a cluster (if it has children) or leaf node."""
        lines = []
        prefix = "    " * indent
        node_id = node["id"]
        escaped_id = _escape_dot_id(node_id)
        label = _build_dot_label(node)

        if has_children(node_id):
            # Emit as subgraph cluster
            lines.append(f'{prefix}subgraph cluster_{escaped_id} {{')
            lines.append(f'{prefix}    label="{label}";')
            lines.append(f"{prefix}    style=rounded;")

            # Recurse into children
            for child in children_map[node_id]:
                lines.extend(emit_node_or_cluster(child, indent + 1))

            lines.append(f"{prefix}}}")
        else:
            # Emit as leaf node
            lines.append(f'{prefix}{escaped_id} [label="{label}"];')

        return lines

    # Build DOT output
    lines = [
        "digraph structural {",
        "    rankdir=TB;",
        '    node [shape=box, style=rounded];',
        "",
    ]

    # Start from root nodes (those with parent=None)
    root_nodes = children_map.get(None, [])
    for root in root_nodes:
        lines.extend(emit_node_or_cluster(root, 1))

    lines.append("}")

    return "\n".join(lines)
