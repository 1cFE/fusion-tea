"""Independent oracle for WI-099 (matched-duty magnet conductor alternatives).

Written from the released contract and the reviewed design only:
  - work/orchestration/goals/magnet-material-comparison/evidence/comparison-contract.md (r3)
  - work/active/WI-099_magnet-conductor-alternatives/design.md (section 2 equations, section 6 names)
The implementer's SysML files and handwritten bodies were not read.

Pure standard-library Python. Every calc of design section 2 is a function of a dict keyed by
that calc's section-2 input names, returning every section-2 output under the same names.
`evaluate_case` takes a case keyed by the section-6 names (duty / economics / nb3sn / rebco) and
returns all outputs per material plus the matched-pair comparison.

Methods deliberately differ from the implementer's (design section 2):
  - Nb3Sn current-sharing temperature: Brent-Dekker root on [0, T_zero] (implementer: bisection).
  - NIST 316 conductivity integral: composite Gauss-Legendre in ln T (implementer: Simpson).
Units: A, T, K, mm^2 (areas), m, kg, W (unless named), USD2021.
"""
from __future__ import annotations

import math

# ---------------------------------------------------------------------------------------------
# Fixed design values (design section 6: domain bounds, T_shield, T_amb and NIST coefficients are
# fixed design values, not case inputs).
# ---------------------------------------------------------------------------------------------
T_SHIELD = 77.0  # K, intercept stage (contract section 6; Stellaris model T_shield = 77.0)
T_AMB = 300.0  # K, heat rejection (contract section 6; model T_amb_cryo = 300.0)

# NIST 316 stainless thermal conductivity fit, log10 k = sum_i c_i (log10 T)^i, W/(m K).
# Source: knowledge/sources/nist_316_stainless_cryogenic_material_properties/output.md:24-32
# (Thermal Conductivity column a..i; data range 4-300 K, equation range 1-300 K, fit error 2 %).
NIST316_COEFFS = (-1.4087, 1.3982, 0.2543, -0.6260, 0.2334, 0.4256, -0.4658, 0.1650, -0.0199)

# Nb3Sn law domain and status bands (contract section 2 and section 3; design section 2.1).
NB3SN_BOUNDS = dict(B_law_min=8.0, B_law_max=14.5, B_design_max=12.2, B_edge_max=13.5,
                    T_law_min=4.2, T_law_max=12.0, eps_min=-0.010, eps_max=0.002)
# REBCO domains (contract section 3; design section 2.2).
REBCO_BOUNDS = dict(B_knot_min=8.0, B_knot_max=20.0, B_law_min=5.0, B_law_max=24.0,
                    T_law_min=4.2, T_law_max=50.0)
REBCO_KNOT_FIELDS = (8.0, 10.0, 12.0, 15.0, 20.0)
# Green 2015 fitted data span, kW (design D6; check-rebco-cryo-cost.md section 4).
GREEN_FIT_MIN_KW = 0.01
GREEN_FIT_MAX_KW = 35.0

TCS_XTOL = 1e-13  # K, Brent absolute tolerance (contract section 8 requires 1e-9 K)


# ---------------------------------------------------------------------------------------------
# Nb3Sn critical surface (Tsui & Hampshire 2012 eq. 6-7; Breschi et al. 2017 Table III form)
# ---------------------------------------------------------------------------------------------
def nb3sn_strain_function(eps: float, Ca1: float, Ca2: float, eps0a: float) -> float:
    """ITER strain function s(eps_I), strains as fractions. Peak s = 1 at eps_I = 0."""
    if Ca2 == 0.0:
        eps_sh = 0.0
    else:
        eps_sh = Ca2 * eps0a / math.sqrt(Ca1 * Ca1 - Ca2 * Ca2)
    num = Ca1 * (math.sqrt(eps_sh * eps_sh + eps0a * eps0a)
                 - math.sqrt((eps - eps_sh) ** 2 + eps0a * eps0a)) - Ca2 * eps
    return 1.0 + num / (1.0 - Ca1 * eps0a)


def nb3sn_ic_strand(B: float, T: float, eps: float, P: dict) -> float:
    """Whole-strand critical current (A) at 10 uV/m. C1 in A*T per strand.

    Zero outside 0 <= t < 1 and 0 < b < 1. The design text says 0 < t; t = 0 (T = 0 K) is
    admitted here because the Tcs definition evaluates n*Ic(B, 0) (see oracle-notes.md, A1).
    """
    s = nb3sn_strain_function(eps, P["Ca1"], P["Ca2"], P["eps0a"])
    if s <= 0.0 or B <= 0.0:
        return 0.0
    tc_star = P["Tc0"] * s ** (1.0 / 3.0)
    t = T / tc_star
    if t < 0.0 or t >= 1.0:
        return 0.0
    one_minus_t152 = 1.0 - t ** 1.52
    bc2 = P["Bc20"] * s * one_minus_t152
    b = B / bc2
    if b <= 0.0 or b >= 1.0:
        return 0.0
    return (P["C1"] / B) * s * one_minus_t152 * (1.0 - t * t) * b ** P["p"] * (1.0 - b) ** P["q"]


def nb3sn_t_zero(B: float, eps: float, P: dict) -> float:
    """Temperature at which b = 1 (Bc2*(T, eps) = B); 0 if B >= Bc2*(0, eps)."""
    s = nb3sn_strain_function(eps, P["Ca1"], P["Ca2"], P["eps0a"])
    if s <= 0.0:
        return 0.0
    ratio = B / (P["Bc20"] * s)
    if ratio >= 1.0:
        return 0.0
    t0 = (1.0 - ratio) ** (1.0 / 1.52)
    return t0 * P["Tc0"] * s ** (1.0 / 3.0)


def brent_root(f, a: float, b: float, xtol: float = TCS_XTOL, maxiter: int = 500) -> float:
    """Brent-Dekker root of f on [a, b], f(a)*f(b) <= 0. Own implementation (not bisection)."""
    fa, fb = f(a), f(b)
    if fa == 0.0:
        return a
    if fb == 0.0:
        return b
    if fa * fb > 0.0:
        raise ValueError("root not bracketed")
    c, fc = a, fa
    d = e = b - a
    for _ in range(maxiter):
        if fb * fc > 0.0:
            c, fc = a, fa
            d = e = b - a
        if abs(fc) < abs(fb):
            a, b, c = b, c, b
            fa, fb, fc = fb, fc, fb
        tol1 = 2.0 * 2.220446049250313e-16 * abs(b) + 0.5 * xtol
        xm = 0.5 * (c - b)
        if abs(xm) <= tol1 or fb == 0.0:
            return b
        if abs(e) >= tol1 and abs(fa) > abs(fb):
            s = fb / fa
            if a == c:  # secant
                p = 2.0 * xm * s
                q = 1.0 - s
            else:  # inverse quadratic interpolation
                q = fa / fc
                r = fb / fc
                p = s * (2.0 * xm * q * (q - r) - (b - a) * (r - 1.0))
                q = (q - 1.0) * (r - 1.0) * (s - 1.0)
            if p > 0.0:
                q = -q
            p = abs(p)
            if 2.0 * p < min(3.0 * xm * q - abs(tol1 * q), abs(e * q)):
                e = d
                d = p / q
            else:
                d = xm
                e = d
        else:
            d = xm
            e = d
        a, fa = b, fb
        if abs(d) > tol1:
            b += d
        else:
            b += tol1 if xm > 0.0 else -tol1
        fb = f(b)
    return b


def _nb3sn_params(x: dict) -> dict:
    return {k: float(x[k]) for k in ("p", "q", "C1", "Ca1", "Ca2", "eps0a", "Bc20", "Tc0")}


def nb3sn_cable_critical_surface(x: dict) -> dict:
    """Design section 2.1 'Nb3Sn Cable Critical Surface'."""
    bd = dict(NB3SN_BOUNDS)
    bd.update({k: float(x[k]) for k in NB3SN_BOUNDS if k in x})
    n = float(x["n_strands"] if "n_strands" in x else x["n_elements"])
    d = float(x["strand_diameter"])
    I = float(x["turn_current"])
    B = float(x["B_peak"])
    eps = float(x["eps_intrinsic"])
    P = _nb3sn_params(x)
    T_cond = float(x["T_supply"]) + float(x["nuclear_rise"])
    T_rule = T_cond + float(x["margin_rise"])

    ic_strand_op = nb3sn_ic_strand(B, T_cond, eps, P)
    ic_cable_op = n * ic_strand_op
    operating_fraction = I / ic_cable_op if ic_cable_op > 0.0 else math.inf

    if n * nb3sn_ic_strand(B, 0.0, eps, P) < I:
        T_cs, tcs_defined = 0.0, 0
    else:
        T_zero = nb3sn_t_zero(B, eps, P)
        T_cs = brent_root(lambda T: n * nb3sn_ic_strand(B, T, eps, P) - I, 0.0, T_zero)
        tcs_defined = 1

    temp_rule_margin = T_cs - T_rule
    fraction_rule_margin = float(x["fraction_rule"]) - operating_fraction
    acceptance_margin = temp_rule_margin if float(x["acceptance_rule"]) == 0.0 else fraction_rule_margin

    in_domain = (bd["B_law_min"] <= B <= bd["B_law_max"]
                 and bd["T_law_min"] <= T_cond <= bd["T_law_max"]
                 and bd["eps_min"] <= eps <= bd["eps_max"])
    if not in_domain:
        status = 0
    elif B <= bd["B_design_max"]:
        status = 1
    elif B <= bd["B_edge_max"]:
        status = 2
    else:
        status = 3
    supported = 1 if status != 0 else 0
    element_area_total = n * math.pi / 4.0 * d * d * 1e6
    return dict(
        T_conductor=T_cond,
        ic_strand_op=ic_strand_op,
        ic_cable_op=ic_cable_op,
        operating_fraction=operating_fraction,
        T_cs=T_cs,
        tcs_defined=tcs_defined,
        temperature_margin=T_cs - T_cond,
        temp_rule_margin=temp_rule_margin,
        fraction_rule_margin=fraction_rule_margin,
        acceptance_margin=acceptance_margin,
        status_code=status,
        supported=supported,
        acceptance_pass=1 if (supported and acceptance_margin >= 0.0) else 0,
        element_area_total=element_area_total,
        element_copper_area=float(x["strand_copper_fraction"]) * element_area_total,
    )


# ---------------------------------------------------------------------------------------------
# REBCO critical surface (Molodyk 2021 Fig. 1a shape; Senatore 2016 exponential T law)
# ---------------------------------------------------------------------------------------------
def rebco_shape(B: float, x: dict) -> float:
    """g(B) = Ic(B)/Ic(20 T) at 20 K. Mode 0: log-log interpolation of the knots; mode 1: power law.

    Outside the knot range (unsupported) the end segment is extended in log-log; such values carry
    no claim (status 0).
    """
    if float(x["shape_mode"]) == 1.0:
        return (B / 20.0) ** (-float(x["alpha"]))
    knots = [(8.0, float(x["g8"])), (10.0, float(x["g10"])), (12.0, float(x["g12"])),
             (15.0, float(x["g15"])), (20.0, float(x["g20"]))]
    if B <= knots[0][0]:
        (b0, g0), (b1, g1) = knots[0], knots[1]
    elif B >= knots[-1][0]:
        (b0, g0), (b1, g1) = knots[-2], knots[-1]
    else:
        for (b0, g0), (b1, g1) in zip(knots, knots[1:]):
            if b0 <= B <= b1:
                break
    if B == b0:
        return g0
    if B == b1:
        return g1
    slope = (math.log(g1) - math.log(g0)) / (math.log(b1) - math.log(b0))
    return math.exp(math.log(g0) + slope * (math.log(B) - math.log(b0)))


def rebco_cable_critical_surface(x: dict) -> dict:
    """Design section 2.2 'REBCO Cable Critical Surface'."""
    bd = dict(REBCO_BOUNDS)
    bd.update({k: float(x[k]) for k in REBCO_BOUNDS if k in x})
    n = float(x["n_tapes"] if "n_tapes" in x else x["n_elements"])
    I = float(x["turn_current"])
    B = float(x["B_peak"])
    T_star = float(x["T_star"])
    deg = float(x["degradation"])
    anchor = float(x["anchor_ic"])
    T_cond = float(x["T_supply"]) + float(x["nuclear_rise"])
    T_rule = T_cond + float(x["margin_rise"])
    g = rebco_shape(B, x)
    ic_tape_op = anchor * g * math.exp(-(T_cond - 20.0) / T_star)
    ic_cable_op = n * deg * ic_tape_op
    operating_fraction = I / ic_cable_op if ic_cable_op > 0.0 else math.inf
    arg = n * deg * anchor * g / I if I > 0.0 else math.inf
    if arg > 0.0 and math.isfinite(arg):
        T_cs, tcs_defined = 20.0 + T_star * math.log(arg), 1
    else:
        T_cs, tcs_defined = 0.0, 0
    temp_rule_margin = T_cs - T_rule
    fraction_rule_margin = float(x["fraction_rule"]) - operating_fraction
    acceptance_margin = temp_rule_margin if float(x["acceptance_rule"]) == 0.0 else fraction_rule_margin
    if float(x["shape_mode"]) == 1.0:
        field_ok = bd["B_law_min"] <= B <= bd["B_law_max"]
    else:
        field_ok = bd["B_knot_min"] <= B <= bd["B_knot_max"]
    temp_ok = bd["T_law_min"] <= T_cond <= bd["T_law_max"]
    status = 1 if (field_ok and temp_ok) else 0
    element_area_total = n * float(x["tape_width"]) * float(x["tape_thickness"]) * 1e6
    return dict(
        T_conductor=T_cond,
        ic_tape_op=ic_tape_op,
        ic_cable_op=ic_cable_op,
        operating_fraction=operating_fraction,
        T_cs=T_cs,
        tcs_defined=tcs_defined,
        temperature_margin=T_cs - T_cond,
        temp_rule_margin=temp_rule_margin,
        fraction_rule_margin=fraction_rule_margin,
        acceptance_margin=acceptance_margin,
        status_code=status,
        supported=status,
        acceptance_pass=1 if (status and acceptance_margin >= 0.0) else 0,
        element_area_total=element_area_total,
        element_copper_area=float(x["tape_copper_fraction"]) * element_area_total,
    )


# ---------------------------------------------------------------------------------------------
# Winding turn area screen (design section 2.3; contract section 4)
# ---------------------------------------------------------------------------------------------
def winding_turn_area_screen(x: dict) -> dict:
    I = float(x["turn_current"])
    B = float(x["B_peak"])
    cable = float(x["element_area"]) / float(x["cabling_factor"]) / (1.0 - float(x["cable_void"]))
    net = (cable + float(x["cu_space"]) + float(x["steel_area"]) + float(x["misc_area"])
           + float(x["solder_area"]))
    gross = net / (1.0 - float(x["ins_fraction"]))
    fit_margin = float(x["available_area"]) - gross
    J = float(x["J_cu_rule"])
    if J > 0.0:
        cu_required = max(0.0, I / J - float(x["element_copper_area"])) / (1.0 - float(x["cu_void"]))
    else:
        cu_required = float(x["cu_per_kA_rule"]) * I / 1000.0
    scale = B / float(x["B_steel_ref"]) if float(x["steel_B_scaling"]) != 0.0 else 1.0
    steel_required = float(x["steel_per_kA_rule"]) * (I / 1000.0) * scale
    cu_margin = float(x["cu_space"]) - cu_required
    steel_margin = float(x["steel_area"]) - steel_required
    return dict(
        cable_area=cable,
        net_area=net,
        gross_area=gross,
        fit_margin=fit_margin,
        fit_margin_fraction=fit_margin / float(x["available_area"]),
        required_envelope_J=I / gross,
        cu_required=cu_required,
        cu_margin=cu_margin,
        steel_required=steel_required,
        steel_margin=steel_margin,
        fit_pass=1 if fit_margin >= 0.0 else 0,
        cu_pass=1 if cu_margin >= 0.0 else 0,
        steel_pass=1 if steel_margin >= 0.0 else 0,
    )


# ---------------------------------------------------------------------------------------------
# Winding inventory and cost (design section 2.4; contract section 7)
# ---------------------------------------------------------------------------------------------
def winding_inventory_and_cost(x: dict) -> dict:
    L = float(x["turns"]) * float(x["coils"]) * float(x["turn_length"])
    element_length = float(x["n_elements"]) * L
    element_mass = float(x["element_area"]) * 1e-6 * L * float(x["element_density"])
    cu_mass = float(x["cu_space"]) * (1.0 - float(x["cu_void"])) * 1e-6 * L * float(x["rho_cu"])
    # steel and solder have no void input: mass = area * length * density (oracle-notes.md, A4)
    steel_mass = float(x["steel_area"]) * 1e-6 * L * float(x["rho_steel"])
    solder_mass = float(x["solder_area"]) * 1e-6 * L * float(x["rho_solder"])
    sc_cost = element_length * float(x["element_price_per_m"])
    materials_cost = (cu_mass * float(x["price_cu"]) + steel_mass * float(x["price_steel"])
                      + solder_mass * float(x["price_solder"]))
    manufacturing_cost = L * float(x["manufacturing_per_m"])
    return dict(
        conductor_length=L,
        element_length=element_length,
        element_mass=element_mass,
        cu_mass=cu_mass,
        steel_mass=steel_mass,
        solder_mass=solder_mass,
        sc_cost=sc_cost,
        materials_cost=materials_cost,
        manufacturing_cost=manufacturing_cost,
        winding_capital=sc_cost + materials_cost + manufacturing_cost,
        ampere_metres=float(x["turn_current"]) * L,
    )


# ---------------------------------------------------------------------------------------------
# NIST 316 conductivity integral: composite Gauss-Legendre in u = ln T
# ---------------------------------------------------------------------------------------------
def k316(T: float, coeffs=NIST316_COEFFS) -> float:
    x = math.log10(T)
    return 10.0 ** sum(c * x ** i for i, c in enumerate(coeffs))


def _gauss_legendre(n: int):
    """Nodes and weights on [-1, 1] by Newton iteration on P_n (standard library only)."""
    nodes, weights = [], []
    for i in range(1, n + 1):
        x = math.cos(math.pi * (i - 0.25) / (n + 0.5))
        for _ in range(100):
            p0, p1 = 1.0, x
            for k in range(2, n + 1):
                p0, p1 = p1, ((2 * k - 1) * x * p1 - (k - 1) * p0) / k
            dp = n * (x * p1 - p0) / (x * x - 1.0)
            dx = p1 / dp
            x -= dx
            if abs(dx) < 1e-16:
                break
        p0, p1 = 1.0, x
        for k in range(2, n + 1):
            p0, p1 = p1, ((2 * k - 1) * x * p1 - (k - 1) * p0) / k
        dp = n * (x * p1 - p0) / (x * x - 1.0)
        nodes.append(x)
        weights.append(2.0 / ((1.0 - x * x) * dp * dp))
    return nodes, weights


_GL_NODES, _GL_WEIGHTS = _gauss_legendre(10)


def k316_integral(T_low: float, T_high: float = T_SHIELD, panels: int = 64) -> float:
    """K = integral_{T_low}^{T_high} k316(T) dT (W/m), 10-point Gauss-Legendre on `panels`
    equal sub-intervals of ln T."""
    if T_low == T_high:
        return 0.0
    sign = 1.0
    if T_low > T_high:
        T_low, T_high, sign = T_high, T_low, -1.0
    u0, u1 = math.log(T_low), math.log(T_high)
    h = (u1 - u0) / panels
    total = 0.0
    for j in range(panels):
        mid = u0 + (j + 0.5) * h
        for xi, wi in zip(_GL_NODES, _GL_WEIGHTS):
            u = mid + 0.5 * h * xi
            T = math.exp(u)
            total += wi * k316(T) * T
    return sign * 0.5 * h * total


# ---------------------------------------------------------------------------------------------
# Magnet cold-stage load (design section 2.5; contract section 6)
# ---------------------------------------------------------------------------------------------
def magnet_cold_stage_load(x: dict) -> dict:
    T = float(x["T_supply"])
    Ts = float(x.get("T_shield", T_SHIELD))
    Ta = float(x.get("T_amb", T_AMB))
    I = abs(float(x["turn_current"]))
    K_T = k316_integral(T, Ts)
    K_ref = k316_integral(float(x["T_conduction_ref"]), Ts)
    q_cond = float(x["conduction_ref"]) * K_T / K_ref
    q_rad = float(x["radiation_ref"])
    q_nuc = float(x["nuclear_density"]) * float(x["cold_volume"])
    L0 = float(x["L0"])
    lead_factor = float(x["f_lead"]) * float(x["n_leads"]) * I
    q_lead = lead_factor * math.sqrt(L0 * (Ts * Ts - T * T))
    q_joint = float(x["p_joint_ref"]) * (float(x["turn_current"]) / float(x["I_joint_ref"])) ** 2
    q_cold = float(x["load_multiplier"]) * (q_nuc + q_rad + q_cond + q_lead + q_joint)
    q_shield = float(x["shield_static"]) + lead_factor * math.sqrt(L0 * (Ta * Ta - Ts * Ts))
    return dict(
        q_nuclear=q_nuc,
        q_radiation=q_rad,
        q_conduction=q_cond,
        q_leads=q_lead,
        q_joints=q_joint,
        q_cold=q_cold,
        q_shield=q_shield,
        k_integral=K_T,
    )


# ---------------------------------------------------------------------------------------------
# Staged refrigeration screen (design section 2.6; contract section 6)
# ---------------------------------------------------------------------------------------------
def staged_refrigeration_screen(x: dict) -> dict:
    T = float(x["T_supply"])
    Ts = float(x.get("T_shield", T_SHIELD))
    Ta = float(x.get("T_amb", T_AMB))
    rating_kW = float(x["rating_cold"]) / 1000.0
    carnot = (Ta - T) / T
    carnot_ref = (Ta - float(x["T_green"])) / float(x["T_green"])
    equiv = carnot / carnot_ref
    capital_mode = float(x["capital_mode"])
    R_equiv = rating_kW * (equiv if capital_mode == 0.0 else 1.0)
    eta_mode = float(x["eta_mode"])
    if eta_mode == 1.0:
        eta = float(x["eta_const"])
        eta_arg = None
    else:
        eta_arg = rating_kW if eta_mode == 0.0 else rating_kW * equiv
        eta = float(x["green_a"]) * eta_arg ** float(x["green_b"])
    p_in_cold = float(x["q_cold"]) * carnot / eta
    p_in_shield = float(x["q_shield"]) * (Ta - Ts) / Ts / float(x["f_carnot_shield"])
    capital = float(x["green_c"]) * R_equiv ** float(x["green_d"]) * float(x["usd2015_to_2021"])
    args = [R_equiv] + ([eta_arg] if eta_arg is not None else [])
    extrap = 1 if any(a < GREEN_FIT_MIN_KW or a > GREEN_FIT_MAX_KW for a in args) else 0
    margin = float(x["rating_cold"]) - float(x["q_cold"])
    return dict(
        carnot_specific_power=carnot,
        eta_cold=eta,
        p_in_cold=p_in_cold,
        p_in_shield=p_in_shield,
        p_in_total_MW=(p_in_cold + p_in_shield) / 1e6,
        R_equiv_kW=R_equiv,
        refrigerator_capital=capital,
        capacity_margin=margin,
        capacity_pass=1 if margin >= 0.0 else 0,
        green_extrapolated=extrap,
    )


# ---------------------------------------------------------------------------------------------
# Subsystem annualized cost (design section 2.7; contract section 7)
# ---------------------------------------------------------------------------------------------
def subsystem_annualized_cost(x: dict) -> dict:
    capital_total = float(x["winding_capital"]) + float(x["refrigerator_capital"])
    annual_electricity = (float(x["p_in_total_MW"]) * float(x["hours"]) * float(x["availability"])
                          * float(x["electricity_price"]))
    return dict(
        capital_total=capital_total,
        annual_electricity=annual_electricity,
        annualized_cost=float(x["crf"]) * capital_total + annual_electricity,
    )


# ---------------------------------------------------------------------------------------------
# Matched pair comparison (design section 2.8; contract section 7)
# ---------------------------------------------------------------------------------------------
def matched_pair_comparison(x: dict) -> dict:
    rankable = int(x["all_pass_nb3sn"]) * int(x["all_pass_rebco"])
    both_supported = int(x["status_nb3sn"]) != 0 and int(x["status_rebco"]) != 0
    pair_status = int(x["status_nb3sn"]) if both_supported else 0
    diff = float(x["annualized_rebco"]) - float(x["annualized_nb3sn"])
    be_m = float(x["rebco_price_per_m"]) - diff / (float(x["crf"]) * float(x["rebco_element_length"]))
    ic = float(x["rebco_ic_tape_op"])
    be_kAm = be_m / (ic / 1000.0) if ic > 0.0 else math.nan
    return dict(
        rankable=rankable,
        pair_status=pair_status,
        cost_difference=diff,
        breakeven_rebco_price_per_m=be_m,
        breakeven_rebco_price_per_kAm=be_kAm,
    )


# ---------------------------------------------------------------------------------------------
# Case-level evaluation (design section 3 binding, section 6 names)
# ---------------------------------------------------------------------------------------------
def turn_current(duty: dict) -> float:
    return float(duty["I_ref"]) * float(duty["B_peak"]) / float(duty["B_ref"])


def evaluate_material(case: dict, material: str) -> dict:
    """All section-2 outputs for one material part. Returns {calc_name: outputs, ..., 'flat': merged}."""
    duty, econ, part = case["duty"], case["economics"], case[material]
    I = turn_current(duty)
    B = float(duty["B_peak"])
    cx = dict(part)
    cx.update(turn_current=I, B_peak=B)
    if material == "nb3sn":
        cond = nb3sn_cable_critical_surface(cx)
    elif material == "rebco":
        cond = rebco_cable_critical_surface(cx)
    else:
        raise KeyError(material)
    ax = dict(part)
    ax.update(turn_current=I, B_peak=B, available_area=duty["available_area"],
              element_area=cond["element_area_total"], element_copper_area=cond["element_copper_area"])
    area = winding_turn_area_screen(ax)
    ix = dict(part)
    ix.update(turn_current=I, turns=duty["turns"], coils=duty["coils"], turn_length=duty["turn_length"],
              element_area=cond["element_area_total"])
    inv = winding_inventory_and_cost(ix)
    lx = dict(part)
    lx.update(turn_current=I)
    cold = magnet_cold_stage_load(lx)
    rx = dict(part)
    rx.update(q_cold=cold["q_cold"], q_shield=cold["q_shield"], usd2015_to_2021=econ["usd2015_to_2021"])
    refr = staged_refrigeration_screen(rx)
    ann = subsystem_annualized_cost(dict(
        winding_capital=inv["winding_capital"], refrigerator_capital=refr["refrigerator_capital"],
        p_in_total_MW=refr["p_in_total_MW"], crf=econ["crf"], hours=econ["hours"],
        availability=econ["availability"], electricity_price=econ["electricity_price"]))
    all_pass = (cond["acceptance_pass"] * area["fit_pass"] * area["cu_pass"] * area["steel_pass"]
                * refr["capacity_pass"])
    flat = {}
    for block in (cond, area, inv, cold, refr, ann):
        flat.update(block)
    flat["turn_current"] = I
    flat["all_pass"] = all_pass
    return dict(conductor=cond, area=area, inventory=inv, cold_load=cold, refrigeration=refr,
                annualized=ann, all_pass=all_pass, flat=flat)


def evaluate_case(case: dict) -> dict:
    nb = evaluate_material(case, "nb3sn")
    re = evaluate_material(case, "rebco")
    pair = matched_pair_comparison(dict(
        annualized_nb3sn=nb["annualized"]["annualized_cost"],
        annualized_rebco=re["annualized"]["annualized_cost"],
        all_pass_nb3sn=nb["all_pass"], all_pass_rebco=re["all_pass"],
        status_nb3sn=nb["conductor"]["status_code"], status_rebco=re["conductor"]["status_code"],
        rebco_element_length=re["inventory"]["element_length"],
        rebco_price_per_m=case["rebco"]["element_price_per_m"],
        rebco_ic_tape_op=re["conductor"]["ic_tape_op"],
        crf=case["economics"]["crf"]))
    return dict(nb3sn=nb, rebco=re, pair=pair)


def ballarino_w_per_kA(T_cold: float, T_warm: float = T_AMB, L0: float = 2.45e-8) -> float:
    """Minimum heat leak of an optimized conduction-cooled lead, W/kA (Ballarino Table 1 form)."""
    return 1000.0 * math.sqrt(L0 * (T_warm * T_warm - T_cold * T_cold))
