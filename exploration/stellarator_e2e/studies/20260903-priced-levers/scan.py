"""Oracle window scan for `20260903-priced-levers` (runbook step 7).

Probes the candidate range with the package-owned oracle BEFORE any point runs, so the
executed windows are chosen from evidence rather than guessed. Reports, per axis, where
each fence flips -- in particular where the WI-036 sizing lever `j_wp` moves
`wp_stress_ok` and `cond_strain_ok`, and whether `peak_field_ok` alone still closes the
door at the printed 50 MW installed heating.
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
BASE = {"I_coil": 15.4e6, "n_e0": 5.06e20, "T_i0": 14.63, "p_input": 50.0,
        "j_wp": 118.8271604938272}

def point(I, ne, pin, j):
    return {f"{P}R": HELD["R"], f"{P}magnet__R0": HELD["R"], f"{P}a": HELD["a"],
            f"{P}availability": HELD["availability"], f"{P}discount_rate": HELD["discount_rate"],
            f"{P}magnet__I_coil": I, f"{P}n_e0": ne, f"{P}T_i0": BASE["T_i0"],
            f"{P}p_input": pin, f"{P}p_ecrh": pin, f"{P}magnet__j_wp": j}

def probe(pt):
    try:
        ch = oe.evaluate(pt)
    except Exception as exc:
        return None, f"{type(exc).__name__}: {exc}"
    return ch, None

def bounds():
    plant = json.loads((route.PACKAGE_DIR / "inputs" / "stellarator_plant_params.json").read_text())
    return {"B_max": plant[f"{P}magnet__B_max"], "sigma_allow": plant[f"{P}magnet__sigma_allow"],
            "eps_allow": plant[f"{P}magnet__eps_cond_allow"], "beta_limit": plant[f"{P}beta_limit"],
            "wall_limit": plant[f"{P}wall_load_limit"]}

def main():
    B = bounds()
    print("bounds read from the package:", B)
    out = {"bounds": B, "rows": []}
    I_VALUES = [12e6 + 1e6 * i for i in range(13)]
    J_VALUES = [90.0, 100.0, 112.0, 118.8271604938272, 130.0]
    for pin in (50.0, 110.0):
        print(f"\n--- installed heating {pin:.0f} MW ---")
        print(" I_MA  j_wp   B_peak  sigma_MPa  eps%   p_aux_req  field  stress strain sustain")
        for I in I_VALUES:
            for j in J_VALUES:
                ch, err = probe(point(I, BASE["n_e0"], pin, j))
                if err:
                    print("  %4.1f %6.1f  ORACLE ERROR %s" % (I/1e6, j, err[:60])); continue
                bp, sg, ep = ch[f"{P}peak_field_calc__B_peak"], ch[f"{P}wp_stress__sigma_wp"], ch[f"{P}cond_strain__eps_cond"]
                pa = ch[f"{P}sustain__p_aux_required"]
                row = dict(p_input=pin, I=I, j_wp=j, B_peak=bp, sigma=sg, eps=ep, p_aux_required=pa,
                           field_ok=bp <= B["B_max"], stress_ok=sg <= B["sigma_allow"],
                           strain_ok=ep <= B["eps_allow"], sustain_ok=pa <= pin)
                out["rows"].append(row)
                print("  %4.1f %6.1f %7.2f %9.1f %6.3f %10.1f   %-6s %-6s %-6s %s" % (
                    I/1e6, j, bp, sg/1e6, ep*100, pa,
                    "ok" if row["field_ok"] else "VIOL", "ok" if row["stress_ok"] else "VIOL",
                    "ok" if row["strain_ok"] else "VIOL", "ok" if row["sustain_ok"] else "VIOL"))
    (HERE / "results").mkdir(parents=True, exist_ok=True)
    (HERE / "results" / "window_scan.json").write_text(json.dumps(out, indent=1) + "\n")
    n_all = sum(1 for r in out["rows"] if r["field_ok"] and r["stress_ok"] and r["strain_ok"] and r["sustain_ok"])
    n_nofield = sum(1 for r in out["rows"] if r["stress_ok"] and r["strain_ok"] and r["sustain_ok"])
    print(f"\nscanned {len(out['rows'])} candidates: {n_all} pass all four fences; "
          f"{n_nofield} pass every fence EXCEPT the conductor ceiling")

if __name__ == "__main__":
    main()
