"""Current radius ownership: reject retired inputs and preserve native numerics."""

from tests.models.current_mfe_regressions import WI059_PARAMETERS, WI059_EXISTING_MAPPED_PARAMETERS, WI059_CHANNELS, WI059_NATIVE_ONLY_PARAMETERS, WI059_NATIVE_ONLY_VALUES

import json
import sys
from pathlib import Path
from tests.study.structure_ledger import renamed, renamed_keys


import pytest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "exploration/stellarator_e2e/studies"))
import oracle_entry as oracle  # noqa: E402 — runtime import path established above
import study_route as route  # noqa: E402 — runtime import path established above

OLD = route.P + "magnet__R0"
R = route.P + "plasma__R"
RETIRED = [{OLD: 14}, {R: 14, OLD: 14}, {R: 14, OLD: 12.7}, {OLD: 0}, {OLD: object()}]


@pytest.mark.parametrize("point", RETIRED)
def test_retired_flat_key_rejected_before_conversion(point):
    with pytest.raises(oracle.OracleSeamError, match=OLD):
        oracle.evaluate(point)
    with pytest.raises(route.RouteError, match=OLD):
        route.validate_proposal(point)


@pytest.mark.parametrize("value", [14, 12.7, 0])
def test_retired_local_alias_rejected(value):
    with pytest.raises(oracle.OracleSeamError, match="magnet_R0"):
        oracle._compute({"R": 14, "magnet_R0": value})
    saved = dict(oracle.vs.IN)
    try:
        oracle.vs.IN["magnet_R0"] = value
        with pytest.raises(ValueError, match="magnet_R0"):
            oracle.vs.compute()
    finally:
        oracle.vs.IN.clear()
        oracle.vs.IN.update(saved)


def test_exact_input_contract():
    from tests.models.current_mfe_regressions import WI040_PARAMETERS, WI038_PARAMETERS, WI058_PARAMETERS, WI058_RETIRED
    # WI-058 (2026-09-14): k_coil retired from the contract and the seam, c_coil_ref added (the winding
    # length follows the coil bore); the counts (265 inputs, 118 mapped, 147 unmapped) do not move.
    added = WI040_PARAMETERS | WI038_PARAMETERS | WI058_PARAMETERS | WI059_PARAMETERS
    inputs = {}
    for path in (route.PACKAGE_DIR / "inputs").glob("*.json"):
        inputs.update(json.loads(path.read_text()))
    assert len(inputs) == 265 + len(WI059_PARAMETERS | WI059_NATIVE_ONLY_PARAMETERS)
    coverage = json.loads(
        (
            ROOT
            / ".project/active/mfe-major-radius-study-package/implementation/contract-coverage.json"
        ).read_text()
    )
    assert set(inputs) == ({renamed(k) for k in coverage["native_inputs"]} - WI058_RETIRED) | added | WI059_NATIVE_ONLY_PARAMETERS
    entering = renamed_keys(coverage["entering_mapping"])
    current = oracle.ENTRY_KEY_TO_ORACLE_INPUT
    mapped_added = added | WI059_EXISTING_MAPPED_PARAMETERS
    assert len(entering) == 100 and len(current) == 118 + len(WI059_PARAMETERS | WI059_EXISTING_MAPPED_PARAMETERS)
    assert {k: v for k, v in current.items() if k not in mapped_added} == {key: value for key, value in entering.items() if key != OLD and key not in WI058_RETIRED}
    assert set(current) - set(entering) == mapped_added
    assert WI058_RETIRED <= set(entering) and not WI058_RETIRED & set(current)
    assert set(inputs) - set(current) == ({renamed(k) for k in coverage["unmapped_native_inputs"]} - WI059_EXISTING_MAPPED_PARAMETERS) | WI059_NATIVE_ONLY_PARAMETERS
    assert len(coverage["unmapped_native_inputs"]) == 147
    assert {key: inputs[key] for key in WI059_NATIVE_ONLY_VALUES} == WI059_NATIVE_ONLY_VALUES
    for key in WI059_NATIVE_ONLY_PARAMETERS:
        with pytest.raises(oracle.OracleSeamError, match="no declared oracle mapping"):
            oracle.evaluate({key: inputs[key]})


def test_fixed_references_and_model_owned_proposal():
    assert "magnet_R0" not in oracle.vs.IN
    assert oracle.vs.IN["magnet_R_ref"] == 12.7
    assert oracle.vs.IN["magnet_a_coil_ref"] == 3.1500000000000004
    assert oracle.vs.IN["wall_peak_R_ref"] == 12.7
    assert oracle.vs.IN["R_ref_divertor"] == 12.7
    assert route.proposal_for(14, 1.3, 0) == {
        R: 14,
        route.P + "plasma__a": 1.3,
        route.P + "availability_direct": 0,
    }
    assert json.loads(route.MANIFEST_PATH.read_text())["ties"] == []


def test_current_radius_controls_match_frozen_model_and_independent_oracle(
    tmp_path, stock_simkit_path
):
    from tests.study import financial_radius_controls as controls

    results = controls.check_controls(tmp_path)
    assert results["baseline"]["verdicts"]["divertor_heat_ok"] == "violated"
    assert {k for k, v in results["R14"]["verdicts"].items() if v == "violated"} == {
        "divertor_heat_ok",
        "wall_load_ok",
        "sustainment_ok",
        "loop_capacity_ok",
    }


@pytest.mark.parametrize("point", RETIRED[:4])
def test_current_execution_refuses_retired_radius(point, tmp_path, stock_simkit_path):
    with pytest.raises(route.RouteError, match=OLD):
        route.run_points("retired-radius", [point], tmp_path)


@pytest.mark.parametrize("radius", [4.0, 3.0, 3.1500000000000004, 0.0, -1.0])
def test_current_invalid_radius_is_retained_as_execution_failure(
    radius, tmp_path, stock_simkit_path
):
    cases, _ = route.run_points("invalid-radius", [{R: radius}], tmp_path)
    assert len(cases) == 1
    assert cases[0].state == "execution_failed"
    with pytest.raises(route.RouteError):
        route.csv_rows(cases, ["R"])


@pytest.mark.parametrize(
    "key",
    json.loads(
        (
            ROOT
            / ".project/active/mfe-major-radius-study-package/implementation/contract-coverage.json"
        ).read_text()
    )["unmapped_native_inputs"],
    ids=lambda k: renamed(k),
)
def test_unmapped_native_inputs_remain_explicitly_refused(key):
    key = renamed(key)  # WI-057 (2026-09-13): the key carries its part's path
    if key in WI059_EXISTING_MAPPED_PARAMETERS:
        assert key in oracle.ENTRY_KEY_TO_ORACLE_INPUT
        assert route.validate_proposal({key: 1.0}) is not None
        return
    with pytest.raises(oracle.OracleSeamError, match=key):
        oracle.evaluate({key: 1.0})
