"""Guarded nominal ideal-gas component; normative equations in SysML/spec."""
import math
AUTO_IMPLEMENTED = False

def positive(name, value):
    if value <= 0:
        raise ValueError(name + ' must be positive')

def finish(values):
    if not all(math.isfinite(x) for x in values):
        raise ValueError('nonfinite component output')
    from brayton_tea.schemas.equal_capacity_recuperator_output import Equal_Capacity_RecuperatorOutput
    outputs = dict(zip(['cold_temperature_out', 'hot_temperature_out', 'transferred_heat'], values))
    return tuple(outputs[name] for name in Equal_Capacity_RecuperatorOutput.model_fields)

def run_equal_capacity_recuperator(inputs):
    for name, value in inputs.model_dump().items():
        if not math.isfinite(value):
            raise ValueError(name + " must be finite")
    for name in ('cold_temperature_in', 'hot_temperature_in', 'flow_in', 'cp_in'):
        positive(name, getattr(inputs, name))
    if not 0 <= inputs.effectiveness_in <= 1: raise ValueError('effectiveness must be in [0,1]')
    if inputs.hot_temperature_in < inputs.cold_temperature_in: raise ValueError('recuperator hot inlet below cold inlet')
    rise = inputs.effectiveness_in*(inputs.hot_temperature_in-inputs.cold_temperature_in)
    return finish((inputs.cold_temperature_in+rise, inputs.hot_temperature_in-rise, inputs.flow_in*inputs.cp_in*rise/1e6))
