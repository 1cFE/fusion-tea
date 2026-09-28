"""Reviewed native calculation; emitted from WI-090 authoring record."""
import math
from component_alternatives_tea.handwritten.integrated_equipment_costs.common import values, require, finish
AUTO_IMPLEMENTED = False

def _reviewed_run_scaled_amount(inputs):
    v = values(inputs)
    require(v['amount']>=0 and v['factor']>=0, 'amount and factor must be nonnegative')
    result=dict(amount=v['amount']*v['factor'])
    return finish('scaled_amount', result)


from component_alternatives_tea.modules.integrated_equipment_costs.scaled_amount import Scaled_AmountInput


def run_scaled_amount(inputs: Scaled_AmountInput) -> float:
    """Typed native adapter; delegates unchanged reviewed calculation."""
    return _reviewed_run_scaled_amount(inputs)
