"""WI-059 empirical total support mass; no local structural qualification."""
import math
from stellarator_tea.modules.mfe_magnet_cost.magnet_support_mass import Magnet_Support_MassInput

AUTO_IMPLEMENTED = False


def run_magnet_support_mass(inputs: Magnet_Support_MassInput) -> float:
    if not math.isfinite(inputs.c_support) or inputs.c_support < 0.0:
        raise ValueError("Magnet Support Mass: coefficient must be finite and nonnegative")
    if inputs.c_support == 0.0:
        return 0.0
    if not (math.isfinite(inputs.W_mag) and inputs.W_mag >= 0.0 and math.isfinite(inputs.e_support) and inputs.e_support > 0.0):
        raise ValueError("Magnet Support Mass: finite nonnegative energy and positive exponent required")
    mass = 1000.0 * inputs.c_support * (inputs.W_mag/1e6)**inputs.e_support
    if not math.isfinite(mass):
        raise ValueError("Magnet Support Mass: nonfinite mass")
    return mass
