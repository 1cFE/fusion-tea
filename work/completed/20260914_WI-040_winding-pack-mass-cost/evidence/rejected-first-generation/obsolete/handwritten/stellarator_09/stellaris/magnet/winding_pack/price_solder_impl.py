"""Auto-generated implementation for price_solder.

AUTO_IMPLEMENTED = True

SysML Source: root-0/designs/stellarator_09/stellarator_plant.sysml:316

SysML Expressions:
"""

AUTO_IMPLEMENTED = True

from stellarator_tea.modules.stellarator_09.stellaris.magnet.winding_pack.price_solder import price_solderInput


def run_price_solder(inputs: price_solderInput) -> float:
    """Execute price_solder calculation.

SysML Source: root-0/designs/stellarator_09/stellarator_plant.sysml:316

Args:
    inputs: Input parameters validated against price_solderInput schema

Returns:
    float: price_solder

Example:
    >>> inputs = price_solderInput(...)
    >>> result = run_price_solder(inputs)
    """
    return (29.23 / 0.45359237)
