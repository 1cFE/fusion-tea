"""Auto-generated implementation for Meier_HIF_Driver_Cost.

AUTO_IMPLEMENTED = True

SysML Source: /home/reid/1cfe/fusion-tea/exploration/ife_e2e/models/analyses/hif_economics.sysml:4

SysML Expressions:
    cost_billions = (0.32 + 0.088 * beam_energy_mj) * (1.25 + 0.05 * num_chambers) * (1.0 + 0.0088 * (rep_rate - 5.0))
    bank_energy_joules = beam_energy_mj * 1000000.0 / driver_efficiency
    gamma = cost_billions * 1000000000.0 / bank_energy_joules
    
Documentation:
Heavy-ion induction linac driver capital cost from Meier's
parametric formula. Returns gamma ($/J of bank energy) as the
primary output for use in Hawker's LCOE model. Also exposes
cost_billions as an intermediate for Meier's COE chain.

Input E_d is beam energy on target (MJ), consistent with Meier's
convention. The calc converts to bank energy using driver efficiency
to produce gamma in $/J of bank energy (Hawker's convention).

Constants: 0.32, 0.088 = baseline + marginal accelerator cost
coefficients (fit to induction linac studies). Reference: 5 Hz,
single chamber.

*Source**: knowledge/sources/economic_studies_for_heavy_ion_fusion_electric_power_plants/output.md
*Ref**: Eq. 5 (lines 173-192)
*Basis**: Meier 1986 parametric driver cost formula for HIF
induction linacs. Year-dollars: 1988$.
"""

AUTO_IMPLEMENTED = True

from ife_tea.modules.hif_economics.meier_hif_driver_cost import Meier_HIF_Driver_CostInput


def run_meier_hif_driver_cost(inputs: Meier_HIF_Driver_CostInput) -> tuple[float, float]:
    """Execute Meier_HIF_Driver_Cost calculation.

Heavy-ion induction linac driver capital cost from Meier's
parametric formula. Returns gamma ($/J of bank energy) as the
primary output for use in Hawker's LCOE model. Also exposes
cost_billions as an intermediate for Meier's COE chain.

Input E_d is beam energy on target (MJ), consistent with Meier's
convention. The calc converts to bank energy using driver efficiency
to produce gamma in $/J of bank energy (Hawker's convention).

Constants: 0.32, 0.088 = baseline + marginal accelerator cost
coefficients (fit to induction linac studies). Reference: 5 Hz,
single chamber.

*Source**: knowledge/sources/economic_studies_for_heavy_ion_fusion_electric_power_plants/output.md
*Ref**: Eq. 5 (lines 173-192)
*Basis**: Meier 1986 parametric driver cost formula for HIF
induction linacs. Year-dollars: 1988$.

SysML Source: /home/reid/1cfe/fusion-tea/exploration/ife_e2e/models/analyses/hif_economics.sysml:4

SysML Expressions:
    cost_billions = (0.32 + 0.088 * beam_energy_mj) * (1.25 + 0.05 * num_chambers) * (1.0 + 0.0088 * (rep_rate - 5.0))
    bank_energy_joules = beam_energy_mj * 1000000.0 / driver_efficiency
    gamma = cost_billions * 1000000000.0 / bank_energy_joules
    
Documentation:
Heavy-ion induction linac driver capital cost from Meier's
parametric formula. Returns gamma ($/J of bank energy) as the
primary output for use in Hawker's LCOE model. Also exposes
cost_billions as an intermediate for Meier's COE chain.

Input E_d is beam energy on target (MJ), consistent with Meier's
convention. The calc converts to bank energy using driver efficiency
to produce gamma in $/J of bank energy (Hawker's convention).

Constants: 0.32, 0.088 = baseline + marginal accelerator cost
coefficients (fit to induction linac studies). Reference: 5 Hz,
single chamber.

*Source**: knowledge/sources/economic_studies_for_heavy_ion_fusion_electric_power_plants/output.md
*Ref**: Eq. 5 (lines 173-192)
*Basis**: Meier 1986 parametric driver cost formula for HIF
induction linacs. Year-dollars: 1988$.

Args:
    inputs: Input parameters validated against Meier_HIF_Driver_CostInput schema

Returns:
    tuple[float, ...]: (cost_billions, gamma)

Example:
    >>> inputs = Meier_HIF_Driver_CostInput(...)
    >>> cost_billions, gamma = run_meier_hif_driver_cost(inputs)
    """
    bank_energy_joules = ((inputs.beam_energy_mj * 1000000.0) / inputs.driver_efficiency)
    cost_billions = (((0.32 + (0.088 * inputs.beam_energy_mj)) * (1.25 + (0.05 * inputs.num_chambers))) * (1.0 + (0.0088 * (inputs.rep_rate - 5.0))))
    gamma = ((cost_billions * 1000000000.0) / bank_energy_joules)
    return (
        cost_billions,
        gamma,
    )
