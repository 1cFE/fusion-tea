"""Guarded nominal ideal-gas component; normative equations in SysML/spec."""
import math
AUTO_IMPLEMENTED = False

def positive(name, value):
    if value <= 0:
        raise ValueError(name + ' must be positive')

def finish(values):
    if not all(math.isfinite(x) for x in values):
        raise ValueError('nonfinite component output')
    from brayton_tea.schemas.brayton_cycle_ledger_output import Brayton_Cycle_LedgerOutput
    outputs = dict(zip(['compressor_demand', 'rejected_heat', 'net_shaft', 'shaft_efficiency', 'energy_residual', 'total_pressure_ratio'], values))
    return tuple(outputs[name] for name in Brayton_Cycle_LedgerOutput.model_fields)

def run_brayton_cycle_ledger(inputs):
    for name, value in inputs.model_dump().items():
        if not math.isfinite(value):
            raise ValueError(name + " must be finite")
    for name in ('compressor_1_in','compressor_2_in','compressor_3_in','turbine_work_in'):
        if getattr(inputs,name)<0: raise ValueError(name+' shaft magnitude must be nonnegative')
    for name in ('intercooler_1_in','intercooler_2_in','precooler_in'):
        if getattr(inputs,name)>0: raise ValueError(name+' cooling heat must be nonpositive')
    for name in ('heater_in','inlet_pressure_in','discharge_pressure_in'):
        positive(name,getattr(inputs,name))
    compression = inputs.compressor_1_in+inputs.compressor_2_in+inputs.compressor_3_in
    rejection = -inputs.intercooler_1_in-inputs.intercooler_2_in-inputs.precooler_in
    net = inputs.turbine_work_in-compression
    return finish((compression,rejection,net,net/inputs.heater_in,inputs.heater_in-rejection-net,inputs.discharge_pressure_in/inputs.inlet_pressure_in))
