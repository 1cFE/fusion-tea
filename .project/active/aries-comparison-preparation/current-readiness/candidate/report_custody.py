"""File custody only: no reveal authorization or scientific readiness decision."""
import json
import os
from pathlib import Path
import tarfile

from candidate_common import digest, strict_json, typed, validate_rules
from export_model_values import extract


FIRST = 'first-forward.identity.json'
SCHEMA = 'candidate-report-identity/v1'


def require(condition, message):
    if not condition:
        raise ValueError(message)


def relative(path, directory):
    return os.path.relpath(Path(path).resolve(), Path(directory).resolve())


def read_original(register, original):
    register = Path(register).resolve()
    original = Path(original).resolve()
    require(original == register/FIRST, 'original forward identity must be the declared register receipt')
    receipt = strict_json(original.read_bytes())
    require(receipt.get('schema_version') == SCHEMA and receipt.get('report_kind') == 'forward'
            and receipt.get('state') == 'completed', 'original forward identity is not completed')
    required = {'archive', 'rules', 'request', 'native_result', 'model_export', 'observations',
                'manifest', 'contract', 'package_contract', 'candidate_identity', 'diagnostics', 'report'}
    require(set(receipt['artifacts']) == required, 'original forward artifact inventory differs')
    paths = {}
    for name, row in receipt['artifacts'].items():
        paths[name] = register/row['path']
        require(digest(paths[name]) == row['sha256'], 'original forward artifact changed: '+name)
    native = strict_json(paths['native_result'].read_bytes())
    report = strict_json(paths['report'].read_bytes())
    require(native.get('state') == 'completed' and native.get('run_kind') == 'blind',
            'original forward native result must be completed blind execution')
    require(report.get('report_kind') == 'forward' and report.get('native_result_sha256') == digest(paths['native_result']),
            'original forward report/native join differs')
    require(report.get('custody_artifacts') == {k: v['sha256'] for k, v in receipt['artifacts'].items() if k != 'report'},
            'original forward report/identity artifact joins differ')
    require(receipt.get('executable_fingerprint') == native.get('executable_fingerprint'),
            'original forward executable identity differs')
    return receipt


def validate_artifacts(root, here, paths):
    """Hash real bytes, verify archive members, and reconstruct request/export joins."""
    from build_freeze import verify
    from execute_frozen import select_inputs

    root, here = Path(root).resolve(), Path(here).resolve()
    hashes = {name: digest(path) for name, path in paths.items()}
    archive = verify(paths['archive'])
    require(archive['archive_sha256'] == hashes['archive'], 'archive changed during verification')
    with tarfile.open(paths['archive'], 'r:gz') as tar:
        for name in ('rules', 'manifest', 'contract', 'package_contract', 'candidate_identity', 'diagnostics'):
            path = Path(paths[name]).resolve()
            member = path.relative_to(root).as_posix()
            require(tar.extractfile(member).read() == path.read_bytes(), 'archive/current bytes differ: '+name)
    identity = strict_json(Path(paths['candidate_identity']).read_bytes())
    rules = strict_json(Path(paths['rules']).read_bytes())
    native = strict_json(Path(paths['native_result']).read_bytes())
    request = strict_json(Path(paths['request']).read_bytes())
    manifest = strict_json(Path(paths['manifest']).read_bytes())
    contract = strict_json(Path(paths['contract']).read_bytes())
    package_contract = strict_json(Path(paths['package_contract']).read_bytes())
    require(native.get('state') == 'completed', 'post-reveal custody requires completed native execution')
    require(identity['input_rules_sha256'] == hashes['rules'] == native.get('rules_sha256'), 'rules/native/candidate identity join differs')
    require(native.get('raw_request_sha256') == hashes['request'], 'raw request/native identity differs')
    require(identity['semantic_fingerprint'] == contract['semantic_fingerprint'], 'candidate semantic identity differs')
    require(bool(identity['executable_fingerprint']) and identity['executable_fingerprint'] == native.get('executable_fingerprint'),
            'candidate/native executable identities differ')
    require(identity['executable_fingerprint'] == package_contract['executable_fingerprint'], 'candidate/package executable identities differ')
    for key in ('semantic_fingerprint', 'executable_fingerprint'):
        require(native.get('lineage', {}).get(key) == identity[key], 'native lineage identity differs: '+key)
    selected, classification = select_inputs(rules, request)
    defaults = validate_rules(rules)
    selected = {key: typed(value, rules['input_types'][key], key) for key, value in selected.items()}
    # Mirror the executor's explicitly retained Boolean-default admission.
    selected.update({key: value for key, value in defaults.items() if rules['input_types'][key] == 'bool' and key not in selected})
    require(native.get('requested_overrides') == selected and native.get('effective_inputs') == defaults | selected,
            'request/native selected inputs differ')
    require(all(native.get(key) == value for key, value in classification.items()), 'request/native classification differs')
    require(strict_json(Path(paths['model_export']).read_bytes()) == extract(manifest, contract, native),
            'model export differs from retained native result')
    for name, path in paths.items():
        require(digest(path) == hashes[name], 'artifact changed during validation: '+name)
    return hashes, native


class Register:
    """An exclusive lock plus exclusive identity files; no overwrite or auto-recovery."""
    def __init__(self, directory):
        self.directory = Path(directory).resolve()
        self.directory.mkdir(parents=True, exist_ok=True)
        self.lock = self.directory/'registration.lock'
        with self.lock.open('x') as stream:
            stream.write('In-progress report registration. A crash requires explicit recovery.\n')

    def release(self):
        self.lock.unlink()

    def prepare(self, kind, original, archive_hash, executable):
        if kind == 'forward':
            require(not (self.directory/FIRST).exists(), 'first forward already registered; use corrected or conditioned')
            require(original is None, 'first forward cannot name another original')
            return None
        require(original is not None, 'follow-up requires original forward identity')
        receipt = read_original(self.directory, original)
        require(receipt['artifacts']['archive']['sha256'] == archive_hash, 'follow-up archive differs from original forward')
        require(receipt['executable_fingerprint'] == executable, 'follow-up executable differs from original forward')
        return {'identity_receipt': relative(original, self.directory), 'identity_sha256': digest(original),
                'native_result_sha256': receipt['artifacts']['native_result']['sha256'],
                'report_sha256': receipt['artifacts']['report']['sha256'], 'relationship': kind+' follow-up'}

    def finish(self, kind, report_path, paths, hashes, native, original):
        for name, path in paths.items():
            require(digest(path) == hashes[name], 'artifact changed before registration: '+name)
        if original is not None:
            require(digest(self.directory/original['identity_receipt']) == original['identity_sha256'], 'original identity changed before registration')
            read_original(self.directory, self.directory/original['identity_receipt'])
        receipt = {'schema_version': SCHEMA, 'state': 'completed', 'report_kind': kind,
                   'executable_fingerprint': native['executable_fingerprint'], 'original_forward_result': original,
                   'publication_ready': False, 'authorization': 'Custody does not establish owner reveal or adoption authorization.',
                   'artifacts': {name: {'path': relative(path, self.directory), 'sha256': hashes[name]} for name, path in paths.items()}}
        receipt['artifacts']['report'] = {'path': relative(report_path, self.directory), 'sha256': digest(report_path)}
        target = self.directory/FIRST if kind == 'forward' else Path(str(report_path)+'.identity.json')
        # Serialize before opening so malformed data cannot consume a valid receipt name.
        payload = json.dumps(receipt, indent=2, sort_keys=True, allow_nan=False)+'\n'
        with target.open('x') as stream:
            stream.write(payload)
        return target
