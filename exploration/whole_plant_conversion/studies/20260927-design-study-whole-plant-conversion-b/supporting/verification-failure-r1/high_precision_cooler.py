"""Independent high-precision cooler adjudication of the retained failing point.

Integrate heat/temperature-gap over piecewise-linear water enthalpy intervals.
No production body is imported; original oracle code is read but never edited.
"""
from pathlib import Path
from decimal import Decimal,localcontext
import json,sys,math
ROOT=Path(__file__).resolve().parents[6];HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT))
from exploration.whole_plant_conversion import verify,oracle_thermal
P=verify.P
RECORD=ROOT/'exploration/whole_plant_conversion/studies/20260927-design-study-whole-plant-conversion'

def reference(raw,precision=80):
 with localcontext() as ctx:
  ctx.prec=precision
  # Preserve the supplied binary64 inputs exactly, then perform the physical
  # equations at high precision with decimal SI conversion constants.
  d=Decimal.from_float;x={k:d(v) for k,v in raw.items()};D=Decimal
  table=[(D(str(r['t'])),D(str(r['h']))) for r in oracle_thermal._liquid_rows()]
  def interpolation(value,reverse=False):
   rows=[(h,t) for t,h in table] if reverse else table
   for (a,fa),(b,fb) in zip(rows,rows[1:]):
    if a<=value<=b:return fa+(fb-fa)*(value-a)/(b-a)
   raise ValueError('reference interpolation outside retained water table')
  q=-x['gas_heat_into_fluid'];hot=x['gas_inlet_K']-D('273.15');cold=x['gas_outlet_K']-D('273.15')
  electric=D('9.80665')*x['head']/(D(1000)*x['eta_p']*x['eta_motor']);reservoir=interpolation(x['water_inlet_C']);inlet_h=reservoir+electric;inlet=interpolation(inlet_h,True)
  def at(outlet):
   end_h=interpolation(outlet);rise=end_h-inlet_h;flow=D(1000)*q/rise
   nodes=[(inlet,inlet_h)]+[(t,h) for t,h in table if inlet<t<outlet]+[(outlet,end_h)]
   gaps=[cold+(hot-cold)*(h-inlet_h)/rise-t for t,h in nodes]
   ua=D(0)
   for i in range(len(nodes)-1):
    heat=q*(nodes[i+1][1]-nodes[i][1])/rise;a,b=gaps[i:i+2]
    ua+=heat*((b/a).ln()/(b-a) if b!=a else 1/a)
   return ua,flow,min(gaps)
  lo=inlet+D('1e-7');hi=min(hot,D(60))-D('1e-7')
  for iteration in range(400):
   mid=(lo+hi)/2
   if at(mid)[0]<x['ua']:lo=mid
   else:hi=mid
   if hi-lo<D(10)**(-(precision-15)):break
  else:raise ValueError('reference bracket did not converge')
  mid=(lo+hi)/2;ua,flow,gap=at(mid);power=flow*electric/1000
  result=dict(water_outlet_C=mid,water_inlet_after_C=inlet,min_gap=gap,required_ua=ua,ua_residual=ua-x['ua'],water_flow=flow,pump_electric=power,total_rejection=q+power,energy_residual=flow*(interpolation(mid)-reservoir)/1000-q-power,flow_margin=x['flow_rating']-flow,power_margin=x['power_rating']-power)
  return {k:str(v) for k,v in result.items()},dict(iterations=iteration+1,root_bracket_width_K=str(hi-lo),decimal_precision=precision)

case=next(r for r in json.loads((RECORD/'results/cases.json').read_text())['cases'] if r['candidate_id'].endswith(':c1868'))
pipeline=verify.yaml.safe_load((verify.PACKAGE/'pipelines/pipeline.yaml').read_text())
def extract(values):
 result={}
 for formal,source in pipeline['modules'][P+'water_pre__evaluate']['inputs'].items():
  key=source.split(' ',1)[1]
  result[formal.removesuffix('_in')]=case['inputs'][key.split('.',1)[1]] if key.startswith('plant_params.') else values[key]
 return result
independent=verify.evaluate(case['inputs']);native_inputs=extract(case['outputs']);oracle_inputs=extract(independent)
records=[]
for label,inputs,outputs in [('native',native_inputs,case['outputs']),('oracle',oracle_inputs,independent)]:
 ref,meta=reference(inputs);ref60,_=reference(inputs,60)
 comparisons={k:dict(recorded=outputs[P+'water_pre__evaluate__'+k],reference=v,error=str(Decimal.from_float(outputs[P+'water_pre__evaluate__'+k])-Decimal(v))) for k,v in ref.items()}
 records.append(dict(input_basis=label,inputs=inputs,reference=ref,convergence=meta,repeat_60_digit_max_difference=max(float(abs(Decimal(v)-Decimal(ref60[k]))) for k,v in ref.items()),comparisons=comparisons))
# Full downstream propagation uses only this independent reference's outputs.
original_calculate=verify.calculate;replacement={k:float(v) for k,v in records[1]['reference'].items()}
def diagnostic_calculate(definition,inputs,owner,calc,gas):
 result=original_calculate(definition,inputs,owner,calc,gas)
 if owner=='water_pre' and definition=='Finite Water Cooler':result.update(replacement)
 return result
verify.calculate=diagnostic_calculate
try:propagated=verify.evaluate(case['inputs'])
finally:verify.calculate=original_calculate
owners=('gas_operating','gas_whole','gas_ledger','water_pre')
changes={k:dict(native=case['outputs'][k],original_oracle=independent[k],reference_propagated=propagated[k],propagation_delta=propagated[k]-independent[k]) for k in propagated if any(k.startswith(P+owner+'__') for owner in owners) and (propagated[k]!=independent[k] or any(word in k for word in ('net_export','power_residual','economic_defined','balance','lcoe','energy_residual')))}
result=dict(kind='independent high-precision adjudication; unchanged native/acceptance/oracle files',case=case['case'],candidate_id=case['candidate_id'],method='80-digit Decimal SI equations, independently transcribed piecewise-water enthalpy, analytic segment integration in water temperature, root bracket below1e-65K; repeated at60digits',input_differences={k:dict(native=native_inputs[k],oracle=oracle_inputs[k]) for k in native_inputs if native_inputs[k]!=oracle_inputs[k]},references=records,downstream_propagation=changes)
(HERE/'high-precision-cooler.json').write_text(json.dumps(result,indent=2)+'\n')
for record in records:
 print(record['input_basis'],record['convergence'])
 for k in ('water_outlet_C','min_gap','required_ua','ua_residual'):print(k,record['comparisons'][k])
