"""Strict native development runner. Complete new-package inputs only; no model math.

Legacy migration belongs to studies/migrate_controls.py. This runner does not
publish or release a main study interface.
"""
from pathlib import Path
import argparse,dataclasses,json,math,os,sys,traceback
from collections.abc import Mapping
ROOT=Path(__file__).resolve().parents[2];HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT));sys.path.insert(0,str(Path(os.environ['STOP_PARSER_TEAX_ROOT'])/'packages/teax-simkit'))
PACKAGE=HERE/'whole_plant_conversion_tea'
def prepare(work):
 from simkit.evaluation.evaluator import PreparedEvaluator
 from simkit.evaluation.package_load import ProvisionalPackageLoader
 from simkit.study.model_contract import load_model_contract,ships_constraint_report
 loader=ProvisionalPackageLoader(package_dir=PACKAGE.resolve(),package_name='whole_plant_conversion_tea',link_root=Path(work)/'package-link')
 specs=list((PACKAGE/'pipelines').glob('*.yaml'));assert len(specs)==1
 return PreparedEvaluator(loader,specs[0],expects_constraint_report=ships_constraint_report(load_model_contract(PACKAGE.resolve())))
def plain(value):
 if isinstance(value,Mapping):return {k:plain(v) for k,v in value.items()}
 if isinstance(value,(tuple,list)):return [plain(v) for v in value]
 return value
def execute(points,out):
 out=Path(out);out.mkdir(parents=True,exist_ok=True);prepared=prepare(out);rows=[]
 fields={k for m in prepared.entry_models.values() for k in m.model_fields}
 for index,point in enumerate(points):
  name=point.get('case',f'case{index:04d}');values=point['inputs'];row=dict(case=name,inputs=values,executable_fingerprint=prepared.fingerprint)
  try:
   if set(values)!=fields:raise ValueError(f'complete-input mismatch missing={sorted(fields-set(values))}, extra={sorted(set(values)-fields)}')
   if any(not isinstance(v,(int,float)) or not math.isfinite(v) for v in values.values()):raise ValueError('inputs must be finite numeric')
   typed={channel:model(**{k:values[k] for k in model.model_fields}) for channel,model in prepared.entry_models.items()}
   e=prepared.evaluate(typed)
   row.update(state='completed',status='evaluated',fingerprint=prepared.fingerprint,effective_inputs=values,outputs=dict(e.outputs),responses=dict(e.responses),constraint_report=plain(e.report),provenance=e.provenance.model_dump(mode='json'))
  except Exception as err:row.update(state='failed',error=str(err),exception_type=type(err).__name__,traceback=traceback.format_exc())
  rows.append(row);(out/'cases.json').write_text(json.dumps({'cases':rows},indent=2,default=str)+'\n')
  print(name,row['state'],row.get('error',''),flush=True)
 return rows
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--points',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args();d=json.loads(a.points.read_text());execute(d['cases'] if isinstance(d,dict) else d,a.out)
