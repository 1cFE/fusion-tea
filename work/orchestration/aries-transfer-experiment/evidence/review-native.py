"""Independent targeted native replay and original-file preservation check."""
import hashlib,json,math
from pathlib import Path
from decimal import Decimal
import yaml
from simkit.core.pipeline import execute_pipeline
from simkit.evaluation.package_load import ProvisionalPackageLoader
ROOT=Path.cwd(); E=ROOT/'work/orchestration/aries-transfer-experiment/evidence'; R=Path('/tmp/aries-independent-review'); R.mkdir(exist_ok=True)
baseline=json.loads((E/'baseline.json').read_text())['files']
changed=[p for p,h in baseline.items() if not (ROOT/p).exists() or hashlib.sha256((ROOT/p).read_bytes()).hexdigest()!=h]
assert not changed,changed
pkg=ROOT/'exploration/aries_transfer/fuel_reuse/fuel_tea'
mod,fp=ProvisionalPackageLoader(package_dir=pkg,package_name='fuel_tea',link_root=R/'fuel-link').load()
records=[]
for name,power,supported in [('new_load',3000.,True),('unsupported',2436.,False)]:
 d=R/name;d.mkdir(exist_ok=True); cfg=yaml.safe_load((pkg/'pipelines/pipeline.yaml').read_text())
 for key,binding in cfg['modules']['entry_fusion']['inputs'].items():
  schema,relative=binding.split(' ',1);vals=json.loads((pkg/'pipelines'/relative).read_text())
  if key=='fuel_reuse_params': vals.update(aries_fuel_reuse__fuel_system__fusion_load_mw=power,aries_fuel_reuse__processing__assumed_conditions_supported=supported)
  inp=d/(key+'.json');inp.write_text(json.dumps(vals));cfg['modules']['entry_fusion']['inputs'][key]=schema+' '+str(inp)
 pipe=d/'pipeline.yaml';pipe.write_text(yaml.safe_dump(cfg));out=execute_pipeline(pipe,d/'out',registry=mod.create_fuel_tea_registry(),custom_schema_types=mod.CUSTOM_SCHEMA_TYPES).outputs
 expected=float(Decimal(str(power))*Decimal('1e6')/(Decimal('17.58')*Decimal('1.6021766339999998e-13'))*19)
 exhaust=out['aries_fuel_reuse__fuel_system__flows__exhaust_rate'];cap='aries_fuel_reuse__processing__capacity__'
 assert math.isclose(exhaust,expected,rel_tol=2e-15)
 assert out[cap+'margin']==2e22-exhaust
 assert out[cap+'capacity_ok']==(supported and expected<=2e22)
 assert out[cap+'evaluation_defined']==float(supported)
 status=out['constraint_report'].model_dump()['results'][0]['status'];assert status=='violated'
 records.append(dict(case=name,exhaust=exhaust,expected=expected,selected_rating=2e22,defined=out[cap+'evaluation_defined'],capacity_ok=out[cap+'capacity_ok'],constraint_status=status))
receipt=json.loads((ROOT/'work/active/WI-082_aries-existing-component-transfer-proof/evidence/reuse-hashes.json').read_text())
for p,h in receipt['source_hashes'].items():assert hashlib.sha256((ROOT/p).read_bytes()).hexdigest()==h
base=ROOT/'exploration/stellarator_e2e/generated/handwritten/mfe_viability/offered_capacity_screen_impl.py';new=pkg/'handwritten/mfe_viability/offered_capacity_screen_impl.py'
assert base.read_text()==new.read_text().replace('from fuel_tea.','from stellarator_tea.')
result=dict(protected_file_count=len(baseline),changed=changed,fuel_cases=records,capacity_completion_prefix_only=True,fuel_fingerprint=str(fp))
(E/'review-native.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
