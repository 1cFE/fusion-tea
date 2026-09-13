"""Independent exact fresh fixed point, source semantics and current metadata."""
import ast, importlib.util, json, subprocess, sys, tempfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3];HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT))
from scripts.study import manifest
p=ROOT/'work/active/WI-055_winding-pack-input-domain/evidence/regenerate.py'
s=importlib.util.spec_from_file_location('corrected_winding_generator',p);g=importlib.util.module_from_spec(s);s.loader.exec_module(g)
receipt=json.loads((p.parent/'corrected-package-hashes.json').read_text())
assert g.inventory(g.PACKAGE)==receipt
with tempfile.TemporaryDirectory(prefix='winding-audit-corrected-') as tmp:
 fresh=g.seed_and_generate(Path(tmp)/'fresh',models_path=ROOT/'exploration/stellarator_e2e/models')
 assert g.inventory(fresh)==receipt
# Compare package public contract, excluding only content hashes/identity.
path=g.PACKAGE/'contracts/package_contract.json';current=json.loads(path.read_text())
old=json.loads(subprocess.check_output(['git','show','747a8a35:'+str(path.relative_to(ROOT))],text=True,cwd=ROOT))
identity=current['executable_fingerprint']
for obj in (current,old):obj.pop('artifact_hashes');obj.pop('executable_fingerprint')
assert old==current
m=manifest.load(ROOT/'exploration/stellarator_e2e/studies/manifest.json')
manifest.assert_package_identity(m,g.PACKAGE);manifest.assert_pin_matches(m,manifest.indicator_input_fingerprint(g.PACKAGE))
contract=json.loads((g.PACKAGE/'contracts/model_contract.json').read_text());by={}
for row in contract['parameters']:by.setdefault(row['entry_type'],[]).append(row['qualified_name'])
census={'derived_against_semantic_fingerprint':contract['semantic_fingerprint'],'entry_points':len(contract['parameters']),'by_entry_type':{k:sorted(v) for k,v in by.items()}}
assert census==json.loads((ROOT/'tests/models/data/mfe_census.json').read_text())
# Verify the complete correction's generated executable equivalence independently.
def executable(text):
 tree=ast.parse(text)
 for node in ast.walk(tree):
  if hasattr(node,'body') and isinstance(node.body,list):node.body=[v for v in node.body if not (isinstance(v,ast.Expr) and isinstance(v.value,ast.Constant) and isinstance(v.value.value,str))]
 return ast.dump(tree,include_attributes=False)
checked=[]
for name in json.loads((HERE/'generation-delta.json').read_text()):
 if name.endswith('.py'):
  path=g.PACKAGE/name
  old=subprocess.check_output(['git','show','747a8a35:'+str(path.relative_to(ROOT))],text=True,cwd=ROOT)
  assert executable(old)==executable(path.read_text()),name
  checked.append(name)
rows={'verdict':'PASS','receipt_files':len(receipt),'fresh_exact':True,'executable_fingerprint':identity,'manifest_identity':True,'census_inputs':len(contract['parameters']),'unchanged_python_AST':checked}
(HERE/'correction.json').write_text(json.dumps(rows,indent=2)+'\n');print(json.dumps(rows,indent=2))
