"""Oracle window scan for `20260903-priced-levers` (runbook step 7).

Probes the candidate range with the package-owned oracle BEFORE any point runs, so the
executed windows are chosen from evidence rather than guessed.

REVISION 2026-09-03, after the pre-execution critique returned MAJOR. The first scan
covered I_coil x j_wp at two heating levels and held n_e0 and T_i0 at baseline, and the
windows were nonetheless described as scan-derived across all axes (critique MAJOR 3).
Worse, the held T_i0 = 14.63 slice produced a fence conclusion the dropped axis
contradicts (critique MAJOR 2): with T and n free there are points at the printed 50 MW
BELOW the conductor ceiling whose only violated fence is the neutron wall load. This scan
covers all four candidate axes so the windows are fixed from evidence over the space the
study actually claims to search.
"""
from __future__ import annotations
import json, sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
STUDIES = HERE.parent
if str(STUDIES) not in sys.path:
    sys.path.insert(0, str(STUDIES))
import study_route as route  # noqa: E402
import oracle_entry as oe    # noqa: E402
P = route.P

HELD = {"a": 1.3, "availability": 0.85, "discount_rate": 0.07, "R": 12.7}
NE0 = 5.06e20

def point(I, ne, T, pin, j):
    return {f"{P}R": HELD["R"], f"{P}magnet__R0": HELD["R"], f"{P}a": HELD["a"],
            f"{P}availability": HELD["availability"], f"{P}discount_rate": HELD["discount_rate"],
            f"{P}magnet__I_coil": I, f"{P}n_e0": ne, f"{P}T_i0": T,
            f"{P}p_input": pin, f"{P}p_ecrh": pin, f"{P}magnet__j_wp": j}

def bounds():
    plant = json.loads((route.PACKAGE_DIR / "inputs" / "stellarator_plant_params.json").read_text())
    mfe = json.loads((route.PACKAGE_DIR / "inputs" / "mfe_plant_params.json").read_text())
    return {"B_max": plant[f"{P}magnet__B_max"], "sigma_allow": plant[f"{P}magnet__sigma_allow"],
            "eps_cond_allow": plant[f"{P}magnet__eps_cond_allow"], "beta_limit": plant[f"{P}beta_limit"],
            "wall_load_limit": plant[f"{P}wall_load_limit"],
            "recirc_threshold": mfe[f"{P}recirc_ok__threshold"]}

def probe(pt, pin, B):
    try:
        ch = oe.evaluate(pt)
    except Exception as exc:
        return None, f"{type(exc).__name__}: {exc}"
    v = []
    if ch[f"{P}peak_field_calc__B_peak"] > B["B_max"]: v.append("field")
    if ch[f"{P}wp_stress__sigma_wp"] > B["sigma_allow"]: v.append("stress")
    if ch[f"{P}cond_strain__eps_cond"] > B["eps_cond_allow"]: v.append("strain")
    if ch[f"{P}sustain__p_aux_required"] > pin: v.append("sustain")
    if ch[f"{P}wall_load_calc__wall_load"] > B["wall_load_limit"]: v.append("wall")
    if ch[f"{P}beta_calc__beta"] > B["beta_limit"]: v.append("beta")
    if ch[f"{P}pb__rec_frac"] > B["recirc_threshold"]: v.append("recirc")
    if ch[f"{P}pb__p_net"] <= 0: v.append("net")
    return {"B_peak": ch[f"{P}peak_field_calc__B_peak"], "sigma": ch[f"{P}wp_stress__sigma_wp"],
            "eps": ch[f"{P}cond_strain__eps_cond"], "p_aux": ch[f"{P}sustain__p_aux_required"],
            "wall": ch[f"{P}wall_load_calc__wall_load"], "beta": ch[f"{P}beta_calc__beta"],
            "lcoe": ch[f"{P}lcoe_calc__lcoe"], "violated": v}, None

def main():
    B = bounds()
    print("bounds read from the package:", {k: round(v, 4) for k, v in B.items()})
    rows = []
    I_VALUES = [round(13.0e6 + 0.5e6 * i) for i in range(9)]      # 13.0 .. 17.0 MA step 0.5
    I_HIGH   = [18.0e6, 20.0e6, 22.0e6]                            # above-ceiling probes
    J_VALUES = [90.0, 112.0, 118.8271604938272, 130.0]
    T_VALUES = [12.0, 14.63, 16.0, 17.0, 18.0, 19.0, 20.0, 22.0]
    NE_MULT  = [0.8, 0.9, 1.0, 1.1, 1.2, 1.3, 1.4, 1.6]
    for pin in (50.0, 110.0):
        for I in I_VALUES + I_HIGH:
            for j in J_VALUES:
                for T in T_VALUES:
                    for nf in NE_MULT:
                        r, err = probe(point(I, NE0 * nf, T, pin, j), pin, B)
                        if err:
                            rows.append({"p_input": pin, "I": I, "j_wp": j, "T_i0": T, "ne_mult": nf,
                                         "error": err}); continue
                        r.update({"p_input": pin, "I": I, "j_wp": j, "T_i0": T, "ne_mult": nf})
                        rows.append(r)
    out = {"bounds": B, "axes_scanned": ["I_coil", "j_wp", "T_i0", "n_e0", "p_input"], "rows": rows}
    (HERE / "results").mkdir(parents=True, exist_ok=True)
    (HERE / "results" / "window_scan.json").write_text(json.dumps(out, indent=1) + "\n")

    ok = [r for r in rows if not r.get("error") and not r["violated"]]
    print(f"\nscanned {len(rows)} candidates ({sum(1 for r in rows if r.get('error'))} oracle errors); "
          f"{len(ok)} pass every fence")
    for pin in (50.0, 110.0):
        sub = [r for r in rows if r.get("p_input") == pin and not r.get("error")]
        okp = [r for r in sub if not r["violated"]]
        print(f"\n--- p = {pin:.0f} MW: {len(sub)} evaluated, {len(okp)} feasible ---")
        if okp:
            best = min(okp, key=lambda r: r["lcoe"])
            print("  best feasible LCOE %.3f at I=%.1f MA j_wp=%.1f T=%.2f n=%.1fx"
                  % (best["lcoe"], best["I"]/1e6, best["j_wp"], best["T_i0"], best["ne_mult"]))
            print("  feasible I range %.1f..%.1f MA, T %.2f..%.2f, n %.1f..%.1fx"
                  % (min(r["I"] for r in okp)/1e6, max(r["I"] for r in okp)/1e6,
                     min(r["T_i0"] for r in okp), max(r["T_i0"] for r in okp),
                     min(r["ne_mult"] for r in okp), max(r["ne_mult"] for r in okp)))
        from collections import Counter
        c = Counter(",".join(r["violated"]) for r in sub if r["violated"])
        print("  most common violation sets:", c.most_common(6))
        wall_only = [r for r in sub if r["violated"] == ["wall"]]
        print(f"  blocked by WALL LOAD ALONE: {len(wall_only)}")
        field_only = [r for r in sub if r["violated"] == ["field"]]
        print(f"  blocked by CONDUCTOR CEILING ALONE: {len(field_only)}")
        print("  beta max over the scanned window: %.4f (limit %.3f)"
              % (max(r["beta"] for r in sub), B["beta_limit"]))

if __name__ == "__main__":
    main()
