"""IFE_Present_Value_FactorsModule Module Wrapper

TEAx module for IFE_Present_Value_Factors calculation.

Continuous closed-form factors for existing Hawker streams.
Integer construction payments occur in years 1 through Yc; operation
payments and energy occur in years Yc+1 through Yc+Nop. Real durations
retain the same algebraic extension, with exact-zero factors Yc and Nop.
A(n,d) = -expm1(-n*log1p(d))/d; A(n,0)=n.
Construction = A(Yc,d); operation = exp(-Yc*log1p(d))*A(Nop,d).
Rate dimensionless; durations and factors in years.
Native typed manual completion supplies stable transcendental evaluation.
*Source**: knowledge/sources/a_simplified_economic_model_for_inertial_fusion/output.md
*Ref**: Eq. 2.1 and construction/operation definition following Eq. 2.1
*Reference**: knowledge/sources/a_simplified_economic_model_for_inertial_fusion/output.md:141-148
*Basis**: [DERIVED] Algebraically identical geometric streams and finite zero limit;
work/active/WI-049_ife-zero-discount-repair/design.md, Evaluation and numerical argument.
*Last Updated**: 2026-09-11

Inputs:
    - construction_years_in: construction_years_in parameter
    - discount_rate_in: discount_rate_in parameter
    - operational_years_in: operational_years_in parameter

Outputs:
    - operation_factor: operation_factor result
    - construction_factor: construction_factor result

SysML Source: root-0/analyses/ife_lcoe.sysml:126

SysML Source: root-0/analyses/ife_lcoe.sysml:126

GAP: Code generator does NOT implement calc logic - only wrapper structure.
Handwritten implementation required in handwritten/ife_lcoe/ife_present_value_factors_impl.py
"""

from pydantic import BaseModel, Field, RootModel
from simkit.core.base import ModuleBase, ModuleResult

from ife_tea.primitives import Float
from ife_tea.schemas.ife_present_value_factors_output import IFE_Present_Value_FactorsOutput


class IFE_Present_Value_FactorsInput(BaseModel):
    """Input model for IFE_Present_Value_FactorsModule.

    Attributes:
        construction_years_in: construction_years_in input
        discount_rate_in: discount_rate_in input
        operational_years_in: operational_years_in input
    """
    construction_years_in: float = Field(..., description="construction_years_in input")
    discount_rate_in: float = Field(..., description="discount_rate_in input")
    operational_years_in: float = Field(..., description="operational_years_in input")


class IFE_Present_Value_FactorsModule(ModuleBase[IFE_Present_Value_FactorsInput, IFE_Present_Value_FactorsOutput]):
    """TEAx module for IFE_Present_Value_Factors calculation.

Continuous closed-form factors for existing Hawker streams.
Integer construction payments occur in years 1 through Yc; operation
payments and energy occur in years Yc+1 through Yc+Nop. Real durations
retain the same algebraic extension, with exact-zero factors Yc and Nop.
A(n,d) = -expm1(-n*log1p(d))/d; A(n,0)=n.
Construction = A(Yc,d); operation = exp(-Yc*log1p(d))*A(Nop,d).
Rate dimensionless; durations and factors in years.
Native typed manual completion supplies stable transcendental evaluation.
*Source**: knowledge/sources/a_simplified_economic_model_for_inertial_fusion/output.md
*Ref**: Eq. 2.1 and construction/operation definition following Eq. 2.1
*Reference**: knowledge/sources/a_simplified_economic_model_for_inertial_fusion/output.md:141-148
*Basis**: [DERIVED] Algebraically identical geometric streams and finite zero limit;
work/active/WI-049_ife-zero-discount-repair/design.md, Evaluation and numerical argument.
*Last Updated**: 2026-09-11

Inputs:
    - construction_years_in: construction_years_in parameter
    - discount_rate_in: discount_rate_in parameter
    - operational_years_in: operational_years_in parameter

Outputs:
    - operation_factor: operation_factor result
    - construction_factor: construction_factor result

SysML Source: root-0/analyses/ife_lcoe.sysml:126

    SysML Source: root-0/analyses/ife_lcoe.sysml:126

    Calculation Specification:
        See documentation:
Continuous closed-form factors for existing Hawker streams.
Integer construction payments occur in years 1 through Yc; operation
payments and energy occur in years Yc+1 through Yc+Nop. Real durations
retain the same algebraic extension, with exact-zero factors Yc and Nop.
A(n,d) = -expm1(-n*log1p(d))/d; A(n,0)=n.
Construction = A(Yc,d); operation = exp(-Yc*log1p(d))*A(Nop,d).
Rate dimensionless; durations and factors in years.
Native typed manual completion supplies stable transcendental evaluation.
*Source**: knowledge/sources/a_simplified_economic_model_for_inertial_fusion/output.md
*Ref**: Eq. 2.1 and construction/operation definition following Eq. 2.1
*Reference**: knowledge/sources/a_simplified_economic_model_for_inertial_fusion/output.md:141-148
*Basis**: [DERIVED] Algebraically identical geometric streams and finite zero limit;
work/active/WI-049_ife-zero-discount-repair/design.md, Evaluation and numerical argument.
*Last Updated**: 2026-09-11

    IMPLEMENTATION: See ife_tea.handwritten.ife_lcoe.ife_present_value_factors_impl
    for manual implementation.

    NOTE: Uses MultiOutput pattern for type-safe multi-output support.
    TEAx automatically extracts operation_factor, construction_factor fields to separate channels.
    """

    name: str = "IFE_Present_Value_FactorsModule"
    version: str = "v0.1"

    def validate_and_fill_default(
        self, construction_years_in: float, discount_rate_in: float, operational_years_in: float    ) -> IFE_Present_Value_FactorsInput:
        """Validate inputs and fill defaults.

        Args:
            construction_years_in: construction_years_in input
            discount_rate_in: discount_rate_in input
            operational_years_in: operational_years_in input

        Returns:
            Validated input model
        """
        return IFE_Present_Value_FactorsInput(construction_years_in=construction_years_in, discount_rate_in=discount_rate_in, operational_years_in=operational_years_in)

    def run(
        self, construction_years_in: float, discount_rate_in: float, operational_years_in: float    ) -> ModuleResult[IFE_Present_Value_FactorsOutput]:
        """Execute calculation.

        Args:
            construction_years_in: construction_years_in input
            discount_rate_in: discount_rate_in input
            operational_years_in: operational_years_in input

        Returns:
            Module result with IFE_Present_Value_FactorsOutput (operation_factor, construction_factor)
        """
        # Validate inputs
        validated_inputs = self.validate_and_fill_default(construction_years_in, discount_rate_in, operational_years_in)

        # Import handwritten implementation
        from ife_tea.handwritten.ife_lcoe.ife_present_value_factors_impl import (
            run_ife_present_value_factors,
        )

        # Execute implementation - returns tuple of values
        operation_factor, construction_factor = run_ife_present_value_factors(validated_inputs)


        # Return MultiOutput container (TEAx auto-extracts to channels)
        # MultiOutput fields use plain float (not RootModel[float])
        return ModuleResult(
            data=IFE_Present_Value_FactorsOutput(
                operation_factor=operation_factor,
                construction_factor=construction_factor,
            )
        )
