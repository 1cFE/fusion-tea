"""Grounding probe for goal `plant-closure` (2026-09-08): what the three
closures are predicted to do at the design point, computed on the oracle
seam (verify_stellaris.compute with overridden inputs). Oracle-side
diagnostic only -- never package evidence. Every number here is a
prediction to be tested by the model item and the study, not a target.

(i)   Primary loop: Moscato 2017 reference circuit (8 MPa, 300->500 C,
      2101.7 MW, 2025.7 kg/s, 9 loops; per-path losses IB 363.9 / OB 315.7
      kPa; IHX duty 2231.1 MW; printed circulator power 130.8 MW total),
      transferred as a representative circuit with the loop count sized at
      the design point so per-loop flow <= the reference's, constant loss
      coefficients per component, compressor from the pressure ratio.
(ii)  Cycle: Kovari et al. 2016 Table 4 Rankine fit, eta = 0.1802 ln(T2_C+273)
      - 0.7823, T2 = blanket outlet - 20 K approach, domain 384-642 C.
(iii) Calendar: deterministic finite horizon, one bundled in-vessel event,
      L = fluence_limit / q_peak, outage d = 7/12 yr (Stellaris estimate),
      residual unplanned fraction u in {0, 0.05, 0.10}, N = 30 yr.
"""
import json, math, sys
from pathlib import Path
sys.path.insert(0, "exploration/stellarator_e2e")
import verify_stellaris as vs

base = vs.compute()
P = vs.IN
# --- reference circuit (Moscato output.md:79-81, :89-91, Table 1 :105-113,
#     Table 2 :128, Table 3 :151-154; raw p.6-7) ---
cp = 5193.0          # J/(kg K), ideal helium (NIST 20.786 J/(mol K) / 4.002602 g/mol)
gamma = 5.0 / 3.0
Q_ref, mdot_ref, N_ref = 2101.7, 2025.7, 9.0
T2_ref, T3_ref = 300.0 + 273.15, 500.0 + 273.15
p2 = 8.0e6
dp_ib = (214.0 + 62.0 + 87.9) * 1e3
dp_ob = (174.0 + 56.6 + 85.1) * 1e3
Q_ihx_ref = 2231.1
W_fluid_ref_check = Q_ihx_ref - Q_ref          # 129.4 MW, the source's own energy check
P_circ_printed = 3 * 2 * 6.8 + 6 * 2 * 7.5     # 130.8 MW
# implied cp from the source's own numbers
cp_implied = Q_ref * 1e6 / (mdot_ref * (T3_ref - T2_ref))
# flow-weighted mean per-path loss (IB 3 loops x 208.1 MW, OB 6 x 267.8)
w_ib, w_ob = 3 * 208.1, 6 * 267.8
dp_ref = (w_ib * dp_ib + w_ob * dp_ob) / (w_ib + w_ob)
# isentropic compressor: T1 from held T2 and ratio r = p2/(p2 - dp)
def compressor(T2, dp, eta_is):
    r = p2 / (p2 - dp)
    T1 = T2 / (1.0 + (r ** ((gamma - 1) / gamma) - 1.0) / eta_is)
    return T1, r
# derive eta_is at the reference from the energy check (source-point calibration)
dT_actual_ref = W_fluid_ref_check * 1e6 / (mdot_ref * cp)
r_ref = p2 / (p2 - dp_ref)
dT_is_ref = T2_ref * (1.0 - 1.0 / r_ref ** ((gamma - 1) / gamma))
eta_is_ref = dT_is_ref / dT_actual_ref
# --- Stellaris design point ---
p_fus = base["p_fus"]
p_alpha = (3.52 / 17.58) * p_fus
p_neutron = p_fus - p_alpha
Q_b = P["mn"] * p_neutron + p_alpha + 50.0          # reactor source heat, no pump credit
mdot = Q_b * 1e6 / (cp * (T3_ref - T2_ref))
N_loops = math.ceil(mdot / (mdot_ref / N_ref))
mdot_loop = mdot / N_loops
dp = dp_ref * (mdot_loop / (mdot_ref / N_ref)) ** 2  # constant loss coefficient, rho at the same nominal state
T1, r = compressor(T2_ref, dp, eta_is_ref)
W_fluid = mdot * cp * (T2_ref - T1) / 1e6
P_loop_elec = W_fluid                                # the source's printed boundary: circulator power = fluid work (lower bound on electrical)
Q_ihx = Q_b + W_fluid
# --- cycle ---
T_turb_C = 500.0 - 20.0
eta_rankine = 0.1802 * math.log(T_turb_C + 273.0) - 0.7823
eta_sco2 = 0.4347 * math.log(T_turb_C + 273.0) - 2.5043
# --- calendar ---
q_peak = base["wall_load_peak"]
L = P["fluence_limit"] / q_peak
def calendar(L, d, u, N):
    b = 1.0 - u
    t, F, Tp, Tu, k, events = 0.0, 0.0, 0.0, 0.0, 0, []
    while True:
        run = L / b
        if t + run >= N:                      # horizon ends mid-run
            F += b * (N - t); Tu += u * (N - t); t = N; break
        t += run; F += L; Tu += u * run
        if t + d < N:                         # restart strictly before N
            events.append(t); k += 1; Tp += d; t += d
        else:
            Tterm = N - t; t = N
            return dict(F=F, Tp=Tp, Tu=Tu, Tterm=Tterm, k=k, events=events, A=F / N)
    return dict(F=F, Tp=Tp, Tu=Tu, Tterm=0.0, k=k, events=events, A=F / N)
cal = {u: calendar(L, 7.0 / 12.0, u, P["operational_years"]) for u in (0.0, 0.05, 0.10)}
cal5 = {u: calendar(L, 5.0 / 12.0, u, P["operational_years"]) for u in (0.0, 0.05, 0.10)}
# --- oracle re-evaluation with the three closures substituted (u = 0) ---
def with_overrides(**kw):
    saved = {k: P[k] for k in kw}
    P.update(kw)
    try:
        return vs.compute()
    finally:
        P.update(saved)
arms = {
    "held (pin 30abb21b)": {},
    "loop only": dict(p_pump=P_loop_elec, eta_p=1.0),
    "cycle only": dict(eta_th=eta_rankine),
    "calendar only (u=0)": dict(availability=cal[0.0]["A"]),
    "calendar only (u=0.05)": dict(availability=cal[0.05]["A"]),
    "all three (u=0)": dict(p_pump=P_loop_elec, eta_p=1.0, eta_th=eta_rankine, availability=cal[0.0]["A"]),
    "all three (u=0.05)": dict(p_pump=P_loop_elec, eta_p=1.0, eta_th=eta_rankine, availability=cal[0.05]["A"]),
}
rows = {}
for name, ov in arms.items():
    r_ = with_overrides(**ov)
    rows[name] = {k: r_[k] for k in ("p_th", "p_et", "p_net", "rec_frac", "cas72_annual", "annual_fuel", "lcoe", "lcoe_1cfe", "total_capital")}
out = dict(
    reference=dict(cp_implied=cp_implied, dp_ref_flow_weighted_kPa=dp_ref / 1e3, r_ref=r_ref,
                   dT_actual_ref_K=dT_actual_ref, dT_is_ref_K=dT_is_ref, eta_is_ref=eta_is_ref,
                   W_fluid_ref_check_MW=W_fluid_ref_check, P_circ_printed_MW=P_circ_printed),
    design_point=dict(p_fus=p_fus, Q_b_MW=Q_b, mdot_kg_s=mdot, N_loops=N_loops, mdot_loop=mdot_loop,
                      dp_kPa=dp / 1e3, r=r, T1_K=T1, W_fluid_MW=W_fluid, P_loop_elec_MW=P_loop_elec,
                      Q_ihx_MW=Q_ihx, p_th_new_MW=Q_ihx, p_th_held=base["p_th"],
                      p_pump_held=P["p_pump"], eta_p_held=P["eta_p"], recovered_held_MW=P["eta_p"] * P["p_pump"],
                      W_fluid_frac_of_Qb=W_fluid / Q_b),
    cycle=dict(T_turb_C=T_turb_C, eta_rankine=eta_rankine, eta_sco2=eta_sco2, eta_held=P["eta_th"]),
    calendar=dict(q_peak=q_peak, L_fpy=L, seven_months={str(u): v for u, v in cal.items()},
                  five_months={str(u): v for u, v in cal5.items()}, availability_held=P["availability"],
                  L_cal_held=L / P["availability"], n_rep_held=max(0, math.ceil(30 / (L / P["availability"])) - 1)),
    arms=rows,
)
Path("work/orchestration/goals/plant-closure/evidence/grounding_probe/probe_results.json").write_text(json.dumps(out, indent=1))
print(json.dumps(out["reference"], indent=1)); print(json.dumps(out["design_point"], indent=1)); print(json.dumps(out["cycle"], indent=1))
print("calendar L", L, {u: (v["k"], round(v["A"], 4), [round(e, 2) for e in v["events"]]) for u, v in cal.items()})
print("calendar 5mo", {u: (v["k"], round(v["A"], 4)) for u, v in cal5.items()}, "held n_rep", out["calendar"]["n_rep_held"])
for n, r_ in rows.items(): print(f"{n:26s} p_th {r_['p_th']:8.2f} p_et {r_['p_et']:8.2f} p_net {r_['p_net']:8.2f} rec {r_['rec_frac']:.4f} cas72 {r_['cas72_annual']/1e6:7.2f} lcoe {r_['lcoe']:9.4f}")
