"""Reviewed native calculation; emitted from WI-090 authoring record."""
import math
from aries_integrated.handwritten.integrated_equipment_costs.common import values, require, finish
AUTO_IMPLEMENTED = False

def run_scaled_amount(inputs):
    v = values(inputs)
    require(v['amount']>=0 and v['factor']>=0, 'amount and factor must be nonnegative')
    result=dict(amount=v['amount']*v['factor'])
    return finish('scaled_amount', result)
