"""Materialize only the reviewed additive WI-096 definitions/design; no model execution."""
from pathlib import Path
import importlib.util,json,re
ROOT=Path(__file__).resolve().parents[2];HERE=Path(__file__).resolve().parent
DOC='**Source**: work/active/WI-096_matched-conversion-subsystems/design.md. **Reference**: reviewed fourth submission, sections 2-8. **Basis**: [AGENT] conditional component offer and explicitly reviewed equations; hydraulic, price and loss-sink qualification remain unverified. **Last Updated**: 2026-09-26.'
contracts={}
for p in (HERE/'bodies/component_alternatives_thermal').glob('*_impl.py'):
 spec=importlib.util.spec_from_file_location(p.stem,p);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
 name=p.stem.removesuffix('_impl').replace('_',' ').title()
 contracts[name]={'inputs':m.INPUTS,'outputs':m.OUTPUTS,'body':str(p.relative_to(HERE))}
text='package component_alternatives_thermal {\n    private import ScalarValues::*;\n'
for name,c in contracts.items():
 text+=f"    calc def '{name}' {{\n        doc /* {DOC} Numerical semantics are the complete calculate function in exploration/component_alternatives/{c['body']}; units MW, K/degC, kg/s, Pa, MW/K, USD2025 and years as named. */\n"
 for k,v in c['inputs'].items():text+=f'        in attribute {k}_in : Real default := {v};\n'
 for k in c['outputs']:text+=f'        out attribute {k} : Real;\n'
 text+='    }\n'
text+=f"    constraint def 'Nonnegative Margin' {{ doc /* {DOC} Chosen capacity minus calculated demand; no physical tolerance. */ in margin_in : Real; margin_in >= 0.0 }}\n"
text+=f"    constraint def 'Required Flag' {{ doc /* {DOC} A calculated admission flag must equal one. */ in flag_in : Real; flag_in >= 1.0 }}\n"
text+=f"    constraint def 'Numerical Residual' {{ doc /* {DOC} Nonnegative residual magnitude compared with numerical calculation tolerance; no physical capacity allowance. */ in residual_in : Real; in tolerance_in : Real; residual_in <= tolerance_in }}\n}}\n"
(ROOT/'models/library/analyses/component_alternatives_thermal.sysml').write_text(text)
(HERE/'definition-contracts.json').write_text(json.dumps(contracts,indent=2)+'\n')
# Parse only definition declarations for authoring typed input/output bindings.
def declarations(path,name):
 src=Path(path).read_text();a=src.index("calc def '"+name+"'");m=re.search(r'\n    (?:calc|constraint|part) def ',src[a+1:]);b=a+1+m.start() if m else len(src);chunk=src[a:b]
 ins=re.findall(r'in attribute (\w+) : (Real|Boolean)(?: default := ([^;{]+))?',chunk)
 outs=re.findall(r'out attribute (\w+) : (Real|Boolean)',chunk)
 return ins,outs
parts=[]
def part(name,definition,values,source=None,checks=()):
 if source is None:
  c=contracts[definition];ins=[(k+'_in','Real',str(v)) for k,v in c['inputs'].items()];outs=[(k,'Real') for k in c['outputs']]
 else:ins,outs=declarations(ROOT/source,definition)
 body=f'        part {name} {{\n            doc /* {DOC} {name} owns its selected inputs and exposed calculation outputs. */\n';binds=[]
 for formal,typ,default in ins:
  key=formal.removesuffix('_in');v=values.get(key,default)
  if v is None or v=='':raise ValueError((name,formal,'missing input'))
  if isinstance(v,str) and '.' in v and not re.fullmatch(r'[-+0-9.eE]+',v):target=v
  else:
   lit=str(v).lower() if isinstance(v,bool) else str(v)
   attr='selected_'+key if any(key==o[0] for o in outs) else key
   body+=f'            attribute {attr} : {typ} = {lit};\n';target=attr
  binds.append(f'                in {formal} = {target};\n')
 body+=f"            calc evaluate : '{definition}' {{\n"+''.join(binds)+'            }\n'
 for o,t in outs:body+=f'            attribute {o} : {t} = evaluate.{o};\n'
 for check,kind,binding in checks:
  if kind=='Boolean Requirement':
   flag_value=name+'.'+binding['flag_in'];calc_name=check+'_screen'
   body+=f"            calc {calc_name} : 'Offered Capacity Screen' {{\n                in rating_in = 1.0;\n                in demand_in = 0.0;\n                in applicable_in = true;\n                in conditions_supported_in = {flag_value};\n                in demand_available_in = true;\n            }}\n"
   body+=f'            attribute {check}_defined : Real = {calc_name}.evaluation_defined;\n            attribute {check}_margin : Real = {calc_name}.margin;\n'
   kind='Offered Equipment Capacity';binding={'defined_in':check+'_defined','margin_in':check+'_margin'}
  body+=f"            assert constraint {check} : '{kind}' {{\n"+''.join(f'                in {k} = {v};\n' for k,v in binding.items())+'            }\n'
 body+='        }\n';parts.append(body)
def flag(name):return(name+'_ok','Required Flag',{'flag_in':name})
def margin(name):return(name+'_ok','Nonnegative Margin',{'margin_in':name})
def boolcheck(name):return(name+'_required','Boolean Requirement',{'flag_in':name})
old=(ROOT/'models/designs/costed_loop_brayton/costed_loop_brayton.sysml').read_text()
pat=list(re.finditer(r'^        part (\w+)[^\n]*\{',old,re.M));oldparts={m.group(1):old[m.start():pat[i+1].start() if i+1<len(pat) else old.rfind('\n    }')] for i,m in enumerate(pat)}
for name in ['blanket_source','primary_loop','cycle','compressor_1','intercooler_1','compressor_2','intercooler_2','compressor_3','pressure_loss','he_hx','idle_branches','heat_exchangers','turbine','recuperator','precooler','electrical','compressor_capacity','turbine_capacity','generator_capacity','he_capacity','return_control','cost_accounts','compressor_equipment','turbine_equipment','generator_equipment','heat_rejection_equipment','he_duty_equipment','conversion_services']:
 s=oldparts[name]
 if name=='blanket_source':s=s.replace('3125.9322770825056','2500.0')
 if name=='primary_loop':s=s.replace('f_loss : Real = 1.0','f_loss : Real = 1.1');s=s.replace('            attribute mdot :','            attribute w_fluid : Real = evaluate.w_fluid;\n            attribute p_loop_margin : Real = evaluate.p_loop_margin;\n            attribute mdot :')
 if name=='cycle':s=s.replace('selected_flow : Real = 2500.0','selected_flow : Real = 2000.0').replace('recuperator_effectiveness : Real = 0.8','recuperator_effectiveness : Real = recuperator_hardware.effectiveness')
 if name.startswith('compressor_'):s=s.replace('1.5182944859378311','1.5')
 if name=='electrical':
  for attr in ('auxiliary_heat','cryo','fuel_base','control','other_electric'):s=re.sub(r'(attribute '+attr+r' : Real = )[^;]+;',r'\g<1>0.0;',s)
  s=s.replace('pump_electric_in = primary_loop.p_elec','pump_electric_in = zero_load').replace('pump_recovered_in = primary_loop.q_recovered_total','pump_recovered_in = zero_load')
  s=s.replace('            attribute auxiliary_heat','            attribute zero_load : Real = 0.0;\n            attribute auxiliary_heat')
  s=s.replace("'Plant Electrical Balance' with the loop's own pump electricity and recovered friction;", "'Plant Electrical Balance' with upstream and whole-plant loads excluded;")
 if name in ('compressor_capacity','turbine_capacity','generator_capacity','he_capacity'):
  rating={'compressor_capacity':3200,'turbine_capacity':7000,'generator_capacity':3600,'he_capacity':3500}[name]
  s=re.sub(r'selected_rating : Real = [^;]+',f'selected_rating : Real = {rating}.0',s)
 if name=='return_control':s=s.replace('max_bypass : Real = 1.0','max_bypass : Real = 0.5')
 parts.append(s)
part('recuperator_hardware','Recuperator Installed Capability',dict(ua=60,flow='cycle.selected_flow',cp='cycle.cp'))
# Steam salt equipment uses source-owned channels; unused upstream subaccounts are excluded.
part('steam_transport','Cooling Equipment With Selected Salt Pump Count',dict(enabled=True,n_loops=14,salt_pumps_per_circuit=4,mdot_loop='primary_loop.mdot_loop',dp_loop='primary_loop.dp_loop',helium_suction_K='primary_loop.T_comp_in',helium_discharge_Pa='primary_loop.loop_p',helium_hot_K='primary_loop.T_out',helium_cp='primary_loop.loop_cp',helium_gamma='primary_loop.loop_gamma',primary_shaft_MW='primary_loop.w_fluid',primary_electric_MW='primary_loop.p_elec',q_ihx_MW='primary_loop.q_ihx',helium_design_shaft_MW=6.259319085874574,helium_design_suction_Pa=7670812.814306844,salt_design_flow_kg_s=250,salt_design_head_m=40,salt_design_eta_p=.75,salt_design_eta_motor=.95,helium_purchased_mass_kg=100000,salt_purchased_mass_kg=1608750.9823889225,discount=.05),source='models/library/analyses/cooling_equipment_selected_pumps.sysml',checks=[boolcheck(k) for k in ['ihx_capacity_ok','design_pump_size_ok','design_pump_type_ok','design_motor_base_ok','design_motor_factor_ok','pump_size_ok','pump_type_ok','motor_base_ok','motor_factor_ok','salt_head_ok','salt_flow_regime_ok']])
part('steam_return_control','Primary Bypass Control',dict(ua='steam_transport.installed_total_UA_MW_K',primary_flow='primary_loop.mdot',primary_cp='primary_loop.loop_cp',secondary_flow='steam_transport.total_salt_flow_kg_s',secondary_cp=1560,primary_limit='primary_loop.T_out',secondary_inlet=543.15,duty='primary_loop.q_ihx',required_return='primary_loop.T_comp_in',max_bypass=.5,tolerance=1e-6),source='models/library/analyses/loop_return_control.sysml')
for prefix,control in [('steam','steam_return_control'),('gas','return_control')]:
 values=dict(available='primary_loop.q_ihx',capability_open=control+'.capability_open',raw_heat=control+'.capability_at_solution',feasible=control+'.feasible',return_residual=control+'.return_residual',primary_flow='primary_loop.mdot',exchanger_flow=control+'.exchanger_primary_flow',bypass_fraction=control+'.bypass_fraction',pressure='primary_loop.loop_p',hot_temperature='primary_loop.T_out',dp='primary_loop.dp_loop',loss_factor='primary_loop.f_loss',max_bypass=control+'.max_bypass')
 if prefix=='steam':values.update(salt_flow='steam_transport.total_salt_flow_kg_s',salt_shaft='steam_transport.salt_shaft_MW',salt_electric='steam_transport.salt_electric_MW')
 part(prefix+'_boundary','Controlled Conversion Boundary',values,checks=[flag('source_adequate'),flag('controller_capacity_ok')]+[margin(k) for k in ['total_flow_margin','exchanger_flow_margin','bypass_flow_margin','bypass_fraction_margin','pressure_margin','temperature_margin','added_dp_margin']])
steam=dict(enabled=1,heat_available_MW='steam_boundary.steam_heat',source_heat_MW='steam_boundary.actual_heat',selected_recovered_MW='steam_transport.salt_shaft_MW',salt_flow_per_circuit='steam_transport.salt_flow',salt_circuit_count='steam_transport.n_loops',salt_hot_C='steam_boundary.salt_hot',salt_return_C='steam_boundary.salt_return',salt_cp_kJ_kgK=1.56,main_pressure_MPa=6.2,extraction_pressure_MPa=.8,steam_temperature_C=445,reheat_temperature_C=445,condenser_temperature_C=42,eta_hp=.9,eta_lp=.9,eta_condensate_pump=.8,eta_feedwater_pump=.8,eta_pump_motor=.95,eta_mechanical=.99,eta_generator=.98)
part('steam_cycle','Matched Steam Cycle',steam,source='models/library/analyses/mfe_matched_steam_cycle.sysml',checks=[boolcheck(k) for k in ['main_UA_available','reheat_UA_available','main_admission_ok','reheat_admission_ok']])
part('steam_losses','Controlled Conversion Boundary',dict(cycle_rejection='steam_cycle.q_rejection_before_cooling_MW',salt_electric='steam_transport.salt_electric_MW',salt_shaft='steam_transport.salt_shaft_MW',actuation='steam_boundary.actuation'))
part('gas_losses','Controlled Conversion Boundary',dict(gross_electric='electrical.gross_electric',net_shaft='electrical.net_shaft',imported_electric='electrical.shaft_import',actuation='gas_boundary.actuation'))
for name,source in [('steam_water','steam_losses'),('gas_loss_water','gas_losses')]:
 part(name,'Cooling Water Rejection',dict(enabled=1,cycle_active=1,q_rejection_before_cooling_MW=source+'.rejection_load',condenser_temperature_C=42,water_inlet_C=25,water_outlet_C=35,head_m=20,eta_pump=.8,eta_motor=.95),source='models/library/analyses/mfe_matched_steam_cycle.sysml',checks=[boolcheck('cooling_approach_ok')])
for name,inlet,conditioning in [('water_ic1','compressor_1','intercooler_1'),('water_ic2','compressor_2','intercooler_2'),('water_pre','recuperator','precooler')]:
 part(name,'Finite Water Cooler',dict(gas_inlet_K=inlet+('.hot_out' if inlet=='recuperator' else '.temperature_out'),gas_outlet_K=conditioning+'.temperature_out',gas_heat_into_fluid=conditioning+'.heat_into_fluid'),checks=[flag('evaluation_defined')]+[margin(k) for k in ['flow_margin','power_margin','duty_margin']])
# Retain point-state predicates; ratings below feed standard capacity screens.
condition=dict(enabled=True)
for suffix,actual,rated in [('main_pressure_MPa','steam_cycle.main_pressure_MPa',6.2),('extraction_pressure_MPa','steam_cycle.extraction_pressure_MPa',.8),('steam_C','steam_cycle.steam_temperature_C',445),('reheat_C','steam_cycle.reheat_temperature_C',445),('condenser_C','steam_cycle.condenser_temperature_C',42),('salt_hot_C','steam_boundary.salt_hot',465),('salt_return_C','steam_boundary.salt_return',269.6647299145299),('salt_cp','steam_cycle.salt_cp_kJ_kgK',1.56)]:condition['actual_'+suffix]=actual;condition['rated_'+suffix]=rated
part('steam_conditions','Steam Offered Conditions',condition,source='models/library/analyses/mfe_viability.sysml',checks=[boolcheck('supported')])
def screen(name,demand,rating,conditions=True):
 part(name,'Offered Capacity Screen',dict(rating=rating,demand=demand,applicable=True,conditions_supported=conditions,demand_available=True),source='models/library/analyses/mfe_viability.sysml',checks=[('capacity_requirement','Offered Equipment Capacity',{'defined_in':'evaluation_defined','margin_in':'margin'})])
for name,output,rating in [('gross','p_gross_MW',1219.9981701764736),('main_ua','main_UA_MW_K',41.07437838721364),('reheat_ua','reheat_UA_MW_K',11.18676341684029),('hp_flow','mdot_hp_kg_s',1108.5733942490049),('hp_shaft','p_hp_shaft_MW',507.1088862154872),('lp_flow','mdot_lp_kg_s',881.3051322292799),('lp_shaft','p_lp_shaft_MW',750.3619138014925),('condenser','q_condenser_MW',2058.639911447174),('condensate_flow','mdot_condensate_kg_s',881.3051322292799),('condensate_electric','p_condensate_electric_MW',.9261383157389033),('feed_flow','mdot_feed_kg_s',1108.5733942490049),('feed_electric','p_feedwater_electric_MW',8.780822331904837)]:screen('steam_'+name+'_capacity','steam_cycle.'+output,rating,'steam_conditions.supported')
# Existing pressure-rise calculation closes selected pump pressure ratings.
for name,hi,lo,rating in [('condensate','steam_cycle.p_condensate_pumped_MPa','steam_cycle.p_condensate_MPa',.7917904366),('feed','steam_cycle.p_feed_MPa','steam_cycle.p_heater_MPa',5.4)]:
 part('steam_'+name+'_pressure','Pump Pressure Rise',dict(active=True,outlet_MPa=hi,inlet_MPa=lo),source='models/library/analyses/mfe_viability.sysml')
 screen('steam_'+name+'_pressure_capacity','steam_'+name+'_pressure.demand',rating,'steam_conditions.supported')
for name,demand,rating in [('salt_fill','steam_transport.salt_required_fill_mass_kg','steam_transport.salt_purchased_mass_kg'),('salt_flow','steam_transport.salt_pump_flow','steam_transport.salt_design_flow_kg_s'),('salt_shaft','steam_transport.salt_pump_shaft_MW','steam_transport.salt_design_shaft_MW'),('salt_electric','steam_transport.salt_pump_electric_MW','steam_transport.salt_design_electric_MW'),('steam_water_flow','steam_water.water_flow_kg_s',50463.801850311946),('steam_water_electric','steam_water.p_cooling_pump_electric_MW',13.023180063562146),('steam_rejection','steam_water.q_total_rejection_MW',2109.621069383624),('gas_loss_flow','gas_loss_water.water_flow_kg_s',3000),('gas_loss_electric','gas_loss_water.p_cooling_pump_electric_MW',1),('gas_loss_duty','gas_losses.rejection_load',100),('recuperator_duty','recuperator.recovered_heat',4000)]:screen(name+'_capacity',demand,rating)
# Primary and net checks use existing predicates. New residual guards check fidelity only.
parts.append('        part source_checks {\n'+f'            doc /* {DOC} */\n'+"            assert constraint flow_ok : 'Loop Capacity' { in mdot_loop_in = primary_loop.mdot_loop; in mdot_loop_rated_in = primary_loop.mdot_loop_rated; }\n"+"            assert constraint pressure_ok : 'Loop Pressure Margin' { in p_loop_margin_in = primary_loop.p_loop_margin; }\n"+'        }\n')
# Ledger capital slots1/2 are separately replaced salt machinery/transport; rest recurring packages.
# Boundary uses existing eight-amount sum for salt capital rather than demand-derived selected input.
part('salt_capital','Eight Amount Sum',dict(amount1='steam_transport.hx_purchase',amount2='steam_transport.hx_installation',amount3='steam_transport.secondary_vendor',amount4='steam_transport.secondary_installation',amount5='steam_transport.secondary_pipe_purchase',amount6='steam_transport.secondary_pipe_installation',amount7='steam_transport.secondary_spare',amount8=0),source='models/library/analyses/integrated_equipment_costs.sysml')
part('bundle_sum','Eight Amount Sum',{**{f'amount{i}':0 for i in range(1,9)},'amount1':'steam_transport.bundle_event_purchase','amount2':'steam_transport.bundle_event_installation','amount3':'steam_transport.bundle_event_removal'},source='models/library/analyses/integrated_equipment_costs.sysml')
part('salt_replaced_capital','Eight Amount Sum',{**{f'amount{i}':0 for i in range(1,9)},'amount1':'steam_transport.secondary_vendor','amount2':'steam_transport.secondary_installation','amount3':'steam_transport.bundle_event_purchase','amount4':'steam_transport.bundle_event_installation'},source='models/library/analyses/integrated_equipment_costs.sysml')
steamledger=dict(separately_replaced_capital='salt_replaced_capital.total',available_heat='primary_loop.q_ihx',actual_heat='steam_boundary.actual_heat',gross='steam_cycle.p_gross_MW',steam_pumps='steam_cycle.p_cycle_pumps_MW',salt_pumps='steam_transport.salt_electric_MW',water1='steam_water.p_cooling_pump_electric_MW',controller_electric='steam_boundary.actuation',rejected1='steam_water.q_total_rejection_MW',capital1='salt_capital.total',capital2='steam_transport.salt_inventory_cost',capital3=247464428.83859593,capital4=115939531.80564217,salt_vendor='steam_transport.salt_machine_event_purchase',salt_installation='steam_transport.salt_machine_event_installation',salt_removal='steam_transport.salt_machine_event_removal',bundle_event='bundle_sum.total',salt_stock_cost='steam_transport.salt_inventory_cost')
part('steam_ledger','Conversion Subsystem Ledger',steamledger,checks=[('net_positive','Net Power Positive',{'net_electric':'evaluate.net_electric'}),('balance','Numerical Residual',{'residual_in':'conversion_energy_residual_magnitude','tolerance_in':'energy_tolerance'})])
# Add tolerance as a selected numerical scalar, not an extra physics calculation.
# Tolerance is computed by the ledger from available heat.
gasledger=dict(available_heat='primary_loop.q_ihx',actual_heat='heat_exchangers.accepted_heat',gross='electrical.gross_electric',shaft_import='electrical.shaft_import',water1='water_ic1.pump_electric',water2='water_ic2.pump_electric',water3='water_pre.pump_electric',water4='gas_loss_water.p_cooling_pump_electric_MW',controller_electric='gas_boundary.actuation',rejected1='water_ic1.total_rejection',rejected2='water_ic2.total_rejection',rejected3='water_pre.total_rejection',rejected4='gas_loss_water.q_total_rejection_MW',capital3='compressor_equipment.estimated_cost',capital4='turbine_equipment.estimated_cost',capital5='generator_equipment.estimated_cost',capital6='he_hx.estimated_cost',capital7='he_duty_equipment.estimated_cost',capital8='conversion_services.estimated_cost',capital9=85933000,capital10='heat_rejection_equipment.estimated_cost',currency_factor=321.9/188.9)
part('gas_ledger','Conversion Subsystem Ledger',gasledger,checks=[('net_positive','Net Power Positive',{'net_electric':'evaluate.net_electric'}),('balance','Numerical Residual',{'residual_in':'conversion_energy_residual_magnitude','tolerance_in':'energy_tolerance'})])
screen('rejection_capacity','gas_ledger.total_rejected',5000)
# The capacity screen helper names selected rating `rating`; retained purchase expects selected_rating.
parts[-1]=parts[-1].replace('attribute rating : Real','attribute selected_rating : Real').replace('rating_in = rating;','rating_in = selected_rating;')
imports=['ScalarValues','mfe_primary_loop','loop_return_control','integrated_heat_electricity','integrated_equipment_costs','ideal_gas_brayton_components','mfe_viability','integrated_equipment_parts','costed_component','mfe_account_costs','mfe_matched_steam_cycle','cooling_equipment_selected_pumps','component_alternatives_thermal']
output='package component_alternatives {\n'+f'    doc /* {DOC} */\n'+''.join('    private import '+i+'::*;\n' for i in imports)+'    part plant {\n'+f'        doc /* {DOC} Selected steam offer versus tested Brayton offers; separate ledgers, common source. */\n'+''.join(parts)+'    }\n}\n'
folder=ROOT/'models/designs/component_alternatives';folder.mkdir(parents=True,exist_ok=True);(folder/'plant.sysml').write_text(output)
print('Authored',len(parts),'parts and',len(contracts),'new thermal calculation definitions')
