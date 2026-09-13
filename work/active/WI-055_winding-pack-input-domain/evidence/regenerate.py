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
 from sysml_codegen.cli import GenerationConfig,run_codegen
 entering=json.loads((HERE/'manual-seeds.json').read_text())
 before=inventory(PACKAGE)
 for n,h in entering.items():
  if n!=MODIFIED:assert before['handwritten/'+n]==h,n
 expected={'handwritten/'+n:before['handwritten/'+n] for n in SEEDS}
 assert len(expected)==12
 for smart in (False,True):
  old=inventory(PACKAGE)
  assert run_codegen(GenerationConfig(models_path=ROOT/'exploration/stellarator_e2e/models',output_path=PACKAGE,package_name='stellarator_tea',overwrite=True,preserve_handwritten=True,smart_regen=smart))
  new=inventory(PACKAGE)
  assert all(new[n]==h for n,h in expected.items())
  if smart:assert old==new,'Repeated generation drift'
 (HERE/'candidate-package-hashes.json').write_text(json.dumps(new,indent=2)+'\n')
 (HERE/'candidate-seeds.json').write_text(json.dumps(expected,indent=2)+'\n')
 old=json.loads((HERE/'entering-package-hashes.json').read_text())
 (HERE/'package-changes.json').write_text(json.dumps({n:{'before':old.get(n),'after':new.get(n)} for n in sorted(set(old)|set(new)) if old.get(n)!=new.get(n)},indent=2)+'\n')
 print('PASS twelve seeds preserved; nine inherited seeds unchanged; generation byte-stable')
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
