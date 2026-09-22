"""Independent WI087 native state/energy and role-boundary review."""
import hashlib,json,math
from pathlib import Path
import yaml
from simkit.core.pipeline import execute_pipeline
from simkit.evaluation.package_load import ProvisionalPackageLoader
ROOT=Path.cwd();E=ROOT/'work/orchestration/aries-transfer-experiment/evidence';R=Path('/tmp/aries-brayton-review');R.mkdir(exist_ok=True)
pkg=ROOT/'exploration/aries_transfer/nominal_brayton/brayton_tea';ev=ROOT/'work/active/WI-087_aries-nominal-brayton-component-cycle/evidence'
receipt=json.loads((ev/'results.json').read_text());hashes=json.loads((ev/'build-hashes.json').read_text())
for p,h in hashes['source_hashes'].items():assert hashlib.sha256((ROOT/p).read_bytes()).hexdigest()==h
for p,h in hashes['completion_hashes'].items():assert hashlib.sha256((pkg/'handwritten/ideal_gas_brayton_components'/p).read_bytes()).hexdigest()==h
original=ROOT/'exploration/stellarator_e2e/generated/handwritten/mfe_viability/offered_capacity_screen_impl.py';copied=pkg/'handwritten/mfe_viability/offered_capacity_screen_impl.py';assert original.read_text()==copied.read_text().replace('from brayton_tea.','from stellarator_tea.')
mod,fp=ProvisionalPackageLoader(package_dir=pkg,package_name='brayton_tea',link_root=R/'links').load();assert str(fp)==receipt['fingerprint']
P='aries_nominal_brayton__';base=json.loads((pkg/'inputs/nominal_brayton_params.json').read_text());cfg=yaml.safe_load((pkg/'pipelines/pipeline.yaml').read_text())
rows=[]
for name,changes,error in [('asymmetric_state',{'compressor_2__selected_ratio':1.8,'intercooler_1__target_temperature':320.,'operating_point__return_pressure':4.,'operating_point__selected_flow':1150.},None),('cooler_reinterpreted',{'intercooler_1__heating_role':1.,'intercooler_1__target_temperature':400.},'cooling heat must be nonpositive')]:
 d=R/name;d.mkdir(exist_ok=True);values={**base,**{P+k:v for k,v in changes.items()}}
 for k in values:
  if k.endswith(('__assumed_supported','__scenario_applicable','__demand_available')):values[k]=bool(values[k])
 inp=d/'inputs.json';inp.write_text(json.dumps(values));cfg['modules']['entry_fusion']['inputs']['nominal_brayton_params']='NominalBraytonParams '+str(inp);pipe=d/'pipeline.yaml';pipe.write_text(yaml.safe_dump(cfg))
 try:raw=execute_pipeline(pipe,d/'outputs',registry=mod.create_brayton_tea_registry(),custom_schema_types=mod.CUSTOM_SCHEMA_TYPES).outputs
 except Exception as exc:
  assert error and error in str(exc),(name,str(exc));rows.append(dict(case=name,refused=True,message=str(exc)));continue
 assert error is None
 out={k:v.model_dump(mode='json') if hasattr(v,'model_dump') else v for k,v in raw.items()}
 def get(part,calc,key):return out[P+part+'__'+calc+'__'+key]
 def close(a,b):assert math.isclose(a,b,rel_tol=2e-13,abs_tol=2e-9),(a,b)
 c=1150.*5193./1e6;a=.4;p=4.;tin=308.15;work=0.;rejected=0.
 for i,r in enumerate([base[P+'compressor_1__selected_ratio'],1.8,base[P+'compressor_3__selected_ratio']],1):
  p*=r;tout=tin*(1+(r**a-1)/.89)
  close(get(f'compressor_{i}','performance','pressure_out'),p);close(get(f'compressor_{i}','performance','temperature_out'),tout)
  close(get(f'compressor_{i}','performance','shaft_demand'),c*(tout-tin));work+=c*(tout-tin)
  if i<3:
   tin=320. if i==1 else 308.15;rejected+=c*(tout-tin)
 tt=980.15*(1-.93*(1-(4./(p*.955))**a));close(get('equivalent_turbine','performance','temperature_out'),tt)
 cold=tout+.95*(tt-tout);hot=tt-.95*(tt-tout);qh=c*(980.15-cold);rejected+=c*(hot-308.15);net=c*(980.15-tt)-work
 for field,expected in [('compressor_demand',work),('rejected_heat',rejected),('net_shaft',net),('shaft_efficiency',net/qh),('energy_residual',0.),('total_pressure_ratio',p/4.)]:close(get('cycle_ledger','balance',field),expected)
 close(get('heater','conditioning','heat_into_fluid'),qh);close(qh-rejected,net)
 close(get('recuperator','exchange','cold_temperature_out')+get('recuperator','exchange','hot_temperature_out'),tout+tt)
 verdicts={}
 for kind,demand,rating in [('compressor',work,1100.),('heater',qh,2000.),('rejection',rejected,1200.)]:
  assert values[P+kind+'_capacity__offered_rating']==rating
  verdicts[kind]=out[P+kind+'_capacity__screen__capacity_ok'];assert verdicts[kind]==(rating>=demand)
 assert not all(verdicts.values())
 rows.append(dict(case=name,discharge_pressure_MPa=p,total_ratio=p/4.,compressor_MW=work,heater_MW=qh,rejected_MW=rejected,net_shaft_MW=net,capacity_ok=verdicts,energy_residual_MW=get('cycle_ledger','balance','energy_residual')))
baseline=json.loads((E/'baseline.json').read_text())['files'];changed=[p for p,h in baseline.items() if hashlib.sha256((ROOT/p).read_bytes()).hexdigest()!=h];assert not changed
result=dict(fingerprint=str(fp),cases=rows,protected_count=len(baseline),changed=changed);(E/'review-brayton.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
