"""Attribution arithmetic -- what the printed Stellaris point-A values give under the profile family.

A first pass at the second half of the goal's question ("what in the profile integral produces
the +9.2%"), using only (i) the printed Table 5 / Table 2 values read from the page images,
(ii) the paper's own stated parametrization, Eqs. (2)-(3) on p. 8 (T_e = T_e0 (1-rho^2)^alpha_T,
n_i = n_i0 (1-rho^2)^alpha_n) with the Fig. 16 caption's alpha_T = 1.2, alpha_n = 0.35 (p. 10),
and (iii) the model's own bound exponents (alpha_n 0.33, alpha_T 1.19, alpha_n_e 0.596).
Nothing is fitted. The oracle's own profile integral is used for the fusion-power sensitivity.

Every quantity is oracle-side arithmetic, not package evidence. No Fig. 16 digitization.
"""
import json, math, sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
REPO = HERE.parents[5]
E2E = REPO / "exploration" / "stellarator_e2e"
sys.path.insert(0, str(E2E))
import verify_stellaris as vs

KEV = 1.602176634e-16
MU0 = 1.25663706212e-6
# --- printed, point A (Table 5 image page_009_table_0.png; Table 2 image page_002_table_0.png) ---
PR = dict(n_e0=5.06e20, n_D0=1.96e20, n_T0=1.96e20, n_He0=0.56e20, T_e0=15.40, T_i0=14.63,
          n_e_volav=3.17e20, beta_volav=0.0276, W_total_MJ=504.65, V=425.0, B0=9.0, tau_E=1.46,
          p_fus=2700.0, p_rad_photon=228.9, tau_sd_ms=43.76)
PAPER = dict(alpha_T=1.2, alpha_n=0.35)      # Fig. 16 caption, Eqs. (2)-(3)
MODEL = dict(alpha_T=1.19, alpha_n=0.33, alpha_n_e=0.596)   # stellarator_plant.sysml bindings
E_FUS = 2.817e-12; F_ALPHA = 0.95; ASH_FRAC = 0.2002

def W_family(a_ne, a_ni, a_T, V=PR["V"]):
    """W = 1.5 <p> V with <p> = k [n_e0 T_e0/(1+a_ne+a_T) + (n_D0+n_T0+n_He0) T_i0/(1+a_ni+a_T)] (the model's form)."""
    p = KEV * (PR["n_e0"] * PR["T_e0"] / (1 + a_ne + a_T) + (PR["n_D0"] + PR["n_T0"] + PR["n_He0"]) * PR["T_i0"] / (1 + a_ni + a_T))
    return 1.5 * p * V * 1e-6, p

out = {}
def rec(tag, W, note):
    out[tag] = {"W_MJ": W, "vs_printed_pct": 100 * (W / PR["W_total_MJ"] - 1), "note": note}
    print(f"{tag:44s} W = {W:7.2f} MJ  ({100*(W/PR['W_total_MJ']-1):+5.1f} % vs printed 504.65)  {note}")

W_model, p_model = W_family(MODEL["alpha_n_e"], MODEL["alpha_n"], MODEL["alpha_T"])
rec("model family, printed peaks", W_model, "alpha_n_e 0.596 / alpha_n 0.33 / alpha_T 1.19 -- the bound exponents on the printed peaks")
W_paper, p_paper = W_family(PAPER["alpha_n"], PAPER["alpha_n"], PAPER["alpha_T"])
rec("caption exponents on every species 0.35/1.2", W_paper, "a NAIVE reading: the caption's alpha_n is the ion density's (Eq. 3); the figure's electron curve digitizes at 0.62 (WI-022), as quasi-neutrality with a peaked ash requires")
W_qn, _ = W_family(MODEL["alpha_n_e"], MODEL["alpha_n_e"], MODEL["alpha_T"])
rec("model family, ions at the electron exponent", W_qn, "alpha_n := alpha_n_e = 0.596 for the fuel and ash too (quasi-neutral shapes)")
W_qn2, _ = W_family(MODEL["alpha_n_e"], MODEL["alpha_n_e"], PAPER["alpha_T"])
rec("  same, alpha_T 1.2 exactly", W_qn2, "")
# --- a figure-consistent family: fuel at the digitized 0.33, the helium ash PEAKED (Fig. 16(a): the
# He curve falls to ~0 by rho 0.8; alpha_He read by eye as ~2, bracketed 1-3), electrons by
# quasi-neutrality n_e = n_D + n_T + 2 n_He, T at 1.19. The model instead gives the ash the fuel
# exponent, which is what makes its family charge-inconsistent off-axis.
def W_qn_family(a_fuel, a_He, a_T, V=PR["V"]):
    n_fuel0 = PR["n_D0"] + PR["n_T0"]
    p_e = PR["T_e0"] * (n_fuel0 / (1 + a_fuel + a_T) + 2 * PR["n_He0"] / (1 + a_He + a_T))
    p_i = PR["T_i0"] * (n_fuel0 / (1 + a_fuel + a_T) + PR["n_He0"] / (1 + a_He + a_T))
    p = KEV * (p_e + p_i)
    ne_av = n_fuel0 / (1 + a_fuel) + 2 * PR["n_He0"] / (1 + a_He)
    return 1.5 * p * V * 1e-6, ne_av
for a_He in (1.0, 2.0, 3.0):
    Wf, ne_av = W_qn_family(0.33, a_He, 1.19)
    rec(f"figure-consistent, ash peaked alpha_He {a_He:.0f}", Wf, f"fuel 0.33 / He {a_He:.0f} / T 1.19, electrons by quasi-neutrality; <n_e> {ne_av/1e20:.2f}e20 (printed 3.17), effective alpha_n_e {PR['n_e0']/ne_av-1:.3f}")
# the exponent sum the printed W would need, at the printed peaks, all species one shape
p_needed = PR["W_total_MJ"] * 1e6 / (1.5 * PR["V"])
num = KEV * (PR["n_e0"] * PR["T_e0"] + (PR["n_D0"] + PR["n_T0"] + PR["n_He0"]) * PR["T_i0"])
s_needed = num / p_needed - 1.0
out["exponent_sum_for_printed_W"] = s_needed
print(f"exponent sum (alpha_n + alpha_T) the printed W needs, all species one shape: {s_needed:.3f}  (paper's 1.55; model's electron 1.786 / ion 1.52)")

# --- the printed beta against the printed W, under the model's definitions -------------
p_from_beta = PR["beta_volav"] * PR["B0"] ** 2 / (2 * MU0)
W_from_beta = 1.5 * p_from_beta * PR["V"] * 1e-6
B_for_consistency = math.sqrt(2 * MU0 * p_needed / PR["beta_volav"])
out["printed_beta_implies"] = {"p_avg_Pa": p_from_beta, "W_MJ_at_V425_B9": W_from_beta,
                               "B_T_that_reconciles_beta_with_printed_W": B_for_consistency,
                               "model_beta_at_baseline": 2 * MU0 * p_model / PR["B0"] ** 2}
print(f"printed beta 2.76 % at B0 9.0, V 425  ->  <p> {p_from_beta:,.0f} Pa  ->  W {W_from_beta:.1f} MJ ({100*(W_from_beta/PR['W_total_MJ']-1):+.1f} % vs printed W)")
print(f"  the printed W and printed beta agree only if beta is referenced to B = {B_for_consistency:.2f} T (not the axis 9.0)")
print(f"  model beta at baseline (same <p> as its W, B 9.0): {2*MU0*p_model/PR['B0']**2*100:.3f} %  vs printed 2.76 %")

# --- the printed <n_e> against the exponents ------------------------------------------
ratio = PR["n_e_volav"] / PR["n_e0"]
out["printed_ne_ratio"] = {"volav_over_peak": ratio, "alpha_ne_if_volume_average": 1 / ratio - 1,
                           "volav_over_peak_at_paper_alpha_n": 1 / (1 + PAPER["alpha_n"])}
print(f"printed <n_e>/n_e0 = {ratio:.4f} -> alpha_n_e {1/ratio-1:.3f} as a volume average (the model's back-computation); the paper's alpha_n 0.35 would give {1/(1+PAPER['alpha_n']):.3f}")

# --- local quasi-neutrality of the model's family (fuel broader than electrons) --------
qn = []
for rho in (0.5, 0.7, 0.8, 0.9, 0.95):
    u = 1 - rho * rho
    ne = PR["n_e0"] * u ** MODEL["alpha_n_e"]
    ni = (PR["n_D0"] + PR["n_T0"]) * u ** MODEL["alpha_n"] + 2 * PR["n_He0"] * u ** MODEL["alpha_n"]
    qn.append({"rho": rho, "n_e": ne, "n_D+n_T+2n_He": ni, "charge_excess_pct": 100 * (ni / ne - 1)})
out["model_family_quasineutrality"] = qn
print("model family, ion charge density vs electron density along rho (printed peaks):")
for q in qn:
    print(f"  rho {q['rho']:.2f}: n_e {q['n_e']:.3e}  ion charge {q['n_D+n_T+2n_He']:.3e}  excess {q['charge_excess_pct']:+.1f} %")

# --- what the ion exponent costs in fusion power (the oracle's own integral, printed peaks) ---
def p_fus(a_n, a_T, T0=PR["T_i0"]):
    I = vs._profile_integral(a_n, a_T, T0)
    return PR["n_D0"] * PR["n_T0"] * I * E_FUS * PR["V"] * 1e-6
pf = {"model 0.33/1.19": p_fus(0.33, 1.19), "paper 0.35/1.2": p_fus(0.35, 1.2), "ions at 0.596/1.19": p_fus(0.596, 1.19)}
out["p_fus_at_printed_peaks"] = pf
for k, v in pf.items():
    print(f"p_fus at the printed peaks, exponents {k:20s}: {v:7.1f} MW  ({100*(v/PR['p_fus']-1):+5.1f} % vs printed 2700)")

# --- the printed pair through the appendix balance (A.3), p_aux = 0 ---------------------
P_alpha_heat = F_ALPHA * ASH_FRAC * PR["p_fus"]
W_over_tau = PR["W_total_MJ"] / PR["tau_E"]
resid = P_alpha_heat - PR["p_rad_photon"] - W_over_tau
out["printed_pair_balance"] = {"f_alpha_P_alpha_MW": P_alpha_heat, "W_over_tau_E_MW": W_over_tau, "p_rad_MW": PR["p_rad_photon"],
                               "residual_MW_at_p_aux_0": resid, "tau_E_for_balance_s": PR["W_total_MJ"] / (P_alpha_heat - PR["p_rad_photon"])}
print(f"printed pair through A.3 at p_aux = 0: f_a P_a {P_alpha_heat:.1f} - p_rad {PR['p_rad_photon']:.1f} - W/tau_E {W_over_tau:.1f} = {resid:+.1f} MW "
      f"(tau_E that would balance the printed W: {PR['W_total_MJ']/(P_alpha_heat-PR['p_rad_photon']):.3f} s vs printed 1.46)")
# fast-alpha energy content (order of magnitude): P_alpha * tau_sd / 2
W_alpha = (3.52 / 17.58) * PR["p_fus"] * PR["tau_sd_ms"] * 1e-3 / 2
out["fast_alpha_energy_MJ_order"] = W_alpha
print(f"fast-alpha stored energy, order of magnitude (P_alpha x tau_sd / 2): {W_alpha:.1f} MJ = {100*W_alpha/PR['W_total_MJ']:.1f} % of the printed W")
(HERE / "attribution_arithmetic.json").write_text(json.dumps(out, indent=1) + "\n")
