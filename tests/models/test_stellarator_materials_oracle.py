"""Pure-oracle tests for the WI-100 glue oracle (T-015 independent oracle author).

The oracle under test is exploration/stellarator_materials/oracle_glue.py, written from the
reviewed WI-100 design (with Recheck R1-R6) and plant contract r4 only. These tests run no model
package: they check the oracle against the pinned reference record, against the plant oracle it
composes, and against the design's stated identities and anchors.

Run: .codex-test/run python -m pytest tests/models/test_stellarator_materials_oracle.py -q
"""
from __future__ import annotations

import importlib.util
import json
import math
import random
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
GLUE_PATH = ROOT / "exploration" / "stellarator_materials" / "oracle_glue.py"


def _load_glue():
    name = "wi100_oracle_glue"
    if name in sys.modules:
        return sys.modules[name]
    spec = importlib.util.spec_from_file_location(name, GLUE_PATH)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


g = _load_glue()
vs, oe, r1 = g.vs, g.oe, g.r1
P = g.REFERENCE_PREFIX


def _rel(a, b):
    return abs(a - b) / abs(b) if b != 0 else abs(a - b)


def _same(a, b):
    return a == b or (isinstance(a, float) and isinstance(b, float) and math.isnan(a) and math.isnan(b))


# ---------------------------------------------------------------------------------------------
# Shared cases
# ---------------------------------------------------------------------------------------------
@pytest.fixture(scope="module")
def pin_outputs():
    return json.loads(g.PIN_OUTPUTS_PATH.read_text())["outputs"]


@pytest.fixture(scope="module")
def plant_reference():
    return vs.compute()


def _construction_C():
    """Construction C (Stellaris Table 7), calibrated from the plant's own composition fractions.

    Per-turn areas = fraction x the pack share wp_side^2 / turns (420.779 mm2 at 50 kA); copper and
    steel per kA at 50 kA, steel scaled by B/24.9 T; cabling 1, void 0, insulation 0, helium in misc
    (contract section 4; Round 1 oracle-notes.md, construction C and A2).
    """
    p = vs.IN
    share = p["magnet_wp_side"] * p["magnet_wp_side"] * 1e6 / p["magnet_reference_turns"]
    kA = p["magnet_turn_current"] / 1000.0
    f = {k: p["magnet_f_" + k] for k in ("copper", "solder", "steel", "helium")}
    return dict(cabling_factor=1.0, cable_void=0.0, cu_space=f["copper"] * share, steel_area=f["steel"] * share,
                misc_area=f["helium"] * share, solder_area=f["solder"] * share, ins_fraction=0.0, J_cu_rule=0.0,
                cu_void=0.0, cu_per_kA_rule=f["copper"] * share / kA, steel_per_kA_rule=f["steel"] * share / kA,
                B_steel_ref=24.9, steel_B_scaling=1.0)


def bridge_inputs(**extra):
    """Design 2.10 REBCO default: the Stellaris design, construction C at 50 kA, n = 1.5 n_ref (4 mm)."""
    n_ref = vs.compute()["conductor_parallel_tapes_reference"]
    inputs = {"magnet__" + k: v for k, v in _construction_C().items()}
    inputs.update({"magnet__n_elements": 1.5 * n_ref, "magnet__element_price_per_m": 80.0})
    inputs.update(extra)
    return inputs


@pytest.fixture(scope="module")
def bridge_case():
    return g.evaluate_material_case(bridge_inputs(), "rebco")


@pytest.fixture(scope="module")
def bridge_carnot_case():
    """The bridge with the plant's own 0.20-of-Carnot cold stage (design test 4(b))."""
    return g.evaluate_material_case(bridge_inputs(**{"cryoplant__eta_mode": 1.0, "cryoplant__eta_const": 0.20}),
                                    "rebco")


def nb3sn_inputs():
    """A synthetic Nb3Sn case on the HELIAS-class ratio at about 12 T (contract sections 3.2, 5).

    194 turns at 50 kA with peak_ratio 2.12 and f_ren 1.8; strand count is the smallest meeting
    Round 1's temperature-margin rule at the anchored field; construction P at its rule values.
    It is a test point for the oracle, not a policy design.
    """
    turns, current = 194.0, 50000.0
    B = 2.12 * 9.0 * turns / 308.0
    facts = dict(g.NB3SN_FACTS)

    def conductor(n):
        return r1.nb3sn_cable_critical_surface(dict(facts, n_elements=n, turn_current=current, B_peak=B,
                                                    T_supply=4.5, eps_intrinsic=-0.003))
    n = 350
    while conductor(n)["acceptance_margin"] < 0:
        n += 1
    element = conductor(n)
    construction = dict(cabling_factor=0.97, cable_void=0.2, ins_fraction=0.237, J_cu_rule=93.4, cu_void=0.1,
                        cu_per_kA_rule=0.0, steel_per_kA_rule=12.66, B_steel_ref=12.04, steel_B_scaling=1.0,
                        cu_space=max(0.0, current / 93.4 - element["element_copper_area"]) / 0.9,
                        steel_area=12.66 * current / 1000.0 * B / 12.04, misc_area=1.1077 * current / 1000.0,
                        solder_area=0.0)
    inputs = {"magnet__" + k: v for k, v in construction.items()}
    inputs.update({"magnet__n_elements": float(n), "magnet__element_price_per_m": 8.0, g.EPS_KEY: -0.003,
                   "magnet__coil__reference_turns": turns, "magnet__coil__peak_ratio": 2.12,
                   "plasma__f_ren": 1.8})
    return inputs


@pytest.fixture(scope="module")
def nb3sn_case():
    return g.evaluate_material_case(nb3sn_inputs(), "nb3sn")


@pytest.fixture(scope="module")
def synthetic_rebco_case():
    """A synthetic REBCO case away from every reference value that matters for the breakdown."""
    inputs = bridge_inputs(**{"magnet__n_elements": 190.0, "magnet__element_price_per_m": 30.0,
                              g.ARM_SLOPE_KEY: 0.0641, "magnet__winding_pack__wp_side": 0.38,
                              "magnet__coil__coil_t": 0.32, "cryoplant__rated_cold_W": 30000.0})
    return g.evaluate_material_case(inputs, "rebco")


# ---------------------------------------------------------------------------------------------
# 1. The plant oracle reproduces the pinned reference at the manifest point
# ---------------------------------------------------------------------------------------------
def test_plant_oracle_reproduces_pinned_reference_lcoe_at_manifest_point(pin_outputs):
    manifest = json.loads(g.MANIFEST_PATH.read_text())
    point = dict(manifest["baseline"]["point"])
    channels = g.evaluate_reference_case(point)
    lcoe = channels[P + "lcoe_calc__lcoe"]
    assert _rel(lcoe, pin_outputs[P + "lcoe_calc__lcoe"]) <= 1e-12
    assert _rel(lcoe, manifest["baseline"]["headline"]["value"]) <= 1e-12
    # every one of the pin's recorded outputs, at the harness tolerance (absolute floor for the two
    # zero-valued residual channels)
    assert set(pin_outputs) <= set(channels)
    bad = {k: (channels[k], v) for k, v in pin_outputs.items()
           if not (abs(channels[k] - v) <= 1e-9 * abs(v) or abs(channels[k] - v) <= 1e-12)}
    assert bad == {}
    assert channels[P + g.REFERENCE_NEW_OUTPUT] == 1.0  # declared delta, review R4
    # the three declared new entry keys at their neutral values change nothing
    neutral = dict(point, **{P + k: v for k, v in g.NEW_REFERENCE_KEYS.items()})
    assert g.evaluate_reference_case(neutral) == channels


def test_reference_case_refuses_non_neutral_new_keys():
    with pytest.raises(g.GlueOracleError):
        g.evaluate_reference_case({P + "magnet__rebco_law_enabled": 0.0})
    with pytest.raises(g.GlueOracleError):
        g.evaluate_reference_case({P + "magnet__coil__arm_slope": 0.0641})


# ---------------------------------------------------------------------------------------------
# 2. The re-derived plant chain is the plant oracle, bit for bit, at the reference legs
# ---------------------------------------------------------------------------------------------
def test_reference_chain_is_bit_identical(plant_reference):
    mine, glue = g._plant_chain(dict(vs.IN), None)
    assert glue is None
    mine = {k: v for k, v in mine.items() if not k.startswith("_")}
    assert set(mine) == set(plant_reference)
    assert {k: (mine[k], v) for k, v in plant_reference.items() if not _same(mine[k], v)} == {}


def test_composed_material_equals_plant_oracle_where_the_plant_oracle_can_run(bridge_case):
    """At 20 K and 24.9 T the plant oracle can run the material instance's plant inputs.

    Every plant-owned channel of the composed material instance must equal it bit for bit
    (inventory disabled on both sides, as 'Staged Cryoplant' makes it final).
    """
    p = g._plant_parameters(bridge_case["inputs"], "rebco")
    plant = oe._compute(p)
    owned = [s for s in bridge_case["channels"] if g.channel_owner(s) == "plant"]
    assert len(owned) > 1200
    suffix_to_name = {s: n for n, s in g.ORACLE_TO_SUFFIX.items()}
    diff = {s: (bridge_case["channels"][s], float(plant[suffix_to_name[s]])) for s in owned
            if not _same(bridge_case["channels"][s], float(plant[suffix_to_name[s]]))}
    assert diff == {}


def test_plant_oracle_refuses_material_points_the_composition_evaluates(nb3sn_case):
    """Premise of the composition: verify_stellaris.compute cannot run a 4.5 K instance."""
    p = g._plant_parameters(nb3sn_case["inputs"], "nb3sn")
    with pytest.raises(ValueError, match="unsupported temperature"):
        oe._compute(p)
    c = nb3sn_case["channels"]
    for suffix in g.SECTION_5_2_CHANNELS:
        assert math.isfinite(c[suffix]), suffix
    assert c["magnet__conductor__status_code"] == 1.0 and c["magnet__conductor__tcs_defined"] == 1.0
    assert c["magnet__conductor__acceptance_margin"] >= 0.0
    assert len(nb3sn_case["verdicts"]) == 73


# ---------------------------------------------------------------------------------------------
# 3. Neutral defaults reproduce the plant: B_peak, p_cryo and magnet capital (basis bridge)
# ---------------------------------------------------------------------------------------------
def test_basis_bridge_identity_at_neutral_defaults(plant_reference, bridge_carnot_case):
    ref = plant_reference
    c = bridge_carnot_case["channels"]
    # B_peak: the arm slot at slope 0 (with arm_x_ref 35.278 bound) is the plant's field exactly
    assert c["magnet__peak_field_calc__B_peak"] == ref["B_peak"]
    assert c["magnet__wp_stress__sigma_wp"] == ref["sigma_wp"]
    assert c["magnet__cond_strain__eps_cond"] == ref["eps_cond"]
    # p_cryo: the staged chain at the plant's 0.20 of Carnot reaches the plant's refrigeration power
    assert _rel(bridge_carnot_case["seam_operands"]["pb_p_cryo"], ref["p_cryo"]) <= 1e-12
    assert _rel(c["cryoplant__staged_drive__p_drive"], ref["thermal_p_drive"]) <= 1e-12
    assert _rel(c["power_supplies__tf_power__total"], ref["p_tf_total"]) <= 1e-12
    # magnet capital at the composition-implied count, on the plant's own quantity and price basis:
    # 6 mm tape, n = parallel_tapes_set, 20 $/m, per-turn areas = plant fractions x vol basis.
    p = vs.IN
    turns, wp = p["magnet_reference_turns"], p["magnet_wp_side"]
    vol_basis = wp * wp * 1e6 * p["magnet_f_wp_vol"] / (turns * p["magnet_f_set"])
    identity = bridge_inputs(**{
        "magnet__tape_width": p["magnet_tape_width"], "magnet__tape_thickness": p["magnet_tape_thickness"],
        "magnet__n_elements": ref["conductor_parallel_tapes_set"],
        "magnet__element_price_per_m": p["magnet_tape_price_per_m"],
        "magnet__cu_space": p["magnet_f_copper"] * vol_basis, "magnet__cu_void": 0.0,
        "magnet__steel_area": p["magnet_f_steel"] * vol_basis, "magnet__solder_area": p["magnet_f_solder"] * vol_basis,
        "cryoplant__eta_mode": 1.0, "cryoplant__eta_const": 0.20})
    case = g.evaluate_material_case(identity, "rebco")
    ci = case["channels"]
    assert _rel(ci["magnet__inventory__sc_cost"], ref["tape_procurement_cost"]) <= 1e-12
    assert _rel(ci["magnet__winding_sum__cost"], ref["winding_pack"]) <= 1e-12
    assert _rel(ci["magnet__magnet_capital_rollup__capital_cost"], ref["magnet_capital_rollup"]) <= 1e-12
    assert _rel(ci["powercore_capital__powercore_capital"], ref["powercore_capital"]) <= 1e-12


def test_design_bridge_count_carries_the_declared_quantity_basis_gap(plant_reference, bridge_case):
    """D12: the bridge's 4 mm metres at n = 1.5 n_ref are f_set/f_wp_vol of the plant's tape metres."""
    ref, c, p = plant_reference, bridge_case["channels"], vs.IN
    six_mm_equivalent = c["magnet__inventory__element_length"] * (0.004 / p["magnet_tape_width"])
    ratio = six_mm_equivalent / ref["tape_length"]
    assert _rel(ratio, p["magnet_f_set"] / p["magnet_f_wp_vol"]) <= 1e-12
    assert 0.990 < ratio < 0.992


def test_staged_cryo_reproduces_the_pin_at_20K(pin_outputs, bridge_case, bridge_carnot_case):
    c = bridge_case["channels"]
    assert round(c["cryoplant__static_loads__q_radiation"], 2) == 266.68
    assert round(c["cryoplant__static_loads__conduction_ref"], 2) == 590.28
    assert round(c["cryoplant__static_loads__shield_static"], 2) == 7561.69
    assert round(c["cryoplant__staged_drive__p_drive"], 7) == 0.0502673
    # design test 4(b) channel map, at 1e-9 relative
    cc = bridge_carnot_case["channels"]
    pairs = {
        "cryoplant__refrigeration__p_in_cold": "cryoplant__cryo_elec__p_elec",
        "cryoplant__refrigeration__p_in_shield": "cryoplant__shield_elec__p_elec",
        "cryoplant__refrigeration__p_in_total_MW": "cryoplant__refrigeration_sum__total",
        "cryoplant__cold_stage__q_cold": "cryoplant__cold_load_W_demand_conversion__demand",
        "cryoplant__cold_stage__q_shield": "cryoplant__inventory__q_inventory_shield",
        "cryoplant__staged_drive__p_drive": "cryoplant__inventory__p_drive",
    }
    scale = {"cryoplant__refrigeration__p_in_cold": 1e-6, "cryoplant__refrigeration__p_in_shield": 1e-6}
    for mine, pinned in pairs.items():
        assert _rel(cc[mine] * scale.get(mine, 1.0), pin_outputs[P + pinned]) <= 1e-9, mine
    # the seamed screens read the staged demands; the dormant plant chain stays in the outputs
    assert cc["cryoplant__cold_stage_capability__margin"] == (
        vs.IN["capability_cryoplant__rated_cold_W"] - cc["cryoplant__cold_stage__q_cold"])
    assert cc["cryoplant__intercept_stage_capability__evaluation_defined"] == 1.0
    assert cc["cryoplant__inventory__q_inventory_shield"] == 0.0
    # with the Green efficiency only the cold-stage electricity and its dependents move (test 4(c))
    assert c["cryoplant__refrigeration__p_in_shield"] == cc["cryoplant__refrigeration__p_in_shield"]
    assert c["cryoplant__refrigeration__p_in_cold"] != cc["cryoplant__refrigeration__p_in_cold"]
    assert c["cryoplant__aux_cooling__cryo_cost"] == c["cryoplant__refrigeration__refrigerator_capital"]


# ---------------------------------------------------------------------------------------------
# 4. The arm at slope 0 is identity; the arm's sign
# ---------------------------------------------------------------------------------------------
def test_arm_at_slope_zero_is_identity():
    rng = random.Random(20260930)
    for _ in range(300):
        R = rng.uniform(8.0, 25.0)
        a_coil = rng.uniform(1.5, 0.6 * R)
        x = dict(B_axis_in=rng.uniform(2.0, 12.0), peak_ratio_in=rng.uniform(1.8, 3.0), R_in=R, a_coil_in=a_coil,
                 R_ref_in=12.7, a_coil_ref_in=3.1500000000000004, wp_side_in=rng.uniform(0.15, 0.9),
                 arm_slope_in=0.0)
        bore_norm = (R / (R - a_coil)) / (12.7 / (12.7 - 3.1500000000000004))
        expected = x["B_axis_in"] * x["peak_ratio_in"] * bore_norm  # verify_stellaris.py:1077 order
        for x_ref in (0.0, 35.278, 1e3):
            assert g.conductor_peak_field(dict(x, arm_x_ref_in=x_ref))["B_peak"] == expected


def test_arm_value_and_sign_at_the_reference_pack():
    base = dict(B_axis_in=9.0, peak_ratio_in=2.7666666666666666, R_in=12.7, a_coil_in=3.1500000000000004,
                R_ref_in=12.7, a_coil_ref_in=3.1500000000000004, arm_slope_in=0.0641, arm_x_ref_in=35.278)
    at_ref = g.conductor_peak_field(dict(base, wp_side_in=0.35999999999999993))["B_peak"]
    assert _rel(at_ref, 9.0 * (2.7666666666666666 + 0.0641 * (12.7 / 0.35999999999999993 - 35.278))) <= 1e-15
    assert round(at_ref, 5) == 24.89987
    bigger_pack = g.conductor_peak_field(dict(base, wp_side_in=12.7 / 30.0))["B_peak"]
    assert bigger_pack < at_ref
    for bad in (dict(wp_side_in=0.0), dict(wp_side_in=0.36, arm_slope_in=math.nan),
                dict(wp_side_in=0.2, arm_slope_in=-10.0)):
        with pytest.raises(ValueError):
            g.conductor_peak_field(dict(base, **bad))


# ---------------------------------------------------------------------------------------------
# 5. The Ampere floor at Stellaris coil 0; the pack area at the Stellaris pack (construction C)
# ---------------------------------------------------------------------------------------------
def test_ampere_floor_at_stellaris_coil_0(bridge_case):
    out = g.pack_field_checks(dict(B_peak_in=24.6, I_coil_in=15.4e6, R_in=12.7, wp_side_in=0.36, mu0_in=g.MU0))
    assert round(out["ampere_floor"], 2) == 13.44
    assert g.ampere_floor_ok(out["ampere_floor_margin"]) is True
    assert round(out["R_over_sqrt_A_wp"], 3) == 35.278
    c = bridge_case["channels"]
    assert round(c["magnet__pack_field__ampere_floor"], 2) == 13.44
    assert bridge_case["verdicts"]["magnet__ampere_floor_ok"] == "satisfied"
    # a pack too small for its current puts the modeled peak below the floor: failed
    tiny = g.pack_field_checks(dict(B_peak_in=24.6, I_coil_in=15.4e6, R_in=12.7, wp_side_in=0.19, mu0_in=g.MU0))
    assert g.ampere_floor_ok(tiny["ampere_floor_margin"]) is False
    assert g.ampere_floor_ok(math.nan) is None


def test_pack_area_ok_at_the_stellaris_pack_under_construction_C(bridge_case):
    c, p = bridge_case["channels"], vs.IN
    share = p["magnet_wp_side"] * p["magnet_wp_side"] * 1e6 / p["magnet_reference_turns"]
    assert _rel(c["magnet__area__gross_area"], 420.779220779) <= 1e-6
    assert _rel(c["magnet__area__gross_area"], 0.1296e6 / 308.0) <= 1e-12
    # boundary by calibration (K15): the margin sits at zero to rounding; the bridge reports the margin
    assert abs(c["magnet__area__fit_margin"]) <= 1e-9 * share
    # design test 9: the margin is the contract section 5 inequality divided by turns
    identity = (p["magnet_wp_side"] ** 2 * 1e6 - p["magnet_reference_turns"] * c["magnet__area__gross_area"]) \
        / p["magnet_reference_turns"]
    assert abs(c["magnet__area__fit_margin"] - identity) <= 1e-12 * share
    assert c["magnet__adapter__pack_area_per_turn"] == c["magnet__area__gross_area"] + c["magnet__area__fit_margin"]


# ---------------------------------------------------------------------------------------------
# 6. The LCOE breakdown of design section 5.2 closes to LCOE (D2)
# ---------------------------------------------------------------------------------------------
@pytest.mark.parametrize("which", ["synthetic_rebco", "nb3sn", "bridge"])
def test_lcoe_breakdown_closes(which, synthetic_rebco_case, nb3sn_case, bridge_case):
    case = {"synthetic_rebco": synthetic_rebco_case, "nb3sn": nb3sn_case, "bridge": bridge_case}[which]
    c, inputs = case["channels"], case["inputs"]
    breakdown = g.lcoe_breakdown(c, inputs)
    assert abs(breakdown["relative_residual"]) <= 1e-9
    assert _rel(breakdown["capital_total"], c["total_capital__total_capital"]) <= 1e-9
    residuals = g.closure_residuals(c, inputs)
    assert {k: v for k, v in residuals.items() if abs(v) > 1e-9} == {}
    # each capital account enters once
    refs = [r for refs in g.CAPITAL_GROUPS.values() for r in refs]
    assert len(refs) == len(set(refs))
    assert not set(refs) & set(g.REPORTED_ONLY)


def test_lcoe_breakdown_closes_on_the_reference(pin_outputs):
    channels = {k[len(P):]: v for k, v in pin_outputs.items()}
    inputs = g.PIN_SUFFIX_INPUTS
    assert abs(g.lcoe_breakdown(channels, inputs, reference=True)["relative_residual"]) <= 1e-9
    residuals = g.closure_residuals(channels, inputs, reference=True)
    assert {k: v for k, v in residuals.items() if abs(v) > 1e-9} == {}


def test_synthetic_case_moves_what_the_seams_move(synthetic_rebco_case, bridge_case):
    s, b = synthetic_rebco_case["channels"], bridge_case["channels"]
    # the arm moved the field and every reader of it; the rollup reads the one-basis winding account
    assert s["magnet__peak_field_calc__B_peak"] != b["magnet__peak_field_calc__B_peak"]
    assert synthetic_rebco_case["seam_operands"]["rollup_winding_cost"] == s["magnet__winding_sum__cost"]
    assert s["magnet__magnet_capital_rollup__capital_cost"] == (
        s["magnet__winding_sum__cost"] + s["magnet__magnet_structure_cost__cost"]
        + s["magnet__insulation_inventory__stock_cost"])
    assert s["magnet__winding_procurement__cost"] != s["magnet__winding_sum__cost"]  # dormant plant account


# ---------------------------------------------------------------------------------------------
# 7. Gate, shape branch, status-only behaviour, structure-mass rule, refusals, the reuse map
# ---------------------------------------------------------------------------------------------
def test_gated_plant_rebco_law(plant_reference, bridge_case):
    p = dict(vs.IN)
    args = (p, plant_reference["B_peak"], plant_reference["tape_length"], plant_reference["conductor_length"])
    off = g.gated_rebco_conductor_current(*args, enabled=0.0)
    assert set(off) == set(g.CONDUCTOR_CURRENT_OUTPUTS) | {"evaluation_defined"}
    assert all(v == 0.0 for v in off.values())
    on = g.gated_rebco_conductor_current(*args, enabled=1.0)
    assert on.pop("evaluation_defined") == 1.0
    assert on == {k: plant_reference["conductor_" + k] for k in g.CONDUCTOR_CURRENT_OUTPUTS}
    for bad in (0.5, math.nan, True):
        with pytest.raises(ValueError):
            g.gated_rebco_conductor_current(*args, enabled=bad)
    c = bridge_case["channels"]
    assert all(c["magnet__conductor_current__" + k] == 0.0 for k in (*g.CONDUCTOR_CURRENT_OUTPUTS, "evaluation_defined"))


def test_rebco_shape_branch_is_continuous_at_20T_and_status_ends_at_25T():
    facts = dict(g.REBCO_FACTS, n_elements=169.0, turn_current=50000.0, T_supply=20.0)

    def law(B):
        mode = g.rebco_shape_branch(dict(B_peak_in=B, B_knot_max_in=facts["B_knot_max"]))["shape_mode"]
        return r1.rebco_cable_critical_surface(dict(facts, B_peak=B, shape_mode=mode))
    assert _rel(law(20.01)["ic_cable_op"], law(20.0)["ic_cable_op"]) < 1e-3
    assert law(25.0)["status_code"] == 1 and law(25.01)["status_code"] == 0


def test_rebco_above_25T_is_unsupported_by_status_not_refusal():
    case = g.evaluate_material_case(bridge_inputs(**{"magnet__coil__reference_turns": 322.0}), "rebco")
    c = case["channels"]
    assert c["magnet__peak_field_calc__B_peak"] > 25.0
    assert c["magnet__conductor__status_code"] == 0.0 and c["magnet__conductor__supported"] == 0.0
    assert case["verdicts"]["magnet__acceptance_ok"] == "violated"
    assert all(math.isfinite(c[s]) for s in g.SECTION_5_2_CHANNELS)


def test_structure_mass_rule_as_recorded_design_check(bridge_case):
    W = bridge_case["channels"]["magnet__stored_energy__W_mag"]
    assert W == 111e9
    assert g.structure_mass_rule(W) == 11_615_600.0
    assert g.structure_mass_rule(W, 2.0) == 2 * 11_615_600.0
    check = bridge_case["checks"]["structure_mass"]
    # the pinned supplied mass is the unrounded 11,615.604 t: 3.9e-7 from the printed 11,615.6 t
    assert check["consistent"] is False and 3.8e-7 < check["relative_residual"] < 3.9e-7
    assert g.structure_mass_check(vs.IN["magnet_support_mass"], W, rel_tol=1e-6)["consistent"] is True


def test_input_refusals():
    base = bridge_inputs()
    other = g.MATERIAL_PREFIXES["nb3sn"]
    cases = [
        dict(base, **{other + "plasma__R": 12.7}),               # one material per case
        dict(base, **{P + "plasma__R": 12.7}),                   # the reference is pinned
        dict(base, **{"cryoplant__purchase_cost_per_module": 1.0}),  # Removed class (K11, R5)
        dict(base, **{"cryoplant__inventory_enabled": True}),
        dict(base, **{"magnet__rebco_law_enabled": 1.0}),
        dict(base, **{"magnet__not_a_key": 1.0}),               # unknown key
        dict(base, **{"cryoplant__T_amb_cryo": 290.0}),          # held by the plant oracle
        dict(base, **{"cryoplant__k_d": -0.6}),                  # NIST fit is Round 1's constant
        {k: v for k, v in base.items() if k != "magnet__n_elements"},  # supplied quantity missing
    ]
    for inputs in cases:
        with pytest.raises(g.GlueOracleError):
            g.resolve_material_inputs(inputs, "rebco")
    with pytest.raises(g.GlueOracleError):  # Nb3Sn needs eps_intrinsic (K6)
        g.resolve_material_inputs({k: v for k, v in nb3sn_inputs().items() if k != g.EPS_KEY}, "nb3sn")
    with pytest.raises(g.GlueOracleError):
        g.resolve_material_inputs(dict(base, **{g.EPS_KEY: -0.003}), "rebco")
    resolved, provenance = g.resolve_material_inputs(
        {g.MATERIAL_PREFIXES["rebco"] + k: v for k, v in base.items()}, "rebco")
    assert provenance["magnet__n_elements"] == "supplied" and provenance["plasma__R"] == "pin"
    assert resolved["cryoplant__k_c"] == 5.39362701769  # the plant's support conductance, not NIST k_c


def test_reuse_map_is_current_and_complete(bridge_case, nb3sn_case):
    committed = json.loads(g.REUSE_PATH.read_text())
    assert committed == json.loads(json.dumps(g.build_reuse_map()))
    material_channels = committed["material_channels"]
    for case in (bridge_case, nb3sn_case):
        emitted = set(case["channels"])
        mapped = {s for s, e in material_channels.items() if case["material"] in e["materials"]}
        assert emitted == mapped
        assert set(case["verdicts"]) == set(committed["material_verdicts"])
    assert len(committed["material_verdicts"]) == 73
    assert all(e["owner"] in ("plant", "round1", "glue", "composed") for e in material_channels.values())
    assert all(len(e["produced_by"]) == 1 for e in material_channels.values())
    assert set(committed["section_5_2"]["channels"]) <= set(material_channels)
    owners = committed["section_5_2"]["channels"]
    assert owners["magnet__peak_field_calc__B_peak"] == "glue"            # D3
    assert owners["magnet__conductor__acceptance_margin"] == "round1"
    assert owners["lcoe_calc__lcoe"] == "composed"
    assert owners["plasma__fusion__p_fus"] == "plant"
    verdicts = committed["section_5_2"]["verdicts"]
    assert verdicts["wp_stress_ok"] == verdicts["cond_strain_ok"] == "glue"  # R4
    assert committed["prefixes"]["reference"]["exceptions"][g.REFERENCE_NEW_OUTPUT]["owner"] == "glue"  # R4
