"""Reproducible authoring of the reviewed native SysML equipment extension."""
from pathlib import Path
import json

ROOT=Path(__file__).resolve().parents[4]
DESIGN='work/active/WI-090_aries-integrated-equipment-and-costs/design.md'
HERE=ROOT/'exploration/aries_integrated'
doc=f'doc /* **Source**: {DESIGN}. **Ref**: accepted equations, variable-role table and assumptions E1-E10; source-basis.md linked there. **Basis**: [ASSUMED] conditional engineering estimate, USD2004. **Last Updated**: 2026-09-22. */'
definitions=[]
implementations={}

def definition(name, ins, outs, body):
    key=name.lower().replace(' ','_')
    definitions.append(f"    calc def '{name}' {{\n        {doc}\n"+''.join(f'        in attribute {i}_in : Real;\n' for i in ins)+''.join(f'        out attribute {o} : Real;\n' for o in outs)+'    }\n')
    implementations[key]=('"""Reviewed native calculation; emitted from WI-090 authoring record."""\n'
        'import math\nfrom aries_integrated.handwritten.integrated_equipment_costs.common import values, require, finish\nAUTO_IMPLEMENTED = False\n\n'
        f'def run_{key}(inputs):\n    v = values(inputs)\n'+''.join('    '+line+'\n' for line in body.splitlines())+f'    return finish({key!r}, result)\n')

definition('Selected Inventory Purchase',['quantity','reference_quantity','reference_cost','price_factor','mode'],['purchased_quantity','quantity_ratio','capital','source_budget','extrapolated'],'''require(v['quantity'] >= 0 and v['reference_quantity'] > 0 and v['reference_cost'] >= 0 and v['price_factor'] > 0, 'invalid selected inventory purchase')
require(v['mode'] in (0,1), 'purchase mode must be 0 scaled or 1 fixed')
r = v['quantity']/v['reference_quantity']
result = dict(purchased_quantity=v['quantity'], quantity_ratio=r, capital=v['reference_cost']*v['price_factor']*(r if v['mode']==0 else 1), source_budget=v['reference_cost'], extrapolated=float(r<.5 or r>1.5))''')
definition('Exchanger Area Conductance',['area','u'],['ua','area'],'''require(v['area'] >= 0 and v['u'] > 0, 'area must be nonnegative and U positive')
result = dict(ua=v['area']*v['u']/1e6,area=v['area'])''')
definition('Selected Flow Pump',['flow','reference_flow','reference_power','efficiency','reference_efficiency','mode','fixed_power'],['electric','hydraulic_supported','operating_flow','mode'],'''require(v['flow']>=0 and v['reference_flow']>0 and v['reference_power']>=0 and v['fixed_power']>=0, 'invalid pump flow/power')
require(0<v['efficiency']<=1 and 0<v['reference_efficiency']<=1, 'pump efficiency must be in (0,1]')
require(v['mode'] in (0,1), 'pump mode must be 0 proxy or 1 fixed-source')
p=v['fixed_power'] if v['mode']==1 else v['reference_power']*(v['flow']/v['reference_flow'])**3*v['reference_efficiency']/v['efficiency']
result=dict(electric=p,hydraulic_supported=0.,operating_flow=v['flow'],mode=v['mode'])''')
definition('Selected Stock Atoms',['stock_kg','atom_mass'],['atoms','stock_kg'],'''require(v['stock_kg']>=0 and v['atom_mass']>0, 'invalid selected stock')
result=dict(atoms=v['stock_kg']/v['atom_mass'],stock_kg=v['stock_kg'])''')
definition('Annual Selected Fuel',['stock_kg','atom_mass','decay','seconds','availability','burn','loss','exhaust','residence','annual_recovery','tritium_price'],['annual_burn','annual_loss','annual_decay','annual_recovery','annual_external','annual_cost','required_stock','breeding_supported'],'''require(all(x>=0 for x in v.values()), 'fuel inputs must be nonnegative')
require(v['atom_mass']>0 and v['seconds']>0 and 0<v['availability']<=1, 'invalid fuel constants/availability')
b=v['burn']*v['atom_mass']*v['seconds']*v['availability']
l=v['loss']*v['atom_mass']*v['seconds']*v['availability']
d=v['stock_kg']*v['decay']*v['seconds']
e=max(b+l+d-v['annual_recovery'],0.)
result=dict(annual_burn=b,annual_loss=l,annual_decay=d,annual_recovery=v['annual_recovery'],annual_external=e,annual_cost=e*v['tritium_price'],required_stock=v['exhaust']*v['atom_mass']*v['residence'],breeding_supported=0.)''')
definition('Replacement Events',['event_cost','life_fpy','availability','plant_years'],['event_cost','interval_years','event_count','lifetime_total','annual_reserve','first_event_year','last_event_year'],'''require(v['event_cost']>=0 and v['life_fpy']>0 and v['plant_years']>0 and 0<v['availability']<=1, 'invalid replacement schedule')
interval=v['life_fpy']/v['availability']
n=max(0,math.ceil(v['plant_years']/interval)-1)
require(n<1000000, 'replacement event count outside supported bound')
result=dict(event_cost=v['event_cost'],interval_years=interval,event_count=float(n),lifetime_total=n*v['event_cost'],annual_reserve=v['event_cost']/interval,first_event_year=interval if n else 0.,last_event_year=n*interval)''')
definition('Eight Amount Sum',[f'amount{i}' for i in range(1,9)],['total'],'''require(all(x>=0 for x in v.values()), 'amounts must be nonnegative')
result=dict(total=sum(v.values()))''')
definition('Scaled Amount',['amount','factor'],['amount'],'''require(v['amount']>=0 and v['factor']>=0, 'amount and factor must be nonnegative')
result=dict(amount=v['amount']*v['factor'])''')
definition('Comparison Difference',['left','right'],['difference'],'''result=dict(difference=v['left']-v['right'])''')
definition('Equipment Cost Ledger',['direct','source_direct','source_inclusive','indirect','contingency','owner','om','tritium','deuterium','consumables','replacement_reserve','replacement_total','net_power','availability','import_price','source_reactor_gap','source_core_excess','source_coil_excess','currency_year'],['direct','source_direct','source_inclusive','direct_difference','overnight','annual_operating','annual_replacement_reserve','lifetime_replacement','annual_export_mwh','annual_import_mwh','annual_import_cost','source_reactor_gap','source_core_excess','source_coil_excess','currency_year'],'''require(all(x>=0 for k,x in v.items() if k not in ('net_power','source_reactor_gap','source_core_excess','source_coil_excess')), 'cost inputs must be nonnegative')
require(0<v['availability']<=1, 'availability must be in (0,1]')
imp=max(-v['net_power'],0.)*8760*v['availability']
result=dict(direct=v['direct'],source_direct=v['source_direct'],source_inclusive=v['source_inclusive'],direct_difference=v['direct']-v['source_direct'],overnight=v['direct']+v['indirect']+v['contingency']+v['owner'],annual_operating=v['om']+v['tritium']+v['deuterium']+v['consumables']+imp*v['import_price'],annual_replacement_reserve=v['replacement_reserve'],lifetime_replacement=v['replacement_total'],annual_export_mwh=max(v['net_power'],0.)*8760*v['availability'],annual_import_mwh=imp,annual_import_cost=imp*v['import_price'],source_reactor_gap=v['source_reactor_gap'],source_core_excess=v['source_core_excess'],source_coil_excess=v['source_coil_excess'],currency_year=v['currency_year'])''')

lib=ROOT/'models/library/analyses/integrated_equipment_costs.sysml'
lib.write_text('package integrated_equipment_costs {\n    private import ScalarValues::*;\n'+''.join(definitions)+'}\n')
(ROOT/'models/library/structure/integrated_equipment_parts.sysml').write_text("package integrated_equipment_parts {\n    private import costed_component::*;\n    part def 'Selected Equipment' :> 'Costed Component' {\n        "+doc+'\n    }\n}\n')
out=HERE/'native_completions/equipment'
out.mkdir(exist_ok=True)
for name, content in implementations.items(): (out/(name+'_impl.py')).write_text(content)
(out/'common.py').write_text('''"""Finite scalar ABI helpers for reviewed equipment completions."""
import importlib
import math
def require(condition, message):
    if not condition: raise ValueError(message)
def values(inputs):
    data=inputs.model_dump()
    require(all(not isinstance(x,bool) and isinstance(x,(int,float)) and math.isfinite(x) for x in data.values()), 'inputs must be finite numeric scalars')
    return {k.removesuffix('_in'):v for k,v in data.items()}
def finish(module, values):
    require(all(math.isfinite(x) for x in values.values()), 'outputs must be finite')
    if len(values)==1: return next(iter(values.values()))
    mod=importlib.import_module('aries_integrated.schemas.'+module+'_output')
    schema=getattr(mod, '_'.join(x.capitalize() for x in module.split('_'))+'Output')
    require(set(schema.model_fields)==set(values), 'completion output contract mismatch')
    return next(iter(values.values())) if len(schema.model_fields)==1 else tuple(values[k] for k in schema.model_fields)
''')

parts=[]
manifest=[]
def part(name, lines, cas=None):
    heading=f"    part {name}"+(" : 'Selected Equipment'" if cas else '')+' {\n'
    parts.append(heading+'        '+doc+'\n'+(f'        :>> cas_code = "{cas}";\n' if cas else '')+'\n'.join('        '+line for line in lines)+'\n    }\n')
def attr(k,v): return f'attribute {k} : Real = {v};'
def calc(name, definition, bindings, outputs):
    return [f"calc {name} : '{definition}' {{"]+[f'    in {k} = {"aries_integrated_plant::"+v if "." in v and not v.replace(".","",1).isdigit() else v};' for k,v in bindings.items()]+['}']+[attr(k,f'{name}.{v}') for k,v in outputs.items()]
def purchase(name,q,q0,cost,cas,extra=None,quantity_key='selected_quantity'):
    if q==1. and q0==1. and not extra:
        lines=[attr(quantity_key,1.),attr('reference_cost',cost*1e6),attr('price_factor',1.)]
        lines+=calc('estimate','Scaled Amount',{'amount_in':'reference_cost','factor_in':'price_factor'},{'supplied_budget':'amount'})
        lines+=calc('purchase','Supplied Purchase Cost',{'purchase_cost_in':'supplied_budget','n_mod_in':quantity_key},{'estimated_cost':'cost'})
        lines+=[':>> capital_cost = purchase.cost;']
        part(name,lines,cas)
        manifest.append({'owner':name,'cas':cas,'quantity':quantity_key,'reference_quantity':q0,'reference_musd2004':cost,'cost_output':'cost','fixed_package':True})
        return
    lines=[] if isinstance(q,str) else [attr(quantity_key,q)]
    source=q if isinstance(q,str) else quantity_key
    lines += [attr('reference_quantity',q0),attr('reference_cost',cost*1e6),attr('price_factor',1.)]
    lines += calc('purchase','Selected Inventory Purchase',{'quantity_in':source,'reference_quantity_in':'reference_quantity','reference_cost_in':'reference_cost','price_factor_in':'price_factor','mode_in':'cost_accounts.estimate_mode'},{'inventory_quantity':'purchased_quantity','quantity_ratio':'quantity_ratio','estimated_cost':'capital','cost_extrapolated':'extrapolated'})
    lines += [':>> capital_cost = purchase.capital;']
    if extra:lines+=extra
    part(name,lines,cas)
    manifest.append({'owner':name,'cas':cas,'quantity':source,'reference_quantity':q0,'reference_musd2004':cost})
def sum_part(name, refs):
    assert len(refs)<=8
    part(name,calc('evaluate','Eight Amount Sum',{f'amount{i+1}_in':v for i,v in enumerate(refs+['0.0']*(8-len(refs)))},{'total':'total'}))

part('cost_accounts',[attr('estimate_mode',0.),attr('one_module',1.)])
part('cost_schedule',[attr('availability',.85),attr('plant_years',40.),attr('replacement_life_fpy',5.),attr('replacement_factor',1.),attr('lipb_makeup_fraction',.05)])
for b,m,p,rating in [('he',3261.,156.,1500.),('pbli',26860.,.01,1800.),('divertor',500.,10.,800.)]:
    extra=[attr('selected_area',50000.),attr('assumed_u',1000.)]+calc('evaluate','Exchanger Area Conductance',{'area_in':'selected_area','u_in':'assumed_u'},{'ua':'ua','area':'area'})
    purchase(b+'_hx','selected_area',50000.,388.838*.45/3,'22.2',extra)
    extra=[attr('selected_flow_capacity',m),attr('efficiency',.8),attr('reference_flow',m),attr('reference_power',p),attr('reference_efficiency',.8),attr('pump_mode',0.),attr('fixed_power',p)]
    extra+=calc('evaluate','Selected Flow Pump',{'flow_in':f'heat_exchangers.{b}_flow','reference_flow_in':'reference_flow','reference_power_in':'reference_power','efficiency_in':'efficiency','reference_efficiency_in':'reference_efficiency','mode_in':'pump_mode','fixed_power_in':'fixed_power'},{'electric':'electric','operating_flow':'operating_flow','hydraulic_supported':'hydraulic_supported'})
    extra+=calc('screen','Offered Capacity Screen',{'rating_in':'selected_flow_capacity','demand_in':'operating_flow','applicable_in':'true','conditions_supported_in':'true','demand_available_in':'true'},{'margin':'margin','evaluation_defined':'evaluation_defined'})
    extra += ["assert constraint capacity_ok : 'Offered Equipment Capacity' {",'    in defined_in = evaluation_defined;','    in margin_in = margin;','}']
    purchase(b+'_pump','selected_flow_capacity',m,388.838*.15/3,'22.2',extra)
    purchase(b+'_duty_equipment',b+'_capacity.selected_rating',rating,388.838*.25/3,'22.2')
purchase('primary_piping',1.,1.,388.838*.15,'22.2')
purchase('secondary_transport',1.,1.,85.933,'22.2')
for name,owner,ref,cost,cas in [('compressor_equipment','compressor',1600.,314.558*.25,'23'),('turbine_equipment','turbine',3500.,314.558*.4,'23'),('generator_equipment','generator',1800.,314.558*.15,'23'),('heat_rejection_equipment','rejection',2500.,56.086,'27'),('fuel_processing_equipment','fuel',3e22,16.590,'22.5')]:
    purchase(name,owner+'_capacity.selected_rating',ref,cost,cas)
purchase('conversion_services',1.,1.,314.558*.2,'23')
extra=[attr('selected_winding_mass',627200.),attr('selected_structure_mass',3465000.)]+calc('inventory','Eight Amount Sum',{'amount1_in':'selected_winding_mass','amount2_in':'selected_structure_mass',**{f'amount{i}_in':'0.0' for i in range(3,9)}},{'selected_mass':'total'})
purchase('magnet_inventory','selected_mass',4092200.,204.208,'22.1.3',extra)
purchase('vf_coils',1.,1.,13.358,'22.1.3')
purchase('divertor_inventory',1.,1.,5.318,'22.1.3')
purchase('blanket_inventory',662500.,662500.,59.347,'22.1.1',quantity_key='selected_mass')
extra=[attr('selected_shield_mass',3280000.),attr('selected_manifold_mass',1305000.)]+calc('inventory','Eight Amount Sum',{'amount1_in':'selected_shield_mass','amount2_in':'selected_manifold_mass',**{f'amount{i}_in':'0.0' for i in range(3,9)}},{'selected_mass':'total'})
purchase('shield_inventory','selected_mass',4585000.,228.627,'22.1.2',extra)
purchase('primary_support',2909000.,2909000.,73.126,'22.1.5',quantity_key='selected_mass')
extra=[attr('selected_vessel_mass',1440000.),attr('selected_cryostat_mass',1333000.)]+calc('inventory','Eight Amount Sum',{'amount1_in':'selected_vessel_mass','amount2_in':'selected_cryostat_mass',**{f'amount{i}_in':'0.0' for i in range(3,9)}},{'selected_mass':'total'})
purchase('vacuum_equipment','selected_mass',2773000.,137.135,'22.1.6',extra)
for name,cost,cas in [('site_land',12.929,'20'),('facilities',336.133,'21'),('heating_equipment',66.427,'22.1.4'),('magnet_power_supplies',70.624,'22.1.7'),('impurity_control',6.561,'22.1.8'),('auxiliary_cooling',3.735,'22.3'),('waste_equipment',6.655,'22.4'),('fuel_services',38.689,'22.5'),('other_reactor_equipment',60.723,'22.6'),('instrumentation_control',44.558,'22.7'),('unallocated_source_scope',28.396,'22'),('electrical_equipment',138.764,'24'),('miscellaneous_equipment',70.958,'25')]:
    purchase(name,1.,1.,cost,cas)
extra=[attr('selected_core_mass',3532000.),attr('external_mass_factor',2.5)]+calc('inventory','Scaled Amount',{'amount_in':'selected_core_mass','factor_in':'external_mass_factor'},{'total_mass':'amount'})
purchase('lipb_inventory','total_mass',8830000.,151.327,'26',extra)

stock=[attr('selected_tritium_kg',10.),attr('process_residence_s',1000.),attr('annual_recovery_kg',0.),attr('tritium_price',30e6),attr('deuterium_price',1000.),attr('deuterium_atom_kg',3.3435837724e-27)]
stock+=calc('atoms','Selected Stock Atoms',{'stock_kg_in':'selected_tritium_kg','atom_mass_in':'fuel.tritium_atom_kg'},{'selected_tritium_atoms':'atoms'})
stock+=calc('purchase','Scaled Amount',{'amount_in':'selected_tritium_kg','factor_in':'tritium_price'},{'initial_stock_cost':'amount'})+[':>> capital_cost = purchase.amount;']
stock+=calc('annual','Annual Selected Fuel',{'stock_kg_in':'selected_tritium_kg','atom_mass_in':'fuel.tritium_atom_kg','decay_in':'fuel.decay_constant_s','seconds_in':'fuel.seconds_per_year','availability_in':'cost_schedule.availability','burn_in':'fuel.burn_rate','loss_in':'fuel.loss_rate','exhaust_in':'fuel.exhaust_rate','residence_in':'process_residence_s','annual_recovery_in':'annual_recovery_kg','tritium_price_in':'tritium_price'},{k:k for k in ['annual_burn','annual_loss','annual_decay','annual_recovery','annual_external','annual_cost','required_stock','breeding_supported']})
stock+=calc('screen','Offered Capacity Screen',{'rating_in':'selected_tritium_kg','demand_in':'required_stock','applicable_in':'true','conditions_supported_in':'true','demand_available_in':'true'},{'margin':'margin','evaluation_defined':'evaluation_defined'})+["assert constraint capacity_ok : 'Offered Equipment Capacity' {",'    in defined_in = evaluation_defined;','    in margin_in = margin;','}']
stock+=calc('deuterium_rate','Scaled Amount',{'amount_in':'deuterium_atom_kg','factor_in':'deuterium_price'},{'deuterium_per_reaction':'amount'})
stock+=calc('deuterium','DT Fuel Cost',{'p_fus':'source.selected_power','n_mod_in':'cost_accounts.one_module','availability_in':'cost_schedule.availability','cost_per_rxn':'deuterium_per_reaction','q_eff':'fuel.reaction_energy_mev','mev_to_joules_in':'fuel.mev_joules','burn_fraction_in':'fuel.pass_burn_fraction','fuel_recovery_in':'fuel.exhaust_recovery'},{'annual_deuterium_cost':'annual_fuel'})
part('fuel_inventory',stock,'26.fuel')

sourcevals=[12.929,336.133,1538.817,314.558,138.764,70.958,151.327,56.086]
part('source_budget',[attr(f'account_{i+1}',x*1e6) for i,x in enumerate(sourcevals)]+[attr('inclusive_multiplier',1.93)]+calc('evaluate','Disjoint Capital Budget',{**{f'account_{i+1}_in':f'account_{i+1}' for i in range(8)},'inclusive_multiplier_in':'inclusive_multiplier'},{'direct_total':'direct_total','inclusive_capital':'inclusive_capital'}))
# Source-reference reconciliation is separate from selected equipment accounting.
sum_part('source_reactor_children',['source_reconciliation.core_parent','474771000.0','3735000.0','6655000.0','source_reconciliation.fuel_parent','60723000.0','44558000.0'])
sum_part('source_core_children_first',['59347000.0','228627000.0','source_reconciliation.coil_parent','66427000.0','73126000.0','137135000.0','70624000.0','6561000.0'])
sum_part('source_coil_children',[str(x*1e6) for x in [115.960,13.358,5.318,93.535]])
sum_part('source_fuel_children',[str(x*1e6) for x in [14.134,16.590,7.067,3.353,7.067,7.067]])
source_lines=[attr('core_parent',864.700e6),attr('coil_parent',222.884e6),attr('fuel_parent',55.279e6)]
for key,left,right in [('reactor_gap','source_budget.account_3','source_reactor_children.total'),('core_excess','source_core_children_first.total','core_parent'),('coil_excess','source_coil_children.total','coil_parent'),('fuel_gap','fuel_parent','source_fuel_children.total')]:
    source_lines+=calc(key+'_calc','Comparison Difference',{'left_in':left,'right_in':right},{key:'difference'})
part('source_reconciliation',source_lines)
sum_part('known_dry_inventory',['magnet_inventory.selected_mass','blanket_inventory.selected_mass','shield_inventory.selected_mass','vacuum_equipment.selected_mass','primary_support.selected_mass'])
part('inventory_comparison',[attr('source_dry_core_mass',13688000.),attr('vf_mass_available',0.)]+calc('evaluate','Comparison Difference',{'left_in':'known_dry_inventory.total','right_in':'source_dry_core_mass'},{'known_mass_minus_source':'difference'})+calc('support','Scaled Amount',{'amount_in':'vf_mass_available','factor_in':'1.0'},{'vf_mass_availability':'amount'}))
part('lipb_comparison',[attr('source_unit_rate',17.1)]+calc('price','Scaled Amount',{'amount_in':'lipb_inventory.total_mass','factor_in':'source_unit_rate'},{'material_price':'amount'})+calc('evaluate','Comparison Difference',{'left_in':'material_price','right_in':'source_budget.account_7'},{'material_minus_source':'difference'}))
source_replace=[attr('event_cost',75e6),attr('events',13.),attr('event_mass',842000.),attr('printed_lifetime_cost',966e6)]
source_replace+=calc('cost','Scaled Amount',{'amount_in':'event_cost','factor_in':'events'},{'rounded_lifetime_cost':'amount'})
source_replace+=calc('mass','Scaled Amount',{'amount_in':'event_mass','factor_in':'events'},{'lifetime_mass':'amount'})
source_replace+=calc('evaluate','Comparison Difference',{'left_in':'rounded_lifetime_cost','right_in':'printed_lifetime_cost'},{'rounded_minus_printed':'difference'})
part('source_replacement_comparison',source_replace)
core=['blanket_inventory','shield_inventory','magnet_inventory','vf_coils','divertor_inventory','heating_equipment','primary_support','vacuum_equipment']
sum_part('core_first',[x+'.capital_cost' for x in core])
sum_part('core_cost',['core_first.total','magnet_power_supplies.capital_cost','impurity_control.capital_cost'])
sum_part('primary_heat_cost',[x+'.capital_cost' for x in ['he_hx','pbli_hx','divertor_hx','he_pump','pbli_pump','divertor_pump','primary_piping']])
sum_part('heat_transport_cost',['primary_heat_cost.total']+[b+'_duty_equipment.capital_cost' for b in ['he','pbli','divertor']]+['secondary_transport.capital_cost'])
sum_part('fuel_equipment',['fuel_processing_equipment.capital_cost','fuel_services.capital_cost'])
sum_part('reactor_cost',['core_cost.total','heat_transport_cost.total','auxiliary_cooling.capital_cost','waste_equipment.capital_cost','fuel_equipment.total','other_reactor_equipment.capital_cost','instrumentation_control.capital_cost','unallocated_source_scope.capital_cost'])
sum_part('conversion_equipment',[x+'.capital_cost' for x in ['compressor_equipment','turbine_equipment','generator_equipment','conversion_services']])
sum_part('direct_source_scope',['site_land.capital_cost','facilities.capital_cost','reactor_cost.total','conversion_equipment.total','electrical_equipment.capital_cost','miscellaneous_equipment.capital_cost','lipb_inventory.capital_cost','heat_rejection_equipment.capital_cost'])
sum_part('direct_cost',['direct_source_scope.total','fuel_inventory.capital_cost'])
part('indirect_cost',[attr('fraction',.2)]+calc('evaluate','Indirect Cost',{'indirect_fraction_in':'fraction','direct_cost':'direct_cost.total','construction_time':'6.0','reference_construction_time':'6.0'},{'amount':'cost'}))
sum_part('contingency_basis',['direct_cost.total','indirect_cost.amount'])
part('contingency',[attr('fraction',.2)]+calc('evaluate','Contingency Cost',{'contingency_rate_in':'fraction','direct_subtotal':'contingency_basis.total'},{'amount':'cost'}))
part('owner_commissioning',[attr('fraction',.05)]+calc('evaluate','Scaled Amount',{'amount_in':'direct_cost.total','factor_in':'fraction'},{'amount':'amount'}))
part('annual_om',[attr('selected_amount',70e6)]+calc('evaluate','Annual OM Cost',{'om_ref':'0.0','p_net':'1000.0','n_mod_in':'1.0','ref_net_power':'1000.0','alpha':'0.5','om_direct':'selected_amount'},{'amount':'annual_om'}))
part('replacement_lipb',calc('evaluate','Scaled Amount',{'amount_in':'lipb_inventory.capital_cost','factor_in':'cost_schedule.lipb_makeup_fraction'},{'amount':'amount'}))
sum_part('replacement_scope',['blanket_inventory.capital_cost','divertor_inventory.capital_cost','replacement_lipb.amount'])
part('replacement_price',calc('evaluate','Scaled Amount',{'amount_in':'replacement_scope.total','factor_in':'cost_schedule.replacement_factor'},{'amount':'amount'}))
part('replacement',calc('evaluate','Replacement Events',{'event_cost_in':'replacement_price.amount','life_fpy_in':'cost_schedule.replacement_life_fpy','availability_in':'cost_schedule.availability','plant_years_in':'cost_schedule.plant_years'},{x:x for x in ['event_cost','interval_years','event_count','lifetime_total','annual_reserve','first_event_year','last_event_year']}))
ledger=[attr('consumables',5e6),attr('import_price',50.)]
ledger+=calc('evaluate','Equipment Cost Ledger',{'direct_in':'direct_cost.total','source_direct_in':'source_budget.direct_total','source_inclusive_in':'source_budget.inclusive_capital','indirect_in':'indirect_cost.amount','contingency_in':'contingency.amount','owner_in':'owner_commissioning.amount','om_in':'annual_om.amount','tritium_in':'fuel_inventory.annual_cost','deuterium_in':'fuel_inventory.annual_deuterium_cost','consumables_in':'consumables','replacement_reserve_in':'replacement.annual_reserve','replacement_total_in':'replacement.lifetime_total','net_power_in':'plant_ledger.net_electric','availability_in':'cost_schedule.availability','import_price_in':'import_price','source_reactor_gap_in':'source_reconciliation.reactor_gap','source_core_excess_in':'source_reconciliation.core_excess','source_coil_excess_in':'source_reconciliation.coil_excess','currency_year_in':'2004.0'},{x:x for x in ['direct','source_direct','source_inclusive','direct_difference','overnight','annual_operating','annual_replacement_reserve','lifetime_replacement','annual_export_mwh','annual_import_mwh','annual_import_cost','source_reactor_gap','source_core_excess','source_coil_excess','currency_year']})
part('cost_ledger',ledger)

plant=ROOT/'models/designs/aries_cs_integrated/plant.sysml'
text=plant.read_text()
marker='    // WI-090 selected inventory and cost ownership'
if marker in text:text=text.split(marker)[0]+'}\n'
text=text.replace('    private import ScalarValues::*;','    private import ScalarValues::*;\n    private import integrated_equipment_costs::*;\n    private import integrated_equipment_parts::*;\n    private import mfe_account_costs::*;\n    private import source_budget_accounting::*;',1) if 'private import integrated_equipment_costs' not in text else text
for b,p in [('he',156.),('pbli',.01),('divertor',10.)]:
    text=text.replace(f'attribute {b}_pump : Real = {p};',f'attribute {b}_pump : Real = aries_integrated_plant::{b}_pump.electric;')
    text=text.replace(f'attribute {b}_ua : Real = 50.0;',f'attribute {b}_ua : Real = {b}_hx.ua;')
text=text.replace('        attribute dormant_inventory_atoms : Real = 0.0;\n','')
text=text.replace('in I_total_in = dormant_inventory_atoms;','in I_total_in = fuel_inventory.selected_tritium_atoms;')
text=text.replace('        attribute loss_rate : Real = evaluate.loss_rate;','        attribute loss_rate : Real = evaluate.loss_rate;\n        attribute tbr_required : Real = evaluate.tbr_required;') if 'attribute tbr_required' not in text else text
text=text.replace('= he_pump.electric;', '= aries_integrated_plant::he_pump.electric;').replace('= pbli_pump.electric;', '= aries_integrated_plant::pbli_pump.electric;').replace('= divertor_pump.electric;', '= aries_integrated_plant::divertor_pump.electric;')
text=text.rstrip()[:-1]+marker+'\n'+''.join(parts)+'}\n'
plant.write_text(text)
(Path(__file__).parent/'account-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
print(f'Wrote {len(definitions)} definitions, {len(parts)} occurrences and {len(manifest)} priced inventory owners.')
