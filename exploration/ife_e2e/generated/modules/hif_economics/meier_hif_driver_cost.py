"""Meier_HIF_Driver_CostModule Module Wrapper

TEAx module for Meier_HIF_Driver_Cost calculation.

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

Inputs:
    - beam_energy_mj: beam_energy_mj parameter
    - driver_efficiency: driver_efficiency parameter
    - num_chambers: num_chambers parameter
    - rep_rate: rep_rate parameter

Outputs:
    - cost_billions: cost_billions result
    - gamma: gamma result

SysML Source: /home/reid/1cfe/fusion-tea/exploration/ife_e2e/models/analyses/hif_economics.sysml:4

SysML Source: /home/reid/1cfe/fusion-tea/exploration/ife_e2e/models/analyses/hif_economics.sysml:4

GAP: Code generator does NOT implement calc logic - only wrapper structure.
Handwritten implementation required in handwritten/hif_economics/meier_hif_driver_cost_impl.py
"""

from pydantic import BaseModel, Field, RootModel
from simkit.core.base import ModuleBase, ModuleResult

from ife_tea.primitives import Float
from ife_tea.schemas.meier_hif_driver_cost_output import Meier_HIF_Driver_CostOutput


class Meier_HIF_Driver_CostInput(BaseModel):
    """Input model for Meier_HIF_Driver_CostModule.

    Attributes:
        beam_energy_mj: beam_energy_mj input
        driver_efficiency: driver_efficiency input
        num_chambers: num_chambers input
        rep_rate: rep_rate input
    """
    beam_energy_mj: float = Field(..., description="beam_energy_mj input")
    driver_efficiency: float = Field(..., description="driver_efficiency input")
    num_chambers: float = Field(..., description="num_chambers input")
    rep_rate: float = Field(..., description="rep_rate input")


class Meier_HIF_Driver_CostModule(ModuleBase[Meier_HIF_Driver_CostInput, Meier_HIF_Driver_CostOutput]):
    """TEAx module for Meier_HIF_Driver_Cost calculation.

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

Inputs:
    - beam_energy_mj: beam_energy_mj parameter
    - driver_efficiency: driver_efficiency parameter
    - num_chambers: num_chambers parameter
    - rep_rate: rep_rate parameter

Outputs:
    - cost_billions: cost_billions result
    - gamma: gamma result

SysML Source: /home/reid/1cfe/fusion-tea/exploration/ife_e2e/models/analyses/hif_economics.sysml:4

    SysML Source: /home/reid/1cfe/fusion-tea/exploration/ife_e2e/models/analyses/hif_economics.sysml:4

    Calculation Specification:
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

    IMPLEMENTATION: See ife_tea.handwritten.hif_economics.meier_hif_driver_cost_impl
    for manual implementation.

    NOTE: Uses MultiOutput pattern for type-safe multi-output support.
    TEAx automatically extracts cost_billions, gamma fields to separate channels.
    """

    name: str = "Meier_HIF_Driver_CostModule"
    version: str = "v0.1"

    def validate_and_fill_default(
        self, beam_energy_mj: float, driver_efficiency: float, num_chambers: float, rep_rate: float    ) -> Meier_HIF_Driver_CostInput:
        """Validate inputs and fill defaults.

        Args:
            beam_energy_mj: beam_energy_mj input
            driver_efficiency: driver_efficiency input
            num_chambers: num_chambers input
            rep_rate: rep_rate input

        Returns:
            Validated input model
        """
        return Meier_HIF_Driver_CostInput(beam_energy_mj=beam_energy_mj, driver_efficiency=driver_efficiency, num_chambers=num_chambers, rep_rate=rep_rate)

    def run(
        self, beam_energy_mj: float, driver_efficiency: float, num_chambers: float, rep_rate: float    ) -> ModuleResult[Meier_HIF_Driver_CostOutput]:
        """Execute calculation.

        Args:
            beam_energy_mj: beam_energy_mj input
            driver_efficiency: driver_efficiency input
            num_chambers: num_chambers input
            rep_rate: rep_rate input

        Returns:
            Module result with Meier_HIF_Driver_CostOutput (cost_billions, gamma)
        """
        # Validate inputs
        validated_inputs = self.validate_and_fill_default(beam_energy_mj, driver_efficiency, num_chambers, rep_rate)

        # Import handwritten implementation
        from ife_tea.handwritten.hif_economics.meier_hif_driver_cost_impl import (
            run_meier_hif_driver_cost,
        )

        # Execute implementation - returns tuple of values
        cost_billions, gamma = run_meier_hif_driver_cost(validated_inputs)


        # Return MultiOutput container (TEAx auto-extracts to channels)
        # MultiOutput fields use plain float (not RootModel[float])
        return ModuleResult(
            data=Meier_HIF_Driver_CostOutput(
                cost_billions=cost_billions,
                gamma=gamma,
            )
        )
