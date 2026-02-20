"""idiot_indexModule Module Wrapper

TEAx module for idiot_index calculation.

Inputs:
    - capital_cost: capital_cost parameter
    - raw_material_cost: raw_material_cost parameter

Outputs:
    - idiot_index: idiot_index result

SysML Source: unknown:0

SysML Source: unknown:0

GAP: Code generator does NOT implement calc logic - only wrapper structure.
Handwritten implementation required in handwritten/solarbatterydesign/solar_battery_plant/idiot_index_impl.py
"""

from pydantic import BaseModel, Field, RootModel
from simkit.core.base import ModuleBase, ModuleResult

from solar_battery_v5.primitives import Float


class idiot_indexInput(BaseModel):
    """Input model for idiot_indexModule.

    Attributes:
        capital_cost: capital_cost input
        raw_material_cost: raw_material_cost input
    """
    capital_cost: float = Field(..., description="capital_cost input")
    raw_material_cost: float = Field(..., description="raw_material_cost input")


class idiot_indexModule(ModuleBase[idiot_indexInput, Float]):
    """TEAx module for idiot_index calculation.

Inputs:
    - capital_cost: capital_cost parameter
    - raw_material_cost: raw_material_cost parameter

Outputs:
    - idiot_index: idiot_index result

SysML Source: unknown:0

    SysML Source: unknown:0

    Calculation Specification:
        capital_cost / raw_material_cost

    IMPLEMENTATION: See solar_battery_v5.handwritten.solarbatterydesign.solar_battery_plant.idiot_index_impl
    for manual implementation.

    NOTE: Single-output module - returns Float directly (no MultiOutput needed).
    """

    name: str = "idiot_indexModule"
    version: str = "v0.1"

    def validate_and_fill_default(
        self, capital_cost: float, raw_material_cost: float    ) -> idiot_indexInput:
        """Validate inputs and fill defaults.

        Args:
            capital_cost: capital_cost input
            raw_material_cost: raw_material_cost input

        Returns:
            Validated input model
        """
        return idiot_indexInput(capital_cost=capital_cost, raw_material_cost=raw_material_cost)

    def run(
        self, capital_cost: float, raw_material_cost: float    ) -> ModuleResult[Float]:
        """Execute calculation.

        Args:
            capital_cost: capital_cost input
            raw_material_cost: raw_material_cost input

        Returns:
            Module result with Float (single-output mode)
        """
        # Validate inputs
        validated_inputs = self.validate_and_fill_default(capital_cost, raw_material_cost)

        # Import handwritten implementation
        from solar_battery_v5.handwritten.solarbatterydesign.solar_battery_plant.idiot_index_impl import (
            run_idiot_index,
        )

        # Execute implementation - returns single value
        idiot_index = run_idiot_index(validated_inputs)

        # Single output - return Float directly (RootModel[float])
        # TEAx assigns entire return value to the one channel declared in YAML
        return ModuleResult(data=Float(idiot_index))
