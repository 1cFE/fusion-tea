from pathlib import Path
import runpy
h=Path.cwd()/'work/active/WI-050_mfe-coherent-operating-heating/prototype-r1'
out=h.parent/'review-r1-evidence'
original=Path.write_text
def redirect(self,*args,**kwargs):
    assert self.parent==h,self
    return original(out/self.name,*args,**kwargs)
Path.write_text=redirect
for name in ['consumers.py','check_results.py','check_repair.py']:
    print('RUN',name)
    runpy.run_path(str(h/name),run_name='__main__')
