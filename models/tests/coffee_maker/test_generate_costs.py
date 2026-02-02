"""Tests for the generate_costs module's public API.

Tests the compute_costs() function which provides programmatic access
to cost evaluation for the visualization pipeline.
"""

import sys
from pathlib import Path

import pytest

# Add model directory to path for imports
MODEL_DIR = Path(__file__).parent
sys.path.insert(0, str(MODEL_DIR))


def test_compute_costs_returns_dict():
    """compute_costs returns dict mapping qualified paths to cost dicts."""
    from generate_costs import compute_costs

    result = compute_costs(str(MODEL_DIR))

    assert isinstance(result, dict)
    assert "coffee_maker" in result
    assert "capital_cost" in result["coffee_maker"]


def test_compute_costs_has_all_expected_paths():
    """compute_costs returns all 10 parts (excludes allocation entries)."""
    from generate_costs import compute_costs

    result = compute_costs(str(MODEL_DIR))

    expected_paths = {
        "coffee_maker",
        "coffee_maker.brewing",
        "coffee_maker.brewing.heater",
        "coffee_maker.brewing.pump",
        "coffee_maker.brewing.chamber",
        "coffee_maker.reservoir",
        "coffee_maker.carafe",
        "coffee_maker.housing",
        "coffee_maker.housing.shell",
        "coffee_maker.housing.panel",
    }
    assert set(result.keys()) == expected_paths


def test_compute_costs_has_all_cost_attributes():
    """Each part has all 5 cost attributes."""
    from generate_costs import compute_costs

    result = compute_costs(str(MODEL_DIR))

    expected_attrs = {
        "capital_cost",
        "raw_material_cost",
        "fabrication_cost",
        "installation_cost",
        "idiot_index",
    }

    for path, costs in result.items():
        assert set(costs.keys()) == expected_attrs, f"Missing attributes for {path}"


def test_compute_costs_values_are_numeric():
    """All cost values are floats."""
    from generate_costs import compute_costs

    result = compute_costs(str(MODEL_DIR))

    for path, costs in result.items():
        for attr, value in costs.items():
            assert isinstance(value, (int, float)), f"{path}.{attr} is not numeric"


def test_compute_costs_root_values_match_expected():
    """Root coffee_maker costs match expected values from CSV."""
    from generate_costs import compute_costs

    result = compute_costs(str(MODEL_DIR))

    # Values from expected_output.csv for coffee_maker
    root = result["coffee_maker"]
    assert abs(root["capital_cost"] - 113.96) < 0.02
    assert abs(root["raw_material_cost"] - 68.44) < 0.02
    assert abs(root["fabrication_cost"] - 37.03) < 0.02
    assert abs(root["installation_cost"] - 7.53) < 0.02
    assert abs(root["idiot_index"] - 1.67) < 0.02


def test_compute_costs_heater_values_match_expected():
    """Heater costs match expected values (quantity=2 applied)."""
    from generate_costs import compute_costs

    result = compute_costs(str(MODEL_DIR))

    # Values from expected_output.csv for heater (total, not unit)
    heater = result["coffee_maker.brewing.heater"]
    assert abs(heater["capital_cost"] - 26.25) < 0.02
    assert abs(heater["raw_material_cost"] - 15.00) < 0.02
    assert abs(heater["fabrication_cost"] - 9.00) < 0.02
    assert abs(heater["installation_cost"] - 2.25) < 0.02


def test_compute_costs_invalid_path_raises():
    """compute_costs raises ValueError for invalid path."""
    from generate_costs import compute_costs

    with pytest.raises(ValueError, match="does not exist"):
        compute_costs("/nonexistent/path")
