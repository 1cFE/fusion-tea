import json
from pathlib import Path
H=Path(__file__).resolve().parents[1];R=H/'results';P='stellarator_09__stellaris__'
read=lambda p:json.loads(p.read_text())
coverage=read(H/'context/inherited-cost-operand-coverage.json');rows=read(R/'cases.json');raw={r['candidate_id']:r for r in read(R/'raw-cases.json')};inputs=read(R/'package-inputs.json');out=[]
for row in rows:
 source={**inputs,**row['inputs'],**raw[row['candidate_id']]['outputs']};mods={}
 for module,m in coverage.items():
  operands={}
  for name,expr in m['inputs'].items():
   token=expr.removeprefix('float ').removesuffix('.root');key=token.split('.')[-1]
   operands[name]={'binding':expr,'key':key,'value':source[key]}
  values={k:source[P+k] for k in m['outputs']}
  mods[module]={'classification_inherited':m['classification'],'inputs':operands,'outputs':values,'deltas_from_baseline':{k:value-raw[rows[2]['candidate_id']]['outputs'][P+k] for k,value in values.items()}}
 out.append({'proposal_index':row['proposal_index'],'candidate_id':row['candidate_id'],'modules':mods})
assert len(coverage)==50
(R/'cost-operands.json').write_text(json.dumps({'scope':'Actual recorded inputs and outputs for all fifty previously audited cost/annual/calendar/finance modules, attributed using copied immutable bindings. Inherited examples in context are not current execution.','cases':out},indent=2)+'\n')
print('50 modules x',len(out),'cases, all operands resolved')
