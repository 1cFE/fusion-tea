"""Window scan for `20260901-sustainment-fence` (runbook step 7): the independent
oracle over the candidate ranges, before the window is fixed. Deposits
results/window_scan.json — per-edge fence flips and the predicted structure the
grid must keep in frame. Oracle exceptions (fail-loud ash chain) are recorded."""
from __future__ import annotations
import json, sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
sys.path.insert(0, str(HERE))
import oracle_entry as oe  # noqa: E402
from study import point, I_VALUES, NE_VALUES, T_VALUES, PIN_VALUES, BASE, P  # noqa: E402

BOUNDS = dict(beta=0.05, wall=4.05, B_max=24.9, sigma=800e6, rec=0.5)

def probe(pt):
    try:
        ch = oe.evaluate(pt)
        pr = {k.split("__")[-1]: v for k, v in ch.items()}
        req = ch[f"{P}sustain__p_aux_required"]
        out = dict(
            ok=True,
            sustainment=req <= pt[f"{P}p_input"],
            p_aux_required=req,
            beta=ch[f"{P}beta_calc__beta"] <= BOUNDS["beta"],
            wall=ch[f"{P}wall_load_calc__wall_load"] <= BOUNDS["wall"],
            ceiling=ch[f"{P}peak_field_calc__B_peak"] <= BOUNDS["B_max"],
            stress=ch[f"{P}wp_stress__sigma_wp"] <= BOUNDS["sigma"],
            p_net=ch[f"{P}pb__p_net"],
            lcoe=ch[f"{P}lcoe_calc__lcoe"],
        )
        return out
    except Exception as exc:
        return dict(ok=False, error=f"{type(exc).__name__}: {exc}")

def flips(seq, key):
    prev=None; out=[]
    for label, st in seq:
        cur = st.get(key) if st.get("ok") else None
        if prev is not None and cur is not None and cur != prev[1]:
            out.append({key: f"{prev[0]} -> {label}"})
        if cur is not None: prev=(label,cur)
    return out

def main():
    scan = {}
    # I edge at baseline density/temperature
    seq=[(f"I={I/1e6:.0f}MA", probe(point(I, BASE["n_e0"], BASE["T_i0"], BASE["p_input"]))) for I in I_VALUES]
    scan["I_edge"] = {"points": {l: s for l, s in seq},
                     "flips": {k: flips(seq,k) for k in ("sustainment","beta","wall","ceiling","stress")}}
    # n edge at baseline I/T
    seq=[(f"ne={ne/5.06e20:.1f}x", probe(point(BASE["I_coil"], ne, BASE["T_i0"], BASE["p_input"]))) for ne in NE_VALUES]
    scan["ne_edge"] = {"points": {l: s for l, s in seq},
                      "flips": {k: flips(seq,k) for k in ("sustainment","beta","wall","ceiling","stress")}}
    # T transect
    seq=[(f"T={T:.0f}", probe(point(BASE["I_coil"], BASE["n_e0"], T, BASE["p_input"]))) for T in T_VALUES]
    scan["T_transect"] = {"points": {l: s for l, s in seq},
                          "flips": {k: flips(seq,k) for k in ("sustainment","beta","wall")}}
    # p transect
    seq=[(f"p={p:.0f}", probe(point(BASE["I_coil"], BASE["n_e0"], BASE["T_i0"], p))) for p in PIN_VALUES]
    scan["p_transect"] = {"points": {l: s for l, s in seq},
                          "flips": {k: flips(seq,k) for k in ("sustainment",)}}
    out = HERE / "results" / "window_scan.json"
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(scan, indent=1))
    # console digest
    for edge, data in scan.items():
        fl = {k: v for k, v in data["flips"].items() if v}
        errs = [l for l, s in data["points"].items() if not s.get("ok")]
        print(edge, "flips:", fl, ("errors: "+",".join(errs)) if errs else "")

if __name__ == "__main__":
    main()
