"""WI-038 typed completion of the relative conductor field-envelope contract."""

import math

from stellarator_materials_nb3sn_tea.modules.mfe_conductor_grade.conductor_field_capability import (
    Conductor_Field_CapabilityInput,
)
from stellarator_materials_nb3sn_tea.schemas.conductor_field_capability_output import (
    Conductor_Field_CapabilityOutput,
)

AUTO_IMPLEMENTED = False


def run_conductor_field_capability(
    inputs: Conductor_Field_CapabilityInput,
) -> tuple[float, float]:
    """Apply a conditional field law without claiming qualified absolute capability."""
    name = "Conductor Field Capability"
    for key in ("B_design", "B_reference", "field_exponent", "j_reference"):
        value = getattr(inputs, key)
        if not math.isfinite(value) or value <= 0:
            raise ValueError(f"{name}: {key} must be finite and positive")
    field_ratio = inputs.B_design / inputs.B_reference
    if not math.isfinite(field_ratio) or field_ratio <= 0:
        raise ValueError(f"{name}: field_ratio must be finite and positive")
    try:
        quantity_factor = field_ratio ** inputs.field_exponent
    except OverflowError as exc:
        raise ValueError(f"{name}: quantity_factor must be finite and positive") from exc
    if not math.isfinite(quantity_factor) or quantity_factor <= 0:
        raise ValueError(f"{name}: quantity_factor must be finite and positive")
    j_wp_effective = inputs.j_reference / quantity_factor
    if not math.isfinite(j_wp_effective) or j_wp_effective <= 0:
        raise ValueError(f"{name}: j_wp_effective must be finite and positive")
    by_name = {
        "quantity_factor": quantity_factor,
        "j_wp_effective": j_wp_effective,
    }
    # Generated wrapper/schema order is not SysML declaration order.
    return tuple(by_name[key] for key in Conductor_Field_CapabilityOutput.model_fields)
