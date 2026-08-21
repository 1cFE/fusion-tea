"""Auto-generated implementation for Recirculating_Power_Fraction.

AUTO_IMPLEMENTED = True

SysML Source: root-0/analyses/fusion_cycle.sysml:4

SysML Expressions:
    fusion_cycle_gain = eta * gain * blanket_multiplier * thermal_efficiency
    f_recirc = 1.0 / fusion_cycle_gain
    
Documentation:
Computes the recirculating power fraction for an IFE plant.
f_recirc = 1 / (eta * G * M * epsilon)

The recirculating power fraction determines what fraction of
gross electric output must be fed back to the driver. Values
above ~0.25 (fusion cycle gain below ~4) create a sharp knee
in the cost curve.

*Source**: knowledge/sources/energy_from_inertial_fusion/output.md
*Ref**: Components section (fusion cycle gain discussion)
*Basis**: DI-001 — eta*G must exceed ~10 for viability
"""

AUTO_IMPLEMENTED = True

from ife_tea.modules.fusion_cycle.recirculating_power_fraction import Recirculating_Power_FractionInput


def run_recirculating_power_fraction(inputs: Recirculating_Power_FractionInput) -> float:
    """Execute Recirculating_Power_Fraction calculation.

Computes the recirculating power fraction for an IFE plant.
f_recirc = 1 / (eta * G * M * epsilon)

The recirculating power fraction determines what fraction of
gross electric output must be fed back to the driver. Values
above ~0.25 (fusion cycle gain below ~4) create a sharp knee
in the cost curve.

*Source**: knowledge/sources/energy_from_inertial_fusion/output.md
*Ref**: Components section (fusion cycle gain discussion)
*Basis**: DI-001 — eta*G must exceed ~10 for viability

SysML Source: root-0/analyses/fusion_cycle.sysml:4

SysML Expressions:
    fusion_cycle_gain = eta * gain * blanket_multiplier * thermal_efficiency
    f_recirc = 1.0 / fusion_cycle_gain
    
Documentation:
Computes the recirculating power fraction for an IFE plant.
f_recirc = 1 / (eta * G * M * epsilon)

The recirculating power fraction determines what fraction of
gross electric output must be fed back to the driver. Values
above ~0.25 (fusion cycle gain below ~4) create a sharp knee
in the cost curve.

*Source**: knowledge/sources/energy_from_inertial_fusion/output.md
*Ref**: Components section (fusion cycle gain discussion)
*Basis**: DI-001 — eta*G must exceed ~10 for viability

Args:
    inputs: Input parameters validated against Recirculating_Power_FractionInput schema

Returns:
    float: f_recirc

Example:
    >>> inputs = Recirculating_Power_FractionInput(...)
    >>> result = run_recirculating_power_fraction(inputs)
    """
    fusion_cycle_gain = (((inputs.eta * inputs.gain) * inputs.blanket_multiplier) * inputs.thermal_efficiency)
    return (1.0 / fusion_cycle_gain)
