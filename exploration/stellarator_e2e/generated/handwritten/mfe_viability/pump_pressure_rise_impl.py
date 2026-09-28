"""Required pump pressure rise MPa = outlet minus inlet; inactive returns zero."""
from __future__ import annotations
import math
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from stellarator_tea.modules.mfe_viability.pump_pressure_rise import Pump_Pressure_RiseInput
AUTO_IMPLEMENTED = False
def calculate(x):
    if not isinstance(x['active'],bool): raise ValueError('active must be Boolean')
    if not x['active']: return dict(demand=0.0)
    for key in ['outlet_MPa', 'inlet_MPa']:
        if isinstance(x[key],bool) or not math.isfinite(x[key]): raise ValueError('nonfinite numeric demand input '+key)
    demand=x['outlet_MPa']-x['inlet_MPa']
    if not math.isfinite(demand): raise ValueError('nonfinite demand')
    return dict(demand=demand)
def run_pump_pressure_rise(inputs: Pump_Pressure_RiseInput) -> float:
    result=calculate({key:getattr(inputs,key+'_in') for key in ['active', 'outlet_MPa', 'inlet_MPa']})
    return result['demand']
