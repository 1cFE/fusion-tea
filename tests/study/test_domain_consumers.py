"""Current independent oracle domain rejection and unchanged valid arithmetic."""

import json
import sys
from pathlib import Path
from tests.study.structure_ledger import renamed_keys, renamed_values


from tests.models.current_mfe_regressions import (WI059_PARAMETERS, WI059_EXISTING_MAPPED_PARAMETERS, WI059_CHANNELS, WI059_ORACLE_ADDED_CHANNELS, WI059_REPLAY, wi059_replay, wi059_dormant_outputs)

from tests.models.current_mfe_regressions import WI060_PARAMETERS, LIVE_CONDUCTOR_CHANNELS

import pytest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "exploration/stellarator_e2e/studies"))
import oracle_entry as oracle

EVIDENCE = ROOT / ".project/active/mfe-domain-study-package/implementation/oracle-before.json"
BEFORE = json.loads(EVIDENCE.read_text())
COIL_RADIUS = BEFORE["controls"][0]["outputs"]["r_coil_centre"]
# WI-058 (2026-09-14): the winding length follows the coil bore, c_coil = c_coil_ref * (r_coil_centre /
# a_coil_ref); the frozen control rows were produced with the R-form c_coil = k_coil * R. At the rows' a = 1.3
# the bore ratio is exactly 1.0, so binding c_coil_ref = k_coil * R reproduces the R-form's length to the
# double (uniform-scaling equivalence) and every frozen output stays the exact expectation. The bore form's
# own response is tested in tests/models/test_winding_length_bore.py, not here.
K_COIL_RETIRED = 1.968503937007874


def wi058_overrides(row):
    overrides = wi059_replay(row["overrides"])
    if "R" in overrides:
        overrides["magnet_c_coil_ref"] = K_COIL_RETIRED * overrides["R"]
    return overrides


def wi058_length(p, r_coil_centre):
    return p["magnet_c_coil_ref"] * (r_coil_centre / p["magnet_a_coil_ref"])


def wi040_expected(row):
    """Restate WI-040 accounts with WI-060 physical-tape pricing using mass identities and linear cost increments.

    Frozen controls remain unchanged. Derive downstream increments from their
    existing capital charge rates, independently of the live oracle cost branches.
    """
    p = oracle.vs.IN | wi058_overrides(row)
    old = row['outputs']
    c_coil = wi058_length(p, old['r_coil_centre'])  # WI-058: the bore form
    expected = dict(old)
    # WI-038 entering controls are at q=1. Preserve old outputs and add the exact
    # effective reference values; off-reference grade claims have separate tests.
    assert p['magnet_B_max'] == p['magnet_B_grade_ref']
    expected.update(conductor_quantity_factor=1.0,
                    conductor_j_wp_effective=p['magnet_j_wp'])
    volume = p['magnet_f_wp_vol'] * p['magnet_n_coils'] * p['magnet_I_coil'] / p['magnet_j_wp'] / 1e6 * c_coil
    rho = p['magnet_helium_pressure'] / p['magnet_helium_gas_constant'] / p['T_cold_cryo']
    materials = ('copper', 'solder', 'steel', 'helium')
    for m in materials:
        mass = volume * p['magnet_f_' + m] * (rho if m == 'helium' else p['magnet_rho_' + m])
        expected['winding_mass_' + m] = mass
        expected['winding_cost_' + m] = mass * p['magnet_price_' + m]
    material_cost = sum(expected['winding_cost_' + m] for m in materials)
    kam = p['magnet_n_coils'] * p['magnet_I_coil'] * p['magnet_f_set'] * c_coil / 1000
    tape_volume = volume * (1 - sum(p['magnet_f_' + m] for m in materials))
    tape_length = tape_volume / (p['magnet_tape_width'] * p['magnet_tape_thickness'])
    tape = tape_length * p['magnet_tape_price_per_m']
    length = 1000 * kam / p['magnet_turn_current']
    fabrication = length * p['magnet_winding_rate_1990'] * p['magnet_cost_escalation'] * p['magnet_nonplanar_factor']
    expected.update(vol_winding_pack=volume, winding_helium_density=rho,
                    winding_tape_volume=volume * (1 - sum(p['magnet_f_' + m] for m in materials)),
                    winding_material_cost=material_cost, tape_procurement_cost=tape, tape_length=tape_length,
                    conductor_length=length, winding_fabrication_cost=fabrication,
                    winding_pack_legacy=old['winding_pack'])
    delta = tape + material_cost + fabrication - old['winding_pack']
    increments = dict(winding_pack=delta, magnet_capital_rollup=delta, powercore_capital=delta,
                      installation=delta * p['installation_frac'])
    increments['cas22_capital'] = delta + increments['installation']
    increments['cas2x_pre_contingency'] = increments['cas22_capital']
    increments['contingency_capital'] = increments['cas22_capital'] * p['contingency_rate']
    increments['cas20_capital'] = increments['cas22_capital'] + increments['contingency_capital']
    increments['cas30_capital'] = increments['cas20_capital'] * p['indirect_fraction'] * p['construction_years'] / p['reference_construction_time']
    increments['indirect_capital'] = increments['cas30_capital']
    increments['supplementary'] = ((p['supp_shipping_frac'] + p['supp_tax_frac']) * increments['cas20_capital'] + p['supp_insurance_frac'] * (increments['cas20_capital'] + increments['cas30_capital'])) * (1 + p['supp_contingency_rate'])
    increments['overnight_capital'] = increments['cas20_capital'] + increments['cas30_capital'] + increments['supplementary']
    increments['total_capital'] = increments['overnight_capital']
    increments['idc_capital'] = increments['overnight_capital'] * old['idc_capital'] / old['overnight_capital']
    increments['cas90_1cfe'] = (increments['overnight_capital'] + increments['idc_capital']) * old['cas90_1cfe'] / (old['overnight_capital'] + old['idc_capital'])
    energy = 8760 * old['p_net'] * old['calendar_availability']
    increments['lcoe'] = increments['total_capital'] / old['total_capital'] * (old['lcoe'] - old['annual_om'] / energy)
    increments['lcoe_1cfe'] = increments['cas90_1cfe'] / (energy * p['n_mod'])
    expected.update({name: old[name] + increment for name, increment in increments.items()})
    expected['reactor_equipment_subtotal'] = expected['powercore_capital'] + old['remote_handling']
    expected.update(wi059_dormant_outputs(expected, p))
    return expected, set(increments) | (expected.keys() - old.keys())


@pytest.mark.parametrize("overrides,message", [
    ({"R": 12.7, "coil_t": 20.0}, "live magnet clearance"),
    ({"R": 3.0}, "live magnet clearance"),
    ({"R": COIL_RADIUS}, "live magnet clearance"),
    ({"magnet_R_ref": 3.0}, "reference magnet clearance"),
    ({"magnet_R_ref": COIL_RADIUS}, "reference magnet clearance"),
    ({"magnet_a_coil_ref": 13.0}, "reference magnet clearance"),
    ({"magnet_a_coil_ref": 12.7}, "reference magnet clearance"),
    ({"T_cold_cryo": -1.0}, "0 < T_cold < T_amb"),
    ({"T_cold_cryo": 0.0}, "0 < T_cold < T_amb"),
    ({"T_cold_cryo": 300.0}, "0 < T_cold < T_amb"),
    ({"T_cold_cryo": 301.0}, "0 < T_cold < T_amb"),
    ({"T_amb_cryo": 20.0}, "0 < T_cold < T_amb"),
    ({"T_amb_cryo": 19.0}, "0 < T_cold < T_amb"),
    ({"T_amb_cryo": 0.0}, "0 < T_cold < T_amb"),
    ({"T_cold_cryo": 0.0, "q_nuc_cryo": 0.0, "p_fixed_cryo": 0.0,
      "p_cryo_direct": 2.0}, "0 < T_cold < T_amb"),
])
def test_oracle_rejects_invalid_domains_and_restores_parameters(overrides, message):
    saved = dict(oracle.vs.IN)
    with pytest.raises(ValueError, match=message):
        oracle._compute(wi059_replay(overrides))
    assert oracle.vs.IN == saved


@pytest.mark.parametrize("suffix,value,message", [
    # WI-057 (2026-09-13): the entry keys carry their part's path (plasma, coil, cryoplant).
    ("plasma__R", 3.0, "live magnet clearance"),
    ("plasma__R", COIL_RADIUS, "live magnet clearance"),
    ("magnet__coil__R_ref", COIL_RADIUS, "reference magnet clearance"),
    ("magnet__coil__a_coil_ref", 13.0, "reference magnet clearance"),
    ("cryoplant__T_cold_cryo", 0.0, "0 < T_cold < T_amb"),
    ("cryoplant__T_cold_cryo", 300.0, "0 < T_cold < T_amb"),
    ("cryoplant__T_cold_cryo", 301.0, "0 < T_cold < T_amb"),
])
def test_supported_adapter_inputs_propagate_deliberate_domain_error(suffix, value, message):
    with pytest.raises(ValueError, match=message):
        oracle.evaluate(WI059_REPLAY | {oracle.P + suffix: value})


@pytest.mark.parametrize("row", BEFORE["controls"])
def test_valid_outputs_exactly_preserved_and_physical_identities(row):
    result = oracle._compute(wi058_overrides(row))
    expected, changed = wi040_expected(row)
    assert result.keys() == expected.keys()
    for name, value in expected.items():
        if name in changed:
            assert result[name] == pytest.approx(value, rel=1e-12, abs=1e-9), name
        else:
            assert result[name] == value, name
    p = {**oracle.vs.IN, **wi058_overrides(row)}
    # Multiply the field relation through by clearance; no division near its pole.
    lhs = result["B_peak"] * (p["R"] - result["r_coil_centre"]) * p["magnet_R_ref"]
    rhs = (result["B_axis"] * p["magnet_peak_ratio"] * p["R"]
           * (p["magnet_R_ref"] - p["magnet_a_coil_ref"]))
    assert lhs == pytest.approx(rhs, rel=1e-12)
    # Refrigerator electrical work times cold temperature equals heat times lift.
    cold_volume = (p["magnet_f_wp_vol"] * p["magnet_n_coils"]
                   * p["magnet_I_coil"] / p["magnet_j_wp"] / 1e6
                   * wi058_length(p, result["r_coil_centre"]) + p["vol_cold_cryo"])  # WI-058: the bore form
    heat = (p["q_nuc_cryo"] * cold_volume * 1e-6 + p["p_fixed_cryo"]) * p["f_uplift_cryo"]
    lhs = (result["p_cryo"] - p["p_cryo_direct"]) * p["f_carnot_cryo"] * p["T_cold_cryo"]
    rhs = heat * (p["T_amb_cryo"] - p["T_cold_cryo"])
    assert lhs == pytest.approx(rhs, rel=1e-12, abs=1e-14)


def test_adapter_contract_and_ambient_limit_preserved():
    from tests.models.current_mfe_regressions import (WI040_PARAMETERS, WI040_CHANNELS, WI038_PARAMETERS,
                                                      WI058_PARAMETERS, WI058_RETIRED)
    old_inputs = renamed_keys(BEFORE['input_mapping'])
    # WI-058 (2026-09-14): the seam maps c_coil_ref in place of the retired k_coil; the count stays 118.
    assert WI058_RETIRED <= old_inputs.keys()
    old_inputs = {k: v for k, v in old_inputs.items() if k not in WI058_RETIRED}
    assert {k: v for k, v in oracle.ENTRY_KEY_TO_ORACLE_INPUT.items() if k not in WI040_PARAMETERS | WI038_PARAMETERS | WI058_PARAMETERS | WI059_PARAMETERS | WI059_EXISTING_MAPPED_PARAMETERS | WI060_PARAMETERS} == old_inputs
    assert oracle.ENTRY_KEY_TO_ORACLE_INPUT.keys() - old_inputs.keys() == WI040_PARAMETERS | WI038_PARAMETERS | WI058_PARAMETERS | WI059_PARAMETERS | WI059_EXISTING_MAPPED_PARAMETERS | WI060_PARAMETERS
    old_outputs = renamed_values(BEFORE['output_mapping'])
    # The old selected winding alias now denotes the additive account; preserve its
    # previous channel under the explicit legacy name, and add the subtotal coverage.
    old_outputs['winding_pack_legacy'] = old_outputs.pop('winding_pack')
    old_outputs['p_cryo'] = oracle.P + 'cryoplant__refrigeration_sum__total'
    extras = WI040_CHANNELS | LIVE_CONDUCTOR_CHANNELS | WI059_ORACLE_ADDED_CHANNELS | {oracle.P + 'reactor_equipment_subtotal__reactor_equipment_subtotal'}
    assert {k: v for k, v in oracle.ORACLE_OUTPUT_TO_CHANNEL.items() if v not in extras} == old_outputs
    assert set(oracle.ORACLE_OUTPUT_TO_CHANNEL.values()) - set(old_outputs.values()) == extras
    assert len(oracle.ENTRY_KEY_TO_ORACLE_INPUT) == 118 + len(WI059_PARAMETERS | WI059_EXISTING_MAPPED_PARAMETERS | WI060_PARAMETERS)
    for suffix in ("cryoplant__T_amb_cryo", "unknown_domain_input"):  # WI-057 (2026-09-13): the key carries its part's path
        with pytest.raises(oracle.OracleSeamError, match="no declared oracle mapping"):
            oracle.evaluate({oracle.P + suffix: 300.0})
