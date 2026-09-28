"""Resolve and preserve the coordinator-released candidate without evaluating points."""
import json,shutil
from pathlib import Path
H=Path(__file__).resolve().parents[1]; ROOT=H.parents[3];PREP=H/'preparation'
def read(p):return json.loads(p.read_text())
def write(p,x):p.write_text(json.dumps(x,indent=2,allow_nan=False)+'\n')
release=read(PREP/'scan-release.json');assert release['authorized_by']=='coordinator'
candidate={'candidate':release}
from exploration.stellarator_e2e.studies import study_route as route
from scripts.study.verify import package_input_values
from scripts.study.common import assert_tree_clean

for n in ['manifest.json','oracle_entry.py','ANNEX.md','study_route.py']:shutil.copy2(H.parent/n,PREP/n)
for n in ['verify_stellaris.py','oracle_finance.py']:shutil.copy2(H.parent.parent/n,PREP/n)
for n in ['contracts','inputs','pipelines','schemas']:shutil.copytree(route.PACKAGE_DIR/n,PREP/('package-'+n),dirs_exist_ok=True)
shutil.copy2(ROOT/'work/active/WI-062_absolute-conductor-current-margin/evidence/interface.json',PREP/'interface.json')
interface=read(PREP/'interface.json');m=read(PREP/'manifest.json');c=read(PREP/'package-contracts/model_contract.json')
for key in ['executable_fingerprint','semantic_fingerprint']:assert m['fingerprints']['recorded_provenance'][key]==candidate['candidate'][key]
params=package_input_values(route.PACKAGE_DIR);required=sorted(r['channel_name'] for r in c['outputs'] if r['python_type'] in ['float','int']);catalog=c['constraint_catalog']['concrete_entries']
assert set(interface['outputs'])<=set(required)
assert len(catalog)==20
assert len([r for r in catalog if r['source_local_identity']=='reference_conductor_current_ok'])==1
assert all(params[k]==v for k,v in interface['inputs'].items())
assert params['stellarator_09__stellaris__magnet__coil__turn_current']==50000
keys=[r['key'] for g in read(H/'axes.json')['groups'] for r in g['keys']];assert set(keys)<=set(params)
rows=read(PREP/'proposals-draft.json');unique=[];seen={}
for row in rows:
 row['original_point']=row['point'];row['point']={k:params[k] for k in keys}|row['point']
 sig=json.dumps(params|row['point'],sort_keys=True)
 if sig not in seen:seen[sig]=row['id'];unique.append({'proposal_id':row['id'],'point':row['point']})
 row['canonical_proposal_id']=seen[sig]
assert 0<len(unique)<=320
for n,x in [('resolved-defaults.json',params),('required-channels.json',required),('proposals.json',rows),('unique-proposals.json',unique)]:write(PREP/n,x)
(PREP/'ANNEX-correction.md').write_text('# Study-local annex correction\n\nThe preserved ANNEX.md describes earlier WI-060 counts and pin. For this study the copied manifest and contracts govern the identity and baseline. The final contract contains '+str(len(params))+' public inputs, '+str(len(required))+' numeric outputs and twenty predicates. The old nineteen remain separate from reference_conductor_current_ok. The source/interface review supplies current-margin domain and transfer limitations. Stale count and pin statements in ANNEX.md are historical context only.\n')
print('Resolved',len(rows),'report rows and',len(unique),'native points;',len(params),'inputs;',len(required),'numeric outputs; no evaluation')
