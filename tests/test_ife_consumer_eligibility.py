"""Caller regressions: invalid zero prices cannot win a sweep or certify an anchor."""
from pathlib import Path

import pytest

from exploration.ife_e2e.eligibility import (
    module_balance, module_price, price_eligible, require_price,
)


@pytest.mark.parametrize("price,generating,verdict", [
    (0.0, 0.0, "violated"), (0.0, 1.0, "satisfied"),
    (1.0, 0.0, "satisfied"), (1.0, 1.0, "violated"),
    (1.0, 1.0, None), (float("nan"), 1.0, "satisfied"),
])
def test_invalid_price_cannot_win_or_anchor(price, generating, verdict):
    candidates = [(price, generating, verdict), (100.0, 1.0, "satisfied")]
    winner = min(p for p, g, v in candidates if price_eligible(p, g, v))
    assert winner == 100.0
    with pytest.raises(ValueError, match="ineligible"):
        require_price(price, generating, verdict)


@pytest.mark.parametrize("thermal,expected", [(0.18, "violated"),
                                               (0.20, "violated"),
                                               (0.21, "satisfied")])
def test_generated_boundary_cannot_certify_invalid_anchor(tmp_path, monkeypatch, thermal, expected):
    # The generated wrapper owns output ordering and production arithmetic.
    root = Path(__file__).resolve().parents[1]
    (tmp_path / "ife_tea").symlink_to(root / "exploration/ife_e2e/generated", target_is_directory=True)
    monkeypatch.syspath_prepend(str(tmp_path))
    params = dict(availability=0.9, blanket_energy_multiple=1.0, discount_rate=0.08,
                  driver_cost_constant=55.0, driver_efficiency=0.1, driver_energy=50e6,
                  driver_lifetime_shots=6e9, frequency=5.0, gain=100.0,
                  om_cost_constant=65.0, plant_cost_constant=2000.0,
                  target_cost_constant=10.0, thermal_efficiency=thermal,
                  yield_cost_constant=5e6, construction_years=5.0, operational_years=40.0)
    balance = module_balance(params)
    price, verdict = module_price(balance)
    assert verdict == expected
    if thermal == 0.20:
        assert balance.net_electric_power == 0.0
    if expected == "violated":
        assert (price.price, price.generating) == (0.0, 0.0)
        with pytest.raises(ValueError, match="ineligible"):
            require_price(price.price, price.generating, verdict)
    else:
        assert require_price(price.price, price.generating, verdict) > 0


@pytest.mark.parametrize("case", ["baseline", "negative", "zero"])
def test_whole_pipeline_both_prices_obey_eligibility(tmp_path, monkeypatch, case):
    import json
    import shutil

    from exploration.ife_e2e.eligibility import NET_POSITIVE_ID, P
    from simkit.core.pipeline import execute_pipeline
    from simkit.io.output_router import WriteHandler, create_output_router_with_json_schemas

    root = Path(__file__).resolve().parents[1]
    package = tmp_path / "ife_tea"
    shutil.copytree(root / "exploration/ife_e2e/generated", package)
    monkeypatch.syspath_prepend(str(tmp_path))
    from ife_tea import CUSTOM_SCHEMA_TYPES, create_ife_tea_registry

    changes = {} if case == "baseline" else {
        P + "driver__efficiency": 0.1, P + "gain": 100.0,
        P + "frequency": 5.0,
        P + "chamber__blanket_energy_multiple": 0.6 if case == "negative" else 1.0,
        P + "thermal_efficiency": 0.3 if case == "negative" else 0.2,
    }
    for path in (package / "inputs").glob("*.json"):
        values = json.loads(path.read_text())
        values.update({key: value for key, value in changes.items() if key in values})
        path.write_text(json.dumps(values))
    router = create_output_router_with_json_schemas(
        list(dict.fromkeys(["RootModel[float]"] + [t.__name__ for t in CUSTOM_SCHEMA_TYPES])))
    router.register_handler("float", WriteHandler(
        fn=lambda value, path: Path(path).write_text(json.dumps(value)), extension=".json"))
    result = execute_pipeline(package / "pipelines/pipeline.yaml", output_dir=tmp_path / "outputs",
                              registry=create_ife_tea_registry(), output_router=router,
                              custom_schema_types=CUSTOM_SCHEMA_TYPES)
    out = {key: value.root if hasattr(value, "root") else value
           for key, value in result.outputs.items()}
    verdict = out[NET_POSITIVE_ID + "__evaluation"].status
    assert out[P + "viability__81ddf10fb1d1749b__evaluation"].status == "satisfied"
    if case == "zero":
        assert out[P + "lcoe_calc__net_electric_power"] == 0.0
    for channel in ("hawker_price", "meier_price"):
        price = out[P + channel + "__price"]
        generating = out[P + channel + "__generating"]
        if case == "baseline":
            assert require_price(price, generating, verdict) > 0
        else:
            assert (price, generating, verdict) == (0.0, 0.0, "violated")
            ranked = [(price, generating, verdict), (100.0, 1.0, "satisfied")]
            assert min(p for p, g, v in ranked if price_eligible(p, g, v)) == 100.0
            with pytest.raises(ValueError, match="ineligible"):
                require_price(price, generating, verdict)
