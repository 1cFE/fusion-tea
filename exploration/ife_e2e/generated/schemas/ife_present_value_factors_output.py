from pydantic import Field
from simkit.config.schema import MultiOutput

class IFE_Present_Value_FactorsOutput(MultiOutput):
    """Multi-output container for IFE_Present_Value_Factors.

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

SysML Source: root-0/analyses/ife_lcoe.sysml:126
    """
    operation_factor: float = Field(description="operation_factor output")
    construction_factor: float = Field(description="construction_factor output")
