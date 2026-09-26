"""Guarded native completion of the supplied branch heat balance in MW."""
import math
AUTO_IMPLEMENTED = False

def _reviewed_run_coolant_branch_heat(inputs):
    for name, value in inputs.model_dump().items():
        if not math.isfinite(value) or value < 0:
            raise ValueError(name + ' must be finite nonnegative heat')
    delivered = inputs.deposited_heat_in + inputs.received_exchange_in - inputs.exported_exchange_in + inputs.recovered_friction_in
    if not math.isfinite(delivered) or delivered < 0:
        raise ValueError('delivered heat must be finite nonnegative; supplied export exceeds net branch heat or output overflowed')
    return delivered


from combinations_tea.modules.dual_circuit_heat_accounting.coolant_branch_heat import Coolant_Branch_HeatInput


def run_coolant_branch_heat(inputs: Coolant_Branch_HeatInput) -> float:
    """Typed native adapter; delegates unchanged reviewed calculation."""
    return _reviewed_run_coolant_branch_heat(inputs)
