"""Independent WI083 measure/species/native beta check and reuse identity."""
import ast,hashlib,json,math
from pathlib import Path
from decimal import Decimal,localcontext
import yaml
from simkit.core.pipeline import execute_pipeline
from simkit.evaluation.package_load import ProvisionalPackageLoader
ROOT=Path.cwd();E=ROOT/'work/orchestration/aries-transfer-experiment/evidence';R=Path('/tmp/aries-plasma-review');R.mkdir(exist_ok=True)
pkg=ROOT/'exploration/aries_transfer/plasma_integration/generated';receipt=json.loads((ROOT/'work/active/WI-083_aries-supplied-profile-plasma-integration/evidence/verification.json').read_text())
for p,h in receipt['hashes'].items():
 if p!='reactivity_function_ast_sha256':assert hashlib.sha256((ROOT/p).read_bytes()).hexdigest()==h,p
old=ROOT/'exploration/stellarator_e2e/generated/handwritten/mfe_plasma_scaling/dt_fusion_power_impl.py';new=pkg/'handwritten/supplied_profile_plasma/reused_reactivity.py'
node=lambda p:next(n for n in ast.parse(p.read_text()).body if isinstance(n,ast.FunctionDef) and n.name=='_sigv_dt')
assert ast.dump(node(old))==ast.dump(node(new))
density=ROOT/'exploration/aries_transfer/density_profile/radial_density_profile_impl.py';copy=pkg/'handwritten/radial_density_profile/radial_density_profile_impl.py'
assert density.read_text()==copy.read_text().replace('from aries_plasma_tea.','from aries_density_tea.')
mod,fp=ProvisionalPackageLoader(package_dir=pkg,package_name='aries_plasma_tea',link_root=R/'links').load();assert str(fp)==receipt['fingerprint']
pre='aries_cs_plasma_integration__plasma__';cfg=yaml.safe_load((pkg/'pipelines/pipeline.yaml').read_text())
for key,binding in cfg['modules']['entry_fusion']['inputs'].items():
 schema,relative=binding.split(' ',1);vals=json.loads((pkg/'pipelines'/relative).read_text())
 if key=='plasma_integration_params':vals.update({pre+'volume_exponent':3.0,pre+'helium_fraction':.1,pre+'field':8.0})
 inp=R/(key+'.json');inp.write_text(json.dumps(vals));cfg['modules']['entry_fusion']['inputs'][key]=schema+' '+str(inp)
pipe=R/'pipeline.yaml';pipe.write_text(yaml.safe_dump(cfg));out=execute_pipeline(pipe,R/'outputs',registry=mod.create_aries_plasma_tea_registry(),custom_schema_types=mod.CUSTOM_SCHEMA_TYPES).outputs
get=lambda n:getattr(out[pre+'integration__'+n],'root',out[pre+'integration__'+n])
with localcontext() as ctx:
 ctx.prec=60;c={0:Decimal('.694'),2:Decimal('.306'),12:Decimal('-.594'),14:Decimal('-.306')};m=Decimal(3)
 expected_n=float(Decimal('5e20')*sum(m*v/(k+m) for k,v in c.items()))
 expected_p=float(Decimal('1.9')*Decimal('5e20')*Decimal('1.602176634e-16')*sum(m*v*(Decimal('11.83')/(k+m)-Decimal('11.63')/(k+m+2)) for k,v in c.items()))
assert math.isclose(get('density_mean'),expected_n,rel_tol=2e-9)
assert math.isclose(get('thermal_pressure'),expected_p,rel_tol=2e-9)
beta=getattr(out[pre+'beta_calculation__beta'],'root',out[pre+'beta_calculation__beta']);assert math.isclose(beta,2*1.25663706212e-6*expected_p/64,rel_tol=2e-9)
reference=next(c for c in receipt['checks'] if c['test']=='alternative_measure')['outputs']['integration__fusion_power_MW'];expected_power=reference*(.8/.933)**2
assert math.isclose(get('fusion_power_MW'),expected_power,rel_tol=2e-12)
assert get('field_for_beta')==8.
baseline=json.loads((E/'baseline.json').read_text())['files'];changed=[p for p,h in baseline.items() if hashlib.sha256((ROOT/p).read_bytes()).hexdigest()!=h];assert not changed
result=dict(fingerprint=str(fp),density=get('density_mean'),expected_density=expected_n,pressure=get('thermal_pressure'),expected_pressure=expected_p,beta=beta,fusion_MW=get('fusion_power_MW'),expected_fusion_MW=expected_power,intervals=get('quadrature_intervals'),relative_change=get('quadrature_relative_change'),kernel_ast_equal=True,density_prefix_only=True,protected_count=len(baseline),changed=changed)
(E/'review-plasma.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
