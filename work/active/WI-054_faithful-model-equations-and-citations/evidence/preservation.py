"""Bounded WI-054 capture and comparison; model/package roots only."""
import ast
import hashlib
import json
import re
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[4]
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
from tests.model_families import FAMILIES, canonical_path
PACKAGES = {'mfe':ROOT/'exploration/stellarator_e2e/generated','ife':ROOT/'exploration/ife_e2e/generated'}

def sha(data): return hashlib.sha256(data).hexdigest()
def lexical(text):
    # Lex strings before comments, then compare all remaining tokens including whitespace inside strings.
    tokens=re.findall(r"'(?:[^'\\]|\\.)*'|\"(?:[^\"\\]|\\.)*\"|/\*.*?\*/|//[^\n]*|[A-Za-z_][A-Za-z_0-9]*|\d+(?:\.\d*)?(?:[eE][+-]?\d+)?|[^\s]",text,re.S)
    return [t for t in tokens if not t.startswith(('/*','//')) and t!='doc']

def python_ast(text):
    node=ast.parse(text)
    for n in ast.walk(node):
        if isinstance(n,(ast.Module,ast.ClassDef,ast.FunctionDef,ast.AsyncFunctionDef)) and n.body and isinstance(n.body[0],ast.Expr) and isinstance(n.body[0].value,ast.Constant) and isinstance(n.body[0].value.value,str):n.body.pop(0)
    return ast.dump(node,include_attributes=False)

def inventory(package):
    return {str(p.relative_to(package)):sha(p.read_bytes()) for p in sorted(package.rglob('*')) if p.is_file() and '__pycache__' not in p.parts and p.suffix!='.pyc'}

def capture():
    models={str(canonical_path(n).relative_to(ROOT)):canonical_path(n).read_text() for f in FAMILIES.values() for n in f.owned}
    data={'models':{n:{'sha256':sha(t.encode()),'tokens':lexical(t)} for n,t in models.items()},'packages':{}}
    for family,package in PACKAGES.items():
        data['packages'][family]={'hashes':inventory(package),'python_asts':{str(p.relative_to(package)):python_ast(p.read_text()) for p in package.rglob('*.py')},'contract':json.loads((package/'contracts/model_contract.json').read_text())}
    (HERE/'entering.json').write_text(json.dumps(data,indent=2)+'\n')
    print('Captured canonical family sources and both current package trees')

def compare():
    before=json.loads((HERE/'entering.json').read_text());result={'sysml_tokens_equal':True,'twins_equal':True,'packages':{}}
    for name,row in before['models'].items():assert lexical((ROOT/name).read_text())==row['tokens'],name
    for family in FAMILIES.values():
        for name in family.owned:assert canonical_path(name).read_bytes()==(family.twin/name).read_bytes(),name
    for family,package in PACKAGES.items():
        old=before['packages'][family];new=inventory(package)
        asts={str(p.relative_to(package)):python_ast(p.read_text()) for p in package.rglob('*.py')}
        differences=[n for n in set(old['python_asts'])|set(asts) if old['python_asts'].get(n)!=asts.get(n)]
        contract=json.loads((package/'contracts/model_contract.json').read_text())
        result['packages'][family]={'ast_differences':differences,'contract_equal':contract==old['contract'],'changes':{n:{'before':old['hashes'].get(n),'after':new.get(n)} for n in sorted(set(old['hashes'])|set(new)) if old['hashes'].get(n)!=new.get(n)}}
        (HERE/(family+'-candidate-package-hashes.json')).write_text(json.dumps(new,indent=2)+'\n')
    (HERE/'preservation.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
if __name__=='__main__':{'capture':capture,'compare':compare}[sys.argv[1]]()
