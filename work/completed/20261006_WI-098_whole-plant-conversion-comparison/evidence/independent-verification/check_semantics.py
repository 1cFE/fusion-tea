"""Independent equation checks before native agreement; no native imports."""
import hashlib,json,math,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[5];HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT))
from exploration.whole_plant_conversion import oracle_whole_plant as o
abi=json.loads((HERE.parent/'calc-interfaces.json').read_text())
def defaults(name):return {k.removesuffix('_in'):v for k,v in abi[name]['inputs'].items()}
checks=[]
def check(name,condition):
 assert condition,name
 checks.append(name)
s=defaults('Supplied Source Basis');r=o.source_interface(s)
check('source_forward',abs(r['reconstructed_source_MW']-2500)<1e-9)
check('heating_wall_100MW',r['heating_wall_MW']==100)
check('source3000_divertor_exclusion',o.source_interface(s|{'q_source_MW':3000})['divertor_margin']<0)
f=defaults('Fuel Supply Accounts')|{'fusion_MW':r['fusion_MW']};f0=o.fuel_interface(f)
flow=f0['reaction_rate'];react=flow*f['seconds_year']*f['availability']
check('D_mass_balance',math.isclose(f0['annual_D_kg']/f['m_D'],react*(1+(1-f['burn_fraction'])/f['burn_fraction']*(1-f['recycle'])),rel_tol=1e-14))
check('Li6_atoms_match_gross_bred',math.isclose(f0['annual_Li6_kg']/f['m_Li6'],react*f['tbr'],rel_tol=1e-14))
fext=o.fuel_interface(f|{'extraction':.8});check('extraction_increases_T_supply',fext['annual_T_external']>f0['annual_T_external'])
check('extraction_cannot_reduce_Li6_feed',fext['annual_Li6_kg']==f0['annual_Li6_kg'])
fr=o.fuel_interface(f|{'recycle':.95});check('loss_increases_D_and_T',fr['annual_D_kg']>f0['annual_D_kg'] and fr['annual_T_external']>f0['annual_T_external'])
check('loss_does_not_change_neutron_breeding',fr['annual_Li6_kg']==f0['annual_Li6_kg'])
fp=o.fuel_interface(f|{'tritium_price':0.});check('free_T_retains_D_Li6_cost',fp['annual_fuel']==fp['annual_D_cost']+fp['annual_Li6_cost'])
stock=o.fuel_interface(f|{'stock_kg':6});check('stock_decay_calendar_time',math.isclose(stock['annual_T_need']-f0['annual_T_need'],f['decay']*f['seconds_year'],rel_tol=1e-12))
check('event_at_retirement_excluded',o.event_dates(10,.8,25)==[12.5])
check('two_magnet_events',o.event_dates(10,.8,30)==[12.5,25.])
l=defaults('Whole Plant Lifecycle Ledger')|dict(rate=0,initial_capital=100,annual_export_MWh=10,annual_net_grid_MWh=9,annual_fuel=2,routine_om=0,primary_event=0,wall_load=1,overhaul_base=0)
lr=o.lifecycle_interface(l);check('zero_discount_energy',lr['energy_pv']==300)
check('zero_discount_finance',lr['initial_financed_capital']==100)
check('zero_discount_cost_streams',lr['total_cost_pv']==100+60+10)
try:o.lifecycle_interface(l|{'years':30.5})
except ValueError:check('fractional_life_rejected',True)
else:check('fractional_life_rejected',False)
cap=defaults('Whole Plant Capital Accounts')|dict(controller_capital=0)
c0=o.capital_interface(cap)
# Every common leaf has a distinct basis signature; check membership independently.
for name in o.COMMON_ACCOUNTS:
 c=o.capital_interface(cap|{name:1})
 check('capital_leaf_'+name,c['common_purchases']==1 and c['direct_base']==float(name not in ['land','owner','tritium_initial']) and c['equipment_base']==float(name in o.COMMON_EQUIPMENT) and c['overhaul_base']==float(name in o.OVERHAUL_EQUIPMENT))
for steam in [0,1]:
 for slot in range(1,11):
  c=o.capital_interface(cap|{'steam_branch':steam,'capital_'+str(slot):1})
  equipment=float(slot!=2) if steam else float(slot>=3)
  freight=float(slot in ([3,4] if steam else [3,4,5,6,7,8,10]))
  check(f'branch_membership_{steam}_{slot}',c['branch_purchases']==1 and c['equipment_base']==equipment and c['freight_base']==freight)
op=defaults('Whole Plant Operating Ledger')|dict(conversion_net_MW=500,primary_electric_MW=100,primary_fluid_MW=90,refrigeration_MW=3,coil_drive_MW=.05,cold_W=28000,intercept_W=42000)
op0=o.operating_interface(op);op1=o.operating_interface(op|{'primary_electric_MW':110})
check('primary_motor_loss_owned_once',math.isclose(op0['net_export_MW']-op1['net_export_MW'],10) and math.isclose(op1['auxiliary_heat_MW']-op0['auxiliary_heat_MW'],10))
check('outage_standby_excludes_operating_only',op0['standby_MW']==3+4+2)
check('annual_net_grid_explicit',op0['annual_net_grid_MWh']==op0['annual_export_MWh']-op0['annual_import_MWh'])
(HERE/'semantic-checks.json').write_text(json.dumps(dict(status='pass',checks=checks,oracle_sha256=hashlib.sha256(Path(o.__file__).read_bytes()).hexdigest()),indent=2)+'\n')
print('pass',len(checks),'checks')
