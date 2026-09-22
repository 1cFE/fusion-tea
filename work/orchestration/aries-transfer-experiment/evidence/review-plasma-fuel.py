"""Independent WI085 producer-volume perturbation through actual fuel/capacity graph."""
import ast,hashlib,json,math
from decimal import Decimal
from pathlib import Path
import yaml
from simkit.core.pipeline import execute_pipeline
from simkit.evaluation.package_load import ProvisionalPackageLoader
ROOT=Path.cwd();E=ROOT/'work/orchestration/aries-transfer-experiment/evidence';R=Path('/tmp/aries-plasma-fuel-review');R.mkdir(exist_ok=True)
pkg=ROOT/'exploration/aries_transfer/plasma_fuel/generated';receipt=json.loads((ROOT/'work/active/WI-085_aries-calculated-plasma-to-fuel-integration/evidence/verification.json').read_text())
for p,h in receipt['reuse']['sources'].items():assert hashlib.sha256((ROOT/p).read_bytes()).hexdigest()==h
for row in receipt['reuse']['completions']:
 source=ROOT/row['source'];assert hashlib.sha256(source.read_bytes()).hexdigest()==row['source_sha256']
 target=next(p for p in (pkg/'handwritten').rglob(source.name));assert hashlib.sha256(target.read_bytes()).hexdigest()==row['target_sha256']
 names={'supplied_profile_plasma_impl.py':'aries_plasma_tea','radial_density_profile_impl.py':'aries_density_tea','offered_capacity_screen_impl.py':'stellarator_tea'}
 assert source.read_text()==target.read_text().replace('from plasma_fuel_tea.','from '+names[source.name]+'.')
mod,fp=ProvisionalPackageLoader(package_dir=pkg,package_name='plasma_fuel_tea',link_root=R/'links').load();assert str(fp)==receipt['fingerprint']
p='aries_cs_plasma_integration__plasma__';f='aries_plasma_fuel__fuel_system__flows__';c='aries_plasma_fuel__processing__capacity__';cfg=yaml.safe_load((pkg/'pipelines/pipeline.yaml').read_text());assert cfg['modules']['aries_plasma_fuel__fuel_system__flows']['inputs']['p_fus_in']=='float '+p+'integration__fusion_power_MW'
effective={}
for key,binding in cfg['modules']['entry_fusion']['inputs'].items():
 schema,relative=binding.split(' ',1);vals=json.loads((pkg/'pipelines'/relative).read_text());assert not any('fusion_load' in k or k.endswith('__p_fus_in') for k in vals)
 if p+'volume' in vals:vals[p+'volume']=888.
 effective.update(vals);inp=R/(key+'.json');inp.write_text(json.dumps(vals));cfg['modules']['entry_fusion']['inputs'][key]=schema+' '+str(inp)
pipe=R/'pipeline.yaml';pipe.write_text(yaml.safe_dump(cfg));out=execute_pipeline(pipe,R/'outputs',registry=mod.create_plasma_fuel_tea_registry(),custom_schema_types=mod.CUSTOM_SCHEMA_TYPES).outputs
power=out[p+'integration__fusion_power_MW'];exhaust=out[f+'exhaust_rate'];expected=float(Decimal(str(power))*Decimal('1e6')/(Decimal('17.58')*Decimal('1.6021766339999998e-13'))*19)
assert math.isclose(power,2*receipt['cases'][0]['fusion_power_MW'],rel_tol=2e-14)
assert math.isclose(exhaust,expected,rel_tol=2e-15)
assert effective['aries_plasma_fuel__processing__selected_rating_atoms_s']==2e22
assert out[c+'margin']==2e22-exhaust and out[c+'capacity_ok'] is False
assert out['constraint_report'].model_dump()['results'][0]['status']=='violated'
baseline=json.loads((E/'baseline.json').read_text())['files'];changed=[p for p,h in baseline.items() if hashlib.sha256((ROOT/p).read_bytes()).hexdigest()!=h];assert not changed
result=dict(fingerprint=str(fp),supplied_volume=888.,calculated_fusion_MW=power,exhaust_atoms_s=exhaust,expected_exhaust=expected,fixed_rating_atoms_s=2e22,capacity_ok=False,protected_count=len(baseline),changed=changed);(E/'review-plasma-fuel.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
