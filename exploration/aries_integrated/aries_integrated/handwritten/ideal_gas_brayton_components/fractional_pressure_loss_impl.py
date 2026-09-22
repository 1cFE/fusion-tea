"""Guarded nominal ideal-gas component; normative equations in SysML/spec."""
import math
AUTO_IMPLEMENTED = False

def positive(name, value):
    if value <= 0:
        raise ValueError(name + ' must be positive')

def finish(values):
    if not all(math.isfinite(x) for x in values):
        raise ValueError('nonfinite component output')
    return values

def _reviewed_run_fractional_pressure_loss(inputs):
    for name, value in inputs.model_dump().items():
        if not math.isfinite(value):
            raise ValueError(name + " must be finite")
    positive('pressure_in', inputs.pressure_in)
    if not 0 <= inputs.loss_fraction_in < 1: raise ValueError('pressure loss fraction must be in [0,1)')
    pressure = inputs.pressure_in*(1-inputs.loss_fraction_in)
    positive('outlet pressure', pressure)
    return finish((pressure,))[0]


from aries_integrated.modules.ideal_gas_brayton_components.fractional_pressure_loss import Fractional_Pressure_LossInput


def run_fractional_pressure_loss(inputs: Fractional_Pressure_LossInput) -> float:
    """Typed native adapter; delegates unchanged reviewed calculation."""
    return _reviewed_run_fractional_pressure_loss(inputs)
