"""Independent repaired WI086 exchange topology and downstream duty screen."""
import hashlib,json
from pathlib import Path
import yaml
from simkit.core.pipeline import execute_pipeline
from simkit.evaluation.package_load import ProvisionalPackageLoader
ROOT=Path.cwd();E=ROOT/'work/orchestration/aries-transfer-experiment/evidence';R=Path('/tmp/aries-heat-review');R.mkdir(exist_ok=True)
pkg=ROOT/'exploration/aries_transfer/dual_blanket_heat/heat_tea';ev=ROOT/'work/active/WI-086_aries-dual-blanket-heat-accounting/evidence';receipt=json.loads((ev/'results.json').read_text());hashes=json.loads((ev/'build-hashes.json').read_text())
for p,h in hashes['source_hashes'].items():assert hashlib.sha256((ROOT/p).read_bytes()).hexdigest()==h
for p,h in hashes['completion_hashes'].items():assert hashlib.sha256((pkg/'handwritten/dual_circuit_heat_accounting'/p).read_bytes()).hexdigest()==h
original=ROOT/'exploration/stellarator_e2e/generated/handwritten/mfe_viability/offered_capacity_screen_impl.py';copied=pkg/'handwritten/mfe_viability/offered_capacity_screen_impl.py';assert original.read_text()==copied.read_text().replace('from heat_tea.','from stellarator_tea.')
mod,fp=ProvisionalPackageLoader(package_dir=pkg,package_name='heat_tea',link_root=R/'links').load();assert str(fp)==receipt['fingerprint']
P='aries_dual_blanket_heat__';base=json.loads((pkg/'inputs/dual_blanket_heat_params.json').read_text());assert [k for k in base if 'exchange' in k]==[P+'inter_coolant_exchange__transferred_heat_mw']
cfg=yaml.safe_load((pkg/'pipelines/pipeline.yaml').read_text());he=cfg['modules'][P+'helium__heat']['inputs'];pb=cfg['modules'][P+'pbli__heat']['inputs'];assert he['received_exchange_in']==pb['exported_exchange_in'];assert he['exported_exchange_in']==pb['received_exchange_in'];assert 'absent_boundary_exchange_mw.root' in he['exported_exchange_in']
rows=[]
for name,changes,err in [('exchange_and_friction',{P+'inter_coolant_exchange__transferred_heat_mw':50.,P+'pbli__recovered_friction_mw':10.},None),('legacy_extra',{P+'pbli__absent_incoming_exchange_mw':3.},'Extra inputs'),('infinite_transfer',{P+'inter_coolant_exchange__transferred_heat_mw':float('inf')},'finite')]:
 d=R/name;d.mkdir(exist_ok=True);vals={**base,**changes}
 for k in vals:
  if any(k.endswith('__'+s) for s in ('assumed_conditions_supported','scenario_applicable','duty_available')):vals[k]=bool(vals[k])
 inp=d/'inputs.json';inp.write_text(json.dumps(vals));cfg['modules']['entry_fusion']['inputs']['dual_blanket_heat_params']='DualBlanketHeatParams '+str(inp);pipe=d/'pipeline.yaml';pipe.write_text(yaml.safe_dump(cfg))
 try:out=execute_pipeline(pipe,d/'outputs',registry=mod.create_heat_tea_registry(),custom_schema_types=mod.CUSTOM_SCHEMA_TYPES).outputs
 except Exception as exc:
  assert err and err in str(exc),(name,str(exc));rows.append(dict(case=name,refused=True,message=str(exc)));continue
 assert err is None
 expected={P+'helium__heat__delivered_heat':1131.,P+'pbli__heat__delivered_heat':1515.,P+'blanket_ledger__energy__delivered_total':2646.,P+'blanket_ledger__energy__deposited_total':2495.,P+'blanket_ledger__energy__friction_total':151.,P+'blanket_ledger__energy__energy_residual':0.}
 for k,v in expected.items():assert getattr(out[k],"root",out[k])==v
 assert out[P+'helium__capacity__capacity_ok'] is True and out[P+'pbli__capacity__capacity_ok'] is False
 assert vals[P+'helium__offered_duty_mw']==1250 and vals[P+'pbli__offered_duty_mw']==1500
 status=out['constraint_report'].model_dump()['results'];assert sorted(r['status'] for r in status)==['satisfied','violated']
 rows.append(dict(case=name,outputs=expected,helium_capacity_ok=True,pbli_capacity_ok=False,source_residual=-1.))
baseline=json.loads((E/'baseline.json').read_text())['files'];changed=[p for p,h in baseline.items() if hashlib.sha256((ROOT/p).read_bytes()).hexdigest()!=h];assert not changed
result=dict(fingerprint=str(fp),single_public_exchange=True,cases=rows,protected_count=len(baseline),changed=changed);(E/'review-heat.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
