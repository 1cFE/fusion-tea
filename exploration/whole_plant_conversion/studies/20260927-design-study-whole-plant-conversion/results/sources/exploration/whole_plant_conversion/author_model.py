"""Author the reviewed isolated native assembly. No plant calculations run here."""
from pathlib import Path
import json,re,runpy
ROOT=Path(__file__).resolve().parents[2];HERE=Path(__file__).resolve().parent
DOC='**Source**: work/active/WI-098_whole-plant-conversion-comparison/design.md. **Reference**: accepted r2 and capture correction. **Basis**: [AGENT] conditional supplied source, USD2025; assumptions remain explicit. **Last Updated**: 2026-09-27.'
contracts={}
for p in sorted((HERE/'bodies/whole_plant_conversion_accounts').glob('*_impl.py')):
 m=runpy.run_path(str(p));name=p.stem.removesuffix('_impl').replace('_',' ').title();contracts[name]={'inputs':m['INPUTS'],'outputs':m['OUTPUTS'],'body':str(p.relative_to(HERE))}
lib='package whole_plant_conversion_accounts {\n    private import ScalarValues::*;\n    private import costed_component::*;\n'
lib+=f"    part def 'Supplied Plant Account' :> 'Costed Component' {{ doc /* {DOC} */ }}\n"
for name,c in contracts.items():
 lib+=f"    calc def '{name}' {{\n        doc /* {DOC} Complete normative numerical semantics: exploration/whole_plant_conversion/{c['body']}; reviewed equations in design/configuration. */\n"
 lib+=''.join(f'        in attribute {k}_in : Real;\n' for k in c['inputs'])+''.join(f'        out attribute {k} : Real;\n' for k in c['outputs'])+'    }\n'
for name,op,val in [('Nonnegative','>=','0.0'),('Positive','>','0.0'),('Supported','>=','1.0')]:lib+=f"    constraint def 'Whole Plant {name}' {{ doc /* {DOC} */ in metric_in : Real; metric_in {op} {val} }}\n"
lib+='}\n';(ROOT/'models/library/analyses/whole_plant_conversion_accounts.sysml').write_text(lib)
(HERE/'definition-contracts.json').write_text(json.dumps(contracts,indent=2)+'\n')
parts=[]
def declarations(path,name):
 src=(ROOT/path).read_text();a=src.index("calc def '"+name+"'");m=re.search(r'\n    (?:calc|constraint|part) def ',src[a+1:]);chunk=src[a:a+1+m.start()] if m else src[a:]
 chunk=re.sub(r'/\*.*?\*/','',chunk,flags=re.S)
 return re.findall(r'in attribute (\w+) : (Real|Boolean)(?: default (?::=|=) ([^;{]+))?',chunk),re.findall(r'out attribute (\w+) : (Real|Boolean)',chunk)
def part(name,definition,values=None,source=None,checks=()):
 values=values or {}
 if source:ins,outs=declarations(source,definition)
 else:
  c=contracts[definition];ins=[(k+'_in','Real',str(v)) for k,v in c['inputs'].items()];outs=[(k,'Real') for k in c['outputs']]
 body=f'        part {name} {{\n            doc /* {DOC} */\n';binds=[]
 for formal,typ,default in ins:
  key=formal.removesuffix('_in');v=values.get(key,default)
  if v is None or v=='':raise ValueError((name,formal,'missing'))
  if isinstance(v,str) and '.' in v and not re.fullmatch(r'[-+0-9.eE]+',v):target=v
  else:
   lit=str(v).lower() if isinstance(v,bool) else str(v);attr='selected_'+key if key in dict(outs) else key
   body+=f'            attribute {attr} : {typ} = {lit};\n';target=attr
  binds.append(f'                in {formal} = {target};\n')
 body+=f"            calc evaluate : '{definition}' {{\n"+''.join(binds)+'            }\n'
 body+=''.join(f'            attribute {o} : {t} = evaluate.{o};\n' for o,t in outs)
 for field,kind in checks:body+=f"            assert constraint {field.lower()}_ok : 'Whole Plant {kind}' {{ in metric_in = {field}; }}\n"
 parts.append(body+'        }\n')
def account(name,quote,factor=1.,cas='22'):
 body=f"        part {name}_account : 'Supplied Plant Account' {{\n            doc /* {DOC} Selected procurement, independent of demand; disjoint membership in configuration.md. */\n            :>> cas_code = \"{cas}\";\n"
 if factor is None:
  assert isinstance(quote,str)
  body+=f'            attribute cost : Real = {quote};\n            :>> capital_cost = {quote};\n        }}\n'
  parts.append(body);return
 if isinstance(quote,str):ref=quote
 else:body+=f'            attribute quote_USD2025 : Real = {quote};\n';ref='quote_USD2025'
 if factor is None:fref='1.0'
 elif isinstance(factor,str):fref=factor
 else:body+=f'            attribute price_factor : Real = {factor};\n';fref='price_factor'
 body+=f"            calc purchase : 'Scaled Amount' {{ in amount_in = {ref}; in factor_in = {fref}; }}\n            attribute cost : Real = purchase.amount;\n            :>> capital_cost = purchase.amount;\n        }}\n";parts.append(body)
finance=dict(rate=.05,years=30.,availability=.8,construction_years=8.,contingency_rate=.1,indirect_rate=.2,freight_rate=.015,general_spares_rate=.02,tax_rate=.01,insurance_rate=.015,commissioning_rate=.005)
parts.append('        part finance {\n'+''.join(f'            attribute {k} : Real = {v};\n' for k,v in finance.items())+'        }\n')
part('source_basis','Supplied Source Basis',checks=[(k,'Nonnegative') for k in ['heating_coupled_margin','heating_wall_margin','divertor_margin','fusion_envelope_margin']]+[('domain_supported','Supported')])
parts.append('        part cryogenic_offer {\n            doc /* '+DOC+' Independently selected capacities and installed quote; immutable capture remains reference evidence. */\n            attribute cold_rating_W : Real = 40000.0;\n            attribute intercept_rating_W : Real = 60000.0;\n            attribute quote_USD2025 : Real = 62957384.24217385;\n        }\n')
part('supplied_core','Captured Reactor Offer',checks=[(k,'Nonnegative') for k in ['fit_margin','current_margin','field_margin_T','strain_margin','stress_margin_Pa']]+[('identity_supported','Supported')])
# Capture correction adds cryogenic_demand after its focused design gate.
if 'Conditional Cryogenic Demand' in contracts:
 part('cryogenic_demand','Conditional Cryogenic Demand',{k:('cryogenic_offer.' if k in ('cold_rating_W','intercept_rating_W') else 'supplied_core.')+k for k in contracts['Conditional Cryogenic Demand']['inputs'] if k not in ('q_nuc_W_m3','extra_cold_W')},checks=[('cold_margin_W','Nonnegative'),('intercept_margin_W','Nonnegative'),('domain_supported','Supported')])
 cryo='cryogenic_demand'
else:cryo='supplied_core'
fuelbind={'fusion_MW':'source_basis.fusion_MW','availability':'finance.availability','startup_required_kg':'fuel_inventory.startup_conservative_kg'}
part('fuel_accounts','Fuel Supply Accounts',fuelbind,checks=[('stock_margin','Nonnegative'),('processing_margin','Nonnegative'),('domain_supported','Supported')])
ib=dict(enabled=True,held_inventory=0.,p_fus='source_basis.fusion_MW',q_eff='fuel_accounts.q_eff',mev_to_joules='fuel_accounts.MeV_J',burn_fraction='fuel_accounts.burn_fraction',t_recycle='fuel_accounts.recycle',tbr_available='fuel_accounts.tbr',eta_extract='fuel_accounts.extraction',lambda_T='fuel_accounts.decay',G_stock=0.,m_T_kg='fuel_accounts.m_T',m_D_kg='fuel_accounts.m_D',plasma_volume=425.0000143721807,n_T0=1.9256443867349644e20,alpha_n=.33,tau_feed=1200.,tau_process=14400.,tau_blanket=86400.,tau_extract=86400.,tau_buffer=0.,tau_reserve=86400.,startup_extension=0.,shutdown_duration=86400.,reserve_fraction=.25,availability='finance.availability',s_per_year='fuel_accounts.seconds_year')
part('fuel_inventory','Fuel Inventory',ib,source='models/library/analyses/mfe_fuel_cycle.sysml')
# Existing flow definition adds a separately checked online atom balance.
part('fuel_flows','Fuel Cycle Flows',dict(p_fus='source_basis.fusion_MW',q_eff='fuel_accounts.q_eff',mev_to_joules='fuel_accounts.MeV_J',burn_fraction='fuel_accounts.burn_fraction',t_recycle='fuel_accounts.recycle',tbr_available='fuel_accounts.tbr',eta_extract='fuel_accounts.extraction',lambda_T='fuel_accounts.decay',I_total='fuel_inventory.total_atoms',G_stock=0.,m_T_kg='fuel_accounts.m_T',s_per_fpy='fuel_accounts.seconds_year'),source='models/library/analyses/mfe_fuel_cycle.sysml')
COMMON=dict(land=16901536.908759248,facilities=799758795.94032,magnet='supplied_core.magnet_capital',heating=264145000.,divertor=109109123.15593052,blanket=719155016.1966425,shield=452529516.99448603,structure=32373952.820015125,vessel=113317730.12762633,power_supplies=86013482.74180616,remote_handling=157969959.25281796,installation=509887983.2968712,primary_circulators=442174444.74911624,primary_pipes=2974043934.3757505,primary_spares=12020446.033021579,primary_helium=1409367.527367595,cryoplant='cryogenic_offer.quote_USD2025',auxiliary_rejection=50000000.,waste=6481502.633743829,fuel_processing=22811717.720117148,other_reactor=10098565.144581091,reactor_controls=81921417.18593018,shared_electrical=105407841.90324733,miscellaneous=64159703.76958075,pbl_initial=23815042.059888843,owner=37985982.20350555,digital_twin=5000000.,source_installation_allowance=200000000.,tritium_initial='fuel_accounts.initial_T_cost')
for k,v in COMMON.items():account(k,v,factor=None if k=='tritium_initial' else 1.)
for branch in ['steam','gas']:
 for i in range(1,11):account(f'{branch}_capital_{i}',f'{branch}_ledger.capital_{i}',factor=None,cas='23')
 account(f'{branch}_controller',f'{branch}_ledger.controller_capital',factor=None,cas='23')
 cb={k:f'{k}_account.cost' for k in COMMON}|{f'capital_{i}':f'{branch}_capital_{i}_account.cost' for i in range(1,11)}|dict(controller_capital=f'{branch}_controller_account.cost',steam_branch=float(branch=='steam'))|{k:f'finance.{k}' for k in finance if k not in ['rate','years','availability']}
 if branch=='steam':cb.update(salt_spare='steam_transport.secondary_spare',salt_vendor='steam_transport.secondary_vendor')
 part(branch+'_overheads','Whole Plant Capital Accounts',cb,checks=[('domain_supported','Supported')])
 for name in 'contingency indirect freight general_spares tax insurance nonfuel_commissioning'.split():account(f'{branch}_{name}',f'{branch}_overheads.{name}',factor=None,cas='29' if name=='contingency' else '30' if name=='indirect' else '50')
 ob=dict(conversion_net_MW=f'{branch}_ledger.net_electric',primary_electric_MW='primary_loop.p_elec',primary_fluid_MW='primary_loop.w_fluid',heating_wall_MW='source_basis.heating_wall_MW',deposited_heating_MW='source_basis.deposited_heating_MW',coil_drive_MW='supplied_core.coil_drive_MW',refrigeration_MW=cryo+'.refrigeration_MW',cold_W=cryo+'.cold_W',intercept_W=cryo+'.intercept_W',availability='finance.availability')
 # Common station assumptions owned once, with the second branch binding them.
 if branch=='gas':ob.update({k:'steam_operating.'+k for k in contracts['Whole Plant Operating Ledger']['inputs'] if k not in ob})
 part(branch+'_operating','Whole Plant Operating Ledger',ob,checks=[('net_export_MW','Positive'),('annual_net_grid_MWh','Positive'),('auxiliary_margin_MW','Nonnegative'),('domain_supported','Supported')])
 lb=dict(initial_capital=f'{branch}_overheads.initial_capital',salvage_base=f'{branch}_overheads.salvage_base',overhaul_base=f'{branch}_overheads.overhaul_base',magnet_capital='magnet_account.cost',blanket_capital='blanket_account.cost',divertor_capital='divertor_account.cost',pbl_capital='pbl_initial_account.cost',helium_capital='primary_helium_account.cost',wall_load='source_basis.wall_load',annual_export_MWh=f'{branch}_operating.annual_export_MWh',annual_net_grid_MWh=f'{branch}_operating.annual_net_grid_MWh',annual_import_cost=f'{branch}_operating.annual_import_cost',annual_fuel='fuel_accounts.annual_fuel',conversion_annual_service=f'{branch}_ledger.annual_service',conversion_annual_makeup=f'{branch}_ledger.annual_makeup',conversion_replacement_pv=f'{branch}_ledger.replacement_pv')|{k:'finance.'+k for k in ['rate','years','availability','construction_years']}
 if branch=='gas':lb.update({k:'steam_whole.'+('selected_'+k if k in contracts['Whole Plant Lifecycle Ledger']['outputs'] else k) for k in contracts['Whole Plant Lifecycle Ledger']['inputs'] if k not in lb})
 part(branch+'_whole','Whole Plant Lifecycle Ledger',lb,checks=[('outage_margin','Nonnegative'),('economic_defined','Supported'),('domain_supported','Supported')])
 ab=dict(primary_hot='primary_loop.T_out',primary_exchanger_return=('steam_return_control' if branch=='steam' else 'return_control')+'.exchanger_return',secondary_in='steam_return_control.secondary_inlet' if branch=='steam' else 'heat_exchangers.he_secondary_in',secondary_out='steam_secondary_temperature.value' if branch=='steam' else 'heat_exchangers.turbine_temperature')
 part(branch+'_actual_approach','Actual Exchanger Approaches',ab,checks=[('hot_gap','Positive'),('cold_gap','Positive')])
# Pure calculation owns Celsius-to-Kelvin, and explicit primary offered-rating margin.
part('steam_secondary_temperature','Temperature Kelvin',dict(celsius='steam_boundary.salt_hot'))
part('primary_offer','Supplied Primary Capacity',dict(pressure_demand_Pa='primary_loop.dp_loop',electric_demand_MW='primary_loop.p_elec',path_flow_demand='primary_loop.mdot_loop',path_count='primary_loop.n_loops'),checks=[('pressure_margin_Pa','Nonnegative'),('electric_margin_MW','Nonnegative'),('flow_margin_kg_s','Nonnegative'),('inventory_supported','Supported')])
old=(ROOT/'models/designs/component_alternatives/plant.sysml').read_text().replace('package component_alternatives {','package whole_plant_conversion {',1)
old=old.replace('    private import ScalarValues::*;','    private import ScalarValues::*;\n    private import whole_plant_conversion_accounts::*;\n    private import mfe_fuel_cycle::*;',1)
old=old.replace('attribute q_source : Real = 2500.0;','attribute q_source : Real = source_basis.q_source_MW;',1).replace('in q_source_in = blanket_source.q_source;','in q_source_in = source_basis.q_source_MW;')
# Only the two final branch ledgers own these exact declarations; legacy cost_accounts.discount remains retained.
for k,v in [('rate','0.05'),('years','30.0'),('availability','0.85')]:old=old.replace(f'attribute {k} : Real = {v};',f'attribute {k} : Real = finance.{k};')
cut=old.rfind('\n    }');text=old[:cut]+'\n'+''.join(parts)+old[cut:]
p=ROOT/'models/designs/whole_plant_conversion/plant.sysml';p.parent.mkdir(parents=True,exist_ok=True);p.write_text(text)
print('authored',len(contracts),'new definitions',len(parts),'parts')
