"""Oracle window scan for `20260903-wall-and-heating` (runbook step 7).

Probes the candidate range with the package-owned oracle BEFORE any point runs, so the
executed windows are chosen from evidence rather than guessed.

ORDERING NOTE, recorded rather than hidden: the runbook puts the scan at step 7, after the
pre-execution critique at step 4. This scan was run BEFORE that critique so the critique
could read real numbers instead of proposed windows. Nothing was executed through the
package first -- the scan is an oracle probe and runs no point through the sealed package,
which is what step 4's "before any point runs" governs.

What is new here versus the predecessor scan: `eta_source_heat` is a swept axis. Before
WI-039 the lumped `eta_pin` reached only `net_positive` and `recirc_ok` (measured, not
assumed: `pre_wi039_indicators.json`); through the heating chain both efficiencies and the
wall-plug power now reach `sustainment_ok` as well, so heating-technology efficiency can
move the plasma's own fence for the first time. The scan exists to find out whether it
moves it enough to matter.

`eta_couple_heat` is NOT scanned. It is held at its stated assumption of 1.00 -- see
axes.json for why sweeping an assumption nobody measured would read as knowledge the
model does not have.
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

HELD = {"a": 1.3, "availability": 0.85, "discount_rate": 0.07, "R": 12.7,
        "j_wp": 118.8271604938272, "eta_couple_heat": 1.0}
NE0 = 5.06e20


def point(I, ne, T, wallplug, eta_source):
    return {f"{P}R": HELD["R"], f"{P}magnet__R0": HELD["R"], f"{P}a": HELD["a"],
            f"{P}availability": HELD["availability"],
            f"{P}discount_rate": HELD["discount_rate"],
            f"{P}magnet__I_coil": I, f"{P}n_e0": ne, f"{P}T_i0": T,
            f"{P}magnet__j_wp": HELD["j_wp"],
            f"{P}p_wallplug_heat": wallplug,
            f"{P}eta_source_heat": eta_source,
            f"{P}eta_couple_heat": HELD["eta_couple_heat"],
            f"{P}p_delivered_direct_heat": 0.0,
            f"{P}p_coupled_direct_heat": 0.0}


def bounds():
    plant = json.loads((route.PACKAGE_DIR / "inputs" / "stellarator_plant_params.json").read_text())
    mfe = json.loads((route.PACKAGE_DIR / "inputs" / "mfe_plant_params.json").read_text())
    return {"B_max": plant[f"{P}magnet__B_max"], "sigma_allow": plant[f"{P}magnet__sigma_allow"],
            "eps_cond_allow": plant[f"{P}magnet__eps_cond_allow"],
            "beta_limit": plant[f"{P}beta_limit"],
            "wall_load_limit": plant[f"{P}wall_load_limit"],
            "recirc_threshold": mfe[f"{P}recirc_ok__threshold"]}


def probe(pt, B):
    """One oracle probe. The installed side of the sustainment fence is now COMPUTED
    (the chain's coupled power), not the held entry value it used to be -- so the
    comparison reads the oracle's own heat_coupled rather than the swept wall-plug key."""
    try:
        ch = oe.evaluate(pt)
    except Exception as exc:
        return None, f"{type(exc).__name__}: {exc}"
    coupled = ch[f"{P}heat__p_coupled"]
    v = []
    if ch[f"{P}peak_field_calc__B_peak"] > B["B_max"]: v.append("field")
    if ch[f"{P}wp_stress__sigma_wp"] > B["sigma_allow"]: v.append("stress")
    if ch[f"{P}cond_strain__eps_cond"] > B["eps_cond_allow"]: v.append("strain")
    if ch[f"{P}sustain__p_aux_required"] > coupled: v.append("sustain")
    if ch[f"{P}wall_load_calc__wall_load"] > B["wall_load_limit"]: v.append("wall")
    if ch[f"{P}beta_calc__beta"] > B["beta_limit"]: v.append("beta")
    if ch[f"{P}pb__rec_frac"] > B["recirc_threshold"]: v.append("recirc")
    if ch[f"{P}pb__p_net"] <= 0: v.append("net")
    return {"B_peak": ch[f"{P}peak_field_calc__B_peak"],
            "sigma": ch[f"{P}wp_stress__sigma_wp"],
            "eps": ch[f"{P}cond_strain__eps_cond"],
            "p_aux": ch[f"{P}sustain__p_aux_required"],
            "coupled": coupled,
            "delivered": ch[f"{P}heat__p_delivered"],
            "wallplug_total": ch[f"{P}heat__p_wallplug_total"],
            "heating_capital": ch[f"{P}heating_cost__cost"],
            "wall": ch[f"{P}wall_load_calc__wall_load"],
            "beta": ch[f"{P}beta_calc__beta"],
            "rec_frac": ch[f"{P}pb__rec_frac"],
            "p_net": ch[f"{P}pb__p_net"],
            "lcoe": ch[f"{P}lcoe_calc__lcoe"], "violated": v}, None


def main():
    B = bounds()
    print("bounds read from the package:", {k: round(v, 4) for k, v in B.items()})
    rows = []
    I_VALUES = [round(13.0e6 + 0.5e6 * i) for i in range(11)]   # 13.0 .. 18.0 MA step 0.5
    T_VALUES = [14.63, 16.0, 17.0, 18.0, 19.0, 20.0, 22.0, 24.0]  # PAST 18 keV (#5)
    NE_MULT = [0.8, 0.9, 1.0, 1.1, 1.2, 1.3, 1.4]
    ETA_SOURCE = [0.40, 0.45, 0.50, 0.55, 0.60]
    WALLPLUG = [100.0, 220.0]                                    # 50 and 110 MW coupled at 0.50
    for wp in WALLPLUG:
        for eta in ETA_SOURCE:
            for I in I_VALUES:
                for T in T_VALUES:
                    for nf in NE_MULT:
                        r, err = probe(point(I, NE0 * nf, T, wp, eta), B)
                        stamp = {"wallplug": wp, "eta_source": eta, "I": I,
                                 "T_i0": T, "ne_mult": nf}
                        if err:
                            rows.append({**stamp, "error": err}); continue
                        r.update(stamp); rows.append(r)
    out = {"bounds": B,
           "axes_scanned": ["p_wallplug_heat", "eta_source_heat", "I_coil", "T_i0", "n_e0"],
           "held": HELD, "rows": rows}
    (HERE / "results").mkdir(parents=True, exist_ok=True)
    (HERE / "results" / "window_scan.json").write_text(json.dumps(out, indent=1) + "\n")

    from collections import Counter
    errs = sum(1 for r in rows if r.get("error"))
    ok = [r for r in rows if not r.get("error") and not r["violated"]]
    print(f"\nscanned {len(rows)} candidates ({errs} oracle errors); {len(ok)} pass every fence")
    for wp in WALLPLUG:
        sub = [r for r in rows if r.get("wallplug") == wp and not r.get("error")]
        okp = [r for r in sub if not r["violated"]]
        print(f"\n--- wall-plug {wp:.0f} MW ({wp*0.5:.0f} MW coupled at eta_source 0.50):"
              f" {len(sub)} evaluated, {len(okp)} feasible ---")
        if okp:
            best = min(okp, key=lambda r: r["lcoe"])
            print("  best feasible LCOE %.3f at eta_source=%.2f I=%.1f MA T=%.2f n=%.1fx"
                  % (best["lcoe"], best["eta_source"], best["I"]/1e6, best["T_i0"], best["ne_mult"]))
            print("  feasible eta_source %.2f..%.2f, I %.1f..%.1f MA, T %.2f..%.2f, n %.1f..%.1fx"
                  % (min(r["eta_source"] for r in okp), max(r["eta_source"] for r in okp),
                     min(r["I"] for r in okp)/1e6, max(r["I"] for r in okp)/1e6,
                     min(r["T_i0"] for r in okp), max(r["T_i0"] for r in okp),
                     min(r["ne_mult"] for r in okp), max(r["ne_mult"] for r in okp)))
        c = Counter(",".join(r["violated"]) for r in sub if r["violated"])
        print("  most common violation sets:", c.most_common(6))
        for name in ("wall", "field", "sustain"):
            alone = [r for r in sub if r["violated"] == [name]]
            print(f"  blocked by {name.upper()} ALONE: {len(alone)}")
        # what the efficiency axis actually buys, at fixed everything else
        for eta in ETA_SOURCE:
            e = [r for r in sub if r["eta_source"] == eta]
            eok = [r for r in e if not r["violated"]]
            best = min((r["lcoe"] for r in eok), default=None)
            print("    eta_source %.2f: %3d feasible, coupled %.1f MW, best LCOE %s"
                  % (eta, len(eok), wp * eta,
                     ("%.3f" % best) if best is not None else "-"))


if __name__ == "__main__":
    main()
