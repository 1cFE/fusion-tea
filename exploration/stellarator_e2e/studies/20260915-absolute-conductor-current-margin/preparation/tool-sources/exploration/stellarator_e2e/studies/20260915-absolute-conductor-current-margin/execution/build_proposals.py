"""Prepare declared coordinates only; never import an evaluator."""
import json
from pathlib import Path
H=Path(__file__).resolve().parents[1]
P='stellarator_09__stellaris__'
def read(p):return json.loads(p.read_text())
def write(p,x):p.write_text(json.dumps(x,indent=2,allow_nan=False)+'\n')
selection=read(H/'preparation/selection.json')
entering=read(H/'preparation/entering-comparison.json')['rows']
interface=read(H/'preparation/interface-preliminary.json')
controls={key.removeprefix(P+'magnet__winding_pack__'):key for key in interface['inputs']}
rows=[{'id':r['proposal_id'],'arm':'entering','family':'entering-controls','point':r['point']} for r in entering]
byid={r['id']:r for r in rows}
for aid in selection['anchors']:
 for scenario in selection['scenarios']:
  rows.append({'id':aid+'--'+scenario['id'],'arm':scenario['id'],'family':'performance-sensitivity','anchor_id':aid,'scenario':scenario['id'],'basis':scenario['basis'],'point':byid[aid]['point']|{controls[k]:v for k,v in scenario['controls'].items()}})
for factor in [.8,1.2]:
 rows.append({'id':f'reference--turn-{factor}','arm':'turn_current','family':'turn-repartition','anchor_id':'reference','point':{P+'magnet__coil__turn_current':50000*factor},'basis':'Agent repartition control at unchanged coil ampere-turns; release preparation verifies nominal 50000 A.'})
rows.append({'id':'m000--orientation-3-independence','arm':'predicate-independence','family':'predicate-independence','anchor_id':'m000','point':byid['m000']['point']|{controls['orientation_factor']:3.0},'basis':'Agent assumed orientation scenario tests current versus selected-envelope independence; no qualification.'})
assert len(rows)==296
keys=sorted({k for r in rows for k in r['point']})
axes={'schema_version':'study-axis-declaration/v1','groups':[{'axis':k.removeprefix(P),'note':'Complete attribute public input group; candidate contract validation required. Sensitivity only.','keys':[{'key':k,'provenance':'fan_out'}]} for k in keys]}
write(H/'preparation/proposals-draft.json',rows);write(H/'axes.json',axes)
print(len(rows),'report rows;',len(keys),'declared input groups; no evaluation')
