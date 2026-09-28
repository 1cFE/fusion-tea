"""Capture unchanged package and explicit integer-count diagnostic; no evaluations."""
import json,shutil
from pathlib import Path
from scripts.study.verify import package_input_values
from exploration.stellarator_e2e.studies import study_route as route
H=Path(__file__).resolve().parents[1]; ROOT=H.parents[3]; PREP=H/'preparation'; GOAL=ROOT/'work/orchestration/goals/primary-loop-sizing'; P=route.P
read=lambda p:json.loads(p.read_text())
def write(p,v):p.write_text(json.dumps(v,indent=2,allow_nan=False)+'\n')
for name in ['manifest.json','oracle_entry.py','ANNEX.md','study_route.py']:shutil.copy2(H.parent/name,PREP/name)
for name in ['verify_stellaris.py','oracle_finance.py']:shutil.copy2(H.parent.parent/name,PREP/name)
for name in ['contracts','inputs','pipelines','schemas']:shutil.copytree(route.PACKAGE_DIR/name,PREP/('package-'+name),dirs_exist_ok=True)
for name in ['study-brief.md','source-review.md','hydraulic-source-account.md','entering-cost-account.md']:
 src=GOAL/'evidence'/name
 if src.exists():shutil.copy2(src,PREP/name)
shutil.copy2(GOAL/'evidence/T-002_integration/integration_return.json',PREP/'integration-return.json')
c=read(PREP/'integration-return.json');assert c['class']=='CANDIDATE' and len(c['gates'])==10 and all(g['status']=='pass' for g in c['gates'])
assert 'PASS for the scoped diagnostic' in (PREP/'source-review.md').read_text()
shutil.copy2(GOAL/'goal.md',PREP/'goal-at-authority.md');shutil.copy2(ROOT/'modeling_project/STUDY_POLICY.md',PREP/'STUDY_POLICY.md')
shutil.copytree(GOAL/'evidence/entering',PREP/'entering',dirs_exist_ok=True)
params=package_input_values(route.PACKAGE_DIR);write(PREP/'resolved-defaults.json',params)
contract=read(PREP/'package-contracts/model_contract.json');write(PREP/'required-channels.json',sorted(o['channel_name'] for o in contract['outputs'] if o['python_type'] in ['float','int']))
bases=read(PREP/'entering/native-cases.json')['cases']; nkey=P+'heat_transport__n_loops';assert nkey in params
rows=[];scan=[]
for b in bases:
 for n in range(12,19):
  pid=b['proposal_id']+f'--loops-{n}';r={'id':pid,'proposal_id':pid,'canonical_proposal_id':pid,'family':b['proposal_id'],'base_id':b['proposal_id'],'arm':'arm-native','point':b['point']|{nkey:n}}
  scan.append(r)
  if n in [14,15,16,18]:rows.append(r)
keys=sorted({k for r in rows for k in r['point'] if len({x['point'][k] for x in rows})>1})
groups=[{'axis':k.removeprefix(P),'note':'Complete public attribute; loop count is the intervention, other changing attributes are inherited five-family context. Fixed controls retained in proposals, never varied independently.', 'keys':[{'key':k,'provenance':'fan_out'}]} for k in keys]
assert len(rows)==20 and len({json.dumps(r['point'],sort_keys=True) for r in rows})==20
write(H/'axes.json',{'schema_version':'study-axis-declaration/v1','groups':groups})
for name in ['proposals.json','unique-proposals.json']:write(PREP/name,rows)
write(PREP/'scan-proposals.json',scan)
print('Prepared',len(rows),'native proposals,',len(scan),'oracle scan rows,',len(groups),'groups; no evaluation.')
