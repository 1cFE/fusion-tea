"""WI-057 window equivalence (2026-09-13): does the restructured package on feat/integrated reproduce feat/demo-maturation's
package point for point on the inherited window?

Adapted from the committed study `20260913-structural-decomposition` (feat/model-viz@ff6fdd76), which proved the transform on
the old base. Here: arm-entering = feat/demo-maturation@2e9d7d81 (executable bb60a997…, semantic 15ed665c…) materialized with
`git archive`; arm-restructured = the WI-057 package (cf6f6bb8… / 1459254b…); proposals keyed through the WI-057 ledger.
The retired `magnet__R0` tie of the old study is gone on both lineages (WI-051), so the proposal carries R alone.
Deposited as WI-057 evidence, not as a study record (no record.md, no checkpoint); the comparison rule and the export are the
committed study's, unchanged.

Run (repo root, seam env, PYTHONPATH = repo + teax-simkit), each arm in its own process:
    uv run python .../window_study.py <entering_root> --arm entering | --arm restructured | --export
"""
from __future__ import annotations
import csv, importlib.util, json, math, sqlite3, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent; REPO = HERE.parents[5]; STUDIES = REPO / "exploration/stellarator_e2e/studies"
sys.path.insert(0, str(STUDIES)); sys.path.insert(0, str(REPO))
import study_route as route  # the pinned lineage's route  # noqa: E402

STUDY_ID = "wi057-window-equivalence"
ARM_ENTERING = "arm-entering"; ARM_RESTRUCTURED = "arm-restructured"
LEDGER = json.loads((HERE.parent / "ledger.json").read_text())
P = "stellarator_09__stellaris__"
LCOE = f"{P}lcoe_calc__lcoe"
BY_DESIGN_VIOLATED = {"divertor_heat_ok"}   # violated at the design point by design (the design's divertor load exceeds its allowable); the feasible13 columns read the other thirteen so the baseline reads feasible; record § 4 reports both counts

# ---- the inherited window: 20260907-minor-radius arm-fence-p100, coordinates verbatim (record.md § 11 there) ----
R_GRID = [11.2, 12.7, 14.2, 15.7, 17.2]
A_GRID = [1.3, 1.5, 1.7, 1.8, 2.0, 2.2]
I_GRID = [13.0e6, 14.0e6, 15.0e6, 16.0e6, 18.0e6]
T_GRID = [13.0, 14.63, 16.0, 17.0, 18.0]
NE_GRID = [0.6, 0.7, 0.8, 0.9, 1.0]
NE0 = 5.06e20
BUILD_STACK_M = 2.25            # ANNEX § Validity masks: R > a + 2.25, applied as the committed record applied it; excludes nothing on this grid
WALLPLUG = 100.0
BASE = {"R": 12.7, "a": 1.3, "I_coil": 15.4e6, "n_e0": 5.06e20, "T_i0": 14.63}
# Held keys, every one explicit. `availability_direct` 0.0 selects the LIVE availability mode (mfe_lifecycle.sysml: 0 = the
# WI-046 calendar computes availability from core life; > 0 = held verbatim). It is the pinned baseline's own value on both
# lineages and exercises the calendar chain across the window. The committed sweep held the retired `availability` at 0.85;
# the held mode could reproduce that as `availability_direct` 0.85, and this study chose not to (record § 2). The rest are
# the committed sweep's holds.
HELD_OLD = {f"{P}availability_direct": 0.0, f"{P}discount_rate": 0.07, f"{P}magnet__j_wp": 118.8271604938272,
            f"{P}eta_source_heat": 0.50, f"{P}eta_couple_heat": 1.0, f"{P}p_delivered_direct_heat": 0.0,
            f"{P}p_coupled_direct_heat": 0.0, f"{P}tau_ratio_ash": 8.0}

def old_point(R, a, I, ne, T):
    """One proposal in the ENTERING lineage's names: every swept axis and every held key (no tie: R0 rides with R since WI-051)."""
    return {f"{P}R": R, f"{P}a": a, f"{P}magnet__I_coil": I, f"{P}n_e0": ne, f"{P}T_i0": T,
            f"{P}p_wallplug_heat": WALLPLUG, **HELD_OLD}

def to_new(point):
    """The same proposal in the restructured lineage's names, through the ledger (parameters map)."""
    m = LEDGER["parameters"]; out = {}
    for k, v in point.items():
        assert k in m, f"entry key {k} is not in the ledger"
        out[m[k]] = v
    return out

def proposals_old():
    out = []
    for R in R_GRID:
        for a in A_GRID:
            if not (R > a + BUILD_STACK_M): continue
            for I in I_GRID:
                for T in T_GRID:
                    for nf in NE_GRID:
                        out.append(old_point(R, a, I, NE0 * nf, T))
    out.append(old_point(BASE["R"], BASE["a"], BASE["I_coil"], BASE["n_e0"], BASE["T_i0"]))  # the pinned baseline
    return out

def coord(point):
    """The join key: the five swept values, read from either lineage's names."""
    inv = {v: k for k, v in LEDGER["parameters"].items()}
    old = {inv.get(k, k): v for k, v in point.items()}
    return (old[f"{P}R"], old[f"{P}a"], old[f"{P}magnet__I_coil"], old[f"{P}n_e0"], old[f"{P}T_i0"])

def host_map():
    """Entering calc-host path -> restructured calc-host path, derived from the ledger's outputs map (strip the output
    segment). Used only to read a failure's `module_or_channel` across lineages; both spellings are always reported."""
    m = {}
    for old, new in LEDGER["outputs"].items():
        m[old.rsplit("__", 1)[0]] = new.rsplit("__", 1)[0]
    m.update(LEDGER["outputs"])
    return m

def load_entering_route(entering_root: Path):
    studies = entering_root / "exploration/stellarator_e2e/studies"
    spec = importlib.util.spec_from_file_location("study_route_entering", studies / "study_route.py")
    mod = importlib.util.module_from_spec(spec)
    sys.path.insert(0, str(studies)); spec.loader.exec_module(mod)
    return mod

def arm_setup(arm, entering_root):
    if arm == ARM_ENTERING:
        return load_entering_route(entering_root), (entering_root / "exploration/stellarator_e2e/generated").resolve()
    return route, (REPO / "exploration/stellarator_e2e/generated").resolve()

def work_dir(arm):
    """The runner's working directory: the store, the evidence artifacts, the staging area and the package link. Under
    `_work/` because `**/_work/` is gitignored (the study-store convention); `results/points.csv`,
    `results/comparison_summary.json` and the verification summaries carry every value the record cites. The two arms
    of the committed record executed with this directory at `results/<arm>/` and their working files were moved here
    after execution and before the export (record § 17); a store is position-independent and reopens by content."""
    import os
    return Path(os.environ.get("WI057_WINDOW_WORK", HERE / "results")) / arm / "_work"   # the stores stay out of the evidence tree (WI057_WINDOW_WORK)

def store_path(arm):
    return work_dir(arm) / f"{STUDY_ID}-{arm}.db"

def run_arm(arm, entering_root: Path | None):
    work = work_dir(arm); work.mkdir(parents=True, exist_ok=True)
    r, pkg = arm_setup(arm, entering_root)
    props = proposals_old() if arm == ARM_ENTERING else [to_new(p) for p in proposals_old()]
    cases, db = r.run_points(f"{STUDY_ID}-{arm}", props, work, pkg, required_channels=dict(r.CHANNELS))
    done = [c for c in cases if c.state == "completed"]
    print(f"{arm}: proposed {len(props)}, completed {len(done)}, other states {len(cases) - len(done)}, store {db}")
    return cases, db

def reopen(arm, entering_root):
    """Reopen an arm's committed store without executing anything (the export runs in its own process)."""
    from simkit.study.query import StudyQuery
    from simkit.study.store import StudyStore
    r, pkg = arm_setup(arm, entering_root)
    store = StudyStore(store_path(arm))
    try: cases = StudyQuery(store, pkg).cases()
    finally: store.close()
    # `CaseView` does not carry the failure record; read it from the store's own column (store.py: cases.failure_json).
    con = sqlite3.connect(store_path(arm))
    try:
        failures = {cid: (json.loads(fj) if fj else None) for cid, fj in con.execute("SELECT candidate_id, failure_json FROM cases")}
    finally: con.close()
    return cases, failures, r, pkg

def rows_for(cases_by_arm, failures_by_arm, routes, pkgs):
    omap = LEDGER["outputs"]
    rows = {}
    for arm, cases in cases_by_arm.items():
        cat = routes[arm]._catalog_by_constraint_id(pkgs[arm])
        for c in cases:
            key = coord(dict(c.inputs))          # no guard: a case without inputs is a defect and must raise
            completed = c.state == "completed"
            ch = {(omap[k] if arm == ARM_ENTERING else k): float(v) for k, v in c.outputs.items()} if completed else {}
            vd = {cat[cid]["source_local_identity"]: st for cid, st in c.verdicts.items()} if completed else {}
            assert arm not in rows.get(key, {}), f"duplicate coordinate {key} on {arm}"
            rows.setdefault(key, {})[arm] = {"state": c.state, "channels": ch, "verdicts": vd, "case_id": c.candidate_id,
                                             "failure": failures_by_arm[arm].get(c.candidate_id)}
    return rows

def equal_value(a, b):
    return a == b or (isinstance(a, float) and isinstance(b, float) and math.isnan(a) and math.isnan(b))

def feasible(verdicts):
    """Every fence satisfied except the one violated by design on both lineages (record § 4)."""
    return all(st == "satisfied" for name, st in verdicts.items() if name not in BY_DESIGN_VIOLATED)

def compare(rows):
    hm = host_map()
    summary = {"points": len(rows), "on_both_arms": 0, "both_completed": 0, "both_failed": 0, "both_failed_identically": 0,
               "state_differences": [], "failure_differences": [], "channel_differences": [], "verdict_differences": [],
               "missing_channels": [], "channel_difference_magnitudes": {}, "identical_points": 0,
               "identity_rule": "both completed with every channel and every verdict equal, or both failed with the same phase and cause",
               "first_differing_point_order": "sorted coordinate (R, a, I_coil, n_e0, T_i0)", "feasibility_rule": f"every fence satisfied except {sorted(BY_DESIGN_VIOLATED)}"}
    csv_rows = []; sidecar = []
    for key in sorted(rows):
        e, n = rows[key].get(ARM_ENTERING), rows[key].get(ARM_RESTRUCTURED)
        if e is None or n is None:
            summary["state_differences"].append({"point": key, "entering": e and e["state"], "restructured": n and n["state"], "note": "point present on one arm only"})
            for arm, a in ((ARM_ENTERING, e), (ARM_RESTRUCTURED, n)):
                if a is not None: csv_rows.append([arm, *key, a["state"], False, "", "", "", "", "", a["channels"].get(LCOE, ""), feasible(a["verdicts"]) if a["verdicts"] else "", a["case_id"]])
            continue
        summary["on_both_arms"] += 1
        states_equal = e["state"] == n["state"]
        identical = False; ve = ""; ce = ""; ncomp = ""; first = ""; failures_equal = ""
        if not states_equal:
            summary["state_differences"].append({"point": key, "entering": e["state"], "restructured": n["state"], "entering_failure": e["failure"], "restructured_failure": n["failure"]})
        elif e["state"] == "completed":
            summary["both_completed"] += 1
            ek, nk = set(e["channels"]), set(n["channels"])
            missing = sorted(ek - nk); extra = sorted(nk - ek)
            if missing or extra: summary["missing_channels"].append({"point": key, "entering_only": missing, "restructured_only": extra})
            diffs = []
            for k in sorted(ek & nk):
                a, b = e["channels"][k], n["channels"][k]
                if not equal_value(a, b):
                    ad = abs(a - b) if all(math.isfinite(x) for x in (a, b)) else float("inf")
                    rd = ad / max(abs(a), abs(b)) if all(math.isfinite(x) for x in (a, b)) and max(abs(a), abs(b)) > 0 else (0.0 if ad == 0 else float("inf"))
                    diffs.append({"channel": k, "entering": a, "restructured": b, "abs": ad, "rel": rd})
                    mag = summary["channel_difference_magnitudes"].setdefault(k, {"points": 0, "max_abs": 0.0, "max_rel": 0.0})
                    mag["points"] += 1; mag["max_abs"] = max(mag["max_abs"], ad); mag["max_rel"] = max(mag["max_rel"], rd)
            ve = e["verdicts"] == n["verdicts"]; ce = not diffs and not missing and not extra; ncomp = len(ek & nk)
            if diffs:
                summary["channel_differences"].append({"point": key, "channels": [d["channel"] for d in diffs]}); sidecar.append({"point": key, "differences": diffs})
                first = diffs[0]["channel"]
            if not ve: summary["verdict_differences"].append({"point": key, "entering": e["verdicts"], "restructured": n["verdicts"]})
            identical = bool(ve and ce)
        else:
            summary["both_failed"] += 1
            fe, fn = e["failure"] or {}, n["failure"] or {}
            me, mn = fe.get("module_or_channel"), fn.get("module_or_channel")
            failures_equal = fe.get("phase") == fn.get("phase") and fe.get("cause") == fn.get("cause")
            rec = {"point": key, "state": e["state"], "entering": {"phase": fe.get("phase"), "cause": fe.get("cause"), "module_or_channel": me},
                   "restructured": {"phase": fn.get("phase"), "cause": fn.get("cause"), "module_or_channel": mn},
                   "module_or_channel_maps_through_ledger": (hm.get(me) == mn) if me is not None else (mn is None)}
            if failures_equal: summary["both_failed_identically"] += 1; summary.setdefault("failed_points", []).append(rec)
            else: summary["failure_differences"].append(rec)
            identical = bool(failures_equal)
        summary["identical_points"] += int(identical)
        for arm, a in ((ARM_ENTERING, e), (ARM_RESTRUCTURED, n)):
            csv_rows.append([arm, *key, a["state"], states_equal, ve, ce, ncomp, first, failures_equal,
                             a["channels"].get(LCOE, ""), feasible(a["verdicts"]) if a["verdicts"] else "", a["case_id"]])
    return summary, csv_rows, sidecar

if __name__ == "__main__":
    # Each arm runs in ITS OWN PROCESS: the stock loader imports the package under one module name, and a second
    # package of the same name in the same interpreter would read the first one's cached schema modules.
    entering_root = Path(sys.argv[1]).resolve()
    if "--arm" in sys.argv:
        run_arm(f"arm-{sys.argv[sys.argv.index('--arm') + 1]}", entering_root)
    elif "--export" in sys.argv:
        cases_by_arm, failures_by_arm, routes, pkgs = {}, {}, {}, {}
        for arm in (ARM_ENTERING, ARM_RESTRUCTURED):
            cases, failures, r, pkg = reopen(arm, entering_root)
            cases_by_arm[arm] = cases; failures_by_arm[arm] = failures; routes[arm] = r; pkgs[arm] = pkg
        rows = rows_for(cases_by_arm, failures_by_arm, routes, pkgs)
        summary, csv_rows, sidecar = compare(rows)
        with (HERE / "results" / "points.csv").open("w", newline="") as f:
            w = csv.writer(f)
            # One row per arm per point; the comparison columns (states_equal … failures_equal) describe the point and repeat
            # on both of its rows; `lcoe`, `feasible13` and `case_id` are the row's own arm's.
            w.writerow(["arm_id", "R", "a", "I_coil", "n_e0", "T_i0", "state", "states_equal", "verdicts_equal", "channels_equal",
                        "n_channels_compared", "first_differing_channel", "failures_equal", "lcoe", "feasible13", "case_id"])
            w.writerows(csv_rows)
        # Every verdict at every point on both arms, by local identity (record §§ 4, 6): the fence crossings are read from
        # this file, not from the stores.
        vnames = sorted({v for r_ in rows.values() for a in r_.values() for v in a["verdicts"]})
        with (HERE / "results" / "verdicts.csv").open("w", newline="") as f:
            w = csv.writer(f); w.writerow(["R", "a", "I_coil", "n_e0", "T_i0", "arm", "state", *vnames])
            for key in sorted(rows):
                for arm in (ARM_ENTERING, ARM_RESTRUCTURED):
                    a = rows[key].get(arm)
                    if a is not None: w.writerow([*key, arm, a["state"], *[a["verdicts"].get(v, "") for v in vnames]])
        summary["channels_in_union"] = len({k for r_ in rows.values() for a in r_.values() for k in a["channels"]})
        (HERE / "results" / "comparison_summary.json").write_text(json.dumps(summary, indent=1))
        if sidecar: (HERE / "results" / "channel_differences.json").write_text(json.dumps(sidecar, indent=1))
        print(json.dumps({k: (v if not isinstance(v, (list, dict)) else len(v)) for k, v in summary.items()}, indent=1))
    else:
        raise SystemExit("usage: study.py <entering_root> --arm entering|restructured  |  --export")
