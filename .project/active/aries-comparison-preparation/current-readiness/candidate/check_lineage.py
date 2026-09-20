"""Verify candidate bytes, native integration, full typed inputs and read coverage."""
import argparse
import importlib.util
import json
import sys
from pathlib import Path

from candidate_common import digest, exclusive_document, validate_rules, schema_declarations


def check(root, candidate=None):
    root = Path(root).resolve()
    candidate = Path(candidate or Path(__file__).parent)
    expected = json.loads((candidate/'candidate-identity.json').read_text())
    from runtime_identity import verify as verify_runtime
    runtime_path=candidate/'runtime-requirements.json'
    assert digest(runtime_path) == expected['runtime_requirements_sha256'], 'runtime requirements differ from candidate identity'
    runtime=verify_runtime(json.loads(runtime_path.read_text()))
    rules = json.loads((candidate/'input-rules.json').read_text())
    assert digest(candidate/'input-rules.json') == expected['input_rules_sha256'], 'selected rules differ from candidate identity'
    validate_rules(rules)
    sys.path.insert(0, str(root))
    from scripts.study import indicators, manifest
    package = root/rules['package_path']
    model = json.loads((package/'contracts/model_contract.json').read_text())
    executable = json.loads((package/'contracts/package_contract.json').read_text())
    assert model['semantic_fingerprint'] == expected['semantic_fingerprint']
    assert executable['executable_fingerprint'] == expected['executable_fingerprint']
    spec = importlib.util.spec_from_file_location('candidate_seal_verify', package/'contracts/verify.py')
    verifier = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = verifier
    spec.loader.exec_module(verifier)
    seal = verifier.verify_package(package, 'stellarator_tea', runtime_version='2.0.0', strict=True)
    assert seal.ok, str(seal.diagnostics)
    loaded = manifest.load(root/'exploration/stellarator_e2e/studies/manifest.json')
    manifest.assert_package_identity(loaded, package)
    fingerprint = manifest.indicator_input_fingerprint(package)
    manifest.assert_pin_matches(loaded, fingerprint)
    assert fingerprint['digest'] == expected['indicator_fingerprint']
    parsed = indicators.read_pipelines(package)
    read_paths = parsed.artifact_paths + [package/'contracts/model_contract.json']
    manifest.assert_read_set_covered(read_paths, package, loaded)
    actual_files = {p.resolve().relative_to(package.resolve()).as_posix(): p for p in parsed.input_files}
    assert set(actual_files) == {entry['path'] for entry in rules['input_files']}
    flattened = {}
    for entry in rules['input_files']:
        path = actual_files[entry['path']]
        assert digest(path) == entry['sha256'], entry['path']
        for key, value in json.loads(path.read_text()).items():
            assert key not in flattened or flattened[key] == value, key
            flattened[key] = value
    assert flattened == rules['default_values'], 'frozen raw defaults differ from actual inputs'
    actual_types = schema_declarations(package, model['parameters'])
    assert actual_types == rules['input_types'], 'declared input types changed'
    for name, sha in expected['source_files'].items():
        path = root/name
        assert path.resolve().is_relative_to(root) and not path.is_symlink(), name
        assert digest(path) == sha, name
    integration = json.loads((root/expected['integration_receipt']).read_text())
    assert integration['class'] == 'CANDIDATE', 'native integration did not release candidate'
    for key in ('semantic_fingerprint','executable_fingerprint'):
        assert integration['candidate'][key] == expected[key], key
    assert integration['candidate']['pin'] == fingerprint['digest']
    negative = []
    for path in (package/'uncovered-input.json', root/'outside-package-input.json'):
        try:
            manifest.assert_read_set_covered([path],package,loaded)
        except manifest.ManifestError:
            negative.append(path.name)
        else:
            raise AssertionError(f'uncovered read accepted: {path}')
    return {'status':'pass','semantic_fingerprint':expected['semantic_fingerprint'],
            'executable_fingerprint':expected['executable_fingerprint'],
            'indicator_fingerprint':fingerprint['digest'], 'input_file_count':len(actual_files),
            'input_count':len(flattened),'read_count':len(read_paths),
            'negative_guards':negative,'source_file_count':len(expected['source_files']),
            'integration_receipt':expected['integration_receipt'],'runtime':runtime}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root',type=Path,default=Path.cwd())
    parser.add_argument('--out',type=Path,required=True)
    args=parser.parse_args()
    _,ok=exclusive_document(args.out,lambda:check(args.root),inputs=[Path(__file__).with_name('input-rules.json'),Path(__file__).with_name('candidate-identity.json')])
    return 0 if ok else 1


if __name__=='__main__':
    raise SystemExit(main())
