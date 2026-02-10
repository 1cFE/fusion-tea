"""LCOECalcModule Module Wrapper

TEAx module for LCOECalc calculation.

Levelized Cost of Electricity calculation.
Matches PyFECONS lcoe.py formula with inflation escalation on O&M and fuel.
LCOE = (C900000 + (C700000 + C800000) * (1 + inflation)^lifetime) / annual_energy

*Source**: PyFECONS /home/reid/PyFECONS/pyfecons/costing/calculations/lcoe.py:18-25
*Last Updated**: 2026-02-01

Inputs:
    - annualized_capital_cost: annualized_capital_cost parameter
    - annual_om_cost: annual_om_cost parameter
    - annual_fuel_cost: annual_fuel_cost parameter
    - yearly_inflation: yearly_inflation parameter
    - plant_lifetime: plant_lifetime parameter
    - annual_energy_mwh: annual_energy_mwh parameter

Outputs:
    - lcoe_per_mwh: lcoe_per_mwh result

SysML Source: models/tests/solar_battery/library.sysml:335

SysML Source: models/tests/solar_battery/library.sysml:335

GAP: Code generator does NOT implement calc logic - only wrapper structure.
Handwritten implementation required in handwritten/solarbatterylibrary/lcoecalc_impl.py
"""

from pydantic import BaseModel, Field, RootModel
from simkit.core.base import ModuleBase, ModuleResult

from solar_battery.primitives import Float


class LCOECalcInput(BaseModel):
    """Input model for LCOECalcModule.

    Attributes:
        annualized_capital_cost: annualized_capital_cost input
        annual_om_cost: annual_om_cost input
        annual_fuel_cost: annual_fuel_cost input
        yearly_inflation: yearly_inflation input
        plant_lifetime: plant_lifetime input
        annual_energy_mwh: annual_energy_mwh input
    """
    annualized_capital_cost: float = Field(..., description="annualized_capital_cost input")
    annual_om_cost: float = Field(..., description="annual_om_cost input")
    annual_fuel_cost: float = Field(..., description="annual_fuel_cost input")
    yearly_inflation: float = Field(..., description="yearly_inflation input")
    plant_lifetime: float = Field(..., description="plant_lifetime input")
    annual_energy_mwh: float = Field(..., description="annual_energy_mwh input")


class LCOECalcModule(ModuleBase[LCOECalcInput, Float]):
    """TEAx module for LCOECalc calculation.

Levelized Cost of Electricity calculation.
Matches PyFECONS lcoe.py formula with inflation escalation on O&M and fuel.
LCOE = (C900000 + (C700000 + C800000) * (1 + inflation)^lifetime) / annual_energy

*Source**: PyFECONS /home/reid/PyFECONS/pyfecons/costing/calculations/lcoe.py:18-25
*Last Updated**: 2026-02-01

Inputs:
    - annualized_capital_cost: annualized_capital_cost parameter
    - annual_om_cost: annual_om_cost parameter
    - annual_fuel_cost: annual_fuel_cost parameter
    - yearly_inflation: yearly_inflation parameter
    - plant_lifetime: plant_lifetime parameter
    - annual_energy_mwh: annual_energy_mwh parameter

Outputs:
    - lcoe_per_mwh: lcoe_per_mwh result

SysML Source: models/tests/solar_battery/library.sysml:335

    SysML Source: models/tests/solar_battery/library.sysml:335

    Calculation Specification:
        lcoe_per_mwh = annualized_capital_cost + annual_om_cost + annual_fuel_cost * 1.0 + yearly_inflation ** plant_lifetime / annual_energy_mwh
        
Documentation:
Levelized Cost of Electricity calculation.
Matches PyFECONS lcoe.py formula with inflation escalation on O&M and fuel.
LCOE = (C900000 + (C700000 + C800000) * (1 + inflation)^lifetime) / annual_energy

*Source**: PyFECONS /home/reid/PyFECONS/pyfecons/costing/calculations/lcoe.py:18-25
*Last Updated**: 2026-02-01

    IMPLEMENTATION: See solar_battery.handwritten.solarbatterylibrary.lcoecalc_impl
    for manual implementation.

    NOTE: Single-output module - returns Float directly (no MultiOutput needed).
    """

    name: str = "LCOECalcModule"
    version: str = "v0.1"

    def validate_and_fill_default(
        self, annualized_capital_cost: float, annual_om_cost: float, annual_fuel_cost: float, yearly_inflation: float, plant_lifetime: float, annual_energy_mwh: float    ) -> LCOECalcInput:
        """Validate inputs and fill defaults.

        Args:
            annualized_capital_cost: annualized_capital_cost input
            annual_om_cost: annual_om_cost input
            annual_fuel_cost: annual_fuel_cost input
            yearly_inflation: yearly_inflation input
            plant_lifetime: plant_lifetime input
            annual_energy_mwh: annual_energy_mwh input

        Returns:
            Validated input model
        """
        return LCOECalcInput(annualized_capital_cost=annualized_capital_cost, annual_om_cost=annual_om_cost, annual_fuel_cost=annual_fuel_cost, yearly_inflation=yearly_inflation, plant_lifetime=plant_lifetime, annual_energy_mwh=annual_energy_mwh)

    def run(
        self, annualized_capital_cost: float, annual_om_cost: float, annual_fuel_cost: float, yearly_inflation: float, plant_lifetime: float, annual_energy_mwh: float    ) -> ModuleResult[Float]:
        """Execute calculation.

        Args:
            annualized_capital_cost: annualized_capital_cost input
            annual_om_cost: annual_om_cost input
            annual_fuel_cost: annual_fuel_cost input
            yearly_inflation: yearly_inflation input
            plant_lifetime: plant_lifetime input
            annual_energy_mwh: annual_energy_mwh input

        Returns:
            Module result with Float (single-output mode)
        """
        # Validate inputs
        validated_inputs = self.validate_and_fill_default(annualized_capital_cost, annual_om_cost, annual_fuel_cost, yearly_inflation, plant_lifetime, annual_energy_mwh)

        # Import handwritten implementation
        from solar_battery.handwritten.solarbatterylibrary.lcoecalc_impl import (
            run_lcoecalc,
        )

        # Execute implementation - returns single value
        lcoe_per_mwh = run_lcoecalc(validated_inputs)

        # Single output - return Float directly (RootModel[float])
        # TEAx assigns entire return value to the one channel declared in YAML
        return ModuleResult(data=Float(lcoe_per_mwh))
