"""Auto-generated implementation for Supplied_Annual_Energy.

AUTO_IMPLEMENTED = True

SysML Source: root-0/integrated_lifecycle_costs.sysml:73

SysML Expressions:
    annual_energy = 8760.0 * net_power_in * availability_in
    
Documentation:
*Source**: work/active/WI-091_aries-integrated-lifecycle-cost/design.md. **Ref**: reviewed financial convention, roles and F1-F9 assumptions; work/orchestration/goals/aries-integrated-lcoe/evidence/source-boundary.md. **Basis**: conditional real USD2004 dated lifecycle accounts; assumptions are not scientific qualification. **Last Updated**: 2026-09-22.
"""

AUTO_IMPLEMENTED = True

from aries_integrated.modules.integrated_lifecycle_costs.supplied_annual_energy import Supplied_Annual_EnergyInput


def run_supplied_annual_energy(inputs: Supplied_Annual_EnergyInput) -> float:
    """Execute Supplied_Annual_Energy calculation.

*Source**: work/active/WI-091_aries-integrated-lifecycle-cost/design.md. **Ref**: reviewed financial convention, roles and F1-F9 assumptions; work/orchestration/goals/aries-integrated-lcoe/evidence/source-boundary.md. **Basis**: conditional real USD2004 dated lifecycle accounts; assumptions are not scientific qualification. **Last Updated**: 2026-09-22.

SysML Source: root-0/integrated_lifecycle_costs.sysml:73

SysML Expressions:
    annual_energy = 8760.0 * net_power_in * availability_in
    
Documentation:
*Source**: work/active/WI-091_aries-integrated-lifecycle-cost/design.md. **Ref**: reviewed financial convention, roles and F1-F9 assumptions; work/orchestration/goals/aries-integrated-lcoe/evidence/source-boundary.md. **Basis**: conditional real USD2004 dated lifecycle accounts; assumptions are not scientific qualification. **Last Updated**: 2026-09-22.

Args:
    inputs: Input parameters validated against Supplied_Annual_EnergyInput schema

Returns:
    float: annual_energy

Example:
    >>> inputs = Supplied_Annual_EnergyInput(...)
    >>> result = run_supplied_annual_energy(inputs)
    """
    return ((8760.0 * inputs.net_power_in) * inputs.availability_in)
