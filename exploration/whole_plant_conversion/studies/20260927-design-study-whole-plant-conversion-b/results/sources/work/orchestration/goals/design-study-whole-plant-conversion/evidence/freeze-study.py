"""Seal the independently verified whole-plant trade study once. No model evaluation or physical solve."""
from __future__ import annotations
import argparse
import copy
import hashlib
import json
import shutil
import sqlite3
import subprocess
import sys
import tarfile
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(ROOT))
from scripts.study import common, verify
from exploration.whole_plant_conversion.studies import study_route as route

read = lambda p: json.loads(p.read_text())
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
write = lambda p, value: p.write_text(json.dumps(value, indent=2) + '\n')


def freeze(record):
    record = record.resolve()
    assert not (record / 'snapshot.json').exists(), 'already frozen'
    results = record / 'results'
    cases = read(results / 'cases.json')['cases']
    verification = read(results / 'verification_summary.json')
    assert verification['outcome'] == 'pass'
    assert all(r['state'] == 'completed' for r in cases)
    context = read(results / 'execution-context.json')
    integration = read(results / 'integration_return_used.json')
    manifest = read(results / 'manifest_used.json')
    indicators = read(record / 'indicators.json')
    assert read(record / 'manifest.json') == manifest == read(route.MANIFEST_PATH)
    assert sha(record / 'manifest.json') == indicators['manifest']['digest']
    assert integration['class'] == 'CANDIDATE'
    expected = integration['candidate']['executable_fingerprint']
    assert {r['executable_fingerprint'] for r in cases} == {expected}
    assert route.interface()['executable_fingerprint'] == expected
    common.assert_tree_clean(route.PACKAGE_DIR)
    with tempfile.TemporaryDirectory(prefix='whole-plant-freeze-') as tmp:
        prepared = route.prepare(route.PACKAGE_DIR, Path(tmp))
        entry_models = {k: f'{v.__module__}.{v.__name__}' for k, v in prepared.entry_models.items()}
    verification_tool = {'path':'scripts/study/verify.py','source_digest':common.tool_source_digest(verify.TOOL_SOURCE_FILES)}
    tools = [indicators['tool'], verification_tool, read(record / 'preparation/preflight_results.json')['tool']]
    source_paths = set()
    for tool in tools + [integration['tool']]:
        source_paths.update(r['path'] for r in tool['source_digest']['files'])
    source_paths.update(p.relative_to(ROOT).as_posix() for p in route.HERE.glob('*.py'))
    source_paths.update(p.relative_to(ROOT).as_posix() for p in route.E2E.glob('*.py'))
    source_paths.update(p.relative_to(ROOT).as_posix() for p in route.E2E.glob('oracle_*.json'))
    source_paths.update(p.relative_to(ROOT).as_posix() for p in (route.E2E / 'input_models').glob('*.sysml'))
    source_paths.update(['models/designs/whole_plant_conversion/plant.sysml',
        'models/library/analyses/whole_plant_conversion_accounts.sysml',
        'exploration/whole_plant_conversion/census.json',
        'exploration/whole_plant_conversion/whole_plant_conversion.snapshot.json',
        'exploration/whole_plant_conversion/studies/ANNEX.md',
        'modeling_project/REQUIREMENTS.md', 'modeling_project/STUDY_POLICY.md', 'tests/model_families.py'])
    wi = ROOT / 'work/active/WI-098_whole-plant-conversion-comparison'
    source_paths.update((wi / name).relative_to(ROOT).as_posix() for name in (
        'spec.md','design.md','configuration.md','plan.md','report.md',
        'evidence/validation-detail.json','evidence/validation-detail.py',
        'evidence/independent-verification/verification-report.md',
        'evidence/independent-verification/native-check-final.json',
        'evidence/independent-verification/native-behaviors-final.json',
        'evidence/independent-verification/controls-summary.json',
        'evidence/conversion-controls/comparison.json'))
    source_paths.update(p.relative_to(ROOT).as_posix() for p in (wi / 'evidence/magnet-capture').rglob('*') if p.is_file() and not p.is_symlink() and p.suffix in ('.json','.md','.py') and '__pycache__' not in p.parts and 'package-link' not in p.parts)
    goal = ROOT / 'work/orchestration/goals/design-study-whole-plant-conversion'
    source_paths.update((goal / name).relative_to(ROOT).as_posix() for name in (
        'comparison-contract.md','evidence/owner-brief.md','evidence/upstream-accounting.md',
        'evidence/conversion-interfaces.md','evidence/boundary-review-r2.md',
        'evidence/capture-boundary-review-r2.md','evidence/cryoplant-offer-review.md',
        'evidence/implementation-integration-review.md','evidence/preservation-after-implementation.json',
        'evidence/final-results-review-r2.md','evidence/numerical-repair-r2-proposal.md',
        'evidence/numerical-repair-r2-review.md','evidence/round-1-review.md'))
    source_paths.update(p.relative_to(ROOT).as_posix() for p in (route.E2E / 'bodies').rglob('*.py'))
    source_paths.add(Path(__file__).relative_to(ROOT).as_posix())
    source_paths.update((goal / 'evidence' / name).relative_to(ROOT).as_posix() for name in ('write-record.py','write-answer.py','summarize-evidence.py','render_assembly.py','compare-native-replays.py'))
    for relative in sorted(source_paths):
        target = results / 'sources' / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(ROOT / relative, target)
    archive = record / 'sealed-package.tar.gz'
    assert not archive.exists(), 'prior freeze archive exists'
    with tarfile.open(archive, 'w:gz') as tar:
        for path in sorted(route.PACKAGE_DIR.rglob('*')):
            if path.is_file() and '__pycache__' not in path.parts and path.suffix != '.pyc':
                tar.add(path, arcname=route.PACKAGE_NAME + '/' + path.relative_to(route.PACKAGE_DIR).as_posix())
    store = results / 'native' / (record.name + '.db')
    con = sqlite3.connect('file:' + str(store) + '?mode=ro&immutable=1', uri=True)
    con.row_factory = sqlite3.Row
    compatibility = dict(con.execute('select * from compatibility').fetchone())
    compatibility.pop('singleton', None)
    assert con.execute("select count(*) from cases where state='completed'").fetchone()[0] == len(cases)
    con.close()
    write(results / 'export-proof.json', {
        'persistent_sha256': {p.relative_to(results / 'native').as_posix(): sha(p) for p in sorted((results / 'native').rglob('*')) if p.is_file() and 'pkg_link' not in p.parts},
        'cases_json_sha256': sha(results / 'cases.json'), 'cases_csv_sha256': sha(results / 'cases.csv'), 'completed_cases': len(cases)})
    content = copy.deepcopy(manifest)
    content['fingerprint_names'] = ['indicator_inputs', 'recorded_provenance.executable_fingerprint', 'recorded_provenance.semantic_fingerprint']
    oracle_files = sorted(p.relative_to(ROOT).as_posix() for p in route.E2E.glob('oracle_*.py')) + ['exploration/whole_plant_conversion/verify.py','exploration/whole_plant_conversion/studies/oracle_entry.py','exploration/whole_plant_conversion/oracle_matched_cycle_properties.json']
    content['oracle']['source_digest'] = common.tool_source_digest(tuple(oracle_files))
    artifacts = [{'path': p.relative_to(record).as_posix(), 'sha256': sha(p)} for p in sorted(record.rglob('*')) if p.is_file() and p.name not in ('record.md','snapshot.json') and '__pycache__' not in p.parts and 'pkg_link' not in p.parts and p.suffix != '.pyc']
    snapshot = {
        'snapshot_schema_version':'1', 'study_id':record.name, 'record_status':'verified', 'released':True,
        'package':{'path':route.PACKAGE_DIR.relative_to(ROOT).as_posix(),'package_name':route.PACKAGE_NAME,'repo_commit':context['repo_commit_at_execution'],'git_clean':True},
        'fingerprints':{'indicator_inputs':indicators['package']['indicator_input_fingerprint'],'recorded_provenance.executable_fingerprint':expected,'recorded_provenance.semantic_fingerprint':integration['candidate']['semantic_fingerprint']},
        'manifest':{'path':route.MANIFEST_PATH.relative_to(ROOT).as_posix(),'schema_version':manifest['schema_version'],'digest':indicators['manifest']['digest'],'content_used':content},
        'stores':[{'store_id':record.name,'path':store.relative_to(record).as_posix(),'compatibility_tuple':compatibility}],
        'arms':[{'arm_id':'arm-whole-plant-offers','store_id':record.name,
            'effective_executable_fingerprint':{'value':expected,'inputs':None,'no_adapter':True,'note':'Stock sealed package; no runtime adapter.'},
            'entry_models':entry_models,'strategy':compatibility.get('strategy_identity'),
            'window':{'bounds':read(record / 'window.json'),'provenance':'engineered'},
            'verification':{'command':context['verification_command'],'tool_revision':verification_tool['source_digest'],'sampling_scheme':verification['stores'][0]['sampling'],'tolerance':{'relative':1e-9,'absolute_tolerances':manifest['absolute_tolerances'],'exact_verdicts':True,'note':'All named absolute classes were declared before execution. Four iteration counts are excluded.'},'summary_sha256':sha(results / 'verification_summary.json'),'outcome':'pass'},
            'glue_ledger':[],'glue_ledger_none':True,'artifacts':artifacts}],
        'tools':tools,'teax':{'revision':integration['toolchain']['teax_revision'],'era_pin':None},
        'indicators':{'path':'indicators.json','sha256':sha(record / 'indicators.json'),'output_schema_version':indicators['schema_version'],'axis_declaration':indicators['axis_declaration']},
        'execution_context':'results/execution-context.json','case_count':len(cases),
        'verified_numeric_channels_per_case':len(verification['channels_checked']), 'exact_verdicts_per_case':len(verification['constraints_rederived']),
        'all_checks_satisfied_count':sum(all(v=='satisfied' for v in r['verdicts'].values()) for r in cases),
        'predecessor':{'study_id':'20260926-design-study-component-alternatives-b',
            'snapshot_sha256':'ea6b9de7cf242c88f764a9a997aadd1b6d813560b5c0953e84e63a7aeef9928e',
            'disposition':'Different accounting boundary. All498 inherited controls exactly reproduce872 conversion channels and84 predicates. Whole-plant equipment is reranked at this executable.'},
        'science_qualification':'Numerically verified whole-plant comparison of the declared supplied-source reactor and finite priced conversion catalog. Common engineering checks apply; plasma operating point, nuclear transport and global manufactured fit are unqualified. Engineered stresses are not established uncertainty intervals. No equal global technology optimization claim.'}
    write(record / 'snapshot.json', snapshot)
    print(json.dumps({'snapshot_sha256':sha(record / 'snapshot.json'),'cases':len(cases),'artifacts':len(artifacts),'sources':len(source_paths)}))

if __name__ == '__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--record',type=Path,required=True)
    freeze(parser.parse_args().record)
