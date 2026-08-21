"""Auto-generated implementation for reactor_equipment_subtotal.

AUTO_IMPLEMENTED = True

SysML Source: root-0/designs/generic_mfe/mfe_plant.sysml:456

SysML Expressions:
"""

AUTO_IMPLEMENTED = True

from stellarator_tea.modules.mfe_plant.mfe_power_plant.reactor_equipment_subtotal import reactor_equipment_subtotalInput


def run_reactor_equipment_subtotal(inputs: reactor_equipment_subtotalInput) -> float:
    """Execute reactor_equipment_subtotal calculation.

SysML Source: root-0/designs/generic_mfe/mfe_plant.sysml:456

Args:
    inputs: Input parameters validated against reactor_equipment_subtotalInput schema

Returns:
    float: reactor_equipment_subtotal

Example:
    >>> inputs = reactor_equipment_subtotalInput(...)
    >>> result = run_reactor_equipment_subtotal(inputs)
    """
    return (inputs.powercore_capital + inputs.remote_handling_capital)
