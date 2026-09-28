"""Small independent-seed grid and fixed reference diagnostic cases."""
import argparse
import concurrent.futures
import json
import shutil
import subprocess
from pathlib import Path

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[6]
RUNTIME=ROOT/'.codex-test/breeding-transport'
p=argparse.ArgumentParser();p.add_argument('--cards',type=Path,required=True);p.add_argument('--tag',default='pilot');p.add_argument('--subset',choices=['all','diagnostics','grid'],default='all');p.add_argument('--workers',type=int,default=4);args=p.parse_args()
cases=[]
for t in [.6,.8,1.]:
 for e in [.6,.7,.9]:
  cases.append(dict(name=f'{args.tag}-t{t:.1f}-e{e:.1f}',thickness=t,enrichment=e,seed=10001+104729*len(cases),openings='none',boundary=20.))
baseline=next(c for c in cases if c['thickness']==.8 and c['enrichment']==.7)
for name,seed,openings,boundary in [('repeat',902177,'none',20.),('boundary30',baseline['seed'],'none',30.),('single',1300019,'single',20.),('split',1700021,'split',20.)]:
 cases.append(dict(name=f'{args.tag}-{name}',thickness=.8,enrichment=.7,seed=seed,openings=openings,boundary=boundary))
results=[]
if args.subset=='diagnostics':
 cases=[baseline]+cases[9:]
elif args.subset=='grid':
 cases=cases[:9]
def run_case(case):
 out=RUNTIME/'plant'/case['name']
 command=[str(HERE.parent/'runtime/run'),str(HERE/'plant_transport.py'),'--cards',str(args.cards.resolve()),'--name',case['name'],'--thickness',str(case['thickness']),'--enrichment',str(case['enrichment']),'--seed',str(case['seed']),'--openings',case['openings'],'--boundary-radius',str(case['boundary'])]
 with (RUNTIME/f"{case['name']}.log").open('w') as log:
  run=subprocess.run(['/usr/bin/time','-v','-o',str(RUNTIME/f"{case['name']}-resource.txt"),*command],cwd=ROOT,stdout=log,stderr=subprocess.STDOUT)
 if run.returncode:
  raise RuntimeError(f"Case {case['name']} failed; see log")
 result=json.loads((out/'result.json').read_text())
 result['case']=case
 evidence=HERE/'pilot-results'/case['name']
 evidence.mkdir(parents=True,exist_ok=True)
 for name in ['manifest.json','result.json','model.xml']:
  shutil.copy2(out/name,evidence/name)
 shutil.copy2(RUNTIME/f"{case['name']}-resource.txt",evidence/'resource.txt')
 print(case['name'],result['recoverable_TBR'],result['wall_seconds'],flush=True)
 return result
with concurrent.futures.ThreadPoolExecutor(max_workers=args.workers) as pool:
 for result in pool.map(run_case,cases):
  results.append(result)
  (HERE/f'pilot-summary-{args.subset}.json').write_text(json.dumps(results,indent=2)+'\n')
