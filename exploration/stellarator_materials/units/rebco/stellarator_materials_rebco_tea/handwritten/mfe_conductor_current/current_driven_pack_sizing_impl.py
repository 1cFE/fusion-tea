"""WI-064 optional continuous current-driven inventory; native doc owns equations."""
import math
from stellarator_materials_rebco_tea.modules.mfe_conductor_current.current_driven_pack_sizing import Current_Driven_Pack_SizingInput

AUTO_IMPLEMENTED = False


def run_current_driven_pack_sizing(inputs: Current_Driven_Pack_SizingInput) -> tuple[float, float, float, float, float, float]:
    def positive(key, value):
        if not math.isfinite(value) or value <= 0:
            raise ValueError(f'Current Driven Pack Sizing: {key} must be finite and positive')
        return value

    fractions = ('f_copper', 'f_solder', 'f_steel', 'f_helium')
    for key in type(inputs).model_fields:
        value = getattr(inputs, key)
        if key in ('sizing_mode', 'allow_field_extrapolation'):
            if value not in (0.0, 1.0):
                raise ValueError(f'Current Driven Pack Sizing: {key} must be 0 or 1')
        elif key in fractions:
            if not math.isfinite(value) or value < 0:
                raise ValueError(f'Current Driven Pack Sizing: {key} must be finite and nonnegative')
        else:
            positive(key, value)
    if inputs.inventory_multiplier < 1:
        raise ValueError('Current Driven Pack Sizing: inventory_multiplier must be at least 1')
    for key in ('cabling_factor', 'degradation_factor', 'sharing_factor', 'allowable_fraction'):
        if getattr(inputs, key) > 1:
            raise ValueError(f'Current Driven Pack Sizing: {key} must be at most 1')
    for key, target in (('temperature', 20.0), ('tape_thickness', 56e-6)):
        if getattr(inputs, key) != target:
            raise ValueError(f'Current Driven Pack Sizing: unsupported {key}; expected {target}')
    if not 0.004 <= inputs.tape_width <= 0.006:
        raise ValueError('Current Driven Pack Sizing: tape_width outside 4..6 mm')
    if not 20 <= inputs.B_peak <= 32:
        raise ValueError('Current Driven Pack Sizing: B_peak outside 20..32 T')
    if inputs.B_peak > 24 and not inputs.allow_field_extrapolation:
        raise ValueError('Current Driven Pack Sizing: B_peak above 24 T requires allow_field_extrapolation')
    tape_fraction = positive('tape_fraction', 1 - sum(getattr(inputs, key) for key in fractions))
    if tape_fraction > 1:
        raise ValueError('Current Driven Pack Sizing: tape_fraction must be at most 1')
    tape_area = positive('tape_area', inputs.tape_width * inputs.tape_thickness)
    available = inputs.reference_tape_current
    for key, factor in (('width_transfer', inputs.tape_width / 0.004), ('field_transfer', (inputs.B_peak / 20) ** -0.6), ('material_factor', inputs.material_factor), ('orientation_factor', inputs.orientation_factor), ('cabling_factor', inputs.cabling_factor), ('degradation_factor', inputs.degradation_factor), ('sharing_factor', inputs.sharing_factor)):
        available = positive('tape_current_' + key, available * factor)
    allowed = positive('allowed_tape_current', inputs.allowable_fraction * available)
    required_tapes = positive('required_tapes', inputs.turn_current / allowed)
    conductor_tape_area = positive('conductor_tape_area', required_tapes * tape_area)
    conductor_area = positive('required_conductor_area', conductor_tape_area / tape_fraction)
    turns = positive('turns', inputs.I_coil / inputs.turn_current)
    pack_area = positive('required_pack_area', turns * conductor_area)
    pack_area_mm2 = positive('pack_area_mm2', pack_area * 1e6)
    density = positive('required_effective_density', inputs.I_coil / pack_area_mm2)
    selected = inputs.legacy_effective_density if inputs.sizing_mode == 0 else positive('selected_effective_density', density / inputs.inventory_multiplier)
    return required_tapes, conductor_area, pack_area, density, selected, available
