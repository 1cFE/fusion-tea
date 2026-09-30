"""Pure-oracle tests for WI-099 (independent oracle and offer policy; not the generated package).

Source points and tolerances are those of the released contract section 5
(work/orchestration/goals/magnet-material-comparison/evidence/comparison-contract.md r3), with the
checked values taken from evidence/check-nb3sn.md and evidence/check-rebco-cryo-cost.md.
Run: .codex-test/run python -m pytest tests/models/test_magnet_oracle.py -q
"""
from __future__ import annotations

import copy
import importlib.util
import json
import math
import statistics
import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[2]
MM = REPO / "exploration/magnet_materials"


def _load(name: str, path: Path):
    if name in sys.modules:
        return sys.modules[name]
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


oracle = _load("magnet_materials_independent_oracle", MM / "oracle.py")
op = _load("magnet_materials_offer_policy", MM / "studies/offer_policy.py")
dc = _load("magnet_materials_declare_cases", MM / "studies/declare_cases.py")

SECTION6 = {
    "duty": ["coils", "turns", "turn_length", "available_area", "I_ref", "B_ref", "B_peak"],
    "economics": ["crf", "availability", "electricity_price", "hours", "usd2015_to_2021"],
    "common": ["n_elements", "T_supply", "nuclear_rise", "margin_rise", "fraction_rule", "acceptance_rule",
               "cabling_factor", "cable_void", "cu_space", "steel_area", "misc_area", "solder_area",
               "ins_fraction", "J_cu_rule", "cu_void", "cu_per_kA_rule", "steel_per_kA_rule", "B_steel_ref",
               "steel_B_scaling", "element_density", "rho_cu", "rho_steel", "rho_solder", "price_cu",
               "price_steel", "price_solder", "element_price_per_m", "manufacturing_per_m", "nuclear_density",
               "cold_volume", "radiation_ref", "conduction_ref", "T_conduction_ref", "n_leads", "f_lead", "L0",
               "p_joint_ref", "I_joint_ref", "shield_static", "load_multiplier", "rating_cold", "eta_mode",
               "eta_const", "green_a", "green_b", "f_carnot_shield", "capital_mode", "green_c", "green_d",
               "T_green"],
    "nb3sn": ["strand_diameter", "strand_copper_fraction", "p", "q", "C1", "Ca1", "Ca2", "eps0a", "Bc20", "Tc0",
              "eps_intrinsic"],
    "rebco": ["tape_width", "tape_thickness", "tape_copper_fraction", "anchor_ic", "shape_mode", "g8", "g10",
              "g12", "g15", "g20", "alpha", "T_star", "degradation"],
}

BEAS_II = op.TSUI_BEAS_II
WST = op.STRANDS["WST TFCN5-6"]


def ic(B, T, eps, P):
    return oracle.nb3sn_ic_strand(B, T, eps, P)


def ref_case(anchor="D", B=10.0, pairing="common-P", family="reference", variant="none"):
    asm = op.assumptions(anchor, B, pairing, family, variant)
    prop = op.propose_offer(asm)
    return op.assemble_case(asm, {m: prop[m]["offer"] for m in prop}), prop


# ---------------------------------------------------------------------------------------------
# Source data: Nb3Sn law (contract section 5; check-nb3sn.md sections 3 and Recheck r2/r3)
# ---------------------------------------------------------------------------------------------
def test_beas_ii_iter_spec_point():
    v = ic(12.0, 4.22, 0.0, BEAS_II)
    assert v == pytest.approx(201.30, abs=0.01)  # check-nb3sn.md section 3 table
    assert v > 190.0  # ITER TF specification (Tsui Table 1)
    assert abs(v - 197.0) <= 5.0  # Tsui Fig. 9(a) peak reading, plot tolerance


@pytest.mark.parametrize("B,T,eps,expected", [
    (12.0, 4.2, 0.0, 201.85), (12.0, 5.2, -0.003, 152.95), (12.0, 6.7, -0.003, 106.83),
    (8.0, 6.7, -0.003, 238.93), (12.0, 6.7, -0.006, 73.11), (8.0, 5.2, -0.003, 305.43),
    (9.0, 6.7, -0.003, 197.54), (9.0, 5.2, -0.003, 258.10), (10.0, 6.7, -0.003, 162.50),
    (10.0, 5.2, -0.003, 217.79), (11.0, 6.7, -0.003, 132.56), (11.0, 5.2, -0.003, 183.08),
])
def test_beas_ii_check_a_points(B, T, eps, expected):
    assert ic(B, T, eps, BEAS_II) == pytest.approx(expected, abs=0.01)


def test_ost_check_a_points():
    assert ic(12.0, 6.7, -0.003, op.TSUI_OST) == pytest.approx(138.94, abs=0.01)  # Tsui C, check A r2 item 6
    assert ic(12.0, 6.7, -0.003, op.STRANDS["OST TFEU9"]) == pytest.approx(138.92, abs=0.01)  # r3 item 7


BRESCHI_RECHECK = {  # check-nb3sn.md Recheck r3 item 7, (12 T, 6.7 K, -0.3 %)
    "BEAS TFEU10-12": 111.98, "OST TFUS5R-7R": 121.25, "Luvata TFUS7L-8": 121.41, "Jastec TFJA7-8": 125.83,
    "ChMP TFRF4-7": 126.99, "WST TFCN5-6": 127.31, "Hitachi TFJA6L-9-10": 129.11, "OST TFEU11-13": 136.87,
    "Kiswire TFKO4-8": 138.28, "OST TFEU9": 138.92,
}


@pytest.mark.parametrize("name,expected", sorted(BRESCHI_RECHECK.items()))
def test_breschi_production_sets(name, expected):
    assert ic(12.0, 6.7, -0.003, op.BRESCHI_TABLE_III[name]) == pytest.approx(expected, abs=0.01)


def test_breschi_median_and_reference_strand():
    vals = [ic(12.0, 6.7, -0.003, P) for P in op.BRESCHI_TABLE_III.values()]
    assert len(vals) == 10
    assert statistics.median(vals) == pytest.approx(127.15, abs=0.01)
    ranked = sorted(op.BRESCHI_TABLE_III, key=lambda k: ic(12.0, 6.7, -0.003, op.BRESCHI_TABLE_III[k]))
    assert ranked[5] == op.REFERENCE_STRAND  # upper of the two middle sets
    # WST at 6 T, 4.2 K, eps_I = 0 (price conversion only; check A r3 item 9)
    assert ic(6.0, 4.2, 0.0, WST) == pytest.approx(680.48, abs=0.01)


def test_breschi_spread_at_minus_0_6_percent():
    vals = {k: ic(12.0, 6.7, -0.006, P) for k, P in op.BRESCHI_TABLE_III.items()}
    assert vals["WST TFCN5-6"] == pytest.approx(61.2, abs=0.05)  # check A r3 advisory
    assert statistics.median(vals.values()) == pytest.approx(73.1, abs=0.05)
    assert min(vals.values()) == pytest.approx(58.0, abs=0.05)
    assert max(vals.values()) == pytest.approx(81.4, abs=0.05)
    assert sorted(vals.values(), reverse=True).index(vals["WST TFCN5-6"]) == 7  # 3rd lowest of 10


def test_strain_function_peak_and_units():
    for P in list(op.BRESCHI_TABLE_III.values()) + [BEAS_II, op.TSUI_OST]:
        s = lambda e: oracle.nb3sn_strain_function(e, P["Ca1"], P["Ca2"], P["eps0a"])
        assert s(0.0) == pytest.approx(1.0, abs=1e-12)
        assert s(-0.003) < 1.0 and s(0.001) < 1.0


# ---------------------------------------------------------------------------------------------
# Source data: REBCO shape (contract section 3; check-rebco-cryo-cost.md section 1)
# ---------------------------------------------------------------------------------------------
def test_rebco_shape_within_both_digitizations():
    x = dict(op.REBCO_REF)
    author = {10.0: 1.85, 12.0: 1.61, 15.0: 1.33}
    check_b_geneva = {10.0: 1.85, 12.0: 1.62, 15.0: 1.34}
    for B in (10.0, 12.0, 15.0):
        g = oracle.rebco_shape(B, x)
        assert abs(g - author[B]) <= 0.02 and abs(g - check_b_geneva[B]) <= 0.02
    assert oracle.rebco_shape(20.0, x) == 1.0
    assert oracle.rebco_shape(8.0, x) == 2.11
    grid = [8.0 + 0.25 * i for i in range(49)]
    gs = [oracle.rebco_shape(B, x) for B in grid]
    assert all(a > b for a, b in zip(gs, gs[1:]))  # monotone decreasing
    # log-log linear between 12 and 15 T
    mid = math.sqrt(12.0 * 15.0)
    assert oracle.rebco_shape(mid, x) == pytest.approx(math.sqrt(1.61 * 1.33), rel=1e-12)
    xp = dict(x, shape_mode=1.0)
    assert oracle.rebco_shape(10.0, xp) == pytest.approx(2.0 ** 0.6, rel=1e-12)


def test_rebco_tcs_closed_form_consistent():
    x = dict(op.REBCO_REF, n_elements=300.0, turn_current=80000.0, B_peak=12.0, acceptance_rule=1.0)
    out = oracle.rebco_cable_critical_surface(x)
    ic_at_tcs = 300.0 * 0.9 * 198.0 * oracle.rebco_shape(12.0, x) * math.exp(-(out["T_cs"] - 20.0) / 22.0)
    assert ic_at_tcs == pytest.approx(80000.0, rel=1e-12)


# ---------------------------------------------------------------------------------------------
# Source data: constructions (contract section 4)
# ---------------------------------------------------------------------------------------------
def test_construction_p_reproduces_eu_demo_layer1():
    I, B = 104950.0, 12.04
    elem = 399 * math.pi / 4.0 * 1.0 ** 2  # 399 x 1 mm strands, Cu:non-Cu 1
    P = op.CONSTRUCTIONS["P"]
    x = dict(turn_current=I, B_peak=B, available_area=1296 * 411 / 142, element_area=elem,
             element_copper_area=elem / 2.0, cabling_factor=P["cabling_factor"], cable_void=P["cable_void"],
             cu_space=(I / 93.4 - elem / 2.0) / 0.9, steel_area=9.3635 * I / 1000.0,
             misc_area=P["misc_per_kA"] * I / 1000.0, solder_area=0.0, ins_fraction=P["ins_fraction"],
             J_cu_rule=93.4, cu_void=0.10, cu_per_kA_rule=0.0, steel_per_kA_rule=9.3635, B_steel_ref=12.04,
             steel_B_scaling=1.0)
    out = oracle.winding_turn_area_screen(x)
    assert out["net_area"] == pytest.approx(68.0 * 37.9, rel=1e-6)  # 2577.2 mm^2
    # N2: the same conductor with pack-average steel needs 3831.2 mm^2 gross (check A r3 item 4)
    x2 = dict(x, steel_area=12.66 * I / 1000.0)
    assert oracle.winding_turn_area_screen(x2)["gross_area"] == pytest.approx(3831.2, abs=0.1)


def test_construction_c_reproduces_stellaris_table7():
    A = 0.36 * 0.36 * 1e6 / 308.0
    I, B = 50000.0, 24.9
    C = op.CONSTRUCTIONS["C"]
    kA = I / 1000.0
    cu, solder, he = C["cu_per_kA_rule"] * kA, C["solder_per_kA"] * kA, C["misc_per_kA"] * kA
    steel = C["steel_per_kA_rule"] * kA * B / C["B_steel_ref"]
    for area, frac in ((cu, 0.35), (solder, 0.12), (he, 0.08), (steel, 0.36)):
        assert area == pytest.approx(frac * A, rel=1e-6)
    x = dict(turn_current=I, B_peak=B, available_area=A, element_area=0.09 * A, element_copper_area=0.0,
             cabling_factor=C["cabling_factor"], cable_void=C["cable_void"], cu_space=cu, steel_area=steel,
             misc_area=he, solder_area=solder, ins_fraction=C["ins_fraction"], J_cu_rule=0.0, cu_void=0.0,
             cu_per_kA_rule=C["cu_per_kA_rule"], steel_per_kA_rule=C["steel_per_kA_rule"], B_steel_ref=24.9,
             steel_B_scaling=1.0)
    out = oracle.winding_turn_area_screen(x)
    assert out["gross_area"] == pytest.approx(A, rel=1e-6)
    assert out["cu_margin"] == pytest.approx(0.0, abs=1e-9) and out["steel_margin"] == pytest.approx(0.0, abs=1e-9)
    # the contract prints the calibration to 4 significant figures
    assert (round(C["cu_per_kA_rule"], 3), round(C["solder_per_kA"], 3), round(C["misc_per_kA"], 3),
            round(C["steel_per_kA_rule"], 3)) == (2.945, 1.010, 0.673, 3.030)


# ---------------------------------------------------------------------------------------------
# Source data: cryogenics (contract sections 5-6; check-rebco-cryo-cost.md sections 4-5)
# ---------------------------------------------------------------------------------------------
def _refr(T_supply, rating=10000.0, **kw):
    x = dict(op.REFRIGERATION_REF, T_supply=T_supply, rating_cold=rating, q_cold=1000.0, q_shield=0.0,
             usd2015_to_2021=op.USD2015_TO_2021)
    x.update(kw)
    return oracle.staged_refrigeration_screen(x)


def test_carnot_specific_power():
    assert _refr(4.5)["carnot_specific_power"] == pytest.approx(65.67, abs=0.01)
    assert _refr(20.0)["carnot_specific_power"] == pytest.approx(14.00, abs=0.01)


def test_input_power_equivalence_factor():
    out = _refr(20.0, rating=1000.0)
    assert out["R_equiv_kW"] == pytest.approx(0.2132, abs=1e-4)  # contract section 6
    assert _refr(20.0, rating=1000.0, capital_mode=1.0)["R_equiv_kW"] == 1.0
    assert _refr(4.5, rating=1000.0)["R_equiv_kW"] == pytest.approx(1.0, rel=1e-15)


def test_ballarino_minimum_heat_leak():
    assert oracle.ballarino_w_per_kA(4.2) == pytest.approx(46.95, abs=0.01)
    assert oracle.ballarino_w_per_kA(20.0) == pytest.approx(46.85, abs=0.01)
    # intercepted cold segment used in the cold stage (contract section 6: ~12.0 and 11.6 W/kA)
    assert oracle.ballarino_w_per_kA(4.5, T_warm=77.0) == pytest.approx(12.03, abs=0.01)
    assert oracle.ballarino_w_per_kA(20.0, T_warm=77.0) == pytest.approx(11.64, abs=0.01)


def _simpson_T(a, b, n=20000):
    h = (b - a) / n
    s = oracle.k316(a) + oracle.k316(b)
    s += 4.0 * sum(oracle.k316(a + (2 * i - 1) * h) for i in range(1, n // 2 + 1))
    s += 2.0 * sum(oracle.k316(a + 2 * i * h) for i in range(1, n // 2))
    return s * h / 3.0


def test_316_conductivity_integral():
    K45, K20 = oracle.k316_integral(4.5), oracle.k316_integral(20.0)
    assert K45 == pytest.approx(326.0, rel=0.005)
    assert K20 == pytest.approx(307.4, rel=0.005)
    assert K20 / K45 == pytest.approx(0.943, abs=0.001)
    # own convergence and a second method (Simpson in T) agree far inside 1e-9
    assert oracle.k316_integral(4.5, panels=16) == pytest.approx(K45, rel=1e-13)
    assert oracle.k316_integral(4.5, panels=256) == pytest.approx(K45, rel=1e-13)
    assert _simpson_T(4.5, 77.0) == pytest.approx(K45, rel=1e-10)
    # spot values (check B section 5)
    assert oracle.k316(4.5) == pytest.approx(0.32, abs=0.005)
    assert oracle.k316(20.0) == pytest.approx(2.17, abs=0.005)
    assert oracle.k316(77.0) == pytest.approx(7.92, abs=0.005)


def test_green_efficiency_formula():
    out = _refr(4.5, rating=18000.0)
    assert out["eta_cold"] == pytest.approx(0.155 * 18.0 ** 0.23, rel=1e-9)
    # 15.5 x 18^0.23 % evaluates to 30.13 %; the contract prints 30.2 % (oracle-notes.md A10)
    assert out["eta_cold"] == pytest.approx(0.3013, abs=1e-4)
    assert _refr(4.5, rating=40000.0)["green_extrapolated"] == 1
    assert _refr(4.5, rating=30000.0)["green_extrapolated"] == 0


def test_anchor_s_inventory_reconstructs_rating():
    S = op.ANCHORS["S"]
    x = dict(S["cold"], T_supply=20.0, turn_current=50000.0)
    out = oracle.magnet_cold_stage_load(x)
    assert out["q_cold"] == pytest.approx(21930.0, rel=0.001)  # contract: 21.93 kW
    assert out["q_cold"] == pytest.approx(op.STELLARIS_RATED_COLD_W, rel=1e-12)
    assert out["q_nuclear"] == pytest.approx(4850.0, abs=5.0)
    assert out["q_leads"] == pytest.approx(8730.0, abs=5.0)
    assert out["q_radiation"] == pytest.approx(266.7, abs=0.1)
    assert out["q_conduction"] == pytest.approx(590.3, abs=0.1)
    assert out["q_shield"] == pytest.approx(op.STELLARIS_RATED_INTERCEPT_W, rel=1e-12)
    inv = op._stellaris_inventory()
    assert S["cold"]["shield_static"] == pytest.approx(inv["q_rad_s"] + inv["q_sup_s"], rel=1e-12)


def test_anchor_d_cold_inputs():
    D = op.ANCHORS["D"]["cold"]
    assert D["shield_static"] == pytest.approx(1102.0e3)  # Koncar Table 1: 912.6 + 189.4 kW shields only
    assert 5.9 + 912.6 + 189.4 == pytest.approx(1107.9)  # the table's all-component total
    assert D["cold_volume"] == pytest.approx(474.0, abs=0.5)
    assert D["p_joint_ref"] == pytest.approx(256e-9 * 104950.0 ** 2, rel=1e-15)


# ---------------------------------------------------------------------------------------------
# Tcs root (Brent) against an in-test bisection
# ---------------------------------------------------------------------------------------------
@pytest.mark.parametrize("strand,B,eps,n", [
    ("WST TFCN5-6", 10.0, -0.003, 438), ("WST TFCN5-6", 12.0, -0.006, 900), ("OST TFEU9", 8.0, -0.003, 250),
    ("BEAS TFEU10-12", 13.0, -0.003, 1200), ("Tsui BEAS II", 11.0, -0.003, 700), ("Kiswire TFKO4-8", 14.0, -0.003, 1500),
])
def test_tcs_root(strand, B, eps, n):
    P = op.STRANDS[strand]
    I = 104950.0 * B / 12.04
    x = dict(op.NB3SN_REF, **P)
    x.update(n_elements=float(n), turn_current=I, B_peak=B, eps_intrinsic=eps, acceptance_rule=0.0)
    out = oracle.nb3sn_cable_critical_surface(x)
    assert out["tcs_defined"] == 1
    lo, hi = 0.0, oracle.nb3sn_t_zero(B, eps, P)
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        if n * ic(B, mid, eps, P) >= I:
            lo = mid
        else:
            hi = mid
    assert out["T_cs"] == pytest.approx(0.5 * (lo + hi), abs=1e-9)
    assert n * ic(B, out["T_cs"], eps, P) == pytest.approx(I, rel=1e-9)


def test_tcs_undefined_when_cable_cannot_carry_current_at_zero_kelvin():
    x = dict(op.NB3SN_REF)
    x.update(n_elements=10.0, turn_current=174302.0, B_peak=20.0, eps_intrinsic=-0.006, acceptance_rule=0.0)
    out = oracle.nb3sn_cable_critical_surface(x)
    assert out["tcs_defined"] == 0 and out["T_cs"] == 0.0 and out["acceptance_pass"] == 0


# ---------------------------------------------------------------------------------------------
# MR-7 behaviour of the oracle (contract section 5)
# ---------------------------------------------------------------------------------------------
def test_insufficient_and_sufficient_pairs():
    case, prop = ref_case("D", 10.0)
    base = oracle.evaluate_case(case)
    for m in ("nb3sn", "rebco"):
        assert base[m]["all_pass"] == 1
        # current margin
        c2 = copy.deepcopy(case)
        c2[m]["n_elements"] -= 1.0
        assert oracle.evaluate_case(c2)[m]["conductor"]["acceptance_pass"] == 0
        # protection copper and structural steel
        for key, flag in (("cu_space", "cu_pass"), ("steel_area", "steel_pass")):
            c3 = copy.deepcopy(case)
            c3[m][key] -= 1e-3
            assert oracle.evaluate_case(c3)[m]["area"][flag] == 0
        # refrigerator capacity
        c4 = copy.deepcopy(case)
        c4[m]["rating_cold"] = prop[m]["trace"]["insufficient_rating"]
        assert oracle.evaluate_case(c4)[m]["refrigeration"]["capacity_pass"] == 0
    # fit: the anchor D offer does not fit anchor S's envelope; the anchor S REBCO/C offer does
    cS, _ = ref_case("S", 10.0, "native")
    outS = oracle.evaluate_case(cS)
    assert outS["rebco"]["area"]["fit_pass"] == 1 and outS["nb3sn"]["area"]["fit_pass"] == 0


def test_supplied_design_unchanged_by_evaluation():
    case, _ = ref_case("D", 12.0)
    before = copy.deepcopy(case)
    oracle.evaluate_case(case)
    assert case == before


def test_field_varied_with_hardware_fixed():
    case, _ = ref_case("D", 10.0)
    a = oracle.evaluate_case(case)
    c2 = copy.deepcopy(case)
    c2["duty"]["B_peak"] = 11.0
    b = oracle.evaluate_case(c2)
    for m in ("nb3sn", "rebco"):
        for k in ("element_length", "element_mass", "sc_cost", "cu_mass", "steel_mass", "materials_cost",
                  "winding_capital"):
            assert a[m]["inventory"][k] == b[m]["inventory"][k]
        assert a[m]["refrigeration"]["refrigerator_capital"] == b[m]["refrigeration"]["refrigerator_capital"]
        for k in ("acceptance_margin", "operating_fraction"):
            assert a[m]["conductor"][k] != b[m]["conductor"][k]
        for k in ("cu_required", "steel_required", "cu_margin", "steel_margin"):
            assert a[m]["area"][k] != b[m]["area"][k]
        assert a[m]["cold_load"]["q_cold"] != b[m]["cold_load"]["q_cold"]


def test_unsupported_case_per_conductor():
    case, _ = ref_case("D", 16.0)
    out = oracle.evaluate_case(case)
    assert out["nb3sn"]["conductor"]["status_code"] == 0
    assert out["nb3sn"]["conductor"]["acceptance_pass"] == 0
    assert out["pair"]["rankable"] == 0 and out["pair"]["pair_status"] == 0
    c2, _ = ref_case("D", 20.0)
    c2["duty"]["B_peak"] = 22.0  # outside the measured shape's knots
    out2 = oracle.evaluate_case(c2)
    assert out2["rebco"]["conductor"]["status_code"] == 0
    assert out2["rebco"]["conductor"]["acceptance_pass"] == 0 and out2["pair"]["rankable"] == 0
    c3 = copy.deepcopy(c2)
    c3["rebco"]["shape_mode"] = 1.0  # power law is supported to 24 T
    assert oracle.evaluate_case(c3)["rebco"]["conductor"]["status_code"] == 1


def test_nb3sn_status_bands():
    for B, code in ((8.0, 1), (12.2, 1), (12.21, 2), (13.5, 2), (13.51, 3), (14.5, 3), (14.51, 0), (7.99, 0)):
        x = dict(op.NB3SN_REF, n_elements=500.0, turn_current=50000.0, B_peak=B, acceptance_rule=0.0)
        assert oracle.nb3sn_cable_critical_surface(x)["status_code"] == code


def test_hardware_isolation_d5():
    case, _ = ref_case("D", 10.0)
    a = oracle.evaluate_case(case)
    c2 = copy.deepcopy(case)
    c2["nb3sn"]["n_elements"] += 25.0
    b = oracle.evaluate_case(c2)
    assert a["rebco"]["flat"] == b["rebco"]["flat"]
    assert a["nb3sn"]["cold_load"] == b["nb3sn"]["cold_load"]
    assert a["nb3sn"]["refrigeration"] == b["nb3sn"]["refrigeration"]
    for k in ("cu_mass", "steel_mass", "solder_mass", "materials_cost"):
        assert a["nb3sn"]["inventory"][k] == b["nb3sn"]["inventory"][k]
    assert b["nb3sn"]["inventory"]["sc_cost"] > a["nb3sn"]["inventory"]["sc_cost"]
    c3 = copy.deepcopy(case)
    c3["rebco"]["rating_cold"] = 50000.0
    d = oracle.evaluate_case(c3)
    for blk in ("conductor", "area", "inventory", "cold_load"):
        assert a["rebco"][blk] == d["rebco"][blk]
    changed = {k for k in a["rebco"]["refrigeration"] if a["rebco"]["refrigeration"][k] != d["rebco"]["refrigeration"][k]}
    assert changed == {"eta_cold", "p_in_cold", "p_in_total_MW", "R_equiv_kW", "refrigerator_capital",
                       "capacity_margin", "green_extrapolated"}


def test_breakeven_price_makes_costs_equal():
    case, _ = ref_case("D", 10.0)
    out = oracle.evaluate_case(case)
    assert out["pair"]["rankable"] == 1
    c2 = copy.deepcopy(case)
    c2["rebco"]["element_price_per_m"] = out["pair"]["breakeven_rebco_price_per_m"]
    assert oracle.evaluate_case(c2)["pair"]["cost_difference"] == pytest.approx(0.0, abs=1e-3)


# ---------------------------------------------------------------------------------------------
# Offer policy and the declared case set
# ---------------------------------------------------------------------------------------------
@pytest.fixture(scope="module")
def cases():
    return json.loads((MM / "studies/cases.json").read_text())["cases"]


def test_case_file_is_reproducible(cases):
    assert dc.declare() == cases


def test_every_case_carries_all_section6_inputs(cases):
    assert len(cases) < 3000
    assert len({c["case_id"] for c in cases}) == len(cases)
    for c in cases:
        for sec in ("duty", "economics"):
            assert set(c[sec]) == set(SECTION6[sec])
        for m in ("nb3sn", "rebco"):
            assert set(c[m]) == set(SECTION6["common"]) | set(SECTION6[m])
        assert set(c["labels"]) >= {"anchor", "B_peak", "pairing", "rule_family", "variant", "offer_kind",
                                    "refrigerator_kind"}


def _key(c):
    lb = c["labels"]
    return lb["anchor"], lb["B_peak"], lb["pairing"], lb["rule_family"]


def test_reference_offers_meet_policy(cases):
    ref = {}
    for c in cases:
        lb = c["labels"]
        if lb["variant"] == "none" and lb["offer_kind"] == "reference" and lb["refrigerator_kind"] == "reference":
            ref[_key(c)] = c
    assert len(ref) == 16 * 9
    for key, c in ref.items():
        out = oracle.evaluate_case(c)
        for m in ("nb3sn", "rebco"):
            f = out[m]["flat"]
            assert f["acceptance_margin"] >= 0.0  # support ignored so unsupported points still get an offer
            c2 = copy.deepcopy(c)
            c2[m]["n_elements"] -= 1.0
            assert oracle.evaluate_case(c2)[m]["conductor"]["acceptance_margin"] < 0.0  # smallest n
            assert 0.0 <= f["cu_margin"] <= 1e-6 and 0.0 <= f["steel_margin"] <= 1e-6  # D1
            q = f["q_cold"]
            r = c[m]["rating_cold"]
            assert r >= q and r in op.RATINGS_W
            i = op.RATINGS_W.index(r)
            assert i == 0 or op.RATINGS_W[i - 1] < q
    for c in cases:
        lb = c["labels"]
        if lb["variant"] != "none" and lb["offer_kind"] != "variant-offer":
            continue
        r = ref[(lb["anchor"], lb["B_peak"], lb["pairing"], lb["rule_family"])]
        for m in ("nb3sn", "rebco"):
            n0 = int(r[m]["n_elements"])
            same_areas = all(c[m][k] == r[m][k] for k in ("cu_space", "steel_area", "misc_area", "solder_area"))
            if lb["variant"] == "none" and lb["offer_kind"] == "insufficient":
                assert c[m]["n_elements"] == math.floor(0.9 * n0) and same_areas
            if lb["variant"] == "none" and lb["offer_kind"] == "generous":
                assert c[m]["n_elements"] == -(-12 * n0 // 10) and same_areas
            if lb["refrigerator_kind"] == "insufficient":
                i = op.RATINGS_W.index(r[m]["rating_cold"])
                assert c[m]["rating_cold"] == op.RATINGS_W[i - 1] and c[m]["n_elements"] == n0


def test_variant_reevaluations_keep_the_reference_offer(cases):
    ref = {_key(c): c for c in cases if c["labels"]["variant"] == "none"
           and c["labels"]["offer_kind"] == "reference" and c["labels"]["refrigerator_kind"] == "reference"}
    n = 0
    for c in cases:
        lb = c["labels"]
        if lb["variant"] == "none" or lb["offer_kind"] != "reference":
            continue
        r = ref[_key(c)]
        for m in ("nb3sn", "rebco"):
            for k in op.OFFER_KEYS:
                assert c[m][k] == r[m][k], (c["case_id"], m, k)
        n += 1
    assert n == (len(op.VARIANTS) - 2) * 16 * 2 + 2 * 10 * 2


def test_variant_offers_meet_policy_under_the_variant(cases):
    for c in cases:
        if c["labels"]["offer_kind"] != "variant-offer":
            continue
        out = oracle.evaluate_case(c)
        for m in ("nb3sn", "rebco"):
            if c["policy"][m]["offer_basis"] == "carried-reference":
                assert c["labels"]["variant"].startswith("nb3sn_strain_-0.6pct") and c["labels"]["B_peak"] == 20.0
                continue
            f = out[m]["flat"]
            assert f["acceptance_margin"] >= 0.0 and f["cu_margin"] >= 0.0 and f["steel_margin"] >= 0.0
            if not c["policy"][m]["trace"]["rating_list_exhausted"]:
                assert f["capacity_margin"] >= 0.0


def test_all_cases_evaluate_to_finite_economics(cases):
    for c in cases:
        out = oracle.evaluate_case(c)
        for m in ("nb3sn", "rebco"):
            assert math.isfinite(out[m]["annualized"]["annualized_cost"])
            assert math.isfinite(out[m]["cold_load"]["q_cold"])
        if out["pair"]["rankable"]:
            assert out["nb3sn"]["conductor"]["status_code"] != 0 and out["rebco"]["conductor"]["status_code"] != 0
