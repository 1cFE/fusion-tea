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
import tempfile
from pathlib import Path


def numeric(value, label):
    if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value):
        raise ValueError(f"{label}: finite numeric value required")
    return float(value)


def select_inputs(rules, request):
    from candidate_common import validate_rules
    validate_rules(rules)
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
    if not isinstance(conditioned, dict):
        raise ValueError('conditioned_values must be an object')
    seam_record = {}
    seam = {}
    if kind != "conditioned" and (seam_id is not None or conditioned):
        raise ValueError("blind/verification runs cannot select a conditioned seam")
    if kind == "conditioned":
        seams = {row["id"]: row for row in rules["conditioned_seams"]}
        if seam_id not in seams:
            raise ValueError("unknown conditioned seam")
        seam_record = seams[seam_id]
        seam = seam_record["keys"]
        if seam_id == 'table5_geometry_field' and (supplied or conditioned):
            raise ValueError('fixed Table5 control requires empty values and conditioned_values')
        if set(supplied) & set(seam):
            raise ValueError("independent inputs overlap the selected conditioned seam")
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
        "conditioned_input_keys": sorted(seam),
        "conditioned_input_roles": {
            key: seam_record.get("input_roles", {}).get(key, "supplied") for key in seam
        },
        "conditioned_supplied_quantities": seam_record.get("supplied_quantities", {}),
        "conditioned_output_roles": seam_record.get("output_roles", {}),
        "independent_prediction_credit_for_supplied": False,
        "scope_decision": rules["scope_decision"],
    }


def execute(root, rules_path, request, out):
    """Retain raw request and all pre-execution refusals in an exclusive attempt."""
    from candidate_common import digest, typed, validate_rules, attempt_identity, strict_json
    from check_lineage import check
    root, rules_path, out = Path(root).resolve(), Path(rules_path).resolve(), Path(out).resolve()
    try:
        out.mkdir(parents=True, exist_ok=False)
    except FileExistsError:
        rejection = Path(tempfile.mkdtemp(prefix=out.name+'.overwrite-refused-', dir=out.parent))
        result = {'state':'execution_refused','refusal_stage':'attempt_creation',
                  'error':'requested attempt already exists', 'requested_directory':str(out),
                  'native_execution_started':False, 'all_constraints_satisfied':False}
        (rejection/'native-result.json').write_text(json.dumps(result,indent=2)+'\n')
        attempt_identity(rejection)
        return result
    stage = 'request'
    result = {'state': 'execution_refused', 'run_kind': None,
              'native_execution_started':False, 'attempt_id':out.name,
              'request_source':str(request) if isinstance(request,Path) else 'in-memory request'}
    try:
        raw = request.read_bytes() if isinstance(request, Path) else json.dumps(request).encode()
        (out / 'request.raw.json').write_bytes(raw)
        result['raw_request_sha256'] = hashlib.sha256(raw).hexdigest()
        stage = 'request_decode'
        parsed_request = strict_json(raw)
        if not isinstance(parsed_request, dict):
            raise ValueError('request must be an object')
        (out/'request.json').write_text(json.dumps(parsed_request,indent=2)+'\n')
        stage = 'rules'
        if rules_path != rules_path.with_name('input-rules.json'):
            raise ValueError('candidate requires its canonical input-rules.json')
        rules = strict_json(rules_path.read_text())
        normalized_defaults = validate_rules(rules)
        stage = 'selection'
        point, classification = select_inputs(rules, parsed_request)
        point = {key: typed(value, rules['input_types'][key], key) for key, value in point.items()}
        # Numeric Boolean defaults in the generator are normalized explicitly;
        # preserve their original file values separately, without type inference.
        point.update({key: value for key, value in normalized_defaults.items()
                      if rules['input_types'][key] == 'bool' and key not in point})
        result.update(classification, requested_overrides=point,
                      effective_inputs=normalized_defaults | point,
                      rules_sha256=digest(rules_path), reference_data='none' if classification['run_kind']=='verification' else 'caller supplied; request retained')
        stage = 'identity'
        lineage = check(root, rules_path.parent)
        if digest(rules_path) != result['rules_sha256']:
            raise ValueError('selected rules changed during lineage verification')
        result['lineage'] = lineage
        groups = {}
        for entry in rules['input_files']:
            path = root / rules['package_path'] / entry['path']
            if digest(path) != entry['sha256']:
                raise ValueError('frozen input file changed: '+entry['path'])
            groups[entry['path']] = json.loads(path.read_text())
        result['original_input_groups'] = groups
        sys.path.insert(0, str(root))
        sys.path.insert(0, str(Path(os.environ['STOP_PARSER_TEAX_ROOT'])/'packages/teax-simkit'))
        from exploration.stellarator_e2e.studies import study_route as route
        package = root / rules['package_path']
        contract = json.loads((package/'contracts/model_contract.json').read_text())
        numeric_channels = {r['channel_name']:r['channel_name'] for r in contract['outputs'] if r['python_type'] in ('float','int','bool')}
        stage = 'native_execution'
        result['native_execution_started'] = True
        cases, db = route.run_points('current-comparison-fixed-point', [point], out/'native', package, required_channels=numeric_channels)
        if len(cases) != 1:
            raise ValueError('native route did not retain exactly one requested case')
        case = cases[0]
        result.update(state=case.state, candidate_id=case.candidate_id,
                      executable_fingerprint=case.executable_fingerprint, outputs=dict(case.outputs),
                      verdicts=dict(case.verdicts), store=str(db.relative_to(out)))
        if case.state == 'completed':
            route.require_published(case, numeric_channels)
            expected_ids = {e['constraint_id'] for e in contract['constraint_catalog']['concrete_entries']}
            if set(case.verdicts) != expected_ids or any(v not in ('satisfied','violated') for v in case.verdicts.values()):
                raise ValueError('incomplete or invalid native verdict inventory')
            result['constraints'] = route.short_verdicts(case, package)
            result['all_constraints_satisfied'] = all(v=='satisfied' for v in case.verdicts.values())
        else:
            result['error'] = 'native case did not complete; inspect retained store'
    except Exception as error:
        result.update(state='execution_refused', refusal_stage=stage, error=f'{type(error).__name__}: {error}', all_constraints_satisfied=False)
    def retain_nonfinite(value):
        if isinstance(value, float) and not math.isfinite(value):
            return {'nonfinite_value':repr(value)}
        if isinstance(value, dict):
            return {key:retain_nonfinite(item) for key,item in value.items()}
        if isinstance(value, list):
            return [retain_nonfinite(item) for item in value]
        return value
    raw_payload = json.dumps(result,indent=2,sort_keys=True)
    serializable = retain_nonfinite(result)
    if serializable != result:
        (out/'native-result.raw.json').write_text(raw_payload+'\n')
        result = serializable
        result.update(state='invalid_native_result',refusal_stage='result_validation',
                      error='Nonfinite native value; exact raw representation and tagged values retained',
                      all_constraints_satisfied=False)
    with (out/'native-result.json').open('x') as stream:
        stream.write(json.dumps(result, indent=2, sort_keys=True, allow_nan=False)+'\n')
    attempt_identity(out)
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=Path.cwd())
    parser.add_argument('--rules', type=Path, default=Path(__file__).with_name('input-rules.json'))
    parser.add_argument('--request', type=Path, required=True)
    parser.add_argument('--out-dir', type=Path, required=True)
    args = parser.parse_args()
    result = execute(args.root, args.rules, args.request, args.out_dir)
    print(result['state'])
    return 0 if result['state']=='completed' else 1


if __name__ == '__main__':
    raise SystemExit(main())
