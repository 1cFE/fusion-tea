"""Ordinary native overrides and independent zero-consumer execution evidence."""
import importlib.util,json,math,sys
from pathlib import Path
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3]
s=importlib.util.spec_from_file_location('native_probe',ROOT/'work/active/WI-053_magnet-and-cryogenic-input-domains/evidence/native_probe.py');p=importlib.util.module_from_spec(s);s.loader.exec_module(p)
P=p.P+'magnet__'
values=[('negative_current',-15400000.,119.),('negative_density',15400000.,-119.),('negative_pair',-15400000.,-119.),('zero_current',0.,119.),('negative_zero_current',-0.,119.),('zero_density',15400000.,0.),('negative_zero_density',15400000.,-0.),('zero_pair',0.,0.),('zero_current_negative_density',0.,-119.),*[(name,v,119.) for name,v in [('nan_current',math.nan),('inf_current',math.inf),('negative_inf_current',-math.inf)]],*[(name,15400000.,v) for name,v in [('nan_density',math.nan),('inf_density',math.inf),('negative_inf_density',-math.inf)]]]
p.CASES={'baseline':{},**{name:{P+'I_coil':i,P+'j_wp':j} for name,i,j in values}}
p.run(ROOT/'exploration/stellarator_e2e/generated',HERE/'candidate-domain-native.json')
rows=json.loads((HERE/'candidate-domain-native.json').read_text())['cases']
for name,i,j in values:
 row=rows[name];assert row.get('error')=='EvaluationFailed',(name,row)
 if i==0 and j==119.:
  assert any(msg in row['message'] for msg in ('Plasma Sustainment: B_in must be nonzero','Winding Pack Stress: wp_side must be nonzero')),row
 else:assert 'Winding Pack Sizing:' in row['message'],row
# Capture real baseline sustainment input via its ordinary generated module call,
# then independently call the public module at both signed zeros.
from stellarator_tea.handwritten.mfe_plasma_sustainment import plasma_sustainment_impl as sustain
original=sustain.run_plasma_sustainment
captured=[]
def capture(inputs):
 captured.append(inputs.model_dump());return original(inputs)
sustain.run_plasma_sustainment=capture
p.CASES={'baseline':{}}
p.run(ROOT/'exploration/stellarator_e2e/generated',HERE/'candidate-captured-native.json')
sustain.run_plasma_sustainment=original
assert captured
(HERE/'baseline-sustain-input.json').write_text(json.dumps(captured[-1],indent=2)+'\n')
from stellarator_tea.modules.mfe_plasma_sustainment.plasma_sustainment import Plasma_SustainmentModule
local=[]
for zero in (0.,-0.):
 try:Plasma_SustainmentModule().run(**{**captured[-1],'B_in':zero})
 except sustain.SustainmentError as exc:local.append({'B_in':zero,'error':type(exc).__name__,'message':str(exc)})
 else:raise AssertionError('zero sustainment accepted')
(HERE/'local-sustainment.json').write_text(json.dumps(local,indent=2)+'\n')
print('PASS fifteen invalid/zero native cases and independently invoked public zero sustainment')
