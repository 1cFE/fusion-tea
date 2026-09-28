import ast,collections,hashlib,importlib.util,json,re,subprocess,sys
from pathlib import Path
root=Path.cwd(); h=root/'work/active/WI-054_faithful-model-equations-and-citations/evidence'
sys.path.insert(0,str(root))
from tests.model_families import FAMILIES,canonical_path

def old(p):return subprocess.check_output(['git','show','1caee4f6:'+str(p.relative_to(root))])
def tokens(b):return [t for t in re.findall(r"'(?:[^'\\]|\\.)*'|\"(?:[^\"\\]|\\.)*\"|/\*.*?\*/|//[^\n]*|[^\s]",b.decode(),re.S) if not t.startswith(('/*','//'))]
def tree(b):
 n=ast.parse(b)
 for x in ast.walk(n):
  if isinstance(x,(ast.Module,ast.ClassDef,ast.FunctionDef,ast.AsyncFunctionDef)) and x.body and isinstance(x.body[0],ast.Expr) and isinstance(x.body[0].value,ast.Constant) and isinstance(x.body[0].value.value,str):x.body.pop(0)
 return ast.dump(n,include_attributes=False)
counts={}
for family in FAMILIES.values():
 for name in family.owned:
  p=canonical_path(name);assert tokens(old(p))==tokens(p.read_bytes()),p
  assert p.read_bytes()==(family.twin/name).read_bytes(),p
counts['canonical_tokens_and_twins']='pass'
for kind,pkg in [('mfe',root/'exploration/stellarator_e2e/generated'),('ife',root/'exploration/ife_e2e/generated')]:
 expected=json.loads((h/(kind+'-candidate-package-hashes.json')).read_text())
 paths=[p for p in pkg.rglob('*') if p.is_file() and '__pycache__' not in p.parts and p.suffix!='.pyc']
 actual={str(p.relative_to(pkg)):hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}
 assert expected==actual
 for p in paths:
  if p.suffix=='.py':assert tree(old(p))==tree(p.read_bytes()),p
  if 'handwritten' in p.parts or p.suffix=='.json' and 'inputs' in p.parts:assert old(p)==p.read_bytes(),p
 contract=pkg/'contracts/model_contract.json';assert json.loads(old(contract))==json.loads(contract.read_text())
 counts[kind]={'inventory_files':len(paths),'python_asts':'equal','contract':'equal','manual_and_inputs':'byte_equal'}
counts['census']=json.loads((root/'tests/models/data/mfe_census.json').read_text())
a=json.loads((h.parent.parent/'WI-053_magnet-and-cryogenic-input-domains/evidence/candidate-validation.json').read_text());b=json.loads((h/'validation.json').read_text())
for x,y in zip(a,b,strict=True):
 for key in ('issues','warnings'):
  norm=lambda r:collections.Counter(re.sub(r'(\.sysml):\d+',r'\1:<line>',s) for s in r[key])
  assert norm(x)==norm(y),(x['level'],key)
counts['validation_issue_identities']='equal after source line normalization'
print(json.dumps(counts,indent=2))
