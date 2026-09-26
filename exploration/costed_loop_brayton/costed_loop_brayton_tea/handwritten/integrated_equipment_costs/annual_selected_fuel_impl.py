"""Reviewed native calculation; emitted from WI-090 authoring record."""
import math
from costed_loop_brayton_tea.handwritten.integrated_equipment_costs.common import values, require, finish
AUTO_IMPLEMENTED = False

def _reviewed_run_annual_selected_fuel(inputs):
    v = values(inputs)
    require(all(x>=0 for x in v.values()), 'fuel inputs must be nonnegative')
    require(v['atom_mass']>0 and v['seconds']>0 and 0<v['availability']<=1, 'invalid fuel constants/availability')
    b=v['burn']*v['atom_mass']*v['seconds']*v['availability']
    l=v['loss']*v['atom_mass']*v['seconds']*v['availability']
    d=v['stock_kg']*v['decay']*v['seconds']
    e=max(b+l+d-v['annual_recovery'],0.)
    result=dict(annual_burn=b,annual_loss=l,annual_decay=d,annual_recovery=v['annual_recovery'],annual_external=e,annual_cost=e*v['tritium_price'],required_stock=v['exhaust']*v['atom_mass']*v['residence'],breeding_supported=0.)
    return finish('annual_selected_fuel', result)


from costed_loop_brayton_tea.modules.integrated_equipment_costs.annual_selected_fuel import Annual_Selected_FuelInput


def run_annual_selected_fuel(inputs: Annual_Selected_FuelInput) -> tuple[float, float, float, float, float, float, float, float]:
    """Typed native adapter; delegates unchanged reviewed calculation."""
    return _reviewed_run_annual_selected_fuel(inputs)
