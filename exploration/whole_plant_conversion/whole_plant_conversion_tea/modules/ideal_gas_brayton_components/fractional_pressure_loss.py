"""Fractional_Pressure_LossModule Module Wrapper

TEAx module for Fractional_Pressure_Loss calculation.

Source: work/active/WI-087_aries-nominal-brayton-component-cycle/spec.md. Ref: accepted source/design review in work/orchestration/aries-transfer-experiment/evidence/power-conversion-review.md. Basis: AGENT nominal ideal-gas component approximation. pout=pin*(1-fraction). Supplied nominal fractional loss; not a flow-dependent hydraulic model. Units: K, MPa, kg/s, J/(kg K), MW; efficiencies dimensionless. Typed completion enforces finite outputs and the explicit domain in the spec. Last Updated: 2026-09-21.

Inputs:
    - pressure_in: pressure_in parameter
    - loss_fraction_in: loss_fraction_in parameter

Outputs:
    - pressure_out: pressure_out result

SysML Source: root-0/ideal_gas_brayton_components.sysml:52

SysML Source: root-0/ideal_gas_brayton_components.sysml:52

GAP: Code generator does NOT implement calc logic - only wrapper structure.
Handwritten implementation required in handwritten/ideal_gas_brayton_components/fractional_pressure_loss_impl.py
"""

from pydantic import BaseModel, Field, RootModel
from simkit.core.base import ModuleBase, ModuleResult

from whole_plant_conversion_tea.primitives import Float


class Fractional_Pressure_LossInput(BaseModel):
    """Input model for Fractional_Pressure_LossModule.

    Attributes:
        pressure_in: pressure_in input
        loss_fraction_in: loss_fraction_in input
    """
    pressure_in: float = Field(..., description="pressure_in input")
    loss_fraction_in: float = Field(..., description="loss_fraction_in input")


class Fractional_Pressure_LossModule(ModuleBase[Fractional_Pressure_LossInput, Float]):
    """TEAx module for Fractional_Pressure_Loss calculation.

Source: work/active/WI-087_aries-nominal-brayton-component-cycle/spec.md. Ref: accepted source/design review in work/orchestration/aries-transfer-experiment/evidence/power-conversion-review.md. Basis: AGENT nominal ideal-gas component approximation. pout=pin*(1-fraction). Supplied nominal fractional loss; not a flow-dependent hydraulic model. Units: K, MPa, kg/s, J/(kg K), MW; efficiencies dimensionless. Typed completion enforces finite outputs and the explicit domain in the spec. Last Updated: 2026-09-21.

Inputs:
    - pressure_in: pressure_in parameter
    - loss_fraction_in: loss_fraction_in parameter

Outputs:
    - pressure_out: pressure_out result

SysML Source: root-0/ideal_gas_brayton_components.sysml:52

    SysML Source: root-0/ideal_gas_brayton_components.sysml:52

    Calculation Specification:
        See documentation:
Source: work/active/WI-087_aries-nominal-brayton-component-cycle/spec.md. Ref: accepted source/design review in work/orchestration/aries-transfer-experiment/evidence/power-conversion-review.md. Basis: AGENT nominal ideal-gas component approximation. pout=pin*(1-fraction). Supplied nominal fractional loss; not a flow-dependent hydraulic model. Units: K, MPa, kg/s, J/(kg K), MW; efficiencies dimensionless. Typed completion enforces finite outputs and the explicit domain in the spec. Last Updated: 2026-09-21.

    IMPLEMENTATION: See whole_plant_conversion_tea.handwritten.ideal_gas_brayton_components.fractional_pressure_loss_impl
    for manual implementation.

    NOTE: Single-output module - returns Float directly (no MultiOutput needed).
    """

    name: str = "Fractional_Pressure_LossModule"
    version: str = "v0.1"

    def validate_and_fill_default(
        self, pressure_in: float, loss_fraction_in: float    ) -> Fractional_Pressure_LossInput:
        """Validate inputs and fill defaults.

        Args:
            pressure_in: pressure_in input
            loss_fraction_in: loss_fraction_in input

        Returns:
            Validated input model
        """
        return Fractional_Pressure_LossInput(pressure_in=pressure_in, loss_fraction_in=loss_fraction_in)

    def run(
        self, pressure_in: float, loss_fraction_in: float    ) -> ModuleResult[Float]:
        """Execute calculation.

        Args:
            pressure_in: pressure_in input
            loss_fraction_in: loss_fraction_in input

        Returns:
            Module result with Float (single-output mode)
        """
        # Validate inputs
        validated_inputs = self.validate_and_fill_default(pressure_in, loss_fraction_in)

        # Import handwritten implementation
        from whole_plant_conversion_tea.handwritten.ideal_gas_brayton_components.fractional_pressure_loss_impl import (
            run_fractional_pressure_loss,
        )

        # Execute implementation - returns single value
        pressure_out = run_fractional_pressure_loss(validated_inputs)

        # Single output - return Float directly (RootModel[float])
        # TEAx assigns entire return value to the one channel declared in YAML
        return ModuleResult(data=Float(pressure_out))
