"""Guarded nominal ideal-gas component; normative equations in SysML/spec."""
import math
AUTO_IMPLEMENTED = False

def positive(name, value):
    if value <= 0:
        raise ValueError(name + ' must be positive')

def finish(values):
    if not all(math.isfinite(x) for x in values):
        raise ValueError('nonfinite component output')
    from aries_integrated.schemas.fixed_outlet_conditioning_output import Fixed_Outlet_ConditioningOutput
    outputs = dict(zip(['temperature_out', 'pressure_out', 'heat_into_fluid'], values))
    return tuple(outputs[name] for name in Fixed_Outlet_ConditioningOutput.model_fields)

def _reviewed_run_fixed_outlet_conditioning(inputs):
    for name, value in inputs.model_dump().items():
        if not math.isfinite(value):
            raise ValueError(name + " must be finite")
    for name in ('temperature_in', 'target_temperature_in', 'pressure_in', 'flow_in', 'cp_in'):
        positive(name, getattr(inputs, name))
    delta = inputs.target_temperature_in-inputs.temperature_in
    if inputs.heating_role_in not in (0., 1.): raise ValueError('heating role must be zero or one')
    if inputs.heating_role_in == 1 and delta <= 0: raise ValueError('heater requires positive temperature rise')
    if inputs.heating_role_in == 0 and delta > 0: raise ValueError('cooler outlet must not exceed inlet')
    heat = inputs.flow_in * inputs.cp_in * delta/1e6
    return finish((inputs.target_temperature_in, inputs.pressure_in, heat))


from aries_integrated.modules.ideal_gas_brayton_components.fixed_outlet_conditioning import Fixed_Outlet_ConditioningInput


def run_fixed_outlet_conditioning(inputs: Fixed_Outlet_ConditioningInput) -> tuple[float, float, float]:
    """Typed native adapter; delegates unchanged reviewed calculation."""
    return _reviewed_run_fixed_outlet_conditioning(inputs)
