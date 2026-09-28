"""Independent fresh generation and twelve-seed mutation rejection."""
import hashlib, importlib.util, json, shutil, tempfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3];HERE=Path(__file__).resolve().parent
p=ROOT/'work/active/WI-055_winding-pack-input-domain/evidence/regenerate.py'
s=importlib.util.spec_from_file_location('current_winding_generator',p);g=importlib.util.module_from_spec(s);s.loader.exec_module(g)
receipt=json.loads((p.parent/'candidate-package-hashes.json').read_text());seeds=json.loads((p.parent/'candidate-seeds.json').read_text())
rows={}
with tempfile.TemporaryDirectory(prefix='winding-audit-') as tmp:
 tmp=Path(tmp)
 fresh=g.seed_and_generate(tmp/'fresh',models_path=ROOT/'exploration/stellarator_e2e/models')
 assert g.inventory(fresh)==receipt
 rows['fresh']='exact full current receipt, twelve retained seeds'
 for case in ('missing','changed','extra'):
  source=tmp/case
  for name in seeds:
   q=source/name;q.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(g.PACKAGE/name,q)
  q=source/'handwritten/mfe_magnet_field/winding_pack_sizing_impl.py'
  if case=='missing':q.unlink()
  elif case=='changed':q.write_text(q.read_text()+'\n# mutation\n')
  else:(q.parent/'unexpected_impl.py').write_text('AUTO_IMPLEMENTED = False\n')
  calls=[]
  try:g.seed_and_generate(tmp/(case+'-target'),source,generator=lambda config:calls.append(config) or True,models_path=ROOT/'exploration/stellarator_e2e/models')
  except ValueError as error:rows[case]=str(error)
  else:raise AssertionError(case+' accepted')
  assert not calls
assert g.inventory(g.PACKAGE)==receipt
(HERE/'generation.json').write_text(json.dumps(rows,indent=2)+'\n');print('PASS exact fresh generation and three pre-generation seed mutation refusals')
