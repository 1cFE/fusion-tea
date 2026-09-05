"""Basis B -- the paper's own closure (the operating-point prototype), with W forced to the printed value.

Loads `work/orchestration/goals/operating-point-closure/evidence/T-002_prototype/op_solve_final.py`
as SOURCE, drops its top-level runs, and patches its two `W=1.5*p*V*1e-6` statements to
`... * W_SCALE`. Nothing on disk is edited. The prototype is the independent check on the
model-side result: same appendix closure, coarser quadrature (N = 400), V = 425, R = 12.74.

Reports the point-A balance residual g = f_alpha*ash_frac*p_fus + p_aux - rad - W/tau_E
(negative = heating short) unmodified and with W scaled, and whether a burn attractor
exists at the point-A levers.
"""
import json, sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
REPO = HERE.parents[5]
PROTO = REPO / "work/orchestration/goals/operating-point-closure/evidence/T-002_prototype/op_solve_final.py"
src = PROTO.read_text().split("# 1) ash chain check")[0]
LINE = "W=1.5*p*V*1e-6"
assert src.count(LINE) == 2, src.count(LINE)
src = src.replace(LINE, LINE + "*W_SCALE")
ns = {"W_SCALE": 1.0}
exec(compile(src, str(PROTO), "exec"), ns)
state, burn = ns["state"], ns["burn"]
W_PRINTED = 504.65
out = {}
s0 = state(14.63, 5.06e20, 0.0, 9.0, 0.92)
ns["W_SCALE"] = W_PRINTED / s0["W"]
s1 = state(14.63, 5.06e20, 0.0, 9.0, 0.92)
for tag, s in (("unmodified", s0), ("W_forced", s1)):
    out[tag] = {k: s[k] for k in ("g", "p_fus", "W", "tauE", "rad", "n_He0", "beta")} | {"W_over_tauE": s["W"] / s["tauE"]}
    print(f"{tag:11s} W {s['W']:8.3f} MJ tauE {s['tauE']:.4f} s W/tauE {s['W']/s['tauE']:7.2f} MW rad {s['rad']:7.2f} p_fus {s['p_fus']:7.1f} "
          f"n_He0 {s['n_He0']:.3e} beta {s['beta']:.5f}  residual g(p_aux=0) {s['g']:+8.2f} MW  -> required {-s['g']:7.2f} MW vs 50 coupled")
out["W_scale"] = ns["W_SCALE"]
# burn attractors at the point-A levers, both states (the prototype's finding 2/3 re-read)
for tag, sc in (("unmodified", 1.0), ("W_forced", out["W_scale"])):
    ns["W_SCALE"] = sc
    out[tag]["burn"] = {}
    for paux in (0.0, 50.0):
        Tb = burn(5.06e20, paux, 9.0)
        rec = None
        if Tb:
            sb = state(Tb, 5.06e20, paux, 9.0, 0.92)
            rec = {"T_burn": Tb, "p_fus": sb["p_fus"], "wall_proxy": ns["WALL_K"] * sb["p_fus"], "beta": sb["beta"]}
        out[tag]["burn"][f"paux_{paux:.0f}"] = rec
        print(f"  {tag:11s} paux {paux:3.0f}: " + ("no burn" if rec is None else f"T_burn {rec['T_burn']:.2f} keV p_fus {rec['p_fus']:.0f} wall-proxy {rec['wall_proxy']:.2f} beta {rec['beta']*100:.2f}%"))
(HERE / "op_solve_counterfactual.json").write_text(json.dumps(out, indent=1) + "\n")
