"""Native fresh generation for the reviewed WI-079..080 supplied-equipment migration."""
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
PRIOR = ROOT/'work/active/WI-075_supplied-magnet-design-evaluation/integration/candidate-seeds.json'
RECIPE = ROOT/'work/completed/20260914_WI-040_winding-pack-mass-cost/evidence/regenerate.py'
REPLACEMENTS = {
 'handwritten/mfe_viability/cold_load_watts_impl.py':'WI-080_supplied-thermal-equipment-capability-and-demand-checks',
 'handwritten/mfe_viability/pump_pressure_rise_impl.py':'WI-080_supplied-thermal-equipment-capability-and-demand-checks',
 'handwritten/mfe_viability/salt_machine_electric_impl.py':'WI-080_supplied-thermal-equipment-capability-and-demand-checks',
 'handwritten/mfe_account_costs/supplied_cost_class_impl.py':'WI-079_supplied-equipment-design-bases-for-residual-costs',
 'handwritten/mfe_viability/helium_offered_conditions_impl.py':'WI-080_supplied-thermal-equipment-capability-and-demand-checks',
 'handwritten/mfe_viability/salt_offered_conditions_impl.py':'WI-080_supplied-thermal-equipment-capability-and-demand-checks',
 'handwritten/mfe_viability/steam_offered_conditions_impl.py':'WI-080_supplied-thermal-equipment-capability-and-demand-checks',
 'handwritten/mfe_viability/water_offered_conditions_impl.py':'WI-080_supplied-thermal-equipment-capability-and-demand-checks',
 'handwritten/mfe_viability/cryogenic_offered_conditions_impl.py':'WI-080_supplied-thermal-equipment-capability-and-demand-checks',
 'handwritten/mfe_viability/offered_capacity_screen_impl.py':'WI-080_supplied-thermal-equipment-capability-and-demand-checks',
 'handwritten/mfe_account_costs/supplied_purchase_cost_impl.py':'WI-079_supplied-equipment-design-bases-for-residual-costs',
 'handwritten/mfe_account_costs/supplied_auxiliary_cooling_cost_impl.py':'WI-079_supplied-equipment-design-bases-for-residual-costs',
 'handwritten/mfe_cooling_equipment/cooling_equipment_impl.py':'WI-080_supplied-thermal-equipment-capability-and-demand-checks',
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
