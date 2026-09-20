"""WI-073 explicit canonical authoring; run once against the entering sources."""
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[5]
ITEM = ROOT / 'work/active/WI-073_matched-steam-cycle-for-current-comparison'
SOURCE = 'work/orchestration/goals/current-model-comparison-readiness/evidence/round2/cycle-proposal-v2.md'
DOC = f'**Source**: {SOURCE} **Reference**: WI-073 design.md and interface-inventory.md; original NIST tables and independent physical review. **Basis**: [AGENT] reviewed reduced extraction/reheat cycle and conditional cooling-water scenario; equipment and installed cost unqualified. **Last Updated**: 2026-09-19'

states = ['feed', 'main', 'hp', 'reheat', 'lp', 'condensate', 'condensate_pumped', 'heater']
state_out = []
for state in states:
    state_out.extend(f'{kind}_{state}_{unit}' for kind, unit in [('p','MPa'),('h','kJ_kg'),('mdot','kg_s')])
    if state != 'condensate_pumped':
        state_out.extend([f't_{state}_C', f's_{state}_kJ_kgK'])
cycle_out = state_out + '''bleed_fraction mdot_bleed_kg_s salt_flow_total_kg_s salt_main_flow_kg_s salt_reheat_flow_kg_s q_main_MW q_reheat_MW q_condenser_MW p_hp_shaft_MW p_lp_shaft_MW p_condensate_shaft_MW p_feedwater_shaft_MW p_condensate_electric_MW p_feedwater_electric_MW p_cycle_pumps_MW p_gross_MW eta_gross p_cycle_net_before_cooling_MW q_mechanical_loss_MW q_generator_loss_MW q_pump_motor_loss_MW q_rejection_before_cooling_MW lp_quality lp_moisture_fraction main_min_gap_K reheat_min_gap_K main_UA_MW_K reheat_UA_MW_K salt_heat_residual_MW heater_mass_residual_kg_s heater_energy_residual_MW cycle_shaft_residual_MW cycle_electric_residual_MW'''.split()
cycle_bool = 'active main_UA_available reheat_UA_available main_admission_ok reheat_admission_ok turbine_equipment_qualified installed_sg_capacity_qualified'.split()
cycle_in = '''enabled heat_available_MW salt_flow_per_circuit salt_circuit_count salt_hot_C salt_return_C salt_cp_kJ_kgK main_pressure_MPa extraction_pressure_MPa steam_temperature_C reheat_temperature_C condenser_temperature_C eta_hp eta_lp eta_condensate_pump eta_feedwater_pump eta_pump_motor eta_mechanical eta_generator'''.split()
cw_in = 'enabled cycle_active q_rejection_before_cooling_MW condenser_temperature_C water_inlet_C water_outlet_C head_m eta_pump eta_motor'.split()
cw_out = 'water_flow_kg_s p_cooling_pump_shaft_MW p_cooling_pump_electric_MW q_cooling_motor_loss_MW q_total_rejection_MW water_pump_rise_K condenser_water_gap_K water_energy_residual_MW denominator_kJ_kg'.split()
cw_bool = 'active reference_scenario site_qualified cooling_approach_ok'.split()
select_in = 'matched_enabled legacy_eta matched_eta legacy_domain_product'.split()

def calc(name, inputs, outputs, booleans=()):
    return '\n'.join([f"    calc def '{name}' {{", f'        doc /* {DOC} Numerical semantic: the normative handwritten implementation executes the exact state/work equations in the cited design. Disabled modes branch before property access; no extrapolation. Units are given by the scalar names and interface inventory. */', *[f'        in attribute {n}_in : Real;' for n in inputs], *[f'        out attribute {n} : Real;' for n in outputs], *[f'        out attribute {n} : Boolean;' for n in booleans], '    }'])

analysis = 'package mfe_matched_steam_cycle {\n    private import ScalarValues::*;\n'
analysis += '\n'.join([calc('Matched Steam Cycle', cycle_in, cycle_out, cycle_bool), calc('Cooling Water Rejection', cw_in, cw_out, cw_bool), calc('Cycle Mode Selection', select_in, ['eta_selected'], ['legacy_domain_applicable', 'matched_domain_applicable'])])
analysis += f'''\n    constraint def 'Active Steam Heat Direction' {{
        doc /* {DOC} Positive temperature difference is necessary for the modeled heat direction. Disabled mode is inapplicable; raw module flags and margins remain separately visible. This does not replace the prior scenario-specific20K screen or qualify installed capacity. */
        in attribute enabled_in : Real;
        in attribute gap_in : Real;
        enabled_in == 0.0 or gap_in > 0.0
    }}
}}\n'''
(ROOT/'models/library/analyses/mfe_matched_steam_cycle.sysml').write_text(analysis)

interfaces = ROOT/'models/library/structure/mfe_interfaces.sysml'
s = interfaces.read_text(); assert "item def 'Water State Stream'" not in s
s = s.rstrip()[:-1] + f'''
    item def 'Water State Stream' {{
        doc /* {DOC} Supported water boundary: pressure MPa, enthalpy kJ/kg, mass flow kg/s. Component state properties expose temperature/entropy only where evaluated. */
        attribute pressure_MPa : Real;
        attribute enthalpy_kJ_kg : Real;
        attribute mass_flow_kg_s : Real;
    }}
    port def 'Water State Port' {{ doc /* {DOC} Water or steam leaving a component. */ out item stream : 'Water State Stream'; }}
    port def 'Heat Duty Port' {{ doc /* {DOC} Heat duty MW. */ out item heat : 'Electric Power'; }}
    port def 'Shaft Power Port' {{ doc /* {DOC} Mechanical shaft work MW; type carries power only, not electrical ownership. */ out item shaft : 'Electric Power'; }}
}}
'''
interfaces.write_text(s)

# The stream ports describe physical direction; scalar properties carry actual solver bindings.
def partdef(name, attrs, ports='', parent=''):
    inh = f" :> '{parent}'" if parent else ''
    return '\n'.join([f"    part def '{name}'{inh} {{", f'        doc /* {DOC} No individual installed price is implied by this physical occurrence. */', ports, *[f'        attribute {a} : Real;' for a in attrs], '    }'])
boundary = 'p_in_MPa h_in_kJ_kg flow_in_kg_s p_out_MPa h_out_kJ_kg flow_out_kg_s'.split()
body = 'package mfe_steam_cycle_components {\n    private import ScalarValues::*;\n    private import mfe_interfaces::*;\n'
body += partdef('Steam State Component', boundary, "        port inlet : ~'Water State Port';\n        port outlet : 'Water State Port';")
body += '\n' + partdef('Steam Heat Exchanger', 'pressure_MPa outlet_temperature_C heat_MW minimum_gap_K required_UA_MW_K salt_flow_kg_s'.split(), "        port salt : ~'Thermal Port';", 'Steam State Component')
body += '\n' + partdef('Steam Expansion', ['efficiency', 'shaft_MW'], "        port shaft_out : 'Shaft Power Port';", 'Steam State Component')
body += '\n' + partdef('Steam Feed Heater', 'pressure_MPa bleed_flow_kg_s bleed_h_kJ_kg mass_residual_kg_s energy_residual_MW'.split(), "        port bleed_in : ~'Water State Port';", 'Steam State Component')
body += '\n' + partdef('Steam Condenser', ['temperature_C', 'rejected_MW'], "        port rejection : 'Heat Duty Port';", 'Steam State Component')
body += '\n' + partdef('Steam Liquid Pump', ['efficiency', 'shaft_MW', 'electric_MW'], "        port electric_in : ~'Electric Port';", 'Steam State Component')
body += '\n' + partdef('Steam Generator Machine', 'mechanical_efficiency generator_efficiency hp_shaft_MW lp_shaft_MW gross_MW mechanical_loss_MW generator_loss_MW'.split(), "        port hp_shaft : ~'Shaft Power Port';\n        port lp_shaft : ~'Shaft Power Port';\n        port electric_out : 'Electric Port';")
body += '\n' + partdef('Circulating Water Pump', 'head_m efficiency motor_efficiency flow_kg_s shaft_MW electric_MW'.split(), "        port electric_in : ~'Electric Port';")
body += '\n}\n'
(ROOT/'models/library/structure/mfe_steam_cycle_components.sysml').write_text(body)

# Cycle state aliases are producer interfaces; nested components bind aliases, not calc internals.
def state_bind(start, end, owner='Turbine Plant', flow_start=None):
    values = dict(p_in_MPa=f'p_{start}_MPa', h_in_kJ_kg=f'h_{start}_kJ_kg', flow_in_kg_s=flow_start or f'mdot_{start}_kg_s', p_out_MPa=f'p_{end}_MPa', h_out_kJ_kg=f'h_{end}_kJ_kg', flow_out_kg_s=f'mdot_{end}_kg_s')
    return '\n'.join(f"            :>> {key} = '{owner}'::{val};" for key,val in values.items())
def component(name, type_, start=None, end=None, aliases=None, facts=()):
    lines=[f"        part {name} : '{type_}' {{"]
    if start: lines.append(state_bind(start,end,flow_start='mdot_reheat_kg_s' if name=='reheater' else None))
    for key,val in (aliases or {}).items(): lines.append(f"            :>> {key} = 'Turbine Plant'::{val};")
    for key in facts: lines.append(f"            :>> {key} default 0.0;")
    lines.append('        }');return '\n'.join(lines)

components = [
component('main_steam_generator','Steam Heat Exchanger','feed','main',dict(heat_MW='q_main_MW',minimum_gap_K='main_min_gap_K',required_UA_MW_K='main_UA_MW_K',salt_flow_kg_s='salt_main_flow_kg_s'),['pressure_MPa','outlet_temperature_C']),
component('hp_turbine','Steam Expansion','main','hp',dict(shaft_MW='p_hp_shaft_MW'),['efficiency']),
component('reheater','Steam Heat Exchanger','hp','reheat',dict(heat_MW='q_reheat_MW',minimum_gap_K='reheat_min_gap_K',required_UA_MW_K='reheat_UA_MW_K',salt_flow_kg_s='salt_reheat_flow_kg_s'),['pressure_MPa','outlet_temperature_C']),
component('lp_turbine','Steam Expansion','reheat','lp',dict(shaft_MW='p_lp_shaft_MW'),['efficiency']),
component('open_feedwater_heater','Steam Feed Heater','condensate_pumped','heater',dict(bleed_flow_kg_s='mdot_bleed_kg_s',bleed_h_kJ_kg='h_hp_kJ_kg',mass_residual_kg_s='heater_mass_residual_kg_s',energy_residual_MW='heater_energy_residual_MW'),['pressure_MPa']),
component('condenser','Steam Condenser','lp','condensate',dict(rejected_MW='q_condenser_MW'),['temperature_C']),
component('condensate_pump','Steam Liquid Pump','condensate','condensate_pumped',dict(shaft_MW='p_condensate_shaft_MW',electric_MW='p_condensate_electric_MW'),['efficiency']),
component('feedwater_pump','Steam Liquid Pump','heater','feed',dict(shaft_MW='p_feedwater_shaft_MW',electric_MW='p_feedwater_electric_MW'),['efficiency']),
component('generator','Steam Generator Machine',aliases=dict(hp_shaft_MW='p_hp_shaft_MW',lp_shaft_MW='p_lp_shaft_MW',gross_MW='p_gross_MW',mechanical_loss_MW='q_mechanical_loss_MW',generator_loss_MW='q_generator_loss_MW'),facts=['mechanical_efficiency','generator_efficiency'])]
bindings = dict(enabled='matched_cycle_enabled',heat_available_MW='cycle_heat_available_MW',salt_flow_per_circuit='cycle_salt_flow_per_circuit',salt_circuit_count='cycle_salt_circuit_count',salt_hot_C='cycle_salt_hot_C',salt_return_C='cycle_salt_return_C',salt_cp_kJ_kgK='cycle_salt_cp_kJ_kgK',main_pressure_MPa='main_steam_generator.pressure_MPa',extraction_pressure_MPa='open_feedwater_heater.pressure_MPa',steam_temperature_C='main_steam_generator.outlet_temperature_C',reheat_temperature_C='reheater.outlet_temperature_C',condenser_temperature_C='condenser.temperature_C',eta_hp='hp_turbine.efficiency',eta_lp='lp_turbine.efficiency',eta_condensate_pump='condensate_pump.efficiency',eta_feedwater_pump='feedwater_pump.efficiency',eta_pump_motor='pump_motor_efficiency',eta_mechanical='generator.mechanical_efficiency',eta_generator='generator.generator_efficiency')
extra = f'''        // WI-073 matched state calculation; generic inactive before property evaluation.
        attribute matched_cycle_enabled : Real default 0.0;
        attribute pump_motor_efficiency : Real default 0.0;
        port pump_electric_in : ~'Electric Port';
        port cycle_rejection : 'Heat Duty Port';
        port main_salt_branch : 'Thermal Port';
        port reheat_salt_branch : 'Thermal Port';
'''
for val in list(bindings.values())[1:7]: extra+=f'        attribute {val} : Real default 0.0;\n'
for n in cycle_out: extra+=f'        attribute {n} : Real = matched_cycle.{n};\n'
for n in cycle_bool: extra+=f'        attribute matched_{n} : Boolean = matched_cycle.{n};\n'
extra+='\n'.join(components)+'\n'
extra+="        calc matched_cycle : 'Matched Steam Cycle' {\n"+'\n'.join(f'            in {n}_in = {bindings[n]};' for n in cycle_in)+'\n        }\n'
extra+="""        calc cycle_selection : 'Cycle Mode Selection' {
            in matched_enabled_in = matched_cycle_enabled;
            in legacy_eta_in = cycle.eta_th;
            in matched_eta_in = matched_cycle.eta_gross;
            in legacy_domain_product_in = cycle.domain_product;
        }
        attribute legacy_domain_applicable : Boolean = cycle_selection.legacy_domain_applicable;
        attribute matched_domain_applicable : Boolean = cycle_selection.matched_domain_applicable;
"""
for left,right in [('main_steam_generator.outlet','hp_turbine.inlet'),('hp_turbine.outlet','reheater.inlet'),('hp_turbine.outlet','open_feedwater_heater.bleed_in'),('reheater.outlet','lp_turbine.inlet'),('lp_turbine.outlet','condenser.inlet'),('condenser.outlet','condensate_pump.inlet'),('condensate_pump.outlet','open_feedwater_heater.inlet'),('open_feedwater_heater.outlet','feedwater_pump.inlet'),('feedwater_pump.outlet','main_steam_generator.inlet'),('hp_turbine.shaft_out','generator.hp_shaft'),('lp_turbine.shaft_out','generator.lp_shaft'),('main_salt_branch','main_steam_generator.salt'),('reheat_salt_branch','reheater.salt')]:extra+=f'        connect {left} to {right};\n'

sub=ROOT/'models/designs/generic_mfe/mfe_subsystems.sysml';s=sub.read_text();assert 'attribute matched_cycle_enabled' not in s
s=s.replace('    private import mfe_power_cycle::*;','    private import mfe_power_cycle::*;\n    private import mfe_matched_steam_cycle::*;\n    private import mfe_steam_cycle_components::*;')
s=s.replace('        attribute eta_th : Real = cycle.eta_th;', '        attribute eta_th : Real = cycle_selection.eta_selected;')
needle="        calc turbine_cost : 'Linear Power Cost' {";assert s.count(needle)==1;s=s.replace(needle,extra+needle)
cwbindings=dict(enabled='cooling_water_enabled',cycle_active='matched_cycle_mode',q_rejection_before_cooling_MW='cycle_rejection_MW',condenser_temperature_C='cycle_condenser_C',water_inlet_C='water_inlet_C',water_outlet_C='water_outlet_C',head_m='circulating_water_pump.head_m',eta_pump='circulating_water_pump.efficiency',eta_motor='circulating_water_pump.motor_efficiency')
cwextra=''
for a in ['cooling_water_enabled','matched_cycle_mode','cycle_rejection_MW','cycle_condenser_C','water_inlet_C','water_outlet_C']:cwextra+=f'        attribute {a} : Real default 0.0;\n'
for a in cw_out:cwextra+=f'        attribute {a} : Real = cooling_water.{a};\n'
for a in cw_bool:cwextra+=f'        attribute cooling_{a} : Boolean = cooling_water.{a};\n'
cwextra+="""        port cycle_heat_in : ~'Heat Duty Port';
        port environmental_heat : 'Heat Duty Port';
        port electric_in : ~'Electric Port';
        part circulating_water_pump : 'Circulating Water Pump' {
            :>> head_m default 0.0;
            :>> efficiency default 0.0;
            :>> motor_efficiency default 0.0;
            :>> flow_kg_s = 'Heat Rejection'::water_flow_kg_s;
            :>> shaft_MW = 'Heat Rejection'::p_cooling_pump_shaft_MW;
            :>> electric_MW = 'Heat Rejection'::p_cooling_pump_electric_MW;
        }
        calc cooling_water : 'Cooling Water Rejection' {
"""+'\n'.join(f'            in {n}_in = {cwbindings[n]};' for n in cw_in)+'\n        }\n'
s=s.replace("        calc heat_rejection_cost : 'Linear Power Cost' {",cwextra+"        calc heat_rejection_cost : 'Linear Power Cost' {");sub.write_text(s)

hp=ROOT/'models/library/structure/mfe_plant_systems.sysml';s=hp.read_text();needle='        attribute T_out : Real = primary_loop.T_out;';assert s.count(needle)==1
s=s.replace(needle,needle+f'''\n        // WI-073: expose existing salt-boundary scenario, not a new technology.
        attribute conversion_heat_MW : Real = equipment.conversion_heat_MW;
        attribute salt_flow_per_circuit : Real = equipment.salt_flow;
        attribute salt_circuit_count : Real = equipment.ihx_count;
        attribute salt_return_C : Real = equipment.salt_return_C;
        attribute salt_hot_C : Real = 465.0 {{ doc /* {DOC} Existing WI-067 equipment scenario hot state. */ }}
        attribute salt_cp_kJ_kgK : Real = 1.560 {{ doc /* {DOC} Existing WI-067 constant salt heat capacity1560J/kg/K, expressed kJ/kg/K. */ }}
''');hp.write_text(s)

plant=ROOT/'models/designs/generic_mfe/mfe_plant.sysml';s=plant.read_text();s=s.replace('    private import mfe_power_cycle::*;','    private import mfe_power_cycle::*;\n    private import mfe_matched_steam_cycle::*;')
needle='            :>> T_out = heat_transport.T_out;';assert s.count(needle)==1
s=s.replace(needle,needle+'\n'+'\n'.join(f'            :>> cycle_{dest} = heat_transport.{src};' for dest,src in [('heat_available_MW','conversion_heat_MW'),('salt_flow_per_circuit','salt_flow_per_circuit'),('salt_circuit_count','salt_circuit_count'),('salt_hot_C','salt_hot_C'),('salt_return_C','salt_return_C'),('salt_cp_kJ_kgK','salt_cp_kJ_kgK')]))
needle="        part heat_rejection : 'Heat Rejection' {";s=s.replace(needle,needle+'''\n            :>> matched_cycle_mode = turbine.matched_cycle_enabled;
            :>> cycle_rejection_MW = turbine.q_rejection_before_cooling_MW;
            :>> cycle_condenser_C = turbine.condenser.temperature_C;
''')
s=s.replace('            in p_pump_total_in = heat_transport.p_pump_total;','            in p_pump_total_in = heat_transport.p_pump_total;\n            in p_cycle_pumps_in = turbine.p_cycle_pumps_MW;\n            in p_cooling_water_in = heat_rejection.p_cooling_pump_electric_MW;')
needle='        connect turbine.gross_electric to electric_plant.gross_in;'
pos=s.index(needle);s=s[:pos]+'''        // WI-073 explicit cycle loads and rejection; scalar bindings execute these exchanges.
        connect electric_plant.recirculating to turbine.pump_electric_in;
        connect electric_plant.recirculating to turbine.condensate_pump.electric_in;
        connect electric_plant.recirculating to turbine.feedwater_pump.electric_in;
        connect electric_plant.recirculating to heat_rejection.electric_in;
        connect electric_plant.recirculating to heat_rejection.circulating_water_pump.electric_in;
        connect turbine.condenser.rejection to heat_rejection.cycle_heat_in;
        connect turbine.cycle_rejection to heat_rejection.cycle_heat_in;
'''+s[pos:]
for name,enabled,gap in [('matched_main_heat_direction','turbine.matched_cycle_enabled','turbine.main_min_gap_K'),('matched_reheat_heat_direction','turbine.matched_cycle_enabled','turbine.reheat_min_gap_K'),('cooling_water_heat_direction','heat_rejection.cooling_water_enabled','heat_rejection.condenser_water_gap_K')]:
    s=s.replace("        assert constraint cycle_domain_ok : 'Cycle Fit Domain' {",f"        assert constraint {name} : 'Active Steam Heat Direction' {{\n            in enabled_in = {enabled};\n            in gap_in = {gap};\n        }}\n        assert constraint cycle_domain_ok : 'Cycle Fit Domain' {{",1)
plant.write_text(s)

pb=ROOT/'models/library/analyses/mfe_power_balance.sysml';s=pb.read_text();s=s.replace('        in attribute p_pump_total_in : Real;','        in attribute p_pump_total_in : Real;\n        // WI-073 explicit water-cycle and cooling-water electricity, each counted once [MW].\n        in attribute p_cycle_pumps_in : Real default 0.0;\n        in attribute p_cooling_water_in : Real default 0.0;')
s=s.replace('            + p_wallplug_in;','            + p_wallplug_in + p_cycle_pumps_in + p_cooling_water_in;');pb.write_text(s)

inst=ROOT/'models/designs/stellarator_09/stellarator_plant.sysml';s=inst.read_text();needle='        part :>> turbine {';assert s.count(needle)==1
fact=lambda name,value:f'            :>> {name} = {value} {{ doc /* {DOC} Explicit selected reference assumption; no vendor/site qualification. */ }}\n'
facts=fact('matched_cycle_enabled','1.0')+fact('pump_motor_efficiency','0.95')
for part,attrs in {'main_steam_generator':{'pressure_MPa':6.2,'outlet_temperature_C':445.0},'reheater':{'pressure_MPa':0.8,'outlet_temperature_C':445.0},'open_feedwater_heater':{'pressure_MPa':0.8},'hp_turbine':{'efficiency':0.90},'lp_turbine':{'efficiency':0.90},'condenser':{'temperature_C':42.0},'condensate_pump':{'efficiency':0.8},'feedwater_pump':{'efficiency':0.8},'generator':{'mechanical_efficiency':0.99,'generator_efficiency':0.98}}.items():
    facts+=f'            part :>> {part} {{\n'+''.join(fact(n,v) for n,v in attrs.items())+'            }\n'
s=s.replace(needle,needle+'\n'+facts)
needle='        part :>> heat_rejection {';assert s.count(needle)==1
s=s.replace(needle,needle+'\n'+fact('cooling_water_enabled','1.0')+fact('water_inlet_C','25.0')+fact('water_outlet_C','35.0')+"            part :>> circulating_water_pump {\n"+fact('head_m','20.0')+fact('efficiency','0.80')+fact('motor_efficiency','0.95')+'            }\n');inst.write_text(s)

family=ROOT/'tests/model_families.py';s=family.read_text();s=s.replace('        "analyses/mfe_power_cycle.sysml",','        "analyses/mfe_matched_steam_cycle.sysml",\n        "structure/mfe_steam_cycle_components.sysml",\n        "analyses/mfe_power_cycle.sysml",');family.write_text(s)
(ITEM/'evidence/model-authoring/interfaces.json').write_text(json.dumps({'matched':{'inputs':cycle_in,'real':cycle_out,'boolean':cycle_bool},'cooling_water':{'inputs':cw_in,'real':cw_out,'boolean':cw_bool},'selection':{'inputs':select_in,'real':['eta_selected'],'boolean':['legacy_domain_applicable','matched_domain_applicable']}},indent=2)+'\n')
print('Authored canonical WI-073 model and family inventory; no generation performed.')
