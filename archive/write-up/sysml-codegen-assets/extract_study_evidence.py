"""Extract existing native stellarator results for the public execution explainer.

Run from the repository root with:
    .codex-test/run python archive/write-up/sysml-codegen-assets/extract_study_evidence.py

This reads recorded artifacts only. It does not load or execute a model.
"""

import csv
import hashlib
import json
from collections import Counter
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
STUDIES = ROOT / "exploration/stellarator_e2e/studies"
PREFIX = "stellarator_09__stellaris__"
SOURCES = {}


def read(study, filename):
    path = STUDIES / study / filename
    SOURCES[str(path.relative_to(ROOT))] = hashlib.sha256(path.read_bytes()).hexdigest()
    if path.suffix == ".csv":
        with path.open(newline="") as handle:
            return list(csv.DictReader(handle))
    return json.loads(path.read_text())


def write_csv(name, rows):
    with (HERE / name).open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def output(case, key):
    return case["outputs"][PREFIX + key]


def verdict(case, name):
    matches = [v for k, v in case["verdicts"].items() if k.startswith(PREFIX + name + "__")]
    assert len(matches) == 1
    return matches[0]


def main():
    study = "20260917-pre-reveal-feasible-neighborhood"
    native = {c["candidate_id"]: c for c in read(study, "results/native-cases.json")}
    analysis = {c["candidate_id"]: c for c in read(study, "results/analysis.json")["cases"]}
    mapping = read(study, "results/map-data.csv")
    snapshot = read(study, "snapshot.json")
    rows = []
    selected_native = []
    for point in mapping:
        case = native[point["native_candidate_id"]]
        summarized = analysis[case["candidate_id"]]
        quantities = summarized["quantities"]
        valid = quantities["power_account_valid"]
        all_pass = all(v == "satisfied" for v in case["verdicts"].values())
        assert len(case["verdicts"]) == 20
        classification = "invalid-account" if not valid else "pass" if all_pass else "fail"
        assert classification == point["classification"]
        assert float(point["R_m"]) == case["inputs"][PREFIX + "plasma__R"]
        assert float(point["current_MAturn"]) == case["inputs"][PREFIX + "magnet__coil__I_coil"] / 1e6
        lcoe = output(case, "lcoe_calc__lcoe")
        assert lcoe == quantities["LCOE_dollars_MWh"]
        rows.append({
            "proposal_id": point["proposal_id"],
            "candidate_id": case["candidate_id"],
            "R_m": float(point["R_m"]),
            "current_MAturn": float(point["current_MAturn"]),
            "classification": classification,
            "power_account_valid": valid,
            "all20_satisfied": all_pass,
            "LCOE_dollars_MWh": lcoe,
            "field_margin_T": float(point["field_margin_T"]),
            "divertor_margin_MW_m2": float(point["divertor_margin_MW_m2"]),
            "auxiliary_window_margin_MW": float(point["auxiliary_window_margin_MW"]),
            "net_electric_MW": quantities["net_electric_MW"],
            "violated": point["violated"],
        })
        selected_native.append(case)
    counts = dict(Counter(row["classification"] for row in rows))
    assert counts == {"fail": 210, "pass": 44, "invalid-account": 2}
    assert len({(row["R_m"], row["current_MAturn"]) for row in rows}) == 256
    varying = {PREFIX + "plasma__R", PREFIX + "magnet__coil__I_coil"}
    fixed = {k: v for k, v in selected_native[0]["inputs"].items() if k not in varying}
    for case in selected_native:
        assert {k: v for k, v in case["inputs"].items() if k not in varying} == fixed
    write_csv("feasibility-cost-map.csv", rows)
    passing_lcoes = [r["LCOE_dollars_MWh"] for r in rows if r["classification"] == "pass"]
    meta = {
        "reading": "Agent-authored presentation extraction from retained study records; no model execution or independent physical qualification.",
        "feasibility_map": {
            "study_id": study, "package": snapshot["package"],
            "integration_candidate_pin": snapshot["integration_candidate_pin"],
            "rows": len(rows), "counts": counts,
            "passing_lcoe_range_dollars_MWh": [min(passing_lcoes), max(passing_lcoes)],
            "fixed_explicit_inputs": fixed,
            "other_defaults_source": str((STUDIES / study / "preparation/resolved-defaults.json").relative_to(ROOT)),
            "interpretation": "Historical 20-screen snapshot. Passing means all then-implemented screens and valid power account, not a qualified plant or complete cost estimate. Show individual samples; no interpolation or global optimum claim.",
        },
    }

    study = "20260915-joint-magnet-sizing"
    native = {c["candidate_id"]: c for c in read(study, "results/native-cases.json")}
    analysis = read(study, "results/analysis.json")
    snapshot = read(study, "snapshot.json")
    selections = [
        ("reference", "Original inventory, original allocation"),
        ("reference-sized", "Current-sized inventory, original allocation"),
        ("reference-accommodated", "Current-sized inventory, enlarged allocation"),
    ]
    rows = []
    inputs = {}
    for alias, label in selections:
        matches = [c for c in analysis["cases"] if alias in c["report_aliases"]]
        assert len(matches) == 1
        summarized = matches[0]
        case = native[summarized["candidate_id"]]
        q = summarized["quantities"]
        assert output(case, "lcoe_calc__lcoe") == summarized["lcoe"]
        assert output(case, "magnet__peak_field_calc__B_peak") == q["actual_field_T"]
        inputs[alias] = case["inputs"]
        rows.append({
            "label": label,
            "report_alias": alias,
            "proposal_id": case["proposal_id"],
            "candidate_id": case["candidate_id"],
            "LCOE_dollars_MWh": summarized["lcoe"],
            "magnet_cost_dollars": q["magnet_cost"],
            "tape_length_m": q["tape_length_m"],
            "actual_field_T": q["actual_field_T"],
            "field_limit_T": q["selected_field_limit_T"],
            "radial_exterior_m": q["independent_radial_allocation_m"],
            "transverse_cavity_m": q["independent_transverse_cavity_m"],
            "required_cavity_x_m": q["required_cavity_x_m"],
            "required_cavity_y_m": q["required_cavity_y_m"],
            "current_status": verdict(case, "reference_conductor_current_ok"),
            "fit_status": verdict(case, "wp_fit_ok"),
            "field_status": verdict(case, "peak_field_ok"),
            "all20_satisfied": summarized["all20_satisfied"],
            "violated": ";".join(summarized["violated"]),
        })
    write_csv("magnet-sizing-comparison.csv", rows)
    meta["magnet_comparison"] = {
        "study_id": study, "package": snapshot["package"],
        "integration_candidate_pin": snapshot["integration_candidate_pin"],
        "selected_rows": len(rows), "unique_native_cases_in_study": analysis["unique_cases"],
        "selected_explicit_inputs": inputs,
        "interpretation": "Three matched reference examples from one historical executable. First change enables current sizing with 1% physical inventory reserve; second enlarges both independent allocations. All three fail the full plant screen.",
    }
    meta["source_sha256"] = SOURCES
    (HERE / "study-evidence.json").write_text(json.dumps(meta, indent=2) + "\n")
    print(json.dumps({"map_counts": counts, "passing_lcoe_range": meta["feasibility_map"]["passing_lcoe_range_dollars_MWh"], "magnet_comparison": rows}, indent=2))


if __name__ == "__main__":
    main()
