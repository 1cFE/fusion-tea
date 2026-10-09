"""WI-075 procurement of supplied geometry and continuous installed turns."""
from __future__ import annotations
import math
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from stellarator_materials_rebco_tea.modules.mfe_winding_pack_cost.winding_pack_procurement_cost import Winding_Pack_Procurement_CostInput
AUTO_IMPLEMENTED = False


def calculate(x):
    name = 'Winding Pack Procurement Cost'
    nonnegative = ('tape_volume_in', 'tape_price_per_m', 'winding_rate_1990', 'material_cost_in')
    positive = ('n_coils', 'reference_turns', 'c_coil', 'tape_width', 'tape_thickness', 'cost_escalation', 'nonplanar_factor')
    for key in nonnegative + positive + ('f_set',):
        value = x[key]
        if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value):
            raise ValueError(f'{name}: {key} must be finite')
        if value < 0 or (key not in nonnegative and value == 0):
            raise ValueError(f'{name}: invalid {key}')
    if x['f_set'] > 1:
        raise ValueError(f'{name}: f_set must be in (0, 1]')

    def checked(key, value, must_positive):
        if not math.isfinite(value) or (must_positive and value <= 0):
            raise ValueError(f'{name}: {key} arithmetic overflow/underflow')
        return value

    area = checked('tape_area', x['tape_width'] * x['tape_thickness'], True)
    tape_length = checked('tape_length', x['tape_volume_in'] / area, x['tape_volume_in'] > 0)
    tape_cost = checked('tape_cost', tape_length * x['tape_price_per_m'], tape_length > 0 and x['tape_price_per_m'] > 0)
    conductor_length = x['n_coils']
    for key in ('reference_turns', 'f_set', 'c_coil'):
        conductor_length = checked('conductor_length', conductor_length * x[key], True)
    fabrication = conductor_length
    for key in ('winding_rate_1990', 'cost_escalation', 'nonplanar_factor'):
        fabrication = checked('winding_fabrication_cost', fabrication * x[key], fabrication > 0 and x[key] > 0)
    total = checked('cost', tape_cost + x['material_cost_in'] + fabrication, False)
    return dict(tape_length=tape_length, tape_cost=tape_cost, conductor_length=conductor_length,
                winding_fabrication_cost=fabrication, cost=total)


def run_winding_pack_procurement_cost(inputs: Winding_Pack_Procurement_CostInput) -> tuple[float, float, float, float, float]:
    from stellarator_materials_rebco_tea.schemas.winding_pack_procurement_cost_output import Winding_Pack_Procurement_CostOutput
    result = calculate(type(inputs).model_dump(inputs))
    return tuple(result[key] for key in Winding_Pack_Procurement_CostOutput.model_fields)
