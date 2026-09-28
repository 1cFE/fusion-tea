"""Prove namespace matching and injected-error rejection without executing a model."""
import json
import tempfile
from pathlib import Path
from exploration.whole_plant_conversion.studies.compare_controls import compare
from exploration.whole_plant_conversion.studies.migrate_controls import OLD, NEW

old_record = Path("exploration/component_alternatives/studies/20260926-design-study-component-alternatives-b")
cases = json.loads((old_record / "results/cases.json").read_text())
catalog = json.loads((old_record / "results/constraint_catalog.json").read_text())
for row in cases["cases"]:
    row["outputs"] = {k.replace(OLD, NEW, 1): v for k, v in row["outputs"].items()}
    row["verdicts"] = {k.replace(OLD, NEW, 1): v for k, v in row["verdicts"].items()}
for row in catalog.values():
    row["constraint_id"] = row["constraint_id"].replace(OLD, NEW, 1)
    row["owner_instance_path"] = row["owner_instance_path"].replace(OLD, NEW, 1)
with tempfile.TemporaryDirectory(prefix="whole-control-comparator-") as directory:
    root = Path(directory)
    contract = root / "contract.json"
    points = root / "cases.json"
    contract.write_text(json.dumps({"constraint_catalog": {"concrete_entries": list(catalog.values())}}))
    points.write_text(json.dumps(cases))
    clean = compare(old_record, points, contract)
    assert clean["status"] == "pass"
    row = cases["cases"][0]
    first_channel = json.loads((old_record / "manifest.json").read_text())["objective_catalog"][0]["channel"]
    key = first_channel.replace(OLD, NEW, 1)
    row["outputs"][key] += max(10, abs(row["outputs"][key]) * .01)
    cid = next(iter(row["verdicts"]))
    row["verdicts"][cid] = "violated" if row["verdicts"][cid] == "satisfied" else "satisfied"
    points.write_text(json.dumps(cases))
    corrupt = compare(old_record, points, contract)
    assert corrupt["status"] == "fail" and len(corrupt["failures"]) == 2
receipt = {"status": "pass", "namespace_only_cases": clean["cases"],
           "channels_per_case": clean["channels_per_case"], "predicates_per_case": clean["predicates_per_case"],
           "injected_errors_detected": len(corrupt["failures"]),
           "scope": "Comparator harness only; no whole-plant model execution or verification claim."}
Path(__file__).with_name("comparator-receipt.json").write_text(json.dumps(receipt, indent=2) + "\n")
print(json.dumps(receipt))
