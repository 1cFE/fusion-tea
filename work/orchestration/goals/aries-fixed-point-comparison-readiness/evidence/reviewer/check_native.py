"""Independent retained-evidence checks and synthetic role-credit probe; no physics."""
import hashlib, importlib.util, json, sqlite3
from pathlib import Path
ROOT=Path(__file__).resolve().parents[6]
P=ROOT/'.project/active/aries-comparison-preparation/package'
HERE=Path(__file__).resolve().parent

def load(name,path):
 s=importlib.util.spec_from_file_location(name,path); m=importlib.util.module_from_spec(s); s.loader.exec_module(m); return m
r=load('reporter',ROOT/'scripts/compare_fixed_point.py')
a=load('accounting',P/'check_accounting.py')
e=load('export',P/'export_model_values.py')
m=json.loads((P/'manifest.json').read_text()); n=json.loads((P/'selected-mode/native-result.json').read_text())
c=json.loads((ROOT/m['package_path']/'contracts/model_contract.json').read_text())
recon=a.reconcile(); assert recon==json.loads((P/'reconciliation.json').read_text())
con=sqlite3.connect('file:'+str(P/'selected-mode/native/frozen-fixed-point.db')+'?mode=ro',uri=True)
row=con.execute('select candidate_id,state,inputs_json,evidence_digest from cases').fetchall(); assert len(row)==1
cid,state,inputs,digest=row[0]; assert cid==n['candidate_id'] and state==n['state']
artifact=P/'selected-mode/native/artifacts'/f'{digest}.json'; data=artifact.read_bytes(); assert hashlib.sha256(data).hexdigest()==digest
proof=json.loads(data); assert all(proof['outputs'][k]==v for k,v in n['outputs'].items())
assert {v['constraint_id']:v['status'] for v in proof['report']['results']}==n['verdicts']
# Synthetic declared observations isolate row credit; no physical/reference values.
o=json.loads((P/'synthetic-input.json').read_text()); report=r.compare(m,o)
credit={x['id']:{k:x[k] for k in ('role','status','independent_credit')} for x in report['rows'] if x['id'] in ('fit_cavity_y','fit_exterior_x','installed_wallplug')}
exported=e.extract(m,c,n)
assert len(exported['quantities'])==len(m['quantities'])
assert exported==json.loads((P/'selected-mode-values.json').read_text())
result={'physics_evaluations':0,'quantities':len(m['quantities']),'all_reconciliation_receipt_equal':True,'accounting_checks':len(recon['checks']),'selected_case_store_join':True,'selected_artifact_digest':digest,'selected_export_exact':True,'synthetic_alias_credit':credit,'file_hashes':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in [P/'manifest.json',ROOT/'scripts/compare_fixed_point.py',P/'export_model_values.py']}}
(HERE/'native-check.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
