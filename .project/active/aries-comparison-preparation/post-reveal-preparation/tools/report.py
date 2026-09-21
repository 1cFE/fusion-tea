"""Post-reveal comparison report with retained attempt custody and historical criteria."""
import argparse
import copy
import sys
from pathlib import Path
import adapter as a


def report(attempt, observations, store, name):
    out, first = a.reserve(store, name)
    result = {'report_kind': 'post_reveal_comparison', 'blind': False,
              'publication_ready': False, 'first_report_attempt': first}
    try:
        a.verify_identity()
        attempt = Path(attempt).resolve()
        if not attempt.is_dir():
            raise ValueError('execution attempt directory does not exist')
        pointer = attempt.parent / 'first-attempt.json'
        first_execution = a.strict(pointer.read_bytes()) | {'pointer_sha256': a.sha(pointer)}
        if set(first_execution) != {'schema_version', 'attempt', 'pointer_sha256'} or first_execution['schema_version'] != 'first-attempt/v1' or not a.re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9_.-]*', first_execution['attempt']):
            raise ValueError('invalid first execution pointer')
        if not (attempt.parent / first_execution['attempt']).is_dir():
            raise ValueError('first execution directory missing')
        interrupted = not a.terminal_custody(attempt)
        if interrupted:
            native = {'state': 'interrupted', 'first_attempt': first_execution, 'verdicts': {},
                      'outputs': {}, 'effective_inputs': {}, 'input_roles': {}, 'purpose': None}
            if (attempt / 'request.raw.json').exists():
                try:
                    native['purpose'] = a.strict((attempt / 'request.raw.json').read_bytes()).get('purpose')
                except ValueError:
                    pass
        else:
            receipt = a.strict((attempt / 'receipt.json').read_bytes())
            for path, digest in receipt['artifacts'].items():
                if a.sha(attempt / path) != digest:
                    raise ValueError('attempt receipt mismatch: ' + path)
            native = a.strict((attempt / 'result.json').read_bytes())
            if native.get('identity_sha256', a.sha(a.HERE / 'identity.json')) != a.sha(a.HERE / 'identity.json'):
                raise ValueError('attempt/package identity mismatch')
            if native['first_attempt'] != first_execution:
                raise ValueError('first-attempt pointer differs from retained custody')
        evidence = {str(p.relative_to(attempt)):a.sha(p) for p in sorted(attempt.rglob('*')) if p.is_file()}
        raw = Path(observations).read_bytes()
        (out / 'observations.raw.json').write_bytes(raw)
        obs = a.strict(raw)
        if obs['run_kind'] != 'conditioned':
            raise ValueError('post-reveal observations use conditioned comparison semantics')
        state = 'completed' if native['state'] == 'completed' else 'refused' if native['state'] == 'execution_refused' else 'failed'
        if obs['execution_status'] != state or obs['constraints'] != {k:v == 'satisfied' for k,v in native.get('verdicts',{}).items()}:
            raise ValueError('observations/native execution or predicates mismatch')
        manifest = a.strict((a.HERE / 'historical-manifest.json').read_bytes())
        contract = a.strict((a.PACKAGE / 'contracts/model_contract.json').read_bytes())
        exported = a.export(native, manifest, contract)
        if not interrupted and exported != a.strict((attempt / 'model-export.json').read_bytes()):
            raise ValueError('retained export differs from native evidence')
        sys.path.insert(0, str(a.ROOT))
        from scripts.compare_fixed_point import compare, normalize
        current = copy.deepcopy(manifest)
        mapped = {r['id']:r for r in exported['rows']}
        for q in current['quantities']:
            actual = mapped[q['id']]
            q['role'] = actual['role'] if actual['role'] in ('held','supplied') else 'derived'
            row = obs['quantities'].get(q['id'])
            if row is None:
                continue
            if q['axis'] == 'structural':
                if native['state'] != 'completed' and row['model_valid']:
                    raise ValueError('failed execution cannot supply valid structural prediction')
                continue
            normalized = normalize(row['model'], q)
            if actual['status'] == 'mapped':
                if normalized['issues'] or normalized['adjusted'] is None or normalized['adjusted']['value'] != actual['value']:
                    raise ValueError('model observation differs from retained output: ' + q['id'])
            elif row['model_valid'] or row['model']['value'] is not None:
                raise ValueError('unavailable native prediction must remain unavailable: ' + q['id'])
        current['required_constraints'] = [row['constraint_id'] for row in contract['constraint_catalog']['concrete_entries']]
        numerical = compare(current, obs)
        numerical.update(run_kind='post_reveal_comparison', blind_comparison_pass=False, **{'pass': False})
        for row in numerical['rows']:
            row['independent_credit'] = False
            row['native_prediction_status'] = mapped[row['id']]['status']
        a.verify_identity()
        result.update(state='reported', numerical_comparison=numerical,
                      native_result_sha256=a.sha(attempt / 'result.json') if not interrupted else None,
                      attempt_path=str(attempt), attempt_artifacts=evidence, interrupted=interrupted,
                      observations_sha256=a.sha(out / 'observations.raw.json'),
                      identity_sha256=a.sha(a.HERE / 'identity.json'),
                      first_execution_attempt=native['first_attempt'],
                      purpose=native.get('purpose'), current_predicates=native.get('verdicts',{}),
                      selection={k:native.get(k) for k in ('held_fallback','missing_proposed_inputs','fully_reference_specified')},
                      engineering_acceptance_withheld=True,
                      qualification='Post-reveal conditional comparison. Historical criteria/accounting retained; engineering qualification and unresolved source correspondence remain separate.')
    except Exception as exc:
        result.update(state='report_refused', error=f'{type(exc).__name__}: {exc}')
    a.document(out / 'report.json', result)
    a.document(out / 'receipt.json', {'artifacts':{p.name:a.sha(p) for p in out.iterdir() if p.is_file()}})
    return result


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--attempt-dir',required=True,type=Path)
    p.add_argument('--observations',required=True,type=Path)
    p.add_argument('--store',required=True,type=Path)
    p.add_argument('--name',required=True)
    args=p.parse_args()
    r=report(args.attempt_dir,args.observations,args.store,args.name)
    print(r['state'])
    return 0 if r['state']=='reported' else 1

if __name__=='__main__':
    raise SystemExit(main())
