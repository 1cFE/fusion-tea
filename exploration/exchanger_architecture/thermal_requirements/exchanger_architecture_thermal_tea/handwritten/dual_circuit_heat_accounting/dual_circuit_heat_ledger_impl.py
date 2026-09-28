"""Native two-branch ledger; signed residuals are deliberately preserved."""
import math
AUTO_IMPLEMENTED = False

def run_dual_circuit_heat_ledger(inputs):
    from heat_tea.schemas.dual_circuit_heat_ledger_output import Dual_Circuit_Heat_LedgerOutput
    for name, value in inputs.model_dump().items():
        if not math.isfinite(value) or value < 0:
            raise ValueError(name + ' must be finite nonnegative heat')
    delivered = inputs.duty_1_in + inputs.duty_2_in
    deposited = inputs.deposition_1_in + inputs.deposition_2_in
    friction = inputs.friction_1_in + inputs.friction_2_in
    out = {'delivered_total': delivered, 'deposited_total': deposited, 'friction_total': friction, 'energy_residual': delivered - deposited - friction}
    if not all(math.isfinite(value) for value in out.values()):
        raise ValueError('nonfinite heat ledger output')
    return tuple(out[name] for name in Dual_Circuit_Heat_LedgerOutput.model_fields)
