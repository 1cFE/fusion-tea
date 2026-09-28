"""Capture this goal's native study evidence after execution and verification."""
import argparse
import copy
import hashlib
import json
from pathlib import Path
import shutil
import sqlite3
import subprocess
import sys
import tarfile
import tempfile

ROOT = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(ROOT))
from scripts.study import common
from exploration.aries_integrated.studies import study_route as route

parser = argparse.ArgumentParser()
parser.add_argument('--record', type=Path, required=True)
args = parser.parse_args()
record = args.record.resolve()
assert not (record / 'snapshot.json').exists(), 'snapshot already exists; preserve it'
read = lambda p: json.loads(p.read_text())
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
write = lambda p, d: p.write_text(json.dumps(d, indent=2) + '\n')
results = record / 'results'
cases = read(results / 'cases.json')['cases']
verification = read(results / 'verification_summary.json')
assert verification['outcome'] == 'pass'
assert all(r['state'] == 'completed' for r in cases)
context = read(results / 'execution-context.json')
integration = read(results / 'integration_return_used.json')
manifest = read(results / 'manifest_used.json')
indicators = read(record / 'indicators.json')
common.assert_tree_clean(route.PACKAGE_DIR)
assert read(route.MANIFEST_PATH) == manifest
assert sha(route.MANIFEST_PATH) == indicators['manifest']['digest']
assert integration['class'] == 'CANDIDATE'
expected = integration['candidate']['executable_fingerprint']
assert {r['executable_fingerprint'] for r in cases} == {expected}
assert route.interface()['executable_fingerprint'] == expected
with tempfile.TemporaryDirectory(prefix='aries-freeze-prepare-') as tmp:
    prepared = route.prepare(route.PACKAGE_DIR, Path(tmp))
    entry_models = {k: f'{v.__module__}.{v.__name__}' for k, v in prepared.entry_models.items()}

tools = [indicators['tool'], verification['tool']]
preflight = read(results / 'integration' / 'preflight_results.json')
if 'tool' in preflight:
    tools.append(preflight['tool'])
source_paths = set()
for tool in tools:
    source_paths.update(r['path'] for r in tool['source_digest']['files'])
source_paths.update(r['path'] for r in integration['tool']['source_digest']['files'])
source_paths.update(p.relative_to(ROOT).as_posix() for p in route.HERE.glob('*.py'))
source_paths.update([route.MANIFEST_PATH.relative_to(ROOT).as_posix(),
                     (route.HERE / 'axes.json').relative_to(ROOT).as_posix(),
                     (route.HERE / 'ANNEX.md').relative_to(ROOT).as_posix(),
                     'work/completed/20260922_WI-090_aries-integrated-equipment-and-costs/design.md',
                     'work/completed/20260922_WI-090_aries-integrated-equipment-and-costs/evidence/account-manifest.json',
                     'work/completed/20260922_WI-090_aries-integrated-equipment-and-costs/evidence/financial-handoff.md',
                     'work/orchestration/goals/aries-integrated-equipment-costs/evidence/source-basis.md',
                     'work/orchestration/goals/aries-integrated-equipment-costs/evidence/source-review.md',
                     'work/orchestration/goals/aries-integrated-equipment-costs/evidence/design-review.md',
                     'work/orchestration/goals/aries-integrated-equipment-costs/evidence/implementation-review.md'])
source_paths.update([
    'work/active/WI-091_aries-integrated-lifecycle-cost/spec.md',
    'work/active/WI-091_aries-integrated-lifecycle-cost/design.md',
    'work/active/WI-091_aries-integrated-lifecycle-cost/plan.md',
    'work/orchestration/goals/aries-integrated-lcoe/evidence/owner-brief.md',
    'work/orchestration/goals/aries-integrated-lcoe/evidence/owner-supplement.md',
    'work/orchestration/goals/aries-integrated-lcoe/evidence/source-boundary.md',
    'work/orchestration/goals/aries-integrated-lcoe/evidence/design-review.md',
    'work/orchestration/goals/aries-integrated-lcoe/evidence/implementation-review.md',
    'work/orchestration/goals/aries-integrated-lcoe/evidence/design-review-arithmetic.json',
    'work/orchestration/goals/aries-integrated-lcoe/evidence/implementation-review-probe.json',
    'work/orchestration/goals/aries-integrated-lcoe/evidence/implementation-review-probe.py',
    'work/active/WI-091_aries-integrated-lifecycle-cost/evidence/interface-handoff.json',
    'work/active/WI-091_aries-integrated-lifecycle-cost/report.md',
    'exploration/aries_integrated/build.py',
    'exploration/aries_integrated/run.py',
    'exploration/aries_integrated/verify.py',
    'tests/model_families.py',
])
source_paths.update(p.relative_to(ROOT).as_posix() for p in (ROOT/'exploration/aries_integrated/native_completions').rglob('*.py'))
source_paths.update(p.relative_to(ROOT).as_posix() for p in (ROOT/'exploration/aries_integrated/input_models').glob('*.sysml'))
source_paths.add(Path(__file__).relative_to(ROOT).as_posix())
for relative in sorted(source_paths):
    target = results / 'sources' / relative
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(ROOT / relative, target)
archive = record / 'sealed-package.tar.gz'
assert not archive.exists(), 'archive exists; preserve prior freeze attempt'
with tarfile.open(archive, 'w:gz') as tar:
    for path in sorted(route.PACKAGE_DIR.rglob('*')):
        if path.is_file() and '__pycache__' not in path.parts and path.suffix != '.pyc':
            tar.add(path, arcname='aries_integrated/' + path.relative_to(route.PACKAGE_DIR).as_posix())

store = results / 'native' / (record.name + '.db')
con = sqlite3.connect('file:' + str(store) + '?mode=ro&immutable=1', uri=True)
con.row_factory = sqlite3.Row
compatibility = dict(con.execute('select * from compatibility').fetchone())
compatibility.pop('singleton')
assert con.execute("select count(*) from cases where state='completed'").fetchone()[0] == len(cases)
con.close()
content = copy.deepcopy(manifest)
content['fingerprint_names'] = ['indicator_inputs', 'recorded_provenance.executable_fingerprint', 'recorded_provenance.semantic_fingerprint']
oracle_files = tuple(p.relative_to(ROOT).as_posix() for p in sorted(route.HERE.glob('*.py')))
content['oracle']['source_digest'] = common.tool_source_digest(oracle_files)
artifacts = []
for path in sorted(record.rglob('*')):
    if path.is_file() and path.name not in ('record.md', 'snapshot.json', 'synthesis.md') and '__pycache__' not in path.parts and 'pkg_link' not in path.parts and path.suffix != '.pyc':
        artifacts.append({'path': path.relative_to(record).as_posix(), 'sha256': sha(path)})
axis_plan = read(record / 'axis-plan.json')
plan_axes = axis_plan['axes']
summary = {
    'snapshot_schema_version': '1', 'study_id': record.name,
    'package': {'path': route.PACKAGE_DIR.relative_to(ROOT).as_posix(), 'package_name': route.PACKAGE_NAME, 'repo_commit': context['repo_commit_at_execution'], 'git_clean': True},
    'fingerprints': {'indicator_inputs': indicators['package']['indicator_input_fingerprint'],
                     'recorded_provenance.executable_fingerprint': expected,
                     'recorded_provenance.semantic_fingerprint': integration['candidate']['semantic_fingerprint']},
    'manifest': {'path': route.MANIFEST_PATH.relative_to(ROOT).as_posix(), 'schema_version': manifest['schema_version'], 'digest': indicators['manifest']['digest'], 'content_used': content},
    'stores': [{'store_id': record.name, 'path': store.relative_to(record).as_posix(), 'compatibility_tuple': compatibility}],
    'arms': [{'arm_id': 'arm-declared-sensitivity', 'store_id': record.name,
              'effective_executable_fingerprint': {'value': expected, 'inputs': None, 'no_adapter': True, 'note': 'No runtime adapter; sealed package is the execution identity.'},
              'entry_models': entry_models, 'strategy': compatibility['strategy_identity'],
              'window': {'bounds': plan_axes, 'provenance': 'engineered'},
              'verification': {'command': context['verification_command'], 'tool_revision': verification['tool']['source_digest'], 'sampling_scheme': verification['stores'][0]['sampling'], 'tolerance': {'relative': 1e-9, 'absolute_tolerances': manifest.get('absolute_tolerances', []), 'exact_verdicts': True}, 'summary_sha256': sha(results / 'verification_summary.json')},
              'glue_ledger': [], 'glue_ledger_none': True, 'artifacts': artifacts}],
    'tools': tools, 'teax': {'revision': integration['toolchain']['teax_revision'], 'era_pin': None, 'identity_evidence': 'results/integration_return_used.json'},
    'indicators': {'path': 'indicators.json', 'sha256': sha(record / 'indicators.json'), 'output_schema_version': indicators['schema_version'], 'axis_declaration': indicators['axis_declaration']},
    'execution_context': 'results/execution-context.json', 'case_count': len(cases),
    'numeric_outputs_per_case': sorted({len(r['outputs']) for r in cases}),
    'verified_numeric_channels_per_case': len(verification['channels_checked']),
    'exact_verdicts_per_case': len(verification['constraints_rederived']),
    'all_scoped_checks_satisfied_count': sum(all(v == 'satisfied' for v in r['verdicts'].values()) for r in cases),
    'science_qualification': 'Conditional scenario only; inherited unsupported scientific checks remain unsupported.'}
write(record / 'snapshot.json', summary)
print(json.dumps({'snapshot': str(record / 'snapshot.json'), 'sha256': sha(record / 'snapshot.json'), 'cases': len(cases), 'hashed_artifacts': len(artifacts)}))
