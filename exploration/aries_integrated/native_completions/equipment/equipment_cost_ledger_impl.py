"""Reviewed native calculation; emitted from WI-090 authoring record."""
import math
from aries_integrated.handwritten.integrated_equipment_costs.common import values, require, finish
AUTO_IMPLEMENTED = False

def run_equipment_cost_ledger(inputs):
    v = values(inputs)
    require(all(x>=0 for k,x in v.items() if k not in ('net_power','source_reactor_gap','source_core_excess','source_coil_excess')), 'cost inputs must be nonnegative')
    require(0<v['availability']<=1, 'availability must be in (0,1]')
    imp=max(-v['net_power'],0.)*8760*v['availability']
    result=dict(direct=v['direct'],source_direct=v['source_direct'],source_inclusive=v['source_inclusive'],direct_difference=v['direct']-v['source_direct'],overnight=v['direct']+v['indirect']+v['contingency']+v['owner'],annual_operating=v['om']+v['tritium']+v['deuterium']+v['consumables']+imp*v['import_price'],annual_replacement_reserve=v['replacement_reserve'],lifetime_replacement=v['replacement_total'],annual_export_mwh=max(v['net_power'],0.)*8760*v['availability'],annual_import_mwh=imp,annual_import_cost=imp*v['import_price'],source_reactor_gap=v['source_reactor_gap'],source_core_excess=v['source_core_excess'],source_coil_excess=v['source_coil_excess'],currency_year=v['currency_year'])
    return finish('equipment_cost_ledger', result)
