"""Independent non-grid polynomial check and rejected upstream input replay."""
import hashlib,json,math
from pathlib import Path
from decimal import Decimal,localcontext
import yaml
from simkit.core.pipeline import execute_pipeline
from simkit.evaluation.package_load import ProvisionalPackageLoader
ROOT=Path.cwd();E=ROOT/'work/orchestration/aries-transfer-experiment/evidence';R=Path('/tmp/aries-density-review');R.mkdir(exist_ok=True)
pkg=ROOT/'exploration/aries_transfer/density_profile/generated'; receipt=json.loads((ROOT/'work/active/WI-081_aries-hollow-finite-edge-density-profile/evidence/verification.json').read_text())
for p,h in receipt['source_hashes'].items():assert hashlib.sha256((ROOT/p).read_bytes()).hexdigest()==h
assert (pkg/'handwritten/radial_density_profile/radial_density_profile_impl.py').read_bytes()==(ROOT/'exploration/aries_transfer/density_profile/radial_density_profile_impl.py').read_bytes()
mod,fp=ProvisionalPackageLoader(package_dir=pkg,package_name='aries_density_tea',link_root=R/'links').load();assert str(fp)==receipt['fingerprint']
pre='aries_cs_density_profile__plasma_profile__';rows=[]
for name,changes,bad in [('nongrid',{'rho':.37,'amplitude':3.25},False),('upstream_nan',{'edge_ratio':float('nan')},True)]:
 d=R/name;d.mkdir(exist_ok=True);cfg=yaml.safe_load((pkg/'pipelines/pipeline.yaml').read_text());vals=json.loads((pkg/'inputs/density_profile_params.json').read_text());vals.update({pre+k:v for k,v in changes.items()});inp=d/'inputs.json';inp.write_text(json.dumps(vals));cfg['modules']['entry_fusion']['inputs']['density_profile_params']='DensityProfileParams '+str(inp);pipe=d/'pipeline.yaml';pipe.write_text(yaml.safe_dump(cfg))
 try: out=execute_pipeline(pipe,d/'outputs',registry=mod.create_aries_density_tea_registry(),custom_schema_types=mod.CUSTOM_SCHEMA_TYPES).outputs
 except Exception as e:
  assert bad and 'density profile requires finite inputs' in str(e),str(e);rows.append(dict(case=name,refused=True,error=str(e)));continue
 assert not bad
 with localcontext() as ctx:
  ctx.prec=60;r=Decimal('.37');expected=float(Decimal('3.25')*(Decimal('.694')+Decimal('.306')*r**2-Decimal('.594')*r**12-Decimal('.306')*r**14))
 actual=out[pre+'profile__density'].root;assert math.isclose(actual,expected,rel_tol=2e-15);assert out[pre+'edge_density__edge_density'].root==3.25*.1
 rows.append(dict(case=name,actual=actual,expected=expected))
result=dict(fingerprint=str(fp),checks=rows,source_hashes=receipt['source_hashes']);(E/'review-density.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
