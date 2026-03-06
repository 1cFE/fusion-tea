"""Tests for the generate_costs module's public API.

Tests the compute_costs() function which provides programmatic access
to cost evaluation for the visualization pipeline.
"""

import json
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
    assert "solar_battery_plant" in result
    assert "capital_cost" in result["solar_battery_plant"]


def test_compute_costs_has_all_expected_paths():
    """compute_costs returns all 13 parts (excludes allocation entries)."""
    from generate_costs import compute_costs

    result = compute_costs(str(MODEL_DIR))

    expected_paths = {
        "solar_battery_plant",
        "solar_battery_plant.solar_array",
        "solar_battery_plant.solar_array.pv_module",
        "solar_battery_plant.solar_array.inverter",
        "solar_battery_plant.solar_array.array_bos",
        "solar_battery_plant.battery_system",
        "solar_battery_plant.battery_system.battery_pack",
        "solar_battery_plant.battery_system.hybrid_inverter",
        "solar_battery_plant.battery_system.battery_bos",
        "solar_battery_plant.site_infra",
        "solar_battery_plant.site_infra.racking",
        "solar_battery_plant.site_infra.electrical_panel",
        "solar_battery_plant.site_infra.permitting",
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
    """Root solar_battery_plant costs match expected values from CSV."""
    from generate_costs import compute_costs

    result = compute_costs(str(MODEL_DIR))

    # Values from expected_output.csv for solar_battery_plant
    root = result["solar_battery_plant"]
    assert abs(root["capital_cost"] - 41205.00) < 0.02
    assert abs(root["raw_material_cost"] - 22716.00) < 0.02
    assert abs(root["fabrication_cost"] - 10179.00) < 0.02
    assert abs(root["installation_cost"] - 6786.00) < 0.02
    assert abs(root["idiot_index"] - 1.81) < 0.02


def test_compute_costs_pv_module_values_match_expected():
    """PV Module costs match expected values (quantity=20 applied)."""
    from generate_costs import compute_costs

    result = compute_costs(str(MODEL_DIR))

    # Values from expected_output.csv for pv_module (total, not unit)
    pv = result["solar_battery_plant.solar_array.pv_module"]
    assert abs(pv["capital_cost"] - 14980.00) < 0.02
    assert abs(pv["raw_material_cost"] - 8560.00) < 0.02
    assert abs(pv["fabrication_cost"] - 3852.00) < 0.02
    assert abs(pv["installation_cost"] - 2568.00) < 0.02


def test_compute_costs_invalid_path_raises():
    """compute_costs raises ValueError for invalid path."""
    from generate_costs import compute_costs

    with pytest.raises(ValueError, match="does not exist"):
        compute_costs("/nonexistent/path")


def test_write_component_costs_json(tmp_path):
    """write_component_costs_json produces correct JSON structure and values."""
    from generate_costs import (
        ROOT_PART_NAME,
        _compute_part_hierarchy_costs,
        extract_calc_defs,
        extract_design_hierarchy,
        map_part_defs_to_calcs,
        write_component_costs_json,
    )

    from agentic_mbse.sysml.syside_adapter import SysideAdapter

    model, _ = SysideAdapter.load_model([MODEL_DIR])
    calc_defs = extract_calc_defs(model, SysideAdapter)
    part_def_to_calc = map_part_defs_to_calcs(model, SysideAdapter)
    root = extract_design_hierarchy(model, SysideAdapter, calc_defs, part_def_to_calc)
    results = _compute_part_hierarchy_costs(root, calc_defs)

    output_path = tmp_path / "component_costs.json"
    write_component_costs_json(results, output_path)

    data = json.loads(output_path.read_text())
    assert abs(data["total_capex"] - 41205.00) < 0.02
    assert "solar_array" in data
    assert abs(data["solar_array"]["total_cost"] - 21204.00) < 0.02
    assert abs(data["battery_system"]["total_cost"] - 16005.50) < 0.02
    assert abs(data["site_infra"]["total_cost"] - 3995.50) < 0.02


def test_write_design_params_json(tmp_path):
    """write_design_params_json produces correct JSON with all 11 keys."""
    from generate_costs import (
        ROOT_PART_NAME,
        extract_design_params,
        write_design_params_json,
    )

    from agentic_mbse.sysml.syside_adapter import SysideAdapter

    model, _ = SysideAdapter.load_model([MODEL_DIR])

    # Find root usage
    root_usage = None
    for part_usage in SysideAdapter.elements_of_type(model, "PartUsage"):
        if getattr(part_usage, "name", None) == ROOT_PART_NAME:
            root_usage = part_usage
            break
    assert root_usage is not None, "Could not find root part usage"

    params = extract_design_params(root_usage, total_capex=41205.00)
    output_path = tmp_path / "design_params.json"
    write_design_params_json(params, output_path)

    data = json.loads(output_path.read_text())
    assert len(data) == 11
    assert data["p_net_mw"] == 0.008
    assert data["p_net_kw"] == 8.0
    assert data["total_capex"] == 41205.00
    assert data["plant_lifetime"] == 25.0
    assert data["discount_rate"] == 0.05
    assert data["fuel_unit_cost"] == 0.0
    assert data["fuel_consumption"] == 0.0


def test_verify_system_outputs_passes():
    """verify_system_outputs computes correct LCOE from design params."""
    from generate_costs import (
        ROOT_PART_NAME,
        extract_design_params,
        verify_system_outputs,
    )

    from agentic_mbse.sysml.syside_adapter import SysideAdapter

    model, _ = SysideAdapter.load_model([MODEL_DIR])

    # Find root usage
    root_usage = None
    for part_usage in SysideAdapter.elements_of_type(model, "PartUsage"):
        if getattr(part_usage, "name", None) == ROOT_PART_NAME:
            root_usage = part_usage
            break
    assert root_usage is not None, "Could not find root part usage"

    params = extract_design_params(root_usage, total_capex=41205.00)
    expected_path = MODEL_DIR / "expected_system_outputs.csv"
    passed, diffs = verify_system_outputs(params, expected_path)
    assert passed, f"System output verification failed: {diffs}"
