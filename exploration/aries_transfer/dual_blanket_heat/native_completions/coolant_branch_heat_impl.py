"""Guarded native completion of the supplied branch heat balance in MW."""
import math
AUTO_IMPLEMENTED = False

def run_coolant_branch_heat(inputs):
    for name, value in inputs.model_dump().items():
        if not math.isfinite(value) or value < 0:
            raise ValueError(name + ' must be finite nonnegative heat')
    delivered = inputs.deposited_heat_in + inputs.received_exchange_in - inputs.exported_exchange_in + inputs.recovered_friction_in
    if not math.isfinite(delivered) or delivered < 0:
        raise ValueError('delivered heat must be finite nonnegative; supplied export exceeds net branch heat or output overflowed')
    return delivered
