"""WI-060 typed completion of the canonical additive procurement contract."""

import math

from stellarator_tea.modules.mfe_winding_pack_cost.winding_pack_procurement_cost import (
    Winding_Pack_Procurement_CostInput,
)
from stellarator_tea.schemas.winding_pack_procurement_cost_output import (
    Winding_Pack_Procurement_CostOutput,
)

AUTO_IMPLEMENTED = False


def run_winding_pack_procurement_cost(
    inputs: Winding_Pack_Procurement_CostInput,
) -> tuple[float, float, float, float, float]:
    """Keep tape, other materials and conductor-metre winding operations separate."""
    name = "Winding Pack Procurement Cost"
    nonnegative = ("I_coil", "tape_volume_in", "tape_price_per_m", "winding_rate_1990", "material_cost_in")
    positive = ("n_coils", "c_coil", "turn_current", "tape_width", "tape_thickness", "cost_escalation", "nonplanar_factor")
    for key in nonnegative:
        value = getattr(inputs, key)
        if not math.isfinite(value) or value < 0:
            raise ValueError(f"{name}: {key} must be finite and nonnegative")
    for key in positive:
        value = getattr(inputs, key)
        if not math.isfinite(value) or value <= 0:
            raise ValueError(f"{name}: {key} must be finite and positive")
    if not math.isfinite(inputs.f_set) or not 0 < inputs.f_set <= 1:
        raise ValueError(f"{name}: f_set must be finite and in (0, 1]")

    tape_area = inputs.tape_width * inputs.tape_thickness
    if not math.isfinite(tape_area) or tape_area <= 0:
        raise ValueError(f"{name}: tape_area must be finite and positive")
    tape_length = inputs.tape_volume_in / tape_area
    if not math.isfinite(tape_length) or (inputs.tape_volume_in > 0 and tape_length <= 0):
        raise ValueError(f"{name}: tape_length must be finite and positive for positive volume")
    tape_cost = tape_length * inputs.tape_price_per_m
    if not math.isfinite(tape_cost) or (tape_length > 0 and inputs.tape_price_per_m > 0 and tape_cost <= 0):
        raise ValueError(f"{name}: tape_cost must be finite and positive for positive length and price")
    conductor_length = (inputs.n_coils * inputs.I_coil * inputs.f_set * inputs.c_coil
                        / inputs.turn_current)
    winding_fabrication_cost = (
        conductor_length * inputs.winding_rate_1990
        * inputs.cost_escalation * inputs.nonplanar_factor
    )
    cost = tape_cost + inputs.material_cost_in + winding_fabrication_cost
    output = (tape_length, tape_cost, conductor_length, winding_fabrication_cost, cost)
    keys = ("tape_length", "tape_cost", "conductor_length", "winding_fabrication_cost", "cost")
    for key, value in zip(keys, output, strict=True):
        if not math.isfinite(value):
            raise ValueError(f"{name}: {key} must be finite")
    # Match the generated positional ABI without treating declaration order as ABI.
    by_name = dict(zip(keys, output, strict=True))
    return tuple(by_name[key] for key in Winding_Pack_Procurement_CostOutput.model_fields)
