"""Attribution, second pass -- the printed point A under the SOURCED definition of W.

REQ-W-01 (run 20260905T145916478870) registered the same author's systems-code paper (Lion et al.
2021, Nucl. Fusion 61 126021, Eqs. (8)-(11)) and thesis (Lion 2023, Eqs. (2.10)-(2.12)): W is the
thermal energy from the imposed species profiles, W = V * 3/2 * int_0^1 drho sqrt(g) n T with the
effective-radius element sqrt(g) ~ rho, no fast-alpha term. The Stellaris paper's own rules (p. 8-9,
Appendix A): T_e = T_e0 (1-rho^2)^1.2, n_i = n_i0 (1-rho^2)^0.35 (Eqs. 2-3, Fig. 16), T_i/T_e = 0.95,
helium ash from A.5 (n_He / tau*_alpha = n_D n_T <sigma v>, tau* = 8 tau_E, uniform in rho), V = 425 m^3,
B0 = 9.0 T axis-averaged. This script applies exactly that, on the printed peaks, and reports what it
gives for W, beta, p_fus, n_e0 and <n_e>. Nothing is fitted to 504.65 MJ. Oracle-side arithmetic,
not package evidence; the reactivity is the oracle's own (_sigv_dt).
"""
import json, sys
from pathlib import Path
import numpy as np
HERE = Path(__file__).resolve().parent
REPO = HERE.parents[5]
sys.path.insert(0, str(REPO / "exploration" / "stellarator_e2e"))
import verify_stellaris as vs

KEV = 1.602176634e-16; MU0 = 1.25663706212e-6; E_FUS = 2.817e-12
PR = dict(n_e0=5.06e20, n_D0=1.96e20, n_T0=1.96e20, n_He0=0.56e20, T_e0=15.40, T_i0=14.63,
          n_e_volav=3.17e20, beta_volav=0.0276, W_total_MJ=504.65, V=425.0, B0=9.0, p_fus=2700.0)
rho = np.linspace(0.0, 1.0, 20001); u = 1.0 - rho**2
w = 2.0 * rho                                   # sqrt(g) ~ rho, normalised: int_0^1 2 rho drho = 1
def volav(f): return np.trapezoid(f * w, rho)       # <f> over V

def point(alpha_T=1.2, alpha_n=0.35, ti_ratio=0.95, ash="A5", alpha_He=None, alpha_ne=None, T_i0=None):
    T_e = PR["T_e0"] * u**alpha_T
    T_i = (T_i0 if T_i0 is not None else ti_ratio * PR["T_e0"]) * u**alpha_T
    n_D = PR["n_D0"] * u**alpha_n; n_T = PR["n_T0"] * u**alpha_n
    sigv = np.array([vs._sigv_dt(max(t, 1e-3)) for t in T_i])
    if ash == "A5":                             # n_He proportional to n_D n_T <sigma v>(T_i), scaled to the printed peak
        shape = n_D * n_T * sigv; n_He = PR["n_He0"] * shape / shape[0]
    else:                                       # power law
        n_He = PR["n_He0"] * u**alpha_He
    n_e = PR["n_e0"] * u**alpha_ne if alpha_ne is not None else n_D + n_T + 2 * n_He
    p = KEV * (n_e * T_e + (n_D + n_T + n_He) * T_i)
    W = 1.5 * volav(p) * PR["V"] * 1e-6
    beta = 2 * MU0 * volav(p) / PR["B0"]**2
    pfus = E_FUS * volav(n_D * n_T * sigv) * PR["V"] * 1e-6
    # effective power-law exponent of the ash shape (least squares on log, rho <= 0.85)
    m = rho <= 0.85
    a_He_eff = float(np.polyfit(np.log(u[m][1:]), np.log(n_He[m][1:] / n_He[0]), 1)[0]) if ash == "A5" else alpha_He
    return dict(W_MJ=float(W), vs_printed_pct=float(100 * (W / PR["W_total_MJ"] - 1)), beta_pct=float(100 * beta),
                p_fus_MW=float(pfus), n_e0=float(n_e[0]), n_e_volav=float(volav(n_e)), alpha_He_eff=a_He_eff,
                W_e_MJ=float(1.5 * volav(KEV * n_e * T_e) * PR["V"] * 1e-6), W_i_MJ=float(1.5 * volav(KEV * (n_D + n_T + n_He) * T_i) * PR["V"] * 1e-6))

out = {}
def rec(tag, r, note=""):
    out[tag] = dict(r, note=note)
    print(f"{tag:58s} W {r['W_MJ']:6.1f} MJ ({r['vs_printed_pct']:+5.1f} %)  beta {r['beta_pct']:.2f} %  p_fus {r['p_fus_MW']:6.0f}  n_e0 {r['n_e0']/1e20:.2f}  <n_e> {r['n_e_volav']/1e20:.2f}  alpha_He_eff {r['alpha_He_eff']:.2f}  {note}")

print("printed: W 504.65, beta 2.76, p_fus 2700, n_e0 5.06, <n_e> 3.17\n")
rec("SOURCED: paper rules (1.2/0.35, Ti/Te 0.95, A.5 ash, QN electrons)", point(), "the registered definition applied with the paper's own rules")
rec("  same, T_i peak at the printed 14.63 (ratio 0.950)", point(T_i0=PR["T_i0"]))
rec("  same, ash power-law alpha_He 2 (NOTES sec 7 bracket)", point(ash="pl", alpha_He=2.0))
rec("  same, ash power-law alpha_He 3", point(ash="pl", alpha_He=3.0))
rec("  same, ash at the fuel exponent 0.35 (the model's ash shape)", point(ash="pl", alpha_He=0.35))
rec("MODEL family: 1.19/0.33, ash at 0.33, n_e at 0.596, printed peaks", point(alpha_T=1.19, alpha_n=0.33, ash="pl", alpha_He=0.33, alpha_ne=0.596, T_i0=PR["T_i0"]), "the model's bound exponents (NOTES sec 7 row 1)")
rec("  model exponents but A.5 ash and QN electrons", point(alpha_T=1.19, alpha_n=0.33, T_i0=PR["T_i0"]), "what the ash shape alone is worth at the model's exponents")

s = out["SOURCED: paper rules (1.2/0.35, Ti/Te 0.95, A.5 ash, QN electrons)"]
p_from_printed_W = PR["W_total_MJ"] * 1e6 / (1.5 * PR["V"])
out["printed_pair"] = {
    "beta_pct_implied_by_printed_W_at_B0": 100 * 2 * MU0 * p_from_printed_W / PR["B0"]**2,
    "W_MJ_implied_by_printed_beta_at_B0": 1.5 * PR["beta_volav"] * PR["B0"]**2 / (2 * MU0) * PR["V"] * 1e-6,
    "B_T_reconciling_printed_beta_with_printed_W": float(np.sqrt(2 * MU0 * p_from_printed_W / PR["beta_volav"])),
    "sourced_W_over_printed": s["W_MJ"] / PR["W_total_MJ"], "model_W_over_sourced": out["MODEL family: 1.19/0.33, ash at 0.33, n_e at 0.596, printed peaks"]["W_MJ"] / s["W_MJ"]}
pp = out["printed_pair"]
print(f"\nprinted W 504.65 at B0 9.0 implies beta {pp['beta_pct_implied_by_printed_W_at_B0']:.2f} %; printed beta 2.76 % implies W {pp['W_MJ_implied_by_printed_beta_at_B0']:.1f} MJ; they agree only at B = {pp['B_T_reconciling_printed_beta_with_printed_W']:.2f} T")
print(f"sourced W / printed W = {pp['sourced_W_over_printed']:.4f};  model W / sourced W = {pp['model_W_over_sourced']:.4f}")
(HERE / "attribution_sourced_definition.json").write_text(json.dumps(out, indent=1) + "\n")
