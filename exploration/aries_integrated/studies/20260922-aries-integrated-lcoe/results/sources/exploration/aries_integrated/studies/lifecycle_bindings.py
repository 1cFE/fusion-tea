"""WI-091 independent oracle bindings; graph outputs never feed the checker."""
from . import lifecycle_oracle
from .equipment_bindings import P, out

# Generated account output -> independent dated-cashflow result.
FIELDS = {
    'noncapital_annual':'noncapital_annual','financed_capital':'financed_capital',
    'idc':'idc','annual_capital':'annual_capital','annual_energy':'annual_energy',
    'lifetime_energy':'lifetime_energy','pv_energy':'pv_energy',
    'pv_operating':'pv_annual_operating','pv_supply':'pv_supply_service',
    'pv_replacement':'pv_replacement','pv_other_overhaul':'pv_other_overhaul',
    'gross_terminal':'gross_terminal_amount','salvage':'salvage_amount',
    'pv_terminal_gross':'pv_decommissioning','pv_salvage':'pv_salvage',
    'pv_terminal_net':'pv_terminal','other_overhaul_cost':'other_overhaul_amount',
    'other_overhaul_occurs':'other_overhaul_occurs','pv_total_cost':'pv_total',
    'lcoe_sum':'lcoe','capital_lcoe':'lcoe_capital','om_lcoe':'lcoe_om',
    'tritium_lcoe':'lcoe_tritium','deuterium_lcoe':'lcoe_deuterium',
    'consumables_lcoe':'lcoe_consumables','imports_lcoe':'lcoe_import',
    'supply_lcoe':'lcoe_supply_service','replacement_lcoe':'lcoe_replacement',
    'other_overhaul_lcoe':'lcoe_other_overhaul','terminal_lcoe':'lcoe_decommissioning',
    'salvage_lcoe':'lcoe_salvage','gross_makeup':'gross_new_tritium_requirement',
    'new_feed':'additional_feed','external_shortfall':'external_tritium',
    'curtailed_feed':'curtailed_feed',
}
FLAGS={'supply_supported':0.,'breeding_supported':0.,'financial_defined':1.,'currency_year':2004.,'real_convention':1.}


def evaluate(point, independently_calculated):
    get=lambda owner,field:point[P+owner+'__'+field]
    val=lambda owner,field,calc='evaluate':independently_calculated[out(owner,calc,field)]
    if get('source_finance','construction_years') != 0:
        raise ValueError('already-financed source capital permits exactly zero construction duration')
    shared=dict(years=get('cost_schedule','plant_years'),availability=get('cost_schedule','availability'),
        discount_rate=get('finance','discount_rate'),annual_operating=val('cost_ledger','annual_operating'),
        annual_om=val('annual_om','annual_om'),annual_tritium=val('fuel_inventory','annual_cost','annual'),
        annual_deuterium=val('fuel_inventory','annual_fuel','deuterium'),
        annual_consumables=get('cost_ledger','consumables'),annual_import=val('cost_ledger','annual_import_cost'),
        supply_service_annual=get('finance','supply_service_annual'),
        replacement_interval=val('replacement','interval_years'),replacement_count=val('replacement','event_count'),
        replacement_event_cost=val('replacement','event_cost'),terminal_fraction=get('finance','terminal_fraction'),
        salvage_fraction=get('finance','salvage_fraction'),other_overhaul_fraction=get('finance','other_overhaul_fraction'),
        other_overhaul_year=get('finance','other_overhaul_year'),
        annual_burn_kg=val('fuel_inventory','annual_burn','annual'),annual_loss_kg=val('fuel_inventory','annual_loss','annual'),
        annual_decay_kg=val('fuel_inventory','annual_decay','annual'),new_feed_kg=get('fuel_inventory','annual_recovery_kg'))
    result={}
    for name in ('lifecycle','source_lifecycle'):
        source=name.startswith('source_')
        power=get('source_finance','net_power') if source else val('plant_ledger','net_electric')
        energy=8760*power*shared['availability'] if source else val('cost_ledger','annual_export_mwh')
        values=lifecycle_oracle.evaluate(**shared,
            overnight=val('source_budget','inclusive_capital') if source else val('cost_ledger','overnight'),
            net_power=power,annual_energy=energy,
            construction_years=0. if source else get('finance','construction_years'))
        values['annual_energy']=energy
        # Published PV salvage is a positive magnitude; its LCOE contribution is negative.
        values['pv_salvage']=-values['pv_salvage']
        result.update({out(name+'_accounts','evaluate',field):values[ref] for field,ref in FIELDS.items()})
        result.update({out(name+'_accounts','evaluate',field):value for field,value in FLAGS.items()})
        result[out(name+'_price','evaluate','lcoe')]=values['lcoe']
        if not source:
            result[out('operating_levelization','evaluate','crf')]=values['crf']
            result[out('operating_levelization','evaluate','levelized')]=shared['annual_operating']
        else:result[out('source_finance_energy','evaluate','annual_energy')]=energy
    result[out('source_finance','boundary','years')]=0.
    return result


def comparison_catalog():
    return [out(owner+'_accounts','evaluate',field) for owner in ('lifecycle','source_lifecycle') for field in (*FIELDS,*FLAGS)]+[
        out(owner+'_price','evaluate','lcoe') for owner in ('lifecycle','source_lifecycle')]+[
        out('operating_levelization','evaluate',field) for field in ('crf','levelized')]+[
        out('source_finance_energy','evaluate','annual_energy'),out('source_finance','boundary','years')]
