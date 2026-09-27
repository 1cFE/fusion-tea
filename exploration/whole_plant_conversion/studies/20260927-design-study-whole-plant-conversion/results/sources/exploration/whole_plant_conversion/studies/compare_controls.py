"""Compare inherited channels and predicates using their original tolerances."""
import argparse
import json
import math
from pathlib import Path

from exploration.whole_plant_conversion.studies.migrate_controls import NEW, OLD


def compare(old_record: Path, new_cases: Path, new_contract: Path) -> dict:
    old = json.loads((old_record / "results/cases.json").read_text())["cases"]
    fresh = json.loads(new_cases.read_text())["cases"]
    fresh = {row["case"]: row for row in fresh}
    if set(fresh) != {row["case"] for row in old} or len(fresh) != len(old):
        raise ValueError("control case identities differ")
    manifest = json.loads((old_record / "manifest.json").read_text())
    channels = [row["channel"] for row in manifest["objective_catalog"]]
    tolerances = {row["channel"]: row["value"] for row in manifest["absolute_tolerances"]}
    old_catalog = json.loads((old_record / "results/constraint_catalog.json").read_text())
    new_catalog = json.loads(new_contract.read_text())["constraint_catalog"]["concrete_entries"]
    by_identity = {(row["owner_instance_path"], row["source_local_identity"]): row["constraint_id"] for row in new_catalog}
    mapping = {cid: by_identity[(row["owner_instance_path"].replace(OLD, NEW, 1), row["source_local_identity"])]
               for cid, row in old_catalog.items()}
    failures = []
    max_relative = (0.0, "", "")
    for before in old:
        after = fresh[before["case"]]
        verdicts = after.get("verdicts", after.get("responses"))
        if verdicts is None:
            verdicts = {r["constraint_id"]: r["status"] for r in after["outputs"]["constraint_report"]["results"]}
        for key in channels:
            a = before["outputs"][key]
            b = after["outputs"][key.replace(OLD, NEW, 1)]
            if not math.isclose(a, b, rel_tol=1e-9, abs_tol=tolerances.get(key, 0.0)):
                failures.append({"case": before["case"], "channel": key, "before": a, "after": b})
            relative = abs(a - b) / max(abs(a), abs(b), 1e-300)
            if relative > max_relative[0]:
                max_relative = (relative, before["case"], key)
        for old_id, new_id in mapping.items():
            if before["verdicts"][old_id] != verdicts[new_id]:
                failures.append({"case": before["case"], "constraint": old_id,
                                 "before": before["verdicts"][old_id], "after": verdicts[new_id]})
    return {"status": "fail" if failures else "pass", "cases": len(old),
            "channels_per_case": len(channels), "predicates_per_case": len(mapping),
            "relative_tolerance": 1e-9, "absolute_tolerance_source": str(old_record / "manifest.json"),
            "largest_relative_difference": max_relative, "failures": failures,
            "scope": "Inherited conversion channels and predicates only; excludes four solver iteration diagnostics and new whole-plant outputs."}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--old-record", type=Path, required=True)
    parser.add_argument("--new-cases", type=Path, required=True)
    parser.add_argument("--new-contract", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    report = compare(args.old_record, args.new_cases, args.new_contract)
    with args.out.open("x") as stream:
        json.dump(report, stream, indent=2)
        stream.write("\n")
    print(json.dumps({k: v for k, v in report.items() if k != "failures"}))
    raise SystemExit(report["status"] != "pass")
