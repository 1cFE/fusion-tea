"""Seal study 20260926-design-study-parameters after the owner-ruled re-verification (G-001): hash every record artifact, copy the tool, route, model and evidence sources, seal the package bytes, write results/export-proof.json and snapshot.json. Never edits results already committed, indicators.json or the record's executed manifest. Adapted from the design-space-combinations goal's freeze-study.py."""
import argparse, copy, hashlib, json, shutil, sqlite3, sys, tarfile, tempfile
from pathlib import Path
ROOT = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(ROOT))
from scripts.study import common
from exploration.costed_loop_brayton.studies import study_route as route

parser = argparse.ArgumentParser()
parser.add_argument('--record', type=Path, required=True)
args = parser.parse_args()
record = args.record.resolve()
route.MANIFEST_PATH = record / 'manifest.json'
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
verification_manifest = read(record / 'verification-manifest.json') if (record / 'verification-manifest.json').exists() else read(record / 'manifest.json')  # round 1 verified under a post-ruling manifest; later records verify under their own
indicators = read(record / 'indicators.json')
common.assert_tree_clean(route.PACKAGE_DIR)
assert read(route.MANIFEST_PATH) == manifest, 'the record manifest is the executed manifest'
executed_without = copy.deepcopy(verification_manifest); executed_without['absolute_tolerances'] = executed_without['absolute_tolerances'][:len(manifest['absolute_tolerances'])]
assert executed_without == manifest, 'the verification manifest is the executed manifest plus appended classes only'
assert sha(route.MANIFEST_PATH) == indicators['manifest']['digest']
assert integration['class'] == 'CANDIDATE'
expected = integration['candidate']['executable_fingerprint']
assert {r['executable_fingerprint'] for r in cases} == {expected}
assert route.interface()['executable_fingerprint'] == expected
with tempfile.TemporaryDirectory(prefix='clb-freeze-prepare-') as tmp:
    prepared = route.prepare(route.PACKAGE_DIR, Path(tmp))
    entry_models = {k: f'{v.__module__}.{v.__name__}' for k, v in prepared.entry_models.items()}

tools = [indicators['tool'], verification['tool']]
preflight = read(record / 'preparation' / 'preflight_results.json')
if 'tool' in preflight:
    tools.append(preflight['tool'])
source_paths = set()
for tool in tools:
    source_paths.update(r['path'] for r in tool['source_digest']['files'])
source_paths.update(r['path'] for r in integration['tool']['source_digest']['files'])
source_paths.update(p.relative_to(ROOT).as_posix() for p in route.HERE.glob('*.py'))
source_paths.update([route.MANIFEST_PATH.relative_to(ROOT).as_posix()] + ([(record / 'verification-manifest.json').relative_to(ROOT).as_posix()] if (record / 'verification-manifest.json').exists() else []) + [
                     (record / 'axes.json').relative_to(ROOT).as_posix(), (route.HERE / 'ANNEX.md').relative_to(ROOT).as_posix(),
                     'exploration/costed_loop_brayton/build.py', 'exploration/costed_loop_brayton/run.py', 'exploration/costed_loop_brayton/verify.py',
                     'exploration/costed_loop_brayton/census.json', 'exploration/costed_loop_brayton/costed_loop_brayton.snapshot.json',
                     'models/designs/costed_loop_brayton/costed_loop_brayton.sysml', 'models/designs/combinations/combinations_loop_brayton.sysml',
                     'work/completed/20260926_WI-094_costed-loop-brayton/spec.md', 'work/completed/20260926_WI-094_costed-loop-brayton/design.md', 'work/completed/20260926_WI-094_costed-loop-brayton/report.md',
                     'work/completed/20260926_WI-094_costed-loop-brayton/evidence/build-hashes.json', 'work/completed/20260926_WI-094_costed-loop-brayton/evidence/native_runs/summary.json',
                     'work/completed/20260926_WI-094_costed-loop-brayton/evidence/verification-summary.json',
                     'work/orchestration/goals/design-study-parameters/goal.md', 'work/orchestration/goals/design-study-parameters/trail.md',
                     'modeling_project/REQUIREMENTS.md', 'tests/model_families.py'])
source_paths.update(p.relative_to(ROOT).as_posix() for p in (ROOT / 'exploration/costed_loop_brayton/input_models').glob('*.sysml'))
GOAL_EVIDENCE = ROOT / 'work/orchestration/goals/design-study-parameters/evidence'
source_paths.update(p.relative_to(ROOT).as_posix() for p in GOAL_EVIDENCE.rglob('*') if p.is_file() and p.suffix in ('.md', '.json', '.py', '.log', '.txt', '.diff') and p.name not in ('preservation-entry.json',) and 'sources' not in p.parts)
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
            tar.add(path, arcname=route.PACKAGE_NAME + '/' + path.relative_to(route.PACKAGE_DIR).as_posix())

store = results / 'native' / (record.name + '.db')
con = sqlite3.connect('file:' + str(store) + '?mode=ro&immutable=1', uri=True)
con.row_factory = sqlite3.Row
compatibility = dict(con.execute('select * from compatibility').fetchone())
compatibility.pop('singleton', None)
assert con.execute("select count(*) from cases where state='completed'").fetchone()[0] == len(cases)
con.close()
export_proof = {'persistent_sha256': {p.relative_to(results / 'native').as_posix(): sha(p) for p in sorted((results / 'native').rglob('*')) if p.is_file() and 'pkg_link' not in p.parts},
                'cases_json_sha256': sha(results / 'cases.json'), 'cases_csv_sha256': sha(results / 'cases.csv'), 'completed_cases': len(cases)}
write(results / 'export-proof.json', export_proof)
content = copy.deepcopy(manifest)
content['fingerprint_names'] = ['indicator_inputs', 'recorded_provenance.executable_fingerprint', 'recorded_provenance.semantic_fingerprint']
oracle_files = tuple(p.relative_to(ROOT).as_posix() for p in sorted(route.HERE.glob('*.py')))
content['oracle']['source_digest'] = common.tool_source_digest(oracle_files)
content['verification_manifest'] = {'path': ((record / 'verification-manifest.json') if (record / 'verification-manifest.json').exists() else (record / 'manifest.json')).relative_to(ROOT).as_posix(), 'sha256': sha((record / 'verification-manifest.json') if (record / 'verification-manifest.json').exists() else (record / 'manifest.json')),
                                    'appended_absolute_tolerances': verification_manifest['absolute_tolerances'][len(manifest['absolute_tolerances']):],
                                    'ruling': 'work/orchestration/goals/design-study-parameters/evidence/owner-ruling-g001.md' if (record / 'verification-manifest.json').exists() else None}
artifacts = []
for path in sorted(record.rglob('*')):
    if path.is_file() and path.name not in ('record.md', 'snapshot.json') and '__pycache__' not in path.parts and 'pkg_link' not in path.parts and path.suffix != '.pyc':
        artifacts.append({'path': path.relative_to(record).as_posix(), 'sha256': sha(path)})
axis_plan = read(record / 'axis-plan.json')
summary = {
    'snapshot_schema_version': '1', 'study_id': record.name,
    'package': {'path': route.PACKAGE_DIR.relative_to(ROOT).as_posix(), 'package_name': route.PACKAGE_NAME, 'repo_commit': context['repo_commit_at_execution'], 'git_clean': True},
    'fingerprints': {'indicator_inputs': indicators['package']['indicator_input_fingerprint'],
                     'recorded_provenance.executable_fingerprint': expected,
                     'recorded_provenance.semantic_fingerprint': integration['candidate']['semantic_fingerprint']},
    'manifest': {'path': route.MANIFEST_PATH.relative_to(ROOT).as_posix(), 'schema_version': manifest['schema_version'], 'digest': indicators['manifest']['digest'], 'content_used': content},
    'stores': [{'store_id': record.name, 'path': store.relative_to(record).as_posix(), 'compatibility_tuple': compatibility}],
    'arms': [{'arm_id': 'arm-flow-ratio', 'store_id': record.name,
              'effective_executable_fingerprint': {'value': expected, 'inputs': None, 'no_adapter': True, 'note': 'No runtime adapter; the sealed package is the execution identity.'},
              'entry_models': entry_models, 'strategy': compatibility.get('strategy_identity'),
              'window': {'bounds': {k: axis_plan[k] for k in ('grid', 'inventories', 'sensitivities', 'anchors', 'designs', 'boundary', 'boundary_solve', 'refused_by_oracle_scan') if k in axis_plan}, 'provenance': 'engineered'},
              'verification': {'command': context['verification_command'].replace(record.name + '/manifest.json', record.name + '/verification-manifest.json'),
                               'tool_revision': verification['tool']['source_digest'], 'sampling_scheme': verification['stores'][0]['sampling'],
                               'tolerance': {'relative': 1e-9, 'absolute_tolerances': verification_manifest.get('absolute_tolerances', []), 'exact_verdicts': True,
                                             'note': ('The three hot-bound margin classes were declared after execution on owner ruling G-001; a verification tolerance on calculated temperature margins, never permission to accept a physical constraint violation.' if (record / 'verification-manifest.json').exists() else 'All twelve classes were declared in the manifest before execution (six from round 1, three ruled under G-001, three for the WI-095 root-solve channels).')},
                               'summary_sha256': sha(results / 'verification_summary.json')},
              'glue_ledger': [], 'glue_ledger_none': True, 'artifacts': artifacts}],
    'tools': tools, 'teax': {'revision': integration['toolchain']['teax_revision'], 'era_pin': None, 'identity_evidence': 'results/integration_return_used.json'},
    'indicators': {'path': 'indicators.json', 'sha256': sha(record / 'indicators.json'), 'output_schema_version': indicators['schema_version'], 'axis_declaration': indicators['axis_declaration']},
    'execution_context': 'results/execution-context.json', 'case_count': len(cases),
    'numeric_outputs_per_case': sorted({len(r['outputs']) for r in cases}),
    'verified_numeric_channels_per_case': len(verification['channels_checked']),
    'exact_verdicts_per_case': len(verification['constraints_rederived']),
    'all_scoped_checks_satisfied_count': sum(all(v == 'satisfied' for v in r['verdicts'].values()) for r in cases),
    'science_qualification': ('Round 3: the round-1 leading points re-evaluated with the loop return requirement enforced by an explicit primary-side bypass control, plus the matched-exchanger boundary family; the bypass loss, valve hardware and cost are unmodeled; ' if record.name.endswith('-b') else '') + 'A flow x stage-ratio sweep at fixed machine efficiencies on a costed assembly of reviewed definitions; the passing region is bounded by engineering checks, not qualified as a design; the auxiliary register, pump law, rest-of-plant constant and fuel convention are declared assumptions tested at anchors; no off-design map, hydraulic model, blanket-inlet requirement or cost-side check exists; no optimum is interpolated.'}
write(record / 'snapshot.json', summary)
print(json.dumps({'snapshot': str(record / 'snapshot.json'), 'sha256': sha(record / 'snapshot.json'), 'cases': len(cases), 'hashed_artifacts': len(artifacts), 'sources': len(source_paths)}))
