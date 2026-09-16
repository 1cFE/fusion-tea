"""Independent frozen-study custody, sample and all-point oracle review."""
import hashlib
import importlib.util
import json
import math
import os
import sqlite3
import subprocess
import sys
from collections import Counter
from pathlib import Path

ROOT = Path.cwd()
OUT = Path(__file__).resolve().parent
H = ROOT / 'exploration/stellarator_e2e/studies/20260915-divertor-heat-account'
P = 'stellarator_09__stellaris__'
FROZEN = 'ac1b529baeadf06172cfc141ae2666dbc81191b7'
read = lambda p: json.loads(p.read_text())
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
native = read(H / 'results/native-cases.json')
catalog = read(H / 'results/predicate-catalog.json')

if len(sys.argv) > 1:
    mode = sys.argv[1]
    folder = H / ('preparation' if mode == 'current' else 'preparation/entering')
    sys.path[:0] = [str(ROOT), str(Path(os.environ['STOP_PARSER_TEAX_ROOT']) / 'packages/teax-simkit')]
    def load(name, path):
        spec = importlib.util.spec_from_file_location(name, path)
        module = importlib.util.module_from_spec(spec)
        sys.modules[name] = module
        spec.loader.exec_module(module)
        assert Path(module.__file__).resolve() == path.resolve()
        return module
    load('oracle_finance', folder / 'oracle_finance.py')
    load('verify_stellaris', folder / 'verify_stellaris.py')
    oracle = load('review_oracle', folder / 'oracle_entry.py')
    from scripts.study.verify import derive_verdict
    params = read(H / 'preparation/resolved-defaults.json')
    count = predicates = 0
    for row in native:
        point = dict(row['inputs'])
        if mode == 'entering': point.pop(P + 'divertor__target_capture_fraction')
        values = oracle.evaluate(point)
        assert len(values) == (226 if mode == 'current' else 218)
        for k, v in values.items():
            assert math.isclose(v, row['outputs'][k], rel_tol=1e-9, abs_tol=1e-9), (mode, row['proposal_id'], k, v, row['outputs'][k])
            count += 1
        for cid, entry in catalog.items():
            expected = 'satisfied' if derive_verdict(cid, entry, oracle.operand_bindings(), point, params, values)[0] else 'violated'
            assert expected == row['verdicts'][cid], (mode, row['proposal_id'], cid)
            predicates += 1
    result = dict(mode=mode, scalars=count, predicates=predicates, outcome='pass')
    (OUT / (mode + '-replay.json')).write_text(json.dumps(result, indent=2) + '\n')
    print(result)
    raise SystemExit

snap = read(H / 'snapshot.json')
assert sha(H / 'snapshot.json') == '92d2a24565645de602384a530ee6c32776e66b4787af8245b81d3d099df3fbbd'
artifacts = sum((snap[k] for k in ['preparation_artifacts', 'review_artifacts', 'execution_artifacts', 'definition_artifacts']), [])
artifacts += sum((a['artifacts'] for a in snap['arms']), [])
for item in artifacts:
    path = H / item['path']
    assert sha(path) == item['sha256'], path
    assert path.read_bytes() == subprocess.check_output(['git', 'show', FROZEN + ':' + str(path.relative_to(ROOT))]), path
assert not subprocess.check_output(['git', 'diff', '48b65159', '--', 'models', 'exploration/stellarator_e2e/models', 'exploration/stellarator_e2e/generated', 'exploration/stellarator_e2e/verify_stellaris.py', 'exploration/stellarator_e2e/studies/oracle_entry.py'])
bycid = {r['candidate_id']: r for r in native}
stores = []
for path in sorted((H / 'results').rglob('*.db')):
    db = sqlite3.connect('file:' + str(path) + '?mode=ro', uri=True)
    rows = db.execute('select candidate_id,state,inputs_json,evidence_digest from cases').fetchall()
    matched = 0
    for cid, state, inputs, digest in rows:
        assert state == 'completed'
        evidencepath = path.parent / 'artifacts' / (digest + '.json')
        assert sha(evidencepath) == digest
        ev = read(evidencepath)
        verdicts = {cid: ev['responses'][cid] for cid in catalog}
        assert {r['constraint_id']: r['status'] for r in ev['report']['results']} == verdicts
        assert ev['report']['coverage']['coverage_state'] == 'complete'
        if cid in bycid:
            row = bycid[cid]
            assert json.loads(inputs) == row['inputs']
            assert ev['outputs'] == row['outputs'] and verdicts == row['verdicts']
            assert ev['responses']['headline'] == row['headline']
            matched += 1
    proposals = db.execute('select raw_json,valid,candidate_id from proposals').fetchall()
    if matched:
        assert matched == len(native) == len(proposals) == 27
        for raw, valid, cid in proposals: assert valid == 1 and json.loads(raw) == bycid[cid]['inputs']
    stores.append(dict(path=str(path.relative_to(H)), cases=len(rows), export_joins=matched))
    db.close()
assert len(stores) == 2 and sum(s['cases'] for s in stores) == 28

props = {r['proposal_id']: r for r in read(H / 'preparation/proposals.json')}
byid = {r['proposal_id']: r for r in native}
assert len(byid) == 27 and set(byid) == set(props)
assert Counter(p['family'] for p in props.values()) == {'base-control': 5, 'source-profile': 5, 'radiation-sensitivity': 10, 'radius-sensitivity': 6, 'invalid-account-control': 1}
defaults = read(H / 'preparation/resolved-defaults.json')
for pid, prop in props.items():
    row = byid[pid]
    assert row['inputs'] == prop['point']
    base = props.get(prop['base_id'])
    if base and base != prop:
        changed = {k for k in prop['point'] if prop['point'][k] != base['point'][k]}
        if prop['family'] == 'source-profile':
            assert changed == {P+'divertor__q_target_ref', P+'divertor__target_capture_fraction'}
            assert prop['point'][P+'divertor__q_target_ref'] == 5 and prop['point'][P+'divertor__target_capture_fraction'] == .97
        elif prop['family'] == 'radiation-sensitivity':
            assert changed == {P+'divertor__f_rad_total'} and prop['point'][P+'divertor__f_rad_total'] in [.88, .92]
        else:
            assert changed == {P+'plasma__R'}
            assert math.isclose(abs(prop['point'][P+'plasma__R']-base['point'][P+'plasma__R']), .2)
for old in read(H / 'preparation/entering/native-cases.json')['cases']:
    row = byid[old['proposal_id']]
    for k,v in old['outputs'].items(): assert row['outputs'][k] == v
    assert old['responses'] == dict(row['verdicts'], headline=row['headline'])

dh = lambda row, key: row['outputs'][P+'divertor__divheat__'+key]
invalid = [pid for pid,row in byid.items() if dh(row,'power_account_valid') == 0]
assert set(invalid) == {'signed-negative-burn-control', 'r-13.1-1.45-1.54e+07--radius--0.2'}
passes = 0
reductions = {}
for pid,row in byid.items():
    v = row['outputs']; params = defaults | row['inputs']; h=dh(row,'p_heat_abs'); q=dh(row,'q_target_peak')
    c=params[P+'divertor__target_capture_fraction']; f=params[P+'divertor__f_rad_total']; ref=params[P+'divertor__q_target_ref']; nr=params[P+'divertor__p_nonrad_ref']
    assert params[P+'divertor__q_target_limit'] == 10
    assert math.isclose(h, v[P+'plasma__sustain__p_rad']+dh(row,'p_rad_edge')+dh(row,'p_target_deposited')+dh(row,'p_nonrad_uncaptured'),abs_tol=1e-9)
    assert q == ref * (h-f*h) / nr
    assert math.isclose(q, dh(row,'p_target_deposited')/dh(row,'peak_equivalent_area'),rel_tol=1e-12)
    assert math.isclose(dh(row,'q_target_peak_area_scaled'),q*params[P+'divertor__R_ref_divertor']/params[P+'plasma__R'],rel_tol=1e-12)
    assert any(s=='violated' for s in row['verdicts'].values())
    if q <= 10 and dh(row,'power_account_valid') == 1: passes += 1
    if props[pid]['family'] in ['source-profile','radiation-sensitivity']:
        base=byid[props[pid]['base_id']]
        for k in v:
            if '__divertor__divheat__' not in k: assert v[k] == base['outputs'][k],(pid,k)
    if props[pid]['family'] == 'base-control' and q>10:
        reductions[pid]=dict(power_reduction=1-10/q, area_increase=q/10-1, radiation_threshold=1-10*nr/(ref*h))
assert passes==13
verify=read(H/'results/verification_summary.json'); assert verify['outcome']=='pass' and len(verify['channels_checked'])==27 and len(verify['constraints_rederived'])==20 and not verify['verdict_mismatches']
sampled=verify['stores'][0]['sampling']['sampled_case_ids']
stratum=lambda row:tuple(sorted(row['verdicts'].items()))
assert len({stratum(row) for row in native}) == len({stratum(bycid[cid]) for cid in sampled}) == 13
ret=read(ROOT/'work/orchestration/goals/divertor-peak-heat-load/evidence/T-003_integration/integration_return.json')
assert ret['class']=='CANDIDATE' and len(ret['gates'])==10 and all(g['status']=='pass' for g in ret['gates'])
assert ret['candidate']['pin']==snap['integration_candidate_pin']
for gate in ret['gates']:
    for name in gate['evidence']: assert (ROOT/name).is_file()
report=dict(outcome='pass',snapshot_artifacts=len(artifacts),stores=stores,sample_cases=27,invalid_accounts=invalid,valid_divertor_passes=passes,all_predicate_passes=0,conditional_requirements=reductions,integrated_gates=10,strata_checked=13,unchanged_implementation_revision='48b65159')
(OUT/'custody-and-account.json').write_text(json.dumps(report,indent=2)+'\n')
print(report)
