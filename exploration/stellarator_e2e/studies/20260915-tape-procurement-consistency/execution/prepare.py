"""Capture the released candidate and resolve proposal coordinates without evaluating points."""
import json, shutil, hashlib
from pathlib import Path
from exploration.stellarator_e2e.studies import study_route as route
from scripts.study.verify import package_input_values
from scripts.study.preflight import package_channels
H=Path(__file__).resolve().parents[1]; ROOT=H.parents[3]; P=H/'preparation'; R=H/'results'
def write(p,x): p.write_text(json.dumps(x,indent=2,allow_nan=False)+'\n')
G=ROOT/'work/orchestration/goals/tape-procurement-consistency/evidence'
release=json.loads((G/'T-006_integration/integration_return.json').read_text()); assert release['class']=='CANDIDATE'; assert all(g['status']=='pass' for g in release['gates'])
assert release['candidate']['pin']=='b028a7d198da6184e7e28d98bbb22f20485094a60c652d27be963e9babeedbe1'
shutil.copy2(G/'T-006_integration/integration_return.json',P/'integration-return.json')
for f in ['design-review.md','implementation-review.md']: shutil.copy2(G/f,H/'reviews'/f)
for f in ['tape-basis-research.md','preimplementation-prediction.json']: shutil.copy2(G/f,P/f)
shutil.copy2(ROOT/'work/active/WI-060_tape-procurement-quantity-basis/design.md',P/'implemented-design.md')
for f in ['manifest.json','oracle_entry.py','ANNEX.md','study_route.py']: shutil.copy2(H.parent/f,P/f)
for f in ['verify_stellaris.py','oracle_finance.py']: shutil.copy2(H.parent.parent/f,P/f)
for d in ['contracts','inputs','pipelines','schemas']: shutil.copytree(route.PACKAGE_DIR/d,P/('package-'+d),dirs_exist_ok=True)
params=package_input_values(route.PACKAGE_DIR); write(P/'resolved-defaults.json',params)
write(P/'required-channels.json',sorted(package_channels(route.PACKAGE_DIR)))
rows=json.loads((P/'proposals-draft.json').read_text()); axes=json.loads((H/'axes.json').read_text())['groups']; keys=[g['keys'][0]['key'] for g in axes]
seen={}; unique=[]
for r in rows:
 r['original_point']=r['point']; r['point']={k:r['point'].get(k,params[k]) for k in keys}
 # Explicitly preserve all non-axis overrides, including the pinned calendar mode.
 r['point'].update(r['original_point']); sig=json.dumps(r['point'],sort_keys=True)
 # Compare full resolved parameter sets, since the explicit baseline adds default fields.
 sig=json.dumps(params|r['point'],sort_keys=True)
 if sig not in seen: seen[sig]=r['id']; unique.append({'proposal_id':r['id'],'point':r['point']})
 r['canonical_proposal_id']=seen[sig]
write(P/'proposals.json',rows); write(P/'unique-proposals.json',unique)
print('resolved',len(rows),'report rows;',len(unique),'unique native cases;',len(package_channels(route.PACKAGE_DIR)),'native channels')
