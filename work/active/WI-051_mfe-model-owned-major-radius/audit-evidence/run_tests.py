"""Run unchanged kept tests, redirecting three deterministic retained-evidence writes."""
import sys
from pathlib import Path
ROOT=Path.cwd(); A=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT))
import pytest
original=Path.write_text
protected={ROOT/'work/active/WI-051_mfe-model-owned-major-radius/implementation'/n for n in ('contract-checks.json','edges.json','contract-delta.json')}
redirects=[]
def guarded(self,data,*args,**kwargs):
    if self.absolute() in protected:
        assert self.read_text()==data, f'Retained evidence differs: {self}'
        redirects.append(str(self))
        return original(A/('test-replay-'+self.name),data,*args,**kwargs)
    return original(self,data,*args,**kwargs)
Path.write_text=guarded
code=pytest.main(['tests/models/','-v','-ra','--junitxml='+str(A/'tests.xml')])
original(A/'test-redirects.txt','\n'.join(redirects)+'\n')
raise SystemExit(code)
