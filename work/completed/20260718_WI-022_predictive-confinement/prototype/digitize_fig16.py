"""Digitize Fig 16 panels (Stellaris paper extraction images) and fit (1-rho^2)^alpha.

Calibration: plot box spines give x in [0,1]; y=0 at bottom spine; shape fit uses
values normalized to the curve's own peak, so y tick scale cancels.
"""
import numpy as np
from PIL import Image

IMGDIR = "knowledge/concept_research/09-qi-stellarator-hts/iter-01/sources/stellaris-design-details/images"
MPL = {  # matplotlib default cycle colors
    "blue": (31, 119, 180),
    "orange": (255, 127, 14),
    "green": (44, 160, 44),
    "red": (214, 39, 40),
}

def load(name):
    return np.asarray(Image.open(f"{IMGDIR}/{name}").convert("RGB"), dtype=float)

def find_box(a):
    """Plot box = rectangle of light-gray frame spines (nonwhite runs spanning the panel)."""
    nonwhite = (a.sum(axis=2) < 740)
    H, W = nonwhite.shape
    cols = [c for c in range(W) if nonwhite[:, c].sum() > 0.7 * H]
    rows = [r for r in range(H) if nonwhite[r, :].sum() > 0.7 * W]
    return min(cols), max(cols), min(rows), max(rows)  # x0,x1,ytop,ybot

def curve(a, color, box, tol=90):
    """Return (rho, val_pixels) tracking the curve left->right by continuity,
    so legend swatches (short horizontal runs at fixed y) are rejected."""
    x0, x1, yt, yb = box
    t = np.array(color, dtype=float)
    d = np.abs(a - t).sum(axis=2)
    xs, ys = [], []
    prev = None
    for c in range(x0 + 1, x1):
        rowsel = np.where(d[yt + 1:yb, c] < tol)[0]
        if len(rowsel) == 0:
            continue
        rows = rowsel + yt + 1
        # group contiguous runs
        runs, start = [], rows[0]
        for i in range(1, len(rows)):
            if rows[i] != rows[i - 1] + 1:
                runs.append((start, rows[i - 1])); start = rows[i]
        runs.append((start, rows[-1]))
        centers = [0.5 * (r0 + r1) for r0, r1 in runs]
        if prev is None:
            y = min(centers)  # first columns: curve is the topmost mark
        else:
            y = min(centers, key=lambda v: abs(v - prev))
            if abs(y - prev) > 12:  # jump -> probably legend; keep tracking direction
                continue
        prev = y
        xs.append(c); ys.append(y)
    if not ys:
        return None, None
    xs = np.array(xs); ys = np.array(ys, dtype=float)
    rho = (xs - x0) / (x1 - x0)
    val = (yb - ys)  # pixels above y=0 (bottom spine)
    return rho, val

def fit_alpha(rho, val, rho_max=0.85):
    """Fit val/val0 = (1-rho^2)^alpha via log-log least squares."""
    v0 = val[rho < 0.06].mean() if (rho < 0.06).any() else val.max()
    m = (rho > 0.05) & (rho < rho_max) & (val > 0.02 * v0)
    X = np.log(1 - rho[m] ** 2)
    Y = np.log(val[m] / v0)
    alpha = (X * Y).sum() / (X * X).sum()  # through-origin LSQ
    resid = Y - alpha * X
    return alpha, np.sqrt((resid ** 2).mean()), v0

import json
DUMP = {}

print("=== Temperature panel (pdf-9-1) ===")
a = load("stellaris-high-field-quasi-isodynamic-stellarator.pdf-9-1.png")
box = find_box(a)
print("box:", box)
for cname, key in [("electrons", "blue"), ("D (ion)", "orange"), ("T (ion)", "green")]:
    rho, val = curve(a, MPL[key], box)
    if rho is None or len(rho) < 15:
        print(f"{cname}: too few pixels ({0 if rho is None else len(rho)})")
        continue
    alpha, rms, v0 = fit_alpha(rho, val)
    DUMP[f"T_{key}"] = {"rho": rho.tolist(), "frac": (val / v0).tolist()}
    # sample values at rho = 0.5, 0.8 in fraction-of-peak
    for r in (0.5, 0.6, 0.8):
        sel = np.abs(rho - r) < 0.03
        if sel.any():
            print(f"  {cname}: frac(rho={r}) = {val[sel].mean()/v0:.3f}  "
                  f"[(1-r^2)^a pred a=1.2: {(1-r**2)**1.2:.3f}, a=3.0: {(1-r**2)**3.0:.3f}]")
    print(f"  {cname}: fitted alpha_T = {alpha:.2f} (rms logres {rms:.3f}, npix {len(rho)})")

print("\n=== Density panel (pdf-9-0) ===")
a = load("stellaris-high-field-quasi-isodynamic-stellarator.pdf-9-0.png")
box = find_box(a)
print("box:", box)
for cname, key in [("electrons", "blue"), ("D", "orange"), ("T", "green"), ("He4", "red")]:
    rho, val = curve(a, MPL[key], box)
    if rho is None or len(rho) < 15:
        print(f"{cname}: too few pixels ({0 if rho is None else len(rho)})")
        continue
    alpha, rms, v0 = fit_alpha(rho, val)
    DUMP[f"n_{key}"] = {"rho": rho.tolist(), "frac": (val / v0).tolist()}
    for r in (0.5, 0.8):
        sel = np.abs(rho - r) < 0.03
        if sel.any():
            print(f"  {cname}: frac(rho={r}) = {val[sel].mean()/v0:.3f}  "
                  f"[a=1.2 pred: {(1-r**2)**1.2:.3f}, a=0.35 pred: {(1-r**2)**0.35:.3f}]")
    print(f"  {cname}: fitted alpha_n = {alpha:.2f} (rms logres {rms:.3f}, npix {len(rho)})")

with open("/tmp/wi022_proto/fig16_curves.json", "w") as f:
    json.dump(DUMP, f)
print("\ncurves dumped to /tmp/wi022_proto/fig16_curves.json")
