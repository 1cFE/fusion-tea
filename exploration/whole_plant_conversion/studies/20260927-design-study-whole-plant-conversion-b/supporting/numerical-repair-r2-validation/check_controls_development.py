"""Stock-rule regression of retained native controls and development receipts."""
from pathlib import Path
from types import SimpleNamespace
import sys,json,hashlib
ROOT=Path(__file__).resolve().parents[6];HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT))
from scripts.study import verify as stock,manifest
from exploration.whole_plant_conversion import verify
from exploration.whole_plant_conversion.studies import study_route as route
loaded=manifest.load(route.MANIFEST_PATH);_,evaluate,bindings=stock.load_oracle(loaded)
objectives=stock.objective_channels(loaded);limits={r['channel']:r['value'] for r in loaded.data.get('absolute_tolerances',[])}
catalog={r['constraint_id']:r for r in json.loads((route.PACKAGE_DIR/'contracts/model_contract.json').read_text())['constraint_catalog']['concrete_entries']};package_inputs=stock.package_input_values(route.PACKAGE_DIR)
wi=ROOT/'work/active/WI-098_whole-plant-conversion-comparison/evidence'
groups={'controls498':sorted((wi/'conversion-controls/native').glob('batch-*/cases.json')),'development35':[wi/'development-final/native/cases.json']}
summaries={}
for name,paths in groups.items():
 rows=[];sources=[]
 for path in paths:
  sources.append(dict(path=str(path.relative_to(ROOT)),sha256=hashlib.sha256(path.read_bytes()).hexdigest()))
  for row in json.loads(path.read_text())['cases']:
   label=row['case'];result=dict(case=label)
   if row.get('state')=='completed':
    case=SimpleNamespace(candidate_id=row.get('candidate_id',label),inputs=row['inputs'],outputs=row['outputs'],verdicts={k:v for k,v in row['responses'].items() if k!='headline'},executable_fingerprint=row['executable_fingerprint'])
    try:
     worst,compared,predicates,_=stock.check_case(case,evaluate,bindings,catalog,objectives,package_inputs,route.interface()['executable_fingerprint'],limits)
     result.update(status='pass',scalar_comparisons=len(compared),predicates=len(predicates),worst_relative_deviation=worst[0])
    except Exception as error:result.update(status='fail',error=repr(error))
   else:
    try:evaluate(row['inputs'])
    except (ValueError,ZeroDivisionError) as error:result.update(status='consistent_refusal',oracle_error=str(error),native_state=row.get('state'))
    else:result.update(status='fail',error='native refusal has no corresponding independent refusal')
   rows.append(result)
  print(name,path.parent.name,len(rows),flush=True)
 counts={s:sum(r['status']==s for r in rows) for s in ('pass','consistent_refusal','fail')}
 summary=dict(status='pass' if counts['fail']==0 else 'fail',cases=len(rows),counts=counts,scalar_comparisons=sum(r.get('scalar_comparisons',0) for r in rows),predicate_comparisons=sum(r.get('predicates',0) for r in rows),sources=sources,results=rows)
 (HERE/(name+'.json')).write_text(json.dumps(summary,indent=2)+'\n');summaries[name]={k:v for k,v in summary.items() if k not in ('sources','results')}
assert summaries['controls498']['counts']=={'pass':498,'consistent_refusal':0,'fail':0}
assert summaries['development35']['counts']=={'pass':32,'consistent_refusal':3,'fail':0}
(HERE/'controls-development-summary.json').write_text(json.dumps(summaries,indent=2)+'\n');print(json.dumps(summaries,indent=2))
