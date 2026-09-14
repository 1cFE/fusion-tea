"""Native completion of mfe_cryo_plant::'Cryoplant Electrical Power'.

Authority: models/library/analyses/mfe_cryo_plant.sysml, normative temperature
domain and refrigeration equations (WI-053). Valid operation order, signed
loads, default dormant behavior and additive direct demand are retained.
"""
from stellarator_tea.modules.mfe_cryo_plant.cryoplant_electrical_power import Cryoplant_Electrical_PowerInput

AUTO_IMPLEMENTED = False


def run_cryoplant_electrical_power(inputs: Cryoplant_Electrical_PowerInput) -> float:
    """Return electrical demand after checking the temperature domain."""
    if not (inputs.T_cold > 0 and inputs.T_amb > inputs.T_cold):
        raise ValueError('Cryoplant Electrical Power: require 0 < T_cold < T_amb')
    p_cold = (inputs.q_nuc * inputs.vol_cold * 1.0e-6 + inputs.p_fixed) * inputs.f_uplift
    cop_carnot = inputs.T_cold / (inputs.T_amb - inputs.T_cold)
    cop = inputs.f_carnot * cop_carnot
    return p_cold / cop + inputs.p_direct
