"""WI-072: full independent numeric coverage and preserved strict predicates."""
import json
import math

import pytest

from tests.models.test_winding_pack_cost import ROOT, P, runtime_paths, evaluate


# These two modes preserve the defined historical energy-off scenarios.
# Active matched conversion instead refuses an inconsistent recovered-heat budget.
HISTORICAL_CYCLE = {"turbine__matched_cycle_enabled": 0.,
                    "heat_rejection__cooling_water_enabled": 0.}

CASES = [
    pytest.param({}, id="baseline"),
    pytest.param({"heat_transport__equipment_cost_mode": 0.}, id="energy-only"),
    pytest.param(HISTORICAL_CYCLE | {"heat_transport__secondary_energy_mode": 0.}, id="cost-only"),
    pytest.param(HISTORICAL_CYCLE | {"heat_transport__equipment_cost_mode": 0.,
                  "heat_transport__secondary_energy_mode": 0.,
                  "heat_transport__equipment_enabled": False,
                  "buildings__facilities_enabled": False,
                  "buildings__facilities_cost_mode": 0.,
                  "buildings__facilities_capacity_mode": 0.}, id="disabled"),
    pytest.param({"discount_rate": 0.}, id="zero-discount"),
    pytest.param({"plasma__R": 13.}, id="permitted-radius"),
]


@pytest.mark.codegen_available
@pytest.mark.parametrize("changes", CASES)
def test_all_numeric_channels_and_strict_predicates(evaluate, changes):
    import oracle_entry
    from scripts.study.verify import derive_verdict, package_input_values

    row = evaluate(changes)
    point = {P + key: value for key, value in changes.items()}
    expected = oracle_entry.evaluate(point)
    mapping = oracle_entry.ORACLE_OUTPUT_TO_CHANNEL
    assert len(mapping.values()) == len(set(mapping.values()))
    assert set(row.outputs) == set(expected) == set(mapping.values())
    for key, value in expected.items():
        # Established integrated scalar policy, with tiny mass channels kept
        # meaningful. This tolerance never participates in a physical predicate.
        assert row.outputs[key] == pytest.approx(
            value, rel=1e-9, abs=1e-18 if "__inventory__" in key else 1e-6
        ), key

    independently_computed = oracle_entry._compute(oracle_entry._oracle_overrides(point))
    assert independently_computed["fuel_handling"] == independently_computed["processing_cost"]
    package = ROOT / "exploration/stellarator_e2e/generated"
    defaults = package_input_values(package)
    contract = json.loads((package / "contracts/model_contract.json").read_text())
    entries = contract["constraint_catalog"]["concrete_entries"]
    bindings = oracle_entry.operand_bindings()
    assert set(bindings) == {entry["constraint_id"] for entry in entries}
    for entry in entries:
        cid = entry["constraint_id"]
        for channels in (row.outputs, expected):
            satisfied, _ = derive_verdict(cid, entry, bindings, point, defaults, channels)
            assert row.responses[cid] == ("satisfied" if satisfied else "violated"), cid

    rate = changes.get("discount_rate", defaults[P + "discount_rate"])
    years = defaults[P + "operational_years"]
    assert years == int(years)
    payment_factor = 1 / math.fsum((1 + rate) ** -year for year in range(1, int(years) + 1))
    for suffix in ("cas71_calc__crf", "cas80_calc__crf"):
        assert row.outputs[P + suffix] == pytest.approx(payment_factor, rel=1e-12, abs=1e-14)
    if changes.get("heat_transport__equipment_cost_mode") == 0:
        for suffix in ("consumables_annual", "replacement_annual", "shipping_exclusion"):
            assert row.outputs[P + "heat_transport__cooling_selection__" + suffix] == 0.


@pytest.mark.parametrize("changes", [
    {"heat_transport__equipment_cost_mode": 2.},
    {"heat_transport__secondary_energy_mode": -.1},
    {"heat_transport__equipment_cost_mode": float("nan")},
    {"heat_transport__equipment_enabled": False},
])
def test_independent_mode_validation_refuses(runtime_paths, changes):
    import oracle_entry
    with pytest.raises(ValueError):
        oracle_entry.evaluate({P + key: value for key, value in changes.items()})


@pytest.mark.codegen_available
def test_disabled_cooling_with_live_facilities_remains_incompatible(evaluate):
    import oracle_entry
    from simkit.evaluation.failure import EvaluationFailed
    changes = HISTORICAL_CYCLE | {"heat_transport__equipment_cost_mode": 0.,
               "heat_transport__secondary_energy_mode": 0.,
               "heat_transport__equipment_enabled": False}
    with pytest.raises(EvaluationFailed, match="cooling_helium_count must be positive"):
        evaluate(changes)
    with pytest.raises(ValueError, match="active facilities require enabled cooling equipment"):
        oracle_entry.evaluate({P + key: value for key, value in changes.items()})


@pytest.mark.codegen_available
@pytest.mark.parametrize("changed_mode", ["heat_transport__secondary_energy_mode",
                                         "heat_transport__loop_live"])
def test_active_matched_cycle_refuses_inconsistent_heat_modes(evaluate, changed_mode):
    """A historical recovery switch cannot silently change only the plant heat budget."""
    import oracle_entry
    from simkit.evaluation.failure import EvaluationFailed
    changes = {changed_mode: 0.}
    with pytest.raises(EvaluationFailed, match="plant and cycle heat join"):
        evaluate(changes)
    with pytest.raises(ValueError):
        oracle_entry.evaluate({P + key: value for key, value in changes.items()})
