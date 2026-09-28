"""WI-045 prototype (goal plant-closure, round 1, T-003; 2026-09-08).

Pure Python. Executes the loop and the cycle equations the design proposes,
reconstructs the Moscato reference circuit, proves the held-mode identity
bit-for-bit, and predicts the live baseline and three off-design points on the
oracle seam (verify_stellaris.compute() with IN overridden; the oracle is
imported, never edited). Every number in design.md comes from proto_results.json.

Run: uv run python work/active/WI-045_primary-loop-and-cycle/prototype/proto.py
"""
import json, math, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT / "exploration/stellarator_e2e"))
import verify_stellaris as vs  # noqa: E402

OUT = Path(__file__).resolve().parent / "proto_results.json"
P = vs.IN
res = {}

# ---------------------------------------------------------------- (a) reference
# Moscato 2017 (output.md:79-81, :89-91, Table 1 :105-113, Table 2 :128, Table 3 :151-154).
cp = 5193.0                     # J/(kg K), ideal helium (NIST 20.786 J/(mol K) / 4.002602e-3 kg/mol)
cp_nist = 20.786 / 4.002602e-3
gamma = 5.0 / 3.0
Q_ref, mdot_ref, N_ref = 2101.7, 2025.7, 9
T_in_ref, dT_ref = 300.0 + 273.15, 200.0
p_loop = 8.0e6
dp_ib = (214.0 + 62.0 + 87.9) * 1e3
dp_ob = (174.0 + 56.6 + 85.1) * 1e3
Q_ihx_ib, Q_ihx_ob = 208.1, 267.8
Q_ihx_ref = 3 * Q_ihx_ib + 6 * Q_ihx_ob                 # 2231.1
W_check = Q_ihx_ref - Q_ref                             # 129.4 MW, the source's own energy check
P_circ_printed = 3 * 2 * 6.8 + 6 * 2 * 7.5              # 130.8 MW
cp_implied = Q_ref * 1e6 / (mdot_ref * dT_ref)
w_ib, w_ob = 3 * Q_ihx_ib, 6 * Q_ihx_ob
dp_weighted = (w_ib * dp_ib + w_ob * dp_ob) / (w_ib + w_ob)
mdot_loop_ref = mdot_ref / N_ref
k = (gamma - 1.0) / gamma

def T_comp_in(T_in, dp, eta_is):
    r = p_loop / (p_loop - dp)
    return r, T_in / (1.0 + (r ** k - 1.0) / eta_is)

def derive_eta_is(dp):
    """eta_is at which the reference's fluid work equals its own energy check,
    solved on the calc's own compressor form: T_in = T1 (1 + (r^k - 1)/eta_is),
    so with T_in - T1 = dT_actual, eta_is = (r^k - 1) T1 / dT_actual, T1 = T_in - dT_actual
    (isentropic compression FROM the compressor inlet, the form the calc evaluates)."""
    r = p_loop / (p_loop - dp)
    dT_actual = W_check * 1e6 / (mdot_ref * cp)
    T1 = T_in_ref - dT_actual
    dT_is = T1 * (r ** k - 1.0)
    return dT_is / dT_actual, r, dT_actual, dT_is

def w_fluid_at(mdot, T_in, dp, eta_is):
    r, T1 = T_comp_in(T_in, dp, eta_is)
    return mdot * cp * (T_in - T1) / 1e6, r, T1

ref = {}
for name, dp in (("weighted", dp_weighted), ("ob_path", dp_ob), ("ib_path", dp_ib)):
    eta_is, r, dT_a, dT_is = derive_eta_is(dp)
    w, _, T1 = w_fluid_at(mdot_ref, T_in_ref, dp, eta_is)
    # ulp search for an eta_is that reproduces 129.4 exactly, within +-4 ulps
    exact = None
    for n in range(-4, 5):
        e = eta_is
        for _ in range(abs(n)):
            e = math.nextafter(e, math.inf if n > 0 else -math.inf)
        if w_fluid_at(mdot_ref, T_in_ref, dp, e)[0] == W_check:
            exact = (n, e); break
    ref[name] = dict(dp_kPa=dp / 1e3, r=r, dT_actual_K=dT_a, dT_is_K=dT_is, eta_is=eta_is,
                     eta_is_repr=repr(eta_is), w_fluid_reproduced_MW=w, w_residual_MW=w - W_check,
                     T_comp_in_K=T1, exact_ulp_hit=exact)
res["reference"] = dict(cp=cp, cp_nist=cp_nist, cp_implied=cp_implied, cp_discrepancy=cp_implied / cp - 1.0,
                        dp_ib_kPa=dp_ib / 1e3, dp_ob_kPa=dp_ob / 1e3, dp_weighted_kPa=dp_weighted / 1e3,
                        Q_ihx_MW=Q_ihx_ref, W_check_MW=W_check, P_circ_printed_MW=P_circ_printed,
                        residual_printed_minus_fluid_MW=P_circ_printed - W_check,
                        mdot_loop_ref=mdot_loop_ref, paths=ref)

# --------------------------------------------------------- the instance's circuit
ETA_IS = ref["weighted"]["eta_is"]           # D2: the derived double, not rounded
DP_REF = dp_weighted                         # D1: flow-weighted per-path loss
CIRCUIT = dict(T_in=T_in_ref, dT_blanket=dT_ref, cp=cp, gamma=gamma, p_loop=p_loop, n_loops=14,
               mdot_loop_ref=mdot_loop_ref, dp_loop_ref=DP_REF, f_loss=1.0, eta_is=ETA_IS, eta_drive=1.0)
FIT = dict(dT_approach=20.0, a_fit=0.1802, b_fit=0.7823, T_offset_fit=273.0, T2_min=384.0, T2_max=642.0, delta_eta=0.0)
SCO2 = dict(a_fit=0.4347, b_fit=2.5043, T2_min=135.0, T2_max=750.0)

def loop(q_source, c=CIRCUIT, loop_live=1.0):
    mdot = q_source * 1.0e6 / (c["cp"] * c["dT_blanket"])
    T_out = c["T_in"] + c["dT_blanket"]
    mdot_loop = mdot / c["n_loops"]
    dp_loop = c["f_loss"] * c["dp_loop_ref"] * (mdot_loop / c["mdot_loop_ref"]) ** 2
    p_loop_margin = c["p_loop"] - dp_loop
    r_comp = c["p_loop"] / (c["p_loop"] - dp_loop)
    T_ci = c["T_in"] / (1.0 + (r_comp ** ((c["gamma"] - 1.0) / c["gamma"]) - 1.0) / c["eta_is"])
    w_fluid = mdot * c["cp"] * (c["T_in"] - T_ci) / 1.0e6
    p_elec = w_fluid / c["eta_drive"]
    q_ihx = q_source + w_fluid
    return dict(mdot=mdot, T_out=T_out, mdot_loop=mdot_loop, dp_loop=dp_loop, p_loop_margin=p_loop_margin,
                r_comp=r_comp, T_comp_in=T_ci, w_fluid=w_fluid, p_elec=p_elec, q_ihx=q_ihx,
                p_elec_live=loop_live * p_elec, q_recovered_live=loop_live * w_fluid,
                capacity_margin=c["mdot_loop_ref"] - mdot_loop)

def cycle(T_hot, f=FIT, cycle_live=1.0, eta_th_direct=0.0):
    T2_C = T_hot - f["dT_approach"] - 273.15
    eta_fit = f["a_fit"] * math.log(T2_C + f["T_offset_fit"]) - f["b_fit"] - f["delta_eta"]
    margin_low = T2_C - f["T2_min"]; margin_high = f["T2_max"] - T2_C
    return dict(T2_C=T2_C, eta_fit=eta_fit, eta_th=cycle_live * eta_fit + eta_th_direct,
                margin_low=margin_low, margin_high=margin_high, domain_product=margin_low * margin_high)

# ------------------------------------------------ (b)(c) design point, both modes
base = vs.compute()
p_fus = base["p_fus"]
p_alpha = (3.52 / 17.58) * p_fus
p_neutron = p_fus - p_alpha
p_input = base["heat_coupled"]
q_source = P["mn"] * p_neutron + p_alpha + p_input
L = loop(q_source); C = cycle(L["T_out"])
# held mode: the dormant contributions formed as the design writes them
q_rec_held = 0.0 * L["w_fluid"] + 0.5 * 195.0
p_pump_total_held = 0.0 * L["p_elec"] + 195.0
eta_th_held = 0.0 * C["eta_fit"] + 0.333
p_th_held_new = P["mn"] * p_neutron + p_alpha + p_input + q_rec_held
p_th_old = P["mn"] * p_neutron + p_alpha + p_input + P["eta_p"] * P["p_pump"]
identity = dict(q_recovered_held=q_rec_held, q_recovered_eq=(q_rec_held == P["eta_p"] * P["p_pump"]),
                p_pump_total_held=p_pump_total_held, p_pump_total_eq=(p_pump_total_held == P["p_pump"]),
                eta_th_held=eta_th_held, eta_th_eq=(eta_th_held == P["eta_th"]),
                p_th_new_vs_oracle=(p_th_held_new == base["p_th"]), p_th_old_form_eq=(p_th_old == base["p_th"]))
# recirculating: the oracle's sum with the total in the same position
p_coils = P["p_tf"] + P["p_pf"]; p_sub = P["f_sub"] * base["p_et"]; p_aux = P["p_trit"] + P["p_house"]
p_cool = P["p_tfcool"] + P["p_pfcool"]
recirc_new = p_coils + p_pump_total_held + p_sub + p_aux + p_cool + base["p_cryo"] + base["heat_wallplug_total"]
recirc_old = p_coils + P["p_pump"] + p_sub + p_aux + p_cool + base["p_cryo"] + base["heat_wallplug_total"]
identity["recirc_eq"] = (recirc_new == recirc_old)
identity["q_eng_eq"] = (base["p_et"] / recirc_new == base["q_eng"])
res["held_mode_identity"] = identity

def with_overrides(**kw):
    saved = {k_: P[k_] for k_ in kw}
    P.update(kw)
    try:
        return vs.compute()
    finally:
        P.update(saved)

def live_eval(point_overrides, n_loops=14, f_loss=1.0):
    """Evaluate the loop and cycle at a point, then the oracle in live mode."""
    o = with_overrides(**point_overrides)                       # held chain at the point (for p_fus etc.)
    pf = o["p_fus"]; pa = (3.52 / 17.58) * pf; pn = pf - pa
    qs = P["mn"] * pn + pa + o["heat_coupled"]
    c = dict(CIRCUIT, n_loops=n_loops, f_loss=f_loss)
    Lp = loop(qs, c); Cp = cycle(Lp["T_out"])
    live = with_overrides(**point_overrides, p_pump=Lp["p_elec"], eta_p=1.0, eta_th=Cp["eta_th"])
    keys = ("p_th", "p_et", "p_net", "q_eng", "rec_frac", "lcoe", "lcoe_1cfe", "total_capital",
            "cas72_annual", "annual_fuel", "wall_load_peak", "B_peak", "beta", "p_aux_required")
    return dict(q_source=qs, p_fus=pf, loop=Lp, cycle=Cp,
                held={k_: o[k_] for k_ in keys}, live={k_: live[k_] for k_ in keys},
                verdicts_new=dict(loop_pressure_ok=Lp["p_loop_margin"] > 0.0,
                                  loop_capacity_ok=Lp["mdot_loop"] <= c["mdot_loop_ref"],
                                  cycle_domain_ok=Cp["domain_product"] >= 0.0),
                fences_live=dict(net_positive=live["p_net"] > 0.0, recirc_ok_rec_frac=live["rec_frac"],
                                 peak_field_ok=live["B_peak"] <= P["magnet_B_max"],
                                 wall_load_ok=live["wall_load_peak"] <= 4.05,
                                 burn_hold_ok=live["p_aux_required"] >= 0.0,
                                 sustainment_ok=live["p_aux_required"] <= live["heat_coupled"]))

res["circuit"] = CIRCUIT | dict(eta_is_repr=repr(ETA_IS)); res["fit"] = FIT; res["sco2_arm"] = SCO2
P0 = live_eval({})
P0["cycle_sco2"] = cycle(L["T_out"], dict(FIT, **SCO2))
P0["loop_only_lcoe"] = with_overrides(p_pump=L["p_elec"], eta_p=1.0)["lcoe"]
P0["cycle_only_lcoe"] = with_overrides(eta_th=C["eta_th"])["lcoe"]
P0["energy_check_closes"] = (L["q_ihx"] == q_source + L["w_fluid"]) and (L["p_elec"] == L["w_fluid"])
res["P0_design_point"] = P0
# a design-column point one step off (R 12.7, a 1.4, 15.4 MA, the baseline's plasma levers)
res["P1_design_a1.4"] = live_eval(dict(a=1.4))
# the committed cheapest machine c2823 at the instance's 14 loops
c2823 = dict(R=15.7, magnet_R0=15.7, a=2.2, magnet_I_coil=13000000.0, n_e0=5.06e20, T_i0=13.0, p_wallplug_heat=100.0)
res["P3_c2823_14loops"] = live_eval(c2823)
# c2823 with the loop count re-sized by the same rule (the study lever)
n27 = math.ceil(res["P3_c2823_14loops"]["loop"]["mdot"] / mdot_loop_ref)
res["P4_c2823_resized"] = dict(n_loops=n27, **live_eval(c2823, n_loops=n27))
# synthetic fail-closed checks: a 350 C hot leg (the Stellaris local segment) and a halved loop count
res["synthetic"] = dict(
    T_hot_350C=cycle(350.0 + 273.15),
    n_loops_7=loop(q_source, dict(CIRCUIT, n_loops=7)),
    dp_at_p_loop_margin_zero_flow_multiple=math.sqrt(p_loop / DP_REF) * mdot_loop_ref / L["mdot_loop"],
)
res["threshold_q_source_capacity_14_loops_MW"] = 14 * mdot_loop_ref * cp * dT_ref / 1e6
# window extremes for the dormant-term finiteness check (the largest committed plasma)
big = live_eval(dict(R=17.2, magnet_R0=17.2, a=2.2, magnet_I_coil=14000000.0, n_e0=5.06e20, T_i0=13.0, p_wallplug_heat=100.0))
res["window_extreme_c3598"] = dict(q_source=big["q_source"], loop=big["loop"], finite=all(math.isfinite(v) for v in big["loop"].values()))
OUT.write_text(json.dumps(res, indent=1, default=str))
print(json.dumps(res["reference"]["paths"]["weighted"], indent=1))
print("identity", identity)
for k_ in ("P0_design_point", "P1_design_a1.4", "P3_c2823_14loops", "P4_c2823_resized"):
    d = res[k_]; Lp = d["loop"]; Cp = d["cycle"]
    print(k_, "q_source", round(d["q_source"], 3), "mdot_loop", round(Lp["mdot_loop"], 3), "dp", round(Lp["dp_loop"] / 1e3, 2),
          "p_elec", round(Lp["p_elec"], 4), "eta", round(Cp["eta_th"], 6), "verdicts", d["verdicts_new"],
          "live lcoe", round(d["live"]["lcoe"], 6), "held lcoe", round(d["held"]["lcoe"], 6), "p_net", round(d["live"]["p_net"], 3), "rec", round(d["live"]["rec_frac"], 5))
print("loop-only / cycle-only LCOE", P0["loop_only_lcoe"], P0["cycle_only_lcoe"], "sco2", P0["cycle_sco2"]["eta_th"])
print("threshold q_source", res["threshold_q_source_capacity_14_loops_MW"], "synthetic", res["synthetic"]["T_hot_350C"]["domain_product"], res["synthetic"]["n_loops_7"]["capacity_margin"])
