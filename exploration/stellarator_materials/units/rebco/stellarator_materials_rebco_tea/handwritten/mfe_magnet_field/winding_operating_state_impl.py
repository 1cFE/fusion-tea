"""WI-075 supplied winding identity; native calc doc owns the contract."""
from __future__ import annotations
import math
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from stellarator_materials_rebco_tea.modules.mfe_magnet_field.winding_operating_state import Winding_Operating_StateInput
AUTO_IMPLEMENTED = False


def calculate(x):
    def positive(key, value):
        if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value) or value <= 0:
            raise ValueError(f'Winding Operating State: {key} must be finite and positive')
        return value
    for key in ('reference_turns', 'turn_current', 'wp_side'):
        positive(key, x[key])
    current = positive('I_coil', x['reference_turns'] * x['turn_current'])
    area = positive('pack_area', x['wp_side'] * x['wp_side'])
    area_mm2 = positive('pack_area_mm2', area * 1e6)
    density = positive('j_wp_effective', current / area_mm2)
    return dict(I_coil=current, j_wp_effective=density)


def run_winding_operating_state(inputs: Winding_Operating_StateInput) -> tuple[float, float]:
    from stellarator_materials_rebco_tea.schemas.winding_operating_state_output import Winding_Operating_StateOutput
    result = calculate(type(inputs).model_dump(inputs))
    return tuple(result[key] for key in Winding_Operating_StateOutput.model_fields)
