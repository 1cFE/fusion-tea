"""Corrected current MFE generator: exact typed seeds and stock smart regeneration."""
import hashlib,json,re,shutil,sys,tempfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[4];HERE=Path(__file__).resolve().parent
PACKAGE=ROOT/'exploration/stellarator_e2e/generated'
sys.path.insert(0,str(HERE))
from implement import inventory

def seed_and_generate(path,source=PACKAGE,*,generator=None,**kwargs):
 from sysml_codegen.cli import GenerationConfig,run_codegen
 path,source=Path(path),Path(source)
 if path.is_symlink() or path.exists() and (not path.is_dir() or any(path.iterdir())):raise FileExistsError(f'Nonfresh destination: {path}')
 expected=json.loads((HERE/'corrected-candidate-seeds.json').read_text())
 found={str(p.relative_to(source)) for p in (source/'handwritten').rglob('*.py') if p.name=='financial_factors.py' or re.search(r'^AUTO_IMPLEMENTED = False$',p.read_text(),re.M)}
 if found!=set(expected):raise ValueError('Unexpected normative seed inventory')
 path.mkdir(exist_ok=True)
 for name,digest in expected.items():
  original=source/name
  if original.is_symlink() or hashlib.sha256(original.read_bytes()).hexdigest()!=digest:raise ValueError('Missing, symlink or mismatched seed: '+name)
  target=path/name;target.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(original,target)
 assert (generator or run_codegen)(GenerationConfig(output_path=path,package_name='stellarator_tea',overwrite=True,preserve_handwritten=True,smart_regen=True,**kwargs))
 actual=inventory(path)
 assert all(actual[name]==h for name,h in expected.items())
 return path

def generate():
 with tempfile.TemporaryDirectory(prefix='wi056-fresh-') as tmp:
  fresh=seed_and_generate(Path(tmp)/'fresh',models_path=ROOT/'exploration/stellarator_e2e/models')
  before,expected=inventory(PACKAGE),inventory(fresh)
  assert set(before)==set(expected),'Unexpected package paths'
  changes={n:{'before':before[n],'after':expected[n]} for n in before if before[n]!=expected[n]}
  for name in changes:shutil.copyfile(fresh/name,PACKAGE/name)
  assert inventory(PACKAGE)==expected
  again=seed_and_generate(Path(tmp)/'again',models_path=ROOT/'exploration/stellarator_e2e/models')
  assert inventory(again)==expected,'Fresh generation is not exact'
  receipt=HERE/'corrected-package-hashes.json'
  if receipt.exists():assert json.loads(receipt.read_text())==expected,'Frozen package receipt drift'
  else:receipt.write_text(json.dumps(expected,indent=2)+'\n')
  (HERE/'coherence/generation-changes.json').write_text(json.dumps(changes,indent=2)+'\n')
 print('PASS exact fresh equality for all package files, thirteen normative seeds')
if __name__=='__main__':generate()
