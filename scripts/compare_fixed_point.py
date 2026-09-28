#!/usr/bin/env python
"""Frozen-manifest comparison reporter; no model execution or reference lookup."""
import argparse
import copy
import json
import math
from pathlib import Path


class InvalidInput(ValueError):
    """Malformed decision-bearing data."""


def obj(value, required, optional=(), where="object"):
    if not isinstance(value, dict):
        raise InvalidInput(f"{where}: expected object")
    missing = set(required) - value.keys()
    extra = value.keys() - set(required) - set(optional)
    if missing or extra:
        raise InvalidInput(f"{where}: missing {sorted(missing)}, unknown {sorted(extra)}")


def strings(value, where):
    if not isinstance(value, list) or any(not isinstance(x, str) or not x for x in value):
        raise InvalidInput(f"{where}: expected list of nonempty strings")


def finite(value):
    return type(value) in (int, float) and math.isfinite(value)


# Scales are fixed code, not caller-supplied factors. Exact unit identity works for
# other manifest units; changing dimensions is never inferred.
UNITS = {
    "W": ("power", 1), "kW": ("power", 1000), "MW": ("power", 1e6), "GW": ("power", 1e9),
    "USD": ("money", 1), "kUSD": ("money", 1000), "MUSD": ("money", 1e6),
    "USD/kWh": ("energy_cost", 1000), "USD/MWh": ("energy_cost", 1),
    "m": ("length", 1), "cm": ("length", .01), "mm": ("length", .001),
    "kg": ("mass", 1), "t": ("mass", 1000), "1": ("fraction", 1), "%": ("fraction", .01),
}
ROW_FIELDS = "id axis formal meaning unit aggregation producers calculation role depends_on included_scope excluded_scope technology validity_limits reference_required conversion verification applicability reference_value exclusion".split()


def validate_manifest(manifest):
    # Extra manifest annotations cannot affect decisions. All decision fields below
    # have explicit schemas; observations have no such extensibility.
    if not isinstance(manifest, dict) or not set(("schema_version", "package_path", "prefix", "quantities", "accounting")) <= manifest.keys():
        raise InvalidInput("manifest: missing required fields")
    if type(manifest["schema_version"]) is not int or manifest["schema_version"] != 1:
        raise InvalidInput("manifest schema_version must be 1")
    if not isinstance(manifest["quantities"], list) or not manifest["quantities"]:
        raise InvalidInput("manifest needs quantities")
    ids = set()
    for q in manifest["quantities"]:
        if not isinstance(q, dict) or not set(ROW_FIELDS) <= q.keys():
            raise InvalidInput("manifest quantity missing required fields")
        for k in ("id", "meaning", "unit", "aggregation", "technology"):
            if not isinstance(q[k], str) or not q[k]:
                raise InvalidInput(f"quantity {k}: expected nonempty string")
        if q["id"] in ids:
            raise InvalidInput("duplicate quantity id")
        ids.add(q["id"])
        if q["axis"] not in ("structural", "derived", "cost", "diagnostic") or type(q["formal"]) is not bool:
            raise InvalidInput("invalid axis/formal")
        if q["role"] not in ("supplied", "held", "independent", "derived") or q["applicability"] not in ("conditional", "unresolved", "supported"):
            raise InvalidInput("invalid role/applicability")
        if q["reference_value"] is not None or q["exclusion"] not in (None, "C220107"):
            raise InvalidInput("manifest must have null reference values and declared exclusions")
        if q["calculation"] is not None and not isinstance(q["calculation"], str):
            raise InvalidInput("invalid calculation")
        for k in ("producers", "depends_on", "included_scope", "excluded_scope", "validity_limits", "reference_required", "verification"):
            strings(q[k], k)
        c = q["conversion"]
        obj(c, ("basis", "allowed_units", "allowed_basis_conversions"), where="conversion")
        if not isinstance(c["basis"], str) or not c["basis"]:
            raise InvalidInput("conversion basis required")
        strings(c["allowed_units"], "allowed units")
        if q["unit"] not in c["allowed_units"] or not isinstance(c["allowed_basis_conversions"], list):
            raise InvalidInput("canonical unit and conversion list required")
        conversion_ids = set()
        for rule in c["allowed_basis_conversions"]:
            obj(rule, ("id", "from", "to", "factor", "evidence"), where="basis conversion")
            if any(not isinstance(rule[k], str) or not rule[k] for k in ("id", "from", "to", "evidence")) or not finite(rule["factor"]) or rule["factor"] <= 0:
                raise InvalidInput("invalid basis conversion")
            if rule["to"] != c["basis"] or rule["id"] in conversion_ids:
                raise InvalidInput("basis conversion must target canonical basis with unique id")
            conversion_ids.add(rule["id"])
    for q in manifest["quantities"]:
        if set(q["depends_on"]) - ids:
            raise InvalidInput("unknown dependency")
    if not isinstance(manifest["accounting"], list):
        raise InvalidInput("accounting must be list")
    equation_ids = set()
    edges = {}
    for eq in manifest["accounting"]:
        obj(eq, ("id", "parent", "children", "meaning"), ("limitations",), "accounting equation")
        strings(eq["children"], "children")
        if not eq["children"] or len(set(eq["children"])) != len(eq["children"]) or eq["parent"] in eq["children"]:
            raise InvalidInput("accounting children must be nonempty and disjoint")
        if eq["parent"] not in ids or set(eq["children"]) - ids or eq["id"] in equation_ids or eq["parent"] in edges:
            raise InvalidInput("unknown/duplicate accounting quantity or equation")
        equation_ids.add(eq["id"])
        edges[eq["parent"]] = eq["children"]
    def leaves(node, stack):
        if node in stack:
            raise InvalidInput("accounting cycle")
        result = []
        for child in edges.get(node, []):
            result.extend(leaves(child, stack | {node}))
        if len(result) != len(set(result)):
            raise InvalidInput("accounting double counts a descendant")
        return result or [node]
    for node in edges:
        leaves(node, set())


def normalize(side, q):
    obj(side, ("value", "unit", "basis", "scope", "technology"), ("basis_conversion",), "observation side")
    strings(side["scope"], "scope")
    for key in ("unit", "basis", "technology"):
        if not isinstance(side[key], str) or not side[key]:
            raise InvalidInput(f"{key}: expected nonempty string")
    if "basis_conversion" in side and not isinstance(side["basis_conversion"], str):
        raise InvalidInput("basis_conversion must be frozen rule id")
    raw = copy.deepcopy(side)
    result = {"raw": raw, "adjusted": None, "conversions": [], "issues": []}
    if not finite(side["value"]) and not (q["axis"] == "structural" and side["value"] is None):
        result["issues"].append("missing_or_nonfinite_value")
        return result
    value = side["value"]
    if sorted(side["scope"]) != sorted(q["included_scope"]):
        result["issues"].append("scope_mismatch")
    if side["technology"] != q["technology"]:
        result["issues"].append("technology_mismatch")
    unit = side["unit"]
    if unit not in q["conversion"]["allowed_units"]:
        result["issues"].append("unsupported_unit")
    elif unit != q["unit"]:
        source, target = UNITS.get(unit), UNITS.get(q["unit"])
        if source is None or target is None or source[0] != target[0]:
            result["issues"].append("unsupported_unit")
        else:
            factor = source[1] / target[1]
            value = value * factor if value is not None else None
            result["conversions"].append({"kind": "unit", "from": unit, "to": q["unit"], "factor": factor})
    basis = q["conversion"]["basis"]
    if side["basis"] != basis:
        rule = next((r for r in q["conversion"]["allowed_basis_conversions"] if r["id"] == side.get("basis_conversion") and r["from"] == side["basis"]), None)
        if rule is None:
            result["issues"].append("unsupported_basis")
        else:
            value = value * rule["factor"] if value is not None else None
            result["conversions"].append({"kind": "basis", **rule})
    elif "basis_conversion" in side:
        result["issues"].append("unnecessary_basis_conversion")
    if value is not None and not finite(value):
        result["issues"].append("nonfinite_adjusted_value")
    if not result["issues"]:
        result["adjusted"] = {"value": value, "unit": q["unit"], "basis": basis}
    return result


def compare(manifest, observations):
    validate_manifest(manifest)
    obj(observations, ("schema_version", "run_kind", "execution_status", "constraints", "extrapolations", "quantities"), ("notes",), "observations")
    if type(observations["schema_version"]) is not int or observations["schema_version"] != 1:
        raise InvalidInput("observation schema_version must be 1")
    if observations["run_kind"] not in ("blind", "conditioned") or observations["execution_status"] not in ("completed", "failed", "refused"):
        raise InvalidInput("invalid run kind or execution status")
    if "notes" in observations and not isinstance(observations["notes"], str):
        raise InvalidInput("notes must be a string")
    constraints = observations["constraints"]
    if not isinstance(constraints, dict) or any(not isinstance(k, str) or not k or type(v) is not bool for k, v in constraints.items()):
        raise InvalidInput("constraints must map names to booleans")
    strings(observations["extrapolations"], "extrapolations")
    quantities = observations["quantities"]
    ids = {q["id"] for q in manifest["quantities"]}
    if not isinstance(quantities, dict) or quantities.keys() - ids:
        raise InvalidInput("unknown observation quantity")
    rows = []
    for q in manifest["quantities"]:
        row = {"id": q["id"], "axis": q["axis"], "formal": q["formal"], "role": q["role"], "status": "blocked", "issues": [], "ratio": None, "independent_credit": False, "exclusion": q["exclusion"]}
        rows.append(row)
        obs = quantities.get(q["id"])
        if obs is None:
            row["issues"].append("missing_observation")
            continue
        obj(obs, ("model", "reference", "model_valid", "applicability_evidence"), ("structural_evidence",), f"quantity {q['id']}")
        if type(obs["model_valid"]) is not bool or not isinstance(obs["applicability_evidence"], str):
            raise InvalidInput("invalid validity/applicability evidence")
        row["model_valid"] = obs["model_valid"]
        row["applicability_evidence"] = obs["applicability_evidence"]
        for side in ("model", "reference"):
            row[side] = normalize(obs[side], q)
            row["issues"].extend(f"{side}:{issue}" for issue in row[side]["issues"])
        if not obs["model_valid"]:
            row["issues"].append("model_invalid")
        if q["applicability"] == "unresolved" or (q["applicability"] == "conditional" and not obs["applicability_evidence"].strip()):
            row["issues"].append("unresolved_applicability")
        if observations["execution_status"] != "completed":
            row["issues"].append("execution_" + observations["execution_status"])
        structural = obs.get("structural_evidence")
        if structural is not None:
            obj(structural, ("corresponds", "evidence"), where="structural evidence")
            if type(structural["corresponds"]) is not bool or not isinstance(structural["evidence"], str):
                raise InvalidInput("invalid structural evidence")
            row["structural_evidence"] = copy.deepcopy(structural)
        if q["axis"] == "structural":
            if structural is None or not structural["evidence"].strip():
                row["issues"].append("missing_structural_evidence")
            matched = structural is not None and structural["corresponds"]
        else:
            matched = False
            if row["reference"]["adjusted"] is not None and row["reference"]["adjusted"]["value"] <= 0:
                row["issues"].append("nonpositive_denominator")
            if not row["issues"]:
                ratio = row["model"]["adjusted"]["value"] / row["reference"]["adjusted"]["value"]
                if not finite(ratio):
                    row["issues"].append("nonfinite_ratio")
                else:
                    row["ratio"] = ratio
                    if q["axis"] != "diagnostic":
                        low, high = (.5, 2) if q["axis"] == "cost" else (1 / 3, 3)
                        row["band"] = [low, high]
                        matched = low <= ratio <= high
        if not row["issues"]:
            row["status"] = "pass" if matched else "fail"
            if q["axis"] == "diagnostic":
                row["status"] = "diagnostic"
            elif q["role"] in ("supplied", "held"):
                row["status"] = "informational_match" if matched else "informational_mismatch"
            elif q["exclusion"]:
                row["status"] = "excluded"
            else:
                row["independent_credit"] = matched and q["formal"] and q["axis"] != "diagnostic" and observations["run_kind"] == "blind"
    by_id = {r["id"]: r for r in rows}
    # Dependency validity propagates, but supplied input agreement is never credit.
    for _ in rows:
        changed = False
        for q in manifest["quantities"]:
            row = by_id[q["id"]]
            if any(by_id[d]["status"] == "blocked" for d in q["depends_on"]) and "blocked_dependency" not in row["issues"]:
                row["issues"].append("blocked_dependency")
                row["status"], row["independent_credit"] = "blocked", False
                changed = True
        if not changed:
            break
    reconciliations = []
    contaminated = {q["id"] for q in manifest["quantities"] if q["exclusion"]}
    for _ in rows:
        before = len(contaminated)
        for eq in manifest["accounting"]:
            if contaminated.intersection(eq["children"]):
                contaminated.add(eq["parent"])
        for q in manifest["quantities"]:
            if contaminated.intersection(q["depends_on"]):
                contaminated.add(q["id"])
        if len(contaminated) == before:
            break
    for eq in manifest["accounting"]:
        record = {"id": eq["id"], "parent": eq["parent"], "children": eq["children"], "status": "pass", "sides": {}}
        for side in ("model", "reference"):
            values = [by_id[k].get(side, {}).get("adjusted") for k in [eq["parent"], *eq["children"]]]
            if any(v is None for v in values) or len({(v["unit"], v["basis"]) for v in values if v}) != 1:
                record["sides"][side] = {"status": "blocked", "reason": "missing_or_incompatible_account"}
            else:
                parent, total = values[0]["value"], math.fsum(v["value"] for v in values[1:])
                ok = math.isclose(parent, total, rel_tol=1e-10, abs_tol=1e-8)
                record["sides"][side] = {"status": "pass" if ok else "fail", "parent_value": parent, "children_sum": total, "residual": parent - total}
            if record["sides"][side]["status"] != "pass":
                record["status"] = record["sides"][side]["status"]
        reconciliations.append(record)
    for row in rows:
        row["contains_C220107"] = row["id"] in contaminated
        if row["id"] in contaminated and not row["exclusion"]:
            row["disclosure"] = "Quantity includes or depends on excluded C220107; agreement is footnoted and is not uncontaminated independent evidence."
            row["independent_credit"] = False
    axes = {}
    for axis in ("structural", "derived", "cost"):
        required = [r for r in rows if r["formal"] and r["axis"] == axis and not r["exclusion"] and r["role"] not in ("supplied", "held")]
        axes[axis] = {"required_ids": [r["id"] for r in required], "pass": bool(required) and all(r["status"] == "pass" for r in required)}
    numerical_pass = all(a["pass"] for a in axes.values()) and all(e["status"] == "pass" for e in reconciliations) and observations["execution_status"] == "completed" and all(r["status"] != "blocked" for r in rows if r["formal"])
    constraint_ids = manifest.get("required_constraints", [])
    strings(constraint_ids, "required_constraints")
    constraints_complete = bool(constraint_ids) and set(constraints) == set(constraint_ids)
    return {"schema_version": 1, "notes": observations.get("notes", ""), "run_kind": observations["run_kind"], "execution_status": observations["execution_status"], "rows": rows, "axes": axes, "accounting": reconciliations, "constraints": copy.deepcopy(constraints), "constraints_complete": constraints_complete, "physical_feasibility": observations["execution_status"] == "completed" and constraints_complete and all(constraints.values()), "extrapolations": observations["extrapolations"], "numerical_comparison_pass": numerical_pass, "blind_comparison_pass": numerical_pass and observations["run_kind"] == "blind" and constraints_complete, "pass": numerical_pass and observations["run_kind"] == "blind" and constraints_complete, "qualification": "Numerical comparison does not establish engineering qualification."}


def load_json(path):
    def unique(pairs):
        result = {}
        for key, value in pairs:
            if key in result:
                raise InvalidInput(f"duplicate JSON key: {key}")
            result[key] = value
        return result
    return json.loads(Path(path).read_text(), object_pairs_hook=unique, parse_constant=lambda x: (_ for _ in ()).throw(InvalidInput(f"nonfinite JSON literal {x}")))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", required=True)
    parser.add_argument("--input", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    try:
        report = compare(load_json(args.manifest), load_json(args.input))
        # No nonstandard JSON numbers can escape the report.
        rendered = json.dumps(report, indent=2, sort_keys=True, allow_nan=False) + "\n"
    except (InvalidInput, ValueError, TypeError, KeyError, OverflowError) as exc:
        report = {"schema_version": 1, "pass": False, "error": str(exc)}
        rendered = json.dumps(report, indent=2, sort_keys=True) + "\n"
        Path(args.output).write_text(rendered)
        return 2
    Path(args.output).write_text(rendered)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
