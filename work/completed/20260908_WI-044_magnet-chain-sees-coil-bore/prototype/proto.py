"""WI-044 design prototype: the anchored coil-bore shapes in the generated arithmetic order.

Replicates the radial build and the axis field exactly as the generated modules
compute them (mfe_radial_build.py, coil_set_axis_field.py) and evaluates the three
anchored forms in the operation order the design authors, at P0-P3. Prints the
reference floats to bind and checks the design-point identity to the double.
"""
import json, sys
from pathlib import Path

MU0 = 1.25663706212e-6; TWO_PI = 6.283185307179586
LAYERS = dict(vacuum_t=0.10, firstwall_t=0.05, blanket_t=0.80, reflector_t=0.20,
              ht_shield_t=0.20, structure_t=0.15, gap1_t=0.10, vessel_t=0.10, coil_t=0.30)
K_LINK = 0.7731331164622419; N_COILS = 48.0; PEAK_RATIO = 2.7666666666666666
K_SIGMA = 0.6102331403536223; F_COND = 0.6666666666666666; E_WP = 200000000000.0
STEEL = 6.0; F_FAB = 3.0; W_REF = 111.0e9; I_REF = 15400000.0; R_REF = 12.7; M_REF = 63000.0

def radial(a):
    L = LAYERS
    vacuum_or = a + L["vacuum_t"]; firstwall_or = vacuum_or + L["firstwall_t"]
    blanket_or = firstwall_or + L["blanket_t"]; reflector_or = blanket_or + L["reflector_t"]
    ht_shield_or = reflector_or + L["ht_shield_t"]; structure_or = ht_shield_or + L["structure_t"]
    gap1_or = structure_or + L["gap1_t"]; vessel_or = gap1_or + L["vessel_t"]
    r_coil_centre = vessel_or + L["coil_t"] / 2.0          # the authored expression
    return vessel_or, r_coil_centre

def b_axis(I, R0):
    return MU0 * K_LINK * N_COILS * I / (TWO_PI * R0)

A_COIL_REF = radial(1.3)[1]

def chain(R0, a, I, j_wp=118.8271604938272):
    vessel_or, a_coil = radial(a)
    B = b_axis(I, R0)
    # 'Conductor Peak Field' (geometry-aware): two intermediates, then the product
    bore_factor = R0 / (R0 - a_coil)
    bore_factor_ref = R_REF / (R_REF - A_COIL_REF)
    bore_norm = bore_factor / bore_factor_ref
    B_peak = B * PEAK_RATIO * bore_norm
    B_peak_old = B * PEAK_RATIO
    wp_side = (I / j_wp) ** 0.5 / 1000.0
    sigma = K_SIGMA * I * B_peak / wp_side
    eps = F_COND * sigma / E_WP
    # 'Coil Set Stored Energy'
    W = W_REF * (I / I_REF) ** 2 * (a_coil / A_COIL_REF) ** 2 * (R_REF / R0)
    # 'Magnet Casing Mass'
    m = M_REF * (W / W_REF) ** 0.78
    struct = N_COILS * m * STEEL * F_FAB
    struct_old = N_COILS * M_REF * STEEL * F_FAB
    return dict(R0=R0, a=a, I=I, vessel_or=vessel_or, a_coil=a_coil, B_axis=B, bore_norm=bore_norm,
                B_peak=B_peak, B_peak_old=B_peak_old, sigma_wp=sigma, eps_cond=eps, W_mag=W,
                m_casing=m, structure_cost=struct, structure_cost_old=struct_old,
                peak_field_ok=B_peak <= 24.9, wp_stress_ok=sigma <= 8.0e8, cond_strain_ok=eps <= 0.004,
                aspect_ratio=R0 / a)

pts = {"P0_baseline": (12.7, 1.3, 15400000.0), "P1_design_a1.4": (12.7, 1.4, 15400000.0),
       "P2_design_a2.2": (12.7, 2.2, 15400000.0), "P3_c2823": (15.7, 2.2, 13000000.0)}
out = {k: chain(*v) for k, v in pts.items()}
print("a_coil_ref (coil centre at a=1.3) =", repr(A_COIL_REF), " vessel_or =", repr(radial(1.3)[0]))
p0 = out["P0_baseline"]
print("P0 B_axis", repr(p0["B_axis"]), "bore_norm", repr(p0["bore_norm"]), "B_peak", repr(p0["B_peak"]),
      "== 24.9:", p0["B_peak"] == 24.9, "| old", repr(p0["B_peak_old"]))
print("P0 W_mag", repr(p0["W_mag"]), "m_casing", repr(p0["m_casing"]), "struct", repr(p0["structure_cost"]),
      "== old:", p0["structure_cost"] == p0["structure_cost_old"], "sigma", repr(p0["sigma_wp"]), "eps", repr(p0["eps_cond"]))
for k, v in out.items():
    print(k, {kk: (round(vv, 6) if isinstance(vv, float) else vv) for kk, vv in v.items() if kk not in ("B_axis",)})
Path(__file__).with_name("proto_results.json").write_text(json.dumps({"a_coil_ref": A_COIL_REF, "points": out}, indent=2))
