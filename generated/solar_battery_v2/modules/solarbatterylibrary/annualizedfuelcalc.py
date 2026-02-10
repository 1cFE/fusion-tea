"""AnnualizedFuelCalcModule Module Wrapper

TEAx module for AnnualizedFuelCalc calculation.

Annualized fuel cost.
For solar: fuel_unit_cost = 0, fuel_consumption = 0 → annual_fuel_cost = 0.
Included for pipeline completeness (fusion plants have non-zero fuel costs).

*Source**: PyFECONS /home/reid/PyFECONS/pyfecons/costing/calculations/cas80_annualized_fuel.py:14
*Last Updated**: 2026-02-01

Inputs:
    - fuel_unit_cost: fuel_unit_cost parameter
    - fuel_consumption: fuel_consumption parameter

Outputs:
    - annual_fuel_cost: annual_fuel_cost result

SysML Source: models/tests/solar_battery/library.sysml:298

SysML Source: models/tests/solar_battery/library.sysml:298

GAP: Code generator does NOT implement calc logic - only wrapper structure.
Handwritten implementation required in handwritten/solarbatterylibrary/annualizedfuelcalc_impl.py
"""

from pydantic import BaseModel, Field, RootModel
from simkit.core.base import ModuleBase, ModuleResult

from solar_battery_v2.primitives import Float


class AnnualizedFuelCalcInput(BaseModel):
    """Input model for AnnualizedFuelCalcModule.

    Attributes:
        fuel_unit_cost: fuel_unit_cost input
        fuel_consumption: fuel_consumption input
    """
    fuel_unit_cost: float = Field(..., description="fuel_unit_cost input")
    fuel_consumption: float = Field(..., description="fuel_consumption input")


class AnnualizedFuelCalcModule(ModuleBase[AnnualizedFuelCalcInput, Float]):
    """TEAx module for AnnualizedFuelCalc calculation.

Annualized fuel cost.
For solar: fuel_unit_cost = 0, fuel_consumption = 0 → annual_fuel_cost = 0.
Included for pipeline completeness (fusion plants have non-zero fuel costs).

*Source**: PyFECONS /home/reid/PyFECONS/pyfecons/costing/calculations/cas80_annualized_fuel.py:14
*Last Updated**: 2026-02-01

Inputs:
    - fuel_unit_cost: fuel_unit_cost parameter
    - fuel_consumption: fuel_consumption parameter

Outputs:
    - annual_fuel_cost: annual_fuel_cost result

SysML Source: models/tests/solar_battery/library.sysml:298

    SysML Source: models/tests/solar_battery/library.sysml:298

    Calculation Specification:
        annual_fuel_cost = fuel_unit_cost * fuel_consumption
        
Documentation:
Annualized fuel cost.
For solar: fuel_unit_cost = 0, fuel_consumption = 0 → annual_fuel_cost = 0.
Included for pipeline completeness (fusion plants have non-zero fuel costs).

*Source**: PyFECONS /home/reid/PyFECONS/pyfecons/costing/calculations/cas80_annualized_fuel.py:14
*Last Updated**: 2026-02-01

    IMPLEMENTATION: See solar_battery_v2.handwritten.solarbatterylibrary.annualizedfuelcalc_impl
    for manual implementation.

    NOTE: Single-output module - returns Float directly (no MultiOutput needed).
    """

    name: str = "AnnualizedFuelCalcModule"
    version: str = "v0.1"

    def validate_and_fill_default(
        self, fuel_unit_cost: float, fuel_consumption: float    ) -> AnnualizedFuelCalcInput:
        """Validate inputs and fill defaults.

        Args:
            fuel_unit_cost: fuel_unit_cost input
            fuel_consumption: fuel_consumption input

        Returns:
            Validated input model
        """
        return AnnualizedFuelCalcInput(fuel_unit_cost=fuel_unit_cost, fuel_consumption=fuel_consumption)

    def run(
        self, fuel_unit_cost: float, fuel_consumption: float    ) -> ModuleResult[Float]:
        """Execute calculation.

        Args:
            fuel_unit_cost: fuel_unit_cost input
            fuel_consumption: fuel_consumption input

        Returns:
            Module result with Float (single-output mode)
        """
        # Validate inputs
        validated_inputs = self.validate_and_fill_default(fuel_unit_cost, fuel_consumption)

        # Import handwritten implementation
        from solar_battery_v2.handwritten.solarbatterylibrary.annualizedfuelcalc_impl import (
            run_annualizedfuelcalc,
        )

        # Execute implementation - returns single value
        annual_fuel_cost = run_annualizedfuelcalc(validated_inputs)

        # Single output - return Float directly (RootModel[float])
        # TEAx assigns entire return value to the one channel declared in YAML
        return ModuleResult(data=Float(annual_fuel_cost))
