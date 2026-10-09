"""Independent winding-pack magnitudes, units and current adapter boundary."""

import json
import math
import sys
from pathlib import Path

import pytest

from tests.models.current_mfe_regressions import (
    CURRENT_NUMERIC,
    LATER_MAPPED_EXISTING,
    LIVE_CONDUCTOR_CHANNELS,
    MR7_PREDICATES,
    WI038_PARAMETERS,
    WI040_CHANNELS,
    WI040_PARAMETERS,
    WI058_PARAMETERS,
    WI058_RETIRED,
    WI059_CHANNELS,
    WI059_EXISTING_MAPPED_PARAMETERS,
    WI059_ORACLE_ADDED_CHANNELS,
    WI059_PARAMETERS,
    WI059_REPLAY,
    WI060_PARAMETERS,
    WI061_CHANNELS,
    WI061_MAPPED_PARAMETERS,
    WI062_CHANNELS,
    WI062_PARAMETERS,
    WI063_CHANNELS,
    WI063_PARAMETERS,
    assert_current_predicates,
)
from tests.study.structure_ledger import renamed_keys, renamed_values
from tests.study.test_domain_consumers import wi040_expected, wi058_overrides

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "exploration/stellarator_e2e/studies"))
import oracle_entry as oracle

BEFORE = json.loads(
    (
        ROOT / ".project/active/winding-pack-current-consumers/implementation/oracle-before.json"
    ).read_text()
)
INVALID = [
    ({"magnet_I_coil": -1.0}, "I_coil must be finite and nonnegative"),
    ({"magnet_I_coil": -1.0, "magnet_j_wp": -2.0}, "I_coil must be finite and nonnegative"),
    ({"magnet_I_coil": math.nan}, "I_coil must be finite and nonnegative"),
    ({"magnet_I_coil": math.inf}, "I_coil must be finite and nonnegative"),
    ({"magnet_I_coil": -math.inf}, "I_coil must be finite and nonnegative"),
    ({"magnet_j_wp": -1.0}, "j_wp must be finite and positive"),
    ({"magnet_j_wp": 0.0}, "j_wp must be finite and positive"),
    ({"magnet_j_wp": math.nan}, "j_wp must be finite and positive"),
    ({"magnet_j_wp": math.inf}, "j_wp must be finite and positive"),
    ({"magnet_j_wp": -math.inf}, "j_wp must be finite and positive"),
    ({"magnet_I_coil": 0.0}, "oracle current sizing: invalid loading"),
]


@pytest.mark.parametrize("local", ["magnet_I_coil", "magnet_j_wp"])
@pytest.mark.parametrize("value", [-1.0, 0.0, math.nan, math.inf, -math.inf])
def test_retired_sizing_inputs_are_refused(local, value):
    suffix = "magnet__coil__I_coil" if local == "magnet_I_coil" else "magnet__winding_pack__j_wp"
    with pytest.raises(oracle.OracleSeamError, match="retired magnet entry keys"):
        oracle.evaluate({oracle.P + suffix: value})
    with pytest.raises(ValueError, match="retired magnet oracle inputs"):
        oracle._compute({local: value})


@pytest.mark.parametrize(
    "local", ["magnet_reference_turns", "magnet_turn_current", "magnet_wp_side"]
)
@pytest.mark.parametrize("value", [-1.0, 0.0, math.nan, math.inf, -math.inf])
def test_invalid_public_oracle_inputs_are_deliberate(local, value):
    names = {v: k for k, v in oracle.ENTRY_KEY_TO_ORACLE_INPUT.items()}
    saved = dict(oracle.vs.IN)
    with pytest.raises(ValueError, match="oracle Winding Operating State: invalid " + local):
        oracle.evaluate(WI059_REPLAY | {names[local]: value})
    assert oracle.vs.IN == saved


@pytest.mark.parametrize(
    "current,density,side",
    [(0.0, 1.0, 0.0), (1e6, 100.0, 0.1), (4e6, 100.0, 0.2), (4e6, 400.0, 0.1)],
)
def test_local_sizing_area_units_and_scale(current, density, side):
    actual = oracle.vs._winding_pack_side(current, density)
    assert actual == side
    assert (actual * 1000.0) ** 2 * density == pytest.approx(current, rel=1e-12)
    assert oracle.vs._winding_pack_side(current * 4.0, density) == actual * 2.0
    assert oracle.vs._winding_pack_side(current, density * 4.0) == actual / 2.0


@pytest.mark.parametrize("overrides,message", INVALID[:-1])
def test_local_sizing_invalid_magnitudes(overrides, message):
    values = dict(magnet_I_coil=1.0, magnet_j_wp=1.0) | overrides
    with pytest.raises(ValueError, match=message):
        oracle.vs._winding_pack_side(values["magnet_I_coil"], values["magnet_j_wp"])


def test_zero_field_is_rejected_by_sustainment_consumer():
    # Test the existing consumer directly; zero sizing is separately accepted above.
    with pytest.raises(RuntimeError, match="B_axis must be nonzero"):
        oracle.vs._sustainment(oracle.vs.IN, 1000.0, 0.0)
    # WI-062 rejects zero actual field before the downstream sustainment calculation.
    with pytest.raises(ValueError, match="conductor current: invalid field"):
        oracle.evaluate(
            {oracle.P + "magnet__coil__k_link": 0.0}
        )  # WI-057 (2026-09-13): the key carries its part's path


@pytest.mark.parametrize("row", BEFORE["controls"])
def test_valid_full_oracle_outputs_and_stress_units_preserved(row):
    actual = oracle._compute(wi058_overrides(row))
    # WI-040: independently derive only the additive-account cost increments;
    # all frozen physics and unrelated output values retain exact comparison.
    expected, changed = wi040_expected(row)
    from tests.models.current_mfe_regressions import assert_local_partition

    index = BEFORE["controls"].index(row)
    changed_partition = assert_local_partition(
        "winding-local-" + str(index), actual, row["outputs"]
    )
    for name in changed:
        assert actual[name] == pytest.approx(expected[name], rel=1e-12, abs=1e-9), name
    p = oracle.vs.IN | wi058_overrides(row)
    current = p["magnet_reference_turns"] * p["magnet_turn_current"]
    side = p["magnet_wp_side"]
    assert actual["winding_I_coil"] == current
    assert actual["winding_j_wp_effective"] * side**2 * 1e6 == pytest.approx(current, rel=1e-12)
    # Current stress evaluates supplied square side in metres.
    expected = p["magnet_k_sigma"] * actual["B_peak"] * current / side
    assert actual["sigma_wp"] == pytest.approx(expected, rel=1e-12)


def test_adapter_coverage_remains_exact():
    from tests.models.current_mfe_regressions import (
        ALL_ADDED_PARAMETERS,
        ALL_RETIRED_PARAMETERS,
        MR7_RETIRED_CHANNELS,
        MR7_RETIRED_LOCALS,
        PROFILE_MAPPED,
        WI059_NATIVE_ONLY_PARAMETERS,
    )

    old_inputs = renamed_keys(BEFORE["input_mapping"])
    added = (
        (ALL_ADDED_PARAMETERS - WI059_NATIVE_ONLY_PARAMETERS)
        | WI059_EXISTING_MAPPED_PARAMETERS
        | WI061_MAPPED_PARAMETERS
        | PROFILE_MAPPED
        | set(LATER_MAPPED_EXISTING)
    )
    assert (
        set(oracle.ENTRY_KEY_TO_ORACLE_INPUT) == (set(old_inputs) - ALL_RETIRED_PARAMETERS) | added
    )
    for key, value in old_inputs.items():
        if key not in ALL_RETIRED_PARAMETERS:
            assert oracle.ENTRY_KEY_TO_ORACLE_INPUT[key] == value, key
    assert set(oracle.ORACLE_OUTPUT_TO_CHANNEL.values()) == CURRENT_NUMERIC
    assert len(set(oracle.ORACLE_OUTPUT_TO_CHANNEL.values())) == len(
        oracle.ORACLE_OUTPUT_TO_CHANNEL
    )
    expected = renamed_values(BEFORE["output_mapping"])
    expected["winding_pack_legacy"] = expected.pop("winding_pack")
    expected["p_cryo"] = oracle.P + "cryoplant__refrigeration_sum__total"
    for old, new in [
        ("buildings", "buildings_legacy"),
        ("precon", "precon_legacy"),
        ("coolant", "coolant_legacy"),
        ("fuel_handling", "fuel_handling_legacy"),
    ]:
        expected[new] = expected.pop(old)
    expected["calendar_cas72_annual"] = expected.pop("cas72_annual")
    for key, value in expected.items():
        if key in MR7_RETIRED_LOCALS or value in MR7_RETIRED_CHANNELS:
            continue
        assert oracle.ORACLE_OUTPUT_TO_CHANNEL[key] == value, (key, value)
    assert (
        oracle.ORACLE_OUTPUT_TO_CHANNEL["cas72_annual"] == oracle.P + "cooling_annual__cas72_total"
    )


def test_current_native_winding_route_agrees_with_independent_oracle(tmp_path, stock_simkit_path):
    import study_route as route

    names = {value: key for key, value in oracle.ENTRY_KEY_TO_ORACLE_INPUT.items()}
    points = [
        WI059_REPLAY
        | {
            names[key]: value
            for key, value in wi058_overrides(row).items()
            if not key.startswith("selected_")
        }
        for row in BEFORE["controls"]
    ]
    cases, _ = route.run_points("winding-consumer-controls", points, tmp_path)
    assert len(cases) == len(points)
    for index, case in enumerate(cases):
        assert case.state == "completed", (dict(case.inputs), case.state)
        expected = oracle.evaluate(case.inputs)
        assert (
            set(case.outputs) == set(expected) == CURRENT_NUMERIC
        )  # WI-038 adds three grade outputs
        for key, value in expected.items():
            assert case.outputs[key] == pytest.approx(value, rel=1e-9, abs=1e-9), key
        from types import SimpleNamespace

        assert_current_predicates(
            SimpleNamespace(
                outputs=case.outputs, responses=dict(case.verdicts, headline=case.headline)
            ),
            case.inputs,
            expected,
        )
        if index == 0:
            assert {
                key
                for key, value in route.short_verdicts(case).items()
                if value == "violated"
                and key
                not in {cid.removeprefix(oracle.P).rsplit("__", 1)[0] for cid in MR7_PREDICATES}
            } == {"divertor_heat_ok", "wp_fit_ok", "reference_conductor_current_ok", "tbr_ok"}


def test_combined_retired_public_sizing_inputs_are_refused():
    """Preserve the original two-input payload under the current retired-key contract."""
    overrides = {"magnet_I_coil": -1.0, "magnet_j_wp": -2.0}
    point = {
        oracle.P + "magnet__coil__I_coil": overrides["magnet_I_coil"],
        oracle.P + "magnet__winding_pack__j_wp": overrides["magnet_j_wp"],
    }
    saved = dict(oracle.vs.IN)
    with pytest.raises(oracle.OracleSeamError, match="retired magnet entry keys") as exc:
        oracle.evaluate(WI059_REPLAY | point)
    # Refusal precedes magnitude conversion and names both retired keys in sorted order.
    assert str(exc.value) == (
        f"retired magnet entry keys {sorted(point)}; "
        "migrate to supplied pack side, reference turns and masses"
    )
    assert oracle.vs.IN == saved
