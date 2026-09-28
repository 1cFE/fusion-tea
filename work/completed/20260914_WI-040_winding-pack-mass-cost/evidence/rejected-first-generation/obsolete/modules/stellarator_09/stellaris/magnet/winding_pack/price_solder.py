"""price_solderModule Module Wrapper

TEAx module for price_solder calculation.

Outputs:
    - price_solder: price_solder result

SysML Source: root-0/designs/stellarator_09/stellarator_plant.sysml:316

SysML Source: root-0/designs/stellarator_09/stellarator_plant.sysml:316

GAP: Code generator does NOT implement calc logic - only wrapper structure.
Handwritten implementation required in handwritten/stellarator_09/stellaris/magnet/winding_pack/price_solder_impl.py
"""

from pydantic import BaseModel, Field, RootModel
from simkit.core.base import ModuleBase, ModuleResult

from stellarator_tea.primitives import Float


class price_solderInput(BaseModel):
    """Input model for price_solderModule.

    Attributes:
    """


class price_solderModule(ModuleBase[price_solderInput, Float]):
    """TEAx module for price_solder calculation.

Outputs:
    - price_solder: price_solder result

SysML Source: root-0/designs/stellarator_09/stellarator_plant.sysml:316

    SysML Source: root-0/designs/stellarator_09/stellarator_plant.sysml:316

    Calculation Specification:

    IMPLEMENTATION: See stellarator_tea.handwritten.stellarator_09.stellaris.magnet.winding_pack.price_solder_impl
    for manual implementation.

    NOTE: Single-output module - returns Float directly (no MultiOutput needed).
    """

    name: str = "price_solderModule"
    version: str = "v0.1"

    def validate_and_fill_default(
        self,     ) -> price_solderInput:
        """Validate inputs and fill defaults.

        Args:

        Returns:
            Validated input model
        """
        return price_solderInput()

    def run(
        self,     ) -> ModuleResult[Float]:
        """Execute calculation.

        Args:

        Returns:
            Module result with Float (single-output mode)
        """
        # Validate inputs
        validated_inputs = self.validate_and_fill_default()

        # Import handwritten implementation
        from stellarator_tea.handwritten.stellarator_09.stellaris.magnet.winding_pack.price_solder_impl import (
            run_price_solder,
        )

        # Execute implementation - returns single value
        price_solder = run_price_solder(validated_inputs)

        # Single output - return Float directly (RootModel[float])
        # TEAx assigns entire return value to the one channel declared in YAML
        return ModuleResult(data=Float(price_solder))
