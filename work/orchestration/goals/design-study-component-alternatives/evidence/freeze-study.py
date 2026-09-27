"""Seal the blocked matched-comparison evidence once; never releases verification. No model evaluation or physical solve."""
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
from exploration.component_alternatives.studies import study_route as route

read = lambda p: json.loads(p.read_text())
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
write = lambda p, value: p.write_text(json.dumps(value, indent=2) + '\n')


def freeze(record):
    record = record.resolve()
    assert not (record / 'snapshot.json').exists(), 'already frozen'
    results = record / 'results'
    cases = read(results / 'cases.json')['cases']
    verification = read(results / 'verification-blocker.json')
    assert verification['outcome'] == 'fail'
    diagnostics = read(results / 'verification-diagnostics.json')
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
    with tempfile.TemporaryDirectory(prefix='matched-freeze-') as tmp:
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
    source_paths.update(['models/designs/component_alternatives/plant.sysml',
        'models/library/analyses/component_alternatives_thermal.sysml',
        'models/library/analyses/cooling_equipment_selected_pumps.sysml',
        'exploration/component_alternatives/census.json',
        'exploration/component_alternatives/component_alternatives.snapshot.json',
        'exploration/component_alternatives/studies/ANNEX.md',
        'modeling_project/REQUIREMENTS.md', 'modeling_project/STUDY_POLICY.md', 'tests/model_families.py'])
    wi = ROOT / 'work/active/WI-096_matched-conversion-subsystems'
    source_paths.update((wi / name).relative_to(ROOT).as_posix() for name in ('spec.md','design.md','plan.md','report.md','evidence/validation-detail.md','evidence/validation-detail.json','evidence/implementation-census-final.json','evidence/independent-verification-final.json','evidence/constraint-identity-check.json','evidence/build-hashes.json'))
    goal = ROOT / 'work/orchestration/goals/design-study-component-alternatives'
    source_paths.update((goal / name).relative_to(ROOT).as_posix() for name in ('comparison-contract.md','evidence/engineering-equalities.md','evidence/design-review-fourth-submission.md','evidence/implementation-integration-review.md','evidence/owner-brief.md','evidence/owner-direction-fourth-submission.md','evidence/original-preservation-after-implementation.json','evidence/verification-failure-review.md','evidence/cooler-verification-diagnosis.md'))
    source_paths.add(Path(__file__).relative_to(ROOT).as_posix())
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
    oracle_files = sorted(p.relative_to(ROOT).as_posix() for p in route.E2E.glob('oracle_*.py')) + ['exploration/component_alternatives/verify.py','exploration/component_alternatives/studies/oracle_entry.py','exploration/component_alternatives/oracle_matched_cycle_properties.json']
    content['oracle']['source_digest'] = common.tool_source_digest(tuple(oracle_files))
    artifacts = [{'path': p.relative_to(record).as_posix(), 'sha256': sha(p)} for p in sorted(record.rglob('*')) if p.is_file() and p.name not in ('record.md','snapshot.json') and '__pycache__' not in p.parts and 'pkg_link' not in p.parts and p.suffix != '.pyc']
    snapshot = {
        'snapshot_schema_version':'1', 'study_id':record.name, 'record_status':'blocked_at_verification', 'released':False,
        'package':{'path':route.PACKAGE_DIR.relative_to(ROOT).as_posix(),'package_name':route.PACKAGE_NAME,'repo_commit':context['repo_commit_at_execution'],'git_clean':True},
        'fingerprints':{'indicator_inputs':indicators['package']['indicator_input_fingerprint'],'recorded_provenance.executable_fingerprint':expected,'recorded_provenance.semantic_fingerprint':integration['candidate']['semantic_fingerprint']},
        'manifest':{'path':route.MANIFEST_PATH.relative_to(ROOT).as_posix(),'schema_version':manifest['schema_version'],'digest':indicators['manifest']['digest'],'content_used':content},
        'stores':[{'store_id':record.name,'path':store.relative_to(record).as_posix(),'compatibility_tuple':compatibility}],
        'arms':[{'arm_id':'arm-matched-offers','store_id':record.name,
            'effective_executable_fingerprint':{'value':expected,'inputs':None,'no_adapter':True,'note':'Stock sealed package; no runtime adapter.'},
            'entry_models':entry_models,'strategy':compatibility.get('strategy_identity'),
            'window':{'bounds':read(record / 'window.json'),'provenance':'engineered'},
            'verification':{'command':context['verification_command'],'tool_revision':verification_tool['source_digest'],'sampling_scheme':{'requested':'all 498 via stock stratification','outcome':'aborted at first mismatch','supplemental_diagnostic':'all 498 exported cases, 872 channels and 84 predicates; not a stock verification pass'},'tolerance':{'relative':1e-9,'absolute_tolerances':manifest['absolute_tolerances'],'exact_verdicts':True,'note':'All named absolute classes were declared before execution. Four iteration counts are excluded.'},'summary_sha256':None,'failure_sha256':sha(results / 'verification-blocker.json'),'diagnostics_sha256':sha(results / 'verification-diagnostics.json'),'outcome':'fail'},
            'glue_ledger':[],'glue_ledger_none':True,'artifacts':artifacts}],
        'tools':tools,'teax':{'revision':integration['toolchain']['teax_revision'],'era_pin':None},
        'indicators':{'path':'indicators.json','sha256':sha(record / 'indicators.json'),'output_schema_version':indicators['schema_version'],'axis_declaration':indicators['axis_declaration']},
        'execution_context':'results/execution-context.json','case_count':len(cases),
        'diagnostic_numeric_channels_per_case':diagnostics['channels_per_case'], 'diagnostic_predicates_per_case':diagnostics['constraints_per_case'], 'cases_with_numeric_mismatches':diagnostics['cases_with_numeric_mismatches'], 'cases_with_predicate_mismatches':diagnostics['cases_with_predicate_mismatches'],
        'all_checks_satisfied_count':sum(all(v=='satisfied' for v in r['verdicts'].values()) for r in cases),
        'science_qualification':'Verification blocked; no released economic result. Selected steam offer versus tested Brayton offers at matched source conditions; conversion-subsystem cost per net MWh. Conditional prices, pressure service and machinery efficiencies. No whole-plant or equally optimized technology claim.'}
    write(record / 'snapshot.json', snapshot)
    print(json.dumps({'snapshot_sha256':sha(record / 'snapshot.json'),'cases':len(cases),'artifacts':len(artifacts),'sources':len(source_paths)}))

if __name__ == '__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--record',type=Path,required=True)
    freeze(parser.parse_args().record)
