"""Pinned, separate diagnostic assessment of the retained post-reveal request."""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import re
import sys
import tarfile
import tempfile
import traceback

HERE = Path(__file__).resolve().parent
TASK = HERE.parent
COMPARISON = TASK.parent
ROOT = COMPARISON.parents[2]
PRIOR = COMPARISON / 'post-reveal-results/post-reveal-v1'
PREP = COMPARISON / 'post-reveal-preparation'
IMPL = COMPARISON / 'post-reveal-investigation/failure-propagation'
ARCHIVE = PREP / 'package/post-reveal-v1.tar.gz'
IDENTITY = TASK / 'adoption.json'


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def load(path):
    return json.loads(Path(path).read_bytes())


def write(path, value):
    with Path(path).open('x') as stream:
        json.dump(value, stream, indent=2, sort_keys=True, allow_nan=False)
        stream.write('\n')


def verify():
    identity = load(IDENTITY)
    for key, expected in identity['files'].items():
        if sha(ROOT / key) != expected:
            raise ValueError('adopted file changed: ' + key)
    code_files = {str(p.relative_to(ROOT)) for p in HERE.glob('*.py')}
    if not code_files <= identity['files'].keys():
        raise ValueError('untracked runner code')
    runtime = load(IMPL / 'implementation-identity.json')
    for key, expected in runtime['files'].items():
        if sha(IMPL / key) != expected:
            raise ValueError('reviewed runtime changed: ' + key)
    actual = {str(p.relative_to(IMPL)) for p in (IMPL / 'native-teax').rglob('*.py')}
    if not actual <= runtime['files'].keys():
        raise ValueError('untracked runtime code')
    return identity


def reserve(store, name):
    if not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9_.-]*', name):
        raise ValueError('invalid diagnostic attempt name')
    store.mkdir(parents=True, exist_ok=True)
    out = store / name
    out.mkdir()
    write(out / 'reservation.json', {'attempt': name, 'kind': 'partial_diagnostic',
                                   'original_first_forward_replaced': False})
    try:
        os.link(out / 'reservation.json', store / 'first-diagnostic.json')
    except FileExistsError:
        pass
    first = load(store / 'first-diagnostic.json')
    if first.get('kind') != 'partial_diagnostic' or not (store / first['attempt']).is_dir():
        raise ValueError('invalid first-diagnostic pointer')
    return out, first


def import_file(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def verify_loaded_runtime(expected_digest):
    import simkit.core.pipeline_executor as executor
    import simkit.evaluation.evaluator as evaluator
    import simkit.evaluation.diagnostics as diagnostics
    for module in (executor, evaluator, diagnostics):
        expected = IMPL / 'native-teax' / (module.__name__.replace('.', '/') + '.py')
        if Path(module.__file__).resolve() != expected.resolve():
            raise ValueError('runtime import did not use adopted source: ' + module.__name__)
    if diagnostics.source_digest() != expected_digest:
        raise ValueError('loaded runtime source digest differs from adopted runtime')


def execute(store, name):
    out, first = reserve(Path(store).resolve(), name)
    result = {'schema_version': 'partial-diagnostic-attempt/v1', 'state': 'refused',
              'first_diagnostic': first, 'native_execution_started': False,
              'original_first_forward_replaced': False, 'engineering_acceptance': False}
    try:
        identity = verify()
        result['adoption_sha256'] = sha(IDENTITY)
        request_path = PRIOR / 'attempts/first-forward/request.raw.json'
        (out / 'request.raw.json').write_bytes(request_path.read_bytes())
        prior = load(PRIOR / 'attempts/first-forward/result.json')
        with tempfile.TemporaryDirectory(prefix='partial-assessment-') as temporary:
            restored = Path(temporary)
            with tarfile.open(ARCHIVE) as archive:
                archive.extractall(restored, filter='data')
            tools = restored / PREP.relative_to(ROOT) / 'tools'
            adapter = import_file('partial_frozen_adapter', tools / 'adapter.py')
            old_identity = adapter.verify_identity()
            contract = load(adapter.PACKAGE / 'contracts/model_contract.json')
            point, selection = adapter.select(adapter.strict(request_path.read_bytes()), adapter.defaults(contract))
            if (selection['effective_inputs'] != prior['effective_inputs'] or
                    selection['input_roles'] != prior['input_roles'] or point != prior['requested_overrides']):
                raise ValueError('original input selection changed')
            if len(selection['effective_inputs']) != 704:
                raise ValueError('original input inventory changed')
            write(out / 'selection.json', selection | {'requested_overrides': point})
            sys.path.insert(0, str(restored))
            sys.path.insert(0, str(IMPL / 'native-teax'))
            from simkit.study.bridge import CandidateBridge
            from simkit.evaluation.diagnostics import source_digest
            from exploration.stellarator_e2e.studies import study_route as route
            from qualification import qualify
            from definedness import assess_definedness
            from reporting import build_report
            verify_loaded_runtime(identity['native_source_digest'])
            if not Path(route.__file__).resolve().is_relative_to(restored):
                raise ValueError('route did not load from adopted archive')
            prepared = route.prepare(adapter.PACKAGE, restored / 'working')
            if prepared.fingerprint != old_identity['executable_fingerprint']:
                raise ValueError('generated executable identity changed')
            typed = CandidateBridge(prepared.entry_models).build(selection['effective_inputs'])
            entered = {k: v for entry in typed.values() for k, v in entry.model_dump().items()}
            if entered != selection['effective_inputs']:
                raise ValueError('typed entry changed a selected design choice')
            write(out / 'execution-started.json', {'typed_input_count': len(entered),
                 'original_effective_inputs_exact': True, 'archive_sha256': sha(ARCHIVE),
                 'native_source_digest': source_digest(), 'executable_fingerprint': prepared.fingerprint})
            result['native_execution_started'] = True
            diagnostic = prepared.diagnose(typed).to_document()
            write(out / 'native-diagnostic.json', diagnostic)
            if {k: v for entry in typed.values() for k, v in entry.model_dump().items()} != entered:
                raise ValueError('native evaluation mutated selected inputs')
            qualifications = qualify(prepared._graph, diagnostic, contract)
            definedness = assess_definedness(prepared._graph, diagnostic)
            write(out / 'field-qualification.json', qualifications)
            write(out / 'model-definedness.json', definedness)
            manifest = load(tools / 'historical-manifest.json')
            observations = load(PRIOR / 'observations.json')
            report = build_report(diagnostic, qualifications, selection, manifest,
                                  load(tools / 'current-overlay.json'), observations, contract, definedness)
            if [r['id'] for r in report['rows']] != [q['id'] for q in manifest['quantities']]:
                raise ValueError('comparison row inventory changed')
            if set(report['predicates']) != {p['constraint_id'] for p in contract['constraint_catalog']['concrete_entries']}:
                raise ValueError('predicate inventory changed')
            assert report['row_count'] == 276 and report['predicate_count'] == 67
            write(out / 'report.json', report)
            adapter.verify_identity()
            verify()
            result.update(state='partial_assessment_recorded', native_state=diagnostic['state'],
                          original_effective_inputs_exact=True, design_choices_preserved=True,
                          source_identity=diagnostic['provenance'],
                          counts={k: report[k] for k in ('numeric_output_count', 'predicate_count', 'row_count',
                                                       'predicate_counts', 'row_counts', 'field_row_counts')})
    except Exception as exc:
        result.update(error=f'{type(exc).__name__}: {exc}')
        (out / 'exception.txt').write_text(traceback.format_exc())
    write(out / 'result.json', result)
    write(out / 'receipt.json', {'artifacts': {p.name: sha(p) for p in sorted(out.iterdir()) if p.is_file()},
                                'adoption_sha256': sha(IDENTITY)})
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--verify', action='store_true')
    parser.add_argument('--store', type=Path)
    parser.add_argument('--name')
    args = parser.parse_args()
    if args.verify:
        verify()
        print('Pinned runner, archive, original request and reviewed runtime verified')
        return 0
    if not args.store or not args.name:
        parser.error('--store and --name required')
    result = execute(args.store, args.name)
    print(json.dumps(result, indent=2))
    return 0 if result['state'] == 'partial_assessment_recorded' else 1


if __name__ == '__main__':
    raise SystemExit(main())
