from __future__ import annotations
"""WI-068 domain guard for actual combined delivered-capital shipping scope."""
import math
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from stellarator_tea.modules.mfe_facilities.facility_shipping_scope import Facility_Shipping_ScopeInput
AUTO_IMPLEMENTED = False

def calculate(inputs):
    x=dict(inputs)
    if any(isinstance(v,bool) or not math.isfinite(v) or v<0 for v in x.values()):raise ValueError('shipping scope requires finite nonnegative values')
    fuel = x.get('fuel_installation', 0.0) * (1 + x.get('contingency', 0.0))
    if not math.isfinite(fuel): raise ValueError('Nonfinite fuel installation exclusion')
    rest=x['cas20']-x['cooling_exclusion']-x['facility_exclusion']-fuel
    if rest<0:raise ValueError('combined shipping exclusions exceed CAS20')
    return dict(fuel_installation_exclusion=fuel,cooling_exclusion=x['cooling_exclusion'],facility_exclusion=x['facility_exclusion'],remaining_shipping_base=rest)


def run_facility_shipping_scope(inputs: Facility_Shipping_ScopeInput) -> tuple[float, float, float, float]:
    from stellarator_tea.schemas.facility_shipping_scope_output import Facility_Shipping_ScopeOutput
    x = {name.removesuffix("_in"): getattr(inputs,name) for name in type(inputs).model_fields}
    out = calculate(x)
    return tuple(out[name] for name in Facility_Shipping_ScopeOutput.model_fields)
