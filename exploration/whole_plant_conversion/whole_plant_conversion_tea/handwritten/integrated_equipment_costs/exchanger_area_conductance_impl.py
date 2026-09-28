"""Reviewed native calculation; emitted from WI-090 authoring record."""
import math
from whole_plant_conversion_tea.handwritten.integrated_equipment_costs.common import values, require, finish
AUTO_IMPLEMENTED = False

def _reviewed_run_exchanger_area_conductance(inputs):
    v = values(inputs)
    require(v['area'] >= 0 and v['u'] > 0, 'area must be nonnegative and U positive')
    result = dict(ua=v['area']*v['u']/1e6,area=v['area'])
    return finish('exchanger_area_conductance', result)


from whole_plant_conversion_tea.modules.integrated_equipment_costs.exchanger_area_conductance import Exchanger_Area_ConductanceInput


def run_exchanger_area_conductance(inputs: Exchanger_Area_ConductanceInput) -> tuple[float, float]:
    """Typed native adapter; delegates unchanged reviewed calculation."""
    return _reviewed_run_exchanger_area_conductance(inputs)
