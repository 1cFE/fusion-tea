"""Reviewed native calculation; emitted from WI-090 authoring record."""
import math
from aries_integrated.handwritten.integrated_equipment_costs.common import values, require, finish
AUTO_IMPLEMENTED = False

def _reviewed_run_comparison_difference(inputs):
    v = values(inputs)
    result=dict(difference=v['left']-v['right'])
    return finish('comparison_difference', result)


from aries_integrated.modules.integrated_equipment_costs.comparison_difference import Comparison_DifferenceInput


def run_comparison_difference(inputs: Comparison_DifferenceInput) -> float:
    """Typed native adapter; delegates unchanged reviewed calculation."""
    return _reviewed_run_comparison_difference(inputs)
