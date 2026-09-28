"""Capture the candidate and construct complete diagnostic groups without evaluations."""
import json
import shutil
import subprocess
from pathlib import Path
from scripts.study.verify import package_input_values
from exploration.stellarator_e2e.studies import study_route as route

H = Path(__file__).resolve().parents[1]
ROOT = H.parents[3]
PREP = H / 'preparation'
P = route.P
GOAL = ROOT / 'work/orchestration/goals/divertor-peak-heat-load'
OLD = 'f76ec031951d7918fbfec2de23d298830941c121'
read = lambda p: json.loads(p.read_text())
def write(path, value):
    path.write_text(json.dumps(value, indent=2, allow_nan=False)+'\n')

for name in ['manifest.json', 'oracle_entry.py', 'ANNEX.md', 'study_route.py']:
    shutil.copy2(H.parent/name, PREP/name)
for name in ['verify_stellaris.py', 'oracle_finance.py']:
    shutil.copy2(H.parent.parent/name, PREP/name)
for name in ['contracts', 'inputs', 'pipelines', 'schemas']:
    shutil.copytree(route.PACKAGE_DIR/name, PREP/('package-'+name), dirs_exist_ok=True)
shutil.copy2(GOAL/'evidence/T-003_integration/integration_return.json', PREP/'integration-return.json')
candidate = read(PREP/'integration-return.json')
assert candidate['class'] == 'CANDIDATE' and len(candidate['gates']) == 10
assert all(g['status'] == 'pass' for g in candidate['gates'])
assert candidate['candidate']['pin'] == '6e427038e8515501e9c42c39823f85e3b0bcbd9f54f830b2779a792851f02551'
for name in ['study-brief.md', 'external-research.md', 'source-math-review.md', 'implementation-review.md']:
    src = GOAL/'evidence'/name
    if src.exists(): shutil.copy2(src, PREP/name)
(PREP/'goal-at-authority.md').write_bytes(subprocess.check_output(['git','show','25f9ce82:work/orchestration/goals/divertor-peak-heat-load/goal.md']))
for name in ['STUDY_POLICY.md']:
    shutil.copy2(ROOT/'modeling_project'/name, PREP/name)
old = PREP/'entering'
old.mkdir(exist_ok=True)
for name in ['native-cases.json', 'negative-native-cases.json', 'oracle_entry.py', 'verify_stellaris.py']:
    shutil.copy2(GOAL/'evidence/entering'/name, old/name)
for name in ['oracle_entry.py','verify_stellaris.py','oracle_finance.py']:
    rel = ('exploration/stellarator_e2e/studies/' if name=='oracle_entry.py' else 'exploration/stellarator_e2e/')+name
    data = subprocess.check_output(['git','show',OLD+':'+rel])
    if name != 'oracle_finance.py': assert data == (old/name).read_bytes()
    else:
        assert data == (PREP/name).read_bytes(), 'Finance helper changed from entering'
        (old/name).write_bytes(data)
for rel, dest in [('contracts/model_contract.json','model-contract.json'),('contracts/package_contract.json','package-contract.json')]:
    (old/dest).write_bytes(subprocess.check_output(['git','show',OLD+':exploration/stellarator_e2e/generated/'+rel]))
files = subprocess.check_output(['git','ls-tree','-r','--name-only',OLD,'exploration/stellarator_e2e/generated/inputs'],text=True).splitlines()
for rel in files:
    dst=old/'inputs'/Path(rel).name
    dst.parent.mkdir(exist_ok=True)
    dst.write_bytes(subprocess.check_output(['git','show',OLD+':'+rel]))
write(old/'provenance.json',{'repository_revision':OLD,'oracle_files_verified_against_git':True,'finance_identical_to_current':True,'native_controls_scope':'Five named regular controls and signed-negative control captured before implementation; study attribution otherwise uses isolated entering oracle.'})
params = package_input_values(route.PACKAGE_DIR)
write(PREP/'resolved-defaults.json', params)
contract = read(PREP/'package-contracts/model_contract.json')
write(PREP/'required-channels.json', sorted(o['channel_name'] for o in contract['outputs'] if o['python_type'] in ['float','int']))
base_names = ['reference','current-sized-reference','allocated-current-sized-reference','r-12.7-1.35-1.62e+07','r-13.1-1.45-1.54e+07']
bases = {r['proposal_id']:r['point'] for r in read(old/'native-cases.json')['cases']}
rows=[]
def add(pid,family,point,base_id=None):
    rows.append({'id':pid,'proposal_id':pid,'family':family,'arm':'arm-native','base_id':base_id,'point':point.copy()})
for name in base_names:
    high=bases[name]|{P+'divertor__target_capture_fraction':.99,P+'divertor__q_target_ref':9.5,P+'divertor__p_nonrad_ref':50.,P+'divertor__f_rad_total':.90}
    add(name,'base-control',high,name)
    add(name+'--low-profile','source-profile',high|{P+'divertor__target_capture_fraction':.97,P+'divertor__q_target_ref':5.},name)
    for f in [.88,.92]: add(name+f'--radiation-{f:.2f}','radiation-sensitivity',high|{P+'divertor__f_rad_total':f},name)
    if name in ['reference','r-12.7-1.35-1.62e+07','r-13.1-1.45-1.54e+07']:
        for delta in [-.2,.2]: add(name+f'--radius-{delta:+.1f}','radius-sensitivity',high|{P+'plasma__R':round(high[P+'plasma__R']+delta,2)},name)
negative=next(r for r in read(old/'negative-native-cases.json')['cases'] if not r['sized'])
add('signed-negative-burn-control','invalid-account-control',negative['point'])
for r in rows:
    key=P+'magnet__winding_pack__B_max'
    if key in r['point']:
        assert r['point'][key] == params[key]
        del r['point'][key]
keys=sorted({k for r in rows for k in r['point']})
pair=[P+'divertor__q_target_ref',P+'divertor__target_capture_fraction']
groups=[{'axis':k.removeprefix(P),'note':'Complete public-attribute group; diagnostic context control or sensitivity. Acceptance limits remain held.', 'keys':[{'key':k,'provenance':'fan_out'}]} for k in keys if k not in pair]
groups.append({'axis':'paired-source-profile','note':'Coordinator-declared source-case tie: q_ref=9.5/capture=.99 or q_ref=5/capture=.97, both at Nref=50. Distinct transport cases on the same proposed target arrangement; not one physical scalar identity or a continuous free design axis.', 'keys':[{'key':k,'provenance':'tie'} for k in pair]})
assert set(keys)<=set(params)
for r in rows:
    r['original_point']=r['point'].copy()
    r['point']={k:params[k] for k in keys}|r['point']
    r['canonical_proposal_id']=r['id']
assert len(rows)==27 and len({json.dumps(r['point'],sort_keys=True) for r in rows})==27
write(H/'axes.json',{'schema_version':'study-axis-declaration/v1','groups':groups})
write(PREP/'scan-proposals.json',rows)
write(PREP/'proposals.json',rows)
write(PREP/'unique-proposals.json',rows)
print(f'Prepared {len(rows)} candidates, {len(groups)} complete groups, {len(params)} defaults; no point evaluated.')
