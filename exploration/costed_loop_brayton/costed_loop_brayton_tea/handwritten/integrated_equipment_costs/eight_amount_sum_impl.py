"""Reviewed native calculation; emitted from WI-090 authoring record."""
import math
from costed_loop_brayton_tea.handwritten.integrated_equipment_costs.common import values, require, finish
AUTO_IMPLEMENTED = False

def _reviewed_run_eight_amount_sum(inputs):
    v = values(inputs)
    require(all(x>=0 for x in v.values()), 'amounts must be nonnegative')
    result=dict(total=sum(v.values()))
    return finish('eight_amount_sum', result)


from costed_loop_brayton_tea.modules.integrated_equipment_costs.eight_amount_sum import Eight_Amount_SumInput


def run_eight_amount_sum(inputs: Eight_Amount_SumInput) -> float:
    """Typed native adapter; delegates unchanged reviewed calculation."""
    return _reviewed_run_eight_amount_sum(inputs)
