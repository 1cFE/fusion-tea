"""Bounded validation probes; never calls comparison or an optimizer."""
from pathlib import Path
import os,sys,json,hashlib,traceback,dataclasses,datetime
from collections.abc import Mapping
ROOT=Path(__file__).resolve().parents[3]; OUT=Path(__file__).resolve().parent
for path in [ROOT, ROOT/'exploration/stellarator_e2e/studies',Path(os.environ['STOP_PARSER_TEAX_ROOT'])/'packages/teax-simkit']:
 sys.path.insert(0,str(path))
import study_route as route
from simkit.study.bridge import CandidateBridge
P=route.P; package=route.PACKAGE_DIR
public={}
for f in (package/'inputs').glob('*.json'): public.update(json.loads(f.read_text()))
def val(k): return public[P+k]
def clean(x):
 if hasattr(x,'model_fields'):return {k:clean(getattr(x,k)) for k in type(x).model_fields}
 if dataclasses.is_dataclass(x):return clean(dataclasses.asdict(x))
 if isinstance(x,Mapping):return {str(k):clean(v) for k,v in x.items()}
 if isinstance(x,(list,tuple)):return [clean(v) for v in x]
 if isinstance(x,(str,int,float,bool)) or x is None:return x
 return repr(x)
cases=[('baseline',{})]
for k,vs in {
 'plasma__R':[12.6,12.8,15.7], 'plasma__a':[1.2,1.4,2.2],
 'plasma__n_e0':[val('plasma__n_e0')*f for f in [.9,1.1]],
 'plasma__T_i0':[val('plasma__T_i0')*f for f in [.9,1.1]],
 'magnet__coil__turn_current':[val('magnet__coil__turn_current')*f for f in [.8,1.3]],
 'cryoplant__T_cold_cryo':[21.],
 'blanket__blanket_t':[.599,.6,1.,1.001],
 'heat_transport__loop_dT_blanket':[160.,250.],
 'heat_transport__loop_p':[1e5],
 'turbine__main_steam_generator__outlet_temperature_C':[455.,456.],
 'turbine__open_feedwater_heater__pressure_MPa':[.9],
 'turbine__condenser__temperature_C':[20.,60.],
 'heat_rejection__water_outlet_C':[42.,61.],
 'heat_transport__loop_cp':[0.],
}.items():
 assert P+k in public,k
 for v in vs:cases.append((f'{k}={v}',{P+k:v}))
# Individually admitted temperatures, coupled zero terminal approach.
cases.append(('coupled_water_approach', {P+'heat_rejection__water_inlet_C':35.,P+'heat_rejection__water_outlet_C':42.,P+'turbine__condenser__temperature_C':42.}))
cases=[cases[i] for i in [0,1,3,6,7,8,11,12,13,14,15,16,18,19,20,21,22,23,24,25,29]]
assert len(cases)<=21
(OUT/'proposals.json').write_text(json.dumps(cases,indent=2))
engine=route.prepare(package,OUT/'native');bridge=CandidateBridge(engine.entry_models)
identity={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'route':'study_route.prepare -> CandidateBridge.build -> PreparedEvaluator.evaluate','fingerprint':clean(engine.fingerprint),'envelope_sha256':hashlib.sha256((OUT/'intended-envelope.md').read_bytes()).hexdigest(),'files':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(package.rglob('*')) if p.is_file() and '__pycache__' not in str(p)},'route_sha256':hashlib.sha256(Path(route.__file__).read_bytes()).hexdigest()}
(OUT/'identity.json').write_text(json.dumps(identity,indent=2))
for i,(label,changes) in enumerate(cases):
 record={'index':i,'prior_native_attempts_including_interrupted':19,'label':label,'proposal':changes,'utc':datetime.datetime.now(datetime.timezone.utc).isoformat()}
 try:
  typed=bridge.build(route.validate_proposal(changes));record['typed_inputs']=clean(typed)
  row=engine.evaluate(typed);record['native_returned']=True;record['result']=clean(row);record['status']='returned'
 except Exception as e:
  record.update(status='raised',exception_type=type(e).__name__,exception=str(e),traceback=traceback.format_exc(),exception_attributes=clean(vars(e)))
 (OUT/f'case-{i:02d}.json').write_text(json.dumps(record,indent=2,allow_nan=False))
 print(i,label,record['status'],record.get('exception',''),flush=True)
