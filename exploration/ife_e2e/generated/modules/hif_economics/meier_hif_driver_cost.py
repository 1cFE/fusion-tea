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
*Reference**: images/page_004_eq_0.png, Eq. 5
*Last Updated**: 2026-09-10
*Basis**: Meier 1986 parametric driver cost formula for HIF
induction linacs. Year-dollars: 1988$.

Inputs:
    - beam_energy_mj_in: beam_energy_mj_in parameter
    - num_chambers_in: num_chambers_in parameter
    - rep_rate: rep_rate parameter
    - driver_efficiency: driver_efficiency parameter

Outputs:
    - gamma: gamma result
    - bank_energy_joules: bank_energy_joules result
    - cost_billions: cost_billions result

SysML Source: root-0/analyses/hif_economics.sysml:4

SysML Source: root-0/analyses/hif_economics.sysml:4

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
        beam_energy_mj_in: beam_energy_mj_in input
        num_chambers_in: num_chambers_in input
        rep_rate: rep_rate input
        driver_efficiency: driver_efficiency input
    """
    beam_energy_mj_in: float = Field(..., description="beam_energy_mj_in input")
    num_chambers_in: float = Field(..., description="num_chambers_in input")
    rep_rate: float = Field(..., description="rep_rate input")
    driver_efficiency: float = Field(..., description="driver_efficiency input")


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
*Reference**: images/page_004_eq_0.png, Eq. 5
*Last Updated**: 2026-09-10
*Basis**: Meier 1986 parametric driver cost formula for HIF
induction linacs. Year-dollars: 1988$.

Inputs:
    - beam_energy_mj_in: beam_energy_mj_in parameter
    - num_chambers_in: num_chambers_in parameter
    - rep_rate: rep_rate parameter
    - driver_efficiency: driver_efficiency parameter

Outputs:
    - gamma: gamma result
    - bank_energy_joules: bank_energy_joules result
    - cost_billions: cost_billions result

SysML Source: root-0/analyses/hif_economics.sysml:4

    SysML Source: root-0/analyses/hif_economics.sysml:4

    Calculation Specification:
        cost_billions = (0.32 + 0.088 * beam_energy_mj_in) * (1.25 + 0.05 * num_chambers_in) * (1.0 + 0.0088 * (rep_rate - 5.0))
        bank_energy_joules = beam_energy_mj_in * 1000000.0 / driver_efficiency
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
*Reference**: images/page_004_eq_0.png, Eq. 5
*Last Updated**: 2026-09-10
*Basis**: Meier 1986 parametric driver cost formula for HIF
induction linacs. Year-dollars: 1988$.

    IMPLEMENTATION: See ife_tea.handwritten.hif_economics.meier_hif_driver_cost_impl
    for manual implementation.

    NOTE: Uses MultiOutput pattern for type-safe multi-output support.
    TEAx automatically extracts gamma, bank_energy_joules, cost_billions fields to separate channels.
    """

    name: str = "Meier_HIF_Driver_CostModule"
    version: str = "v0.1"

    def validate_and_fill_default(
        self, beam_energy_mj_in: float, num_chambers_in: float, rep_rate: float, driver_efficiency: float    ) -> Meier_HIF_Driver_CostInput:
        """Validate inputs and fill defaults.

        Args:
            beam_energy_mj_in: beam_energy_mj_in input
            num_chambers_in: num_chambers_in input
            rep_rate: rep_rate input
            driver_efficiency: driver_efficiency input

        Returns:
            Validated input model
        """
        return Meier_HIF_Driver_CostInput(beam_energy_mj_in=beam_energy_mj_in, num_chambers_in=num_chambers_in, rep_rate=rep_rate, driver_efficiency=driver_efficiency)

    def run(
        self, beam_energy_mj_in: float, num_chambers_in: float, rep_rate: float, driver_efficiency: float    ) -> ModuleResult[Meier_HIF_Driver_CostOutput]:
        """Execute calculation.

        Args:
            beam_energy_mj_in: beam_energy_mj_in input
            num_chambers_in: num_chambers_in input
            rep_rate: rep_rate input
            driver_efficiency: driver_efficiency input

        Returns:
            Module result with Meier_HIF_Driver_CostOutput (gamma, bank_energy_joules, cost_billions)
        """
        # Validate inputs
        validated_inputs = self.validate_and_fill_default(beam_energy_mj_in, num_chambers_in, rep_rate, driver_efficiency)

        # Import handwritten implementation
        from ife_tea.handwritten.hif_economics.meier_hif_driver_cost_impl import (
            run_meier_hif_driver_cost,
        )

        # Execute implementation - returns tuple of values
        gamma, bank_energy_joules, cost_billions = run_meier_hif_driver_cost(validated_inputs)


        # Return MultiOutput container (TEAx auto-extracts to channels)
        # MultiOutput fields use plain float (not RootModel[float])
        return ModuleResult(
            data=Meier_HIF_Driver_CostOutput(
                gamma=gamma,
                bank_energy_joules=bank_energy_joules,
                cost_billions=cost_billions,
            )
        )
