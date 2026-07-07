"""Meier_Total_Capital_CostModule Module Wrapper

TEAx module for Meier_Total_Capital_Cost calculation.

Total plant capital cost including indirect cost multiplier.
Factor 1.83 = total-to-direct cost ratio (midway between coal
at 1.53 and nuclear-best at 2.07).

*Source**: knowledge/sources/economic_studies_for_heavy_ion_fusion_electric_power_plants/output.md
*Ref**: Eq. 2 (lines 102-117)
*Basis**: Meier 1986 indirect cost multiplier. Year-dollars: 1988$.

Inputs:
    - reactor_cost: reactor_cost parameter
    - driver_cost: driver_cost parameter
    - target_factory_cost: target_factory_cost parameter

Outputs:
    - total_capital_billions: total_capital_billions result

SysML Source: /home/reid/1cfe/fusion-tea/exploration/ife_e2e/models/analyses/hif_economics.sysml:65

SysML Source: /home/reid/1cfe/fusion-tea/exploration/ife_e2e/models/analyses/hif_economics.sysml:65

GAP: Code generator does NOT implement calc logic - only wrapper structure.
Handwritten implementation required in handwritten/hif_economics/meier_total_capital_cost_impl.py
"""

from pydantic import BaseModel, Field, RootModel
from simkit.core.base import ModuleBase, ModuleResult

from ife_tea.primitives import Float


class Meier_Total_Capital_CostInput(BaseModel):
    """Input model for Meier_Total_Capital_CostModule.

    Attributes:
        reactor_cost: reactor_cost input
        driver_cost: driver_cost input
        target_factory_cost: target_factory_cost input
    """
    reactor_cost: float = Field(..., description="reactor_cost input")
    driver_cost: float = Field(..., description="driver_cost input")
    target_factory_cost: float = Field(..., description="target_factory_cost input")


class Meier_Total_Capital_CostModule(ModuleBase[Meier_Total_Capital_CostInput, Float]):
    """TEAx module for Meier_Total_Capital_Cost calculation.

Total plant capital cost including indirect cost multiplier.
Factor 1.83 = total-to-direct cost ratio (midway between coal
at 1.53 and nuclear-best at 2.07).

*Source**: knowledge/sources/economic_studies_for_heavy_ion_fusion_electric_power_plants/output.md
*Ref**: Eq. 2 (lines 102-117)
*Basis**: Meier 1986 indirect cost multiplier. Year-dollars: 1988$.

Inputs:
    - reactor_cost: reactor_cost parameter
    - driver_cost: driver_cost parameter
    - target_factory_cost: target_factory_cost parameter

Outputs:
    - total_capital_billions: total_capital_billions result

SysML Source: /home/reid/1cfe/fusion-tea/exploration/ife_e2e/models/analyses/hif_economics.sysml:65

    SysML Source: /home/reid/1cfe/fusion-tea/exploration/ife_e2e/models/analyses/hif_economics.sysml:65

    Calculation Specification:
        total_capital_billions = 1.83 * (reactor_cost + driver_cost + target_factory_cost)
        
Documentation:
Total plant capital cost including indirect cost multiplier.
Factor 1.83 = total-to-direct cost ratio (midway between coal
at 1.53 and nuclear-best at 2.07).

*Source**: knowledge/sources/economic_studies_for_heavy_ion_fusion_electric_power_plants/output.md
*Ref**: Eq. 2 (lines 102-117)
*Basis**: Meier 1986 indirect cost multiplier. Year-dollars: 1988$.

    IMPLEMENTATION: See ife_tea.handwritten.hif_economics.meier_total_capital_cost_impl
    for manual implementation.

    NOTE: Single-output module - returns Float directly (no MultiOutput needed).
    """

    name: str = "Meier_Total_Capital_CostModule"
    version: str = "v0.1"

    def validate_and_fill_default(
        self, reactor_cost: float, driver_cost: float, target_factory_cost: float    ) -> Meier_Total_Capital_CostInput:
        """Validate inputs and fill defaults.

        Args:
            reactor_cost: reactor_cost input
            driver_cost: driver_cost input
            target_factory_cost: target_factory_cost input

        Returns:
            Validated input model
        """
        return Meier_Total_Capital_CostInput(reactor_cost=reactor_cost, driver_cost=driver_cost, target_factory_cost=target_factory_cost)

    def run(
        self, reactor_cost: float, driver_cost: float, target_factory_cost: float    ) -> ModuleResult[Float]:
        """Execute calculation.

        Args:
            reactor_cost: reactor_cost input
            driver_cost: driver_cost input
            target_factory_cost: target_factory_cost input

        Returns:
            Module result with Float (single-output mode)
        """
        # Validate inputs
        validated_inputs = self.validate_and_fill_default(reactor_cost, driver_cost, target_factory_cost)

        # Import handwritten implementation
        from ife_tea.handwritten.hif_economics.meier_total_capital_cost_impl import (
            run_meier_total_capital_cost,
        )

        # Execute implementation - returns single value
        total_capital_billions = run_meier_total_capital_cost(validated_inputs)

        # Single output - return Float directly (RootModel[float])
        # TEAx assigns entire return value to the one channel declared in YAML
        return ModuleResult(data=Float(total_capital_billions))
