"""Reproduce the native verifier's refusal of the actual audited IFE predicate."""
import json
from pathlib import Path

from scripts.study.verify import VerifyError, derive_verdict

ROOT = Path(__file__).resolve().parents[3]
P = "hif_plant_pkg__hif_plant__"
contract = json.loads((ROOT / "exploration/ife_e2e/generated/contracts/model_contract.json").read_text())
entry = next(e for e in contract["constraint_catalog"]["concrete_entries"]
             if e["source_local_identity"] == "viability")
bindings = {entry["constraint_id"]: {
    "eta": {"kind": "input", "key": P + "driver__efficiency"},
    "gain_in": {"kind": "input", "key": P + "gain"},
    "threshold": {"kind": "input", "key": P + "viability__threshold"},
}}
inputs = {p["qualified_name"]: p["default_value"] for p in contract["parameters"]}
try:
    result = derive_verdict(entry["constraint_id"], entry, bindings, {}, inputs, {})
except VerifyError as exc:
    print(json.dumps({"result": "PREREQUISITE", "producer": "scripts/study/verify.py",
                      "constraint_id": entry["constraint_id"], "error": str(exc)}, indent=2))
else:
    print(json.dumps({"result": "SUPPORTED", "verdict": result}, indent=2))
