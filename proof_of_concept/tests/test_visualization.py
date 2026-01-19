"""Tests for structural view extraction.

Compares extraction output against the golden reference for the coffee_maker model.
"""

import json
from pathlib import Path

import pytest

# Paths
GOLDEN_REF = Path(__file__).parent.parent / "golden_references" / "coffee_maker_structural.json"
MODEL_DIR = Path(__file__).parent.parent.parent / "models" / "tests" / "coffee_maker"


@pytest.fixture
def golden_reference():
    """Load golden reference JSON."""
    with open(GOLDEN_REF) as f:
        return json.load(f)


@pytest.fixture
def extracted_result():
    """Run extraction on coffee_maker model."""
    from proof_of_concept.extraction.visualization import extract_structural_view

    import syside

    files = syside.collect_files_recursively(str(MODEL_DIR))
    model, diagnostics = syside.try_load_model(files)
    assert not diagnostics.contains_errors(), f"Model load failed: {diagnostics}"

    return extract_structural_view(model, root="coffee_maker")


def test_node_count(extracted_result, golden_reference):
    """Extraction produces exactly 10 nodes."""
    assert len(extracted_result["nodes"]) == len(golden_reference["nodes"])


def test_edge_count(extracted_result, golden_reference):
    """Extraction produces exactly 9 edges."""
    assert len(extracted_result["edges"]) == len(golden_reference["edges"])


def test_root_node_exists(extracted_result):
    """Root node is coffee_maker."""
    node_ids = [n["id"] for n in extracted_result["nodes"]]
    assert "coffee_maker" in node_ids


def test_multiplicity_on_heater(extracted_result):
    """Heater has multiplicity [2, 2] (from heater_count default)."""
    heater = next(n for n in extracted_result["nodes"] if n["name"] == "heater")
    assert heater["multiplicity"] == [2, 2]


def test_hierarchy_depth(extracted_result):
    """Maximum depth is 2."""
    max_depth = max(n["depth"] for n in extracted_result["nodes"])
    assert max_depth == 2


def test_qualified_path_ids(extracted_result):
    """Node IDs are qualified paths."""
    node_ids = [n["id"] for n in extracted_result["nodes"]]
    assert "coffee_maker.brewing" in node_ids
    assert "coffee_maker.brewing.heater" in node_ids


def test_containment_edges(extracted_result):
    """Edges connect parents to children."""
    edge_sources = {e["source"] for e in extracted_result["edges"]}
    edge_targets = {e["target"] for e in extracted_result["edges"]}

    # coffee_maker should be a source (has children)
    assert "coffee_maker" in edge_sources
    # brewing.heater should be a target (is a child)
    assert "coffee_maker.brewing.heater" in edge_targets


def test_type_names_extracted(extracted_result):
    """Type names are extracted from definitions."""
    root = next(n for n in extracted_result["nodes"] if n["id"] == "coffee_maker")
    assert root["type_name"] == "Coffee Maker"


def test_structure_matches_golden_reference(extracted_result, golden_reference):
    """Full structural comparison."""
    # Compare node names (order-independent)
    extracted_names = {n["name"] for n in extracted_result["nodes"]}
    golden_names = {n["name"] for n in golden_reference["nodes"]}
    assert extracted_names == golden_names

    # Compare edge count
    assert len(extracted_result["edges"]) == len(golden_reference["edges"])


# =============================================================================
# Phase 4: Edge Cases + Polish
# =============================================================================


def test_stdlib_elements_excluded(extracted_result):
    """Standard library elements are not in output."""
    node_names = {n["name"] for n in extracted_result["nodes"]}
    # These are common stdlib elements that should be filtered
    assert "start" not in node_names
    assert "done" not in node_names


def test_all_nodes_have_element_type(extracted_result):
    """Every node has element_type field set to 'part'."""
    for node in extracted_result["nodes"]:
        assert "element_type" in node
        assert node["element_type"] == "part"  # Structural view only has parts


def test_metadata_present(extracted_result):
    """Metadata contains expected fields."""
    meta = extracted_result["metadata"]
    assert meta["view"] == "structural"
    assert meta["root"] == "coffee_maker"
    assert meta["total_nodes"] == 10
    assert meta["max_depth"] == 2


# =============================================================================
# Phase 1: Format Converters (POC Item 3)
# =============================================================================


def test_to_cytoscape_format(extracted_result):
    """to_cytoscape returns correct structure."""
    from proof_of_concept.extraction.visualization import to_cytoscape

    result = to_cytoscape(extracted_result)

    assert "elements" in result
    assert len(result["elements"]) == 10  # 10 nodes
    assert all("data" in el for el in result["elements"])


def test_to_cytoscape_labels(extracted_result):
    """Labels include multiplicity notation."""
    from proof_of_concept.extraction.visualization import to_cytoscape

    result = to_cytoscape(extracted_result)
    labels = {el["data"]["label"] for el in result["elements"]}

    assert "heater [2]" in labels  # Has multiplicity
    assert "pump" in labels  # No multiplicity


def test_to_dot_contains_structure(extracted_result):
    """DOT output has expected keywords."""
    from proof_of_concept.extraction.visualization import to_dot

    result = to_dot(extracted_result)

    assert "digraph" in result
    assert "subgraph cluster_" in result
    assert "coffee_maker" in result


# =============================================================================
# Phase 2: Model Loading Helper (POC Item 3)
# =============================================================================


def test_load_model_valid_path():
    """load_model loads coffee_maker model."""
    from proof_of_concept.extraction.visualization import load_model

    model = load_model(MODEL_DIR)

    assert model is not None


def test_load_model_invalid_path():
    """load_model raises ValueError for bad path."""
    from proof_of_concept.extraction.visualization import load_model

    with pytest.raises(ValueError, match="not found"):
        load_model("/nonexistent/path")


# =============================================================================
# Phase 5: Cost Extraction (POC Item 5)
# =============================================================================


@pytest.fixture
def extracted_result_with_costs():
    """Run extraction with cost attributes enabled."""
    from proof_of_concept.extraction.visualization import extract_structural_view

    import syside

    files = syside.collect_files_recursively(str(MODEL_DIR))
    model, _ = syside.try_load_model(files)

    return extract_structural_view(
        model,
        root="coffee_maker",
        include_cost_attributes=[
            "capital_cost",
            "raw_material_cost",
            "fabrication_cost",
            "installation_cost",
            "idiot_index",
        ],
        model_path=MODEL_DIR,
    )


def test_costs_field_present(extracted_result_with_costs):
    """Nodes have costs field when cost extraction enabled."""
    for node in extracted_result_with_costs["nodes"]:
        assert "costs" in node


def test_root_has_all_cost_attributes(extracted_result_with_costs):
    """Root node has all requested cost attributes."""
    root = next(
        n for n in extracted_result_with_costs["nodes"] if n["id"] == "coffee_maker"
    )
    costs = root.get("costs", {})

    expected_attrs = {
        "capital_cost",
        "raw_material_cost",
        "fabrication_cost",
        "installation_cost",
        "idiot_index",
    }
    assert set(costs.keys()) == expected_attrs


def test_cost_values_are_numeric(extracted_result_with_costs):
    """All cost values are floats."""
    for node in extracted_result_with_costs["nodes"]:
        costs = node.get("costs")
        if costs:
            for value in costs.values():
                assert isinstance(value, (int, float))


def test_to_cytoscape_includes_costs(extracted_result_with_costs):
    """to_cytoscape passes through cost data."""
    from proof_of_concept.extraction.visualization import to_cytoscape

    result = to_cytoscape(extracted_result_with_costs)

    # Find root element
    root_el = next(
        el for el in result["elements"] if el["data"]["id"] == "coffee_maker"
    )

    assert "costs" in root_el["data"]
    assert "capital_cost" in root_el["data"]  # Flattened for Cytoscape access


def test_backward_compatible_no_costs():
    """Extraction without cost attributes still works."""
    from proof_of_concept.extraction.visualization import extract_structural_view

    import syside

    files = syside.collect_files_recursively(str(MODEL_DIR))
    model, _ = syside.try_load_model(files)

    result = extract_structural_view(model, root="coffee_maker")

    # Should work, costs field should be None
    assert len(result["nodes"]) == 10
    for node in result["nodes"]:
        assert node.get("costs") is None


# =============================================================================
# Phase 3: Golden Reference with Costs
# =============================================================================

GOLDEN_REF_COSTS = (
    Path(__file__).parent.parent / "golden_references" / "coffee_maker_with_costs.json"
)


@pytest.fixture
def golden_reference_with_costs():
    """Load golden reference with costs."""
    with open(GOLDEN_REF_COSTS) as f:
        return json.load(f)


def test_costs_match_golden_reference(extracted_result_with_costs, golden_reference_with_costs):
    """Extracted costs match golden reference values within tolerance."""
    # Build lookup by ID for golden reference
    golden_by_id = {n["id"]: n for n in golden_reference_with_costs["nodes"]}

    for extracted_node in extracted_result_with_costs["nodes"]:
        node_id = extracted_node["id"]
        assert node_id in golden_by_id, f"Node {node_id} not in golden reference"

        golden_node = golden_by_id[node_id]
        golden_costs = golden_node.get("costs", {})
        extracted_costs = extracted_node.get("costs", {})

        assert extracted_costs is not None, f"Node {node_id} missing costs"

        for attr, expected_value in golden_costs.items():
            actual_value = extracted_costs.get(attr)
            assert actual_value is not None, f"{node_id}.{attr} missing"
            assert abs(actual_value - expected_value) < 0.02, (
                f"{node_id}.{attr}: expected {expected_value}, got {actual_value}"
            )
