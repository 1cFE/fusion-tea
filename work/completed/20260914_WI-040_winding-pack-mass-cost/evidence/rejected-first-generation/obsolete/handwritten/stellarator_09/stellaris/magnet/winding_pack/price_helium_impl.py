"""Auto-generated implementation for price_helium.

AUTO_IMPLEMENTED = True

SysML Source: root-0/designs/stellarator_09/stellarator_plant.sysml:322

SysML Expressions:
"""

AUTO_IMPLEMENTED = True

from stellarator_tea.modules.stellarator_09.stellaris.magnet.winding_pack.price_helium import price_heliumInput


def run_price_helium(inputs: price_heliumInput) -> float:
    """Execute price_helium calculation.

SysML Source: root-0/designs/stellarator_09/stellarator_plant.sysml:322

Args:
    inputs: Input parameters validated against price_heliumInput schema

Returns:
    float: price_helium

Example:
    >>> inputs = price_heliumInput(...)
    >>> result = run_price_helium(inputs)
    """
    return ((((14.0 * 2077.2644) * 288.15) / 101325.0) * (334.4 / 313.7))
