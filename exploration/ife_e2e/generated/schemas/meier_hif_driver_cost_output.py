from pydantic import Field
from simkit.config.schema import MultiOutput

class Meier_HIF_Driver_CostOutput(MultiOutput):
    """Multi-output container for Meier_HIF_Driver_Cost.

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
    """
    cost_billions: float = Field(description="cost_billions output")
    gamma: float = Field(description="gamma output")
