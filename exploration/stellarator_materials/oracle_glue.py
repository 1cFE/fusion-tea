"""Independent glue oracle for WI-100 (plant-level conductor material variants).

Author: T-015 independent oracle author, brief
work/orchestration/goals/magnet-material-comparison/evidence/briefs/t015-glue-oracle.md.

Written from the reviewed design and the contract only:
  - work/active/WI-100_stellarator-material-variants/design.md (D1-D18 applied in place)
  - work/orchestration/goals/magnet-material-comparison/evidence/design-review-wi100.md, Recheck R1-R6
  - work/orchestration/goals/magnet-material-comparison/evidence/plant-contract.md (r4) sections 3-7
The implementer's package (everything else under exploration/stellarator_materials/) and the
WI-100 implementation notes, build and prototype directories were not read.

Composition is by import only; no existing oracle file is edited:
  - the plant oracle family: exploration/stellarator_e2e/verify_stellaris.py (its function-level
    pieces), its oracle_*.py modules, and exploration/stellarator_e2e/studies/oracle_entry.py
    (entry-key map, output-channel map, operand bindings, and the reference evaluate);
  - Round 1's oracle: exploration/magnet_materials/oracle.py.

What is computed here:
  - every glue calc of design section 2.4, the arm-modified 'Conductor Peak Field' (2.2), the
    gated plant REBCO law (2.1), the structure-mass rule as a recorded-design check;
  - the material-instance plant chain (`_plant_chain`), which recomposes the plant oracle's
    function-level pieces with the rebound legs (Round 1 and glue). The plant oracle's own
    `compute()` cannot evaluate a material instance: it runs the plant REBCO law unconditionally,
    and that law refuses any supply temperature other than 20 K and any field outside 20-32 T
    (verify_stellaris.py:902-909). So the inline equations of `compute()` are re-derived here,
    each against its SysML source, and `test_reference_chain_is_bit_identical` proves the
    re-derivation reproduces `compute()` bit for bit when the legs are the reference ones;
  - the power balance, capital rollups, CAS70/80 levelization, DCF and LCOE of a material
    instance; its 73 verdicts (the 67 plant predicates, read from the reference package's predicate
    IR, plus the six new checks); the LCOE breakdown of design section 5.2 (D2).

Numerical methods: no glue calc has a free method (all are closed-form). The Round 1 pieces keep
Round 1's own independent methods (Brent-Dekker Tcs root, Gauss-Legendre NIST integral). The plant
ash fixed point and profile quadrature are the plant's fixed discretization contract and are
imported unchanged.

Units: A, T, K, m, kg, W unless named; Round 1 areas mm2; money in the plant's dollars, with Round 1
prices and the Green refrigerator capital in USD2021 (design K14, contract section 6 F12).
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import math
import sys
from collections.abc import Mapping
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
E2E = ROOT / "exploration" / "stellarator_e2e"
E2E_STUDIES = E2E / "studies"
for _path in (E2E, E2E_STUDIES):
    if str(_path) not in sys.path:
        sys.path.insert(0, str(_path))

import oracle_entry as oe  # noqa: E402  (plant seam; also memoizes the profile integral)
import verify_stellaris as vs  # noqa: E402  (the independent plant oracle)


def _load_round1():
    path = ROOT / "exploration" / "magnet_materials" / "oracle.py"
    name = "magnet_materials_round1_oracle"
    if name in sys.modules:
        return sys.modules[name]
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


r1 = _load_round1()

# ---------------------------------------------------------------------------------------------
# Identity, pin and reference contract
# ---------------------------------------------------------------------------------------------
REFERENCE_PREFIX = oe.P  # 'stellarator_09__stellaris__'
MATERIALS = ("rebco", "nb3sn")
MATERIAL_PREFIXES = {
    "rebco": "stellarator_09_materials__rebco_material__",
    "nb3sn": "stellarator_09_materials__nb3sn_material__",
}
PIN_INPUTS_PATH = (ROOT / "work" / "active" / "WI-098_whole-plant-conversion-comparison" / "evidence"
                   / "magnet-probe" / "baseline-inputs.json")
PIN_OUTPUTS_PATH = (ROOT / "work" / "active" / "WI-080_supplied-thermal-equipment-capability-and-demand-checks"
                    / "integration" / "baseline.json")
REFERENCE_CONTRACT_PATH = E2E / "pkg" / "stellarator_tea" / "contracts" / "model_contract.json"
MANIFEST_PATH = E2E_STUDIES / "manifest.json"
REUSE_PATH = Path(__file__).resolve().parent / "oracle-reuse.json"

#: Vacuum permeability, as 'Coil Set Axis Field' (models/library/analyses/mfe_magnet_field.sysml:52-53).
MU0 = 1.25663706212e-6

#: Declared reference-prefix entry-key delta (design section 1.5, D6) and its neutral values.
NEW_REFERENCE_KEYS = {"magnet__rebco_law_enabled": 1.0, "magnet__coil__arm_slope": 0.0,
                      "magnet__coil__arm_x_ref": 0.0}
#: Declared reference-prefix output delta (design section 1.5; review R4 assigns it here).
REFERENCE_NEW_OUTPUT = "magnet__conductor_current__evaluation_defined"


class GlueOracleError(Exception):
    """An input, key or domain this oracle refuses. Always a declared failure, never a pass."""


def _load_json(path: Path):
    return json.loads(path.read_text())


PIN_SUFFIX_INPUTS: dict[str, object] = {
    key[len(REFERENCE_PREFIX):]: value for key, value in _load_json(PIN_INPUTS_PATH).items()}
#: suffix -> plant-oracle input name, taken from the plant seam (never re-declared here).
SUFFIX_TO_ORACLE: dict[str, str] = {
    key[len(REFERENCE_PREFIX):]: name for key, name in oe.ENTRY_KEY_TO_ORACLE_INPUT.items()}
#: suffix -> channel suffix for every plant-oracle output the plant package records.
ORACLE_TO_SUFFIX: dict[str, str] = {
    name: channel[len(REFERENCE_PREFIX):] for name, channel in oe.ORACLE_OUTPUT_TO_CHANNEL.items()}

# ---------------------------------------------------------------------------------------------
# Material-instance key schema (design sections 2.5-2.7, 5.1; review R5)
# ---------------------------------------------------------------------------------------------
NB3SN_LAW = ("strand_diameter", "strand_copper_fraction", "p", "q", "C1", "Ca1", "Ca2", "eps0a",
             "Bc20", "Tc0", "nuclear_rise", "margin_rise", "fraction_rule", "acceptance_rule")
NB3SN_BOUNDS = ("B_law_min", "B_law_max", "B_design_max", "B_edge_max", "T_law_min", "T_law_max",
                "eps_min", "eps_max")
REBCO_LAW = ("tape_width", "tape_thickness", "tape_copper_fraction", "anchor_ic", "g8", "g10", "g12",
             "g15", "g20", "alpha", "T_star", "degradation", "nuclear_rise", "margin_rise",
             "fraction_rule", "acceptance_rule")
REBCO_BOUNDS = ("B_knot_min", "B_knot_max", "B_law_min", "B_law_max", "T_law_min", "T_law_max")
CONSTRUCTION = ("cabling_factor", "cable_void", "cu_space", "steel_area", "misc_area", "solder_area",
                "ins_fraction", "J_cu_rule", "cu_void", "cu_per_kA_rule", "steel_per_kA_rule",
                "B_steel_ref", "steel_B_scaling")
NIST_NAMES = ("k_a", "k_b", "k_c", "k_d", "k_e", "k_f", "k_g", "k_h", "k_i")
#: Design 2.7 declares the NIST fit as 'Staged Cryoplant' attributes k_a ... k_i, but 'Cryoplant'
#: already owns k_c, the support conductance integral (mfe_plant_systems.sysml:554, bound 5.39362701769
#: at stellarator_plant.sysml:1387). So cryoplant__k_c stays the plant's key here; the NIST fit is
#: Round 1's fixed constant (oracle.NIST316_COEFFS) and the eight non-colliding names are accepted
#: only at Round 1's values. See oracle-notes.md, ambiguity G1.
NIST_OPTIONAL_KEYS = {"cryoplant__" + name: value for name, value in zip(NIST_NAMES, r1.NIST316_COEFFS)
                      if name != "k_c"}
STAGED_CRYO = ("load_multiplier", "eta_mode", "eta_const", "green_a", "green_b",
               "capital_mode", "green_c", "green_d", "T_green", "usd2015_to_2021", "T_conduction_ref",
               "I_joint_ref")

ARM_SLOPE_KEY = "magnet__coil__arm_slope"
ARM_XREF_KEY = "magnet__coil__arm_x_ref"
MU0_KEY = "magnet__pack_field__mu0_in"
EPS_KEY = "magnet__conductor__eps_intrinsic_in"
INTERCEPT_AVAILABLE_KEY = "cryoplant__intercept_demand_available"
#: Removed class of the section 5.1 partition (K11, R5): refused under a material prefix.
REMOVED_KEYS = ("cryoplant__purchase_cost_per_module", "cryoplant__inventory_enabled",
                "magnet__rebco_law_enabled")

#: Held material facts, default values as the design binds them (E7), from the Round 1 design file.
#: Nb3Sn law models/designs/magnet_materials/magnet_subsystem.sysml:56-100, bounds :238-261,
#: element density :142.
NB3SN_FACTS = dict(strand_diameter=0.00082, strand_copper_fraction=0.5, p=0.578, q=2.211, C1=20823.0,
                   Ca1=47.52, Ca2=0.0, eps0a=0.00218, Bc20=34.22, Tc0=16.26, nuclear_rise=0.7,
                   margin_rise=1.5, fraction_rule=0.8, acceptance_rule=0.0, B_law_min=8.0,
                   B_law_max=14.5, B_design_max=12.2, B_edge_max=13.5, T_law_min=4.2, T_law_max=12.0,
                   eps_min=-0.01, eps_max=0.002, element_density=8900.0)
#: REBCO law magnet_subsystem.sysml:472-521, bounds :660-677 with B_law_max = 25.0 (contract
#: section 4 F10, design E7), element density :564.
REBCO_FACTS = dict(tape_width=0.004, tape_thickness=5.6e-05, tape_copper_fraction=0.17857142857142858,
                   anchor_ic=198.0, g8=2.11, g10=1.85, g12=1.61, g15=1.33, g20=1.0, alpha=0.6,
                   T_star=22.0, degradation=0.9, nuclear_rise=0.7, margin_rise=1.5, fraction_rule=0.8,
                   acceptance_rule=1.0, B_knot_min=8.0, B_knot_max=20.0, B_law_min=5.0, B_law_max=25.0,
                   T_law_min=4.2, T_law_max=50.0, element_density=8900.0)
#: 'Staged Cryoplant' held facts: Green and NIST magnet_subsystem.sysml:203-235, :268-293;
#: T_conduction_ref 20.0 and I_joint_ref 50,000 per design E7 (stellarator_plant.sysml:1387, :1416
#: with :202).
STAGED_CRYO_FACTS = dict(load_multiplier=1.0, eta_mode=0.0,
                         eta_const=0.24, green_a=0.155, green_b=0.23, capital_mode=0.0,
                         green_c=3100000.0, green_d=0.65, T_green=4.5,
                         usd2015_to_2021=1.1434599156118144, T_conduction_ref=20.0,
                         I_joint_ref=50000.0)
#: Material values on plant keys (design E8).
MATERIAL_PLANT_VALUES = {
    "rebco": {"cryoplant__T_cold_cryo": 20.0, "cryoplant__rated_cryogenic_cold_K": 20.0,
              "magnet__winding_pack__B_max": 25.0, "magnet__winding_pack__eps_cond_allow": 0.004},
    "nb3sn": {"cryoplant__T_cold_cryo": 4.5, "cryoplant__rated_cryogenic_cold_K": 4.5,
              "magnet__winding_pack__B_max": 13.0, "magnet__winding_pack__eps_cond_allow": 0.003},
}
#: Glue slot defaults: arm slope 0 (H3 library default), arm_x_ref 35.278 (E7), mu0 held (D5).
GLUE_DEFAULTS = {ARM_SLOPE_KEY: 0.0, ARM_XREF_KEY: 35.278, MU0_KEY: MU0}

#: Supplied-design quantities with no design-stated value: the caller must supply them.
REQUIRED_SUPPLIED = {
    "rebco": tuple("magnet__" + n for n in ("n_elements", *CONSTRUCTION, "element_price_per_m")),
    "nb3sn": tuple("magnet__" + n for n in ("n_elements", *CONSTRUCTION, "element_price_per_m")) + (EPS_KEY,),
}


def material_facts(material: str) -> dict[str, float]:
    """The held material and cryo facts a material instance binds by default (suffix keys)."""
    _check_material(material)
    facts = NB3SN_FACTS if material == "nb3sn" else REBCO_FACTS
    out = {"magnet__" + k: v for k, v in facts.items()}
    out.update({"cryoplant__" + k: v for k, v in STAGED_CRYO_FACTS.items()})
    out.update(MATERIAL_PLANT_VALUES[material])
    out.update(GLUE_DEFAULTS)
    return out


def variant_keys(material: str) -> set[str]:
    """Every suffix key the material instance adds to the plant keys."""
    keys = (set(material_facts(material)) | set(REQUIRED_SUPPLIED[material]) | {INTERCEPT_AVAILABLE_KEY}
            | set(NIST_OPTIONAL_KEYS))
    return keys - set(MATERIAL_PLANT_VALUES[material])


def _check_material(material: str) -> None:
    if material not in MATERIALS:
        raise GlueOracleError(f"unknown material {material!r}; expected one of {MATERIALS}")


def _finite(name: str, value) -> float:
    if isinstance(value, bool):
        raise GlueOracleError(f"{name}: Boolean where a real is required")
    try:
        value = float(value)
    except (TypeError, ValueError) as exc:
        raise GlueOracleError(f"{name}: not a real number") from exc
    if not math.isfinite(value):
        raise GlueOracleError(f"{name}: nonfinite value {value!r}")
    return value


# ---------------------------------------------------------------------------------------------
# Glue calc defs (design section 2.4), each a function of its section-2.4 input names
# ---------------------------------------------------------------------------------------------
def material_winding_adapter(x: Mapping[str, float]) -> dict[str, float]:
    """'Material Winding Adapter': the plant's per-turn length and the pack's share per turn.

    turn_length = f_set * c_coil [m] (the plant conductor-length identity,
    models/library/analyses/mfe_winding_pack_cost.sysml:44); pack_area_per_turn =
    wp_side * wp_side * 1e6 / reference_turns [mm2] (contract section 5 pack-side rule).
    """
    return dict(turn_length=x["f_set_in"] * x["c_coil_in"],
                pack_area_per_turn=x["wp_side_in"] * x["wp_side_in"] * 1e6 / x["reference_turns_in"])


def material_winding_cost(x: Mapping[str, float]) -> dict[str, float]:
    """'Material Winding Cost': the one-basis winding account of contract section 6 (N3, N4)."""
    return dict(cost=x["superconductor_cost_in"] + x["materials_cost_in"] + x["helium_cost_in"]
                + x["winding_operations_cost_in"])


def pack_field_checks(x: Mapping[str, float]) -> dict[str, float]:
    """'Pack Field Checks' (contract sections 3.2 and 7 r4 (C)).

    R_over_sqrt_A_wp = R / wp_side; ampere_floor = mu0 * I_coil / (4 * wp_side) [T], the exact
    Ampere floor on the mean tangential field around a square pack of side wp_side carrying the
    coil current I_coil; ampere_floor_margin = B_peak - ampere_floor [T].
    """
    wp_side = x["wp_side_in"]
    floor = x["mu0_in"] * x["I_coil_in"] / (4.0 * wp_side)
    return dict(R_over_sqrt_A_wp=x["R_in"] / wp_side, ampere_floor=floor,
                ampere_floor_margin=x["B_peak_in"] - floor)


def rebco_shape_branch(x: Mapping[str, float]) -> dict[str, float]:
    """'REBCO Shape Branch': measured knots up to B_knot_max, power law above (contract section 4)."""
    return dict(shape_mode=1.0 if x["B_peak_in"] > x["B_knot_max_in"] else 0.0)


def staged_static_loads(x: Mapping[str, float]) -> dict[str, float]:
    """'Staged Static Loads': the plant's static-term equations without its 10-30 K guard.

    Plant equations models/library/analyses/mfe_cryo_inventory.sysml:11-16 (WI-059 D3-D4):
      area_cold      = n_coils * c_coil * 4 * (wp_side + 2 t_case)
      q_radiation    = area_cold * eps_eff * sigma_SB * (T_shield^4 - T_cold^4)
      conduction_ref = n_coils * g_per_coil * k_c * (T_shield - T_conduction_ref)
      shield_static  = shield_area_ratio * area_cold * q_MLI - q_radiation
                       + n_coils * g_per_coil * k_s * (T_amb - T_shield) - conduction_ref
      p_joint_ref    = p_fixed_MW * 1e6 [W]
    """
    area = x["n_coils_in"] * x["c_coil_in"] * 4.0 * (x["wp_side_in"] + 2.0 * x["t_case_in"])
    t_shield, t_cold = x["T_shield_in"], x["T_cold_in"]
    radiation = area * x["eps_eff_in"] * x["sigma_SB_in"] * (t_shield ** 4 - t_cold ** 4)
    bridge = x["n_coils_in"] * x["g_per_coil_in"]
    conduction = bridge * x["k_c_in"] * (t_shield - x["T_conduction_ref_in"])
    shield_static = (x["shield_area_ratio_in"] * area * x["q_MLI_in"] - radiation
                     + bridge * x["k_s_in"] * (x["T_amb_in"] - t_shield) - conduction)
    return dict(area_cold=area, q_radiation=radiation, conduction_ref=conduction,
                shield_static=shield_static, p_joint_ref=x["p_fixed_MW_in"] * 1e6)


def staged_drive_power(x: Mapping[str, float]) -> dict[str, float]:
    """'Staged Drive Power': lead Joule heat plus the driven share of joint heat [MW].

    p_drive = (q_leads + (q_shield - shield_static) + joint_drive_fraction * q_joints) * 1e-6;
    the plant drive definition models/library/analyses/mfe_cryo_inventory.sysml:17.
    """
    return dict(p_drive=(x["q_leads_in"] + (x["q_shield_in"] - x["shield_static_in"])
                         + x["joint_drive_fraction_in"] * x["q_joints_in"]) * 1e-6)


def ampere_floor_ok(margin: float) -> bool | None:
    """Constraint def 'Ampere Floor': margin_in >= 0.0 (Kleene: NaN is indeterminate)."""
    return None if math.isnan(margin) else margin >= 0.0


# ---------------------------------------------------------------------------------------------
# Arm-modified 'Conductor Peak Field' (design section 2.2, hunks H2-H4, body B2)
# ---------------------------------------------------------------------------------------------
def conductor_peak_field(x: Mapping[str, float]) -> dict[str, float]:
    """B_peak = (B_axis * ratio_eff) * bore_norm, ratio_eff = peak_ratio + arm_slope*(R/wp_side - x_ref).

    bore_norm = [R/(R - a_coil)] / [R_ref/(R_ref - a_coil_ref)] (mfe_plasma_scaling.sysml:426-428).
    Refusals, in body B2's order: the two clearances (mfe_plasma_scaling.sysml:465), then nonfinite
    arm inputs, wp_side <= 0, and ratio_eff <= 0. At arm_slope = 0 the result is bit-identical to
    the unmodified calc for every finite arm_x_ref (0.0 * finite = +-0.0 and peak_ratio + -0.0 =
    peak_ratio in IEEE-754).
    """
    B_axis, peak_ratio = x["B_axis_in"], x["peak_ratio_in"]
    R, a_coil, R_ref, a_coil_ref = x["R_in"], x["a_coil_in"], x["R_ref_in"], x["a_coil_ref_in"]
    wp_side = x.get("wp_side_in", 1.0)
    slope = x.get("arm_slope_in", 0.0)
    x_ref = x.get("arm_x_ref_in", 0.0)
    if not R - a_coil > 0.0:
        raise ValueError("glue Conductor Peak Field: live clearance R - a_coil must be > 0")
    if not R_ref - a_coil_ref > 0.0:
        raise ValueError("glue Conductor Peak Field: reference clearance R_ref - a_coil_ref must be > 0")
    for name, value in (("wp_side_in", wp_side), ("arm_slope_in", slope), ("arm_x_ref_in", x_ref)):
        if isinstance(value, bool) or not math.isfinite(value):
            raise ValueError(f"glue Conductor Peak Field: nonfinite arm input {name}")
    if not wp_side > 0.0:
        raise ValueError("glue Conductor Peak Field: wp_side_in must be > 0")
    bore_factor = R / (R - a_coil)
    bore_factor_ref = R_ref / (R_ref - a_coil_ref)
    bore_norm = bore_factor / bore_factor_ref
    x_pack = R / wp_side
    ratio_eff = peak_ratio + slope * (x_pack - x_ref)
    if not ratio_eff > 0.0:
        raise ValueError("glue Conductor Peak Field: effective peak ratio must be > 0")
    return dict(B_peak=(B_axis * ratio_eff) * bore_norm, ratio_eff=ratio_eff,
                R_over_sqrt_A_wp=x_pack, bore_norm=bore_norm)


# ---------------------------------------------------------------------------------------------
# Gated plant 'REBCO Conductor Current' (design section 2.1, H1-H2, body B1)
# ---------------------------------------------------------------------------------------------
CONDUCTOR_CURRENT_OUTPUTS = (
    "parallel_tapes_set", "parallel_tapes_reference", "tape_critical_current",
    "critical_current_reference", "critical_current_set", "operating_fraction_reference",
    "operating_fraction_set", "allowable_current", "margin_fraction", "margin_current",
    "field_extrapolated")


def gated_rebco_conductor_current(p: Mapping[str, float], field: float, tape_length: float,
                                  conductor_length: float, enabled: float) -> dict[str, float]:
    """enabled = 0: all 11 outputs and evaluation_defined are 0.0 before any domain check.

    enabled = 1: the unchanged plant law (verify_stellaris._conductor_current, imported) with
    evaluation_defined = 1.0. Any other value refuses (WI-080 pattern, mfe_viability.sysml:106-118).
    """
    if isinstance(enabled, bool) or not math.isfinite(enabled) or enabled not in (0.0, 1.0):
        raise ValueError("glue REBCO Conductor Current: enabled must be 0 or 1")
    if enabled == 0.0:
        out = dict.fromkeys(CONDUCTOR_CURRENT_OUTPUTS, 0.0)
        out["evaluation_defined"] = 0.0
        return out
    out = dict(vs._conductor_current(p, field, tape_length, conductor_length))
    out["evaluation_defined"] = 1.0
    return out


# ---------------------------------------------------------------------------------------------
# Structure-mass rule as a recorded-design check (contract section 5; design section 6.3)
# ---------------------------------------------------------------------------------------------
#: 11,615.6 t and 111 GJ exactly as contract section 5 prints them.
STRUCTURE_MASS_ANCHOR_KG = 11_615_600.0
STRUCTURE_W_MAG_ANCHOR_J = 111.0e9


def structure_mass_rule(W_mag: float, variant: float = 1.0) -> float:
    """m_support = 11,615.6 t x (W_mag / 111 GJ) x variant [kg]; variants 0.5 and 2 (contract F13)."""
    return STRUCTURE_MASS_ANCHOR_KG * (W_mag / STRUCTURE_W_MAG_ANCHOR_J) * variant


def structure_mass_check(m_support: float, W_mag: float, variant: float = 1.0,
                         rel_tol: float = 1e-9) -> dict[str, float | bool]:
    """Whether a recorded supplied m_support equals the rule at the design's own W_mag."""
    rule = structure_mass_rule(W_mag, variant)
    residual = (m_support - rule) / rule
    return dict(rule_mass_kg=rule, supplied_mass_kg=m_support, relative_residual=residual,
                variant=variant, rel_tol=rel_tol, consistent=abs(residual) <= rel_tol)


# ---------------------------------------------------------------------------------------------
# The material legs: Round 1 and glue pieces bound as design sections 2.5-2.9 bind them
# ---------------------------------------------------------------------------------------------
class _MaterialLegs:
    def __init__(self, material: str, resolved: Mapping[str, object]):
        self.material = material
        self.v = resolved

    def arm(self) -> tuple[float, float]:
        return float(self.v[ARM_SLOPE_KEY]), float(self.v[ARM_XREF_KEY])

    def glue(self, p: Mapping[str, float], st: Mapping[str, object]) -> dict[str, object]:
        v, rebco = self.v, self.material == "rebco"
        B = st["B_peak"]
        I_turn = p["magnet_turn_current"]
        turns = p["magnet_reference_turns"]
        n_coils = p["magnet_n_coils"]
        T_supply = p["T_cold_cryo"]  # winding_pack.T_inventory = cryoplant.T_cold_cryo (mfe_plant.sysml:126)
        adapter = material_winding_adapter(dict(
            reference_turns_in=turns, f_set_in=p["magnet_f_set"], c_coil_in=st["c_coil"],
            wp_side_in=st["wp_side"]))
        law_names = (REBCO_LAW + REBCO_BOUNDS) if rebco else (NB3SN_LAW + NB3SN_BOUNDS)
        law = {name: float(v["magnet__" + name]) for name in law_names}
        n_elements = float(v["magnet__n_elements"])
        out: dict[str, object] = {"adapter": adapter}
        if rebco:
            shape = rebco_shape_branch(dict(B_peak_in=B, B_knot_max_in=law["B_knot_max"]))
            out["shape_branch"] = shape
            conductor = r1.rebco_cable_critical_surface(dict(
                law, n_elements=n_elements, turn_current=I_turn, B_peak=B, T_supply=T_supply,
                shape_mode=shape["shape_mode"]))
        else:
            conductor = r1.nb3sn_cable_critical_surface(dict(
                law, n_elements=n_elements, turn_current=I_turn, B_peak=B, T_supply=T_supply,
                eps_intrinsic=float(v[EPS_KEY])))
        construction = {name: float(v["magnet__" + name]) for name in CONSTRUCTION}
        area = r1.winding_turn_area_screen(dict(
            construction, turn_current=I_turn, B_peak=B, available_area=adapter["pack_area_per_turn"],
            element_area=conductor["element_area_total"],
            element_copper_area=conductor["element_copper_area"]))
        inventory = r1.winding_inventory_and_cost(dict(
            n_elements=n_elements, element_area=conductor["element_area_total"],
            element_density=float(v["magnet__element_density"]), turns=turns, coils=n_coils,
            turn_length=adapter["turn_length"], turn_current=I_turn,
            cu_space=construction["cu_space"], cu_void=construction["cu_void"],
            steel_area=construction["steel_area"], solder_area=construction["solder_area"],
            rho_cu=p["magnet_rho_copper"], rho_steel=p["magnet_rho_steel"],
            rho_solder=p["magnet_rho_solder"], price_cu=p["magnet_price_copper"],
            price_steel=p["magnet_price_steel"], price_solder=p["magnet_price_solder"],
            element_price_per_m=float(v["magnet__element_price_per_m"]), manufacturing_per_m=0.0))
        pack = pack_field_checks(dict(B_peak_in=B, I_coil_in=st["I_coil"], R_in=p["R"],
                                      wp_side_in=st["wp_side"], mu0_in=float(v[MU0_KEY])))
        winding_sum = material_winding_cost(dict(
            superconductor_cost_in=inventory["sc_cost"], materials_cost_in=inventory["materials_cost"],
            helium_cost_in=st["material_inventory"]["cost_helium"],
            winding_operations_cost_in=st["procurement"]["winding_fabrication_cost"]))
        cryo = {name: float(v["cryoplant__" + name]) for name in STAGED_CRYO}
        static = staged_static_loads(dict(
            n_coils_in=n_coils, c_coil_in=st["c_coil"], wp_side_in=st["wp_side"],
            t_case_in=p["cryo_t_case"], shield_area_ratio_in=p["cryo_shield_area_ratio"],
            eps_eff_in=p["cryo_emittance"], sigma_SB_in=p["cryo_sigma_SB"], q_MLI_in=p["cryo_q_mli"],
            g_per_coil_in=p["cryo_g_per_coil"], k_c_in=p["cryo_k_cold"], k_s_in=p["cryo_k_shield"],
            T_cold_in=T_supply, T_shield_in=p["T_shield_cryo"], T_amb_in=p["T_amb_cryo"],
            T_conduction_ref_in=cryo["T_conduction_ref"], p_fixed_MW_in=p["p_fixed_cryo"]))
        cold = r1.magnet_cold_stage_load(dict(
            T_supply=T_supply, T_shield=p["T_shield_cryo"], T_amb=p["T_amb_cryo"], turn_current=I_turn,
            nuclear_density=p["q_nuc_cryo"], cold_volume=st["vol_cold_total"],
            radiation_ref=static["q_radiation"], conduction_ref=static["conduction_ref"],
            T_conduction_ref=cryo["T_conduction_ref"], n_leads=p["cryo_n_leads"],
            f_lead=p["cryo_f_lead"], L0=p["cryo_L0"], p_joint_ref=static["p_joint_ref"],
            I_joint_ref=cryo["I_joint_ref"], shield_static=static["shield_static"],
            load_multiplier=cryo["load_multiplier"]))
        refrigeration = r1.staged_refrigeration_screen(dict(
            q_cold=cold["q_cold"], T_supply=T_supply, q_shield=cold["q_shield"],
            T_shield=p["T_shield_cryo"], T_amb=p["T_amb_cryo"],
            rating_cold=p["capability_cryoplant__rated_cold_W"], eta_mode=cryo["eta_mode"],
            eta_const=cryo["eta_const"], green_a=cryo["green_a"], green_b=cryo["green_b"],
            f_carnot_shield=p["f_carnot_shield"], capital_mode=cryo["capital_mode"],
            green_c=cryo["green_c"], green_d=cryo["green_d"], T_green=cryo["T_green"],
            usd2015_to_2021=cryo["usd2015_to_2021"]))
        capital = refrigeration["refrigerator_capital"]
        if not math.isfinite(capital) or capital < 0.0:
            # 'Supplied Auxiliary Cooling Cost' native domain (mfe_account_costs.sysml:33-40).
            raise ValueError("glue Staged Cryoplant: refrigerator capital must be finite and nonnegative")
        drive = staged_drive_power(dict(
            q_leads_in=cold["q_leads"], q_shield_in=cold["q_shield"],
            shield_static_in=static["shield_static"], q_joints_in=cold["q_joints"],
            joint_drive_fraction_in=p["cryo_joint_drive_fraction"]))
        available = v.get(INTERCEPT_AVAILABLE_KEY, True)
        if available not in (False, True, 0.0, 1.0):
            raise GlueOracleError(f"{INTERCEPT_AVAILABLE_KEY} must be Boolean")
        out.update(conductor=conductor, area=area, inventory=inventory, pack_field=pack,
                   winding_sum=winding_sum, static_loads=static, cold_stage=cold,
                   refrigeration=refrigeration, staged_drive=drive,
                   # the seam values of design sections 2.3, 2.8, 2.9 and hunk H6
                   winding_cost=winding_sum["cost"], p_elec=refrigeration["p_in_total_MW"],
                   p_drive=drive["p_drive"], cryo_cost=capital, cold_demand_W=cold["q_cold"],
                   intercept_demand_W=cold["q_shield"], intercept_available=bool(available))
        return out


# ---------------------------------------------------------------------------------------------
# The plant chain, re-derived. legs=None reproduces verify_stellaris.compute() bit for bit.
# ---------------------------------------------------------------------------------------------
def _plant_chain(p: dict, legs: _MaterialLegs | None = None) -> tuple[dict, dict | None]:
    """Recompose the plant chain from the plant oracle's function-level pieces.

    Each inline block cites the SysML definition it re-derives; the imported pieces are named.
    With legs=None every value equals verify_stellaris.compute() on the same p (tested bitwise).
    With material legs: B_peak carries the arm; the plant REBCO law is gated off; the rollup reads
    the one-basis winding account; pb.p_cryo reads the staged refrigeration electricity; tf_power
    reads the staged drive; the cryo package price is the Green capital; the cold and intercept
    screens read the staged demands. Dormant plant channels (tape metres, cold chain, inventory)
    are still computed and reported, as the design keeps them (K23).
    """
    for key in ("magnet_R0", "tbr", "I_total"):
        if key in p:
            raise ValueError(f"retired oracle input {key}")
    vs.oracle_procurement.validate(p)  # imported: supplied package amounts and one module
    # 'Winding Operating State' (mfe_magnet_field.sysml:4)
    for key in ("magnet_reference_turns", "magnet_turn_current", "magnet_wp_side"):
        if isinstance(p[key], bool) or not math.isfinite(p[key]) or p[key] <= 0:
            raise ValueError("oracle Winding Operating State: invalid " + key)
    I_coil = p["magnet_reference_turns"] * p["magnet_turn_current"]
    area = p["magnet_wp_side"] * p["magnet_wp_side"]
    area_mm2 = area * 1e6
    if any(not math.isfinite(v) or v <= 0 for v in (I_coil, area, area_mm2)):
        raise ValueError("oracle Winding Operating State: invalid current/area arithmetic")
    effective_density = I_coil / area_mm2
    if not math.isfinite(effective_density) or effective_density <= 0:
        raise ValueError("oracle Winding Operating State: invalid density arithmetic")
    for mode in ("cooling_cost_mode", "cooling_energy_mode"):
        if not math.isfinite(p[mode]) or p[mode] not in (0., 1.):
            raise ValueError("oracle cooling modes must be finite binary selectors")
    if (p["cooling_cost_mode"] or p["cooling_energy_mode"]) and not p["cooling_enabled"]:
        raise ValueError("oracle selected cooling effects require enabled equipment")
    if p["facility_facilities_enabled"] and not p["cooling_enabled"]:
        raise ValueError("oracle active facilities require enabled cooling equipment")
    # 'Plasma Geometry' (mfe_plasma_scaling.sysml:4)
    V = 2.0 * (p["pi"] ** 2) * p["R"] * (p["a"] ** 2) * p["kappa"] * p["f_shape"]
    # 'MFE Radial Build' (mfe_plasma_scaling.sysml:52)
    vacuum_or = p["a"] + p["vacuum_t"]
    firstwall_or = vacuum_or + p["firstwall_t"]
    blanket_or = firstwall_or + p["blanket_t"]
    reflector_or = blanket_or + p["reflector_t"]
    ht_shield_or = reflector_or + p["ht_shield_t"]
    structure_or = ht_shield_or + p["structure_t"]
    gap1_or = structure_or + p["gap1_t"]
    vessel_or = gap1_or + p["vessel_t"]
    coil_or = vessel_or + p["coil_t"]
    gap2_or = coil_or + p["gap2_t"]
    lt_shield_or = gap2_or + p["lt_shield_t"]
    C = p["kappa"] * 2.0 * (p["pi"] ** 2) * p["R"]
    firstwall_vol = C * ((firstwall_or ** 2) - (vacuum_or ** 2))
    blanket_layer_vol = C * ((blanket_or ** 2) - (firstwall_or ** 2))
    reflector_vol = C * ((reflector_or ** 2) - (blanket_or ** 2))
    ht_shield_vol = C * ((ht_shield_or ** 2) - (reflector_or ** 2))
    lt_shield_vol = C * ((lt_shield_or ** 2) - (gap2_or ** 2))
    blanket_vol = firstwall_vol + blanket_layer_vol + reflector_vol
    shield_vol = ht_shield_vol + lt_shield_vol
    structure_vol = C * ((structure_or ** 2) - (ht_shield_or ** 2))
    vessel_vol = C * ((vessel_or ** 2) - (gap1_or ** 2))
    wall_area = p["kappa"] * 4.0 * (p["pi"] ** 2) * p["R"] * vacuum_or
    r_coil = vessel_or
    r_coil_centre = vessel_or + p["coil_t"] / 2.0
    A = p["R"] / p["a"]
    # CAS27 special materials (stellarator_plant.sysml:1968)
    special_materials_capital = blanket_vol * 0.50 * 9400.0 * 5.0
    # 'Coil Set Axis Field' (mfe_magnet_field.sysml:16)
    B_axis = (p["mu0"] * p["magnet_k_link"] * p["magnet_n_coils"] * I_coil
              / (p["magnet_two_pi"] * p["R"]))
    # 'Conductor Peak Field' with the pack-arm slot (mfe_plasma_scaling.sysml:420; design 2.2)
    arm_slope, arm_x_ref = (0.0, 0.0) if legs is None else legs.arm()
    peak = conductor_peak_field(dict(
        B_axis_in=B_axis, peak_ratio_in=p["magnet_peak_ratio"], R_in=p["R"], a_coil_in=r_coil_centre,
        R_ref_in=p["magnet_R_ref"], a_coil_ref_in=p["magnet_a_coil_ref"], wp_side_in=p["magnet_wp_side"],
        arm_slope_in=arm_slope, arm_x_ref_in=arm_x_ref))
    B_peak = peak["B_peak"]
    # 'Coil Set Stored Energy' (mfe_magnet_field.sysml:310)
    W_mag = (p["magnet_W_mag_ref"] * (I_coil / p["magnet_I_ref"]) ** 2
             * (r_coil_centre / p["magnet_a_coil_ref"]) ** 2 * (p["magnet_R_ref"] / p["R"]))
    m_casing = p["magnet_m_casing"]
    support_mass = p["magnet_support_mass"]
    for key in ("magnet_m_casing", "magnet_support_mass", "cryo_q_nuc_structure"):
        if not math.isfinite(p[key]) or p[key] < 0:
            raise ValueError("oracle coil support: nonnegative finite mass/heating required")
    if not math.isfinite(p["cryo_rho_structure"]) or p["cryo_rho_structure"] <= 0:
        raise ValueError("oracle coil support: positive finite structure density required")
    for key in ("magnet_legacy_casing_fraction", "structure_residual_fraction", "cryo_joint_drive_fraction"):
        if not math.isfinite(p[key]) or not 0 <= p[key] <= 1:
            raise ValueError("oracle coil support: accounting fractions must lie in [0,1]")
    wp_side = p["magnet_wp_side"]
    # 'Coil Winding Length' (mfe_magnet_field.sysml:154)
    c_coil = p["magnet_c_coil_ref"] * (r_coil_centre / p["magnet_a_coil_ref"])
    if wp_side == 0.0:
        raise ValueError("oracle Winding Pack Stress: wp_side must be nonzero")
    # 'Winding Pack Stress' (mfe_magnet_field.sysml:60) and 'Conductor Strain' (:263): read B_peak
    sigma_wp = p["magnet_k_sigma"] * I_coil * B_peak / wp_side
    eps_cond = p["magnet_f_cond"] * sigma_wp / p["magnet_E_wp"]
    # 'Winding Pack Cold Volume' (mfe_magnet_field.sysml:218)
    vol_cold_total = (p["magnet_f_wp_vol"] * p["magnet_n_coils"] * wp_side * wp_side
                      * c_coil + p["vol_cold_cryo"])
    vol_winding_pack = p["magnet_f_wp_vol"] * p["magnet_n_coils"] * wp_side * wp_side * c_coil
    if not 0.0 < p["T_cold_cryo"] < p["T_amb_cryo"]:
        raise ValueError("oracle cryoplant: require 0 < T_cold < T_amb")
    inventory = vs._winding_material_inventory(p, vol_winding_pack)  # imported
    tape_volume_direct = (wp_side ** 2 * p["magnet_n_coils"] * p["magnet_f_wp_vol"] * c_coil
                          * (1 - sum(p["magnet_f_" + m] for m in ("copper", "solder", "steel", "helium"))))
    if not math.isclose(tape_volume_direct, inventory["tape_volume"], rel_tol=1e-12):
        raise ValueError("oracle expanded tape volume disagrees with inventory")
    procurement = vs._winding_procurement(p, c_coil, inventory["material_cost"], inventory["tape_volume"])
    insulation = vs._insulation_inventory(p, c_coil, wp_side, vol_winding_pack)
    if legs is None:
        conductor = vs._conductor_current(p, B_peak, procurement["tape_length"],
                                          procurement["conductor_length"])
        glue = None
    else:
        conductor = gated_rebco_conductor_current(p, B_peak, procurement["tape_length"],
                                                  procurement["conductor_length"], enabled=0.0)
        glue = legs.glue(p, dict(B_peak=B_peak, c_coil=c_coil, wp_side=wp_side, I_coil=I_coil,
                                 vol_cold_total=vol_cold_total, material_inventory=inventory,
                                 procurement=procurement))
    sust = vs._sustainment(p, V, B_axis)  # imported
    # 'DT Fusion Power' (mfe_plasma_scaling.sysml:148)
    if p["sigma_v"] > 0.0:
        p_fus = 0.25 * (p["n_e"] ** 2) * p["sigma_v"] * p["E_fus"] * V * 1.0e-6
    else:
        integral = vs._profile_integral(p["alpha_n"], p["alpha_T"], p["T_i0"])
        p_fus = sust["n_D0"] * sust["n_T0"] * integral * p["E_fus"] * V * 1.0e-6
    # 'MFE Power Balance Calc' front terms (mfe_power_balance.sysml:4)
    p_alpha = (3.52 / 17.58) * p_fus
    p_neutron = p_fus - p_alpha
    p_cool = p["p_tfcool"] + p["p_pfcool"]
    p_aux = p["p_trit"] + p["p_house"]
    thermal = vs._coil_thermal_inventory(p, c_coil, wp_side)  # imported (zeros when disabled)
    # 'Power Supplies' tf_power = p_tf + p_tf_extra; p_tf_extra reads the cryoplant.p_drive seam
    # (mfe_plant.sysml:192; design 2.3 and 2.8)
    p_tf_total = p["p_tf"] + (thermal["p_drive"] if glue is None else glue["p_drive"])
    p_coils = p_tf_total + p["p_pf"]
    # 'Heating Power Chain' and 'Operating Heating Power' (mfe_heating_chain.sysml:4, :79)
    heat_eta_pin_eff = p["eta_source_heat"] * p["eta_couple_heat"]
    heat_delivered = (p["p_wallplug_heat"] * p["eta_source_heat"] + p["p_delivered_direct_heat"])
    heat_coupled = (p["p_wallplug_heat"] * p["eta_source_heat"] * p["eta_couple_heat"]
                    + p["p_coupled_direct_heat"])
    heat_wallplug_total = (p["p_wallplug_heat"] + p["p_coupled_direct_heat"] / heat_eta_pin_eff)
    operating_heat_coupled = sust["p_aux_required"]
    operating_heat_delivered = operating_heat_coupled / p["eta_couple_heat"]
    operating_heat_wallplug = operating_heat_delivered / p["eta_source_heat"]
    # 'Reactor Source Heat' (mfe_power_balance.sysml:174), 'Primary Coolant Loop'
    # (mfe_primary_loop.sysml:4), 'Power Cycle Efficiency' (mfe_power_cycle.sysml:4)
    q_source = p["mn"] * p_neutron + p_alpha + operating_heat_coupled
    loop_mdot = vs._primary_loop_mass_flow(q_source, p["loop_cp"], p["loop_dT_blanket"])
    loop_T_out = p["loop_T_in"] + p["loop_dT_blanket"]
    loop_mdot_loop = loop_mdot / p["n_loops"]
    loop_dp_loop = p["f_loss"] * p["dp_loop_ref"] * (loop_mdot_loop / p["mdot_loop_ref"]) ** 2
    loop_p_loop_margin = p["loop_p"] - loop_dp_loop
    if loop_p_loop_margin <= 0.0:
        raise RuntimeError("oracle loop: pressure domain -- the per-path loss exceeds the loop pressure (p_loop_margin <= 0)")
    loop_r_comp = p["loop_p"] / (p["loop_p"] - loop_dp_loop)
    loop_k_isen = (p["loop_gamma"] - 1.0) / p["loop_gamma"]
    loop_T_comp_in = p["loop_T_in"] / (1.0 + (loop_r_comp ** loop_k_isen - 1.0) / p["eta_is"])
    loop_w_fluid = loop_mdot * p["loop_cp"] * (p["loop_T_in"] - loop_T_comp_in) / 1.0e6
    loop_p_elec = loop_w_fluid / p["eta_drive"]
    loop_q_ihx = q_source + loop_w_fluid
    loop_capacity_margin = p["mdot_loop_rated"] - loop_mdot_loop
    loop_p_pump_total = p["loop_live"] * loop_p_elec + p["p_pump_direct"]
    loop_q_recovered_total = (p["loop_live"] * loop_w_fluid + p["eta_p_direct"] * p["p_pump_direct"])
    cycle_T2_C = loop_T_out - p["dT_approach"] - 273.15
    cycle_eta_fit = (p["a_fit"] * math.log(cycle_T2_C + p["T_offset_fit"]) - p["b_fit"] - p["delta_eta"])
    cycle_eta_th = p["cycle_live"] * cycle_eta_fit + p["eta_th_direct"]
    cooling = vs.cooling_oracle.calculate({  # imported
        **{key: p["cooling_" + key] for key in [
            "helium_design_shaft_MW", "helium_design_suction_Pa", "salt_design_flow_kg_s",
            "salt_design_head_m", "salt_design_eta_p", "salt_design_eta_motor",
            "helium_purchased_mass_kg", "salt_purchased_mass_kg"]},
        "enabled": p["cooling_enabled"], "layout_multiplier": p["cooling_layout_multiplier"],
        "tube_wall": p["cooling_tube_wall"], "shell_wall": p["cooling_shell_wall"],
        "accessory_mass": p["cooling_accessory_mass"], "secondary_head": p["cooling_secondary_head"],
        "eta_p": p["cooling_eta_p"], "eta_motor": p["cooling_eta_motor"],
        "machine_life": p["cooling_machine_life"], "bundle_life": p["cooling_bundle_life"],
        "makeup_fraction": p["cooling_makeup_fraction"], "inventory_reserve": p["cooling_inventory_reserve"],
        "removal_multiplier": p["cooling_removal_multiplier"],
        "saltprice_source_choice": p["cooling_saltprice_source_choice"],
        "costscale": p["cooling_costscale"], "fabrication_rate_2017": p["cooling_fabrication_rate_2017"],
        "n_mod": p["n_mod"], "n_loops": p["n_loops"], "mdot_loop": loop_mdot_loop, "dp_loop": loop_dp_loop,
        "helium_suction_K": loop_T_comp_in, "helium_discharge_Pa": p["loop_p"],
        "helium_hot_K": loop_T_out, "helium_cp": p["loop_cp"], "helium_gamma": p["loop_gamma"],
        "primary_shaft_MW": loop_w_fluid, "primary_electric_MW": loop_p_elec, "q_ihx_MW": loop_q_ihx,
        "years": p["operational_years"], "discount": p["discount_rate"], "sourcefitargument_C": cycle_T2_C,
    })
    cooling.update(hx_shell_bore=3.2 if p["cooling_enabled"] else 0.,
                   hx_shell_wall=p["cooling_shell_wall"] if p["cooling_enabled"] else 0.,
                   hx_shell_length=13. if p["cooling_enabled"] else 0.,
                   hx_tube_length=11.6 if p["cooling_enabled"] else 0.)
    # 'Cooling Energy Addition' (mfe_cooling_accounts.sysml:42)
    cooling_electric_total = loop_p_pump_total + p["cooling_energy_mode"] * cooling["salt_electric_MW"]
    cooling_recovered_total = loop_q_recovered_total + p["cooling_energy_mode"] * cooling["salt_shaft_MW"]
    cycle_margin_low = cycle_T2_C - p["T2_min"]
    cycle_margin_high = p["T2_max"] - cycle_T2_C
    cycle_domain_product = cycle_margin_low * cycle_margin_high
    matched_cycle = vs.matched_cycle_oracle.matched_interface({  # imported
        "enabled": p["matched_cycle_enabled"], "heat_available_MW": cooling["conversion_heat_MW"],
        "source_heat_MW": q_source, "selected_recovered_MW": cooling_recovered_total,
        "salt_flow_per_circuit": cooling["salt_flow"], "salt_circuit_count": cooling["ihx_count"],
        "salt_return_C": cooling["salt_return_C"],
        **{name: p["matched_" + name] for name in (
            "salt_hot_C", "salt_cp_kJ_kgK", "main_pressure_MPa", "extraction_pressure_MPa",
            "steam_temperature_C", "reheat_temperature_C", "condenser_temperature_C",
            "eta_hp", "eta_lp", "eta_condensate_pump", "eta_feedwater_pump",
            "eta_pump_motor", "eta_mechanical", "eta_generator")},
    })
    cooling_water = vs.matched_cycle_oracle.cooling_interface({  # imported
        "enabled": p["cooling_water_enabled"], "cycle_active": p["matched_cycle_enabled"],
        "q_rejection_before_cooling_MW": matched_cycle["q_rejection_before_cooling_MW"],
        "condenser_temperature_C": p["matched_condenser_temperature_C"],
        **{name: p["cw_" + name] for name in ("water_inlet_C", "water_outlet_C", "head_m", "eta_pump", "eta_motor")},
    })
    cycle_selection = vs.matched_cycle_oracle.selection_interface({  # imported
        "matched_enabled": p["matched_cycle_enabled"], "legacy_eta": cycle_eta_th,
        "matched_eta": matched_cycle["eta_gross"], "legacy_domain_product": cycle_domain_product,
    })
    # 'MFE Power Balance Calc' thermal and electric terms (mfe_power_balance.sysml:4-150)
    p_th = (p["mn"] * p_neutron + p_alpha + operating_heat_coupled + cooling_recovered_total)
    p_the = cycle_selection["eta_selected"] * p_th
    p_et = p_the
    p_sub = p["f_sub"] * p_et
    # Dormant plant cold chain: 'Cryoplant Electrical Power' (mfe_cryo_plant.sysml:4),
    # 'Cold Load Sum' (mfe_cryo_inventory.sysml:62), 'Intercept Electrical Power' (:89),
    # 'Electrical Power Sum' (:81). In material instances it reaches no priced or checked channel.
    cop_carnot = (p["T_cold_cryo"] / (p["T_amb_cryo"] - p["T_cold_cryo"]))
    cop = (p["f_carnot_cryo"] * cop_carnot)
    structure_nuclear = p["cryo_q_nuc_structure"] * support_mass / p["cryo_rho_structure"] * 1e-6
    p_cold = ((p["q_nuc_cryo"] * vol_cold_total * 1e-6 + p["p_fixed_cryo"] + structure_nuclear)
              * p["f_uplift_cryo"] + thermal["q_cold"] * 1e-6)
    p_cryo_cold = p_cold / cop + p["p_cryo_direct"]
    p_cryo_shield = (thermal["q_shield"] * 1e-6 * (p["T_amb_cryo"] - p["T_shield_cryo"])
                     / (p["f_carnot_shield"] * p["T_shield_cryo"])) if p["cryo_inventory_enabled"] else 0.0
    p_cryo = p_cryo_cold + p_cryo_shield
    # pb.p_cryo reads the cryoplant.p_elec seam (mfe_plant.sysml:395; design 2.8)
    pb_p_cryo = p_cryo if glue is None else glue["p_elec"]
    # recirculating, q_eng, rec_frac, p_net (mfe_power_balance.sysml:159-172)
    recirculating = (p_coils + cooling_electric_total + p_sub + p_aux + p_cool + pb_p_cryo
                     + operating_heat_wallplug)
    if matched_cycle["p_cycle_pumps_MW"] != 0 or cooling_water["p_cooling_pump_electric_MW"] != 0:
        recirculating += matched_cycle["p_cycle_pumps_MW"] + cooling_water["p_cooling_pump_electric_MW"]
    q_eng = p_et / recirculating
    rec_frac = 1.0 / q_eng
    p_net = (1.0 - rec_frac) * p_et
    # 'Magnet Coil Cost' comparison channel (mfe_magnet_cost.sysml:4)
    total_kAm = (p["magnet_G"] * B_axis * p["R"] * r_coil / (p["mu0"] * 1000.0))
    magnet = total_kAm * p["magnet_cost_per_kAm"] * p["magnet_coil_markup"]
    # 'Winding Pack Cost' legacy channel (mfe_magnet_cost.sysml:56)
    kAm_wind = p["magnet_n_coils"] * I_coil * p["magnet_f_set"] * c_coil / 1000.0
    winding_pack_legacy = kAm_wind * p["magnet_cost_per_kAm"] * p["magnet_f_wp_fab"]
    winding_pack = procurement["cost"]  # the plant procurement account (dormant in material instances)
    # 'Magnet Structure Cost' (mfe_magnet_cost.sysml:157, :178)
    magnet_structure = ((p["magnet_legacy_casing_fraction"] * p["magnet_n_coils"] * m_casing + support_mass)
                        * p["magnet_steel_price"] * p["magnet_f_steel_fab"])
    support_effective_all_in_rate = p["magnet_steel_price"] * p["magnet_f_steel_fab"]
    for name in ("magnet_steel_price", "magnet_f_steel_fab"):
        if not math.isfinite(p[name]) or p[name] < 0:
            raise ValueError("oracle support rate: invalid " + name)
    if not math.isfinite(support_effective_all_in_rate):
        raise ValueError("oracle support rate: nonfinite product")
    # 'Magnet Capital' (mfe_magnet_cost.sysml:203); winding_cost seam (mfe_power_core.sysml:129, :361;
    # design 2.9, H6): the rollup reads the one-basis winding account in material instances.
    rollup_winding_cost = winding_pack if glue is None else glue["winding_cost"]
    magnet_capital_rollup = rollup_winding_cost + magnet_structure + insulation["stock_cost"]
    # radial-build accounts: 'Blanket Cost' (mfe_account_costs.sysml:72), 'Shield Cost' (:102),
    # 'Structure Cost' (:131), 'Vessel Cost' (:164); supplied packages 'Supplied Purchase Cost'
    # (:17); 'Heating Cost' (:252); 'Linear Power Cost' (:282)
    blanket = (p["blanket_unit_cost"] * p["blanket_structure_factor"] * blanket_vol
               * (p["selected_blanket_cost_thermal_class_MW"] / p["p_th_ref"]) ** p["alpha_06"])
    shield = (p["shield_unit_cost"] * shield_vol * p["shield_scale"]
              * (p["selected_shield_cost_thermal_class_MW"] / p["p_th_ref"]) ** p["alpha_06"])
    structure_legacy_cost = (p["structure_unit_cost"] * structure_vol
                             * (p["selected_structure_cost_gross_class_MWe"] / p["p_et_ref"]) ** p["alpha_05"])
    structure = p["structure_residual_fraction"] * structure_legacy_cost
    vessel = (p["vessel_unit_cost"] * vessel_vol
              * (p["selected_vessel_cost_gross_class_MWe"] / p["p_et_ref"]) ** p["alpha_06"])
    power_supplies = p["selected_power_supplies_purchase_cost_per_module"]
    divertor = p["selected_divertor_purchase_cost_per_module"]
    heating = p["heating_ecrh_per_mw"] * heat_delivered
    turbine = p["n_mod"] * p["selected_turbine_purchase_cost_per_module"]
    electric = p["n_mod"] * p["selected_electric_plant_installed_gross_rating_MWe"] * p["electric_per_mw"]
    heat_rejection = p["n_mod"] * p["selected_heat_rejection_purchase_cost_per_module"]
    misc = p["n_mod"] * p["selected_misc_plant_cost_gross_class_MWe"] * p["misc_per_mw"]
    # 'Neutron Wall Load' (mfe_plasma_scaling.sysml:237), calibration (:273), peak (:342)
    wall_load = p_fus * (1.0 - 0.2002) / wall_area
    A_ref = (p["wall_peak_kappa_ref"] * 4.0 * (p["pi"] ** 2) * p["wall_peak_R_ref"]
             * (p["wall_peak_a_ref"] + p["wall_peak_standoff_ref"]))
    p_n_ref = p["wall_peak_p_fus_ref"] * (1.0 - 0.2002)
    wall_peak_calibration = (p["wall_peak_q_ref"] * A_ref / p_n_ref + p["wall_peak_calibration_direct"])
    wall_load_peak = wall_load * wall_peak_calibration
    replacement_cost_per_event = (blanket + divertor) * p["n_mod"]
    cal = vs._oracle_lifecycle_calendar(  # imported
        cost_per_event=replacement_cost_per_event, q_n=wall_load_peak,
        fluence_limit=p["fluence_limit"], interest_rate=p["discount_rate"],
        operational_years=p["operational_years"], outage_years=p["outage_years"],
        unplanned_fraction=p["unplanned_fraction"], coil_life_fpy=p["coil_life_fpy"],
        availability_direct=p["availability_direct"])
    # 'Buildings Cost' (mfe_account_costs.sysml:360), 'Preconstruction Cost' (:422) legacy operands
    buildings = (((((p["bldg_fixed_base"]
        + (p["bldg_fus_base"] * ((p["selected_buildings_legacy_cost_fusion_class_MW"] * p["n_mod"]) / p["bldg_p_fus_ref"])))
        + (p["bldg_staff_base"] * (((p["selected_buildings_legacy_cost_gross_class_MWe"] * p["n_mod"]) / p["p_et_ref"]) ** 0.5)))
        + (p["bldg_the_base"] * ((p["selected_buildings_legacy_cost_thermal_electric_class_MWe"] * p["n_mod"]) / p["p_et_ref"])))
        + (p["bldg_th_base"] * ((p["selected_buildings_legacy_cost_thermal_class_MW"] * p["n_mod"]) / p["p_th_ref"])))
        + (p["bldg_et_base"] * ((p["selected_buildings_legacy_cost_gross_class_MWe"] * p["n_mod"]) / p["p_et_ref"])))
    precon = (((p["land_intensity"] * (((p["selected_precon_legacy_cost_net_class_MWe"] * p["n_mod"]) * p["ref_net_power"]) ** 0.5))
               * p["land_cost"]) + p["precon_fixed_base"])
    facilities = vs.facilities_oracle.layout(  # imported
        {key: p["facility_" + key] for key in vs.facilities_oracle.DEFAULTS},
        dict(n_mod=p["n_mod"], major_radius=p["R"], minor_outer_radius=lt_shield_or,
             blanket_volume=blanket_vol, calendar_mode=p["availability_direct"],
             calendar_years=p["operational_years"], calendar_outage=p["outage_years"],
             cooling_helium_count=cooling["circulator_count"], cooling_salt_count=cooling["salt_pump_count"],
             cooling_bundle_count=cooling["ihx_count"], cooling_circuits=cooling["ihx_count"],
             cooling_machine_life=p["cooling_machine_life"], cooling_bundle_life=p["cooling_bundle_life"],
             hx_tube_length=11.6, hx_shell_bore=3.2, hx_shell_wall=p["cooling_shell_wall"], hx_shell_length=13.),
        cal["events"])
    buildings_legacy, precon_legacy = buildings, precon
    # 'Facility Account Selection' (mfe_facilities.sysml:746), 'Facility Preconstruction Selection' (:769)
    facility_mode = p["facility_facilities_cost_mode"]
    buildings = (1 - facility_mode) * buildings_legacy + facility_mode * facilities["layout_buildings_capital"]
    precon = (1 - facility_mode) * precon_legacy + facility_mode * (p["precon_fixed_base"] + facilities["layout_land_cost"])
    facility_exclusion = facility_mode * (1 + p["contingency_rate"]) * facilities["installed_facility_capital"]
    # 'Annual OM Cost' (mfe_account_costs.sysml:459)
    annual_om_unlevelized = ((p["om_annual_ref"] * (((p["selected_om_staffing_net_class_MWe"] * p["n_mod"]) / p["ref_net_power"]) ** p["om_alpha"]))
                             + p["om_direct"])
    # powercore and BOP rollups (mfe_plant.sysml:461-464, :467-469)
    powercore_capital = (magnet_capital_rollup + heating + divertor + blanket + shield
                         + structure + vessel + power_supplies)
    bop_capital = turbine + electric + heat_rejection + misc
    breeding = vs.breeding_oracle.response(p)  # imported
    inventory_parameters = {key: p["inventory_" + key] for key in vs.inventory_oracle.DEFAULTS}
    inventory_parameters["enabled"] = inventory_parameters.pop("inventory_enabled")
    inventory_parameters.update(
        p_fus=p_fus, q_eff=p["fuel_q_eff"], mev_to_joules=p["mev_to_joules"],
        burn_fraction=p["burn_fraction"], t_recycle=p["t_recycle"],
        tbr_available=breeding["tbr_mean"], breeding_defined=breeding["defined_flag"],
        eta_extract=p["eta_extract"], lambda_T=p["lambda_T"], G_stock=p["G_stock"],
        m_T_kg=p["m_T_kg"], plasma_volume=V, n_T0=sust["n_T0"],
        alpha_n=p["alpha_n"], availability=cal["availability"])
    fuel_inventory = vs.inventory_oracle.evaluate(**inventory_parameters)  # imported
    n = p["n_mod"]
    # CAS22 tail: 'Remote Handling Cost' (mfe_account_costs.sysml:534), 'Installation Labor Cost'
    # (:561), 'Coolant Cost' (:584) with 'Cooling Account Selection' (mfe_cooling_accounts.sysml:19),
    # 'Supplied Auxiliary Cooling Cost' (mfe_account_costs.sysml:33), 'Plant Power-Law Cost' (:507)
    remote_handling = (p["remote_handling_base"] * p["concept_scale"]
                       * (p["selected_remote_handling_cost_gross_class_MWe"] / p["rh_p_et_ref"]) ** p["rh_alpha"])
    reactor_equipment_subtotal = powercore_capital + remote_handling
    installation = p["installation_frac"] * reactor_equipment_subtotal
    coolant = (p["coolant_primary_base"] * (n * p["selected_heat_transport_legacy_cost_net_class_MWe"] / p["coolant_ref_net"])
               + p["coolant_intermediate_base"] * (n * p["selected_heat_transport_legacy_cost_thermal_class_MW"] / p["coolant_p_th_ref"]) ** p["coolant_alpha"])
    aux_cost = p["aux_per_mw"] * (n * p["selected_cryoplant_aux_cost_thermal_class_MW"])
    # cryo package amount: supplied (reference) or the Green capital at the supplied rating
    # (design 2.7, purchase_cost_per_module = refrigeration.refrigerator_capital)
    cryo_cost = p["selected_cryoplant_purchase_cost_per_module"] if glue is None else glue["cryo_cost"]
    coolant_legacy = coolant
    coolant = (1 - p["cooling_cost_mode"]) * coolant_legacy + p["cooling_cost_mode"] * cooling["installed_total"]
    aux_cooling = aux_cost + cryo_cost
    waste = p["waste_base"] * (n * p["selected_waste_cost_thermal_class_MW"] / p["waste_ref"]) ** p["waste_alpha"]
    fuel_handling_legacy = p["fuel_handling_base"] * (n * p["selected_fuel_cycle_legacy_cost_net_class_MWe"] / p["fuel_ref"]) ** p["fuel_alpha"]
    processing = vs.processing_oracle.calculate(  # imported
        {key: p["processing_" + key] for key in vs.PROCESSING_DEFAULTS} | dict(
            flow=fuel_inventory["dt_processor_kg_s"], inventory_enabled=p["inventory_inventory_enabled"],
            n_mod=n, legacy_cost=fuel_handling_legacy))
    fuel_handling = processing["cost"]
    processing_exclusion = (1 + p["contingency_rate"]) * processing["installation_total"]
    other_rpe = p["other_rpe_base"] * (n * p["selected_other_rpe_cost_net_class_MWe"] / p["other_ref"]) ** p["other_alpha"]
    inc = p["inc_base"] * (n * p["selected_inc_cost_thermal_class_MW"] / p["inc_ref"]) ** p["inc_alpha"]
    # cas22 (mfe_plant.sysml:561-564)
    cas22_tail_capital = (remote_handling + installation + coolant + aux_cooling
                          + waste + fuel_handling + other_rpe + inc)
    cas22_capital = powercore_capital + cas22_tail_capital
    cas28_capital = p["cas28_capital"]
    # cas2x (mfe_plant.sysml:572-574), 'Contingency Cost' (mfe_account_costs.sysml:311), cas20
    # (mfe_plant.sysml:586), 'Indirect Cost' (mfe_account_costs.sysml:332), cas23_to_28 (:602-603)
    cas2x_pre_contingency = (buildings + cas22_capital + bop_capital + special_materials_capital + cas28_capital)
    contingency_capital = p["contingency_rate"] * cas2x_pre_contingency
    cas20_capital = cas2x_pre_contingency + contingency_capital
    cas30_capital = (p["indirect_fraction"] * cas20_capital
                     * (p["construction_years"] / p["reference_construction_time"]))
    cas23_to_28_capital = bop_capital + special_materials_capital + cas28_capital
    # owner ('Plant Power-Law Cost', mfe_plant.sysml:613) and 'Supplementary Cost'
    # (mfe_account_costs.sysml:651) with 'Facility Shipping Scope' (mfe_facilities.sysml:690)
    owner = p["owner_base"] * (n * p["selected_owner_cost_net_class_MWe"] / p["owner_ref"]) ** p["owner_alpha"]
    supplementary = ((p["supp_shipping_frac"] * (cas20_capital - p["cooling_cost_mode"] * cooling["delivered_total"] - facility_exclusion - processing_exclusion)
                      + p["supp_spares_frac"] * cas23_to_28_capital
                      + p["supp_tax_frac"] * cas20_capital
                      + p["supp_insurance_frac"] * (cas20_capital + cas30_capital)
                      + p["supp_startup_base"] * (n * p["selected_startup_cost_net_class_MWe"] / p["ref_net_power"])
                      + p["supp_decom_base"] * (n * p["selected_decom_cost_net_class_MWe"] / p["ref_net_power"]))
                     * (1.0 + p["supp_contingency_rate"]))
    # overnight (mfe_plant.sysml:669-671), 'IDC Closed-Form Cost' (mfe_account_costs.sysml:712),
    # total_capital = overnight (Option C, mfe_plant.sysml:688-690)
    overnight_capital = (precon + cas20_capital + cas30_capital + owner + supplementary)
    f_idc = vs.finance.idc_factor(p["discount_rate"], p["construction_years"])  # imported
    idc_capital = f_idc * overnight_capital
    total_capital = overnight_capital
    indirect_capital = cas30_capital
    # 'Levelized Annual Cost' (mfe_account_costs.sysml:747) for CAS71/CAS80, 'Cooling Annual
    # Addition' (mfe_cooling_accounts.sysml:57), 'DT Fuel Cost' (mfe_account_costs.sysml:804),
    # 'Annual Cost Rollup' (:879)
    i_rate = p["discount_rate"]
    n_life = p["operational_years"]
    g_infl = p["inflation_rate"]
    t_c = p["construction_years"]

    def _levelized_annual_cost(annual_cost):
        return vs.finance.annuity(annual_cost, i_rate, g_infl, n_life, t_c)  # imported

    cooling_om_total = annual_om_unlevelized + p["cooling_cost_mode"] * cooling["consumables_annual"]
    cas71_annual = _levelized_annual_cost(cooling_om_total)
    availability = cal["availability"]
    cas72_annual = cal["cas72_annual"] + p["cooling_cost_mode"] * cooling["replacement_annual"]
    annual_fuel_raw = (n * p_fus * (3600.0 * 8760.0) * 1.0e6 * availability
                       * p["fuel_cost_per_rxn"] / (p["fuel_q_eff"] * p["mev_to_joules"]))
    burn_correction = (1.0 + (1.0 - p["burn_fraction"]) / p["burn_fraction"] * (1.0 - p["fuel_recovery"]))
    annual_fuel = annual_fuel_raw * burn_correction
    cas80_annual = _levelized_annual_cost(annual_fuel)
    cas70_annual = cas71_annual + cas72_annual
    annual_om = cas70_annual + cas80_annual
    # 'Fuel Cycle Flows' (mfe_fuel_cycle.sysml:4), 'Vacuum Gas Load' (mfe_vacuum.sysml:4)
    fuel_E_fus_J = p["fuel_q_eff"] * p["mev_to_joules"]
    fuel_burn_rate = p_fus * 1.0e6 / fuel_E_fus_J
    fuel_inject_rate = fuel_burn_rate / p["burn_fraction"]
    fuel_exhaust_rate = fuel_inject_rate - fuel_burn_rate
    fuel_loss_rate = (1.0 - p["t_recycle"]) * fuel_exhaust_rate
    fuel_tbr_required = ((fuel_burn_rate + fuel_loss_rate + p["lambda_T"] * fuel_inventory["total_atoms"] + p["G_stock"])
                         / (p["eta_extract"] * fuel_burn_rate))
    fuel_tbr_margin = breeding["tbr_mean"] - fuel_tbr_required
    breeding_adequacy = vs.breeding_oracle.adequacy(  # imported
        mean=breeding["tbr_mean"], lower=breeding["tbr_lower"], defined=breeding["defined_flag"],
        floor=p["tbr_floor"], required=fuel_tbr_required, burn=fuel_burn_rate,
        loss=fuel_loss_rate, extraction=p["eta_extract"], decay_constant=p["lambda_T"],
        inventory=fuel_inventory["total_atoms"], growth=p["G_stock"], burn_fraction=p["burn_fraction"],
        recycle=p["t_recycle"])
    fuel_burn_kg_per_fpy = fuel_burn_rate * p["m_T_kg"] * p["s_per_fpy"]
    divheat = vs.divertor_account(  # imported
        alpha=sust["p_alpha_heat"], auxiliary=operating_heat_coupled,
        core_radiation=sust["p_rad"], radiation_fraction=p["f_rad_total"],
        capture_fraction=p["target_capture_fraction"], reference_peak=p["q_target_ref"],
        reference_power=p["p_nonrad_ref"], limit=p["q_target_limit"],
        radius=p["R"], reference_radius=p["R_ref_divertor"],
        auxiliary_required=sust["p_aux_required"], installed=heat_coupled)
    vacuum_n_molecules = (fuel_exhaust_rate + fuel_exhaust_rate) / 2.0 + fuel_burn_rate
    vacuum_Q_total = vacuum_n_molecules * p["k_B"] * p["T_gas"]
    vacuum_S_eff_required = vacuum_Q_total / p["p_exhaust"]
    # 'LCOE DCF' (mfe_lcoe_dcf.sysml:12-17; bound at mfe_plant.sysml:799-807)
    d = p["discount_rate"]
    N = p["operational_years"]
    crf = vs.finance.crf(d, N)
    idc_factor = vs.finance.growth(d, p["construction_years"] / 2.0)
    annual_capital = total_capital * idc_factor * crf
    annual_energy_mwh = 8760.0 * p_net * availability
    lcoe = (annual_capital + annual_om) / annual_energy_mwh
    # '1cfe-Form Capital Charge' (mfe_account_costs.sysml:901), '1cfe-Form LCOE' (:931)
    crf_71 = vs.finance.crf(i_rate, n_life)
    cas90_1cfe = crf_71 * (overnight_capital + idc_capital)
    lcoe_1cfe = ((cas90_1cfe + cas70_annual + cas80_annual) / (8760.0 * p_net * n * availability))
    # 'Volume-Averaged Beta' (mfe_plasma_scaling.sysml:367)
    beta = 2.0 * p["beta_mu0"] * sust["p_avg"] / (B_axis ** 2)

    result = dict(
        coverage_annual_total=annual_om, coverage_cas70=cas70_annual, coverage_cas71_crf=crf_71,
        coverage_cas71_levelized=cas71_annual, coverage_cas80_crf=crf_71,
        coverage_cas80_levelized=cas80_annual,
        coverage_cooling_cost_mode=p["cooling_cost_mode"], coverage_cooling_energy_mode=p["cooling_energy_mode"],
        coverage_cooling_consumables=p["cooling_cost_mode"] * cooling["consumables_annual"],
        coverage_cooling_replacements=p["cooling_cost_mode"] * cooling["replacement_annual"],
        coverage_cooling_shipping=p["cooling_cost_mode"] * cooling["delivered_total"],
        coverage_coil_length=c_coil, coverage_wp_side=wp_side, coverage_cold_volume=vol_cold_total,
        coverage_blanket_volume=blanket_vol, coverage_outer_radius=lt_shield_or,
        coverage_coil_inner_radius=r_coil, coverage_shield_volume=shield_vol,
        coverage_structure_volume=structure_vol, coverage_vessel_volume=vessel_vol,
        coverage_wall_area=wall_area, coverage_replacement_event=replacement_cost_per_event,
        **{"conductor_" + key: value for key, value in conductor.items()},
        **{"fit_" + key: value for key, value in vs._winding_fit(p).items()},  # imported
        winding_I_coil=I_coil, winding_j_wp_effective=effective_density,
        V=V, p_fus=p_fus, p_th=p_th, p_the=p_the, p_et=p_et,
        p_cryo=p_cryo, p_cryo_cold=p_cryo_cold, p_cryo_shield=p_cryo_shield,
        support_mass=support_mass, p_tf_total=p_tf_total, p_cold=p_cold,
        structure_nuclear=structure_nuclear * 1e6, structure_legacy_cost=structure_legacy_cost,
        **{"thermal_" + name: value for name, value in thermal.items()},
        q_eng=q_eng, rec_frac=rec_frac, p_net=p_net, wall_load=wall_load,
        wall_peak_calibration=wall_peak_calibration, wall_load_peak=wall_load_peak,
        beta=beta, B_peak=B_peak, B_axis=B_axis, sigma_wp=sigma_wp, eps_cond=eps_cond,
        W_mag=W_mag, m_casing=m_casing, r_coil_centre=r_coil_centre, A=A,
        n_bar19=sust["n_bar19"], n_He0=sust["n_He0"], n_D0=sust["n_D0"],
        n_T0=sust["n_T0"], T_e0=sust["T_e0"], W_th=sust["W_th"],
        tau_E=sust["tau_E"], p_brems=sust["p_brems"], p_line=sust["p_line"],
        p_sync=sust["p_sync"], p_rad=sust["p_rad"],
        p_alpha_heat=sust["p_alpha_heat"], p_aux_required=sust["p_aux_required"],
        p_avg=sust["p_avg"], n_e_volav=sust["n_e_volav"],
        alpha_n_e_eff=sust["alpha_n_e_eff"], alpha_He_eff=sust["alpha_He_eff"],
        operating_heat_coupled=operating_heat_coupled, operating_heat_delivered=operating_heat_delivered,
        operating_heat_wallplug=operating_heat_wallplug,
        heat_eta_pin_eff=heat_eta_pin_eff, heat_delivered=heat_delivered,
        heat_coupled=heat_coupled, heat_wallplug_total=heat_wallplug_total,
        q_source=q_source,
        loop_mdot=loop_mdot, loop_T_out=loop_T_out, loop_mdot_loop=loop_mdot_loop,
        loop_dp_loop=loop_dp_loop, loop_p_loop_margin=loop_p_loop_margin,
        loop_r_comp=loop_r_comp, loop_T_comp_in=loop_T_comp_in,
        loop_w_fluid=loop_w_fluid, loop_p_elec=loop_p_elec, loop_q_ihx=loop_q_ihx,
        loop_capacity_margin=loop_capacity_margin,
        loop_p_pump_total=loop_p_pump_total, loop_q_recovered_total=loop_q_recovered_total,
        cycle_T2_C=cycle_T2_C, cycle_eta_fit=cycle_eta_fit, cycle_eta_th=cycle_eta_th,
        cycle_margin_low=cycle_margin_low, cycle_margin_high=cycle_margin_high,
        cycle_domain_product=cycle_domain_product,
        **{"matched_" + name: value for name, value in matched_cycle.items()},
        **{"cw_" + name: value for name, value in cooling_water.items()},
        **{"cycle_selection_" + name: value for name, value in cycle_selection.items()},
        winding_pack=winding_pack, magnet_structure=magnet_structure,
        support_effective_all_in_rate=support_effective_all_in_rate,
        **{"insulation_" + name: value for name, value in insulation.items()},
        winding_pack_legacy=winding_pack_legacy, vol_winding_pack=vol_winding_pack,
        **{"winding_" + name: value for name, value in inventory.items()},
        tape_length=procurement["tape_length"], tape_procurement_cost=procurement["tape_cost"],
        conductor_length=procurement["conductor_length"],
        winding_fabrication_cost=procurement["winding_fabrication_cost"],
        magnet_capital_rollup=magnet_capital_rollup,
        aux_cost=aux_cost, cryo_cost=cryo_cost,
        magnet=magnet, heating=heating, divertor=divertor, blanket=blanket,
        shield=shield, structure=structure, vessel=vessel,
        power_supplies=power_supplies, turbine=turbine, electric=electric,
        heat_rejection=heat_rejection, misc=misc,
        buildings=buildings, precon=precon, annual_om=annual_om,
        special_materials=special_materials_capital,
        powercore_capital=powercore_capital, bop_capital=bop_capital,
        remote_handling=remote_handling, installation=installation,
        coolant=coolant, coolant_legacy=coolant_legacy, aux_cooling=aux_cooling, waste=waste,
        cooling_electric_total=cooling_electric_total, cooling_recovered_total=cooling_recovered_total,
        cooling_om_total=cooling_om_total,
        **{"cooling_" + name: value for name, value in cooling.items()},
        **{"facility_" + name: value for name, value in facilities.items()},
        buildings_legacy=buildings_legacy, precon_legacy=precon_legacy, facility_exclusion=facility_exclusion,
        facility_site_allowance=facilities["active"] * p["facility_retained_site_improvements"],
        facility_selected_parcel_x_min=p["facility_selected_parcel_x_min"] + p["facility_parcel_origin_x_offset"],
        facility_selected_parcel_y_min=p["facility_selected_parcel_y_min"] + p["facility_parcel_origin_y_offset"],
        facility_initial_sector_start_days=p["facility_initial_sector_start_days"],
        facility_cooling_initial_handoff_days=p["facility_cooling_initial_handoff_days"],
        shipping_cooling_exclusion=p["cooling_cost_mode"] * cooling["delivered_total"],
        shipping_facility_exclusion=facility_exclusion,
        shipping_remaining_base=cas20_capital - p["cooling_cost_mode"] * cooling["delivered_total"] - facility_exclusion - processing_exclusion,
        fuel_handling_legacy=fuel_handling_legacy,
        shipping_fuel_installation_exclusion=processing_exclusion,
        **{"processing_" + key: value for key, value in processing.items()},
        fuel_handling=fuel_handling, other_rpe=other_rpe, inc=inc,
        owner=owner, supplementary=supplementary, idc_capital=idc_capital,
        reactor_equipment_subtotal=reactor_equipment_subtotal,
        cas22_capital=cas22_capital, cas28_capital=cas28_capital,
        cas2x_pre_contingency=cas2x_pre_contingency, cas20_capital=cas20_capital,
        cas30_capital=cas30_capital, cas23_to_28_capital=cas23_to_28_capital,
        overnight_capital=overnight_capital, contingency_capital=contingency_capital,
        indirect_capital=indirect_capital, total_capital=total_capital, lcoe=lcoe,
        annual_om_unlevelized=annual_om_unlevelized, annual_fuel=annual_fuel,
        cas71_annual=cas71_annual, cas72_annual=cas72_annual,
        calendar_availability=cal["availability"],
        calendar_coil_life_margin_fpy=cal["coil_life_margin_fpy"],
        calendar_replacement_pv=cal["replacement_pv"],
        calendar_planned_downtime_yr=cal["planned_downtime_yr"],
        calendar_terminal_downtime_yr=cal["terminal_downtime_yr"],
        calendar_unplanned_downtime_yr=cal["unplanned_downtime_yr"],
        calendar_productive_fpy=cal["productive_fpy"],
        calendar_dated_energy_ratio=cal["dated_energy_ratio"],
        calendar_cas72_annual=cal["cas72_annual"],
        calendar_n_replacements=cal["n_replacements"],
        calendar_physical_life_fpy=cal["physical_life_fpy"],
        cas70_annual=cas70_annual, cas80_annual=cas80_annual,
        cas90_1cfe=cas90_1cfe, lcoe_1cfe=lcoe_1cfe,
        fuel_burn_rate=fuel_burn_rate, fuel_inject_rate=fuel_inject_rate,
        fuel_exhaust_rate=fuel_exhaust_rate, fuel_loss_rate=fuel_loss_rate,
        fuel_tbr_required=fuel_tbr_required, fuel_tbr_margin=fuel_tbr_margin,
        fuel_burn_kg_per_fpy=fuel_burn_kg_per_fpy,
        **{"inventory_" + name: value for name, value in fuel_inventory.items()},
        **{"breeding_" + name: value for name, value in breeding.items()},
        **{"breeding_adequacy_" + name: value for name, value in breeding_adequacy.items()},
        **{"divheat_" + name: value for name, value in divheat.items()},
        vacuum_n_molecules=vacuum_n_molecules, vacuum_Q_total=vacuum_Q_total,
        vacuum_S_eff_required=vacuum_S_eff_required,
    )
    result.update(vs.oracle_capability.evaluate(p, result))  # imported
    if glue is not None:
        # Cold and intercept screens read the staged demands (H5 seams :485, :500, :503).
        cap = vs.oracle_capability
        applicable = result["capability_cryogenic_state_applicable"]
        supported = result["capability_cryogenic_state_supported"]
        cold_flag = "capability_flag_cryoplant__cold_stage_capability__demand_available_in"
        cold_screen = cap.screen(p["capability_cryoplant__rated_cold_W"], glue["cold_demand_W"],
                                 applicable, supported, bool(p[cold_flag]))
        intercept_screen = cap.screen(p["capability_cryoplant__rated_intercept_W"], glue["intercept_demand_W"],
                                      applicable, supported, glue["intercept_available"])
        result.update({"capability_cold_stage_" + k: v for k, v in cold_screen.items()})
        result.update({"capability_intercept_stage_" + k: v for k, v in intercept_screen.items()})
    result.update({"procurement_guard_" + suffix: p[name]
                   for suffix, (name, value) in vs.oracle_procurement.PUBLIC_DEFAULTS.items() if "class_" in suffix})
    # Not channels: the power-balance operands the seams feed (kept for tests and notes).
    result["_pb_p_cryo"] = pb_p_cryo
    result["_rollup_winding_cost"] = rollup_winding_cost
    result["_ratio_eff"] = peak["ratio_eff"]
    return result, glue


# ---------------------------------------------------------------------------------------------
# Inputs of one material instance
# ---------------------------------------------------------------------------------------------
def resolve_material_inputs(inputs: Mapping[str, object], material: str) -> tuple[dict, dict]:
    """Complete one material instance's inputs, keyed by section 5.1 suffixes (after the prefix).

    Keys may be bare suffixes or carry this material's prefix. Refused: keys of the other material
    or of the reference prefix (one material per case; the reference is pinned), the Removed class
    (K11, R5), unknown keys, and missing supplied-design quantities with no design-stated value.
    Defaults, in order: the pin's value of each held plant key; the design's material values (E7,
    E8) and glue slot defaults. Returns (resolved inputs, provenance per key).
    """
    _check_material(material)
    prefix = MATERIAL_PREFIXES[material]
    foreign = [REFERENCE_PREFIX] + [MATERIAL_PREFIXES[m] for m in MATERIALS if m != material]
    supplied: dict[str, object] = {}
    for key, value in inputs.items():
        if key.startswith(prefix):
            suffix = key[len(prefix):]
        elif any(key.startswith(other) for other in foreign):
            raise GlueOracleError(f"key {key!r} belongs to another instance; one material per case")
        elif key.startswith("stellarator_09"):
            raise GlueOracleError(f"key {key!r} carries an unknown instance prefix")
        else:
            suffix = key
        if suffix in REMOVED_KEYS:
            raise GlueOracleError(f"{suffix!r} is final in the material variants (K11) and refused")
        if suffix in supplied and supplied[suffix] != value:
            raise GlueOracleError(f"key {suffix!r} supplied twice with different values")
        supplied[suffix] = value
    resolved = {k: v for k, v in PIN_SUFFIX_INPUTS.items() if k not in REMOVED_KEYS}
    provenance = dict.fromkeys(resolved, "pin")
    for key, value in material_facts(material).items():
        resolved[key] = value
        provenance[key] = "design default"
    allowed = (set(resolved) | set(REQUIRED_SUPPLIED[material]) | {INTERCEPT_AVAILABLE_KEY}
               | set(NIST_OPTIONAL_KEYS))
    if material == "rebco":
        allowed.discard(EPS_KEY)
    for key, value in supplied.items():
        if key not in allowed:
            raise GlueOracleError(f"key {key!r} is not an entry key of the {material} instance")
        if key in NIST_OPTIONAL_KEYS:
            if _finite(key, value) != NIST_OPTIONAL_KEYS[key]:
                raise GlueOracleError(f"{key} must equal Round 1's NIST 316 coefficient "
                                      f"{NIST_OPTIONAL_KEYS[key]}; the Round 1 cold-stage oracle holds the fit")
            continue
        if (key in PIN_SUFFIX_INPUTS and key not in SUFFIX_TO_ORACLE and key not in VERDICT_INPUT_KEYS
                and value != PIN_SUFFIX_INPUTS[key]):
            raise GlueOracleError(f"held plant key {key!r} cannot vary: the plant oracle holds it "
                                  f"at {PIN_SUFFIX_INPUTS[key]!r}")
        resolved[key] = value
        provenance[key] = "supplied"
    missing = [key for key in REQUIRED_SUPPLIED[material] if key not in resolved]
    if missing:
        raise GlueOracleError(f"missing supplied-design keys for {material}: {missing}")
    for key in variant_keys(material):
        if key in resolved and key != INTERCEPT_AVAILABLE_KEY:
            resolved[key] = _finite(key, resolved[key])
    return resolved, provenance


def _verdict_input_keys() -> set[str]:
    keys = set()
    for operands in oe.OPERAND_BINDINGS.values():
        for binding in operands.values():
            if binding["kind"] == "input":
                keys.add(binding["key"][len(REFERENCE_PREFIX):])
    return keys


VERDICT_INPUT_KEYS = _verdict_input_keys()


def _plant_parameters(resolved: Mapping[str, object], material: str) -> dict:
    """The plant-oracle parameter dict of one material instance (held keys checked)."""
    point = {}
    extra = variant_keys(material)
    for suffix, value in resolved.items():
        if suffix in SUFFIX_TO_ORACLE:
            point[REFERENCE_PREFIX + suffix] = value
        elif suffix in extra or suffix in VERDICT_INPUT_KEYS:
            continue
        elif suffix in PIN_SUFFIX_INPUTS:
            if value != PIN_SUFFIX_INPUTS[suffix]:
                raise GlueOracleError(f"held plant key {suffix!r} cannot vary: the plant oracle holds it "
                                      f"at {PIN_SUFFIX_INPUTS[suffix]!r}")
        else:
            raise GlueOracleError(f"unmapped key {suffix!r}")
    overrides = oe._oracle_overrides(point)  # imported: the plant seam's typing and consistency rules
    p = dict(vs.IN)
    p.update(overrides)
    p["cryo_inventory_enabled"] = False  # final in 'Staged Cryoplant' (design 2.7)
    return p


# ---------------------------------------------------------------------------------------------
# Channels of a material instance
# ---------------------------------------------------------------------------------------------
GLUE_BLOCKS = {  # glue-dict block -> channel usage path (design sections 2.5-2.7)
    "adapter": "magnet__adapter__", "conductor": "magnet__conductor__", "area": "magnet__area__",
    "inventory": "magnet__inventory__", "pack_field": "magnet__pack_field__",
    "winding_sum": "magnet__winding_sum__", "shape_branch": "magnet__shape_branch__",
    "static_loads": "cryoplant__static_loads__", "cold_stage": "cryoplant__cold_stage__",
    "refrigeration": "cryoplant__refrigeration__", "staged_drive": "cryoplant__staged_drive__",
}


def _material_channels(result: Mapping[str, object], glue: Mapping[str, object]) -> dict[str, float]:
    channels = {suffix: float(result[name]) for name, suffix in ORACLE_TO_SUFFIX.items()}
    channels[REFERENCE_NEW_OUTPUT] = float(result["conductor_evaluation_defined"])
    for block, path in GLUE_BLOCKS.items():
        if block in glue:
            for name, value in glue[block].items():
                channels[path + name] = float(value)
    return channels


# ---------------------------------------------------------------------------------------------
# Verdicts: Kleene three-valued predicate IR (the reference package's own predicates)
# ---------------------------------------------------------------------------------------------
def _reference_catalog() -> dict[str, dict]:
    catalog = _load_json(REFERENCE_CONTRACT_PATH)["constraint_catalog"]["concrete_entries"]
    return {entry["constraint_id"]: entry for entry in catalog}


_CATALOG = _reference_catalog()


def _ref(name):
    return {"kind": "feature_ref", "reference": {"source_name": name}}


def _lit(value):
    return {"kind": "literal", "literal": {"value": value}}


def _op(operator, *operands):
    return {"kind": "operator", "operator": operator, "operands": list(operands)}


#: The six new material checks: Round 1 constraint defs
#: (models/library/analyses/magnet_conductor_alternatives.sysml:266-295) and 'Ampere Floor' (design 2.4).
NEW_VERDICTS = {
    "magnet__acceptance_ok": (_op("and", _op(">=", _ref("supported_in"), _lit(1.0)),
                                  _op(">=", _ref("margin_in"), _lit(0.0))),
                              {"supported_in": ("channel", "magnet__conductor__supported"),
                               "margin_in": ("channel", "magnet__conductor__acceptance_margin")}),
    "magnet__copper_ok": (_op(">=", _ref("cu_margin_in"), _lit(0.0)),
                          {"cu_margin_in": ("channel", "magnet__area__cu_margin")}),
    "magnet__steel_ok": (_op(">=", _ref("steel_margin_in"), _lit(0.0)),
                         {"steel_margin_in": ("channel", "magnet__area__steel_margin")}),
    "magnet__pack_area_ok": (_op(">=", _ref("fit_margin_in"), _lit(0.0)),
                             {"fit_margin_in": ("channel", "magnet__area__fit_margin")}),
    "magnet__ampere_floor_ok": (_op(">=", _ref("margin_in"), _lit(0.0)),
                                {"margin_in": ("channel", "magnet__pack_field__ampere_floor_margin")}),
    "cryoplant__capacity_ok": (_op(">=", _ref("capacity_margin_in"), _lit(0.0)),
                               {"capacity_margin_in": ("channel", "cryoplant__refrigeration__capacity_margin")}),
}
#: E6: the only re-pointed plant predicate operand in material instances.
REPOINTED_OPERANDS = {"reference_conductor_current_ok":
                      {"margin_fraction_in": ("channel", "magnet__conductor__acceptance_margin")}}


def _plant_verdict_specs() -> dict[str, tuple[dict, dict]]:
    specs = {}
    for cid, operands in oe.OPERAND_BINDINGS.items():
        entry = _CATALOG[cid]
        local = entry["source_local_identity"]
        ir = json.loads(entry["predicate_ir"])
        bound = {name: (b["kind"], b["key"][len(REFERENCE_PREFIX):]) for name, b in operands.items()}
        specs[local] = (ir, bound)
    if len(specs) != 67 or len(_CATALOG) != 67:
        raise GlueOracleError("reference predicate catalog is not the pinned 67")
    return specs


PLANT_VERDICTS = _plant_verdict_specs()


def _kleene(node, values):
    kind = node["kind"]
    if kind == "literal":
        return float(node["literal"]["value"])
    if kind == "feature_ref":
        return values[node["reference"]["source_name"]]
    if kind != "operator":
        raise GlueOracleError(f"unsupported predicate node {kind!r}")
    op = node["operator"]
    args = [_kleene(child, values) for child in node["operands"]]
    if op in ("and", "or"):
        if any(a is not None and not isinstance(a, bool) for a in args):
            raise GlueOracleError("Boolean connective over a non-Boolean operand")
        if op == "and":
            return False if False in args else (None if None in args else True)
        return True if True in args else (None if None in args else False)
    a, b = args
    if a is None or b is None or isinstance(a, bool) or isinstance(b, bool):
        raise GlueOracleError("comparison over a non-real operand")
    if math.isnan(a) or math.isnan(b):
        return None
    return {">": a > b, ">=": a >= b, "<": a < b, "<=": a <= b, "==": a == b}[op]


def _verdict_word(value):
    return {True: "satisfied", False: "violated", None: "indeterminate"}[value]


def _operand_value(kind, key, channels, resolved):
    source = channels if kind == "channel" else resolved
    value = source[key]
    return float(value)


def material_verdicts(channels: Mapping[str, float], resolved: Mapping[str, object]) -> dict[str, str]:
    """All 73 verdicts of a material instance, keyed by suffix-stripped local identity."""
    verdicts = {}
    for local, (ir, bound) in PLANT_VERDICTS.items():
        bound = dict(bound, **REPOINTED_OPERANDS.get(local, {}))
        values = {name: _operand_value(kind, key, channels, resolved) for name, (kind, key) in bound.items()}
        verdicts[local] = _verdict_word(_kleene(ir, values))
    for local, (ir, bound) in NEW_VERDICTS.items():
        values = {name: _operand_value(kind, key, channels, resolved) for name, (kind, key) in bound.items()}
        verdicts[local] = _verdict_word(_kleene(ir, values))
    return verdicts


def operand_bindings(material: str) -> dict[str, dict[str, dict[str, str]]]:
    """Qualified operand bindings of the 73 material predicates, keyed by local identity."""
    _check_material(material)
    prefix = MATERIAL_PREFIXES[material]
    out = {}
    for local, (ir, bound) in PLANT_VERDICTS.items():
        bound = dict(bound, **REPOINTED_OPERANDS.get(local, {}))
        out[local] = {name: {"kind": kind, "key": prefix + key} for name, (kind, key) in bound.items()}
    for local, (ir, bound) in NEW_VERDICTS.items():
        out[local] = {name: {"kind": kind, "key": prefix + key} for name, (kind, key) in bound.items()}
    return out


# ---------------------------------------------------------------------------------------------
# Public evaluation surfaces
# ---------------------------------------------------------------------------------------------
def _labels(material, channels, verdicts, resolved):
    """Study-side labels the oracle can recompute from channels (contract section 7; for cross-check)."""
    B = channels["magnet__peak_field_calc__B_peak"]
    x = channels["magnet__pack_field__R_over_sqrt_A_wp"]
    labels = dict(
        free_capacity=["cryoplant__rated_intercept_W"],  # D17
        envelope_flag=verdicts["peak_field_ok"] == "violated",
        green_extrapolated=channels["cryoplant__refrigeration__green_extrapolated"] == 1.0,
        arm_extrapolated=not 25.0 <= x <= 40.0,
        R_over_sqrt_A_wp=x,
        ampere_floor_margin=channels["magnet__pack_field__ampere_floor_margin"],
        beta_ok_0_05=verdicts["beta_ok"],
        beta_ok_0_04=_verdict_word(None if math.isnan(channels["plasma__beta_calc__beta"])
                                   else channels["plasma__beta_calc__beta"] <= 0.04),
        conductor_status_code=channels["magnet__conductor__status_code"],
        conductor_supported=channels["magnet__conductor__supported"],
    )
    if material == "rebco":
        labels.update(extrapolated=20.0 < B <= 24.0, beyond_law_extents=24.0 < B <= 25.0,
                      above_stellaris_envelope=B > 24.9)
    return labels


def evaluate_material_case(inputs: Mapping[str, object], material: str) -> dict:
    """Every channel and verdict of one material instance (design section 5.2 and more).

    Returns {"material", "prefix", "channels" (suffix -> float), "verdicts" (local identity ->
    satisfied|violated|indeterminate), "labels", "checks" (structure-mass rule), "inputs"
    (resolved suffix inputs), "input_provenance"}. Qualified names are prefix + suffix.
    Refusals (domain errors of any imported or glue piece, non-convergence) propagate as
    exceptions; the route records them as `unsupported (domain refusal)` (K25).
    """
    resolved, provenance = resolve_material_inputs(inputs, material)
    p = _plant_parameters(resolved, material)
    result, glue = _plant_chain(p, _MaterialLegs(material, resolved))
    channels = _material_channels(result, glue)
    verdicts = material_verdicts(channels, resolved)
    checks = dict(structure_mass=structure_mass_check(p["magnet_support_mass"],
                                                     channels["magnet__stored_energy__W_mag"]))
    return dict(material=material, prefix=MATERIAL_PREFIXES[material], channels=channels,
                verdicts=verdicts, labels=_labels(material, channels, verdicts, resolved),
                checks=checks, inputs=resolved, input_provenance=provenance,
                seam_operands=dict(pb_p_cryo=result["_pb_p_cryo"],
                                   rollup_winding_cost=result["_rollup_winding_cost"],
                                   peak_ratio_eff=result["_ratio_eff"]))


def evaluate_reference_case(inputs: Mapping[str, object]) -> dict[str, float]:
    """The reference instance: delegates to the plant oracle (oracle_entry.evaluate) unchanged.

    Keys may be qualified (reference prefix) or bare suffixes. The three declared new entry keys
    must sit at their neutral values (rebco_law_enabled 1.0, arm_slope 0.0, any finite arm_x_ref)
    and are then dropped; held plant keys the plant seam does not map must equal the pin. The one
    declared new output, magnet__conductor_current__evaluation_defined = 1.0, is added (review R4).
    """
    point = {}
    for key, value in inputs.items():
        if key.startswith(REFERENCE_PREFIX):
            suffix = key[len(REFERENCE_PREFIX):]
        elif key.startswith("stellarator_09"):
            raise GlueOracleError(f"key {key!r} is not a reference-prefix key")
        else:
            suffix = key
        if suffix in NEW_REFERENCE_KEYS:
            if suffix == "magnet__rebco_law_enabled" and value != 1.0:
                raise GlueOracleError("the plant oracle evaluates only rebco_law_enabled = 1")
            if suffix == "magnet__coil__arm_slope" and value != 0.0:
                raise GlueOracleError("the plant oracle evaluates only arm_slope = 0")
            if suffix == "magnet__coil__arm_x_ref":
                _finite(suffix, value)
            continue
        if suffix not in SUFFIX_TO_ORACLE:
            if suffix in PIN_SUFFIX_INPUTS and value == PIN_SUFFIX_INPUTS[suffix]:
                continue
            raise GlueOracleError(f"reference key {suffix!r} is held by the plant oracle or unknown")
        point[REFERENCE_PREFIX + suffix] = value
    channels = oe.evaluate(point)
    channels[REFERENCE_PREFIX + REFERENCE_NEW_OUTPUT] = 1.0
    return channels


def qualified(case: Mapping[str, object]) -> dict[str, float]:
    """Channels of an evaluate_material_case result under their qualified names."""
    return {case["prefix"] + suffix: value for suffix, value in case["channels"].items()}


# ---------------------------------------------------------------------------------------------
# LCOE breakdown (design section 5.2, D2) and the rollup identities (test 13)
# ---------------------------------------------------------------------------------------------
CAPITAL_GROUPS = {
    "conductor_purchase": ("magnet__inventory__sc_cost",),
    "other_winding_materials_and_operations": (
        "magnet__inventory__materials_cost", "magnet__material_inventory__cost_helium",
        "magnet__winding_procurement__winding_fabrication_cost", "magnet__insulation_inventory__stock_cost"),
    "structure": ("magnet__magnet_structure_cost__cost",),
    "refrigeration_capital": ("cryoplant__aux_cooling__cryo_cost",),
    "heating_capital": ("heating__heating_cost__cost",),
    "radial_build": ("blanket__blanket_cost__cost", "shield__shield_cost__cost",
                     "structure__structure_cost__cost", "vessel__vessel_cost__cost"),
    "packages_and_plant_accounts": (
        "turbine__turbine_cost__cost", "electric_plant__electric_cost__cost",
        "heat_rejection__heat_rejection_cost__cost", "misc_plant__misc_cost__cost",
        "power_supplies__power_supplies_cost__cost", "divertor__divertor_cost__cost",
        "cryoplant__aux_cooling__aux_cost", "heat_transport__cooling_selection__cost"),
    "fuel_cycle_capital": ("fuel_cycle__processing_cost__cost",),
    "cas22_tail": ("remote_handling__cost", "installation__cost", "waste__cost", "other_rpe__cost",
                   "inc_cost__cost"),
    "buildings_and_other_direct": ("buildings__facility_accounts__cost",
                                   "special_materials_capital__special_materials_capital", "input:cas28_capital"),
    "multipliers_and_owner": ("contingency__cost", "indirect__cost", "owner__cost", "supplementary__cost",
                              "facility_preconstruction__cost"),
}
#: The reference instance's winding terms (the plant basis).
REFERENCE_WINDING_GROUPS = {
    "conductor_purchase": ("magnet__winding_procurement__tape_cost",),
    "other_winding_materials_and_operations": (
        "magnet__material_inventory__material_cost", "magnet__winding_procurement__winding_fabrication_cost",
        "magnet__insulation_inventory__stock_cost"),
}
ANNUAL_GROUPS = {"om_cas71": ("cas71_calc__levelized",), "replacements_cas72": ("cooling_annual__cas72_total",),
                 "fuel_cas80": ("cas80_calc__levelized",)}
REPORTED_ONLY = ("idc__cost", "precon_cost__cost", "heat_transport__coolant__cost",
                 "fuel_cycle__fuel_handling__cost", "cryoplant__aux_cooling__cost", "calendar__cas72_annual",
                 "fuel_cycle__fuel_calc__annual_fuel", "cryoplant__refrigeration__p_in_total_MW",
                 "operating_heat__p_wallplug")


def _value(ref, channels, inputs):
    if ref.startswith("input:"):
        return float(inputs[ref[len("input:"):]])
    return channels[ref]


def lcoe_breakdown(channels: Mapping[str, float], inputs: Mapping[str, object],
                   reference: bool = False) -> dict:
    """Account-group capital and its LCOE share, annual groups, and the closure residual (D2).

    LCOE = (total_capital * idc * crf + CAS71 + CAS72 + CAS80) / (8760 * p_net * availability)
    (mfe_lcoe_dcf.sysml:12-17), so each capital group contributes group * idc * crf / E.
    """
    groups = dict(CAPITAL_GROUPS)
    if reference:
        groups.update(REFERENCE_WINDING_GROUPS)
    d, Yc, N = (float(inputs["discount_rate"]), float(inputs["construction_years"]),
                float(inputs["operational_years"]))
    crf = vs.finance.crf(d, N)
    idc = vs.finance.growth(d, Yc / 2.0)
    energy = 8760.0 * channels["pb__p_net"] * channels["calendar__availability"]
    capital = {g: math.fsum(_value(r, channels, inputs) for r in refs) for g, refs in groups.items()}
    annual = {g: math.fsum(channels[r] for r in refs) for g, refs in ANNUAL_GROUPS.items()}
    contributions = {g: v * idc * crf / energy for g, v in capital.items()}
    contributions.update({g: v / energy for g, v in annual.items()})
    total = math.fsum(contributions.values())
    lcoe = channels["lcoe_calc__lcoe"]
    return dict(capital=capital, annual=annual, contributions=contributions,
                capital_total=math.fsum(capital.values()), lcoe_sum=total, lcoe=lcoe,
                relative_residual=(total - lcoe) / lcoe, energy_MWh=energy, idc_factor=idc, crf=crf,
                reported_only={r: channels[r] for r in REPORTED_ONLY if r in channels})


def closure_residuals(channels: Mapping[str, float], inputs: Mapping[str, object],
                      reference: bool = False) -> dict[str, float]:
    """Relative residuals of the plant's rollup identities recomputed from the breakdown accounts."""
    c = channels
    cas28 = float(inputs["cas28_capital"])
    if reference:
        winding = c["magnet__winding_procurement__cost"]
    else:
        winding = (c["magnet__inventory__sc_cost"] + c["magnet__inventory__materials_cost"]
                   + c["magnet__material_inventory__cost_helium"]
                   + c["magnet__winding_procurement__winding_fabrication_cost"])
    magnet = winding + c["magnet__magnet_structure_cost__cost"] + c["magnet__insulation_inventory__stock_cost"]
    powercore = (magnet + c["heating__heating_cost__cost"] + c["divertor__divertor_cost__cost"]
                 + c["blanket__blanket_cost__cost"] + c["shield__shield_cost__cost"]
                 + c["structure__structure_cost__cost"] + c["vessel__vessel_cost__cost"]
                 + c["power_supplies__power_supplies_cost__cost"])
    bop = (c["turbine__turbine_cost__cost"] + c["electric_plant__electric_cost__cost"]
           + c["heat_rejection__heat_rejection_cost__cost"] + c["misc_plant__misc_cost__cost"])
    aux_cooling = c["cryoplant__aux_cooling__aux_cost"] + c["cryoplant__aux_cooling__cryo_cost"]
    cas22 = (powercore + c["remote_handling__cost"] + c["installation__cost"]
             + c["heat_transport__cooling_selection__cost"] + aux_cooling + c["waste__cost"]
             + c["fuel_cycle__processing_cost__cost"] + c["other_rpe__cost"] + c["inc_cost__cost"])
    cas2x = (c["buildings__facility_accounts__cost"] + cas22 + bop
             + c["special_materials_capital__special_materials_capital"] + cas28)
    cas20 = cas2x + c["contingency__cost"]
    total = (c["facility_preconstruction__cost"] + cas20 + c["indirect__cost"] + c["owner__cost"]
             + c["supplementary__cost"])
    annual = c["cas71_calc__levelized"] + c["cooling_annual__cas72_total"] + c["cas80_calc__levelized"]
    d, Yc, N = (float(inputs["discount_rate"]), float(inputs["construction_years"]),
                float(inputs["operational_years"]))
    lcoe = ((total * vs.finance.growth(d, Yc / 2.0) * vs.finance.crf(d, N) + annual)
            / (8760.0 * c["pb__p_net"] * c["calendar__availability"]))
    pairs = {
        "magnet_capital": (magnet, c["magnet__magnet_capital_rollup__capital_cost"]),
        "aux_cooling": (aux_cooling, c["cryoplant__aux_cooling__cost"]),
        "powercore_capital": (powercore, c["powercore_capital__powercore_capital"]),
        "bop_capital": (bop, c["bop_capital__bop_capital"]),
        "cas22_capital": (cas22, c["cas22_capital__cas22_capital"]),
        "cas2x_pre_contingency": (cas2x, c["cas2x_pre_contingency__cas2x_pre_contingency"]),
        "cas20_capital": (cas20, c["cas20_capital__cas20_capital"]),
        "overnight_capital": (total, c["overnight_capital__overnight_capital"]),
        "total_capital": (total, c["total_capital__total_capital"]),
        "cas70_annual_total": (annual, c["cas70_calc__annual_total"]),
        "lcoe": (lcoe, c["lcoe_calc__lcoe"]),
    }
    return {name: (lhs - rhs) / rhs for name, (lhs, rhs) in pairs.items()}


# ---------------------------------------------------------------------------------------------
# Channel-to-oracle map (design section 6.3, D3; review R4) -> oracle-reuse.json
# ---------------------------------------------------------------------------------------------
IMPORTED_BY_PREFIX = (  # plant-oracle output-name prefix -> imported function
    ("breeding_adequacy_", "oracle_breeding.adequacy"),
    ("breeding_", "oracle_breeding.response"),
    ("fit_", "verify_stellaris._winding_fit"),
    ("insulation_", "verify_stellaris._insulation_inventory"),
    ("thermal_", "verify_stellaris._coil_thermal_inventory"),
    ("facility_", "oracle_facilities.layout"),
    ("inventory_", "oracle_fuel_inventory.evaluate"),
    ("processing_", "oracle_fuel_processing.calculate"),
    ("matched_", "oracle_matched_cycle.matched_interface"),
    ("cw_", "oracle_matched_cycle.cooling_interface"),
    ("cycle_selection_", "oracle_matched_cycle.selection_interface"),
    ("capability_", "oracle_capability.evaluate"),
    ("divheat_", "verify_stellaris.divertor_account"),
    ("calendar_", "verify_stellaris._oracle_lifecycle_calendar"),
    ("procurement_guard_", "oracle_procurement.PUBLIC_DEFAULTS (supplied class passthrough)"),
    ("cooling_", "oracle_cooling.calculate"),
)
IMPORTED_BY_NAME = {
    **dict.fromkeys(("n_bar19", "n_He0", "n_D0", "n_T0", "T_e0", "W_th", "tau_E", "p_brems", "p_line",
                     "p_sync", "p_rad", "p_alpha_heat", "p_aux_required", "p_avg", "n_e_volav",
                     "alpha_n_e_eff", "alpha_He_eff"), "verify_stellaris._sustainment"),
    **dict.fromkeys(("winding_mass_copper", "winding_mass_solder", "winding_mass_steel", "winding_mass_helium",
                     "winding_cost_copper", "winding_cost_solder", "winding_cost_steel", "winding_cost_helium",
                     "winding_material_cost", "winding_helium_density", "winding_tape_volume"),
                    "verify_stellaris._winding_material_inventory"),
    **dict.fromkeys(("tape_length", "tape_procurement_cost", "conductor_length", "winding_fabrication_cost",
                     "winding_pack"), "verify_stellaris._winding_procurement"),
    "loop_mdot": "verify_stellaris._primary_loop_mass_flow",
    "p_fus": "verify_stellaris._profile_integral + 'DT Fusion Power' mfe_plasma_scaling.sysml:148",
}
LIB = "models/library/analyses/"
REDERIVED = {  # plant-oracle output name -> SysML definition re-derived inline in _plant_chain
    "winding_I_coil": LIB + "mfe_magnet_field.sysml:4 'Winding Operating State'",
    "winding_j_wp_effective": LIB + "mfe_magnet_field.sysml:4 'Winding Operating State'",
    "V": LIB + "mfe_plasma_scaling.sysml:4 'Plasma Geometry'",
    "A": LIB + "mfe_plasma_scaling.sysml:4 'Plasma Geometry'",
    "r_coil_centre": LIB + "mfe_plasma_scaling.sysml:52 'MFE Radial Build'",
    "B_axis": LIB + "mfe_magnet_field.sysml:16 'Coil Set Axis Field'",
    "W_mag": LIB + "mfe_magnet_field.sysml:310 'Coil Set Stored Energy'",
    "vol_winding_pack": LIB + "mfe_magnet_field.sysml:218 'Winding Pack Cold Volume'",
    "p_th": LIB + "mfe_power_balance.sysml:4 'MFE Power Balance Calc'",
    "p_the": LIB + "mfe_power_balance.sysml:4 'MFE Power Balance Calc'",
    "p_et": LIB + "mfe_power_balance.sysml:4 'MFE Power Balance Calc' (p_et, :150)",
    "q_eng": LIB + "mfe_power_balance.sysml:164-165 'MFE Power Balance Calc'",
    "rec_frac": LIB + "mfe_power_balance.sysml:167-168",
    "p_net": LIB + "mfe_power_balance.sysml:159-161, :170-171 (recirculating, p_net); p_cryo seam models/designs/generic_mfe/mfe_plant.sysml:395",
    "q_source": LIB + "mfe_power_balance.sysml:174 'Reactor Source Heat'",
    "p_cryo": LIB + "mfe_cryo_inventory.sysml:81 'Electrical Power Sum' (dormant plant chain)",
    "p_cryo_cold": LIB + "mfe_cryo_plant.sysml:4 'Cryoplant Electrical Power' (dormant)",
    "p_cryo_shield": LIB + "mfe_cryo_inventory.sysml:89 'Intercept Electrical Power' (dormant)",
    "p_cold": LIB + "mfe_cryo_inventory.sysml:62 'Cold Load Sum' (dormant)",
    "structure_nuclear": LIB + "mfe_cryo_inventory.sysml:62 'Cold Load Sum' (dormant)",
    "p_tf_total": "models/designs/generic_mfe/mfe_plant.sysml:192 (p_tf_extra seam) with 'Power Supplies' tf_power",
    "operating_heat_coupled": LIB + "mfe_heating_chain.sysml:79 'Operating Heating Power'",
    "operating_heat_delivered": LIB + "mfe_heating_chain.sysml:79 'Operating Heating Power'",
    "operating_heat_wallplug": LIB + "mfe_heating_chain.sysml:79 'Operating Heating Power'",
    "heat_coupled": LIB + "mfe_heating_chain.sysml:4 'Heating Power Chain'",
    "heat_delivered": LIB + "mfe_heating_chain.sysml:4 'Heating Power Chain'",
    "heat_wallplug_total": LIB + "mfe_heating_chain.sysml:4 'Heating Power Chain'",
    "heat_eta_pin_eff": LIB + "mfe_heating_chain.sysml:4 'Heating Power Chain'",
    "cycle_T2_C": LIB + "mfe_power_cycle.sysml:4 'Power Cycle Efficiency'",
    "cycle_eta_fit": LIB + "mfe_power_cycle.sysml:4 'Power Cycle Efficiency'",
    "cycle_eta_th": LIB + "mfe_power_cycle.sysml:4 'Power Cycle Efficiency'",
    "cycle_margin_low": LIB + "mfe_power_cycle.sysml:4 'Power Cycle Efficiency'",
    "cycle_margin_high": LIB + "mfe_power_cycle.sysml:4 'Power Cycle Efficiency'",
    "cycle_domain_product": LIB + "mfe_power_cycle.sysml:4 'Power Cycle Efficiency'",
    "cooling_electric_total": LIB + "mfe_cooling_accounts.sysml:42 'Cooling Energy Addition'",
    "cooling_recovered_total": LIB + "mfe_cooling_accounts.sysml:42 'Cooling Energy Addition'",
    "cooling_om_total": LIB + "mfe_cooling_accounts.sysml:57 'Cooling Annual Addition'",
    "wall_load": LIB + "mfe_plasma_scaling.sysml:237 'Neutron Wall Load'",
    "wall_peak_calibration": LIB + "mfe_plasma_scaling.sysml:273 'Neutron Wall Load Peak Calibration'",
    "wall_load_peak": LIB + "mfe_plasma_scaling.sysml:342 'Neutron Wall Load Peak'",
    "beta": LIB + "mfe_plasma_scaling.sysml:367 'Volume-Averaged Beta'",
    "B_peak": LIB + "mfe_plasma_scaling.sysml:420 'Conductor Peak Field' + design 2.2 arm slot (H4, B2)",
    "sigma_wp": LIB + "mfe_magnet_field.sysml:60 'Winding Pack Stress' (reads the arm B_peak)",
    "eps_cond": LIB + "mfe_magnet_field.sysml:263 'Conductor Strain' (reads sigma_wp)",
    "magnet": LIB + "mfe_magnet_cost.sysml:4 'Magnet Coil Cost'",
    "winding_pack_legacy": LIB + "mfe_magnet_cost.sysml:56 'Winding Pack Cost'",
    "magnet_structure": LIB + "mfe_magnet_cost.sysml:157 'Magnet Structure Cost'",
    "support_effective_all_in_rate": LIB + "mfe_magnet_cost.sysml:177 'Magnet Structure Cost'",
    "magnet_capital_rollup": LIB + "mfe_magnet_cost.sysml:203 'Magnet Capital' with the winding_cost seam models/library/cost_structure/mfe_power_core.sysml:129, :361 (design 2.9, H6)",
    "blanket": LIB + "mfe_account_costs.sysml:72 'Blanket Cost'",
    "shield": LIB + "mfe_account_costs.sysml:102 'Shield Cost'",
    "structure_legacy_cost": LIB + "mfe_account_costs.sysml:131 'Structure Cost'",
    "structure": LIB + "mfe_account_costs.sysml:131 'Structure Cost' (residual fraction)",
    "vessel": LIB + "mfe_account_costs.sysml:164 'Vessel Cost'",
    "power_supplies": LIB + "mfe_account_costs.sysml:17 'Supplied Purchase Cost'",
    "divertor": LIB + "mfe_account_costs.sysml:17 'Supplied Purchase Cost'",
    "turbine": LIB + "mfe_account_costs.sysml:17 'Supplied Purchase Cost'",
    "heat_rejection": LIB + "mfe_account_costs.sysml:17 'Supplied Purchase Cost'",
    "heating": LIB + "mfe_account_costs.sysml:252 'Heating Cost'",
    "electric": LIB + "mfe_account_costs.sysml:282 'Linear Power Cost'",
    "misc": LIB + "mfe_account_costs.sysml:282 'Linear Power Cost'",
    "buildings_legacy": LIB + "mfe_account_costs.sysml:360 'Buildings Cost'",
    "precon_legacy": LIB + "mfe_account_costs.sysml:422 'Preconstruction Cost'",
    "buildings": LIB + "mfe_facilities.sysml:746 'Facility Account Selection'",
    "precon": LIB + "mfe_facilities.sysml:769 'Facility Preconstruction Selection'",
    "annual_om_unlevelized": LIB + "mfe_account_costs.sysml:459 'Annual OM Cost'",
    "powercore_capital": "models/designs/generic_mfe/mfe_plant.sysml:461-464",
    "bop_capital": "models/designs/generic_mfe/mfe_plant.sysml:467-469",
    "remote_handling": LIB + "mfe_account_costs.sysml:534 'Remote Handling Cost'",
    "reactor_equipment_subtotal": "models/designs/generic_mfe/mfe_plant.sysml:500",
    "installation": LIB + "mfe_account_costs.sysml:561 'Installation Labor Cost'",
    "coolant": LIB + "mfe_cooling_accounts.sysml:19 'Cooling Account Selection'",
    "coolant_legacy": LIB + "mfe_account_costs.sysml:584 'Coolant Cost'",
    "aux_cost": LIB + "mfe_account_costs.sysml:33 'Supplied Auxiliary Cooling Cost'",
    "cryo_cost": LIB + "mfe_account_costs.sysml:33 'Supplied Auxiliary Cooling Cost'; material instances: purchase_cost_per_module = refrigeration.refrigerator_capital (design 2.7)",
    "aux_cooling": LIB + "mfe_account_costs.sysml:33 'Supplied Auxiliary Cooling Cost'",
    "waste": LIB + "mfe_account_costs.sysml:507 'Plant Power-Law Cost'",
    "other_rpe": LIB + "mfe_account_costs.sysml:507 'Plant Power-Law Cost'",
    "inc": LIB + "mfe_account_costs.sysml:507 'Plant Power-Law Cost'",
    "owner": LIB + "mfe_account_costs.sysml:507 'Plant Power-Law Cost' (mfe_plant.sysml:613)",
    "fuel_handling_legacy": LIB + "mfe_account_costs.sysml:507 'Plant Power-Law Cost'",
    "special_materials": "models/designs/stellarator_09/stellarator_plant.sysml:1968",
    "cas22_capital": "models/designs/generic_mfe/mfe_plant.sysml:561-564",
    "cas2x_pre_contingency": "models/designs/generic_mfe/mfe_plant.sysml:572-574",
    "contingency_capital": LIB + "mfe_account_costs.sysml:311 'Contingency Cost'",
    "cas20_capital": "models/designs/generic_mfe/mfe_plant.sysml:586",
    "indirect_capital": LIB + "mfe_account_costs.sysml:332 'Indirect Cost'",
    "cas23_to_28_capital": "models/designs/generic_mfe/mfe_plant.sysml:602-603",
    "supplementary": LIB + "mfe_account_costs.sysml:651 'Supplementary Cost'",
    "overnight_capital": "models/designs/generic_mfe/mfe_plant.sysml:669-671",
    "total_capital": "models/designs/generic_mfe/mfe_plant.sysml:688-690",
    "idc_capital": LIB + "mfe_account_costs.sysml:712 'IDC Closed-Form Cost' (oracle_finance.idc_factor)",
    "lcoe": LIB + "mfe_lcoe_dcf.sysml:12-17 'LCOE DCF' (mfe_plant.sysml:799-807; oracle_finance.crf, growth)",
    "annual_fuel": LIB + "mfe_account_costs.sysml:804 'DT Fuel Cost'",
    "cas72_annual": LIB + "mfe_cooling_accounts.sysml:57 'Cooling Annual Addition'",
    "cas90_1cfe": LIB + "mfe_account_costs.sysml:901 '1cfe-Form Capital Charge'",
    "lcoe_1cfe": LIB + "mfe_account_costs.sysml:931 '1cfe-Form LCOE'",
    "shipping_cooling_exclusion": LIB + "mfe_facilities.sysml:690 'Facility Shipping Scope'",
    "shipping_facility_exclusion": LIB + "mfe_facilities.sysml:690 'Facility Shipping Scope'",
    "shipping_remaining_base": LIB + "mfe_facilities.sysml:690 'Facility Shipping Scope' (reads cas20)",
    "shipping_fuel_installation_exclusion": LIB + "mfe_facilities.sysml:690 'Facility Shipping Scope'",
    **dict.fromkeys(("fuel_burn_rate", "fuel_inject_rate", "fuel_exhaust_rate", "fuel_loss_rate",
                     "fuel_tbr_required", "fuel_tbr_margin", "fuel_burn_kg_per_fpy"),
                    LIB + "mfe_fuel_cycle.sysml:4 'Fuel Cycle Flows'"),
    **dict.fromkeys(("vacuum_n_molecules", "vacuum_Q_total", "vacuum_S_eff_required"),
                    LIB + "mfe_vacuum.sysml:4 'Vacuum Gas Load'"),
    **dict.fromkeys(("loop_T_out", "loop_mdot_loop", "loop_dp_loop", "loop_p_loop_margin", "loop_r_comp",
                     "loop_T_comp_in", "loop_w_fluid", "loop_p_elec", "loop_q_ihx", "loop_capacity_margin",
                     "loop_p_pump_total", "loop_q_recovered_total"),
                    LIB + "mfe_primary_loop.sysml:4 'Primary Coolant Loop'"),
    "coverage_annual_total": LIB + "mfe_account_costs.sysml:879 'Annual Cost Rollup'",
    "coverage_cas70": LIB + "mfe_account_costs.sysml:879 'Annual Cost Rollup'",
    "coverage_cas71_crf": LIB + "mfe_account_costs.sysml:747 'Levelized Annual Cost' (oracle_finance.crf)",
    "coverage_cas71_levelized": LIB + "mfe_account_costs.sysml:747 'Levelized Annual Cost' (oracle_finance.annuity)",
    "coverage_cas80_crf": LIB + "mfe_account_costs.sysml:747 'Levelized Annual Cost' (oracle_finance.crf)",
    "coverage_cas80_levelized": LIB + "mfe_account_costs.sysml:747 'Levelized Annual Cost' (oracle_finance.annuity)",
    **dict.fromkeys(("coverage_cooling_cost_mode", "coverage_cooling_energy_mode"),
                    LIB + "mfe_cooling_accounts.sysml:4 'Cooling Scenario Guard'"),
    **dict.fromkeys(("coverage_cooling_consumables", "coverage_cooling_replacements", "coverage_cooling_shipping"),
                    LIB + "mfe_cooling_accounts.sysml:19 'Cooling Account Selection'"),
    "coverage_coil_length": LIB + "mfe_magnet_field.sysml:154 'Coil Winding Length'",
    "coverage_cold_volume": LIB + "mfe_magnet_field.sysml:218 'Winding Pack Cold Volume'",
    **dict.fromkeys(("coverage_blanket_volume", "coverage_outer_radius", "coverage_coil_inner_radius",
                     "coverage_shield_volume", "coverage_structure_volume", "coverage_vessel_volume",
                     "coverage_wall_area"), LIB + "mfe_plasma_scaling.sysml:52 'MFE Radial Build'"),
    "coverage_replacement_event": "models/designs/generic_mfe/mfe_plant.sysml replacement_cost_per_event (blanket + divertor) x n_mod",
    "coverage_wp_side": "supplied wp_side passthrough (stellarator_plant.sysml:447)",
    "facility_site_allowance": LIB + "mfe_facilities.sysml:763 'Facility Site Allowance'",
    "facility_selected_parcel_x_min": "supplied parcel offsets (WI-076 identities)",
    "facility_selected_parcel_y_min": "supplied parcel offsets (WI-076 identities)",
    "facility_initial_sector_start_days": "supplied passthrough",
    "facility_cooling_initial_handoff_days": "supplied passthrough",
}
#: Channel-suffix ownership rules (design section 6.3 with D3, R4). First match wins.
GLUE_CHANNEL_PREFIXES = (
    "magnet__peak_field_calc__", "magnet__wp_stress__", "magnet__cond_strain__", "magnet__pack_field__",
    "magnet__adapter__", "magnet__winding_sum__", "magnet__shape_branch__", "cryoplant__static_loads__",
    "cryoplant__staged_drive__", "magnet__conductor_current__", "cryoplant__cold_stage_capability__",
    "cryoplant__intercept_stage_capability__", "power_supplies__tf_power__",
    "power_supplies__magnet_tf_electric_capability__", "cryoplant__aux_cooling__cryo_cost",
)
ROUND1_CHANNEL_PREFIXES = ("magnet__conductor__", "magnet__area__", "magnet__inventory__",
                           "cryoplant__cold_stage__", "cryoplant__refrigeration__")
COMPOSED_CHANNEL_PREFIXES = (
    "pb__", "magnet__magnet_capital_rollup__", "cryoplant__aux_cooling__cost", "powercore_capital__",
    "bop_capital__", "reactor_equipment_subtotal__", "installation__", "cas22_capital__",
    "cas2x_pre_contingency__", "contingency__", "cas20_capital__", "indirect__", "cas23_to_28_capital__",
    "supplementary__", "shipping_scope__remaining_shipping_base", "overnight_capital__",
    "total_capital__", "idc__", "cas70_calc__", "cas71_calc__", "cas80_calc__", "cooling_annual__cas72_total",
    "cas90_1cfe_calc__", "lcoe_calc__", "lcoe_1cfe_calc__",
)
GLUE_VERDICTS = ("peak_field_ok", "wp_stress_ok", "cond_strain_ok", "reference_conductor_current_ok",
                 "cold_stage_capacity_ok", "intercept_stage_capacity_ok", "magnet_tf_electric_capacity_ok",
                 "magnet__pack_area_ok", "magnet__ampere_floor_ok", "cryoplant__capacity_ok")
ROUND1_VERDICTS = ("magnet__acceptance_ok", "magnet__copper_ok", "magnet__steel_ok")
COMPOSED_VERDICTS = ("net_positive", "recirc_ok")
ROUND1_FUNCTIONS = {
    "magnet__conductor__": "oracle.nb3sn_cable_critical_surface | oracle.rebco_cable_critical_surface",
    "magnet__area__": "oracle.winding_turn_area_screen", "magnet__inventory__": "oracle.winding_inventory_and_cost",
    "cryoplant__cold_stage__": "oracle.magnet_cold_stage_load",
    "cryoplant__refrigeration__": "oracle.staged_refrigeration_screen",
}
GLUE_FUNCTIONS = {
    "magnet__peak_field_calc__": "oracle_glue.conductor_peak_field",
    "magnet__wp_stress__": "_plant_chain 'Winding Pack Stress' on the glue B_peak leg",
    "magnet__cond_strain__": "_plant_chain 'Conductor Strain' on the glue B_peak leg",
    "magnet__pack_field__": "oracle_glue.pack_field_checks", "magnet__adapter__": "oracle_glue.material_winding_adapter",
    "magnet__winding_sum__": "oracle_glue.material_winding_cost", "magnet__shape_branch__": "oracle_glue.rebco_shape_branch",
    "cryoplant__static_loads__": "oracle_glue.staged_static_loads",
    "cryoplant__staged_drive__": "oracle_glue.staged_drive_power",
    "magnet__conductor_current__": "oracle_glue.gated_rebco_conductor_current (enabled = 0)",
    "cryoplant__cold_stage_capability__": "oracle_capability.screen on cold_stage.q_cold (H5 seam :485)",
    "cryoplant__intercept_stage_capability__": "oracle_capability.screen on cold_stage.q_shield, available true (H5 :500, :503)",
    "power_supplies__tf_power__": "p_tf + staged_drive.p_drive (p_drive seam, mfe_plant.sysml:192)",
    "power_supplies__magnet_tf_electric_capability__": "oracle_capability.evaluate on the seamed tf_power",
    "cryoplant__aux_cooling__cryo_cost": "refrigeration.refrigerator_capital (Green law; design 2.7)",
}


def _first(prefixes, suffix):
    for prefix in prefixes:
        if suffix.startswith(prefix):
            return prefix
    return None


def channel_owner(suffix: str) -> str:
    """Owner of a material-instance channel: glue, round1, composed or plant (design 6.3, D3)."""
    if _first(GLUE_CHANNEL_PREFIXES, suffix):
        return "glue"
    if _first(ROUND1_CHANNEL_PREFIXES, suffix):
        return "round1"
    if _first(COMPOSED_CHANNEL_PREFIXES, suffix):
        return "composed"
    return "plant"


def verdict_owner(local: str) -> str:
    if local in GLUE_VERDICTS:
        return "glue"
    if local in ROUND1_VERDICTS:
        return "round1"
    if local in COMPOSED_VERDICTS:
        return "composed"
    return "plant"


def _realization(oracle_name: str | None, suffix: str) -> dict[str, str]:
    """How this oracle produces a channel: an imported function or a re-derived SysML equation."""
    prefix = _first(GLUE_FUNCTIONS, suffix)
    if prefix:
        return {"glue": GLUE_FUNCTIONS[prefix]}
    prefix = _first(ROUND1_FUNCTIONS, suffix)
    if prefix:
        return {"import": "exploration/magnet_materials/" + ROUND1_FUNCTIONS[prefix]}
    if oracle_name is None:
        raise GlueOracleError(f"no realization for {suffix}")
    if oracle_name in IMPORTED_BY_NAME:
        return {"import": IMPORTED_BY_NAME[oracle_name]}
    if oracle_name in REDERIVED:
        return {"rederived": REDERIVED[oracle_name]}
    for name_prefix, function in IMPORTED_BY_PREFIX:
        if oracle_name.startswith(name_prefix):
            return {"import": function}
    raise GlueOracleError(f"no realization declared for plant-oracle output {oracle_name!r}")


SECTION_5_2_CHANNELS = (
    "lcoe_calc__lcoe",
    *sorted({r for refs in CAPITAL_GROUPS.values() for r in refs if not r.startswith("input:")}),
    "cryoplant__refrigeration__refrigerator_capital", "cryoplant__refrigeration__p_in_total_MW",
    "operating_heat__p_wallplug", "idc__cost", "precon_cost__cost", "heat_transport__coolant__cost",
    "fuel_cycle__fuel_handling__cost", "cas71_calc__levelized", "cooling_annual__cas72_total",
    "calendar__cas72_annual", "cas80_calc__levelized", "cas70_calc__annual_total",
    "fuel_cycle__fuel_calc__annual_fuel", "magnet__magnet_capital_rollup__capital_cost",
    "powercore_capital__powercore_capital", "cas22_capital__cas22_capital", "cas20_capital__cas20_capital",
    "overnight_capital__overnight_capital", "total_capital__total_capital", "pb__p_net", "pb__p_et",
    "pb__p_th", "calendar__availability", "buildings__layout__geometry_fit_margin_m",
    "buildings__layout__occupancy_area_margin_m2", "buildings__layout__parcel_fit_margin_m",
    "heating__heat__p_coupled", "magnet__stored_energy__W_mag", "plasma__fusion__p_fus",
    "plasma__sustain__p_aux_required", "plasma__beta_calc__beta", "magnet__field_calc__B_axis",
    "magnet__peak_field_calc__B_peak", "magnet__wp_stress__sigma_wp", "magnet__cond_strain__eps_cond",
    "magnet__wp_fit__minimum_margin",
    *("magnet__conductor__" + n for n in ("T_conductor", "ic_cable_op", "operating_fraction", "T_cs",
                                           "tcs_defined", "acceptance_margin", "status_code", "supported",
                                           "acceptance_pass")),
    *("magnet__area__" + n for n in ("gross_area", "fit_margin", "fit_margin_fraction", "cu_margin",
                                      "steel_margin")),
    "magnet__inventory__conductor_length", "magnet__inventory__element_length",
    "magnet__pack_field__R_over_sqrt_A_wp", "magnet__pack_field__ampere_floor",
    "magnet__pack_field__ampere_floor_margin", "magnet__conductor_current__evaluation_defined",
    *("cryoplant__cold_stage__" + n for n in ("q_nuclear", "q_radiation", "q_conduction", "q_leads",
                                               "q_joints", "q_cold", "q_shield")),
    *("cryoplant__refrigeration__" + n for n in ("eta_cold", "p_in_cold", "p_in_shield", "R_equiv_kW",
                                                  "capacity_margin", "green_extrapolated")),
    "cryoplant__cold_stage_capability__margin", "cryoplant__intercept_stage_capability__margin",
    "cryoplant__staged_drive__p_drive",
)


def material_channel_names(material: str) -> list[str]:
    """Every channel suffix evaluate_material_case returns for this material (static)."""
    names = set(ORACLE_TO_SUFFIX.values()) | {REFERENCE_NEW_OUTPUT}
    blocks = {
        "adapter": ("turn_length", "pack_area_per_turn"),
        "conductor": ("T_conductor", "ic_strand_op" if material == "nb3sn" else "ic_tape_op", "ic_cable_op",
                      "operating_fraction", "T_cs", "tcs_defined", "temperature_margin", "temp_rule_margin",
                      "fraction_rule_margin", "acceptance_margin", "status_code", "supported", "acceptance_pass",
                      "element_area_total", "element_copper_area"),
        "area": ("cable_area", "net_area", "gross_area", "fit_margin", "fit_margin_fraction",
                 "required_envelope_J", "cu_required", "cu_margin", "steel_required", "steel_margin",
                 "fit_pass", "cu_pass", "steel_pass"),
        "inventory": ("conductor_length", "element_length", "element_mass", "cu_mass", "steel_mass",
                      "solder_mass", "sc_cost", "materials_cost", "manufacturing_cost", "winding_capital",
                      "ampere_metres"),
        "pack_field": ("R_over_sqrt_A_wp", "ampere_floor", "ampere_floor_margin"),
        "winding_sum": ("cost",),
        "static_loads": ("area_cold", "q_radiation", "conduction_ref", "shield_static", "p_joint_ref"),
        "cold_stage": ("q_nuclear", "q_radiation", "q_conduction", "q_leads", "q_joints", "q_cold", "q_shield",
                       "k_integral"),
        "refrigeration": ("carnot_specific_power", "eta_cold", "p_in_cold", "p_in_shield", "p_in_total_MW",
                          "R_equiv_kW", "refrigerator_capital", "capacity_margin", "capacity_pass",
                          "green_extrapolated"),
        "staged_drive": ("p_drive",),
    }
    if material == "rebco":
        blocks["shape_branch"] = ("shape_mode",)
    for block, outputs in blocks.items():
        names.update(GLUE_BLOCKS[block] + o for o in outputs)
    return sorted(names)


def build_reuse_map() -> dict:
    """The channel-to-oracle map for all three prefixes (design 6.3/D3, review R4)."""
    suffix_to_oracle_name = {suffix: name for name, suffix in ORACLE_TO_SUFFIX.items()}
    material_channels = {}
    for material in MATERIALS:
        for suffix in material_channel_names(material):
            entry = material_channels.setdefault(suffix, {"materials": []})
            entry["materials"].append(material)
            entry["owner"] = channel_owner(suffix)
            entry["produced_by"] = _realization(suffix_to_oracle_name.get(suffix), suffix)
    verdicts = {local: {"owner": verdict_owner(local),
                        "predicate": ("reference package predicate IR (" + _CATALOG_ID(local) + ")"
                                      if local in PLANT_VERDICTS else "oracle_glue.NEW_VERDICTS"),
                        "operands": {name: f"{kind}:{key}" for name, (kind, key) in
                                     dict(bound, **REPOINTED_OPERANDS.get(local, {})).items()}}
                for local, (ir, bound) in {**PLANT_VERDICTS, **NEW_VERDICTS}.items()}
    counts = {}
    for entry in material_channels.values():
        counts[entry["owner"]] = counts.get(entry["owner"], 0) + 1
    verdict_counts = {}
    for entry in verdicts.values():
        verdict_counts[entry["owner"]] = verdict_counts.get(entry["owner"], 0) + 1
    section = {"channels": {s: channel_owner(s) for s in SECTION_5_2_CHANNELS},
               "verdicts": {v: verdict_owner(v) for v in verdicts}}
    return {
        "schema": "wi100-oracle-reuse/v1",
        "author": "T-015 independent oracle author (oracle_glue.py); generated by `oracle_glue.py --write-reuse`",
        "sources": ["work/active/WI-100_stellarator-material-variants/design.md sections 5.2, 6.3 (D2, D3)",
                    "work/orchestration/goals/magnet-material-comparison/evidence/design-review-wi100.md Recheck R4",
                    "work/orchestration/goals/magnet-material-comparison/evidence/plant-contract.md r4 sections 3-7"],
        "owners": {
            "plant": "unchanged plant calc; produced by the plant oracle family's function-level pieces "
                     "(import) or by the inline equation of verify_stellaris.compute re-derived in "
                     "oracle_glue._plant_chain (rederived). verify_stellaris.compute itself refuses every "
                     "material instance (plant REBCO law domain, verify_stellaris.py:902-909).",
            "round1": "Round 1 oracle exploration/magnet_materials/oracle.py, with B_peak_in from the glue leg (D3)",
            "glue": "oracle_glue functions and seam insertions (design 2.1-2.4, 2.8-2.9, D3, R4)",
            "composed": "downstream aggregation re-derived in oracle_glue._plant_chain from the plant "
                        "oracle's pieces with the rebound legs (power balance, rollups, CAS70/80, DCF, LCOE)",
        },
        "prefixes": {
            "reference": {"prefix": REFERENCE_PREFIX, "owner": "plant",
                          "produced_by": "oracle_entry.evaluate via oracle_glue.evaluate_reference_case "
                                         "(every channel of oracle_entry.ORACLE_OUTPUT_TO_CHANNEL)",
                          "exceptions": {REFERENCE_NEW_OUTPUT: {"owner": "glue", "value": 1.0,
                                                                "basis": "design 1.5 declared delta; review R4"}}},
            "rebco_material": {"prefix": MATERIAL_PREFIXES["rebco"], "channels": "see material_channels"},
            "nb3sn_material": {"prefix": MATERIAL_PREFIXES["nb3sn"], "channels": "see material_channels"},
            "unselected_material": {"owner": "witness", "basis": "design D4 and test 12: the prefix a case "
                                    "does not vary is covered by bit-equality with the manifest baseline "
                                    "record, not by an oracle run"},
        },
        "counts": {"material_channels": counts, "material_verdicts": verdict_counts,
                   "reference_channels": len(ORACLE_TO_SUFFIX) + 1},
        "section_5_2": section,
        "material_channels": dict(sorted(material_channels.items())),
        "material_verdicts": dict(sorted(verdicts.items())),
    }


def _CATALOG_ID(local):
    for cid, entry in _CATALOG.items():
        if entry["source_local_identity"] == local:
            return entry["definition_qualified_name"]
    return "?"


def _main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--write-reuse", action="store_true", help=f"write {REUSE_PATH.name}")
    args = parser.parse_args(argv)
    reuse = build_reuse_map()
    if args.write_reuse:
        REUSE_PATH.write_text(json.dumps(reuse, indent=1, sort_keys=False) + "\n")
        print(f"wrote {REUSE_PATH}")
    print(json.dumps(reuse["counts"], indent=1))


if __name__ == "__main__":
    _main()
