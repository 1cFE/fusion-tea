"""Independent fresh generation and twelve-seed mutation rejection."""
import ast, difflib, hashlib, importlib.util, json, shutil, tempfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3];HERE=Path(__file__).resolve().parent
p=ROOT/'work/active/WI-055_winding-pack-input-domain/evidence/regenerate.py'
s=importlib.util.spec_from_file_location('current_winding_generator',p);g=importlib.util.module_from_spec(s);s.loader.exec_module(g)
receipt=json.loads((p.parent/'candidate-package-hashes.json').read_text());seeds=json.loads((p.parent/'candidate-seeds.json').read_text())
rows={}
with tempfile.TemporaryDirectory(prefix='winding-audit-') as tmp:
 tmp=Path(tmp)
 fresh=g.seed_and_generate(tmp/'fresh',models_path=ROOT/'exploration/stellarator_e2e/models')
 actual=g.inventory(fresh)
 delta={k:{'expected':receipt.get(k),'actual':actual.get(k)} for k in set(receipt)|set(actual) if receipt.get(k)!=actual.get(k)}
 (HERE/'generation-delta.json').write_text(json.dumps(delta,indent=2)+'\n')
 comparisons={}
 for name in delta:
  old=(g.PACKAGE/name).read_text();new=(fresh/name).read_text()
  comparisons[name]=''.join(difflib.unified_diff(old.splitlines(True),new.splitlines(True)))
 (HERE/'generation-diffs.json').write_text(json.dumps(comparisons,indent=2)+'\n')
 def executable(text):
  tree=ast.parse(text)
  for node in ast.walk(tree):
   if hasattr(node,'body') and isinstance(node.body,list):node.body=[v for v in node.body if not (isinstance(v,ast.Expr) and isinstance(v.value,ast.Constant) and isinstance(v.value.value,str))]
  return ast.dump(tree,include_attributes=False)
 for name in delta:
  if name.endswith('.py'):assert executable((g.PACKAGE/name).read_text())==executable((fresh/name).read_text()),name
  else:assert name=='contracts/package_contract.json',name
 rows['fresh']={'byte_differences':len(delta),'result':'all Python executable ASTs unchanged; twelve seeds exact; contract delta retained for review'}
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
(HERE/'generation.json').write_text(json.dumps(rows,indent=2)+'\n');print('PASS executable AST equivalence, twelve seeds and three mutation refusals; exact receipt mismatch remains R10-A1')
