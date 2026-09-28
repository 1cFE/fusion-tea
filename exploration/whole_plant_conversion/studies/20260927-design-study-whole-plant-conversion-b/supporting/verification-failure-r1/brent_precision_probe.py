"""One-case solver-precision experiment; no installed oracle/tolerance edits."""
from pathlib import Path
import hashlib,json,sys,math
ROOT=Path(__file__).resolve().parents[6];HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT))
from exploration.whole_plant_conversion import verify,oracle_thermal
from scripts.study import common,manifest,verify as stock
from exploration.whole_plant_conversion.studies import study_route as route
record=route.HERE/'20260927-design-study-whole-plant-conversion';case=next(r for r in json.loads((record/'results/cases.json').read_text())['cases'] if r['candidate_id'].endswith(':c1868'))
source=Path(oracle_thermal.__file__);before=hashlib.sha256(source.read_bytes()).hexdigest();loaded=manifest.load(route.MANIFEST_PATH);limits={r['channel']:r['value'] for r in loaded.data.get('absolute_tolerances',[])}
original=oracle_thermal.brentq;calls=[]
def tighter(function,a,b,**kwargs):
 kwargs.update(xtol=math.nextafter(0.,1.),rtol=4*sys.float_info.epsilon)
 result=original(function,a,b,**kwargs);calls.append(dict(outlet=result,residual=function(result),xtol=kwargs['xtol'],rtol=kwargs['rtol']));return result
oracle_thermal.brentq=tighter
try:outputs=verify.evaluate(case['inputs'])
finally:oracle_thermal.brentq=original
failures=[]
for k,e in outputs.items():
 a=case['outputs'][k];relative=common.relative_deviation(a,e);absolute=abs(a-e)
 if relative>=stock.TOLERANCE and absolute>=limits.get(k,0.):failures.append(dict(channel=k,native=a,oracle=e,relative=relative,absolute=absolute))
predicates=[]
for cid,item in verify.operand_bindings().items():
 values={k:(case['inputs'] if v['kind']=='input' else outputs)[v['key']] for k,v in item.items()};expected='satisfied' if verify.predicate(values,verify.authored_constraint_types()[cid.rsplit('__',1)[0]]) else 'violated'
 if expected!=case['verdicts'][cid]:predicates.append(cid)
after=hashlib.sha256(source.read_bytes()).hexdigest();P=verify.P
result=dict(kind='diagnostic in-process Brent stopping-precision experiment only; no acceptance change',case=case['case'],candidate_id=case['candidate_id'],source_sha256_before=before,source_sha256_after=after,files_unchanged=before==after,solver_calls=calls,scalar_comparisons=len(outputs),failed_comparisons=failures,predicate_comparisons=len(case['verdicts']),predicate_mismatches=predicates,precooler_outputs={k:v for k,v in outputs.items() if k.startswith(P+'water_pre__evaluate__')},operating_outputs={k:v for k,v in outputs.items() if k.startswith(P+'gas_operating__evaluate__')})
(HERE/'brent-precision-probe.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:v for k,v in result.items() if k not in ('precooler_outputs','operating_outputs')},indent=2))
