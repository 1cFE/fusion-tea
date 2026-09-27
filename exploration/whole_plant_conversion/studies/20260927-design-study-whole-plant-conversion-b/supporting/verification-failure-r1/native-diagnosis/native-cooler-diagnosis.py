import json,sys,math,hashlib,os
from pathlib import Path
import yaml
root=Path('/home/reid/1cfe/fusion-tea');sys.path.insert(0,str(root/'exploration/whole_plant_conversion'))
sys.path.insert(0,str(Path(os.environ['STOP_PARSER_TEAX_ROOT'])/'packages/teax-simkit'))
from whole_plant_conversion_tea.handwritten.component_alternatives_thermal import finite_water_cooler_impl as native
record=root/'exploration/whole_plant_conversion/studies/20260927-design-study-whole-plant-conversion'
r=next(r for r in json.loads((record/'results/cases.json').read_text())['cases'] if r['case']=='gas-favourable::gas-q2500-m2500-r1.8-ua40-40-60')
params=yaml.safe_load((root/'exploration/whole_plant_conversion/whole_plant_conversion_tea/pipelines/pipeline.yaml').read_text())['modules']['whole_plant_conversion__plant__water_pre__evaluate']['inputs']
x={}
for formal,binding in params.items():
 ref=binding.split()[-1];x[formal.removesuffix('_in')]=(r['inputs'][ref.split('.',1)[1]] if '.' in ref else r['outputs'][ref])
saved={}
def trace(frame,event,arg):
 if frame.f_code is native.calculate.__code__ and event=='return':saved.update(frame.f_locals)
 return trace
sys.settrace(trace)
try:o=native.calculate(x)
finally:sys.settrace(None)
at=saved['at'];lo=saved['lo'];hi=saved['hi'];mid=saved['mid'];u=x['ua'];delta=1e-10
result={'case':r['case'],'candidate_id':r['candidate_id'],'inputs':x,'native_exact_receipt_match':all(o[k]==r['outputs']['whole_plant_conversion__plant__water_pre__evaluate__'+k] for k in native.OUTPUTS),'native_outputs':o,'final_bracket':{'lo':lo,'hi':hi,'width_K':hi-lo,'adjacent_binary64':math.nextafter(lo,math.inf)==hi,'lo_UA':at(lo)[0],'hi_UA':at(hi)[0],'selected':mid},'profile':{'gas_hot_C':saved['hot'],'gas_cold_C':saved['cold'],'water_inlet_after_C':saved['ta'],'water_outlet_C':mid},'local_native_UA_derivative_MW_per_K2':(at(mid+delta)[0]-at(mid-delta)[0])/(2*delta),'body_sha256':hashlib.sha256(Path(native.__file__).read_bytes()).hexdigest()}
Path('/tmp/wi098-native-cooler-diagnosis.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
