"""Generating_Electricity_PriceModule Module Wrapper

TEAx module for Generating_Electricity_Price calculation.

Guard only the final price division, using actual net power in W.
If net_power > 0, price = numerator / denominator and generating = 1.
Otherwise price = 0 and generating = 0. Zero price is an invalid sentinel.
Consumers must require generating = 1 and satisfied net_positive before ranking.
The numerator and denominator retain the bound channel's units: Hawker
discounted dollars/MWh or Meier annualized billion dollars/scaled energy
giving 1988 cents/kWh. generating is a dimensionless Real restricted to 0/1.
Implemented by the native handwritten completion because the pinned
arithmetic renderer does not support this conditional. No finance is duplicated.

*Source**: knowledge/sources/a_simplified_economic_model_for_inertial_fusion/output.md,
knowledge/sources/economic_studies_for_heavy_ion_fusion_electric_power_plants/output.md
*Reference**: Hawker Eq. 2.1 and Eqs. 2.12-2.16; Meier Eq. 1
*Basis**: [DERIVED] A generating price requires strictly positive net output.
*Last Updated**: 2026-09-10

Inputs:
    - net_power: net_power parameter
    - numerator: numerator parameter
    - denominator: denominator parameter

Outputs:
    - price: price result
    - generating: generating result

SysML Source: root-0/analyses/ife_lcoe.sysml:141

SysML Source: root-0/analyses/ife_lcoe.sysml:141

GAP: Code generator does NOT implement calc logic - only wrapper structure.
Handwritten implementation required in handwritten/ife_lcoe/generating_electricity_price_impl.py
"""

from pydantic import BaseModel, Field, RootModel
from simkit.core.base import ModuleBase, ModuleResult

from ife_tea.primitives import Float
from ife_tea.schemas.generating_electricity_price_output import Generating_Electricity_PriceOutput


class Generating_Electricity_PriceInput(BaseModel):
    """Input model for Generating_Electricity_PriceModule.

    Attributes:
        net_power: net_power input
        numerator: numerator input
        denominator: denominator input
    """
    net_power: float = Field(..., description="net_power input")
    numerator: float = Field(..., description="numerator input")
    denominator: float = Field(..., description="denominator input")


class Generating_Electricity_PriceModule(ModuleBase[Generating_Electricity_PriceInput, Generating_Electricity_PriceOutput]):
    """TEAx module for Generating_Electricity_Price calculation.

Guard only the final price division, using actual net power in W.
If net_power > 0, price = numerator / denominator and generating = 1.
Otherwise price = 0 and generating = 0. Zero price is an invalid sentinel.
Consumers must require generating = 1 and satisfied net_positive before ranking.
The numerator and denominator retain the bound channel's units: Hawker
discounted dollars/MWh or Meier annualized billion dollars/scaled energy
giving 1988 cents/kWh. generating is a dimensionless Real restricted to 0/1.
Implemented by the native handwritten completion because the pinned
arithmetic renderer does not support this conditional. No finance is duplicated.

*Source**: knowledge/sources/a_simplified_economic_model_for_inertial_fusion/output.md,
knowledge/sources/economic_studies_for_heavy_ion_fusion_electric_power_plants/output.md
*Reference**: Hawker Eq. 2.1 and Eqs. 2.12-2.16; Meier Eq. 1
*Basis**: [DERIVED] A generating price requires strictly positive net output.
*Last Updated**: 2026-09-10

Inputs:
    - net_power: net_power parameter
    - numerator: numerator parameter
    - denominator: denominator parameter

Outputs:
    - price: price result
    - generating: generating result

SysML Source: root-0/analyses/ife_lcoe.sysml:141

    SysML Source: root-0/analyses/ife_lcoe.sysml:141

    Calculation Specification:
        See documentation:
Guard only the final price division, using actual net power in W.
If net_power > 0, price = numerator / denominator and generating = 1.
Otherwise price = 0 and generating = 0. Zero price is an invalid sentinel.
Consumers must require generating = 1 and satisfied net_positive before ranking.
The numerator and denominator retain the bound channel's units: Hawker
discounted dollars/MWh or Meier annualized billion dollars/scaled energy
giving 1988 cents/kWh. generating is a dimensionless Real restricted to 0/1.
Implemented by the native handwritten completion because the pinned
arithmetic renderer does not support this conditional. No finance is duplicated.

*Source**: knowledge/sources/a_simplified_economic_model_for_inertial_fusion/output.md,
knowledge/sources/economic_studies_for_heavy_ion_fusion_electric_power_plants/output.md
*Reference**: Hawker Eq. 2.1 and Eqs. 2.12-2.16; Meier Eq. 1
*Basis**: [DERIVED] A generating price requires strictly positive net output.
*Last Updated**: 2026-09-10

    IMPLEMENTATION: See ife_tea.handwritten.ife_lcoe.generating_electricity_price_impl
    for manual implementation.

    NOTE: Uses MultiOutput pattern for type-safe multi-output support.
    TEAx automatically extracts price, generating fields to separate channels.
    """

    name: str = "Generating_Electricity_PriceModule"
    version: str = "v0.1"

    def validate_and_fill_default(
        self, net_power: float, numerator: float, denominator: float    ) -> Generating_Electricity_PriceInput:
        """Validate inputs and fill defaults.

        Args:
            net_power: net_power input
            numerator: numerator input
            denominator: denominator input

        Returns:
            Validated input model
        """
        return Generating_Electricity_PriceInput(net_power=net_power, numerator=numerator, denominator=denominator)

    def run(
        self, net_power: float, numerator: float, denominator: float    ) -> ModuleResult[Generating_Electricity_PriceOutput]:
        """Execute calculation.

        Args:
            net_power: net_power input
            numerator: numerator input
            denominator: denominator input

        Returns:
            Module result with Generating_Electricity_PriceOutput (price, generating)
        """
        # Validate inputs
        validated_inputs = self.validate_and_fill_default(net_power, numerator, denominator)

        # Import handwritten implementation
        from ife_tea.handwritten.ife_lcoe.generating_electricity_price_impl import (
            run_generating_electricity_price,
        )

        # Execute implementation - returns tuple of values
        price, generating = run_generating_electricity_price(validated_inputs)


        # Return MultiOutput container (TEAx auto-extracts to channels)
        # MultiOutput fields use plain float (not RootModel[float])
        return ModuleResult(
            data=Generating_Electricity_PriceOutput(
                price=price,
                generating=generating,
            )
        )
