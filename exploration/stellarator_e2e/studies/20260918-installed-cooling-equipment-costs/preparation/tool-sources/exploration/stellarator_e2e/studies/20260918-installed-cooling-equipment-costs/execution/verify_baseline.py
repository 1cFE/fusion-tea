"""Compare retained baseline evidence to corrected oracle without native reevaluation."""
from pathlib import Path
import json,math,sys
H=Path(__file__).resolve().parents[1];ROOT=H.parents[3];sys.path.insert(0,str(ROOT))
from exploration.stellarator_e2e.studies import oracle_entry as oe
from scripts.study.verify import derive_verdict
read=lambda p:json.loads(p.read_text())
b=read(H/'results/baseline_result.json');values=oe.evaluate(b['point']);defaults=read(H/'preparation/resolved-defaults.json');catalog=read(H/'results/predicate-catalog.json');fail=[]
for k,v in values.items():
 got=b['channels'][k]
 if not math.isclose(got,v,rel_tol=1e-9,abs_tol=1e-9):fail.append({'channel':k,'native':got,'oracle':v})
# Native baseline receipt verdicts are published by source-local identity.
for cid,e in catalog.items():
 expected='satisfied' if derive_verdict(cid,e,oe.operand_bindings(),b['point'],defaults,values)[0] else 'violated'
 got=next(r['status'] for r in b['verdicts'] if r['constraint_id']==cid)
 if got!=expected:fail.append({'constraint_id':cid,'native':got,'oracle':expected})
result={'outcome':'fail' if fail else 'pass','scalar_comparisons':len(values),'predicate_comparisons':len(catalog),'relative_tolerance':1e-9,'absolute_tolerance':1e-9,'failures':fail,'native_reexecution':False}
(H/'results/corrected-oracle-baseline.json').write_text(json.dumps(result,indent=2)+'\n');print(result)
