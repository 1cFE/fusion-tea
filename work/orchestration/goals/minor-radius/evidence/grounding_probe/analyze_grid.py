"""Bottleneck (minimax) access paths, connectivity of the <= P_installed region, ignition contour, heat map."""
import csv, heapq, json, os, sys, math
from collections import deque
SCR = os.path.dirname(os.path.abspath(__file__))
tag = sys.argv[1]; T_target_exact = float(sys.argv[2]); T_target_grid = float(sys.argv[3])
rows = [r for r in csv.DictReader(open(os.path.join(SCR, f"access_grid_{tag}.csv")))]
def fl(x):
    return None if x in ("", None) else float(x)
grid = {}
errs = []
for r in rows:
    f = round(float(r["n_factor"]), 2); T = float(r["T"])
    if r["err"]:
        errs.append((f, T, r["err"])); continue
    grid[(f, T)] = {k: fl(r[k]) for k in ("p_aux_required", "p_fus", "W_th", "p_alpha_heat", "p_rad", "tau_E", "p_net", "n_He0")}
Fs = sorted({k[0] for k in grid}); Ts_all = sorted({k[1] for k in grid})
Ts_reg = [T for T in Ts_all if abs(T * 2 - round(T * 2)) < 1e-9]  # the regular 0.5 keV rows
def need(node):
    return max(0.0, grid[node]["p_aux_required"])
def neighbours(node, Ts, eight):
    f, T = node; fi = Fs.index(f); ti = Ts.index(T)
    for df in (-1, 0, 1):
        for dt in (-1, 0, 1):
            if df == 0 and dt == 0: continue
            if not eight and df != 0 and dt != 0: continue
            fj, tj = fi + df, ti + dt
            if 0 <= fj < len(Fs) and 0 <= tj < len(Ts):
                nb = (Fs[fj], Ts[tj])
                if nb in grid: yield nb
def minimax(starts, target, Ts, eight):
    """Dijkstra with path cost = max node need (start node included). Returns (value, path)."""
    best = {}; prev = {}; pq = []
    for s in starts:
        if s in grid:
            best[s] = need(s); prev[s] = None; heapq.heappush(pq, (best[s], s))
    done = set()
    while pq:
        c, u = heapq.heappop(pq)
        if u in done: continue
        done.add(u)
        if u == target: break
        for v in neighbours(u, Ts, eight):
            nc = max(c, need(v))
            if nc < best.get(v, math.inf):
                best[v] = nc; prev[v] = u; heapq.heappush(pq, (nc, v))
    if target not in best: return None, None
    path = []; u = target
    while u is not None: path.append(u); u = prev[u]
    return best[target], path[::-1]
def connected(level, starts, target, Ts, eight):
    """BFS through nodes with need <= level; returns shortest path (in moves) or None."""
    ok = lambda n: need(n) <= level
    q = deque(); prev = {}
    for s in starts:
        if s in grid and ok(s): prev[s] = None; q.append(s)
    while q:
        u = q.popleft()
        if u == target: break
        for v in neighbours(u, Ts, eight):
            if v not in prev and ok(v): prev[v] = u; q.append(v)
    if target not in prev: return None
    path = []; u = target
    while u is not None: path.append(u); u = prev[u]
    return path[::-1]
out = {"geom": tag, "n_grid_nodes": len(grid), "n_raised": len(errs), "raised": errs[:20], "Fs": Fs, "Ts_regular": Ts_reg,
       "exact_T_row_present": T_target_exact in Ts_all}
cold_edge = [(f, Ts_reg[0]) for f in Fs]
A_grid = (1.0, T_target_grid)
out["A_grid"] = {"node": A_grid, "p_aux_required": grid[A_grid]["p_aux_required"]}
if T_target_exact in Ts_all:
    out["A_exact"] = {"node": (1.0, T_target_exact), "p_aux_required": grid[(1.0, T_target_exact)]["p_aux_required"]}
    Ts_with_exact = sorted(set(Ts_reg) | {T_target_exact})
for label, Ts, target in (("grid_target", Ts_reg, A_grid),) + ((("exact_target", Ts_with_exact, (1.0, T_target_exact)),) if T_target_exact in Ts_all else ()):
    res = {}
    for eight in (False, True):
        k = "8nb" if eight else "4nb"
        v1, p1 = minimax([(Fs[0], Ts[0])], target, Ts, eight)
        res[f"from_cold_corner_{k}"] = {"start": (Fs[0], Ts[0]), "minimax_MW": v1, "path": p1,
                                        "path_needs": [round(need(n), 2) for n in p1] if p1 else None}
        v2, p2 = minimax(cold_edge, target, Ts, eight)
        res[f"best_start_on_cold_edge_{k}"] = {"start": p2[0] if p2 else None, "minimax_MW": v2, "path": p2,
                                               "path_needs": [round(need(n), 2) for n in p2] if p2 else None}
        per_start = {}
        for s in cold_edge:
            vs_, _ = minimax([s], target, Ts, eight); per_start[str(s[0])] = vs_
        res[f"minimax_by_start_density_{k}"] = per_start
        levels = {}
        for L in (50.0, 60.0, 75.0, 100.0, 150.0):
            p = connected(L, cold_edge, target, Ts, eight)
            levels[str(L)] = {"path_exists": p is not None, "n_moves": (len(p) - 1) if p else None, "path": p,
                              "path_needs": [round(need(n), 2) for n in p] if p else None}
        res[f"installed_levels_{k}"] = levels
        res[f"min_installed_for_a_path_{k}"] = v2
    out[label] = res
# <= 50 MW region size and the ignition contour (requirement <= 0)
le50 = [n for n in grid if need(n) <= 50.0]
out["n_nodes_le_50MW"] = len(le50)
ign = sorted([n for n in grid if grid[n]["p_aux_required"] <= 0.0])
out["n_ignited_nodes"] = len(ign)
# ignition contour: for each density, the lowest T with p_aux_required <= 0 and the range
contour = {}
for f in Fs:
    Tign = [T for T in Ts_reg if (f, T) in grid and grid[(f, T)]["p_aux_required"] <= 0.0]
    contour[str(f)] = {"T_ignited": Tign, "T_first_ignited": Tign[0] if Tign else None,
                       "min_p_aux_over_T": min((grid[(f, T)]["p_aux_required"], T) for T in Ts_reg if (f, T) in grid)}
out["ignition_contour"] = contour
# per-density ramp maximum (for the reference table)
out["ramp_max_by_density"] = {str(f): max((grid[(f, T)]["p_aux_required"], T) for T in Ts_reg if (f, T) in grid) for f in Fs}
json.dump(out, open(os.path.join(SCR, f"access_analysis_{tag}.json"), "w"), indent=1, default=str)
# plot
try:
    import numpy as np, matplotlib
    matplotlib.use("Agg"); import matplotlib.pyplot as plt
    Z = np.full((len(Fs), len(Ts_reg)), np.nan)
    for i, f in enumerate(Fs):
        for j, T in enumerate(Ts_reg):
            if (f, T) in grid: Z[i, j] = grid[(f, T)]["p_aux_required"]
    fig, ax = plt.subplots(figsize=(11, 7))
    Zc = np.clip(Z, -100, 400)
    im = ax.pcolormesh(Ts_reg, Fs, Zc, cmap="viridis", shading="nearest")
    cb = fig.colorbar(im, ax=ax); cb.set_label("p_aux_required, MW (clipped to [-100, 400])")
    Tg, Fg = np.meshgrid(Ts_reg, Fs)
    cs = ax.contour(Tg, Fg, Z, levels=[0.0], colors="white", linewidths=2); ax.clabel(cs, fmt="ignition (0 MW)")
    cs2 = ax.contour(Tg, Fg, Z, levels=[50.0], colors="orange", linewidths=2); ax.clabel(cs2, fmt="50 MW")
    ax.contourf(Tg, Fg, np.where(Z <= 50.0, 1.0, np.nan), levels=[0.5, 1.5], colors=["none"], hatches=["//"], alpha=0.0)
    g = out["grid_target"]
    p = g["best_start_on_cold_edge_8nb"]["path"]
    if p: ax.plot([n[1] for n in p], [n[0] for n in p], "r-o", ms=4, lw=2, label=f"minimax path (8-nb) max {g['best_start_on_cold_edge_8nb']['minimax_MW']:.1f} MW")
    p4 = g["from_cold_corner_4nb"]["path"]
    if p4: ax.plot([n[1] for n in p4], [n[0] for n in p4], "m--", lw=1.5, label=f"minimax from cold corner (4-nb) max {g['from_cold_corner_4nb']['minimax_MW']:.1f} MW")
    ax.plot([A_grid[1]], [A_grid[0]], "w*", ms=16, mec="k", label=f"A (n 1.00x, T {A_grid[1]})")
    ax.set_xlabel("T_i0, keV"); ax.set_ylabel("n_e0 / 5.06e20"); ax.set_title(f"Access map {tag}: steady-state heating requirement (hatched: <= 50 MW)")
    ax.legend(loc="upper left", fontsize=8)
    png = os.path.join(SCR, f"access_map_{tag}.png"); fig.savefig(png, dpi=130, bbox_inches="tight"); out["png"] = png
    json.dump(out, open(os.path.join(SCR, f"access_analysis_{tag}.json"), "w"), indent=1, default=str)
    print("png", png)
except Exception as e:
    print("plot skipped:", type(e).__name__, e)
# console summary
print(json.dumps({k: out[k] for k in ("n_grid_nodes", "n_raised", "A_grid", "n_nodes_le_50MW", "n_ignited_nodes")}, default=str))
for label in ("grid_target", "exact_target"):
    if label not in out: continue
    g = out[label]; print("==", label)
    for k in ("from_cold_corner_4nb", "from_cold_corner_8nb", "best_start_on_cold_edge_4nb", "best_start_on_cold_edge_8nb"):
        print(k, "minimax", g[k]["minimax_MW"], "start", g[k]["start"], "len", len(g[k]["path"]) if g[k]["path"] else None)
    print("by start density 8nb", g["minimax_by_start_density_8nb"])
    for L, v in g["installed_levels_8nb"].items(): print("level", L, "8nb path exists", v["path_exists"], "moves", v["n_moves"])
    for L, v in g["installed_levels_4nb"].items(): print("level", L, "4nb path exists", v["path_exists"], "moves", v["n_moves"])
print("ignition first T by density:", {f: c["T_first_ignited"] for f, c in out["ignition_contour"].items()})
print("ramp max by density:", {f: (round(v[0], 1), v[1]) for f, v in out["ramp_max_by_density"].items()})
