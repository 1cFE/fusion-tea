"""Guarded nominal ideal-gas component; normative equations in SysML/spec."""
import math
AUTO_IMPLEMENTED = False

def positive(name, value):
    if value <= 0:
        raise ValueError(name + ' must be positive')

def finish(values):
    if not all(math.isfinite(x) for x in values):
        raise ValueError('nonfinite component output')
    from exchanger_architecture_thermal_tea.schemas.ideal_gas_compressor_output import Ideal_Gas_CompressorOutput
    outputs = dict(zip(['temperature_out', 'pressure_out', 'shaft_demand'], values))
    return tuple(outputs[name] for name in Ideal_Gas_CompressorOutput.model_fields)

def _reviewed_run_ideal_gas_compressor(inputs):
    for name, value in inputs.model_dump().items():
        if not math.isfinite(value):
            raise ValueError(name + " must be finite")
    for name in ('temperature_in', 'pressure_in', 'flow_in', 'cp_in'):
        positive(name, getattr(inputs, name))
    if inputs.gamma_in <= 1: raise ValueError('gamma must exceed one')
    if inputs.ratio_in < 1: raise ValueError('compression ratio must be at least one')
    if not 0 < inputs.efficiency_in <= 1: raise ValueError('efficiency must be in (0,1]')
    temperature = inputs.temperature_in * (1 + (inputs.ratio_in ** ((inputs.gamma_in-1)/inputs.gamma_in)-1)/inputs.efficiency_in)
    pressure = inputs.pressure_in * inputs.ratio_in
    work = inputs.flow_in * inputs.cp_in * (temperature-inputs.temperature_in)/1e6
    return finish((temperature, pressure, work))


from exchanger_architecture_thermal_tea.modules.ideal_gas_brayton_components.ideal_gas_compressor import Ideal_Gas_CompressorInput


def run_ideal_gas_compressor(inputs: Ideal_Gas_CompressorInput) -> tuple[float, float, float]:
    """Typed native adapter; delegates unchanged reviewed calculation."""
    return _reviewed_run_ideal_gas_compressor(inputs)
