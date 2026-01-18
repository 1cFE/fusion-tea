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
