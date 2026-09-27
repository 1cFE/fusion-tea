"""Reviewed native calculation; emitted from WI-090 authoring record."""
import math
from exchanger_architecture_thermal_tea.handwritten.integrated_equipment_costs.common import values, require, finish
AUTO_IMPLEMENTED = False

def _reviewed_run_comparison_difference(inputs):
    v = values(inputs)
    result=dict(difference=v['left']-v['right'])
    return finish('comparison_difference', result)


from exchanger_architecture_thermal_tea.modules.integrated_equipment_costs.comparison_difference import Comparison_DifferenceInput


def run_comparison_difference(inputs: Comparison_DifferenceInput) -> float:
    """Typed native adapter; delegates unchanged reviewed calculation."""
    return _reviewed_run_comparison_difference(inputs)
