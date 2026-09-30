"""Declared offer policy for WI-099 (contract section 5), built on the independent oracle.

The policy sits outside the evaluator. For each anchor, field, material, pairing, rule family and
assumption variant it proposes an offer:
  - n_elements: the smallest integer element count whose acceptance margin (the case's acceptance
    rule, evaluated by the oracle) is >= 0 under that case's assumptions;
  - per-turn areas: the construction rule's requirement at that duty, computed in double precision
    and rounded UP to the next 1e-6 mm^2 (design section 5, D1);
  - rating_cold: the smallest rating in the fixed list at or above the offer's cold-stage demand;
    the next lower listed rating is the insufficient refrigerator.
Insufficient offers take floor(0.9 n_ref) and generous offers ceil(1.2 n_ref), both with the
reference offer's component areas and rating (integer arithmetic, no float rounding).

Every value below is cited to the contract, the design or a source file; see oracle-notes.md.
"""
from __future__ import annotations

import copy
import importlib.util
import math
import sys
from pathlib import Path

_HERE = Path(__file__).resolve()
_ORACLE_PATH = _HERE.parents[1] / "oracle.py"


def load_oracle():
    name = "magnet_materials_independent_oracle"
    if name in sys.modules:
        return sys.modules[name]
    spec = importlib.util.spec_from_file_location(name, _ORACLE_PATH)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


oracle = load_oracle()

# ---------------------------------------------------------------------------------------------
# Fixed rating list (contract section 5), W at the cold stage.
# ---------------------------------------------------------------------------------------------
RATINGS_W = (1e3, 1.5e3, 2e3, 3e3, 5e3, 7.5e3, 10e3, 15e3, 20e3, 30e3, 50e3, 75e3)

# ---------------------------------------------------------------------------------------------
# Currency (contract section 7): Minneapolis Fed CPI, 2015 237.0, 2021 271.0.
# Source: knowledge/sources/federal_reserve_bank_of_minneapolis_annual_consumer_price/output.md:731, :773
# ---------------------------------------------------------------------------------------------
CPI = {1974: 49.3, 1990: 130.7, 2014: 236.7, 2015: 237.0, 2016: 240.0, 2021: 271.0}
USD2015_TO_2021 = CPI[2021] / CPI[2015]

ECONOMICS_REF = dict(crf=0.08, availability=0.8, electricity_price=60.0, hours=8760.0,
                     usd2015_to_2021=USD2015_TO_2021)

# ---------------------------------------------------------------------------------------------
# Anchors (contract section 2 and section 6)
# ---------------------------------------------------------------------------------------------
L0_WF = 2.45e-8  # W Ohm / K^2, Wiedemann-Franz (Ballarino; Stellaris model cryoplant.L0)


def _anchor_d():
    """EU DEMO TF envelope (Dematte): 16 coils x 142 turns, 104.95 kA at 12.04 T, pack 1296 x 411 mm."""
    pack_w, pack_h = 1296.0, 411.0  # mm (Dematte Table I; check-nb3sn.md section 4)
    turn_length = 55.6  # m, bounded assumption (contract section 2 table)
    I_ref = 104950.0
    return dict(
        name="D",
        duty=dict(coils=16.0, turns=142.0, turn_length=turn_length,
                  available_area=pack_w * pack_h / 142.0, I_ref=I_ref, B_ref=12.04),
        pack_area_m2=pack_w * pack_h * 1e-6,
        cold=dict(
            nuclear_density=35.5,  # W/m^3, Stellaris model q_nuc_cryo (stellarator_plant.sysml:492)
            # cold volume = coils x pack area x turn length (contract section 6, bounded assumption)
            cold_volume=16.0 * pack_w * pack_h * 1e-6 * turn_length,
            radiation_ref=1300.0,  # W, Koncar 2017 Table 1 (cryo-loads.md:26)
            conduction_ref=4600.0,  # W, 4.4 thermal anchor + 0.2 VVTS support (cryo-loads.md:26)
            T_conduction_ref=4.0,  # K, Koncar magnets at 4 K
            n_leads=4.0, f_lead=1.25, L0=L0_WF,  # bounded assumption (contract section 6)
            # 1 nOhm per joint x 16 joints per coil x 16 coils (contract section 6)
            p_joint_ref=16.0 * 16.0 * 1e-9 * I_ref ** 2, I_joint_ref=I_ref,
            # Koncar Table 1 shield loads VVTS 912.6 + CTS 189.4 kW (cryo-loads.md:27); see notes A6
            shield_static=(912.6 + 189.4) * 1e3,
            load_multiplier=1.0),
    )


def _stellaris_inventory():
    """Recompute the Stellaris 'Coil Thermal Inventory' terms at the published design.

    Formulas: models/library/analyses/mfe_cryo_inventory.sysml:10-17. Inputs:
    models/designs/stellarator_09/stellarator_plant.sysml (cryoplant block :1343-1422) with
    c_coil = 321600 / (48 * 308 * f_set) = 25.0 m (f_set = 0.8701298701298701, :231; conductor
    length 321,600 m from the replay record, binding-audit.md:113) and wp_side 0.36 m (:447).
    """
    n_coils, c_coil, wp_side, t_case = 48.0, 25.0, 0.36, 0.10
    eps_eff, sigma, q_mli, area_ratio = 0.05, 5.670374419e-8, 1.0, 1.2
    g_per_coil, k_c, k_s = 0.04, 5.39362701769, 12.12875814211
    n_leads, f_lead, I = 12.0, 1.25, 50000.0
    Tc, Ts, Ta = 20.0, 77.0, 300.0
    A_c = n_coils * c_coil * 4.0 * (wp_side + 2.0 * t_case)
    A_s = area_ratio * A_c
    q_rad_c = A_c * eps_eff * sigma * (Ts ** 4 - Tc ** 4)
    q_rad_s = A_s * q_mli - q_rad_c
    G = n_coils * g_per_coil
    q_sup_c = G * k_c * (Ts - Tc)
    q_sup_s = G * k_s * (Ta - Ts) - q_sup_c
    q_lead_c = f_lead * n_leads * I * math.sqrt(L0_WF * (Ts ** 2 - Tc ** 2))
    q_lead_s = f_lead * n_leads * I * math.sqrt(L0_WF * (Ta ** 2 - Ts ** 2))
    return dict(q_rad_c=q_rad_c, q_rad_s=q_rad_s, q_sup_c=q_sup_c, q_sup_s=q_sup_s,
                q_lead_c=q_lead_c, q_lead_s=q_lead_s, A_c=A_c)


STELLARIS_RATED_COLD_W = 21933.902368719853  # stellarator_plant.sysml:1346
STELLARIS_RATED_INTERCEPT_W = 41599.953939961626  # stellarator_plant.sysml:1347
STELLARIS_COLD_VOLUME = 136.56  # m^3, replay s0 vol_cold_total 136.55999999999997 (binding-audit.md:84)
STELLARIS_JOINTS_W = 7500.0  # stellarator_plant.sysml p_fixed_cryo = 0.0075 MW at 50 kA


def _anchor_s():
    """Stellaris coil set: 48 x 308 turns, 50 kA at 24.9 T, 0.36 m square pack of 308 turns."""
    inv = _stellaris_inventory()
    return dict(
        name="S",
        duty=dict(coils=48.0, turns=308.0,
                  # model conductor length 321,600 m / (48 x 308) (contract section 2 table); notes A7
                  turn_length=321600.0 / (48.0 * 308.0),
                  available_area=0.36 * 0.36 * 1e6 / 308.0, I_ref=50000.0, B_ref=24.9),
        cold=dict(
            nuclear_density=35.5, cold_volume=STELLARIS_COLD_VOLUME,
            radiation_ref=inv["q_rad_c"], conduction_ref=inv["q_sup_c"], T_conduction_ref=20.0,
            n_leads=12.0, f_lead=1.25, L0=L0_WF,
            p_joint_ref=STELLARIS_JOINTS_W, I_joint_ref=50000.0,
            shield_static=STELLARIS_RATED_INTERCEPT_W - inv["q_lead_s"],
            load_multiplier=1.0),
    )


ANCHORS = {"D": _anchor_d(), "S": _anchor_s()}

# Construction C calibration: Stellaris Table 7 fractions of the 0.36 m / 308-turn envelope at
# 50 kA and 24.9 T (contract section 4; Table 7 9/35/12/36/8 % tape/Cu/solder/steel/He,
# check-rebco-cryo-cost.md section 3). Unrounded so the Table 7 test holds at 1e-6 (notes A2).
_A_S = 0.36 * 0.36 * 1e6 / 308.0
C_CU_PER_KA = 0.35 * _A_S / 50.0
C_SOLDER_PER_KA = 0.12 * _A_S / 50.0
C_HELIUM_PER_KA = 0.08 * _A_S / 50.0
C_STEEL_PER_KA = 0.36 * _A_S / 50.0

# ---------------------------------------------------------------------------------------------
# Constructions (contract section 4)
# ---------------------------------------------------------------------------------------------
CONSTRUCTIONS = {
    "P": dict(cabling_factor=0.97, cable_void=0.20, ins_fraction=0.237,
              J_cu_rule=93.4, cu_void=0.10, cu_per_kA_rule=0.0,
              steel_per_kA_rule=12.66, B_steel_ref=12.04, steel_B_scaling=1.0,
              misc_per_kA=1.1077, solder_per_kA=0.0),
    "C": dict(cabling_factor=1.0, cable_void=0.0, ins_fraction=0.0,
              J_cu_rule=0.0, cu_void=0.0, cu_per_kA_rule=C_CU_PER_KA,
              steel_per_kA_rule=C_STEEL_PER_KA, B_steel_ref=24.9, steel_B_scaling=1.0,
              misc_per_kA=C_HELIUM_PER_KA, solder_per_kA=C_SOLDER_PER_KA),
}
PAIRINGS = {"common-P": {"nb3sn": "P", "rebco": "P"},
            "native": {"nb3sn": "P", "rebco": "C"},
            "common-C": {"nb3sn": "C", "rebco": "C"}}
RULE_FAMILIES = {"reference": {"nb3sn": 0.0, "rebco": 1.0},
                 "both-temperature": {"nb3sn": 0.0, "rebco": 0.0},
                 "both-fraction": {"nb3sn": 1.0, "rebco": 1.0}}

# ---------------------------------------------------------------------------------------------
# Conductors (contract section 3)
# ---------------------------------------------------------------------------------------------
STRAND_D = 0.82e-3  # m
# Breschi et al. 2017 Table III (printed p.22, PDF p.24), rendered and read from
# knowledge/sources/performance_analysis_of_the_toroidal_field_iter_production/raw.pdf.
# eps0a column holds fractions (check-nb3sn.md r2 item 6).
BRESCHI_TABLE_III = {
    "Jastec TFJA7-8": dict(p=0.84, q=2.570, Ca1=47.02, Ca2=11.76, eps0a=0.00231, Bc20=32.35, Tc0=16.22, C1=33000.0),
    "OST TFEU9": dict(p=0.746, q=2.335, Ca1=79.94, Ca2=45.04, eps0a=0.00207, Bc20=32.59, Tc0=16.26, C1=28622.88),
    "BEAS TFEU10-12": dict(p=0.549, q=1.726, Ca1=133.95, Ca2=111.72, eps0a=0.00389, Bc20=30.66, Tc0=16.07, C1=13173.6),
    "OST TFEU11-13": dict(p=0.999, q=2.581, Ca1=218.03, Ca2=187.61, eps0a=0.00156, Bc20=31.91, Tc0=16.12, C1=42910.56),
    "Kiswire TFKO4-8": dict(p=0.827, q=2.488, Ca1=70.28, Ca2=32.91, eps0a=0.0044, Bc20=31.58, Tc0=15.95, C1=35986.0),
    "Hitachi TFJA6L-9-10": dict(p=0.979945, q=2.561, Ca1=44.4841, Ca2=8.5389, eps0a=0.002525, Bc20=31.7556, Tc0=16.7055, C1=35557.3),
    "ChMP TFRF4-7": dict(p=0.519, q=1.662, Ca1=49.62, Ca2=9.51, eps0a=0.00259, Bc20=29.52, Tc0=16.62, C1=15250.0),
    "OST TFUS5R-7R": dict(p=0.471, q=1.670, Ca1=44.33, Ca2=0.0, eps0a=0.00194, Bc20=30.59, Tc0=16.16, C1=14928.0),
    "Luvata TFUS7L-8": dict(p=0.652, q=2.000, Ca1=46.04, Ca2=0.0, eps0a=0.00216, Bc20=31.8, Tc0=16.16, C1=20292.0),
    "WST TFCN5-6": dict(p=0.578, q=2.211, Ca1=47.52, Ca2=0.0, eps0a=0.00218, Bc20=34.22, Tc0=16.26, C1=20823.0),
}
STRAND_AREA_M2 = math.pi / 4.0 * STRAND_D ** 2
# Tsui & Hampshire 2012 Table 5 (printed p.8), engineering Jc; C in A T m^-2 -> C1 = C x strand area
# (nb3sn-law.md:22-24; check-nb3sn.md section 1).
TSUI_BEAS_II = dict(p=0.489, q=1.618, Ca1=226.93, Ca2=203.86, eps0a=0.00187, Bc20=30.28, Tc0=16.02,
                    C1=2.227e10 * STRAND_AREA_M2)
TSUI_OST = dict(p=0.746, q=2.335, Ca1=79.94, Ca2=45.04, eps0a=0.00207, Bc20=32.59, Tc0=16.26,
                C1=5.421e10 * STRAND_AREA_M2)
STRANDS = dict(BRESCHI_TABLE_III)
STRANDS["Tsui BEAS II"] = TSUI_BEAS_II
REFERENCE_STRAND = "WST TFCN5-6"

INVENTORY_REF = dict(
    element_density=8900.0,  # kg/m^3 [AGENT]; reported element mass only (notes A5)
    rho_cu=8940.0, rho_steel=8000.0, rho_solder=8390.0,  # stellarator_plant.sysml:380-387
    price_cu=11.0, price_steel=6.0, price_solder=64.44111923663972,  # stellarator_plant.sysml:389-396
    manufacturing_per_m=0.0)
REFRIGERATION_REF = dict(eta_mode=0.0, eta_const=0.24, green_a=0.155, green_b=0.23, f_carnot_shield=0.20,
                         capital_mode=0.0, green_c=3.1e6, green_d=0.65, T_green=4.5)

NB3SN_REF = dict(T_supply=4.5, nuclear_rise=0.7, margin_rise=1.5, fraction_rule=0.8,
                 strand_diameter=STRAND_D, strand_copper_fraction=0.5, eps_intrinsic=-0.003,
                 element_price_per_m=8.0, **STRANDS[REFERENCE_STRAND])
REBCO_REF = dict(T_supply=20.0, nuclear_rise=0.7, margin_rise=1.5, fraction_rule=0.8,
                 tape_width=0.004, tape_thickness=56e-6, tape_copper_fraction=10.0 / 56.0,
                 anchor_ic=198.0, shape_mode=0.0, g8=2.11, g10=1.85, g12=1.61, g15=1.33, g20=1.0,
                 alpha=0.6, T_star=22.0, degradation=0.90, element_price_per_m=80.0)

OFFER_KEYS = ("n_elements", "cabling_factor", "cable_void", "cu_space", "steel_area", "misc_area",
              "solder_area", "ins_fraction", "rating_cold")


# ---------------------------------------------------------------------------------------------
# Variants (contract sections 3-8), applied one at a time to the assumption set.
# Each variant is a list of (target, key, value): target is "duty", "economics", "nb3sn", "rebco",
# "cold" (both materials' cold-load inputs), "constr:P", "constr:C", or "constr:P:<material>".
# ---------------------------------------------------------------------------------------------
def _strand_edits(name):
    return [("nb3sn", k, v) for k, v in STRANDS[name].items()]


VARIANTS = {
    "nb3sn_strand_OST_TFEU9": _strand_edits("OST TFEU9"),
    "nb3sn_strand_BEAS_TFEU10-12": _strand_edits("BEAS TFEU10-12"),
    "nb3sn_strand_BEAS_II_Tsui": _strand_edits("Tsui BEAS II"),
    "nb3sn_strain_-0.6pct": [("nb3sn", "eps_intrinsic", -0.006)],
    "nb3sn_strain_-0.6pct_OST_TFEU9": [("nb3sn", "eps_intrinsic", -0.006)] + _strand_edits("OST TFEU9"),
    "nb3sn_strain_-0.6pct_BEAS_TFEU10-12": [("nb3sn", "eps_intrinsic", -0.006)] + _strand_edits("BEAS TFEU10-12"),
    "nb3sn_tcs_6.5K": [("nb3sn", "margin_rise", 1.3)],
    "rebco_shape_power_law": [("rebco", "shape_mode", 1.0)],
    "rebco_anchor_225A": [("rebco", "anchor_ic", 225.0)],
    "rebco_Tstar_17K": [("rebco", "T_star", 17.0)],
    "rebco_Tstar_33K": [("rebco", "T_star", 33.0)],
    "rebco_degradation_0.80": [("rebco", "degradation", 0.80)],
    "rebco_degradation_0.95": [("rebco", "degradation", 0.95)],
    "steel_base_layer1_9.3635": [("constr:P", "steel_per_kA_rule", 982.7 / 104.95)],
    "steel_base_layer8_16.24": [("constr:P", "steel_per_kA_rule", 16.24)],
    "steel_no_field_scaling": [("constr:P", "steel_B_scaling", 0.0), ("constr:C", "steel_B_scaling", 0.0)],
    "cu_density_common_100": [("constr:P", "J_cu_rule", 100.0)],
    "cu_density_material_93.4_100": [("constr:P:rebco", "J_cu_rule", 100.0)],
    "eta_constant_0.24": [("nb3sn", "eta_mode", 1.0), ("rebco", "eta_mode", 1.0)],
    "eta_input_power_20K": [("rebco", "eta_mode", 2.0)],
    "capital_capacity_basis_20K": [("rebco", "capital_mode", 1.0)],
    "combined_unfavourable_20K": [("rebco", "eta_mode", 2.0), ("rebco", "capital_mode", 1.0)],
    "cold_load_x0.5": [("cold", "load_multiplier", 0.5)],
    "cold_load_x2": [("cold", "load_multiplier", 2.0)],
    "electricity_30": [("economics", "electricity_price", 30.0)],
    "electricity_120": [("economics", "electricity_price", 120.0)],
    "crf_0.05": [("economics", "crf", 0.05)],
    "crf_0.11": [("economics", "crf", 0.11)],
    "turn_length_D_45m": [("duty", "turn_length", 45.0)],
    "turn_length_D_60m": [("duty", "turn_length", 60.0)],
    "manufacturing_nb3sn_only": [("nb3sn", "manufacturing_per_m", 1128.0)],
    "manufacturing_both": [("nb3sn", "manufacturing_per_m", 1128.0), ("rebco", "manufacturing_per_m", 1128.0)],
    "price_nb3sn_5.4": [("nb3sn", "element_price_per_m", 5.4)],
    "price_nb3sn_13.5": [("nb3sn", "element_price_per_m", 13.5)],
    "price_rebco_30_target": [("rebco", "element_price_per_m", 30.0)],
    "price_rebco_10_volume": [("rebco", "element_price_per_m", 10.0)],
}
ANCHOR_ONLY_VARIANTS = {"turn_length_D_45m": "D", "turn_length_D_60m": "D"}


# ---------------------------------------------------------------------------------------------
# Assumption sets
# ---------------------------------------------------------------------------------------------
def assumptions(anchor: str, B: float, pairing: str, family: str, variant: str = "none") -> dict:
    """Everything except the offer: duty, economics, per-material law/rule/cost/cold/refrigeration
    inputs, and each material's construction rule (with generation-only misc/solder per kA)."""
    A = ANCHORS[anchor]
    duty = dict(A["duty"], B_peak=float(B))
    econ = dict(ECONOMICS_REF)
    mats = {}
    for m, base in (("nb3sn", NB3SN_REF), ("rebco", REBCO_REF)):
        full = dict(INVENTORY_REF)
        full.update(REFRIGERATION_REF)
        full.update(A["cold"])
        full.update(base)
        full["acceptance_rule"] = RULE_FAMILIES[family][m]
        mats[m] = full
    constr = {m: copy.deepcopy(CONSTRUCTIONS[PAIRINGS[pairing][m]]) for m in mats}
    edits = [] if variant == "none" else VARIANTS[variant]
    if variant in ANCHOR_ONLY_VARIANTS and ANCHOR_ONLY_VARIANTS[variant] != anchor:
        raise ValueError(f"{variant} applies to anchor {ANCHOR_ONLY_VARIANTS[variant]} only")
    for target, key, value in edits:
        if target == "duty":
            duty[key] = float(value)
            if key == "turn_length" and anchor == "D":
                # anchor D cold volume = coils x pack area x turn length (contract section 6); notes A8
                for m in mats:
                    mats[m]["cold_volume"] = duty["coils"] * A["pack_area_m2"] * duty["turn_length"]
        elif target == "economics":
            econ[key] = float(value)
        elif target == "cold":
            for m in mats:
                mats[m][key] = float(value)
        elif target in mats:
            mats[target][key] = float(value)
        elif target.startswith("constr:"):
            parts = target.split(":")
            for m in mats:
                if PAIRINGS[pairing][m] != parts[1]:
                    continue
                if len(parts) == 3 and parts[2] != m:
                    continue
                constr[m][key] = float(value)
        else:
            raise KeyError(target)
    for m in mats:
        # rule inputs (requirement side) travel with the assumptions, not with the offer
        c = constr[m]
        for k in ("J_cu_rule", "cu_void", "cu_per_kA_rule", "steel_per_kA_rule", "B_steel_ref", "steel_B_scaling"):
            mats[m][k] = c[k]
    return dict(anchor=anchor, pairing=pairing, family=family, variant=variant,
                duty=duty, economics=econ, construction=constr, materials=mats)


# ---------------------------------------------------------------------------------------------
# Offer generation
# ---------------------------------------------------------------------------------------------
def round_up_1e6(x: float) -> float:
    """Round up to the next 1e-6 mm^2 (design D1), guaranteeing the float result is >= x."""
    k = math.ceil(x * 1e6)
    r = k / 1e6
    while r < x:
        k += 1
        r = k / 1e6
    return r


def _case_from(asm: dict, offers: dict) -> dict:
    case = dict(duty=dict(asm["duty"]), economics=dict(asm["economics"]))
    for m in ("nb3sn", "rebco"):
        part = dict(asm["materials"][m])
        part.update(offers[m])
        case[m] = part
    return case


def _conductor_eval(asm: dict, material: str, n: int) -> dict:
    part = dict(asm["materials"][material])
    part["n_elements"] = float(n)
    I = oracle.turn_current(asm["duty"])
    part.update(turn_current=I, B_peak=asm["duty"]["B_peak"])
    if material == "nb3sn":
        return oracle.nb3sn_cable_critical_surface(part)
    return oracle.rebco_cable_critical_surface(part)


def _rule_ic_per_element(asm: dict, material: str) -> float:
    """Per-element critical current at the rule temperature (temperature rule) or the operating
    temperature times fraction_rule (fraction rule); used only for the starting estimate."""
    p = asm["materials"][material]
    B = asm["duty"]["B_peak"]
    T_cond = p["T_supply"] + p["nuclear_rise"]
    if p["acceptance_rule"] == 0.0:
        T = T_cond + p["margin_rise"]
        frac = 1.0
    else:
        T = T_cond
        frac = p["fraction_rule"]
    if material == "nb3sn":
        ic = oracle.nb3sn_ic_strand(B, T, p["eps_intrinsic"], oracle._nb3sn_params(p))
    else:
        ic = (p["degradation"] * p["anchor_ic"] * oracle.rebco_shape(B, p)
              * math.exp(-(T - 20.0) / p["T_star"]))
    return frac * ic


def smallest_n(asm: dict, material: str, n_cap: int = 10_000_000):
    """Smallest integer n with acceptance_margin >= 0 (oracle), ignoring the support status so an
    offer exists at unsupported points. Returns (n or None, trace)."""
    I = oracle.turn_current(asm["duty"])
    ic = _rule_ic_per_element(asm, material)
    if ic <= 0.0:
        return None, dict(n_continuous=None, reason="rule-point critical current is zero")
    n_est = I / ic
    if n_est > n_cap:
        return None, dict(n_continuous=n_est, reason="exceeds cap")
    n = max(1, int(math.floor(n_est)) - 2)
    while _conductor_eval(asm, material, n)["acceptance_margin"] < 0.0:
        n += 1
    while n > 1 and _conductor_eval(asm, material, n - 1)["acceptance_margin"] >= 0.0:
        n -= 1
    ev = _conductor_eval(asm, material, n)
    return n, dict(n_continuous=n_est, acceptance_margin=ev["acceptance_margin"],
                   status_code=ev["status_code"], margin_at_n_minus_1=(
                       _conductor_eval(asm, material, n - 1)["acceptance_margin"] if n > 1 else None))


def generate_areas(asm: dict, material: str, n: int) -> tuple[dict, dict]:
    """Construction-rule areas at the offer's reference duty, rounded up (D1)."""
    c = asm["construction"][material]
    duty = asm["duty"]
    I = oracle.turn_current(duty)
    B = duty["B_peak"]
    cond = _conductor_eval(asm, material, n)
    elem_cu = cond["element_copper_area"]
    if c["J_cu_rule"] > 0.0:
        cu_req = max(0.0, I / c["J_cu_rule"] - elem_cu) / (1.0 - c["cu_void"])
    else:
        cu_req = c["cu_per_kA_rule"] * I / 1000.0
    scale = B / c["B_steel_ref"] if c["steel_B_scaling"] != 0.0 else 1.0
    steel_req = c["steel_per_kA_rule"] * (I / 1000.0) * scale
    misc = c["misc_per_kA"] * I / 1000.0
    solder = c["solder_per_kA"] * I / 1000.0
    areas = dict(cabling_factor=c["cabling_factor"], cable_void=c["cable_void"],
                 cu_space=round_up_1e6(cu_req), steel_area=round_up_1e6(steel_req),
                 misc_area=round_up_1e6(misc), solder_area=round_up_1e6(solder) if solder > 0.0 else 0.0,
                 ins_fraction=c["ins_fraction"])
    trace = dict(cu_required_generation=cu_req, steel_required_generation=steel_req,
                 cu_roundup=areas["cu_space"] - cu_req, steel_roundup=areas["steel_area"] - steel_req)
    return areas, trace


def select_rating(q_cold: float) -> dict:
    """Smallest listed rating >= demand; next lower listed rating is the insufficient refrigerator."""
    idx = next((i for i, r in enumerate(RATINGS_W) if r >= q_cold), None)
    if idx is None:
        return dict(rating=RATINGS_W[-1], insufficient=RATINGS_W[-2], list_exhausted=True)
    return dict(rating=RATINGS_W[idx], insufficient=RATINGS_W[idx - 1] if idx > 0 else None,
                list_exhausted=False)


def cold_demand(asm: dict, material: str) -> float:
    part = dict(asm["materials"][material])
    part["turn_current"] = oracle.turn_current(asm["duty"])
    return oracle.magnet_cold_stage_load(part)["q_cold"]


def propose_offer(asm: dict) -> dict:
    """The reference offer for each material under the assumption set `asm`.

    Returns {material: {"offer": {...OFFER_KEYS...}, "trace": {...}}}. If no integer n meets the
    rule (critical current zero at the rule point), the material's offer is None.
    """
    result = {}
    for m in ("nb3sn", "rebco"):
        n, ntrace = smallest_n(asm, m)
        q = cold_demand(asm, m)
        sel = select_rating(q)
        if n is None:
            result[m] = dict(offer=None, trace=dict(ntrace, q_cold_generation=q, **sel))
            continue
        areas, atrace = generate_areas(asm, m, n)
        offer = dict(n_elements=float(n), **areas, rating_cold=sel["rating"])
        trace = dict(ntrace, **atrace, q_cold_generation=q, rating_list_exhausted=sel["list_exhausted"],
                     insufficient_rating=sel["insufficient"])
        result[m] = dict(offer=offer, trace=trace)
    return result


def insufficient_n(n: int) -> int:
    return (9 * n) // 10  # floor(0.9 n), integer arithmetic


def generous_n(n: int) -> int:
    return (12 * n + 9) // 10  # ceil(1.2 n), integer arithmetic


def assemble_case(asm: dict, offers: dict) -> dict:
    """Full section-6 case from an assumption set and per-material offers."""
    return _case_from(asm, offers)
