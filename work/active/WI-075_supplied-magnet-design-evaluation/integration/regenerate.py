"""Native fresh generation for the reviewed WI-075..078 design-choice migration."""
import hashlib
import importlib.util
import json
import shutil
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT))
HERE = Path(__file__).resolve().parent
PACKAGE = ROOT/'exploration/stellarator_e2e/generated'
PRIOR = ROOT/'work/active/WI-073_matched-steam-cycle-for-current-comparison/evidence/candidate-seeds.json'
RECIPE = ROOT/'work/completed/20260914_WI-040_winding-pack-mass-cost/evidence/regenerate.py'
REPLACEMENTS = {
 'handwritten/mfe_magnet_field/winding_operating_state_impl.py':'WI-075_supplied-magnet-design-evaluation',
 'handwritten/mfe_winding_pack_cost/winding_pack_procurement_cost_impl.py':'WI-075_supplied-magnet-design-evaluation',
 'handwritten/mfe_facilities/facility_layout_impl.py':'WI-076_supplied-facility-design-evaluation',
 'handwritten/mfe_fuel_cycle/fuel_processing_cost_impl.py':'WI-077_supplied-fuel-processing-capacity-evaluation',
 'handwritten/mfe_cooling_equipment/cooling_equipment_impl.py':'WI-078_supplied-cooling-design-point-evaluation',
 'handwritten/mfe_primary_loop/primary_coolant_loop_impl.py':'WI-078_supplied-cooling-design-point-evaluation',
}

def sha(path):
 return hashlib.sha256(path.read_bytes()).hexdigest()

def recipe():
 spec=importlib.util.spec_from_file_location('mr7_native_recipe',RECIPE)
 module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
 module.SEEDS=HERE/'candidate-seeds.json'
 return module

def seed_and_generate(path,source=PACKAGE,**kwargs):
 try:
  return recipe().seed_and_generate(path,source,**kwargs)
 except AssertionError:
  expected=json.loads((HERE/"candidate-seeds.json").read_text())
  actual=recipe().inventory(path)
  changed=[name for name,digest in expected.items() if actual.get(name)!=digest]
  diagnostic=Path(tempfile.mkdtemp(prefix="mr7-seed-drift-"))
  shutil.copytree(path,diagnostic/"generated")
  shutil.copytree(source,diagnostic/"seeds")
  raise AssertionError(("native generation changed normative seeds",changed,str(diagnostic)))

def generate():
 from tests.model_families import MFE,canonical_path
 for logical in MFE.owned:
  assert canonical_path(logical).read_bytes()==(MFE.twin/logical).read_bytes(),logical
 before=recipe().inventory(PACKAGE)
 entering=json.loads(PRIOR.read_text())
 with tempfile.TemporaryDirectory(prefix='mr7-generation-') as scratch:
  source=Path(scratch)/'seeds';source.mkdir()
  for name,digest in entering.items():
   if name in REPLACEMENTS:continue
   assert before[name]==digest,('unreviewed entering seed drift',name)
   target=source/name;target.parent.mkdir(parents=True,exist_ok=True)
   shutil.copyfile(PACKAGE/name,target)
  for name,item in REPLACEMENTS.items():
   target=source/name;target.parent.mkdir(parents=True,exist_ok=True)
   shutil.copyfile(ROOT/'work/active'/item/'seeds'/Path(name).name,target)
  seeds=recipe().inventory(source)
  (HERE/'candidate-seeds.json').write_text(json.dumps(seeds,indent=2)+'\n')
  fresh=seed_and_generate(Path(scratch)/'fresh',source,models_path=MFE.twin)
  expected=recipe().inventory(fresh)
  # Only the live generated tree is replaced. Frozen packages never enter this path.
  for name in sorted(set(before)-set(expected)):
   (PACKAGE/name).unlink()
  for name,digest in expected.items():
   if before.get(name)!=digest:
    target=PACKAGE/name;target.parent.mkdir(parents=True,exist_ok=True)
    shutil.copyfile(fresh/name,target)
  assert recipe().inventory(PACKAGE)==expected
  again=seed_and_generate(Path(scratch)/'again',PACKAGE,models_path=MFE.twin)
  assert recipe().inventory(again)==expected,'fresh regeneration drift'
 (HERE/'model-hashes.json').write_text(json.dumps({logical:sha(canonical_path(logical)) for logical in MFE.owned},indent=2)+'\n')
 (HERE/'package-hashes.json').write_text(json.dumps(expected,indent=2)+'\n')
 (HERE/'generation-changes.json').write_text(json.dumps({n:{'before':before.get(n),'after':expected.get(n)} for n in sorted(set(before)|set(expected)) if before.get(n)!=expected.get(n)},indent=2)+'\n')
 print('PASS fresh native generation and exact second regeneration',len(seeds),'manual bodies')

if __name__=='__main__':generate()
