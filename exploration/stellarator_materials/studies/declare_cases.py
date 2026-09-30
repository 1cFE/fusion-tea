"""Declare every WI-100 Round 2 study case and write cases.json next to this file.

Run from the repository root (about an hour on ten workers; order 10^4 oracle evaluations):
    .codex-test/run python exploration/stellarator_materials/studies/declare_cases.py [--workers N]
        [--cache-dir DIR]

The grid is contract r4 section 5 (work/orchestration/goals/magnet-material-comparison/evidence/
plant-contract.md) as the offer policy (offer_policy.py) realizes it; policy-notes.md states every rule:
  - first pass: 9 cells (geometry anchored / helias / arm x f_ren 1.0 / 1.4 / 1.8) x 7 sizes x
    (Nb3Sn 10, 11, 12, 13 T; REBCO equal duty 10, 11, 12 T on the Nb3Sn design's turns; REBCO 18,
    20, 22, 24.9 T), each with its ignited companion where one exists;
  - MR-7 offers: insufficient floor(0.9 n) and generous ceil(1.2 n) element counts on the
    reference-cell (anchored x 1.0) designs at the reference size and the HELIAS 5-B size;
  - re-evaluation variants on recorded designs: every REBCO design at 30 and 10 USD/m; every design
    under the CPI 2021->2026 scalar; the anchored-cell Nb3Sn designs at 5.4 and 13.5 USD/m;
  - design variants, placed from the first pass: strain -0.6 % (Nb3Sn, anchored cells), common-P
    (REBCO, arm cells), k_link 0.95 and 86 kA turn current (both materials, HELIAS cells), each at the
    field of the cell's first-pass best design of the affected material, over the seven sizes;
  - structure-mass x0.5 / x2 on the two cells whose best designs differ most in W_mag, purchase
    exponent 0.5 / 1.0 on the cell whose best designs' re-supplied package purchases differ most.
Every case stores every supplied input of its material prefix, so the study evaluates it without the
policy; the unselected prefix is the manifest baseline point (design D4), declared once in the header.
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import math
import multiprocessing as mp
import sys
import time
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
_spec = importlib.util.spec_from_file_location("stellarator_materials_offer_policy", HERE / "offer_policy.py")
op = importlib.util.module_from_spec(_spec)
sys.modules["stellarator_materials_offer_policy"] = op
_spec.loader.exec_module(op)
og = op.og

OUT = HERE / "cases.json"
CELLS = tuple((g, f) for g in op.GEOMETRIES for f in op.F_REN_CELLS)
REFERENCE_CELL = ("anchored", 1.0)
MR7_SIZES = (op.REFERENCE_SIZE, op.HELIAS_SIZE)
DESIGN_VARIANT_PLACEMENT = {  # variant -> (geometry, affected materials)
    "strain_-0.6": ("anchored", ("nb3sn",)),
    "common-P": ("arm", ("rebco",)),
    "k_link_0.95": ("helias", ("nb3sn", "rebco")),
    "turn_current_86kA": ("helias", ("nb3sn", "rebco")),
}
RANKED_STATUS = "supported"


# ---------------------------------------------------------------------------------------------
# Records -> cases
# ---------------------------------------------------------------------------------------------
def _labels(geometry, f_ren, material, B, size, rec, variant):
    price = rec["design"]["magnet__element_price_per_m"] if rec.get("design") else None
    return dict(cell_geometry=geometry, cell_f_ren=f_ren, material=material, B_peak_target=B, R=size[0],
                a=size[1], T_i0_ladder=rec.get("T_i0_ladder"), offer_kind=rec["offer_kind"], variant=variant,
                price_rebco=price if material == "rebco" else op.PRICE_REBCO,
                price_nb3sn=price if material == "nb3sn" else op.PRICE_NB3SN,
                equal_duty=bool(material == "rebco" and B in op.REBCO_EQUAL_DUTY_FIELDS))


def _case_id(lb):
    return (f"{lb['cell_geometry']}-{lb['cell_f_ren']:g}-{lb['material']}-{lb['B_peak_target']:g}T-"
            f"R{lb['R']:g}-a{lb['a']:g}-{lb['offer_kind']}-{lb['variant']}")


def _case(geometry, f_ren, material, B, size, rec, variant, grid_point):
    lb = _labels(geometry, f_ren, material, B, size, rec, variant)
    exp = rec.get("expected") or {}
    lb["expected"] = dict(p_fus=exp.get("p_fus"), p_aux_required=exp.get("p_aux_required"), beta=exp.get("beta"),
                          B_peak=exp.get("B_peak"), status_expected=rec["status_expected"])
    prefix = og.MATERIAL_PREFIXES[material]
    inputs = {prefix + k: v for k, v in sorted((rec.get("design") or {}).items())}
    return dict(case_id=_case_id(lb), grid_point=grid_point, labels=lb, inputs=inputs,
                unselected=dict(prefix=og.MATERIAL_PREFIXES["rebco" if material == "nb3sn" else "nb3sn"],
                                baseline="header.baseline_points." + ("rebco" if material == "nb3sn" else "nb3sn")),
                status_expected=rec["status_expected"], reasons=rec.get("reasons", []),
                flags=rec.get("flags"), expected=exp,
                policy=dict(trace=rec.get("trace"), evaluations=rec.get("evaluations"),
                            plasma_solves=rec.get("plasma_solves"), B_peak_target_error=rec.get("B_peak_target_error"),
                            power_short=rec.get("power_short"), n_reference=rec.get("n_reference"),
                            base_case=rec.get("base_case")))


# ---------------------------------------------------------------------------------------------
# Worker tasks
# ---------------------------------------------------------------------------------------------
def _reeval_variants(geometry, material, variant):
    if variant != "none":
        return ("price_30", "price_10") if material == "rebco" else ()
    out = ["cpi_2021_2026"]
    if material == "rebco":
        out += ["price_30", "price_10"]
    elif geometry == "anchored":
        out += ["nb3sn_price_5.4", "nb3sn_price_13.5"]
    return tuple(out)


def _policy_digest():
    return _sha(HERE / "offer_policy.py")


def _emit(geometry, f_ren, material, B, size, rec, variant, gp, mr7, ev):
    """A design record's case plus its re-evaluation and MR-7 cases."""
    case = _case(geometry, f_ren, material, B, size, rec, variant, gp)
    out = [case]
    if not rec.get("expected"):
        return out
    for rv in _reeval_variants(geometry, material, variant):
        rr = op.reevaluate(rec, rv, material, ev)
        rr["base_case"] = case["case_id"]
        c2 = _case(geometry, f_ren, material, B, size, rr, variant if variant != "none" else rv, gp)
        if variant != "none":
            c2["labels"]["variant"] = f"{variant}+{rv}"
            c2["case_id"] = _case_id(c2["labels"])
        out.append(c2)
    if mr7 and rec["offer_kind"] == "reference":
        for kind in ("insufficient", "generous"):
            rm = op.mr7_offer(rec, kind, material, ev)
            rm["base_case"] = case["case_id"]
            out.append(_case(geometry, f_ren, material, B, size, rm, variant, gp))
    return out


def run_point(task: dict) -> dict:
    """One (cell, size, variant) grid point: its designs, companions, re-evaluations and MR-7 offers."""
    t0 = time.time()
    geometry, f_ren, size, variant = task["geometry"], task["f_ren"], tuple(task["size"]), task["variant"]
    ev = op.Evaluator()
    misses0 = op.MEMO_STATS["misses"]
    cases = []
    nb3sn_turns = dict(task.get("nb3sn_turns", {}))
    with op.sustainment_cache():
        for material, B, mode in task["designs"]:
            gp = f"{geometry}-{f_ren:g}-{material}-{B:g}T-R{size[0]:g}-a{size[1]:g}-{variant}"
            fixed = None
            if mode == "equal_duty":
                fixed = nb3sn_turns.get(str(B))
                if fixed is None:
                    rec = dict(offer_kind="reference", status_expected="unsupported", design=None,
                               reasons=["no Nb3Sn design at this field to share ampere-turns with"])
                    cases.append(_case(geometry, f_ren, material, B, size, rec, variant, gp))
                    continue
            try:
                recs = op.propose_design(material, geometry, f_ren, size, B, variant, fixed_turns=fixed, evaluate=ev)
            except Exception as exc:  # a policy defect: record it loudly, never drop the point
                recs = [dict(offer_kind="reference", status_expected="unsupported", design=None,
                             reasons=[f"policy exception {type(exc).__name__}: {exc}"])]
            for rec in recs:
                if material == "nb3sn" and rec["offer_kind"] == "reference" and rec.get("design"):
                    nb3sn_turns[str(B)] = int(rec["design"]["magnet__coil__reference_turns"])
                cases += _emit(geometry, f_ren, material, B, size, rec, variant, gp, task.get("mr7"), ev)
        for rv, targets in task.get("reevaluations", {}).items():
            for base in targets:
                rec = _record_from_case(base)
                rr = op.reevaluate(rec, rv, base["labels"]["material"], ev)
                rr["base_case"] = base["case_id"]
                lb = base["labels"]
                cases.append(_case(lb["cell_geometry"], lb["cell_f_ren"], lb["material"], lb["B_peak_target"],
                                   (lb["R"], lb["a"]), rr, rv, base["grid_point"]))
    return dict(task_id=task["task_id"], task=task, cases=cases, evaluations=ev.count,
                plasma_solves=op.MEMO_STATS["misses"] - misses0, seconds=time.time() - t0,
                nb3sn_turns=nb3sn_turns, policy_sha256=_policy_digest())


def refresh_point(res: dict) -> dict:
    """Re-run the re-supply fixed point on every recorded design of a result produced by an earlier
    policy digest whose magnet and operating-point rules are unchanged, and regenerate its derived cases.

    Valid because re-supply (structure, heating, cryo, packages, classes, facilities, schedule) feeds no
    quantity the magnet sizing or the operating-point search reads (they read B_peak, conductor, fit
    and plasma channels only). Used once in this run, for the facility campus-clearance amendment (Q12).
    """
    t0 = time.time()
    ev = op.Evaluator()
    misses0 = op.MEMO_STATS["misses"]
    task_id = res["task_id"]
    parts = task_id.split("-")
    out = []
    with op.sustainment_cache():
        for c in res["cases"]:
            if c["policy"].get("base_case") is not None:
                continue  # derived cases are regenerated below
            lb = c["labels"]
            if not c.get("expected"):
                out.append(c)
                continue
            rec0 = _record_from_case(c)
            m = lb["material"]
            e0 = ev.count
            final, case, rtrace = op._converge_resupply(ev, m, rec0["design"])
            trace = dict(c["policy"]["trace"] or {}, **rtrace, refreshed=True)
            kind = "ignited" if (trace.get("operating_point") == "ignited" and lb["offer_kind"] == "reference") \
                else "reference"
            status, reasons = op.status_of(m, case, kind, rtrace)
            if kind == "ignited" and status == "ignited":
                reasons = c["reasons"]
            rec = dict(offer_kind=lb["offer_kind"], design=final, T_i0_ladder=lb["T_i0_ladder"],
                       power_short=c["policy"]["power_short"], status_expected=status, reasons=reasons, trace=trace,
                       evaluations=(c["policy"]["evaluations"] or 0) + (ev.count - e0),
                       plasma_solves=c["policy"]["plasma_solves"])
            if "refusal" not in case:
                rec["expected"] = op.expectations(case)
                rec["flags"] = op.flags_of(m, case, final, rec["power_short"])
                rec["B_peak_target_error"] = case["channels"]["magnet__peak_field_calc__B_peak"] - lb["B_peak_target"]
            variant = lb["variant"]
            mr7 = (lb["cell_geometry"], lb["cell_f_ren"]) == REFERENCE_CELL and (lb["R"], lb["a"]) in MR7_SIZES \
                and variant == "none"
            out += _emit(lb["cell_geometry"], lb["cell_f_ren"], m, lb["B_peak_target"], (lb["R"], lb["a"]), rec,
                         variant, c["grid_point"], mr7, ev)
    new = dict(res, cases=out, evaluations=res["evaluations"] + ev.count,
               plasma_solves=res["plasma_solves"] + op.MEMO_STATS["misses"] - misses0,
               seconds=res["seconds"] + time.time() - t0, policy_sha256=_policy_digest(),
               refreshed_from=res.get("policy_sha256", "pre-digest"))
    return new


def _record_from_case(case):
    prefix = og.MATERIAL_PREFIXES[case["labels"]["material"]]
    design = {k[len(prefix):]: v for k, v in case["inputs"].items()}
    return dict(offer_kind=case["labels"]["offer_kind"], design=design, T_i0_ladder=case["labels"]["T_i0_ladder"],
                power_short=case["policy"]["power_short"], case_id=case["case_id"])


def _designs_for(nb3sn_fields, rebco_ed_fields, rebco_own_fields):
    out = [("nb3sn", B, "own") for B in nb3sn_fields]
    out += [("rebco", B, "equal_duty") for B in rebco_ed_fields]
    out += [("rebco", B, "own") for B in rebco_own_fields]
    return out


def first_pass_tasks():
    tasks = []
    for geometry, f_ren in CELLS:
        for size in op.SIZES:
            tasks.append(dict(task_id=f"p1-{geometry}-{f_ren:g}-R{size[0]:g}-a{size[1]:g}", geometry=geometry,
                              f_ren=f_ren, size=list(size), variant="none",
                              designs=_designs_for(op.NB3SN_FIELDS, op.REBCO_EQUAL_DUTY_FIELDS, op.REBCO_OWN_FIELDS),
                              mr7=(geometry, f_ren) == REFERENCE_CELL and tuple(size) in MR7_SIZES))
    # the heaviest (strong confinement, ash-limited) first, for balance
    tasks.sort(key=lambda t: (-t["f_ren"], t["size"][0]))
    return tasks


# ---------------------------------------------------------------------------------------------
# Placement after the first pass (contract section 5 F13; notes Q14)
# ---------------------------------------------------------------------------------------------
def _is_design(case):
    return case["labels"]["variant"] == "none" and case["labels"]["offer_kind"] in ("reference", "companion")


def best_designs(cases, geometry, f_ren, material, variant="none"):
    """Lowest-LCOE supported design of a material in a cell (REBCO 80, Nb3Sn 8 USD/m); if none is
    supported, the nearest: the lowest-LCOE failed or capacity-limited design with positive p_net."""
    pool = [c for c in cases if c["labels"]["cell_geometry"] == geometry and c["labels"]["cell_f_ren"] == f_ren
            and c["labels"]["material"] == material and c["labels"]["variant"] == variant
            and c["labels"]["offer_kind"] in ("reference", "companion") and c.get("expected")]
    sup = [c for c in pool if c["status_expected"] == RANKED_STATUS]
    if sup:
        return min(sup, key=lambda c: c["expected"]["channels"]["lcoe_calc__lcoe"]), True
    near = [c for c in pool if c["status_expected"] in ("failed", "capacity-limited")
            and c["expected"]["channels"]["pb__p_net"] > 0.0]
    if near:
        return min(near, key=lambda c: c["expected"]["channels"]["lcoe_calc__lcoe"]), False
    return None, False


def _package_purchase(case):
    prefix = og.MATERIAL_PREFIXES[case["labels"]["material"]]
    return sum(case["inputs"][prefix + p] for p, r in op.PURCHASES.values())


def placements(cases):
    rows = {}
    for geometry, f_ren in CELLS:
        rb, rs = best_designs(cases, geometry, f_ren, "rebco")
        nb, ns = best_designs(cases, geometry, f_ren, "nb3sn")
        rows[(geometry, f_ren)] = dict(rebco=rb, nb3sn=nb, both_supported=rs and ns)
    def ranked(metric):
        full = [(k, v) for k, v in rows.items() if v["rebco"] and v["nb3sn"]]
        full.sort(key=lambda kv: (not kv[1]["both_supported"], -metric(kv[1])))
        return full
    wmag = lambda v: abs(v["rebco"]["expected"]["channels"]["magnet__stored_energy__W_mag"]
                         - v["nb3sn"]["expected"]["channels"]["magnet__stored_energy__W_mag"])  # noqa: E731
    pkg = lambda v: abs(_package_purchase(v["rebco"]) - _package_purchase(v["nb3sn"]))  # noqa: E731
    structure_cells = ranked(wmag)[:2]
    exponent_cells = ranked(pkg)[:1]
    return rows, structure_cells, exponent_cells


def variant_tasks(cases, rows):
    """Design variants at the field of each placement cell's first-pass best design, seven sizes."""
    tasks = []
    for variant, (geometry, materials) in DESIGN_VARIANT_PLACEMENT.items():
        for f_ren in op.F_REN_CELLS:
            row = rows[(geometry, f_ren)]
            nb_f, rb_ed, rb_own = set(), set(), set()
            for m in materials:
                best = row[m]
                if best is None:
                    continue
                B = best["labels"]["B_peak_target"]
                if m == "nb3sn":
                    nb_f.add(B)
                elif B in op.REBCO_EQUAL_DUTY_FIELDS:
                    rb_ed.add(B)
                    if variant != "common-P":
                        nb_f.add(B)  # the equal-duty pair needs the variant Nb3Sn turns
                else:
                    rb_own.add(B)
            if not (nb_f or rb_ed or rb_own):
                continue
            for size in op.SIZES:
                turns = {}
                if variant == "common-P" and rb_ed:  # Nb3Sn is unaffected: its first-pass turns
                    for c in cases:
                        lb = c["labels"]
                        if (lb["cell_geometry"], lb["cell_f_ren"], lb["material"], lb["R"], lb["a"]) == \
                                (geometry, f_ren, "nb3sn", size[0], size[1]) and _is_design(c) \
                                and lb["offer_kind"] == "reference" and c["inputs"]:
                            turns[str(lb["B_peak_target"])] = int(c["inputs"][og.MATERIAL_PREFIXES["nb3sn"]
                                                                              + "magnet__coil__reference_turns"])
                fields = ("n" + ",".join(f"{B:g}" for B in sorted(nb_f)) + "-re" + ",".join(f"{B:g}" for B in sorted(rb_ed))
                          + "-ro" + ",".join(f"{B:g}" for B in sorted(rb_own)))
                tasks.append(dict(task_id=f"p2-{variant}-{geometry}-{f_ren:g}-R{size[0]:g}-a{size[1]:g}-{fields}",
                                  geometry=geometry, f_ren=f_ren, size=list(size), variant=variant,
                                  designs=_designs_for(sorted(nb_f), sorted(rb_ed), sorted(rb_own)),
                                  nb3sn_turns=turns))
    return tasks


def reevaluation_task(structure_cells, exponent_cells, rows):
    targets = {}
    for (geometry, f_ren), row in structure_cells:
        for m in ("rebco", "nb3sn"):
            for v in op.STRUCTURE_VARIANTS:
                targets.setdefault(v, []).append(row[m])
    for (geometry, f_ren), row in exponent_cells:
        for m in ("rebco", "nb3sn"):
            for v in ("purchase_exp_0.5", "purchase_exp_1.0"):
                targets.setdefault(v, []).append(row[m])
    key = hashlib.sha256(json.dumps({v: [c["case_id"] for c in cs] for v, cs in sorted(targets.items())},
                                    sort_keys=True).encode()).hexdigest()[:12]
    return dict(task_id=f"p2-reevaluations-{key}", geometry="-", f_ren=0.0, size=[0, 0], variant="none", designs=[],
                reevaluations=targets)


# ---------------------------------------------------------------------------------------------
# Baseline points (design D4, section 2.10, A6, K22) and output
# ---------------------------------------------------------------------------------------------
INTERFACE_PATH = HERE / "interface_data.py"


def baseline_points(cases):
    """The unselected prefix of every case is the manifest baseline point (design D4, section 5.3).

    It is the package's own point (exploration/stellarator_materials/studies/interface_data.py,
    INTERFACE['units'][material]['baseline_point']), which the route fills and witnesses bit for bit.
    This policy does not restate its values (the brief bars reading them); it names it, and names the
    policy-recorded Nb3Sn design that evaluates without refusal as the K22 fallback default.
    """
    nb = next((c for c in cases if _is_design(c) and c["labels"]["material"] == "nb3sn"
               and c["labels"]["cell_geometry"] == "anchored" and c["labels"]["cell_f_ren"] == 1.0
               and c["labels"]["B_peak_target"] == 12.0 and (c["labels"]["R"], c["labels"]["a"]) == op.REFERENCE_SIZE
               and c["labels"]["offer_kind"] == "reference"), None)
    ref = dict(path=str(INTERFACE_PATH.relative_to(op.ROOT)),
               sha256=_sha(INTERFACE_PATH) if INTERFACE_PATH.exists() else None)
    return dict(
        nb3sn=dict(source=ref, key="INTERFACE['units']['nb3sn']['baseline_point']",
                   k22_candidate=nb["case_id"] if nb else None,
                   k22_candidate_status=nb["status_expected"] if nb else None),
        rebco=dict(source=ref, key="INTERFACE['units']['rebco']['baseline_point']"),
        note="design D4: the route completes each case with this point for the prefix the case does not vary")


def normalize_inputs(case):
    """Every key the oracle resolves for this case that the policy supplies, that is a material or
    cryo fact, or whose value differs from the pin: the case is then evaluable from its own inputs
    whatever the package defaults are (held plant keys at the pin are named by the header)."""
    material = case["labels"]["material"]
    prefix = og.MATERIAL_PREFIXES[material]
    supplied = {k[len(prefix):]: v for k, v in case["inputs"].items()}
    if not supplied:
        return case
    resolved, provenance = og.resolve_material_inputs(supplied, material)
    out = {}
    for k, v in resolved.items():
        if k in supplied or k not in op.PIN or v != op.PIN[k] or provenance.get(k) == "design default":
            out[prefix + k] = v
    case["inputs"] = dict(sorted(out.items()))
    return case


def counts(cases):
    by = {}
    for key in ("cell_geometry", "cell_f_ren", "material", "B_peak_target", "offer_kind", "variant", "T_i0_ladder",
                "price_rebco", "price_nb3sn"):
        by[key] = dict(sorted(Counter(str(c["labels"][key]) for c in cases).items()))
    by["status_expected"] = dict(sorted(Counter(c["status_expected"] for c in cases).items()))
    by["size"] = dict(sorted(Counter(f"R{c['labels']['R']:g}-a{c['labels']['a']:g}" for c in cases).items()))
    designs = [c for c in cases if c["labels"]["offer_kind"] in ("reference", "companion")
               and "+" not in c["labels"]["variant"] and c["labels"]["variant"] not in op.REEVALUATION_VARIANTS]
    by["recorded_designs"] = len(designs)
    by["recorded_designs_by_status"] = dict(sorted(Counter(c["status_expected"] for c in designs).items()))
    by["recorded_designs_by_variant"] = dict(sorted(Counter(c["labels"]["variant"] for c in designs).items()))
    by["recorded_designs_by_offer_kind"] = dict(sorted(Counter(c["labels"]["offer_kind"] for c in designs).items()))
    by["first_pass_grid_points"] = len({c["grid_point"] for c in cases if c["labels"]["variant"] == "none"
                                        and c["labels"]["offer_kind"] == "reference"})
    return by


def write(cases, header):
    ids = [c["case_id"] for c in cases]
    dup = [k for k, n in Counter(ids).items() if n > 1]
    if dup:
        raise RuntimeError(f"duplicate case ids: {dup[:5]}")
    lines = ["{", f' "header": {json.dumps(header, sort_keys=True)},', ' "cases": [']
    for i, c in enumerate(cases):
        lines.append("  " + json.dumps(c, sort_keys=False) + ("," if i < len(cases) - 1 else ""))
    lines += [" ]", "}"]
    OUT.write_text("\n".join(lines) + "\n")


def _sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def _run(tasks, workers, cache_dir, refreshable=False):
    """Run tasks, reusing cached results. A cached result from an earlier policy digest is refreshed
    (re-supply only, `refresh_point`) when `refreshable`, else re-run."""
    done, todo, stale = [], [], []
    digest = _policy_digest()
    for t in tasks:
        f = cache_dir / f"{t['task_id']}.json" if cache_dir else None
        if f and f.exists():
            res = json.loads(f.read_text())
            if res.get("policy_sha256") == digest:
                done.append(res)
            elif refreshable:
                stale.append(res)
            else:
                todo.append(t)
        else:
            todo.append(t)
    if stale:
        ctx = mp.get_context("fork")
        with ctx.Pool(workers) as pool:
            for res in pool.imap_unordered(refresh_point, stale):
                if cache_dir:
                    (cache_dir / f"{res['task_id']}.json").write_text(json.dumps(res))
                done.append(res)
                print(f"  refreshed {res['task_id']}", flush=True)
    if todo:
        ctx = mp.get_context("fork")
        with ctx.Pool(workers) as pool:
            for res in pool.imap_unordered(run_point, todo):
                if cache_dir:
                    (cache_dir / f"{res['task_id']}.json").write_text(json.dumps(res))
                done.append(res)
                print(f"  {res['task_id']}: {len(res['cases'])} cases, {res['evaluations']} evals, "
                      f"{res['seconds']:.0f} s", flush=True)
    return done


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--workers", type=int, default=10)
    ap.add_argument("--cache-dir", type=Path, default=None, help="resume store for per-task results")
    args = ap.parse_args(argv)
    if args.cache_dir:
        args.cache_dir.mkdir(parents=True, exist_ok=True)
    t0 = time.time()
    p1 = _run(first_pass_tasks(), args.workers, args.cache_dir, refreshable=True)
    cases = [c for r in p1 for c in r["cases"]]
    rows, structure_cells, exponent_cells = placements(cases)
    p2_tasks = variant_tasks(cases, rows) + [reevaluation_task(structure_cells, exponent_cells, rows)]
    p2 = _run(p2_tasks, args.workers, args.cache_dir)
    cases += [c for r in p2 for c in r["cases"]]
    cases = [normalize_inputs(c) for c in cases]
    cases.sort(key=lambda c: c["case_id"])
    evaluations = dict(first_pass=sum(r["evaluations"] for r in p1), second_pass=sum(r["evaluations"] for r in p2),
                       first_pass_plasma_solves=sum(r["plasma_solves"] for r in p1),
                       second_pass_plasma_solves=sum(r["plasma_solves"] for r in p2))
    evaluations["total"] = evaluations["first_pass"] + evaluations["second_pass"]
    placement = dict(
        structure_mass_cells=[dict(cell=list(k), both_supported=v["both_supported"],
                                   rebco=v["rebco"]["case_id"], nb3sn=v["nb3sn"]["case_id"]) for k, v in structure_cells],
        purchase_exponent_cells=[dict(cell=list(k), both_supported=v["both_supported"],
                                      rebco=v["rebco"]["case_id"], nb3sn=v["nb3sn"]["case_id"]) for k, v in exponent_cells],
        first_pass_best={f"{k[0]}-{k[1]:g}": dict(rebco=v["rebco"]["case_id"] if v["rebco"] else None,
                                                  nb3sn=v["nb3sn"]["case_id"] if v["nb3sn"] else None,
                                                  both_supported=v["both_supported"]) for k, v in rows.items()})
    header = dict(
        schema="wi100-cases-v1",
        generated_by="exploration/stellarator_materials/studies/declare_cases.py",
        policy="exploration/stellarator_materials/studies/offer_policy.py",
        oracle="exploration/stellarator_materials/oracle_glue.py",
        oracle_sha256=_sha(op.ORACLE_PATH), policy_sha256=_sha(HERE / "offer_policy.py"),
        contract="work/orchestration/goals/magnet-material-comparison/evidence/plant-contract.md (r4) section 5",
        design="work/active/WI-100_stellarator-material-variants/design.md sections 4, 5.1, 5.2, 9 (A1-A8)",
        notes="exploration/stellarator_materials/studies/policy-notes.md",
        layout=("each case: case_id, grid_point, labels (incl. expected p_fus, p_aux_required, beta, B_peak, "
                "status_expected), inputs (every supplied key of the selected material prefix; held plant keys not "
                "listed take the pin value, oracle_glue.PIN_INPUTS_PATH), unselected (the baseline point, header), "
                "status_expected, reasons, flags, expected (policy's recorded channels), policy (trace, not an input)"),
        held_inputs=dict(path=str(og.PIN_INPUTS_PATH.relative_to(op.ROOT)), sha256=_sha(og.PIN_INPUTS_PATH)),
        p_fus_match=op.P_FUS_MATCH, tolerances=dict(p_fus_rel=op.TOL_P_FUS, B_peak_T=op.TOL_B_PEAK,
                                                     beta_fallback_fraction=op.BETA_FALLBACK_FRACTION),
        baseline_points=baseline_points(cases), placement=placement, evaluations=evaluations,
        n_cases=len(cases), counts=counts(cases), wall_seconds=time.time() - t0)
    write(cases, header)
    print(json.dumps(dict(n_cases=len(cases), evaluations=evaluations, counts=header["counts"]), indent=1))
    print("wrote", OUT, OUT.stat().st_size, "bytes")


if __name__ == "__main__":
    main()
