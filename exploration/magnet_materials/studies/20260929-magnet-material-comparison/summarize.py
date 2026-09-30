"""Tabulate the executed evidence (results/cases.json) for the record; every number here is recomputable from it.

    .codex-test/run bash -c 'PYTHONPATH="$PWD" exec python <record>/summarize.py'
"""
from __future__ import annotations

import json
import math
from collections import Counter, defaultdict
from pathlib import Path

from scripts.study import common

RECORD = Path(__file__).resolve().parent
P = "magnet_subsystem__subsystem__"
STATUS = {0: "unsupported", 1: "supported", 2: "edge", 3: "law-only"}
NEAR = 0.02


def ch(row, name):
    return row["outputs"][P + name]


def main():
    data = json.loads((RECORD / "results" / "cases.json").read_text())
    rows = data["cases"]
    catalog = json.loads((RECORD / "results" / "constraint_catalog.json").read_text())
    n = len(rows)
    labels = lambda k: dict(sorted(Counter(str(r["labels"][k]) for r in rows).items()))
    counts = {k: labels(k) for k in ("anchor", "point_class", "pairing", "rule_family", "offer_kind", "refrigerator_kind")}
    counts["B_peak"] = dict(sorted(Counter(f"{r['labels']['B_peak']:g}" for r in rows).items(), key=lambda kv: float(kv[0])))
    counts["variant"] = dict(sorted(Counter(r["labels"]["variant"] for r in rows).items()))
    counts["anchor_x_pairing"] = dict(sorted(Counter(f"{r['labels']['anchor']}|{r['labels']['pairing']}" for r in rows).items()))
    # constraint outcomes by qualified identity, over declared cases and over stored points
    verdicts = {}
    for cid, entry in catalog.items():
        declared = Counter(r["verdicts"][cid] for r in rows)
        stored = Counter(r["verdicts"][cid] for r in rows if not r["aliases"] or r["case_id"] == min([r["case_id"], *r["aliases"]]))
        verdicts[cid] = {"definition_qualified_name": entry["definition_qualified_name"],
                         "source_local_identity": entry["source_local_identity"],
                         "owner": entry["owner_instance_path"].split("__")[-1],
                         "declared_cases": dict(declared), "stored_points": dict(stored)}
    # material statuses and pass flags
    materials = {}
    for m in ("nb3sn", "rebco"):
        st = Counter(STATUS[int(ch(r, f"{m}__conductor__status_code"))] for r in rows)
        allp = sum(int(ch(r, f"{m}__all_pass__all_pass")) for r in rows)
        fails = {c: sum(1 for r in rows if not int(ch(r, f"{m}__{grp}__{c}_pass"))) for grp, c in
                 (("conductor", "acceptance"), ("area", "fit"), ("area", "cu"), ("area", "steel"), ("refrigeration", "capacity"))}
        near = {
            "acceptance": sum(1 for r in rows if abs(ch(r, f"{m}__conductor__acceptance_margin")) <= NEAR * (
                (r["inputs"][P + f"{m}__T_supply"] + r["inputs"][P + f"{m}__nuclear_rise"] + r["inputs"][P + f"{m}__margin_rise"])
                if r["inputs"][P + f"{m}__acceptance_rule"] == 0 else r["inputs"][P + f"{m}__fraction_rule"])),
            "fit": sum(1 for r in rows if abs(ch(r, f"{m}__area__fit_margin")) <= NEAR * ch(r, f"{m}__area__gross_area")),
            "copper": sum(1 for r in rows if ch(r, f"{m}__area__cu_required") > 0 and abs(ch(r, f"{m}__area__cu_margin")) <= NEAR * ch(r, f"{m}__area__cu_required")),
            "steel": sum(1 for r in rows if abs(ch(r, f"{m}__area__steel_margin")) <= NEAR * ch(r, f"{m}__area__steel_required")),
            "capacity": sum(1 for r in rows if abs(ch(r, f"{m}__refrigeration__capacity_margin")) <= NEAR * ch(r, f"{m}__cold_load__q_cold")),
        }
        by_anchor_field = defaultdict(lambda: Counter())
        for r in rows:
            by_anchor_field[f"{r['labels']['anchor']}-{r['labels']['B_peak']:g}T"][STATUS[int(ch(r, f"{m}__conductor__status_code"))]] += 1
        materials[m] = {"status": dict(sorted(st.items())), "all_pass": allp, "check_failures": fails,
                        "near_threshold": near,
                        "green_extrapolated": sum(int(ch(r, f"{m}__refrigeration__green_extrapolated")) for r in rows),
                        "status_by_anchor_field": {k: dict(v) for k, v in sorted(by_anchor_field.items())}}
    # objective over rankable pairs
    rankable = [r for r in rows if int(ch(r, "pair__rankable")) == 1]
    def stats(vals):
        vals = sorted(vals)
        return {"n": len(vals), "min": vals[0], "median": vals[len(vals) // 2], "max": vals[-1]} if vals else {"n": 0}
    objective = {
        "rankable_pairs": len(rankable),
        "rankable_by_anchor": dict(sorted(Counter(r["labels"]["anchor"] for r in rankable).items())),
        "rankable_by_pairing": dict(sorted(Counter(r["labels"]["pairing"] for r in rankable).items())),
        "rankable_by_point_class": dict(sorted(Counter(r["labels"]["point_class"] for r in rankable).items())),
        "rankable_by_B_peak": dict(sorted(Counter(f"{r['labels']['B_peak']:g}" for r in rankable).items(), key=lambda kv: float(kv[0]))),
        "cost_difference_sign": dict(Counter("rebco_dearer" if ch(r, "pair__cost_difference") > 0 else "nb3sn_dearer" for r in rankable)),
        "cost_difference_USD_per_yr": stats([ch(r, "pair__cost_difference") for r in rankable]),
        "breakeven_rebco_price_USD_per_m": stats([ch(r, "pair__breakeven_rebco_price_per_m") for r in rankable]),
        "annualized_nb3sn_USD_per_yr": stats([ch(r, "nb3sn__annualized__annualized_cost") for r in rankable]),
        "annualized_rebco_USD_per_yr": stats([ch(r, "rebco__annualized__annualized_cost") for r in rankable]),
        "nb3sn_dearer_cases": [{"case_id": r["case_id"], "cost_difference": ch(r, "pair__cost_difference"),
                                "breakeven_rebco_price_per_m": ch(r, "pair__breakeven_rebco_price_per_m")}
                               for r in rankable if ch(r, "pair__cost_difference") <= 0],
        "baseline_case": next(({"case_id": r["case_id"], "cost_difference": ch(r, "pair__cost_difference"),
                                "breakeven_rebco_price_per_m": ch(r, "pair__breakeven_rebco_price_per_m"),
                                "annualized_nb3sn": ch(r, "nb3sn__annualized__annualized_cost"),
                                "annualized_rebco": ch(r, "rebco__annualized__annualized_cost")}
                               for r in rows if r["case_id"] == "D-10T-common-P-reference-none-reference-reference"), None),
    }
    # reference-offer matched pairs (base grid, reference family, reference offer & refrigerator) per anchor, field, pairing
    ref_pairs = []
    for r in rows:
        lb = r["labels"]
        if lb["variant"] == "none" and lb["offer_kind"] == "reference" and lb["refrigerator_kind"] == "reference" and lb["rule_family"] == "reference":
            ref_pairs.append({"anchor": lb["anchor"], "B_peak": lb["B_peak"], "pairing": lb["pairing"],
                              "nb3sn_status": STATUS[int(ch(r, "nb3sn__conductor__status_code"))],
                              "nb3sn_all_pass": int(ch(r, "nb3sn__all_pass__all_pass")),
                              "rebco_all_pass": int(ch(r, "rebco__all_pass__all_pass")),
                              "nb3sn_fit_margin_mm2": ch(r, "nb3sn__area__fit_margin"),
                              "rebco_fit_margin_mm2": ch(r, "rebco__area__fit_margin"),
                              "nb3sn_n": r["inputs"][P + "nb3sn__n_elements"], "rebco_n": r["inputs"][P + "rebco__n_elements"],
                              "nb3sn_p_in_total_MW": ch(r, "nb3sn__refrigeration__p_in_total_MW"),
                              "rebco_p_in_total_MW": ch(r, "rebco__refrigeration__p_in_total_MW"),
                              "rankable": int(ch(r, "pair__rankable")),
                              "cost_difference": ch(r, "pair__cost_difference"),
                              "breakeven_rebco_price_per_m": ch(r, "pair__breakeven_rebco_price_per_m")})
    ref_pairs.sort(key=lambda p: (p["anchor"], p["pairing"], p["B_peak"]))
    document = {"kind": "study-summary/v1", "declared_cases": n, "stored_points": len({r["candidate_id"] for r in rows}),
                "counts": counts, "constraint_outcomes": verdicts, "materials": materials, "objective": objective,
                "reference_offer_pairs": ref_pairs}
    common.write_document(document, RECORD / "results" / "summary.json")
    print(json.dumps({k: v for k, v in document.items() if k not in ("reference_offer_pairs",)}, indent=1))


if __name__ == "__main__":
    main()
