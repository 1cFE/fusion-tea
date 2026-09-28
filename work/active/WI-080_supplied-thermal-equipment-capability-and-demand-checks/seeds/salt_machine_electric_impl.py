"""Per-machine demand MW = total MW / machine count; inactive short circuits before division."""
from __future__ import annotations
import math
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from stellarator_tea.modules.mfe_viability.salt_machine_electric import Salt_Machine_ElectricInput
AUTO_IMPLEMENTED = False
def calculate(x):
    if not isinstance(x['active'],bool): raise ValueError('active must be Boolean')
    if not x['active']: return dict(demand=0.0)
    for key in ['total_MW', 'count']:
        if isinstance(x[key],bool) or not math.isfinite(x[key]): raise ValueError('nonfinite numeric demand input '+key)
    if x['count']<=0: raise ValueError('active machine count must be positive')
    demand=x['total_MW']/x['count']
    if not math.isfinite(demand): raise ValueError('nonfinite demand')
    return dict(demand=demand)
def run_salt_machine_electric(inputs: Salt_Machine_ElectricInput) -> float:
    result=calculate({key:getattr(inputs,key+'_in') for key in ['active', 'total_MW', 'count']})
    return result['demand']
