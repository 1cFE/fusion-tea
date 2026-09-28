"""Fresh audit oracle: literal dates for integer streams, Decimal powers otherwise."""
import json, math, shutil
from pathlib import Path
from decimal import Decimal as D, localcontext
from dataclasses import replace
from tests.ife_oracle import BASE, BOUNDARIES, PREFIX, NET_GATE
from simkit.evaluation.evaluator import PreparedEvaluator
from simkit.evaluation.package_load import ProvisionalPackageLoader
from simkit.study.bridge import CandidateBridge
from sysml_codegen.cli import GenerationConfig, run_codegen
root=Path(__file__).resolve().parent
package=Path('exploration/ife_e2e/generated').resolve()
def evaluator(path,link):
 e=PreparedEvaluator(ProvisionalPackageLoader(path,'ife_tea',root/link),path/'pipelines/pipeline.yaml',expects_constraint_report=True)
 return e,CandidateBridge(e.entry_models)
e,b=evaluator(package,'audit-link')
rates=[.08,0.]+[s*10.**-p for p in [4,8,12,14,16,18] for s in [1,-1]]
cases=[(name,over|dict(construction_duration=c,operational_duration=o,discount_rate=r)) for c,o in [(5.,40.),(5.5,40.5),(.25,.5),(1.,1.),(20.,100.),(50.5,200.5)] for name,over in [('baseline',{}),('zero',BOUNDARIES['zero']),('negative',BOUNDARIES['counterexample'])] for r in rates+([.5,-.5] if name=='baseline' else [])]
cases += [('positive_neighbor',BOUNDARIES['positive_neighbor']|dict(discount_rate=r)) for r in [0.,1e-12,-1e-12,.08]]
rows=[]
for name,over in cases:
 result=e.evaluate(b.build({PREFIX+k:v for k,v in over.items()}))
 with localcontext() as ctx:
  ctx.prec=90
  v={k:D(str(x)) for k,x in (BASE|over).items()}
  beam=v['driver__beam_energy_mj']; f=v['frequency']; eff=v['driver__efficiency']; gain=v['gain']; av=v['availability']
  net=beam*10**6*f*(gain*v['chamber__blanket_energy_multiple']*v['thermal_efficiency']-2/eff)
  shots=f*av*D('31557600')
  driver=(D('.32')+D('.088')*beam)*(D('1.25')+D('.05')*v['driver__num_chambers'])*(1+D('.0088')*(f-5))*10**9
  capital=v['plant_cost_constant']*net/1000+v['chamber__yield_cost_constant']*beam*gain/1000+driver
  running=v['target_factory__cost_per_target']*shots+v['om_cost_constant']*net/1000+driver*shots/v['driver__lifetime_shots']
  annual_energy=net/10**6*8760*av
  c=v['construction_duration']; o=v['operational_duration']; rate=v['discount_rate']; q=1+rate
  integer=c==int(c) and o==int(o)
  if integer:
   cost=sum((capital/c)/q**year for year in range(1,int(c)+1))+sum(running/q**year for year in range(int(c)+1,int(c+o)+1))
   energy=sum(annual_energy/q**year for year in range(int(c)+1,int(c+o)+1))
   fc=sum(q**-year for year in range(1,int(c)+1)); fo=sum(q**-year for year in range(int(c)+1,int(c+o)+1))
  else:
   fc=c if rate==0 else (1-q**(-c))/rate
   fo=o if rate==0 else (q**(-c)-q**(-c-o))/rate
   cost=capital*fc/c+running*fo; energy=annual_energy*fo
  expected={'lcoe_calc__discounted_cost':cost,'lcoe_calc__discounted_energy':energy,'hawker_price__price':cost/energy if net>0 else D(0),'pv_factors__construction_factor':fc,'pv_factors__operation_factor':fo}
  errors={}
  for key,want in expected.items():
   actual=result.outputs[PREFIX+key]; assert math.isfinite(actual)
   residual=abs(D.from_float(actual)-want)/(abs(want) if want else 1)
   assert residual <= D('1e-9'),(name,over,key,residual)
   errors[key]=float(residual)
  eligible=net>0
  assert result.responses[NET_GATE]==('satisfied' if eligible else 'violated')
  for method in ['hawker','meier']:
   assert result.outputs[PREFIX+method+'_price__generating']==float(eligible)
   if not eligible: assert result.outputs[PREFIX+method+'_price__price']==0
  rows.append(dict(scenario=name,inputs=over,reference_kind='dated' if integer else 'fractional',expected={k:str(x) for k,x in expected.items()},actual={k:result.outputs[PREFIX+k] for k in expected},errors=errors))
(root/'numerical.json').write_text(json.dumps(rows,indent=2)+'\n')
print('FRESH NUMERICAL',len(rows),'max residual',max(max(row['errors'].values()) for row in rows))
base=json.loads(Path('work/active/WI-049_ife-zero-discount-repair/entry-baseline/baseline_result.json').read_text())
result=e.evaluate(b.build({})); assert len(result.outputs)==32 and len(base['channels'])==30
residuals={k:abs(result.outputs[k]-v)/abs(v) if v else abs(result.outputs[k]) for k,v in base['channels'].items()}
assert max(residuals.values())<=1e-9
assert all(result.responses[x['constraint_id']]==x['status'] for x in base['verdicts'])
print('BASELINE 30 channels max residual',max(residuals.values()),'two exact verdicts')
(root/'baseline.json').write_text(json.dumps(residuals,indent=2)+'\n')
copy=root/'native-copy'; shutil.copytree(package,copy,ignore=shutil.ignore_patterns('__pycache__'),dirs_exist_ok=True)
config=GenerationConfig(models_path=Path('exploration/ife_e2e/models').resolve(),output_path=copy,package_name='ife_tea',overwrite=True,preserve_handwritten=True)
def tree(): return {str(p.relative_to(copy)):p.read_bytes() for p in copy.rglob('*') if p.is_file() and '__pycache__' not in p.parts}
before=tree()
for smart in [False,True]:
 assert run_codegen(replace(config,smart_regen=smart)); assert tree()==before
 print('NATIVE COPY BYTE IDENTITY',smart,len(before))
shutil.rmtree(copy)
