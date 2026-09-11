import sys,json,math,importlib.util,tempfile,hashlib,subprocess,re
from pathlib import Path
root=Path.cwd();sys.path.insert(0,str(root));h=Path(__file__).resolve().parent;support=h.parent/'implementation'
def load(name):
 spec=importlib.util.spec_from_file_location(name,support/(name+'.py'));m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
run=load('run_acceptance');pkg=root/'exploration/stellarator_e2e/generated';ev,bridge=run.evaluator(pkg,'stellarator_tea',Path(tempfile.mkdtemp(prefix='wi050-audit-shipped-'))/'link')
results={name:run.execute(ev,bridge,{run.P+k:v for k,v in controls.items()}) for name,controls in run.CASES.items()}
inputs={}
for f in (pkg/'inputs').glob('*.json'):inputs.update(json.loads(f.read_text()))
def eq(a,b):assert math.isclose(a,b,rel_tol=1e-9,abs_tol=1e-9),(a,b)
retained=json.loads((support/'results.json').read_text())
for name,r in results.items():
 if 'outputs' in r:assert r['outputs']==retained[name]['outputs'] and r['responses']==retained[name]['responses']
 else:assert r['error']==retained[name]['error']
financial={}
for name in ['baseline','reserve','demand','efficiency','availability']:
 o=results[name]['outputs'];v=lambda k:o[run.P+k];i=dict(inputs,**{run.P+k:x for k,x in run.CASES[name].items()});p=lambda k:i[run.P+k]
 rate=p('discount_rate');years=p('operational_years');build=p('construction_years');growth=p('inflation_rate')
 recovery=1/sum((1+rate)**(-t) for t in range(1,int(years)+1))
 capital=v('overnight_capital__overnight_capital');idc=capital*((((1+rate)**build-1)/rate)/build-1)
 eq(idc,v('idc__cost'))
 headline=capital*(1+rate)**(build/2)*recovery;comparison=(capital+idc)*recovery;eq(comparison,v('cas90_1cfe_calc__cas90'))
 annuals={}
 for leaf,raw in [('cas71_calc__levelized','om_cost__annual_om'),('cas80_calc__levelized','fuel_calc__annual_fuel')]:
  # Sum the existing first-year convention explicitly instead of using its closed form.
  pv=sum(v(raw)*(1+growth)**(build+t-1)/(1+rate)**t for t in range(1,int(years)+1));annuals[leaf]=pv*recovery;eq(annuals[leaf],v(leaf))
 life=p('fluence_limit')/v('wall_peak_calc__wall_load_peak');unplanned=p('unplanned_fraction');outage=p('outage_years');elapsed=0;dates=[]
 while True:
  elapsed+=life/(1-unplanned)
  if elapsed+outage>=years:break
  dates.append(elapsed);elapsed+=outage
 event=(v('blanket_cost__cost')+v('divertor_cost__cost'))*p('n_mod');pv=sum(event/(1+rate)**t for t in dates);eq(pv,v('calendar__replacement_pv'));eq(len(dates),v('calendar__n_replacements'));eq(pv*recovery,v('calendar__cas72_annual'))
 energy=8760*v('pb__p_net')*v('calendar__availability');annual=sum(annuals.values())+pv*recovery
 eq((headline+annual)/energy,v('lcoe_calc__lcoe'));eq((comparison+annual)/(energy*p('n_mod')),v('lcoe_1cfe_calc__lcoe'))
 financial[name]={'capital':capital,'idc':idc,'headline_numerator':headline+annual,'comparison_numerator':comparison+annual,'energy':energy,'replacement_dates':dates,'annual':annual}
# Repeat conservation checks whose expressions were read against unchanged source relations.
load('check_results').check(results,inputs)
old=json.loads((root/'work/analysis/20260911-190758_mfe-operating-state-evidence/baseline/all_outputs.json').read_text());new=results['baseline']['outputs'];scalars={k:{'before':v,'after':new[k],'delta':new[k]-v} for k,v in old.items() if k in new and isinstance(v,(int,float)) and isinstance(new[k],(int,float))}
assert len(scalars)==155 and sum(x['delta']!=0 for x in scalars.values())==72
coverage=json.loads((support/'cost-operand-coverage.json').read_text());assert len(coverage)==50
import yaml
modules=yaml.safe_load((pkg/'pipelines/pipeline.yaml').read_text())['modules']
for name,row in coverage.items():assert modules[run.P+name]['inputs']==row['inputs']
manual=json.loads((support/'normative-handwritten.json').read_text())
for path,digest in manual.items():assert hashlib.sha256((pkg/path).read_bytes()).hexdigest()==digest
# Check all tracked implementation bytes are still the frozen implementation bytes.
changed=subprocess.check_output(['git','diff','--name-only','b9d096f6','--','models','exploration/stellarator_e2e/generated','tests/models','data/traceability_matrix.csv','modeling_project/VALIDATION_MATRIX.md',str(support.relative_to(root))]).decode();assert not changed,changed
preserved=['knowledge/SOURCE_INDEX.md','work/active/WI-050_mfe-coherent-operating-heating/prototype','work/active/WI-050_mfe-coherent-operating-heating/prototype-r1','work/active/WI-050_mfe-coherent-operating-heating/review.md','exploration/stellarator_e2e/studies']
assert not subprocess.check_output(['git','diff','--name-only','d8e92cdf','b9d096f6','--',*preserved]).strip()
(h/'shipped-results.json').write_text(json.dumps(results,indent=2,default=str)+'\n');(h/'independent-finance.json').write_text(json.dumps(financial,indent=2)+'\n');(h/'scalar-bridge.json').write_text(json.dumps(scalars,indent=2)+'\n')
(h/'checks.json').write_text(json.dumps({'shipped_retained_parity':True,'explicit_finance_calendar_sums':True,'conservation':True,'historical_scalars':155,'changed':72,'unchanged':83,'cost_modules':50,'manual_hashes':manual,'frozen_implementation_unchanged':True,'historical_preservation':True},indent=2)+'\n')
print('PASS shipped execution, explicit finance sums, conservation, 155 scalar bridge, 50 module operands, frozen and historical preservation')
