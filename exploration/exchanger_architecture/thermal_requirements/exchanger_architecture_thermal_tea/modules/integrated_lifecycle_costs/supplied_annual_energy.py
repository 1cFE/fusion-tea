"""Supplied_Annual_EnergyModule Module Wrapper

TEAx module for Supplied_Annual_Energy calculation.

*Source**: work/active/WI-091_aries-integrated-lifecycle-cost/design.md. **Ref**: reviewed financial convention, roles and F1-F9 assumptions; work/orchestration/goals/aries-integrated-lcoe/evidence/source-boundary.md. **Basis**: conditional real USD2004 dated lifecycle accounts; assumptions are not scientific qualification. **Last Updated**: 2026-09-22.

Inputs:
    - net_power_in: net_power_in parameter
    - availability_in: availability_in parameter

Outputs:
    - annual_energy: annual_energy result

SysML Source: root-0/integrated_lifecycle_costs.sysml:73

SysML Source: root-0/integrated_lifecycle_costs.sysml:73

GAP: Code generator does NOT implement calc logic - only wrapper structure.
Handwritten implementation required in handwritten/integrated_lifecycle_costs/supplied_annual_energy_impl.py
"""

from pydantic import BaseModel, Field, RootModel
from simkit.core.base import ModuleBase, ModuleResult

from exchanger_architecture_thermal_tea.primitives import Float


class Supplied_Annual_EnergyInput(BaseModel):
    """Input model for Supplied_Annual_EnergyModule.

    Attributes:
        net_power_in: net_power_in input
        availability_in: availability_in input
    """
    net_power_in: float = Field(..., description="net_power_in input")
    availability_in: float = Field(..., description="availability_in input")


class Supplied_Annual_EnergyModule(ModuleBase[Supplied_Annual_EnergyInput, Float]):
    """TEAx module for Supplied_Annual_Energy calculation.

*Source**: work/active/WI-091_aries-integrated-lifecycle-cost/design.md. **Ref**: reviewed financial convention, roles and F1-F9 assumptions; work/orchestration/goals/aries-integrated-lcoe/evidence/source-boundary.md. **Basis**: conditional real USD2004 dated lifecycle accounts; assumptions are not scientific qualification. **Last Updated**: 2026-09-22.

Inputs:
    - net_power_in: net_power_in parameter
    - availability_in: availability_in parameter

Outputs:
    - annual_energy: annual_energy result

SysML Source: root-0/integrated_lifecycle_costs.sysml:73

    SysML Source: root-0/integrated_lifecycle_costs.sysml:73

    Calculation Specification:
        annual_energy = 8760.0 * net_power_in * availability_in
        
Documentation:
*Source**: work/active/WI-091_aries-integrated-lifecycle-cost/design.md. **Ref**: reviewed financial convention, roles and F1-F9 assumptions; work/orchestration/goals/aries-integrated-lcoe/evidence/source-boundary.md. **Basis**: conditional real USD2004 dated lifecycle accounts; assumptions are not scientific qualification. **Last Updated**: 2026-09-22.

    IMPLEMENTATION: See exchanger_architecture_thermal_tea.handwritten.integrated_lifecycle_costs.supplied_annual_energy_impl
    for manual implementation.

    NOTE: Single-output module - returns Float directly (no MultiOutput needed).
    """

    name: str = "Supplied_Annual_EnergyModule"
    version: str = "v0.1"

    def validate_and_fill_default(
        self, net_power_in: float, availability_in: float    ) -> Supplied_Annual_EnergyInput:
        """Validate inputs and fill defaults.

        Args:
            net_power_in: net_power_in input
            availability_in: availability_in input

        Returns:
            Validated input model
        """
        return Supplied_Annual_EnergyInput(net_power_in=net_power_in, availability_in=availability_in)

    def run(
        self, net_power_in: float, availability_in: float    ) -> ModuleResult[Float]:
        """Execute calculation.

        Args:
            net_power_in: net_power_in input
            availability_in: availability_in input

        Returns:
            Module result with Float (single-output mode)
        """
        # Validate inputs
        validated_inputs = self.validate_and_fill_default(net_power_in, availability_in)

        # Import handwritten implementation
        from exchanger_architecture_thermal_tea.handwritten.integrated_lifecycle_costs.supplied_annual_energy_impl import (
            run_supplied_annual_energy,
        )

        # Execute implementation - returns single value
        annual_energy = run_supplied_annual_energy(validated_inputs)

        # Single output - return Float directly (RootModel[float])
        # TEAx assigns entire return value to the one channel declared in YAML
        return ModuleResult(data=Float(annual_energy))
