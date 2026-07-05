"""WI-016 H2 Probe — comparison phase.

Evaluates the blind-derived relations (derivation.md, frozen) against the
1costingfe answer key at the concept 01 (ARC-class) and 20a (Infinity Two
stellarator) design points, plus an R x B0 scaling grid.

Run from the fusion-tea repo root:
    uv run python work/active/WI-016_h2-blind-derivation/comparison/compare.py

Outputs (same directory as this file):
    results.json — point-value comparisons
    grid.csv     — R x B0 sweep, derived vs answer key
"""

import csv
import json
import math
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = Path("/home/reid/1cfe/fusion-tea")
sys.path.insert(0, str(REPO / "exploration" / "concept_analysis" / "scripts"))

from costingfe import ConfinementConcept, CostModel, Fuel  # noqa: E402
from costingfe.layers.geometry import RadialBuild, compute_geometry  # noqa: E402
from costingfe.layers.physics import mfe_forward_power_balance  # noqa: E402
from costingfe.layers.tokamak import (  # noqa: E402
    MU_0,
    compute_beta_N,
    compute_fusion_power,
    compute_greenwald_density,
    compute_plasma_current,
    _plasma_volume,
)
from lib.model_setup_helpers import generic_reference  # noqa: E402

MU0 = 1.25663706127e-06
E_KEV = 1.602176634e-16  # J per keV
E_FUS_MEV = 17.6  # derived model's D-T energy (pretraining value)
E_FUS_J = E_FUS_MEV * 1e6 * 1.602176634e-19

# ===========================================================================
# Derived relations (implemented exactly as written in derivation.md)
# ===========================================================================


def derived_pfus_from_state(n_e, T_keV, V, C_prof=1.05):
    """Relation 1, plasma-state form: S = (n^2/4) <sigma v> E_fus,
    <sigma v> = 1.1e-24 T^2 [m^3/s] (quadratic closure, 10-20 keV)."""
    sigv = 1.1e-24 * T_keV**2
    S = 0.25 * n_e**2 * sigv * E_FUS_J  # W/m^3
    return S * V * 1e-6 * C_prof  # MW


def derived_pfus_from_beta(beta_T, B0, R, a, kappa, C_prof=1.05):
    """Relation 1, beta form: P_fus = 1.20 C_prof beta_T^2 B0^4 (2 pi^2 R a^2 k)."""
    V = 2 * math.pi**2 * R * a**2 * kappa
    return 1.20 * C_prof * beta_T**2 * B0**4 * V


def derived_power_balance(p_fus, p_aux_coupled, eta_th, eta_wp, M_n=1.2,
                          p_cryo=1.0, p_house=0.0):
    """Relation 2 as written."""
    p_alpha = p_fus / 5.0
    p_n = 4.0 * p_fus / 5.0
    p_th = M_n * p_n + p_alpha + p_aux_coupled
    p_gross = eta_th * p_th
    p_recirc = p_aux_coupled / eta_wp + p_cryo + p_house
    p_net = p_gross - p_recirc
    return dict(
        p_alpha=p_alpha, p_n=p_n, p_th=p_th, p_gross=p_gross,
        p_recirc=p_recirc, p_net=p_net,
        q_p=p_fus / p_aux_coupled,
        q_e=p_net / p_recirc,
        f_recirc=p_recirc / p_gross,
    )


def derived_magnet_cost(R, B0, ell_coil, I_tape=660.0, c_hts_lo=18.0,
                        c_hts_hi=36.0, E_mag=None, k_st=20.0,
                        c_fab=1.06, sigma_allow=6.6e8, rho=7900.0,
                        r_coil=None):
    """Relation 3 as written. Costs in M$ (2014$ for the FOAK anchors).

    Conductor: L_tape = (2 pi R B0 / mu0) * ell / I_tape; cost = c_hts * L.
    Structure: M = k_st * rho * E_mag / sigma; cost = c_fab [M$/t] * M [t].
    If E_mag is None it is estimated as (B0^2/2mu0) * V_field with
    V_field = 2 pi R * pi r_coil^2 (torus of bore r_coil).
    """
    NI = 2 * math.pi * R * B0 / MU0  # ampere-turns
    L_tape_m = NI * ell_coil / I_tape
    cond_lo = c_hts_lo * L_tape_m / 1e6  # M$
    cond_hi = c_hts_hi * L_tape_m / 1e6
    kAm = NI * ell_coil / 1000.0
    if E_mag is None:
        V_field = 2 * math.pi * R * math.pi * r_coil**2
        E_mag = B0**2 / (2 * MU0) * V_field
    M_struct_t = k_st * rho * E_mag / sigma_allow / 1000.0  # tonnes
    struct_cost = c_fab * M_struct_t  # M$
    return dict(
        NI=NI, L_tape_km=L_tape_m / 1e3, kAm=kAm,
        conductor_lo=cond_lo, conductor_hi=cond_hi,
        E_mag_GJ=E_mag / 1e9, M_struct_t=M_struct_t,
        structure=struct_cost,
        total_lo=cond_lo + struct_cost, total_hi=cond_hi + struct_cost,
    )


# ===========================================================================
# Answer key helpers
# ===========================================================================

def answer_key_coil_cost(concept, B, R0, r_coil, per_kam=50.0, markup=None,
                         path_factor=2.0):
    """cas22.py C220103 tokamak/stellarator branch, reproduced exactly.
    total_kAm = G * b_center * R0 * r_coil / (mu0 * 1000); G = 4pi^2 (tokamak)
    or 4pi^2 * path_factor (stellarator). Cost = kAm * $/kAm * markup / 1e6 M$.
    Markups from costing_constants.yaml: tokamak 3.09, stellarator 5.87."""
    if concept == "stellarator":
        G = 4 * math.pi**2 * path_factor
        markup = 5.87 if markup is None else markup
    else:
        G = 4 * math.pi**2
        markup = 3.09 if markup is None else markup
    total_kAm = G * B * R0 * r_coil / (MU0 * 1000)
    conductor = total_kAm * per_kam / 1e6  # M$
    return dict(G=G, kAm=total_kAm, conductor=conductor, c220103=conductor * markup)


def vessel_or_from_params(p):
    rb = RadialBuild(
        R0=p["R0"], plasma_t=p["plasma_t"], elon=p.get("elon", 1.0),
        blanket_t=p["blanket_t"], ht_shield_t=p["ht_shield_t"],
        structure_t=p["structure_t"], vessel_t=p["vessel_t"],
    )
    return rb


# ===========================================================================
# Main
# ===========================================================================

results = {}

# ---- ARC published anchor (source-quoted, derivation.md header) ----
ARC = dict(R=3.3, a=1.13, kappa=1.84, B0=9.2, Ip=7.8, n20=1.3, T=13.9,
           beta_N=2.59, p_fus_pub=525.0, p_net_pub=190.0, q_e_pub=3.0)

# ===========================================================================
# 1. Relation 1 — fusion power at the ARC point
# ===========================================================================
V_arc = 2 * math.pi**2 * ARC["R"] * ARC["a"]**2 * ARC["kappa"]
n_e = ARC["n20"] * 1e20

pfus_derived = derived_pfus_from_state(n_e, ARC["T"], V_arc, C_prof=1.05)
pfus_derived_flat = derived_pfus_from_state(n_e, ARC["T"], V_arc, C_prof=1.0)
pfus_key = float(compute_fusion_power(n_e, ARC["T"], V_arc))

# beta-form cross-check (derivation.md worked example)
beta_T = ARC["beta_N"] * ARC["Ip"] / (ARC["a"] * ARC["B0"]) / 100.0
pfus_derived_beta = derived_pfus_from_beta(beta_T, ARC["B0"], ARC["R"],
                                           ARC["a"], ARC["kappa"], C_prof=1.05)

# answer-key implied q95 / f_GW at the ARC operating point
q95_arc = float(2 * math.pi * ARC["a"]**2 * ARC["kappa"] * ARC["B0"]
                / (MU_0 * ARC["R"] * ARC["Ip"] * 1e6))
nGW = float(compute_greenwald_density(ARC["Ip"], ARC["a"]))
f_GW_arc = ARC["n20"] / nGW
beta_N_key = float(compute_beta_N(n_e, ARC["T"], ARC["T"], 1.0, ARC["B0"],
                                  ARC["Ip"], ARC["a"]))

results["relation1_arc_point"] = dict(
    published=ARC["p_fus_pub"],
    derived_state_form_Cprof105=round(pfus_derived, 1),
    derived_state_form_Cprof100=round(pfus_derived_flat, 1),
    derived_beta_form_Cprof105=round(pfus_derived_beta, 1),
    answer_key_bosch_hale=round(pfus_key, 1),
    V_plasma=round(V_arc, 1),
    q95_implied=round(q95_arc, 2), f_GW_implied=round(f_GW_arc, 3),
    beta_N_answer_key=round(beta_N_key, 2),
    sigv_quadratic_13p9keV=1.1e-24 * 13.9**2,
)

# ===========================================================================
# 2. Grid sweep: R x B0, everything else fixed at ARC values.
#    Common closure: Ip from q95 (fixed at ARC-implied 4.20), n = f_GW * n_GW
#    (f_GW fixed 0.669), T fixed 13.9 keV. This isolates the reactivity
#    functional form (quadratic vs Bosch-Hale). The derived model's native
#    Troyon-pinned closure is also evaluated (beta_N = 2.59 fixed).
# ===========================================================================
grid_rows = []
for R in (2.5, 3.3, 4.5, 6.0):
    for B0 in (5.0, 7.0, 9.0, 12.0):
        a, kappa, T = ARC["a"], ARC["kappa"], ARC["T"]
        Ip = float(compute_plasma_current(a, kappa, B0, R, q95_arc))
        n = f_GW_arc * float(compute_greenwald_density(Ip, a)) * 1e20
        V = float(_plasma_volume(R, a, kappa))
        pf_key = float(compute_fusion_power(n, T, V))
        pf_der = derived_pfus_from_state(n, T, V, C_prof=1.05)
        # derived native closure: beta pinned at Troyon margin
        bT = ARC["beta_N"] * Ip / (a * B0) / 100.0
        pf_der_troyon = derived_pfus_from_beta(bT, B0, R, a, kappa, C_prof=1.05)
        bN = float(compute_beta_N(n, T, T, 1.0, B0, Ip, a))
        # magnet cost per formula, both sides (NOAK-comparable conductor only,
        # answer-key geometry: r_coil = vessel outer radius with concept-01
        # radial build: a + 0.15 (vac+fw) + 0.8 + 0.2 (refl) + 0.2 + 0.2 + 0.1
        # (gap) + 0.2)
        r_coil = a + 0.15 + 0.8 + 0.2 + 0.2 + 0.2 + 0.1 + 0.2
        key_coil = answer_key_coil_cost("tokamak", B0, R, r_coil)
        der_mag = derived_magnet_cost(R, B0, ell_coil=2 * math.pi * r_coil,
                                      r_coil=r_coil)
        grid_rows.append(dict(
            R=R, B0=B0, Ip_MA=round(Ip, 2), n20=round(n / 1e20, 3),
            beta_N=round(bN, 2),
            pfus_key=round(pf_key, 1), pfus_derived=round(pf_der, 1),
            ratio_der_over_key=round(pf_der / pf_key, 3),
            pfus_derived_troyon=round(pf_der_troyon, 1),
            key_kAm=round(key_coil["kAm"], 0),
            derived_kAm=round(der_mag["kAm"], 0),
            key_C220103_M=round(key_coil["c220103"], 1),
            derived_conductor_mid_M=round(
                0.5 * (der_mag["conductor_lo"] + der_mag["conductor_hi"]), 1),
            derived_structure_M=round(der_mag["structure"], 0),
        ))

with open(HERE / "grid.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(grid_rows[0].keys()))
    w.writeheader()
    w.writerows(grid_rows)

# Temperature sweep: the R x B0 grid holds T fixed, so the derived/key P_fus
# ratio is constant there. The only functional difference between the two
# reactivity models is the T dependence — expose it directly.
from costingfe.layers.tokamak import sigma_v_dt  # noqa: E402
results["reactivity_T_sweep"] = {
    f"{T:g}_keV": round(1.1e-24 * T**2 / float(sigma_v_dt(T)), 3)
    for T in (5.0, 8.0, 10.0, 13.9, 15.0, 20.0, 25.0, 30.0)
}

# ===========================================================================
# 3. Relation 2 — power balance at the ARC point (p_fus = 525 MW)
# ===========================================================================
# Derived, as in the worked example: eta_wp such that 38.6 MW coupled costs
# 69 MW wall-plug (25/0.50 + 19), cryo ~1 MW.
eta_wp_arc = 38.6 / 69.0
der_pb_12 = derived_power_balance(525.0, 38.6, 0.40, eta_wp_arc, M_n=1.2)
der_pb_11 = derived_power_balance(525.0, 38.6, 0.40, eta_wp_arc, M_n=1.1)

# Answer key: mfe_forward_power_balance at the same point. ARC-matched
# efficiencies (eta_th=0.40, eta_pin=38.6/69), tokamak-YAML house loads,
# wall_material=None -> p_rad = bremsstrahlung + synchrotron (Z_eff 1.2).
def key_balance(mn, zero_aux_loads=False, p_rad_off=False):
    aux = dict(p_coils=2.0, p_cool=13.7, p_pump=1.0, p_trit=10.0,
               p_house=4.0, p_cryo=0.5, f_sub=0.03)
    if zero_aux_loads:
        aux = dict(p_coils=0.0, p_cool=0.0, p_pump=0.0, p_trit=0.0,
                   p_house=0.0, p_cryo=1.0, f_sub=0.0)
    pt = mfe_forward_power_balance(
        p_fus=525.0, fuel=Fuel.DT, p_input=38.6, mn=mn, eta_th=0.40,
        eta_p=0.5, eta_pin=eta_wp_arc, eta_de=0.85, f_dec=0.0,
        n_e=n_e, T_e=ARC["T"], Z_eff=1.2, plasma_volume=V_arc, B=ARC["B0"],
        dd_f_T=0.969, dd_f_He3=0.689, dhe3_dd_frac=0.131, dhe3_f_T=0.5,
        dhe3_f_He3=0.1, pb11_f_alpha_n=0.0, pb11_f_p_n=0.0,
        wall_material=None, T_edge=0.05, tau_ratio=3.0, fw_area=0.0,
        R_major=ARC["R"], a_minor=ARC["a"], kappa=ARC["kappa"], R_w=0.6,
        f_rad_fus=(0.0 if p_rad_off else None),
        **aux,
    )
    return {k: round(float(getattr(pt, k)), 2) for k in
            ("p_ash", "p_neutron", "p_rad", "p_th", "p_the", "p_et",
             "p_net", "q_sci", "q_eng", "rec_frac", "p_input")}

results["relation2_arc_point"] = dict(
    published=dict(p_net=190.0, q_e=3.0, q_p=13.6),
    derived_Mn12={k: round(v, 2) for k, v in der_pb_12.items()},
    derived_Mn11={k: round(v, 2) for k, v in der_pb_11.items()},
    key_mn11_full_loads=key_balance(1.1),
    key_mn12_full_loads=key_balance(1.2),
    key_mn12_arc_matched_loads=key_balance(1.2, zero_aux_loads=True),
    note=("key rec_frac = recirc/p_et, same definition as derived f_recirc; "
          "key q_eng = p_et/recirc, so derived q_e = q_eng - 1 equivalent"),
)

# ===========================================================================
# 4. Actual answer-key runs at both design points (native generic forwards,
#    identical to the concept model_setup.py generic references).
# ===========================================================================
spec01 = dict(R0=3.3, plasma_t=1.1, elon=1.8, B=9.2, p_input=38.6)
m01 = CostModel(concept=ConfinementConcept.TOKAMAK, fuel=Fuel.DT)
g01 = generic_reference(m01, spec01, 233.0)
pt01 = g01.power_table
rb01 = vessel_or_from_params(g01.params)
geo01 = compute_geometry(rb01, ConfinementConcept.TOKAMAK)

# direct forward for the 0D plasma-state detail (same call generic_reference
# makes under the hood: use_0d_model=True, library availability/lifetime)
from costingfe.validation import CostingInput, default_availability  # noqa: E402
fr01 = m01.forward(
    net_electric_mw=233.0,
    availability=default_availability(m01.concept),
    lifetime_yr=CostingInput.model_fields["lifetime_yr"].default,
    use_0d_model=True,
    **spec01,
)
ps01 = fr01.plasma_state

results["concept01_native_run"] = dict(
    target_net_MW=233.0,
    p_fus=round(float(pt01.p_fus), 1), p_net=round(float(pt01.p_net), 1),
    p_th=round(float(pt01.p_th), 1), p_et=round(float(pt01.p_et), 1),
    q_eng=round(float(pt01.q_eng), 2), rec_frac=round(float(pt01.rec_frac), 3),
    eta_th=float(g01.params["eta_th"]), mn=float(g01.params["mn"]),
    eta_pin=round(float(g01.params.get("eta_pin", 0.0)), 3),
    C220103=round(g01.cas22_detail.get("C220103", 0.0), 1),
    vessel_or=round(float(geo01.vessel_or), 3),
    plasma_state=(None if ps01 is None else dict(
        I_p=round(float(ps01.I_p), 2),
        T_e=round(float(ps01.T_e), 2),
        n_e20=round(float(ps01.n_e) / 1e20, 3),
        beta_N=round(float(ps01.beta_N), 2),
        f_GW=round(float(ps01.f_GW), 3),
        p_rad=round(float(ps01.p_rad), 1),
    )),
)

# reproduce C220103 by formula with the run's actual r_coil
key01 = answer_key_coil_cost("tokamak", 9.2, 3.3, float(geo01.vessel_or))
results["concept01_coil_formula_check"] = {
    k: round(v, 1) for k, v in key01.items()}

# Derived magnet cost at concept 01 geometry (same bore for the perimeter)
der01_geom = derived_magnet_cost(3.3, 9.2,
                                 ell_coil=2 * math.pi * float(geo01.vessel_or),
                                 r_coil=float(geo01.vessel_or))
# Derived magnet cost with ARC-corpus anchors (ell=25 m, E_mag=18 GJ)
der01_arc = derived_magnet_cost(3.3, 9.2, ell_coil=25.0, E_mag=18e9)
der01_arc_kst7 = derived_magnet_cost(3.3, 9.2, ell_coil=25.0, E_mag=18e9,
                                     k_st=7.0)
results["concept01_magnet_cost"] = dict(
    answer_key_C220103_computed=round(g01.cas22_detail.get("C220103", 0.0), 1),
    analyst_override_noak=1030.0,
    arc_paper_foak_fabricated="5100-5200 (2014$, structure-dominated)",
    derived_geombore={k: round(float(v), 1) for k, v in der01_geom.items()},
    derived_arc_anchored_kst20={k: round(float(v), 1)
                                for k, v in der01_arc.items()},
    derived_arc_anchored_kst7={k: round(float(v), 1)
                               for k, v in der01_arc_kst7.items()},
    derived_effective_dollars_per_kAm="27-55 (2014 FOAK tape at 23 T/20 K)",
    key_effective_dollars_per_kAm=50.0 * 3.09,
)

# ---- 20a stellarator ----
spec20a = dict(R0=12.5, plasma_t=1.25, B=9.0, p_input=20.0, elon=1.0)
m20 = CostModel(concept=ConfinementConcept.STELLARATOR, fuel=Fuel.DT)
g20 = generic_reference(m20, spec20a, 350.0)
pt20 = g20.power_table
rb20 = vessel_or_from_params(g20.params)
geo20 = compute_geometry(rb20, ConfinementConcept.STELLARATOR)

results["concept20a_native_run"] = dict(
    target_net_MW=350.0,
    p_fus=round(float(pt20.p_fus), 1), p_net=round(float(pt20.p_net), 1),
    p_th=round(float(pt20.p_th), 1), p_et=round(float(pt20.p_et), 1),
    q_eng=round(float(pt20.q_eng), 2), rec_frac=round(float(pt20.rec_frac), 3),
    eta_th=float(g20.params["eta_th"]), mn=float(g20.params["mn"]),
    eta_pin=round(float(g20.params.get("eta_pin", 0.0)), 3),
    C220103=round(g20.cas22_detail.get("C220103", 0.0), 1),
    vessel_or=round(float(geo20.vessel_or), 3),
    published=dict(p_fus=800.0, q_p=40.0, eta_th=">0.30"),
)

# Derived power balance forward at the published 20a point
# (P_fus=800, coupled ECRH 20 MW, gyrotron wall-plug ~0.4-0.5)
der20_small = derived_power_balance(800.0, 20.0, 0.33, 0.45, M_n=1.2,
                                    p_cryo=5.0, p_house=0.0)
der20_house = derived_power_balance(800.0, 20.0, 0.33, 0.45, M_n=1.2,
                                    p_cryo=5.0, p_house=65.0)
results["concept20a_derived_balance"] = dict(
    published_p_net=350.0,
    derived_small_house={k: round(v, 2) for k, v in der20_small.items()},
    derived_70MW_house={k: round(v, 2) for k, v in der20_house.items()},
)

# 20a coil: answer key formula vs derived
key20 = answer_key_coil_cost("stellarator", 9.0, 12.5, float(geo20.vessel_or))
der20_mag = derived_magnet_cost(12.5, 9.0,
                                ell_coil=2 * math.pi * float(geo20.vessel_or),
                                r_coil=float(geo20.vessel_or))
results["concept20a_magnet_cost"] = dict(
    answer_key_C220103=round(g20.cas22_detail.get("C220103", 0.0), 1),
    formula_check={k: round(v, 1) for k, v in key20.items()},
    derived_same_bore={k: round(float(v), 1) for k, v in der20_mag.items()},
    key_stellarator_penalty_vs_tokamak=round((2 * 5.87) / 3.09, 2),
    derived_f3d_range="2-5 (judgment; corpus gives direction only)",
)

with open(HERE / "results.json", "w") as f:
    json.dump(results, f, indent=2)

print(json.dumps(results, indent=2))
print("\nGrid written to", HERE / "grid.csv")
