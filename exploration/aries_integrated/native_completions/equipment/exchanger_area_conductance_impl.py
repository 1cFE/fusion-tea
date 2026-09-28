"""Reviewed native calculation; emitted from WI-090 authoring record."""
import math
from aries_integrated.handwritten.integrated_equipment_costs.common import values, require, finish
AUTO_IMPLEMENTED = False

def run_exchanger_area_conductance(inputs):
    v = values(inputs)
    require(v['area'] >= 0 and v['u'] > 0, 'area must be nonnegative and U positive')
    result = dict(ua=v['area']*v['u']/1e6,area=v['area'])
    return finish('exchanger_area_conductance', result)
