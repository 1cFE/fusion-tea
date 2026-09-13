"""Study-local direct-API protocol; invoke one native stage at a time."""
import argparse
import csv
import json
from pathlib import Path
from scripts.study import common, preflight, verify
from exploration.ife_e2e.studies import study_route as route, oracle_entry as oracle
from tests.ife_oracle import BOUNDARIES

HERE = Path(__file__).resolve().parent
RESULTS = HERE / "results"
P = route.P


def baseline_point():
    return json.loads(route.MANIFEST_PATH.read_text())["baseline"]["point"]


def baseline():
    paths = route.execute_baseline(RESULTS / "baseline")
    result = preflight.run_gates(route.PACKAGE_DIR, route.MANIFEST_PATH, HERE / "axes.json",
                                 paths["identity"], paths["baseline_result"])
    common.write_document(result, RESULTS / "preflight.json")
    if result["outcome"] != "pass":
        raise RuntimeError("baseline preflight failed")


def scan():
    rows = []
    base = baseline_point()
    for name, key, values in (
        ("beam_energy_mj", "driver__beam_energy_mj", [2.5, 4, 5, 6, 7.5, 10]),
        ("frequency", "frequency", [2.3, 3.6, 4.6, 5.6, 6.9, 9.2]),
    ):
        for value in values:
            point = base | {P + key: value}
            rows.append({"axis": name, "value": value, "inputs": point, "oracle_outputs": oracle.evaluate(point)})
    common.write_document({"provenance": "engineered", "rows": rows}, RESULTS / "oracle-scan.json")


def proposed_cases():
    base = baseline_point()
    cases = [{"role": "baseline", "point": base}]
    for name, key, values in (
        ("beam", "driver__beam_energy_mj", [4.0, 6.0]),
        ("rate", "frequency", [3.6, 5.6]),
    ):
        cases.extend({"role": f"{name}-{value}", "point": base | {P + key: value}} for value in values)
    for name in ("counterexample", "zero"):
        cases.append({"role": name, "point": base | {P + key: value for key, value in BOUNDARIES[name].items()}})
    return cases


def execute():
    proposals = proposed_cases()
    common.write_document({"cases": proposals}, RESULTS / "proposals.json")
    cases, db = route.run_points("20260910-ife-operating-point", [p["point"] for p in proposals], RESULTS / "_work")
    route._completed(cases, "IFE operating-point study")
    roles = {tuple(sorted(p["point"].items())): p["role"] for p in proposals}
    rows, records = [], []
    for case in cases:
        role = roles[tuple(sorted(case.inputs.items()))]
        verdicts = route.short_verdicts(case)
        prices = route.eligible_prices(case)
        records.append({"case_id": case.candidate_id, "role": role, "state": case.state,
                        "inputs": dict(case.inputs), "outputs": dict(case.outputs),
                        "verdicts": dict(case.verdicts), "price_eligibility": prices,
                        "executable_fingerprint": case.executable_fingerprint})
        rows.append({"arm_id": "arm-ife", "case_id": case.candidate_id, "role": role,
                     "beam_energy_mj": case.inputs[P + "driver__beam_energy_mj"],
                     "frequency_hz": case.inputs[P + "frequency"],
                     "net_electric_mw": case.outputs[P + "lcoe_calc__net_electric_power"] / 1e6,
                     "hawker_mixed_dollars_per_mwh": case.outputs[P + "hawker_price__price"],
                     "meier_1988_cents_per_kwh": case.outputs[P + "meier_price__price"],
                     **verdicts, **{name + "_eligible": value for name, value in prices.items()},
                     "model_feasible": all(v == "satisfied" for v in verdicts.values())})
    common.write_document({"cases": records}, RESULTS / "cases.json")
    with (RESULTS / "points.csv").open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    summary = verify.build_summary(route.PACKAGE_DIR, route.MANIFEST_PATH,
                                    RESULTS / "baseline/package_identity.json", [db], 100, None, [])
    common.write_document(summary, RESULTS / "verification_summary.json")
    clean = preflight.run_clean(route.PACKAGE_DIR)
    common.write_document(clean, RESULTS / "post-run-clean.json")
    prepared = route.prepare(route.PACKAGE_DIR, RESULTS / "_work")
    common.write_document({key: value.__module__ + "." + value.__qualname__
                           for key, value in prepared.entry_models.items()}, RESULTS / "entry-models.json")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("stage", choices=["baseline", "scan", "execute"])
    {"baseline": baseline, "scan": scan, "execute": execute}[parser.parse_args().stage]()
