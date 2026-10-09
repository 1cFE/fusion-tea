"""Prove magnitude-only representation preserves all prior numerical outputs/verdicts."""
import argparse,json
from pathlib import Path
HERE=Path(__file__).resolve().parent
p=argparse.ArgumentParser();p.add_argument('--out',type=Path,required=True);args=p.parse_args()
rows={}
for folder in sorted((HERE/'native_runs').iterdir()):
 if '.attempt' in folder.name or not (folder/'result.json').exists():continue
 before_paths=list(folder.parent.glob(folder.name+'.attempt*/result.json'))
 if not before_paths:continue
 previous=next(q for q in sorted(before_paths,key=lambda q:int(q.parent.name.rsplit('attempt',1)[1]),reverse=True) if json.loads(q.read_text())['status']!='evaluated' or len([v for v in json.loads(q.read_text())['outputs'].values() if isinstance(v,(int,float,bool))])==874)
 before=json.loads(previous.read_text());after=json.loads((folder/'result.json').read_text())
 assert before['status']==after['status']
 if after['status']!='evaluated':
  assert before['error']==after['error'];rows[folder.name]={'status':'same refusal'};continue
 a,b=before['outputs'],after['outputs'];keys={k for k,v in a.items() if isinstance(v,(int,float,bool))}
 assert all(a[k]==b[k] for k in keys)
 extras={k for k,v in b.items() if isinstance(v,(int,float,bool))}-keys
 assert len(extras)==2 and all(k.endswith('__conversion_energy_residual_magnitude') for k in extras)
 for k in extras:assert b[k]==abs(b[k.removesuffix('_magnitude')])
 def verdicts(o):return {r['constraint_id'].rsplit('__',1)[0].lower():r['status'] for r in o['constraint_report']['results']}
 assert verdicts(a)==verdicts(b) and len(verdicts(b))==84
 rows[folder.name]={'status':'pass','unchanged_scalar_channels':len(keys),'added_magnitude_channels':sorted(extras),'unchanged_predicates':84,'before':str(previous.relative_to(HERE))}
if args.out.exists():raise FileExistsError(args.out)
args.out.write_text(json.dumps(rows,indent=2)+'\n');print(json.dumps({'cases':len(rows),'evaluated':sum(r['status']=='pass' for r in rows.values())}))
