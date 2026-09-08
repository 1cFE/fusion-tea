"""WI-047 prototype (2026-09-08): the three reduced calcs evaluated in pure Python on
the entering pin's channels; the source divertor case reproduced; the t_recycle
transect; two off-design points; the gas load. Writes proto_results.json.
Every equation here is the design's statement of the calc; the oracle is written
from the same equations, the generated modules from the SysML text."""
import json, math
from pathlib import Path

HERE = Path(__file__).resolve().parent
base = json.load(open("exploration/stellarator_e2e/studies/20260907-minor-radius/results/baseline_result.json"))
ch = base["channels"]; P = "stellarator_09__stellaris__"
g = lambda k: ch[P + k]

# ---- instance facts (design D-decisions) ------------------------------------
fuel_q_eff, mev_to_joules = 17.58, 1.6021766339999998e-13          # instance :1154, :1157
E_fus_J = fuel_q_eff * mev_to_joules                                # per reaction [J]
burn_fraction, t_recycle, tbr_available = 0.05, 0.99, 1.074        # :1160, :1163 (read as recovery), :1295
eta_extract, I_total, G_stock = 1.0, 0.0, 0.0                       # dormant (packet § 6)
t_half_s = 4500.0 * 86400.0                                         # NIST 4500 +/- 8 d
lambda_T = math.log(2.0) / t_half_s
u_kg = 1.66053906892e-27                                            # the instance's atomic mass unit (fuel_cost_per_rxn doc)
m_T_kg = 3.01604928 * u_kg                                          # tritium atomic mass [kg]
s_per_fpy = 8760.0 * 3600.0                                         # the model's year (8760 h; mfe_lcoe_dcf, 'DT Fuel Cost')
f_rad_total, q_target_ref, p_nonrad_ref, q_target_limit = 0.9, 9.5, 50.0, 10.0
q_target_ref_low = 5.0
R_ref = 12.7
k_B, T_gas, p_exhaust = 1.380649e-23, 300.0, 1.0
f_alpha_fast, ash_frac = 0.95, 0.2002                               # instance :687; sustain default ash_frac_in

def fuel(p_fus):
    burn_rate = p_fus * 1.0e6 / E_fus_J
    inject_rate = burn_rate / burn_fraction
    exhaust_rate = inject_rate - burn_rate
    loss_rate = (1.0 - t_recycle) * exhaust_rate
    tbr_required = (burn_rate + loss_rate + lambda_T * I_total + G_stock) / (eta_extract * burn_rate)
    tbr_margin = tbr_available - tbr_required
    burn_kg_per_fpy = burn_rate * m_T_kg * s_per_fpy
    return dict(burn_rate=burn_rate, inject_rate=inject_rate, exhaust_rate=exhaust_rate, loss_rate=loss_rate,
                tbr_required=tbr_required, tbr_margin=tbr_margin, burn_kg_per_fpy=burn_kg_per_fpy)

def divheat(p_alpha_heat, p_coupled, p_aux_required, p_rad_core, R, q_ref=q_target_ref):
    p_heat_abs = p_alpha_heat + p_coupled
    p_sep = p_heat_abs - p_rad_core
    f_rad_edge = (f_rad_total * p_heat_abs - p_rad_core) / p_sep
    f_rad_edge_in_range = f_rad_edge * (1.0 - f_rad_edge)
    p_target_nonrad = p_heat_abs - f_rad_total * p_heat_abs   # D4: this form reproduces the source case (500 - 450 = 50) exactly
    q_target_peak = q_ref * p_target_nonrad / p_nonrad_ref
    q_target_peak_area_scaled = q_target_peak * R_ref / R
    q_target_margin = q_target_limit - q_target_peak
    p_heat_operating_minus_installed = p_aux_required - p_coupled
    return dict(p_heat_abs=p_heat_abs, p_sep=p_sep, f_rad_edge=f_rad_edge, f_rad_edge_in_range=f_rad_edge_in_range,
                p_target_nonrad=p_target_nonrad, q_target_peak=q_target_peak,
                q_target_peak_area_scaled=q_target_peak_area_scaled, q_target_margin=q_target_margin,
                p_heat_operating_minus_installed=p_heat_operating_minus_installed,
                divertor_heat_ok=("satisfied" if q_target_peak <= q_target_limit else "violated"))

def vacuum(exhaust_D, exhaust_T, helium):
    Q_total = ((exhaust_D + exhaust_T) / 2.0 + helium) * k_B * T_gas
    return dict(Q_total=Q_total, S_eff_required=Q_total / p_exhaust,
                n_molecules_per_s=(exhaust_D + exhaust_T) / 2.0 + helium)

out = {}
# ---- P0 the design point on the entering pin's channels ---------------------
p_fus = g("fusion__p_fus"); pah = g("sustain__p_alpha_heat"); prad = g("sustain__p_rad")
paux = g("sustain__p_aux_required"); pc = g("heat__p_coupled")
assert abs(f_alpha_fast * ash_frac * p_fus - pah) < 1e-9, (f_alpha_fast * ash_frac * p_fus, pah)
F0 = fuel(p_fus); D0 = divheat(pah, pc, paux, prad, 12.7); D0low = divheat(pah, pc, paux, prad, 12.7, q_target_ref_low)
V0 = vacuum(F0["exhaust_rate"], F0["exhaust_rate"], F0["burn_rate"])
out["P0_design_point"] = dict(inputs=dict(p_fus=p_fus, p_alpha_heat=pah, p_rad=prad, p_aux_required=paux, p_coupled=pc),
                              fuel=F0, divheat_pessimistic=D0, divheat_low_case=D0low, vacuum=V0,
                              operating_basis_check=divheat(pah, paux, paux, prad, 12.7))
# identity: p_fus reconstructed from the burn rate
out["P0_design_point"]["p_fus_reconstructed_MW"] = F0["burn_rate"] * E_fus_J / 1.0e6
# ---- the source case reproduced (500 MW absorbed, 90 % radiated) ------------
src = divheat(500.0, 0.0, 0.0, 0.0, R_ref)          # core radiation 0 -> all 90 % in the edge
src_low = divheat(500.0, 0.0, 0.0, 0.0, R_ref, q_target_ref_low)
out["source_case"] = dict(p_target_nonrad=src["p_target_nonrad"], q_peak_pessimistic=src["q_target_peak"],
                          q_peak_low=src_low["q_target_peak"], f_rad_edge_with_zero_core=src["f_rad_edge"],
                          doubled_load_peak=divheat(1000.0, 0.0, 0.0, 0.0, R_ref)["q_target_peak"])
# ---- the t_recycle transect and the zero-margin threshold --------------------
thr = 1.0 - (tbr_available - 1.0) * burn_fraction / (1.0 - burn_fraction)
tr = {}
for t in (0.99, 0.992, 0.994, 0.996, 0.9961, thr, 0.997, 0.998, 0.999, 1.0):
    t_recycle = t; f = fuel(p_fus); tr[f"{t:.6f}"] = dict(tbr_required=f["tbr_required"], tbr_margin=f["tbr_margin"])
t_recycle = 0.99
out["t_recycle_transect"] = dict(threshold=thr, rows=tr, identity_1p19=fuel(p_fus)["tbr_required"])
# acceptance: lossless loop at t_recycle 1 -> tbr_required 1.0 for any burn fraction
saved = burn_fraction
chk = {}
for bf in (0.01, 0.05, 0.2):
    burn_fraction = bf; t_recycle = 1.0; f = fuel(p_fus); chk[str(bf)] = dict(loss=f["loss_rate"], tbr_required=f["tbr_required"], inject=f["inject_rate"])
burn_fraction, t_recycle = saved, 0.99
out["lossless_check"] = chk
# ---- off-design points -------------------------------------------------------
def offpoint(name, p_fus_pt, R, paux_pt):
    pah_pt = f_alpha_fast * ash_frac * p_fus_pt
    d = dict(name=name, p_fus=p_fus_pt, R=R, p_alpha_heat=pah_pt, p_heat_abs=pah_pt + pc,
             p_target_nonrad=(pah_pt + pc) - f_rad_total * (pah_pt + pc),
             q_target_peak_pessimistic=q_target_ref * ((pah_pt + pc) - f_rad_total * (pah_pt + pc)) / p_nonrad_ref,
             q_target_peak_low=q_target_ref_low * ((pah_pt + pc) - f_rad_total * (pah_pt + pc)) / p_nonrad_ref,
             p_heat_operating_minus_installed=paux_pt - pc, fuel=fuel(p_fus_pt))
    d["q_target_peak_area_scaled"] = d["q_target_peak_pessimistic"] * R_ref / R
    d["divertor_heat_ok"] = "satisfied" if d["q_target_peak_pessimistic"] <= q_target_limit else "violated"
    d["note"] = "p_rad (core radiation) is not a column of the committed CSV, so p_sep and f_rad_edge are read at execution; the peak needs only p_fus and p_coupled"
    d["vacuum"] = vacuum(d["fuel"]["exhaust_rate"], d["fuel"]["exhaust_rate"], d["fuel"]["burn_rate"])
    return d
out["P3_c2823"] = offpoint("c2823 (R 15.7, a 2.2, 13 MA, 13 keV, n 5.06e20, 100 MW)", 5363.434926736221, 15.7, 33.34053528836671)
out["P4_c3598_highest_heating_feasible"] = offpoint("c3598 (R 17.2, a 2.2, 14 MA, 13 keV, 100 MW; the highest-p_fus ten-verdict feasible point at 100 MW)", 5973.4561207478655, 17.2, 41.246208392590916)
# the absorbed heating at which the pessimistic fence is exactly satisfied at fixed geometry
out["p_heat_abs_at_limit"] = dict(pessimistic=q_target_limit * p_nonrad_ref / (q_target_ref * (1 - f_rad_total)),
                                  low=q_target_limit * p_nonrad_ref / (q_target_ref_low * (1 - f_rad_total)))
# ---- molecule-count check and doubling -----------------------------------------
out["vacuum_checks"] = dict(atoms_per_s=2 * F0["exhaust_rate"] + F0["burn_rate"], molecules_per_s=V0["n_molecules_per_s"],
                            ratio=(2 * F0["exhaust_rate"] + F0["burn_rate"]) / V0["n_molecules_per_s"],
                            doubled=vacuum(2 * F0["exhaust_rate"], 2 * F0["exhaust_rate"], 2 * F0["burn_rate"])["S_eff_required"] / V0["S_eff_required"])
out["constants"] = dict(E_fus_J=E_fus_J, lambda_T=lambda_T, m_T_kg=m_T_kg, s_per_fpy=s_per_fpy, k_B=k_B, u_kg=u_kg)
json.dump(out, open(HERE / "proto_results.json", "w"), indent=1)
d = out["P0_design_point"]
print("P0 fuel", {k: f"{v:.6g}" for k, v in d["fuel"].items()})
print("P0 divheat pess", {k: (f"{v:.6g}" if isinstance(v, float) else v) for k, v in d["divheat_pessimistic"].items()})
print("P0 low q", d["divheat_low_case"]["q_target_peak"], "vacuum", d["vacuum"])
print("source", out["source_case"]); print("threshold", thr, "1.19 identity", out["t_recycle_transect"]["identity_1p19"])
print("c2823 q", out["P3_c2823"]["q_target_peak_pessimistic"], out["P3_c2823"]["q_target_peak_area_scaled"], out["P3_c2823"]["q_target_peak_low"])
print("c3598 q", out["P4_c3598_highest_heating_feasible"]["q_target_peak_pessimistic"]); print("limit p_heat_abs", out["p_heat_abs_at_limit"]); print("vac checks", out["vacuum_checks"])
