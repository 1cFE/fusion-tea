"""Three post-repair native refusal checks, separate from coverage exploration."""
from pathlib import Path
import os,sys,json,traceback,dataclasses
from collections.abc import Mapping
ROOT=Path(__file__).resolve().parents[3];OUT=Path(__file__).resolve().parent
for p in [ROOT,ROOT/'exploration/stellarator_e2e/studies',Path(os.environ['STOP_PARSER_TEAX_ROOT'])/'packages/teax-simkit']:
 sys.path.insert(0,str(p))
import study_route as route
from simkit.study.bridge import CandidateBridge

def clean(x):
 if hasattr(x,'model_fields'):return {k:clean(getattr(x,k)) for k in type(x).model_fields}
 if dataclasses.is_dataclass(x):return clean(dataclasses.asdict(x))
 if isinstance(x,Mapping):return {str(k):clean(v) for k,v in x.items()}
 if isinstance(x,(tuple,list)):return [clean(v) for v in x]
 if isinstance(x,(str,int,float,bool)) or x is None:return x
 return repr(x)
engine=route.prepare(route.PACKAGE_DIR,OUT/'native-acceptance')
bridge=CandidateBridge(engine.entry_models)
records=[]
for name,proposal,expected in [
 ('primary-suction',{'heat_transport__loop_p':100000.},['unsupported compressor pressure state','p_loop_in=100000.0 Pa','dp_loop=','suction=']),
 ('conductor-field',{'magnet__coil__turn_current':40000.},['B_peak outside 20..32 T','actual=']),
 ('conductor-temperature',{'cryoplant__T_cold_cryo':21.},['temperature=21.0 K','expected 20.0 K']),
]:
 point={route.P+k:v for k,v in proposal.items()}
 record={'name':name,'proposal':point,'executable_fingerprint':engine.fingerprint}
 try:
  row=engine.evaluate(bridge.build(point))
 except Exception as exc:
  record.update(status='refused',exception=str(exc),exception_type=type(exc).__name__,attributes=clean(vars(exc)),traceback=traceback.format_exc())
  assert all(x in str(exc) for x in expected),str(exc)
 else:
  raise AssertionError((name,'unsupported point unexpectedly completed'))
 records.append(record)
(OUT/'native-refusals.json').write_text(json.dumps(records,indent=2)+'\n')
print('PASS three native domain refusals with offending values; no completed outputs manufactured')
