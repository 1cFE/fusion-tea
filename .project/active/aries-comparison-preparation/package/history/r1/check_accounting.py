"""Reconcile retained native results; never execute the physical model."""
import hashlib
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
HERE = Path(__file__).resolve().parent
STUDY = ROOT / 'exploration/stellarator_e2e/studies/20260916-bounded-feasibility-transfer/results/native-cases.json'


def reconcile():
    manifest = json.loads((HERE / 'manifest.json').read_text())
    contract = json.loads((ROOT / manifest['package_path'] / 'contracts/model_contract.json').read_text())
    parameters = {p['qualified_name']: p['default_value'] for p in contract['parameters']}
    channels = set(parameters) | {o['channel_name'] for o in contract['outputs']}
    rows = {q['id']: q for q in manifest['quantities']}
    assert len(rows) == len(manifest['quantities'])
    assert all(q['reference_value'] is None for q in rows.values())
    assert all(p in channels for q in rows.values() for p in q['producers'])
    cases = json.loads(STUDY.read_text())
    for case in cases:
        case['accounting_mode'] = 'retained_bounded_feasibility_study'
    selected_path = HERE / 'selected-mode/native-result.json'
    selected = json.loads(selected_path.read_text())
    assert selected['state'] == 'completed', selected['state']
    cases.append(dict(candidate_id=selected['candidate_id'], inputs=selected['effective_inputs'], outputs=selected['outputs'], accounting_mode='frozen_selected_forward_mode'))
    checks = []
    passthrough_checks = []
    role_condition = manifest["role_audit"]["frozen_condition"]
    contamination = {'C220107'}
    # Propagate only from the declared manifest graph, including non-additive paths.
    while True:
        prior = set(contamination)
        for equation in manifest['accounting']:
            if contamination.intersection(equation['children']):
                contamination.add(equation['parent'])
        for row in rows.values():
            if contamination.intersection(row['depends_on']):
                contamination.add(row['id'])
        if prior == contamination:
            break
    for case in cases:
        values = dict(parameters)
        values.update(case['inputs'])
        values.update(case['outputs'])
        assert values[role_condition['key']] == role_condition['value']
        for row_id in manifest['role_audit']['input_passthrough_output_rows']:
            row = rows[row_id]
            assert row['role'] == 'held' and row['role_input'] in parameters
            output = values[row['producers'][0]]
            selected_input = values[row['role_input']]
            assert output == selected_input, (case['candidate_id'], row_id)
            passthrough_checks.append(dict(candidate_id=case['candidate_id'], row_id=row_id, output=output, input=selected_input, passed=True))
        mapped = {}
        for key, row in rows.items():
            producers = row['producers']
            if len(producers) == 1 and producers[0] in values:
                mapped[key] = values[producers[0]]
            elif row['calculation'] == 'sum of producers in cumulative radial order':
                mapped[key] = sum(values[p] for p in producers)
            elif key == 'recirculating_power':
                mapped[key] = values[producers[0]] - values[producers[1]]
        for equation in manifest['accounting']:
            parent = mapped[equation['parent']]
            child_sum = sum(mapped[c] for c in equation['children'])
            error = parent - child_sum
            passed = math.isclose(parent, child_sum, rel_tol=1e-12, abs_tol=1e-5)
            checks.append(dict(candidate_id=case['candidate_id'], accounting_mode=case['accounting_mode'], equation=equation['id'], parent=parent, child_sum=child_sum, residual=error, passed=passed))
    return dict(schema_version=1, source=str(STUDY.relative_to(ROOT)), source_sha256=hashlib.sha256(STUDY.read_bytes()).hexdigest(), manifest_sha256=hashlib.sha256((HERE/'manifest.json').read_bytes()).hexdigest(), semantic_fingerprint=contract['semantic_fingerprint'], physical_evaluations=0, retained_study_cases=len(cases)-1, selected_mode_case=dict(source=str(selected_path.relative_to(ROOT)), source_sha256=hashlib.sha256(selected_path.read_bytes()).hexdigest(), candidate_id=selected['candidate_id'], accounting_mode='frozen_selected_forward_mode', requested_overrides=selected['requested_overrides'], violated_constraints=[k for k,v in selected['constraints'].items() if v == 'violated']), native_cases=len(cases), equations=len(manifest['accounting']), checks=checks, input_passthrough_checks=passthrough_checks, all_passed=all(x['passed'] for x in checks), max_absolute_residual=max(abs(x['residual']) for x in checks), tolerance={'relative':1e-12,'absolute_USD':1e-5}, c220107_contaminated_rows=sorted(contamination), unresolved_charges={'manufacturing_remainder':None,'additional_loop_installed':None}, limitations=['Arithmetic checks do not establish scope completeness or common-year currency','Retained native-case summaries supply numerical values; coordinator verifies immutable store joins and lineage','No reference values or new physical evaluations'])


if __name__ == '__main__':
    result = reconcile()
    (HERE / 'reconciliation.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps({k: v for k, v in result.items() if k not in ('checks', 'input_passthrough_checks')}, indent=2))
    raise SystemExit(0 if result['all_passed'] else 1)
