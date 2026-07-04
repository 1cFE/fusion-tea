"""AnnualizedFinancialCalcModule Module Wrapper

TEAx module for AnnualizedFinancialCalc calculation.

Annualized financial cost using Capital Recovery Factor.
CRF = r * (1+r)^n / ((1+r)^n - 1)
Computes CRF from discount_rate and plant_lifetime rather than using
PyFECONS's hardcoded 0.09 default.

*Source**: PyFECONS /home/reid/PyFECONS/pyfecons/costing/calculations/cas90_annualized_financial.py:14
*Last Updated**: 2026-02-01

Inputs:
    - total_capex: total_capex parameter
    - discount_rate: discount_rate parameter
    - plant_lifetime: plant_lifetime parameter

Outputs:
    - capital_recovery_factor: capital_recovery_factor result
    - annualized_capital_cost: annualized_capital_cost result

SysML Source: solar_battery_model/library.sysml:314

SysML Source: solar_battery_model/library.sysml:314

GAP: Code generator does NOT implement calc logic - only wrapper structure.
Handwritten implementation required in handwritten/solarbatterylibrary/annualizedfinancialcalc_impl.py
"""

from pydantic import BaseModel, Field, RootModel
from simkit.core.base import ModuleBase, ModuleResult

from solar_battery_tea.primitives import Float
from solar_battery_tea.schemas.annualizedfinancialcalc_output import AnnualizedFinancialCalcOutput


class AnnualizedFinancialCalcInput(BaseModel):
    """Input model for AnnualizedFinancialCalcModule.

    Attributes:
        total_capex: total_capex input
        discount_rate: discount_rate input
        plant_lifetime: plant_lifetime input
    """
    total_capex: float = Field(..., description="total_capex input")
    discount_rate: float = Field(..., description="discount_rate input")
    plant_lifetime: float = Field(..., description="plant_lifetime input")


class AnnualizedFinancialCalcModule(ModuleBase[AnnualizedFinancialCalcInput, AnnualizedFinancialCalcOutput]):
    """TEAx module for AnnualizedFinancialCalc calculation.

Annualized financial cost using Capital Recovery Factor.
CRF = r * (1+r)^n / ((1+r)^n - 1)
Computes CRF from discount_rate and plant_lifetime rather than using
PyFECONS's hardcoded 0.09 default.

*Source**: PyFECONS /home/reid/PyFECONS/pyfecons/costing/calculations/cas90_annualized_financial.py:14
*Last Updated**: 2026-02-01

Inputs:
    - total_capex: total_capex parameter
    - discount_rate: discount_rate parameter
    - plant_lifetime: plant_lifetime parameter

Outputs:
    - capital_recovery_factor: capital_recovery_factor result
    - annualized_capital_cost: annualized_capital_cost result

SysML Source: solar_battery_model/library.sysml:314

    SysML Source: solar_battery_model/library.sysml:314

    Calculation Specification:
        capital_recovery_factor = discount_rate * LiteralRationalEvaluation() + discount_rate ** plant_lifetime / LiteralRationalEvaluation() + discount_rate ** plant_lifetime - LiteralRationalEvaluation()
        annualized_capital_cost = capital_recovery_factor * total_capex
        
Documentation:
Annualized financial cost using Capital Recovery Factor.
CRF = r * (1+r)^n / ((1+r)^n - 1)
Computes CRF from discount_rate and plant_lifetime rather than using
PyFECONS's hardcoded 0.09 default.

*Source**: PyFECONS /home/reid/PyFECONS/pyfecons/costing/calculations/cas90_annualized_financial.py:14
*Last Updated**: 2026-02-01

    IMPLEMENTATION: See solar_battery_tea.handwritten.solarbatterylibrary.annualizedfinancialcalc_impl
    for manual implementation.

    NOTE: Uses MultiOutput pattern for type-safe multi-output support.
    TEAx automatically extracts capital_recovery_factor, annualized_capital_cost fields to separate channels.
    """

    name: str = "AnnualizedFinancialCalcModule"
    version: str = "v0.1"

    def validate_and_fill_default(
        self, total_capex: float, discount_rate: float, plant_lifetime: float    ) -> AnnualizedFinancialCalcInput:
        """Validate inputs and fill defaults.

        Args:
            total_capex: total_capex input
            discount_rate: discount_rate input
            plant_lifetime: plant_lifetime input

        Returns:
            Validated input model
        """
        return AnnualizedFinancialCalcInput(total_capex=total_capex, discount_rate=discount_rate, plant_lifetime=plant_lifetime)

    def run(
        self, total_capex: float, discount_rate: float, plant_lifetime: float    ) -> ModuleResult[AnnualizedFinancialCalcOutput]:
        """Execute calculation.

        Args:
            total_capex: total_capex input
            discount_rate: discount_rate input
            plant_lifetime: plant_lifetime input

        Returns:
            Module result with AnnualizedFinancialCalcOutput (capital_recovery_factor, annualized_capital_cost)
        """
        # Validate inputs
        validated_inputs = self.validate_and_fill_default(total_capex, discount_rate, plant_lifetime)

        # Import handwritten implementation
        from solar_battery_tea.handwritten.solarbatterylibrary.annualizedfinancialcalc_impl import (
            run_annualizedfinancialcalc,
        )

        # Execute implementation - returns tuple of values
        capital_recovery_factor, annualized_capital_cost = run_annualizedfinancialcalc(validated_inputs)


        # Return MultiOutput container (TEAx auto-extracts to channels)
        # MultiOutput fields use plain float (not RootModel[float])
        return ModuleResult(
            data=AnnualizedFinancialCalcOutput(
                capital_recovery_factor=capital_recovery_factor,
                annualized_capital_cost=annualized_capital_cost,
            )
        )
