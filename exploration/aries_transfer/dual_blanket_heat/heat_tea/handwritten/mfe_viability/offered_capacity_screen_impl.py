"""WI080 guarded necessary scalar capacity at separately evaluated conditions."""
from __future__ import annotations
import math
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from heat_tea.modules.mfe_viability.offered_capacity_screen import Offered_Capacity_ScreenInput
AUTO_IMPLEMENTED = False
def calculate(x):
    for key in ('applicable','conditions_supported','demand_available'):
        if not isinstance(x[key], bool):
            raise ValueError(key + ' must be Boolean')
    rating=x['rating']; demand=x['demand']
    if isinstance(rating,bool) or not math.isfinite(rating) or rating<0:
        raise ValueError('rating must be finite nonnegative numeric')
    if x['applicable'] and (isinstance(demand,bool) or not math.isfinite(demand) or demand<0):
        raise ValueError('active demand must be finite nonnegative numeric')
    supported=x['applicable'] and x['conditions_supported'] and x['demand_available']
    margin=rating-demand if x['applicable'] else 0.0
    if not math.isfinite(margin):
        raise ValueError('nonfinite margin')
    return dict(margin=margin,applicable=x['applicable'],supported=supported,
                evaluation_defined=1.0 if supported else 0.0,capacity_ok=supported and margin>=0.0)
def run_offered_capacity_screen(inputs: Offered_Capacity_ScreenInput) -> tuple[float, float, float, float, float]:
    result=calculate({key:getattr(inputs,key+'_in') for key in ('rating','demand','applicable','conditions_supported','demand_available')})
    from heat_tea.schemas.offered_capacity_screen_output import Offered_Capacity_ScreenOutput
    return tuple(result[name] for name in Offered_Capacity_ScreenOutput.model_fields)
