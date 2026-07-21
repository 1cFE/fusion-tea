"""Auto-generated implementation for cas22_capital.

AUTO_IMPLEMENTED = True

SysML Source: unknown:0

SysML Expressions:
    powercore_capital + remote_handling_capital + installation_capital + coolant_capital + aux_cooling_capital + waste_capital + fuel_handling_capital + other_rpe_capital + inc_capital
"""

AUTO_IMPLEMENTED = True

from stellarator_tea.modules.stellarator_09.stellaris.cas22_capital import cas22_capitalInput


def run_cas22_capital(inputs: cas22_capitalInput) -> float:
    """Execute cas22_capital calculation.

SysML Source: unknown:0

SysML Expressions:
    powercore_capital + remote_handling_capital + installation_capital + coolant_capital + aux_cooling_capital + waste_capital + fuel_handling_capital + other_rpe_capital + inc_capital

Args:
    inputs: Input parameters validated against cas22_capitalInput schema

Returns:
    float: cas22_capital

Example:
    >>> inputs = cas22_capitalInput(...)
    >>> result = run_cas22_capital(inputs)
    """
    return ((((((((inputs.powercore_capital + inputs.remote_handling_capital) + inputs.installation_capital) + inputs.coolant_capital) + inputs.aux_cooling_capital) + inputs.waste_capital) + inputs.fuel_handling_capital) + inputs.other_rpe_capital) + inputs.inc_capital)
