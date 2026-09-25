"""Reviewed native calculation; emitted from WI-090 authoring record."""
import math
from aries_integrated.handwritten.integrated_equipment_costs.common import values, require, finish
AUTO_IMPLEMENTED = False

def run_comparison_difference(inputs):
    v = values(inputs)
    result=dict(difference=v['left']-v['right'])
    return finish('comparison_difference', result)
