"""Runbook step 15: resolve every snapshot value now and write snapshot.json (write-once)."""
import hashlib, json, os, subprocess, sys, importlib, inspect
from pathlib import Path
H = Path(__file__).resolve().parents[1]; R = H / "results"; ROOT = H.parents[3]
sys.path.insert(0, str(ROOT))
from scripts.study import common
from scripts.study.manifest import _canonical_digest
read = lambda p: json.loads(Path(p).read_text())
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def artifacts(d):
    out = []
    for root, dirs, files in os.walk(d, followlinks=False):
        dirs[:] = [x for x in dirs if x not in ('pkg_link', '__pycache__') and not (Path(root) / x).is_symlink()]
        for n in sorted(files):
            p = Path(root) / n
            if p.is_symlink() or n.endswith(('.db-wal', '.db-shm', '.pyc')): continue
            out.append({'path': str(p.relative_to(H)), 'sha256': sha(p)})
    return sorted(out, key=lambda x: x['path'])
def main():
    assert not (H / 'snapshot.json').exists(), 'write-once'
    manifest = read(ROOT / 'exploration/stellarator_e2e/studies/manifest.json'); ind = read(H / 'indicators.json'); pre = read(R / 'preflight_results.json')
    ident = read(R / 'package_identity.json'); compat = read(R / 'store-compatibility.json'); summary = read(R / 'execution-summary.json')
    EXE = ident['identity']['digest']; SEM = manifest['fingerprints']['recorded_provenance']['semantic_fingerprint']
    assert EXE == manifest['fingerprints']['recorded_provenance']['executable_fingerprint']
    common.assert_tree_clean(ROOT / 'exploration/stellarator_e2e/generated')
    oracle_files = ('exploration/stellarator_e2e/verify_stellaris.py', 'exploration/stellarator_e2e/oracle_finance.py', 'exploration/stellarator_e2e/studies/oracle_entry.py')
    content = {k: manifest[k] for k in ('ties', 'objective_catalog', 'baseline', 'oracle')}
    content['oracle']['source_digest'] = common.tool_source_digest(oracle_files)
    content['fingerprint_names'] = ['indicator_inputs', 'recorded_provenance.executable_fingerprint', 'recorded_provenance.semantic_fingerprint']
    props = read(H / 'preparation/proposals.json'); axes = read(H / 'axes.json')['groups']
    P = 'stellarator_09__stellaris__'
    stores, arms = [], []
    tools = [ind['tool'], pre['tool']]
    ver = read(R / 'verification_summary.json'); tools.append(ver['tool'])
    stores.append({'store_id': 'study', 'path': summary['arms']['study']['store'], 'compatibility_tuple': compat['study'], 'note': 'One store for every arm: the union of four arms:180unique proposals and183arm rows; design and cheap anchors are shared by the transect arms.'})
    allpts = read(R / 'oracle-all-points.json')
    for arm in ('arm-a-transect', 'arm-R-transect', 'arm-matched-window', 'arm-assumptions'):
        pts = [r['point'] for r in props[arm]]
        bounds = {g['axis']: sorted({p.get(g['keys'][0]['key'], 'default') for p in pts}, key=lambda v: (isinstance(v, str), v)) for g in axes}
        arms.append({'arm_id': arm, 'store_id': 'study',
            'effective_executable_fingerprint': {'value': EXE, 'inputs': None, 'no_adapter': True, 'note': 'No adapter exists; the sealed fingerprint is the identity.'},
            'entry_models': {'note': 'stock strict loader; ten generated input groups, with all input files retained in preparation/package-inputs'},
            'strategy': {'kind': 'PreparedListStrategy', 'proposals_in_arm': len(pts), 'definition_fingerprint': compat['study']['study_definition_fingerprint']},
            'window': {'bounds': bounds, 'points': len(pts), 'provenance': 'engineered'},
            'verification': {'command': ver['command'], 'tool_revision': ver['tool']['source_digest'], 'sampling_scheme': 'generic verify.py stratified sample by verdict combination over the shared store, plus the record-local all-point comparison of every oracle-published required channel at every point of every arm (results/oracle-all-points.json) and the c_coil / vol_cold_total identities', 'tolerance': {'oracle_relative': 1e-9, 'identity_relative': 1e-12, 'predicates': 'authored exact operators'}, 'summary_sha256': sha(R / 'verification_summary.json'), 'all_points_sha256': sha(R / 'oracle-all-points.json'), 'all_points_outcome': allpts['outcome']},
            'glue_ledger': [], 'glue_ledger_none': True, 'artifacts': artifacts(R)})
    local = [str((H / n).relative_to(ROOT)) for n in ('study.py', 'execution/execute.py', 'execution/analyze.py', 'execution/scan.py', 'execution/freeze.py', 'execution/write_record.py')]
    tools.append({'path': str((H / 'execution/execute.py').relative_to(ROOT)), 'source_digest': common.tool_source_digest(tuple(local))})
    seen = set(); tools = [t for t in tools if not (t['path'] in seen or seen.add(t['path']))]
    teax_rev = subprocess.check_output(['git', '-C', str(Path(inspect.getfile(importlib.import_module('simkit.study.store'))).parents[4]), 'rev-parse', 'HEAD'], text=True).strip()
    snap = {'snapshot_schema_version': '1', 'study_id': H.name,
        'package': {'path': manifest['package']['path'], 'package_name': 'stellarator_tea', 'repo_commit': subprocess.check_output(['git', 'rev-parse', 'HEAD'], text=True).strip(), 'git_clean': pre['outcome'] == 'pass'},
        'fingerprints': {'indicator_inputs': ind['package']['indicator_input_fingerprint'] if 'indicator_input_fingerprint' in ind.get('package', {}) else manifest['fingerprints']['indicator_inputs'], 'recorded_provenance.executable_fingerprint': EXE, 'recorded_provenance.semantic_fingerprint': SEM},
        'manifest': {'path': 'exploration/stellarator_e2e/studies/manifest.json', 'schema_version': manifest['schema_version'], 'digest': sha(ROOT / 'exploration/stellarator_e2e/studies/manifest.json'), 'content_used': content},
        'stores': stores, 'arms': arms, 'tools': tools, 'teax': {'revision': teax_rev, 'era_pin': None},
        'indicators': {'path': 'indicators.json', 'sha256': sha(H / 'indicators.json'), 'output_schema_version': ind['schema_version'], 'axis_declaration': {'path': 'axes.json', 'schema_version': 'study-axis-declaration/v1', 'digest': sha(H / 'axes.json'), 'groups_declared': [g['axis'] for g in axes], 'subset': False}},
        'preparation_artifacts': artifacts(H / 'preparation'), 'review_artifacts': artifacts(H / 'reviews'), 'execution_artifacts': artifacts(H / 'execution'),
        'entering_pin': {'executable': 'e11e4c17b11681ac98b754e1ecbd60452fc11c758ef2d9ce72cfc57d4e740cad', 'semantic': '8eb332b9c73e1b80a5d7629e4de3532c739c280bbc889f45cb7bf3672269959d'},
        'plant_closure_reference_pin': read(H / 'preparation/before-plant-closure-anchors.json')['source_pin_extra']}
    assert teax_rev == '8d877460ac4f6f264561d916e40c1708adb13397', teax_rev
    assert set(content['fingerprint_names']) == set(snap['fingerprints'])
    (H / 'snapshot.json').write_text(json.dumps(snap, indent=2, allow_nan=False) + '\n')
    print('snapshot sha256', sha(H / 'snapshot.json'))
if __name__ == '__main__': main()
