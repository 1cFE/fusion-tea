import json,hashlib,sys
from pathlib import Path
sys.path.insert(0,str(Path.cwd()))
from agentic_mbse.sysml.syside_adapter import get_syside
out=Path(__file__).resolve().parent/'evidence'
syside=get_syside(); files=sorted(Path('models').rglob('*.sysml'))
model,diagnostics=syside.try_load_model([str(p) for p in files])
errors=[str(d) for category in ('parser','sema') for d in getattr(diagnostics,category) if d.severity==syside.DiagnosticSeverity.Error]
rows=[]
for kind in ('PartDefinition','PartUsage','AttributeUsage','CalculationDefinition','CalculationUsage','ConstraintUsage','AssertConstraintUsage','ConstraintDefinition'):
 for e in model.elements(getattr(syside,kind)):
  q=str(e.qualified_name)
  if not any(x in q.lower() for x in ('mfe','stellarator','stellaris','fusion_cycle','hif','ife')): continue
  row={'kind':kind,'qualified_name':q,'name':e.name,'documentation':[d.body for d in e.documentation]}
  rows.append(row)
(out/'model-traversal.json').write_text(json.dumps({'source_hashes':{str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in files},'errors':errors,'elements':rows},indent=2)+'\n')
print('files',len(files),'errors',len(errors),'elements',len(rows))
print({k:sum(r['kind']==k for r in rows) for k in set(r['kind'] for r in rows)})
import yaml
package=Path('exploration/stellarator_e2e/generated')
c=json.loads((package/'contracts/model_contract.json').read_text())
y=yaml.safe_load((package/'pipelines/pipeline.yaml').read_text())
consumers={}
for module,desc in y['modules'].items():
 for port,binding in (desc.get('inputs') or {}).items():
  consumers.setdefault(binding.split(' ',1)[-1],[]).append({'module':module,'input':port})
params=[]
for p in c['parameters']:
 key=p['param_group']+'.'+p['qualified_name']
 params.append(dict(p,consumers=consumers.get(key,[])))
(out/'generated-binding-census.json').write_text(json.dumps({'parameters':params,'modules':y['modules'],'outputs':c['outputs'],'constraint_catalog':c['constraint_catalog'],'source_hashes':{str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in [package/'contracts/model_contract.json',package/'pipelines/pipeline.yaml']}},indent=2)+'\n')
print('parameters',len(params),'modules',len(y['modules']),'outputs',len(c['outputs']),'unconsumed',sum(not p['consumers'] for p in params))
