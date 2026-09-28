"""Auto-generated implementation for absent_boundary_exchange_mw.

AUTO_IMPLEMENTED = True

SysML Source: root-0/dual_blanket_heat.sysml:10

SysML Expressions:
"""

AUTO_IMPLEMENTED = True

from heat_tea.modules.aries_dual_blanket_heat.inter_coolant_exchange.absent_boundary_exchange_mw import absent_boundary_exchange_mwInput


def run_absent_boundary_exchange_mw(inputs: absent_boundary_exchange_mwInput) -> float:
    """Execute absent_boundary_exchange_mw calculation.

SysML Source: root-0/dual_blanket_heat.sysml:10

Args:
    inputs: Input parameters validated against absent_boundary_exchange_mwInput schema

Returns:
    float: absent_boundary_exchange_mw

Example:
    >>> inputs = absent_boundary_exchange_mwInput(...)
    >>> result = run_absent_boundary_exchange_mw(inputs)
    """
    return (inputs.transferred_heat_mw - inputs.transferred_heat_mw)
