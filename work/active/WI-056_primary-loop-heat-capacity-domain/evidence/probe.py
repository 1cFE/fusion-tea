"""Capture supported native and local primary-loop boundary behavior."""
import importlib.util,json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[4];HERE=Path(__file__).resolve().parent
s=importlib.util.spec_from_file_location('native',ROOT/'work/active/WI-053_magnet-and-cryogenic-input-domains/evidence/native_probe.py');p=importlib.util.module_from_spec(s);s.loader.exec_module(p)
P=p.P
invalid={'zero':0.,'negative':-1.,'nan':float('nan'),'inf':float('inf'),'negative_inf':-float('inf')}
p.CASES={'baseline':{},'double_cp':{P+'loop_cp':10386.},'double_dT':{P+'loop_dT_blanket':400.},'dormant':{P+'loop_live':0.},'finance_zero':{P+'discount_rate':0.},'magnet_half':{P+'magnet__I_coil':7700000.},**{f'{mode}_{field}_{name}':{P+'loop_'+field:v,P+'loop_live':live} for mode,live in [('live',1.),('dormant',0.)] for field in ('cp','dT_blanket') for name,v in invalid.items()},'negative_pair':{P+'loop_cp':-5193.,P+'loop_dT_blanket':-200.}}
p.run(ROOT/'exploration/stellarator_e2e/generated',HERE/(sys.argv[1]+'-native.json'))
from stellarator_tea.modules.mfe_primary_loop.primary_coolant_loop import Primary_Coolant_LoopInput
from stellarator_tea.handwritten.mfe_primary_loop.primary_coolant_loop_impl import run_primary_coolant_loop
BASE=dict(q_source_in=2101.7,T_in_in=573.15,dT_blanket_in=200.,cp_in=5193.,gamma_in=1.6667,p_loop_in=8e6,n_loops_in=9.,mdot_loop_ref_in=2025.7/9,dp_loop_ref_in=550000.,f_loss_in=1.,eta_is_in=.9,eta_drive_in=1.,loop_live_in=1.,p_pump_direct_in=3.,eta_p_direct_in=.5)
rows={}
for live in (0.,1.):
 for q in (0.,2101.7):
  for name,overrides in [('baseline',{}),('negative_pair',{'cp_in':-5193.,'dT_blanket_in':-200.})]+[(field+'_'+name,{field:v}) for field in ('cp_in','dT_blanket_in') for name,v in invalid.items()]:
   try:r={'outputs':run_primary_coolant_loop(Primary_Coolant_LoopInput(**(BASE|{'loop_live_in':live,'q_source_in':q}|overrides)))}
   except Exception as e:r={'error':type(e).__name__,'message':str(e)}
   rows[f'{live}/{q}/{name}']=r
(HERE/(sys.argv[1]+'-local.json')).write_text(json.dumps(rows,indent=2,default=str)+'\n')
