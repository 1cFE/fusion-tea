"""Synthetic custody artifacts only; no plant, holdout data, reveal or adoption."""
import json
from pathlib import Path
import sys
from concurrent.futures import ThreadPoolExecutor

import pytest

ROOT = Path(__file__).resolve().parents[1]
HERE = ROOT/'.project/active/aries-comparison-preparation/current-readiness/candidate'
sys.path.insert(0, str(HERE))
from candidate_common import digest, validate_rules, typed
from compare_candidate import write_report
from execute_frozen import select_inputs
from export_model_values import extract
from report_custody import FIRST, Register, read_original


def put(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2)+'\n')
    return path


@pytest.fixture
def bundle(tmp_path):
    """Use the fixed selection/comparison schema with synthetic execution identities."""
    from build_freeze import build
    here = tmp_path/'candidate'
    rules = json.loads((HERE/'input-rules.json').read_text())
    manifest = json.loads((HERE/'manifest.json').read_text())
    manifest['package_path'] = 'pkg'
    put(here/'input-rules.json', rules)
    put(here/'manifest.json', manifest)
    put(here/'diagnostic-inventory.json', {'diagnostics': [], 'unresolved_essential_evidence': ['Synthetic unresolved science']})
    contract = {'semantic_fingerprint': 'synthetic-semantic',
                'parameters': [{'qualified_name': k, 'default_value': v} for k, v in rules['default_values'].items()],
                'constraint_catalog': {'concrete_entries': [{'constraint_id': cid, 'evaluation_channel': cid+'__evaluation'} for cid in manifest['required_constraints']]}}
    put(tmp_path/'pkg/contracts/model_contract.json', contract)
    put(tmp_path/'pkg/contracts/package_contract.json', {'executable_fingerprint': 'synthetic-executable'})
    identity = {'status': 'draft_candidate', 'base_revision': 'synthetic-base',
                'semantic_fingerprint': 'synthetic-semantic', 'executable_fingerprint': 'synthetic-executable',
                'input_rules_sha256': digest(here/'input-rules.json')}
    put(here/'candidate-identity.json', identity)
    put(here/'archive-members.json', [p.relative_to(tmp_path).as_posix() for p in tmp_path.rglob('*.json')])
    build(tmp_path, here, tmp_path/'synthetic-archive')
    return {'root': tmp_path, 'here': here, 'rules': rules, 'manifest': manifest, 'contract': contract,
            'result_register': tmp_path/'register', 'archive': tmp_path/'synthetic-archive/comparison-freeze.tar.gz'}


def execution(bundle, name='first', kind='blind', state='completed'):
    here = bundle['root']/name
    request = {'run_kind': kind, 'values': {}}
    if kind == 'conditioned':
        request.update(conditioned_seam='table5_geometry_field', conditioned_values={})
    request_path = put(here/'request.raw.json', request)
    rules = bundle['rules']
    selected, classification = select_inputs(rules, request)
    defaults = validate_rules(rules)
    selected = {key: typed(value, rules['input_types'][key], key) for key, value in selected.items()}
    selected.update({key: value for key, value in defaults.items() if rules['input_types'][key] == 'bool' and key not in selected})
    native = classification | {'candidate_id': 'synthetic-'+name, 'state': state,
        'executable_fingerprint': 'synthetic-executable', 'rules_sha256': digest(bundle['here']/'input-rules.json'),
        'raw_request_sha256': digest(request_path), 'requested_overrides': selected, 'effective_inputs': defaults | selected,
        'outputs': {}, 'verdicts': {cid: 'violated' for cid in bundle['manifest']['required_constraints']},
        'lineage': {'semantic_fingerprint': 'synthetic-semantic', 'executable_fingerprint': 'synthetic-executable'}}
    native_path = put(here/'native-result.json', native)
    exported = put(here/'model-export.json', extract(bundle['manifest'], bundle['contract'], native))
    observation = {'schema_version': 1, 'run_kind': kind, 'execution_status': 'completed' if state == 'completed' else 'refused',
                   'constraints': {cid: False for cid in native['verdicts']}, 'extrapolations': [], 'quantities': {}}
    return {'native_path': native_path, 'observation_path': put(here/'observations.json', observation),
            'request': request_path, 'model_export': exported}


def write(bundle, files, name, **options):
    args = {key: bundle[key] for key in ('here', 'result_register', 'archive')}
    args.update(files)
    args.update(options)
    return write_report(bundle['root'], out=bundle['root']/name, **args)


def test_forward_registers_failed_comparison_and_engineering_result(bundle):
    files = execution(bundle)
    report, ok = write(bundle, files, 'report.json', report_kind='forward')
    assert ok and not report['publication_ready']
    assert not report['numerical_comparison']['numerical_comparison_pass']
    assert report['engineering_evidence']['engineering_acceptance_withheld']
    receipt = read_original(bundle['result_register'], bundle['result_register']/FIRST)
    assert receipt['artifacts']['report']['sha256'] == digest(bundle['root']/'report.json')
    assert 'report' not in report['custody_artifacts']
    assert len(receipt['artifacts']) == 12
    assert not receipt['publication_ready']


def test_differently_named_second_forward_cannot_replace_original(bundle):
    files = execution(bundle)
    assert write(bundle, files, 'a.json', report_kind='forward')[1]
    first = (bundle['result_register']/FIRST).read_bytes()
    report, ok = write(bundle, execution(bundle, 'later'), 'b.json', report_kind='forward')
    assert not ok and 'already registered' in report['error']
    assert (bundle['result_register']/FIRST).read_bytes() == first


@pytest.mark.parametrize('kind,native_kind', [('conditioned', 'conditioned'), ('corrected', 'blind')])
def test_followup_names_original_identity_and_own_kind(bundle, kind, native_kind):
    assert write(bundle, execution(bundle), 'a.json', report_kind='forward')[1]
    original = bundle['result_register']/FIRST
    report, ok = write(bundle, execution(bundle, 'later', native_kind), 'b.json', report_kind=kind,
                       original_identity=original, correction_reason='Synthetic transcription correction' if kind == 'corrected' else None)
    assert ok and report['report_kind'] == kind
    assert report['original_forward_result']['identity_sha256'] == digest(original)
    assert (bundle['root']/'b.json.identity.json').exists()
    assert not report['publication_ready']


@pytest.mark.parametrize('kind', ['verification', 'conditioned', 'blind'])
def test_preparation_never_requires_or_creates_original(bundle, kind):
    files = execution(bundle, kind=kind)
    report, ok = write_report(bundle['root'], files['native_path'], files['observation_path'], bundle['root']/'prep.json', here=bundle['here'])
    assert ok and report['report_kind'] == 'preparation'
    assert not report['numerical_comparison']['blind_comparison_pass']
    assert all(not row['independent_credit'] for row in report['numerical_comparison']['rows'])
    assert not (bundle['result_register']/FIRST).exists()
    assert report['original_forward'] is None


@pytest.mark.parametrize('artifact', ['archive', 'request', 'model_export', 'rules', 'native_result'])
def test_mismatched_bytes_refuse_and_retain_inputs(bundle, artifact):
    files = execution(bundle)
    paths = files | {'archive': bundle['archive'], 'rules': bundle['here']/'input-rules.json', 'native_result': files['native_path']}
    path = paths[artifact]
    if artifact == 'archive':
        path.write_bytes(b'not an archive')
    else:
        value = json.loads(path.read_text())
        value['synthetic_tamper'] = True
        if artifact == 'native_result':
            value['raw_request_sha256'] = 'false claim'
        put(path, value)
    result, ok = write(bundle, files, 'refusal.json', report_kind='forward')
    assert not ok and result['state'] == 'refused'
    assert list(bundle['root'].glob('refusal.json.attempt-*/input-0.raw'))
    assert not (bundle['result_register']/FIRST).exists()


def test_missing_archive_is_not_replaced_by_caller_hash(bundle):
    files = execution(bundle)
    bundle['archive'].unlink()
    result, ok = write(bundle, files, 'missing.json', report_kind='forward')
    assert not ok and 'FileNotFoundError' in result['error']
    assert not (bundle['result_register']/FIRST).exists()


def test_missing_candidate_identity_refuses(bundle):
    files = execution(bundle)
    (bundle['here']/'candidate-identity.json').unlink()
    assert not write(bundle, files, 'missing.json', report_kind='forward')[1]


def test_uncompleted_native_never_reserves_first(bundle):
    files = execution(bundle, state='execution_refused')
    result, ok = write(bundle, files, 'failed.json', report_kind='forward')
    assert not ok and 'completed native' in result['error']
    assert not (bundle['result_register']/FIRST).exists()
    assert write(bundle, execution(bundle, 'completed'), 'later.json', report_kind='forward')[1]


def test_raw_malformed_observations_retained_and_original_name_not_consumed(bundle):
    files = execution(bundle)
    files['observation_path'].write_bytes(b'{malformed')
    result, ok = write(bundle, files, 'bad.json', report_kind='forward')
    assert not ok
    assert next(bundle['root'].glob('bad.json.attempt-*/input-1.raw')).read_bytes() == b'{malformed'
    assert not (bundle['result_register']/FIRST).exists()


def test_existing_destination_refuses_before_parser_and_preserves_bytes(bundle):
    files = execution(bundle)
    out = bundle['root']/'same.json'
    out.write_bytes(b'original exact bytes')
    files['observation_path'].write_bytes(b'{')
    with pytest.raises(FileExistsError):
        write(bundle, files, out.name, report_kind='forward')
    assert out.read_bytes() == b'original exact bytes'
    assert list(bundle['root'].glob('same.json.overwrite-refused-*/receipt.json'))


def test_concurrent_different_reports_yield_one_original(bundle):
    files = execution(bundle)
    with ThreadPoolExecutor(max_workers=2) as pool:
        results = list(pool.map(lambda name: write(bundle, files, name, report_kind='forward'), ['one.json', 'two.json']))
    assert sum(ok for _, ok in results) == 1
    read_original(bundle['result_register'], bundle['result_register']/FIRST)


def test_concurrent_same_destination_yields_one_writer(bundle):
    files = execution(bundle)
    def attempt(_):
        try:
            return write(bundle, files, 'same.json', report_kind='forward')[1]
        except FileExistsError:
            return False
    with ThreadPoolExecutor(max_workers=2) as pool:
        assert sum(pool.map(attempt, range(2))) == 1


@pytest.mark.parametrize('artifact', ['report', 'native_result', 'model_export', 'request', 'archive'])
def test_changed_original_artifact_refuses_followup(bundle, artifact):
    assert write(bundle, execution(bundle), 'a.json', report_kind='forward')[1]
    identity = bundle['result_register']/FIRST
    receipt = json.loads(identity.read_text())
    target = bundle['result_register']/receipt['artifacts'][artifact]['path']
    target.write_bytes(target.read_bytes()+b' ')
    result, ok = write(bundle, execution(bundle, 'later', 'conditioned'), 'b.json', report_kind='conditioned', original_identity=identity)
    assert not ok


def test_corrected_requires_reason_and_original_receipt(bundle):
    assert write(bundle, execution(bundle), 'a.json', report_kind='forward')[1]
    files = execution(bundle, 'later')
    assert not write(bundle, files, 'no-reason.json', report_kind='corrected', original_identity=bundle['result_register']/FIRST)[1]
    assert not write(bundle, files, 'no-original.json', report_kind='corrected', correction_reason='Synthetic correction')[1]


def test_identity_failure_keeps_register_blocked_for_explicit_recovery(bundle, monkeypatch):
    def fail(*args, **kwargs):
        raise OSError('synthetic receipt write failure')
    monkeypatch.setattr(Register, 'finish', fail)
    report, ok = write(bundle, execution(bundle), 'a.json', report_kind='forward')
    assert not ok and report['report_kind'] == 'forward'
    assert (bundle['result_register']/'registration.lock').exists()
    assert (bundle['root']/'a.json.custody-refusal.json').exists()
    assert not (bundle['result_register']/FIRST).exists()


@pytest.mark.parametrize('field', ['requested_overrides', 'effective_inputs', 'held_fallback', 'lineage'])
def test_rehashed_native_claims_still_need_request_and_identity_joins(bundle, field):
    files = execution(bundle)
    native = json.loads(files['native_path'].read_text())
    native[field] = False if field == 'held_fallback' else {}
    put(files['native_path'], native)
    # Even a freshly regenerated export cannot make the wrong request joins valid.
    put(files['model_export'], extract(bundle['manifest'], bundle['contract'], native))
    result, ok = write(bundle, files, 'wrong-join.json', report_kind='forward')
    assert not ok and any(word in result['error'] for word in ('selected inputs', 'classification', 'lineage'))


def test_post_validation_artifact_change_cannot_receive_identity(bundle, monkeypatch):
    import compare_candidate
    actual = compare_candidate.compare
    files = execution(bundle)
    def changed(*args, **kwargs):
        report = actual(*args, **kwargs)
        files['model_export'].write_bytes(files['model_export'].read_bytes()+b' ')
        return report
    monkeypatch.setattr(compare_candidate, 'compare', changed)
    report, ok = write(bundle, files, 'race.json', report_kind='forward')
    assert not ok and report['report_kind'] == 'forward'
    assert not (bundle['result_register']/FIRST).exists()
    assert (bundle['result_register']/'registration.lock').exists()


def test_original_register_bundle_can_relocate_together(bundle, tmp_path):
    import shutil
    assert write(bundle, execution(bundle), 'a.json', report_kind='forward')[1]
    relocated = tmp_path.parent/(tmp_path.name+'-relocated')
    shutil.copytree(tmp_path, relocated)
    receipt = read_original(relocated/'register', relocated/'register'/FIRST)
    assert receipt['state'] == 'completed'


def test_different_original_register_is_not_accepted(bundle):
    assert write(bundle, execution(bundle), 'a.json', report_kind='forward')[1]
    other = put(bundle['root']/'other'/FIRST, json.loads((bundle['result_register']/FIRST).read_text()))
    result, ok = write(bundle, execution(bundle, 'later', 'conditioned'), 'later.json', report_kind='conditioned', original_identity=other)
    assert not ok and 'declared register' in result['error']


def test_unmet_post_reveal_prerequisites_are_retained(bundle):
    files = execution(bundle)
    result, ok = write_report(bundle['root'], files['native_path'], files['observation_path'], bundle['root']/'absent.json',
                              here=bundle['here'], report_kind='forward')
    assert not ok and 'requires archive' in result['error']
