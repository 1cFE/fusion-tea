"""Auto-generated implementation for Electrical_Power_Sum.

AUTO_IMPLEMENTED = True

SysML Source: root-0/analyses/mfe_cryo_inventory.sysml:81

SysML Expressions:
    p_a = 0.0
    p_b = 0.0
    total = p_a + p_b
    
Documentation:
Sum electrical MW with no category conversion.
*Source**: work/active/WI-059_coil-thermal-and-total-support-inventory/design.md **Reference**: D3/D5.
*Basis**: additive electrical balance. **Last Updated**: 2026-09-15
"""

AUTO_IMPLEMENTED = True

from stellarator_tea.modules.mfe_cryo_inventory.electrical_power_sum import Electrical_Power_SumInput


def run_electrical_power_sum(inputs: Electrical_Power_SumInput) -> float:
    """Execute Electrical_Power_Sum calculation.

Sum electrical MW with no category conversion.
*Source**: work/active/WI-059_coil-thermal-and-total-support-inventory/design.md **Reference**: D3/D5.
*Basis**: additive electrical balance. **Last Updated**: 2026-09-15

SysML Source: root-0/analyses/mfe_cryo_inventory.sysml:81

SysML Expressions:
    p_a = 0.0
    p_b = 0.0
    total = p_a + p_b
    
Documentation:
Sum electrical MW with no category conversion.
*Source**: work/active/WI-059_coil-thermal-and-total-support-inventory/design.md **Reference**: D3/D5.
*Basis**: additive electrical balance. **Last Updated**: 2026-09-15

Args:
    inputs: Input parameters validated against Electrical_Power_SumInput schema

Returns:
    float: total

Example:
    >>> inputs = Electrical_Power_SumInput(...)
    >>> result = run_electrical_power_sum(inputs)
    """
    return (inputs.p_a + inputs.p_b)
