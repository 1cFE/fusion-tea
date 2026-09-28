import json,sys
from pathlib import Path
from exploration.stellarator_e2e.studies import oracle_entry as oe,study_route as route
from scripts.study.verify import evaluate_operand,package_input_values
H=Path(__file__).resolve().parents[1];P=route.P
cat=route._catalog_by_constraint_id(route.PACKAGE_DIR);b=oe.operand_bindings();params=package_input_values(route.PACKAGE_DIR)
rows=[]
for f in sorted((H/'results').glob('*-oracle-scan.json')):rows+=json.loads(f.read_text())['rows']
seen=set();out=[]
for r in rows:
 k=json.dumps(r['point'],sort_keys=True)
 if k in seen:continue
 seen.add(k)
 if r['outcome']!='evaluated':continue
 margins={}
 for cid,e in cat.items():
  ir=json.loads(e['predicate_ir']); x,y=[evaluate_operand(cid,o,b,r['point'],params,r['channels'])[0] for o in ir['operands']]
  s=(y-x) if ir['operator'] in ('<=','<') else (x-y)
  margins[e['source_local_identity']]={'lhs':x,'rhs':y,'margin':s,'normalized':s/max(abs(x),abs(y),1)}
 out.append(r|{'margins':margins,'score':min(v['normalized'] for v in margins.values())})
out.sort(key=lambda r:r['score'],reverse=True)
(H/'results/ranked.json').write_text(json.dumps(out,indent=2)+'\n')
for r in out[:16]:print(r['id'],[round(r['point'][P+k],5) for k in ['plasma__R','plasma__a','magnet__coil__I_coil','magnet__coil__coil_t']],round(r['score'],5),[(k,round(v['margin'],5)) for k,v in r['margins'].items() if v['margin']<0])
print('count',len(out),'pass',sum(r['full_satisfied'] for r in out),'total calls',len(rows))
