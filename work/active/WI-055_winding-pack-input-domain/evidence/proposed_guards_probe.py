"""Runtime-only experiment: local sizing and stress denominator checks."""
import importlib.util,json,math
from pathlib import Path
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[3]
s=importlib.util.spec_from_file_location('native_probe',ROOT/'work/active/WI-053_magnet-and-cryogenic-input-domains/evidence/native_probe.py');p=importlib.util.module_from_spec(s);s.loader.exec_module(p)
package=ROOT/'exploration/stellarator_e2e/generated'
ev=p.PreparedEvaluator(p.ProvisionalPackageLoader(package,'stellarator_tea',HERE/'link',strict=True),package/'pipelines/pipeline.yaml',expects_constraint_report=True)
from stellarator_tea.handwritten.mfe_magnet_field import winding_pack_sizing_impl as sizing
original=sizing.run_winding_pack_sizing
calls=[]
def checked(inputs):
 calls.append((inputs.I_coil,inputs.j_wp))
 if not math.isfinite(inputs.I_coil) or inputs.I_coil<0 or not math.isfinite(inputs.j_wp) or inputs.j_wp<=0:raise ValueError('LOCAL_WINDING_DOMAIN')
 return original(inputs)
sizing.run_winding_pack_sizing=checked
from stellarator_tea.handwritten.mfe_magnet_field import winding_pack_stress_impl as stress
original_stress=stress.run_winding_pack_stress
stress_calls=[]
def checked_stress(inputs):
 stress_calls.append(inputs.wp_side)
 if inputs.wp_side<=0:raise ValueError('LOCAL_STRESS_DOMAIN')
 return original_stress(inputs)
stress.run_winding_pack_stress=checked_stress
from stellarator_tea.handwritten.mfe_plasma_sustainment import plasma_sustainment_impl as sustain
original_sustain=sustain.run_plasma_sustainment
sustain_calls=[]
def checked_sustain(inputs):
 sustain_calls.append(inputs.B_in)
 if inputs.B_in == 0:raise sustain.SustainmentError('SUSTAIN_ZERO_FIELD_DOMAIN')
 return original_sustain(inputs)
sustain.run_plasma_sustainment=checked_sustain
bridge=p.CandidateBridge(ev.entry_models);rows={}
for name,i in [('negative',-15400000.),('zero',0.),('nan',float('nan')),('inf',float('inf'))]:
 calls.clear();stress_calls.clear();sustain_calls.clear()
 try:ev.evaluate(bridge.build({p.P+'magnet__I_coil':i}));row={'result':'success'}
 except Exception as e:row={'error':type(e).__name__,'message':str(e)}
 rows[name]={**row,'sizing_calls':list(calls),'stress_calls':list(stress_calls),'sustain_calls':list(sustain_calls)}
(HERE/'proposed-guards-native.json').write_text(json.dumps(rows,indent=2)+'\n');print(rows)
