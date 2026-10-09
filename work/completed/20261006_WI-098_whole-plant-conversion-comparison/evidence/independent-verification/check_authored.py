"""Binding and MR-7 checks using authored literals; not a native execution receipt."""
import json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[5];HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT))
from exploration.whole_plant_conversion import verify as v
attrs,calcs=v.authored()
d={v.P+p+'__'+n:v.literal(x) for p,n,t,x in attrs if v.literal(x) is not None}
for p,n,t,b in calcs:
 for key,x in b.items():
  if v.literal(x) is not None:d[v.P+p+'__'+n+'__'+key]=v.literal(x)
v.defaults=lambda:d.copy()
base=v.evaluate({});high=v.evaluate({v.P+'source_basis__q_source_MW':2800})
checks={}
def check(name,condition):
 assert condition,name
 checks[name]='pass'
get=lambda r,p,n:r[v.P+p+'__evaluate__'+n]
for p in ['steam_overheads','gas_overheads']:
 check(p+'_capital_invariant',get(base,p,'initial_capital')==get(high,p,'initial_capital'))
for p,n in [('source_basis','fusion_MW'),('primary_loop','w_fluid'),('fuel_accounts','annual_D_kg')]:
 check(p+'_demand_responds',get(high,p,n)>get(base,p,n))
quote=v.P+'steam_ledger__capital3'
if quote in d:
 q=v.evaluate({quote:d[quote]*1.1})
 check('steam_quote_changes_steam_total',get(q,'steam_overheads','initial_capital')>get(base,'steam_overheads','initial_capital'))
 check('steam_quote_preserves_gas_total',get(q,'gas_overheads','initial_capital')==get(base,'gas_overheads','initial_capital'))
 check('steam_quote_preserves_common_total',get(q,'steam_overheads','common_purchases')==get(base,'steam_overheads','common_purchases'))
for heat,extra,positive in [(35.5,0,True),(50,0,True),(80,0,False),(35.5,10000,True),(35.5,13000,False)]:
 changed=v.evaluate({v.P+'cryogenic_demand__q_nuc_W_m3':heat,v.P+'cryogenic_demand__extra_cold_W':extra})
 check(f'cryo_capacity_{heat}_{extra}',(get(changed,'cryogenic_demand','cold_margin_W')>=0)==positive)
 for branch in ['steam','gas']:
  check(f'cryo_capital_fixed_{branch}_{heat}_{extra}',get(changed,branch+'_overheads','initial_capital')==get(base,branch+'_overheads','initial_capital'))
  refri_delta=get(changed,'cryogenic_demand','refrigeration_MW')-get(base,'cryogenic_demand','refrigeration_MW')
  check(f'cryo_electric_propagates_{branch}_{heat}_{extra}',abs(get(base,branch+'_operating','net_export_MW')-get(changed,branch+'_operating','net_export_MW')-refri_delta)<1e-9)
  heat_delta=(get(changed,'cryogenic_demand','cold_W')-get(base,'cryogenic_demand','cold_W'))*1e-6
  check(f'cryo_heat_propagates_{branch}_{heat}_{extra}',abs(get(changed,branch+'_operating','auxiliary_heat_MW')-get(base,branch+'_operating','auxiliary_heat_MW')-refri_delta-heat_delta)<1e-9)
 check(f'cryo_fusion_fixed_{heat}_{extra}',get(changed,'source_basis','fusion_MW')==get(base,'source_basis','fusion_MW'))
record=dict(status='pass' ,kind='authored oracle only; native evidence is separate',numerical_outputs=len(base),checks=checks)
(HERE/'authored-checks.json').write_text(json.dumps(record,indent=2)+'\n');print(json.dumps(record))
