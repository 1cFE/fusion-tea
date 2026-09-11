from pathlib import Path
import json
from sysml_codegen.cli import GenerationConfig, run_codegen
from simkit.evaluation.evaluator import PreparedEvaluator
from simkit.evaluation.package_load import ProvisionalPackageLoader
from simkit.study.bridge import CandidateBridge
root=Path(__file__).parent.resolve(); package=root/'generated'/'wi048_probe'
assert run_codegen(GenerationConfig(models_path=root/'models',output_path=package,package_name='wi048_probe',overwrite=True))
(package/"handwritten/ife_lcoe/generating_electricity_price_impl.py").write_text((root/"price_impl.py").read_text())
assert run_codegen(GenerationConfig(models_path=root/"models",output_path=package,package_name="wi048_probe",overwrite=True,preserve_handwritten=True))
evaluator=PreparedEvaluator(ProvisionalPackageLoader(package,'wi048_probe',root/'link'),package/'pipelines/pipeline.yaml',expects_constraint_report=True)
bridge=CandidateBridge(evaluator.entry_models)
p='hif_plant_pkg__hif_plant__'
cases={'baseline':{}, 'beam10':{'driver__beam_energy_mj':10.0},'eff35':{'driver__efficiency':0.35},'rate5':{'frequency':5.0},'negative':{'driver__efficiency':0.1,'gain':100.0,'chamber__blanket_energy_multiple':0.6,'thermal_efficiency':0.3},'zero':{'frequency':5.0,'driver__efficiency':0.1,'gain':100.0,'chamber__blanket_energy_multiple':1.0,'thermal_efficiency':0.2},'positive':{'driver__efficiency':0.1,'gain':100.0,'chamber__blanket_energy_multiple':1.0,'thermal_efficiency':0.21}}
results={}
for name,values in cases.items():
 r=evaluator.evaluate(bridge.build({p+k:v for k,v in values.items()})); print(name,dict(r.responses)); results[name]={'outputs':dict(r.outputs),'responses':dict(r.responses)}
(root/'execution.json').write_text(json.dumps(results,indent=2))
from math import isclose
for name, record in results.items():
 o=record['outputs']; lp=p+'lcoe_calc__'; d=p+'driver__meier_cost__'
 assert isclose(o[lp+'net_electric_power'],o[lp+'gross_electric_power']-o[lp+'driver_electric_power']-o[lp+'other_parasitic_power'],rel_tol=1e-9,abs_tol=1e-6)
 assert isclose(o[d+'gamma']*o[d+'bank_energy_joules'],o[d+'cost_billions']*1e9,rel_tol=1e-9)
 for usage in ('hawker_price','meier_price'):
  valid=o[p+usage+'__generating']; cost=o[p+usage+'__price']
  assert valid == (0.0 if name in ('negative','zero') else 1.0)
  if not valid: assert cost == 0.0 and record['responses']['headline']=='violated'
b=results['baseline']['outputs']; doubled=results['beam10']['outputs']; d=p+'driver__meier_cost__'
assert isclose(doubled[d+'bank_energy_joules']/b[d+'bank_energy_joules'],2.0,rel_tol=1e-9)
assert isclose(doubled[d+'cost_billions']/b[d+'cost_billions'],1.5789473684210527,rel_tol=1e-9)
print('PASS: identities, beam mutation, and invalid-price/verdict pairing for seven public executions')
