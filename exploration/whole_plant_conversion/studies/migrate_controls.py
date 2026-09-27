"""Map complete predecessor controls to the reviewed shared input interface.

No physical or financial arithmetic: paired retired keys must agree before an
explicit scenario override is applied. New values come from a named native receipt.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
from pathlib import Path

OLD = "component_alternatives__plant__"
NEW = "whole_plant_conversion__plant__"
GROUPS = {
    "source_basis__q_source_MW": ("blanket_source__q_source",),
    **{f"finance__{field}": tuple(f"{branch}_ledger__{field}" for branch in ("steam", "gas"))
       for field in ("rate", "years", "availability")},
}
RETIRED = {OLD + suffix for group in GROUPS.values() for suffix in group}
ROOT = Path(__file__).resolve().parents[3]


def predecessor_keys() -> set[str]:
    keys = set()
    for path in (ROOT / "exploration/component_alternatives/component_alternatives_tea/inputs").glob("*_params.json"):
        keys.update(json.loads(path.read_text()))
    if not keys:
        raise ValueError("predecessor input schema is absent")
    return keys


def finite_map(values: dict) -> dict[str, float]:
    if any(isinstance(v, bool) or not isinstance(v, (int, float)) or not math.isfinite(v)
           for v in values.values()):
        raise ValueError("inputs must contain finite numbers")
    return {k: float(v) for k, v in values.items()}


def migrate(legacy: dict, new_defaults: dict, *, overrides: dict | None = None) -> dict:
    old_keys = predecessor_keys()
    supplied = finite_map(legacy)
    point = finite_map(new_defaults)
    if old_keys - supplied.keys() or supplied.keys() - (old_keys | point.keys()):
        raise ValueError({"missing_old": sorted(old_keys - supplied.keys()),
                          "unknown": sorted(supplied.keys() - (old_keys | point.keys()))})
    mapped = {}
    for target, sources in GROUPS.items():
        values = [supplied[OLD + key] for key in sources]
        if NEW + target in supplied:
            values.append(supplied[NEW + target])
        if any(value != values[0] for value in values):
            raise ValueError("inconsistent duplicate values for " + target)
        mapped[NEW + target] = values[0]
    for key in old_keys - RETIRED:
        target = NEW + key.removeprefix(OLD)
        if target in supplied and supplied[target] != supplied[key]:
            raise ValueError("inconsistent duplicate values for " + target)
        mapped[target] = supplied[key]
    if mapped.keys() - point.keys():
        raise ValueError({"unexpected_retired_keys": sorted(mapped.keys() - point.keys())})
    point.update({k: v for k, v in supplied.items() if k in point})
    point.update(mapped)
    years = point[NEW + "finance__years"]
    if years <= 0 or not years.is_integer():
        raise ValueError("legacy operating horizon must be a positive integer")
    changes = finite_map(overrides or {})
    if changes.keys() - point.keys():
        raise ValueError("unknown scenario override")
    point.update(changes)
    years = point[NEW + "finance__years"]
    if years <= 0 or not years.is_integer():
        raise ValueError("operating horizon must be a positive integer")
    return point


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--old-cases", type=Path, required=True)
    parser.add_argument("--receipt", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--case", help="Exact case label in a bundled native receipt")
    args = parser.parse_args()
    from exploration.whole_plant_conversion.studies.prepare_interface import normalize_receipt
    receipt = normalize_receipt(json.loads(args.receipt.read_text()), args.case)
    if receipt.get("status") != "evaluated":
        raise ValueError("new baseline receipt did not evaluate")
    rows = json.loads(args.old_cases.read_text())["cases"]
    controls = [{"case": row["case"], "predecessor_candidate_id": row["candidate_id"],
                 "point": migrate(row["inputs"], receipt["effective_inputs"])} for row in rows]
    digest = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
    with args.out.open("x") as stream:
        json.dump({"kind": "legacy_finance_conversion_controls", "cases": controls,
                   "old_cases": str(args.old_cases), "old_cases_sha256": digest(args.old_cases),
                   "new_defaults_receipt": str(args.receipt), "receipt_sha256": digest(args.receipt),
                   "new_executable": receipt["fingerprint"], "scenario_overrides": {}}, stream, indent=2)
        stream.write("\n")
    print(json.dumps({"migrated": len(controls), "out": str(args.out)}))


if __name__ == "__main__":
    main()
