"""Reproduce WI-091's reviewed additive native lifecycle definitions and bindings."""
from pathlib import Path
ROOT=Path(__file__).resolve().parents[4]
HERE=ROOT/'exploration/aries_integrated'
DOC='doc /* **Source**: work/active/WI-091_aries-integrated-lifecycle-cost/design.md. **Ref**: reviewed financial convention, roles and F1-F9 assumptions; work/orchestration/goals/aries-integrated-lcoe/evidence/source-boundary.md. **Basis**: conditional real USD2004 dated lifecycle accounts; assumptions are not scientific qualification. **Last Updated**: 2026-09-22. */'
INS=['overnight','net_power','annual_energy','annual_operating','om','tritium','deuterium','consumables','imports','supply_service','crf','discount','construction_years','plant_years','availability','event_cost','interval_years','event_count','terminal_fraction','salvage_fraction','other_overhaul_fraction','other_overhaul_year','annual_burn','annual_loss','annual_decay','annual_feed','external_shortfall']
OUTS=['noncapital_annual','financed_capital','idc','annual_capital','annual_energy','lifetime_energy','pv_energy','pv_operating','pv_supply','pv_replacement','pv_other_overhaul','gross_terminal','salvage','pv_terminal_gross','pv_salvage','pv_terminal_net','other_overhaul_cost','other_overhaul_occurs','pv_total_cost','lcoe_sum','capital_lcoe','om_lcoe','tritium_lcoe','deuterium_lcoe','consumables_lcoe','imports_lcoe','supply_lcoe','replacement_lcoe','other_overhaul_lcoe','terminal_lcoe','salvage_lcoe','gross_makeup','new_feed','external_shortfall','curtailed_feed','supply_supported','breeding_supported','financial_defined','currency_year','real_convention']
def definition(name,ins,outs,expressions=None):
    return "    calc def '"+name+"' {\n        "+DOC+'\n'+''.join(f'        in attribute {x}_in : Real;\n' for x in ins)+''.join(f'        out attribute {x} : Real'+(' = '+expressions[x] if expressions else '')+';\n' for x in outs)+'    }\n'
text='package integrated_lifecycle_costs {\n    private import ScalarValues::*;\n'
text+=definition('Lifecycle Cashflow Accounts',INS,OUTS)
text+=definition('Already Financed Duration',['years'],['years'])
text+=definition('Supplied Annual Energy',['net_power','availability'],['annual_energy'],{'annual_energy':'8760.0 * net_power_in * availability_in'})
(ROOT/'models/library/analyses/integrated_lifecycle_costs.sysml').write_text(text+'}\n')
completion=HERE/'native_completions/lifecycle';completion.mkdir(parents=True,exist_ok=True)
(completion/'lifecycle_cashflow_accounts_impl.py').write_text('''"""Reviewed WI-091 real cashflow accounts; production native completion, not oracle.
Source: models/library/analyses/integrated_lifecycle_costs.sysml.
Ref: work/active/WI-091_aries-integrated-lifecycle-cost/design.md.
"""
import math
from aries_integrated.handwritten.integrated_equipment_costs.common import values, require, finish
AUTO_IMPLEMENTED = False

def run_lifecycle_cashflow_accounts(inputs):
    v=values(inputs)
    r=v['discount']; n=v['plant_years']; crf=v['crf']; energy=v['annual_energy']
    require(0 <= r <= 1, 'financial discount must be real in [0,1]')
    require(n>0 and n.is_integer(), 'financial life must be positive integer calendar years')
    require(v['construction_years']>=0 and 0<v['availability']<=1, 'invalid financial construction/availability')
    require(v['net_power']>0 and energy>0, 'LCOE undefined for nonpositive net electricity')
    require(all(v[k]>=0 for k in v if k not in ('net_power',)), 'financial accounts must be nonnegative inputs')
    require(crf>0 and math.isclose(crf,1/n if r==0 else r/-math.expm1(-n*math.log1p(r)),rel_tol=1e-12), 'inconsistent capital recovery factor')
    require(math.isclose(energy,8760*v['net_power']*v['availability'],rel_tol=1e-12), 'inconsistent annual net electricity')
    operating=sum(v[k] for k in ('om','tritium','deuterium','consumables','imports'))
    require(math.isclose(v['annual_operating'],operating,rel_tol=1e-12,abs_tol=1e-7), 'annual accounts do not reconcile')
    tau=v['interval_years']; count=v['event_count']
    require(tau>0 and count.is_integer() and 0<=count<1000000, 'invalid replacement interval/count')
    require(count==max(0,math.ceil(n/tau)-1), 'replacement count inconsistent with horizon')
    require(v['other_overhaul_year']>0, 'other overhaul year must be positive')
    weight=lambda t: math.exp(-t*math.log1p(r))
    capital=v['overnight']; financed=capital/weight(v['construction_years']/2)
    pv_rep=math.fsum(v['event_cost']*weight(k*tau) for k in range(1,int(count)+1))
    occurs=float(v['other_overhaul_year']<n)
    other=capital*v['other_overhaul_fraction']*occurs
    pv_other=other*weight(v['other_overhaul_year'])
    gross=capital*v['terminal_fraction']; salvage=capital*v['salvage_fraction']
    pv_gross=gross*weight(n); pv_salvage=salvage*weight(n)
    pv_operating=operating/crf; pv_supply=v['supply_service']/crf
    pv_energy=energy/crf
    noncapital=operating+v['supply_service']+crf*(pv_rep+pv_other+pv_gross-pv_salvage)
    total=financed+pv_operating+pv_supply+pv_rep+pv_other+pv_gross-pv_salvage
    makeup=sum(v[k] for k in ('annual_burn','annual_loss','annual_decay'))
    shortfall=max(makeup-v['annual_feed'],0.)
    require(math.isclose(v['external_shortfall'],shortfall,rel_tol=1e-12,abs_tol=1e-12),'fuel feed boundary does not reconcile')
    result=dict(noncapital_annual=noncapital,financed_capital=financed,idc=financed-capital,annual_capital=financed*crf,
        annual_energy=energy,lifetime_energy=energy*n,pv_energy=pv_energy,pv_operating=pv_operating,pv_supply=pv_supply,
        pv_replacement=pv_rep,pv_other_overhaul=pv_other,gross_terminal=gross,salvage=salvage,pv_terminal_gross=pv_gross,
        pv_salvage=pv_salvage,pv_terminal_net=pv_gross-pv_salvage,other_overhaul_cost=other,other_overhaul_occurs=occurs,
        pv_total_cost=total,lcoe_sum=total/pv_energy,capital_lcoe=financed/pv_energy,
        supply_lcoe=v['supply_service']/energy,replacement_lcoe=pv_rep/pv_energy,other_overhaul_lcoe=pv_other/pv_energy,
        terminal_lcoe=pv_gross/pv_energy,salvage_lcoe=-pv_salvage/pv_energy,gross_makeup=makeup,new_feed=v['annual_feed'],
        external_shortfall=shortfall,curtailed_feed=max(v['annual_feed']-makeup,0.),supply_supported=0.,breeding_supported=0.,
        financial_defined=1.,currency_year=2004.,real_convention=1.)
    for key in ('om','tritium','deuterium','consumables','imports'):
        result[key+'_lcoe']=v[key]/energy
    return finish('lifecycle_cashflow_accounts',result)
''')
(completion/'already_financed_duration_impl.py').write_text('"""Guard the supplied already-financed capital boundary; no second IDC."""\nfrom aries_integrated.handwritten.integrated_equipment_costs.common import values, require, finish\nAUTO_IMPLEMENTED = False\n\ndef run_already_financed_duration(inputs):\n    v=values(inputs)\n    require(v[\'years\']==0., \'already-financed capital requires exactly zero additional construction years\')\n    return finish(\'already_financed_duration\',dict(years=0.))\n')
plant=ROOT/'models/designs/aries_cs_integrated/plant.sysml';text=plant.read_text()
assert '    part finance {' not in text, 'authoring script is only run once per baseline'
text=text.replace('    private import ScalarValues::*;','    private import ScalarValues::*;\n    private import integrated_lifecycle_costs::*;\n    private import mfe_lcoe_dcf::*;',1)
text=text.replace('        attribute annual_recovery_kg : Real = 0.0;', '        // New usable T feed [kg/calendar year], excluding already recycled exhaust; no breeding qualification.\n        attribute annual_recovery_kg : Real = 0.0;')
parts=[]
def part(name,lines):
    parts.append('    part '+name+' {\n        '+DOC+'\n'+''.join('        '+x+'\n' for x in lines)+'    }\n')
def attrs(vals):return [f'attribute {k} : Real = {v};' for k,v in vals.items()]
def calc(name,definition,bindings,outs):return ["calc "+name+" : '"+definition+"' {"]+['    in '+k+' = '+v+';' for k,v in bindings.items()]+['}']+[f'attribute {alias} : Real = {name}.{out};' for alias,out in outs.items()]
q=lambda x:x if x=='0.0' else 'aries_integrated_plant::'+x
part('finance',attrs(dict(discount_rate=.05,construction_years=6.,terminal_fraction=.1,salvage_fraction=.02,other_overhaul_fraction=.05,other_overhaul_year=20.,supply_service_annual=0.)))
part('source_finance',attrs(dict(net_power=1000.,construction_years=0.))+calc('boundary','Already Financed Duration',dict(years_in='construction_years'),dict(validated_years='years')))
part('operating_levelization',calc('evaluate','Levelized Annual Cost',dict(annual_cost=q('cost_ledger.annual_operating'),interest_rate=q('finance.discount_rate'),inflation_rate_in='0.0',operational_years_in=q('cost_schedule.plant_years'),project_time='0.0'),dict(factor='crf',annual='levelized')))
part('source_finance_energy',calc('evaluate','Supplied Annual Energy',dict(net_power_in=q('source_finance.net_power'),availability_in=q('cost_schedule.availability')),dict(annual_energy='annual_energy')))
bindings=dict(overnight='cost_ledger.overnight',net_power='plant_ledger.net_electric',annual_energy='cost_ledger.annual_export_mwh',annual_operating='cost_ledger.annual_operating',om='annual_om.amount',tritium='fuel_inventory.annual_cost',deuterium='fuel_inventory.annual_deuterium_cost',consumables='cost_ledger.consumables',imports='cost_ledger.annual_import_cost',supply_service='finance.supply_service_annual',crf='operating_levelization.factor',discount='finance.discount_rate',construction_years='finance.construction_years',plant_years='cost_schedule.plant_years',availability='cost_schedule.availability',event_cost='replacement.event_cost',interval_years='replacement.interval_years',event_count='replacement.event_count',terminal_fraction='finance.terminal_fraction',salvage_fraction='finance.salvage_fraction',other_overhaul_fraction='finance.other_overhaul_fraction',other_overhaul_year='finance.other_overhaul_year',annual_burn='fuel_inventory.annual_burn',annual_loss='fuel_inventory.annual_loss',annual_decay='fuel_inventory.annual_decay',annual_feed='fuel_inventory.annual_recovery_kg',external_shortfall='fuel_inventory.annual_external')
for prefix in ('lifecycle','source_lifecycle'):
    b=bindings.copy()
    if prefix=='source_lifecycle':b.update(overnight='source_budget.inclusive_capital',net_power='source_finance.net_power',annual_energy='source_finance_energy.annual_energy',construction_years='source_finance.validated_years')
    part(prefix+'_accounts',calc('evaluate','Lifecycle Cashflow Accounts',{k+'_in':q(v) for k,v in b.items()},{x:x for x in OUTS}))
    part(prefix+'_price',calc('evaluate','LCOE DCF',dict(total_capital_in=q(b['overnight']),annual_om_in=q(prefix+'_accounts.noncapital_annual'),net_electric_mw=q(b['net_power']),availability_in=q('cost_schedule.availability'),discount_rate_in=q('finance.discount_rate'),construction_years_in=q(b['construction_years']),operational_years_in=q('cost_schedule.plant_years')),dict(lcoe='lcoe')))
assert text.endswith('}\n');plant.write_text(text[:-2]+''.join(parts)+'}\n')
