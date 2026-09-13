"""Independent local guards, error precedence, and native plant observations."""
import importlib
import json
import math
import os
from pathlib import Path
import sys
ROOT=Path.cwd()
sys.path[:0]=[str(ROOT/'exploration/stellarator_e2e/pkg'),str(Path(os.environ['STOP_PARSER_TEAX_ROOT'])/'packages/teax-simkit')]
field=importlib.import_module('stellarator_tea.modules.mfe_plasma_scaling.conductor_peak_field').Conductor_Peak_FieldModule()
cryo=importlib.import_module('stellarator_tea.modules.mfe_cryo_plant.cryoplant_electrical_power').Cryoplant_Electrical_PowerModule()
f=dict(B_axis_in=9.,peak_ratio_in=24.9/9.,R_in=12.7,a_coil_in=3.,R_ref_in=12.7,a_coil_ref_in=3.)
c=dict(q_nuc=0.,vol_cold=0.,p_fixed=0.,f_uplift=1.,T_cold=20.,T_amb=300.,f_carnot=1.,p_direct=0.)
checks=[]
def refuses(name,run,args,message):
    try: run(**args)
    except ValueError as exc:
        assert message in str(exc),(name,str(exc))
        checks.append({'case':name,'error':str(exc)})
    else: raise AssertionError(name)
# Both guards must precede any division: live R=0 with positive clearance gives
# zero bore factor; invalid reference must still win before normalization.
refuses('reference_before_zero_normalizer',field.run,dict(f,R_in=0.,a_coil_in=-1.,R_ref_in=0.,a_coil_ref_in=0.),'reference clearance')
refuses('both_invalid_live_first',field.run,dict(f,R_in=0.,a_coil_in=0.,R_ref_in=0.,a_coil_ref_in=0.),'live clearance')
for side,r,a in [('live','R_in','a_coil_in'),('reference','R_ref_in','a_coil_ref_in')]:
    for radius,coil in [(12.7,13.),(12.7,12.7),(float('nan'),3.)]:
        refuses(f'{side}_{radius}_{coil}',field.run,dict(f,**{r:radius,a:coil}),f'{side} clearance')
for cold,ambient in [(0,300),(-1,300),(300,300),(301,300),(20,0),(20,-1),(math.nan,300),(20,math.nan)]:
    # A zero f_carnot would divide by zero if domain checks were delayed.
    refuses(f'temperature_{cold}_{ambient}',cryo.run,dict(c,T_cold=cold,T_amb=ambient,f_carnot=0.),'require 0 < T_cold < T_amb')
for scale in [.1,1.,7.]:
    value=field.run(**dict(f,R_in=15*scale,a_coil_in=3*scale,R_ref_in=12.7*scale,a_coil_ref_in=3*scale)).data.root
    assert math.isclose(value*(15-3)*12.7,9*(24.9/9)*15*(12.7-3),rel_tol=1e-12)
for cold,amb in [(4.5,300),(20,300),(299,300)]:
    value=cryo.run(**dict(c,q_nuc=1000,vol_cold=100,p_fixed=.05,f_uplift=1.1,T_cold=cold,T_amb=amb,f_carnot=.25,p_direct=2.)).data.root
    assert math.isclose((value-2)*.25*cold, .165*(amb-cold),rel_tol=1e-12)
assert field.run(**dict(f,B_axis_in=-9.)).data.root==-24.9
assert cryo.run(**dict(c,p_direct=-17.)).data.root==-17.
Path(sys.argv[1]).write_text(json.dumps({'guard_checks':checks,'identity_checks':8},indent=2)+'\n')
print(f'{len(checks)} guard precedence/refusal and 8 identity/control checks passed')
