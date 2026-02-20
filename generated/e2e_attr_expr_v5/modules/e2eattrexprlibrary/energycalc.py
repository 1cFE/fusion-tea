"""EnergyCalcModule Module Wrapper

TEAx module for EnergyCalc calculation.

Inputs:
    - power_mw: power_mw parameter
    - availability: availability parameter

Outputs:
    - annual_energy_mwh: annual_energy_mwh result

SysML Source: models/tests/e2e_attr_expr/library.sysml:31

SysML Source: models/tests/e2e_attr_expr/library.sysml:31

GAP: Code generator does NOT implement calc logic - only wrapper structure.
Handwritten implementation required in handwritten/e2eattrexprlibrary/energycalc_impl.py
"""

from pydantic import BaseModel, Field, RootModel
from simkit.core.base import ModuleBase, ModuleResult

from e2e_attr_expr_v5.primitives import Float


class EnergyCalcInput(BaseModel):
    """Input model for EnergyCalcModule.

    Attributes:
        power_mw: power_mw input
        availability: availability input
    """
    power_mw: float = Field(..., description="power_mw input")
    availability: float = Field(..., description="availability input")


class EnergyCalcModule(ModuleBase[EnergyCalcInput, Float]):
    """TEAx module for EnergyCalc calculation.

Inputs:
    - power_mw: power_mw parameter
    - availability: availability parameter

Outputs:
    - annual_energy_mwh: annual_energy_mwh result

SysML Source: models/tests/e2e_attr_expr/library.sysml:31

    SysML Source: models/tests/e2e_attr_expr/library.sysml:31

    Calculation Specification:
        annual_energy_mwh = LiteralRationalEvaluation() * power_mw * availability

    IMPLEMENTATION: See e2e_attr_expr_v5.handwritten.e2eattrexprlibrary.energycalc_impl
    for manual implementation.

    NOTE: Single-output module - returns Float directly (no MultiOutput needed).
    """

    name: str = "EnergyCalcModule"
    version: str = "v0.1"

    def validate_and_fill_default(
        self, power_mw: float, availability: float    ) -> EnergyCalcInput:
        """Validate inputs and fill defaults.

        Args:
            power_mw: power_mw input
            availability: availability input

        Returns:
            Validated input model
        """
        return EnergyCalcInput(power_mw=power_mw, availability=availability)

    def run(
        self, power_mw: float, availability: float    ) -> ModuleResult[Float]:
        """Execute calculation.

        Args:
            power_mw: power_mw input
            availability: availability input

        Returns:
            Module result with Float (single-output mode)
        """
        # Validate inputs
        validated_inputs = self.validate_and_fill_default(power_mw, availability)

        # Import handwritten implementation
        from e2e_attr_expr_v5.handwritten.e2eattrexprlibrary.energycalc_impl import (
            run_energycalc,
        )

        # Execute implementation - returns single value
        annual_energy_mwh = run_energycalc(validated_inputs)

        # Single output - return Float directly (RootModel[float])
        # TEAx assigns entire return value to the one channel declared in YAML
        return ModuleResult(data=Float(annual_energy_mwh))
