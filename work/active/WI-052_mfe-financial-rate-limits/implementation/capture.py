"""Entering evidence capture restricted to explicit model/package/test paths."""
import hashlib
import json
import os
import shutil
import subprocess
import sys
import time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[4]
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT))
from tests.model_families import MFE, materialize_canonical_subset

def hashes(root):
    return {str(p.relative_to(root)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(root.rglob('*')) if p.is_file() and '__pycache__' not in p.parts and p.suffix!='.pyc'}

def logged(name,args,destination):
    command=[str(ROOT/'.codex-test/run'),*args]
    started=time.monotonic()
    with (destination/(name+'.log')).open('w') as out:
        result=subprocess.run(command,cwd=ROOT,stdout=out,stderr=subprocess.STDOUT)
    with (HERE/'commands.md').open('a') as out:
        out.write(f"\n- `{name}`: `{__import__('shlex').join(command)}`; exit {result.returncode}; elapsed {time.monotonic()-started:.3f}s; `{destination.name}/{name}.log`.\n")
    return result.returncode

def capture():
    destination=HERE/'entering';destination.mkdir(exist_ok=False)
    package=ROOT/'exploration/stellarator_e2e/generated'
    shutil.copytree(package,destination/'package',ignore=shutil.ignore_patterns('__pycache__','*.pyc'))
    materialize_canonical_subset(MFE,destination/'models')
    (destination/'inventory.json').write_text(json.dumps({'package':hashes(package),'models':hashes(destination/'models'),'head':subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),'python':sys.executable},indent=2)+'\n')
    logged('native',['python',str(HERE/'native_probe.py'),str(destination/'package'),str(destination/'native.json')],destination)
    for label,model in [('canonical',ROOT/'models'),('family',destination/'models'),('mirror',MFE.twin)]:
        logged('validation-'+label,['agentic-mbse','validate','--complete',str(model)],destination)
        logged('issues-'+label,['python',str(HERE/'validation_issues.py'),str(model),str(destination/('issues-'+label+'.json'))],destination)
    for suite in ('models','study'):
        logged('pytest-'+suite,['python','-m','pytest','tests/'+suite+'/', '-v','-ra','--tb=short','--junitxml='+str(destination/('pytest-'+suite+'.xml'))],destination)

if __name__=='__main__':capture()
