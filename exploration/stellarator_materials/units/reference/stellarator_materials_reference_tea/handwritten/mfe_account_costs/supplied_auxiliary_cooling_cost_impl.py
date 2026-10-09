"""WI-079 selected auxiliary allowance plus supplied cryogenic package amount."""
from __future__ import annotations

import math

AUTO_IMPLEMENTED = False


def calculate(aux_per_mw_in: float, thermal_class_in: float,
              purchase_cost_in: float, n_mod_in: float) -> tuple[float, float, float]:
    for name, value in [('aux_per_mw_in', aux_per_mw_in), ('thermal_class_in', thermal_class_in),
                        ('purchase_cost_in', purchase_cost_in), ('n_mod_in', n_mod_in)]:
        if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value) or value < 0:
            raise ValueError(f'{name} must be a finite nonnegative number')
    if n_mod_in != 1.0:
        raise ValueError('Supplied package accounts support one module only')
    aux_cost = aux_per_mw_in * thermal_class_in * n_mod_in
    cryo_cost = purchase_cost_in
    cost = aux_cost + cryo_cost
    if not all(math.isfinite(v) for v in (aux_cost, cryo_cost, cost)):
        raise ValueError('Nonfinite supplied auxiliary cooling cost')
    return aux_cost, cryo_cost, cost


def run_supplied_auxiliary_cooling_cost(inputs: Supplied_Auxiliary_Cooling_CostInput) -> tuple[float, float, float]:
    from stellarator_materials_reference_tea.schemas.supplied_auxiliary_cooling_cost_output import Supplied_Auxiliary_Cooling_CostOutput
    values = calculate(inputs.aux_per_mw_in, inputs.thermal_class_in, inputs.purchase_cost_in, inputs.n_mod_in)
    named = dict(zip(("aux_cost", "cryo_cost", "cost"), values, strict=True))
    return tuple(named[name] for name in Supplied_Auxiliary_Cooling_CostOutput.model_fields)
