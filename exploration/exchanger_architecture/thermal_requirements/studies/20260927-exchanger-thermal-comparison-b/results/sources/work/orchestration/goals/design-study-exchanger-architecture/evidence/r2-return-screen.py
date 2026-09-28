"""Necessary return/hot-cap assessment of sealed round-1 cases, not a new plant model.

The conditional N-R targets and boundary convention are in r2-thermal-requirements.md.
This reads delivered duty, never only the heat an inadequate exchanger accepted.
It does not choose control, alter native outputs or declare any case thermally passing.
"""
import argparse
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[5]
SOURCE = ROOT / "exploration/exchanger_architecture/studies/20260926-design-study-exchanger-architecture/results/cases.json"
PREFIX = "aries_integrated_plant__"
TARGETS = {"he": 659.15, "pbli": 724.15, "divertor": 846.15}
PARTITION = {"he": (0.41164, 141.0), "pbli": (0.56636, 0.0), "divertor": (0.15, 29.0)}


def assess(source):
    cases = []
    bounds = {}
    for row in source["cases"]:
        if not row["case"].startswith("main-"):
            continue
        inputs, outputs = row["inputs"], row["outputs"]
        load = inputs[PREFIX + "source__reference_fusion_mw"]
        branches = {}
        for branch, target in TARGETS.items():
            key = PREFIX + "heat_exchangers__" + branch
            capacity_rate = inputs[key + "_flow"] * inputs[key + "_cp"] / 1e6
            hot_cap = inputs[key + "_limit"]
            delivered = outputs[PREFIX + branch + "_coolant__evaluate__delivered_heat"]
            slope, intercept = PARTITION[branch]
            assert math.isclose(delivered, slope * load + intercept, abs_tol=1e-8, rel_tol=1e-12)
            required_hot = target + delivered / capacity_rate
            margin = hot_cap - required_hot
            bound = (capacity_rate * (hot_cap - target) - intercept) / slope
            if branch in bounds:
                assert math.isclose(bound, bounds[branch], abs_tol=1e-9, rel_tol=0)
            bounds[branch] = bound
            branches[branch] = {
                "target_return_k": target,
                "delivered_duty_mw": delivered,
                "primary_capacity_rate_mw_per_k": capacity_rate,
                "hot_cap_k": hot_cap,
                "required_hot_k": required_hot,
                "hot_margin_k": margin,
                "necessary_hot_cap_condition": margin >= -1e-9,
            }
        cases.append({
            "candidate_id": row["candidate_id"], "case": row["case"],
            "source_mw": load, "branches": branches,
            "necessary_hot_cap_conditions_hold": all(b["necessary_hot_cap_condition"] for b in branches.values()),
            "complete_thermal_assessment": "not established: return control and approach requirements unresolved",
        })
    assert len(cases) == 432
    return {
        "kind": "necessary-condition assessment; not a native model update or a new study",
        "authority": "r2-thermal-requirements.md, N-R aggregate return convention",
        "native_evidence": str(SOURCE.relative_to(ROOT)) + "@afd96d51",
        "source_upper_bounds_mw": bounds,
        "main_cases_assessed": len(cases),
        "necessary_hot_cap_conditions_hold": sum(c["necessary_hot_cap_conditions_hold"] for c in cases),
        "necessary_hot_cap_conditions_fail": sum(not c["necessary_hot_cap_conditions_hold"] for c in cases),
        "cases": cases,
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    result = assess(json.loads(SOURCE.read_text()))
    args.out.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({k: v for k, v in result.items() if k != "cases"}, indent=2))
