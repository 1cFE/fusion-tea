"""Auto-generated implementation for powercore_capital.

AUTO_IMPLEMENTED = True

SysML Source: root-0/designs/generic_mfe/mfe_plant.sysml:423

SysML Expressions:
"""

AUTO_IMPLEMENTED = True

from stellarator_tea.modules.mfe_plant.mfe_power_plant.powercore_capital import powercore_capitalInput


def run_powercore_capital(inputs: powercore_capitalInput) -> float:
    """Execute powercore_capital calculation.

SysML Source: root-0/designs/generic_mfe/mfe_plant.sysml:423

Args:
    inputs: Input parameters validated against powercore_capitalInput schema

Returns:
    float: powercore_capital

Example:
    >>> inputs = powercore_capitalInput(...)
    >>> result = run_powercore_capital(inputs)
    """
    return (((((((inputs.magnet_capital_cost + inputs.heating_capital_cost) + inputs.divertor_capital_cost) + inputs.blanket_capital_cost) + inputs.shield_capital_cost) + inputs.structure_capital_cost) + inputs.vessel_capital_cost) + inputs.power_supplies_capital_cost)
