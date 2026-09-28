"""Retain independent stock in-place contract delta on a disposable package copy."""
import hashlib,json,shutil,subprocess,tempfile
from pathlib import Path
R=Path.cwd();O=Path(__file__).resolve().parent;P=R/'exploration/stellarator_e2e/generated'
def hashes(p):return {str(f.relative_to(p)):hashlib.sha256(f.read_bytes()).hexdigest() for f in p.rglob('*') if f.is_file() and '__pycache__' not in f.parts and f.suffix!='.pyc'}
with tempfile.TemporaryDirectory(prefix='wi056-inplace-audit-') as t:
 q=Path(t)/'package';shutil.copytree(P,q,ignore=shutil.ignore_patterns('__pycache__','*.pyc'))
 before=hashes(q);old=json.loads((q/'contracts/package_contract.json').read_text())
 command=[str(R/'.codex-test/run'),'sysml-codegen','generate','--models',str(R/'exploration/stellarator_e2e/models'),'--output',str(q),'--package-name','stellarator_tea','--overwrite','--smart-regen','--preserve-handwritten']
 result=subprocess.run(command,text=True,capture_output=True);(O/'stock-original.log').write_text(result.stdout+result.stderr);assert result.returncode==0
 after=hashes(q);new=json.loads((q/'contracts/package_contract.json').read_text())
 (O/'stock-original-delta.json').write_text(json.dumps({'command':command,'changed_files':[f for f in before.keys()|after.keys() if before.get(f)!=after.get(f)],'contract_field_deltas':{k:{'before':old.get(k),'after':new.get(k)} for k in old.keys()|new.keys() if old.get(k)!=new.get(k)}},indent=2)+'\n')
 print((O/'stock-original-delta.json').read_text())
