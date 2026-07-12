"""Meier_Reactor_CostModule Module Wrapper

TEAx module for Meier_Reactor_Cost calculation.

HIF reactor plant direct cost (excluding driver and target factory).
Scales from the HYLIFE/Cascade reference design using thermal power
and accounts for multi-unit site savings.

Constants: C_r = $0.66B (Cascade reference at 1.67 GWt),
b = 0.49 (power scaling exponent).

*Source**: knowledge/sources/economic_studies_for_heavy_ion_fusion_electric_power_plants/output.md
*Ref**: Eq. 3 (lines 119-137)
*Basis**: Meier 1986 reactor cost scaling. Year-dollars: 1988$.

Inputs:
    - thermal_power_gw: thermal_power_gw parameter
    - num_units: num_units parameter

Outputs:
    - reactor_cost_billions: reactor_cost_billions result

SysML Source: /home/reid/1cfe/fusion-tea/exploration/ife_e2e/models/analyses/hif_economics.sysml:43

SysML Source: /home/reid/1cfe/fusion-tea/exploration/ife_e2e/models/analyses/hif_economics.sysml:43

GAP: Code generator does NOT implement calc logic - only wrapper structure.
Handwritten implementation required in handwritten/hif_economics/meier_reactor_cost_impl.py
"""

from pydantic import BaseModel, Field, RootModel
from simkit.core.base import ModuleBase, ModuleResult

from ife_tea.primitives import Float


class Meier_Reactor_CostInput(BaseModel):
    """Input model for Meier_Reactor_CostModule.

    Attributes:
        thermal_power_gw: thermal_power_gw input
        num_units: num_units input
    """
    thermal_power_gw: float = Field(..., description="thermal_power_gw input")
    num_units: float = Field(..., description="num_units input")


class Meier_Reactor_CostModule(ModuleBase[Meier_Reactor_CostInput, Float]):
    """TEAx module for Meier_Reactor_Cost calculation.

HIF reactor plant direct cost (excluding driver and target factory).
Scales from the HYLIFE/Cascade reference design using thermal power
and accounts for multi-unit site savings.

Constants: C_r = $0.66B (Cascade reference at 1.67 GWt),
b = 0.49 (power scaling exponent).

*Source**: knowledge/sources/economic_studies_for_heavy_ion_fusion_electric_power_plants/output.md
*Ref**: Eq. 3 (lines 119-137)
*Basis**: Meier 1986 reactor cost scaling. Year-dollars: 1988$.

Inputs:
    - thermal_power_gw: thermal_power_gw parameter
    - num_units: num_units parameter

Outputs:
    - reactor_cost_billions: reactor_cost_billions result

SysML Source: /home/reid/1cfe/fusion-tea/exploration/ife_e2e/models/analyses/hif_economics.sysml:43

    SysML Source: /home/reid/1cfe/fusion-tea/exploration/ife_e2e/models/analyses/hif_economics.sysml:43

    Calculation Specification:
        reactor_cost_billions = 0.66 * (thermal_power_gw / 1.67) ** 0.49 * (0.72 * num_units + 0.28)
        
Documentation:
HIF reactor plant direct cost (excluding driver and target factory).
Scales from the HYLIFE/Cascade reference design using thermal power
and accounts for multi-unit site savings.

Constants: C_r = $0.66B (Cascade reference at 1.67 GWt),
b = 0.49 (power scaling exponent).

*Source**: knowledge/sources/economic_studies_for_heavy_ion_fusion_electric_power_plants/output.md
*Ref**: Eq. 3 (lines 119-137)
*Basis**: Meier 1986 reactor cost scaling. Year-dollars: 1988$.

    IMPLEMENTATION: See ife_tea.handwritten.hif_economics.meier_reactor_cost_impl
    for manual implementation.

    NOTE: Single-output module - returns Float directly (no MultiOutput needed).
    """

    name: str = "Meier_Reactor_CostModule"
    version: str = "v0.1"

    def validate_and_fill_default(
        self, thermal_power_gw: float, num_units: float    ) -> Meier_Reactor_CostInput:
        """Validate inputs and fill defaults.

        Args:
            thermal_power_gw: thermal_power_gw input
            num_units: num_units input

        Returns:
            Validated input model
        """
        return Meier_Reactor_CostInput(thermal_power_gw=thermal_power_gw, num_units=num_units)

    def run(
        self, thermal_power_gw: float, num_units: float    ) -> ModuleResult[Float]:
        """Execute calculation.

        Args:
            thermal_power_gw: thermal_power_gw input
            num_units: num_units input

        Returns:
            Module result with Float (single-output mode)
        """
        # Validate inputs
        validated_inputs = self.validate_and_fill_default(thermal_power_gw, num_units)

        # Import handwritten implementation
        from ife_tea.handwritten.hif_economics.meier_reactor_cost_impl import (
            run_meier_reactor_cost,
        )

        # Execute implementation - returns single value
        reactor_cost_billions = run_meier_reactor_cost(validated_inputs)

        # Single output - return Float directly (RootModel[float])
        # TEAx assigns entire return value to the one channel declared in YAML
        return ModuleResult(data=Float(reactor_cost_billions))
