"""Verify stored native development receipts through the unchanged study checker.

This diagnostic reads current generated metadata in memory before the package is
committed. It writes no package/interface state and authorizes no main study.
Persistent interface preparation still requires the stock clean-package gate.
"""
import argparse
import hashlib
import inspect
import json
from pathlib import Path
from types import SimpleNamespace

from scripts.study import verify
from exploration.exchanger_architecture.thermal_requirements.studies import (
    oracle_entry, prepare_interface, study_route, thermal_oracle,
)
from exploration.aries_integrated.studies import (
    oracle_entry as inherited, equipment_bindings, equipment_oracle,
    lifecycle_bindings, lifecycle_oracle, study_route as inherited_route,
    interface_data as inherited_interface,
)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--receipts", type=Path, nargs="+", required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    inventory = prepare_interface.discover(study_route.PACKAGE_DIR)
    contract = json.loads((study_route.PACKAGE_DIR/"contracts/model_contract.json").read_text())
    entries = {e["constraint_id"]: e for e in contract["constraint_catalog"]["concrete_entries"]}
    rows = []
    for file in args.receipts:
        receipt = json.loads(file.read_text())
        rows.extend(receipt if isinstance(receipt, list) else [receipt])
    first = next(r for r in rows if r["status"] == "evaluated")
    temporary_interface = inventory["fingerprints"]["recorded_provenance"] | {
        "entry_keys": inventory["entry_keys"],
        "channels": {k:k for k,v in first["outputs"].items() if isinstance(v, (int,float))},
        "constraints": {k:v["source_local_identity"] for k,v in entries.items()},
    }
    study_route.interface = lambda: temporary_interface
    bindings = oracle_entry.operand_bindings()
    catalog = oracle_entry.comparison_catalog()
    absolute = {row["channel"]: row["value"] for row in prepare_interface.ABSOLUTE_TOLERANCES}
    fingerprint = temporary_interface["executable_fingerprint"]
    results = []
    for row in rows:
        result = {"case": row["case"], "native_status": row["status"]}
        try:
            if row["status"] != "evaluated":
                raise ValueError("native development case did not evaluate")
            verdicts = {v["constraint_id"]: v["status"] for v in row["outputs"]["constraint_report"]["results"]}
            if set(verdicts) != set(entries):
                raise ValueError("receipt verdict set differs from actual contract")
            case = SimpleNamespace(candidate_id=row["case"], inputs=row["effective_inputs"],
                outputs=row["outputs"], verdicts=verdicts, executable_fingerprint=row["fingerprint"])
            worst, channels, checks, calculated = verify.check_case(case, oracle_entry.evaluate,
                bindings, entries, catalog, {}, fingerprint, absolute)
            result.update(status="PASS", channels=len(channels), predicates=len(checks),
                worst_relative_deviation=worst[0], worst_channel=worst[2],
                engineering_satisfied=all(v == "satisfied" for v in verdicts.values()),
                largest_thermal_absolute_error=max(abs(case.outputs[k]-calculated[k])
                    for k in channels if "heat_exchangers__evaluate__" in k))
        except Exception as error:
            result.update(status="FAIL", error=f"{type(error).__name__}: {error}")
        results.append(result)
    lineage = {}
    for module in (oracle_entry, thermal_oracle, inherited, equipment_bindings, equipment_oracle,
                   lifecycle_bindings, lifecycle_oracle, inherited_route, inherited_interface,
                   prepare_interface, study_route):
        file = Path(inspect.getfile(module)).resolve()
        lineage[str(file.relative_to(prepare_interface.ROOT))] = hashlib.sha256(file.read_bytes()).hexdigest()
    source_manifest = prepare_interface.ROOT/"exploration/aries_integrated/studies/manifest.json"
    lineage[str(source_manifest.relative_to(prepare_interface.ROOT))] = hashlib.sha256(source_manifest.read_bytes()).hexdigest()
    document = {"status": "PASS" if all(r["status"] == "PASS" for r in results) else "FAIL",
        "kind": "all-point native development numerical verification; not main study",
        "executable_fingerprint": fingerprint, "relative_tolerance": verify.TOLERANCE,
        "absolute_tolerances": prepare_interface.ABSOLUTE_TOLERANCES,
        "comparison_catalog": catalog, "operand_bindings": bindings,
        "source_sha256": lineage, "cases": results}
    args.output.write_text(json.dumps(document, indent=2)+"\n")
    print(json.dumps({"status": document["status"], "cases": len(results),
        "passed": sum(r["status"] == "PASS" for r in results), "catalog": len(catalog),
        "predicates": len(bindings), "failures": [r for r in results if r["status"] != "PASS"]}, indent=2))
    if document["status"] != "PASS":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
