"""WI-042 prototype (oracle-side, scratch): the sustainment chain with the helium-ash profile from
the paper's A.5 rule (tau* uniform in rho) and electrons by quasi-neutrality, substituted into the
oracle's full plant computation. Nothing here touches the package. Prints old vs new at the
baseline and a small geometry-window table."""
import sys, math, json, time, copy
sys.path.insert(0, "exploration/stellarator_e2e")
import verify_stellaris as vs

KEV = vs.KEV_TO_J

def _sustainment_qn(p, V, B_axis):
    """Same contract as vs._sustainment; the ash profile from the rule, electrons by quasi-neutrality."""
    n_e0 = p["n_e0"]; T_i0 = p["T_i0"]; a = p["a"]; R = p["magnet_R0"]; B = B_axis
    alpha_n = p["alpha_n"]; alpha_T = p["alpha_T"]
    T_e0 = T_i0 / p["Ti_over_Te"]
    sigv_peak = vs._sigv_dt(T_i0)
    # ash shape S(rho) = u^(2 alpha_n) sigv(T_i0 u^alpha_T) / sigv(T_i0); S(0) = 1
    S = lambda u: (u ** (2.0 * alpha_n)) * vs._sigv_dt(T_i0 * (u ** alpha_T)) / sigv_peak
    I_line_fuel = vs._trapz_rho(lambda u, rho: u ** alpha_n)          # chord average of the fuel shape
    I_line_S = vs._trapz_rho(lambda u, rho: S(u))                      # chord average of the ash shape
    I_W_S = vs._trapz_rho(lambda u, rho: S(u) * (u ** alpha_T) * 2.0 * rho)   # <S u^alpha_T>_V
    I_vol_S = vs._trapz_rho(lambda u, rho: S(u) * 2.0 * rho)           # <S>_V
    fus_I = vs._profile_integral(alpha_n, alpha_T, T_i0)
    Cgeo = 0.134 * p["f_ren"] * a ** 2.28 * B ** 0.84 * p["iota_23"] ** 0.41 * R ** 0.64

    def state(n_He0):
        n_fuel = n_e0 - 2.0 * n_He0
        if n_fuel <= 0.0: raise RuntimeError("non-positive fuel")
        n_D0 = n_T0 = 0.5 * n_fuel
        n_bar19 = (2.0 * n_D0 * I_line_fuel + 2.0 * n_He0 * I_line_S) / 1e19
        C = Cgeo * n_bar19 ** 0.54
        p_avg = KEV * (2.0 * n_D0 * (T_e0 + T_i0) / (1.0 + alpha_n + alpha_T)
                       + n_He0 * (2.0 * T_e0 + T_i0) * I_W_S)
        W_th = 1.5 * p_avg * V * 1e-6
        tau_E = (C * W_th ** -0.61) ** (1.0 / 0.39)
        return n_D0, n_T0, W_th, tau_E, n_bar19, p_avg

    n_He0 = 0.0; converged = False
    for _ in range(vs.ASH_CAP):
        n_D0, n_T0, W_th, tau_E, n_bar19, p_avg = state(n_He0)
        n_He_new = p["f_suppr_ash"] * p["tau_ratio_ash"] * tau_E * n_D0 * n_T0 * sigv_peak
        if abs(n_He_new - n_He0) < vs.ASH_TOL:
            n_He0 = n_He_new; converged = True; break
        n_He0 = 0.5 * (n_He0 + n_He_new)
    if not converged: raise RuntimeError("ash fixed point did not converge")
    n_D0, n_T0, W_th, tau_E, n_bar19, p_avg = state(n_He0)
    p_fus = n_D0 * n_T0 * fus_I * p["E_fus"] * V * 1e-6
    n_e = lambda u: 2.0 * n_D0 * (u ** alpha_n) + 2.0 * n_He0 * S(u)
    p_brems = (5.35e-37 * p["Z_eff_core"]
               * vs._trapz_rho(lambda u, rho: n_e(u) ** 2 * math.sqrt(max(T_e0 * (u ** alpha_T), 1e-9)) * 2.0 * rho)
               * V * 1e-6)
    p_line = (p["f_W_core"]
              * vs._trapz_rho(lambda u, rho: n_e(u) ** 2 * vs._lz_w(T_e0 * (u ** alpha_T)) * 2.0 * rho)
              * V * 1e-6)
    n_e_volav = 2.0 * n_D0 / (1.0 + alpha_n) + 2.0 * n_He0 * I_vol_S
    alpha_n_e_eff = n_e0 / n_e_volav - 1.0       # the vol-av/peak relation the 0.596 was bound from
    p_sync = vs._p_sync_albajar(T_e0, n_e0 / 1e20, B, R, a, p["kappa_sync"], p["R_w_sync"], alpha_n_e_eff, alpha_T)
    p_rad = p_brems + p_line + p_sync
    p_alpha_heat = p["f_alpha_fast"] * p["sustain_ash_frac"] * p_fus
    p_aux_required = p_rad + W_th / tau_E - p_alpha_heat
    # effective power-law exponent of the ash shape (least squares on log, rho <= 0.85), as in the round-1 attribution
    xs, ys = [], []
    for i in range(1, 1701):
        rho = i / 2000.0; u = 1.0 - rho * rho
        xs.append(math.log(u)); ys.append(math.log(S(u)))
    mx = sum(xs) / len(xs); my = sum(ys) / len(ys)
    a_He_eff = sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / sum((x - mx) ** 2 for x in xs)
    return dict(n_bar19=n_bar19, n_He0=n_He0, n_D0=n_D0, n_T0=n_T0, T_e0=T_e0, W_th=W_th, tau_E=tau_E,
                p_brems=p_brems, p_line=p_line, p_sync=p_sync, p_rad=p_rad, p_alpha_heat=p_alpha_heat,
                p_aux_required=p_aux_required, p_avg=p_avg, n_e_volav=n_e_volav, alpha_n_e_eff=alpha_n_e_eff,
                alpha_He_eff=a_He_eff, I_W_S=I_W_S, I_line_S=I_line_S)

def run(overrides=None, qn=False):
    saved = dict(vs.IN); saved_fn = vs._sustainment
    try:
        if overrides: vs.IN.update(overrides)
        if qn: vs._sustainment = _sustainment_qn
        r = vs.compute()
        # beta from the SAME <p> as W (one pressure integral): beta = 2 mu0 <p> / B^2, <p> = W/(1.5 V)
        r["beta_from_W"] = 2.0 * vs.IN["beta_mu0"] * (r["W_th"] * 1e6 / (1.5 * r["V"])) / (r["B_axis"] ** 2)
        if qn:
            s = _sustainment_qn(vs.IN, r["V"], r["B_axis"])
            r.update({k: s[k] for k in ("alpha_n_e_eff", "alpha_He_eff", "n_e_volav", "p_avg")})
        return r
    finally:
        vs.IN.clear(); vs.IN.update(saved); vs._sustainment = saved_fn

keys = ["W_th", "tau_E", "n_bar19", "n_He0", "n_D0", "p_fus", "p_brems", "p_line", "p_sync", "p_rad",
        "p_alpha_heat", "p_aux_required", "wall_load", "wall_load_peak", "beta", "beta_from_W", "B_axis",
        "p_net", "rec_frac", "cas72_annual", "lcoe", "lcoe_1cfe"]
t0 = time.time()
old = run(); new = run(qn=True)
print(f"baseline old vs new ({time.time()-t0:.1f}s)")
print(f"{'channel':18s} {'old':>16s} {'new':>16s} {'new/old':>9s}")
for k in keys:
    if k in old and k in new:
        o, n = old[k], new[k]
        print(f"{k:18s} {o:16.6f} {n:16.6f} {n/o:9.5f}" if o else f"{k:18s} {o:16.6f} {n:16.6f}")
print(f"alpha_n_e_eff {new['alpha_n_e_eff']:.4f}  alpha_He_eff {new['alpha_He_eff']:.3f}  <n_e> {new['n_e_volav']/1e20:.3f}e20 (printed 3.17; bound exponent 0.596)")
print(f"verdicts: sustainment old {old['p_aux_required']:.2f} vs 50 -> {'violated' if old['p_aux_required']>50 else 'satisfied'}; new {new['p_aux_required']:.2f} -> {'violated' if new['p_aux_required']>50 else 'satisfied'}")
print(f"wall: old peak {old['wall_load_peak']:.4f} vs 4.05; new {new['wall_load_peak']:.4f}")
json.dump({"old": {k: old.get(k) for k in keys}, "new": {k: new.get(k) for k in keys + ['alpha_n_e_eff','alpha_He_eff','n_e_volav']}},
          open(sys.argv[1] + "/baseline_old_new.json", "w"), indent=1)

# the ash shape's effective exponent vs T_i0 (the scaling question, shape only: depends on T_i0, alpha_n, alpha_T)
print("\nash shape vs T_i0 (alpha_n 0.33, alpha_T 1.19): T_i0, alpha_He_eff, I_W_S, I_line_S")
for T in (10.0, 12.0, 14.63, 16.0, 18.0, 20.0):
    s = _sustainment_qn(dict(vs.IN, T_i0=T), old["V"], old["B_axis"])
    print(f"  {T:6.2f}  {s['alpha_He_eff']:.3f}  {s['I_W_S']:.4f}  {s['I_line_S']:.4f}")

# geometry-window corners: W ratio new/old with the closure live at each corner (R with its tie, a, T, n)
print("\nwindow corners (I_coil at the baseline; R with magnet_R0 tie): R a T n_e0x | W_old W_new ratio | p_aux_old p_aux_new | alpha_He_eff alpha_n_e_eff")
rows = []
for R in (11.2, 14.2, 17.2):
    for a in (1.3, 2.2):
        for T in (12.0, 18.0):
            for nx in (0.9, 1.1):
                ov = dict(R=R, magnet_R0=R, a=a, T_i0=T, n_e0=5.06e20 * nx)
                try:
                    o = run(ov); n = run(ov, qn=True)
                    rows.append(dict(R=R, a=a, T=T, nx=nx, W_old=o["W_th"], W_new=n["W_th"], p_aux_old=o["p_aux_required"], p_aux_new=n["p_aux_required"], aHe=n["alpha_He_eff"], ane=n["alpha_n_e_eff"]))
                    print(f"  {R:5.1f} {a:4.1f} {T:5.1f} {nx:4.1f} | {o['W_th']:8.1f} {n['W_th']:8.1f} {n['W_th']/o['W_th']:.4f} | {o['p_aux_required']:8.2f} {n['p_aux_required']:8.2f} | {n['alpha_He_eff']:.3f} {n['alpha_n_e_eff']:.3f}")
                except Exception as e:
                    print(f"  {R:5.1f} {a:4.1f} {T:5.1f} {nx:4.1f} | FAILED: {e}")
json.dump(rows, open(sys.argv[1] + "/window_corners.json", "w"), indent=1)
print(f"done {time.time()-t0:.1f}s")
