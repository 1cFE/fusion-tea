"""WI-062 conditional absolute current; normative equations in the native calc doc."""
import math
from stellarator_tea.modules.mfe_conductor_current.rebco_conductor_current import REBCO_Conductor_CurrentInput
from stellarator_tea.schemas.rebco_conductor_current_output import REBCO_Conductor_CurrentOutput

AUTO_IMPLEMENTED = False


def run_rebco_conductor_current(inputs: REBCO_Conductor_CurrentInput) -> tuple[float, float, float, float, float, float, float, float, float, float, float]:
    def positive(key, value):
        if not math.isfinite(value) or value <= 0:
            raise ValueError(f'REBCO Conductor Current: {key} must be finite and positive')
        return value

    for key in type(inputs).model_fields:
        value = getattr(inputs, key)
        if key == 'allow_field_extrapolation':
            if value not in (0.0, 1.0):
                raise ValueError('REBCO Conductor Current: allow_field_extrapolation must be 0 or 1')
        else:
            positive(key, value)
    for key in ('cabling_factor', 'degradation_factor', 'sharing_factor', 'allowable_fraction'):
        if getattr(inputs, key) > 1:
            raise ValueError(f'REBCO Conductor Current: {key} must be at most 1')
    for key, target in (('temperature', 20.0), ('tape_thickness', 56e-6)):
        if getattr(inputs, key) != target:
            raise ValueError(f'REBCO Conductor Current: unsupported {key}; expected {target}')
    if not 0.004 <= inputs.tape_width <= 0.006:
        raise ValueError('REBCO Conductor Current: tape_width outside 4..6 mm')
    if not 20 <= inputs.B_peak <= 32:
        raise ValueError('REBCO Conductor Current: B_peak outside 20..32 T')
    extrapolated = float(inputs.B_peak > 24)
    if extrapolated and not inputs.allow_field_extrapolation:
        raise ValueError('REBCO Conductor Current: B_peak above 24 T requires allow_field_extrapolation')
    out = {}
    out['parallel_tapes_set'] = positive('parallel_tapes_set', inputs.tape_length / inputs.conductor_length)
    intermediate = positive('reference_count_numerator', out['parallel_tapes_set'] * inputs.f_set)
    out['parallel_tapes_reference'] = positive('parallel_tapes_reference', intermediate / inputs.f_wp_vol)
    tape = inputs.reference_tape_current
    for key, factor in (('width_transfer', inputs.tape_width / 0.004), ('field_transfer', (inputs.B_peak / 20) ** -0.6), ('material_factor', inputs.material_factor), ('orientation_factor', inputs.orientation_factor)):
        tape = positive('tape_current_' + key, tape * factor)
    out['tape_critical_current'] = tape
    for scope in ('reference', 'set'):
        current = positive('critical_current_' + scope, out['parallel_tapes_' + scope] * tape)
        for key in ('cabling_factor', 'degradation_factor', 'sharing_factor'):
            current = positive('critical_current_' + scope + '_' + key, current * getattr(inputs, key))
        out['critical_current_' + scope] = current
        out['operating_fraction_' + scope] = positive('operating_fraction_' + scope, inputs.turn_current / current)
    out['allowable_current'] = positive('allowable_current', inputs.allowable_fraction * out['critical_current_reference'])
    out['margin_fraction'] = inputs.allowable_fraction - out['operating_fraction_reference']
    out['margin_current'] = out['allowable_current'] - inputs.turn_current
    out['field_extrapolated'] = extrapolated
    for key, value in out.items():
        if not math.isfinite(value):
            raise ValueError(f'REBCO Conductor Current: nonfinite {key}')
    return tuple(out[key] for key in REBCO_Conductor_CurrentOutput.model_fields)
