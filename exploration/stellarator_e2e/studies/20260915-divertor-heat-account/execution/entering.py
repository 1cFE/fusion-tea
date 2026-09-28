"""Use the isolated captured entering oracle at every selected point; no old native run."""
import importlib.util
import json
import sys
from pathlib import Path
from scripts.study.verify import derive_verdict

H=Path(__file__).resolve().parents[1]
R=H/'results'
P='stellarator_09__stellaris__'
read=lambda p:json.loads(p.read_text())
def load(name,path):
    spec=importlib.util.spec_from_file_location(name,path)
    m=importlib.util.module_from_spec(spec)
    sys.modules[name]=m
    spec.loader.exec_module(m)
    assert Path(m.__file__).resolve()==path.resolve()
    return m

old=H/'preparation/entering'
load('oracle_finance',old/'oracle_finance.py')
load('verify_stellaris',old/'verify_stellaris.py')
oe=load('divertor_entering_oracle',old/'oracle_entry.py')
catalog={e['constraint_id']:e for e in read(old/'model-contract.json')['constraint_catalog']['concrete_entries']}
current={e['constraint_id']:e for e in read(H/'preparation/package-contracts/model_contract.json')['constraint_catalog']['concrete_entries']}
assert len(catalog)==20
assert {k:e['predicate_ir'] for k,e in catalog.items()}=={k:e['predicate_ir'] for k,e in current.items()}
params={}
for path in (old/'inputs').glob('*.json'):
    data=read(path)
    if isinstance(data,dict): params.update(data)
# This contract exports qualified keys in per-channel input files.
assert P+'divertor__q_target_limit' in params
rows=[]
for row in read(R/'native-cases.json'):
    point={k:v for k,v in row['inputs'].items() if k!=P+'divertor__target_capture_fraction'}
    try:
        channels=oe.evaluate(point)
        verdicts={cid:'satisfied' if derive_verdict(cid,e,oe.operand_bindings(),point,params,channels)[0] else 'violated' for cid,e in catalog.items()}
        rows.append({'proposal_id':row['proposal_id'],'point':point,'outcome':'evaluated','channels':channels,'verdicts':verdicts})
    except Exception as error:
        rows.append({'proposal_id':row['proposal_id'],'point':point,'outcome':'refused','error':repr(error)})
result={'scope':'Isolated frozen f76 entering oracle at matched points with only new capture input removed; not old-native reexecution. Original native controls retained separately.','predicate_ir_identical':True,'rows':rows}
(R/'entering-all-points.json').write_text(json.dumps(result,indent=2,allow_nan=False)+'\n')
print('Entering comparisons',len(rows),'refused',sum(r['outcome']=='refused' for r in rows))
