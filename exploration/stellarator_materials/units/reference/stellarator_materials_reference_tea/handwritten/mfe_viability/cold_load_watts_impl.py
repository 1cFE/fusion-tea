"""Cold load W = cold_MW * 1000000; fixed unit conversion."""
from __future__ import annotations
import math
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from stellarator_materials_reference_tea.modules.mfe_viability.cold_load_watts import Cold_Load_WattsInput
AUTO_IMPLEMENTED = False
def calculate(x):
    for key in ['cold_MW']:
        if isinstance(x[key],bool) or not math.isfinite(x[key]): raise ValueError('nonfinite numeric demand input '+key)
    demand=x['cold_MW']*1e6
    if not math.isfinite(demand): raise ValueError('nonfinite demand')
    return dict(demand=demand)
def run_cold_load_watts(inputs: Cold_Load_WattsInput) -> float:
    result=calculate({key:getattr(inputs,key+'_in') for key in ['cold_MW']})
    return result['demand']
