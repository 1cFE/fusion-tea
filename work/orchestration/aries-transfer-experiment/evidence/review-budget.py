"""Independent WI088 convention, guarded interface and exact reuse checks."""
import hashlib,json,math
from pathlib import Path
from decimal import Decimal
import yaml
from simkit.core.pipeline import execute_pipeline
from simkit.evaluation.package_load import ProvisionalPackageLoader
ROOT=Path.cwd();E=ROOT/'work/orchestration/aries-transfer-experiment/evidence';R=Path('/tmp/aries-budget-review');R.mkdir(exist_ok=True)
pkg=ROOT/'exploration/aries_transfer/source_budget/budget_tea';ev=ROOT/'work/active/WI-088_aries-source-budget-cost-contribution/evidence';hashes=json.loads((ev/'build-hashes.json').read_text())
for p,h in hashes['source_hashes'].items():assert hashlib.sha256((ROOT/p).read_bytes()).hexdigest()==h
for p,h in hashes['completion_hashes'].items():assert hashlib.sha256((pkg/'handwritten/source_budget_accounting'/p).read_bytes()).hexdigest()==h
original=ROOT/'exploration/stellarator_e2e/generated/handwritten/mfe_account_costs/n_1cfe_form_lcoe_impl.py';copied=pkg/'handwritten/mfe_account_costs/n_1cfe_form_lcoe_impl.py';assert original.read_text()==copied.read_text().replace('from budget_tea.','from stellarator_tea.')
mod,fp=ProvisionalPackageLoader(package_dir=pkg,package_name='budget_tea',link_root=R/'links').load()
P='aries_source_budget__';base=json.loads((pkg/'inputs/source_budget_params.json').read_text());cfg=yaml.safe_load((pkg/'pipelines/pipeline.yaml').read_text());assert not any(k.endswith(('module_count','excluded_annual_channel')) for k in base)
assert all(v.startswith('float '+P+'budget_period__period__') for v in cfg['modules'][P+'partial_cost__cost_per_energy']['inputs'].values())
rows=[]
for name,changes,error in [('literal',{'budget_period__selected_availability':.6,'land__selected_cost_usd2004':15000000.},None),('fpy',{'budget_period__selected_availability':.6,'land__selected_cost_usd2004':15000000.,'budget_period__selected_mode':1.},None),('ratio_overflow',{'land__selected_cost_usd2004':1e300,'budget_period__selected_net_power':1e-20},'nonfinite partial cost quotient'),('extra_module',{'budget_period__module_count':2.},'Extra inputs'),('extra_cost',{'budget_period__excluded_annual_channel':100.},'Extra inputs')]:
 d=R/name;d.mkdir(exist_ok=True);values={**base,**{P+k:v for k,v in changes.items()}};inp=d/'inputs.json';inp.write_text(json.dumps(values));cfg['modules']['entry_fusion']['inputs']['source_budget_params']='SourceBudgetParams '+str(inp);pipe=d/'pipeline.yaml';pipe.write_text(yaml.safe_dump(cfg))
 try:raw=execute_pipeline(pipe,d/'outputs',registry=mod.create_budget_tea_registry(),custom_schema_types=mod.CUSTOM_SCHEMA_TYPES).outputs
 except Exception as exc:
  assert error and error in str(exc),(name,str(exc));rows.append(dict(case=name,refused=True,message=str(exc)));continue
 assert error is None
 out={k:v.model_dump(mode='json') if hasattr(v,'model_dump') else v for k,v in raw.items()};period=Decimal(40) if name=='literal' else Decimal(40)/Decimal('.6');direct=Decimal('2619572000')+Decimal('2071000');capital=direct*Decimal('1.93');replacement=Decimal('966000000');energy=Decimal(8760)*Decimal(1000)*Decimal('.6');expected=float((capital+replacement)/(period*energy));value=out[P+'partial_cost__cost_per_energy__lcoe']
 assert math.isclose(value,expected,rel_tol=3e-15)
 assert out[P+'capital_budget__total__direct_total']==float(direct)
 prefix=P+'budget_period__period__';assert out[prefix+'module_count']==1 and out[prefix+'excluded_annual_channel']==0
 for key,expected_value in [('comparison_period',period),('annual_capital',capital/period),('annual_replacement',replacement/period),('annual_energy',energy),('lifetime_energy',energy*period)]:assert math.isclose(out[prefix+key],float(expected_value),rel_tol=3e-15)
 # Execute the original exact implementation body against identical guarded inputs.
 original_namespace={};exec('\n'.join(line for line in original.read_text().splitlines() if not line.startswith('from stellarator_tea.')).replace('inputs: n_1cfe_Form_LCOEInput','inputs'),original_namespace)
 from types import SimpleNamespace
 ref=original_namespace['run_n_1cfe_form_lcoe'](SimpleNamespace(cas90=out[prefix+'annual_capital'],cas70=out[prefix+'annual_replacement'],cas80=0.,net_electric_mw=1000.,n_mod_in=1.,availability_in=.6));assert value==ref
 rows.append(dict(case=name,period=float(period),annual_energy_MWh=float(energy),lifetime_energy_MWh=float(energy*period),partial_cost_USD2004_MWh=value,original_formula_exact=True))
assert math.isclose(rows[1]['partial_cost_USD2004_MWh'],.6*rows[0]['partial_cost_USD2004_MWh'],rel_tol=3e-15)
baseline=json.loads((E/'baseline.json').read_text())['files'];changed=[p for p,h in baseline.items() if hashlib.sha256((ROOT/p).read_bytes()).hexdigest()!=h];assert not changed
result=dict(fingerprint=str(fp),cases=rows,protected_count=len(baseline),changed=changed);(E/'review-budget.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
