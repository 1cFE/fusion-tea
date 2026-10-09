"""WI-059 intercept refrigerator; dormant branch precedes thermal arithmetic."""
import math
from stellarator_materials_rebco_tea.modules.mfe_cryo_inventory.intercept_electrical_power import Intercept_Electrical_PowerInput

AUTO_IMPLEMENTED = False


def run_intercept_electrical_power(inputs: Intercept_Electrical_PowerInput) -> float:
    if not inputs.inventory_enabled:
        return 0.0
    if not (inputs.T_shield == 77.0 and inputs.T_amb == 300.0 and 0.0 < inputs.f_carnot <= 1.0):
        raise ValueError("Intercept Electrical Power: require T_shield=77, T_amb=300 K and Carnot fraction in (0, 1]")
    if not math.isfinite(inputs.q_shield) or inputs.q_shield < 0.0:
        raise ValueError("Intercept Electrical Power: negative warm net load")
    return inputs.q_shield * 1e-6 * (inputs.T_amb-inputs.T_shield)/(inputs.f_carnot*inputs.T_shield)
