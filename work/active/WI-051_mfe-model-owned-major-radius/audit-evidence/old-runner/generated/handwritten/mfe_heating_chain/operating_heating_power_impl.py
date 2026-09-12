"""Auto-generated implementation for Operating_Heating_Power.

AUTO_IMPLEMENTED = True

SysML Source: root-0/analyses/mfe_heating_chain.sysml:79

SysML Expressions:
    p_coupled = p_required_in
    p_delivered = p_required_in / eta_couple_in
    p_wallplug = p_delivered / eta_source_in
    
Documentation:
Sustained heating at held two-stage efficiency. Signed demand remains diagnostic outside burn hold; no clipping at zero or capacity. All powers MW, efficiencies dimensionless. **Source**: models/library/analyses/mfe_heating_chain.sysml **Ref**: Heating Power Chain two-stage identities; work/active/WI-050_mfe-coherent-operating-heating/spec.md MR-WI050-1/2 **Basis**: algebraic inverse at constant efficiencies, supported domain 0 < efficiency <= 1 **Last Updated**: 2026-09-11
"""

AUTO_IMPLEMENTED = True

from stellarator_tea.modules.mfe_heating_chain.operating_heating_power import Operating_Heating_PowerInput


def run_operating_heating_power(inputs: Operating_Heating_PowerInput) -> tuple[float, float, float]:
    """Execute Operating_Heating_Power calculation.

Sustained heating at held two-stage efficiency. Signed demand remains diagnostic outside burn hold; no clipping at zero or capacity. All powers MW, efficiencies dimensionless. **Source**: models/library/analyses/mfe_heating_chain.sysml **Ref**: Heating Power Chain two-stage identities; work/active/WI-050_mfe-coherent-operating-heating/spec.md MR-WI050-1/2 **Basis**: algebraic inverse at constant efficiencies, supported domain 0 < efficiency <= 1 **Last Updated**: 2026-09-11

SysML Source: root-0/analyses/mfe_heating_chain.sysml:79

SysML Expressions:
    p_coupled = p_required_in
    p_delivered = p_required_in / eta_couple_in
    p_wallplug = p_delivered / eta_source_in
    
Documentation:
Sustained heating at held two-stage efficiency. Signed demand remains diagnostic outside burn hold; no clipping at zero or capacity. All powers MW, efficiencies dimensionless. **Source**: models/library/analyses/mfe_heating_chain.sysml **Ref**: Heating Power Chain two-stage identities; work/active/WI-050_mfe-coherent-operating-heating/spec.md MR-WI050-1/2 **Basis**: algebraic inverse at constant efficiencies, supported domain 0 < efficiency <= 1 **Last Updated**: 2026-09-11

Args:
    inputs: Input parameters validated against Operating_Heating_PowerInput schema

Returns:
    tuple[float, ...]: (p_wallplug, p_coupled, p_delivered)

Example:
    >>> inputs = Operating_Heating_PowerInput(...)
    >>> p_wallplug, p_coupled, p_delivered = run_operating_heating_power(inputs)
    """
    p_delivered = (inputs.p_required_in / inputs.eta_couple_in)
    return (
        (p_delivered / inputs.eta_source_in),  # p_wallplug
        inputs.p_required_in,  # p_coupled
        p_delivered,
    )
