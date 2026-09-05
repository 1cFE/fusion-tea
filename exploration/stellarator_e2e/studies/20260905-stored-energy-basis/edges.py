"""One-axis edge transects at the WI-042 chain (runbook step 7; critique F1(a), 2026-09-05).
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
             "a": [1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9, 2.0, 2.1, 2.2, 2.4],
             "I": [11.0e6, 12.0e6, 13.0e6, 14.0e6, 15.0e6, 16.0e6, 17.0e6, 18.0e6],
             "T": [11.0, 12.0, 12.5, 13.0, 13.5, 14.0, 14.63, 16.0, 17.0, 18.0, 20.0],
             "n": [0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.1, 1.2]}
def main():
    B = scan.bounds()
    out = {"bounds": B, "held": scan.HELD, "chain": "WI-042 (the ash on the fusion-rate profile, electrons by quasi-neutrality)",
           "anchors": [{"wallplug": wp, "tag": tag, **pt} for wp, tag, pt in ANCHORS], "rows": []}
    for wp, tag, base in ANCHORS:
        for axis, values in TRANSECTS.items():
            for v in values:
                pt = dict(base); pt[axis] = v
                r, err = scan.probe(scan.point(pt["R"], pt["a"], pt["I"], scan.NE0 * pt["n"], pt["T"], wp), B)
                stamp = {"wallplug": wp, "anchor": tag, "axis": axis, "R": pt["R"], "a": pt["a"], "I": pt["I"],
                         "T_i0": pt["T"], "ne_mult": pt["n"]}
                out["rows"].append({**stamp, "error": err} if err else {**r, **stamp})
    (HERE / "results" / "window_edges.json").write_text(json.dumps(out, indent=1) + "\n")
    print("rows", len(out["rows"]), "errors", sum(1 for r in out["rows"] if r.get("error")))
if __name__ == "__main__":
    main()
