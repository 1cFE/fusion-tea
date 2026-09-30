"""Step 7: scan the declared case list with the independent oracle and record what the scan shows.

The candidate set is the declared case list (studies/cases.json), not a swept window: the scan fixes nothing, it
records per-case statuses, pass flags, rankability and near-threshold flags (contract r3 section 8: a margin within
2 % of its requirement) before any point runs. Window provenance: engineered (declared offers).

    .codex-test/run bash -c 'PYTHONPATH="$PWD" exec python <record>/oracle_scan.py'
"""
from __future__ import annotations

import hashlib
import json
import math
from collections import Counter
from pathlib import Path

from exploration.magnet_materials import oracle

RECORD = Path(__file__).resolve().parent
CASES = RECORD.parent / "cases.json"
NEAR = 0.02
STATUS_NAMES = {0: "unsupported", 1: "supported", 2: "edge", 3: "law-only"}


def near(margin: float, requirement: float) -> bool:
    return math.isfinite(margin) and abs(margin) <= NEAR * abs(requirement)


def scan_case(case: dict) -> dict:
    r = oracle.evaluate_case(case)
    row = {"case_id": case["case_id"], "labels": case["labels"], "materials": {}}
    for m in ("nb3sn", "rebco"):
        cond, area, refr, cold = r[m]["conductor"], r[m]["area"], r[m]["refrigeration"], r[m]["cold_load"]
        part = case[m]
        rule_temp = part["acceptance_rule"] == 0
        requirement = (part["T_supply"] + part["nuclear_rise"] + part["margin_rise"]) if rule_temp else part["fraction_rule"]
        row["materials"][m] = {
            "status_code": int(cond["status_code"]), "status": STATUS_NAMES[int(cond["status_code"])],
            "supported": int(cond["supported"]), "tcs_defined": int(cond["tcs_defined"]),
            "T_cs": cond["T_cs"], "operating_fraction": cond["operating_fraction"],
            "acceptance_margin": cond["acceptance_margin"], "acceptance_pass": int(cond["acceptance_pass"]),
            "fit_margin": area["fit_margin"], "fit_pass": int(area["fit_pass"]),
            "cu_margin": area["cu_margin"], "cu_pass": int(area["cu_pass"]),
            "steel_margin": area["steel_margin"], "steel_pass": int(area["steel_pass"]),
            "capacity_margin": refr["capacity_margin"], "capacity_pass": int(refr["capacity_pass"]),
            "green_extrapolated": int(refr["green_extrapolated"]),
            "all_pass": int(r[m]["all_pass"]),
            "annualized_cost": r[m]["annualized"]["annualized_cost"],
            "near_threshold": {
                "acceptance": near(cond["acceptance_margin"], requirement),
                "fit": near(area["fit_margin"], area["gross_area"]),
                "copper": near(area["cu_margin"], area["cu_required"]) if area["cu_required"] > 0 else False,
                "steel": near(area["steel_margin"], area["steel_required"]),
                "capacity": near(refr["capacity_margin"], cold["q_cold"]),
            },
        }
    row["pair"] = {k: r["pair"][k] for k in ("rankable", "pair_status", "cost_difference", "breakeven_rebco_price_per_m")}
    row["policy"] = {m: {"offer_basis": case["policy"][m]["offer_basis"],
                         "rating_list_exhausted": bool(case["policy"][m]["trace"].get("rating_list_exhausted"))}
                     for m in ("nb3sn", "rebco")}
    return row


def summarize(rows: list[dict]) -> dict:
    by = {}
    for key in ("anchor", "point_class", "pairing", "rule_family", "offer_kind", "refrigerator_kind"):
        by[key] = dict(sorted(Counter(str(r["labels"][key]) for r in rows).items()))
    by["B_peak"] = dict(sorted(Counter(f"{r['labels']['B_peak']:g}" for r in rows).items(), key=lambda kv: float(kv[0])))
    for m in ("nb3sn", "rebco"):
        mat = [r["materials"][m] for r in rows]
        by[f"{m}_status"] = dict(sorted(Counter(x["status"] for x in mat).items()))
        by[f"{m}_all_pass"] = sum(x["all_pass"] for x in mat)
        by[f"{m}_check_failures"] = {c: sum(1 for x in mat if not x[f"{c}_pass"]) for c in ("acceptance", "fit", "cu", "steel", "capacity")}
        by[f"{m}_near_threshold"] = {c: sum(1 for x in mat if x["near_threshold"][c]) for c in ("acceptance", "fit", "copper", "steel", "capacity")}
        by[f"{m}_green_extrapolated"] = sum(x["green_extrapolated"] for x in mat)
        by[f"{m}_carried_reference_offers"] = sum(1 for r in rows if r["policy"][m]["offer_basis"] == "carried-reference")
        by[f"{m}_rating_list_exhausted"] = sum(1 for r in rows if r["policy"][m]["rating_list_exhausted"])
    by["rankable_pairs"] = sum(r["pair"]["rankable"] for r in rows)
    by["rankable_by_anchor"] = dict(sorted(Counter(r["labels"]["anchor"] for r in rows if r["pair"]["rankable"]).items()))
    by["rankable_by_pairing"] = dict(sorted(Counter(r["labels"]["pairing"] for r in rows if r["pair"]["rankable"]).items()))
    by["rankable_cost_difference_sign"] = dict(Counter(
        "rebco_dearer" if r["pair"]["cost_difference"] > 0 else "nb3sn_dearer" for r in rows if r["pair"]["rankable"]))
    by["both_supported"] = sum(1 for r in rows if r["pair"]["pair_status"] != 0)
    return by


if __name__ == "__main__":
    out = RECORD / "results" / "oracle_scan.json"
    if out.exists():
        raise SystemExit("oracle scan exists; preserve evidence")
    raw = CASES.read_bytes()
    data = json.loads(raw)
    rows = [scan_case(c) for c in data["cases"]]
    document = {
        "kind": "pre-execution-oracle-scan/v1",
        "cases_file": {"path": CASES.relative_to(RECORD.parents[3]).as_posix(), "sha256": hashlib.sha256(raw).hexdigest(),
                       "n_cases": len(rows), "header": data["header"]},
        "oracle": {"path": "exploration/magnet_materials/oracle.py",
                   "sha256": hashlib.sha256((RECORD.parents[1] / "oracle.py").read_bytes()).hexdigest()},
        "near_threshold_rule": f"|margin| <= {NEAR} x requirement (contract r3 section 8)",
        "window_provenance": "engineered",
        "summary": summarize(rows),
        "cases": rows,
    }
    out.write_text(json.dumps(document, indent=1) + "\n")
    print(json.dumps(document["summary"], indent=1))
    print("wrote", out, out.stat().st_size, "bytes")
