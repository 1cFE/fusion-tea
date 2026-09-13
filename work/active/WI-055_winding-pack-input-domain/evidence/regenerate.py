"""Current MFE completion with twelve explicitly inventoried normative seeds."""
import hashlib,json,re,shutil,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[4];HERE=Path(__file__).resolve().parent
PACKAGE=ROOT/'exploration/stellarator_e2e/generated'
sys.path.insert(0,str(HERE))
from capture import inventory
SEEDS=tuple(json.loads((HERE/'manual-seeds.json').read_text()))+('mfe_magnet_field/winding_pack_sizing_impl.py','mfe_magnet_field/winding_pack_stress_impl.py')
MODIFIED='mfe_plasma_sustainment/plasma_sustainment_impl.py'
def generate():
 """Regenerate auto bodies from current model; preserve only normative seeds.

 The initial in-place procedure at 747a8a35 preserved stale AUTO_IMPLEMENTED
 docstrings. Fresh generation is the authoritative corrected producer.
 """
 import ast,tempfile
 def executable(text):
  tree=ast.parse(text)
  for node in ast.walk(tree):
   if hasattr(node,'body') and isinstance(node.body,list):
    node.body=[v for v in node.body if not(isinstance(v,ast.Expr) and isinstance(v.value,ast.Constant) and isinstance(v.value.value,str))]
  return ast.dump(tree,include_attributes=False)
 before=inventory(PACKAGE)
 with tempfile.TemporaryDirectory(prefix='wi055-corrected-') as tmp:
  fresh=seed_and_generate(Path(tmp)/'fresh',models_path=ROOT/'exploration/stellarator_e2e/models')
  expected=inventory(fresh)
  assert set(before)==set(expected),'Unexpected package path changes'
  changes={n:{'before':before[n],'after':expected[n]} for n in before if before[n]!=expected[n]}
  for name in changes:
   if name=='contracts/package_contract.json':continue
   old,new=PACKAGE/name,fresh/name
   assert name.startswith('handwritten/') and 'AUTO_IMPLEMENTED = True' in old.read_text(),name
   assert executable(old.read_text())==executable(new.read_text()),name
  for name in changes:shutil.copyfile(fresh/name,PACKAGE/name)
  assert inventory(PACKAGE)==expected
  again=seed_and_generate(Path(tmp)/'again',models_path=ROOT/'exploration/stellarator_e2e/models')
  assert inventory(again)==expected,'Fresh generation not a fixed point'
  seeds=json.loads((HERE/'candidate-seeds.json').read_text())
  assert all(expected[n]==h for n,h in seeds.items())
  receipt=HERE/'corrected-package-hashes.json'
  if receipt.exists():assert json.loads(receipt.read_text())==expected,'Corrected receipt drift'
  else:receipt.write_text(json.dumps(expected,indent=2)+'\n')
  record=HERE/'coherence-repair.json'
  if not record.exists():record.write_text(json.dumps({'changes':changes,'preserved_seeds':seeds,'fresh_generation_exact':True,'all_changed_body_ASTs_equal':True},indent=2)+'\n')
 print('PASS fresh generation coherent; twelve seeds preserved; changed auto-body ASTs unchanged')
def seed_and_generate(path,source=PACKAGE,*,generator=None,**kwargs):
 from sysml_codegen.cli import GenerationConfig,run_codegen
 path,source=Path(path),Path(source)
 if path.is_symlink() or path.exists() and (not path.is_dir() or any(path.iterdir())):raise FileExistsError(f'Nonfresh destination: {path}')
 expected=json.loads((HERE/'candidate-seeds.json').read_text())
 found={str(p.relative_to(source)) for p in (source/'handwritten').rglob('*.py') if p.name=='financial_factors.py' or re.search(r'^AUTO_IMPLEMENTED = False$',p.read_text(),re.M)}
 if found!=set(expected):raise ValueError('Unexpected normative seed inventory')
 path.mkdir(exist_ok=True)
 for name,digest in expected.items():
  original=source/name
  if original.is_symlink() or hashlib.sha256(original.read_bytes()).hexdigest()!=digest:raise ValueError('Missing, symlink or mismatched seed: '+name)
  target=path/name;target.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(original,target)
 assert (generator or run_codegen)(GenerationConfig(output_path=path,package_name='stellarator_tea',overwrite=True,preserve_handwritten=True,**kwargs))
 actual=inventory(path)
 assert all(actual[name]==h for name,h in expected.items())
 return path
if __name__=='__main__':generate()
