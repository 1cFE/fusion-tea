"""One-axis edge transects at the WI-044 pin (runbook step 7, the restated-window rule; goal minor-radius T-003).
The window is inherited from `20260907-burn-control` (the 20260905 arms); WI-044 moved no physics number but made the
magnet chain see the coil bore, so the FIELD, STRESS and STRAIN edges can move: a transect point whose peak field now
exceeds the ceiling reads "field" where the committed re-read called it "ok". Anchors: the committed cheapest ten-verdict
machine c2823 (R 15.7, a 2.2, I 13 MA, T 13 keV, n 1.0x, both levels) and the design column; the same five transects,
the `a` transect extended to 3.4 on every anchor (the critique's F1: each column's top is where its own closure
stops answering -- the design column at 2.45, the c2823 column at 3.4 -- so error rows past a column's seam are witnessed, not claimed). The tenth fence is read as "burn" beside the nine, as committed. Every
row carries B_peak, W_mag, m_casing and the structure cost so a reader sees the bore's price along each edge. Deposits
results/window_edges.json. The committed edges docstrings follow, inherited verbatim:

One-axis edge transects at the WI-042 chain (runbook step 7; critique F1(a), 2026-09-05).
The committed study's windows are inherited as this restatement's object (record.md section 11),
but the committed transects (`studies/20260904-wall-and-heating/edges.py`, anchored on points
driven at the WI-037 family) no longer say which executed edge is fence-caught at the rule: the
committed anchors IGNITE at the rule. So the transects are re-read here, anchored on a point
driven at the rule (the critique's (R 15.7, a 2.2, I 13 MA, T 13 keV, n 1.0x) at both heating
levels) and on the design column, with the T transect refined below the committed window's
bottom. Deposits results/window_edges.json. Same held keys and fence reading as scan.py
(inherited verbatim; its full 14,400-candidate scan is NOT re-run -- the window is inherited)."""
from __future__ import annotations
import json, sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))
if str(HERE.parent) not in sys.path:
    sys.path.insert(0, str(HERE.parent))
import scan  # noqa: E402
ANCHORS = [
    (100.0, "driven-at-the-rule-100", dict(R=15.7, a=2.2, I=13.0e6, T=13.0, n=1.0)),
    (220.0, "driven-at-the-rule-220", dict(R=15.7, a=2.2, I=13.0e6, T=13.0, n=1.0)),
    (100.0, "design-column-100", dict(R=12.7, a=1.3, I=15.4e6, T=14.63, n=1.0)),
]
TRANSECTS = {"R": [9.7, 11.2, 12.7, 14.2, 15.7, 17.2, 18.7, 20.2],
             "a": [1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9, 2.0, 2.1, 2.2, 2.3, 2.4, 2.5, 2.6, 2.7, 2.8, 2.9, 3.0, 3.1, 3.2, 3.3, 3.4],   # critique F1: to the closure seam on each column (the design column errors past 2.4, witnessed as error rows)
             "I": [11.0e6, 12.0e6, 13.0e6, 14.0e6, 15.0e6, 16.0e6, 17.0e6, 18.0e6],
             "T": [11.0, 12.0, 12.5, 13.0, 13.5, 14.0, 14.63, 16.0, 17.0, 18.0, 20.0],
             "n": [0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.1, 1.2]}
def main():
    B = scan.bounds()
    out = {"bounds": B, "held": scan.HELD, "chain": "WI-042 (the ash on the fusion-rate profile, electrons by quasi-neutrality) at the WI-044 pin (the magnet chain sees the coil bore: eq. 39 / eq. 2.82 / eq. 56 anchored at the design point; the two-sided sustainment condition; \"burn\" in violated where p_aux_required < 0)",
           "anchors": [{"wallplug": wp, "tag": tag, **pt} for wp, tag, pt in ANCHORS], "rows": []}
    for wp, tag, base in ANCHORS:
        for axis, values in TRANSECTS.items():
            for v in values:
                pt = dict(base); pt[axis] = v
                r, err = scan.probe(scan.point(pt["R"], pt["a"], pt["I"], scan.NE0 * pt["n"], pt["T"], wp), B)
                if not err and r["p_aux"] < 0.0:
                    r["violated"] = list(r["violated"]) + ["burn"]   # the tenth fence, read here beside the nine (as committed)
                stamp = {"wallplug": wp, "anchor": tag, "axis": axis, "R": pt["R"], "a": pt["a"], "I": pt["I"],
                         "T_i0": pt["T"], "ne_mult": pt["n"]}
                out["rows"].append({**stamp, "error": err} if err else {**r, **stamp})
    (HERE / "results" / "window_edges.json").write_text(json.dumps(out, indent=1) + "\n")
    print("rows", len(out["rows"]), "errors", sum(1 for r in out["rows"] if r.get("error")))
if __name__ == "__main__":
    main()
