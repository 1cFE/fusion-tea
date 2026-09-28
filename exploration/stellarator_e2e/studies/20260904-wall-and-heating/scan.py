"""Oracle window scan for `20260904-wall-and-heating` (runbook step 7).

Probes the candidate range with the package-owned oracle BEFORE any point runs, so the
executed windows are chosen from evidence rather than guessed. Same ordering note as the
predecessor, recorded rather than hidden: the scan runs before the step-4 critique so the
critique reads real numbers; no point runs through the sealed package here.

What is new versus the predecessor scan: the wall fence is HONEST. The scan reads the
oracle's own `wall_peak_calc__wall_load_peak` (the circular-torus average x the WI-041
source-anchored calibration 1.316441) against the printed 4.05 peak, exactly as the
package's `wall_load_ok` does, and geometry (R with its tie, a) is swept for the first
time on this fence. The round-1 external band (net 1.15x and 1.83x on the average) is
carried as a shadow, so the anchor's sensitivity is visible in the scan too. The
consequence chain is read per candidate from the oracle's own CAS72 and from the
fluence-limited core life re-derived from the peak (18 MW-yr/m^2 over the peak, clipped
as the calc clips it).

Held, every key explicit: eta_source_heat 0.50, eta_couple_heat 1.00, both dormant
direct-heat terms 0.0, j_wp 118.8271604938272, availability 0.85, discount_rate 0.07,
and the six wall_peak_* reference facts at their bound values (not passed: the oracle
carries them as `IN` defaults identical to the package's bound values).
"""
from __future__ import annotations
import json, math, sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
STUDIES = HERE.parent
if str(STUDIES) not in sys.path:
    sys.path.insert(0, str(STUDIES))
import study_route as route  # noqa: E402
import oracle_entry as oe    # noqa: E402
P = route.P

HELD = {"availability": 0.85, "discount_rate": 0.07, "j_wp": 118.8271604938272,
        "eta_source_heat": 0.50, "eta_couple_heat": 1.0,
        "p_delivered_direct_heat": 0.0, "p_coupled_direct_heat": 0.0}
NE0 = 5.06e20
FLUENCE_LIMIT = 18.0
SHADOW = {"lo": 1.15, "hi": 1.83}   # round-1 external band on the AVERAGE (T-001 round 1)


def point(R, a, I, ne, T, wallplug):
    return {f"{P}R": R, f"{P}magnet__R0": R, f"{P}a": a,
            f"{P}availability": HELD["availability"], f"{P}discount_rate": HELD["discount_rate"],
            f"{P}magnet__I_coil": I, f"{P}n_e0": ne, f"{P}T_i0": T,
            f"{P}magnet__j_wp": HELD["j_wp"],
            f"{P}p_wallplug_heat": wallplug,
            f"{P}eta_source_heat": HELD["eta_source_heat"],
            f"{P}eta_couple_heat": HELD["eta_couple_heat"],
            f"{P}p_delivered_direct_heat": HELD["p_delivered_direct_heat"],
            f"{P}p_coupled_direct_heat": HELD["p_coupled_direct_heat"]}


def bounds():
    plant = json.loads((route.PACKAGE_DIR / "inputs" / "stellarator_plant_params.json").read_text())
    mfe = json.loads((route.PACKAGE_DIR / "inputs" / "mfe_plant_params.json").read_text())
    return {"B_max": plant[f"{P}magnet__B_max"], "sigma_allow": plant[f"{P}magnet__sigma_allow"],
            "eps_cond_allow": plant[f"{P}magnet__eps_cond_allow"],
            "beta_limit": plant[f"{P}beta_limit"],
            "wall_load_limit": plant[f"{P}wall_load_limit"],
            "recirc_threshold": mfe[f"{P}recirc_ok__threshold"],
            "operational_years": plant[f"{P}operational_years"],
            "availability": plant[f"{P}availability"]}


def core_life(peak, B):
    """The fluence-limited core life in full-power years and the replacement count,
    re-derived from the peak exactly as 'Levelized Replacement Cost' clips them."""
    fpy = min(max(FLUENCE_LIMIT / max(peak, 1e-6), 0.5), B["operational_years"] * B["availability"])
    cal = fpy / B["availability"]
    n_rep = max(0.0, float(math.ceil(B["operational_years"] / cal)) - 1.0)
    return fpy, n_rep


def probe(pt, B):
    try:
        ch = oe.evaluate(pt)
    except Exception as exc:
        return None, f"{type(exc).__name__}: {exc}"
    coupled = ch[f"{P}heat__p_coupled"]
    avg = ch[f"{P}wall_load_calc__wall_load"]
    peak = ch[f"{P}wall_peak_calc__wall_load_peak"]
    v = []
    if ch[f"{P}peak_field_calc__B_peak"] > B["B_max"]: v.append("field")
    if ch[f"{P}wp_stress__sigma_wp"] > B["sigma_allow"]: v.append("stress")
    if ch[f"{P}cond_strain__eps_cond"] > B["eps_cond_allow"]: v.append("strain")
    if ch[f"{P}sustain__p_aux_required"] > coupled: v.append("sustain")
    if peak > B["wall_load_limit"]: v.append("wall")
    if ch[f"{P}beta_calc__beta"] > B["beta_limit"]: v.append("beta")
    if ch[f"{P}pb__rec_frac"] > B["recirc_threshold"]: v.append("recirc")
    if ch[f"{P}pb__p_net"] <= 0: v.append("net")
    fpy, n_rep = core_life(peak, B)
    return {"B_peak": ch[f"{P}peak_field_calc__B_peak"], "sigma": ch[f"{P}wp_stress__sigma_wp"],
            "eps": ch[f"{P}cond_strain__eps_cond"], "p_aux": ch[f"{P}sustain__p_aux_required"],
            "coupled": coupled, "p_fus": ch[f"{P}fusion__p_fus"],
            "wall_avg": avg, "wall_peak": peak,
            "calibration": ch[f"{P}wall_peak_cal__calibration"],
            "wall_shadow_lo": avg * SHADOW["lo"], "wall_shadow_hi": avg * SHADOW["hi"],
            "core_life_fpy": fpy, "n_rep": n_rep, "cas72": ch[f"{P}cas72_calc__cost"],
            "beta": ch[f"{P}beta_calc__beta"], "rec_frac": ch[f"{P}pb__rec_frac"],
            "p_net": ch[f"{P}pb__p_net"], "lcoe": ch[f"{P}lcoe_calc__lcoe"],
            "magnet_capital": ch[f"{P}magnet_capital_rollup__capital_cost"],
            "violated": v}, None


R_VALUES = [9.7, 11.2, 12.7, 14.2, 15.7]
A_VALUES = [1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8]      # brackets the committed a >= 1.70
I_VALUES = [13.0e6, 14.0e6, 15.0e6, 16.0e6, 17.0e6, 18.0e6]
T_VALUES = [14.63, 16.0, 18.0, 20.0, 22.0]                  # past 18 keV
NE_MULT = [0.8, 0.9, 1.0, 1.1, 1.2, 1.3]
WALLPLUG = [100.0, 220.0]


def main():
    B = bounds()
    print("bounds read from the package:", {k: round(v, 4) for k, v in B.items()})
    rows = []
    for wp in WALLPLUG:
        for R in R_VALUES:
            for a in A_VALUES:
                if not (R > a + 2.25):
                    continue  # ANNEX validity mask: a torus that self-intersects is not a machine
                for I in I_VALUES:
                    for T in T_VALUES:
                        for nf in NE_MULT:
                            r, err = probe(point(R, a, I, NE0 * nf, T, wp), B)
                            stamp = {"wallplug": wp, "R": R, "a": a, "I": I, "T_i0": T, "ne_mult": nf}
                            if err:
                                rows.append({**stamp, "error": err}); continue
                            r.update(stamp); rows.append(r)
    out = {"bounds": B, "axes_scanned": ["p_wallplug_heat", "R+tie", "a", "I_coil", "T_i0", "n_e0"],
           "held": HELD, "shadow_factors_on_average": SHADOW, "rows": rows}
    (HERE / "results").mkdir(parents=True, exist_ok=True)
    (HERE / "results" / "window_scan.json").write_text(json.dumps(out, indent=1) + "\n")

    from collections import Counter
    errs = sum(1 for r in rows if r.get("error"))
    print(f"\nscanned {len(rows)} candidates ({errs} oracle errors)")
    for wp in WALLPLUG:
        sub = [r for r in rows if r.get("wallplug") == wp and not r.get("error")]
        ok = [r for r in sub if not r["violated"]]
        print(f"\n--- wall-plug {wp:.0f} MW ({wp*0.5:.0f} MW coupled): {len(sub)} evaluated, {len(ok)} feasible ---")
        if ok:
            best = min(ok, key=lambda r: r["lcoe"])
            print("  best feasible LCOE %.3f at R=%.1f a=%.2f I=%.1f MA T=%.2f n=%.1fx  peak %.3f life %.2f FPY n_rep %d cas72 %.1f M$"
                  % (best["lcoe"], best["R"], best["a"], best["I"]/1e6, best["T_i0"], best["ne_mult"], best["wall_peak"], best["core_life_fpy"], best["n_rep"], best["cas72"]/1e6))
            for ax in ("R", "a", "I", "T_i0", "ne_mult"):
                vals = sorted(set(r[ax] for r in ok)); print(f"  feasible {ax}: {vals}")
        c = Counter(",".join(r["violated"]) for r in sub if r["violated"])
        print("  most common violation sets:", c.most_common(8))
        for name in ("wall", "field", "sustain", "beta", "recirc"):
            alone = [r for r in sub if r["violated"] == [name]]
            print(f"  blocked by {name.upper()} ALONE: {len(alone)}")
        # the shadow band: how many of the feasible set survive the external bounds
        lo = [r for r in ok if r["wall_shadow_lo"] <= B["wall_load_limit"]]
        hi = [r for r in ok if r["wall_shadow_hi"] <= B["wall_load_limit"]]
        print(f"  feasible surviving shadow lo (1.15x avg): {len(lo)}; hi (1.83x): {len(hi)}")
        # the wall's price: cheapest feasible-but-for-the-wall vs cheapest feasible
        but_wall = [r for r in sub if r["violated"] == ["wall"]]
        if but_wall and ok:
            bw = min(but_wall, key=lambda r: r["lcoe"]); bo = min(ok, key=lambda r: r["lcoe"])
            print("  cheapest wall-alone-blocked LCOE %.3f (peak %.3f) vs cheapest feasible %.3f -> wall's price %.3f $/MWh"
                  % (bw["lcoe"], bw["wall_peak"], bo["lcoe"], bo["lcoe"] - bw["lcoe"]))
        # a-dependence at the baseline column (R 12.7, I 15 MA, T 14.63, n 1.0x)
        col = [r for r in sub if r["R"] == 12.7 and r["I"] == 15.0e6 and r["T_i0"] == 14.63 and r["ne_mult"] == 1.0]
        for r in sorted(col, key=lambda r: r["a"]):
            print("    a=%.2f peak=%.3f avg=%.3f p_aux=%.1f coupled=%.1f B_peak=%.2f lcoe=%.2f viol=%s" % (r["a"], r["wall_peak"], r["wall_avg"], r["p_aux"], r["coupled"], r["B_peak"], r["lcoe"], r["violated"]))
        # R-dependence at the baseline column (a 1.3, I 15 MA, T 14.63, n 1.0x)
        col = [r for r in sub if r["a"] == 1.3 and r["I"] == 15.0e6 and r["T_i0"] == 14.63 and r["ne_mult"] == 1.0]
        for r in sorted(col, key=lambda r: r["R"]):
            print("    R=%.1f peak=%.3f avg=%.3f p_fus=%.1f p_aux=%.1f B_peak=%.2f lcoe=%.2f viol=%s" % (r["R"], r["wall_peak"], r["wall_avg"], r["p_fus"], r["p_aux"], r["B_peak"], r["lcoe"], r["violated"]))


if __name__ == "__main__":
    main()
