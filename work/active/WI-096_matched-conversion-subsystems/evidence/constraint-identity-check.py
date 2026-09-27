"""Check stock module/catalog identity and preserve semantics through label repair."""
import argparse,json
from pathlib import Path
import yaml
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3]
p=argparse.ArgumentParser();p.add_argument('--out',type=Path,required=True);args=p.parse_args()
package=ROOT/'exploration/component_alternatives/component_alternatives_tea'
pipeline=yaml.safe_load((package/'pipelines/pipeline.yaml').read_text())
ids={mid:mod['outputs']['evaluation'].split(' ',1)[1].removesuffix('__evaluation') for mid,mod in pipeline['modules'].items() if mod['module_type'].endswith('ConstraintModule')}
assert len(ids)==84 and all(k==v for k,v in ids.items())
rows={};id_map={}
for folder in sorted((HERE/'native_runs').iterdir()):
 if '.attempt' in folder.name or not (folder/'result.json').exists():continue
 previous=max(folder.parent.glob(folder.name+'.attempt*/result.json'),key=lambda q:int(q.parent.name.rsplit('attempt',1)[1]))
 a=json.loads(previous.read_text());b=json.loads((folder/'result.json').read_text())
 assert a['status']==b['status'] and a['effective_inputs']==b['effective_inputs']
 if b['status']!='evaluated':
  assert a['error']==b['error'];rows[folder.name]={'status':'same refusal'};continue
 old={k:v for k,v in a['outputs'].items() if isinstance(v,(int,float,bool))};new={k:v for k,v in b['outputs'].items() if isinstance(v,(int,float,bool))}
 assert old==new and len(new)==876
 before={r['constraint_id']:r['status'] for r in a['outputs']['constraint_report']['results']};after={r['constraint_id']:r['status'] for r in b['outputs']['constraint_report']['results']}
 assert set(after)==set(ids)
 normalize=lambda k:k.rsplit('__',1)[0].lower()
 assert {normalize(k):v for k,v in before.items()}=={normalize(k):v for k,v in after.items()}
 for k in set(before)-set(after):id_map[k]=next(v for v in after if normalize(k)==normalize(v))
 rows[folder.name]={'status':'pass','unchanged_scalars':len(new),'unchanged_predicate_verdicts':len(after),'before':str(previous.relative_to(HERE))}
assert len(id_map)==2
result={'status':'pass','constraint_module_ids':sorted(ids),'old_to_new':id_map,'cases':rows}
if args.out.exists():raise FileExistsError(args.out)
args.out.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({'status':'pass','module_id_matches':84,'old_to_new':id_map,'cases':len(rows)}))
