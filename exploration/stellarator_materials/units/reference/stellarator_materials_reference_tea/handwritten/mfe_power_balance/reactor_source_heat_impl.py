"""Auto-generated implementation for Reactor_Source_Heat.

AUTO_IMPLEMENTED = True

SysML Source: root-0/analyses/mfe_power_balance.sysml:174

SysML Expressions:
    p_alpha = 3.52 / 17.58 * p_nrl
    p_neutron = p_nrl - p_alpha
    q_source = mn_in * p_neutron + p_alpha + p_input_in
    
Documentation:
The reactor's heat with no pump credit (WI-045, goal plant-closure):
  q_source = mn * p_neutron + p_alpha + p_input
the first three terms of 'MFE Power Balance Calc''s thermal sum in the
same order, published as its own producer so the primary loop can size
its flow from it without a dependency cycle (the power balance consumes
the loop's recovered heat). The alpha/neutron split is the inlined D-T
ratio 3.52/17.58 exactly as the power balance forms it, so q_source
equals the power balance's own partial sum to the bit.
*Source**: models/library/analyses/mfe_power_balance.sysml ('MFE Power Balance Calc', p_th)
*Ref**: WI-019 collapse p_th = mn*p_neutron + p_alpha + p_input + (recovered pump heat)
*Basis**: reactor source heat before the loop's own recovered work; the heat ledger's one source (packet § 5)
"""

AUTO_IMPLEMENTED = True

from stellarator_materials_reference_tea.modules.mfe_power_balance.reactor_source_heat import Reactor_Source_HeatInput


def run_reactor_source_heat(inputs: Reactor_Source_HeatInput) -> float:
    """Execute Reactor_Source_Heat calculation.

The reactor's heat with no pump credit (WI-045, goal plant-closure):
  q_source = mn * p_neutron + p_alpha + p_input
the first three terms of 'MFE Power Balance Calc''s thermal sum in the
same order, published as its own producer so the primary loop can size
its flow from it without a dependency cycle (the power balance consumes
the loop's recovered heat). The alpha/neutron split is the inlined D-T
ratio 3.52/17.58 exactly as the power balance forms it, so q_source
equals the power balance's own partial sum to the bit.
*Source**: models/library/analyses/mfe_power_balance.sysml ('MFE Power Balance Calc', p_th)
*Ref**: WI-019 collapse p_th = mn*p_neutron + p_alpha + p_input + (recovered pump heat)
*Basis**: reactor source heat before the loop's own recovered work; the heat ledger's one source (packet § 5)

SysML Source: root-0/analyses/mfe_power_balance.sysml:174

SysML Expressions:
    p_alpha = 3.52 / 17.58 * p_nrl
    p_neutron = p_nrl - p_alpha
    q_source = mn_in * p_neutron + p_alpha + p_input_in
    
Documentation:
The reactor's heat with no pump credit (WI-045, goal plant-closure):
  q_source = mn * p_neutron + p_alpha + p_input
the first three terms of 'MFE Power Balance Calc''s thermal sum in the
same order, published as its own producer so the primary loop can size
its flow from it without a dependency cycle (the power balance consumes
the loop's recovered heat). The alpha/neutron split is the inlined D-T
ratio 3.52/17.58 exactly as the power balance forms it, so q_source
equals the power balance's own partial sum to the bit.
*Source**: models/library/analyses/mfe_power_balance.sysml ('MFE Power Balance Calc', p_th)
*Ref**: WI-019 collapse p_th = mn*p_neutron + p_alpha + p_input + (recovered pump heat)
*Basis**: reactor source heat before the loop's own recovered work; the heat ledger's one source (packet § 5)

Args:
    inputs: Input parameters validated against Reactor_Source_HeatInput schema

Returns:
    float: q_source

Example:
    >>> inputs = Reactor_Source_HeatInput(...)
    >>> result = run_reactor_source_heat(inputs)
    """
    p_alpha = ((3.52 / 17.58) * inputs.p_nrl)
    p_neutron = (inputs.p_nrl - p_alpha)
    return (((inputs.mn_in * p_neutron) + p_alpha) + inputs.p_input_in)
