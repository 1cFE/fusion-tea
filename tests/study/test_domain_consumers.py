"""Current independent oracle domain rejection and unchanged valid arithmetic."""

import json
import sys
from pathlib import Path

import pytest

from tests.models.current_mfe_regressions import (
    ADDITIONAL_DOMAIN,
    ADDITIONAL_MAPPING,
    CURRENT_NUMERIC,
    CURRENT_PREDICATES,
    LIVE_CONDUCTOR_CHANNELS,
    MR7_DELTA,
    MR7_LOCALS,
    MR7_PARAMETERS,
    MR7_RETIRED_CHANNELS,
    MR7_RETIRED_LOCALS,
    MR7_RETIRED_PARAMETERS,
    WI059_CHANNELS,
    WI059_EXISTING_MAPPED_PARAMETERS,
    WI059_ORACLE_ADDED_CHANNELS,
    WI059_PARAMETERS,
    WI059_REPLAY,
    WI060_PARAMETERS,
    WI061_CHANNELS,
    WI061_MAPPED_PARAMETERS,
    WI061_PARAMETERS,
    WI062_CHANNELS,
    WI062_PARAMETERS,
    WI063_CHANNELS,
    WI063_PARAMETERS,
    assert_current_predicates,
    wi059_dormant_outputs,
    wi059_replay,
)
from tests.study.structure_ledger import renamed_keys, renamed_values

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "exploration/stellarator_e2e/studies"))
import oracle_entry as oracle

EVIDENCE = ROOT / ".project/active/mfe-domain-study-package/implementation/oracle-before.json"
BEFORE = json.loads(EVIDENCE.read_text())
COIL_RADIUS = BEFORE["controls"][0]["outputs"]["r_coil_centre"]
# WI-058 (2026-09-14): the winding length follows the coil bore, c_coil = c_coil_ref *
# (r_coil_centre /
# a_coil_ref); the frozen control rows were produced with the R-form c_coil = k_coil * R. At the
# rows' a = 1.3
# the bore ratio is exactly 1.0, so binding c_coil_ref = k_coil * R reproduces the R-form's length
# to the
# double (uniform-scaling equivalence) and every frozen output stays the exact expectation. The
# bore form's
# own response is tested in tests/models/test_winding_length_bore.py, not here.
K_COIL_RETIRED = 1.968503937007874


def historical_supplied_overrides(row):
    """Explicit test construction of WI-079 offers from the frozen demand basis.

    These controls exercise the old consumer scenario. Current native controls
    separately retain the current fixed offers; no historical receipt is changed.
    """
    old = row["outputs"]
    values = {}
    for local, _ in oracle.vs.oracle_procurement.PUBLIC_DEFAULTS.values():
        if "thermal_electric_class" in local or "gross" in local:
            values[local] = old["p_et"]
        elif "net_class" in local:
            values[local] = old["p_net"]
        elif "fusion_class" in local:
            values[local] = old["p_fus"]
        elif "thermal_class" in local:
            values[local] = old["p_th"]
    for equipment in ("turbine", "heat_rejection", "power_supplies", "divertor"):
        values["selected_" + equipment + "_purchase_cost_per_module"] = old[equipment]
    values["selected_cryoplant_purchase_cost_per_module"] = old["cryo_cost"]
    # WI-075 makes hardware choices explicit. Reconstruct only this historical scenario.
    values["magnet_m_casing"] = old["m_casing"]
    legacy = oracle.vs.IN | row["overrides"]
    current = legacy.get(
        "magnet_I_coil", legacy["magnet_reference_turns"] * legacy["magnet_turn_current"]
    )
    # Historical baseline density: verify_stellaris.py@18b67dd5:295.
    density = legacy.get("magnet_j_wp", 118.8271604938272)
    if "magnet_I_coil" in row["overrides"] or "magnet_j_wp" in row["overrides"]:
        values["magnet_reference_turns"] = current / legacy["magnet_turn_current"]
        values["magnet_wp_side"] = (current / density) ** 0.5 / 1000.0
    return values


def wi058_overrides(row):
    overrides = wi059_replay(
        {k: v for k, v in row["overrides"].items() if k not in {"magnet_I_coil", "magnet_j_wp"}}
    ) | historical_supplied_overrides(row)
    if "R" in overrides:
        overrides["magnet_c_coil_ref"] = K_COIL_RETIRED * overrides["R"]
        # Explicit test-only construction of the frozen radius-selected casing.
        overrides["magnet_m_casing"] = 63000.0 * (12.7 / overrides["R"]) ** 0.78
    return overrides


def wi058_length(p, r_coil_centre):
    return p["magnet_c_coil_ref"] * (r_coil_centre / p["magnet_a_coil_ref"])


def wi040_expected(row):
    """Restate WI-040 accounts with WI-060 physical-tape pricing.

    Use mass identities and linear cost increments.

    Frozen controls remain unchanged. Derive downstream increments from their
    existing capital charge rates, independently of the live oracle cost branches.
    """
    p = oracle.vs.IN | wi058_overrides(row)
    old = row["outputs"]
    c_coil = wi058_length(p, old["r_coil_centre"])  # WI-058: the bore form
    expected = dict(old)
    # MR-7: current explicit hardware, with independent material/price identities.
    # Frozen rows remain the financial base; no hidden field-grade construction.
    volume = p["magnet_f_wp_vol"] * p["magnet_n_coils"] * p["magnet_wp_side"] ** 2 * c_coil
    rho = p["magnet_helium_pressure"] / p["magnet_helium_gas_constant"] / p["T_cold_cryo"]
    materials = ("copper", "solder", "steel", "helium")
    for m in materials:
        mass = volume * p["magnet_f_" + m] * (rho if m == "helium" else p["magnet_rho_" + m])
        expected["winding_mass_" + m] = mass
        expected["winding_cost_" + m] = mass * p["magnet_price_" + m]
    material_cost = sum(expected["winding_cost_" + m] for m in materials)
    tape_volume = volume * (1 - sum(p["magnet_f_" + m] for m in materials))
    tape_length = tape_volume / (p["magnet_tape_width"] * p["magnet_tape_thickness"])
    tape = tape_length * p["magnet_tape_price_per_m"]
    length = p["magnet_n_coils"] * p["magnet_reference_turns"] * p["magnet_f_set"] * c_coil
    fabrication = (
        length
        * p["magnet_winding_rate_1990"]
        * p["magnet_cost_escalation"]
        * p["magnet_nonplanar_factor"]
    )
    expected.update(
        vol_winding_pack=volume,
        winding_helium_density=rho,
        winding_tape_volume=volume * (1 - sum(p["magnet_f_" + m] for m in materials)),
        winding_material_cost=material_cost,
        tape_procurement_cost=tape,
        tape_length=tape_length,
        conductor_length=length,
        winding_fabrication_cost=fabrication,
        winding_pack_legacy=old["winding_pack"],
    )
    delta = tape + material_cost + fabrication - old["winding_pack"]
    increments = dict(
        winding_pack=delta,
        magnet_capital_rollup=delta,
        powercore_capital=delta,
        installation=delta * p["installation_frac"],
    )
    increments["cas22_capital"] = delta + increments["installation"]
    increments["cas2x_pre_contingency"] = increments["cas22_capital"]
    increments["contingency_capital"] = increments["cas22_capital"] * p["contingency_rate"]
    increments["cas20_capital"] = increments["cas22_capital"] + increments["contingency_capital"]
    increments["cas30_capital"] = (
        increments["cas20_capital"]
        * p["indirect_fraction"]
        * p["construction_years"]
        / p["reference_construction_time"]
    )
    increments["indirect_capital"] = increments["cas30_capital"]
    increments["supplementary"] = (
        (p["supp_shipping_frac"] + p["supp_tax_frac"]) * increments["cas20_capital"]
        + p["supp_insurance_frac"] * (increments["cas20_capital"] + increments["cas30_capital"])
    ) * (1 + p["supp_contingency_rate"])
    increments["overnight_capital"] = (
        increments["cas20_capital"] + increments["cas30_capital"] + increments["supplementary"]
    )
    increments["total_capital"] = increments["overnight_capital"]
    increments["idc_capital"] = (
        increments["overnight_capital"] * old["idc_capital"] / old["overnight_capital"]
    )
    increments["cas90_1cfe"] = (
        (increments["overnight_capital"] + increments["idc_capital"])
        * old["cas90_1cfe"]
        / (old["overnight_capital"] + old["idc_capital"])
    )
    energy = 8760 * old["p_net"] * old["calendar_availability"]
    increments["lcoe"] = (
        increments["total_capital"]
        / old["total_capital"]
        * (old["lcoe"] - old["annual_om"] / energy)
    )
    increments["lcoe_1cfe"] = increments["cas90_1cfe"] / (energy * p["n_mod"])
    expected.update({name: old[name] + increment for name, increment in increments.items()})
    expected["reactor_equipment_subtotal"] = expected["powercore_capital"] + old["remote_handling"]
    expected.update(wi059_dormant_outputs(expected, p))
    expected.update({"fit_" + k: v for k, v in oracle.vs._winding_fit(p).items()})
    return expected, set(increments) | (expected.keys() - old.keys())


@pytest.mark.parametrize(
    "overrides,message",
    [
        ({"R": 12.7, "coil_t": 20.0}, "live magnet clearance"),
        ({"R": 3.0}, "live magnet clearance"),
        ({"R": COIL_RADIUS}, "live magnet clearance"),
        ({"magnet_R_ref": 3.0}, "reference magnet clearance"),
        ({"magnet_R_ref": COIL_RADIUS}, "reference magnet clearance"),
        ({"magnet_a_coil_ref": 13.0}, "reference magnet clearance"),
        ({"magnet_a_coil_ref": 12.7}, "reference magnet clearance"),
        ({"T_cold_cryo": -1.0}, "oracle cryoplant: require 0 < T_cold < T_amb"),
        ({"T_cold_cryo": 0.0}, "oracle cryoplant: require 0 < T_cold < T_amb"),
        ({"T_cold_cryo": 300.0}, "oracle cryoplant: require 0 < T_cold < T_amb"),
        ({"T_cold_cryo": 301.0}, "oracle cryoplant: require 0 < T_cold < T_amb"),
        ({"T_amb_cryo": 20.0}, "0 < T_cold < T_amb"),
        ({"T_amb_cryo": 19.0}, "0 < T_cold < T_amb"),
        ({"T_amb_cryo": 0.0}, "0 < T_cold < T_amb"),
        (
            {"T_cold_cryo": 0.0, "q_nuc_cryo": 0.0, "p_fixed_cryo": 0.0, "p_cryo_direct": 2.0},
            "oracle cryoplant: require 0 < T_cold < T_amb",
        ),
    ],
)
def test_oracle_rejects_invalid_domains_and_restores_parameters(overrides, message):
    saved = dict(oracle.vs.IN)
    with pytest.raises(ValueError, match=message):
        oracle._compute(wi059_replay(overrides))
    assert oracle.vs.IN == saved


@pytest.mark.parametrize(
    "suffix,value,message",
    [
        # WI-057 (2026-09-13): the entry keys carry their part's path (plasma, coil, cryoplant).
        ("plasma__R", 3.0, "live magnet clearance"),
        ("plasma__R", COIL_RADIUS, "live magnet clearance"),
        ("magnet__coil__R_ref", COIL_RADIUS, "reference magnet clearance"),
        ("magnet__coil__a_coil_ref", 13.0, "reference magnet clearance"),
        ("cryoplant__T_cold_cryo", 0.0, "oracle cryoplant: require 0 < T_cold < T_amb"),
        ("cryoplant__T_cold_cryo", 300.0, "oracle cryoplant: require 0 < T_cold < T_amb"),
        ("cryoplant__T_cold_cryo", 301.0, "oracle cryoplant: require 0 < T_cold < T_amb"),
    ],
)
def test_supported_adapter_inputs_propagate_deliberate_domain_error(suffix, value, message):
    with pytest.raises(ValueError, match=message):
        oracle.evaluate(WI059_REPLAY | {oracle.P + suffix: value})


@pytest.mark.parametrize("row", BEFORE["controls"])
def test_valid_outputs_exactly_preserved_and_physical_identities(row):
    overrides = wi058_overrides(row)
    if overrides.get("T_cold_cryo", 20.0) != 20.0:
        # WI-062 adds the narrower material-temperature domain to the full plant.
        with pytest.raises(ValueError, match="unsupported temperature/construction"):
            oracle._compute(overrides)
        return
    result = oracle._compute(overrides)
    expected, changed = wi040_expected(row)
    part = ADDITIONAL_DOMAIN[str(BEFORE["controls"].index(row))]
    unchanged = set(part["unaffected_exact_locals"])
    changed_names = set(part["changed_current_equation_locals"])
    assert set(row["outputs"]) == unchanged | changed_names
    assert (
        set(result)
        == (set(row["outputs"]) | set(part["added_local_names"]) | MR7_LOCALS) - MR7_RETIRED_LOCALS
    )
    unchanged -= MR7_RETIRED_LOCALS
    changed -= MR7_RETIRED_LOCALS
    changed_names -= MR7_RETIRED_LOCALS
    for name in unchanged:
        assert result[name] == row["outputs"][name], name
    for name in changed | changed_names:
        value = (
            result["breeding_tbr_mean"] - result["fuel_tbr_required"]
            if name == "fuel_tbr_margin"
            else expected[name]
        )
        assert result[name] == pytest.approx(value, rel=1e-12, abs=1e-9), name
    p = {**oracle.vs.IN, **wi058_overrides(row)}
    # Multiply the field relation through by clearance; no division near its pole.
    lhs = result["B_peak"] * (p["R"] - result["r_coil_centre"]) * p["magnet_R_ref"]
    rhs = (
        result["B_axis"]
        * p["magnet_peak_ratio"]
        * p["R"]
        * (p["magnet_R_ref"] - p["magnet_a_coil_ref"])
    )
    assert lhs == pytest.approx(rhs, rel=1e-12)
    # Refrigerator electrical work times cold temperature equals heat times lift.
    cold_volume = (
        p["magnet_f_wp_vol"]
        * p["magnet_n_coils"]
        * p["magnet_wp_side"] ** 2
        * wi058_length(p, result["r_coil_centre"])
        + p["vol_cold_cryo"]
    )  # WI-058: the bore form
    heat = (p["q_nuc_cryo"] * cold_volume * 1e-6 + p["p_fixed_cryo"]) * p["f_uplift_cryo"]
    lhs = (result["p_cryo"] - p["p_cryo_direct"]) * p["f_carnot_cryo"] * p["T_cold_cryo"]
    rhs = heat * (p["T_amb_cryo"] - p["T_cold_cryo"])
    assert lhs == pytest.approx(rhs, rel=1e-12, abs=1e-14)


def test_adapter_contract_and_ambient_limit_preserved():
    assert (
        set(oracle.ENTRY_KEY_TO_ORACLE_INPUT)
        == (set(ADDITIONAL_MAPPING["mapped_input_keys"]) - MR7_RETIRED_PARAMETERS) | MR7_PARAMETERS
    )
    for key, value in ADDITIONAL_MAPPING["unchanged_input_bindings"].items():
        if key in MR7_RETIRED_PARAMETERS:
            continue
        assert oracle.ENTRY_KEY_TO_ORACLE_INPUT[key] == value, key
    expected = (
        ADDITIONAL_MAPPING["historical_output_bindings_after_explicit_alias_translation"]
        | ADDITIONAL_MAPPING["added_output_bindings"]
    )
    expected = {key: value for key, value in expected.items() if value not in MR7_RETIRED_CHANNELS}
    expected.update(MR7_DELTA["added_local_bindings"])
    assert oracle.ORACLE_OUTPUT_TO_CHANNEL == expected
    assert set(expected.values()) == CURRENT_NUMERIC
    assert len(expected) == len(set(expected.values()))
    for suffix in ("cryoplant__T_amb_cryo", "unknown_domain_input"):
        with pytest.raises(oracle.OracleSeamError, match="no declared oracle mapping"):
            oracle.evaluate({oracle.P + suffix: 300.0})


@pytest.mark.parametrize(
    "cold,dormant",
    [
        (-1.0, False),
        (0.0, False),
        (300.0, False),
        (301.0, False),
        (0.0, True),
        (0.0, False),
        (300.0, False),
        (301.0, False),
    ],
)
def test_original_cryoplant_domain_guard_remains(cold, dormant, stock_simkit_path):
    sys.path.insert(0, str(ROOT / "exploration/stellarator_e2e/pkg"))
    from stellarator_tea.handwritten.mfe_cryo_plant.cryoplant_electrical_power_impl import (
        run_cryoplant_electrical_power,
    )
    from stellarator_tea.modules.mfe_cryo_plant.cryoplant_electrical_power import (
        Cryoplant_Electrical_PowerInput,
    )

    inputs = Cryoplant_Electrical_PowerInput(
        T_cold=cold,
        T_amb=300.0,
        q_nuc=0.0 if dormant else 1000.0,
        vol_cold=1.0,
        p_fixed=0.0 if dormant else 0.1,
        f_uplift=1.0,
        f_carnot=0.2,
        p_direct=2.0 if dormant else 0.0,
    )
    with pytest.raises(
        ValueError, match="^Cryoplant Electrical Power: require 0 < T_cold < T_amb$"
    ):
        run_cryoplant_electrical_power(inputs)


def test_three_qualified_domain_rows_have_complete_independent_native_coverage(
    tmp_path, stock_simkit_path
):
    from types import SimpleNamespace

    import study_route as route

    names = {local: key for key, local in oracle.ENTRY_KEY_TO_ORACLE_INPUT.items()}
    names.update(
        {
            "q_nuc_cryo": oracle.P + "magnet__winding_pack__q_nuc_cryo",
            "p_fixed_cryo": oracle.P + "cryoplant__p_fixed_cryo",
            "p_cryo_direct": oracle.P + "cryoplant__p_cryo",
        }
    )
    points = []
    expectations = []
    for index in (0, 1, 3):
        row = BEFORE["controls"][index]
        point = WI059_REPLAY | {names[k]: v for k, v in wi058_overrides(row).items()}
        if "R" in row["overrides"]:
            point[names["magnet_c_coil_ref"]] = K_COIL_RETIRED * row["overrides"]["R"]
            point[names["magnet_m_casing"]] = 63000.0 * (12.7 / row["overrides"]["R"]) ** 0.78
        points.append(point)
        independent = oracle._compute(wi058_overrides(row))
        expectations.append(
            {
                channel: float(independent[name])
                for name, channel in oracle.ORACLE_OUTPUT_TO_CHANNEL.items()
            }
        )
    cases, _ = route.run_points("domain-historical-qualified", points, tmp_path)
    assert len(cases) == 3
    for case, point, expected in zip(cases, points, expectations):
        assert case.state == "completed"
        assert set(case.outputs) == set(expected) == CURRENT_NUMERIC
        for key, value in expected.items():
            assert case.outputs[key] == pytest.approx(value, rel=1e-9, abs=1e-9), key
        assert_current_predicates(
            SimpleNamespace(
                outputs=case.outputs, responses=dict(case.verdicts, headline=case.headline)
            ),
            point,
            expected,
        )
