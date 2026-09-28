"""Execute one fixed point through the existing native route and frozen input rules.

Inputs must already use the rule's units, with source and definition evidence.
This adapter performs no reference extraction, optimization or technology substitution.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
import sys
from pathlib import Path


def numeric(value, label):
    if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value):
        raise ValueError(f"{label}: finite numeric value required")
    return float(value)


def select_inputs(rules, request):
    if set(request) - {"run_kind", "values", "conditioned_seam", "conditioned_values"}:
        raise ValueError("unknown request field")
    kind = request.get("run_kind")
    if kind not in {"blind", "conditioned", "verification"}:
        raise ValueError("run_kind must be blind, conditioned or verification")
    supplied = request.get("values", {})
    if not isinstance(supplied, dict):
        raise ValueError("values must be an object")
    allowed = {row["key"]: row for row in rules["independent_reference_inputs"]}
    point = dict(rules["forward_overrides"])
    for key, record in supplied.items():
        if key not in allowed:
            raise ValueError(f"not a permitted independent input: {key}")
        if not isinstance(record, dict) or set(record) != {"value", "unit", "source", "definition", "resolution"}:
            raise ValueError(f"{key}: value, unit, source, definition and resolution required")
        if record["unit"] != allowed[key]["unit"]:
            raise ValueError(f"{key}: preconvert explicitly to {allowed[key]['unit']}")
        if not all(isinstance(record[x], str) and record[x].strip() for x in ("source", "definition")):
            raise ValueError(f"{key}: source and definition evidence required")
        if record["resolution"] != "matched":
            raise ValueError(f"{key}: unresolved reference input")
        point[key] = numeric(record["value"], key)
    if kind == "verification" and supplied:
        raise ValueError("verification is the frozen model-side default point only")
    seam_id = request.get("conditioned_seam")
    conditioned = request.get("conditioned_values", {})
    if kind != "conditioned" and (seam_id is not None or conditioned):
        raise ValueError("blind/verification runs cannot select a conditioned seam")
    if kind == "conditioned":
        seams = {row["id"]: row for row in rules["conditioned_seams"]}
        if seam_id not in seams:
            raise ValueError("unknown conditioned seam")
        seam = seams[seam_id]["keys"]
        required = {key for key, value in seam.items() if value is None}
        if not isinstance(conditioned, dict) or set(conditioned) != required:
            raise ValueError(f"conditioned values must name exactly {sorted(required)}")
        point.update({key: numeric(value, key) for key, value in seam.items() if value is not None})
        point.update({key: numeric(value, key) for key, value in conditioned.items()})
        if seam_id == "held_calendar" and not 0 < next(iter(conditioned.values())) <= 1:
            raise ValueError("held availability must be in (0,1]")
    return point, {
        "run_kind": kind,
        "supplied_input_keys": sorted(supplied),
        "missing_independent_inputs": sorted(set(allowed) - set(supplied)),
        "held_fallback": kind != "verification" and set(supplied) != set(allowed),
        "conditioned_seam": seam_id,
        "independent_prediction_credit_for_supplied": False,
        "scope_decision": rules["scope_decision"],
    }


def execute(root, rules_path, request, out):
    rules = json.loads(rules_path.read_text())
    defaults_bytes = (root / rules["defaults_source"]).read_bytes()
    if hashlib.sha256(defaults_bytes).hexdigest() != rules["defaults_sha256"]:
        raise ValueError("frozen package defaults changed")
    point, classification = select_inputs(rules, request)
    sys.path.insert(0, str(root))
    sys.path.insert(0, str(Path(os.environ["STOP_PARSER_TEAX_ROOT"]) / "packages/teax-simkit"))
    from exploration.stellarator_e2e.studies import study_route as route

    package = root / rules["package_path"]
    contract = json.loads((package / "contracts/model_contract.json").read_text())
    numeric_channels = {r["channel_name"]: r["channel_name"] for r in contract["outputs"]
                        if r["python_type"] in ("float", "int")}
    # A fresh output directory prevents an earlier run from being overwritten or reused.
    out.mkdir(parents=True, exist_ok=False)
    (out / "request.json").write_text(json.dumps(request, indent=2, sort_keys=True) + "\n")
    result = {**classification, "requested_overrides": point,
              "effective_inputs": {**rules["default_values"], **point},
              "rules_sha256": hashlib.sha256(rules_path.read_bytes()).hexdigest(),
              "reference_data": "none" if classification["run_kind"] == "verification" else "caller-supplied; source adjudication retained in request.json"}
    try:
        cases, db = route.run_points("frozen-fixed-point", [point], out / "native", package,
                                    required_channels=numeric_channels)
        if len(cases) != 1:
            raise ValueError("native route did not return exactly one case")
        case = cases[0]
        result.update(state=case.state, candidate_id=case.candidate_id,
                      executable_fingerprint=case.executable_fingerprint,
                      outputs=dict(case.outputs), verdicts=dict(case.verdicts),
                      store=str(db.relative_to(out)))
        if case.state == "completed":
            route.require_published(case, numeric_channels)
            result["constraints"] = route.short_verdicts(case, package)
            result["all_constraints_satisfied"] = all(v == "satisfied" for v in case.verdicts.values())
        else:
            result["error"] = "native case did not complete; inspect retained native store"
    except Exception as error:
        result.update(state="execution_refused", error=f"{type(error).__name__}: {error}")
    (out / "native-result.json").write_text(json.dumps(result, indent=2, sort_keys=True, allow_nan=False) + "\n")
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--rules", type=Path, default=Path(__file__).with_name("input-rules.json"))
    parser.add_argument("--request", type=Path, required=True)
    parser.add_argument("--out-dir", type=Path, required=True)
    args = parser.parse_args()
    result = execute(args.root.resolve(), args.rules.resolve(), json.loads(args.request.read_text()), args.out_dir.resolve())
    print(result["state"])
    return 0 if result["state"] == "completed" else 1


if __name__ == "__main__":
    raise SystemExit(main())
