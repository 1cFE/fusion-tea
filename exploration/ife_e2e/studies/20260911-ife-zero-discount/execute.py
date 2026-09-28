"""Study-local direct-API protocol; invoke one native stage at a time."""
import argparse
import csv
import json
from pathlib import Path
from scripts.study import common, preflight, verify
from exploration.ife_e2e.studies import study_route as route, oracle_entry as oracle
from tests.ife_oracle import BOUNDARIES, decimal_present_value_reference
import math
from decimal import Decimal, localcontext

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


RATES = [-1e-4, -1e-8, -1e-12, -1e-14, -1e-16, -1e-18, 0., 1e-18, 1e-16, 1e-14, 1e-12, 1e-8, 1e-4, .08]


def scan():
    rows = []
    for rate in RATES:
        point = baseline_point() | {P + "discount_rate": rate}
        outputs = oracle.evaluate(point)
        if not all(math.isfinite(value) for value in outputs.values()):
            raise RuntimeError("nonfinite scan")
        rows.append({"rate": rate, "inputs": point, "oracle_outputs": outputs})
    common.write_document({"provenance": "engineered", "rows": rows}, RESULTS / "oracle-scan.json")


def proposed_cases():
    base = baseline_point()
    cases = [{"role": "baseline" if rate == .08 else "response", "point": base | {P + "discount_rate": rate}} for rate in RATES]
    for name in ("counterexample", "zero"):
        for rate in (-1e-9, 0., 1e-9):
            cases.append({"role": name, "point": base | {P + key: value for key, value in BOUNDARIES[name].items()} | {P + "discount_rate": rate}})
    return cases


def execute():
    proposals = proposed_cases()
    common.write_document({"cases": proposals}, RESULTS / "proposals.json")
    cases, db = route.run_points("20260911-ife-zero-discount", [p["point"] for p in proposals], RESULTS / "_work")
    route._completed(cases, "IFE zero-discount study")
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
                     "discount_rate": case.inputs[P + "discount_rate"],
                     "discounted_cost": case.outputs[P + "lcoe_calc__discounted_cost"],
                     "discounted_energy": case.outputs[P + "lcoe_calc__discounted_energy"],
                     "construction_factor": case.outputs[P + "pv_factors__construction_factor"],
                     "operation_factor": case.outputs[P + "pv_factors__operation_factor"],
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
    if summary["outcome"] != "pass":
        raise RuntimeError("native verification failed")
    decimal_rows = []
    mapping = {"discounted_cost": "lcoe_calc__discounted_cost", "discounted_energy": "lcoe_calc__discounted_energy", "price": "hawker_price__price", "construction_factor": "pv_factors__construction_factor", "operation_factor": "pv_factors__operation_factor"}
    for case in cases:
        values = {key.removeprefix(P): value for key, value in case.inputs.items()}
        reference, method = decimal_present_value_reference(values)
        comparisons = {}
        for key, channel in mapping.items():
            expected, actual = reference[key], case.outputs[P + channel]
            with localcontext() as context:
                context.prec = 80
                delta = abs(Decimal.from_float(actual) - expected)
                error = float(delta / abs(expected) if expected else delta)
            if error > 1e-12:
                raise RuntimeError((case.candidate_id, key, actual, expected))
            comparisons[key] = {"actual": actual, "reference_decimal": str(reference[key]), "relative_error_or_absolute_at_zero": error}
        decimal_rows.append({"case_id": case.candidate_id, "method": method, "comparisons": comparisons})
    common.write_document({"outcome": "pass", "cases": decimal_rows}, RESULTS / "decimal-verification.json")
    clean = preflight.run_clean(route.PACKAGE_DIR)
    common.write_document(clean, RESULTS / "post-run-clean.json")
    if clean["outcome"] != "pass":
        raise RuntimeError("package dirty after execution")
    prepared = route.prepare(route.PACKAGE_DIR, RESULTS / "_work")
    common.write_document({key: value.__module__ + "." + value.__qualname__
                           for key, value in prepared.entry_models.items()}, RESULTS / "entry-models.json")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("stage", choices=["baseline", "scan", "execute"])
    {"baseline": baseline, "scan": scan, "execute": execute}[parser.parse_args().stage]()
