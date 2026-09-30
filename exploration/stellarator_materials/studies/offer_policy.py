"""Declared supplied-design offer policy for the WI-100 Round 2 plant study (contract r5 section 5).

Author: T-016 fresh policy author, brief
work/orchestration/goals/magnet-material-comparison/evidence/briefs/t016-policy-cases.md.
Specification: work/orchestration/goals/magnet-material-comparison/evidence/plant-contract.md (r5)
sections 3-8 (r5 rulings marked "(P)": least-heating ladder choice, divertor_heat_ok carried like
tbr_ok, the schedule resources and the IHX exchanger count re-supplied; notes Q1, Q5, Q13, Q14); entry keys and channels from work/active/WI-100_stellarator-material-variants/design.md
sections 4, 5.1, 5.2 and amendments A1-A8. Every rule below is [AGENT] unless it cites the contract.

The policy sits outside the evaluator. The evaluator is the independent composite oracle
exploration/stellarator_materials/oracle_glue.py (`evaluate_material_case`). For one design
(geometry cell, confinement cell, material, target peak field, size, variant) the mechanism is the
contract's (F14): propose -> evaluate the plant -> re-supply the dependent quantities -> evaluate
again, with the matched-fusion-power search on n_e0 at each operating-point ladder temperature run on
plant evaluations. The final supplied design is recorded; the study evaluates it without the policy.

Quantities the rules need from the plant (B_peak, acceptance margin, gross turn area, fusion power,
beta, required heating, stored energy, cold and intercept loads, every screened demand, every
facility requirement, the computed powers for the classes) are read from oracle evaluations, or from
the oracle's own component functions (`oracle_glue.conductor_peak_field`, the Round 1 pieces
`oracle_glue.r1.*`) called with the inputs the composite oracle passes them. The only plant arithmetic
written here is the rule's own inversion of the axis-field and bore relations (target B_peak -> B_axis
-> ampere-turns), copied in the oracle's statement order and always confirmed by an evaluation.

Speed: `vs._sustainment` (the plant oracle's ash fixed point, about 1 s per call) is memoized on its
exact inputs while the policy runs (`sustainment_cache`). The cache returns the oracle's own result
for identical inputs, so it changes no value; the policy-acceptance tests evaluate without it.

See policy-notes.md for every constant's source, the evaluation counts and every ambiguity resolved.
"""
from __future__ import annotations

import contextlib
import copy
import importlib.util
import json
import math
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
ORACLE_PATH = HERE.parent / "oracle_glue.py"


def load_oracle():
    name = "stellarator_materials_oracle_glue"
    if name in sys.modules:
        return sys.modules[name]
    spec = importlib.util.spec_from_file_location(name, ORACLE_PATH)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


og = load_oracle()
vs = og.vs  # the plant oracle module the composite oracle imports (verify_stellaris)
r1 = og.r1  # Round 1 oracle (exploration/magnet_materials/oracle.py) as the composite oracle loads it

MATERIALS = og.MATERIALS
PIN = dict(og.PIN_SUFFIX_INPUTS)  # suffix -> pinned Stellaris input (704 keys)
_PIN_OUT_RAW = json.loads(og.PIN_OUTPUTS_PATH.read_text())["outputs"]
PIN_OUT = {k[len(og.REFERENCE_PREFIX):]: v for k, v in _PIN_OUT_RAW.items() if k.startswith(og.REFERENCE_PREFIX)}

# ---------------------------------------------------------------------------------------------
# Contract section 5 constants
# ---------------------------------------------------------------------------------------------
#: Matched fusion power: the reference's p_fus (contract section 5 "2,653 MW"), taken exactly from the
#: pinned output plasma__fusion__p_fus of work/active/WI-080_.../integration/baseline.json.
P_FUS_MATCH = float(PIN_OUT["plasma__fusion__p_fus"])
TOL_P_FUS = 0.005  # relative, contract section 5
TOL_B_PEAK = 0.1  # T after turn rounding, contract section 5
BETA_FALLBACK_FRACTION = 0.95  # beta fallback at 0.95 x beta_limit, contract section 5
SEARCH_REL_TOL = 2.0e-4  # internal n_e0 search tolerance on p_fus (inside TOL_P_FUS) [AGENT]
BETA_SEARCH_REL_TOL = 2.0e-4  # internal tolerance on the beta-fallback density [AGENT]
AUX_ZERO_TOL_MW = 0.05  # driven-boundary tolerance on p_aux_required for the companion [AGENT]
LADDER_KEV = (11.0, 13.0, 14.63, 16.0, 18.0)  # T_i0 operating-point ladder, contract section 5 (F1a)
LADDER_TIE_KEV = 14.63  # r5 (P): equal least required heating goes to 14.63 keV (notes Q1)
TURN_CURRENT_A = 50_000.0  # held turn current, contract section 5
TURN_CURRENT_VARIANT_A = 86_000.0  # HELIAS 5-B cable, contract section 5 (Schauer 2013 Table 1)
BETA_LIMIT = float(PIN["beta_limit"])  # 0.05, contract section 3.1 (supported uses 0.05)
BETA_SECOND_VERDICT = 0.04  # recorded on every design (F13), contract section 3.1

SIZES = ((10.0, 1.0), (11.0, 1.1), (12.7, 1.3), (15.0, 1.5), (18.0, 1.8), (22.0, 2.2), (22.0, 1.8))
REFERENCE_SIZE = (12.7, 1.3)
HELIAS_SIZE = (22.0, 1.8)  # [A: HELIAS 5-B], contract section 5
NB3SN_FIELDS = (10.0, 11.0, 12.0, 13.0)  # 13 T edge, flagged (contract section 5)
REBCO_EQUAL_DUTY_FIELDS = (10.0, 11.0, 12.0)  # equal duty with the Nb3Sn design (F3)
REBCO_OWN_FIELDS = (18.0, 20.0, 22.0, 24.9)  # 24.9 = Stellaris reference duty

#: Geometry cells, contract section 3.2. The anchored ratio is the pinned Stellaris value.
GEOMETRIES = {
    "anchored": dict(peak_ratio=float(PIN["magnet__coil__peak_ratio"]), arm_slope=0.0),
    "helias": dict(peak_ratio=2.12, arm_slope=0.0),
    "arm": dict(peak_ratio=float(PIN["magnet__coil__peak_ratio"]), arm_slope=0.0641),
}
ARM_X_REF = 35.278  # contract section 3.2 r4 (C); design E7
F_REN_CELLS = (1.0, 1.4, 1.8)  # contract section 3.1
K_LINK_HELD = float(PIN["magnet__coil__k_link"])
K_LINK_VARIANT = 0.95  # HELIAS-line 0.92-0.97, contract section 3.2

#: Material prices, contract section 4 (USD2021 per metre of element).
PRICE_REBCO = 80.0
PRICE_REBCO_EVALUATED = (80.0, 30.0)  # every REBCO design, contract section 8 (F15)
PRICE_REBCO_VOLUME = 10.0  # re-selection price, contract section 8
PRICE_NB3SN = 8.0
PRICE_NB3SN_VARIANTS = (5.4, 13.5)  # on the anchored cells (brief)
EPS_INTRINSIC_HELD = -0.003  # contract section 4; design K6 (required key)
EPS_INTRINSIC_VARIANT = -0.006
#: CPI 2021 -> 2026 (Minneapolis Fed annual CPI, 2021 271.0 and estimated 2026 334.4,
#: knowledge/sources/federal_reserve_bank_of_minneapolis_annual_consumer_price/output.md:773, :808-812;
#: the plant's own 2026 basis, stellarator_plant.sysml:413-414). Contract section 6 (F12), design K14.
CPI_2021_TO_2026 = 334.4 / 271.0

#: Fixed cold-stage rating list [W], Round 1's (exploration/magnet_materials/studies/offer_policy.py:43).
RATINGS_W = (1e3, 1.5e3, 2e3, 3e3, 5e3, 7.5e3, 10e3, 15e3, 20e3, 30e3, 50e3, 75e3)
#: Package re-supply margin and purchase scaling, contract section 5 (F2, F8) [U].
PACKAGE_MARGIN = 1.05
PURCHASE_EXPONENT = 0.7
PURCHASE_EXPONENT_VARIANTS = (0.5, 1.0)
#: Heating rule, contract section 5 [U]: max(100 MW, 1.1 x p_aux_required / 0.5), up to 10 MW.
HEATING_FLOOR_MW = 100.0
HEATING_FACTOR = 1.1
HEATING_STEP_MW = 10.0
#: Structure-mass rule, contract section 5 [U]: 11,615.6 t x (W_mag / 111 GJ) (oracle_glue.structure_mass_rule).
STRUCTURE_VARIANTS = {"m_support_x0.5": 0.5, "m_support_x2": 2.0}
PACK_STEP_M = 0.005  # wp_side rounded up to 5 mm (contract section 5; K15 next step on exact landing)
ALLOC_STEP_M = 0.01  # coil_t and interior_y rounded up to 10 mm (contract section 5)

# ---------------------------------------------------------------------------------------------
# Construction rules (contract section 4): Round 1's P and C, exploration/magnet_materials/studies/
# offer_policy.py:127-143 (P: EU DEMO layer-1 calibrated; C: Stellaris Table 7 fractions of the
# 0.36 m / 308-turn pack at 50 kA and 24.9 T, unrounded as Round 1 A2).
# ---------------------------------------------------------------------------------------------
_A_S = 0.36 * 0.36 * 1e6 / 308.0
CONSTRUCTIONS = {
    "P": dict(cabling_factor=0.97, cable_void=0.20, ins_fraction=0.237, J_cu_rule=93.4, cu_void=0.10,
              cu_per_kA_rule=0.0, steel_per_kA_rule=12.66, B_steel_ref=12.04, steel_B_scaling=1.0,
              misc_per_kA=1.1077, solder_per_kA=0.0),
    "C": dict(cabling_factor=1.0, cable_void=0.0, ins_fraction=0.0, J_cu_rule=0.0, cu_void=0.0,
              cu_per_kA_rule=0.35 * _A_S / 50.0, steel_per_kA_rule=0.36 * _A_S / 50.0, B_steel_ref=24.9,
              steel_B_scaling=1.0, misc_per_kA=0.08 * _A_S / 50.0, solder_per_kA=0.12 * _A_S / 50.0),
}
NATIVE_CONSTRUCTION = {"nb3sn": "P", "rebco": "C"}
RULE_KEYS = ("J_cu_rule", "cu_void", "cu_per_kA_rule", "steel_per_kA_rule", "B_steel_ref", "steel_B_scaling")

# ---------------------------------------------------------------------------------------------
# Variants (contract sections 3-8; brief). Design-changing variants re-run the policy; the others
# re-evaluate a recorded design with changed inputs only.
# ---------------------------------------------------------------------------------------------
DESIGN_VARIANTS = ("strain_-0.6", "common-P", "k_link_0.95", "turn_current_86kA")
REEVALUATION_VARIANTS = ("m_support_x0.5", "m_support_x2", "purchase_exp_0.5", "purchase_exp_1.0",
                         "cpi_2021_2026", "price_30", "price_10", "nb3sn_price_5.4", "nb3sn_price_13.5")

# ---------------------------------------------------------------------------------------------
# Supplied-package tables (contract section 5 "Offered-capacity packages and occupancy"; design 5.1)
# ---------------------------------------------------------------------------------------------
#: Screened ratings: (rating input key, screen margin channel). Demand = supplied rating - margin
#: (oracle_capability.screen: margin = rating - demand). Re-supplied at demand x 1.05.
SCREENED_RATINGS = (
    ("heat_transport__mdot_loop_rated", "heat_transport__helium_flow_capability__margin"),
    ("heat_transport__equipment_helium_design_shaft_MW", "heat_transport__helium_pumping_capability__margin"),
    ("heat_transport__helium_rated_dp_Pa", "heat_transport__helium_pressure_rise_capability__margin"),
    ("heat_transport__helium_rated_electric_MW", "heat_transport__helium_electric_capability__margin"),
    ("heat_transport__equipment_salt_design_flow_kg_s", "heat_transport__salt_flow_capability__margin"),
    ("heat_transport__equipment_salt_design_head_m", "heat_transport__salt_head_capability__margin"),
    ("turbine__selected_gross_MWe", "turbine__turbine_gross_capability__margin"),
    ("turbine__hp_turbine__rated_flow_kg_s", "turbine__hp_flow_capability__margin"),
    ("turbine__hp_turbine__rated_shaft_MW", "turbine__hp_shaft_capability__margin"),
    ("turbine__lp_turbine__rated_flow_kg_s", "turbine__lp_flow_capability__margin"),
    ("turbine__lp_turbine__rated_shaft_MW", "turbine__lp_shaft_capability__margin"),
    ("turbine__main_steam_generator__installed_UA_MW_K", "turbine__main_UA_capability__margin"),
    ("turbine__reheater__installed_UA_MW_K", "turbine__reheat_UA_capability__margin"),
    ("turbine__condenser__rated_rejection_MW", "turbine__condenser_rejection_capability__margin"),
    ("turbine__condensate_pump__rated_flow_kg_s", "turbine__condensate_flow_capability__margin"),
    ("turbine__condensate_pump__rated_dp_MPa", "turbine__condensate_pressure_rise_capability__margin"),
    ("turbine__condensate_pump__rated_electric_MW", "turbine__condensate_electric_capability__margin"),
    ("turbine__feedwater_pump__rated_flow_kg_s", "turbine__feedwater_flow_capability__margin"),
    ("turbine__feedwater_pump__rated_dp_MPa", "turbine__feedwater_pressure_rise_capability__margin"),
    ("turbine__feedwater_pump__rated_electric_MW", "turbine__feedwater_electric_capability__margin"),
    ("heat_rejection__rated_rejection_MW", "heat_rejection__water_rejection_capability__margin"),
    ("heat_rejection__rated_water_flow_kg_s", "heat_rejection__water_flow_capability__margin"),
    ("heat_rejection__rated_water_head_m", "heat_rejection__water_head_capability__margin"),
    ("heat_rejection__rated_water_electric_MW", "heat_rejection__water_electric_capability__margin"),
    ("electric_plant__installed_gross_rating_MWe", "electric_plant__electric_gross_capability__margin"),
    ("power_supplies__rated_tf_MWe", "power_supplies__magnet_tf_electric_capability__margin"),
    ("power_supplies__rated_pf_MWe", "power_supplies__magnet_pf_electric_capability__margin"),
    ("cryoplant__rated_direct_electric_MW", "cryoplant__direct_electric_capability__margin"),
)
#: Offered conditions (the WI-080 state screens require rated == actual to 8 ulp,
#: exploration/stellarator_e2e/oracle_capability.py:292-299): re-supplied at the actual value, not x 1.05.
#: The helium design-point suction (a cost design point, equal to the rated suction at the pin) follows it.
OFFERED_STATES = (
    ("heat_transport__rated_helium_suction_K", "heat_transport__primary_loop__T_comp_in"),
    ("heat_transport__rated_helium_suction_Pa", "heat_transport__equipment__circulator_suction_Pa"),
    ("heat_transport__equipment_helium_design_suction_Pa", "heat_transport__equipment__circulator_suction_Pa"),
    ("heat_transport__rated_helium_hot_K", "heat_transport__primary_loop__T_out"),
    ("heat_transport__rated_salt_return_C", "heat_transport__equipment__salt_return_C"),
    ("turbine__rated_steam_salt_return_C", "heat_transport__equipment__salt_return_C"),
    ("heat_rejection__rated_water_condenser_C", "turbine__matched_cycle__t_condensate_C"),
)
#: Represented coolant fill (represented_coolant_fill_ok): purchased mass = 1.05 x required fill.
PURCHASED_MASSES = (
    ("heat_transport__equipment_helium_purchased_mass_kg", "heat_transport__equipment__helium_required_fill_mass_kg"),
    ("heat_transport__equipment_salt_purchased_mass_kg", "heat_transport__equipment__salt_required_fill_mass_kg"),
)
#: Purchase-cost scaling: package -> (purchase key, rating key or None). captured x (rating/captured)^0.7.
PURCHASES = {
    "turbine": ("turbine__purchase_cost_per_module", "turbine__selected_gross_MWe"),
    "heat_rejection": ("heat_rejection__purchase_cost_per_module", "heat_rejection__rated_rejection_MW"),
    "power_supplies": ("power_supplies__purchase_cost_per_module", "power_supplies__rated_tf_MWe"),
    "divertor": ("divertor__purchase_cost_per_module", None),  # no screened rating: held (notes Q10)
}


def _class_map():
    """Class key -> channel it was captured from (WI-079 public-defaults.json native_channel)."""
    path = (ROOT / "work" / "active" / "WI-079_supplied-equipment-design-bases-for-residual-costs"
            / "evidence" / "public-defaults.json")
    rows = json.loads(path.read_text())["inputs"]
    out = {}
    for key, row in rows.items():
        if "_class_" in key:
            out[key] = row["native_channel"][len(og.REFERENCE_PREFIX):]
    if len(out) != 22:
        raise RuntimeError(f"expected the 22 power classes, found {len(out)}")
    return out


CLASS_MAP = _class_map()

#: Facility re-supply (notes Q12). Design-dependent rooms follow their requirement channels x 1.05.
DIRECTIONS = ("east", "north", "west", "south")
FACILITY_SCALED_ROOMS = tuple(f"sector_wing_{d}" for d in DIRECTIONS)
FACILITY_LINKS = tuple(f"sector_link_{d}" for d in DIRECTIONS)
FACILITY_OCCUPANCY_ROOMS = ("administration", "control", "security")
SECTOR_ALLOCATIONS = (
    ("buildings__clean_positions", "buildings__layout__initial_clean_required"),
    ("buildings__dirty_buffer_positions", "buildings__layout__dirty_buffer_required"),
    ("buildings__dirty_store_positions", "buildings__layout__dirty_store_required"),
)
PIN_PARCEL_X_MIN = -186.9046987566545  # facility entering datum (oracle_facilities.py DEFAULTS)
PIN_PARCEL_Y_MIN = -256.9046987566545
NUCLEAR_WALL = float(PIN["buildings__nuclear_wall"])

#: Re-supplied quantities with no cost response in the plant (contract section 5: `free_capacity`).
#: Turbine and heat-rejection amounts scale with gross and rejection ratings only; the loop, helium and
#: child-equipment ratings enter screens only (oracle_glue._plant_chain cost statements); the intercept
#: rating is uncosted in the material instances (design D17).
FREE_CAPACITY = (
    "cryoplant__rated_intercept_W", "heat_transport__mdot_loop_rated", "heat_transport__helium_rated_dp_Pa",
    "heat_transport__helium_rated_electric_MW", "turbine__hp_turbine__rated_flow_kg_s",
    "turbine__hp_turbine__rated_shaft_MW", "turbine__lp_turbine__rated_flow_kg_s", "turbine__lp_turbine__rated_shaft_MW",
    "turbine__main_steam_generator__installed_UA_MW_K", "turbine__reheater__installed_UA_MW_K",
    "turbine__condenser__rated_rejection_MW", "turbine__condensate_pump__rated_flow_kg_s",
    "turbine__condensate_pump__rated_dp_MPa", "turbine__condensate_pump__rated_electric_MW",
    "turbine__feedwater_pump__rated_flow_kg_s", "turbine__feedwater_pump__rated_dp_MPa",
    "turbine__feedwater_pump__rated_electric_MW", "heat_rejection__rated_water_flow_kg_s",
    "heat_rejection__rated_water_head_m", "heat_rejection__rated_water_electric_MW",
    "cryoplant__rated_direct_electric_MW", "power_supplies__rated_pf_MWe",
    "buildings__sector_service_teams", "buildings__initial_receipt_lead_days",
    "buildings__component_receipt_lead_days",
)

MAX_RESUPPLY_ITERATIONS = 12
#: r5 (P), notes Q14: the IHX exchanger count joins the re-supplied set (the plant's only IHX lever).
IHX_COUNT_KEY = "heat_transport__n_loops"
MAX_MAGNET_ITERATIONS = 40


class PolicyError(Exception):
    """A policy rule that cannot be applied (always a declared failure, never silent)."""


# ---------------------------------------------------------------------------------------------
# The sustainment memo (identity of results; see the module docstring)
# ---------------------------------------------------------------------------------------------
class _Tracker(dict):
    def __init__(self, *a, **k):
        super().__init__(*a, **k)
        self.read = set()

    def __getitem__(self, key):
        self.read.add(key)
        return super().__getitem__(key)


def _sustainment_keys():
    tracker = _Tracker(vs.IN)
    tracker["sustain_ash_frac"] = tracker.get("sustain_ash_frac", 0.2002)
    vs._sustainment(tracker, 425.0, 9.0)
    return tuple(sorted(tracker.read))


_ORIGINAL_SUSTAINMENT = vs._sustainment
_SUSTAIN_KEYS = None
_SUSTAIN_MEMO: dict = {}
_LAST_SUSTAIN: dict = {}
MEMO_STATS = {"calls": 0, "misses": 0}


def _memo_sustainment(p, V, B_axis):
    key = (V, B_axis) + tuple(p[k] for k in _SUSTAIN_KEYS)
    MEMO_STATS["calls"] += 1
    hit = _SUSTAIN_MEMO.get(key)
    _LAST_SUSTAIN.clear()
    if hit is None:
        MEMO_STATS["misses"] += 1
        try:
            hit = _ORIGINAL_SUSTAINMENT(p, V, B_axis)
        except Exception as exc:  # the refusal is part of the oracle's result for these inputs
            hit = exc
        if len(_SUSTAIN_MEMO) > 20000:
            _SUSTAIN_MEMO.clear()
        _SUSTAIN_MEMO[key] = hit
    if isinstance(hit, Exception):
        raise type(hit)(*hit.args)
    _LAST_SUSTAIN.update(value=(dict(hit), V, B_axis), point=(p["n_e0"], p["T_i0"], p["R"], p["a"]))
    return dict(hit)


@contextlib.contextmanager
def sustainment_cache(enabled: bool = True):
    """Memoize vs._sustainment on its exact inputs while the policy runs (identical results)."""
    global _SUSTAIN_KEYS
    if not enabled:
        yield
        return
    if _SUSTAIN_KEYS is None:
        _SUSTAIN_KEYS = _sustainment_keys()
    previous = vs._sustainment
    vs._sustainment = _memo_sustainment
    try:
        yield
    finally:
        vs._sustainment = previous


# ---------------------------------------------------------------------------------------------
# Evaluation with counting
# ---------------------------------------------------------------------------------------------
class Evaluator:
    """Counts oracle evaluations; domain refusals become {'refusal': text} (contract section 7 item 1)."""

    def __init__(self):
        self.count = 0

    def __call__(self, inputs: dict, material: str) -> dict:
        self.count += 1
        try:
            return og.evaluate_material_case(inputs, material)
        except og.GlueOracleError:
            raise  # an input the policy should never produce: a policy defect, not a design outcome
        except (ValueError, RuntimeError, ZeroDivisionError, OverflowError) as exc:
            return {"refusal": f"{type(exc).__name__}: {exc}"}


# ---------------------------------------------------------------------------------------------
# Cells, assumptions and the held part of a design
# ---------------------------------------------------------------------------------------------
def cell_inputs(geometry: str, f_ren: float, variant: str = "none") -> dict:
    g = GEOMETRIES[geometry]
    k_link = K_LINK_VARIANT if variant == "k_link_0.95" else K_LINK_HELD
    return {"plasma__f_ren": float(f_ren), "magnet__coil__peak_ratio": g["peak_ratio"],
            "magnet__coil__arm_slope": g["arm_slope"], "magnet__coil__arm_x_ref": ARM_X_REF,
            "magnet__coil__k_link": k_link, "beta_limit": BETA_LIMIT}


def material_assumptions(material: str, variant: str = "none") -> dict:
    """Material facts (oracle_glue.material_facts, design E7/E8) plus the policy's rule choices."""
    facts = og.material_facts(material)
    construction = "P" if (variant == "common-P" or material == "nb3sn") else NATIVE_CONSTRUCTION[material]
    out = dict(facts=facts, construction=construction, construction_rule=dict(CONSTRUCTIONS[construction]),
               price=PRICE_NB3SN if material == "nb3sn" else PRICE_REBCO)
    if material == "nb3sn":
        out["eps_intrinsic"] = EPS_INTRINSIC_VARIANT if variant == "strain_-0.6" else EPS_INTRINSIC_HELD
    return out


def turn_current(variant: str) -> float:
    return TURN_CURRENT_VARIANT_A if variant == "turn_current_86kA" else TURN_CURRENT_A


# ---------------------------------------------------------------------------------------------
# Magnet sizing (contract section 5 rows: target peak field, element count, pack side, allocation)
# ---------------------------------------------------------------------------------------------
def _law(material: str, facts: dict) -> dict:
    names = (og.REBCO_LAW + og.REBCO_BOUNDS) if material == "rebco" else (og.NB3SN_LAW + og.NB3SN_BOUNDS)
    return {name: float(facts["magnet__" + name]) for name in names}


def conductor_eval(material: str, asm: dict, n: float, I_turn: float, B: float) -> dict:
    """The Round 1 conductor piece exactly as the composite oracle binds it (oracle_glue.py:413-426)."""
    facts = asm["facts"]
    law = _law(material, facts)
    T_supply = float(facts["cryoplant__T_cold_cryo"])
    if material == "rebco":
        shape = og.rebco_shape_branch(dict(B_peak_in=B, B_knot_max_in=law["B_knot_max"]))
        return r1.rebco_cable_critical_surface(dict(law, n_elements=float(n), turn_current=I_turn, B_peak=B,
                                                    T_supply=T_supply, shape_mode=shape["shape_mode"]))
    return r1.nb3sn_cable_critical_surface(dict(law, n_elements=float(n), turn_current=I_turn, B_peak=B,
                                                T_supply=T_supply, eps_intrinsic=float(asm["eps_intrinsic"])))


def smallest_n(material: str, asm: dict, I_turn: float, B: float, n_cap: int = 5_000_000):
    """Smallest integer element count whose acceptance margin (the Round 1 rule) is >= 0.

    Round 1 offer rule (contract section 5; Round 1 offer_policy.smallest_n): support status is not
    required here, so an unsupported point still gets an offer, filed `unsupported` by its status.
    """
    def margin(n):
        return conductor_eval(material, asm, n, I_turn, B)["acceptance_margin"]

    lo, hi = 1, 2
    while margin(hi) < 0.0:
        lo, hi = hi, hi * 2
        if hi > n_cap:
            return None
    if margin(lo) >= 0.0:
        return lo
    while hi - lo > 1:  # margin(lo) < 0 <= margin(hi); acceptance margin rises with n
        mid = (lo + hi) // 2
        if margin(mid) >= 0.0:
            hi = mid
        else:
            lo = mid
    return hi


def round_up_1e6(x: float) -> float:
    """Round an area up to the next 1e-6 mm^2 with a float guard (Round 1 design D1)."""
    k = math.ceil(x * 1e6)
    r = k / 1e6
    while r < x:
        k += 1
        r = k / 1e6
    return r


def construction_areas(material: str, asm: dict, n: int, I_turn: float, B: float) -> dict:
    """The construction rule's per-turn areas at the design's current and peak field (Round 1 D1)."""
    c = asm["construction_rule"]
    cond = conductor_eval(material, asm, n, I_turn, B)
    if c["J_cu_rule"] > 0.0:
        cu = max(0.0, I_turn / c["J_cu_rule"] - cond["element_copper_area"]) / (1.0 - c["cu_void"])
    else:
        cu = c["cu_per_kA_rule"] * I_turn / 1000.0
    scale = B / c["B_steel_ref"] if c["steel_B_scaling"] != 0.0 else 1.0
    steel = c["steel_per_kA_rule"] * (I_turn / 1000.0) * scale
    misc = c["misc_per_kA"] * I_turn / 1000.0
    solder = c["solder_per_kA"] * I_turn / 1000.0
    areas = dict(cabling_factor=c["cabling_factor"], cable_void=c["cable_void"], cu_space=round_up_1e6(cu),
                 steel_area=round_up_1e6(steel), misc_area=round_up_1e6(misc),
                 solder_area=round_up_1e6(solder) if solder > 0.0 else 0.0, ins_fraction=c["ins_fraction"])
    areas.update({k: c[k] for k in RULE_KEYS})
    return areas


def gross_turn_area(material: str, asm: dict, n: int, areas: dict, I_turn: float, B: float,
                    available_area: float = 1.0) -> dict:
    cond = conductor_eval(material, asm, n, I_turn, B)
    return r1.winding_turn_area_screen(dict(
        {k: areas[k] for k in og.CONSTRUCTION}, turn_current=I_turn, B_peak=B, available_area=available_area,
        element_area=cond["element_area_total"], element_copper_area=cond["element_copper_area"]))


def _plant(key: str, design: dict):
    return design[key] if key in design else PIN[key]


def radial_centre(design: dict) -> float:
    """r_coil_centre in the oracle's statement order (oracle_glue.py:533-556)."""
    a = design["plasma__a"]
    vacuum_or = a + _plant("blanket__first_wall__vacuum_t", design)
    firstwall_or = vacuum_or + _plant("blanket__first_wall__firstwall_t", design)
    blanket_or = firstwall_or + _plant("blanket__blanket_t", design)
    reflector_or = blanket_or + _plant("blanket__reflector_t", design)
    ht_shield_or = reflector_or + _plant("shield__ht_shield_t", design)
    structure_or = ht_shield_or + _plant("structure__structure_t", design)
    gap1_or = structure_or + _plant("vessel__gap1_t", design)
    vessel_or = gap1_or + _plant("vessel__vessel_t", design)
    return vessel_or + design["magnet__coil__coil_t"] / 2.0


def axis_field(design: dict, turns: float, I_turn: float) -> float:
    """'Coil Set Axis Field' in the oracle's order (oracle_glue.py:561-562)."""
    return (_plant("magnet__field_calc__mu0", design) * design["magnet__coil__k_link"]
            * _plant("magnet__coil__n_coils", design) * (turns * I_turn)
            / (_plant("magnet__field_calc__two_pi", design) * design["plasma__R"]))


def peak_field(design: dict, turns: float, I_turn: float) -> dict:
    """B_peak through the composite oracle's own arm-slot function (oracle_glue.conductor_peak_field)."""
    return og.conductor_peak_field(dict(
        B_axis_in=axis_field(design, turns, I_turn), peak_ratio_in=design["magnet__coil__peak_ratio"],
        R_in=design["plasma__R"], a_coil_in=radial_centre(design), R_ref_in=PIN["magnet__coil__R_ref"],
        a_coil_ref_in=PIN["magnet__coil__a_coil_ref"], wp_side_in=design["magnet__winding_pack__wp_side"],
        arm_slope_in=design["magnet__coil__arm_slope"], arm_x_ref_in=design["magnet__coil__arm_x_ref"]))


def turns_for_target(design: dict, B_target: float, I_turn: float) -> tuple[int, float]:
    """Contract section 5: target B_peak under the design's geometry and own bore factor -> B_axis ->
    ampere-turns at the design's R (k_link, n_coils held) -> turns = ampere-turns / I rounded up."""
    unit = peak_field(design, 1.0, I_turn)  # B_peak is linear in turns at fixed geometry
    per_turn = unit["B_peak"]
    B_axis_target = B_target / (unit["ratio_eff"] * unit["bore_norm"])
    ampere_turns = (B_axis_target * _plant("magnet__field_calc__two_pi", design) * design["plasma__R"]
                    / (_plant("magnet__field_calc__mu0", design) * design["magnet__coil__k_link"]
                       * _plant("magnet__coil__n_coils", design)))
    turns = math.ceil(ampere_turns / I_turn - 1e-9)
    # Rounded up (contract section 5), unless that misses the +-0.1 T tolerance while one turn fewer
    # meets it: where one turn exceeds 0.1 T (R 10 m at 50 kA; 86 kA below R 15 m) rounding up alone
    # cannot always honour the stated tolerance (notes Q18).
    if (peak_field(design, turns, I_turn)["B_peak"] - B_target > TOL_B_PEAK
            and B_target - peak_field(design, turns - 1, I_turn)["B_peak"] <= TOL_B_PEAK):
        turns -= 1
    return int(turns), per_turn


def pack_side(turns: int, gross_mm2: float) -> float:
    """sqrt(turns x gross) rounded up to 5 mm; exact landing takes the next step (design K15)."""
    s = math.sqrt(turns * gross_mm2) / 1000.0
    k = math.floor(s / PACK_STEP_M + 1e-12) + 1
    side = k / 200.0
    while side * side * 1e6 < turns * gross_mm2:  # float guard: pack_area_ok by construction
        k += 1
        side = k / 200.0
    return side


def allocation(side: float) -> tuple[float, float]:
    """coil_t and interior_y = side x (1 + internal) + 2 ground + 2 clearance + 2 wall, up to 10 mm.

    Contract section 5 literally ("same for interior_y"); the plant's y cavity excludes the walls, so
    interior_y carries 2 x wall of surplus with no cost response (notes Q6). Each value is bumped by a
    step if the oracle's own fit arithmetic (verify_stellaris._winding_fit) would fall below zero.
    """
    ground = PIN["magnet__winding_pack__ground_insulation"]
    clearance = PIN["magnet__casing__assembly_clearance"]
    wall = PIN["magnet__casing__wall_thickness"]
    out = []
    for axis in ("x", "y"):
        internal = PIN[f"magnet__winding_pack__internal_build_{axis}"]
        need = side * (1.0 + internal) + 2 * ground + 2 * clearance + 2 * wall
        k = math.ceil(need / ALLOC_STEP_M - 1e-9)
        while True:
            value = k / 100.0
            nominal = side
            required = nominal + nominal * internal + 2 * ground + 2 * clearance
            cavity = value - 2 * wall if axis == "x" else value
            if cavity - required >= 0.0 and value >= need - 1e-12:
                break
            k += 1
        out.append(value)
    return out[0], out[1]


def size_magnet(material: str, asm: dict, design: dict, B_target: float, I_turn: float,
                fixed_turns: int | None = None) -> dict:
    """Fixed point of turns, element count, per-turn areas, pack side and allocation.

    Free iteration first; if it cycles, a monotone pass where pack side and allocation can only grow
    (which terminates). Returns the magnet keys plus a trace.
    """
    d = dict(design)
    d.setdefault("magnet__winding_pack__wp_side", 0.36)
    d.setdefault("magnet__coil__coil_t", 0.42)
    seen = []
    mode = "free"
    for it in range(MAX_MAGNET_ITERATIONS):
        if fixed_turns is None:
            turns, _ = turns_for_target(d, B_target, I_turn)
        else:
            turns = int(fixed_turns)
        B = peak_field(d, turns, I_turn)["B_peak"]
        n = smallest_n(material, asm, I_turn, B)
        if n is None:
            raise PolicyError(f"no element count meets the acceptance rule at {B:.4f} T")
        areas = construction_areas(material, asm, n, I_turn, B)
        gross = gross_turn_area(material, asm, n, areas, I_turn, B)["gross_area"]
        side = pack_side(turns, gross)
        coil_t, interior_y = allocation(side)
        if mode == "monotone":
            side = max(side, d["magnet__winding_pack__wp_side"])
            coil_t = max(coil_t, d["magnet__coil__coil_t"])
            interior_y = max(interior_y, d.get("magnet__casing__interior_y", 0.0))
        state = (turns, n, side, coil_t, interior_y)
        if seen and state == seen[-1]:
            break
        if state in seen and mode == "free":
            mode = "monotone"
        seen.append(state)
        d["magnet__winding_pack__wp_side"] = side
        d["magnet__coil__coil_t"] = coil_t
        d["magnet__casing__interior_y"] = interior_y
    else:
        raise PolicyError("magnet sizing did not reach a fixed point")
    turns, n, side, coil_t, interior_y = seen[-1]
    d.update({"magnet__coil__reference_turns": float(turns), "magnet__coil__turn_current": I_turn,
              "magnet__n_elements": float(n), "magnet__winding_pack__wp_side": side,
              "magnet__coil__coil_t": coil_t, "magnet__casing__interior_y": interior_y})
    for k in og.CONSTRUCTION:
        d["magnet__" + k] = areas[k]
    B = peak_field(d, turns, I_turn)
    trace = dict(magnet_iterations=len(seen), magnet_mode=mode, B_peak_policy=B["B_peak"],
                 R_over_sqrt_A_wp=B["R_over_sqrt_A_wp"], gross_area_mm2=gross,
                 pack_fill=(turns * gross) / (side * side * 1e6))
    return dict(design=d, trace=trace)


# ---------------------------------------------------------------------------------------------
# Operating point (contract section 5 row "Operating point"; F1a, F1b)
# ---------------------------------------------------------------------------------------------
def _ch(case: dict, name: str) -> float:
    return float(case["channels"][name])


def _n_guess(design: dict, T: float) -> float:
    """Starting density: the pinned point scaled to this volume and temperature (search seed only)."""
    V_ref = 2.0 * PIN["plasma__geom__pi"] ** 2 * PIN["plasma__R"] * PIN["plasma__a"] ** 2
    V = 2.0 * PIN["plasma__geom__pi"] ** 2 * design["plasma__R"] * design["plasma__a"] ** 2
    I_ref = vs._profile_integral(PIN["plasma__alpha_n"], PIN["plasma__alpha_T"], PIN["plasma__T_i0"])
    I_T = vs._profile_integral(PIN["plasma__alpha_n"], PIN["plasma__alpha_T"], T)
    return PIN["plasma__n_e0"] * math.sqrt(V_ref / V * I_ref / I_T)


def _plasma(case: dict, design: dict) -> dict:
    """p_fus, p_aux_required and beta of an evaluation.

    From the channels when the plant evaluates. When the plant refuses after its plasma solve (a
    primary-loop or exchanger domain at a very large heating load), the search still needs the plasma
    values to navigate: they are read from the oracle's own sustainment result for this point (the
    memo's last call) through the plant's fusion-power and beta statements (oracle_glue.py:616-620,
    :954). Search navigation only: a refused point is never recorded as a supported design.
    """
    if "refusal" not in case:
        return dict(p_fus=_ch(case, "plasma__fusion__p_fus"), p_aux=_ch(case, "plasma__sustain__p_aux_required"),
                    beta=_ch(case, "plasma__beta_calc__beta"), evaluable=True, plasma=True)
    last = _LAST_SUSTAIN.get("value")
    msg = case["refusal"]
    if last is None or "sustainment" in msg or _LAST_SUSTAIN.get("point") != (design["plasma__n_e0"],
                                                                              design["plasma__T_i0"],
                                                                              design["plasma__R"],
                                                                              design["plasma__a"]):
        return dict(evaluable=False, plasma=False, refusal=msg)
    sust, V, B_axis = last
    fus_I = vs._profile_integral(PIN["plasma__alpha_n"], PIN["plasma__alpha_T"], design["plasma__T_i0"])
    p_fus = sust["n_D0"] * sust["n_T0"] * fus_I * PIN["plasma__E_fus"] * V * 1.0e-6
    beta = 2.0 * PIN["plasma__beta_calc__mu0"] * sust["p_avg"] / (B_axis ** 2)
    return dict(p_fus=p_fus, p_aux=sust["p_aux_required"], beta=beta, evaluable=False, plasma=True, refusal=msg)


class _Probe:
    """Evaluations of one design at (n_e0, T) with a small cache of plasma values."""

    def __init__(self, evaluate, material, design):
        self.evaluate, self.material, self.design = evaluate, material, design
        self.cache = {}

    def __call__(self, n: float, T: float):
        key = (n, T)
        if key not in self.cache:
            d = dict(self.design, **{"plasma__n_e0": n, "plasma__T_i0": T})
            case = self.evaluate(d, self.material)
            self.cache[key] = (case, _plasma(case, d))
        return self.cache[key]


def _matched(probe: _Probe, T: float, n0: float, max_evals: int = 14) -> dict:
    """Lowest-density n_e0 at which p_fus = P_FUS_MATCH at T_i0 = T (secant in log-log, bracketed).

    p_fus rises with n_e0 until helium-ash dilution turns it over; a maximum below the target, or a
    plasma refusal (non-positive fuel, ash non-convergence) before it, makes matched power
    unattainable at this T (notes Q3).
    """
    lt = math.log(P_FUS_MATCH)
    good = []  # (log n, log p_fus)
    upper = math.inf  # plasma-refusal bound on log n
    x = math.log(n0)
    evals = 0
    while evals < max_evals:
        evals += 1
        case, pl = probe(math.exp(x), T)
        if not pl["plasma"]:
            upper = min(upper, x)
            below = [g for g in good if g[1] < lt]
            x = 0.5 * (x + max(g[0] for g in below)) if below else x - 0.7
            if below and upper - max(g[0] for g in below) < 1e-4:
                break
            continue
        p = pl["p_fus"]
        if abs(p / P_FUS_MATCH - 1.0) <= SEARCH_REL_TOL:
            return dict(T=T, matched=True, n_e0=math.exp(x), case=case, **pl)
        good.append((x, math.log(p)))
        good.sort()
        below = [g for g in good if g[1] < lt]
        above = [g for g in good if g[1] > lt]
        if len(good) >= 2 and not above:
            ys = [g[1] for g in good]
            i = ys.index(max(ys))
            if 0 < i < len(ys) - 1 and len(good) >= 3:
                break  # an interior maximum below the target: ash-limited
            if upper < math.inf and i == len(ys) - 1:
                (xa, ya), (xb, yb) = good[-2], good[-1]
                slope = (yb - ya) / (xb - xa) if xb != xa else 0.0
                if upper - xb < 0.01 or yb + max(slope, 0.0) * (upper - xb) < lt - 1e-3:
                    break  # even extrapolated to the plasma-refusal bound it stays below the target
        if below and above:
            a = max(below)
            b = min(above, key=lambda g: g[0])
            if b[0] > a[0]:
                xn = a[0] + (lt - a[1]) * (b[0] - a[0]) / (b[1] - a[1])
                xn = min(max(xn, a[0] + 0.02 * (b[0] - a[0])), b[0] - 0.02 * (b[0] - a[0]))
            else:  # the target is crossed downward: past the maximum; bisect toward lower density
                xn = 0.5 * (a[0] + b[0])
        elif len(good) >= 2:
            (xa, ya), (xb, yb) = good[-2], good[-1]
            slope = (yb - ya) / (xb - xa) if xb != xa else 2.0
            if slope <= 0.05:  # flat or falling: the maximum is at or below these densities
                xn = 0.5 * (xa + xb) if slope < 0 else xb + 0.2
                if slope < 0 and not above:
                    xn = xa - 0.05
            else:
                xn = good[-1][0] + (lt - good[-1][1]) / min(max(slope, 0.25), 6.0)
        else:
            xn = x + (lt - math.log(p)) / 2.0
        xn = min(max(xn, x - 1.0), x + 1.0)
        if xn >= upper:
            xn = 0.5 * (max(g[0] for g in good) + upper) if good else upper - 0.5
        x = xn
    best = max(good, key=lambda g: g[1]) if good else None
    return dict(T=T, matched=False, reason="p_fus maximum below the matched power" if good else "plasma refusal",
                p_fus_max_seen=math.exp(best[1]) if best else None, n_best=math.exp(best[0]) if best else None)


def _feasible(pl: dict, beta_cap: float) -> bool:
    return pl["plasma"] and pl["beta"] <= beta_cap and pl["p_aux"] >= 0.0


def _driven_max(probe: _Probe, T: float, seed: float, beta_cap: float, max_evals: int = 18,
                rising_to: float | None = None):
    """Largest p_fus at T with beta <= beta_cap, p_aux_required >= 0 and an evaluable plasma.

    The admissible densities form an interval below the first of: the beta cap, the driven boundary
    p_aux = 0, the plasma refusal. p_fus is maximal at that bound unless ash dilution turns it over
    first. Returns dict(n_e0, case, p_fus, limit) or None.
    """
    lo = hi = None  # lo admissible (n, pl, case); hi inadmissible
    n = seed
    evals = 0
    while evals < max_evals:
        evals += 1
        case, pl = probe(n, T)
        if _feasible(pl, beta_cap):
            if lo is None or n > lo[0]:
                lo = (n, pl, case)
        elif hi is None or n < hi[0]:
            hi = (n, pl, case)
        if lo and hi:
            if hi[0] / lo[0] - 1.0 <= 1e-4:
                break
            hp, lp = hi[1], lo[1]
            if hp["plasma"] and hp["beta"] > beta_cap and lp["beta"] < beta_cap:
                t = (beta_cap - lp["beta"]) / (hp["beta"] - lp["beta"])
                if abs(lp["beta"] / beta_cap - 1.0) <= BETA_SEARCH_REL_TOL:
                    break
            elif hp["plasma"] and hp["p_aux"] < 0.0 and lp["p_aux"] > 0.0:
                t = lp["p_aux"] / (lp["p_aux"] - hp["p_aux"])
                if lp["p_aux"] <= AUX_ZERO_TOL_MW:
                    break
            else:
                t = 0.5
            t = min(max(t, 0.02), 0.98)
            n = lo[0] + t * (hi[0] - lo[0])
        elif lo:
            n = lo[0] * 1.35
        else:
            n = hi[0] / 1.35
    if lo is None:
        return None
    n_b, pl_b, case_b = lo
    if hi is None:
        limit = "search"
    elif not hi[1]["plasma"]:
        limit = "plasma_refusal"
    elif hi[1]["beta"] > beta_cap:
        limit = "beta"
    else:
        limit = "driven"
    # ash turn-over below the bound: golden-section on log n for the p_fus maximum (skipped where the
    # matched search already saw p_fus rising through a higher density)
    turn_over = False
    if rising_to is None or n_b > rising_to:
        case_m, pl_m = probe(n_b / 1.03, T)
        turn_over = pl_m["plasma"] and pl_m["p_fus"] > pl_b["p_fus"] and _feasible(pl_m, beta_cap)
    if turn_over:
        a, b = math.log(n_b) - 1.2, math.log(n_b)
        g = (math.sqrt(5.0) - 1.0) / 2.0
        c, e = b - g * (b - a), a + g * (b - a)
        fc = probe(math.exp(c), T)[1].get("p_fus", -1.0)
        fe = probe(math.exp(e), T)[1].get("p_fus", -1.0)
        for _ in range(14):
            if fc > fe:
                b, e, fe = e, c, fc
                c = b - g * (b - a)
                fc = probe(math.exp(c), T)[1].get("p_fus", -1.0)
            else:
                a, c, fc = c, e, fe
                e = a + g * (b - a)
                fe = probe(math.exp(e), T)[1].get("p_fus", -1.0)
            if b - a < 2e-3:
                break
        x = c if fc > fe else e
        case_x, pl_x = probe(math.exp(x), T)
        if _feasible(pl_x, beta_cap) and pl_x["evaluable"]:
            return dict(T=T, n_e0=math.exp(x), case=case_x, p_fus=pl_x["p_fus"], p_aux_required=pl_x["p_aux"],
                        beta=pl_x["beta"], limit="ash_maximum", evaluable=True)
    return dict(T=T, n_e0=n_b, case=case_b, p_fus=pl_b["p_fus"], p_aux_required=pl_b["p_aux"], beta=pl_b["beta"],
                limit=limit, evaluable=pl_b["evaluable"])


def select_matched(ladder: list) -> dict | None:
    """Contract r5 section 5 (P), notes Q1: among the ladder temperatures meeting the bounds at matched
    power (beta <= 0.95 x beta_limit, 0 <= p_aux_required, evaluable), the one with the least required
    heating; equal heating goes to 14.63 keV, then to the lower temperature. Rows are recorded traces."""
    ok = [r for r in ladder if r["matched"] and r.get("within_beta") and r["p_aux"] >= 0.0 and r["evaluable"]]
    if not ok:
        return None
    return min(ok, key=lambda r: (r["p_aux"], r["T"] != LADDER_TIE_KEV, r["T"]))


def operating_point(evaluate, material, design):
    """Contract section 5 operating-point rule, every ladder value recorded.

    - matched: among the ladder T whose matched power has beta <= 0.95 x beta_limit,
      0 <= p_aux_required (installed heating is re-supplied above it) and an evaluable plant, the one
      with the least required heating, ties to 14.63 keV (contract r5 (P), notes Q1; `select_matched`);
    - ignited: matched power within beta only with p_aux_required < 0 at every ladder value reaching
      it; the companion is the largest driven fusion power over the ladder (F1b);
    - power-short: matched power unattainable within beta at every ladder value; n_e0 at the largest
      admissible density (the beta cap 0.95 x beta_limit where beta binds, contract section 5), the
      ladder T with the largest fusion power (notes Q2, Q3).
    """
    beta_cap = BETA_FALLBACK_FRACTION * BETA_LIMIT
    probe = _Probe(evaluate, material, design)
    ladder = []
    for T in LADDER_KEV:
        row = _matched(probe, T, _n_guess(design, T))
        if row["matched"]:
            row["within_beta"] = row["beta"] <= beta_cap
        ladder.append(row)
    selected = select_matched(ladder)
    public = [{k: v for k, v in r.items() if k != "case"} for r in ladder]
    if selected is not None:
        return dict(kind="matched", T=selected["T"], n_e0=selected["n_e0"], case=selected["case"], ladder=public,
                    power_short=0)
    reaching = [r for r in ladder if r["matched"] and r["within_beta"]]
    driven = []
    for T in LADDER_KEV:
        row = next(r for r in ladder if r["T"] == T)
        if row["matched"] and row["beta"] > beta_cap:
            seed = row["n_e0"] * beta_cap / row["beta"]  # beta ~ n_e0 near the matched point
        elif row["matched"]:
            seed = row["n_e0"] * 0.9
        else:
            seed = row.get("n_best") or _n_guess(design, T)
        found = _driven_max(probe, T, seed, beta_cap, rising_to=row["n_e0"] if row["matched"] else None)
        if found is not None and found["evaluable"]:
            driven.append(found)
    driven_public = [{k: v for k, v in r.items() if k != "case"} for r in driven]
    best = max(driven, key=lambda r: r["p_fus"]) if driven else None
    if reaching and all(r["p_aux"] < 0.0 for r in reaching):
        first = reaching[0]
        return dict(kind="ignited", T=first["T"], n_e0=first["n_e0"], case=first["case"], ladder=public,
                    power_short=0, companion=best, driven=driven_public)
    if reaching:  # within beta with p_aux >= 0 but the plant refused there (loop or exchanger domain)
        refused = [r for r in reaching if r["p_aux"] >= 0.0]
        first = refused[0]
        return dict(kind="refused", T=first["T"], n_e0=first["n_e0"], case=first["case"], ladder=public,
                    power_short=0, driven=driven_public)
    if best is None:
        raise PolicyError("no admissible operating point at any ladder temperature")
    return dict(kind="power_short", T=best["T"], n_e0=best["n_e0"], case=best["case"], ladder=public,
                power_short=1, limit=best["limit"], driven=driven_public)


# ---------------------------------------------------------------------------------------------
# Re-supply (contract section 5 rows: structure, heating, cryo ratings, packages, classes, facilities)
# ---------------------------------------------------------------------------------------------
def heating_rule(p_aux_required: float) -> float:
    eta_source = PIN["heating__eta_source_heat"]
    need = max(HEATING_FLOOR_MW, HEATING_FACTOR * p_aux_required / eta_source)
    return math.ceil(need / HEATING_STEP_MW - 1e-12) * HEATING_STEP_MW


def list_rating(demand_W: float) -> tuple[float, bool]:
    """Smallest listed rating >= demand; list exhausted -> the largest rating, flagged (Round 1 A13)."""
    for r in RATINGS_W:
        if r >= demand_W:
            return r, False
    return RATINGS_W[-1], True


def _count_up(value: float) -> float:
    return float(math.ceil(PACKAGE_MARGIN * value - 1e-9))


def ihx_count(ch: dict, d: dict, floor: int = 1) -> tuple[float, int]:
    """IHX exchanger count, contract r5 section 5 (P), notes Q14: the smallest integer count with
    1.05 x required area per exchanger <= installed area. The required area per exchanger at the
    evaluated count n is q_ihx / (n U LMTD) (exploration/stellarator_e2e/oracle_cooling.py:259-268), so
    the count the evaluated duty needs is ceil(1.05 n A_req / A_installed). The circulator work, and so
    q_ihx, rises as the count falls; a count that fails at its own evaluation raises the floor, so the
    fixed point is the smallest count that meets the rule at its own duty. Returns (count, floor)."""
    n = int(round(float(d.get(IHX_COUNT_KEY, PIN[IHX_COUNT_KEY]))))
    req = ch["heat_transport__equipment__ihx_required_area"]
    inst = ch["heat_transport__equipment__ihx_installed_area"]
    if PACKAGE_MARGIN * req > inst:
        floor = max(floor, n + 1)
    count = max(math.ceil(PACKAGE_MARGIN * n * req / inst - 1e-9), floor, 1)
    return float(count), floor


def resupply(case: dict, design: dict, exponent: float = PURCHASE_EXPONENT, structure_variant: float = 1.0,
             state: dict | None = None) -> tuple[dict, dict]:
    """One re-supply pass from an evaluated case. Returns (new design, trace). `state` carries the IHX
    count floor across the passes of one fixed point."""
    ch = case["channels"]
    d = dict(design)
    trace = {}
    state = {} if state is None else state
    # IHX exchanger count (contract r5 (P), notes Q14); the plant's equations carry its consequences
    d[IHX_COUNT_KEY], state["ihx_floor"] = ihx_count(ch, d, state.get("ihx_floor", 1))
    trace["ihx_floor"] = state["ihx_floor"]
    # structure mass, contract section 5 [U]
    d["magnet__m_support"] = og.structure_mass_rule(ch["magnet__stored_energy__W_mag"], structure_variant)
    # installed heating, contract section 5 [U]
    d["heating__p_wallplug_heat"] = heating_rule(ch["plasma__sustain__p_aux_required"])
    # cryo ratings from the staged cold-stage calc with the fixed list (contract section 5)
    cold, cold_exhausted = list_rating(ch["cryoplant__cold_stage__q_cold"])
    icpt, icpt_exhausted = list_rating(ch["cryoplant__cold_stage__q_shield"])
    d["cryoplant__rated_cold_W"] = cold
    d["cryoplant__rated_intercept_W"] = icpt
    trace["cryo_list_exhausted"] = [n for n, f in (("cold", cold_exhausted), ("intercept", icpt_exhausted)) if f]
    # screened ratings x 1.05 (demand = rating - margin)
    for key, margin in SCREENED_RATINGS:
        if ch[margin.replace("__margin", "__applicable")] != 1.0:
            continue  # an inapplicable screen reports margin 0 and no demand: the rating is held
        rating = float(d.get(key, PIN[key]))
        demand = rating - ch[margin]
        d[key] = PACKAGE_MARGIN * max(demand, 0.0)
    for key, actual in OFFERED_STATES:
        d[key] = float(ch[actual])
    for key, fill in PURCHASED_MASSES:
        d[key] = PACKAGE_MARGIN * ch[fill]
    # purchase costs: captured x (rating / captured rating)^exponent [U]
    for name, (purchase, rating_key) in PURCHASES.items():
        if rating_key is None:
            d[purchase] = PIN[purchase]
            continue
        captured_rating = PIN[rating_key]
        d[purchase] = PIN[purchase] * (d[rating_key] / captured_rating) ** exponent
    # power classes = the design's computed powers (WI-079 native channels)
    negative = []
    for key, channel in CLASS_MAP.items():
        value = float(ch[channel])
        if value < 0.0:
            negative.append(key)
            value = 0.0
        d[key] = value
    trace["classes_clamped_at_zero"] = negative
    # facilities (notes Q12)
    trace.update(_facility_resupply(ch, d))
    return d, trace


def _facility_resupply(ch: dict, d: dict) -> dict:
    """Design-dependent facility demands x 1.05; design-independent items held at the pin."""
    t = NUCLEAR_WALL
    for key, required in SECTOR_ALLOCATIONS:
        d[key] = _count_up(ch[required])
    d["buildings__selected_blanket_packages_per_sector"] = _count_up(
        ch["buildings__layout__blanket_packages_required_per_sector"])
    for room in FACILITY_SCALED_ROOMS:
        for axis in ("length", "width", "height"):
            d[f"buildings__selected_{room}_{axis}"] = PACKAGE_MARGIN * ch[f"buildings__layout__{room}_required_{axis}"]
    link_length = PIN["buildings__selected_sector_link_east_length"]
    for link in FACILITY_LINKS:
        d[f"buildings__selected_{link}_length"] = link_length
        for axis in ("width", "height"):
            d[f"buildings__selected_{link}_{axis}"] = PACKAGE_MARGIN * ch[f"buildings__layout__{link}_required_{axis}"]
    wing_width = max(d[f"buildings__selected_sector_wing_{x}_width"] for x in DIRECTIONS)
    hall_need = PACKAGE_MARGIN * max(ch["buildings__layout__reactor_hall_required_length"],
                                     ch["buildings__layout__reactor_hall_required_width"])
    # adjacent wings must not overlap: (hall + 2t)/2 + link >= (wing + 2t)/2, i.e. hall >= wing - 2 link
    hall = max(hall_need, wing_width - 2.0 * link_length)
    d["buildings__selected_reactor_hall_length"] = hall
    d["buildings__selected_reactor_hall_width"] = hall
    d["buildings__selected_reactor_hall_height"] = PACKAGE_MARGIN * ch["buildings__layout__reactor_hall_required_height"]
    # r5 (P), notes Q14: the cooling facilities follow the exchanger count, so they become design-dependent
    # and are re-supplied at requirement x 1.05: the cooling hall length (ceil(circuits / 2) cells), the
    # spare-unit positions (clean and dirty, per helium circulator, salt pump and bundle), and the annex
    # depths those positions need. The hall width and height, annex length and height, store widths and the
    # cooling link have design-independent requirements and keep the pin (Q12).
    d["buildings__selected_cooling_hall_length"] = PACKAGE_MARGIN * ch["buildings__layout__cooling_hall_required_length"]
    north, south = annex_requirement(d)  # at the evaluated allocations
    published = ch["buildings__layout__cooling_annex_required_width"]
    if abs(north + south - published) > 1e-9 * max(1.0, published):
        raise PolicyError(f"annex depth split {north} + {south} disagrees with the oracle's requirement {published}")
    d["buildings__selected_cooling_annex_north_depth"] = PACKAGE_MARGIN * north
    d["buildings__selected_cooling_annex_width"] = PACKAGE_MARGIN * (north + south)
    for state in ("clean", "dirty"):
        for kind in COOLING_KINDS:
            d[f"buildings__cooling_{state}_{kind}_positions"] = _count_up(
                ch[f"buildings__layout__cooling_{state}_{kind}_required"])
    # The conventional campus row starts `building_separation` below the south wing, while the cooling
    # annex reaches down to -(annex width - north depth) - wall beside it
    # (oracle_facilities.layout placement). When the maintenance cross is smaller than the reference,
    # the row rises into the annex. The south link is lengthened just enough to keep them apart (Q12).
    tc = PIN["buildings__conventional_wall"]
    annex_south = (d["buildings__selected_cooling_annex_width"] - d["buildings__selected_cooling_annex_north_depth"]
                   + tc)
    reach = (hall + 2.0 * t) / 2.0 + d["buildings__selected_sector_wing_south_length"] + 2.0 * t \
        + PIN["buildings__building_separation"]
    south_link = max(link_length, math.ceil((annex_south - reach) * 100.0 + 1.0) / 100.0)
    d["buildings__selected_sector_link_south_length"] = south_link
    aspect = PIN["buildings__selected_administration_length"] / PIN["buildings__selected_administration_width"]
    for room in FACILITY_OCCUPANCY_ROOMS:
        area = PACKAGE_MARGIN * ch[f"buildings__layout__{room}_required_area"]
        width = math.sqrt(area / aspect)
        d[f"buildings__selected_{room}_length"] = aspect * width
        d[f"buildings__selected_{room}_width"] = width
        d[f"buildings__selected_{room}_height"] = PACKAGE_MARGIN * ch[f"buildings__layout__{room}_required_height"]
    schedule = _schedule_resupply(ch, d)
    # parcel = required bounds x 1.05, centred (entering datum moved by the public offsets)
    x0, x1 = ch["buildings__layout__required_parcel_x_min"], ch["buildings__layout__required_parcel_x_max"]
    y0, y1 = ch["buildings__layout__required_parcel_y_min"], ch["buildings__layout__required_parcel_y_max"]
    sx, sy = x1 - x0, y1 - y0
    d["buildings__selected_parcel_length"] = PACKAGE_MARGIN * sx
    d["buildings__selected_parcel_width"] = PACKAGE_MARGIN * sy
    d["buildings__parcel_origin_x_offset"] = (x0 - 0.5 * (PACKAGE_MARGIN - 1.0) * sx) - PIN_PARCEL_X_MIN
    d["buildings__parcel_origin_y_offset"] = (y0 - 0.5 * (PACKAGE_MARGIN - 1.0) * sy) - PIN_PARCEL_Y_MIN
    return dict(schedule, reactor_hall_rule="overlap" if hall > hall_need else "requirement")


COOLING_KINDS = ("helium", "salt", "bundle")
HX_TUBE_LENGTH_M = 11.6  # the exchanger tube length the composite oracle passes the facility layout (hx_tube_length)


def annex_requirement(d: dict) -> tuple[float, float]:
    """North and south annex depths the allocated cooling spare positions need, in the facility oracle's
    statement order (exploration/stellarator_e2e/oracle_facilities.py:470-477). The oracle publishes only
    their sum (`cooling_annex_required_width`), which the caller checks this split against."""
    g = lambda k: float(d.get("buildings__" + k, PIN["buildings__" + k]))  # noqa: E731
    margin, aisle = g("cooling_package_margin"), g("cooling_aisle_width")
    pitches = (g("helium_package_length") + 2 * margin, g("salt_package_length") + 2 * margin,
               HX_TUBE_LENGTH_M + 2 * margin)
    machine = 2 * (max(g("helium_package_length"), g("salt_package_length")) + 2 * margin)
    reserve = g("cooling_cross_width") / 2 + g("cooling_airlock_length") + 2 * g("conventional_wall")
    clean = max(math.ceil(g(f"cooling_clean_{k}_positions") / 2) * p + aisle for k, p in zip(COOLING_KINDS, pitches))
    dirty = max(max(math.ceil(g(f"cooling_dirty_{k}_positions") / 2) * p + aisle for k, p in zip(COOLING_KINDS, pitches)),
                machine / 2 + (HX_TUBE_LENGTH_M + 2 * margin) + 10 * margin)
    return reserve + clean, reserve + dirty


def _schedule_resupply(ch: dict, d: dict) -> dict:
    """Maintenance schedule resources the facility screens (notes Q13), uncosted (free_capacity).

    - sector_service_teams: the smallest count (at most one per sector) whose campaign outage x 1.05
      fits the calendar's allowed outage and whose initial installation finishes by commissioning,
      from the facility oracle's own schedule functions (oracle_facilities.sector_schedule,
      sector_inventory) at the design's packages per sector;
    - initial and recurring receipt leads: the preparation time the campaign demands (packages x
      prepare days on one station per wing) x 1.05, plus the initial start offset for the initial lead.
    """
    fo = vs.facilities_oracle
    g = lambda k: float(d.get("buildings__" + k, PIN["buildings__" + k]))  # noqa: E731
    packages = d["buildings__selected_blanket_packages_per_sector"] + g("divertor_packages_per_sector")
    allowed = ch["buildings__layout__outage_allowed_days"]
    opts = dict(cooldown=g("cooldown_days"), split=g("sector_split_days"), transport=g("sector_transport_days"),
                cleaning=g("sector_clean_days"), testing=g("sector_test_days"), joining=g("sector_join_days"),
                recommission=g("recommission_days"))
    start = fo.DEFAULTS["initial_sector_start_days"]
    sectors = int(g("sector_count"))
    teams, bound = None, False
    for k in range(1, sectors + 1):
        _, outage = fo.sector_schedule(packages, k, g("component_remove_days"), g("component_install_days"), **opts)
        inv = fo.sector_inventory([], packages, float(PIN["operational_years"]), teams=k,
                                  remove=g("component_remove_days"), install=g("component_install_days"),
                                  process=g("component_process_days"), prepare=g("component_prepare_days"),
                                  lead=g("component_receipt_lead_days"), initial_lead=g("initial_receipt_lead_days"),
                                  hold=g("component_hold_days"), yield_factor=g("waste_package_yield"),
                                  initial_start=start, schedule_options=opts)
        if PACKAGE_MARGIN * outage <= allowed and inv["initial_finish"] <= 0.0:
            teams = k
            break
    if teams is None:
        teams, bound = sectors, True
    d["buildings__sector_service_teams"] = float(teams)
    prep = packages * g("component_prepare_days")
    d["buildings__initial_receipt_lead_days"] = -start + PACKAGE_MARGIN * prep
    d["buildings__component_receipt_lead_days"] = PACKAGE_MARGIN * prep
    return {"sector_service_teams_at_bound": bound}


# ---------------------------------------------------------------------------------------------
# Labels, flags and statuses (contract section 7; design A4)
# ---------------------------------------------------------------------------------------------
#: Verdicts that do not disqualify `supported`: the envelope flag, and the two open plant gaps carried with
#: their margins (tbr_ok; divertor_heat_ok by the contract r5 (P) ruling on notes Q5, flag `divertor_pass`).
NOT_FAILING = ("peak_field_ok", "tbr_ok", "divertor_heat_ok")
CAPACITY_SCREENS = {"cold": ("cold_stage_capacity_ok", "cryoplant__capacity_ok"),
                    "intercept": ("intercept_stage_capacity_ok",),
                    "teams": ("facility_outage_ok", "facility_initial_ready")}


def flags_of(material: str, case: dict, design: dict, power_short: int) -> dict:
    ch = case["channels"]
    v = case["verdicts"]
    B = ch["magnet__peak_field_calc__B_peak"]
    code = ch["magnet__conductor__status_code"]
    x = ch["magnet__pack_field__R_over_sqrt_A_wp"]
    beta = ch["plasma__beta_calc__beta"]
    out = dict(
        envelope_flag=v["peak_field_ok"] == "violated",
        green_extrapolated=ch["cryoplant__refrigeration__green_extrapolated"] == 1.0,
        power_short=int(power_short),
        arm_extrapolated=bool(design["magnet__coil__arm_slope"] != 0.0 and not 25.0 <= x <= 40.0),
        R_over_sqrt_A_wp=x,
        ampere_floor_margin=ch["magnet__pack_field__ampere_floor_margin"],
        beta_verdict_0_05=v["beta_ok"],
        beta_verdict_0_04=("indeterminate" if math.isnan(beta) else
                           ("satisfied" if beta <= BETA_SECOND_VERDICT else "violated")),
        free_capacity=list(FREE_CAPACITY),
        divertor_pass=v["divertor_heat_ok"] == "satisfied",  # r5 (P), notes Q5
        divertor_q_target_margin=ch["divertor__divheat__q_target_margin"],
        tbr_pass=v["tbr_ok"] == "satisfied",
    )
    if material == "rebco":
        out.update(extrapolated=20.0 < B <= 24.0, beyond_law_extents=24.0 < B <= 25.0,
                   above_stellaris_envelope=B > 24.9)
    else:
        out.update(extrapolated=code in (2.0, 3.0), beyond_law_extents=False, above_stellaris_envelope=False)
    return out


def status_of(material: str, case: dict, kind: str, trace: dict) -> tuple[str, list]:
    """Contract section 7 statuses in order: unsupported, ignited, capacity-limited, failed, supported."""
    if "refusal" in case:
        return "unsupported", ["domain refusal: " + case["refusal"]]
    ch = case["channels"]
    B = ch["magnet__peak_field_calc__B_peak"]
    if ch["magnet__conductor__status_code"] == 0.0 or (material == "rebco" and B > 25.0):
        return "unsupported", ["conductor status 0" if ch["magnet__conductor__status_code"] == 0.0 else "REBCO above 25 T"]
    if kind == "ignited":
        return "ignited", ["p_aux_required < 0 at every ladder value reaching matched power"]
    violated = sorted(k for k, s in case["verdicts"].items() if s != "satisfied" and k not in NOT_FAILING)
    exhausted = list(trace.get("cryo_list_exhausted", []))
    if trace.get("sector_service_teams_at_bound"):
        exhausted.append("teams")
    bound = [s for which in exhausted for s in CAPACITY_SCREENS[which] if s in violated]
    if bound:
        return "capacity-limited", bound
    if violated:
        return "failed", violated
    return "supported", []


# ---------------------------------------------------------------------------------------------
# One design: propose -> evaluate -> re-supply -> evaluate
# ---------------------------------------------------------------------------------------------
def base_design(material: str, geometry: str, f_ren: float, size, variant: str) -> dict:
    asm = material_assumptions(material, variant)
    d = cell_inputs(geometry, f_ren, variant)
    d.update({"plasma__R": float(size[0]), "plasma__a": float(size[1]),
              "magnet__element_price_per_m": asm["price"],
              "magnet__winding_pack__B_max": asm["facts"]["magnet__winding_pack__B_max"],
              "cryoplant__T_cold_cryo": asm["facts"]["cryoplant__T_cold_cryo"],
              "cryoplant__rated_cryogenic_cold_K": asm["facts"]["cryoplant__rated_cryogenic_cold_K"]})
    if material == "nb3sn":
        d[og.EPS_KEY] = asm["eps_intrinsic"]
    return d, asm


def _converge_resupply(evaluate, material, design, exponent=PURCHASE_EXPONENT, structure_variant=1.0):
    """Evaluate, re-supply, repeat until the re-supplied design equals the evaluated one."""
    d = dict(design)
    trace = {}
    state = {}
    for it in range(1, MAX_RESUPPLY_ITERATIONS + 1):
        case = evaluate(d, material)
        if "refusal" in case:
            return d, case, dict(trace, resupply_iterations=it)
        new, trace = resupply(case, d, exponent, structure_variant, state)
        if new == d:
            return d, case, dict(trace, resupply_iterations=it)
        d = new
    case = evaluate(d, material)
    trace["resupply_not_converged"] = True
    return d, case, dict(trace, resupply_iterations=MAX_RESUPPLY_ITERATIONS + 1)


def expectations(case: dict) -> dict:
    ch = case["channels"]
    names = ("plasma__fusion__p_fus", "plasma__sustain__p_aux_required", "plasma__beta_calc__beta",
             "magnet__peak_field_calc__B_peak", "magnet__field_calc__B_axis", "lcoe_calc__lcoe", "pb__p_net",
             "magnet__stored_energy__W_mag", "magnet__conductor__acceptance_margin",
             "magnet__conductor__status_code", "magnet__area__fit_margin", "magnet__wp_fit__minimum_margin",
             "cryoplant__cold_stage__q_cold", "cryoplant__cold_stage__q_shield", "heating__heat__p_coupled",
             "magnet__pack_field__ampere_floor", "magnet__pack_field__ampere_floor_margin",
             "magnet__inventory__sc_cost", "magnet__magnet_capital_rollup__capital_cost",
             "total_capital__total_capital", "calendar__availability")
    out = {"p_fus": ch["plasma__fusion__p_fus"], "p_aux_required": ch["plasma__sustain__p_aux_required"],
           "beta": ch["plasma__beta_calc__beta"], "B_peak": ch["magnet__peak_field_calc__B_peak"]}
    out["channels"] = {n: ch[n] for n in names}
    out["violated"] = sorted(k for k, s in case["verdicts"].items() if s != "satisfied")
    return out


def _finish(evaluate, material, d, kind, T, n_e0, power_short, B_target, base_trace, offer_kind="reference"):
    """Re-supply at the chosen operating point and file the record (contract sections 5 and 7)."""
    d = dict(d, **{"plasma__n_e0": n_e0, "plasma__T_i0": T})
    final, case, rtrace = _converge_resupply(evaluate, material, d)
    status, reasons = status_of(material, case, kind, rtrace)
    rec = dict(offer_kind=offer_kind, design=final, T_i0_ladder=T, power_short=power_short,
               status_expected=status, reasons=reasons, trace=dict(base_trace, **rtrace))
    if "refusal" not in case:
        rec["expected"] = expectations(case)
        rec["flags"] = flags_of(material, case, final, power_short)
        rec["B_peak_target_error"] = case["channels"]["magnet__peak_field_calc__B_peak"] - B_target
    return rec


def _confirm_magnet(evaluate, material, asm, d, I_turn):
    """One evaluation confirms the policy's magnet arithmetic against the oracle (B_peak, acceptance,
    pack area, fit); on disagreement the magnet is re-sized at the oracle's B_peak. The point is a low
    density at the reference temperature, where no plant domain refuses; the magnet channels do not
    depend on the operating point."""
    probe = dict(d, **{"plasma__n_e0": 0.3 * _n_guess(d, PIN["plasma__T_i0"]), "plasma__T_i0": PIN["plasma__T_i0"]})
    case = evaluate(probe, material)
    corrections = 0
    while "refusal" not in case and corrections < 5:
        ch = case["channels"]
        if (ch["magnet__conductor__acceptance_margin"] >= 0.0 and ch["magnet__area__fit_margin"] >= 0.0
                and ch["magnet__wp_fit__minimum_margin"] >= 0.0):
            break
        corrections += 1
        B = ch["magnet__peak_field_calc__B_peak"]
        n = smallest_n(material, asm, I_turn, B) + (corrections - 1)
        areas = construction_areas(material, asm, n, I_turn, B)
        gross = gross_turn_area(material, asm, n, areas, I_turn, B)["gross_area"]
        side = max(pack_side(int(d["magnet__coil__reference_turns"]), gross), d["magnet__winding_pack__wp_side"])
        coil_t, iy = allocation(side)
        d.update({"magnet__n_elements": float(n), "magnet__winding_pack__wp_side": side,
                  "magnet__coil__coil_t": coil_t, "magnet__casing__interior_y": iy})
        for k in og.CONSTRUCTION:
            d["magnet__" + k] = areas[k]
        probe = dict(probe, **{k: d[k] for k in d if k.startswith("magnet__")})
        case = evaluate(probe, material)
    return case, corrections


def propose_design(material: str, geometry: str, f_ren: float, size, B_target: float, variant: str = "none",
                   fixed_turns: int | None = None, evaluate: Evaluator | None = None) -> list:
    """The recorded supplied design(s) for one grid point: the design and, for an ignited design,
    its power-short companion (contract section 5, F1b)."""
    evaluate = evaluate or Evaluator()
    start = evaluate.count
    misses0 = MEMO_STATS["misses"]
    d, asm = base_design(material, geometry, f_ren, size, variant)
    I_turn = turn_current(variant)

    def done(records):
        for r in records:
            r["evaluations"] = evaluate.count - start
            r["plasma_solves"] = MEMO_STATS["misses"] - misses0
        return records

    try:
        mag = size_magnet(material, asm, d, B_target, I_turn, fixed_turns)
    except PolicyError as exc:
        return done([dict(offer_kind="reference", status_expected="unsupported", reasons=[str(exc)], design=None)])
    d = mag["design"]
    confirm, corrections = _confirm_magnet(evaluate, material, asm, d, I_turn)
    base_trace = dict(mag["trace"], oracle_corrections=corrections)
    if "refusal" in confirm:
        return done([dict(offer_kind="reference", status_expected="unsupported", design=d, trace=base_trace,
                          reasons=["domain refusal: " + confirm["refusal"]])])
    try:
        op = operating_point(evaluate, material, d)
    except PolicyError as exc:
        return done([dict(offer_kind="reference", status_expected="unsupported", design=d, trace=base_trace,
                          reasons=[str(exc)])])
    trace = dict(base_trace, operating_point=op["kind"], ladder=op["ladder"])
    if "driven" in op:
        trace["driven"] = op["driven"]
    if op["kind"] == "refused":
        rec = dict(offer_kind="reference", design=dict(d, **{"plasma__n_e0": op["n_e0"], "plasma__T_i0": op["T"]}),
                   T_i0_ladder=op["T"], power_short=0, status_expected="unsupported", trace=trace,
                   reasons=["domain refusal at the matched point: " + op["case"]["refusal"]])
        return done([rec])
    if op["kind"] == "power_short":
        trace["power_short_limit"] = op["limit"]
    records = [_finish(evaluate, material, d, op["kind"], op["T"], op["n_e0"], op["power_short"], B_target, trace)]
    if op["kind"] == "ignited":
        comp = op.get("companion")
        if comp is None:
            records[0]["reasons"].append("no driven operating point at any ladder temperature: no companion")
        else:
            ctrace = dict(base_trace, operating_point="companion", companion_limit=comp["limit"])
            records.append(_finish(evaluate, material, d, "companion", comp["T"], comp["n_e0"], 1, B_target, ctrace,
                                   offer_kind="companion"))
    return done(records)


def mr7_offer(record: dict, kind: str, material: str, evaluate: Evaluator) -> dict:
    """Insufficient floor(0.9 n) or generous ceil(1.2 n) element offer, every other input unchanged
    (contract section 5 row "Winding element count"; Round 1 A9: same areas and rating)."""
    n = int(record["design"]["magnet__n_elements"])
    n2 = (9 * n) // 10 if kind == "insufficient" else (12 * n + 9) // 10
    d = dict(record["design"], **{"magnet__n_elements": float(n2)})
    case = evaluate(d, material)
    status, reasons = status_of(material, case, "reference", {})
    rec = dict(offer_kind=kind, design=d, T_i0_ladder=record["T_i0_ladder"], power_short=record["power_short"],
               status_expected=status, reasons=reasons, n_reference=n, evaluations=1)
    if "refusal" not in case:
        rec["expected"] = expectations(case)
        rec["flags"] = flags_of(material, case, d, record["power_short"])
    return rec


def reevaluate(record: dict, variant: str, material: str, evaluate: Evaluator) -> dict:
    """A recorded design re-evaluated under a re-evaluation variant (inputs changed, design held)."""
    d = dict(record["design"])
    structure_variant = STRUCTURE_VARIANTS.get(variant, 1.0)
    exponent = {"purchase_exp_0.5": 0.5, "purchase_exp_1.0": 1.0}.get(variant, PURCHASE_EXPONENT)
    if variant in STRUCTURE_VARIANTS:
        case0 = evaluate(d, material)
        d["magnet__m_support"] = og.structure_mass_rule(case0["channels"]["magnet__stored_energy__W_mag"],
                                                        structure_variant)
        evals = 2
    elif variant in ("purchase_exp_0.5", "purchase_exp_1.0"):
        for name, (purchase, rating_key) in PURCHASES.items():
            if rating_key is not None:
                d[purchase] = PIN[purchase] * (d[rating_key] / PIN[rating_key]) ** exponent
        evals = 1
    elif variant == "cpi_2021_2026":
        d["magnet__element_price_per_m"] = d["magnet__element_price_per_m"] * CPI_2021_TO_2026
        d["cryoplant__usd2015_to_2021"] = og.STAGED_CRYO_FACTS["usd2015_to_2021"] * CPI_2021_TO_2026
        evals = 1
    elif variant == "price_30":
        d["magnet__element_price_per_m"] = 30.0
        evals = 1
    elif variant == "price_10":
        d["magnet__element_price_per_m"] = PRICE_REBCO_VOLUME
        evals = 1
    elif variant in ("nb3sn_price_5.4", "nb3sn_price_13.5"):
        d["magnet__element_price_per_m"] = float(variant.rsplit("_", 1)[1])
        evals = 1
    else:
        raise PolicyError(f"unknown re-evaluation variant {variant}")
    case = evaluate(d, material)
    status, reasons = status_of(material, case, "reference", {})
    rec = dict(offer_kind=record["offer_kind"], design=d, T_i0_ladder=record["T_i0_ladder"],
               power_short=record["power_short"], status_expected=status, reasons=reasons, evaluations=evals,
               base_of=record.get("case_id"))
    if "refusal" not in case:
        rec["expected"] = expectations(case)
        rec["flags"] = flags_of(material, case, d, record["power_short"])
    return rec
