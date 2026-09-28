"""Independent WI084 mixed perturbation, repaired refusal and edge checks."""
import hashlib,json,math
from pathlib import Path
from decimal import Decimal
import yaml
from simkit.core.pipeline import execute_pipeline
from simkit.evaluation.package_load import ProvisionalPackageLoader
ROOT=Path.cwd();E=ROOT/'work/orchestration/aries-transfer-experiment/evidence';R=Path('/tmp/aries-constituent-review');R.mkdir(exist_ok=True)
pkg=ROOT/'exploration/aries_transfer/constituent_inventory/inventory_tea';ev=ROOT/'work/active/WI-084_aries-sector-constituent-inventory/evidence';receipt=json.loads((ev/'results.json').read_text());hashes=json.loads((ev/'build-hashes.json').read_text())
for p,h in hashes['source_hashes'].items():assert hashlib.sha256((ROOT/p).read_bytes()).hexdigest()==h
for p,h in hashes['completion_hashes'].items():assert hashlib.sha256((pkg/'handwritten/sector_constituent_inventory'/p).read_bytes()).hexdigest()==h
mod,fp=ProvisionalPackageLoader(package_dir=pkg,package_name='inventory_tea',link_root=R/'links').load();assert str(fp)==receipt['fingerprint']
P='aries_constituent_inventory__';base=json.loads((pkg/'inputs/constituent_inventory_params.json').read_text());cfg=yaml.safe_load((pkg/'pipelines/pipeline.yaml').read_text());edges=0
for i,r in enumerate(('full','behind_divertor','tapered'),1):
 for j,m in enumerate(('lipb','sic_insert','ferritic_steel'),1):
  ins=cfg['modules'][P+r+'__'+m+'__inventory']['inputs'];assert P+r+'__layer__volume' in ins['region_volume_in'];edges+=1
  ins=cfg['modules'][P+r+'__recipe']['inputs'];assert P+r+'__'+m+'__inventory__known_mass' in ins[f'mass_{j}_in'];assert P+r+'__'+m+'__inventory__source_price_subtotal' in ins[f'price_{j}_in'];edges+=2
 ins=cfg['modules'][P+'reference_blanket_subset__totals']['inputs'];assert P+r+'__recipe__known_mass' in ins[f'mass_{i}_in'];assert P+r+'__coverage' in ins[f'coverage_{i}_in'];edges+=2
rows=[]
for name,changes,error in [('mixed',{P+'tapered__midpoint_area_basis':3.,P+'full__sic_insert__component_rate':151.},None),('invalid_partition',{P+'full__coverage':.7},'sector coverages'),('zero_invalid_recipe',{**{P+r+'__midpoint_area_basis':0. for r in ('full','behind_divertor','tapered')},P+'full__helium_fraction':.09},'recipe fractions')]:
 d=R/name;d.mkdir(exist_ok=True);vals={**base,**changes};inp=d/'inputs.json';inp.write_text(json.dumps(vals));cfg['modules']['entry_fusion']['inputs']['constituent_inventory_params']='ConstituentInventoryParams '+str(inp);pipe=d/'pipeline.yaml';pipe.write_text(yaml.safe_dump(cfg))
 try:out=execute_pipeline(pipe,d/'outputs',registry=mod.create_inventory_tea_registry(),custom_schema_types=mod.CUSTOM_SCHEMA_TYPES).outputs
 except Exception as exc:
  assert error and error in str(exc);rows.append(dict(case=name,error=str(exc)));continue
 assert error is None
 D=Decimal;volume=mass=price=helium=D(0)
 # Source numbers hardcoded independently of generated bindings and receipt oracle.
 for area,cov,th,fracs,rates in [('1','.654','.543',('.79','.07','.06'),('17.1','151','103')),('1','.106','.35',('.75','.09','.08'),('17.1','101','103')),('3','.24','.25',('.76','.08','.08'),('17.1','101','103'))]:
  v=D(area)*D(cov)*D(th);volume+=v;helium+=v*D('.08')
  for f,density,rate in zip(fracs,('8897','3200','7800'),rates):kg=v*D(f)*D(density);mass+=kg;price+=kg*D(rate)
 expected=dict(volume=float(volume),known_mass=float(mass),source_price_subtotal=float(price),unquantified_volume=float(helium));actual={k:out[P+'reference_blanket_subset__totals__'+k] for k in expected}
 for k in expected:assert math.isclose(actual[k],expected[k],rel_tol=3e-15,abs_tol=1e-12),(k,actual,expected)
 rows.append(dict(case=name,actual=actual,expected=expected))
baseline=json.loads((E/'baseline.json').read_text())['files'];changed=[p for p,h in baseline.items() if hashlib.sha256((ROOT/p).read_bytes()).hexdigest()!=h];assert not changed
result=dict(fingerprint=str(fp),native_edges_checked=edges,cases=rows,protected_count=len(baseline),changed=changed);(E/'review-constituent.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
