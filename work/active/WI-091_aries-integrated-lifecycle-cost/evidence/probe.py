import sys,json,tempfile
from pathlib import Path
sys.path.insert(0,str(Path('exploration/aries_integrated').resolve()))
from run import load_runtime,execute_case,PREFIX
root=Path(tempfile.mkdtemp(prefix='wi091-probe-'))
row=execute_case('base',{PREFIX+'source__producer_mode':1.},load_runtime(),root=root)
Path('work/active/WI-091_aries-integrated-lifecycle-cost/evidence/probe-result.json').write_text(json.dumps(row,indent=2)+'\n')
print(row['status'],root)
if row['status']=='refused':print(row['traceback'])
else:
 print(json.dumps({k:v for k,v in row['outputs'].items() if any(x in k for x in ('lifecycle','operating_levelization'))},indent=2))
