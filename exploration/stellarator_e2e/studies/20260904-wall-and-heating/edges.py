"""One-axis edge transects through the oracle scan's best point at each heating level
(runbook step 7, second pass). The 14,400-candidate scan (scan.py) found the feasible
region; these transects extend each axis past the scanned range through the best point
so every executed window edge is either fence-caught or disclosed as not caught.
Deposits results/window_edges.json. Same held keys and fence reading as scan.py."""
from __future__ import annotations
import json, sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))
if str(HERE.parent) not in sys.path:
    sys.path.insert(0, str(HERE.parent))
import scan  # noqa: E402

BEST = {100.0: dict(R=14.2, a=1.8, I=14.0e6, T=16.0, n=0.8),
        220.0: dict(R=14.2, a=1.8, I=14.0e6, T=14.63, n=0.9)}
TRANSECTS = {"R": [9.7, 11.2, 12.7, 14.2, 15.7, 17.2, 18.7, 20.2],
             "a": [1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9, 2.0, 2.1, 2.2],
             "I": [11.0e6, 12.0e6, 13.0e6, 14.0e6, 15.0e6, 16.0e6, 17.0e6, 18.0e6],
             "T": [11.0, 12.0, 13.0, 14.63, 16.0, 17.0, 18.0, 20.0],
             "n": [0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.1, 1.2]}


def main():
    B = scan.bounds()
    out = {"bounds": B, "held": scan.HELD, "anchors": {str(k): v for k, v in BEST.items()}, "rows": []}
    for wp, base in BEST.items():
        for axis, values in TRANSECTS.items():
            for v in values:
                pt = dict(base); pt[axis] = v
                r, err = scan.probe(scan.point(pt["R"], pt["a"], pt["I"], scan.NE0 * pt["n"], pt["T"], wp), B)
                stamp = {"wallplug": wp, "axis": axis, "R": pt["R"], "a": pt["a"], "I": pt["I"],
                         "T_i0": pt["T"], "ne_mult": pt["n"]}
                out["rows"].append({**stamp, "error": err} if err else {**r, **stamp})
    (HERE / "results" / "window_edges.json").write_text(json.dumps(out, indent=1) + "\n")
    print("rows", len(out["rows"]), "errors", sum(1 for r in out["rows"] if r.get("error")))


if __name__ == "__main__":
    main()
