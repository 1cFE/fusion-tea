"""Re-execute original helper failure and successful single runner from git bytes."""
import importlib,json,shutil,subprocess,sys
from pathlib import Path
ROOT=Path.cwd();A=Path(__file__).resolve().parent;I=A.parent/'implementation';dest=A/'old-runner';dest.mkdir()
base='exploration/stellarator_e2e/'
for name in ('run_stellaris.py','run_stellaris_single.py','verify_stellaris.py'):
    (dest/name).write_bytes(subprocess.check_output(['git','show','45003717:'+base+name]))
shutil.copytree(I/'entering-package',dest/'generated',ignore=shutil.ignore_patterns('__pycache__','*.pyc'))
# Verify every original package payload against committed pre-implementation bytes.
for p in (dest/'generated').rglob('*'):
    if p.is_file():assert p.read_bytes()==subprocess.check_output(['git','show','45003717:'+base+'generated/'+str(p.relative_to(dest/'generated'))])
sys.path.insert(0,str(dest));rs=importlib.import_module('run_stellaris');single=importlib.import_module('run_stellaris_single')
frozen=json.loads((A.parent/'prototype/direct-entering.json').read_text())['results'];rows={}
for case in ('baseline','R14'):
    scratch=dest/case;scratch.mkdir();shutil.copytree(dest/'generated/inputs',scratch/'inputs');(scratch/'pipelines').mkdir()
    shutil.copyfile(dest/'generated/pipelines/pipeline.yaml',scratch/'pipelines/pipeline.yaml')
    if case=='R14':
        f=scratch/'inputs/stellarator_plant_params.json';p=json.loads(f.read_text());p.update({'stellarator_09__stellaris__R':14.,'stellarator_09__stellaris__magnet__R0':14.});f.write_text(json.dumps(p))
    rs.PIPELINE=scratch/'pipelines/pipeline.yaml';rs.E2E=scratch
    rows[case]={}
    for name,fn in [('single',single._execute_package),('helper',lambda:rs.run_pipeline('helper'))]:
        try:rows[case][name]={'outputs':{k:v.model_dump(mode='json') if hasattr(v,'model_dump') else v for k,v in fn().items()}}
        except Exception as e:rows[case][name]={'error':type(e).__name__,'message':str(e)}
    assert rows[case]['single']==frozen[case]['single']
    assert rows[case]['helper']['error']==frozen[case]['helper']['error']=='PipelineValidationError'
(A/'old-runner-results.json').write_text(json.dumps(rows,indent=2)+'\n')
print('PASS original single 177 raw outputs exact baseline/R14; original helper routing failure reproduced')
