"""WI-022 prototype grid: profile-integrated D-T fusion power, anchor-derived exponents.

Image-verified Point-A inputs (Table 5 IMAGE page_009_table_0.png + Fig 16 panels):
  n_D0 = n_T0 = 1.96e20 m^-3   (peak fuel densities, printed)
  T_i0 = 14.63 keV             (peak ion temperature, printed)
  V_source = 425 m^3           (Table 5's own plasma volume, printed)
  V_model  = 448 m^3           (WI-020 model volume, owner-ratified Table-2 target)
  P_fus (printed, cross-checked vs tritium burn rate 416.57 g/day) = 2700 MW
  Peak fusion heating (printed) = 5.51 MW/m^3 ; Table 4 image: f_alpha = 0.95

Digitized Fig 16 fits: alpha_T = 1.19 (all species), alpha_n(fuel) = 0.33.
Caption (text-extracted, refuted by figure): alpha_n = 1.2, alpha_T = 3.0.
"""
import json
import numpy as np

def sigv_dt(T_keV):
    """D-T reactivity [m^3/s], Bosch-Hale (1costingFE reactivity.py:54-70)."""
    BG, mrc2 = 34.3827, 1124656.0
    C1, C2, C3 = 1.17302e-9, 1.51361e-2, 7.51886e-2
    C4, C5, C6, C7 = 4.60643e-3, 1.35000e-2, -1.06750e-4, 1.36600e-5
    T = np.asarray(T_keV, dtype=float)
    theta = T / (1.0 - T*(C2 + T*(C4 + T*C6))/(1.0 + T*(C3 + T*(C5 + T*C7))))
    xi = (BG**2/(4.0*theta))**(1.0/3.0)
    return C1*theta*np.sqrt(xi/(mrc2*T**3))*np.exp(-3.0*xi)*1e-6

nD0 = nT0 = 1.96e20
Ti0 = 14.63
E_fus_J = 17.58e6 * 1.602176634e-19
V_SRC, V_MODEL = 425.0, 448.0

rho = np.linspace(0.0, 1.0, 200_001)
u = 1.0 - rho**2

def p_fus_param(an, aT, V):
    nD = nD0 * u**an
    Ti = np.maximum(Ti0 * u**aT, 1e-6)
    integrand = nD * nD * sigv_dt(Ti) * E_fus_J * 2.0 * rho
    return np.trapezoid(integrand, rho) * V / 1e6

print("peak fusion power density  =", f"{nD0*nT0*sigv_dt(Ti0)*E_fus_J/1e6:.3f} MW/m^3")
print("  x f_alpha 0.95 (alpha part x5.51/... check): peak heating pred =",
      f"{nD0*nT0*sigv_dt(Ti0)*E_fus_J/1e6*0.95:.3f}  (source prints 5.51; f_alpha=0.95 Table 4)")

print(f"\n{'alpha_n':>8} {'alpha_T':>8} {'P@V=425':>9} {'P@V=448':>9}   note")
CASES = [
    (1.2, 3.0,  "caption pair (text) — refuted by figure"),
    (1.2, 1.2,  "prior session's 'figure-consistent' guess"),
    (0.35, 1.2, "pre-image estimate (garbled-table-derived)"),
    (0.33, 1.19, "DIGITIZED Fig 16 fits (anchor-derived)"),
    (0.33, 1.0,  "sensitivity: flatter T"),
    (0.33, 1.27, "sensitivity: steeper T (elec-frac BC)"),
    (0.0, 0.0,   "flat-profile limit (0D at peak values)"),
]
for an, aT, note in CASES:
    p425 = p_fus_param(an, aT, V_SRC)
    p448 = p_fus_param(an, aT, V_MODEL)
    print(f"{an:8.2f} {aT:8.2f} {p425:9.1f} {p448:9.1f}   {note}")

# --- nonparametric: integrate directly over the digitized curves ---
with open("/tmp/wi022_proto/fig16_curves.json") as f:
    C = json.load(f)

def interp_frac(key):
    r = np.array(C[key]["rho"]); v = np.array(C[key]["frac"])
    o = np.argsort(r)
    return np.interp(rho, r[o], v[o], left=v[o][0], right=0.0)

f_n = interp_frac("n_green")      # tritium density curve (cleanest fuel trace)
f_T = interp_frac("T_green")      # tritium temperature curve
nD = nD0 * f_n
Ti = np.maximum(Ti0 * f_T, 1e-6)
integrand = nD * nD * sigv_dt(Ti) * E_fus_J * 2.0 * rho
avg = np.trapezoid(integrand, rho)
print(f"\nnonparametric (digitized curves): P@V=425 = {avg*V_SRC/1e6:.1f} MW, "
      f"P@V=448 = {avg*V_MODEL/1e6:.1f} MW   (source design point: 2700)")

# volume-average consistency cross-checks vs Table 5 image
fe = interp_frac("n_blue")
print(f"\n<n_e>/n_e0 digitized (2 rho drho) = {np.trapezoid(fe*2*rho, rho):.3f}  "
      f"(Table 5 image: 3.17/5.06 = {3.17/5.06:.3f})")
print(f"<n_fuel>/n_fuel0 digitized        = {np.trapezoid(f_n*2*rho, rho):.3f}")
