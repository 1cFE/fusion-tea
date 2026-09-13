"""Entering local and native winding-domain observations, without production changes."""
import importlib.util,json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[4]
HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('native_probe',ROOT/'work/active/WI-053_magnet-and-cryogenic-input-domains/evidence/native_probe.py')
p=importlib.util.module_from_spec(spec);spec.loader.exec_module(p)
P=p.P+'magnet__'
p.CASES={'baseline':{},**{name:{P+'I_coil':i,P+'j_wp':j} for name,i,j in [('negative_current',-15400000.,118.8271604938272),('negative_density',15400000.,-118.8271604938272),('negative_pair',-15400000.,-118.8271604938272),('zero_current',0.,118.8271604938272),('zero_density',15400000.,0.),('zero_pair',0.,0.),('nan_current',float('nan'),119.),('inf_current',float('inf'),119.),('nan_density',15400000.,float('nan')),('inf_density',15400000.,float('inf'))]}}
p.run(ROOT/'exploration/stellarator_e2e/generated',HERE/'entering-native.json')
from stellarator_tea.handwritten.mfe_magnet_field.winding_pack_sizing_impl import run_winding_pack_sizing
from stellarator_tea.modules.mfe_magnet_field.winding_pack_sizing import Winding_Pack_SizingInput
rows={}
for name,values in p.CASES.items():
 args={'I_coil':values.get(P+'I_coil',15400000.),'j_wp':values.get(P+'j_wp',118.8271604938272)}
 try: rows[name]={'result':str(run_winding_pack_sizing(Winding_Pack_SizingInput(**args)))}
 except Exception as e:rows[name]={'error':type(e).__name__,'message':str(e)}
(HERE/'entering-local.json').write_text(json.dumps(rows,indent=2)+'\n')
print(rows)
