"""Compare the fixed fresh helper with exact stock CLI options in scratch."""
import hashlib,json,shutil,subprocess,tempfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[5];HERE=Path(__file__).resolve().parent;PACKAGE=ROOT/'exploration/stellarator_e2e/generated'
def inventory(path):return {str(p.relative_to(path)):hashlib.sha256(p.read_bytes()).hexdigest() for p in path.rglob('*') if p.is_file() and '__pycache__' not in p.parts and p.suffix!='.pyc'}
with tempfile.TemporaryDirectory(prefix='wi056-stock-') as tmp:
 dest=Path(tmp)/'package';shutil.copytree(PACKAGE,dest,ignore=shutil.ignore_patterns('__pycache__','*.pyc'))
 before=inventory(dest);a=json.loads((dest/'contracts/package_contract.json').read_text())
 cmd=[str(ROOT/'.codex-test/run'),'sysml-codegen','generate','--models',str(ROOT/'exploration/stellarator_e2e/models'),'--output',str(dest),'--package-name','stellarator_tea','--overwrite','--smart-regen','--preserve-handwritten']
 r=subprocess.run(cmd,cwd=ROOT,text=True,capture_output=True);(HERE/'stock-corrected.log').write_text(r.stdout+r.stderr);assert r.returncode==0
 after=inventory(dest);b=json.loads((dest/'contracts/package_contract.json').read_text())
 (HERE/'stock-corrected-contract.json').write_text(json.dumps(b,indent=2)+'\n')
 delta={k:{'before':a.get(k),'after':b.get(k)} for k in a.keys()|b.keys() if a.get(k)!=b.get(k)}
 out={'command':cmd,'moved':{k:{'before':before.get(k),'after':after.get(k)} for k in before.keys()|after.keys() if before.get(k)!=after.get(k)},'contract_delta':delta}
 (HERE/'stock-corrected-delta.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
