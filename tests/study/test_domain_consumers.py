"""Current independent oracle domain rejection and unchanged valid arithmetic."""

import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "exploration/stellarator_e2e/studies"))
import oracle_entry as oracle

EVIDENCE = ROOT / ".project/active/mfe-domain-study-package/implementation/oracle-before.json"
BEFORE = json.loads(EVIDENCE.read_text())
COIL_RADIUS = BEFORE["controls"][0]["outputs"]["r_coil_centre"]


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
        oracle._compute(overrides)
    assert oracle.vs.IN == saved


@pytest.mark.parametrize("suffix,value,message", [
    ("R", 3.0, "live magnet clearance"),
    ("R", COIL_RADIUS, "live magnet clearance"),
    ("magnet__R_ref", COIL_RADIUS, "reference magnet clearance"),
    ("magnet__a_coil_ref", 13.0, "reference magnet clearance"),
    ("T_cold_cryo", 0.0, "0 < T_cold < T_amb"),
    ("T_cold_cryo", 300.0, "0 < T_cold < T_amb"),
    ("T_cold_cryo", 301.0, "0 < T_cold < T_amb"),
])
def test_supported_adapter_inputs_propagate_deliberate_domain_error(suffix, value, message):
    with pytest.raises(ValueError, match=message):
        oracle.evaluate({oracle.P + suffix: value})


@pytest.mark.parametrize("row", BEFORE["controls"])
def test_valid_outputs_exactly_preserved_and_physical_identities(row):
    result = oracle._compute(row["overrides"])
    assert result == row["outputs"]
    p = {**oracle.vs.IN, **row["overrides"]}
    # Multiply the field relation through by clearance; no division near its pole.
    lhs = result["B_peak"] * (p["R"] - result["r_coil_centre"]) * p["magnet_R_ref"]
    rhs = (result["B_axis"] * p["magnet_peak_ratio"] * p["R"]
           * (p["magnet_R_ref"] - p["magnet_a_coil_ref"]))
    assert lhs == pytest.approx(rhs, rel=1e-12)
    # Refrigerator electrical work times cold temperature equals heat times lift.
    cold_volume = (p["magnet_f_wp_vol"] * p["magnet_n_coils"]
                   * p["magnet_I_coil"] / p["magnet_j_wp"] / 1e6
                   * p["magnet_k_coil"] * p["R"] + p["vol_cold_cryo"])
    heat = (p["q_nuc_cryo"] * cold_volume * 1e-6 + p["p_fixed_cryo"]) * p["f_uplift_cryo"]
    lhs = (result["p_cryo"] - p["p_cryo_direct"]) * p["f_carnot_cryo"] * p["T_cold_cryo"]
    rhs = heat * (p["T_amb_cryo"] - p["T_cold_cryo"])
    assert lhs == pytest.approx(rhs, rel=1e-12, abs=1e-14)


def test_adapter_contract_and_ambient_limit_preserved():
    assert oracle.ENTRY_KEY_TO_ORACLE_INPUT == BEFORE["input_mapping"]
    assert oracle.ORACLE_OUTPUT_TO_CHANNEL == BEFORE["output_mapping"]
    assert len(oracle.ENTRY_KEY_TO_ORACLE_INPUT) == 99
    for suffix in ("T_amb_cryo", "unknown_domain_input"):
        with pytest.raises(oracle.OracleSeamError, match="no declared oracle mapping"):
            oracle.evaluate({oracle.P + suffix: 300.0})
