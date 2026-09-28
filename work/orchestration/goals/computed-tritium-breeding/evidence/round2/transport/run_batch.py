"""Execute a frozen explicit case plan; never mutate production artifacts."""
import argparse
import concurrent.futures
import json
import shutil
import subprocess
from pathlib import Path

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[6]
RUNTIME=ROOT/'.codex-test/breeding-transport'
p=argparse.ArgumentParser();p.add_argument('plan',type=Path);p.add_argument('--workers',type=int,default=4);args=p.parse_args()
plan=json.loads(args.plan.read_text())

def run_case(case):
    out=RUNTIME/'plant'/case['name']
    command=[str(HERE.parent/'runtime/run'),str(HERE/'plant_transport.py'),'--name',case['name']]
    for k,v in case['arguments'].items():
        command.append('--'+k.replace('_','-'))
        if not isinstance(v,bool): command.append(str(v))
    log_path=RUNTIME/f"{case['name']}.log"
    resource=RUNTIME/f"{case['name']}-resource.txt"
    with log_path.open('w') as log:
        run=subprocess.run(['/usr/bin/time','-v','-o',str(resource),*command],cwd=ROOT,stdout=log,stderr=subprocess.STDOUT)
    if run.returncode:
        raise RuntimeError(f"{case['name']} failed; inspect {log_path}")
    result=json.loads((out/'result.json').read_text()); result['case']=case
    evidence=HERE/'results'/case['name']; evidence.mkdir(parents=True,exist_ok=True)
    for name in ['manifest.json','result.json','model.xml']:
        shutil.copy2(out/name,evidence/name)
    shutil.copy2(resource,evidence/'resource.txt')
    shutil.copy2(log_path,evidence/'engine.log')
    print(case['name'],result['recoverable_TBR'],result['wall_seconds'],flush=True)
    return result

results=[]
with concurrent.futures.ThreadPoolExecutor(max_workers=args.workers) as pool:
    for result in pool.map(run_case,plan['cases']):
        results.append(result)
        args.plan.with_name(args.plan.stem+'-results.json').write_text(json.dumps(results,indent=2)+'\n')
