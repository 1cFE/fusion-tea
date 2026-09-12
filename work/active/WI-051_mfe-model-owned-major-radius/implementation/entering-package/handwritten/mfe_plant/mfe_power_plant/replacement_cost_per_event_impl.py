"""Auto-generated implementation for replacement_cost_per_event.

AUTO_IMPLEMENTED = True

SysML Source: root-0/designs/generic_mfe/mfe_plant.sysml:689

SysML Expressions:
"""

AUTO_IMPLEMENTED = True

from stellarator_tea.modules.mfe_plant.mfe_power_plant.replacement_cost_per_event import replacement_cost_per_eventInput


def run_replacement_cost_per_event(inputs: replacement_cost_per_eventInput) -> float:
    """Execute replacement_cost_per_event calculation.

SysML Source: root-0/designs/generic_mfe/mfe_plant.sysml:689

Args:
    inputs: Input parameters validated against replacement_cost_per_eventInput schema

Returns:
    float: replacement_cost_per_event

Example:
    >>> inputs = replacement_cost_per_eventInput(...)
    >>> result = run_replacement_cost_per_event(inputs)
    """
    return ((inputs.blanket_capital_cost + inputs.divertor_capital_cost) * inputs.n_mod)
